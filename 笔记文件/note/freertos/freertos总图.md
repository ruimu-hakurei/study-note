![[Pasted image 20260826021623.png]]这张图可以当成一张 **FreeRTOS 全景地图**。你现在先别试图一次把所有模块都记住，最重要的是先看清楚：**FreeRTOS 其实就是围绕“任务调度 + 任务通信 + 时间管理 + 内存管理”这四件事展开的。**

图中央最核心的是“调度器”。所有用户任务、空闲任务、定时器任务，最后都要由调度器决定什么时候运行。上方的三个中断——`SysTick`、`SVC`、`PendSV`——可以理解成 Cortex-M 上支撑 FreeRTOS 调度的底层机制。

其中 `SysTick` 最容易先理解。它会周期性产生系统节拍 Tick，例如每 1 ms 来一次，用于推进系统时间、判断哪些 `vTaskDelay()` 到期、哪些软件定时器应该处理等。你前面学到：

```
vTaskDelay(pdMS_TO_TICKS(1000));
```

背后就离不开 Tick。

`PendSV` 主要用于 **任务上下文切换**。比如当前任务进入阻塞状态，或者更高优先级任务变成 Ready，FreeRTOS 就需要把当前任务的寄存器现场保存起来，再恢复另一个任务的现场，这一套切换通常借助 PendSV 完成。

`SVC` 可以先理解成 Cortex-M 的系统服务异常，在 FreeRTOS 启动第一个任务等过程中会参与工作。现在不用深挖汇编，知道它属于调度底层即可。

图中间下面这一排：

```
空闲任务
定时器任务
用户任务1
用户任务2
……
用户任务n
```

表示 FreeRTOS 中真正被调度的各种 Task。

你自己写的：

```
void MotorTask(void *arg)
{
    while(1)
    {
        ...
    }
}
```

属于“用户任务”。

而 **Idle Task 空闲任务** 是 FreeRTOS 自动创建的。它优先级最低，当所有用户任务都不能运行时：

```
Task1 → Blocked
Task2 → Blocked
Task3 → Blocked
```

CPU 并不是“没有程序运行”，而是去执行：

```
Idle Task
```

所以以后你看到 CPU 空闲率、低功耗、删除任务后的资源回收，都和 Idle Task 有关系。

“定时器任务”则与软件定时器有关。以后你创建：

```
xTimerCreate(...)
```

软件定时器到期之后，并不是自己变成一个独立 Task，而通常是由 FreeRTOS 的 **Timer Service Task / Timer Daemon Task** 来执行对应的回调函数。

它旁边的：

```
定时器命令队列
```

也是因为其他任务对软件定时器的操作，例如：

```
xTimerStart()
xTimerStop()
xTimerReset()
```

往往要把命令发送给这个定时器任务处理。

---

右侧这一大列，其实可以看成 FreeRTOS 提供给任务使用的“工具箱”。

最上面：

```
队列
队列集合
事件组
软件定时器
```

再往下：

```
二进制信号量
计数信号量
互斥锁
递归互斥锁
临界区
```

再下面：

```
任务通知
消息缓冲区
流缓冲区
```

它们看起来很多，但实际上主要解决三类问题。

第一类是：

> **任务之间怎么传数据？**

典型就是 **Queue 队列**。

比如机器人里：

```
IMU采集任务
      ↓
    Queue
      ↓
姿态解算任务
```

采集任务得到：

```
imu_data
```

通过：

```
xQueueSend()
```

发送。

姿态任务：

```
xQueueReceive()
```

取出。

这解决的是：

**数据传输。**

第二类是：

> **任务之间怎么通知“某件事发生了”？**

这时可以用：

```
二值信号量
事件组
任务通知
```

例如：

```
DMA完成中断
     ↓
给信号量
     ↓
数据处理Task醒来
```

或者：

```
Task A
 ↓
通知 Task B：
“新的IMU数据到了”
```

这解决的是：

**同步和事件通知。**

第三类是：

> **多个任务同时访问同一个资源怎么办？**

比如两个任务都想使用 UART：

```
Task1 ──→ UART
Task2 ──→ UART
```

如果同时操作，就可能把数据搞乱。

于是使用：

```
Mutex
```

让资源一次只能被一个任务占用：

```
Task1
 ↓
拿到Mutex
 ↓
使用UART
 ↓
释放Mutex

Task2才能继续
```

所以：

**Mutex 主要解决共享资源互斥访问。**

这里特别要注意：信号量和互斥锁看起来很像，但用途不完全一样。以后这是 FreeRTOS 的一个重点。

---

图里的：

```
二进制信号量
计数信号量
互斥锁
递归互斥锁
```

其实底层和 Queue 有很深关系。

你可以暂时理解成 FreeRTOS 有一个非常核心的“队列机制”，然后在这个机制上构造出了很多同步工具。因此你以后学习顺序最好是：

```
Queue
 ↓
Semaphore
 ↓
Mutex
 ↓
Event Group
 ↓
Task Notification
```

这样会比较顺。

---

### 临界区是什么

图中还有一个：

```
临界区
```

它解决的是：

> 有一小段代码绝对不能被某些中断或任务切换打断。

例如：

```
counter++;
```

表面只有一行，但 CPU 实际可能需要：

```
读取 counter
↓
+1
↓
写回 counter
```

如果中间被打断：

```
Task A读取 counter
        ↓
发生切换
        ↓
Task B修改 counter
        ↓
切回来
        ↓
Task A按照旧数据写回
```

就会出错。

于是可以进入临界区：

```
taskENTER_CRITICAL();

/* 关键代码 */

taskEXIT_CRITICAL();
```

不过临界区不能乱用，因为进入太久会影响实时性。

---

## Event Group 是干什么的

事件组特别适合表达：

> 多个事件条件。

例如机器人初始化：

```
bit0：IMU初始化成功
bit1：CAN初始化成功
bit2：电机初始化成功
bit3：ROS通信成功
```

可以形成：

```
EventGroup
00001111
```

然后一个任务可以等待：

```
等 IMU + CAN + Motor 全部就绪
```

再开始运行。

所以它不是主要用来传复杂数据，而是表示：

**事件标志位。**

---

## Task Notification 很重要

图里的：

```
任务通知
```

你以后做工程会经常用。

它可以理解成：

> 每个 Task 自带一个非常轻量的通知槽。

比如：

```
中断
 ↓
vTaskNotifyGiveFromISR()
 ↓
Task被唤醒
```

相比 Queue 或 Semaphore，它通常更轻量、更快。

所以 FreeRTOS 里经常出现：

```
ISR → Task Notification → Task
```

例如：

```
IMU Data Ready 中断
         ↓
Task Notification
         ↓
IMU Task
```

这个模式对机器人特别实用。

---

## Stream Buffer 和 Message Buffer

最后两个：

```
消息缓冲区
流缓冲区
```

也不用现在死记。

Stream Buffer 更像：

```
连续字节流
```

例如 UART：

```
A B C D E F G ...
```

不断接收。

Message Buffer 更强调：

```
一条消息
一条消息
一条消息
```

例如：

```
消息1：10字节
消息2：20字节
消息3：5字节
```

两者以后学通信时再详细看。

---

# 最下面：Heap 内存管理

图中：

```
heap1
heap2
heap3
heap4
heap5
```

这是 FreeRTOS 的几种动态内存管理实现。

因为你执行：

```
xTaskCreate()
```

FreeRTOS 可能需要给任务分配：

```
TCB
+
Task Stack
```

创建 Queue 也需要内存：

```
Queue控制结构
+
Queue数据存储区
```

所以需要：

```
pvPortMalloc()
vPortFree()
```

FreeRTOS 给了不同的 Heap 实现。

你现在简单知道：

```
heap_1
heap_2
heap_3
heap_4
heap_5
```

是五种不同的内存分配策略。

STM32 工程里很常见：

```
heap_4
```

因为它支持：

```
分配
释放
合并相邻空闲块
```

以后讲内存时我们专门分析。

---

# 把整张图压缩成一个非常重要的框架

你现在可以在脑子里把 FreeRTOS 看成这样：

```
                    FreeRTOS
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
      调度            通信            内存
        │              │              │
        │          Queue             Heap
        │          Semaphore
        │          Mutex
        │          EventGroup
        │          Notification
        │
   Task1 Task2 Task3
        ↑
        │
   Scheduler
        ↑
        │
 ┌──────┼──────┐
 ↓      ↓      ↓
SysTick SVC  PendSV
```

再加上：

```
时间管理
   │
   ├── vTaskDelay
   └── Software Timer
```

基本就是整张图。

---

