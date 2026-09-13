## Git 极简全能通关指南
[[learning]]

日常开发中，Git 的核心心法其实很简单：**“改代码 $\rightarrow$ 暂存区 $\rightarrow$ 本地库 $\rightarrow$ 远程库”**。下面为你整理了一份兼顾日常开发与团队协作的 Git 操作指南。

## 🛠️ 1. 初始化与配置

在电脑上第一次使用 Git 时，或者重装系统后，首先需要自报家门。

Bash

```
# 配置全局用户名和邮箱
git config --global user.name "YourName"
git config --global user.email "your_email@example.com"

# 查看当前配置
git config --list
```

### 新建本地仓库

Bash

```
cd my_project
git init  # 初始化本地 Git 仓库，会生成一个隐藏的 .git 文件夹
```

## 💻 2. 日常开发“死循环”

这是个人开发或写代码时最常用的高频命令。

代码段

```
graph LR
    A[工作区 Modified] -->|git add| B[暂存区 Staged]
    B -->|git commit| C[本地库 Committed]
    C -->|git push| D[远程库 Remote]
```

- **查看状态**：随时查看哪些文件被修改了、哪些还没提交。
    
    Bash
    
    ```
    git status
    ```
    
- **添加暂存区**：把修改过的文件托付给 Git 暂存。
    
    Bash
    
    ```
    git add .              # 暂存当前目录下所有修改过的文件（最常用）
    git add main.c         # 仅暂存指定文件
    ```
    
- **提交本地库**：为这次修改打上版本号快照。
    
    Bash
    
    ```
    git commit -m "feat: 完成电机PID控制算法调优"
    ```
    

## 🌿 3. 分支管理（团队协作/多任务并存）

不要直接在 `main` 或 `master` 分支上改代码！每开发一个新功能，都应该开一个独立的分支。

|**命令**|**作用**|
|---|---|
|`git branch`|查看本地所有分支（带 `*` 的为当前分支）|
|`git checkout -b feature-balance`|**新建并切换** 到名为 `feature-balance` 的新分支|
|`git switch main`|切换回主分支|
|`git merge feature-balance`|将 `feature-balance` 分支的代码**合并**到当前分支|
|`git branch -d feature-balance`|删除已合并的本地分支|

## ☁️ 4. 远程仓库同步（GitHub/Gitee）

将本地代码推送到云端备份，或者与队友协同。

### 关联远程库（仅需做一次）

Bash

```
git remote add origin git@github.com:username/repo-name.git
```

### 推送与拉取

- **首次推送**（建立本地与远程分支的追踪关系）：
    
    Bash
    
    ```
    git push -u origin main
    ```
    
- **后续日常推送**：
    
    Bash
    
    ```
    git push
    ```
    
- **拉取远程最新代码**：当队友更新了代码，用这个命令同步到本地。
    
    Bash
    
    ```
    git pull
    ```
    
- **克隆现有的项目**：直接下载远程仓库到本地。
    
    Bash
    
    ```
    git clone git@github.com:username/repo-name.git
    ```
    

## 🛡️ 5. 后悔药与时光机（版本回退）

写崩了、提错了？别慌，Git 都能救回来。

### 还没 commit，想放弃工作区的修改

Bash

```
git checkout -- main.c   # 撤销单个文件的修改（恢复到最近一次 commit 或 add 的状态）
git restore .            # 撤销本地所有未暂存的修改
```

### 已经 commit，但还没 push（仅撤销 commit 动作）

Bash

```
git reset --soft HEAD~1  # 撤销最近一次 commit，修改的代码仍然保留在暂存区
```

### 彻底回退到历史的某个版本（慎用！会覆盖本地修改）

Bash

```
# 1. 查看历史提交记录，找到你想回退的 commit ID（一串十六进制字符）
git log --oneline

# 2. 彻底回退到那个版本
git reset --hard <commit_id>
```

## 💡 6. 避坑进阶小 Tips

> 📌 **`.gitignore` 文件是刚需**
> 
> 项目根目录下一定要建一个 `.gitignore` 文件。把那些不需要进 Git 管理的编译生成文件（如 C 语言编译出的 `.o`、`.exe`，Keil 编译生成的 `Objects/`、`Listings/` 文件夹，或者 Python 的 `__pycache__/`、`.build` 文件夹）写进去。**不要把编译垃圾推送到远程库！**

> 📌 **遇到冲突（Conflict）怎么办？**
> 
> 当你和队友修改了同一个文件的同一行，`git pull` 时会报冲突。这时候 Git 会在代码里留下这种标记：
> 
> C
> 
> ```
> <<<<<<< HEAD
> // 你本地修改的代码
> motor_set_speed(100);
> =======
> // 队友推送到远程的代码
> motor_set_speed(120);
> >>>>>>> origin/main
> ```
> 
> **解决办法**：肉眼比对，删掉 Git 自动生成的标记行（`<<<<<<<`, `=======`, `>>>>>>>`），决定留下哪一部分代码，保存文件后重新执行 `git add .` 和 `git commit` 即可。