# DMA 直接存储器访问

> DMA 初始化、软件触发转运、非自动重装模式

---

## 底层

### DMA 工作原理

DMA（Direct Memory Access）可以在不占用 CPU 的情况下，直接在**外设 ↔ 内存**或**内存 ↔ 内存**之间搬运数据：

```
              ┌─→ 外设地址 (Peripheral Address)
DMA 控制器 ───┤
              └─→ 内存地址 (Memory Address)
                   每次转运 BufferSize 次，完成后触发中断
```

**关键概念：**
- **DMA 通道**：每个 DMA 控制器有 7 个通道，不同外设对应不同通道（查 DMA 通道映射表）
- **BufferSize**：转运次数，每次转运递减，减到 0 时转运完成
- **自动重装 (Circular)**：BufferSize 归零后自动恢复初始值继续转运，适合 ADC 循环采样
- **M2M (Memory to Memory)**：软件触发模式，用于内存到内存的块拷贝

### 两种触发方式

| 触发方式 | 配置 | 说明 |
|----------|------|------|
| 硬件触发 | M2M=DISABLE | 外设事件触发（如 ADC 转换完成、USART TXE），通道对应关系查 DMA 通道映射表 |
| **软件触发** | **M2M=ENABLE** | 开启 DMA 后立即转运，用于内存到内存拷贝。M2M 模式下**不能自动重装** |

### 地址自增规则

| 场景 | 外设地址自增 | 内存地址自增 |
|------|-------------|-------------|
| 转运 ADC1->DR 到数组 | **不自增**（固定读同一个寄存器） | 自增（依次存数组元素） |
| 内存到内存拷贝 | 自增 | 自增 |
| 串口发送 | 不自增 | 自增 |

---

## 应用

| 场景 | DMA 配置 |
|------|----------|
| ADC 多通道连续采样 | 硬件触发 + 循环模式 + 外设不自增 |
| 内存块快速拷贝 | M2M 软件触发 + 单次模式 |
| USART 大数据发送 | 硬件触发 + 单次模式 |
| 波形发生器 | M2M + 循环模式搬运波形表到 DAC |

---

## 代码

### DMA 初始化（M2M 内存到内存）

```c
void MyDMA_Init(uint32_t AddrA, uint32_t AddrB, uint16_t Size)
{
    RCC_AHBPeriphClockCmd(RCC_AHBPeriph_DMA1, ENABLE);  // DMA 时钟在 AHB 上，不是 APB！

    DMA_InitTypeDef DMA_InitStructure;

    /* 外设端（源或目标，取决于 DIR） */
    DMA_InitStructure.DMA_PeripheralBaseAddr = AddrA;
    DMA_InitStructure.DMA_PeripheralDataSize = DMA_PeripheralDataSize_Byte;
    DMA_InitStructure.DMA_PeripheralInc = DMA_PeripheralInc_Enable;

    /* 内存端 */
    DMA_InitStructure.DMA_MemoryBaseAddr = AddrB;
    DMA_InitStructure.DMA_MemoryDataSize = DMA_MemoryDataSize_Byte;
    DMA_InitStructure.DMA_MemoryInc = DMA_MemoryInc_Enable;

    /* 通用设置 */
    DMA_InitStructure.DMA_BufferSize = Size;                 // 转运次数
    DMA_InitStructure.DMA_DIR = DMA_DIR_PeripheralSRC;       // 外设→内存
    DMA_InitStructure.DMA_M2M = DMA_M2M_Enable;              // 软件触发
    DMA_InitStructure.DMA_Mode = DMA_Mode_Normal;            // 非自动重装
    DMA_InitStructure.DMA_Priority = DMA_Priority_Medium;

    DMA_Init(DMA1_Channel1, &DMA_InitStructure);

    DMA_Cmd(DMA1_Channel1, ENABLE);                          // M2M 模式：开启即开始转运
}
```

> **关键注意事项：**
> - DMA 时钟在 **AHB** 总线上，不是 APB！用 `RCC_AHBPeriphClockCmd`
> - **软件触发 (M2M) 不能自动重装** —— BufferSize 转运完就停了
> - 硬件触发通道的映射关系要查 DMA 通道映射表（比如 ADC1 对应 DMA1_Channel1）
> - 转运 ADC1->DR 时 `DMA_PeripheralInc = DISABLE`（始终读同一个寄存器）

### 非自动重装重新触发

```c
void MyDMA_Transfer(void)
{
    DMA_Cmd(DMA1_Channel1, DISABLE);           // 先关 DMA
    DMA_SetCurrDataCounter(DMA1_Channel1, MyDMA_Size); // 重设 BufferSize
    DMA_Cmd(DMA1_Channel1, ENABLE);            // 再开启

    while (DMA_GetFlagStatus(DMA1_FLAG_TC1) == RESET); // 等待完成
    DMA_ClearFlag(DMA1_FLAG_TC1);                       // 清标志
}
```

---

## HAL 库对照

```c
void MyDMA_Transfer(uint32_t AddrA, uint32_t AddrB, uint32_t MyDMA_Size)
{
    HAL_DMA_Start(&hdma_memtomem_dma1_channel1, AddrA, AddrB, MyDMA_Size);
    HAL_DMA_PollForTransfer(&hdma_memtomem_dma1_channel1, HAL_DMA_FULL_TRANSFER, HAL_MAX_DELAY);
}
```

> **HAL 注意事项：** NVIC 设置里把 "Force DMA channels Interrupts" 关了。

---

## 相关笔记

- [[06-ADC]]（ADC + DMA 连续采集）
- [[04-USART]]（DMA 串口发送）
