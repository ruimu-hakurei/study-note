# GPIO 与 EXTI 外部中断

> GPIO 初始化、电平读写、AFIO 复用、EXTI 外部中断配置

---

## 底层

### GPIO 工作原理

每个 GPIO 引脚内部结构：

```
输出模式：CPU写ODR → 输出控制 → 推挽/开漏驱动 → I/O引脚
输入模式：I/O引脚 → TTL施密特触发器 → IDR寄存器 → CPU读取
```

- **ODR**（Output Data Register）：输出数据寄存器，写什么电平就输出什么
- **IDR**（Input Data Register）：输入数据寄存器，读取引脚实际电平
- **推挽输出**：高低电平都能主动驱动，点亮LED、驱动MOS管
- **开漏输出**：只能拉低不能拉高，需要外部上拉电阻，适合 I2C、多设备共享总线
- **浮空输入**：引脚悬空时电平不确定，必须外接确定电平
- **上拉/下拉输入**：内部弱电阻固定默认电平，适合按键检测

### EXTI 外部中断原理

EXTI（External Interrupt）可以检测 GPIO 引脚的边沿信号并触发中断：

```
GPIO引脚 → AFIO（选择中断引脚）→ EXTI边沿检测 → NVIC → CPU中断响应
```

- 每个 GPIO 口（A/B/C...）的同一序号 Pin 只能选一个接入 EXTI（如 PA0/PB0/PC0 只能三选一）
- EXTI0~4：各自独立中断通道
- EXTI5~9：共用一个中断通道 EXTI9_5_IRQHandler
- **EXTI10~15：共用一个中断通道 EXTI15_10_IRQHandler**（最常用）
- 多个通道共用时需要在 ISR 里逐个判断标志位

### EXTI 中断深度解析

#### 1. 从引脚边沿到 CPU 的完整路径

以 PB14 下降沿为例：

```
PB14 电平 1→0
    │
    ▼
AFIO_EXTICR 选择“EXTI14 观察 PB14”
    │
    ▼
FTSR14 下降沿检测器命中
    │
    ▼
PR14 Pending 位置 1
    │  IMR14 是否放行中断请求？
    ▼
NVIC 的 EXTI15_10_IRQn Pending
    │  NVIC 已使能且优先级允许？
    ▼
CPU 执行 EXTI15_10_IRQHandler()
```

EXTI 相关寄存器可以按“选择、检测、放行、记录”来记：

| 模块/寄存器 | 作用 |
|---|---|
| `AFIO_EXTICR` | 给 EXTI0~15 选择对应的 GPIO 端口 A/B/C... |
| `RTSR` | 允许上升沿触发 |
| `FTSR` | 允许下降沿触发；两者可同时开启形成双边沿 |
| `IMR` | Interrupt Mask，是否把该 Line 送往 NVIC |
| `EMR` | Event Mask，只产生事件，不进入普通 ISR，可用于唤醒/外设联动 |
| `PR` | Pending Register，记录已经发生的边沿；**写 1 清除** |
| `SWIER` | 软件触发，用于测试或软件制造 EXTI 请求 |

> ✅ GPIO 电平恢复以后，Pending 位仍会保留，直到软件清除。因此 ISR 判断的是“是否发生过边沿”，不是当前引脚是否仍保持触发电平。

#### 2. Line 与 IRQHandler 不是一一对应

| EXTI Line | NVIC 通道 / ISR |
|---|---|
| Line0 | `EXTI0_IRQn` / `EXTI0_IRQHandler` |
| Line1 | `EXTI1_IRQn` / `EXTI1_IRQHandler` |
| Line2 | `EXTI2_IRQn` / `EXTI2_IRQHandler` |
| Line3 | `EXTI3_IRQn` / `EXTI3_IRQHandler` |
| Line4 | `EXTI4_IRQn` / `EXTI4_IRQHandler` |
| Line5~9 | `EXTI9_5_IRQn` / `EXTI9_5_IRQHandler` |
| Line10~15 | `EXTI15_10_IRQn` / `EXTI15_10_IRQHandler` |

共享入口中必须使用多个独立 `if`，不能想当然写成 `else if`：Line10 和 Line14 可能在 CPU 进入 ISR 前都已经 Pending，需要一次全部处理。

```c
void EXTI15_10_IRQHandler(void)
{
    if (EXTI_GetITStatus(EXTI_Line10) != RESET)
    {
        EXTI_ClearITPendingBit(EXTI_Line10); // 写1清除，先解除本次请求
        SensorA_Event = 1;                   // 只发布事件
    }

    if (EXTI_GetITStatus(EXTI_Line14) != RESET)
    {
        EXTI_ClearITPendingBit(EXTI_Line14);
        Key_Event = 1;
    }
}
```

#### 3. 配置顺序

1. 开启 GPIO 和 AFIO 时钟。
2. GPIO 配成浮空/上拉/下拉输入，保证空闲电平明确。
3. `GPIO_EXTILineConfig()` 选择某条 Line 来自哪个端口。
4. 配置上升沿、下降沿或双边沿，并开启 EXTI Line。
5. 清除初始化期间可能遗留的 Pending 位。
6. 配置并使能正确的 NVIC 通道。
7. 最后再允许外部信号工作，避免半初始化状态误触发。

```c
/* PB14：上拉输入，按下接地，下降沿触发 */
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB |
                       RCC_APB2Periph_AFIO, ENABLE);

GPIO_InitTypeDef gpio;
gpio.GPIO_Pin = GPIO_Pin_14;
gpio.GPIO_Mode = GPIO_Mode_IPU;
gpio.GPIO_Speed = GPIO_Speed_50MHz;
GPIO_Init(GPIOB, &gpio);

GPIO_EXTILineConfig(GPIO_PortSourceGPIOB, GPIO_PinSource14);

EXTI_InitTypeDef exti;
exti.EXTI_Line = EXTI_Line14;
exti.EXTI_Mode = EXTI_Mode_Interrupt;
exti.EXTI_Trigger = EXTI_Trigger_Falling;
exti.EXTI_LineCmd = ENABLE;
EXTI_Init(&exti);
EXTI_ClearITPendingBit(EXTI_Line14);

NVIC_InitTypeDef nvic;
nvic.NVIC_IRQChannel = EXTI15_10_IRQn;
nvic.NVIC_IRQChannelPreemptionPriority = 2;
nvic.NVIC_IRQChannelSubPriority = 0;
nvic.NVIC_IRQChannelCmd = ENABLE;
NVIC_Init(&nvic);
```

#### 4. 按键消抖不能在 ISR 里阻塞

机械按键一次按下可能在几毫秒内产生多个边沿：

```text
理想：──────┐________________
实际：──────┐_┌─┐__┌────────  ← 抖动造成多次 EXTI
```

在 ISR 中 `Delay_ms(20)` 或 `HAL_Delay(20)` 会长时间占住 CPU；低优先级中断无法执行，同级中断只能等待，高优先级中断虽可抢占但会让时序更复杂。推荐两种非阻塞方案：

- ISR 只记录边沿时间，20 ms 内的重复边沿丢弃。
- ISR 暂时屏蔽该 EXTI Line，由 1 ms 定时任务确认稳定电平后再恢复。

下面的 `Timer_Millis()` 由自由运行的 1 ms 时基提供，写法见 [[05-定时器#5. 1 ms 中断应该做时基，不要做全部业务|1 ms 非阻塞时基]]。

```c
volatile uint8_t Key_Event;
static volatile uint32_t Key_LastIrqMs;

void EXTI15_10_IRQHandler(void)
{
    if (EXTI_GetITStatus(EXTI_Line14) != RESET)
    {
        uint32_t now = Timer_Millis();      // 只读取自由运行的毫秒计数，不延时
        EXTI_ClearITPendingBit(EXTI_Line14);

        /* 无符号减法即使毫秒计数回绕，也能正确计算短时间差。 */
        if ((uint32_t)(now - Key_LastIrqMs) >= 20U)
        {
            Key_LastIrqMs = now;
            Key_Event = 1;                  // 主循环再读取引脚并执行按键动作
        }
    }
}
```

#### 5. 什么时候不该用 EXTI

| 需求 | 更合适的方案 |
|---|---|
| 低速按键/报警引脚/数据就绪 | EXTI |
| 高频脉冲精确计数 | TIM 外部时钟或输入捕获 |
| 正交编码器高速计数 | [[05-定时器#编码器接口|TIM 编码器接口]] |
| 固定周期采样 | TIM 触发 ADC，而不是 GPIO 软件翻转 |

EXTI 让 CPU 对每个边沿都执行一次 ISR；频率升高后，中断开销和丢边沿风险都会增加。定时器硬件可以在 CPU 不介入的情况下先计数或锁存时间戳。

### 旋转编码器原理

- A、B 两相输出，相位差 90°
- 正转：A 超前 B 90°，**B 下降沿时 A = 低电平**
- 反转：B 超前 A 90°，**A 下降沿时 B = 低电平**
- 通过检测一个相的下降沿时另一个相的电平来判断方向

---

## 应用

| 场景 | 配置 |
|------|------|
| LED 控制 | 推挽输出，高电平点亮 |
| 按键检测 | 上拉输入，按下为低电平；配合 EXTI 下降沿中断 |
| 旋转编码器 | 上拉输入 + EXTI 双下降沿中断，读另一相电平判方向 |
| 传感器数字量 | 浮空输入或上拉输入，轮询或中断读取 |
| I2C/SPI 复用引脚 | AF 复用推挽/开漏输出 |

---

## 代码

### GPIO 初始化

> **前置依赖**：[[01-时钟系统#代码|开启 GPIO 时钟]]

```c
/* GPIO初始化 */
GPIO_InitTypeDef GPIO_InitStructure;

GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;       // 推挽输出
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_13;             // 多Pin用 | 连接，如 GPIO_Pin_0 | GPIO_Pin_1
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
GPIO_Init(GPIOC, &GPIO_InitStructure);
```

**模式速查表：**

| 模式宏 | 含义 | 用途 |
|--------|------|------|
| `GPIO_Mode_AIN` | 模拟输入 | ADC 采样 |
| `GPIO_Mode_IN_FLOATING` | 浮空输入 | 外部信号确定电平 |
| `GPIO_Mode_IPD` | 下拉输入 | 默认低电平 |
| `GPIO_Mode_IPU` | 上拉输入 | 默认高电平（按键检测首选） |
| `GPIO_Mode_Out_OD` | 开漏输出 | I2C、线与 |
| `GPIO_Mode_Out_PP` | 推挽输出 | LED、MOS 管 |
| `GPIO_Mode_AF_OD` | 复用开漏 | 外设控制，开漏 |
| `GPIO_Mode_AF_PP` | 复用推挽 | 外设控制，推挽（USART/SPI等） |

---

### 电平读写

> **前置依赖**：GPIO 初始化

```c
/* ----- 改变电平 ----- */
GPIO_SetBits(GPIOC, GPIO_Pin_13);                      // 置高
GPIO_ResetBits(GPIOC, GPIO_Pin_13);                    // 置低
GPIO_WriteBit(GPIOA, GPIO_Pin_0, Bit_RESET);           // 写单个位（Bit_SET/Bit_RESET）
GPIO_Write(GPIOA, ~0x0001);                            // 写整个端口，~取反，16位对应PA0~PA15

/* ----- 检测电平 ----- */
if (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_11) == 0)    // 读输入电平（IDR）
if (GPIO_ReadOutputDataBit(GPIOA, GPIO_Pin_2) == 0)    // 读输出电平（ODR）

/* ----- 电平翻转函数 ----- */
void xx_Turn(void)
{
    if (GPIO_ReadOutputDataBit(GPIOA, GPIO_Pin_2) == 0)
        GPIO_SetBits(GPIOA, GPIO_Pin_2);
    else
        GPIO_ResetBits(GPIOA, GPIO_Pin_2);
}
```

---

### 按键获取键码（消抖 + 阻塞式）

```c
/*
 * 按键获取键码 1~N，不按返回 0
 * 包含：按下消抖(20ms) → 等待松手 → 松开消抖(20ms)
 * 注意：按住不放时会阻塞，直到松手
 */
uint8_t Key_GetNum(void)
{
    uint8_t KeyNum = 0;

    if (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_1) == 0)
    {
        Delay_ms(20);                                   // 按下消抖
        while (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_1) == 0);  // 等待松手
        Delay_ms(20);                                   // 松开消抖
        KeyNum = 1;
    }
    if (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_11) == 0)
    {
        Delay_ms(20);
        while (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_11) == 0);
        Delay_ms(20);
        KeyNum = 2;
    }
    return KeyNum;
}

// main.c 中这样调用（拿到一次键码后 KeyNum 保持，直到下次读取清零）：
uint8_t KeyNum;
KeyNum = Key_GetNum();
```

---

### AFIO 选择中断引脚 + EXTI 初始化

> **前置依赖**：[[01-时钟系统#代码|开启 AFIO 时钟]]、GPIO 初始化（输入模式）

```c
/* 1. AFIO 选择中断引脚 — 每个Pin只能对应一个GPIOx，不能用 | 连接多个 */
GPIO_EXTILineConfig(GPIO_PortSourceGPIOB, GPIO_PinSource14);  // 选择 PB14 接入 EXTI14

/* 2. EXTI 初始化 */
EXTI_InitTypeDef EXTI_InitStructure;
EXTI_InitStructure.EXTI_Line = EXTI_Line14;    // 这里的 Line 就是上面 AFIO 的 PinSource
EXTI_InitStructure.EXTI_LineCmd = ENABLE;
EXTI_InitStructure.EXTI_Mode = EXTI_Mode_Interrupt;
EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Falling;  // 下降沿触发
EXTI_Init(&EXTI_InitStructure);
```

---

### EXTI 中断函数

> **前置依赖**：EXTI 初始化、[[03-中断NVIC|NVIC 配置]]

**按键事件版本（非阻塞消抖）：**
```c
volatile uint8_t Key_Event;
static volatile uint32_t Key_LastIrqMs;

void EXTI15_10_IRQHandler(void)
{
    if (EXTI_GetITStatus(EXTI_Line14) == SET)           // 判断是哪条 Line
    {
        uint32_t now = Timer_Millis();
        EXTI_ClearITPendingBit(EXTI_Line14);            // 先清本次 Pending

        if ((uint32_t)(now - Key_LastIrqMs) >= 20U)     // 时间窗消抖，不在 ISR 延时
        {
            Key_LastIrqMs = now;
            Key_Event = 1;                              // 主循环处理按键动作
        }
    }
}
```

**不需要消抖的版本：**
```c
void EXTI0_IRQHandler(void)
{
    if (EXTI_GetITStatus(EXTI_Line0) == SET)
    {
        xx_Count++;
        EXTI_ClearITPendingBit(EXTI_Line0);
    }
}
```

**旋转编码器版本（A→Line0, B→Line1，上拉输入）：**
```c
/*
 * 正转（顺时针）：B下降沿时A为低 → Count++
 * 反转（逆时针）：A下降沿时B为低 → Count--
 */
void EXTI0_IRQHandler(void)     // A相
{
    if (EXTI_GetITStatus(EXTI_Line0) == SET)
    {
        if (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_1) == 0)  // B相为低 → 反转
            Encoder_Count--;
        EXTI_ClearITPendingBit(EXTI_Line0);
    }
}

void EXTI1_IRQHandler(void)     // B相
{
    if (EXTI_GetITStatus(EXTI_Line1) == SET)
    {
        if (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_0) == 0)  // A相为低 → 正转
            Encoder_Count++;
        EXTI_ClearITPendingBit(EXTI_Line1);
    }
}
```

---

### AFIO 重映射引脚

> **前置依赖**：[[01-时钟系统#代码|开启 AFIO 时钟]]

```c
/* PA15、PB3、PB4 默认是 JTAG 调试口，重映射前需要先解除调试复用 */
GPIO_PinRemapConfig(GPIO_Remap_SWJ_JTAGDisable, ENABLE);  // 关闭JTAG，保留SWD

/* TIM2 部分重映射 */
GPIO_PinRemapConfig(GPIO_PartialRemap1_TIM2, ENABLE);
```

---

## HAL 库对照

### GPIO 电平操作

```c
HAL_GPIO_WritePin(GPIOA, GPIO_PIN_3, GPIO_PIN_SET);   // 置高
HAL_GPIO_WritePin(GPIOA, GPIO_PIN_3, GPIO_PIN_RESET); // 置低
HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_3);                // 翻转（相当于Turn函数）
HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_3);                  // 读电平（HAL删了读ODR，IDR可反映输出）
```

### EXTI 中断回调（不同 IRQHandler 汇入同一用户回调）

```c
// 非阻塞消抖版本
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if (GPIO_Pin == CountSensor_Pin)
    {
        static uint32_t last_ms;
        uint32_t now = HAL_GetTick();

        if ((uint32_t)(now - last_ms) >= 20U)
        {
            last_ms = now;
            CountSensor_Count++;
        }
    }
}

// 旋转编码器版本
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if (GPIO_Pin == Encoder_A_Pin)
    {
        if (HAL_GPIO_ReadPin(GPIOB, Encoder_B_Pin) == GPIO_PIN_RESET)
            Encoder_Count--;
    }
    else if (GPIO_Pin == Encoder_B_Pin)
    {
        if (HAL_GPIO_ReadPin(GPIOB, Encoder_A_Pin) == GPIO_PIN_RESET)
            Encoder_Count++;
    }
}
```

### 电平翻转

```c
void LED_Turn(void)
{
    if (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_3) == 0)
        HAL_GPIO_WritePin(GPIOA, GPIO_PIN_3, GPIO_PIN_SET);
    else
        HAL_GPIO_WritePin(GPIOA, GPIO_PIN_3, GPIO_PIN_RESET);
}
```

### 按键获取键码

```c
uint8_t Key_GetNum(void)
{
    uint8_t KeyNum = 0;
    if (HAL_GPIO_ReadPin(GPIOB, Key_1_Pin) == 0)
    {
        HAL_Delay(20);
        while (HAL_GPIO_ReadPin(GPIOB, Key_1_Pin) == 0);
        HAL_Delay(20);
        KeyNum = 1;
    }
    if (HAL_GPIO_ReadPin(GPIOB, Key_2_Pin) == 0)
    {
        HAL_Delay(20);
        while (HAL_GPIO_ReadPin(GPIOB, Key_2_Pin) == 0);
        HAL_Delay(20);
        KeyNum = 2;
    }
    return KeyNum;
}
```

> **注意**：HAL 库中 GPIO 初始化、AFIO、EXTI 配置均在 CubeMX 中图形化完成，不需要手写 Init 代码。

CubeMX 生成的真正入口仍然按 Line 分组，例如：

```c
void EXTI15_10_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(CountSensor_Pin); // HAL 清 Pending 后调用用户回调
}
```

若同一共享入口启用了多个 Pin，IRQHandler 中应分别调用 `HAL_GPIO_EXTI_IRQHandler()`，用户回调再用 `GPIO_Pin` 区分来源。

---

## 相关笔记

- [[01-时钟系统]]
- [[03-中断NVIC]]
- [[05-定时器]]（编码器接口模式 vs EXTI 旋转编码器方案）
- [[03-中断NVIC#一次中断到底怎样发生|中断公共链路]]
