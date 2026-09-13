# Jackknife（刀切法）

**Jackknife（刀切法）**是统计学中一种经典的**非参数重抽样（Resampling）技术**，由 Maurice Quenouille 于 1949 年提出，后由 John Tukey 进一步推广并命名。

它的核心思想是：**通过系统性地每次“切掉”样本中的一个观测值（留一重抽样，Leave-One-Out），基于剩余的 $n-1$ 个样本重新计算统计量，从而在无需对总体分布做任何先验假定的情况下，量化并消除估计量的偏差（Bias Reduction），同时精确估计其方差与标准误差。**

## 一、 核心数学构造：留一统计量与伪值

设有一组样本 $\mathbf{X} = (X_1, X_2, \dots, X_n)$，待估计参数为 $\theta$。基于全样本计算出的初始估计量记为：

$$\hat{\theta} = \hat{\theta}(X_1, X_2, \dots, X_n)$$

**1. 留一统计量（Partial Estimates）**

每次剔除第 $i$ 个观测值 $X_i$，用剩余的 $n-1$ 个数据计算该估计量，得到第 $i$ 个刀切估计值：

$$\hat{\theta}_{(i)} = \hat{\theta}(X_1, \dots, X_{i-1}, X_{i+1}, \dots, X_n), \quad (i = 1, 2, \dots, n)$$

所有留一估计值的算术平均记为：

$$\bar{\theta}_{(\cdot)} = \frac{1}{n} \sum_{i=1}^n \hat{\theta}_{(i)}$$

**2. 伪值（Pseudovalues）**

Tukey 引入了“伪值”的概念，将每个局部估计量转化为一组近似[[总体与样本抽样|独立同分布]]的单点等价估计：

$$\tilde{\theta}_i = n \hat{\theta} - (n - 1)\hat{\theta}_{(i)}, \quad (i = 1, 2, \dots, n)$$

## 二、 偏差消除与修正推导（Bias Reduction）

许多常用估计量（如[[MLE|极大似然估计]]、样本相关系数、非线性函数估计等）虽然有偏，但其偏差通常可按样本量 $n$ 的倒数展开为渐近幂级数：

$$E(\hat{\theta}) = \theta + \frac{a_1}{n} + \frac{a_2}{n^2} + O\left(\frac{1}{n^3}\right)$$

由于每个 $\hat{\theta}_{(i)}$ 基于 $n-1$ 个样本，其期望为：

$$E(\hat{\theta}_{(i)}) = \theta + \frac{a_1}{n - 1} + \frac{a_2}{(n - 1)^2} + O\left(\frac{1}{n^3}\right)$$

对所有 $i$ 取平均后，$\bar{\theta}_{(\cdot)}$ 的期望同样为：

$$E(\bar{\theta}_{(\cdot)}) = \theta + \frac{a_1}{n - 1} + O\left(\frac{1}{n^2}\right)$$

**构造消去 $O(1/n)$ 阶偏差的组合：**

我们将全样本估计量乘以 $n$，留一均值乘以 $(n-1)$ 并相减：

$$\hat{\theta}_{\text{Jack}} = n \hat{\theta} - (n - 1)\bar{\theta}_{(\cdot)} = \frac{1}{n}\sum_{i=1}^n \tilde{\theta}_i$$

计算其数学期望：

$$E(\hat{\theta}_{\text{Jack}}) = n\left[\theta + \frac{a_1}{n} + O\left(\frac{1}{n^2}\right)\right] - (n-1)\left[\theta + \frac{a_1}{n-1} + O\left(\frac{1}{n^2}\right)\right]$$

$$= (n\theta - (n-1)\theta) + (a_1 - a_1) + O\left(\frac{1}{n^2}\right) = \theta + O\left(\frac{1}{n^2}\right)$$

- **结论**：原始估计量的首阶偏差项 $\frac{a_1}{n}$ 被完全抵消，新估计量 $\hat{\theta}_{\text{Jack}}$ 的偏差下降到了 $O(1/n^2)$ 阶。
    
- 估计量原本的偏差可估计为：
    
    $$\widehat{\text{Bias}}(\hat{\theta}) = (n - 1)(\bar{\theta}_{(\cdot)} - \hat{\theta})$$
    

## 三、 方差与标准误差估计

Tukey 发现，构造出的伪值 $\tilde{\theta}_1, \dots, \tilde{\theta}_n$ 在性质上与独立的随机变量非常相似。对其计算常规[[样本均值与样本方差|样本方差]]并除以 $n$，即可得到 $\hat{\theta}$ 的刀切方差估计：

$$\widehat{Var}_{\text{Jack}}(\hat{\theta}) = \frac{1}{n(n - 1)}\sum_{i=1}^n (\tilde{\theta}_i - \hat{\theta}_{\text{Jack}})^2$$

将其化简为只依赖 $\hat{\theta}_{(i)}$ 的标准表达形式：

$$\widehat{Var}_{\text{Jack}}(\hat{\theta}) = \frac{n - 1}{n} \sum_{i=1}^n \left(\hat{\theta}_{(i)} - \bar{\theta}_{(\cdot)}\right)^2$$

标准误差（Standard Error, SE）即为方差的算术平方根：

$$\widehat{\text{SE}}_{\text{Jack}}(\hat{\theta}) = \sqrt{\widehat{Var}_{\text{Jack}}(\hat{\theta})}$$

> **常数因子 $\frac{n-1}{n}$ 的直观**：
> 
> 因为每次重抽样只剔除 1 个样本，各 $\hat{\theta}_{(i)}$ 之间共享了 $n-2$ 个数据，彼此高度相关，导致 $\hat{\theta}_{(i)}$ 围绕均值的离散度人为偏小。系数 $\frac{n-1}{n}$（比常规的 $\frac{1}{n(n-1)}$ 大了 $(n-1)^2$ 倍）起到了**放大方差、纠正强自相关性**的作用。

## 四、 经典案例：估计方差与非线性参数

**1. 验证线性统计量（样本均值 $\bar{X}$）**

- 留一估计：$\bar{X}_{(i)} = \frac{n\bar{X} - X_i}{n-1}$
    
- 刀切方差估计：
    
    $$\widehat{Var}_{\text{Jack}}(\bar{X}) = \frac{n-1}{n}\sum_{i=1}^n \left(\frac{n\bar{X}-X_i}{n-1} - \bar{X}\right)^2 = \frac{n-1}{n} \sum_{i=1}^n \left(\frac{\bar{X}-X_i}{n-1}\right)^2 = \frac{\sum(X_i-\bar{X})^2}{n(n-1)} = \frac{S^2}{n}$$
    
    _结果与经典理论完全吻合。_
    

**2. 估计比率或非线性转换（$R = \bar{X}/\bar{Y}$）**

在实际工程、计量经济或传感器校准中，两个测量均值的比值 $\hat{R} = \frac{\bar{X}}{\bar{Y}}$ 往往是有偏的，且难以直接写出解析方差。利用 Jackknife 可以非常轻松地消除一阶偏差并得到稳定的[[总体置信区间|置信区间]]，免去泰勒展开（Delta 方法）的繁琐求导。

## 五、 Jackknife 的优缺点与适用边界

- **核心优势**：
    
    - **确定性计算**：无随机性，只要样本固定，计算结果完全唯一（无需像 Bootstrap 那样设置随机数种子或生成大量 Monte Carlo 重抽样）；
        
    - **计算开销极低**：只需计算 $n$ 次统计量；
        
    - **无需总体分布假设**：属于纯数据驱动的非参数方法。
        
- **致命缺陷（不平滑统计量的失效）**：
    
    - **对非平滑（Non-smooth）统计量完全失效**。例如在估计**样本中位数（Median）**或任意分位数时，Jackknife 得到的方差估计是**不一致的（Inconsistent）**，其方差甚至不会随 $n \to \infty$ 收敛。
        
    - _原因_：剔除一个点后，中位数要么完全不变，要么发生跳变，无法满足局部线性可微的假定。
        
- **与 Bootstrap（自助法）的对比**：
    
    - Jackknife 是**确定性的留一重抽样**，可以视为 Bootstrap 的一阶线性近似（Taylor 展开的一阶项）；
        
    - Bootstrap 是**有放回的随机等容量重抽样**，适用范围更广（能处理中位数等非平滑统计量），但在计算效率和确定性上 Jackknife 更有优势。
