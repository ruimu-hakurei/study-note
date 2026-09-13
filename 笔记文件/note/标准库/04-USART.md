# USART：从一个字节到一个完整数据包

> 本文用 USART1 的异步模式说明通信。先分清 UART 字节帧和应用数据包，再把初始化、收发、中断缓冲与包解析接起来。

## 1. 接线与一帧字节

```text
STM32 TX ─────────→ 对方 RX
STM32 RX ←───────── 对方 TX
GND      ────────── 参考地
```

本文使用 STM32 逻辑电平串口。RS-232、RS-485 是不同的电气接口，需要相应收发器；USB 转串口模块也要确认逻辑电平兼容。

USART 支持同步和异步模式，UART 只支持异步模式。这里不用同步时钟 CK，双方约定相同波特率与字节帧格式。

### 1.1 8N1 到底发了多少位

`8N1` 表示 8 个数据位、无奇偶校验、1 个停止位：

```text
空闲 | 起始位 | D0 D1 D2 D3 D4 D5 D6 D7 | 停止位 | 下一帧或空闲
  1  |   0    |       低位先发          |   1    |
```

一个字节实际占 10 bit。波特率 9600 时，理想连续吞吐为 960 byte/s，每字节约 1.042 ms；115200 时约为 11520 byte/s。波特率不是有效载荷的字节速率。

例如发送 `0x41`，数据位按 `1 0 0 0 0 0 1 0` 的顺序出现。接收软件拿到的是数值 `0x41`，不会另外拿到起始位和停止位。

### 1.2 字节帧不等于应用数据包

```text
应用包：     FF | 01 | 02 | 03 | 04 | FE
UART 线上： [字节帧][字节帧][字节帧][字节帧][字节帧][字节帧]
```

UART 只负责把一个个字节送过来，包头、长度、命令、校验与包尾由应用协议约定。“HEX 发送”只是调试工具把输入按十六进制字节解释，不是一种不同的串口电气协议。

## 2. 初始化与阻塞发送

下面选择默认引脚 PA9=TX、PA10=RX，9600、8N1。代码使用 C99 与 STM32F1 标准库；工程已完成系统时钟与统一的 NVIC 分组配置。

```c
#include "stm32f10x.h"
#include <stdio.h>
#include <stdarg.h>
#include <string.h>

void Serial_Init(void)
{
    GPIO_InitTypeDef gpio;
    USART_InitTypeDef uart;
    NVIC_InitTypeDef nvic;
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA |
                          RCC_APB2Periph_USART1, ENABLE);
    GPIO_StructInit(&gpio);
    gpio.GPIO_Pin = GPIO_Pin_9;
    gpio.GPIO_Mode = GPIO_Mode_AF_PP;
    gpio.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &gpio);
    gpio.GPIO_Pin = GPIO_Pin_10;
    gpio.GPIO_Mode = GPIO_Mode_IPU;
    GPIO_Init(GPIOA, &gpio);

    USART_StructInit(&uart);
    uart.USART_BaudRate = 9600;
    uart.USART_WordLength = USART_WordLength_8b;
    uart.USART_StopBits = USART_StopBits_1;
    uart.USART_Parity = USART_Parity_No;
    uart.USART_Mode = USART_Mode_Tx | USART_Mode_Rx;
    uart.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
    USART_Init(USART1, &uart);

    nvic.NVIC_IRQChannel = USART1_IRQn;
    nvic.NVIC_IRQChannelPreemptionPriority = 1;
    nvic.NVIC_IRQChannelSubPriority = 0;
    nvic.NVIC_IRQChannelCmd = ENABLE;
    NVIC_Init(&nvic);
    USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);
    USART_Cmd(USART1, ENABLE);
}

static int Serial_Wait(uint16_t flag)
{
    uint32_t budget = 100000U;
    while (USART_GetFlagStatus(USART1, flag) == RESET)
        if (--budget == 0U) return 0;
    return 1;
}

int Serial_SendByte(uint8_t byte)
{
    if (!Serial_Wait(USART_FLAG_TXE)) return 0;
    USART_SendData(USART1, byte);
    return 1; // 已交给发送链路，未必已从 TX 发完
}

int Serial_SendArray(const uint8_t *data, uint16_t length)
{
    if (data == 0 && length != 0U) return 0;
    for (uint16_t i = 0; i < length; ++i)
        if (!Serial_SendByte(data[i])) return 0;
    return 1;
}

int Serial_Flush(void)
{
    return Serial_Wait(USART_FLAG_TC); // 等最后一个停止位完成
}
```

等待预算是循环次数，不是固定毫秒；正式驱动应使用统一计时源。发送超时可能意味着前半包已经发出，调用者要终止事务并处理重试，不能当作整包未发送。

F1 的字长配置包含启用的校验位：例如需要 8 个有效数据位加奇偶校验时，要核对 9 位字长配置。本文无校验的 8N1 不涉及这一转换。

## USART 中断深度解析

### 1. TXE、TC 与 RXNE 对应不同阶段

```text
CPU 写 DR → 发送移位寄存器 → TX
              ↑               ↑
        TXE：DR可继续写    TC：全部发送完成

RX → 接收移位寄存器 → DR → CPU / DMA 读走
                       ↑
                    RXNE=1
```

| 标志 | 含义 | 本文使用的处理方式 |
| --- | --- | --- |
| RXNE | DR 中有未读接收数据 | 读 DR |
| TXE | 发送 DR 可写 | 写 DR；没有待发数据时关闭 TXE 中断 |
| TC | 发送链路已完成 | 用于最后结束动作；按手册规定解除标志 |
| IDLE | 出现规定的接收空闲条件 | 先读 SR，再读 DR |
| ORE | 新数据到达时旧数据还未被及时读走 | 记录数据丢失，先读 SR 再读 DR |
| FE、NE、PE | 帧、噪声、校验错误 | 保存错误状态，再完成 SR→DR 读取序列 |

标志清除不是统一的 `ClearITPendingBit()` 收尾。读 DR 后 RXNE 已解除；IDLE/ORE 等则需要规定的 SR→DR 顺序。相关寄存器行为见 [ST RM0008 USART 章节](https://www.st.com/resource/en/reference_manual/cd00171190.pdf)。

RS-485 释放 DE 要等 TC，不能只等 TXE，否则最后一字节可能被截断。TXE 中断发送则应在队列为空时关掉 TXEIE，避免不停进入中断。

### 2. 中断只收字节，主循环解析协议

单个 `RxData + RxFlag` 只能暂存一个字节，连续输入会覆盖旧数据。下面保留一个 ISR，使用单生产者、单消费者环形缓冲区：

```c
#define RX_CAP 128U
#define RX_MASK (RX_CAP - 1U)
static volatile uint8_t RxBuffer[RX_CAP];
static volatile uint16_t RxHead, RxTail;
static volatile uint32_t RxLoss;

void USART1_IRQHandler(void)
{
    uint16_t sr = (uint16_t)USART1->SR;
    uint16_t errors = USART_SR_ORE | USART_SR_FE |
                      USART_SR_NE | USART_SR_PE;
    if ((sr & (USART_SR_RXNE | errors)) == 0U) return;

    uint8_t byte = (uint8_t)USART1->DR; // SR 后读 DR
    if ((sr & errors) != 0U) { ++RxLoss; return; }
    if ((sr & USART_SR_RXNE) == 0U) return;

    uint16_t next = (uint16_t)((RxHead + 1U) & RX_MASK);
    if (next == RxTail) { ++RxLoss; return; } // 满时丢新字节
    RxBuffer[RxHead] = byte;
    RxHead = next;
}

int Serial_ReadByte(uint8_t *out)
{
    if (out == 0 || RxTail == RxHead) return 0;
    *out = RxBuffer[RxTail];
    RxTail = (uint16_t)((RxTail + 1U) & RX_MASK);
    return 1;
}
```

数组长度为 128，可实际存放 127 字节，空出一格区分满与空。这个模型限定在 Cortex-M3 上 ISR 唯一写入、主循环唯一消费；`volatile` 不是通用的多线程同步机制。

检测到 `RxLoss` 变化时，主循环应在短临界区内丢弃残留接收字节，并重置下面的解析器。否则丢掉一个字节后，残缺数据可能被拼成错误包。复杂解析、输出日志与命令执行都放在 ISR 之外。

## 3. 二进制包：固定长度意味着什么

### 3.1 明确写下格式

本文保留原笔记的教学协议：

| 字节偏移 | 内容 | 解释 |
| --- | --- | --- |
| 0 | `FF` | 包头 |
| 1~4 | `D0 D1 D2 D3` | 固定 4 字节载荷 |
| 5 | `FE` | 包尾 |

`D0~D3` 可以取任意字节值，包括 `FF/FE`：因为解析器按长度数满 4 字节后才检查包尾。若把它改成“遇到 FE 就结束”，协议含义就变了。

这个格式没有校验，不保证检测载荷损坏，也不能保证任意噪声下无歧义同步。需要更可靠的协议时，应明确长度上限、命令字段、校验算法、转义或编码规则及超时策略。

### 3.2 状态机只处理已收到的字节

```text
等 FF → 收满 4 字节 → 检查 FE → 交付一个包 → 重新等 FF
                         └─错误：丢包；若当前字节是 FF，作为新包头
```

```c
typedef struct {
    uint8_t state, used;
    uint8_t data[4];
} HexParser;

void HexParser_Reset(HexParser *p)
{
    p->state = 0;
    p->used = 0;
}

int HexParser_Feed(HexParser *p, uint8_t b)
{
    if (p->state == 0U) {
        if (b == 0xFFU) { p->state = 1; p->used = 0; }
    } else if (p->state == 1U) {
        p->data[p->used++] = b;
        if (p->used == 4U) p->state = 2;
    } else {
        p->state = 0;
        if (b == 0xFEU) return 1;
        if (b == 0xFFU) { p->state = 1; p->used = 0; }
    }
    return 0;
}
```

主循环不断 `Serial_ReadByte()`，将每个字节传入 `HexParser_Feed()`；返回 1 时立即处理或复制 `p->data`，随后继续喂入剩余字节。这样一包分多次到达、或者多包连续到达，都使用同一套逻辑。

初始化时将 `HexParser` 清零。收到半包后超过约定的字节间超时，或接收层报告丢字节时，调用 `HexParser_Reset()`。解析器本身不读取系统时钟，由调用者决定超时。

发送时直接组织六字节数组：`FF D0 D1 D2 D3 FE`，调用 `Serial_SendArray()`。多个任务发送时要保护整包，避免两包的字节交错。

## 4. 文本包：结束符与缓冲区边界

另一个独立示例采用 `@内容\r\n`。为使规则明确，本例规定内容为可打印 ASCII，不含 `@`，最长 99 字符，允许空内容；业务层可以进一步拒绝空命令。

```c
typedef struct {
    uint8_t state;
    uint16_t used;
    char text[100];
} TextParser;

int TextParser_Feed(TextParser *p, uint8_t b)
{
    if (b == '@') { p->state = 1; p->used = 0; return 0; }
    if (p->state == 1U) {
        if (b == '\r') p->state = 2;
        else if (b >= 0x20U && b <= 0x7EU &&
                 p->used < sizeof p->text - 1U)
            p->text[p->used++] = (char)b;
        else { p->state = 0; p->used = 0; }
    } else if (p->state == 2U) {
        p->state = 0;
        if (b == '\n') { p->text[p->used] = '\0'; return 1; }
    }
    return 0;
}
```

同样在主循环喂字节，实例先清零，完整包返回 1 后及时消费结果；超时或接收丢失时清零 `state/used`。`\r\n` 在线上是 `0D 0A` 两个字节，C 字符串末尾的 `\0` 只在本地补上，未在这个协议中发送。

二进制包和文本包是两种可选协议示例，不要不加区分地让同一条字节流同时触发两种业务命令。

## 5. 数值编码与调试输出

字符 `'1'` 在线上是 `0x31`，二进制数值 1 是 `0x01`。多字节数字要另行规定字节序，例如 `uint16_t 0x1234` 的小端表示为 `34 12`；这与 UART 逐字节 LSB 先发不是同一件事。

STM32F103 上若双方约定 IEEE 754 binary32、小端顺序，可以明确序列化浮点值：

```c
int Serial_SendFloatLE(float value)
{
    uint32_t bits;
    uint8_t b[4];
    memcpy(&bits, &value, sizeof bits);
    for (unsigned i = 0; i < 4U; ++i)
        b[i] = (uint8_t)(bits >> (8U * i));
    return Serial_SendArray(b, 4);
}

int Serial_Printf(const char *format, ...)
{
    char text[100];
    va_list args;
    va_start(args, format);
    int n = vsnprintf(text, sizeof text, format, args);
    va_end(args);
    if (n < 0 || (unsigned)n >= sizeof text) return 0;
    return Serial_SendArray((const uint8_t *)text, (uint16_t)n);
}
```

`Serial_Printf()` 明确拒绝过长输出，避免 `vsprintf()` 写越界。标准 `printf` 重定向到串口时，`fputc` 或 `_write` 入口取决于工具链，不是串口协议要求。

原笔记中的 `00 00 80 7F` 是特定上位机数据格式可能采用的帧尾，不是通用 USART 包尾。调试打印也不要直接混进设备二进制协议流。

## 6. IDLE、DMA 与 HAL 放在哪一层

IDLE 表示接收线出现规定的空闲条件，DMA 表示将接收数据搬进内存。它们都不会自动判断自定义包的长度、包尾或校验。

```text
DMA 半满/全满或 IDLE 事件 → 提取本次新收到的字节 → 喂给同一个包解析器
```

一包中间可能暂停触发 IDLE，多包也可能连续传送而没有 IDLE。仅当上层协议明确用静默时间分帧，并满足其时长约束时，才可把空闲作为分包依据。

普通 DMA 停止再启动可能有接收空隙；环形 DMA 应根据上次消费位置和当前写入位置处理回绕。缓冲区必须有明确所有权，应用尚未消费的区域不能被 DMA 覆盖。

| 标准库思路 | HAL 对照 |
| --- | --- |
| 轮询发送 | `HAL_UART_Transmit()`，检查返回值 |
| 中断接收 | `HAL_UART_Receive_IT()`，完成后复制/入队并安排下一次接收 |
| DMA 接收并观察空闲 | 可用版本中的 `HAL_UARTEx_ReceiveToIdle_DMA()` |
| 应用包状态机 | 完全可以复用前面的纯 C 解析器 |

HAL 异步缓冲区在回调前必须保持有效。Receive-to-idle 的普通/环形 DMA、半传输/完成事件行为需按工程 HAL 版本核对；不能把每次回调的 `Size` 都不加判断地解释为“一个新数据包”。

## 7. 排查时按层定位

| 现象 | 优先检查 |
| --- | --- |
| 完全无数据 | 接线、电平、参考地、引脚、外设时钟 |
| 字节乱码 | 波特率、字长、校验、停止位、时钟配置 |
| 单字节正确，整包偶尔错 | ORE、环形缓冲溢出、包解析重同步与超时 |
| 发送末尾缺字节 | 把 TXE 当成 TC、过早释放 RS-485 DE |
| ISR 不断进入 | TXEIE 未关闭，或错误/IDLE 标志清除方式不对 |

关联：[[通信协议总览]]、[[01-时钟系统]]、[[02-GPIO与EXTI]]、[[03-中断NVIC]]、[[07-DMA]]。
