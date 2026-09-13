# EM算法（Expectation-Maximization）

EM算法（Expectation-Maximization，期望最大化算法）是一种迭代优化算法，专门用于在包含**隐变量（Latent Variables）**的统计模型中，寻找参数的极大似然估计（MLE）或最大后验估计（MAP）。

## 核心直观比喻（打破"鸡生蛋与蛋生鸡"的僵局）

假设你想统计一所学校里男生和女生的平均身高与方差（待估参数），但你拿到的是一份完全没有标明性别（隐变量）的身高数据表。

- **E步（猜标签）**：先随便假设一组男/女生的平均身高。利用这个假设，计算表中每一个身高数据属于男生或女生的概率。

- **M步（算参数）**：把刚才算出的概率当作权重（"软标签"），重新计算出更准确的男/女生平均身高和方差。

    不断交替重复这两步，直到算出来的身高参数不再发生变化，模型就达到了收敛状态。

## 数学原理解析

当模型含有隐变量 $Z$ 时，直接最大化观测数据 $X$ 的对数似然函数极其困难，因为对数函数内部存在对隐变量的求和/积分：$L(\theta) = \ln \sum_Z P(X, Z \mid \theta)$。EM 算法通过构造似然函数的下界（Q 函数），将复杂优化转化为两步迭代：

- **E步（Expectation 期望）**：

    根据当前参数 $\theta^{(t)}$ 和观测数据 $X$，计算隐变量 $Z$ 的条件后验分布，并求出完全数据对数似然函数的期望（Q 函数）：

    $$Q(\theta, \theta^{(t)}) = E_{Z \mid X, \theta^{(t)}} [\ln P(X, Z \mid \theta)]$$

- **M步（Maximization 最大化）**：

    寻找一个新的参数 $\theta$，使得 E 步构造的 Q 函数最大化，作为下一次迭代的参数 $\theta^{(t+1)}$：

    $$\theta^{(t+1)} = \arg\max_\theta Q(\theta, \theta^{(t)})$$

    EM 算法的核心是通过**构造下界并不断顶高下界**，来解决含有"隐藏变量"（缺失数据）时的极大似然估计问题。

## 一、 问题的数学根源：为什么直接求导失效？

设观测数据为 $X = (x_1, \dots, x_n)$，未观测到的隐变量为 $Z = (z_1, \dots, z_n)$，待估计的模型参数为 $\theta$。

我们希望最大化观测数据的边缘对数似然（Marginal Log-Likelihood）：

$$L(\theta) = \ln P(X \mid \theta) = \ln \sum_{Z} P(X, Z \mid \theta)$$

- **困境**：隐变量的边缘化求和符号 $\sum_{Z}$ 位于对数函数 $\ln(\cdot)$ 的内部。

- 对 $\theta$ 求导时：

    $$\frac{\partial}{\partial \theta} \ln \sum_{Z} P(X, Z \mid \theta) = \frac{\sum_{Z} \frac{\partial P(X, Z \mid \theta)}{\partial \theta}}{\sum_{Z} P(X, Z \mid \theta)}$$

    求和项与参数相互耦合，无法直接求出解析解（闭式解）。

## 二、 核心数学基石：Jensen 不等式与下界（ELBO）构建

引入一个定义在隐变量 $Z$ 上的**任意概率分布** $q(Z)$，满足：

$$\sum_{Z} q(Z) = 1, \quad q(Z) \ge 0$$

对观测似然进行恒等变形并应用 **Jensen 不等式**：

$$L(\theta) = \ln \sum_{Z} P(X, Z \mid \theta) = \ln \sum_{Z} q(Z) \cdot \frac{P(X, Z \mid \theta)}{q(Z)} = \ln E_{q(Z)}\left[ \frac{P(X, Z \mid \theta)}{q(Z)} \right]$$

由于自然对数 $\ln(u)$ 是严格的**凹函数（Concave Function）**，由 Jensen 不等式（$f(E[u]) \ge E[f(u)]$）：

$$\ln E_{q(Z)}\left[ \frac{P(X, Z \mid \theta)}{q(Z)} \right] \ge E_{q(Z)}\left[ \ln \frac{P(X, Z \mid \theta)}{q(Z)} \right]$$

展开右边，得到对数似然的**证据下界（Evidence Lower Bound, ELBO）**，记为 $\mathcal{L}(q, \theta)$：

$$\mathcal{L}(q, \theta) = \sum_{Z} q(Z) \ln \frac{P(X, Z \mid \theta)}{q(Z)} = \sum_{Z} q(Z) \ln P(X, Z \mid \theta) - \sum_{Z} q(Z) \ln q(Z)$$

因此，对于任意的概率分布 $q(Z)$ 和任意参数 $\theta$，恒有：

$$L(\theta) \ge \mathcal{L}(q, \theta)$$

## 三、 目标分解与 KL 散度视角

我们可以将原始的对数似然 $L(\theta)$ 精确分解为两部分：

利用条件概率公式 $P(X, Z \mid \theta) = P(Z \mid X, \theta) P(X \mid \theta)$ 代入 $\mathcal{L}(q, \theta)$：

$$\begin{aligned} \mathcal{L}(q, \theta) &= \sum_{Z} q(Z) \ln \frac{P(Z \mid X, \theta) P(X \mid \theta)}{q(Z)} \\ &= \sum_{Z} q(Z) \ln P(X \mid \theta) + \sum_{Z} q(Z) \ln \frac{P(Z \mid X, \theta)}{q(Z)} \\ &= \ln P(X \mid \theta) \underbrace{\sum_{Z} q(Z)}_{=1} - \sum_{Z} q(Z) \ln \frac{q(Z)}{P(Z \mid X, \theta)} \\ &= L(\theta) - D_{\text{KL}}\big( q(Z) \,\Vert{}\, P(Z \mid X, \theta) \big) \end{aligned}$$

移项得到完整的数学恒等式：

$$L(\theta) = \mathcal{L}(q, \theta) + D_{\text{KL}}\big( q(Z) \,\Vert{}\, P(Z \mid X, \theta) \big)$$

- **$D_{\text{KL}}(q \Vert{} P)$**：$q(Z)$ 与真实后验分布 $P(Z \mid X, \theta)$ 之间的 **KL 散度（Kullback-Leibler Divergence）**。

- 由 Gibbs 不等式可知，KL 散度恒非负：$D_{\text{KL}} \ge 0$。当且仅当 $q(Z) = P(Z \mid X, \theta)$ 时，$D_{\text{KL}} = 0$。

## 四、 E 步与 M 步的严格数学迭代

EM 算法本质上是在优化空间 $(q, \theta)$ 上交替最大化目标函数 $\mathcal{L}(q, \theta)$：

```
                 max_θ L(q*, θ)  [M 步: 参数向上爬升]
                     ^
                     |
         L(q*, θ^(t)) = ln P(X|θ^(t))  [E 步: 下界顶到天花板]
```

### 1. E 步（Expectation Step）

- **固定当前参数** $\theta^{(t)}$，寻找最优分布 $q(Z)$ 使下界 $\mathcal{L}(q, \theta^{(t)})$ 最大化（紧贴真实曲线）：

    $$q^{(t+1)}(Z) = \arg\max_{q} \mathcal{L}(q, \theta^{(t)}) \iff \arg\min_{q} D_{\text{KL}}\big( q(Z) \,\Vert{}\, P(Z \mid X, \theta^{(t)}) \big)$$

- 最小值在 KL 散度为 0 时取得，因此最优选择必然是**后验概率分布**：

    $$q^{(t+1)}(Z) = P(Z \mid X, \theta^{(t)})$$

- 此时下界与原似然函数在 $\theta^{(t)}$ 处完全相等：$\mathcal{L}(q^{(t+1)}, \theta^{(t)}) = L(\theta^{(t)})$。

- 将 $q^{(t+1)}(Z)$ 代入 $\mathcal{L}(q, \theta)$，去掉与待估参数 $\theta$ 无关的熵项后，得到 **$Q$ 函数（完全数据对数似然的期望）**：

    $$Q(\theta, \theta^{(t)}) \triangleq E_{Z \mid X, \theta^{(t)}} [\ln P(X, Z \mid \theta)] = \sum_{Z} P(Z \mid X, \theta^{(t)}) \ln P(X, Z \mid \theta)$$

### 2. M 步（Maximization Step）

- **固定隐变量分布** $q^{(t+1)}(Z)$，对参数 $\theta$ 最大化 $Q$ 函数以获得新参数 $\theta^{(t+1)}$：

    $$\theta^{(t+1)} = \arg\max_{\theta} Q(\theta, \theta^{(t)}) = \arg\max_{\theta} \sum_{Z} P(Z \mid X, \theta^{(t)}) \ln P(X, Z \mid \theta)$$

- 此时由于求和符号在 $\ln$ 外部，通常可以通过求偏导并令其为 0（$\nabla_\theta Q = \mathbf{0}$）直接求解出解析解。

## 五、 经典应用：高斯混合模型（GMM）推导实战

假设数据由 $K$ 个不同的高斯分布混合生成，每个高斯的权重为 $\pi_k$，参数为 $(\mu_k, \sigma_k^2)$。隐变量 $z_{ik} = 1$ 表示第 $i$ 个样本来自第 $k$ 个高斯分量。

- **E 步（算响应度 / 软分配权重）**： 计算第 $i$ 个样本属于第 $k$ 个高斯分布的后验概率 $\gamma_{ik}$：

    $$\gamma_{ik} = P(z_{ik} = 1 \mid x_i, \theta^{(t)}) = \frac{\pi_k^{(t)}\, \mathcal{N}\big(x_i \mid \mu_k^{(t)}, \sigma_k^{2(t)}\big)}{\sum_{j=1}^{K} \pi_j^{(t)}\, \mathcal{N}\big(x_i \mid \mu_j^{(t)}, \sigma_j^{2(t)}\big)}$$

- **M 步（加权更新参数）**： 利用刚才算出的权重 $\gamma_{ik}$，分别更新每个高斯分量的均值、方差和混合权重：

    $$\mu_k^{(t+1)} = \frac{\sum_{i=1}^{n} \gamma_{ik} \, x_i}{\sum_{i=1}^{n} \gamma_{ik}}$$

    $$\sigma_k^{2(t+1)} = \frac{\sum_{i=1}^{n} \gamma_{ik} \left(x_i - \mu_k^{(t+1)}\right)^2}{\sum_{i=1}^{n} \gamma_{ik}}$$

    $$\pi_k^{(t+1)} = \frac{\sum_{i=1}^{n} \gamma_{ik}}{n}$$

## 六、 数学收敛性证明（似然单调递增性）

我们要证明：每进行一次完整的 E 步和 M 步迭代，观测数据的对数似然函数必然**单调不减**，即：

$$L(\theta^{(t+1)}) \ge L(\theta^{(t)})$$

### 证明推导

$$\begin{aligned} L(\theta^{(t+1)}) &\ge \mathcal{L}(q^{(t+1)}, \theta^{(t+1)}) \quad &(\text{因为 } D_{\text{KL}} \ge 0) \\ &\ge \mathcal{L}(q^{(t+1)}, \theta^{(t)}) \quad &(\text{由 M 步定义: } \theta^{(t+1)} \text{ 最大化了 } \mathcal{L}(q^{(t+1)}, \theta)) \\ &= L(\theta^{(t)}) \quad &(\text{由 E 步定义: 当前点处 } D_{\text{KL}} = 0) \end{aligned}$$

即：

$$L(\theta^{(t+1)}) \ge L(\theta^{(t)})$$

### 收敛结论

因为概率 $P(X \mid \theta) \le 1$，所以对数似然函数存在上界 $L(\theta) \le 0$。根据实分析中的**单调有界收敛定理**，序列 $\{L(\theta^{(t)})\}$ 必定收敛到某个有限值。

## 七、 数值实例：双硬币投掷实验（Two-Coin Toss Experiment）

这里以自然语言处理（NLP）和机器学习中最著名的双硬币投掷实验为例，使用极简的具体数值走一遍 EM 算法的完整过程。

### 1. 场景设定与已知数据

桌上有两枚不均匀的硬币 $A$ 和 $B$，正面朝上的概率分别为 $\theta_A$ 和 $\theta_B$（待估计参数）。

实验人员做了 **2 轮实验**，每轮独立投掷 5 次（共 10 次投掷）：

- **第 1 轮**：掷出 **4 次正面，1 次反面**（记为 `4H, 1T`）；
    
- **第 2 轮**：掷出 **1 次正面，4 次反面**（记为 `1H, 4T`）。
    
- **隐变量 $Z$**：实验人员没有记录每一轮具体选用了哪枚硬币（硬币标签缺失）。
    
- **目标**：估计两枚硬币的真实正面概率 $\theta_A$ 与 $\theta_B$。
    

### 2. 第 0 步：初始化参数（初始猜测）

设初始正面概率为：

$$\theta_A^{(0)} = 0.6, \quad \theta_B^{(0)} = 0.5$$

### 3. 第 1 轮迭代：E 步（算硬币来源的后验概率）

根据二项分布公式 $P(k\text{H}, (5-k)\text{T}) = \binom{5}{k} \theta^k (1-\theta)^{5-k}$ 计算每轮数据由各硬币生成的可能性：

- **针对第 1 轮（4H, 1T）**：
    
    - 若来自硬币 $A$：$P_A = \binom{5}{4} (0.6)^4 (0.4)^1 = 5 \times 0.1296 \times 0.4 \approx 0.2592$
        
    - 若来自硬币 $B$：$P_B = \binom{5}{4} (0.5)^4 (0.5)^1 = 5 \times 0.0625 \times 0.5 \approx 0.1563$
        
    - **硬币 $A$ 的归属权重**：$\gamma_{1,A} = \frac{0.2592}{0.2592 + 0.1563} \approx 0.62$
        
    - **硬币 $B$ 的归属权重**：$\gamma_{1,B} = 1 - 0.62 = 0.38$
        
- **针对第 2 轮（1H, 4T）**：
    
    - 若来自硬币 $A$：$P_A = \binom{5}{1} (0.6)^1 (0.4)^4 = 5 \times 0.6 \times 0.0256 \approx 0.0768$
        
    - 若来自硬币 $B$：$P_B = \binom{5}{1} (0.5)^1 (0.5)^4 = 5 \times 0.5 \times 0.0625 \approx 0.1563$
        
    - **硬币 $A$ 的归属权重**：$\gamma_{2,A} = \frac{0.0768}{0.0768 + 0.1563} \approx 0.33$
        
    - **硬币 $B$ 的归属权重**：$\gamma_{2,B} = 1 - 0.33 = 0.67$
        

### 4. 第 1 轮迭代：M 步（按概率软分配并更新参数）

用计算出的归属概率将正反面次数“切分”给两枚硬币，重新统计各自的总正面数与总反面数：

- **硬币 $A$ 贡献的期望计数**：
    
    - 正面总数：$0.62 \times 4\text{H} + 0.33 \times 1\text{H} = 2.48 + 0.33 = 2.81$
        
    - 反面总数：$0.62 \times 1\text{T} + 0.33 \times 4\text{T} = 0.62 + 1.32 = 1.94$
        
    - **更新 $\theta_A^{(1)}$**：
        
        $$\theta_A^{(1)} = \frac{\text{正面期望数}}{\text{总期望投掷数}} = \frac{2.81}{2.81 + 1.94} = \frac{2.81}{4.75} \approx 0.59$$
        
- **硬币 $B$ 贡献的期望计数**：
    
    - 正面总数：$0.38 \times 4\text{H} + 0.67 \times 1\text{H} = 1.52 + 0.67 = 2.19$
        
    - 反面总数：$0.38 \times 1\text{T} + 0.67 \times 4\text{T} = 0.38 + 2.68 = 3.06$
        
    - **更新 $\theta_B^{(1)}$**：
        
        $$\theta_B^{(1)} = \frac{\text{正面期望数}}{\text{总期望投掷数}} = \frac{2.19}{2.19 + 3.06} = \frac{2.19}{5.25} \approx 0.42$$
        

### 5. 总结对比

|**轮次**|**硬币 A 正面概率 $\theta_A$**|**硬币 B 正面概率 $\theta_B$**|**状态说明**|
|---|---|---|---|
|**初始状态**|$0.60$|$0.50$|初始人工猜测|
|**第 1 次迭代后**|$0.59$|$0.42$|第 1 轮偏向 $A$（更可能出正面），第 2 轮偏向 $B$（更可能出反面）|
|**多轮收敛后**|$\approx 0.80$|$\approx 0.20$|最终稳定收敛至局部极大值点|
