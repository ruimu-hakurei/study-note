[[各种器件，外设]]## 一、整体架构说明


这份代码用**GPIO 引脚手动模拟 I2C 时序**（软件 I2C），不依赖 STM32 硬件 I2C 外设，优点是引脚可任意选择、移植性强，缺点是速度略慢、占用 CPU。 代码分层逻辑：

1. **底层 I2C 时序层**：模拟 I2C 起始、停止、发字节的物理时序
2. **OLED 协议层**：按照 SSD1306 控制器规则，发送命令 / 显存数据
3. **功能应用层**：光标设置、清屏、字符 / 数字 / 字符串显示
4. **初始化层**：上电后配置 OLED 控制器的所有寄存器

---

## 二、引脚宏定义与初始化

```
/*引脚配置*/
#define OLED_W_SCL(x) HAL_GPIO_WritePin(SCL_GPIO_Port, SCL_Pin, (GPIO_PinState)(x))
#define OLED_W_SDA(x) HAL_GPIO_WritePin(SDA_GPIO_Port, SDA_Pin, (GPIO_PinState)(x))
```

- 用宏封装了 HAL 库的 GPIO 写电平函数，操作 SCL（时钟线）和 SDA（数据线）的高低电平。
- `SCL_GPIO_Port`、`SCL_Pin` 是 CubeMX 生成的 GPIO 宏，你需要在 CubeMX 中把对应引脚配置为**推挽输出模式**（软件 I2C 也推荐开漏输出 + 外部上拉，推挽在短距离也可正常工作）。
- 参数 `x` 为 0 时输出低电平，为 1 时输出高电平，强转为 `GPIO_PinState` 类型匹配 HAL 库定义。

```
void OLED_I2C_Init(void)
{
    OLED_W_SCL(1);
    OLED_W_SDA(1);
}
```

- I2C 总线的**空闲状态**是 SCL 和 SDA 都为高电平，这个函数把总线拉到空闲状态。
- 注意：GPIO 硬件本身的初始化（时钟、模式）由 CubeMX 生成的 `MX_GPIO_Init()` 完成，此函数仅做总线电平初始化。

---

## 三、底层 I2C 时序函数

I2C 协议的核心规则：**SCL 高电平时，SDA 必须保持稳定；SCL 低电平时，SDA 才允许变化**。所有时序都必须遵守这个规则。

### 1. 起始信号

```
void OLED_I2C_Start(void)
{
    OLED_W_SDA(1);
    OLED_W_SCL(1);
    OLED_W_SDA(0);
    OLED_W_SCL(0);
}
```

- 时序动作：先确保 SDA、SCL 都为高（总线空闲）→ SDA 拉低 → SCL 拉低。
- 协议定义：**SCL 高电平时，SDA 由高变低**，代表 I2C 通信开始。
- 最后拉低 SCL，是为后续发送数据做准备（数据位在 SCL 低电平时改变）。

### 2. 停止信号

```
void OLED_I2C_Stop(void)
{
    OLED_W_SDA(0);
    OLED_W_SCL(1);
    OLED_W_SDA(1);
}
```

- 时序动作：SDA 拉低 → SCL 拉高 → SDA 拉高。
- 协议定义：**SCL 高电平时，SDA 由低变高**，代表 I2C 通信结束，总线回到空闲状态。

### 3. 发送一个字节

```
void OLED_I2C_SendByte(uint8_t Byte)
{
    uint8_t i;
    for (i = 0; i < 8; i++)
    {
        OLED_W_SDA(Byte & (0x80 >> i));
        OLED_W_SCL(1);
        OLED_W_SCL(0);
    }
    OLED_W_SCL(1);        //额外的一个时钟，不处理应答信号
    OLED_W_SCL(0);
}
```

- I2C 是**高位先行**，从 bit7 到 bit0 依次发送，循环 8 次发完 1 个字节。
- 每一位的发送逻辑：
    1. SCL 低电平时，设置 SDA 电平（`Byte & (0x80 >> i)` 提取当前位，非 0 即高电平）
    2. SCL 拉高：此时 SDA 稳定，OLED 从机在 SCL 高电平时读取数据
    3. SCL 拉低：准备下一位数据
- 末尾的额外时钟：标准 I2C 中，第 9 个时钟是**从机应答位（ACK）**，从机会把 SDA 拉低表示接收成功。
    - 这份代码直接忽略了应答检测，只产生一个时钟脉冲。
    - 原因：SSD1306 只要地址正确一定会应答，省略应答可以简化代码；代价是硬件故障时无法通过软件检测。

---

## 四、OLED 命令与数据写入

SSD1306 的 I2C 通信格式：

1. 先发**从机地址**：`0x78`（7 位地址`0x3C`左移 1 位，最低位为 0 表示写操作）
2. 再发**控制字节**：
    - `0x00`：后续字节是**命令**，用于配置 OLED 寄存器
    - `0x40`：后续字节是**显存数据**，写入后直接显示在屏幕上

### 1. 写命令

```
void OLED_WriteCommand(uint8_t Command)
{
    OLED_I2C_Start();
    OLED_I2C_SendByte(0x78);    //从机地址
    OLED_I2C_SendByte(0x00);    //写命令标记
    OLED_I2C_SendByte(Command); 
    OLED_I2C_Stop();
}
```

- 用于发送配置指令，比如设置光标位置、开关显示、调节对比度等。

### 2. 写数据

```
void OLED_WriteData(uint8_t Data)
{
    OLED_I2C_Start();
    OLED_I2C_SendByte(0x78);    //从机地址
    OLED_I2C_SendByte(0x40);    //写数据标记
    OLED_I2C_SendByte(Data);
    OLED_I2C_Stop();
}
```

- 用于向 OLED 的显存（GDDRAM）写入点阵数据，对应屏幕上的像素点亮 / 熄灭。

> 小优化点：当前代码每次写 1 字节都发起始 + 停止，效率较低。实际工程中可以一次起始后连续写多个字节，速度会明显提升。

---

## 五、显存与光标操作

### SSD1306 显存结构（页地址模式）

128×64 的屏幕，显存被分为 **8 页（Page 0~7）**，每页高 8 行像素、宽 128 列像素。

- 每 1 页 = 128 个字节，每个字节对应 1 列的 8 个像素（bit0 在最上方，bit7 在最下方）。
- 写入数据后，列地址会自动向后递增，写完一列自动到下一列。

### 1. 设置光标位置

```
void OLED_SetCursor(uint8_t Y, uint8_t X)
{
    OLED_WriteCommand(0xB0 | Y);                  //设置Y位置（页地址）
    OLED_WriteCommand(0x10 | ((X & 0xF0) >> 4));  //设置X位置高4位
    OLED_WriteCommand(0x00 | (X & 0x0F));         //设置X位置低4位
}
```

- 参数 `Y`：页号，范围 0~7，对应屏幕从上到下的 8 个页。
- 参数 `X`：列号，范围 0~127，对应屏幕从左到右的 128 列。
- 三条命令是 SSD1306 页地址模式下设置坐标的标准写法：
    - `0xB0 | Y`：低 3 位为页号，设置当前写入的页
    - 列地址分两次发：高 4 位和低 4 位，组合成 0~127 的列地址

### 2. 清屏

```
void OLED_Clear(void)
{  
    uint8_t i, j;
    for (j = 0; j < 8; j++)
    {
        OLED_SetCursor(j, 0);
        for(i = 0; i < 128; i++)
        {
            OLED_WriteData(0x00);
        }
    }
}
```

- 遍历 8 个页，每页从第 0 列开始，连续写入 128 个`0x00`。
- 所有显存清零后，屏幕全黑，完成清屏。
- 上电后显存是随机值，会显示乱码，所以初始化最后必须清屏。

---

## 六、字符与数字显示

所有显示函数都基于 **8×16 ASCII 字库**（存在`OLED_Font.h`的`OLED_F8x16`数组中）：

- 每个字符宽 8 像素、高 16 像素，占**2 个页、8 列**。
- 字库从空格（ASCII 32）开始索引，`Char - ' '` 即可得到字符在字库中的下标。
- 每个字符对应 16 个字节：前 8 字节是上半页点阵，后 8 字节是下半页点阵。

### 1. 显示单个字符

```
void OLED_ShowChar(uint8_t Line, uint8_t Column, char Char)
{       
    uint8_t i;
    OLED_SetCursor((Line - 1) * 2, (Column - 1) * 8);    //上半部分
    for (i = 0; i < 8; i++)
    {
        OLED_WriteData(OLED_F8x16[Char - ' '][i]);       //写上半页
    }
    OLED_SetCursor((Line - 1) * 2 + 1, (Column - 1) * 8);//下半部分
    for (i = 0; i < 8; i++)
    {
        OLED_WriteData(OLED_F8x16[Char - ' '][i + 8]);   //写下半页
    }
}
```

- 参数 `Line`：行号，范围 1~4（屏幕 64 行高 ÷ 字符 16 行高 = 4 行）
- 参数 `Column`：列号，范围 1~16（屏幕 128 列宽 ÷ 字符 8 列宽 = 16 列）
- 逻辑：分两次写入，先写上半页的 8 个字节，再把光标移到下一页，写下半页的 8 个字节。

### 2. 显示字符串

```
void OLED_ShowString(uint8_t Line, uint8_t Column, char *String)
{
    uint8_t i;
    for (i = 0; String[i] != '\0'; i++)
    {
        OLED_ShowChar(Line, Column + i, String[i]);
    }
}
```

- 遍历字符串，遇到结束符`\0`停止，逐个字符调用`OLED_ShowChar`显示。
- 注意：没有自动换行逻辑，字符串超出 16 列会溢出屏幕。

### 3. 次方辅助函数

```
uint32_t OLED_Pow(uint32_t X, uint32_t Y)
{
    uint32_t Result = 1;
    while (Y--)
    {
        Result *= X;
    }
    return Result;
}
```

- 计算 X 的 Y 次方，纯整数循环累乘。
- 作用：用于数字显示时，提取每一位的数值。

### 4. 显示无符号十进制数

```
void OLED_ShowNum(uint8_t Line, uint8_t Column, uint32_t Number, uint8_t Length)
{
    uint8_t i;
    for (i = 0; i < Length; i++)							
    {
        OLED_ShowChar(Line, Column + i, Number / OLED_Pow(10, Length - i - 1) % 10 + '0');
    }
}
```

- 从最高位到最低位依次提取每一位数字：
    - 公式：`数字 / 10^n % 10`，得到第 n 位的数值
    - 数值 + `'0'` 转换成对应 ASCII 字符
- `Length` 指定显示位数：位数不足时前面补 0，位数过多时高位被截断。

### 5. 显示有符号十进制数

```
void OLED_ShowSignedNum(uint8_t Line, uint8_t Column, int32_t Number, uint8_t Length)
{
    uint8_t i;
    uint32_t Number1;
    if (Number >= 0)
    {
        OLED_ShowChar(Line, Column, '+');
        Number1 = Number;
    }
    else
    {
        OLED_ShowChar(Line, Column, '-');
        Number1 = -Number;
    }
    for (i = 0; i < Length; i++)							
    {
        OLED_ShowChar(Line, Column + i + 1, Number1 / OLED_Pow(10, Length - i - 1) % 10 + '0');
    }
}
```

- 先判断正负，第一位显示`+`或`-`符号。
- 负数取绝对值后，后续数字显示逻辑和无符号一致，列号向后偏移 1 位（给符号位腾位置）。
- `Length` 是数字部分的长度，总显示宽度为 Length+1 列。

### 6. 显示十六进制数

```
void OLED_ShowHexNum(uint8_t Line, uint8_t Column, uint32_t Number, uint8_t Length)
{
    uint8_t i, SingleNumber;
    for (i = 0; i < Length; i++)							
    {
        SingleNumber = Number / OLED_Pow(16, Length - i - 1) % 16;
        if (SingleNumber < 10)
            OLED_ShowChar(Line, Column + i, SingleNumber + '0');
        else
            OLED_ShowChar(Line, Column + i, SingleNumber - 10 + 'A');
    }
}
```

- 基数为 16，每一位取值 0~15。
- 0~9 直接转成数字字符，10~15 转成大写字母 A~F。

### 7. 显示二进制数

```
void OLED_ShowBinNum(uint8_t Line, uint8_t Column, uint32_t Number, uint8_t Length)
{
    uint8_t i;
    for (i = 0; i < Length; i++)							
    {
        OLED_ShowChar(Line, Column + i, Number / OLED_Pow(2, Length - i - 1) % 2 + '0');
    }
}
```

- 基数为 2，每一位只能是 0 或 1，直接转成字符`0`或`1`。
- 适合调试时查看寄存器位状态。

---

## 七、OLED 初始化函数

```
void OLED_Init(void)
{
    uint32_t i, j;
    
    for (i = 0; i < 1000; i++)        //上电延时
        for (j = 0; j < 1000; j++);
    
    OLED_I2C_Init();                   //端口初始化
    
    OLED_WriteCommand(0xAE);           //关闭显示
    OLED_WriteCommand(0xD5); OLED_WriteCommand(0x80);  //时钟分频与振荡器
    OLED_WriteCommand(0xA8); OLED_WriteCommand(0x3F);  //多路复用率(64行)
    OLED_WriteCommand(0xD3); OLED_WriteCommand(0x00);  //显示偏移
    OLED_WriteCommand(0x40);           //显示起始行
    OLED_WriteCommand(0xA1);           //左右方向正常
    OLED_WriteCommand(0xC8);           //上下方向正常
    OLED_WriteCommand(0xDA); OLED_WriteCommand(0x12);  //COM引脚配置
    OLED_WriteCommand(0x81); OLED_WriteCommand(0xCF);  //对比度
    OLED_WriteCommand(0xD9); OLED_WriteCommand(0xF1);  //预充电周期
    OLED_WriteCommand(0xDB); OLED_WriteCommand(0x30);  //VCOMH电压
    OLED_WriteCommand(0xA4);           //全局显示跟随显存
    OLED_WriteCommand(0xA6);           //正常显示模式
    OLED_WriteCommand(0x8D); OLED_WriteCommand(0x14);  //开启电荷泵
    OLED_WriteCommand(0xAF);           //开启显示
            
    OLED_Clear();                      //清屏
}
```

这是 SSD1306 的标准初始化序列，逐条命令作用如下：

表格

| 命令             | 作用说明                                |
| -------------- | ----------------------------------- |
| 上电延时           | 等待 OLED 电源稳定，单片机上电比 OLED 快，避免命令发送失败 |
| `0xAE`         | 关闭显示，配置过程中先关屏，避免乱码闪烁                |
| `0xD5 + 0x80`  | 设置显示时钟分频和振荡器频率，默认值即可                |
| `0xA8 + 0x3F`  | 设置多路复用率，64 行屏幕对应 0x3F（值 = 行数 - 1）   |
| `0xD3 + 0x00`  | 显示垂直偏移，0 代表不偏移                      |
| `0x40`         | 设置显示起始行，从第 0 行开始显示                  |
| `0xA1`         | 段重映射，控制左右方向；0xA0 则左右翻转              |
| `0xC8`         | COM 扫描方向，控制上下方向；0xC0 则上下翻转          |
| `0xDA + 0x12`  | COM 引脚硬件配置，64 行屏幕标准配置               |
| `0x81 + 0xCF`  | 对比度调节，范围 0~255，值越大越亮                |
| `0xD9 + 0xF1`  | 预充电周期，保证像素充电充分                      |
| `0xDB + 0x30`  | VCOMH 电压等级，影响显示亮度                   |
| `0xA4`         | 全局显示模式，0xA4 = 跟随显存，0xA5 = 全亮        |
| `0xA6`         | 正常显示模式（0 灭 1 亮）；0xA7 为反显            |
| `0x8D + 0x14`  | 开启电荷泵，OLED 必须升压驱动，必开                |
| `0xAF`         | 开启显示，所有配置完成后打开屏幕                    |
| `OLED_Clear()` | 清除上电随机显存，屏幕全黑就绪                     |