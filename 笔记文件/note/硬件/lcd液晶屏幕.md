# LCD 液晶屏幕：从物理原理到 STM32 驱动

> [!abstract] 一句话理解
> LCD 面板是一组由电场控制透光率的微型“光阀”；STM32 通常不直接驱动液晶分子，而是把命令和像素数据交给显示控制器，再由控制器完成显存管理、扫描和像素电压驱动。

> [!warning] 型号差异
> 本文用 ST7789/ILI9341 一类控制器说明通用思路。初始化寄存器、命令参数、颜色顺序、坐标偏移、最高 SPI 频率和复位时序必须以**控制器数据手册、面板规格书和模块原理图**为准，不能整段照抄别人的初始化代码。

## 目录

- [[#01 先建立完整思维模型]]
- [[#02 LCD 为什么能控制亮暗和颜色]]
- [[#03 TFT、像素电容与行列扫描]]
- [[#04 MCU、显示控制器与显存]]
- [[#05 颜色格式与显存计算]]
- [[#06 常见接口：SPI、8080、RGB 与 MIPI DSI]]
- [[#07 刷新率、带宽与 RGB 时序]]
- [[#08 SPI LCD 驱动流程与完整示例]]
- [[#09 DMA 刷屏：速度、状态与缓冲区生命周期]]
- [[#10 图形、字体、LVGL 与软件分层]]
- [[#11 FreeRTOS 中怎样安全管理 LCD]]
- [[#12 触摸屏、OLED 与几个容易混淆的概念]]
- [[#13 故障排查与选型清单]]
- [[#最后记住这条链路]]

---

## 01 先建立完整思维模型

从程序到人眼看到图像，中间至少经过四层：

```text
软件层：控件、字体、图片、绘图 API
                    ↓ 产生像素
驱动层：坐标窗口、命令、RGB565 数据、DMA
                    ↓ SPI / 8080 / RGB 等接口
控制器层：寄存器、GRAM、扫描时序、源极/栅极驱动
                    ↓ 像素电压
面板层：TFT + 液晶 + 偏振片 + 彩色滤光片 + 背光
                    ↓
                  人眼
```

以画一个红点为例：

```text
LCD_DrawPoint(100, 50, RED)
        ↓
设置写入窗口 (100,50)～(100,50)
        ↓
发送红色 RGB565：0xF800
        ↓
控制器更新对应 GRAM/像素通道
        ↓
行列扫描把数值转换为像素驱动电压
        ↓
红色子像素透光，眼睛看到红点
```

后面的 ST7789、ILI9341、DMA、LVGL、FMC、LTDC、Framebuffer 都能放回这条链理解。

---

## 02 LCD 为什么能控制亮暗和颜色

### 2.1 LCD 通常不主动发光

液晶层本身基本不发光。常见透射式 TFT-LCD 使用 LED 背光：

```text
LED 背光 → 导光板/扩散膜 → 较均匀的白光 → 液晶面板
```

调低背光 PWM 会让整块屏幕变暗；改变像素值则控制各子像素对光的调制。

| 控制对象 | 主要影响 |
|---|---|
| 背光亮度 | 整体亮度、功耗 |
| 像素值 | 局部颜色、灰度和图像内容 |

有些反射式或半透反射式 LCD 不依赖同样的背光结构，本文主要讨论常见彩色透射式 TFT-LCD。

### 2.2 偏振片和液晶是“光阀”的核心

第一片偏振片只让特定偏振方向通过；液晶分子的排列会影响光的偏振状态；第二片偏振片再把这种变化转换成透光量变化。

```text
背光 → 后偏振片 → 液晶层 → 前偏振片 → 人眼
                     ↑
                 电场改变排列
```

> [!important] 不能机械记成“没电亮、加电黑”
> 透光率随电压怎样变化取决于 TN/IPS 等工作模式、偏振片方向、常白/常黑设计和 Gamma 电压。应记住“电压控制透光率”，而不是把某一块屏的亮暗方向当成所有 LCD 的规则。

### 2.3 彩色来自 RGB 子像素

```text
Pixel(x,y)
├─ R 子像素：红色滤光片
├─ G 子像素：绿色滤光片
└─ B 子像素：蓝色滤光片
```

控制三个子像素的透光程度，就能在观察距离上混合出颜色：

```text
R 高、G 低、B 低 → 红色
R 高、G 高、B 低 → 黄色
R 高、G 低、B 高 → 紫色
R/G/B 都高         → 接近白色
R/G/B 都低         → 接近黑色
```

黑色不绝对黑，是因为实际结构难以完全阻断背光；边缘装配应力和视角还可能造成漏光或 IPS glow。响应时间来自液晶分子重新排列所需的时间，低温时通常会变慢。

---

## 03 TFT、像素电容与行列扫描

### 3.1 TFT 是每个子像素旁的开关

TFT 是 Thin-Film Transistor，薄膜晶体管。主动矩阵 LCD 为每个子像素配一个开关器件和保持电容：

```text
Gate 行选通信号
        ↓
      TFT 开关 ← Source 列电压
        ↓
  像素电极 + 像素电容
        ↓
   液晶层的有效电场
```

- Gate Driver 逐行选通 TFT。
- Source Driver 给各列提供该行需要的模拟灰阶电压。
- TFT 导通时给像素电容充电。
- 行选通结束后，电容帮助维持电压，直到下一次刷新。

### 3.2 行列扫描怎样完成一帧

```text
选中第 0 行 → 所有列写入这一行 RGB 子像素电压
选中第 1 行 → 所有列写入下一行
...
选中最后一行 → 完成一帧 → 回到顶部
```

刷新率 60 Hz 表示一秒大约扫描 60 帧。像素电容和人眼视觉特性使画面看起来连续。

### 3.3 为什么使用交流极性反转

液晶材料不适合长期承受同方向直流分量。显示驱动会让像素电极相对公共电极 VCOM 的极性按帧、行、列或点变化，同时尽量保持目标灰阶：

```text
真正关心的是 Vpixel - VCOM 的有效大小与极性策略
目标亮度可以不变，但差分电压极性周期性反转
```

这比把像素简单理解成“对地 +3 V、-3 V”更准确。VCOM、Gamma 和反转策略通常由显示驱动 IC 管理，MCU 只传数字像素值。

### 3.4 TN 与 IPS

- TN 主要利用液晶扭转随电场变化，结构简单、响应可以较快，但视角和颜色稳定性通常较弱。
- IPS 让液晶分子主要在面板平面内转动，视角和颜色一致性通常更好，但结构、透光效率和漏光表现不同。

它们仍遵守同一主线：**TFT 控制像素电场，液晶改变光学状态，偏振与滤色形成图像。**

---

## 04 MCU、显示控制器与显存

### 4.1 STM32 通常不直接控制每个 TFT

常见小尺寸 SPI 模块内部带 ST7735、ST7789、ILI9341、GC9A01 等控制器：

```text
STM32 → SPI / 8080 → 显示控制器 → Source/Gate Driver → TFT-LCD
```

STM32 负责“画什么”；控制器负责“怎样扫描并产生像素驱动”。控制器相同，也可能因面板尺寸、坐标偏移、Gamma 和模组布线不同而需要不同初始化参数。

### 4.2 GRAM 与 Framebuffer

GRAM 是显示控制器内部用于保存像素数据的图形 RAM。带 GRAM 的 SPI LCD 可以在写完图像后自行持续刷新，因此 MCU 不必持续重发整帧。

| 架构 | 帧数据常在哪里 | MCU 怎样更新 |
|---|---|---|
| SPI/8080 智能控制器 | 控制器内部 GRAM | 设置窗口，再写像素 |
| STM32 LTDC + RGB 屏 | MCU SRAM 或外部 SDRAM | CPU/DMA2D 改 framebuffer，LTDC 持续读取 |
| 独立显示处理器 | 外部控制器自己的显存 | 通过对应主机接口访问 |

裸 RGB 面板通常要求外部控制器持续提供像素流，本身并不等价于带完整 GRAM 的 SPI 模块。

### 4.3 控制器做什么

```text
命令：睡眠、像素格式、扫描方向、显示窗口、Gamma/电源参数
数据：写入地址映射后的 GRAM
输出：按内部时序扫描并产生像素电压
```

初始化表不是魔法数字。每个字节都应在控制器数据手册或模组厂商资料中找到依据。

---

## 05 颜色格式与显存计算

### 5.1 RGB565

```text
bit 15             11 10               5 4                 0
┌────────────────────┬────────────────────┬──────────────────┐
│       R：5 bit      │       G：6 bit     │      B：5 bit     │
└────────────────────┴────────────────────┴──────────────────┘
```

| 颜色 | RGB565 |
|---|---:|
| 红 | `0xF800` |
| 绿 | `0x07E0` |
| 蓝 | `0x001F` |
| 白 | `0xFFFF` |
| 黑 | `0x0000` |

```c
static uint16_t rgb888_to_565(uint8_t r, uint8_t g, uint8_t b)
{
    return (uint16_t)(((uint16_t)(r & 0xF8U) << 8) |
                      ((uint16_t)(g & 0xFCU) << 3) |
                      ((uint16_t)b >> 3));
}
```

### 5.2 字节顺序与 RGB/BGR 是两类问题

假设红色是 `0xF800`，8 位 SPI 常见顺序是先发高字节 `0xF8`，再发低字节 `0x00`，但必须看控制器接口模式。

- 颜色整体异常：检查 MCU 端序、SPI 数据宽度和字节顺序。
- 红蓝互换：优先检查 RGB/BGR 配置位及图片资源格式。

不能用同一个“交换字节”盲修两类问题。

### 5.3 一帧需要多少内存

```text
Framebuffer 字节数 = 水平像素 × 垂直像素 × 每像素字节数
```

| 分辨率与格式 | 一帧大小 |
|---|---:|
| 320 × 240，RGB565 | 153,600 B ≈ 150 KiB |
| 800 × 480，RGB565 | 768,000 B ≈ 750 KiB |
| 800 × 480，ARGB8888 | 1,536,000 B ≈ 1.46 MiB |

双缓冲再乘 2，还要加图层、绘制缓存、字库和其他程序内存。选 STM32 与 SDRAM 时必须先算内存和带宽。

---

## 06 常见接口：SPI、8080、RGB 与 MIPI DSI

| 接口 | 传输思想 | 优点 | 主要代价 | 常见场景 |
|---|---|---|---|---|
| SPI | 串行发送控制器命令和像素 | 引脚少、入门容易 | 全屏带宽有限 | 小尺寸 MCU 屏 |
| 8080 并口 | 8/16 位数据总线 + WR/RD | 写入快、可配 FMC/FSMC | 引脚多 | 中等分辨率控制器屏 |
| RGB | 按像素时钟连续输出一帧 | 适合持续高带宽刷新 | 要 LTDC、framebuffer，常需 SDRAM | 中大尺寸面板 |
| MIPI DSI | 差分高速串行显示链路 | 高带宽、引脚相对少 | 硬件与协议复杂 | 高分辨率面板 |

### 6.1 SPI LCD 常见引脚

```text
SCK：时钟      MOSI：MCU → LCD 数据
MISO：可选读取 CS：片选
DC/RS：命令/数据选择
RST：硬件复位  BL：背光控制
```

部分模块只引出写方向，读取 ID 的驱动会失败。还要确认逻辑电平，以及 BL 是否需要 MOSFET/恒流电路，不能默认由 GPIO 直接承受背光电流。

### 6.2 8080 + FSMC/FMC

STM32 的 FSMC/FMC 可把外部 LCD 控制器映射成类似存储器的访问；地址线的一位常用于区分命令和数据。但地址、数据建立和保持时间必须按资料配置，“能亮”不等于时序可靠。

### 6.3 RGB + LTDC

RGB 接口常见 R/G/B、PCLK、HSYNC、VSYNC、DE。LTDC 按固定节奏从 framebuffer 读取像素并持续输出。除了面板时序，还要考虑存储器吞吐、总线竞争、图层格式、缓存一致性和双缓冲。

---

## 07 刷新率、带宽与 RGB 时序

### 7.1 SPI 全屏刷新上限

```text
理论时间 = 宽 × 高 × 每像素位数 ÷ SPI 位速率
```

320 × 240、RGB565、40 Mbit/s：

```text
1,228,800 bit ÷ 40,000,000 ≈ 30.72 ms
理论上限约 32.5 帧/秒
```

真实结果还受命令、窗口切换、SPI 间隙、HAL 开销、DMA 分段和控制器限频影响。优化顺序通常是：

1. 只刷新变化区域；
2. 一次设置窗口后连续发送像素；
3. 减少逐像素调用和 CS/DC 切换；
4. 使用 DMA 传大块数据；
5. 在硬件允许范围内提高总线速度。

DMA 减少 CPU 搬运，但不会突破 SPI 链路的比特率上限。

### 7.2 RGB 面板时序

```text
一行：HSYNC + HBP + HACT + HFP
一帧：VSYNC + VBP + VACT + VFP

Htotal = HSYNC + HBP + HACT + HFP
Vtotal = VSYNC + VBP + VACT + VFP
Pixel Clock ≈ Htotal × Vtotal × 刷新率
```

有效区 800 × 480 不代表只按 `800 × 480 × 60` 计算，因为同步和消隐也占时钟。极性、前后肩和像素时钟范围必须查面板规格书。

### 7.3 撕裂与双缓冲

显示控制器读取 framebuffer 的同时，CPU 若改写同一块区域，一帧可能混入两次绘制结果而撕裂。双缓冲让前台缓冲显示、后台缓冲绘制，并在垂直消隐等合适时机交换，但会接近翻倍占用帧缓冲内存。

---

## 08 SPI LCD 驱动流程与完整示例

### 8.1 上电初始化到底做什么

典型流程是：

```text
电源与时钟稳定
  ↓
硬件 RST，并满足数据手册延时
  ↓
Sleep Out，等待内部电路稳定
  ↓
设置像素格式、扫描方向、RGB/BGR、Gamma/电源参数
  ↓
Display On
  ↓
最后打开背光，避免把初始化花屏显示给用户
```

常见 DCS 风格命令有 `0x11` Sleep Out、`0x29` Display On、`0x2A` Column Address Set、`0x2B` Row/Page Address Set、`0x2C` Memory Write、`0x36` Memory Access Control、`0x3A` Pixel Format。**并非所有控制器的参数都相同。**

屏幕方向常由 MADCTL 一类寄存器控制 X/Y 翻转、XY 交换和 RGB/BGR。旋转后还要同步修改逻辑宽高和坐标偏移，否则可能只显示一部分或越界。

### 8.2 命令和数据怎样区分

```text
CS 有效
DC = 命令电平 → 发送命令字节
DC = 数据电平 → 发送该命令的参数或像素
CS 无效 → 本次事务结束
```

DC 具体高低、电源时序和 CS 是否允许在命令与参数间释放，应查控制器资料。下面代码假设：DC 低是命令、DC 高是数据，8 位 SPI 先发 RGB565 高字节。

### 8.3 带边界检查的阻塞式驱动骨架

这份代码展示层次和错误处理。引脚宏、句柄、屏幕尺寸及初始化表必须替换为实际工程配置。

```c
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include "main.h"

extern SPI_HandleTypeDef hspi1;

#define LCD_WIDTH   240U
#define LCD_HEIGHT  320U

#define LCD_CS_LOW()   HAL_GPIO_WritePin(LCD_CS_GPIO_Port, LCD_CS_Pin, GPIO_PIN_RESET)
#define LCD_CS_HIGH()  HAL_GPIO_WritePin(LCD_CS_GPIO_Port, LCD_CS_Pin, GPIO_PIN_SET)
#define LCD_DC_CMD()   HAL_GPIO_WritePin(LCD_DC_GPIO_Port, LCD_DC_Pin, GPIO_PIN_RESET)
#define LCD_DC_DATA()  HAL_GPIO_WritePin(LCD_DC_GPIO_Port, LCD_DC_Pin, GPIO_PIN_SET)

/* HAL1 的 Size 常为 uint16_t，所以长数据主动分块。
 * 这里是便于学习的阻塞版本；实时任务中不要无限阻塞。 */
static bool lcd_spi_write(const uint8_t *data, size_t size)
{
    if ((data == NULL) && (size != 0U))
    {
        return false;
    }

    while (size != 0U)
    {
        uint16_t chunk = (size > UINT16_MAX) ? UINT16_MAX : (uint16_t)size;

        if (HAL_SPI_Transmit(&hspi1, (uint8_t *)data,
                             chunk, HAL_MAX_DELAY) != HAL_OK)
        {
            return false;
        }

        data += chunk;
        size -= chunk;
    }
    return true;
}

/* 一次完成“命令 + 参数”，CS 在整个寄存器事务中保持有效。 */
static bool lcd_write_reg(uint8_t command,
                          const uint8_t *parameters,
                          size_t parameter_count)
{
    bool ok;

    LCD_CS_LOW();
    LCD_DC_CMD();
    ok = lcd_spi_write(&command, 1U);

    if (ok && (parameter_count != 0U))
    {
        LCD_DC_DATA();
        ok = lcd_spi_write(parameters, parameter_count);
    }

    LCD_CS_HIGH();
    return ok;
}

/* 设置写窗口后发 Memory Write，并保持 CS 为低。
 * 成功后调用者必须写像素，最后调用 lcd_end_pixel_stream()。 */
static bool lcd_begin_pixel_stream(uint16_t x1, uint16_t y1,
                                   uint16_t x2, uint16_t y2)
{
    const uint8_t columns[4] = {
        (uint8_t)(x1 >> 8), (uint8_t)x1,
        (uint8_t)(x2 >> 8), (uint8_t)x2
    };
    const uint8_t rows[4] = {
        (uint8_t)(y1 >> 8), (uint8_t)y1,
        (uint8_t)(y2 >> 8), (uint8_t)y2
    };
    uint8_t memory_write = 0x2CU;

    /* 0x2A/0x2B/0x2C 是本例控制器使用的命令，换型号必须核对。 */
    if (!lcd_write_reg(0x2AU, columns, sizeof(columns)) ||
        !lcd_write_reg(0x2BU, rows, sizeof(rows)))
    {
        return false;
    }

    LCD_CS_LOW();
    LCD_DC_CMD();
    if (!lcd_spi_write(&memory_write, 1U))
    {
        LCD_CS_HIGH();
        return false;
    }

    LCD_DC_DATA();
    return true;              // CS 仍为低，像素流不能被其他 SPI 使用者插入
}

static void lcd_end_pixel_stream(void)
{
    LCD_CS_HIGH();
}

bool lcd_fill_rect(uint16_t x, uint16_t y,
                   uint16_t width, uint16_t height,
                   uint16_t rgb565)
{
    uint8_t block[128];       // 64 个 RGB565 像素；避免为整块矩形分配大数组
    uint32_t x_end;
    uint32_t y_end;
    uint32_t pixel_count;

    if ((width == 0U) || (height == 0U) ||
        (x >= LCD_WIDTH) || (y >= LCD_HEIGHT))
    {
        return false;
    }

    /* 用 32 位做加法，避免 uint16_t 的 x + width 先溢出。 */
    x_end = (uint32_t)x + width;
    y_end = (uint32_t)y + height;
    if (x_end > LCD_WIDTH)  { x_end = LCD_WIDTH; }
    if (y_end > LCD_HEIGHT) { y_end = LCD_HEIGHT; }

    pixel_count = (x_end - x) * (y_end - y);

    /* 8 位 SPI 按高字节、低字节排列。 */
    for (size_t i = 0U; i < sizeof(block); i += 2U)
    {
        block[i]     = (uint8_t)(rgb565 >> 8);
        block[i + 1] = (uint8_t)rgb565;
    }

    if (!lcd_begin_pixel_stream(x, y,
                                (uint16_t)(x_end - 1U),
                                (uint16_t)(y_end - 1U)))
    {
        return false;
    }

    while (pixel_count != 0U)
    {
        uint32_t pixels_this_time =
            (pixel_count > 64U) ? 64U : pixel_count;

        if (!lcd_spi_write(block, pixels_this_time * 2U))
        {
            lcd_end_pixel_stream();    // 出错也必须释放 CS
            return false;
        }
        pixel_count -= pixels_this_time;
    }

    lcd_end_pixel_stream();
    return true;
}
```

### 8.4 从画点到画图形

- 画点：设置 1 × 1 窗口，写一个颜色，直观但函数开销大。
- 水平/垂直线：设置一条连续窗口，批量写颜色。
- 任意直线：可用 Bresenham 算法计算像素，但逐点 SPI 更新很慢。
- 填充矩形：设置一个矩形窗口，连续写相同颜色。
- 图片：设置图片窗口，连续写像素数组。

性能关键不是“画点算法写得短”，而是尽量把零散操作合并成连续像素流。

---

## 09 DMA 刷屏：速度、状态与缓冲区生命周期

### 9.1 DMA 改变了谁搬数据

```text
阻塞发送：CPU 反复把 RAM 数据交给 SPI
DMA 发送：CPU 配置一次 → DMA 搬运 RAM → SPI → LCD
```

DMA 可以释放 CPU，但传输仍需要总线时间。`HAL_SPI_Transmit_DMA()` 返回通常只表示“传输已成功启动”，不是所有字节已经到达 LCD。

### 9.2 四条硬规则

1. DMA 完成前，源缓冲区必须继续存在，不能是已经退出函数的局部数组。
2. DMA 完成前，不能修改仍在传输的区域。
3. 像素流完成前不能让其他代码切换同一 LCD 的 CS/DC，也不能无保护地占用共享 SPI。
4. 只有完成/错误回调处理状态后，下一块传输才能安全开始。

在带数据缓存的 Cortex-M7/M55 等芯片上，还要处理 DMA 与 D-Cache 一致性；STM32F103 没有这类数据缓存问题，但仍有缓冲区生命周期和并发问题。

### 9.3 HAL1 单块 DMA 模式示意

下面的状态变量只适用于“唯一 GUI/显示任务发起传输”的模型；`volatile` 只是保证实际读写，不是多任务互斥锁。若允许多个调用者，必须在更高层统一排队或保护整个显示事务。

```c
static volatile bool lcd_dma_busy;
static volatile bool lcd_dma_error;
static TaskHandle_t lcd_waiting_task;

/* pixel_bytes 必须是静态区、堆区或其他能活到回调结束的缓冲区。
 * 调用前已经设置好窗口；本函数让 CS 保持有效直到回调。 */
bool lcd_start_dma_pixels(uint8_t *pixel_bytes, uint16_t byte_count,
                          TaskHandle_t waiting_task)
{
    if (lcd_dma_busy || (pixel_bytes == NULL) || (byte_count == 0U))
    {
        return false;
    }

    lcd_dma_busy = true;
    lcd_dma_error = false;
    lcd_waiting_task = waiting_task;

    /* lcd_begin_pixel_stream() 在这里省略坐标参数，仅强调异步状态。
     * 实际驱动应在启动 DMA 前完成窗口和 0x2C 命令。 */
    if (HAL_SPI_Transmit_DMA(&hspi1, pixel_bytes, byte_count) != HAL_OK)
    {
        lcd_dma_busy = false;
        lcd_waiting_task = NULL;
        LCD_CS_HIGH();
        return false;
    }
    return true;
}

void HAL_SPI_TxCpltCallback(SPI_HandleTypeDef *hspi)
{
    if (hspi == &hspi1)
    {
        BaseType_t higher_priority_task_woken = pdFALSE;
        TaskHandle_t task = lcd_waiting_task;

        LCD_CS_HIGH();                 // 像素事务到这里才真正结束
        lcd_waiting_task = NULL;
        lcd_dma_error = false;
        lcd_dma_busy = false;

        if (task != NULL)
        {
            vTaskNotifyGiveFromISR(task, &higher_priority_task_woken);
        }
        portYIELD_FROM_ISR(higher_priority_task_woken);
    }
}

void HAL_SPI_ErrorCallback(SPI_HandleTypeDef *hspi)
{
    if (hspi == &hspi1)
    {
        BaseType_t higher_priority_task_woken = pdFALSE;
        TaskHandle_t task = lcd_waiting_task;

        /* 错误路径也必须唤醒等待任务，否则它可能永久阻塞。 */
        LCD_CS_HIGH();
        lcd_waiting_task = NULL;
        lcd_dma_error = true;          // 任务醒来后据此判断刷新失败
        lcd_dma_busy = false;

        if (task != NULL)
        {
            vTaskNotifyGiveFromISR(task, &higher_priority_task_woken);
        }
        portYIELD_FROM_ISR(higher_priority_task_woken);
    }
}
```

等待任务收到通知后必须检查 `lcd_dma_error`，成功与失败不能只用同一个通知无条件当成成功。这仍只是状态模式，不是可直接复制的完整驱动：窗口参数、超时恢复、多块 DMA 链接和共享 SPI 仲裁仍需补齐。如果工程中还有其他 SPI 设备也使用 HAL 回调，应在同一个回调里按句柄分发，不能重复定义同名函数。不同 STM32 HAL 版本的句柄、长度类型和回调注册方式可能不同，应以当前工程头文件为准。

### 9.4 大图怎样分块

若 HAL/DMA 一次传输长度有限，可使用两个长期存在的绘制缓冲区：

```text
CPU/LVGL 填充 Buffer A → DMA 发送 A
CPU/LVGL 同时填充 Buffer B
DMA 完成 A → 发送 B → CPU 重新填 A
```

这叫 ping-pong/double draw buffer。每次只能重用已确认完成的那一块，不能只凭固定延时猜 DMA 已结束。

---

## 10 图形、字体、LVGL 与软件分层

### 10.1 字符怎样显示

点阵字体把一个字符保存为若干位：1 表示前景像素，0 表示背景或透明。8 × 16 的单色字符需要：

```text
8 × 16 = 128 bit = 16 Byte
```

16 × 16 汉字需要 32 Byte；大量汉字、多个字号和抗锯齿会显著增加 Flash。可按项目选择子集字库、外部 Flash、LVGL 字体或 FreeType 等方案。

### 10.2 LVGL 不是底层 LCD 驱动

```text
应用：按钮、仪表、状态页面
  ↓
LVGL：布局、控件、字体、绘制和脏区域
  ↓ flush 回调
BSP/控制器驱动：窗口、像素格式、DMA
  ↓
SPI/FMC/LTDC → LCD
```

LVGL 告诉底层“把这块像素刷到指定区域”，底层仍要正确实现显示接口、缓冲区和完成通知。

### 10.3 推荐的软件分层

```text
Application
  ↓
GUI / LVGL
  ↓
BSP LCD：尺寸、方向、背光、公共绘图接口
  ↓
Controller Driver：ST7789/ILI9341 命令与窗口
  ↓
Bus Driver：HAL SPI / DMA / FMC / LTDC
  ↓
Hardware
```

不要把页面逻辑、字库解析、控制器寄存器和 HAL 调用全部塞进 `main.c`。

---

## 11 FreeRTOS 中怎样安全管理 LCD

### 11.1 单一所有者原则

多个任务同时写 LCD 会破坏“命令→参数→像素”的连续事务：

```text
Task A：设置窗口 A → [被抢占]
Task B：设置窗口 B → 写数据
Task A：继续写数据，但当前窗口已经变成 B
```

推荐只有 GUI Task 操作 LCD；其他任务通过队列或通知更新界面模型：

```text
Sensor Task ─┐
Motor Task ──┼─ Queue/Event → GUI Task → LVGL/LCD → DMA
Comm Task ───┘
```

### 11.2 小型消息按值传递

```c
typedef struct
{
    float temperature;
    uint8_t sensor_ok;
} UiSensorMessage;

static QueueHandle_t ui_queue;

void SensorTask(void *argument)
{
    for (;;)
    {
        UiSensorMessage message;
        message.sensor_ok = Sensor_Read(&message.temperature);

        /* 队列复制整个小结构体，局部变量在发送后可以安全离开作用域。 */
        (void)xQueueOverwrite(ui_queue, &message); // 此用法要求队列长度为 1
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

void GuiTask(void *argument)
{
    UiSensorMessage message;

    for (;;)
    {
        if (xQueueReceive(ui_queue, &message,
                          pdMS_TO_TICKS(20)) == pdPASS)
        {
            Gui_SetTemperature(message.temperature, message.sensor_ok);
        }

        Lvgl_RunOneStep(); // 具体 API 与节拍方式以当前 LVGL 版本移植为准
    }
}
```

队列里若传指针，只复制地址，不复制指向的数据。必须定义缓冲区何时有效、谁能修改、谁负责释放。

### 11.3 DMA 与 RTOS 同步

GUI Task 发起 DMA 后可以阻塞等待完成通知，让 CPU 运行其他任务。ISR 中只能使用对应 `...FromISR()` API，并且 SPI/DMA 中断优先级必须位于 FreeRTOS 允许调用内核 API 的范围，参见 [[freertos/配置文件#7. 中断优先级：最容易出错的部分]]。

若多个设备共享一条 SPI，总线互斥锁要覆盖完整事务；DMA 期间不能提前释放互斥锁。更简单的办法是让一个总线/显示任务成为唯一所有者。

---

## 12 触摸屏、OLED 与几个容易混淆的概念

### 12.1 触摸和显示通常是两套链路

```text
STM32 ── SPI/FMC/RGB ──> LCD：负责显示
STM32 <─ I²C/SPI/ADC ── Touch Controller：负责坐标输入
```

常见例子：XPT2046 电阻触摸控制器，FT6x36/GT911 一类电容触摸控制器。即使触摸层贴在 LCD 上，它也可能有独立供电、复位、中断、地址和驱动。

旋转屏幕后，不仅要改 LCD 地址映射，也要同步变换触摸坐标：交换 XY、镜像，并重新考虑有效范围与校准。

### 12.2 LCD 与 OLED

| 项目 | TFT-LCD | OLED |
|---|---|---|
| 发光方式 | 通常依赖背光并调制透光 | 像素自发光 |
| 黑色 | 仍可能有漏光 | 像素关闭时黑色通常更深 |
| 背光 | 常需要 | 不需要独立背光层 |
| 老化 | 面板与背光都有寿命因素 | 有机材料可能老化、烧屏 |
| 驱动接口 | SPI/8080/RGB/DSI 等 | 同样可能使用 SPI、并口等 |

“使用 SPI”只说明 MCU 接口，不说明面板一定是 LCD 或 OLED；“TFT”描述主动矩阵晶体管技术，也不等于具体接口。

---

## 13 故障排查与选型清单

### 13.1 不亮、白屏、黑屏

按层排查：

1. 电源、电压和地是否正确，电流是否异常；
2. 背光是否真的点亮，BL 极性和驱动能力是否正确；
3. RST 波形和上电延时是否满足资料；
4. SPI Mode、频率、CS/DC 和引脚复用是否正确；
5. 控制器型号、初始化表和像素格式是否匹配；
6. 用逻辑分析仪观察是否实际发出了命令与参数。

背光亮只证明背光链路工作，不证明显示控制器已经初始化。

### 13.2 图像错位、缺边或方向错误

- 核对面板有效区域与控制器 GRAM 尺寸；
- 检查 X/Y 起始偏移；
- 检查窗口终点是包含式还是排除式；
- 旋转后更新逻辑宽高、MADCTL 和偏移表；
- 检查坐标加法是否溢出或产生 `x2 < x1`。

### 13.3 颜色异常

| 现象 | 优先检查 |
|---|---|
| 红蓝互换 | RGB/BGR 位、资源格式 |
| 每个颜色都很怪 | RGB565 字节顺序、SPI 8/16 位模式 |
| 渐变断层 | 像素格式、Gamma、颜色转换精度 |
| 随机彩点 | SPI 过快、信号完整性、电源、DMA 缓冲区被改写 |

先发送红、绿、蓝、白、黑五个纯色屏，比直接显示复杂图片更容易定位格式问题。

### 13.4 闪烁、撕裂和偶发花屏

- 闪烁：是否重复清屏、背光 PWM 频率过低、供电不稳；
- 撕裂：写入时机与扫描不同步，考虑局部刷新、TE 信号或双缓冲；
- 偶发花屏：检查 DMA 完成前缓冲区是否被重用、CS 是否提前释放、共享 SPI 是否并发访问；
- 运行一段时间才坏：检查栈、数组越界、缓存一致性和错误恢复路径。

### 13.5 初始化“能亮但颜色不好”

不要随机修改 Gamma 和电源寄存器碰运气。先拿到精确的面板/模组资料，确认控制器版本、参考初始化和测量条件；不同玻璃面板可能需要不同参数。

### 13.6 选屏前的计算与确认

- [ ] 分辨率、物理尺寸、视角和亮度是否满足需求？
- [ ] 控制器准确型号和数据手册是否能获得？
- [ ] 模块逻辑电平、供电和背光电流多大？
- [ ] MCU 是否有合适接口和足够引脚？
- [ ] 全屏数据量、目标刷新率和接口带宽是否算过？
- [ ] 单/双 framebuffer、字库、LVGL 缓冲和程序能否放进 RAM/SDRAM？
- [ ] 是否需要触摸，触摸控制器和坐标映射是什么？
- [ ] DMA、缓存、RTOS 并发和共享总线怎样管理？
- [ ] 是否有原理图、初始化参考和长期供应渠道？

---

## 最后记住这条链路

```text
应用决定画什么
      ↓
GUI/LVGL 生成像素或刷新区域
      ↓
LCD 驱动设置窗口和像素格式
      ↓
SPI / DMA / FMC / LTDC 搬运数据
      ↓
控制器 GRAM 或 MCU Framebuffer
      ↓
行列扫描、像素电压、TFT 与液晶
      ↓
偏振片控制透光，RGB 滤色形成颜色
      ↓
人眼看到图像
```

遇到问题时，先判断故障属于：**物理面板、电源与引脚、总线时序、控制器配置、颜色数据、DMA/缓存、还是软件并发。** 分层后再测量，不要只在初始化数组里盲改数字。

## 相关笔记

- [[freertos/任务管理]]
- [[freertos/配置文件]]
- [[标准库/04-USART|USART 与 DMA 思路参考]]

## 参考资料

- [ST AN4861：STM32 LTDC 控制器、时序、Framebuffer 与带宽](https://www.st.com/resource/en/application_note/dm00287603-lcd-tft-display-controller-ltdc-on-stm32-mcus-stmicroelectronics.pdf)
- [ST：HAL1 到 HAL2 的 SPI DMA 使用差异](https://dev.st.com/stm32cube-docs/hal1-to-hal2-migration/1.1.0/en/docs/markup/drivers_documentation/hal_drivers/spi/hal_spi_use_cases.html)

具体屏幕驱动仍应优先查控制器原始数据手册、面板规格书和模块原理图。
