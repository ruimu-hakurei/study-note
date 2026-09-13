# 极大似然估计（MLE）

极大似然估计（Maximum Likelihood Estimation, MLE）是现代数理统计与机器学习中应用最广泛的参数估计方法，由统计大师罗纳德·费雪（Ronald Fisher）系统性提出并奠定理论基础。

## 一、 核心直观哲学：概率最大化

MLE 的核心原则极其符合人类直觉：

> **"小概率事件在一次试验中几乎不可能发生；既然当前这组数据已经真实发生在我们眼前，那么真实的参数值，必然是那个让当前样本发生概率最大的参数。"**

- **矩估计（MOM）**：试图让样本平均值等于理论平均值（**特征吻合**）；

- **极大似然估计（MLE）**：试图通过调整参数，把当前这批数据出现的联合概率顶到最高峰（**概率最大化**）。

## 二、 极大似然估计的通用求解步骤

设总体 $X$ 的概率分布（离散为 PMF，连续为 PDF）为 $f(x; \theta)$，其中 $\theta$ 为未知参数（可以是标量或向量），$X_1, X_2, \dots, X_n$ 为[[总体与样本抽样|独立同分布]]（i.i.d.）的样本。

**第一步：构造似然函数 $L(\theta)$**

似然函数是样本联合概率分布的表达式，但此时**样本数据 $x_1, \dots, x_n$ 视为已知常数，参数 $\theta$ 视为自变量**：

$$L(\theta) = L(x_1, \dots, x_n; \theta) = \prod_{i=1}^n f(x_i; \theta)$$

**第二步：取对数化简（对数似然函数 $l(\theta)$）**

由于对数函数 $\ln(\cdot)$ 是严格单调递增函数，它不改变极值点的位置，同时能将复杂的连乘转化为求和：

$$l(\theta) = \ln L(\theta) = \sum_{i=1}^n \ln f(x_i; \theta)$$

**第三步：求导并建立似然方程组（求驻点）**

- **单参数情形**：令一阶导数为 0：

    $$\frac{d l(\theta)}{d\theta} = 0$$

- **多参数情形（$\boldsymbol{\theta} = (\theta_1, \dots, \theta_k)^T$）**：对各个分量分别求偏导建立方程组（梯度为 0 向量）：

    $$\nabla_\theta l(\boldsymbol{\theta}) = \mathbf{0} \iff \frac{\partial l(\boldsymbol{\theta})}{\partial \theta_j} = 0 \quad (j = 1, 2, \dots, k)$$

**第四步：解方程并验证极值性**

- 解出似然方程的解 $\hat{\theta}$；

- 检查二阶导数 $\frac{d^2 l(\theta)}{d\theta^2} < 0$（或多元情形下的 Hessian 矩阵负定），确保其为局部极大值；

- 将观测数据 $x_i$ 换回随机变量 $X_i$，写出估计量 $\hat{\theta}_{\text{MLE}}$。

## 三、 经典分布 MLE 求解范例

### 1. 正态分布 $N(\mu, \sigma^2)$（多参数光滑可导）

样本密度为 $f(x; \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$。

- **对数似然函数**：

    $$l(\mu, \sigma^2) = -\frac{n}{2}\ln(2\pi) - \frac{n}{2}\ln(\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^n (x_i - \mu)^2$$

- **分别对 $\mu$ 和 $\sigma^2$ 求偏导**：

    $$\frac{\partial l}{\partial \mu} = \frac{1}{\sigma^2}\sum_{i=1}^n (x_i - \mu) = 0 \implies \hat{\mu}_{\text{MLE}} = \bar{X}$$

    $$\frac{\partial l}{\partial \sigma^2} = -\frac{n}{2\sigma^2} + \frac{1}{2(\sigma^2)^2}\sum_{i=1}^n (x_i - \mu)^2 = 0 \implies \widehat{\sigma^2}_{\text{MLE}} = \frac{1}{n}\sum_{i=1}^n (X_i - \bar{X})^2 = S_n^2$$

### 2. 均匀分布 $U(0, \theta)$（不可导/边界极值情形）

单个样本密度为 $f(x) = \frac{1}{\theta} I_{(0 \le x \le \theta)}$。

- **似然函数**：

    $$L(\theta) = \frac{1}{\theta^n} \cdot I_{(\max(x_i) \le \theta)} \cdot I_{(\min(x_i) \ge 0)}$$

- **分析极值**：

    只要 $\theta \ge x_{(n)} = \max(x_1, \dots, x_n)$，似然函数为 $L(\theta) = \frac{1}{\theta^n}$。

    这是一个关于 $\theta$ 的**严格单调递减函数**（$\theta$ 越小，$\frac{1}{\theta^n}$ 越大）。

- **取边界最小值**：

    为了让 $L(\theta)$ 达到最大，$\theta$ 必须尽量小，但又不能小于观测到的最大样本值 $x_{(n)}$。

    因此最大值点直接取在边界上：

    $$\hat{\theta}_{\text{MLE}} = X_{(n)}$$

## 四、 MLE 的四大优良统计性质

在满足常规正则条件（如分布支撑集与参数无关、可导等）下，极大似然估计拥有极其出色的渐近性质：

- **不变性（Invariance Property）**：

    若 $\hat{\theta}$ 是 $\theta$ 的 MLE，且 $g(t)$ 是单调或任意映射函数，则 $g(\theta)$ 的 MLE 必然为 $g(\hat{\theta})$。

- **强相合性（Strong Consistency）**：

    当 $n \to \infty$ 时，MLE 几乎必然收敛到参数真值：$\hat{\theta}_{\text{MLE}} \xrightarrow{\text{a.s.}} \theta$。

- **渐近正态性（Asymptotic Normality）**：

    大样本下，MLE 的分布无限逼近正态分布：

    $$\sqrt{n}(\hat{\theta}_{\text{MLE}} - \theta) \xrightarrow{d} N\left(0, \, \frac{1}{I(\theta)}\right)$$

- **渐近有效性（Asymptotic Efficiency）**：

    MLE 的渐近方差直接达到了理论方差的下限——**克拉美-罗下界（CRLB）**，在大样本下没有任何无偏估计量的精度可以击败 MLE。

## 五、 矩估计 vs 极大似然估计 对比

| **比较维度**    | **矩估计（MOM）**                                     | **极大似然估计（MLE）**        |
| ----------- | ------------------------------------------------ | ---------------------- |
| **核心机制**    | 样本矩 = 理论矩，列代数方程                                  | 最大化样本联合出现概率（优化导数/边界）   |
| **计算复杂度**   | 计算极简，多为线性/多项式解                                   | 通常需要求导，非正则或非凸分布需数值优化   |
| **充分性**     | 通常无法完全利用充分统计量                                    | 天然与充分统计量绑定（由因子分解定理保证）  |
| **有效性（精度）** | 有限样本及大样本下往往方差偏大                                  | 具有渐近最优性，方差达到 CRLB 理论极限 |
| **参数不变性**   | 不具备（如 $\widehat{\theta^2} \ne (\hat{\theta})^2$） | 天然具备严格的不变性             |

## 六、 严谨性补充：为什么有时必须写 $\arg\sup$ 而不是 $\arg\max$

这页笔记解释的是**极大似然估计（MLE）在数学定义上的严谨性补充**——为什么有时候不能写 $\max$（最大值），而必须写 $\sup$（上确界）和闭包 $\bar{\Theta}$。

### 1. 核心符号逐一拆解

- **$\arg\max$（Argument of the Maximum）**：

    - 意思是：**"让后面这个函数达到最大值时，自变量 $\theta$ 的取值"**。

    - 例如：函数 $f(x) = -(x-2)^2 + 5$，最大值是 $5$，但 $\arg\max f(x) = 2$（要的是自变量 $x=2$）。

- **$\max$（最大值）vs $\sup$（上确界 / Supremum / 最小上界）**：

    - **$\max$**：必须能在集合里**实实在在地取到**。

    - **$\sup$**：是集合上方紧挨着的天花板，**哪怕集合自身取不到这个点，天花板依然存在**。

- **$\bar{\Theta}$（[[参数空间]]的闭包 / Closure）**：

    - $\bar{\Theta} = \Theta \cup \partial\Theta$（原开区间 加上 边界点）。

### 2. 板书中的经典对比例子

|**集合**|**sup（上确界）**|**max（最大值）**|**inf（下确界）**|**min（最小值）**|
|---|---|---|---|---|
|**集合 1**：$\{0, 1, \frac{1}{2}, \frac{1}{3}, \frac{1}{4}, \dots\}$|**$1$**|**$1$**（集合里有 1）|**$0$**|**$0$**（集合里有 0）|
|**集合 2**：$\{1, \frac{1}{2}, \frac{1}{3}, \frac{1}{4}, \dots\}$|**$1$**|**$1$**（集合里有 1）|**$0$**|**不存在**（无限趋近 0，但集合里根本没有 0）|

### 3. 为什么 MLE 有时必须写成 $\hat{\theta} = \arg\sup_{\theta \in \bar{\Theta}} L(\theta)$？

**原因：很多时候参数允许的范围是"开区间"，最优点恰好卡在开区间的边界上，导致严格意义上的最大值 $\max$ 不存在。**

**以均匀分布 $X \sim U(0, \theta)$ 为例**：

- 设参数真实物理意义为开区间 $\Theta = (0, +\infty)$。

- 抽到样本数据 $x_1, \dots, x_n$，最大值为 $x_{(n)}$。

- 如果题目定义开区间均匀分布为 $(0, \theta)$，那么理论上每一个样本点必须严格小于 $\theta$，即要求 $\theta > x_{(n)}$（参数必须落在开区间 $(x_{(n)}, +\infty)$ 内）。

- 似然函数为 $L(\theta) = \frac{1}{\theta^n}$。在开区间 $(x_{(n)}, +\infty)$ 上：

    - 当 $\theta$ 越来越接近 $x_{(n)}$ 时，$L(\theta)$ 越来越大；

    - 但因为 $\theta > x_{(n)}$ 是开区间，$\theta$ **永远取不到 $x_{(n)}$ 本身**！

    - 按照严格高等数学定义，在开区间 $(x_{(n)}, +\infty)$ 上，$L(\theta)$ **没有最大值 $\max$**。

**数学上的严谨修补方案**：

1. 取参数空间的闭包 $\bar{\Theta} = [x_{(n)}, +\infty)$（强行把边界点 $x_{(n)}$ 补进来）；

2. 改用上确界 $\sup$，此时在闭包边界上正好能取到上确界点：

    $$\hat{\theta}_{\text{MLE}} = \arg\sup_{\theta \in \bar{\Theta}} L(\theta) = x_{(n)}$$

**一句话总结：**

写 $\arg\max$ 是通俗写法；写 $\arg\sup_{\theta \in \bar{\Theta}}$ 是为了防止最优点落在开区间边界上导致数学上无解而采用的**严格数学补丁**。

## 七、 例 6.3.2：两点分布（产品不合格率）的 MLE

### 1. 题目条件

设某批产品中，抽取一件产品为不合格品的概率为 $p$（$0 < p < 1$），即总体服从两点分布 $X \sim b(1, p)$：

$$X = \begin{cases} 1, & \text{不合格（概率为 } p \text{）} \\ 0, & \text{合格（概率为 } 1-p \text{）} \end{cases}$$

从该批产品中随机独立抽取容量为 $n$ 的样本 $X_1, X_2, \dots, X_n$。

**求**：参数 $p$（总体不合格率）的极大似然估计量 $\hat{p}$。

### 2. 解题推导（标准四步法）

**第一步：写出单个样本的概率分布与样本的联合似然函数**

单个样本 $X_i$ 的概率质量函数统一写成指数形式：

$$P(X_i = x_i) = p^{x_i} (1-p)^{1-x_i}, \quad x_i \in \{0, 1\}$$

由于各样本独立同分布，构造联合似然函数 $L(p)$（所有样本同时发生的联合概率）：

$$L(p) = \prod_{i=1}^n P(X_i = x_i; p) = \prod_{i=1}^n \left[ p^{x_i} (1-p)^{1-x_i} \right]$$

合并底数相同的幂次：

$$L(p) = p^{\sum_{i=1}^n x_i} (1-p)^{\sum_{i=1}^n (1-x_i)} = p^{\sum_{i=1}^n x_i} (1-p)^{n - \sum_{i=1}^n x_i}$$

**第二步：取对数化简为对数似然函数 $l(p)$**

连乘形式求导极易出错，两边取自然对数，将乘法转化为加法：

$$l(p) = \ln L(p) = \ln\left[ p^{\sum_{i=1}^n x_i} (1-p)^{n - \sum_{i=1}^n x_i} \right]$$

利用对数性质拆开：

$$l(p) = \left(\sum_{i=1}^n x_i\right) \ln p + \left(n - \sum_{i=1}^n x_i\right) \ln(1-p)$$

**第三步：对未知参数 $p$ 求导并令导数为 0（列对数似然方程）**

$$\frac{d l(p)}{dp} = \frac{\sum_{i=1}^n x_i}{p} + \left(n - \sum_{i=1}^n x_i\right) \cdot \frac{-1}{1-p} = 0$$

$$\frac{\sum_{i=1}^n x_i}{p} - \frac{n - \sum_{i=1}^n x_i}{1-p} = 0$$

交叉相乘去分母：

$$(1-p)\sum_{i=1}^n x_i = p\left(n - \sum_{i=1}^n x_i\right)$$

展开去括号：

$$\sum_{i=1}^n x_i - p\sum_{i=1}^n x_i = n p - p\sum_{i=1}^n x_i$$

两边同时消去 $-p\sum_{i=1}^n x_i$：

$$n p = \sum_{i=1}^n x_i \implies p = \frac{1}{n}\sum_{i=1}^n x_i = \bar{x}$$

**第四步：验证驻点为极大值点并给出估计量**

对 $l(p)$ 求二阶导数：

$$\frac{d^2 l(p)}{dp^2} = -\frac{\sum_{i=1}^n x_i}{p^2} - \frac{n - \sum_{i=1}^n x_i}{(1-p)^2}$$

当 $0 < p < 1$ 且样本中至少有一个合格和一个不合格时，二阶导数恒有 $\frac{d^2 l(p)}{dp^2} < 0$，说明函数图形严格上凸，驻点必为全局极大值点。

将具体样本观测值 $x_i$ 换回随机变量 $X_i$，得到**极大似然估计量**：

$$\hat{p}_{\text{MLE}} = \bar{X} = \frac{1}{n}\sum_{i=1}^n X_i$$

### 3. 直观理解

如果抽检 100 个零件（$n=100$），发现有 3 个不合格（$\sum x_i = 3$），[[样本均值与样本方差|样本均值]]即为 $\bar{X} = \frac{3}{100} = 3\%$。

极大似然法从严格的数学角度证明了：**手头这 100 个零件算出的不合格品发生率（$3\%$），就是推测这整批零件真实不合格率 $p$ 最合理的估计值。**

## 八、 例：多项分布（基因型频率）的 MLE

### 1. 题目背景与模型构建

某生物群体中某对等位基因包含三种基因型（如 $AA, Aa, aa$），其理论发生概率分别为：

- $p_1(\theta) = \theta^2$

- $p_2(\theta) = 2\theta(1-\theta)$

- $p_3(\theta) = (1-\theta)^2$

从总体中随机调查 $n$ 个个体，观测到三种基因型出现的频数分别为 $n_1, n_2, n_3$（满足 $n_1 + n_2 + n_3 = n$）。

**求**：基因频率参数 $\theta$（$0 < \theta < 1$）的极大似然估计量 $\hat{\theta}$。

### 2. 似然函数与对数似然函数

由多项分布，样本的联合似然函数为：

$$L(\theta) = p_1^{n_1} p_2^{n_2} p_3^{n_3} = (\theta^2)^{n_1} \cdot [2\theta(1-\theta)]^{n_2} \cdot [(1-\theta)^2]^{n_3} = 2^{n_2} \theta^{2n_1 + n_2} (1-\theta)^{n_2 + 2n_3}$$

两边取自然对数，得到对数似然函数 $l(\theta) = \ln L(\theta)$：

$$l(\theta) = n_2 \ln 2 + (2n_1 + n_2)\ln\theta + (n_2 + 2n_3)\ln(1-\theta)$$

### 3. 求导建立对数似然方程

对未知参数 $\theta$ 求一阶导数，并令其等于 $0$（第一项常数导数为 0）：

$$\frac{d l(\theta)}{d\theta} = \frac{2n_1 + n_2}{\theta} - \frac{n_2 + 2n_3}{1 - \theta} = 0$$

### 4. 解方程求出估计量

移项交叉相乘：

$$(1 - \theta)(2n_1 + n_2) = \theta(n_2 + 2n_3)$$

展开化简：

$$2n_1 + n_2 - \theta(2n_1 + n_2) = \theta(n_2 + 2n_3)$$

$$2n_1 + n_2 = \theta(2n_1 + n_2 + n_2 + 2n_3)$$

合并右边括号内的项：

$$2n_1 + n_2 = \theta(2n_1 + 2n_2 + 2n_3) = 2\theta(n_1 + n_2 + n_3)$$

代入 $n_1 + n_2 + n_3 = n$：

$$2n_1 + n_2 = 2n \theta \implies \hat{\theta} = \frac{2n_1 + n_2}{2n}$$

### 5. 二阶导数验证与生物学意义

1. **二阶导数判据**：

    $$\frac{d^2 l(\theta)}{d\theta^2} = -\frac{2n_1 + n_2}{\theta^2} - \frac{n_2 + 2n_3}{(1-\theta)^2} < 0$$

    驻点必为全局极大值点。

2. **生物学/统计学直观**：

    - $n$ 个二倍体个体总共含有 **$2n$ 个等位基因**（总基因库容量）；

    - 显性纯合子 $AA$（$n_1$ 个）贡献了 $2n_1$ 个显性基因 $A$；

    - 杂合子 $Aa$（$n_2$ 个）贡献了 $n_2$ 个显性基因 $A$；

    - 因此，显性基因 $A$ 在抽样样本中的实际出现频率就是：

        $$\hat{\theta}_{\text{MLE}} = \frac{2n_1 + n_2}{2n}$$

        极大似然估计的结果与生物学中"数基因个数算频率"的朴素直觉完全吻合。

## 九、 渐近正态性：Fisher 信息量与推导全景

这个结论的核心本质是：**极大似然方程经过一阶泰勒展开后，参数的误差项可以被转化为"独立同分布随机变量的算术平均"，随后直接触发了[[Lindeberg-Levy 中心极限定理|中心极限定理]]（CLT）。**

**Fisher 信息量**与**渐近正态性（Asymptotic Normality）**是现代大样本统计学与极大似然理论（MLE）的两大支柱。Fisher 信息量度量了数据对参数的**信息浓度与理论精度上限**，而渐近正态性则指出了**在大样本极限下，MLE 的误差分布必然呈现为均值为 0、方差为 Fisher 信息量倒数的标准钟形曲线**。

### 1. 核心桥梁：Fisher 信息量（Fisher Information）

Fisher 信息量度量了单次抽样中样本所携带的关于未知参数 $\theta$ 的确定性程度。

**（1）评分函数（Score Function）**

对数似然对参数的一阶导数定义为评分函数 $S(X; \theta)$：

$$S(X; \theta) = \frac{\partial \ln f(X; \theta)}{\partial \theta}$$

- **一阶性质（无偏性）**：在全概率积分为 1 的正则条件下，评分函数的期望恒为 0：

    $$E[S(X; \theta)] = \int \frac{\partial \ln f(x; \theta)}{\partial \theta} f(x; \theta) \, dx = \int \frac{\partial f(x; \theta)}{\partial \theta} \, dx = \frac{d}{d\theta}(1) = 0$$

**（2）Fisher 信息量的双重定义与等价性**

单个样本的 Fisher 信息量 $I(\theta)$ 定义为评分函数的方差（二阶原点矩）：

$$I(\theta) \triangleq Var(S(X; \theta)) = E\left[ \left(\frac{\partial \ln f(X; \theta)}{\partial \theta}\right)^2 \right]$$

由二阶对数导数恒等式，它等价于**对数似然二阶导数期望的相反数（似然曲面的平均曲率）**：

$$I(\theta) = -E\left[ \frac{\partial^2 \ln f(X; \theta)}{\partial \theta^2} \right]$$

- **物理/几何直观**：

    - $I(\theta)$ 极大 $\implies$ 似然函数在真值处极度陡峭、曲率极高 $\implies$ 稍有偏离似然值急剧下跌 $\implies$ 参数被极强地锁定，估计精度高。

    - $I(\theta)$ 极小 $\implies$ 似然函数平缓 $\implies$ 观测数据对参数不敏感，估计方差极大。

**（3）样本可加性与 CRLB 理论极限**

- **独立样本可加性**：对于容量为 $n$ 的独立同分布样本，总信息量线性叠加：

    $$I_n(\theta) = n I(\theta)$$

- **克拉美-罗下界（CRLB）**：任何无偏估计量 $\hat{\theta}$ 的方差绝对不可能低于总信息量的倒数：

    $$Var(\hat{\theta}) \ge \frac{1}{n I(\theta)}$$

### 2. 渐近正态性（Asymptotic Normality）推导全景

**定理表述**：

在常规正则条件下，极大似然估计量 $\hat{\theta}_n$ 当 $n \to \infty$ 时，其误差放大 $\sqrt{n}$ 倍后，依分布收敛于均值为 0、方差为单样本 Fisher 信息量倒数的正态分布：

$$\sqrt{n}(\hat{\theta}_n - \theta) \xrightarrow{d} N\left(0, \, \frac{1}{I(\theta)}\right)$$

写成大样本近似形式即为：

$$\hat{\theta}_n \dot{\sim} N\left(\theta, \, \frac{1}{n I(\theta)}\right)$$

**数学推导三步法**：

1. **极大似然方程的一阶泰勒展开**：

    极大似然估计量满足驻点方程 $\sum_{i=1}^n \frac{\partial \ln f(X_i; \hat{\theta}_n)}{\partial \theta} = 0$。

    将总对数似然一阶导在真实参数 $\theta$ 处展开：

    $$0 = l'(\hat{\theta}_n) \approx l'(\theta) + l''(\theta)(\hat{\theta}_n - \theta)$$

    解出估计误差项：

    $$\sqrt{n}(\hat{\theta}_n - \theta) \approx \frac{\frac{1}{\sqrt{n}} l'(\theta)}{-\frac{1}{n} l''(\theta)} = \frac{\frac{1}{\sqrt{n}}\sum_{i=1}^n S(X_i; \theta)}{-\frac{1}{n}\sum_{i=1}^n \frac{\partial^2 \ln f(X_i; \theta)}{\partial \theta^2}}$$

2. **分子触发中心极限定理（CLT）**：

    由于 $S(X_i; \theta)$ 独立同分布，且 $E[S] = 0, Var(S) = I(\theta)$，由独立同分布中心极限定理：

    $$\frac{1}{\sqrt{n}}\sum_{i=1}^n S(X_i; \theta) \xrightarrow{d} N\big(0, \, I(\theta)\big)$$

3. **分母触发辛钦[[大数定律]]（LLN）与 Slutsky 定理**：

    分母为二阶导数的算术平均，依概率收敛于其期望常数：

    $$-\frac{1}{n}\sum_{i=1}^n \frac{\partial^2 \ln f(X_i; \theta)}{\partial \theta^2} \xrightarrow{P} -E\left[\frac{\partial^2 \ln f(X; \theta)}{\partial \theta^2}\right] = I(\theta)$$

    由 Slutsky 定理，分子（正态随机变量）除以分母（确定性常数），方差缩小为：

    $$\frac{Var(N(0, I(\theta)))}{[I(\theta)]^2} = \frac{I(\theta)}{[I(\theta)]^2} = \frac{1}{I(\theta)} \implies \sqrt{n}(\hat{\theta}_n - \theta) \xrightarrow{d} N\left(0, \, \frac{1}{I(\theta)}\right)$$

### 3. 渐近正态性的三大工程与统计应用

- **证明 MLE 达到渐近有效性（Asymptotic Efficiency）**：

    在大样本极限下，MLE 的渐近方差 $\frac{1}{n I(\theta)}$ 严格等于 CRLB 理论下界。说明随着数据量增加，**没有任何统计估计量的精度能够超越 MLE**。

- **无需推导精确分布即可构造置信区间**：

    对于任意未知分布，只要样本量 $n$ 足够大，直接使用经验 Fisher 信息量 $\hat{I}_n = -\frac{1}{n}\sum \frac{\partial^2 \ln f(x_i; \hat{\theta})}{\partial \theta^2}$ 估计方差，其 $95\%$ 置信区间即为：

    $$\left[ \hat{\theta} - 1.96 \sqrt{\frac{1}{n \hat{I}_n}}, \; \hat{\theta} + 1.96 \sqrt{\frac{1}{n \hat{I}_n}} \right]$$

- **构建 Wald 假设检验统计量**：

    检验原假设 $H_0: \theta = \theta_0$，直接构造 Wald 检验统计量：

    $$W = n I(\hat{\theta}) (\hat{\theta} - \theta_0)^2 \xrightarrow{d} \chi^2(1)$$

    无需进行重抽样或复杂代数变换，直接查[[卡方分布]]表即可完成假设检验。
