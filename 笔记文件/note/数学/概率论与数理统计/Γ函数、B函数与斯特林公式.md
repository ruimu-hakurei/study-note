# $\Gamma$ 函数、$B$ 函数与斯特林公式

> 伽玛函数是"连续的阶乘"，贝塔函数是概率分布的"万能归一化分母"。两者通过 $B(p,q) = \frac{\Gamma(p)\Gamma(q)}{\Gamma(p+q)}$ 紧密相连，斯特林公式和沃利斯公式则揭示了阶乘与 $\pi$ 的深层联系。

---

## 1. 伽玛函数 $\Gamma(\alpha)$

### 定义

$$\Gamma(\alpha) = \int_0^{+\infty} x^{\alpha-1} e^{-x} dx \qquad (\alpha > 0)$$

被积函数 $x^{\alpha-1} e^{-x}$ 是一场"三方拔河"——多项式 $x^{\alpha-1}$ 想把面积拉向无穷，指数 $e^{-x}$ 以碾压性的速度把它拉回零。最终指数获胜，积分收敛。

### 基本性质

---

#### 递推公式：$\Gamma(\alpha+1) = \alpha\Gamma(\alpha)$

**工具**：分部积分法 $\int_a^b u\,dv = [uv]_a^b - \int_a^b v\,du$

写出 $\Gamma(\alpha+1)$ 的积分表示：

$$\Gamma(\alpha+1) = \int_0^\infty x^{(\alpha+1)-1} e^{-x} dx = \int_0^\infty x^\alpha e^{-x} dx$$

设定 $u$ 和 $dv$：

$$u = x^\alpha \quad \Rightarrow \quad du = \alpha x^{\alpha-1} dx$$

$$dv = e^{-x} dx \quad \Rightarrow \quad v = \int e^{-x} dx = -e^{-x}$$

代入分部积分公式：

$$\Gamma(\alpha+1) = \left[ u \cdot v \right]_0^\infty - \int_0^\infty v \cdot du$$

$$= \left[ x^\alpha \cdot (-e^{-x}) \right]_0^\infty - \int_0^\infty (-e^{-x}) \cdot \alpha x^{\alpha-1} dx$$

$$= \left[ -x^\alpha e^{-x} \right]_0^\infty + \alpha \int_0^\infty x^{\alpha-1} e^{-x} dx$$

计算边界项：

- 下界 $x = 0$：$\alpha > 0$，故 $0^\alpha = 0$，$e^0 = 1$，$0 \cdot 1 = 0$
- 上界 $x \to \infty$：$\lim_{x\to\infty} \frac{x^\alpha}{e^x} = 0$（洛必达法则，分子反复求导 $\alpha$ 次后为常数，分母仍为 $e^x$，指数碾压多项式）

所以 $\left[ -x^\alpha e^{-x} \right]_0^\infty = 0 - 0 = 0$。于是：

$$\Gamma(\alpha+1) = 0 + \alpha \int_0^\infty x^{\alpha-1} e^{-x} dx = \alpha\,\Gamma(\alpha)$$

**验证基态并推出阶乘**：

$$\Gamma(1) = \int_0^\infty x^{0} e^{-x} dx = \int_0^\infty e^{-x} dx = \left[ -e^{-x} \right]_0^\infty = 0 - (-1) = 1$$

$$\Gamma(2) = 1 \cdot \Gamma(1) = 1, \quad \Gamma(3) = 2 \cdot \Gamma(2) = 2, \quad \Gamma(4) = 3 \cdot \Gamma(3) = 6$$

$$\Gamma(n) = (n-1)(n-2)\cdots 2 \cdot 1 \cdot \Gamma(1) = (n-1)!$$

| $\alpha$ | 1 | 2 | 3 | 4 | $\frac{1}{2}$ |
|------|------|------|------|------|------|
| $\Gamma(\alpha)$ | 1 | 1 | 2 | 6 | $\sqrt{\pi}$ |
| 阶乘视角 | 0! | 1! | 2! | 3! | $(-\frac{1}{2})!$ |

---

#### $\Gamma(1/2) = \sqrt{\pi}$

$$\Gamma\!\left(\frac{1}{2}\right) = \int_0^\infty x^{-1/2} e^{-x} dx$$

做变量代换 $x = u^2$，则 $dx = 2u\,du$，$x^{-1/2} = (u^2)^{-1/2} = u^{-1} = 1/u$。当 $x$ 从 $0 \to \infty$ 时，$u$ 也从 $0 \to \infty$：

$$\Gamma\!\left(\frac{1}{2}\right) = \int_0^\infty \frac{1}{u} \cdot e^{-u^2} \cdot 2u\,du = 2\int_0^\infty e^{-u^2} du$$

由于 $e^{-u^2}$ 是偶函数，它在 $[0, \infty)$ 上的面积恰好是整个实轴 $(-\infty, \infty)$ 上面积的一半：

$$\Gamma\!\left(\frac{1}{2}\right) = 2 \cdot \frac{1}{2} \int_{-\infty}^\infty e^{-u^2} du = \int_{-\infty}^\infty e^{-u^2} du$$

后面这个积分正是高斯积分，其值为 $\sqrt{\pi}$。所以：

$$\Gamma\!\left(\frac{1}{2}\right) = \sqrt{\pi}$$

> 半整数的"阶乘"居然跟圆周率绑在一起——这是数学史上最震撼的发现之一。

---

### 构造、延拓与唯一性

---

#### 反射公式：$\Gamma(z)\Gamma(1-z) = \dfrac{\pi}{\sin(\pi z)}$

> 此证明需用到第 2 节贝塔函数的桥梁公式 $B(p,q)=\frac{\Gamma(p)\Gamma(q)}{\Gamma(p+q)}$，该公式本身独立于反射公式，不存在循环论证。

**第一步**：利用贝塔函数的桥梁公式 $B(p,q) = \frac{\Gamma(p)\Gamma(q)}{\Gamma(p+q)}$，令 $p = z$，$q = 1-z$：

$$B(z, 1-z) = \frac{\Gamma(z)\Gamma(1-z)}{\Gamma(z + 1 - z)} = \frac{\Gamma(z)\Gamma(1-z)}{\Gamma(1)}$$

因为 $\Gamma(1) = 1$：

$$B(z, 1-z) = \Gamma(z)\Gamma(1-z) \qquad(1)$$

**第二步**：利用贝塔函数的有理积分形式 $B(p,q) = \int_0^\infty \frac{u^{p-1}}{(1+u)^{p+q}} du$。代入 $p = z$，$q = 1-z$：

$$B(z, 1-z) = \int_0^\infty \frac{u^{z-1}}{(1+u)^{z + (1-z)}} du = \int_0^\infty \frac{u^{z-1}}{1+u} du \qquad(2)$$

联立 (1) 和 (2)：

$$\Gamma(z)\Gamma(1-z) = \int_0^\infty \frac{u^{z-1}}{1+u} du$$

**第三步**：复变留数定理求积分。考察复平面上的积分 $\oint_C \frac{w^{z-1}}{1+w} dw$，其中 $C$ 是钥匙孔回路（正实轴上沿 → 绕原点小圆 → 正实轴下沿 → 大圆）。

奇点：$w = -1 = e^{i\pi}$，留数 $\text{Res}(e^{i\pi}) = \lim_{w \to e^{i\pi}} (w - e^{i\pi})\frac{w^{z-1}}{1+w} = (e^{i\pi})^{z-1} = e^{i\pi(z-1)}$

由留数定理，正实轴上沿和下沿的积分关系（下沿绕支点后相位差 $2\pi i(z-1)$）：

$$\int_0^\infty \frac{u^{z-1}}{1+u} du - e^{2\pi i(z-1)} \int_0^\infty \frac{u^{z-1}}{1+u} du = 2\pi i \cdot e^{i\pi(z-1)}$$

左边提取公因子 $(1 - e^{2\pi i z})$，利用 $1 - e^{2\pi i z} = e^{i\pi z}(e^{-i\pi z} - e^{i\pi z}) = e^{i\pi z} \cdot (-2i\sin\pi z)$：

$$-2i\sin(\pi z) \cdot e^{i\pi z} \int_0^\infty \frac{u^{z-1}}{1+u} du = 2\pi i \cdot e^{i\pi z} \cdot (-1)$$

两边消去 $2i e^{i\pi z}$：

$$-\sin(\pi z) \int_0^\infty \frac{u^{z-1}}{1+u} du = -\pi$$

$$\int_0^\infty \frac{u^{z-1}}{1+u} du = \frac{\pi}{\sin(\pi z)}$$

$$\boxed{\Gamma(z)\Gamma(1-z) = \frac{\pi}{\sin(\pi z)}}$$

代入 $z = 1/2$ 自洽验证：$\Gamma(1/2)^2 = \pi / \sin(\pi/2) = \pi \Rightarrow \Gamma(1/2) = \sqrt{\pi}$。

当 $z$ 趋近于负整数时 $\sin(\pi z) \to 0$，$\Gamma(z) \to \infty$——伽玛函数在 $0, -1, -2, \dots$ 处有一阶极点。

---

#### 欧拉的原始构造

欧拉的目标：找一个连续函数满足 $f(\alpha+1) = \alpha f(\alpha)$ 且 $f(n+1) = n!$。

**Step 1 — 构造有限积分**

$$I_n = \int_0^n x^{\alpha-1} \left(1 - \frac{x}{n}\right)^n dx$$

其中 $n$ 是正整数。积分上限是 $n$（有限），被积函数 $(1 - x/n)^n$ 是多项式。

**Step 2 — 变量代换 $x = ny$**

$x = ny$，$dx = n\,dy$，$x^{\alpha-1} = (ny)^{\alpha-1} = n^{\alpha-1} y^{\alpha-1}$。$x$ 从 $0 \to n$ 时 $y$ 从 $0 \to 1$：

$$I_n = \int_0^1 (ny)^{\alpha-1} (1 - y)^n \cdot n\,dy = n^\alpha \int_0^1 y^{\alpha-1} (1 - y)^n dy$$

**Step 3 — 第一次分部积分**

令 $u = (1-y)^n$，$dv = y^{\alpha-1} dy$：

$$du = n(1-y)^{n-1} \cdot (-1)\,dy = -n(1-y)^{n-1} dy, \quad v = \frac{y^\alpha}{\alpha}$$

$$\int_0^1 y^{\alpha-1} (1-y)^n dy = \left[(1-y)^n \frac{y^\alpha}{\alpha}\right]_0^1 - \int_0^1 \frac{y^\alpha}{\alpha} \cdot \left(-n(1-y)^{n-1}\right) dy$$

边界项：$y=1$ 时 $(1-1)^n = 0$，$y=0$ 时 $0^\alpha = 0$ → 边界为 $0$。负负得正：

$$= 0 + \frac{n}{\alpha} \int_0^1 y^\alpha (1-y)^{n-1} dy$$

**Step 4 — 观察规律**

第一次分部积分后，$(1-y)$ 的指数从 $n$ 降到 $n-1$，$y$ 的指数从 $\alpha-1$ 升到 $\alpha$。第二次分部积分（令 $u = (1-y)^{n-1}$，$dv = y^\alpha dy$）同理：

$$\frac{n}{\alpha} \cdot \frac{n-1}{\alpha+1} \int_0^1 y^{\alpha+1} (1-y)^{n-2} dy$$

重复 $n$ 次直到 $(1-y)$ 的指数降到 $0$：

$$I_n = n^\alpha \cdot \frac{n}{\alpha} \cdot \frac{n-1}{\alpha+1} \cdot \frac{n-2}{\alpha+2} \cdots \frac{1}{\alpha+n-1} \int_0^1 y^{\alpha+n-1} dy$$

最后积分 $\int_0^1 y^{\alpha+n-1} dy = \frac{1}{\alpha+n}$。分子 $n^\alpha \cdot n \cdot (n-1) \cdots 1 = n^\alpha \cdot n!$，分母 $\alpha(\alpha+1)\cdots(\alpha+n)$：

$$I_n = \frac{n! \cdot n^\alpha}{\alpha(\alpha+1)(\alpha+2)\cdots(\alpha+n)}$$

**Step 5 — 取极限 $n \to \infty$**

左边 $\lim_{n\to\infty} I_n = \lim_{n\to\infty} \int_0^n x^{\alpha-1}(1 - x/n)^n dx$。利用 $\lim_{n\to\infty}(1 - x/n)^n = e^{-x}$，积分上限 $n \to \infty$，化为 $\int_0^\infty x^{\alpha-1} e^{-x} dx = \Gamma(\alpha)$。于是：

$$\Gamma(\alpha) = \lim_{n\to\infty} \frac{n! \cdot n^\alpha}{\alpha(\alpha+1)\cdots(\alpha+n)}$$

---

#### 从欧拉乘积到贝塔积分：生成函数法

欧拉乘积 $\frac{n!}{z(z+1)\cdots(z+n)}$ 和贝塔积分 $\int_0^1 t^{z-1}(1-t)^n dt$ 之间有什么关系？用生成函数+常微分方程可以直接打通。

**Step 1 — 定义数列与递推关系**

定义数列 $a_n = \frac{1}{z(z+1)\cdots(z+n)}$，其中 $a_0 = \frac{1}{z}$。

写出 $a_{n-1} = \frac{1}{z(z+1)\cdots(z+n-1)}$。对比 $a_n$ 和 $a_{n-1}$：

$$(z+n)a_n = (z+n) \cdot \frac{1}{z(z+1)\cdots(z+n-1)(z+n)} = \frac{1}{z(z+1)\cdots(z+n-1)} = a_{n-1}$$

得到递推关系：

$$\boxed{(z+n)a_n = a_{n-1}}$$

**Step 2 — 构造生成函数并导出微分方程**

把离散数列 $\{a_n\}$ 塞进无穷级数，构造生成函数：

$$f(x) = \sum_{n=0}^\infty a_n x^{n+z}$$

逐项求导：

$$f'(x) = \frac{d}{dx} \sum_{n=0}^\infty a_n x^{n+z} = \sum_{n=0}^\infty a_n (n+z) x^{n+z-1}$$

利用递推公式 $(z+n)a_n = a_{n-1}$ 代入：

$$f'(x) = \sum_{n=0}^\infty a_{n-1} x^{n+z-1}$$

$n=0$ 时 $a_{-1}$ 无定义，单独处理：$a_0 \cdot z \cdot x^{z-1} = \frac{1}{z} \cdot z \cdot x^{z-1} = x^{z-1}$。对 $n \ge 1$ 部分做换元 $k = n-1$：

$$f'(x) = x^{z-1} + \sum_{k=0}^\infty a_k x^{(k+1)+z-1} = x^{z-1} + \sum_{k=0}^\infty a_k x^{k+z} = x^{z-1} + f(x)$$

得到一阶线性常微分方程：

$$\boxed{f'(x) - f(x) = x^{z-1}}$$

**Step 3 — 用积分因子法求解 ODE**

两边同乘积分因子 $e^{-x}$：

$$e^{-x} f'(x) - e^{-x} f(x) = e^{-x} x^{z-1}$$

左边是乘积导数的形式 $(e^{-x}f(x))'$：

$$(e^{-x} f(x))' = e^{-x} x^{z-1}$$

两边从 $0$ 积分到 $x$（积分变量改用 $t$ 避免混淆）：

$$\int_0^x (e^{-t} f(t))' dt = \int_0^x e^{-t} t^{z-1} dt$$

$$e^{-x} f(x) - e^{-0} f(0) = \int_0^x t^{z-1} e^{-t} dt$$

由 $f(x) = \sum a_n x^{n+z} = x^z(a_0 + a_1x + \cdots)$，$z > 0$ 时 $f(0) = 0$。两边同乘 $e^x$：

$$f(x) = e^x \int_0^x t^{z-1} e^{-t} dt = \int_0^x t^{z-1} e^{x-t} dt$$

对积分做代换 $t = x \cdot u$，$dt = x\,du$，$u \in [0, 1]$：

$$f(x) = \int_0^1 (xu)^{z-1} e^{x(1-u)} \cdot x\,du = x^z \int_0^1 u^{z-1} e^{x(1-u)} du$$

将 $u$ 换回 $t$：

$$\boxed{f(x) = x^z \int_0^1 t^{z-1} e^{x(1-t)} dt}$$

**Step 4 — 麦克劳林展开提取系数**

回顾 $f(x)$ 的定义：$f(x) = \sum_{n=0}^\infty a_n x^{n+z} = x^z \sum_{n=0}^\infty a_n x^n$。对比积分形式，约去 $x^z$：

$$\sum_{n=0}^\infty a_n x^n = \int_0^1 t^{z-1} e^{x(1-t)} dt$$

根据泰勒级数性质，$a_n = \frac{1}{n!} \cdot \frac{d^n}{dx^n}\Big|_{x=0} \int_0^1 t^{z-1} e^{x(1-t)} dt$。积分对 $t$，求导对 $x$，可交换：

$$\frac{d^n}{dx^n} e^{x(1-t)} = (1-t)^n e^{x(1-t)}$$

令 $x \to 0$，$e^{0(1-t)} = 1$：

$$a_n = \frac{1}{n!} \int_0^1 t^{z-1} (1-t)^n dt$$

代入 $a_n$ 的定义 $\frac{1}{z(z+1)\cdots(z+n)}$，两边同乘 $n!$：

$$\boxed{\frac{n!}{z(z+1)\cdots(z+n)} = \int_0^1 (1-t)^n t^{z-1} dt}$$

> 左边是欧拉无穷乘积的有限截断，右边是贝塔积分的标准形式 $B(z, n+1)$。这证明了欧拉的构造和贝塔函数本质上是同一件事的两种写法——一个是离散的代数分式，一个是连续的积分表示。

---

#### Weierstrass 无穷乘积

从欧拉形式出发：

$$\frac{1}{\Gamma(z)} = \lim_{n\to\infty} \frac{z(z+1)\cdots(z+n)}{n! \cdot n^z}$$

重写分子每一项：

$$z(z+1)(z+2)\cdots(z+n) = z \cdot \prod_{k=1}^n (z+k) = z \cdot \prod_{k=1}^n k\left(1 + \frac{z}{k}\right) = z \cdot n! \cdot \prod_{k=1}^n \left(1 + \frac{z}{k}\right)$$

代入，$n!$ 抵消：

$$\frac{1}{\Gamma(z)} = \lim_{n\to\infty} z \cdot \prod_{k=1}^n \left(1 + \frac{z}{k}\right) \cdot n^{-z}$$

处理 $n^{-z} = e^{-z\ln n}$。将 $\ln n$ 用调和数 $H_n = \sum_{k=1}^n \frac{1}{k}$ 表达：

$$\ln n = \sum_{k=1}^n \frac{1}{k} - (H_n - \ln n)$$

$$e^{-z\ln n} = \exp\left(-z\sum_{k=1}^n \frac{1}{k}\right) \cdot \exp\left(z(H_n - \ln n)\right) = \prod_{k=1}^n e^{-z/k} \cdot e^{z(H_n - \ln n)}$$

代入：

$$\frac{1}{\Gamma(z)} = \lim_{n\to\infty} z \cdot \prod_{k=1}^n \left(1 + \frac{z}{k}\right) e^{-z/k} \cdot e^{z(H_n - \ln n)}$$

当 $n \to \infty$ 时，$H_n - \ln n \to \gamma \approx 0.57721$（欧拉-马歇罗尼常数）：

$$\boxed{\frac{1}{\Gamma(z)} = z e^{\gamma z} \prod_{n=1}^{\infty} \left(1 + \frac{z}{n}\right) e^{-z/n}}$$

从乘积直接读出：
- $\Gamma'(1) = -\gamma$
- $z = 0, -1, -2, \dots$ 时乘积中某一项为零 → 一阶极点，留数为 $(-1)^n/n!$

---

#### Bohr-Mollerup 唯一性定理

**定理**：$\Gamma(x)$ 是 $x > 0$ 上唯一满足以下三条的函数 $f(x)$：

1. $f(1) = 1$
2. $f(x+1) = x f(x)$（函数方程/递推）
3. $f(x)$ 是对数凸函数（$\ln f(x)$ 是凸函数）

**证明**：取 $x \in (0, 1]$ 和正整数 $n \ge 2$。

反复使用条件 2 建立 $f(n+x)$ 与 $f(x)$ 的联系：

$$f(n+x) = (n+x-1)(n+x-2)\cdots(x+1)x \cdot f(x) \qquad\text{(A)}$$

对数凸性（条件 3）：$\ln f$ 凸 ⇒ $f(tx + (1-t)y) \le f(x)^t f(y)^{1-t}$。

**上界**：将 $n+x$ 写为 $x \cdot (n+1) + (1-x) \cdot n$ 的凸组合（$x \in (0, 1]$）：

$$f(n+x) \le f(n+1)^x f(n)^{1-x}$$

由条件 2：$f(n+1) = n!$，$f(n) = (n-1)!$：

$$f(n+x) \le (n!)^x \cdot [(n-1)!]^{1-x} = (n-1)! \cdot n^x \qquad\text{(B上)}$$

**下界**：将 $n+1$ 写为 $\frac{1}{1+x}(n+1+x) + \frac{x}{1+x} \cdot n$ 的凸组合。由对数凸性：

$$f(n+1) \le f(n+1+x)^{\frac{1}{1+x}} f(n)^{\frac{x}{1+x}}$$

$$(n!) \le f(n+1+x)^{\frac{1}{1+x}} \cdot [(n-1)!]^{\frac{x}{1+x}}$$

两边取 $(1+x)$ 次方：$(n!)^{1+x} \le f(n+1+x) \cdot [(n-1)!]^x$：

$$f(n+1+x) \ge \frac{(n!)^{1+x}}{[(n-1)!]^x} = n! \cdot n^x$$

将 $n$ 替换为 $n-1$（使结论适用于 $f(n+x)$）：

$$f(n+x) \ge (n-1)! \cdot (n-1)^x \qquad\text{(B下)}$$

**夹逼**：由 (A)：$f(x) = \frac{f(n+x)}{(n+x-1)(n+x-2)\cdots x}$，代入上下界：

$$\frac{(n-1)! \cdot (n-1)^x}{x(x+1)\cdots(x+n-1)} \le f(x) \le \frac{(n-1)! \cdot n^x}{x(x+1)\cdots(x+n-1)}$$

令 $n \to \infty$，$\frac{(n-1)^x}{n^x} \to 1$，上下界收敛于同一极限——欧拉的 $\Gamma(x)$ 定义：

$$\boxed{f(x) = \lim_{n\to\infty} \frac{n! \cdot n^x}{x(x+1)\cdots(x+n)} = \Gamma(x)}$$

> 不需要积分，只用递推 + 凸性就能唯一确定 $\Gamma$——这是伽玛函数的"宪法"。

---

#### Legendre 倍元公式

> 此证明同样依赖第 2 节的桥梁公式。

$$\Gamma(z)\,\Gamma\!\left(z + \tfrac{1}{2}\right) = 2^{1-2z} \sqrt{\pi} \;\Gamma(2z)$$

**Step 1** — 从贝塔函数 $B(z, z)$ 入手：

$$B(z, z) = \frac{\Gamma(z)\Gamma(z)}{\Gamma(2z)} = \int_0^1 x^{z-1}(1-x)^{z-1} dx$$

**Step 2** — 代换 $x = \sin^2\theta$，则 $1-x = \cos^2\theta$，$dx = 2\sin\theta\cos\theta\,d\theta$，$\theta \in [0, \pi/2]$：

$$B(z,z) = \int_0^{\pi/2} (\sin^2\theta)^{z-1} (\cos^2\theta)^{z-1} \cdot 2\sin\theta\cos\theta\,d\theta$$

$$= 2\int_0^{\pi/2} \sin^{2z-1}\theta \cos^{2z-1}\theta\,d\theta$$

**Step 3** — 用倍角公式 $\sin 2\theta = 2\sin\theta\cos\theta$：

$$\sin^{2z-1}\theta \cos^{2z-1}\theta = (\sin\theta\cos\theta)^{2z-1} = \left(\frac{\sin 2\theta}{2}\right)^{2z-1}$$

$$B(z,z) = 2\int_0^{\pi/2} \frac{\sin^{2z-1}2\theta}{2^{2z-1}} d\theta = \frac{1}{2^{2z-2}} \int_0^{\pi/2} \sin^{2z-1}2\theta\,d\theta$$

**Step 4** — 代换 $u = 2\theta$，$d\theta = du/2$，$u \in [0, \pi]$：

$$B(z,z) = \frac{1}{2^{2z-2}} \cdot \frac{1}{2} \int_0^{\pi} \sin^{2z-1}u\,du = \frac{1}{2^{2z-1}} \int_0^{\pi} \sin^{2z-1}u\,du$$

由 $\sin(\pi - u) = \sin u$，$\int_0^{\pi} \sin^k u\,du = 2\int_0^{\pi/2} \sin^k u\,du$：

$$B(z,z) = \frac{2}{2^{2z-1}} \int_0^{\pi/2} \sin^{2z-1}u\,du$$

**Step 5** — 识别贝塔函数。对照三角形式 $B(p,q) = 2\int_0^{\pi/2} \sin^{2p-1}\theta \cos^{2q-1}\theta\,d\theta$，令 $p = z$，$q = 1/2$（此时 $\cos^{2\cdot(1/2)-1} = \cos^0 = 1$）：

$$2\int_0^{\pi/2} \sin^{2z-1}u\,du = B\!\left(z, \tfrac{1}{2}\right)$$

所以 $\int_0^{\pi/2} \sin^{2z-1}u\,du = \frac{1}{2}B(z, \frac{1}{2})$：

$$B(z,z) = \frac{2}{2^{2z-1}} \cdot \frac{1}{2} B\!\left(z, \tfrac{1}{2}\right) = \frac{1}{2^{2z-1}} B\!\left(z, \tfrac{1}{2}\right)$$

**Step 6** — 用桥梁公式展开两边：

$$\frac{\Gamma(z)^2}{\Gamma(2z)} = \frac{1}{2^{2z-1}} \cdot \frac{\Gamma(z)\Gamma(1/2)}{\Gamma(z + 1/2)}$$

两边约去 $\Gamma(z)$：

$$\frac{\Gamma(z)}{\Gamma(2z)} = \frac{1}{2^{2z-1}} \cdot \frac{\Gamma(1/2)}{\Gamma(z + 1/2)}$$

代入 $\Gamma(1/2) = \sqrt{\pi}$，移项：

$$\boxed{\Gamma(z)\,\Gamma\!\left(z + \tfrac{1}{2}\right) = 2^{1-2z} \sqrt{\pi} \;\Gamma(2z)}$$

> 验证：令 $z = 1/2$，左边 $\Gamma(1/2)\Gamma(1) = \sqrt{\pi} \cdot 1$，右边 $2^0\sqrt{\pi}\,\Gamma(1) = \sqrt{\pi}$，自洽。

---

## 2. 贝塔函数 $B(p,q)$

### 定义

$$B(p, q) = \int_0^1 x^{p-1} (1-x)^{q-1} dx \qquad (p > 0, q > 0)$$

如果伽玛函数是"整个正半轴上的加权面积"，贝塔函数就是"压缩在 $[0,1]$ 区间内的浓缩版"。它在概率论中充当归一化常数——让贝塔分布的积分恰好为 1。

---

### 桥梁公式的证明

**工具**：二重积分 + 极坐标变换

两个伽玛函数相乘，写成第一象限上的二重积分：

$$\Gamma(p)\Gamma(q) = \left(\int_0^\infty u^{p-1} e^{-u} du\right) \left(\int_0^\infty v^{q-1} e^{-v} dv\right)$$

$$= \int_0^\infty \int_0^\infty u^{p-1} v^{q-1} e^{-(u+v)} du\,dv$$

代换 $u = x^2$，$v = y^2$，则：

$$du = 2x\,dx, \quad u^{p-1} = (x^2)^{p-1} = x^{2p-2}$$

$$dv = 2y\,dy, \quad v^{q-1} = (y^2)^{q-1} = y^{2q-2}$$

$$\Gamma(p)\Gamma(q) = \int_0^\infty \int_0^\infty x^{2p-2} y^{2q-2} e^{-(x^2+y^2)} \cdot 2x\,dx \cdot 2y\,dy$$

整理 $x$ 指数：$x^{2p-2} \cdot x = x^{2p-1}$，同理 $y$ 为 $y^{2q-1}$。常数 $2 \times 2 = 4$：

$$\Gamma(p)\Gamma(q) = 4 \int_0^\infty \int_0^\infty x^{2p-1} y^{2q-1} e^{-(x^2+y^2)} dx\,dy$$

极坐标变换：$x = r\cos\theta$，$y = r\sin\theta$，$dx\,dy = r\,dr\,d\theta$，$x^2 + y^2 = r^2$。第一象限 $r \in [0, \infty)$，$\theta \in [0, \pi/2]$：

$$\Gamma(p)\Gamma(q) = 4 \int_0^{\pi/2} \int_0^\infty (r\cos\theta)^{2p-1} (r\sin\theta)^{2q-1} e^{-r^2} \cdot r\,dr\,d\theta$$

分离 $r$ 和 $\theta$。$r$ 的总指数：$(2p-1) + (2q-1) + 1 = 2p + 2q - 1$：

$$\Gamma(p)\Gamma(q) = 4 \underbrace{\left(\int_0^{\pi/2} \cos^{2p-1}\theta \sin^{2q-1}\theta\,d\theta\right)}_{\text{只含 }\theta} \;\cdot\; \underbrace{\left(\int_0^\infty r^{2p+2q-1} e^{-r^2} dr\right)}_{\text{只含 }r}$$

**解 $r$ 积分**：令 $t = r^2$，$dt = 2r\,dr$，$r^{2p+2q-1} = r^{2p+2q-2} \cdot r = t^{p+q-1} \cdot r$：

$$\int_0^\infty r^{2p+2q-1} e^{-r^2} dr = \int_0^\infty t^{p+q-1} e^{-t} \cdot \frac{1}{2} dt = \frac{1}{2} \int_0^\infty t^{(p+q)-1} e^{-t} dt = \frac{1}{2} \Gamma(p+q)$$

**解 $\theta$ 积分**：令 $z = \cos^2\theta$，则 $\sin^2\theta = 1-z$，$dz = -2\cos\theta\sin\theta\,d\theta$：

$$\int_0^{\pi/2} \cos^{2p-1}\theta \sin^{2q-1}\theta\,d\theta = \frac{1}{2}\int_0^1 z^{p-1}(1-z)^{q-1} dz = \frac{1}{2} B(p,q)$$

**组装**：

$$\Gamma(p)\Gamma(q) = 4 \cdot \frac{1}{2} B(p,q) \cdot \frac{1}{2} \Gamma(p+q) = B(p,q) \,\Gamma(p+q)$$

$$\boxed{B(p, q) = \frac{\Gamma(p)\Gamma(q)}{\Gamma(p+q)}}$$

---

### 等价积分形式

**三角形式**（令 $x = \sin^2\theta$）：

$x = \sin^2\theta \Rightarrow 1-x = \cos^2\theta$，$dx = 2\sin\theta\cos\theta\,d\theta$，积分限 $\theta \in [0, \pi/2]$：

$$B(p,q) = \int_0^{\pi/2} (\sin^2\theta)^{p-1} (\cos^2\theta)^{q-1} \cdot 2\sin\theta\cos\theta\,d\theta$$

整理指数：$\sin^{2p-2+1} = \sin^{2p-1}$，$\cos^{2q-2+1} = \cos^{2q-1}$：

$$\boxed{B(p,q) = 2\int_0^{\pi/2} \sin^{2p-1}\theta \cos^{2q-1}\theta\,d\theta}$$

**有理形式**（令 $u = x/(1-x)$）：

$x = \frac{u}{1+u}$，$1-x = \frac{1}{1+u}$，$dx = \frac{du}{(1+u)^2}$，积分限 $u \in [0, \infty)$：

$$B(p,q) = \int_0^\infty \left(\frac{u}{1+u}\right)^{p-1} \left(\frac{1}{1+u}\right)^{q-1} \frac{du}{(1+u)^2}$$

分母 $(1+u)$ 的总指数：$(p-1) + (q-1) + 2 = p+q$：

$$\boxed{B(p,q) = \int_0^\infty \frac{u^{p-1}}{(1+u)^{p+q}} du}$$

---

## 3. 斯特林公式

### 公式与直觉

$n!$ 的增长极其恐怖（$20! \approx 2.43 \times 10^{18}$），直接算不现实。斯特林公式给出了 $n!$ 的**渐进等价**：

$$n! \sim \sqrt{2\pi n}\left(\frac{n}{e}\right)^n \qquad (n \to \infty)$$

$\sim$ 表示 $\lim_{n\to\infty} \frac{n!}{\sqrt{2\pi n}(n/e)^n} = 1$。

取对数：$\ln n! \sim n\ln n - n + \frac{1}{2}\ln(2\pi n)$。三项来源：$n\ln n - n$ 来自 $\int_1^n \ln x\,dx$（主导项），$\frac{1}{2}\ln n$ 来自高斯积分中的 $\sqrt{n}$（峰宽），$\frac{1}{2}\ln(2\pi)$ 来自高斯积分中的 $\sqrt{2\pi}$（归一化残余）。

连续形式：$\Gamma(z+1) \sim \sqrt{2\pi z}(z/e)^z$。

精度：相对误差约 $1/(12n)$，$n \ge 10$ 时前三项足够。更高精度用斯特林级数：

$$\ln n! = n\ln n - n + \frac{1}{2}\ln(2\pi n) + \frac{1}{12n} - \frac{1}{360n^3} + \frac{1}{1260n^5} - \cdots$$

---

### 证明：拉普拉斯方法

**工具**：大参数积分由被积函数最大值邻域主导

**Step 1 — 将 $n!$ 写成指数积分**

$$n! = \Gamma(n+1) = \int_0^\infty x^n e^{-x} dx$$

将被积函数改写为单一的指数形式 $e^{g(x)}$：

$$x^n e^{-x} = e^{n\ln x - x} = e^{g(x)}, \qquad g(x) = n\ln x - x$$

$$n! = \int_0^\infty e^{g(x)} dx$$

**Step 2 — 找到 $g(x)$ 的最大值点**

$$g'(x) = \frac{d}{dx}(n\ln x - x) = \frac{n}{x} - 1$$

令 $g'(x) = 0$：$\frac{n}{x} = 1 \Rightarrow x_0 = n$

$$g''(x) = \frac{d}{dx}\left(\frac{n}{x} - 1\right) = -\frac{n}{x^2}$$

在 $x_0 = n$ 处：$g''(n) = -\frac{n}{n^2} = -\frac{1}{n} < 0$，确认为极大值。

在最大值处的函数值：$g(n) = n\ln n - n$

**Step 3 — 在 $x_0 = n$ 处做二阶泰勒展开**

$$g(x) \approx g(n) + g'(n)(x-n) + \frac{1}{2}g''(n)(x-n)^2$$

$g'(n) = 0$（最大值点一阶导为零），$g''(n) = -\frac{1}{n}$：

$$g(x) \approx n\ln n - n + 0 \cdot (x-n) + \frac{1}{2}\left(-\frac{1}{n}\right)(x-n)^2$$

$$g(x) \approx n\ln n - n - \frac{(x-n)^2}{2n}$$

**Step 4 — 代入积分并分离常数因子**

$$n! \approx \int_0^\infty \exp\left(n\ln n - n - \frac{(x-n)^2}{2n}\right) dx$$

$$= e^{n\ln n - n} \int_0^\infty \exp\left(-\frac{(x-n)^2}{2n}\right) dx$$

$$= \left(\frac{n}{e}\right)^n \int_0^\infty \exp\left(-\frac{(x-n)^2}{2n}\right) dx$$

**Step 5 — 高斯积分近似**

当 $n$ 很大时，被积函数的"高斯峰"中心在 $x = n$，宽度约 $\sqrt{n}$。因为 $n \gg \sqrt{n}$，峰值远在 $x = 0$ 右边，负半轴的尾部贡献是 $e^{-n/2}$ 量级，可以忽略。将积分下限从 $0$ 延拓到 $-\infty$：

$$\int_0^\infty \exp\left(-\frac{(x-n)^2}{2n}\right) dx \approx \int_{-\infty}^\infty \exp\left(-\frac{(x-n)^2}{2n}\right) dx$$

高斯积分公式 $\int_{-\infty}^\infty e^{-u^2/(2\sigma^2)} du = \sigma\sqrt{2\pi}$。这里 $\sigma = \sqrt{n}$：

$$= \sqrt{n} \cdot \sqrt{2\pi} = \sqrt{2\pi n}$$

**Step 6 — 组装**

$$n! \approx \left(\frac{n}{e}\right)^n \cdot \sqrt{2\pi n} = \sqrt{2\pi n}\left(\frac{n}{e}\right)^n$$

> **为什么 $\sqrt{2\pi}$ 会出现在阶乘里？** $g''(n) = -1/n$ 决定了高斯峰的"曲率"，峰宽 $\sigma = \sqrt{n}$ 直接送入高斯积分 $\sigma\sqrt{2\pi} = \sqrt{2\pi n}$。阶乘里的 $\pi$ 就是高斯积分里的那个 $\pi$。

---

## 4. 沃利斯公式

1655 年发现，数学史上第一次将 $\pi$ 表示为有理数的无穷运算：

$$\frac{\pi}{2} = \frac{2}{1} \cdot \frac{2}{3} \cdot \frac{4}{3} \cdot \frac{4}{5} \cdot \frac{6}{5} \cdot \frac{6}{7} \cdots = \prod_{n=1}^{\infty} \frac{4n^2}{4n^2-1}$$

---

### 证法一：斯特林代入法

前 $n$ 项部分积 $W_n = \prod_{k=1}^n \frac{(2k)^2}{(2k-1)(2k+1)}$。将分子分母分别用阶乘表达。

分子：$\prod_{k=1}^n (2k)^2 = 2^{2n} (n!)^2$

分母中的奇数乘积有恒等式 $\prod_{k=1}^n (2k-1) = \frac{(2n)!}{2^n n!}$，故：

$$\prod_{k=1}^n (2k-1)(2k+1) = \left(\frac{(2n)!}{2^n n!}\right)^2 \cdot (2n+1)$$

代入 $W_n$：

$$W_n = \frac{2^{2n}(n!)^2}{\left(\frac{(2n)!}{2^n n!}\right)^2 (2n+1)} = \frac{2^{2n}(n!)^2 \cdot 2^{2n}(n!)^2}{[(2n)!]^2 (2n+1)} = \frac{2^{4n}(n!)^4}{[(2n)!]^2(2n+1)}$$

代入斯特林：$n! \sim \sqrt{2\pi n}(\frac{n}{e})^n$，$(2n)! \sim \sqrt{4\pi n}(\frac{2n}{e})^{2n}$。计算比值：

$$(n!)^4 \sim \left[\sqrt{2\pi n}\left(\frac{n}{e}\right)^n\right]^4 = 4\pi^2 n^2 \left(\frac{n}{e}\right)^{4n}$$

$$[(2n)!]^2 \sim \left[\sqrt{4\pi n}\left(\frac{2n}{e}\right)^{2n}\right]^2 = 4\pi n \left(\frac{2n}{e}\right)^{4n}$$

$$\frac{2^{4n}(n!)^4}{[(2n)!]^2} \sim \frac{2^{4n} \cdot 4\pi^2 n^2 \left(\frac{n}{e}\right)^{4n}}{4\pi n \left(\frac{2n}{e}\right)^{4n}}$$

分子分母的 $e^{-4n}$ 抵消。$2^{4n} \cdot n^{4n} / (2n)^{4n} = 2^{4n} n^{4n} / (2^{4n} n^{4n}) = 1$，也完美抵消！比值 $= \frac{4\pi^2 n^2}{4\pi n} = \pi n$：

$$W_n \sim \frac{\pi n}{2n+1}$$

取极限：

$$\lim_{n\to\infty} W_n = \lim_{n\to\infty} \frac{\pi n}{2n+1} = \lim_{n\to\infty} \frac{\pi}{2 + 1/n} = \frac{\pi}{2}$$

> $\pi/2$ 从斯特林的 $\sqrt{2\pi n}$ 中溢出——$e^{-n}$ 和 $n^n$ 全消灭，只有 $\pi$ 幸存。

---

### 证法二：不等式夹逼法

**Step 1 — 构造不等式链**

起点是基本不等式 $e^t \ge 1 + t$（对所有实数 $t$ 成立）。

① 令 $t = -x^2$（$x \in [0, 1]$）：$e^{-x^2} \ge 1 - x^2$。两边非负，同时取 $n$ 次方：

$$(1-x^2)^n \le e^{-nx^2}$$

② 令 $t = x^2$：$e^{x^2} \ge 1 + x^2$。两边取倒数（不等号反转）：$e^{-x^2} \le \frac{1}{1+x^2}$。同时取 $n$ 次方：

$$e^{-nx^2} \le \frac{1}{(1+x^2)^n}$$

③ 联立：

$$(1-x^2)^n \le e^{-nx^2} \le \frac{1}{(1+x^2)^n}$$

**Step 2 — 对整条不等式链做定积分**

$$\int_0^1 (1-x^2)^n dx \;\le\; \int_0^\infty e^{-nx^2} dx \;\le\; \int_0^\infty \frac{dx}{(1+x^2)^n}$$

注意左侧积分上限是 $1$ 而不是 $\infty$——因为 $x > 1$ 时 $(1-x^2)^n$ 变号，夹逼在 $[0, 1]$ 外不成立。

**Step 3 — 计算三个积分**

**左侧**：令 $x = \sin\theta$，$dx = \cos\theta\,d\theta$，$1 - x^2 = \cos^2\theta$。$x$ 从 $0 \to 1$ 时 $\theta$ 从 $0 \to \pi/2$：

$$\int_0^1 (1-x^2)^n dx = \int_0^{\pi/2} (\cos^2\theta)^n \cos\theta\,d\theta = \int_0^{\pi/2} \cos^{2n+1}\theta\,d\theta$$

由对称性 $\int_0^{\pi/2} \cos^k\theta\,d\theta = \int_0^{\pi/2} \sin^k\theta\,d\theta$。定义沃利斯积分 $I_k := \int_0^{\pi/2} \sin^k\theta\,d\theta$：

左侧 $= I_{2n+1}$

**中间**：令 $u = \sqrt{n}\,x$，$x = u/\sqrt{n}$，$dx = du/\sqrt{n}$：

$$\int_0^\infty e^{-nx^2} dx = \int_0^\infty e^{-n(u/\sqrt{n})^2} \cdot \frac{du}{\sqrt{n}} = \frac{1}{\sqrt{n}} \int_0^\infty e^{-u^2} du$$

高斯积分 $\int_0^\infty e^{-u^2} du = \frac{\sqrt{\pi}}{2}$：

中间 $= \frac{\sqrt{\pi}}{2\sqrt{n}}$

**右侧**：令 $x = \tan\theta$，$dx = \sec^2\theta\,d\theta$，$1+x^2 = \sec^2\theta$：

$$\int_0^\infty \frac{dx}{(1+x^2)^n} = \int_0^{\pi/2} \frac{\sec^2\theta\,d\theta}{(\sec^2\theta)^n} = \int_0^{\pi/2} \cos^{2n-2}\theta\,d\theta = I_{2n-2}$$

**Step 4 — 沃利斯积分的递推公式与显式**

对 $I_k = \int_0^{\pi/2} \sin^k\theta\,d\theta$ 做分部积分。令 $u = \sin^{k-1}\theta$，$dv = \sin\theta\,d\theta$：

$$du = (k-1)\sin^{k-2}\theta\cos\theta\,d\theta, \quad v = -\cos\theta$$

$$I_k = \left[-\sin^{k-1}\theta\cos\theta\right]_0^{\pi/2} + (k-1)\int_0^{\pi/2} \sin^{k-2}\theta\cos^2\theta\,d\theta$$

边界项：$\theta = 0$ 时 $\sin 0 = 0$，$\theta = \pi/2$ 时 $\cos(\pi/2) = 0$ → 边界为 $0$。

代入 $\cos^2\theta = 1 - \sin^2\theta$：

$$I_k = (k-1)\int_0^{\pi/2} \sin^{k-2}\theta(1 - \sin^2\theta) d\theta = (k-1)(I_{k-2} - I_k)$$

移项：

$$I_k = (k-1)I_{k-2} - (k-1)I_k \;\Rightarrow\; k I_k = (k-1)I_{k-2} \;\Rightarrow\; \boxed{I_k = \frac{k-1}{k} I_{k-2}}$$

**奇数次**：$I_1 = \int_0^{\pi/2} \sin\theta\,d\theta = [-\cos\theta]_0^{\pi/2} = 1$

$$I_{2n+1} = \frac{2n}{2n+1} \cdot \frac{2n-2}{2n-1} \cdots \frac{2}{3} \cdot I_1 = \frac{(2n)!!}{(2n+1)!!}$$

**偶数次**：$I_0 = \int_0^{\pi/2} d\theta = \frac{\pi}{2}$

$$I_{2n-2} = \frac{2n-3}{2n-2} \cdot \frac{2n-5}{2n-4} \cdots \frac{1}{2} \cdot I_0 = \frac{(2n-3)!!}{(2n-2)!!} \cdot \frac{\pi}{2}$$

**Step 5 — 代入不等式链并取极限**

$$I_{2n+1} \le \frac{\sqrt{\pi}}{2\sqrt{n}} \le I_{2n-2}$$

两边同乘 $\sqrt{n}$：

$$\sqrt{n} \cdot I_{2n+1} \le \frac{\sqrt{\pi}}{2} \le \sqrt{n} \cdot I_{2n-2}$$

可以证明 $\lim_{n\to\infty} \sqrt{n}\,I_{2n+1} = \lim_{n\to\infty} \sqrt{n}\,I_{2n-2} = \frac{\sqrt{\pi}}{2}$（中间的高斯积分正好是 $\frac{\sqrt{\pi}}{2}$，三明治的两片面包同时夹到中间那层）。代入 $I_{2n+1}$ 和 $I_{2n-2}$ 的显式即得沃利斯乘积：

$$\boxed{\frac{\pi}{2} = \prod_{n=1}^{\infty} \frac{4n^2}{4n^2-1}}$$

> 夹逼法最精妙之处：高斯积分 $\sqrt{\pi}/2$ 作为夹逼的"锚"出现，沃利斯乘积的 $\pi$ 就是高斯积分的 $\pi$。

---

## 5. 应用

### 斯特林公式

| 场景 | 怎么用 |
|------|------|
| 大阶乘估算 | $100! \approx \sqrt{200\pi}(100/e)^{100}$，避免溢出 |
| 组合数渐进 | $\binom{2n}{n} \sim \frac{4^n}{\sqrt{\pi n}}$ |
| 统计力学 | $S = k\ln\Omega$ 中的阶乘展开 → 玻尔兹曼分布 |
| 信息论 | 信道容量渐进分析 |
| 算法分析 | $O(n!)$ 精确量级 |

---

### 概率论中的四大分布

| 分布 | 含有的特殊函数 | 应用场景 |
|------|---------------|----------|
| $\text{Gamma}(\alpha, \lambda)$ | $\Gamma(\alpha)$ | 等待时间、寿命分析 |
| $\text{Beta}(p,q)$ | $B(p,q)$ | 比例/概率建模、A/B 测试 |
| $t$ 分布 | $\Gamma$ | 小样本均值检验 |
| $F$ 分布 | $\Gamma$ | 方差比检验、ANOVA |

**伽玛分布密度**：$f(x) = \frac{\lambda^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\lambda x} \;(x \ge 0)$

> 泊松分布描述"固定时间内事件发生次数"，伽玛分布描述"第 $\alpha$ 次事件发生的等待时间"。

**贝塔分布密度**：$f(x) = \frac{1}{B(p,q)} x^{p-1} (1-x)^{q-1} \;(0 \le x \le 1)$

贝塔分布是二项分布的共轭先验：$\text{Beta}(a,b)$ + $k$ 次成功 → 后验 $\text{Beta}(a+k,\,b+n-k)$。归一化常数 $B(a+k, b+n-k)$ 无需重新积分。

---

### 特殊积分速算

$$\int_0^1 x^3(1-x)^5 dx = B(4,6) = \frac{3! \cdot 5!}{9!} = \frac{1}{1260}$$

$$\int_0^\infty x^5 e^{-2x} dx = \frac{\Gamma(6)}{2^6} = \frac{15}{8}$$

$$\int_0^{\pi/2} \sin^3\theta \cos^4\theta\,d\theta = \frac{1}{2}B\!\left(2, \tfrac{5}{2}\right)$$

---

## 相关笔记

- [[正态分布]]（$\Gamma(1/2) = \sqrt{\pi}$ 是高斯积分的直接推论）
- [[伽马分布]]（$\Gamma(\alpha)$ 是其归一化分母）
- [[贝塔分布]]（$B(p,q)$ 是其归一化分母）
- [[分布之间的关系和意义总结]]（四大分布的归一化常数汇总）
- [[概率论与数理统计中的变量替换（Variable Transformation）]]（贝塔桥梁公式证明使用雅可比极坐标变换）
- [[最核心的五个基础概念]]
- [[切比雪夫不等式]]
