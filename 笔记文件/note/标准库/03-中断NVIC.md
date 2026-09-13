# 中断系统（NVIC）

> 从“外设事件发生”到“CPU 进入 ISR”的完整路径，以及 EXTI、USART、TIM、ADC 四类中断的共同规则。

---

## 底层

### NVIC 优先级分组

Cortex-M3 的 NVIC 使用 **4 位优先级寄存器**，分成抢占优先级和响应优先级两部分。分组方式整个工程只能设置一次：

| 分组 | 抢占优先级 | 响应优先级 | 适用场景 |
|------|-----------|-----------|----------|
| 分组0 | 0位，取值0 | 4位，取值0~15 | 所有中断平级，靠响应优先级排序 |
| 分组1 | 1位，取值0~1 | 3位，取值0~7 | 紧急/普通两级 |
| **分组2** | **2位，取值0~3** | **2位，取值0~3** | **最常用，4级抢占够用** |
| 分组3 | 3位，取值0~7 | 1位，取值0~1 | 抢占为主 |
| 分组4 | 4位，取值0~15 | 0位，取值0 | 只有抢占，无响应优先级 |

**优先级规则：**
- **抢占优先级**高的中断可以打断抢占优先级低的中断（嵌套）
- 抢占优先级相同时，**响应优先级**高的先响应（但不能嵌套）
- 抢占和响应都相同时，**中断向量表编号小**的先响应

### 中断函数的运行机制

- 中断函数名在 `startup_stm32f10x_xx.s` 启动文件里定义，后缀为 `IRQHandler`
- 中断函数**不需要声明**，硬件自动调用
- 中断函数应**尽量短**：不能写长延时（会丢中断），不要直接操作复杂硬件（与 main 冲突）
- 推荐做法：中断里只做标志位置位 + 数据暂存，复杂处理放 main 循环里

### 一次中断到底怎样发生

四类外设中断虽然来源不同，但都经过同一条链路：

```
外设条件成立
    │
    ▼
外设状态标志置位（EXTI_PR / USART_SR / TIM_SR / ADC_SR）
    │  本外设对应的中断使能位已开启？
    ▼
NVIC 将 IRQ 记为 Pending
    │  NVIC 通道已使能，且优先级允许响应？
    ▼
CPU 完成当前指令 → 自动压栈 → 从向量表取 ISR 地址
    │
    ▼
执行 xxx_IRQHandler：判断来源 → 读数据/清标志 → 暂存数据/置事件
    │
    ▼
异常返回：自动出栈，继续被打断的代码
```

> ✅ **中断有三层开关**：外设条件真的发生、外设内部中断使能、NVIC 通道使能。三者缺一不可。

NVIC 中还要分清三个状态：

| 状态 | 含义 |
|---|---|
| Enable | 该 IRQ 是否允许交给 CPU |
| Pending | 中断请求已经到达，正在等待处理 |
| Active | CPU 当前正在执行这个 IRQ 的 ISR |

只清 NVIC Pending 通常不能解决问题。如果外设状态位仍然保持，中断请求会立刻再次进入 NVIC；**真正需要清的是产生请求的外设标志**。

### Cortex-M3 进入与退出 ISR 时做了什么

进入异常时，Cortex-M3 硬件会自动保存 `R0~R3、R12、LR、PC、xPSR`，并从中断向量表装载处理函数地址。退出时再自动恢复，所以普通 ISR 可以写成 C 函数，不需要手写保存现场。

```
线程代码 ──中断──> 自动压栈 ──> ISR ──> 自动出栈 ──> 原位置继续
```

- **Tail-chaining（尾链）**：一个 ISR 退出时若已有另一个中断等待，内核可直接切到下一个 ISR，省去一次完整出栈/压栈。
- **Late arrival（迟到抢占）**：进入低优先级 ISR 的过程中若更高优先级中断到达，内核可以优先执行更紧急者。
- ISR 的执行时间与嵌套深度会占用栈空间；局部大数组、递归、格式化输出都不适合放在 ISR。

### 优先级数字越小，紧急程度越高

`0` 是最高优先级，不是最低。判断是否能抢占时先比较抢占优先级；只有抢占级相同且同时等待时，响应优先级才决定先后。

```text
当前正在执行：抢占优先级 2

新到 IRQ A：抢占优先级 1 → 可以立即抢占
新到 IRQ B：抢占优先级 2、响应优先级 0 → 不能抢占，只能等当前 ISR 退出
新到 IRQ C：抢占优先级 3 → 等待
```

> ⚠️ 优先级分组是全局规则，应在系统初始化阶段设置一次。不同驱动重复修改分组，会让此前配置的优先级含义改变。

### ISR 的四步模板

一段可靠 ISR 通常只做四件事：

1. **确认来源**：共享 IRQ 入口必须逐个检查状态位。
2. **读走必要数据**：某些标志靠读取数据寄存器清除，例如 USART RXNE。
3. **按外设规定清标志**：不同标志的清除顺序不同，不能机械套模板。
4. **发布最小事件**：保存数据、递增计数或置位标志，复杂处理留给主循环。

```c
volatile uint8_t g_event_pending;  // ISR 与主循环共享，防止编译器缓存旧值

void Peripheral_IRQHandler(void)
{
    if (Peripheral_GetITStatus(...) != RESET)
    {
        uint16_t sample = Peripheral_ReadData(...);  // 读必要数据
        Peripheral_ClearITPendingBit(...);           // 按参考手册要求清标志

        g_latest_sample = sample;                    // 快速暂存
        g_event_pending = 1;                         // 通知线程代码
    }
}
```

> `volatile` 只保证每次真正访问内存，**不保证复合操作原子性，也不能替代队列或临界区**。一个 ISR 生产、主循环消费连续数据时，优先使用环形缓冲区；多个字段需要一致快照时，应短暂关中断或使用版本/双缓冲方案。

### 四类中断的核心差异

| 中断 | 触发源 | ISR 最先做什么 | 典型数据通路 | 最常见风险 |
|---|---|---|---|---|
| [[02-GPIO与EXTI#EXTI 中断深度解析|EXTI]] | GPIO 上升/下降沿 | 判断并清 EXTI Pending | 记录按键/脉冲事件 | 按键抖动、共享入口漏判 Line |
| [[04-USART#USART 中断深度解析|USART]] | RXNE/TXE/TC/IDLE/错误 | 按标志规定读 SR/DR 或写 DR | 环形缓冲区、DMA | 接收过载、清标志顺序错误 |
| [[05-定时器#定时器中断深度解析|TIM]] | 更新、捕获比较、触发/刹车 | 判断 SR 中的具体来源并清位 | 周期调度、捕获时间戳 | ISR 超时造成抖动和延迟 |
| [[06-ADC#ADC 中断深度解析|ADC]] | EOC/JEOC/模拟看门狗 | 读 DR/JDR 或处理阈值事件 | 最新值、采样队列、DMA | 连续转换产生中断风暴 |

---

## 应用

| 场景 | 抢占优先级建议 | 说明 |
|------|--------------|------|
| 电机控制/PID 定时中断 | 0（最高） | 必须准时执行 |
| 编码器脉冲计数 | 0~1 | 不能丢脉冲 |
| USART 接收中断 | 1~2 | 波特率高时需要及时读走 |
| EXTI 按键中断 | 2~3 | ISR 只记事件；20ms 消抖放到定时逻辑，不在 ISR 阻塞 |
| 普通定时中断 | 2~3 | |

> 优先级没有万能固定值。真正的依据是：最迟允许多久响应、最坏执行多久、数据丢失后果、是否允许嵌套。高优先级 ISR 必须更短，而不是因为“重要”就塞入更多代码。

---

## 代码

### NVIC 配置

```c
/* NVIC 配置 — 整个工程只分组一次 */
NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);  // 分组2：2位抢占 + 2位响应

NVIC_InitTypeDef NVIC_InitStructure;
NVIC_InitStructure.NVIC_IRQChannel = EXTI15_10_IRQn;              // 中断通道名去 startup 文件找
NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;         // 抢占优先级
NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;                // 响应优先级
NVIC_Init(&NVIC_InitStructure);

// 配多个通道：直接覆盖同名结构体即可，不用新建
```

### 中断函数通用模板

```c
void xx_IRQHandler(void)
{
    if (xx_GetITStatus(...) == SET)     // 判断中断标志
    {
        // 1. 按该外设的规则读取数据或清标志
        // 2. 只保存数据、更新计数或置事件标志
    }
}
```

> ⚠️ 这是结构模板，不代表所有标志都用 `xx_ClearITPendingBit()`。USART 的 RXNE/IDLE/ORE、ADC 的 EOC 等常与读取寄存器的顺序绑定，必须查对应章节或参考手册。

### 主循环消费 ISR 事件

```c
volatile uint8_t g_sample_ready;
volatile uint16_t g_sample;

int main(void)
{
    System_Init();

    while (1)
    {
        if (g_sample_ready != 0)
        {
            uint16_t local_sample;

            __disable_irq();            // 临界区只包住共享状态快照
            local_sample = g_sample;
            g_sample_ready = 0;
            __enable_irq();

            ProcessSample(local_sample); // 滤波、显示、通信放在线程代码
        }
    }
}
```

若事件可能在主循环处理前连续发生多次，单个 `ready` 标志会合并事件；需要保存每一次数据时改用计数器或环形缓冲区。

### 返回值函数模式

**模式一：直接返回累计值**
```c
uint16_t xx_Count;

uint16_t xx_Get(void)
{
    return xx_Count;
}
```

**模式二：返回变化值并清零（编码器常用）**
```c
int16_t Encoder_Get(void)
{
    int16_t Temp;
    Temp = Encoder_Count;
    Encoder_Count = 0;
    return Temp;
}

// main.c 中累加差值：
int16_t Num;
Num += Encoder_Get();
```

---

## HAL 库对照

- HAL 使用统一的回调函数，如 `HAL_GPIO_EXTI_Callback()`、`HAL_TIM_PeriodElapsedCallback()`
- 中断优先级分组和 NVIC 配置在 CubeMX 的 NVIC 标签页完成
- HAL 中断函数内已经做了标志位判断，回调里直接写业务逻辑即可

HAL 的典型调用链是：

```text
真正的 IRQHandler
    → HAL_xxx_IRQHandler(&handle)   // HAL 判断、清标志并更新状态机
        → HAL_xxx_Callback(...)     // 用户回调只做轻量业务
```

不要绕过 `HAL_xxx_IRQHandler()` 直接从 IRQHandler 调用户回调，否则 HAL 内部状态和标志可能无法正确推进。

---

## 相关笔记

- [[02-GPIO与EXTI]]（EXTI 中断函数）
- [[04-USART]]（串口中断）
- [[05-定时器]]（定时器中断）
- [[06-ADC]]（ADC 中断）
