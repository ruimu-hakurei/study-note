# Bayes 估计基础

> 一句话主线：**先有一个看法 → 数据来了 → 更新看法 → 再按损失函数选一个最终估计。**

相关笔记：[[贝叶斯]]（离散形式与公式推导）、[[连续贝叶斯]]、[[贝塔分布]]、[[MLE]]、[[Rao-Blackwell 定理与 UMVUE]]

---

## 一、 核心思想：参数从"常数"变成"随机变量"

经典（频率学派）参数估计中：

> 参数 $\theta$ 是一个**固定但未知的常数**。

比如抛硬币正面概率 $\theta$ 实际上已经是某个确定值，只是我们不知道，所以用样本去估它。

Bayes 学派的出发点不同：

> 在观察数据之前，我对 $\theta$ 本身就有不确定性，因此把 $\theta$ 当作**随机变量**。

于是整个推断过程可以浓缩为：

$$\text{先验信息} + \text{样本信息} \longrightarrow \text{后验信息}$$

这就是 Bayes 估计最核心的思想：看数据之前先有一个初步认识，看到数据之后用数据来修正这个认识。

---

## 二、 三个基本要素

### 1. 先验分布 $\pi(\theta)$

在**观察数据之前**对 $\theta$ 的认识，记作 $\pi(\theta)$。

它描述的是：在看到样本之前，我们认为不同的 $\theta$ 值各有多大可能。以抛一枚陌生硬币为例，$\theta = P(\text{正面})$：

- $\theta$ 接近 $0.5$ → 先验密度较高（多数硬币是接近公平的）；
- $\theta$ 接近 $0$ 或 $1$ → 先验密度较低。

### 2. 似然函数 $L(\theta)$

样本提供的信息由似然函数刻画（与 [[MLE]] 中的似然是同一个东西）。抛 $n$ 次出现 $x$ 次正面：

$$L(\theta) = p(X \mid \theta) \propto \theta^x (1-\theta)^{n-x}$$

它表达的是：**在不同的 $\theta$ 值下，"$x$ 正 $n-x$ 反"这个数据有多合理。**

若 $n = 10,\ x = 8$，则 $L(\theta) \propto \theta^8 (1-\theta)^2$，数据在说"$\theta$ 好像比 $0.5$ 大"。

### 3. 后验分布 $\pi(\theta \mid X)$

把两者用 Bayes 公式结合起来：

$$\pi(\theta \mid X) = \frac{L(\theta)\,\pi(\theta)}{m(X)}, \qquad m(X) = \int_{\Theta} L(\theta)\,\pi(\theta)\,d\theta$$

分母 $m(X)$ 是样本的**边缘分布**（marginal / evidence），与 $\theta$ 无关，只起归一化作用。因此实际计算中几乎总是只看正比关系：

$$\boxed{\ \pi(\theta \mid X) \propto L(\theta)\,\pi(\theta)\ } \qquad\Longleftrightarrow\qquad \text{后验} \propto \text{似然} \times \text{先验}$$

> **后验分布 = 看完数据以后，我们对 $\theta$ 的最新认识。**
>
> 认知的迭代：今天的"后验"就是明天的"先验"。

---

## 三、 完整范例：Beta–Binomial 共轭

估计硬币正面概率 $\theta$。取 [[贝塔分布]] 作为先验：

$$\theta \sim \text{Beta}(a, b), \qquad \pi(\theta) \propto \theta^{a-1}(1-\theta)^{b-1}$$

抛 $n$ 次得 $x$ 次正面，似然：

$$L(\theta) \propto \theta^x (1-\theta)^{n-x}$$

两者相乘并合并指数：

$$\pi(\theta \mid X) \propto \theta^{x}(1-\theta)^{n-x} \cdot \theta^{a-1}(1-\theta)^{b-1} = \theta^{(a+x)-1}(1-\theta)^{(b+n-x)-1}$$

这仍然是一个 Beta 分布的核，所以：

$$\boxed{\ \theta \mid X \sim \text{Beta}(a+x,\ b+n-x)\ }$$

**先验和后验属于同一个分布族**，这种性质称为**共轭性**，$\text{Beta}$ 就是二项似然的**共轭先验**。共轭的好处是后验有解析解，不需要算那个恼人的积分 $m(X)$。

**数值演示**：取先验 $\text{Beta}(2,2)$（倾向于认为 $\theta$ 在 $0.5$ 附近），抛 $10$ 次得 $8$ 次正面：

$$a + x = 2 + 8 = 10, \qquad b + n - x = 2 + 10 - 8 = 4$$

$$\theta \mid X \sim \text{Beta}(10, 4)$$

原本集中在 $0.5$ 的信念，被数据往"正面概率偏大"的方向拉了过去。这就是**Bayes 更新**。

---

## 四、 后验分布不等于估计值：损失函数登场

这是最容易混淆的一点。

经典估计直接给出一个数字 $\hat\theta$；而 Bayes 的第一步产物是一整个**分布** $\pi(\theta \mid X)$，它告诉我们"看完数据后，$\theta$ 的各种可能值分别有多大可信度"。

要从这个分布里挑一个数作为估计，就得先回答：**估错了要付多大代价？**

### 1. 损失函数 $L(\theta, d)$

设真实参数为 $\theta$，给出的估计为 $d$，用 $L(\theta, d)$ 表示损失。最常见的是**平方损失**：

$$L(\theta, d) = (d - \theta)^2$$

即估得越偏，惩罚越重。若真值 $\theta = 0.7$：估 $d = 0.6$ 损失 $0.01$；估 $d = 0.2$ 损失 $0.25$，明显严重得多。

### 2. Bayes 估计的严格定义

真实 $\theta$ 仍然未知，但我们有它的后验分布，于是可以计算估计值 $d$ 的**后验期望损失**：

$$E\big[L(\theta, d) \mid X\big] = \int_{\Theta} L(\theta,d)\,\pi(\theta \mid X)\,d\theta$$

选取使它最小的 $d$：

$$\boxed{\ \hat\theta_B = \arg\min_{d} \ E\big[L(\theta, d) \mid X\big]\ }$$

这才是 Bayes 估计真正严格的定义。

---

## 五、 三种常见损失对应的估计

| 损失函数 | $L(\theta, d)$ | Bayes 估计 |
| :--- | :--- | :--- |
| 平方损失 | $(\theta - d)^2$ | **后验均值** $E(\theta \mid X)$ |
| 绝对损失 | $\lvert \theta - d \rvert$ | **后验中位数** |
| $0\text{-}1$ 型损失 | $\mathbf{1}\{\lvert\theta - d\rvert > \varepsilon\}$ | **后验众数**（即 MAP 估计） |

> 所以并非"Bayes 估计 $=$ 后验均值"永远成立。正确的说法是：**后验分布是核心，最后选哪个数字取决于你如何定义"估错的代价"。**

### 平方损失下为什么是后验均值？

记 $\mu_{\pi} = E(\theta \mid X)$，对后验期望损失做配方分解：

$$E\big[(d-\theta)^2 \mid X\big] = E\big[(\theta - \mu_\pi)^2 \mid X\big] + (d - \mu_\pi)^2 = \operatorname{Var}(\theta \mid X) + (d - \mu_\pi)^2$$

（交叉项 $-2(d-\mu_\pi)E[\theta - \mu_\pi \mid X] = 0$ 自动消失。）

第一项 $\operatorname{Var}(\theta \mid X)$ 与 $d$ 无关，是无法消除的**下界**；因此只需让第二项 $(d - \mu_\pi)^2$ 最小，显然取 $d = \mu_\pi$ 时为零。故：

$$\boxed{\ \text{平方损失下的 Bayes 估计} = \text{后验均值 } E(\theta \mid X)\ }$$

结构上与 [[均方误差]] 的偏差-方差分解完全同源，也可对照 [[条件期望与条件方差]]。

---

## 六、 回到硬币例子：Bayes 估计的加权平均结构

后验 $\theta \mid X \sim \text{Beta}(a+x,\ b+n-x)$，而 Beta 分布的均值是"第一个参数 / 两参数之和"，所以平方损失下：

$$\boxed{\ \hat\theta_B = E(\theta \mid X) = \frac{a+x}{a+b+n}\ }$$

### 1. 与 MLE 的对比

不考虑先验时，[[MLE]] 给出样本比例 $\hat\theta_{MLE} = x/n$。取 $x = 8,\ n = 10$，先验 $\text{Beta}(2,2)$：

| 方法 | 结果 |
| :--- | :--- |
| 样本（MLE） | $\dfrac{8}{10} = 0.8$ |
| 先验均值 | $\dfrac{2}{2+2} = 0.5$ |
| Bayes 估计 | $\dfrac{2+8}{2+2+10} = \dfrac{10}{14} \approx 0.714$ |

Bayes 的结果恰好落在二者之间——这不是巧合。

### 2. 拆成加权平均

$$\frac{a+x}{a+b+n} = \underbrace{\frac{a+b}{a+b+n}}_{w} \cdot \underbrace{\frac{a}{a+b}}_{\text{先验均值}} + \underbrace{\frac{n}{a+b+n}}_{1-w} \cdot \underbrace{\frac{x}{n}}_{\text{样本比例}}$$

$$\boxed{\ \hat\theta_B = w \cdot \text{先验均值} + (1-w)\cdot\text{样本估计}\ }$$

权重由"先验的等效样本量 $a+b$"与"真实样本量 $n$"的比例决定。可以把 $a, b$ 理解为**先验中虚拟的 $a$ 次正面、$b$ 次反面**。

### 3. 大样本行为

- $n$ 很小时：$a, b$ 占比大，先验主导——只有两三个样本时，本就不该因为几次偶然结果推翻既有认识；
- $n \to \infty$ 时：$a, b$ 相对 $n$ 可忽略，$\dfrac{a+x}{a+b+n} \to \dfrac{x}{n}$。

> **数据越多，先验的影响越弱，样本逐渐占主导，Bayes 估计与 MLE 渐近一致。**

这正是 Bayes 方法自洽而自然的地方：证据充分时，先验的偏见会被数据洗掉。

---

## 七、 常见共轭先验速查

| 似然（样本） | 共轭先验 | 后验 | 后验均值 |
| :--- | :--- | :--- | :--- |
| $\text{B}(n,\theta)$ 二项 | $\text{Beta}(a,b)$ | $\text{Beta}(a+x,\ b+n-x)$ | $\dfrac{a+x}{a+b+n}$ |
| $P(\lambda)$ 泊松 | $\text{Ga}(\alpha,\beta)$ | $\text{Ga}\big(\alpha+\textstyle\sum x_i,\ \beta+n\big)$ | $\dfrac{\alpha+\sum x_i}{\beta+n}$ |
| $\text{Exp}(\lambda)$ 指数 | $\text{Ga}(\alpha,\beta)$ | $\text{Ga}\big(\alpha+n,\ \beta+\textstyle\sum x_i\big)$ | $\dfrac{\alpha+n}{\beta+\sum x_i}$ |
| $N(\mu,\sigma^2)$，$\sigma^2$ 已知 | $N(\mu_0,\tau^2)$ | $N(\mu_1, \tau_1^2)$ | 见下 |

正态–正态情形（用**精度** $=$ 方差倒数来记最清楚）：

$$\frac{1}{\tau_1^2} = \frac{1}{\tau^2} + \frac{n}{\sigma^2}, \qquad \mu_1 = \tau_1^2\left(\frac{\mu_0}{\tau^2} + \frac{n\bar X}{\sigma^2}\right)$$

即**后验精度 = 先验精度 + 样本精度**，后验均值是先验均值与样本均值按各自精度的加权平均——和第六节的结构完全一致。

相关：[[伽马分布]]、[[泊松分布]]、[[正态分布]]

---

## 八、 与频率学派（UMVUE 体系）的根本区别

学 [[Rao-Blackwell 定理与 UMVUE]] 时，$\theta$ 被视为固定值。例如 $X_1,\dots,X_n \sim \text{Bernoulli}(\theta)$，我们研究 $E_\theta(U)$ 与 $\operatorname{Var}_\theta(U)$，在**无偏**估计量中寻找方差最小的那个。

Bayes 体系里 $\theta$ 本身服从分布：先验 $\theta \sim \pi(\theta)$，观察 $X$ 后 $\theta \mid X \sim \pi(\theta \mid X)$，我们讨论的是后验均值 $E(\theta \mid X)$ 与后验方差 $\operatorname{Var}(\theta \mid X)$。

| | 频率学派 | Bayes 学派 |
| :--- | :--- | :--- |
| 参数 $\theta$ | **固定**常数，样本随机 | **随机变量**，有分布 |
| 推断依据 | 抽样分布（重复抽样下的性质） | 后验分布（给定这一组数据） |
| 评价标准 | 无偏性、有效性、相合性 | 后验期望损失最小 |
| 区间 | 置信区间（覆盖率是长期频率） | 可信区间（"$\theta$ 有 95% 概率落在其中"） |
| 典型产物 | $\hat\theta_{MLE}$、UMVUE | 后验均值 / 中位数 / MAP |

> **频率学派：参数固定，样本随机；Bayes：参数也作为随机变量处理。**

注意：Bayes 估计一般**是有偏的**（第六节里它被先验往 $0.5$ 拉了），但换来的是更小的方差和小样本下的稳健性。

---

## 九、 一个生活化的理解

判断某学生做某类题的正确率 $\theta$：

- 根据以往经验，多数学生正确率约 $60\%$ —— 这是**先验信息**；
- 让他做了 $20$ 道，做对 $18$ 道 —— 这是**样本信息**。

你既不会完全无视过去的经验，也不会完全无视眼前这 $20$ 道题。Bayes 做的事就是：**把旧认识和新数据按合理的数学规则结合起来，形成新的认识（后验分布）**，再根据你对犯错的惩罚方式，从后验中选出最合适的估计。

---

## 十、 主线总结

$$\text{第一步：给参数一个先验 } \pi(\theta)$$

$$\text{第二步：观察样本，写出似然 } L(\theta)$$

$$\text{第三步：Bayes 公式求后验 } \pi(\theta \mid X) \propto L(\theta)\pi(\theta)$$

$$\text{第四步：按损失函数选估计 } \hat\theta_B = \arg\min_d E[L(\theta,d)\mid X]$$

考试最常见的平方损失情形：

$$\boxed{\ \text{平方损失} \Longrightarrow \text{Bayes 估计} = \text{后验均值}\ }$$

把这条主线理解透，后面的 Beta–Binomial、Gamma–Poisson、正态共轭先验，以及 [[EM算法]] 里的后验计算，都会顺理成章。
