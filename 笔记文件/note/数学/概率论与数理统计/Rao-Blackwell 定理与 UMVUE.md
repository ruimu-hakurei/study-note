## 一、问题：我们想找"无偏 + 方差最小"的估计量

### 1. 无偏估计量不唯一

假设总体分布中有未知参数 $\theta$，想估计某个量 $g(\theta)$。找到一个统计量 $U = U(X_1, \dots, X_n)$，若 $E_\theta(U) = g(\theta)$，则 $U$ 是 $g(\theta)$ 的**[[无偏性|无偏估计]]量**。

但无偏估计量往往不止一个：两个估计量 $U_1, U_2$ 可能都满足 $E(U_1) = E(U_2) = g(\theta)$，那哪个好？

通常更喜欢**方差小**的：$\operatorname{Var}(U_1) < \operatorname{Var}(U_2)$，因为方差越小，估计量越稳定。

于是最终目标锁定为：

$$\boxed{\text{无偏 + 方差尽可能小}}$$

### 2. UMVUE 的定义

UMVUE 全称 **Uniformly Minimum Variance Unbiased Estimator**，中文叫**一致最小方差无偏估计量**。

注意这里的 "Uniformly" 不是"一致估计"的那个一致，而是说：**对[[参数空间]]中的每一个 $\theta$**，它的方差都不比其他无偏估计量大。

设 $\hat{g}(X)$ 是 $g(\theta)$ 的无偏估计量。若对任意其他无偏估计量 $U$，都有

$$\operatorname{Var}_\theta(\hat{g}) \le \operatorname{Var}_\theta(U) \quad (\forall \theta)$$

则 $\hat{g}$ 是 $g(\theta)$ 的 **UMVUE**。

问题就变成：怎么找到这个"最好的无偏估计量"？Rao-Blackwell 定理是其中最重要的一步。

## 二、Rao-Blackwell 定理

### 1. 核心结论

假设已有一个无偏估计量 $U(X_1, \dots, X_n)$，又找到了参数 $\theta$ 的一个**[[充分统计量]]** $T = T(X_1, \dots, X_n)$。Rao-Blackwell 告诉我们：把 $U$ 换成

$$\boxed{U^* = E(U \mid T)}$$

则新估计量 $U^*$ 满足：

$$E(U^*) = E(U), \qquad \boxed{\operatorname{Var}(U^*) \le \operatorname{Var}(U)}$$

也就是说：**对充分统计量取条件期望，可以把一个估计量"压缩"成更好的估计量。**

### 2. 为什么偏偏是 $E(U \mid T)$？

原估计量 $U$ 可能利用了样本里很多"杂乱信息"。但若 $T$ 是充分统计量，$T$ 已经包含关于 $\theta$ 的全部信息。因此可以问：当 $T$ 已确定时，$U$ 平均是多少？这个值就是 $E(U \mid T)$。它只由 $T$ 决定，故可写成 $U^* = h(T)$——一个复杂的估计量被压缩成 $h(T)$，且没有损失关于 $\theta$ 的有效信息。

### 3. 为什么强调"充分"统计量？

纯数学上，对**任意**随机变量 $T$，$\operatorname{Var}[E(U \mid T)] \le \operatorname{Var}(U)$ 都成立。那为什么定理特别强调 $T$ 充分？

因为统计估计中，我们需要 $E_\theta(U \mid T)$ 能成为一个**真正可用的统计量**。若 $T$ 充分，则给定 $T$ 后样本的条件分布不再依赖 $\theta$，于是 $E_\theta(U \mid T)$ 能算成一个只含 $T$ 的函数 $h(T)$，不会偷偷还含着未知的 $\theta$。这点非常关键。

### 4. 定理的标准形式

设 $X = (X_1, \dots, X_n)$ 来自含未知参数 $\theta$ 的总体。若 $T = T(X)$ 是 $\theta$ 的充分统计量，$U = U(X)$ 是 $g(\theta)$ 的无偏估计量且 $E(U^2) < \infty$，定义 $\delta(T) = E(U \mid T)$，则

$$E[\delta(T)] = g(\theta), \qquad \boxed{\operatorname{Var}[\delta(T)] \le \operatorname{Var}(U)}$$

即 $E(U \mid T)$ 是至少不比 $U$ 差的无偏估计量。

## 三、Rao-Blackwell 定理的证明

### 1. 无偏性不变（迭代期望）

由条件期望的迭代期望公式：

$$E[E(U \mid T)] = E(U)$$

所以 $E(U^*) = E(U)$。若原 $U$ 无偏，$E(U) = g(\theta)$，则 $E(U^*) = g(\theta)$，新的估计量仍无偏。

$$\boxed{\text{Rao-Blackwell 化不会改变期望}}$$

### 2. 方差不增大（全方差公式）

这是 Rao-Blackwell 定理最核心的数学原因。用**全方差公式**：

$$\operatorname{Var}(U) = E[\operatorname{Var}(U \mid T)] + \operatorname{Var}[E(U \mid T)]$$

而 $U^* = E(U \mid T)$，故 $\operatorname{Var}(U^*) = \operatorname{Var}[E(U \mid T)]$，于是

$$\operatorname{Var}(U) = E[\operatorname{Var}(U \mid T)] + \operatorname{Var}(U^*)$$

因为 $\operatorname{Var}(U \mid T) \ge 0$，故 $E[\operatorname{Var}(U \mid T)] \ge 0$，于是

$$\boxed{\operatorname{Var}(U^*) \le \operatorname{Var}(U)}$$

### 3. 方差公式的直观理解（"去噪"）

全方差公式可理解为：

$$\operatorname{Var}(U) = \underbrace{E[\operatorname{Var}(U \mid T)]}_{\text{知道 }T\text{ 后仍存在的波动}} + \underbrace{\operatorname{Var}[E(U \mid T)]}_{\text{由 }T\text{ 引起的波动}}$$

Rao-Blackwell 把 $U$ 换成 $E(U \mid T)$，等于把第一部分 $E[\operatorname{Var}(U \mid T)]$ 直接去掉，只留下 $\operatorname{Var}[E(U \mid T)]$，所以方差自然不更大。

换个说法，把 $U$ 拆成

$$U = E(U \mid T) + \big[U - E(U \mid T)\big] = \boxed{\text{有用部分} + \text{额外随机波动}}$$

其中 $E(U \mid T)$ 是用 $T$ 能解释的部分，$U - E(U \mid T)$ 是 $T$ 确定后仍存在的额外随机波动。Rao-Blackwell 相当于把后面这部分扔掉：

$$U \longrightarrow E(U \mid T)$$

所以可以想成：**用充分统计量给估计量做"降噪"。**

## 四、为什么 Rao-Blackwell 只需做一次？（幂等性）

### 1. 数学验证：再做一次等于它自己

核心原因：**Rao-Blackwell 化对同一个充分统计量 $T$ 做一次之后，估计量就已经变成 $T$ 的函数了**，再做一次不会发生任何变化。

设原有无偏估计量 $U$，第一次做 Rao-Blackwell：

$$U^* = E(U \mid T)$$

条件期望 $E(U \mid T)$ 本身就是 $T$ 的函数，可写成 $U^* = h(T)$。再做一次：

$$E(U^* \mid T) = E\big[h(T) \mid T\big]$$

既然已经知道 $T$，$h(T)$ 也完全确定了，所以

$$E\big[h(T) \mid T\big] = h(T)$$

因此

$$\boxed{E\big[E(U \mid T) \mid T\big] = E(U \mid T)}$$

第二次不会继续改进。

### 2. Bernoulli 例子：$X_1 \to \bar{X} \to \bar{X}$

拿 Bernoulli 例子看特别明显。一开始 $U = X_1$，充分统计量 $T = \sum_{i=1}^n X_i$。

第一次 Rao-Blackwell：

$$E(X_1 \mid T) = \frac{T}{n} = \bar{X}$$

现在 $\bar{X} = \frac{T}{n}$ 已完全是 $T$ 的函数。再来一次：

$$E(\bar{X} \mid T) = E\left(\frac{T}{n} \mid T\right) = \frac{T}{n} = \bar{X}$$

所以

$$\boxed{X_1 \xrightarrow{\text{Rao-Blackwell}} \bar{X} \xrightarrow{\text{再做一次}} \bar{X}}$$

不会变成什么"更好的 $\bar{X}$"。

### 3. 从"去噪"和方差分解看

从"去噪"角度：第一次做之前 $U = E(U \mid T) + \big[U - E(U \mid T)\big]$，其中 $U - E(U \mid T)$ 是知道 $T$ 后仍残留的随机波动。RB 第一次就把它去掉了，只留下 $E(U \mid T)$，所以做完后已经没有这种"相对于 $T$ 的额外噪声"可再去掉。

对应方差分解 $\operatorname{Var}(U) = \operatorname{Var}[E(U \mid T)] + E[\operatorname{Var}(U \mid T)]$：第一次 RB 去掉的是 $E[\operatorname{Var}(U \mid T)]$。而令 $U^* = E(U \mid T)$ 后，因知道 $T$ 就完全知道 $U^*$，故 $\operatorname{Var}(U^* \mid T) = 0$。再套一次方差分解：

$$\operatorname{Var}(U^*) = \operatorname{Var}[E(U^* \mid T)] + E[\operatorname{Var}(U^* \mid T)] = \operatorname{Var}[E(U^* \mid T)] + 0$$

第二项已经是 $0$，自然没有东西能继续减少。

### 4. 幂等性：与"四舍五入"类比

有一个很漂亮的数学性质叫**幂等性**：做一次和做很多次效果一样。

$$\boxed{E\big[E(U \mid T) \mid T\big] = E(U \mid T)}$$

类似把一个数四舍五入到整数：$3.72 \to 4$，再四舍五入 $4 \to 4$。第一次已经进入目标集合，第二次不会再变。

Rao-Blackwell 同理：$U(X_1, \dots, X_n) \to h(T)$，第一次就把估计量"投影"到**所有 $T$ 的函数组成的集合**里，一旦已变成 $h(T)$，再投影一次还是自己。

### 5. 澄清：只做一次 ≠ 一定得到 UMVUE

这里有个容易混淆的点：**"Rao-Blackwell 只做一次"不等于"做一次就一定得到 UMVUE"**。

第一次之后只保证 $\operatorname{Var}[E(U \mid T)] \le \operatorname{Var}(U)$，即比原来的 $U$ 好。至于是否已好到"所有无偏估计量里方差最小"，还需进一步判断：如果 $T$ 是**完全充分统计量**，$E(U \mid T)$ 才能由 Lehmann-Scheffé 定理直接认定为 UMVUE。

整个逻辑是：$U \xrightarrow{\text{RB 一次}} E(U \mid T) = h(T)$，因为已是 $T$ 的函数（$E[h(T)\mid T] = h(T)$），所以没必要再 RB；然后问"$T$ 是否完全？"，若是，则 $h(T)$ 就是 UMVUE。

> **Rao-Blackwell 对同一个充分统计量只需做一次，因为第一次之后估计量已完全由这个充分统计量决定，再条件化一次等于它自己。**

## 五、从 Rao-Blackwell 到 UMVUE：完全性

### 1. RB 化不一定得到 UMVUE

**不一定。** Rao-Blackwell 只保证 $U \to E(U \mid T)$ 后方差不增加，它说明：**要找最小方差无偏估计量，可以重点在"充分统计量的函数"中找**。但可能存在很多不同的无偏函数 $h_1(T), h_2(T), h_3(T), \dots$，到底哪一个是 UMVUE？仅靠 Rao-Blackwell 还不能完全回答，这时需要**完全性**。

### 2. 零的无偏估计：唯一性的关键

先看一个奇怪的问题：什么叫"0 的无偏估计"？

一个统计量 $U$，若无论 $\theta$ 取什么值都有 $E_\theta(U) = 0$，就称 $U$ 是 **0 的无偏估计量**。$U \equiv 0$ 当然是；真正关键的问题是：**除了恒为 0，还会不会存在别的"不恒为 0、但期望永远等于 0"的统计量？**

为什么关心这个：若 $U_1, U_2$ 都是 $g(\theta)$ 的无偏估计，两式相减 $E(U_1 - U_2) = 0$，即 $U_1 - U_2$ 就是一个 0 的无偏估计量。若能证明"0 的无偏估计只有恒为 0 那一个"，就能推出 $U_1 = U_2$，即**无偏估计量是唯一的**。

所以"零的无偏估计"并不是单独研究"怎么估计 0"，而是用来证明**两个无偏估计量不可能不同**——这正是完全性和 UMVUE 唯一性的根基。

### 3. 完全统计量的定义

设统计量 $T$ 的分布依赖 $\theta$。若对任意函数 $h$，只要对所有 $\theta$ 都有 $E_\theta[h(T)] = 0$，就一定能推出 $P_\theta(h(T) = 0) = 1$，则称 $T$ 是**完全统计量**。

直观上：在 $T$ 的所有函数里，不存在一个"偷偷不为 0、但平均以后永远等于 0"的东西。所以完全性本质上是一种很强的**唯一性条件**。

因为若 $h_1(T), h_2(T)$ 都是 $g(\theta)$ 的无偏估计，两式相减 $E[h_1(T) - h_2(T)] = 0$，若 $T$ 完全，则只能 $h_1(T) - h_2(T) = 0$（几乎处处），即 $h_1(T) = h_2(T)$。

$$\boxed{\text{完全性保证了无偏估计量的唯一性}}$$

### 4. Lehmann-Scheffé 定理

这条是 Rao-Blackwell 与 UMVUE 之间的最终桥梁。

若 $T$ 是参数 $\theta$ 的**完全充分统计量**，而某个 $h(T)$ 满足 $E[h(T)] = g(\theta)$，则 $h(T)$ 是 $g(\theta)$ 的**唯一 UMVUE**。

整个知识链可串成：

$$\boxed{\text{充分统计量} + \text{Rao-Blackwell} + \text{完全性} \Rightarrow \text{UMVUE}}$$

### 5. 为什么"完全充分统计量的无偏函数"一定是 UMVUE？（证明）

设 $T$ 完全充分，$h(T)$ 满足 $E[h(T)] = g(\theta)$。任取另一个无偏估计量 $U$（$E(U) = g(\theta)$），先对它 RB 化：$U^* = E(U \mid T)$，则 $E(U^*) = g(\theta)$ 且 $\operatorname{Var}(U^*) \le \operatorname{Var}(U)$。

注意 $U^* = k(T)$ 也是 $T$ 的函数，而 $h(T)$ 也是 $g(\theta)$ 的无偏估计，因 $T$ 完全，故 $k(T) = h(T)$，即 $U^* = h(T)$。于是

$$\operatorname{Var}[h(T)] = \operatorname{Var}(U^*) \le \operatorname{Var}(U)$$

因 $U$ 任意，故 $h(T)$ 比所有无偏估计量方差都小，即 $h(T)$ 就是 UMVUE。

### 6. 充分性 vs 完全性

这两个概念特别容易混。

- **充分性解决"信息"问题**：$T$ 包含了样本中关于 $\theta$ 的全部信息，所以希望估计量写成 $h(T)$，而不是依赖一堆无关的随机波动。
- **完全性解决"唯一性"问题**：两个 $T$ 的函数若都是同一参数函数的无偏估计，则它们必相同。

$$\boxed{\text{充分性} = \text{信息够不够}} \qquad \boxed{\text{完全性} = \text{答案唯一不唯一}}$$

$$\boxed{\text{完全充分统计量} = \text{信息全，且无偏估计不重复}}$$

### 7. 指数族：怎么找到完全充分统计量

很多常见分布都属于**指数族**，形式为

$$f(x;\theta) = h(x)\,c(\theta)\,\exp\big\{w(\theta)\,t(x)\big\}$$

不用死记这个形式，真正要记住的是：对于很多指数族分布，若 $n$ 个[[总体与样本抽样|独立同分布]]样本，充分统计量常为

$$T = \sum_{i=1}^n t(X_i)$$

并且在满足一定条件时它还是**完全统计量**。于是

$$\boxed{\text{指数族} \Rightarrow \text{容易找到完全充分统计量}}$$

而一旦找到完全充分统计量，求 UMVUE 就特别方便（见下一节例子）。

## 六、完整例子

### 1. 例1：Bernoulli 分布，估计 $p$（$X_1 \to \bar{X}$）

设 $X_1, \dots, X_n \overset{iid}{\sim} \text{Bernoulli}(p)$，即 $P(X_i=1)=p,\ P(X_i=0)=1-p$。

**① 找无偏估计量与充分统计量**

无偏估计量最简单取 $U = X_1$。因 $E(X_1) = p$，所以 $X_1$ 是 $p$ 的无偏估计量。但它显然很浪费——明明有 $n$ 个样本却只用了第一个，方差 $\operatorname{Var}(X_1) = p(1-p)$。

充分统计量：Bernoulli 样本的联合概率质量函数为

$$P(X_1=x_1,\dots,X_n=x_n) = p^{\sum x_i}(1-p)^{n-\sum x_i}$$

由[[因子分解定理]]，$T = \sum_{i=1}^n X_i$ 是 $p$ 的充分统计量。注意 $T = n\bar{X}$，所以 $\bar{X}$ 本质上也是充分统计量的函数。

**② Rao-Blackwell 化：计算 $E(X_1 \mid T)$**

构造 $U^* = E(X_1 \mid T)$。已知 $T = k$ 意味着 $n$ 个 $X_i$ 中总共有 $k$ 个 $1$。因 $X_1, \dots, X_n$ 地位完全对称，第一个位置是 $1$ 的概率为

$$P(X_1 = 1 \mid T = k) = \frac{k}{n}$$

又 $X_1$ 只取 $0, 1$，故 $E(X_1 \mid T = k) = P(X_1 = 1 \mid T = k) = \frac{k}{n}$。于是

$$E(X_1 \mid T) = \frac{T}{n} = \frac{1}{n}\sum_{i=1}^n X_i = \boxed{\bar{X}}$$

Rao-Blackwell 把只用一个样本的 $X_1$ 改造成了利用全部样本的 $\bar{X}$。

**③ 验证方差下降**

原来 $\operatorname{Var}(X_1) = p(1-p)$，新的 $\operatorname{Var}(\bar{X}) = \frac{p(1-p)}{n}$。当 $n > 1$ 时 $\frac{p(1-p)}{n} < p(1-p)$，即

$$\boxed{\operatorname{Var}(\bar{X}) < \operatorname{Var}(X_1)}$$

这就是 Rao-Blackwell 最直观的效果。

**④ 用 Lehmann-Scheffé 得到 UMVUE**

$T = \sum_{i=1}^n X_i \sim \text{Binomial}(n, p)$，它不仅充分，还是完全统计量，故 $T$ 是**完全充分统计量**。而 $\frac{T}{n} = \bar{X}$ 满足

$$E\left(\frac{T}{n}\right) = \frac{E(T)}{n} = \frac{np}{n} = p$$

由 Lehmann-Scheffé 定理，$\bar{X}$ 是 $p$ 的 **UMVUE**。

注意这个结论比 Rao-Blackwell 更强：RB 只告诉你 $\operatorname{Var}(\bar{X}) \le \operatorname{Var}(X_1)$；而 Lehmann-Scheffé 告诉你 $\bar{X}$ 的方差不大于**任何** $p$ 的无偏估计量。

### 2. 例2：Bernoulli 分布，估计 $p^2$（$X_1 X_2 \to \frac{T(T-1)}{n(n-1)}$）

目标从 $p$ 换成 $p^2$。先找一个无偏估计量：因为 $X_1$ 与 $X_2$ 独立，

$$E(X_1 X_2) = E(X_1) E(X_2) = p^2$$

所以取 $U = X_1 X_2$。仍用充分统计量 $T = \sum_{i=1}^n X_i$，做 Rao-Blackwell 化：

$$E(X_1 X_2 \mid T)$$

已知 $T = k$ 时，$X_1 X_2 = 1$ 当且仅当 $X_1 = X_2 = 1$，所以

$$E(X_1 X_2 \mid T = k) = P(X_1 = 1, X_2 = 1 \mid T = k)$$

已知 $n$ 个位置中有 $k$ 个 $1$：第一个位置是 $1$ 的概率为 $\frac{k}{n}$；若第一个已占用一个 $1$，剩 $n-1$ 个位置、$k-1$ 个 $1$，第二个位置也是 $1$ 的概率为 $\frac{k-1}{n-1}$。于是

$$E(X_1 X_2 \mid T = k) = \frac{k}{n} \cdot \frac{k-1}{n-1}$$

因此

$$\boxed{E(X_1 X_2 \mid T) = \frac{T(T-1)}{n(n-1)}}$$

Rao-Blackwell 把 $X_1 X_2$ 改造成了 $\frac{T(T-1)}{n(n-1)}$。

（注：$T \sim \text{Binomial}(n,p)$ 有 $E[T(T-1)] = n(n-1)p^2$，故 $\frac{T(T-1)}{n(n-1)}$ 仍是 $p^2$ 的无偏估计；又 $T$ 完全充分，由 Lehmann-Scheffé，它同时也是 $p^2$ 的 **UMVUE**。）

### 3. 例3：指数分布，估计 $1/\lambda$ 与 $\lambda$

设 $X_1, \dots, X_n \overset{iid}{\sim} \text{Exp}(\lambda)$，即 $f(x;\lambda) = \lambda e^{-\lambda x},\ x > 0$，$\lambda$ 未知。

**① 找充分统计量**

联合密度：

$$f(x_1,\dots,x_n;\lambda) = \prod_{i=1}^n \lambda e^{-\lambda x_i} = \lambda^n e^{-\lambda(x_1+\cdots+x_n)}$$

所有关于 $\lambda$ 的信息只通过 $X_1 + \cdots + X_n$ 出现，故 $T = \sum_{i=1}^n X_i$ 是充分统计量。指数分布属于指数族，且这里的 $T$ 还是完全统计量，所以 $T$ 是**完全充分统计量**。

**② 估计均值 $1/\lambda$**

因 $E(X_i) = \frac1\lambda$，故 $\bar{X}$ 天然是 $1/\lambda$ 的无偏估计。而 $\bar{X} = \frac{T}{n}$ 本身就是完全充分统计量 $T$ 的函数，于是由 Lehmann-Scheffé：

$$\boxed{\bar{X} \text{ 是 } \frac1\lambda \text{ 的 UMVUE}}$$

注意这里甚至不需要再做 Rao-Blackwell——找到的无偏估计量已经是 $T$ 的函数了。

**③ 估计 $\lambda$ 本身**

不能直接用 $\frac1{\bar{X}}$，因为一般 $E(1/\bar{X}) \neq 1/E(\bar{X})$，它通常不是无偏的。

由 $T \sim \text{Gamma}(n, \lambda)$ 可得 $E(\frac1T) = \frac{\lambda}{n-1}$，故

$$E\left(\frac{n-1}{T}\right) = \lambda$$

于是 $\frac{n-1}{T}$ 是 $\lambda$ 的无偏估计，又它是完全充分统计量 $T$ 的函数，所以：

$$\boxed{\frac{n-1}{T} \text{ 是 } \lambda \text{ 的 UMVUE}}$$

这个例子很典型：**先找完全充分统计量，再构造它的无偏函数，直接得到 UMVUE。**

### 4. 例4：正态分布，估计 $\mu$、$\mu^2$、$\sigma^2$

设 $X_1, \dots, X_n \overset{iid}{\sim} N(\mu, \sigma^2)$。

**① $\sigma^2$ 已知，估计 $\mu$**

正态分布关于 $\mu$ 的充分统计量是 $T = \sum_{i=1}^n X_i$，且 $T$ 完全充分。因 $E(\bar{X}) = \mu$，且 $\bar{X} = \frac{T}{n}$ 是 $T$ 的函数，故

$$\boxed{\bar{X} \text{ 是 } \mu \text{ 的 UMVUE}}$$

**② $\sigma^2$ 已知，估计 $\mu^2$**

$E(\bar{X}^2) \neq \mu^2$，因为 $\operatorname{Var}(\bar{X}) = \frac{\sigma^2}{n}$。由 $\operatorname{Var}(\bar{X}) = E(\bar{X}^2) - [E(\bar{X})]^2$ 得

$$E(\bar{X}^2) = \mu^2 + \frac{\sigma^2}{n}$$

所以为得到 $\mu^2$，把多出来的部分减掉：

$$E\left(\bar{X}^2 - \frac{\sigma^2}{n}\right) = \mu^2$$

故 $\bar{X}^2 - \frac{\sigma^2}{n}$ 是 $\mu^2$ 的无偏估计，又是 $T$ 的函数，于是

$$\boxed{\bar{X}^2 - \frac{\sigma^2}{n} \text{ 是 } \mu^2 \text{ 的 UMVUE}}$$

这个方法很常用：**如果一个统计量"差一点无偏"，就计算它的期望，然后把多出来的偏差减掉。**

**③ $\mu$、$\sigma^2$ 都未知，估计 $\sigma^2$**

此时充分统计量可写成 $T_1 = \sum X_i$、$T_2 = \sum X_i^2$（或等价地 $\bar{X}$ 和 $S^2$），且完全。无偏[[样本均值与样本方差|样本方差]]

$$S^2 = \frac{1}{n-1}\sum_{i=1}^n (X_i - \bar{X})^2$$

满足 $E(S^2) = \sigma^2$，故在完全充分统计量条件下：

$$\boxed{S^2 \text{ 是 } \sigma^2 \text{ 的 UMVUE}}$$

所以 $\bar{X}$ 和 $S^2$ 并不只是"大家习惯这么用"，它们背后有非常扎实的最优性理论。

### 5. 关键观察：RB 的结果取决于 $U$，且整个体系如何配合

**观察一：Rao-Blackwell 并不是简单地把估计量变成样本均值**，真正的规律是

$$\boxed{U \longrightarrow E(U \mid T)}$$

最后得到什么，取决于原来的 $U$：

| 目标 | 原估计量 $U$ | RB 化后 $E(U\mid T)$ |
|---|---|---|
| $p$ | $X_1$ | $\frac{T}{n}$ |
| $p^2$ | $X_1 X_2$ | $\frac{T(T-1)}{n(n-1)}$ |

它们唯一的共同点是：**最终都变成了充分统计量 $T$ 的函数。**

**观察二：整个体系如何配合**（以 $p^2$ 为例）：Rao-Blackwell 先把 $X_1 X_2$ 变成 $\frac{T(T-1)}{n(n-1)}$（方差不增、保持无偏），完全性再告诉你"不用继续找了，这个就是最终的 UMVUE"。

## 七、理解 $E(U \mid T)$ 的两种直觉

### 1. 分组平均：组内取平均，消掉组内波动

这是理解 Rao-Blackwell 最本质、最直观的图像：把全部样本按 $T$ 的取值分成若干组，原来的 $U$ 在同一组内部可能到处乱跳；Rao-Blackwell 做的，就是**把每一组内部统一替换成该组的平均值**。

以 $n=3$、$U=X_1$ 为例，按 $T$ 分组：

| 组 | 样本 | $X_1$ 的值 |
|---|---|---|
| $T=0$ | $(0,0,0)$ | $0$ |
| $T=1$ | $(1,0,0),(0,1,0),(0,0,1)$ | $1,0,0$ |
| $T=2$ | $(1,1,0),(1,0,1),(0,1,1)$ | $1,1,0$ |
| $T=3$ | $(1,1,1)$ | $1$ |

- $T=1$ 组：$X_1$ 取值 $1,0,0$，平均 $= \frac{1+0+0}{3} = \frac13$
- $T=2$ 组：$X_1$ 取值 $1,1,0$，平均 $= \frac{1+1+0}{3} = \frac23$

于是 $E(X_1 \mid T) = \frac{T}{3} = \frac{T}{n}$。直观地：

```
T=1 组内 U 的值：
1    0    0
     ↓ 组内取平均
   1/3
```

原来 $X_1$ 在 $0$ 和 $1$ 之间乱跳，RB 把它变成稳定的 $\frac13$——这就是方差下降的原因。

**组内波动 vs 组间波动（对应全方差公式）**：

$$\operatorname{Var}(U) = \underbrace{E[\operatorname{Var}(U \mid T)]}_{\text{组内波动}} + \underbrace{\operatorname{Var}[E(U \mid T)]}_{\text{组间波动}}$$

- 第一项 $E[\operatorname{Var}(U \mid T)]$：同一个 $T$ 分组**内部**，$U$ 还有多少波动；
- 第二项 $\operatorname{Var}[E(U \mid T)]$：不同 $T$ 分组**之间**，组平均值还有多少波动。

RB 把 $U$ 换成 $E(U \mid T)$ 后，每组内部全部变成同一个值，组内方差直接变成 $0$，只剩组间波动，所以必然 $\operatorname{Var}(U^*) \le \operatorname{Var}(U)$。这样方差为什么降低，就不需要死记了。

### 2. 向量投影：条件期望 = 正交投影

用"向量投影"来理解 Rao-Blackwell 特别漂亮。这不是纯比喻：在平方可积随机变量空间里，条件期望确实可以看成一种**正交投影**。

**① 向量投影回顾**

把向量 $\mathbf{u}$ 正交投影到平面 $V$ 上，得到 $P_V(\mathbf{u})$，则

$$\mathbf{u} = P_V(\mathbf{u}) + \big[\mathbf{u} - P_V(\mathbf{u})\big]$$

其中 $P_V(\mathbf{u})$ 在平面 $V$ 里，$\mathbf{u} - P_V(\mathbf{u})$ 垂直于平面 $V$。

```
                u
               /|
              / |
             /  |  u - P(u)
            /   |
-----------●----+---------- 平面 V
          P(u)
```

即 $\boxed{\text{原向量} = \text{投影部分} + \text{垂直残差}}$。

**② 对应关系：$E(U \mid T)$ 就是正交投影**

把估计量 $U$ 想象成"向量"。考虑所有能写成 $h(T)$ 形式的随机变量（如 $T,\ T^2,\ T/n,\ e^T,\ h(T), \dots$），它们组成一个空间 $\mathcal{H}_T$。

```
所有随机变量构成的大空间

                  U
                 /|
                / |
               /  |  U - E(U|T)
              /   |
-------------●-----+---------
          E(U|T)

      所有 h(T) 构成的子空间 H_T
```

关键：$E(U \mid T)$ 就是把向量 $U$ **正交投影到"所有 $T$ 的函数组成的空间"上**：

$$\boxed{E(U \mid T) = P_{\mathcal{H}_T}(U)}$$

**③ 投影的幂等性 ↔ RB 只做一次**

普通向量投影：若 $\mathbf{v} = P_V(\mathbf{u})$，则 $\mathbf{v}$ 已在平面 $V$ 里，再投影一次 $P_V(\mathbf{v}) = \mathbf{v}$，即

$$\boxed{P_V\big(P_V(\mathbf{u})\big) = P_V(\mathbf{u})}$$

这叫做**投影算子的幂等性**。条件期望完全一样：

$$U^* = E(U \mid T) = h(T) \implies E(U^* \mid T) = E[h(T) \mid T] = h(T)$$

$$\boxed{E\big[E(U \mid T) \mid T\big] = E(U \mid T)}$$

与 $P(P(\mathbf{u})) = P(\mathbf{u})$ 完全对应——这正是第四节"只做一次"的几何解释。

**④ 勾股定理 ↔ 全方差公式**

普通向量有 $\|\mathbf{u}\|^2 = \|P(\mathbf{u})\|^2 + \|\mathbf{u} - P(\mathbf{u})\|^2$（投影部分与残差正交）。

随机变量里，$U = E(U \mid T) + \big[U - E(U \mid T)\big]$，两部分在某种意义下也"正交"。若均值为 $0$，则 $E(U^2) = E\big[E(U \mid T)^2\big] + E\big[(U - E(U \mid T))^2\big]$——几乎是随机变量版的勾股定理。不设均值为 $0$ 时对应到方差：

$$\boxed{\operatorname{Var}(U) = \operatorname{Var}[E(U \mid T)] + E[\operatorname{Var}(U \mid T)]}$$

与勾股定理对照：

$$\underbrace{\operatorname{Var}(U)}_{\text{原向量长度平方}} = \underbrace{\operatorname{Var}[E(U \mid T)]}_{\text{投影长度平方}} + \underbrace{E[\operatorname{Var}(U \mid T)]}_{\text{垂直残差长度平方}}$$

因最后一项非负 $E[\operatorname{Var}(U \mid T)] \ge 0$，所以 $\operatorname{Var}[E(U \mid T)] \le \operatorname{Var}(U)$——这就是 RB 方差降低的几何解释。

**⑤ Bernoulli 例子放进投影图**

原估计量 $U = X_1$，充分统计量 $T = X_1 + \cdots + X_n$，所有 $h(T)$ 构成一个子空间。$X_1$ 通常不完全属于这个子空间：只知道 $T = 2$，可能是 $(1,1,0,0)$ 也可能是 $(0,1,1,0)$，所以 $X_1$ 还有额外随机性。对它做投影：

$$E(X_1 \mid T) = \frac{T}{n} = \bar{X}$$

```
                  X₁
                 /|
                / |
               /  |  多余随机波动
              /   |
-------------●-----+-----------
             X̄

       所有 h(T) 的空间
```

这里 $X_1 - \bar{X}$ 相当于"垂直于子空间的那部分"。RB 做的就是把它去掉：$X_1 = \bar{X} + (X_1 - \bar{X})$，保留 $\bar{X}$、丢掉 $X_1 - \bar{X}$，于是估计更稳定。

**⑥ 一张对应表**

整个 Rao-Blackwell 可以记成一句"线性代数式"的话：

$$\boxed{\text{条件期望} = \text{随机变量空间中的正交投影}}$$

对应关系非常整齐：

| 线性代数 | 概率统计 |
|---|---|
| 向量 $\mathbf{u}$ | 随机变量 $U$ |
| 子空间 $V$ | 所有 $h(T)$ 构成的空间 |
| 投影 $P_V(\mathbf{u})$ | $E(U \mid T)$ |
| 垂直残差 | $U - E(U \mid T)$ |
| 勾股定理 | 全方差公式 |
| 投影一次后不再变化 | $E[E(U \mid T)\mid T] = E(U \mid T)$ |

> 这个"向量投影"的理解，对以后学**条件期望、最小均方误差估计、线性回归**都会非常有帮助，它们背后有非常相似的几何结构。

### 3. 两种视角的统一

"分组平均"和"向量投影"其实是同一件事的两个角度：

- **概率角度**：给定 $T$，把同一组里的 $U$ 取平均；
- **几何角度**：把 $U$ 投影到"所有只依赖 $T$ 的随机变量"组成的空间。

两者都是

$$\boxed{U \longrightarrow E(U \mid T)}$$

第一次投影/平均之后，得到的东西已经是 $T$ 的函数（如 $E(X_1\mid T) = \frac{T}{n}$），完全由 $T$ 决定，所以再做一次 $E(\frac{T}{n}\mid T) = \frac{T}{n}$ 不会再变——这也正是第四节"只需做一次"的另一种解释。

## 八、实战路线与总结

### 1. 求 UMVUE 的标准套路

看到"求 $g(\theta)$ 的 UMVUE"，脑子里可以形成这条路线：

1. **找充分统计量 $T$**：通常用因子分解定理（指数族分布尤其容易，$T = \sum t(X_i)$）。
2. **判断 $T$ 是否完全**：很多常见指数族分布的充分统计量都有完全性。
3. **找到 $g(\theta)$ 的一个无偏估计量 $U$**。
4. 若 $U$ 不是 $T$ 的函数，就做 $E(U \mid T)$。
5. 得到 $h(T)$。
6. 若 $T$ 是完全充分统计量，则直接得到 $h(T)$ 是 UMVUE。

这其实就是大多数题目的标准套路。

### 2. 一张关系图

$$U \xrightarrow{\text{对充分统计量条件化}} E(U \mid T)$$

Rao-Blackwell 保证 $E(U \mid T)$ 仍无偏，且 $\operatorname{Var}[E(U \mid T)] \le \operatorname{Var}(U)$。若进一步 $T$ 完全充分，则 $E(U \mid T)$ 就是 UMVUE。

### 3. 浓缩成三句话

1. $U^* = E(U \mid T)$，其中 $T$ 是充分统计量。

2. $E(U^*) = E(U),\quad \operatorname{Var}(U^*) \le \operatorname{Var}(U)$——这就是 **Rao-Blackwell 定理**。

3. 若 $T$ 还是**完全统计量**且 $E[h(T)] = g(\theta)$，则 $h(T)$ 是 $g(\theta)$ 的唯一 **UMVUE**。

一句话总结：**Rao-Blackwell 负责"把估计量变好"，完全性负责"证明已经好到不能再好了"。**

整章最核心的一条线：

$$\boxed{\text{Rao-Blackwell} \rightarrow \text{充分统计量} \rightarrow \text{完全性} \rightarrow \text{Lehmann-Scheffé} \rightarrow \text{UMVUE}}$$
