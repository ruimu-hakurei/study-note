# 15 Bash 脚本基础

[[linux/Linux基础与实战|← 返回总目录]] · [[linux/14-环境变量与PATH|上一篇：环境变量与PATH]] · [[linux/16-Linux下的C开发|下一篇：Linux下的C开发]]

---

## 脚本怎样运行

用编辑器创建 `hello.sh`：

```bash
#!/usr/bin/env bash
printf 'Hello, Linux!\n'
```

然后：

```bash
bash ./hello.sh                 # 显式用 Bash 解释，不要求脚本有执行位
chmod u+x ./hello.sh
./hello.sh                      # 依赖执行位和第一行解释器声明
```

## 引号：重要程度高于背命令

```bash
name='Linux learner'
printf '%s\n' "$name"          # 展开变量，结果作为一个参数
printf '%s\n' '$name'           # 单引号内不展开，输出字面 $name
```

```text
双引号：允许变量展开，但抑制通常的拆词和通配符展开
单引号：大部分内容按字面保留
不加引号：变量展开结果可能拆成多个参数，再展开通配符
```

对路径变量使用 `"$path"`；对一组参数使用 `"$@"`。不要用 `eval` 来执行拼接的用户输入。

## 参数和退出码

| 变量 | 含义 |
|---|---|
| `$0` | 当前脚本调用名 |
| `$1`、`$2` | 第一个、第二个位置参数 |
| `$#` | 参数数量 |
| `"$@"` | 保留每个参数边界地展开所有参数 |
| `$?` | 最近一条命令的退出码 |
| `$$` | 当前 Shell 的进程标识 |

## 条件、循环、函数

```bash
#!/usr/bin/env bash

show_file() {
    local path="$1"                    # local 限定在函数作用域
    if [[ -f "$path" && -r "$path" ]]; then
        printf '可读文件：%s\n' "$path"
    else
        printf '不是可读普通文件：%s\n' "$path" >&2
        return 1
    fi
}

for path in "$@"; do                   # 文件名包含空格也不会被拆开
    if ! show_file "$path"; then
        exit 1
    fi
done
```

`[[ ... ]]` 是 Bash 语法，不保证 `/bin/sh` 支持；`-f` 普通文件、`-d` 目录、`-r` 可读、`-e` 路径存在。数字比较可使用 `(( count > 10 ))`，赋值如 `count=$((count + 1))`。

## 严格模式不是万能保险

```bash
set -euo pipefail
```

- `-e`：部分失败情形下退出，但在条件、部分逻辑列表等位置有例外。
- `-u`：引用未设置变量时报错，位置参数要先检查。
- `pipefail`：让管道中的失败不只由末尾命令掩盖。

使用它们之后仍需检查预期的非零状态，如 `grep` 无匹配。运行脚本前可先用 `bash -n script.sh` 检查语法；`bash -x` 会显示展开后的命令，含密码时不要启用。完整规则见 [Bash 官方手册](https://www.gnu.org/s/bash/manual/bash.html)。


---

[[linux/Linux基础与实战|← 返回总目录]] · [[linux/14-环境变量与PATH|上一篇：环境变量与PATH]] · [[linux/16-Linux下的C开发|下一篇：Linux下的C开发]]

