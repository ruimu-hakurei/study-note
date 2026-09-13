# t 分布（Student's t-distribution）

$t$ 分布（Student's $t$-distribution）是数理统计三大抽样分布之一，其核心应用场景是：**在正态总体方差未知的情况下，用样本标准差代替总体标准差来估计均值或进行假设检验。**

## 一、数学定义与构造机制

设有两个**相互独立**的随机变量：

- $X \sim N(0, 1)$（标准[[正态分布]]）；

- $Y \sim \chi^2(n)$（自由度为 $n$ 的[[卡方分布]]）。

定义随机变量：

$$T = \frac{X}{\sqrt{Y / n}}$$

则称 $T$ 服从自由度为 $n$ 的 $t$ 分布，记作：

$$T \sim t(n)$$

- **物理直观**：分子是标准正态的"中心测量"，分母是卡方除以自由度开根号，用来对未知的尺度波动进行归一化。

---

## 二、概率密度函数（PDF）与曲线形态

### 2.1 概率密度函数

自由度为 $n$ 的 $t$ 分布概率密度函数为：

$$f(t) = \frac{\Gamma\left(\frac{n+1}{2}\right)}{\sqrt{n\pi} \, \Gamma\left(\frac{n}{2}\right)} \left( 1 + \frac{t^2}{n} \right)^{-\frac{n+1}{2}} \quad (-\infty < t < +\infty)$$

### 2.2 概率密度函数的推导（雅可比行列式法）

推导自由度为 $n$ 的 $t$ 分布概率密度函数，采用二维联合概率密度的变量代换（雅可比行列式法）并对辅助变量积分求边际密度。

#### 第一步：写出独立变量的联合概率密度

设随机变量 $X$ 与 $Y$ 相互独立：

- $X \sim N(0, 1)$，其概率密度函数为：

    $$f_X(x) = \frac{1}{\sqrt{2\pi}} e^{-\frac{x^2}{2}} \quad (-\infty < x < +\infty)$$

- $Y \sim \chi^2(n)$，其概率密度函数为：

    $$f_Y(y) = \frac{1}{2^{\frac{n}{2}}\Gamma\left(\frac{n}{2}\right)} y^{\frac{n}{2}-1} e^{-\frac{y}{2}} \quad (y > 0)$$

由独立性，$(X, Y)$ 的联合概率密度函数为二者之积：

$$f_{X,Y}(x, y) = f_X(x) f_Y(y) = \frac{1}{\sqrt{2\pi} 2^{\frac{n}{2}} \Gamma\left(\frac{n}{2}\right)} y^{\frac{n}{2}-1} e^{-\frac{x^2+y}{2}} \quad (-\infty < x < +\infty, \, y > 0)$$

#### 第二步：二维变量替换与雅可比行列式

根据 $t$ 分布的定义，令目标变量 $T$ 与辅助变量 $U$ 为：

$$\begin{cases} T = \frac{X}{\sqrt{Y/n}} \\ U = Y \end{cases}$$

反解原变量 $(X, Y)$：

$$\begin{cases} X = T \sqrt{\frac{U}{n}} = T n^{-\frac{1}{2}} U^{\frac{1}{2}} \\ Y = U \end{cases}$$

计算从 $(T, U)$ 到 $(X, Y)$ 的雅可比（Jacobian）行列式：

$$J = \det \begin{pmatrix} \frac{\partial x}{\partial t} & \frac{\partial x}{\partial u} \\ \frac{\partial y}{\partial t} & \frac{\partial y}{\partial u} \end{pmatrix} = \det \begin{pmatrix} \sqrt{\frac{u}{n}} & \frac{t}{2\sqrt{n u}} \\ 0 & 1 \end{pmatrix} = \sqrt{\frac{u}{n}}$$

变换后的联合概率密度函数 $f_{T, U}(t, u)$ 为：

$$f_{T, U}(t, u) = f_{X, Y}\left( t\sqrt{\frac{u}{n}}, \, u \right) \cdot |J|$$

将 $x = t\sqrt{\frac{u}{n}}$ 及 $y = u$ 代入指数项：

$$\frac{x^2 + y}{2} = \frac{\frac{t^2 u}{n} + u}{2} = \frac{u}{2}\left(1 + \frac{t^2}{n}\right)$$

整理得到 $(T, U)$ 的联合密度：

$$f_{T, U}(t, u) = \frac{1}{\sqrt{2\pi} 2^{\frac{n}{2}} \Gamma\left(\frac{n}{2}\right)} u^{\frac{n}{2}-1} e^{-\frac{u}{2}\left(1 + \frac{t^2}{n}\right)} \cdot \frac{u^{\frac{1}{2}}}{\sqrt{n}}$$

$$= \frac{1}{\sqrt{2n\pi} 2^{\frac{n}{2}} \Gamma\left(\frac{n}{2}\right)} u^{\frac{n+1}{2}-1} e^{-\frac{u}{2}\left(1 + \frac{t^2}{n}\right)} \quad (-\infty < t < +\infty, \, u > 0)$$

#### 第三步：对辅助变量 $u$ 积分求边际密度

对 $u$ 在区间 $(0, +\infty)$ 上进行积分以获得 $T$ 的边际概率密度 $f_T(t)$：

$$f_T(t) = \int_0^{+\infty} f_{T, U}(t, u) \, du = \frac{1}{\sqrt{2n\pi} 2^{\frac{n}{2}} \Gamma\left(\frac{n}{2}\right)} \int_0^{+\infty} u^{\frac{n+1}{2}-1} e^{-\frac{u}{2}\left(1 + \frac{t^2}{n}\right)} \, du$$

令换元变量：

$$v = \frac{u}{2}\left(1 + \frac{t^2}{n}\right) \implies u = \frac{2v}{1 + \frac{t^2}{n}}, \quad du = \frac{2 \, dv}{1 + \frac{t^2}{n}}$$

代入积分式：

$$\int_0^{+\infty} u^{\frac{n+1}{2}-1} e^{-\frac{u}{2}\left(1 + \frac{t^2}{n}\right)} \, du = \int_0^{+\infty} \left( \frac{2v}{1 + \frac{t^2}{n}} \right)^{\frac{n+1}{2}-1} e^{-v} \left( \frac{2}{1 + \frac{t^2}{n}} \right) dv$$

$$= \frac{2^{\frac{n+1}{2}}}{\left(1 + \frac{t^2}{n}\right)^{\frac{n+1}{2}}} \int_0^{+\infty} v^{\frac{n+1}{2}-1} e^{-v} \, dv$$

根据 Gamma 函数定义 $\int_0^{+\infty} v^{s-1} e^{-v} dv = \Gamma(s)$，此处积分值即为 $\Gamma\left(\frac{n+1}{2}\right)$：

$$= \frac{2^{\frac{n+1}{2}} \Gamma\left(\frac{n+1}{2}\right)}{\left(1 + \frac{t^2}{n}\right)^{\frac{n+1}{2}}}$$

#### 第四步：化简系数得到最终密度

将积分结果代回 $f_T(t)$：

$$f_T(t) = \frac{1}{\sqrt{2n\pi} \, 2^{\frac{n}{2}} \Gamma\left(\frac{n}{2}\right)} \cdot \frac{2^{\frac{n+1}{2}} \Gamma\left(\frac{n+1}{2}\right)}{\left(1 + \frac{t^2}{n}\right)^{\frac{n+1}{2}}}$$

化简常数项中的 2 的幂次：

$$\frac{2^{\frac{n+1}{2}}}{\sqrt{2} \cdot 2^{\frac{n}{2}}} = \frac{2^{\frac{n+1}{2}}}{2^{\frac{n+1}{2}}} = 1$$

化简后得到自由度为 $n$ 的 Student's $t$ 分布概率密度函数：

$$f_T(t) = \frac{\Gamma\left(\frac{n+1}{2}\right)}{\sqrt{n\pi} \, \Gamma\left(\frac{n}{2}\right)} \left( 1 + \frac{t^2}{n} \right)^{-\frac{n+1}{2}} \quad (-\infty < t < +\infty)$$

### 2.3 曲线形态特征

![[Student-t分布概率密度函数.png|600]]

*不同自由度 $n=1,2,5,10,30$ 的 $t$ 分布密度曲线（黑虚线为标准正态 $N(0,1)$）*

- **对称性**：关于 $t = 0$ 严格对称，为钟形曲线。

- **重尾（Fat-tailed）特征**：

    相比于标准正态分布的指数衰减 $e^{-t^2/2}$，$t$ 分布的尾部是**幂律衰减 $\sim t^{-(n+1)}$**。因此，它在两端的概率尾部比正态分布更厚，中心峰值比正态分布更矮更平缓（反映了用[[样本均值与样本方差|样本方差]]估计总体方差时引入的额外不确定性）。

- **渐近正态性**：

    根据极限 $\lim_{n \to \infty} \left(1 + \frac{t^2}{n}\right)^{-\frac{n+1}{2}} = e^{-\frac{t^2}{2}}$，当自由度 $n \to \infty$ 时：

    $$t(n) \xrightarrow{d} N(0, 1)$$

    通常当 $n > 30$ 时，$t$ 分布与标准正态分布已非常接近。

---

## 三、矩性质（期望与方差推导）

利用独立性 $T = X \cdot \sqrt{n} \cdot Y^{-\frac{1}{2}}$：

### 3.1 数学期望（要求 $n > 1$）

$$E(T) = \sqrt{n} \cdot E(X) \cdot E\left(Y^{-\frac{1}{2}}\right)$$

由于 $X \sim N(0, 1)$ 的 $E(X) = 0$：

$$E(T) = 0 \quad (n > 1)$$

- 注意：当 $n = 1$ 时（即柯西分布 $\mathrm{Cauchy}(0,1)$），积分绝对发散，期望不存在。

### 3.2 方差（要求 $n > 2$）

因为 $E(T) = 0$，所以 $\mathrm{Var}(T) = E(T^2)$：

$$\mathrm{Var}(T) = E\left( \frac{X^2}{Y/n} \right) = n \cdot E(X^2) \cdot E(Y^{-1})$$

- $E(X^2) = 1$；

- 由卡方负一阶矩公式 $E(Y^{-1}) = \frac{1}{n-2}$（要求 $n > 2$）；

    $$\mathrm{Var}(T) = n \cdot 1 \cdot \frac{1}{n-2} = \frac{n}{n-2} \quad (n > 2)$$

> **观察**：因为 $\frac{n}{n-2} > 1$，所以 $t$ 分布的方差恒大于标准正态分布的方差（$1$）。当 $n \to \infty$ 时，$\frac{n}{n-2} \to 1$。

---

## 四、核心统计应用：单正态总体均值检验

设总体 $X \sim N(\mu, \sigma^2)$，抽取容量为 $n$ 的样本，样本均值为 $\bar{X}$，样本方差为 $S^2 = \frac{1}{n-1}\sum_{i=1}^n (X_i - \bar{X})^2$。

1. **构造基础量**：

    - 均值标准化：$\frac{\bar{X} - \mu}{\sigma / \sqrt{n}} \sim N(0, 1)$

    - 样本方差卡方化：$\frac{(n-1)S^2}{\sigma^2} \sim \chi^2(n-1)$

    - 且由抽样理论（Fisher 引理），$\bar{X}$ 与 $S^2$ 相互独立。

2. **消去未知参数 $\sigma$**：

    将二者代入 $t$ 分布定义式：

    $$T = \frac{\frac{\bar{X} - \mu}{\sigma / \sqrt{n}}}{\sqrt{\frac{(n-1)S^2 / \sigma^2}{n-1}}} = \frac{\bar{X} - \mu}{S / \sqrt{n}} \sim t(n-1)$$

这使得我们在实际工程和实验中**完全不需要知道真实方差 $\sigma^2$**，仅凭样本数据就能构造均值的精确[[总体置信区间|置信区间]]和显著性检验（$t$ 检验）。

## 五、t 统计量的逐行推导详解（单正态均值检验）

> 本节是第四节「核心统计应用」的**详细版推导**：从零把 $t$ 统计量一步步构造出来。

### 5.1 前置预备知识

推导需要用到三个核心结论，都是之前讲过的内容：

#### t 分布的定义

若随机变量满足：

- $Z \sim N(0,1)$（标准正态分布）
- $W \sim \chi^2(k)$（自由度为 $k$ 的卡方分布）
- $Z$ 与 $W$ 相互独立

则构造的统计量

$$T = \frac{Z}{\sqrt{\dfrac{W}{k}}}$$

服从**自由度为 $k$ 的 $t$ 分布**，记作 $T \sim t(k)$。

#### 正态总体的三个核心抽样结论

设 $X_1,\dots,X_n$ 是来自正态总体 $N(\mu,\sigma^2)$ 的独立样本，则：

1. **样本均值的标准化**：$\frac{\sqrt{n}\,(\bar{X}-\mu)}{\sigma} \sim N(0,1)$
2. **样本方差的卡方分布**：$\frac{(n-1)S^2}{\sigma^2} \sim \chi^2(n-1)$
3. **独立性**：正态总体下，样本均值 $\bar{X}$ 与样本方差 $S^2$ 相互独立。

### 5.2 逐行推导

我们从左到右一步步拆解。

#### 第 1 步：代数变形 —— 分子分母同除以 $\sigma$

$$\frac{\sqrt{n}\,(\bar{X}-\mu)}{S} = \frac{\dfrac{\sqrt{n}\,(\bar{X}-\mu)}{\sigma}}{\sqrt{\dfrac{S^2}{\sigma^2}}}$$

- **操作**：对整个分式的分子、分母同时除以 $\sigma$。注意分母 $S$ 除以 $\sigma$ 后放进根号里，就变成 $S^2/\sigma^2$。
- **目的**：人为构造出 $t$ 分布定义的形式——让分子变成标准正态量，分母变成卡方量的开方。

#### 第 2 步：替换为对应分布

$$= \frac{N(0,1)}{\sqrt{\dfrac{\chi^2(n-1)}{n-1}}}$$

我们分别看分子和分母：

1. **分子**：$\dfrac{\sqrt{n}\,(\bar{X}-\mu)}{\sigma}$，根据前置结论 1，它恰好服从标准正态分布 $N(0,1)$，对应 $t$ 分布定义里的 $Z$。
2. **分母**：我们从样本方差的卡方结论出发变形：$\frac{(n-1)S^2}{\sigma^2} \sim \chi^2(n-1)$，两边同时除以 $n-1$，就得到 $\frac{S^2}{\sigma^2} = \frac{\chi^2(n-1)}{n-1}$，两边开根号后，恰好就是分母里的 $\sqrt{S^2/\sigma^2}$，对应 $t$ 分布定义里的 $\sqrt{W/k}$。

#### 第 3 步：套用 $t$ 分布定义

$$\sim t(n-1)$$

验证 $t$ 分布的三个条件：

- 分子是标准正态分布
- 分母是「卡方变量除以自由度」的平方根
- 由 $\bar{X}$ 与 $S^2$ 相互独立，可知分子和分母相互独立

完全满足 $t$ 分布的定义，因此整体服从自由度为 $n-1$ 的 $t$ 分布。

### 5.3 补充说明

1. **自由度为什么是 $n-1$**：$t$ 分布的自由度由分母里卡方分布的自由度决定。因为样本方差的卡方自由度是 $n-1$（用样本均值估计总体均值，消耗了 1 个自由度），所以最终 $t$ 分布的自由度也是 $n-1$。
2. **和 $Z$ 统计量的区别**：
    - 当总体标准差 $\sigma$ **已知**时，用 $\dfrac{\sqrt{n}(\bar{X}-\mu)}{\sigma}$，服从标准正态分布，对应 $Z$ 检验。
    - 当总体标准差 $\sigma$ **未知**时，用样本标准差 $S$ 替代，得到 $\dfrac{\sqrt{n}(\bar{X}-\mu)}{S}$，服从 $t$ 分布，对应 $t$ 检验。样本量越大，$t$ 分布越接近标准正态分布。
3. **适用前提**：这个结论**精确成立**的前提是总体服从正态分布。对于非正态总体，大样本下可以近似使用。
