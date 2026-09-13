# 一、先回忆一维变量替换

假设：

$$ Y=g(X) $$

例如：

$$ Y=X^2 $$

我们知道：

$$ f_Y(y)=f_X(x)\left|\frac{dx}{dy}\right| $$

为什么有：

$$ \left|\frac{dx}{dy}\right| $$

看一个小区间：

原来：

$$ x\sim x+dx $$

经过变换：

$$ y=g(x) $$

变成：

$$ y\sim y+dy $$

由于概率不变：

$$ P(x<X<x+dx) = P(y<Y<y+dy) $$

所以：

$$ f_X(x)dx=f_Y(y)dy $$

整理：

$$ f_Y(y)=f_X(x)\frac{dx}{dy} $$

所以：

$$ \boxed{\frac{dx}{dy}} $$

就是：

> 新坐标中的长度单位和旧坐标中的长度单位之间的比例。

---

# 二、二维情况为什么需要雅可比？

二维随机变量：

$$ (X,Y) $$

有联合密度：

$$ f_{X,Y}(x,y) $$

如果换变量：

$$ U=u(x,y) $$
$$ V=v(x,y) $$

那么一个小矩形：

$$ dxdy $$

经过变换后，不再是矩形，而变成一个小平行四边形。

例如：

原来的面积：

$$ dxdy $$

新的面积：

$$ dudv $$

但是：

$$ dxdy\neq dudv $$

两者差一个比例：

$$ \boxed{ \left| \frac{\partial(x,y)} {\partial(u,v)} \right| } $$

这就是雅可比行列式。

---

# 三、雅可比到底表示什么？

二维中：

$$ J= \frac{\partial(x,y)} {\partial(u,v)} $$

展开：

$$ J= \begin{vmatrix} 
\frac{\partial x}{\partial u} & \frac{\partial x}{\partial v} \\ 
\frac{\partial y}{\partial u} & \frac{\partial y}{\partial v} 
\end{vmatrix} $$

计算：

$$ = \frac{\partial x}{\partial u} \frac{\partial y}{\partial v} - \frac{\partial x}{\partial v} \frac{\partial y}{\partial u} $$

它实际上就是：

$$ \boxed{ \text{面积缩放比例} } $$

---

# 四、用极坐标理解雅可比（最经典）

二维变换：

$$ x=r\cos\theta $$
$$ y=r\sin\theta $$

我们从直角坐标：

$$ dxdy $$

变成：

$$ drd\theta $$

那么面积怎么变化？

一个小区域：

- 半径方向：

$$ dr $$

- 角度方向：

$$ d\theta $$

但是角度方向对应的实际长度：

不是：

$$ d\theta $$

而是：

$$ r d\theta $$

所以面积：

$$ dA=dr\times rd\theta $$

即：

$$ \boxed{ dxdy=r\,drd\theta } $$

这里的：

$$ r $$

就是雅可比。

---

因此二维密度：

$$ f_{X,Y}(x,y) $$

换成极坐标：

$$ \boxed{ f_{R,\Theta}(r,\theta) = f_{X,Y}(r\cos\theta,r\sin\theta) \cdot r } $$

---

# 五、为什么不能直接替换？

很多人会犯：

假设：

$$ X=R\cos\Theta $$
$$ Y=R\sin\Theta $$

然后写：

$$ f_{R,\Theta} = f_{X,Y} $$

这是错误的。

原因：

概率不是密度。

概率守恒：

$$ \boxed{ f_{X,Y}(x,y)dxdy = f_{R,\Theta}(r,\theta)drd\theta } $$

左边：

旧坐标的小面积

右边：

新坐标的小面积

两个面积不同，所以必须补一个比例。

---

# 六、一个形象比喻

想象你有一张地图。

原地图：

$$ (x,y) $$

你换成：

$$ (u,v) $$

如果：

- 一个小格子被拉长两倍：

密度下降一半

- 一个小格子被压缩一半：

密度增加两倍

雅可比就是告诉你：

> 这个坐标变换把空间压缩/拉伸了多少。

---

# 七、概率论中为什么特别需要它？

因为概率密度不是一个点的概率：

$$ f(x,y) $$

本身没有概率意义。

真正有意义的是：

$$ \boxed{ f(x,y)dxdy } $$

它表示：

一个微小区域里的概率。

变量替换时：

区域大小变了，

所以必须调整密度。

---

# 八、考试记忆版

遇到二维变量替换：

$$ X=X(u,v) $$
$$ Y=Y(u,v) $$

直接写：

$$ \boxed{ f_{U,V}(u,v) = f_{X,Y}(x(u,v),y(u,v)) \left| \frac{\partial(x,y)} {\partial(u,v)} \right| } $$

其中：

$$ \left| \frac{\partial(x,y)} {\partial(u,v)} \right| $$

就是：

**新坐标小面积对应的原坐标面积比例。**

---

## 相关笔记

- [[增补变量法]]
- [[离散型变量的替换]]
- [[Γ函数、B函数与斯特林公式]]
