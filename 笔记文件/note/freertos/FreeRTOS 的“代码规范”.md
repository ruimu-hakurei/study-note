FreeRTOS 的“代码规范”其实不只是排版规范，更重要的是它有一套非常固定的**命名规则**。你一旦看懂这些前缀，很多 API 不用背都能猜出：

> 这个函数返回什么类型、参数是什么、是不是中断版本、是不是内核对象。

这套规范非常值得学，因为你以后看 FreeRTOS 源码时，会轻松很多。

---

## 1. FreeRTOS 最有特色的规范：变量和函数名前缀表示类型

比如你经常看到：

```
vTaskDelay()
xTaskCreate()
uxTaskPriorityGet()
pvPortMalloc()
pxCurrentTCB
```

为什么前面总有：

```
v
x
ux
pv
px
```

这些都不是随便起的。

它们通常是在提示你：

> **这个函数返回什么类型，或者这个变量是什么类型。**

---

# 2. `v`：void

例如：

```
vTaskDelay()
vTaskDelete()
vTaskSuspend()
vTaskStartScheduler()
```

前面的：

```
v
```

通常表示：

```
void
```

也就是：

> 函数没有返回值。

例如：

```
void vTaskDelay(TickType_t xTicksToDelay);
```

所以看到：

```
vTaskDelay(...)
```

你就应该想到：

```
v = void
→ 没返回值
```

---

# 3. `x`：BaseType_t 或某种基础类型

FreeRTOS 里很多函数以：

```
x
```

开头。

例如：

```
xTaskCreate()
xQueueSend()
xQueueReceive()
xSemaphoreTake()
```

这里的 `x` 历史上表示一种：

```
BaseType_t
```

或者与机器字长相关的基本类型。

例如：

```
BaseType_t xTaskCreate(...);
```

可能返回：

```
pdPASS
```

或者：

```
errCOULD_NOT_ALLOCATE_REQUIRED_MEMORY
```

所以：

```
xTaskCreate()
```

不是“xTask”是一个单词，而更像：

```
x + TaskCreate
```

其中：

```
x
→ 返回 BaseType_t
```

---

# 4. `ux`：unsigned BaseType_t

例如：

```
uxTaskPriorityGet()
uxTaskGetNumberOfTasks()
uxQueueMessagesWaiting()
```

前缀：

```
ux
```

通常表示：

```
UBaseType_t
```

也就是无符号的 BaseType_t。

例如：

```
UBaseType_t uxTaskPriorityGet(TaskHandle_t xTask);
```

因为：

```
任务优先级
```

不会是负数。

所以用：

```
UBaseType_t
```

很合理。

---

# 5. `x` 变量前缀也很常见

例如：

```
BaseType_t xResult;
TickType_t xTicksToWait;
TaskHandle_t xTaskHandle;
QueueHandle_t xQueue;
```

这里不一定百分百表示“变量本身就是 BaseType_t”。

更准确地说：

> FreeRTOS 很多对象类型和 typedef 类型习惯使用 `x` 前缀。

例如：

```
TickType_t xTickCount;
```

虽然：

```
TickType_t
```

不一定就是 `BaseType_t`。

所以你把 `x` 理解成：

> FreeRTOS 中常见的“非简单 C 基础标量类型 / 内核对象类型”命名习惯

会更合适。

---

# 6. `p`：pointer，指针

这个非常简单。

```
p = pointer
```

例如：

```
char *pcName;
```

说明：

```
p
→ pointer

c
→ char
```

所以：

```
pcName
```

就是：

> 指向 char 的指针。

---

# 7. `pv`：pointer to void

你最熟悉的就是：

```
void *pvParameters
```

为什么叫：

```
pvParameters
```

拆开：

```
p
→ pointer

v
→ void
```

所以：

```
pv
→ void *
```

因此：

```
void *pvParameters
```

这个名字一看就知道：

> 是一个 void 指针参数。

你创建任务的时候：

```
xTaskCreate(
    Task1,
    "Task1",
    128,
    NULL,
    1,
    NULL
);
```

第四个参数最终传到：

```
void Task1(void *pvParameters)
```

---

# 8. `px`：pointer to x-type object

比如 FreeRTOS 源码里非常常见：

```
TCB_t *pxCurrentTCB;
```

这里：

```
p
→ pointer

x
→ FreeRTOS对象/基础类型习惯
```

所以：

```
pxCurrentTCB
```

表示：

> 指向当前 TCB 的指针。

这个以后你看 FreeRTOS 内核源码会疯狂遇到。

---

# 9. `pc`：pointer to char

例如：

```
char *pcTaskName;
```

或者：

```
const char *pcName;
```

其中：

```
p
→ pointer

c
→ char
```

所以：

```
pc
→ char *
```

---

# 10. `uc`：unsigned char

例如：

```
uint8_t ucValue;
```

或者 FreeRTOS 源码里：

```
unsigned char ucQueueType;
```

前缀：

```
uc
```

就是：

```
unsigned char
```

---

# 11. `c`：char

比如：

```
char cRxData;
```

那么：

```
c
→ char
```

---

# 12. `us`：unsigned short

例如：

```
unsigned short usValue;
```

FreeRTOS 老一些的代码风格里可能会看到：

```
us
→ unsigned short
```

---

# 13. `ul`：unsigned long

例如：

```
unsigned long ulValue;
```

所以：

```
ul
→ unsigned long
```

---

# 14. 一张最实用的前缀表

你可以先记这些：

|前缀|大致含义|
|---|---|
|`v`|`void`|
|`x`|BaseType_t / FreeRTOS对象类型习惯|
|`ux`|`UBaseType_t`|
|`p`|pointer|
|`pv`|`void *`|
|`pc`|`char *`|
|`px`|指向 FreeRTOS 对象/结构的指针|
|`c`|`char`|
|`uc`|`unsigned char`|
|`us`|`unsigned short`|
|`ul`|`unsigned long`|

以后看到：

```
UBaseType_t uxPriority;
```

你应该能直接拆：

```
ux
→ unsigned BaseType_t
```

---

# 15. 函数名第二部分表示模块

例如：

```
vTaskDelay()
```

拆成：

```
v
Task
Delay
```

意思：

```
返回 void
+
Task模块
+
Delay功能
```

再比如：

```
xQueueSend()
```

拆：

```
x
Queue
Send
```

就是：

```
返回某种状态值
+
Queue模块
+
Send
```

---

# 16. 所以 FreeRTOS API 很容易“读”

例如：

```
uxQueueMessagesWaiting()
```

拆：

```
ux
Queue
MessagesWaiting
```

意思：

> 返回一个无符号数量值，查询 Queue 中等待的数据条目数。

再比如：

```
vTaskSuspend()
```

就是：

```
void
Task
Suspend
```

也就是：

> 暂停任务，无返回值。

---

# 17. Handle 的命名规范

FreeRTOS 里到处都是：

```
TaskHandle_t
QueueHandle_t
SemaphoreHandle_t
TimerHandle_t
EventGroupHandle_t
```

这些都是：

> **句柄类型。**

例如：

```
TaskHandle_t xMotorTaskHandle;
```

```
QueueHandle_t xIMUQueue;
```

```
SemaphoreHandle_t xUARTMutex;
```

句柄可以理解成：

> 用来找到某个 FreeRTOS 内核对象的引用。

建议你自己写代码时，也按照这个风格：

```
TaskHandle_t xMotorTaskHandle;
QueueHandle_t xSensorQueue;
SemaphoreHandle_t xI2CMutex;
```

不要写得太随意：

```
void *a;
void *q1;
void *temp;
```

后面工程一大就非常难维护。

---

# 18. 类型名通常以 `_t` 结尾

比如：

```
BaseType_t
UBaseType_t
TickType_t
TaskHandle_t
QueueHandle_t
StackType_t
StaticTask_t
```

这里：

```
_t
```

意思就是：

> type，类型。

这是 C 项目很常见的命名风格。

---

# 19. 宏一般全部大写或有固定 config 前缀

FreeRTOS 宏例如：

```
pdTRUE
pdFALSE
pdPASS
pdFAIL

portMAX_DELAY

configUSE_PREEMPTION
configTICK_RATE_HZ
configMAX_PRIORITIES
```

这里大概分几类。

---

## 20. `configXXX`

例如：

```
configUSE_PREEMPTION
configTICK_RATE_HZ
configTOTAL_HEAP_SIZE
```

表示：

> FreeRTOSConfig.h 中的配置宏。

所以你一看到：

```
config...
```

就知道：

> 这东西很可能是在 `FreeRTOSConfig.h` 里控制功能。

---

# 21. `pdXXX`

例如：

```
pdTRUE
pdFALSE
pdPASS
pdFAIL
```

这里：

```
pd
```

历史上和 FreeRTOS 的 portable definitions 有关。

你学习时直接把它理解成：

> FreeRTOS 定义的一些通用状态常量。

例如：

```
if (xQueueSend(...) == pdPASS)
{
}
```

比直接写：

```
if (xQueueSend(...) == 1)
```

规范得多。

因为：

```
pdPASS
```

语义非常清楚。

---

# 22. `portXXX`

例如：

```
portMAX_DELAY
portTICK_PERIOD_MS
portYIELD()
portENTER_CRITICAL()
```

说明：

> 和 FreeRTOS 移植层 Port 有关。

也就是：

```
具体CPU / 编译器相关
```

例如：

```
portYIELD()
```

和底层任务切换有关。

---

# 23. `taskXXX`

有些宏：

```
taskENTER_CRITICAL()
taskEXIT_CRITICAL()
taskYIELD()
```

它们更偏：

> Task 层接口。

例如：

```
taskENTER_CRITICAL();

sharedData++;

taskEXIT_CRITICAL();
```

---

# 24. ISR 版本一定带 `FromISR`

这是 FreeRTOS 最重要的代码规范之一。

普通任务里：

```
xQueueSend()
xSemaphoreGive()
xTaskNotifyGive()
```

中断里不能乱用这些普通版本。

中断上下文要用：

```
xQueueSendFromISR()
xSemaphoreGiveFromISR()
vTaskNotifyGiveFromISR()
```

只要看到：

```
FromISR
```

就知道：

> 这是给中断服务函数使用的版本。

这是非常非常重要的。

---

# 25. 为什么 ISR 要单独一套 API？

因为中断环境和普通 Task 不一样。

普通 Task 可以：

```
Blocked
等待
让出CPU
```

中断不可以。

比如普通任务：

```
xQueueSend(
    xQueue,
    &data,
    pdMS_TO_TICKS(100)
);
```

如果 Queue 满了，可以：

```
最多等100ms
```

但是 ISR 里：

> 中断不能睡100ms等 Queue。

所以 ISR API 必须立即完成：

```
xQueueSendFromISR(...)
```

成功就成功，失败就返回。

---

# 26. ISR 里常见的 `xHigherPriorityTaskWoken`

例如：

```
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

xQueueSendFromISR(
    xQueue,
    &data,
    &xHigherPriorityTaskWoken
);

portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
```

这里命名也非常 FreeRTOS。

```
xHigherPriorityTaskWoken
```

意思：

> 有没有因为这次 ISR 操作，唤醒了一个更高优先级任务。

如果：

```
pdTRUE
```

那么中断退出的时候可以立即：

```
切换到那个高优先级Task
```

这就是实时性。

---

# 27. Task 函数的规范写法

一般：

```
void vMotorTask(void *pvParameters)
{
    while (1)
    {
        // 任务逻辑

        vTaskDelay(pdMS_TO_TICKS(10));
    }
}
```

注意几个规范。

第一：

```
void
```

无返回值。

第二：

```
void *pvParameters
```

固定任务参数形式。

第三：

```
while (1)
```

任务通常不会直接返回。

---

# 28. Task 不应该直接 `return`

错误思维：

```
void vTask1(void *pvParameters)
{
    DoSomething();

    return;
}
```

FreeRTOS Task 正常情况下不应该这样结束。

如果真的需要删除当前任务：

```
vTaskDelete(NULL);
```

例如：

```
void vInitTask(void *pvParameters)
{
    InitSomething();

    vTaskDelete(NULL);
}
```

这里：

```
NULL
```

表示：

> 删除当前任务。

---

# 29. 推荐任务名带 Task 后缀

你自己写的时候建议：

```
vMotorTask()
vIMUTask()
vCommunicationTask()
vControlTask()
```

而不是：

```
motor()
imu()
aa()
task1()
```

因为：

```
看到名字
↓
立刻知道这是一个FreeRTOS Task
```

大型工程非常重要。

---

# 30. Handle 推荐 `xXXXHandle`

例如：

```
TaskHandle_t xMotorTaskHandle;
QueueHandle_t xIMUQueueHandle;
SemaphoreHandle_t xUARTMutexHandle;
```

有些工程会简化成：

```
QueueHandle_t xIMUQueue;
SemaphoreHandle_t xUARTMutex;
```

也没问题。

关键是：

> 整个项目保持一致。

---

# 31. 时间不要直接写裸数字

例如：

```
vTaskDelay(1000);
```

不推荐。

为什么？

因为：

```
1000到底是1000ms
还是1000 Tick？
```

不清楚。

应该：

```
vTaskDelay(pdMS_TO_TICKS(1000));
```

意思非常明确：

> 延迟 1000ms。

即使以后：

```
configTICK_RATE_HZ
```

改了，也不用重新手算。

---

# 32. 不推荐使用魔法数字

例如：

```
xTaskCreate(
    vMotorTask,
    "Motor",
    512,
    NULL,
    4,
    NULL
);
```

这里：

```
512
4
```

过几个月你可能都不知道为什么。

更规范：

```
#define MOTOR_TASK_STACK_SIZE      512U
#define MOTOR_TASK_PRIORITY        4U
```

然后：

```
xTaskCreate(
    vMotorTask,
    "Motor",
    MOTOR_TASK_STACK_SIZE,
    NULL,
    MOTOR_TASK_PRIORITY,
    &xMotorTaskHandle
);
```

可读性明显提高。

---

# 33. 任务优先级也最好集中定义

比如：

```
#define CONTROL_TASK_PRIORITY      4U
#define IMU_TASK_PRIORITY          3U
#define COMM_TASK_PRIORITY         2U
#define LOG_TASK_PRIORITY          1U
```

比：

```
xTaskCreate(..., 4, ...);
xTaskCreate(..., 3, ...);
xTaskCreate(..., 2, ...);
```

好得多。

你以后调优先级也容易。

---

# 34. Stack 大小也集中管理

比如：

```
#define CONTROL_TASK_STACK_SIZE    256U
#define IMU_TASK_STACK_SIZE        256U
#define COMM_TASK_STACK_SIZE       384U
```

这在机器人工程里特别实用。

---

# 35. 返回值一定要检查

例如：

```
xTaskCreate(...)
```

不建议：

```
xTaskCreate(
    vMotorTask,
    "Motor",
    256,
    NULL,
    3,
    NULL
);
```

然后完全不管。

更规范：

```
BaseType_t xResult;

xResult = xTaskCreate(
    vMotorTask,
    "Motor",
    256,
    NULL,
    3,
    &xMotorTaskHandle
);

if (xResult != pdPASS)
{
    Error_Handler();
}
```

因为 Heap 不够时：

```
Task可能根本没有创建成功
```

如果你不检查，就会觉得：

> “为什么这个Task没运行？”

其实不是调度问题，而是创建失败。

---

# 36. Queue 创建也要检查

例如：

```
xIMUQueue = xQueueCreate(
    10,
    sizeof(IMU_Data_t)
);

if (xIMUQueue == NULL)
{
    Error_Handler();
}
```

因为动态对象创建失败通常返回：

```
NULL
```

---

# 37. Mutex 同样检查

```
xUARTMutex = xSemaphoreCreateMutex();

if (xUARTMutex == NULL)
{
    Error_Handler();
}
```

这个习惯非常重要。

---

# 38. 中断里不要调用阻塞 API

比如中断里绝对不要这种：

```
vTaskDelay(100);
```

也不要：

```
xSemaphoreTake(
    xMutex,
    portMAX_DELAY
);
```

因为 ISR 不是 Task，不能进入 Blocked。

ISR 应该：

```
短
快
只做必要工作
```

典型结构：

```
中断
↓
读取关键状态
↓
清中断标志
↓
Task Notification / Queue / Semaphore
↓
退出
```

真正复杂处理交给 Task。

---

# 39. FreeRTOS 代码里不要长时间关中断

例如：

```
taskENTER_CRITICAL();

/* 一大堆耗时代码 */

taskEXIT_CRITICAL();
```

非常不规范。

临界区应该：

> 越短越好。

比如：

```
taskENTER_CRITICAL();

sharedCounter++;

taskEXIT_CRITICAL();
```

这种才合理。

否则会：

```
延迟硬件中断
↓
破坏系统实时性
```

---

# 40. 不要在高优先级 Task 里死循环不阻塞

比如：

```
void vHighTask(void *pvParameters)
{
    while (1)
    {
        DoSomething();
    }
}
```

假设它是系统最高优先级，而且：

```
永远Ready
```

那么低优先级 Task 可能：

```
永远运行不到
```

更规范：

```
void vHighTask(void *pvParameters)
{
    while (1)
    {
        DoSomething();

        vTaskDelay(pdMS_TO_TICKS(10));
    }
}
```

或者等待：

```
Queue
Semaphore
Notification
Event
```

让 Task 在没事做的时候进入：

```
Blocked
```

这是 FreeRTOS 最重要的设计规范之一。

---

# 41. 周期任务推荐 `vTaskDelayUntil()`

假设控制任务要求：

```
每10ms运行一次
```

普通：

```
vTaskDelay(pdMS_TO_TICKS(10));
```

会受到任务执行时间影响。

例如：

```
执行用了2ms
+
Delay 10ms
=
12ms周期
```

更规范的周期控制任务：

```
void vControlTask(void *pvParameters)
{
    TickType_t xLastWakeTime;

    xLastWakeTime = xTaskGetTickCount();

    while (1)
    {
        MotorControl();

        vTaskDelayUntil(
            &xLastWakeTime,
            pdMS_TO_TICKS(10)
        );
    }
}
```

这样更接近：

```
0ms
10ms
20ms
30ms
40ms
```

固定周期。

对于：

```
PID
IMU采样
控制环
```

尤其重要。

---

# 42. Task 之间不要靠全局变量乱传数据

例如：

```
float imu_angle;
```

Task A：

```
imu_angle = GetAngle();
```

Task B：

```
MotorControl(imu_angle);
```

简单 Demo 可以。

复杂工程容易出现：

```
竞争条件
数据更新到一半
同步问题
```

更规范考虑：

```
Queue
Task Notification
Mutex
Event Group
```

具体选哪个根据需求。

---

# 43. `volatile` 不是线程同步工具

这是很常见的坑。

例如：

```
volatile int flag;
```

`volatile` 只能告诉编译器：

> 每次真的去读内存，不要乱优化。

它并不能自动保证：

```
原子性
互斥
任务同步
内存一致性
```

所以 FreeRTOS 多任务共享数据不能简单想：

```
加 volatile 就安全了
```

这点非常重要。

---

# 44. Callback 里不要做太重的工作

例如软件 Timer Callback：

```
void vTimerCallback(TimerHandle_t xTimer)
{
}
```

它其实运行在：

```
Timer Service Task
```

里面。

如果你写：

```
void vTimerCallback(TimerHandle_t xTimer)
{
    HugeCalculation();
    HAL_Delay(1000);
    printf(...);
}
```

会阻塞其他软件 Timer。

更规范：

```
Timer Callback
↓
发一个Notification/Queue
↓
真正任务做复杂工作
```

---

# 45. 代码布局推荐

一个比较清晰的 FreeRTOS 应用文件可以这样：

```
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"

#define MOTOR_TASK_STACK_SIZE      256U
#define MOTOR_TASK_PRIORITY        3U

static TaskHandle_t xMotorTaskHandle = NULL;

static void vMotorTask(void *pvParameters);

void App_RTOS_Init(void)
{
    BaseType_t xResult;

    xResult = xTaskCreate(
        vMotorTask,
        "Motor",
        MOTOR_TASK_STACK_SIZE,
        NULL,
        MOTOR_TASK_PRIORITY,
        &xMotorTaskHandle
    );

    if (xResult != pdPASS)
    {
        Error_Handler();
    }
}

static void vMotorTask(void *pvParameters)
{
    (void)pvParameters;

    while (1)
    {
        Motor_Control();

        vTaskDelay(pdMS_TO_TICKS(10));
    }
}
```

这里有几个很好的习惯。

---

# 46. 不使用的参数明确 `(void)`

例如：

```
static void vMotorTask(void *pvParameters)
{
    (void)pvParameters;
```

意思：

> 我知道有这个参数，但我故意不用。

这样可以避免编译器警告：

```
unused parameter
```

这是 C 工程很常见的规范。

---

# 47. 只在当前 `.c` 文件使用的东西加 `static`

例如：

```
static TaskHandle_t xMotorTaskHandle;

static void vMotorTask(void *pvParameters);
```

意味着：

> 只允许当前源文件访问。

好处：

```
减少全局命名污染
防止其他文件误访问
模块边界更清楚
```

这其实是非常重要的工程规范。

---

# 48. FreeRTOS 本身大量使用 `static`

你以后看：

```
tasks.c
queue.c
list.c
```

会看到很多内部函数：

```
static ...
```

因为 FreeRTOS 很强调模块封装。

---

# 49. 自己写代码不用完全照搬 FreeRTOS 内核的匈牙利命名

这一点我特别提醒你。

FreeRTOS 内核自己大量使用：

```
uxPriority
pxTCB
pvParameters
xTicksToWait
```

你学习源码最好能看懂。

但你自己的应用代码并不是必须每个变量都严格模仿。

比如：

```
float motor_speed;
uint32_t encoder_count;
```

完全可以。

甚至现代工程常常觉得这种名字更直接。

你真正应该保留的是：

```
Task / Queue / Handle命名清晰
模块一致
类型明确
FromISR区分正确
宏不要魔法数字
```

而不是机械追求：

```
每个变量必须带类型前缀
```

---

# 50. 推荐你自己项目采用的风格

我比较建议你以后 STM32 + FreeRTOS 项目这样：

普通变量：

```
uint32_t encoder_count;
float motor_speed;
IMU_Data_t imu_data;
```

FreeRTOS 对象：

```
TaskHandle_t motor_task_handle;
QueueHandle_t imu_queue;
SemaphoreHandle_t uart_mutex;
```

或者如果课程统一 FreeRTOS 风格：

```
TaskHandle_t xMotorTaskHandle;
QueueHandle_t xIMUQueue;
SemaphoreHandle_t xUARTMutex;
```

选一种，坚持到底就行。

任务：

```
static void vMotorTask(void *pvParameters);
static void vIMUTask(void *pvParameters);
```

宏：

```
#define MOTOR_TASK_PRIORITY       4U
#define MOTOR_TASK_STACK_SIZE     256U
#define CONTROL_PERIOD_MS         10U
```

这已经非常清晰。

---

## 最后，把 FreeRTOS 代码规范压缩成 10 条

1. `v` 通常表示返回 `void`。
2. `x/ux/pv/px` 等前缀提示类型。
3. Task 函数通常是 `void Task(void *pvParameters)`。
4. Task 正常不直接 `return`。
5. ISR 必须优先使用 `xxxFromISR()`。
6. 延时写 `pdMS_TO_TICKS()`，不要直接裸 Tick 数。
7. 动态创建 Task/Queue/Mutex 后检查返回值。
8. 高优先级 Task 不要永远 Ready 空转。
9. 临界区和 ISR 都要尽量短。
10. 任务优先级、栈大小、周期集中定义，不要到处写魔法数字。

如果你接下来开始看 `tasks.c` 源码，最值得先学的其实就是 **FreeRTOS 的数据类型命名规范：`BaseType_t / UBaseType_t / TickType_t / StackType_t / List_t / ListItem_t / TCB_t`**。这些搞懂后，源码可读性会提升非常明显。