# Cramér–Rao 不等式

## 一、问题：无偏估计量的方差有下界吗？

### 1. 从问题出发

假设总体中有未知参数 $\theta$，想估计某个量 $g(\theta)$。找到一个无偏估计量 $U$：

$$E_\theta(U) = g(\theta)$$

现在我们最关心它的方差 $\operatorname{Var}_\theta(U)$，因为方差越小，估计越稳定。自然就会问：**方差能不能无限小？**

答案是通常不能。在一定条件下，Cramér–Rao 不等式告诉我们：

$$\boxed{\operatorname{Var}_\theta(U) \ge \frac{[g'(\theta)]^2}{I_n(\theta)}}$$

右边就是无偏估计量方差的一个**理论下界**（Cramér–Rao 下界，简称 CRLB）。

### 2. 最简单的特殊形式

如果直接估计 $\theta$ 本身，即 $g(\theta) = \theta$，则 $g'(\theta) = 1$，不等式变成：

$$\boxed{\operatorname{Var}_\theta(U) \ge \frac{1}{I_n(\theta)}}$$

所以可以先把它记成一句话：

> **无偏估计量的方差 ≥ Fisher 信息量的倒数。**

### 3. Fisher 信息量的直觉

$I_n(\theta)$ 叫做 **Fisher 信息量**，衡量的是**样本中到底包含多少关于未知参数 $\theta$ 的信息**。

信息越多，$I_n(\theta)$ 越大，$\frac{1}{I_n(\theta)}$ 越小，方差就能做到更小。这非常符合直觉：**样本里关于 $\theta$ 的信息越多，就越能精确估计 $\theta$。**

## 二、Fisher 信息量

### 1. 定义：得分函数与 Fisher 信息

先看一个样本 $X$，其密度（或概率质量函数）为 $f(x;\theta)$。取对数后对 $\theta$ 求导：

$$\frac{\partial}{\partial\theta}\ln f(X;\theta)$$

这个量叫做**得分函数**（score function），记为

$$S(\theta) = \frac{\partial}{\partial\theta}\ln f(X;\theta)$$

Fisher 信息量定义为得分函数的二阶矩：

$$\boxed{I(\theta) = E_\theta\big[S(\theta)^2\big] = E_\theta\left[\left(\frac{\partial}{\partial\theta}\ln f(X;\theta)\right)^2\right]}$$

### 2. 为什么要先取对数

假设有 $n$ 个独立样本，联合密度是乘法：

$$L(\theta) = \prod_{i=1}^n f(X_i;\theta)$$

直接求导很麻烦。取对数后乘法变成加法：

$$\ln L(\theta) = \sum_{i=1}^n \ln f(X_i;\theta)$$

再求导：

$$\frac{\partial}{\partial\theta}\ln L(\theta) = \sum_{i=1}^n \frac{\partial}{\partial\theta}\ln f(X_i;\theta)$$

所以取对数主要是为了让计算大大简化。

### 3. n 个样本的信息量：$I_n = nI_1$

如果 $X_1,\dots,X_n$ [[总体与样本抽样|独立同分布]]，Fisher 信息可以相加：

$$\boxed{I_n(\theta) = n\,I_1(\theta)}$$

其中 $I_1(\theta)$ 是一个样本带来的信息，$I_n(\theta)$ 是 $n$ 个样本的总信息。于是

$$\operatorname{Var}(U) \ge \frac{[g'(\theta)]^2}{n\,I_1(\theta)}$$

一个非常重要的趋势：

$$n \uparrow \ \Rightarrow\ I_n(\theta) \uparrow \ \Rightarrow\ \text{方差下界} \downarrow$$

也就是说：**样本越多，理论上能够估计得越准。**

## 三、例子：计算 Cramér–Rao 下界

### 1. Bernoulli 分布（估计 $p$）

设 $X_1,\dots,X_n \sim \text{Bernoulli}(p)$，即 $P(X=1)=p,\ P(X=0)=1-p$。一个样本的概率质量函数为

$$f(x;p) = p^x(1-p)^{1-x}$$

取对数：

$$\ln f(x;p) = x\ln p + (1-x)\ln(1-p)$$

对 $p$ 求导：

$$\frac{\partial}{\partial p}\ln f(x;p) = \frac{x}{p} - \frac{1-x}{1-p} = \frac{x-p}{p(1-p)}$$

所以得分函数为

$$S(p) = \frac{X-p}{p(1-p)}$$

按定义求 Fisher 信息：

$$I_1(p) = E[S(p)^2] = \frac{E[(X-p)^2]}{p^2(1-p)^2}$$

因为 $E(X)=p$，故 $E[(X-p)^2] = \operatorname{Var}(X) = p(1-p)$，于是

$$\boxed{I_1(p) = \frac{1}{p(1-p)}} \qquad \Rightarrow \qquad \boxed{I_n(p) = \frac{n}{p(1-p)}}$$

现在估计的是 $p$ 本身（$g(p)=p$，$g'(p)=1$），所以

$$\boxed{\operatorname{Var}(U) \ge \frac{p(1-p)}{n}}$$

意思是：**任何无偏估计 $p$ 的统计量，方差都不可能低于这个数。**

而[[样本均值与样本方差|样本均值]] $\bar{X} = \frac{1}{n}\sum X_i$ 满足 $E(\bar{X})=p$、$\operatorname{Var}(\bar{X}) = \frac{p(1-p)}{n}$，**刚好等于下界**，所以

$$\boxed{\bar{X} \text{ 达到了 Cramér–Rao 下界}}$$

它已经不可能再通过其他无偏估计量降低方差，因此 $\bar{X}$ 是 $p$ 的最小方差无偏估计量——这和前面的 UMVUE 联系起来了。

### 2. 正态分布（估计 $\mu$）

设 $X_1,\dots,X_n \sim N(\mu,\sigma^2)$，$\sigma^2$ 已知，估计 $\mu$。一个样本的密度：

$$f(x;\mu) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left[-\frac{(x-\mu)^2}{2\sigma^2}\right]$$

取对数：

$$\ln f(x;\mu) = -\frac12\ln(2\pi\sigma^2) - \frac{(x-\mu)^2}{2\sigma^2}$$

对 $\mu$ 求导：

$$\frac{\partial}{\partial\mu}\ln f(x;\mu) = \frac{x-\mu}{\sigma^2}$$

因此

$$I_1(\mu) = E\left[\left(\frac{X-\mu}{\sigma^2}\right)^2\right] = \frac{E[(X-\mu)^2]}{\sigma^4} = \frac{\sigma^2}{\sigma^4} = \frac{1}{\sigma^2}$$

所以

$$I_n(\mu) = \frac{n}{\sigma^2}, \qquad \boxed{\operatorname{Var}(U) \ge \frac{\sigma^2}{n}}$$

而 $\operatorname{Var}(\bar{X}) = \frac{\sigma^2}{n}$ 刚好等于下界，故 $\bar{X}$ 达到 Cramér–Rao 下界，是 $\mu$ 的有效估计量。

### 3. "下界"像一条地板：有效估计量

可以把 Cramér–Rao 下界想象成一条地板：

```
方差
↑

│      某个无偏估计量
│           ●
│
│    另一个无偏估计量
│       ●
│
│--------------------------  Cramér–Rao 下界
│       ●  X̄
│
└────────────────────────→
```

任何无偏估计量都不能突破这条地板：$\operatorname{Var}(U) \ge CRLB$。

如果某个估计量刚好站在地板上（$\operatorname{Var}(U) = CRLB$），说明它已经达到理论极限了——这种估计量称为**有效估计量**（efficient estimator）。

## 四、Cramér–Rao 不等式为什么成立？（完整证明）

设样本 $X=(X_1,\dots,X_n)$，联合密度 $f(x;\theta)$，统计量 $U$ 无偏估计 $g(\theta)$（$E_\theta(U)=g(\theta)$）。整个证明围绕**三个关键等式**展开。

### 1. 三个关键等式

**（1）$E[S(\theta)] = 0$：得分函数的期望为 0**

得分函数可写成

$$S(\theta) = \frac{\partial}{\partial\theta}\ln f(X;\theta) = \frac{1}{f(X;\theta)}\frac{\partial f(X;\theta)}{\partial\theta}$$

（因为 $\frac{\partial}{\partial\theta}\ln f = \frac1f\frac{\partial f}{\partial\theta}$。）

从期望定义出发：

$$E_\theta[S(\theta)] = \int S(\theta)\,f(x;\theta)\,dx = \int \frac{1}{f(x;\theta)}\frac{\partial f(x;\theta)}{\partial\theta}\,f(x;\theta)\,dx = \int \frac{\partial f(x;\theta)}{\partial\theta}\,dx$$

在正则条件下，可以把"对 $\theta$ 求导"拿到积分号外：

$$= \frac{\partial}{\partial\theta}\int f(x;\theta)\,dx = \frac{\partial}{\partial\theta}(1) = 0$$

$$\boxed{E_\theta[S(\theta)] = 0}$$

**直觉**：得分函数衡量"当 $\theta$ 稍微变化时，当前样本把似然往哪个方向推"。某些样本让似然倾向于 $\theta$ 变大（得分为正），某些让 $\theta$ 变小（得分为负）。在真实参数 $\theta$ 下把所有可能样本平均起来，正负作用刚好抵消，所以 $E(S)=0$。

**（2）$\operatorname{Cov}(U,S) = g'(\theta)$：[[无偏性]]锁定关联**

由无偏性 $E_\theta(U) = g(\theta)$，写成积分：

$$\int U(x)\,f(x;\theta)\,dx = g(\theta)$$

两边对 $\theta$ 求导（$U$ 是样本的函数，不直接含 $\theta$，正则条件下可交换求导与积分）：

$$\int U(x)\,\frac{\partial f(x;\theta)}{\partial\theta}\,dx = g'(\theta)$$

利用 $\frac{\partial f}{\partial\theta} = f\,\frac{\partial\ln f}{\partial\theta}$：

$$\int U(x)\,f(x;\theta)\,\frac{\partial\ln f(x;\theta)}{\partial\theta}\,dx = g'(\theta)$$

而 $\frac{\partial\ln f(X;\theta)}{\partial\theta} = S(\theta)$，所以上式就是

$$E_\theta[U S] = g'(\theta)$$

再结合[[协方差]]定义和 $E(S)=0$：

$$\operatorname{Cov}(U,S) = E(US) - E(U)E(S) = E(US) - 0 = g'(\theta)$$

$$\boxed{\operatorname{Cov}(U,S) = g'(\theta)}$$

**直觉**：无偏估计量 $U$ 与"样本中关于 $\theta$ 的信息方向"$S$ 之间的相关程度，恰好等于 $g(\theta)$ 对 $\theta$ 的变化率。

**（3）$\operatorname{Var}(S) = I_n(\theta)$：Fisher 信息 = 得分函数的方差**

Fisher 信息定义为 $I_n(\theta) = E[S(\theta)^2]$。由 $E[S(\theta)] = 0$：

$$\operatorname{Var}(S) = E(S^2) - [E(S)]^2 = E(S^2) = I_n(\theta)$$

$$\boxed{\operatorname{Var}(S) = I_n(\theta)}$$

所以 Fisher 信息可理解为**得分函数的方差**：得分函数波动越大，样本对 $\theta$ 越敏感，包含的信息越多。

### 2. 用 Cauchy-Schwarz 收尾

对任意两个随机变量 $A, B$：

$$\operatorname{Cov}(A,B)^2 \le \operatorname{Var}(A)\,\operatorname{Var}(B)$$

令 $A=U$、$B=S$：

$$\operatorname{Cov}(U,S)^2 \le \operatorname{Var}(U)\,\operatorname{Var}(S)$$

代入 $\operatorname{Cov}(U,S)=g'(\theta)$ 和 $\operatorname{Var}(S)=I_n(\theta)$：

$$[g'(\theta)]^2 \le \operatorname{Var}(U)\,I_n(\theta)$$

两边除以 $I_n(\theta)$：

$$\boxed{\operatorname{Var}(U) \ge \frac{[g'(\theta)]^2}{I_n(\theta)}}$$

这就是 Cramér–Rao 不等式。

### 3. 证明主线（四步压缩）

1. 无偏性 $E(U)=g(\theta)$，对 $\theta$ 求导得 $E(US)=g'(\theta)$；
2. 因 $E(S)=0$，得 $\operatorname{Cov}(U,S)=g'(\theta)$；
3. Fisher 信息：$\operatorname{Var}(S)=I_n(\theta)$；
4. Cauchy-Schwarz：$[g'(\theta)]^2 \le \operatorname{Var}(U)\,I_n(\theta)$，即得下界。

### 4. 为什么会出现"下界"？（几何视角）

把中心化随机变量看成向量：$U-E(U)$ 与 $S-E(S)$（因 $E(S)=0$，后者就是 $S$）。协方差是"内积"，方差是"长度平方"，所以 Cauchy-Schwarz

$$\operatorname{Cov}(U,S)^2 \le \operatorname{Var}(U)\,\operatorname{Var}(S)$$

和向量里的 $(\mathbf{a}\cdot\mathbf{b})^2 \le \|\mathbf{a}\|^2\|\mathbf{b}\|^2$ 是同一个结构。

关键是：无偏性把 $U$ 与 $S$ 的"内积"锁死了（$\operatorname{Cov}(U,S)=g'(\theta)$），$S$ 的长度也由 Fisher 信息确定（$\operatorname{Var}(S)=I_n(\theta)$）。所以 $U$ 不能想多短就多短：

```
                  U
                 /|
                / |
               /  |
              /   |
-------------●----+---------- S 的方向
          固定投影
```

若 $U$ 的长度太短，就不可能在 $S$ 方向上产生规定大小的投影，因此 $U$ 的长度存在最小值——概率语言里"长度平方"就是 $\operatorname{Var}(U)$，于是得到方差下界。

### 5. 什么时候能达到等号？

Cauchy-Schwarz 取等号当且仅当两个随机变量线性相关，即

$$U - g(\theta) = c(\theta)\,S(\theta)$$

其中 $c(\theta)$ 是只依赖 $\theta$ 的函数。也就是说：**估计误差 $U-g(\theta)$ 必须完全沿着得分函数 $S$ 的方向，没有任何额外的"垂直分量"**。这又和 Rao-Blackwell 的投影思想很像：若 $U$ 还有额外的垂直随机波动，方差就比理论下界大；只有完全沿有效信息方向时才能达到下界。

因此要记住：**不是每一个问题都一定存在达到 Cramér–Rao 下界的估计量。**

### 6. Bernoulli 验证

Bernoulli 估计 $p$，取 $U=\bar{X}$（$E(\bar{X})=p$，故 $g(p)=p$，$g'(p)=1$），Fisher 信息 $I_n(p)=\frac{n}{p(1-p)}$，于是

$$\operatorname{Var}(U) \ge \frac{1}{I_n(p)} = \frac{p(1-p)}{n}$$

而 $\operatorname{Var}(\bar{X}) = \frac{p(1-p)}{n}$ 正好等于下界，即 $\operatorname{Var}(\bar{X}) = CRLB$——样本均值一点多余方差都没有。

### 7. 一句话总结

整个证明围绕三个等式展开：$E(S)=0$、$\operatorname{Cov}(U,S)=g'(\theta)$、$\operatorname{Var}(S)=I_n(\theta)$，再用 Cauchy-Schwarz 把它们扣在一起。

结合 Rao-Blackwell 可这样区分：

> **Rao-Blackwell 是把估计量里多余的随机波动去掉；Cramér–Rao 是利用"估计量必须携带足够多关于参数的信息"这件事，证明它的方差不可能无限小。**

## 五、与 Rao-Blackwell、UMVUE 的关系

### 1. Cramér–Rao 和 Rao-Blackwell 有什么区别？

这两个名字特别像，但作用完全不同：

- **Rao-Blackwell**：给你一个已有的无偏估计量 $U$，利用[[充分统计量]] $T$ 做 $U \to E(U\mid T)$，保证 $\operatorname{Var}[E(U\mid T)] \le \operatorname{Var}(U)$。它是在**改进一个具体的估计量**。
- **Cramér–Rao**：不需要先拿一个估计量做[[条件期望与条件方差|条件期望]]，它直接给出 $\operatorname{Var}(U) \ge CRLB$，是**所有无偏估计量方差的理论底线**。

可以记成：

$$\boxed{\text{Rao-Blackwell：往下压}} \qquad \boxed{\text{Cramér–Rao：告诉你地板在哪}}$$

### 2. 和 UMVUE 的关系

这三者可以完全串起来。假设 $U$ 是无偏估计量：

- 一条路：Rao-Blackwell 帮我们找到更好的估计量 $U \to E(U\mid T)$，若 $T$ 完全充分，再由 Lehmann-Scheffé 得到 UMVUE。
- 另一条路：先算 Cramér–Rao 下界 $CRLB = \frac{[g'(\theta)]^2}{I_n(\theta)}$，再算某无偏估计量 $U$ 的方差，若发现 $\operatorname{Var}(U) = CRLB$，那它已经达到任何无偏估计量都无法突破的下界，因此自然就是 UMVUE：

$$\boxed{\operatorname{Var}(U) = CRLB \ \Rightarrow\ U \text{ 是 UMVUE}}$$

但要小心反过来不一定成立：

> **UMVUE 不一定能达到 Cramér–Rao 下界**，因为 CR 下界不一定可以真正取到。

### 3. 反例：估计 $\mu^2$（UMVUE 但达不到 CRLB）

这个反例把上面"反过来不一定"落到实处。设 $X_1,\dots,X_n \sim N(\mu,\sigma^2)$，$\sigma^2$ 已知，$\mu$ 未知，目标不是 $\mu$ 而是 $\mu^2$。

**① 找无偏估计**：由 $E(\bar{X}^2) = \operatorname{Var}(\bar{X}) + [E(\bar{X})]^2 = \frac{\sigma^2}{n} + \mu^2$，比想要的 $\mu^2$ 多了一项 $\frac{\sigma^2}{n}$，减掉它：

$$U = \bar{X}^2 - \frac{\sigma^2}{n}$$

则 $E(U) = \mu^2$，是 $\mu^2$ 的无偏估计量。

**② 为什么是 UMVUE**：$T=\sum X_i$ 是完全充分统计量，而 $U = \left(\frac{T}{n}\right)^2 - \frac{\sigma^2}{n}$ 是 $T$ 的函数，由 Lehmann-Scheffé：

$$\boxed{\bar{X}^2 - \frac{\sigma^2}{n} \text{ 是 } \mu^2 \text{ 的 UMVUE}}$$

**③ 求 CR 下界**：$g(\mu)=\mu^2$，$g'(\mu)=2\mu$，$I_n(\mu)=\frac{n}{\sigma^2}$，于是

$$\boxed{CRLB = \frac{(2\mu)^2}{n/\sigma^2} = \frac{4\mu^2\sigma^2}{n}}$$

**④ 算 UMVUE 的实际方差**：减去常数不改变方差，$\operatorname{Var}(U) = \operatorname{Var}(\bar{X}^2)$。因 $\bar{X} \sim N(\mu,\frac{\sigma^2}{n})$，对 $Y\sim N(\mu,v)$ 有 $\operatorname{Var}(Y^2)=4\mu^2v+2v^2$，取 $v=\frac{\sigma^2}{n}$：

$$\operatorname{Var}(U) = \frac{4\mu^2\sigma^2}{n} + \frac{2\sigma^4}{n^2} = CRLB + \frac{2\sigma^4}{n^2}$$

显然 $\operatorname{Var}(U) > CRLB$。于是出现我们想要的现象：

$$\boxed{U \text{ 是 UMVUE，但没有达到 C-R 下界}}$$

**⑤ 为什么达不到**：CR 来自 Cauchy-Schwarz，取等号要求 $U - g(\theta) = c(\theta)S(\theta)$（线性相关）。这里得分函数 $S(\mu)=\frac{n(\bar{X}-\mu)}{\sigma^2}$ 关于 $\bar{X}$ 是**一次**，而估计误差 $U-\mu^2 = \bar{X}^2-\frac{\sigma^2}{n}-\mu^2$ 关于 $\bar{X}$ 是**二次**，一般不可能满足线性关系，故 Cauchy-Schwarz 不能取等号。

**⑥ 特别地令 $\mu=0$**：$g'(0)=0$，故 $CRLB=0$，但 $\operatorname{Var}(U)=\frac{2\sigma^4}{n^2}\neq 0$。这直观说明：CR 下界有时非常"松"，$\operatorname{Var}(U)\ge 0$ 当然没错，只是没人能达到 0。

**⑦ 总结：两个不同的问题**

```
方差
↑
│        某个无偏估计
│          ●
│
│     ●  UMVUE
│
│
│-------------------- C-R 理论下界
│
└──────────────────→
```

- **UMVUE 问**：实际存在的所有无偏估计量里，谁最好？（是所有估计量里最低的那个）
- **CR 问**：从数学上，这些无偏估计量的方差至少不能低于多少？（是理论底线）

这两者之间**完全可能还有一段距离**。例如实际无偏估计量方差可能是 $5,7,10,15,\dots$，UMVUE 的方差是 $5$，而 CR 只告诉你 $\operatorname{Var}(U)\ge 4$——没有矛盾，只是没人能达到 $4$。

## 六、做题流程与总结

### 1. 计算 Cramér–Rao 下界的固定流程

看到"求无偏估计量的 Cramér–Rao 下界"，按以下流程：

1. 写一个样本的密度 $f(x;\theta)$；
2. 取对数 $\ln f(x;\theta)$；
3. 对 $\theta$ 求导 $\frac{\partial}{\partial\theta}\ln f(x;\theta)$；
4. 平方后求期望：$I_1(\theta) = E\left[\left(\frac{\partial}{\partial\theta}\ln f(X;\theta)\right)^2\right]$；
5. $n$ 个独立同分布样本：$I_n(\theta) = n\,I_1(\theta)$；
6. 代入：

$$\boxed{\operatorname{Var}(U) \ge \frac{[g'(\theta)]^2}{I_n(\theta)}}$$

若估计的就是 $\theta$ 本身，则退化为

$$\boxed{\operatorname{Var}(U) \ge \frac{1}{I_n(\theta)}}$$

### 2. 整体直觉

Cramér–Rao 最值得理解的一条关系：

$$\boxed{\text{Fisher 信息越大} \Longrightarrow \text{参数信息越丰富} \Longrightarrow \text{方差下界越小} \Longrightarrow \text{可以估计得越精确}}$$

而 $n$ 个独立样本的信息量相加，$I_n(\theta) = n\,I_1(\theta)$，所以样本数增加时 $CRLB \propto \frac1n$——这正是统计里反复看到"样本越多，估计越稳定"的理论来源之一。

最后牢牢记住这三者的分工：

$$\boxed{\text{Rao-Blackwell：把估计量变好}}$$

$$\boxed{\text{完全性 + Lehmann-Scheffé：证明它是 UMVUE}}$$

$$\boxed{\text{Cramér–Rao：给方差划一条不可低于的理论下界}}$$

其中 Cramér–Rao 最核心的两个东西就是 **Fisher 信息量**和 **Cauchy-Schwarz 不等式**。这两个理解了，整个定理就不会只是一个需要背的公式。

## 七、求 UMVUE 的四种方法

以后题目写"求 $g(\theta)$ 的 UMVUE"，你手上有四种武器，按优先级排列。

### 方法一：完全充分统计量 + 无偏性（Lehmann-Scheffé）

这是最常用、最强的方法。若找到完全充分统计量 $T$，又找到它的一个函数 $h(T)$ 满足 $E[h(T)] = g(\theta)$，则由 Lehmann-Scheffé 定理：

$$\boxed{h(T) \text{ 是唯一的 UMVUE}}$$

例：Bernoulli 估计 $p$，$T=\sum X_i$ 完全充分，且 $E(T/n)=p$，故 $\frac{T}{n}=\bar{X}$ 是 $p$ 的 UMVUE。

### 方法二：Rao-Blackwell 化

有时知道完全充分统计量 $T$，但暂时找不到它的无偏函数。那就先随便找一个无偏估计量 $U$，再做

$$U^* = E(U \mid T)$$

Rao-Blackwell 保证 $E(U^*) = E(U)$、$\operatorname{Var}(U^*) \le \operatorname{Var}(U)$，且 $U^*$ 已是 $T$ 的函数。若 $T$ 完全充分，则 $U^*$ 就是 UMVUE。

$$\boxed{\text{先随便找 } U \rightarrow E(U\mid T) \rightarrow UMVUE}$$

### 方法三：达到 Cramér–Rao 下界

若 $U$ 是 $g(\theta)$ 的无偏估计，且算出

$$\operatorname{Var}(U) = \frac{[g'(\theta)]^2}{I_n(\theta)} = CRLB$$

说明 $U$ 达到了所有无偏估计量都不能低于的下界，自然没人能比它方差更小：

$$\boxed{\text{无偏 + 达到 CR 下界} \Longrightarrow UMVUE}$$

例：正态 $\sigma^2$ 已知估计 $\mu$，$\operatorname{Var}(\bar{X}) = \frac{\sigma^2}{n} = CRLB$，故 $\bar{X}$ 是 UMVUE。

**但要特别注意**：如果发现 $\operatorname{Var}(U) > CRLB$，**不能说 $U$ 不是 UMVUE**——因为 CR 下界本身可能没人能达到（见五.3 的 $\mu^2$ 反例）。

$$\boxed{\text{达到 } CRLB \Rightarrow UMVUE} \qquad \boxed{\text{没达到 } CRLB \not\Rightarrow \text{不是 } UMVUE}$$

这句话考试非常容易考。

### 方法四：利用"0 的无偏估计量"

一个非常漂亮的 UMVUE 判别定理（充要条件）：

> $U$ 是 $g(\theta)$ 的 UMVUE，当且仅当 $U$ 与任意一个"0 的无偏估计量"都不相关。即对任意满足 $E(V)=0$ 的 $V$，都有

$$\boxed{\operatorname{Cov}(U,V) = 0}$$

**为什么（充分性）**：设 $U$ 是 UMVUE，任取 $E(V)=0$ 的 $V$。对任意常数 $a$，$U+aV$ 仍无偏（$E(U+aV)=g(\theta)$）。因 $U$ 是 UMVUE，$\operatorname{Var}(U+aV)\ge\operatorname{Var}(U)$ 对所有 $a$ 成立。展开：

$$\operatorname{Var}(U+aV) = \operatorname{Var}(U) + 2a\operatorname{Cov}(U,V) + a^2\operatorname{Var}(V) \ge \operatorname{Var}(U)$$

即 $2a\operatorname{Cov}(U,V)+a^2\operatorname{Var}(V)\ge 0$ 对所有正负 $a$ 都成立，这迫使 $\operatorname{Cov}(U,V)=0$。

**反过来（必要性）**：设 $U$ 与所有零均值 $V$ 都 $\operatorname{Cov}(U,V)=0$。任取另一无偏估计 $W$（$E(W)=g(\theta)$），则 $V=W-U$ 满足 $E(V)=0$，且 $W=U+V$。于是

$$\operatorname{Var}(W) = \operatorname{Var}(U+V) = \operatorname{Var}(U) + \operatorname{Var}(V) + 2\operatorname{Cov}(U,V) = \operatorname{Var}(U) + \operatorname{Var}(V) \ge \operatorname{Var}(U)$$

$W$ 任意，故 $U$ 是 UMVUE。

**这和"平行轴定理"很像**：$W=U+V$ 且 $\operatorname{Cov}(U,V)=0$，所以 $\operatorname{Var}(W)=\operatorname{Var}(U)+\operatorname{Var}(V)$，又是一个"勾股分解"：

$$\boxed{\text{总方差} = \text{UMVUE 方差} + \text{额外方差}}$$

这跟 Rao-Blackwell 的 $\operatorname{Var}(U)=\operatorname{Var}[E(U\mid T)]+E[\operatorname{Var}(U\mid T)]$ 是同一种数学味道。

### 求 UMVUE 的做题路线

按这个顺序想：

1. **第一选择**：找完全充分统计量 $T$，构造 $h(T)$ 使 $E[h(T)]=g(\theta)$，则 $h(T)$ 就是 UMVUE。
2. 若不会直接构造，先随便找无偏 $U$，再做 $E(U\mid T)$ 进行 Rao-Blackwell 化。
3. 若完全充分统计量不好找但 CR 下界好算，试 $Var(U)=CRLB$，正好相等就直接得 UMVUE；**没达到也不要否定它**。
4. 若以上都不好用，可用 $\operatorname{Cov}(U,V)=0$（对所有零均值 $V$）作为 UMVUE 的充要条件。

最后把这一整块知识串起来：

$$\boxed{\text{Rao-Blackwell：改进估计量}}$$

$$\boxed{\text{完全性：保证无偏函数唯一}}$$

$$\boxed{\text{Lehmann-Scheffé：完全充分 + 无偏 } \Rightarrow UMVUE}$$

$$\boxed{\text{Cramér-Rao：提供理论方差下界}}$$

最容易犯的错误就是以为"UMVUE 的方差一定等于 CR 下界"——这是错的。正确关系是：

$$\boxed{\text{达到 C-R 下界，是成为 UMVUE 的充分条件之一，但不是必要条件。}}$$
