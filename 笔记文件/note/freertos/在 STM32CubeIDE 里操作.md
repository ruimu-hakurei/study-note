> **不要把 `FreeRTOS-Kernel` 目录下面所有 `.c` 文件不加选择地全部丢进去。**

因为 `portable` 里面有不同 CPU、不同编译器的 `port.c`，`MemMang` 里面还有 `heap_1.c ~ heap_5.c`。这些不能全部同时编译。对于 STM32F103RCT6 + STM32CubeIDE，一般选择：

```
CPU：Cortex-M3
编译器：GCC
Port：portable/GCC/ARM_CM3
Heap：通常选 heap_4.c
```

下面按照实际操作来。

1. **新建 STM32 工程。** 打开 STM32CubeIDE，进入 `File → New → STM32 Project`。在芯片搜索框输入：

```
STM32F103RCT6
```

选择对应 MCU，然后 `Next`。Project Name 可以先写：

```
FreeRTOS_Test
```

语言选择：

```
C
```

如果看到 Targeted Language：

```
C
```

就选 C。然后 `Finish`。如果询问是否初始化默认外设，可以正常确认。

你最终应该得到类似：

```
FreeRTOS_Test
├── Core
│   ├── Inc
│   └── Src
├── Drivers
├── Debug
└── FreeRTOS_Test.ioc
```

图片里写的“记得设置调试器”，对于大多数 STM32 开发板，如果是 ST-Link，后面通常在：

```
Run
→ Debug Configurations
→ STM32 Cortex-M C/C++ Application
```

使用 ST-LINK。这个暂时不用急着设置，先让工程能编译。

2. **先编译一次裸工程。** 点击锤子：

```
Build
```

或者：

```
Project → Build Project
```

确保现在工程本身没有错误。最好看到：

```
0 errors
```

这样以后加入 FreeRTOS 出错，就知道问题一定来自 FreeRTOS 配置，而不是原始 STM32 工程。

3. **准备 FreeRTOS-Kernel 源码。** 你下载的 FreeRTOS Kernel 通常结构类似：

```
FreeRTOS-Kernel
├── tasks.c
├── queue.c
├── list.c
├── timers.c
├── event_groups.c
├── stream_buffer.c
├── croutine.c
│
├── include
│   ├── FreeRTOS.h
│   ├── task.h
│   ├── queue.h
│   ├── semphr.h
│   ├── timers.h
│   └── ...
│
└── portable
    ├── GCC
    │   ├── ARM_CM3
    │   │   ├── port.c
    │   │   └── portmacro.h
    │   └── ...
    │
    └── MemMang
        ├── heap_1.c
        ├── heap_2.c
        ├── heap_3.c
        ├── heap_4.c
        └── heap_5.c
```

这里你现在要建立一个非常重要的认识：

```
tasks.c
queue.c
list.c
...
```

属于：

```
通用 FreeRTOS 内核
```

而：

```
portable/GCC/ARM_CM3/port.c
```

属于：

```
STM32F103 对应的 CPU 移植层
```

STM32F103RCT6 是：

```
ARM Cortex-M3
```

所以这里一定是：

```
ARM_CM3
```

不是 ARM_CM4F，也不是 ARM_CM7。

4. **在 STM32CubeIDE 工程中新建 FreeRTOS 文件夹。** 在左边 Project Explorer 找到：

```
FreeRTOS_Test
```

右键项目：

```
New → sourceFolder
```

名字：

```
FreeRTOS
```

然后在 `FreeRTOS` 上右键：

```
New → Folder
```

建立：

```
Src
```

再建立：

```
Inc
```

最后建议你整理成：

```
FreeRTOS_Test
├── Core
├── Drivers
│
├── FreeRTOS
│   ├── Src
│   ├── Inc
│   └── portable
│
└── FreeRTOS_Test.ioc
```

图片上只建立 `Src` 也可以，但我更推荐现在直接整理好，不然后面会越来越乱。

5. **复制 FreeRTOS 通用 `.c` 文件。** 从你下载的 `FreeRTOS-Kernel` 根目录复制：

```
tasks.c
list.c
queue.c
timers.c
event_groups.c
stream_buffer.c
```

放到：

```
FreeRTOS/Src
```

如果课程使用协程，还可能有：

```
croutine.c
```

但现代项目基本不用 Co-routine，你暂时甚至可以不管它。

最终类似：

```
FreeRTOS
└── Src
    ├── tasks.c
    ├── list.c
    ├── queue.c
    ├── timers.c
    ├── event_groups.c
    └── stream_buffer.c
```

这里再次强调：图片上的：

> “复制 FreeRTOS-Kernel 下所有 `.c` 文件”

更准确的说法应该是：

> **复制 FreeRTOS-Kernel 根目录中需要的通用内核 `.c` 文件。**

不要现在直接递归复制 `portable` 下面的所有 `.c`。

6. **复制 include 头文件。** 把：

```
FreeRTOS-Kernel/include/
```

里面的头文件复制到：

```
FreeRTOS/Inc
```

比如：

```
FreeRTOS/Inc
├── FreeRTOS.h
├── task.h
├── queue.h
├── semphr.h
├── timers.h
├── event_groups.h
├── stream_buffer.h
├── message_buffer.h
└── ...
```

注意：

```
task.h
```

和：

```
tasks.c
```

名字不完全一样。

`task.h` 是接口声明。

`tasks.c` 是实现。

7. **复制 STM32F103 对应的 Port。** 因为 STM32F103RCT6 是：

```
Cortex-M3
```

而 STM32CubeIDE 默认使用 GCC，所以找到：

```
FreeRTOS-Kernel
└── portable
    └── GCC
        └── ARM_CM3
```

通常里面有：

```
port.c
portmacro.h
```

你可以在自己工程里创建：

```
FreeRTOS/portable
```

然后把它们复制进去：

```
FreeRTOS
└── portable
    ├── port.c
    └── portmacro.h
```

或者保留原目录层次：

```
FreeRTOS
└── portable
    └── GCC
        └── ARM_CM3
            ├── port.c
            └── portmacro.h
```

我更推荐第二种，因为以后看到目录就知道它属于：

```
GCC + Cortex-M3
```

8. **选择一个 Heap 文件。** 找到：

```
FreeRTOS-Kernel
└── portable
    └── MemMang
```

里面有：

```
heap_1.c
heap_2.c
heap_3.c
heap_4.c
heap_5.c
```

你只选择一个。

我们学习阶段推荐：

```
heap_4.c
```

复制到：

```
FreeRTOS/Src
```

于是：

```
FreeRTOS/Src
├── tasks.c
├── list.c
├── queue.c
├── timers.c
├── event_groups.c
├── stream_buffer.c
└── heap_4.c
```

千万不要：

```
heap_1.c
heap_2.c
heap_3.c
heap_4.c
heap_5.c
```

五个同时加入。

否则它们都实现：

```
pvPortMalloc()
vPortFree()
```

链接时会发生重复定义。

9. **配置头文件搜索路径。** 这是第一次手动移植 FreeRTOS 最容易报错的地方。

如果你现在直接 Build，很可能看到：

```
fatal error: FreeRTOS.h: No such file or directory
```

或者：

```
fatal error: portmacro.h: No such file or directory
```

因为编译器不知道这些头文件在哪。

右键项目：

```
Properties
```

然后一般进入：

```
C/C++ Build
→ Settings
→ MCU GCC Compiler
→ Include paths
```

加入：

```
../FreeRTOS/Inc
```

以及：

```
../FreeRTOS/portable/GCC/ARM_CM3
```

如果你的目录层次不一样，就根据自己的实际位置设置。

最后 Include 路径大概有：

```
../Core/Inc
../Drivers/STM32F1xx_HAL_Driver/Inc
../Drivers/CMSIS/Device/ST/STM32F1xx/Include
../Drivers/CMSIS/Include

../FreeRTOS/Inc
../FreeRTOS/portable/GCC/ARM_CM3
```

于是编译器看到：

```
#include "FreeRTOS.h"
```

就能去：

```
FreeRTOS/Inc
```

找。

而 `FreeRTOS.h` 内部需要：

```
#include "portmacro.h"
```

它又能去：

```
FreeRTOS/portable/GCC/ARM_CM3
```

找到。

10. **建立 `FreeRTOSConfig.h`。** 到这里还不能直接编译 FreeRTOS，因为：

```
FreeRTOS.h
```

会需要：

```
FreeRTOSConfig.h
```

这个文件不是通用内核替你决定好的。

因为不同工程：

```
CPU频率
Tick频率
优先级数量
Heap大小
是否抢占
是否启用Mutex
是否启用软件定时器
```

都不一样。

所以每个工程需要自己的：

```
FreeRTOSConfig.h
```

一般从 FreeRTOS 官方 example/template 中复制一份模板，然后修改。

可以把：

```
FreeRTOSConfig.h
```

放到：

```
Core/Inc
```

比如：

```
Core
└── Inc
    ├── main.h
    └── FreeRTOSConfig.h
```

为什么这里可以？

因为：

```
Core/Inc
```

本来就已经在 Include path 里面。

所以：

```
#include "FreeRTOSConfig.h"
```

可以直接找到。

11. **到这里，你的工程应该大概长这样。**

```
FreeRTOS_Test
│
├── Core
│   ├── Inc
│   │   ├── main.h
│   │   └── FreeRTOSConfig.h
│   │
│   └── Src
│       └── main.c
│
├── Drivers
│
├── FreeRTOS
│   │
│   ├── Inc
│   │   ├── FreeRTOS.h
│   │   ├── task.h
│   │   ├── queue.h
│   │   ├── semphr.h
│   │   └── ...
│   │
│   ├── Src
│   │   ├── tasks.c
│   │   ├── list.c
│   │   ├── queue.c
│   │   ├── timers.c
│   │   ├── event_groups.c
│   │   ├── stream_buffer.c
│   │   └── heap_4.c
│   │
│   └── portable
│       └── GCC
│           └── ARM_CM3
│               ├── port.c
│               └── portmacro.h
│
└── FreeRTOS_Test.ioc
```

这个目录非常值得你记住。

它对应你上一节学的：

```
              FreeRTOS
                  │
       ┌──────────┼──────────┐
       ↓          ↓          ↓
   通用内核      Port       Heap
       │          │          │
   tasks.c      port.c    heap_4.c
   queue.c      │
   list.c       ↓
       │      Cortex-M3
       ↓
    FreeRTOS API
```

12. **然后再 Build。** 点击：

```
Build
```

第一次肯定有可能报错，这很正常。

最常见第一类：

```
FreeRTOSConfig.h: No such file or directory
```

说明：

```
FreeRTOSConfig.h
```

没创建或者路径没配置。

第二类：

```
portmacro.h: No such file or directory
```

说明：

```
portable/GCC/ARM_CM3
```

没有添加到 Include path。

第三类：

```
FreeRTOS.h: No such file or directory
```

说明：

```
FreeRTOS/Inc
```

没有添加到 Include path。

第四类可能是：

```
configCPU_CLOCK_HZ undeclared
configTICK_RATE_HZ undeclared
...
```

说明：

```
FreeRTOSConfig.h
```

里面的配置还不完整。

13. **等源码能够编译以后，才开始写第一个任务。** 在：

```
main.c
```

加入：

```
#include "FreeRTOS.h"
#include "task.h"
```

写一个任务：

```
void vTask1(void *pvParameters)
{
    while (1)
    {
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);

        vTaskDelay(pdMS_TO_TICKS(500));
    }
}
```

然后在 `main()` 完成 HAL、Clock、GPIO 初始化之后创建：

```
xTaskCreate(
    vTask1,
    "Task1",
    128,
    NULL,
    1,
    NULL
);

vTaskStartScheduler();
```

结构就是：

```
int main(void)
{
    HAL_Init();

    SystemClock_Config();

    MX_GPIO_Init();

    xTaskCreate(
        vTask1,
        "Task1",
        128,
        NULL,
        1,
        NULL
    );

    vTaskStartScheduler();

    while (1)
    {
    }
}
```

但你现在 **先不要急着复制这段运行**，因为手动移植还涉及一个关键问题：

```
SysTick
PendSV
SVC
```

FreeRTOS 和 STM32 HAL 都会涉及 SysTick，所以中断处理函数还需要正确衔接。这个我们下一步专门处理，否则非常容易出现：

```
能编译
↓
能烧录
↓
但是任务不运行
```

的情况。

你现在这一阶段的目标就只有一个：

```
① STM32F103RCT6 裸工程建立成功
         ↓
② FreeRTOS/Src 建好
         ↓
③ 复制通用 .c
         ↓
④ 复制 include
         ↓
⑤ 加 GCC/ARM_CM3 的 port.c / portmacro.h
         ↓
⑥ 只选一个 heap_4.c
         ↓
⑦ 设置 Include Path
         ↓
⑧ 建立 FreeRTOSConfig.h
         ↓
⑨ Build
```

其中尤其记住三个对应关系：

```
STM32F103RCT6
      ↓
Cortex-M3
      ↓
portable/GCC/ARM_CM3
```

以及：

```
内核通用代码       CPU相关代码       内存管理
    ↓                 ↓                ↓
 tasks.c            port.c          heap_4.c
 queue.c         portmacro.h
 list.c
```

这才是图片里“把 FreeRTOS 添加到 STM32CubeIDE 工程”的完整含义。下一步真正关键的是 **怎么写 `FreeRTOSConfig.h`，以及 STM32F103 的 `SysTick / PendSV / SVC` 应该怎么配置**；这部分搞定之后，第一个 FreeRTOS LED 任务就可以真正跑起来了。