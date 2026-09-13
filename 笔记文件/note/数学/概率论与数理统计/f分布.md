# F 分布（Fisher–Snedecor 分布）

$F$ 分布（Fisher–Snedecor 分布）是数理统计三大抽样分布之一，其核心定义是：**两个相互独立的卡方变量，各自除以其自由度后的比值所服从的概率分布。**

## 一、数学定义与自由度

设 $U \sim \chi^2(n_1)$ 与 $V \sim \chi^2(n_2)$ 相互独立，则定义随机变量：

$$F = \frac{U / n_1}{V / n_2}$$

称 $F$ 服从第一自由度为 $n_1$、第二自由度为 $n_2$ 的 $F$ 分布，记作：

$$F \sim F(n_1, n_2)$$

- **$n_1$（分子自由度）**：分子卡方变量的自由度。

- **$n_2$（分母自由度）**：分母卡方变量的自由度。

---

## 二、核心统计性质

### 2.1 倒数性质（互易性）与分位数互易公式

若 $F \sim F(n_1, n_2)$，则其倒数依然服从 $F$ 分布，两个自由度对调：

$$\frac{1}{F} \sim F(n_2, n_1)$$

对应的临界值关系为：$F_{1-\alpha}(n_1, n_2) = \frac{1}{F_{\alpha}(n_2, n_1)}$。

这个公式是 **$F$ 分布的分位数互易公式（倒数分位公式）**。

它的核心作用是：**在查统计用表时，利用右侧分位数直接反求左侧（下侧）分位数，从而避免印刷两套正反向的 $F$ 分布表。**

#### 符号含义拆解

- **$F_\alpha(n_1, n_2)$**：自由度为 $(n_1, n_2)$ 的 $F$ 分布的**上侧 $\alpha$ 分位数（右尾临界值）**。

    其定义为使得右尾面积为 $\alpha$ 的截断点：

    $$P\big(F > F_\alpha(n_1, n_2)\big) = \alpha$$

- **$F_{1-\alpha}(n_1, n_2)$**：上侧 $1-\alpha$ 分位数（等价于**左尾面积为 $\alpha$ 的下侧临界值**）：

    $$P\big(F < F_{1-\alpha}(n_1, n_2)\big) = \alpha$$

- **$\frac{1}{F_\alpha(n_2, n_1)}$**：把第一和第二自由度**颠倒对调**后查到的上侧 $\alpha$ 分位数的**倒数**。

#### 严格推导证明

设随机变量 $X \sim F(n_1, n_2)$。

1. **利用倒数性质**：

    根据 $F$ 分布定义，$X = \frac{U/n_1}{V/n_2}$，其倒数 $Y = \frac{1}{X} = \frac{V/n_2}{U/n_1}$ 服从自由度对调后的 $F$ 分布：

    $$Y = \frac{1}{X} \sim F(n_2, n_1)$$

2. **列出上侧分位数概率定义式**：

    对于变量 $Y$，其右尾面积为 $\alpha$ 的临界点为 $F_\alpha(n_2, n_1)$：

    $$P\big(Y > F_\alpha(n_2, n_1)\big) = \alpha$$

3. **将 $Y = \frac{1}{X}$ 代回**：

    $$P\left(\frac{1}{X} > F_\alpha(n_2, n_1)\right) = \alpha$$

    不等式两边取倒数（因为 $F$ 变量恒大于 0，不等号方向翻转）：

    $$P\left(X < \frac{1}{F_\alpha(n_2, n_1)}\right) = \alpha$$

4. **对比下侧分位数定义**：

    由定义，$P\big(X < F_{1-\alpha}(n_1, n_2)\big) = \alpha$。

    两式对比即可证得：

    $$F_{1-\alpha}(n_1, n_2) = \frac{1}{F_\alpha(n_2, n_1)}$$

#### 查表实例说明

大多数统计学教材后面的附表只给出 $\alpha = 0.05$ 或 $\alpha = 0.01$ 等较小的**右尾数据**，不会印出诸如 $0.95$ 或 $0.99$ 的左尾大表。

**例如：求 $F_{0.95}(10, 5)$**

1. 交换自由度 $(10, 5) \to (5, 10)$；

2. 查表找出上侧 $0.05$ 分位数：$F_{0.05}(5, 10) = 3.33$；

3. 取倒数计算：

    $$F_{0.95}(10, 5) = \frac{1}{F_{0.05}(5, 10)} = \frac{1}{3.33} \approx 0.300$$

### 2.2 期望与方差

利用前面推导[[卡方分布]]负阶矩的公式（$E(V^{-1})$ 与 $E(V^{-2})$），利用分子分母独立性直接相乘可得：

- **数学期望（要求 $n_2 > 2$）**：

    $$E(F) = E\left(\frac{U}{n_1}\right) E\left(\frac{n_2}{V}\right) = 1 \cdot \frac{n_2}{n_2 - 2} = \frac{n_2}{n_2 - 2}$$

    （注意：期望只与分母自由度 $n_2$ 有关，与分子自由度 $n_1$ 无关）。

- **方差（要求 $n_2 > 4$）**：

    $$\mathrm{Var}(F) = \frac{2n_2^2(n_1 + n_2 - 2)}{n_1(n_2 - 2)^2(n_2 - 4)}$$

### 2.3 与 $t$ 分布的关系

若 $T \sim t(n)$，则其平方服从分子自由度为 $1$、分母自由度为 $n$ 的 $F$ 分布：

$$T^2 \sim F(1, n)$$

---

## 三、概率密度函数（PDF）形态

$$f(x) = \frac{\Gamma\left(\frac{n_1+n_2}{2}\right)}{\Gamma\left(\frac{n_1}{2}\right)\Gamma\left(\frac{n_2}{2}\right)} \left(\frac{n_1}{n_2}\right)^{\frac{n_1}{2}} \frac{x^{\frac{n_1}{2}-1}}{\left(1 + \frac{n_1}{n_2}x\right)^{\frac{n_1+n_2}{2}}} \quad (x > 0)$$
![[Pasted image 20260817230909.png]]

- 定义域恒为正数：$x \in (0, +\infty)$。

- 曲线高度不对称，呈现典型的**单峰右偏**形态。

---

## 四、核心应用场景

### 4.1 双正态总体方差比的 F 统计量构造

设有两个相互独立的正态总体：

- 总体 1：$X \sim N(\mu_1, \sigma_1^2)$，样本量为 $n_1$，[[样本均值与样本方差|样本方差]] $S_1^2 = \frac{1}{n_1-1}\sum_{i=1}^{n_1}(X_i-\bar X)^2$
- 总体 2：$Y \sim N(\mu_2, \sigma_2^2)$，样本量为 $n_2$，样本方差 $S_2^2 = \frac{1}{n_2-1}\sum_{j=1}^{n_2}(Y_j-\bar Y)^2$

由正态总体样本方差的抽样分布性质，两个统计量分别服从卡方分布：

$$\frac{(n_1-1)S_1^2}{\sigma_1^2} \sim \chi^2(n_1-1), \qquad \frac{(n_2-1)S_2^2}{\sigma_2^2} \sim \chi^2(n_2-1)$$

两样本独立，故两个卡方变量也相互独立。将它们分别除以自身自由度再作比，即得方差比 $F$ 统计量：

$$F = \frac{\ \frac{(n_1-1)S_1^2}{\sigma_1^2}\big/(n_1-1)\ }{\ \frac{(n_2-1)S_2^2}{\sigma_2^2}\big/(n_2-1)\ } = \frac{S_1^2/\sigma_1^2}{S_2^2/\sigma_2^2} \sim F(n_1-1,\ n_2-1)$$

这是比较两个总体方差的核心工具：当 $\sigma_1^2=\sigma_2^2$ 时，$F$ 退化为两样本方差之比 $S_1^2/S_2^2$。

### 4.2 方差齐性检验（F 检验）

在原假设 $H_0:\ \sigma_1^2=\sigma_2^2$ 下，由 4.1 得检验统计量

$$F = \frac{S_1^2}{S_2^2} \sim F(n_1-1,\ n_2-1)$$

据此构造拒绝域，检验两总体方差是否相等（常作为两样本均值 $t$ 检验的前置步骤）。

### 4.3 方差比 $\sigma_1^2/\sigma_2^2$ 的置信区间

对 $F \sim F(n_1-1,\ n_2-1)$，选取使中间概率为 $1-\alpha$ 的两个上侧分位数（两侧尾各占 $\alpha/2$）：

$$P\Big(F_{1-\alpha/2}(n_1-1,n_2-1) \le F \le F_{\alpha/2}(n_1-1,n_2-1)\Big) = 1-\alpha$$

将 $F=\frac{S_1^2}{S_2^2}\cdot\frac{\sigma_2^2}{\sigma_1^2}$ 代入并变形，解出 $\sigma_1^2/\sigma_2^2$ 的范围：

$$\frac{S_1^2}{S_2^2}\cdot\frac{1}{F_{\alpha/2}(n_1-1,n_2-1)} \le \frac{\sigma_1^2}{\sigma_2^2} \le \frac{S_1^2}{S_2^2}\cdot\frac{1}{F_{1-\alpha/2}(n_1-1,n_2-1)}$$

利用 §2.1 的倒数分位公式 $F_{1-\alpha}(n,m)=\frac{1}{F_\alpha(m,n)}$ 化简边界，得 $\sigma_1^2/\sigma_2^2$ 的 $1-\alpha$ [[总体置信区间|置信区间]]：

$$\left( \frac{S_1^2}{S_2^2}\,F_{1-\alpha/2}(n_2-1,n_1-1),\ \ \frac{S_1^2}{S_2^2}\,F_{\alpha/2}(n_2-1,n_1-1) \right)$$

**实际意义**：若区间包含 $1$，说明两总体方差无显著差异；若整体大于 $1$，说明 $\sigma_1^2$ 显著大于 $\sigma_2^2$；若整体小于 $1$，说明 $\sigma_1^2$ 显著小于 $\sigma_2^2$。

### 4.4 方差齐性下的合并方差（Pooled Variance）

当两总体方差相等（$\sigma_1^2=\sigma_2^2=\sigma^2$，方差齐性）时，可将两样本信息合并，得到对 $\sigma^2$ 更精准的估计，称为**合并方差（联合方差）**。

由卡方分布的可加性（两独立卡方之和仍为卡方，自由度相加）：

$$\frac{(n_1-1)S_1^2}{\sigma^2} \sim \chi^2(n_1-1), \qquad \frac{(n_2-1)S_2^2}{\sigma^2} \sim \chi^2(n_2-1)$$

$$\implies \frac{(n_1-1)S_1^2 + (n_2-1)S_2^2}{\sigma^2} \sim \chi^2(n_1+n_2-2)$$

定义合并方差 $S_p^2$（也记作 $S_\omega^2$）：

$$S_p^2 = \frac{(n_1-1)S_1^2 + (n_2-1)S_2^2}{n_1+n_2-2}$$

- **[[无偏性]]**：$E[S_p^2]=\sigma^2$，是共同方差的无偏估计；
- **更高效**：同时利用两样本波动信息，比单独用任一样本方差更稳定、误差更小。

合并方差主要用于**方差齐性时两总体均值差的 $t$ 检验**（两样本合并方差 $t$ 检验），是两总体均值推断的核心前提。

### 4.5 方差分析（ANOVA）

将数据总波动分解为"组间平方和（MSA）"与"组内平方和（MSE）"，构造 $F = \frac{\mathrm{MSA}}{\mathrm{MSE}}$ 检验多个总体均值是否全相等。

### 4.6 多元线性回归的整体显著性检验

用于检验模型中全部自变量与因变量之间是否存在显著的整体线性关系（$R^2$ 检验）。

---

## 五、期望与方差的严格推导（卡方负阶矩法）

设 $F = \frac{U/n_1}{V/n_2}$，其中 $U \sim \chi^2(n_1), \, V \sim \chi^2(n_2)$ 相互独立。

### 5.1 准备工作：卡方分布的负阶矩通式

根据前面推导出的卡方分布 $\lambda$ 阶矩公式：

$$E(V^\lambda) = \frac{\Gamma\left(\frac{n_2}{2} + \lambda\right)}{\Gamma\left(\frac{n_2}{2}\right)} 2^\lambda \quad \left(\text{收敛条件：} \frac{n_2}{2} + \lambda > 0\right)$$

- **计算 $E(V^{-1})$（取 $\lambda = -1$）**：

    收敛条件为 $\frac{n_2}{2} - 1 > 0 \implies n_2 > 2$。

    利用 Gamma 函数性质 $\Gamma(s) = (s-1)\Gamma(s-1)$，得 $\Gamma\left(\frac{n_2}{2}\right) = \left(\frac{n_2}{2} - 1\right) \Gamma\left(\frac{n_2}{2} - 1\right)$：

    $$E(V^{-1}) = \frac{\Gamma\left(\frac{n_2}{2} - 1\right)}{\left(\frac{n_2}{2} - 1\right)\Gamma\left(\frac{n_2}{2} - 1\right)} \cdot 2^{-1} = \frac{1}{\frac{n_2 - 2}{2}} \cdot \frac{1}{2} = \frac{1}{n_2 - 2}$$

- **计算 $E(V^{-2})$（取 $\lambda = -2$）**：

    收敛条件为 $\frac{n_2}{2} - 2 > 0 \implies n_2 > 4$。

    连续两次降阶展开分母中的 Gamma 函数：

    $$\Gamma\left(\frac{n_2}{2}\right) = \left(\frac{n_2}{2} - 1\right)\left(\frac{n_2}{2} - 2\right) \Gamma\left(\frac{n_2}{2} - 2\right)$$

    代入得：

    $$E(V^{-2}) = \frac{\Gamma\left(\frac{n_2}{2} - 2\right)}{\left(\frac{n_2-2}{2}\right)\left(\frac{n_2-4}{2}\right)\Gamma\left(\frac{n_2}{2} - 2\right)} \cdot 2^{-2} = \frac{4}{(n_2-2)(n_2-4)} \cdot \frac{1}{4} = \frac{1}{(n_2-2)(n_2-4)}$$

### 5.2 期望 $E(F)$ 的求解

由于 $U$ 与 $V$ 相互独立，$\frac{U}{n_1}$ 与 $\frac{n_2}{V}$ 也相互独立：

$$E(F) = E\left(\frac{U}{n_1} \cdot \frac{n_2}{V}\right) = \frac{1}{n_1} E(U) \cdot n_2 E(V^{-1})$$

已知 $E(U) = n_1$，代入 $E(V^{-1}) = \frac{1}{n_2 - 2}$：

$$E(F) = \frac{1}{n_1}(n_1) \cdot n_2 \left(\frac{1}{n_2 - 2}\right) = \frac{n_2}{n_2 - 2} \quad (n_2 > 2)$$

> **核心直观**：
>
> - 为什么期望只和分母自由度 $n_2$ 有关？因为分子项 $\frac{U}{n_1}$ 的期望恒为 $\frac{n_1}{n_1} = 1$（被自身自由度归一化了）；
>
> - 当 $n_2 \to \infty$ 时，$E(F) = \frac{n_2}{n_2 - 2} \to 1$（分母方差彻底稳定时，比值中心收敛于 1）。

### 5.3 方差 $\mathrm{Var}(F)$ 的求解

根据方差计算公式 $\mathrm{Var}(F) = E(F^2) - [E(F)]^2$：

- **计算二阶矩 $E(F^2)$**：

    $$E(F^2) = E\left[ \left(\frac{U}{n_1}\right)^2 \right] \cdot E\left[ \left(\frac{n_2}{V}\right)^2 \right] = \frac{E(U^2)}{n_1^2} \cdot n_2^2 E(V^{-2})$$

    已知 $E(U^2) = \mathrm{Var}(U) + [E(U)]^2 = 2n_1 + n_1^2 = n_1(n_1 + 2)$，代入 $E(V^{-2})$：

    $$E(F^2) = \frac{n_1(n_1 + 2)}{n_1^2} \cdot \frac{n_2^2}{(n_2-2)(n_2-4)} = \frac{(n_1 + 2) n_2^2}{n_1(n_2-2)(n_2-4)}$$

- **相减化简方差**：

    $$\mathrm{Var}(F) = \frac{(n_1 + 2) n_2^2}{n_1(n_2-2)(n_2-4)} - \left(\frac{n_2}{n_2-2}\right)^2 = \frac{n_2^2}{(n_2-2)^2} \left[ \frac{(n_1+2)(n_2-2)}{n_1(n_2-4)} - 1 \right]$$

    通分括号内部：

    $$\frac{(n_1n_2 - 2n_1 + 2n_2 - 4) - (n_1n_2 - 4n_1)}{n_1(n_2-4)} = \frac{2n_1 + 2n_2 - 4}{n_1(n_2-4)} = \frac{2(n_1 + n_2 - 2)}{n_1(n_2-4)}$$

    乘回外部因子，得出最终结果：

    $$\mathrm{Var}(F) = \frac{2n_2^2(n_1 + n_2 - 2)}{n_1(n_2-2)^2(n_2-4)} \quad (n_2 > 4)$$

---

## 六、与 $t$ 分布的内在联系（$T^2 \sim F(1, n)$）

### 6.1 从定义直接对齐

根据 Student's $t$ 分布定义，若 $Z \sim N(0, 1)$，$V \sim \chi^2(n)$ 且二者相互独立，则：

$$T = \frac{Z}{\sqrt{V / n}} \sim t(n)$$

两边同时平方：

$$T^2 = \frac{Z^2}{V / n} = \frac{Z^2 / 1}{V / n}$$

- 分子部分：$Z \sim N(0, 1) \implies U = Z^2 \sim \chi^2(1)$（自由度为 $1$ 的卡方变量）；

- 分母部分：$V \sim \chi^2(n)$（自由度为 $n$ 的卡方变量）；

- 独立性：$Z$ 与 $V$ 独立 $\implies Z^2$ 与 $V$ 独立。

对照 $F$ 分布的定义式 $F = \frac{\chi^2(n_1)/n_1}{\chi^2(n_2)/n_2}$，取 $n_1 = 1, \, n_2 = n$：

$$T^2 \sim F(1, n)$$

### 6.2 统计学意义

- **单样本 / 双样本 $t$ 检验与单因素方差分析（ANOVA）等价性**：当只有两组数据对比时，做双侧 $t$ 检验得到的 $t$ 统计量的平方，正好精确等于两组做方差分析算出的 $F$ 统计量。

- **分位数对应关系**：$t_{1-\alpha/2}^2(n) = F_{1-\alpha}(1, n)$。

---

## 七、概率密度函数的形态与演变分析

$$f(x) = C \cdot \frac{x^{\frac{n_1}{2} - 1}}{\left(1 + \frac{n_1}{n_2}x\right)^{\frac{n_1+n_2}{2}}} \quad (x > 0)$$

其曲线几何形态由**分子自由度 $n_1$** 和**分母自由度 $n_2$** 共同主导：

### 7.1 原点 $x \to 0^+$ 处的形态（由分子幂次 $\frac{n_1}{2} - 1$ 决定）

- **$n_1 = 1$**：此时幂次为 $x^{-\frac{1}{2}} = \frac{1}{\sqrt{x}}$。当 $x \to 0$ 时，**$f(x) \to +\infty$（在原点处存在垂直渐近线，呈反 L 形无限单调递减）**。

- **$n_1 = 2$**：幂次为 $x^0 = 1$。原点处 $f(0^+) = 1$，**曲线从纵轴截距处单调平滑下降**。

- **$n_1 > 2$**：幂次为正数。$f(0) = 0$，**曲线从原点出发，先上升后下降，形成经典的单峰右偏钟形**。

### 7.2 峰值（众数 Mode）位置

对密度函数求导令 $f'(x) = 0$，可解得峰值出现在：

$$x_{\text{mode}} = \frac{n_1 - 2}{n_1} \cdot \frac{n_2}{n_2 + 2} \quad (\text{当 } n_1 > 2 \text{ 时})$$

由于 $\frac{n_1 - 2}{n_1} < 1$ 且 $\frac{n_2}{n_2 + 2} < 1$，峰值恒在 $1$ 的左侧。

### 7.3 右侧拖尾（重尾性质）

当 $x \to +\infty$ 时，$f(x) \sim x^{\left(\frac{n_1}{2}-1\right) - \left(\frac{n_1+n_2}{2}\right)} = x^{-\left(\frac{n_2}{2} + 1\right)}$。

右尾以幂律衰减（多项式阶衰减）而非指数衰减，这直接解释了为什么分母自由度 $n_2$ 过小时（$n_2 \le 2$ 或 $n_2 \le 4$）高阶矩的积分会发散。

---

## 八、方差 $\mathrm{Var}(F)$ 的另两种推导思路

### 8.1 思路一：二阶矩法拆解

设 $F = \frac{Z_1 / m}{Z_2 / n}$，其中 $Z_1 \sim \chi^2(m)$， $Z_2 \sim \chi^2(n)$ 相互独立。

$$E(F^2) = E\left[ \left(\frac{Z_1}{m}\right)^2 \left(\frac{n}{Z_2}\right)^2 \right] = \frac{n^2}{m^2} E(Z_1^2) E(Z_2^{-2})$$

- **$E(Z_1^2)$**：

    $$E(Z_1^2) = \mathrm{Var}(Z_1) + [E(Z_1)]^2 = 2m + m^2 = m(m+2)$$

- **$E(Z_2^{-2})$**：

    利用前面推导的卡方负二阶矩（要求 $n > 4$）：

    $$E(Z_2^{-2}) = \frac{1}{(n-2)(n-4)}$$

- 代回即得 $E(F^2)$，再减去 $[E(F)]^2 = \left(\frac{n}{n-2}\right)^2$ 得到方差。

### 8.2 思路二：全方差公式法（重点推导）

全方差公式为：

$$\mathrm{Var}(F) = E\big(\mathrm{Var}(F \mid Z_2)\big) + \mathrm{Var}\big(E(F \mid Z_2)\big)$$

**1. 在给定 $Z_2$ 条件下的条件方差与[[条件期望与条件方差|条件期望]]**

当给定 $Z_2$ 时，$Z_2$ 被视为常数：

- **条件方差**：

    $$\mathrm{Var}(F \mid Z_2) = \mathrm{Var}\left( \frac{n}{m Z_2} Z_1 \,\middle|\, Z_2 \right) = \left(\frac{n}{m Z_2}\right)^2 \mathrm{Var}(Z_1) = \frac{n^2}{m^2 Z_2^2} \cdot (2m) = \frac{2n^2}{m} \cdot \frac{1}{Z_2^2}$$

- **条件期望**：

    $$E(F \mid Z_2) = E\left( \frac{n}{m Z_2} Z_1 \,\middle|\, Z_2 \right) = \frac{n}{m Z_2} E(Z_1) = \frac{n}{m Z_2} \cdot m = \frac{n}{Z_2}$$

**2. 将两项代入全方差公式并取期望/方差**

- **第一部分（期望项）**：

    $$E\big(\mathrm{Var}(F \mid Z_2)\big) = \frac{2n^2}{m} E(Z_2^{-2}) = \frac{2n^2}{m(n-2)(n-4)}$$

- **第二部分（方差项）**：

    $$\mathrm{Var}\big(E(F \mid Z_2)\big) = \mathrm{Var}\left(\frac{n}{Z_2}\right) = n^2 \mathrm{Var}(Z_2^{-1}) = n^2 \Big[ E(Z_2^{-2}) - \big(E[Z_2^{-1}]\big)^2 \Big]$$

    代入 $E(Z_2^{-1}) = \frac{1}{n-2}$ 和 $E(Z_2^{-2}) = \frac{1}{(n-2)(n-4)}$：

    $$\mathrm{Var}\big(E(F \mid Z_2)\big) = n^2 \left[ \frac{1}{(n-2)(n-4)} - \frac{1}{(n-2)^2} \right] = \frac{n^2}{(n-2)^2(n-4)} \big[ (n-2) - (n-4) \big] = \frac{2n^2}{(n-2)^2(n-4)}$$

**3. 两项相加通分**

$$\mathrm{Var}(F) = \frac{2n^2}{m(n-2)(n-4)} + \frac{2n^2}{(n-2)^2(n-4)}$$

提取公因式 $\frac{2n^2}{(n-2)^2(n-4)}$：

$$\mathrm{Var}(F) = \frac{2n^2}{(n-2)^2(n-4)} \left( \frac{n-2}{m} + 1 \right) = \frac{2n^2(m + n - 2)}{m(n-2)^2(n-4)}$$

（此结果与将分子自由度记为 $n_1 = m$、分母自由度记为 $n_2 = n$ 的标准方差公式完全一致）。
