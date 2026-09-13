# CAN：从总线仲裁到一条应用报文

> STM32F103 的 bxCAN 支持经典 CAN。控制器负责总线帧、仲裁与错误检测，外部收发器负责电气信号，应用程序负责解释 ID 和最多 8 字节的载荷。

## 1. 接线：MCU 引脚不能直接当成 CAN_H/CAN_L

```text
STM32 CAN_TX/RX ↔ CAN 收发器 ↔ CAN_H / CAN_L 总线 ↔ 其他节点
```

CAN_H、CAN_L 是差分总线线路，不是 MCU 的 TX/RX 引脚。高速 CAN 总线通常在物理两端各放一个 120 Ω 终端电阻，而不是每个节点都放一个；还需合理处理参考地或隔离。

拓扑以主干线和较短支线为基础，波特率、长度、支线及收发器共同决定实际约束。本文示例使用默认 PA11=CAN_RX、PA12=CAN_TX，注意与板上 USB 等用途冲突。

## 2. 多个节点为什么能同时申请发送

CAN 使用显性 0、隐性 1；仲裁时发送隐性位的节点若读到显性位，就知道有更高优先级报文正在发送，于是退出竞争并转为接收。

在相同帧格式下，标识符逐位比较时，先出现显性位的一方获胜，因此数值较小的 ID 通常优先。标准帧和扩展帧混合、数据帧和远程帧混合时，还要考虑 SRR、IDE、RTR 等仲裁位，不能仅比较两个整数。

**ID 首先是报文标识与仲裁依据。** CAN 底层不强制规定源地址、目的地址；具体设备协议可以把节点号、命令号编码在 ID 中。

## 3. 一条经典 CAN 数据帧包含什么

```text
SOF | 仲裁字段 | 控制字段 | 数据字段 | CRC | ACK | EOF
      ID等        DLC      0~8字节
```

| 字段 | 含义 | 应用是否需要手动填 |
| --- | --- | --- |
| 标识符 | 标准帧 11 位，扩展帧 29 位 | 是 |
| IDE | 标准/扩展格式 | 是 |
| RTR | 数据帧/远程帧 | 是 |
| DLC | 数据帧中的载荷长度，本文限定 0~8 | 是 |
| Data | 业务数据 | 是 |
| 位填充、CRC、ACK、EOF | 总线同步、检测与结束机制 | 由控制器处理 |

ACK 表示至少有正常参与总线的其他节点正确接收了底层帧，不表示指定电机已经执行命令。接收过滤器不等于业务确认；有效帧即使未通过某节点的应用接收过滤，正常节点仍可参与 ACK。

普通模式下只有一个节点主动发送、没有其他节点 ACK，可能持续报错或重传。内部回环模式可以检查控制器软件流程，但不能验证收发器、接线和真实总线仲裁。F103 的经典 CAN 示例不支持 CAN FD 的长载荷。

## 4. 位时序：库枚举名称已经代表实际 Tq 数

一个位在 bxCAN 中按以下方式设置：

```text
| 同步段 1 Tq | BS1 | BS2 |
                    ↑
                  采样点
```

$$
f_{\text{bit}}=\frac{f_{\text{PCLK1}}}{\text{Prescaler}\,(1+\text{BS1}+\text{BS2})},\qquad
\text{采样点}=\frac{1+\text{BS1}}{1+\text{BS1}+\text{BS2}}
$$

对 SPL 字段：`CAN_Prescaler` 填实际分频数；`CAN_BS1_9tq` 就是 **9 Tq**，不是 10 Tq。寄存器字段使用“实际值减 1”的编码，不能把寄存器编码规则再次加到库枚举名称上。

PCLK1=36 MHz、BS1=9 Tq、BS2=2 Tq 时，每位共 12 Tq，采样点约 83.3%：

| Prescaler | 计算 | 波特率 |
| --- | --- | --- |
| 24 | $36\text{ MHz}/(24\times12)$ | 125 kbit/s |
| 12 | $36\text{ MHz}/(12\times12)$ | 250 kbit/s |
| 6 | $36\text{ MHz}/(6\times12)$ | 500 kbit/s |

SJW 是重新同步时允许调整的宽度，本例取 1 Tq，并满足不大于 BS2 等约束。相同波特率还要考虑采样点、收发器延迟与线路条件。

原笔记的 `Prescaler=48、BS1_2tq、BS2_3tq` 实际得到 $36\text{ MHz}/[48(1+2+3)]=125\text{ kbit/s}$。原先把 2 Tq、3 Tq 再加 1 的解释有误，算出的 93.75 kbit/s 也不能近似当作 125 kbit/s。

## 5. 过滤器：先判断帧能否进接收 FIFO

掩码模式的逻辑是：

```text
(收到的编码字段 & mask) == (配置的编码字段 & mask)
```

掩码为 1 的位必须匹配，为 0 的位不关心。全零掩码会放行所有匹配范围内的格式，适合初步调试，但不等于“只收 ID=0”。

32 位过滤器组织可同时表示标准或扩展帧；32 位不是“标准帧”的同义词。标准 ID 位于 bit31:21，IDE 位于 bit2，RTR 位于 bit1。精确接收标准数据帧 `0x123` 时：

```text
过滤值 = 0x123 << 21
掩码   = (0x7FF << 21) | (1 << 2) | (1 << 1)
```

这样不仅检查 ID，也要求 IDE=0、RTR=0。字段排列与位时序依据 [ST RM0008 bxCAN 章节](https://www.st.com/resource/en/reference_manual/cd00171190.pdf)，库枚举还与本地 ST 标准库头文件核对。

## 6. 标准库：初始化、发送和轮询接收

代码基于 PCLK1=36 MHz，使用普通模式、500 kbit/s，并只将标准数据帧 `0x123` 放入 FIFO0。先确认真实时钟树和其他节点配置。

### 6.1 初始化与精确过滤

```c
#include "stm32f10x.h"

int MyCAN_Init(void)
{
    GPIO_InitTypeDef gpio;
    CAN_InitTypeDef can;
    CAN_FilterInitTypeDef filter;
    uint32_t id = 0x123UL << 21;
    uint32_t mask = (0x7FFUL << 21) | (1UL << 2) | (1UL << 1);
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_CAN1, ENABLE);
    GPIO_StructInit(&gpio);
    gpio.GPIO_Pin = GPIO_Pin_12;
    gpio.GPIO_Mode = GPIO_Mode_AF_PP;
    gpio.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &gpio);
    gpio.GPIO_Pin = GPIO_Pin_11;
    gpio.GPIO_Mode = GPIO_Mode_IN_FLOATING;
    GPIO_Init(GPIOA, &gpio);

    CAN_StructInit(&can);
    can.CAN_Mode = CAN_Mode_Normal; // 内部自测时另选 CAN_Mode_LoopBack
    can.CAN_Prescaler = 6;
    can.CAN_BS1 = CAN_BS1_9tq;
    can.CAN_BS2 = CAN_BS2_2tq;
    can.CAN_SJW = CAN_SJW_1tq;
    can.CAN_NART = DISABLE; // 允许自动重传
    can.CAN_TXFP = DISABLE; // 邮箱按标识符优先级处理
    can.CAN_RFLM = ENABLE;  // FIFO 满时保留已有帧、丢新帧
    can.CAN_ABOM = ENABLE;  // 允许按硬件规则自动恢复 bus-off
    can.CAN_AWUM = DISABLE;
    can.CAN_TTCM = DISABLE;
    if (CAN_Init(CAN1, &can) != CAN_InitStatus_Success) return 0;

    filter.CAN_FilterNumber = 0;
    filter.CAN_FilterMode = CAN_FilterMode_IdMask;
    filter.CAN_FilterScale = CAN_FilterScale_32bit;
    filter.CAN_FilterIdHigh = (uint16_t)(id >> 16);
    filter.CAN_FilterIdLow = (uint16_t)id;
    filter.CAN_FilterMaskIdHigh = (uint16_t)(mask >> 16);
    filter.CAN_FilterMaskIdLow = (uint16_t)mask;
    filter.CAN_FilterFIFOAssignment = CAN_Filter_FIFO0;
    filter.CAN_FilterActivation = ENABLE;
    CAN_FilterInit(&filter);
    return 1;
}
```

`NART` 的名字表示“禁止自动重传”：设为 ENABLE 才是禁止重传。`ABOM` 允许 bus-off 自动恢复，但不能修复接线错误，也不能保证业务连续性。

### 6.2 发送要区分入队、成功、失败和超时

```c
// 返回：1=成功，0=超时且已申请取消，负数=参数/邮箱/发送错误。
int MyCAN_SendStd(uint16_t id, const uint8_t *data, uint8_t length)
{
    CanTxMsg msg = {0};
    if (id > 0x7FFU || length > 8U || (length && data == 0)) return -1;
    msg.StdId = id;
    msg.IDE = CAN_Id_Standard;
    msg.RTR = CAN_RTR_Data;
    msg.DLC = length;
    for (uint8_t i = 0; i < length; ++i) msg.Data[i] = data[i];

    uint8_t mailbox = CAN_Transmit(CAN1, &msg);
    if (mailbox == CAN_TxStatus_NoMailBox) return -2;
    uint32_t budget = 100000U;
    while (budget-- != 0U) {
        uint8_t status = CAN_TransmitStatus(CAN1, mailbox);
        if (status == CAN_TxStatus_Ok) return 1;
        if (status == CAN_TxStatus_Failed) return -3;
    }
    CAN_CancelTransmit(CAN1, mailbox);
    return 0;
}

int MyCAN_TryReceive(CanRxMsg *out)
{
    if (out == 0 || CAN_MessagePending(CAN1, CAN_FIFO0) == 0U) return 0;
    CAN_Receive(CAN1, CAN_FIFO0, out);
    return 1;
}
```

循环预算不是毫秒，应按项目改为计时超时。超时后申请取消，不保证报文绝未发出：发送完成与取消可能竞争，必要时查询最终邮箱状态，用应用序号和响应避免重复执行。

接收前先确认 FIFO 有帧；收取后仍需检查 IDE、RTR、ID、DLC 与字段范围。不要在同一 FIFO 上同时让轮询代码和 ISR 竞争消费。

## 7. 中断接收：搬出完整帧，再交给应用

使用中断时，开启 `CAN_IT_FMP0` 并配置 `USB_LP_CAN1_RX0_IRQn`。F1 的中断入口要与工程启动文件核对；共享入口还需处理工程实际启用的其他来源。

```c
// 应用需实现：复制整个 msg 入软件队列；满时返回0，不能保存栈指针。
extern int App_CANEnqueue(const CanRxMsg *msg);
static volatile uint32_t CAN_SoftwareDropped;

void USB_LP_CAN1_RX0_IRQHandler(void)
{
    while (CAN_MessagePending(CAN1, CAN_FIFO0) != 0U) {
        CanRxMsg msg;
        CAN_Receive(CAN1, CAN_FIFO0, &msg);
        if (!App_CANEnqueue(&msg)) ++CAN_SoftwareDropped;
    }
}
```

`CAN_Receive()` 读取并释放一个 FIFO 项。硬件 FIFO 容量有限，应用还应监测其溢出标志；ISR 不做耗时解析，队列也不能只用一个会被覆盖的全局消息加标志。

## 8. 载荷怎样变成业务数据

CAN 只知道 Data[0..DLC−1]，不知道哪个字段是电流、速度或角度。应用协议应写清：

| 项目 | 自定义示例，仅用于展示格式 |
| --- | --- |
| ID/格式 | 标准数据帧 `0x123` |
| DLC | 2 |
| 载荷 | 有符号 16 位值，小端，单位 0.01 A |
| `64 00` | 编码值 100，即 +1.00 A |
| `9C FF` | 补码编码值 −100，即 −1.00 A |

这不是任何具体电机的既定协议。连接实际设备时必须使用该设备规定的 ID、大小端、比例、周期、使能与响应规则。

## 9. HAL 对照和排查

| SPL | HAL 对应 |
| --- | --- |
| `CAN_Init()`、`CAN_FilterInit()` | 初始化、`HAL_CAN_ConfigFilter()`，再 `HAL_CAN_Start()` |
| `CAN_Transmit()` | `HAL_CAN_AddTxMessage()`，检查是否成功入队 |
| `CAN_MessagePending()`、`CAN_Receive()` | FIFO 填充数检查与 `HAL_CAN_GetRxMessage()` |
| FIFO 中断配置 | 通知使能、NVIC、`HAL_CAN_RxFifo0MsgPendingCallback()` |

HAL 邮箱“不再 pending”不自动等于成功发送，还需结合完成/错误/中止结果。

| 现象 | 优先检查 |
| --- | --- |
| 回环正常，普通模式失败 | 外部收发器、终端、电源、接线、是否有其他节点 ACK |
| 一直重传或进入 bus-off | 波特率、采样点、收发器状态、错误计数 |
| 总线上有帧但软件收不到 | 过滤值、IDE/RTR 掩码、FIFO、中断配置 |
| 数据收到了但动作不对 | 设备应用协议、DLC、字节序、比例、业务状态 |

关联：[[通信协议总览]]、[[01-时钟系统]]、[[02-GPIO与EXTI]]、[[03-中断NVIC]]、[[04-USART]]。
