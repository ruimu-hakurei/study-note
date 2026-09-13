# 16 Linux 下的 C 开发

[[linux/Linux基础与实战|← 返回总目录]] · [[linux/15-Bash脚本基础|上一篇：Bash脚本基础]] · [[linux/17-实战-日志统计脚本|下一篇：实战-日志统计脚本]]

---

## 从源码到运行

```text
main.c → 预处理 → 编译 → 汇编 → 目标文件 → 链接 → 可执行文件
                                                    ↓
                                              ./app 启动进程
```

GCC 是编译器工具链入口，Make 根据依赖关系决定运行哪些构建命令，GDB 用于调试进程。三者不是同一个工具。

## 示例：安全读取两个整数并求和

创建 `main.c`：

```c
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

static int parse_int(const char *text, int *result)
{
    char *end = NULL;
    errno = 0;                          // errno 可能残留上次库调用的值
    long value = strtol(text, &end, 10);

    if (errno == ERANGE || end == text || *end != '\0' ||
        value < INT_MIN || value > INT_MAX)
    {
        return 0;                       // 没读到数字、存在尾随字符或超范围
    }

    *result = (int)value;                // 通过指针写回调用者的变量
    return 1;
}

int main(int argc, char *argv[])
{
    int a = 0;
    int b = 0;

    if (argc != 3 || !parse_int(argv[1], &a) || !parse_int(argv[2], &b))
    {
        fprintf(stderr, "Usage: %s integer integer\n", argv[0]);
        return EXIT_FAILURE;
    }

    // 先转为 long long 再加；在常见 Linux 32 位 int 平台可容纳两个 int 的和。
    printf("sum = %lld\n", (long long)a + (long long)b);
    return EXIT_SUCCESS;
}
```

```bash
gcc -std=c17 -Wall -Wextra -Wpedantic -g -O0 main.c -o sum
./sum 12 30
./sum abc 30                      # 返回失败，并把使用说明写到 stderr
```

参数说明：`-Wall -Wextra` 启用常见警告，`-g` 生成调试信息，`-O0` 便于入门单步调试，`-o` 指定输出文件。警告不应只靠强制类型转换消掉，要先理解原因。

## 用 GDB 观察参数与指针

```bash
gdb --args ./sum 12 30
```

在 GDB 内输入：

```text
break main
run
next
print argc
print argv[1]
break parse_int
continue
print text
print result
next
continue
quit
```

`result` 保存调用者变量的地址，`*result` 访问该地址对应的对象。这把你在 C 中学的指针、函数参数和进程地址空间连接起来了。

调试自己的内存错误时，还可尝试工具链支持的检测器：

```bash
gcc -std=c17 -Wall -Wextra -g -O1 -fsanitize=address,undefined \
    -fno-omit-frame-pointer main.c -o sum-check
./sum-check 12 30
```

检测器会增加开销，也不能证明程序没有所有错误；交叉编译环境可能不支持对应运行库。

## 一个最小 Makefile

```make
CC = gcc
CFLAGS = -std=c17 -Wall -Wextra -g -O0

sum: main.c
	$(CC) $(CFLAGS) main.c -o sum
```

配方行开头必须是实际 Tab，不是四个空格。执行 `make` 时，Make 会比较文件依赖和时间戳，按需构建。


---

[[linux/Linux基础与实战|← 返回总目录]] · [[linux/15-Bash脚本基础|上一篇：Bash脚本基础]] · [[linux/17-实战-日志统计脚本|下一篇：实战-日志统计脚本]]

