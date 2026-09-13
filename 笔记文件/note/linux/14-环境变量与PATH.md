# 14 环境变量与 PATH

[[linux/Linux基础与实战|← 返回总目录]] · [[linux/13-压缩归档与同步|上一篇：压缩归档与同步]] · [[linux/15-Bash脚本基础|下一篇：Bash脚本基础]]

---

## Shell 变量与环境变量

```bash
project_name='sensor-demo'       # 当前 Shell 的变量，等号两边不能有空格
printf '%s\n' "$project_name"
export APP_MODE='development'    # 导出，之后启动的子进程可以继承
```

子进程通常得到父进程环境的一份副本；子进程改变自己的环境不会反向修改父 Shell。

```bash
printenv PATH
command -v gcc
```

`PATH` 是一组用冒号分隔的程序搜索目录。输入 `gcc` 时 Shell 会搜索它；`./app` 明确表示运行当前目录的文件。

```bash
# 只影响当前 Shell 及之后启动的子进程
export PATH="$HOME/.local/bin:$PATH"
```

不要把 `PATH` 覆盖成只有自己的一个目录，否则许多命令会“找不到”。也不建议把 `.` 放在 PATH 开头，避免误执行当前目录里的同名程序。

## Bash 配置文件

- `~/.bashrc`：交互式非登录 Bash 通常读取。
- `~/.bash_profile`、`~/.bash_login`、`~/.profile`：登录 Bash 按规则选择读取；发行版也可能通过这些文件引入 `.bashrc`。
- 不同 Shell、SSH 启动方式、脚本和 systemd 服务的环境可能不同，不能假设都会读 `.bashrc`。

```bash
source ~/.bashrc                 # 在当前 Shell 执行配置内容，会改变当前环境
```

不要 source 不可信文件。API 密钥和密码也不应直接写进可公开分享的脚本、笔记或命令历史。


---

[[linux/Linux基础与实战|← 返回总目录]] · [[linux/13-压缩归档与同步|上一篇：压缩归档与同步]] · [[linux/15-Bash脚本基础|下一篇：Bash脚本基础]]

