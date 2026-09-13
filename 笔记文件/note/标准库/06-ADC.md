# ADC 模数转换

> ADC 初始化、校准、软件触发读取、DMA 连续采集

---

## 底层

### ADC 工作流程

STM32F103 的 ADC 是 12 位逐次逼近型，工作流程：

```
模拟输入 → 采样保持 → 逐次比较 → 12位数字量存入DR寄存器
```

**关键参数：**
- **分辨率**：12 位（0~4095）
- **参考电压**：通常 VREF+ = 3.3V，VREF- = GND
- **近似换算**：`Vin ≈ 读数值 / 4095 × VREF+`；精确测量应使用实测参考电压并校准增益/偏置

**时钟限制：**
- ADC 挂在 APB2 上（最高 72MHz），但 ADC 自身最高只支持 **14MHz**
- 所以必须对 PCLK2 分频：72MHz 只能用 **6 分频(12MHz)** 或 **8 分频(9MHz)**

### 转换模式

| 模式 | 连续转换 | 扫描模式 | 效果 |
|------|---------|---------|------|
| 单次单通道 | DISABLE | DISABLE | 触发一次 → 读一个通道 → 停 |
| 单次多通道 | DISABLE | ENABLE | 触发一次 → 按序列读完所有通道 → 停 |
| 连续单通道 | ENABLE | DISABLE | 触发一次 → 反复读一个通道 |
| 连续多通道 | ENABLE | ENABLE | 触发一次 → 反复按序列读所有通道 |

> - **连续模式**：读完一次自动开始下一次
> - **扫描模式**：按规则组通道序列依次转换多个通道
> - ADC 只有一个 DR 寄存器，多通道扫描时必须配合 DMA 搬运数据，否则数据会被覆盖

### 规则组与注入组

- **规则组**：最多 16 个通道，常规使用，适合 DMA 循环采集
- **注入组**：最多 4 个通道，可打断规则组插队转换，适合紧急采样

### ADC 中断深度解析

#### 1. 从模拟电压到 EOC 中断

```
触发源（软件 / TIM / EXTI）
    │
    ▼
采样开关闭合，内部采样电容充电
    │  经过设定的采样周期
    ▼
SAR 逐次比较（12.5 个 ADC 周期）
    │
    ▼
12 位结果写入 DR，SR.EOC = 1
    │  CR1.EOCIE = 1？
    ▼
ADC1_2_IRQn → ADC1_2_IRQHandler()
    │
    ▼
读取 DR、保存结果、发布采样完成事件
```

单次 12 位转换的时间近似为：

```text
Tconv = (采样周期 + 12.5) / ADCCLK
```

例如 ADCCLK=12 MHz、采样时间 55.5 周期：`Tconv = 68 / 12MHz ≈ 5.67 μs`。中断频率若接近这个转换速率，CPU 会被大量 ISR 占用，此时应改用 DMA。

#### 2. 采样时间不只是“速度选项”

ADC 输入端内部存在采样保持电容。信号源通过自身输出电阻给它充电；传感器输出阻抗高、RC 滤波电阻大或通道切换频繁时，采样时间太短会导致电容尚未充到真实电压就开始转换，结果偏低或通道间串扰。

| 信号源 | 采样时间建议 |
|---|---|
| 运放缓冲、低阻信号 | 可使用较短采样时间 |
| 电位器、分压器、NTC 等较高阻源 | 加长采样时间 |
| 内部温度传感器/VREFINT | 按数据手册要求使用足够采样时间 |

> ✅ ADC 中断只能告诉你“转换完成”，不能弥补采样电容没有稳定。先保证模拟前端、参考电压和采样时间正确，再讨论 ISR。

#### 3. STM32F1 常用 ADC 中断源

| 中断 | 标志 | 含义 | 应用 |
|---|---|---|---|
| 规则组转换完成 | `EOC` | 一个规则通道结果已进入 DR | 低速单通道采样 |
| 注入组转换完成 | `JEOC` | 注入序列结果已进入 JDRx | 电机电流同步采样 |
| 模拟看门狗 | `AWD` | 转换值越过设定高/低阈值 | 电压、电流越界报警 |

STM32F103 的 ADC1 与 ADC2 共享 `ADC1_2_IRQn`。共享入口必须分别检查两个 ADC 的标志；不要因为本工程当前只开 ADC1，就把 ISR 写成无法扩展的无条件处理。

> F1 的规则组只有一个 DR。扫描多个通道时，EOC 会频繁出现，若软件/ISR 读取不及时，前一个通道结果会被后一个覆盖；连续多通道优先使用 DMA。

#### 4. 规则组 EOC 中断：低速“触发一次、完成通知”

初始化时增加：

```c
ADC_ITConfig(ADC1, ADC_IT_EOC, ENABLE);

NVIC_InitTypeDef nvic;
nvic.NVIC_IRQChannel = ADC1_2_IRQn;
nvic.NVIC_IRQChannelPreemptionPriority = 2;
nvic.NVIC_IRQChannelSubPriority = 1;
nvic.NVIC_IRQChannelCmd = ENABLE;
NVIC_Init(&nvic);
```

ISR 与主循环：

```c
volatile uint16_t AdcLatest;
volatile uint8_t AdcReady;

void ADC1_2_IRQHandler(void)
{
    if (ADC_GetITStatus(ADC1, ADC_IT_EOC) != RESET)
    {
        /* 先读取 DR，保存这次真正的转换结果。 */
        AdcLatest = ADC_GetConversionValue(ADC1);
        ADC_ClearITPendingBit(ADC1, ADC_IT_EOC);
        AdcReady = 1;
    }

    if (ADC_GetITStatus(ADC2, ADC_IT_EOC) != RESET)
    {
        Adc2Latest = ADC_GetConversionValue(ADC2);
        ADC_ClearITPendingBit(ADC2, ADC_IT_EOC);
        Adc2Ready = 1;
    }
}

int main(void)
{
    Hardware_Init();

    while (1)
    {
        if (NeedNewSample())
            ADC_SoftwareStartConvCmd(ADC1, ENABLE); // 只发起，不阻塞等待

        if (AdcReady != 0)
        {
            uint16_t sample = AdcLatest;
            AdcReady = 0;
            FilterAndDisplay(sample);               // 复杂处理放主循环
        }
    }
}
```

单个 `AdcReady` 表示“至少有一个新值”，不是队列。若 ISR 在主循环处理前完成多次转换，中间样本会被新值覆盖；需要保留每个样本时使用 DMA 缓冲区或软件队列。

#### 5. 模拟看门狗中断：硬件阈值监测

模拟看门狗直接比较 ADC 结果与高/低阈值，不需要 CPU 每次轮询：

```c
ADC_AnalogWatchdogThresholdsConfig(ADC1, 3500, 500);       // 高阈值、低阈值
ADC_AnalogWatchdogSingleChannelConfig(ADC1, ADC_Channel_0);
ADC_AnalogWatchdogCmd(ADC1, ADC_AnalogWatchdog_SingleRegEnable);
ADC_ITConfig(ADC1, ADC_IT_AWD, ENABLE);

volatile uint8_t AdcOutOfWindow;

void ADC1_2_IRQHandler(void)
{
    if (ADC_GetITStatus(ADC1, ADC_IT_AWD) != RESET)
    {
        ADC_ClearITPendingBit(ADC1, ADC_IT_AWD);
        AdcOutOfWindow = 1; // 主循环记录、告警、降功率
    }
}
```

对于电机过流等安全场景，ISR 可以立即关闭使能引脚作为第二层保护，但最快、最确定的关断应优先使用比较器连接高级定时器 BKIN 等硬件链路；软件中断延迟不是零。

#### 6. JEOC：定时器同步的注入采样

电机控制常要求在 PWM 中点采样，避开开关噪声。推荐链路：

```text
TIM1 PWM 比较/触发事件
    → ADC 注入组开始采样
        → JDR1/JDR2 写入
            → JEOC 中断
                → 快速读取电流值，更新控制算法输入
```

这比在定时器 ISR 中再调用软件触发更准，因为 TIM 到 ADC 的触发完全由硬件完成，不受 CPU 中断延迟影响。

```c
ADC_ITConfig(ADC1, ADC_IT_JEOC, ENABLE);

void ADC1_2_IRQHandler(void)
{
    if (ADC_GetITStatus(ADC1, ADC_IT_JEOC) != RESET)
    {
        PhaseCurrentA = ADC_GetInjectedConversionValue(
                            ADC1, ADC_InjectedChannel_1);
        PhaseCurrentB = ADC_GetInjectedConversionValue(
                            ADC1, ADC_InjectedChannel_2);
        ADC_ClearITPendingBit(ADC1, ADC_IT_JEOC);
        CurrentSampleReady = 1;
    }
}
```

FOC 等高频控制可能直接在 JEOC ISR 中执行固定时间、经过最坏耗时评估的控制计算；普通显示、日志和通信仍应移出高优先级 ISR。

> ⚠️ 上面的 EOC、AWD、JEOC 为了讲清楚分别展示了 ISR。若同一工程同时开启多个来源，只能保留一个 `ADC1_2_IRQHandler()`，并在其中用多个独立 `if` 检查全部标志；不能定义多个同名处理函数，也不要用 `else if` 漏掉同时 Pending 的来源。

#### 7. 中断、轮询与 DMA 怎样选

| 需求 | 推荐方式 |
|---|---|
| 偶尔读取电位器 | 软件触发 + 轮询，最简单 |
| 低速异步采样，不想阻塞 | EOC 中断 |
| 连续单/多通道波形 | TIM 触发 + DMA 循环/双缓冲 |
| PWM 固定相位电流采样 | TIM 硬件触发注入组 + JEOC |
| 只关心越界 | 模拟看门狗 AWD 中断 |

连续扫描时用“每次 EOC 都进中断”会让 CPU 承担逐样本搬运；DMA 正是为这种固定数据搬运设计的。

---

## 应用

| 场景 | 配置 |
|------|------|
| 读取电位器/传感器 | 单次非连续非扫描，软件触发 |
| 多通道传感器采集 | 连续扫描模式 + DMA 搬运 |
| 电流采样(FOC) | 注入组 + 定时器触发，精确时刻采样 |
| 电源电压监测 | 单通道连续转换 |

---

## 代码

### ADC 初始化 + 软件触发单次读取

> **前置依赖**：[[01-时钟系统#代码|开启 ADC 时钟 + ADC 分频]]、[[02-GPIO与EXTI|GPIO 初始化]]（通道引脚设为模拟输入）

```c
/* 1. ADC 分频 — 必须最先配置 */
RCC_ADCCLKConfig(RCC_PCLK2_Div6);  // 72/6 = 12MHz（只能选6或8分频）

/* 2. 配置规则组通道 */
ADC_RegularChannelConfig(ADC1, ADC_Channel_0, 1, ADC_SampleTime_55Cycles5);
// 参数：ADC编号 | 通道 | 序列号(1~16) | 采样时间

/* 3. ADC 初始化 */
ADC_InitTypeDef ADC_InitStructure;
ADC_InitStructure.ADC_Mode = ADC_Mode_Independent;          // 独立模式
ADC_InitStructure.ADC_DataAlign = ADC_DataAlign_Right;      // 右对齐
ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None; // 软件触发
ADC_InitStructure.ADC_ContinuousConvMode = DISABLE;         // 非连续（单次）
ADC_InitStructure.ADC_NbrOfChannel = 1;                     // 通道数
ADC_InitStructure.ADC_ScanConvMode = DISABLE;               // 非扫描
ADC_Init(ADC1, &ADC_InitStructure);

/* 4. 开启 ADC */
ADC_Cmd(ADC1, ENABLE);

/* 5. 校准 ADC */
ADC_ResetCalibration(ADC1);
while (ADC_GetResetCalibrationStatus(ADC1) == SET);
ADC_StartCalibration(ADC1);
while (ADC_GetCalibrationStatus(ADC1) == SET);
```

### 非连续非扫描读取函数

```c
/*
 * 软件触发，阻塞式读取一次 ADC 值
 * 如果需要连续触发，ADC_SoftwareStartConvCmd 放在 Init 最后
 */
uint16_t AD_GetValue(void)
{
    ADC_SoftwareStartConvCmd(ADC1, ENABLE);                      // 软件触发
    while (ADC_GetFlagStatus(ADC1, ADC_FLAG_EOC) == RESET);      // 等待转换完成
    return ADC_GetConversionValue(ADC1);                         // 读结果
}
```

### ADC + DMA 连续采集

> **前置依赖**：ADC 初始化（连续模式+扫描模式）、[[07-DMA|DMA 初始化]]

```c
/* ADC 配置改为连续+扫描 */
ADC_InitStructure.ADC_ContinuousConvMode = ENABLE;
ADC_InitStructure.ADC_ScanConvMode = ENABLE;

/* 触发 DMA */
ADC_DMACmd(ADC1, ENABLE);

/* 软件触发开始（如果连续模式，触发一次就够了，放 Init 最后） */
ADC_SoftwareStartConvCmd(ADC1, ENABLE);
// 之后 DMA 会自动把 DR 数据搬运到内存数组，无需 CPU 干预
```

> **注意事项**：
> - 连续模式 + 软件触发：触发一次后 DMA 循环搬运，永不停止
> - 转运 ADC1->DR 时，外设地址不自动递增
> - 转运目标（内存数组）需要递增

---

## HAL 库对照

### 校准

```c
HAL_ADCEx_Calibration_Start(&hadc1);
```

### 软件触发单次读取

```c
uint16_t AD_GetValue(void)
{
    uint16_t adcValue;
    HAL_ADC_Start(&hadc1);
    HAL_ADC_PollForConversion(&hadc1, HAL_MAX_DELAY);
    adcValue = HAL_ADC_GetValue(&hadc1);
    HAL_ADC_Stop(&hadc1);
    return adcValue;
}
```

### ADC + DMA

```c
HAL_ADC_Start_DMA(&hadc1, (uint32_t *)adcValue, 2);  // 通道数=2
```

### ADC 中断（HAL）

```c
volatile uint16_t AdcLatest;
volatile uint8_t AdcReady;

void ADC_StartOneSample(void)
{
    HAL_ADC_Start_IT(&hadc1);
}

void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *hadc)
{
    if (hadc->Instance == ADC1)
    {
        AdcLatest = (uint16_t)HAL_ADC_GetValue(hadc);
        AdcReady = 1;
        /* 非连续单次模式已经完成；下一次由任务再次 HAL_ADC_Start_IT。 */
    }
}

void HAL_ADC_LevelOutOfWindowCallback(ADC_HandleTypeDef *hadc)
{
    if (hadc->Instance == ADC1)
        AdcOutOfWindow = 1;
}
```

HAL 工程中真正的 `ADC1_2_IRQHandler()` 应调用 `HAL_ADC_IRQHandler(&hadc1)`，由 HAL 判断/清标志后进入上述回调。若 ADC2 也启用中断，共享入口还要调用对应的 `HAL_ADC_IRQHandler(&hadc2)`。

---

## 相关笔记

- [[01-时钟系统]]
- [[02-GPIO与EXTI]]
- [[07-DMA]]
- [[05-定时器]]（硬件触发 ADC、固定相位采样）
- [[03-中断NVIC#一次中断到底怎样发生|中断公共链路]]
