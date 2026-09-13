# SPI：先看时钟交换，再看设备命令

> SPI 外设负责按时钟交换位；Flash、屏幕或传感器规定这些字节代表什么。本文以 SPI1、GPIO 片选和 W25Q64 普通 SPI 命令说明两者的关系。

## 1. 四根信号线各做什么

```text
STM32 主机                         从机
SCK  ────────────────────────────→ 时钟
MOSI ────────────────────────────→ 数据输入
MISO ←──────────────────────────── 数据输出
CS   ────────────────────────────→ 片选，本文低有效
GND  ───────────────────────────── 参考地
```

主机产生 SCK；普通四线全双工模式下，每个时钟周期同时移出、移入一位。交换一个 8 位字节，需要 8 个时钟。

**读数据为什么还要发送？** 主机要产生时钟才能接收，因此发送占位字节，接收从机同时返回的数据。占位字节取值要遵循设备命令，下面用 `0xFF`。

多个从机通常共享 SCK/MOSI/MISO，各自使用独立 CS。同一时刻只选中一个会驱动公共 MISO 的设备；未选中的从机应按其规格释放该线。

## 2. CPOL、CPHA 决定在哪个边沿采样

CPOL 决定时钟空闲电平；CPHA 决定在离开空闲电平的第一个边沿，还是返回空闲电平的第二个边沿采样。

| 模式 | CPOL | CPHA | 空闲电平 | 采样沿 | 另一边沿用于移出下一位 |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 低 | 上升沿 | 下降沿 |
| 1 | 0 | 1 | 低 | 下降沿 | 上升沿 |
| 2 | 1 | 0 | 高 | 下降沿 | 上升沿 |
| 3 | 1 | 1 | 高 | 上升沿 | 下降沿 |

CPHA=0 时，首位数据必须在第一个采样沿之前准备好。双方还要约定 MSB/LSB 先发，以及字长。数据手册给的是设备支持的模式，不能靠“通常用模式 0”代替核对。

## 3. 一个字节与一次事务的边界

一个字节是 8 个时钟；一次设备事务往往由多个字节组成，通常由 CS 包住整个命令。

以普通读命令 `03h`、地址 `0x001234`、读取两字节为例：

```text
CS    ↓___________________________________________________↑
序号       0      1      2      3      4      5
MOSI      03     00     12     34     FF     FF
MISO      xx     xx     xx     xx     D0     D1
含义      命令   A23:16 A15:8  A7:0   读数据 读数据
```

`xx` 表示本命令下不用的返回值。地址的三个字节由高到低发送；这与每个字节内部 MSB 先发是两个不同层次。

`03h` 普通读在地址后直接返回数据。不要与需要额外 dummy clocks 的快速读命令混用。每个字节后都拉高 CS，会把一条事务拆断。

## 4. 标准库：初始化与最小事务

下面使用默认引脚：PA5=SCK、PA6=MISO、PA7=MOSI，PA4 为普通 GPIO 片选。代码依赖 STM32F1 标准库头文件；它是单主机轮询示例。

### 4.1 初始化

```c
#include "stm32f10x.h"

void MySPI_Init(void)
{
    GPIO_InitTypeDef gpio;
    SPI_InitTypeDef spi;
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA |
                          RCC_APB2Periph_SPI1, ENABLE);

    GPIO_SetBits(GPIOA, GPIO_Pin_4);  // 先预置 CS 空闲电平
    GPIO_StructInit(&gpio);
    gpio.GPIO_Pin = GPIO_Pin_4;
    gpio.GPIO_Mode = GPIO_Mode_Out_PP;
    gpio.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &gpio);
    gpio.GPIO_Pin = GPIO_Pin_5 | GPIO_Pin_7;
    gpio.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_Init(GPIOA, &gpio);
    gpio.GPIO_Pin = GPIO_Pin_6;
    gpio.GPIO_Mode = GPIO_Mode_IN_FLOATING;
    GPIO_Init(GPIOA, &gpio);

    SPI_StructInit(&spi);
    spi.SPI_Mode = SPI_Mode_Master;
    spi.SPI_Direction = SPI_Direction_2Lines_FullDuplex;
    spi.SPI_DataSize = SPI_DataSize_8b;
    spi.SPI_FirstBit = SPI_FirstBit_MSB;
    spi.SPI_CPOL = SPI_CPOL_Low;
    spi.SPI_CPHA = SPI_CPHA_1Edge;
    spi.SPI_NSS = SPI_NSS_Soft;
    spi.SPI_BaudRatePrescaler = SPI_BaudRatePrescaler_128;
    SPI_Init(SPI1, &spi);
    SPI_NSSInternalSoftwareConfig(SPI1, SPI_NSSInternalSoft_Set);
    SPI_Cmd(SPI1, ENABLE);
}
```

若 PCLK2 为 72 MHz，SCK 为 $72\text{ MHz}/128=562.5\text{ kHz}$。使用其他时钟配置时要重新计算。

`SPI_NSS_Soft` 管理的是外设内部 NSS，**不会自动翻转 PA4**。本例用 GPIO 明确划分命令事务。F1 的硬件 NSS 输出也不能理解成“每写一个字节自动生成一次片选脉冲”。

### 4.2 每次交换都接收，再等总线真正完成

```c
static int SPI_Wait(uint16_t flag, FlagStatus value)
{
    uint32_t budget = 100000U;
    while (SPI_I2S_GetFlagStatus(SPI1, flag) != value)
        if (--budget == 0U) return 0;
    return 1;
}

int MySPI_SwapByte(uint8_t tx, uint8_t *rx)
{
    if (rx == 0 || !SPI_Wait(SPI_I2S_FLAG_TXE, SET)) return 0;
    SPI_I2S_SendData(SPI1, tx);
    if (!SPI_Wait(SPI_I2S_FLAG_RXNE, SET)) return 0;
    *rx = (uint8_t)SPI_I2S_ReceiveData(SPI1);
    return 1;
}

int W25_ReadJedecId(uint8_t id[3])
{
    uint8_t discard;
    if (id == 0) return 0;
    GPIO_ResetBits(GPIOA, GPIO_Pin_4);
    if (!MySPI_SwapByte(0x9FU, &discard)) goto fail;
    for (unsigned i = 0; i < 3U; ++i)
        if (!MySPI_SwapByte(0xFFU, &id[i])) goto fail;
    if (!SPI_Wait(SPI_I2S_FLAG_TXE, SET) ||
        !SPI_Wait(SPI_I2S_FLAG_BSY, RESET)) goto fail;
    GPIO_SetBits(GPIOA, GPIO_Pin_4);
    return 1;
fail:
    SPI_Cmd(SPI1, DISABLE); // 中止当前读事务
    GPIO_SetBits(GPIOA, GPIO_Pin_4);
    return 0;             // 调用者诊断并复位/重新初始化外设后再重试
}
```

等待预算是循环次数，不是毫秒。实际驱动应换成统一的计时超时并记录错误。函数返回失败后，`id` 中的部分数据无效；本示例的 SPI 已被禁用，不能忽略返回值继续下一条事务。

发送命令时也会接收一个字节，要及时读走，即使它没有业务含义。末尾的 `TXE` 表示 DR 可写，`BSY=0` 才用于确认本例主机传输结束后可以释放片选。F1 外设行为参见 [RM0008](https://www.st.com/resource/en/reference_manual/cd00171190.pdf)。

## 5. W25Q64 命令是建立在 SPI 之上的设备协议

以下用 W25Q64JV 的常见标准 SPI 指令举例；同系列不同电压、后缀和版本仍需核对对应数据手册。

| 操作 | 一次 CS 有效期间发送的内容 | 完成后做什么 |
| --- | --- | --- |
| 读 JEDEC ID | `9F`，再产生 3 字节时钟 | 获得厂商与器件标识 |
| 普通读取 | `03 + 24 位地址 + 数据时钟` | 接收所需数据 |
| 写使能 | `06` | 结束此事务，再发编程/擦除命令 |
| 页编程 | `02 + 24 位地址 + 1~256 字节数据` | 结束事务后轮询 BUSY |
| 4 KiB 扇区擦除 | `20 + 24 位地址` | 结束事务后轮询 BUSY |
| 读状态寄存器 1 | `05 + 状态读取时钟` | 检查 BUSY、WEL 等位 |

一次编程的完整过程是：等待设备不忙 → 独立发送写使能 → 发页编程事务 → 轮询状态直到不忙。写使能不是给 MCU 的命令，设备 BUSY 也不同于 STM32 的 SPI `BSY`。

容量为 64 Mbit，即 8 MiB。页编程不能越过 256 字节页边界，要按 `min(剩余长度, 256 - 地址%256)` 分段。编程主要将位从 1 变成 0；要将 0 恢复为 1，需要擦除所属区域，并考虑保留该区域其他数据。以上命令与边界见 [Winbond W25Q64JV 数据手册](https://media.digikey.com/pdf/Data%20Sheets/Winbond%20PDFs/W25Q64JV_RevK_3-10-21.pdf)。

## 6. HAL 对应关系与排查

| 标准库动作 | HAL 对应思路 |
| --- | --- |
| 写 DR、等 RXNE、读 DR | `HAL_SPI_TransmitReceive()` |
| GPIO 拉低/拉高 CS | `HAL_GPIO_WritePin()` |
| 等待设备编程完成 | 仍要发设备状态查询命令，HAL 不替你完成 |

HAL 收发返回值必须检查，异步或 DMA 方式要等完成回调后再结束事务。

| 现象 | 优先检查 |
| --- | --- |
| 总读到 `FF` 或 `00` | CS、MISO、电源、设备状态与接线 |
| 数据整体错位 | CPOL/CPHA、位序、首位建立时间 |
| ID 能读，存储读写失败 | 命令、地址字节序、页边界、写使能、BUSY |
| 最后一字节不稳定 | 是否过早释放 CS，是否误把 TXE 当发送结束 |

关联：[[通信协议总览]]、[[01-时钟系统]]、[[02-GPIO与EXTI]]、[[09-I2C]]。
