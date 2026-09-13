# 正态 Bayes 问题（正态均值的共轭推断）

> **一句话直觉：正态 Bayes 估计，就是把"先验均值"和"样本均值"按各自的信息精度做加权平均。**

前置：[[Bayes基础]]、[[正态分布]] ｜ 相关：[[MLE]]、[[Cramér–Rao不等式]]、[[控制算法-卡尔曼滤波]]

---

## 问题设定

观测到

$$X_1,\dots,X_n \mid \mu \ \sim\ N(\mu, \sigma^2) \quad \text{(i.i.d.)}$$

其中 $\mu$ 是未知参数，$\sigma^2$ **已知**。给 $\mu$ 一个正态先验：

$$\mu \sim N(\mu_0, \tau^2)$$

$\mu_0$ 是先验均值，$\tau^2$ 是先验方差。这就是最经典的

$$\text{正态似然} + \text{正态先验}$$

它的后验仍是正态分布，所以正态是自己的**共轭先验**。

---

## 一、 先看直觉

看样本之前我们认为 $\mu \sim N(\mu_0, \tau^2)$。比如 $\mu_0 = 100$，表示原本认为 $\mu$ 大概在 $100$ 附近；

- $\tau^2$ **越小** → 越相信这个先验；
- $\tau^2$ **越大** → 对先验越没把握。

然后观察数据，得到样本均值 $\bar X$。如果 $\bar X \ne \mu_0$，Bayes 会在两者之间做折中：

$$\boxed{\ \text{后验均值} = \text{先验均值与样本均值的加权平均}\ }$$

这就是整道题最重要的直觉，剩下的全部工作只是**把权重算出来**。

---

## 二、 完整推导：似然 $\times$ 先验 $\to$ 配平方

目标有两个：① 求 $\mu$ 的后验分布；② 求平方损失下 $\mu$ 的 Bayes 估计。

推导全程把观测值写作小写 $x_i,\ \bar x$（视为已知常数），最后再换回随机变量 $\bar X$ 写估计量。

### 0. 起点：Bayes 公式

$$\pi(\mu\mid x) \propto L(\mu)\,\pi(\mu) \qquad\Longleftrightarrow\qquad \text{后验} \propto \text{似然}\times\text{先验}$$

所以只需把"似然"和"先验"分别写出来，再相乘。

### 1. 写出似然函数

每个样本 $X_i\mid\mu \sim N(\mu,\sigma^2)$，单个样本密度：

$$f(x_i\mid\mu) = \frac{1}{\sqrt{2\pi\sigma^2}}\exp\left[-\frac{(x_i-\mu)^2}{2\sigma^2}\right]$$

$n$ 个样本独立，联合密度即连乘：

$$L(\mu) = \prod_{i=1}^n f(x_i\mid\mu) = \left(\frac{1}{\sqrt{2\pi\sigma^2}}\right)^{\!n}\exp\left[-\frac{1}{2\sigma^2}\sum_{i=1}^n (x_i-\mu)^2\right]$$

### 2. 为什么可以把常数全扔掉？

现在把 $L(\mu)$ 看作**关于 $\mu$ 的函数**。前面的 $\left(2\pi\sigma^2\right)^{-n/2}$ 完全不含 $\mu$，它只是把整条曲线整体放缩，不改变形状，最终会被后验的归一化常数吸收。因此

$$L(\mu) \propto \exp\left[-\frac{1}{2\sigma^2}\sum_{i=1}^n (x_i-\mu)^2\right]$$

问题归结为如何处理 $\sum_{i=1}^n (x_i-\mu)^2$。

### 3. 平方和分解恒等式（附证明）

$$\boxed{\ \sum_{i=1}^n (x_i-\mu)^2 = \sum_{i=1}^n (x_i-\bar x)^2 + n(\bar x-\mu)^2\ },\qquad \bar x = \frac{x_1+\cdots+x_n}{n}$$

**证明**：在括号里"加一项减一项"，凑出 $\bar x$，再展开：

$$\sum_{i=1}^n (x_i-\mu)^2 = \sum_{i=1}^n \big[(x_i-\bar x) + (\bar x-\mu)\big]^2$$

$$= \sum_{i=1}^n (x_i-\bar x)^2 + 2(\bar x-\mu)\sum_{i=1}^n (x_i-\bar x) + n(\bar x-\mu)^2$$

关键在交叉项：由样本均值的定义 $\sum_{i=1}^n x_i = n\bar x$，故

$$\sum_{i=1}^n (x_i-\bar x) = \sum_{i=1}^n x_i - n\bar x = 0$$

交叉项整体为零，恒等式得证。$\blacksquare$

第一项 $\sum (x_i-\bar x)^2$ 完全不含 $\mu$，对 $\mu$ 而言只是常数，可以扔掉。于是

$$\boxed{\ L(\mu) \propto \exp\left[-\frac{n}{2\sigma^2}(\mu-\bar x)^2\right]\ }$$

> 这一步非常重要，它说明两件事：
> 1. **似然作为 $\mu$ 的函数本身就是一个正态核**，中心在 $\bar x$、"方差"为 $\sigma^2/n$；
> 2. **样本对 $\mu$ 提供的信息，全部只通过 $\bar x$ 进入**——即 $\bar x$ 是 $\mu$ 的充分统计量（见 [[充分统计量]]）。

### 4. 写出先验

$$\pi(\mu) = \frac{1}{\sqrt{2\pi\tau^2}}\exp\left[-\frac{(\mu-\mu_0)^2}{2\tau^2}\right] \propto \exp\left[-\frac{(\mu-\mu_0)^2}{2\tau^2}\right]$$

同样丢掉不依赖 $\mu$ 的常数。

### 5. 似然 $\times$ 先验

$$\pi(\mu\mid x) \propto \exp\left[-\frac{n}{2\sigma^2}(\mu-\bar x)^2\right]\cdot\exp\left[-\frac{1}{2\tau^2}(\mu-\mu_0)^2\right]$$

利用 $e^{A}e^{B} = e^{A+B}$ 合并指数：

$$\pi(\mu\mid x) \propto \exp\left\{-\frac{1}{2}\left[\frac{n}{\sigma^2}(\mu-\bar x)^2 + \frac{1}{\tau^2}(\mu-\mu_0)^2\right]\right\}$$

现在真正的难点是：**怎么把中括号里这一坨重新认成一个正态分布？** 答案是配平方。

### 6. 展开并按 $\mu$ 的幂次合并

分别展开两个平方：

$$(\mu-\bar x)^2 = \mu^2 - 2\mu\bar x + \bar x^2, \qquad (\mu-\mu_0)^2 = \mu^2 - 2\mu\mu_0 + \mu_0^2$$

代回中括号：

$$\frac{n}{\sigma^2}\big(\mu^2-2\mu\bar x+\bar x^2\big) + \frac{1}{\tau^2}\big(\mu^2-2\mu\mu_0+\mu_0^2\big)$$

按 $\mu$ 的幂次归并三类项：

| 项 | 系数 |
| :--- | :--- |
| $\mu^2$ | $\dfrac{n}{\sigma^2}+\dfrac{1}{\tau^2}$ |
| $\mu$ | $-2\left(\dfrac{n\bar x}{\sigma^2}+\dfrac{\mu_0}{\tau^2}\right)$ |
| 常数 | $\dfrac{n\bar x^2}{\sigma^2}+\dfrac{\mu_0^2}{\tau^2}$ |

最后一行不含 $\mu$，仍可当作常数忽略（第 9 小节会回头交代它到底是什么）。于是只需处理

$$\left(\frac{n}{\sigma^2}+\frac{1}{\tau^2}\right)\mu^2 - 2\left(\frac{n\bar x}{\sigma^2}+\frac{\mu_0}{\tau^2}\right)\mu$$

### 7. 简写后配平方

记

$$A = \frac{n}{\sigma^2}+\frac{1}{\tau^2}, \qquad B = \frac{n\bar x}{\sigma^2}+\frac{\mu_0}{\tau^2}$$

上式即 $A\mu^2 - 2B\mu$。提出 $A$：

$$A\mu^2 - 2B\mu = A\left(\mu^2 - 2\frac{B}{A}\mu\right)$$

再用配方恒等式 $\mu^2 - 2c\mu = (\mu-c)^2 - c^2$（取 $c = B/A$）：

$$A\mu^2 - 2B\mu = A\left(\mu-\frac{B}{A}\right)^2 - \frac{B^2}{A}$$

末项 $-B^2/A$ 又不含 $\mu$，照样忽略。因此后验密度化为

$$\boxed{\ \pi(\mu\mid x) \propto \exp\left[-\frac{A}{2}\left(\mu-\frac{B}{A}\right)^2\right]\ }$$

### 8. 与正态标准形式比较

正态分布 $N(m,v)$ 的核是

$$\exp\left[-\frac{1}{2v}(\mu-m)^2\right]$$

与上式逐项对照：

$$\frac{1}{v} = A \ \Longrightarrow\ v = \frac{1}{A} = \frac{1}{\dfrac{n}{\sigma^2}+\dfrac{1}{\tau^2}}, \qquad m = \frac{B}{A} = \frac{\dfrac{n\bar x}{\sigma^2}+\dfrac{\mu_0}{\tau^2}}{\dfrac{n}{\sigma^2}+\dfrac{1}{\tau^2}}$$

**为什么"正比于正态核"就能断定它 _就是_ 正态分布？** 因为后验是一个概率密度，必须满足 $\int_{-\infty}^{+\infty}\pi(\mu\mid x)\,d\mu = 1$。设 $\pi(\mu\mid x) = c\exp\left[-\frac{A}{2}(\mu-m)^2\right]$，由 Gauss 积分

$$\int_{-\infty}^{+\infty} \exp\left[-\frac{A}{2}(\mu-m)^2\right]d\mu = \sqrt{\frac{2\pi}{A}}\quad (A>0)$$

归一化条件把常数**唯一地**逼成 $c = \sqrt{A/2\pi}$，这恰是 $N(m,1/A)$ 的密度常数。所以

$$\boxed{\ \mu\mid x \sim N(m,\ v)\ }$$

一路丢掉的所有常数，在这里被归一化一次性补回——这正是全程只写 $\propto$ 却不损失严谨性的原因。

把观测值 $\bar x$ 换回随机变量 $\bar X$，就得到下一节的估计量形式。

### 9. 附：被扔掉的那些常数到底是什么？

推导中被丢弃的与 $\mu$ 无关的项，合起来是 $\exp\left[-\frac{1}{2}\left(K - \dfrac{B^2}{A}\right)\right]$，其中 $K = \dfrac{n\bar x^2}{\sigma^2}+\dfrac{\mu_0^2}{\tau^2}$。它并非凭空消失，而正是 Bayes 公式的分母（边缘分布 $m(x)$）中依赖数据的那部分。

仍记 $a = n/\sigma^2,\ b = 1/\tau^2$（则 $A = a+b$，$B = a\bar x + b\mu_0$，$K = a\bar x^2 + b\mu_0^2$）：

$$K - \frac{B^2}{A} = \frac{AK-B^2}{A} = \frac{(a+b)(a\bar x^2+b\mu_0^2)-(a\bar x+b\mu_0)^2}{a+b}$$

分子展开后 $a^2\bar x^2$ 与 $b^2\mu_0^2$ 相消，只剩交叉项：

$$= \frac{ab\,\bar x^2 - 2ab\,\bar x\mu_0 + ab\,\mu_0^2}{a+b} = \frac{ab}{a+b}(\bar x-\mu_0)^2$$

而 $\dfrac{ab}{a+b} = \dfrac{1}{\frac1a+\frac1b} = \dfrac{1}{\frac{\sigma^2}{n}+\tau^2}$，所以被扔掉的因子恰好是

$$\exp\left[-\frac{(\bar x-\mu_0)^2}{2\left(\tau^2+\frac{\sigma^2}{n}\right)}\right]$$

这是 $N\!\left(\mu_0,\ \tau^2+\frac{\sigma^2}{n}\right)$ 的正态核——也就是 $\bar X$ 的**边缘分布（先验预测分布）**：

$$\bar X \sim N\!\left(\mu_0,\ \tau^2+\frac{\sigma^2}{n}\right)$$

这个结果单独看也很自然：$\bar X = \mu + (\bar X - \mu)$，其中 $\mu\sim N(\mu_0,\tau^2)$ 与 $\bar X-\mu\sim N(0,\sigma^2/n)$ 独立，由正态可加性方差直接相加。

> 换句话说：**丢掉的常数 $=$ 数据本身出现的概率**。它不影响后验形状，但决定了这批数据有多"令人意外"——与第九节⑥的后验预测分布是同一套逻辑。

---

## 三、 核心结论

$$\boxed{\ \mu \mid X \ \sim\ N(m,\ v)\ }$$

**后验方差**（精度形式最好记）：

$$\frac{1}{v} = \frac{n}{\sigma^2} + \frac{1}{\tau^2} \qquad\Longrightarrow\qquad \boxed{\ v = \frac{1}{\dfrac{n}{\sigma^2}+\dfrac{1}{\tau^2}} = \frac{\sigma^2\tau^2}{n\tau^2 + \sigma^2}\ }$$

**后验均值**：

$$\boxed{\ m = \frac{\dfrac{n}{\sigma^2}\bar X + \dfrac{1}{\tau^2}\mu_0}{\dfrac{n}{\sigma^2}+\dfrac{1}{\tau^2}} = \frac{n\tau^2 \bar X + \sigma^2\mu_0}{n\tau^2+\sigma^2}\ }$$

**平方损失下的 Bayes 估计**即后验均值（见 [[Bayes基础]] 第五节）：

$$\boxed{\ \hat\mu_B = E(\mu\mid X) = m\ }$$

---

## 四、 精度视角：全篇最值得记的一句话

$$\boxed{\ \text{后验精度} = \text{先验精度} + \text{样本精度}\ }\qquad \frac{1}{v} = \frac{1}{\tau^2} + \frac{n}{\sigma^2}$$

这里**精度（precision）$=$ 方差的倒数**：方差越小 → 精度越大 → 信息越可靠。

后验均值则是两个中心按精度加权：

$$m = \frac{a}{a+b}\bar X + \frac{b}{a+b}\mu_0, \qquad \frac{a}{a+b}+\frac{b}{a+b}=1$$

写成完全脱离符号的形式，就是这一节唯一需要记的东西：

$$\boxed{\ \text{后验均值} = \frac{\text{样本精度}\times\bar X + \text{先验精度}\times\mu_0}{\text{样本精度}+\text{先验精度}}\ }$$

> 谁更可靠，谁的方差更小；谁方差更小，谁精度更大；**谁精度更大，谁在后验均值中的权重就更大。**

### 为什么样本精度是 $n/\sigma^2$？

因为真正与先验"对话"的不是单个 $X_i$，而是**样本均值** $\bar X$。由 $X_i\sim N(\mu,\sigma^2)$ 独立同分布得

$$\bar X \sim N\!\left(\mu,\ \frac{\sigma^2}{n}\right)$$

故 $\bar X$ 的方差是 $\sigma^2/n$，取倒数即得它的精度：

$$\frac{1}{\sigma^2/n} = \frac{n}{\sigma^2} = a$$

所以第三节那个加权平均，本质上是在比较两件事的不确定性：

| 信息来源 | 中心 | 不确定性（方差） | 精度 |
| :--- | :--- | :--- | :--- |
| 先验 | $\mu_0$ | $\tau^2$ | $b = 1/\tau^2$ |
| 数据 | $\bar X$ | $\sigma^2/n$ | $a = n/\sigma^2$ |

样本量 $n$ 越大，$\bar X$ 越稳定 → 精度越高 → 权重越大。**"$n$ 越多越可信"这件事，就是通过 $a=n/\sigma^2$ 随 $n$ 线性增长体现出来的。**

### 与 Fisher 信息的联系

对 $N(\mu,\sigma^2)$（$\sigma^2$ 已知），单个样本关于 $\mu$ 的 Fisher 信息为

$$I(\mu) = -E\left[\frac{\partial^2}{\partial\mu^2}\ln f(X;\mu)\right] = \frac{1}{\sigma^2}$$

故 $n$ 个样本的 Fisher 信息**恰好**就是 $n/\sigma^2 = a$。所以"样本精度"不是打比方，它就是 Fisher 信息本身：

$$\text{后验信息} = \text{先验信息} + \text{样本 Fisher 信息}$$

这与 [[Cramér–Rao不等式]] 中"信息越多 $\Rightarrow$ 方差越小"是同一条脉络。

> **工程上的同一件事**：[[控制算法-卡尔曼滤波]] 的更新步就是这个公式——先验（预测）与观测按各自精度融合，卡尔曼增益扮演的正是这里的权重 $a/(a+b)$。

---

## 五、 收缩（Shrinkage）

频率学派直接用 $\bar X$；Bayes 给的是

$$\hat\mu_B = w\bar X + (1-w)\mu_0, \qquad w = \frac{a}{a+b} = \frac{n\tau^2}{n\tau^2+\sigma^2}$$

改写成更能看出"拉扯"的形式：

$$\hat\mu_B = \bar X - (1-w)(\bar X - \mu_0)$$

即把 $\bar X$ 朝先验均值 $\mu_0$ 拉回一段，这种现象称为**收缩（shrinkage）**。

代价是引入了偏差，换来的是方差变小、小样本下更稳健——这也是 Bayes 估计通常**不是无偏估计**的原因。

---

## 六、 极限行为：先验与数据的拉锯

| 情形 | 精度变化 | 后验均值 $m$ | 后验方差 $v$ | 解读 |
| :--- | :--- | :--- | :--- | :--- |
| $n\to\infty$ | $a\to\infty$ | $\to \bar X$ | $\to 0$ | **数据压过先验**，退化为 MLE |
| $\tau^2\to\infty$ | $b\to 0$ | $\to \bar X$ | $\to \sigma^2/n$ | 无信息（平坦）先验，结果与 [[MLE]] 完全一致 |
| $\tau^2\to 0$ | $b\to\infty$ | $\to \mu_0$ | $\to 0$ | 先验是"铁的信念"，数据撼动不了 |
| $n$ 很小 | $a$ 小 | 靠近 $\mu_0$ | 接近 $\tau^2$ | 几个样本不该推翻既有认识 |

两条结论：

- Bayes 并非"永远被先验控制"——**数据足够多，先验的影响必然衰减**；
- 反过来，**先验越强（$\tau^2$ 越小），需要越多样本才能明显拉动它**。

---

## 七、 后验方差一定比两者都小

由 $\dfrac{1}{v} = \dfrac{1}{\tau^2} + \dfrac{n}{\sigma^2}$，两个正数相加必然大于其中任何一个，所以

$$\boxed{\ v < \tau^2 \quad \text{且} \quad v < \frac{\sigma^2}{n}\ }$$

注意这是**严格且恒成立**的（只要 $\tau^2,\sigma^2$ 有限）：融合后的不确定性一定小于单独用先验、也小于单独用数据。

> 加入样本以后，我们对 $\mu$ 的不确定性一定减少——这正是 Bayes 更新最符合直觉的地方。

---

## 八、 数值算例

设 $\mu_0 = 100$，$\tau^2 = 25$，已知 $\sigma^2 = 100$，样本量 $n = 25$，观察到 $\bar X = 110$。

**第一步，算两个精度：**

$$a = \frac{n}{\sigma^2} = \frac{25}{100} = 0.25, \qquad b = \frac{1}{\tau^2} = \frac{1}{25} = 0.04$$

样本信息明显更强（$0.25 \gg 0.04$），权重 $w = 0.25/0.29 \approx 0.862$。

**第二步，后验均值：**

$$m = \frac{0.25\times 110 + 0.04\times 100}{0.25+0.04} = \frac{27.5+4}{0.29} = \frac{31.5}{0.29} \approx 108.62$$

**第三步，后验方差：**

$$v = \frac{1}{0.29} \approx 3.448, \qquad \sqrt{v}\approx 1.857$$

结果核对：

| 量 | 值 |
| :--- | :--- |
| 先验均值 | $100$ |
| 样本均值 | $110$ |
| **后验均值** | $\approx 108.62$ |
| 先验方差 $\tau^2$ | $25$ |
| 样本均值的方差 $\sigma^2/n$ | $4$ |
| **后验方差** $v$ | $\approx 3.448$ |

后验均值确实落在 $100$ 与 $110$ 之间，且因样本信息更强而更靠近 $110$；后验方差 $3.448$ 同时小于 $25$ 和 $4$，印证第七节。

---

## 九、 常见题型

**① 求后验分布**（最经典）：$\sigma^2$ 已知、$\mu\sim N(\mu_0,\tau^2)$，答案 $\mu\mid X\sim N(m,v)$。

**② 代数计算**：给定具体先验与数据，算 $m$ 和 $v$——先算 $a,b$ 两个精度，其余都是加权平均，最不容易错。

**③ 平方损失下的 Bayes 估计**：直接取 $E(\mu\mid X) = m$。

**④ MAP 估计**：后验是正态分布，而**正态的均值 $=$ 中位数 $=$ 众数**，所以三种损失（平方 / 绝对 / $0\text{-}1$）给出的 Bayes 估计在这里**完全重合**：

$$\boxed{\ \hat\mu_{MAP} = \text{后验中位数} = \hat\mu_B = m\ }$$

这是正态情形独有的便利，换成 Beta、Gamma 后验就不成立了。

**⑤ 可信区间（Credible Interval）**：由 $\mu\mid X\sim N(m,v)$ 直接得 $1-\alpha$ 可信区间

$$m \pm z_{\alpha/2}\sqrt{v}$$

上面的算例中 $95\%$ 可信区间为 $108.62 \pm 1.96\times 1.857 \approx (104.98,\ 112.26)$。

注意它的解释与置信区间不同：这里可以直接说"$\mu$ 落在此区间的概率是 $95\%$"。

**⑥ 后验预测分布**：预测下一个观测 $X_{n+1}$。因为 $X_{n+1} = \mu + \varepsilon$，其中 $\mu\mid X\sim N(m,v)$ 与 $\varepsilon\sim N(0,\sigma^2)$ 独立，由正态的可加性（见 [[正态分布的叠加性与稳定性]]）：

$$X_{n+1}\mid X \ \sim\ N(m,\ v+\sigma^2)$$

方差是**参数不确定性 $v$ $+$ 观测噪声 $\sigma^2$** 两部分之和。

---

## 十、 压缩成一张逻辑图

$$\text{先验 } \mu\sim N(\mu_0,\tau^2) \quad + \quad \text{样本 } X_i\mid\mu\sim N(\mu,\sigma^2)\ \big(\text{只通过 }\bar X\text{ 起作用}\big)$$

$$\downarrow \ \text{配平方}$$

$$\boxed{\ \text{后验精度} = \frac{1}{\tau^2}+\frac{n}{\sigma^2}\ } \qquad \boxed{\ m = \frac{\frac{1}{\tau^2}\mu_0 + \frac{n}{\sigma^2}\bar X}{\frac{1}{\tau^2}+\frac{n}{\sigma^2}}\ } \qquad \boxed{\ v = \frac{1}{\frac{1}{\tau^2}+\frac{n}{\sigma^2}}\ }$$

$$\downarrow$$

$$\boxed{\ \mu\mid X\sim N(m,v),\qquad \hat\mu_B = m\ }$$

把这两句话吃透，正态 Bayes 问题基本就掌握了：

> **精度 $=$ 方差的倒数；后验精度 $=$ 先验精度 $+$ 样本精度。**

---

**延伸**：若 $\sigma^2$ 也未知，共轭先验变为**正态–逆 Gamma**（$\mu\mid\sigma^2 \sim N(\mu_0,\sigma^2/\kappa_0)$，$\sigma^2\sim \text{Inv-Ga}(\alpha,\beta)$），此时 $\mu$ 的边际后验是 **$t$ 分布**而非正态（见 [[t分布]]）——尾部更厚，正是"方差本身也不确定"的代价。
