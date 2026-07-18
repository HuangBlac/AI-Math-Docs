# LFTP Chapter 1 笔记整理

> 对应 *Learning Theory from First Principles*：§1.2.3 Bernstein's Inequality、§1.2.4 Expectation of the Maximum、§1.2.5 Estimation of Expectations through Quadrature。
>
> 本文由手写扫描稿整理，并统一了符号、补足了省略步骤、纠正了公式笔误。

---

## 1.2.3 Bernstein 不等式

### 命题

设随机变量 $Z_1,\dots,Z_n$ 相互独立，并满足

$$
\mathbb E[Z_i]=0,\qquad |Z_i|\le c\quad\text{a.s.}
$$

记

$$
\sigma^2=\frac1n\sum_{i=1}^n\operatorname{Var}(Z_i).
$$

则对任意 $t>0$，

$$
\mathbb P\!\left(\left|\frac1n\sum_{i=1}^n Z_i\right|>t\right)
\le
2\exp\!\left(-\frac{nt^2}{2\sigma^2+\frac{2ct}{3}}\right).
$$

等价地，对任意 $\delta\in(0,1)$，以至少 $1-\delta$ 的概率，

$$
\left|\frac1n\sum_{i=1}^n Z_i\right|
\le
\sqrt{\frac{2\sigma^2\log(2/\delta)}{n}}
+
\frac{2c\log(2/\delta)}{3n}.
$$

### 第一步：单个随机变量的矩母函数界

设 $Z$ 满足 $\mathbb E[Z]=0$、$|Z|\le c$ 且 $\mathbb E[Z^2]=\sigma^2$。对任意 $s>0$，

$$
\begin{aligned}
\mathbb E[e^{sZ}]
&=1+s\mathbb E[Z]+\sum_{k=2}^{\infty}\frac{s^k}{k!}\mathbb E[Z^k]\\
&\le 1+\sum_{k=2}^{\infty}\frac{s^k}{k!}\mathbb E[|Z|^k]\\
&\le 1+\sum_{k=2}^{\infty}\frac{s^k}{k!}c^{k-2}\mathbb E[Z^2]\\
&=1+\frac{\sigma^2}{c^2}\bigl(e^{sc}-1-sc\bigr)\\
&\le \exp\!\left[\frac{\sigma^2}{c^2}\bigl(e^{sc}-1-sc\bigr)\right].
\end{aligned}
$$

最后一步使用了 $1+x\le e^x$。

### 第二步：Chernoff 方法

记 $\sigma_i^2=\operatorname{Var}(Z_i)$。由独立性与上面的矩母函数界，

$$
\begin{aligned}
\mathbb P\!\left(\frac1n\sum_{i=1}^n Z_i>t\right)
&=\mathbb P\!\left(e^{s\sum_{i=1}^n Z_i}>e^{nst}\right)\\
&\le e^{-nst}\prod_{i=1}^n\mathbb E[e^{sZ_i}]\\
&\le \exp\!\left[-nst+\frac{n\sigma^2}{c^2}\bigl(e^{sc}-1-sc\bigr)\right].
\end{aligned}
$$

令

$$
u=sc,\qquad \alpha=\frac{ct}{\sigma^2}.
$$

则指数可写为

$$
\frac{n\sigma^2}{c^2}\bigl(e^u-1-u-\alpha u\bigr).
$$

对 $0<u<3$，由级数展开

$$
\begin{aligned}
e^u-1-u
&=\sum_{k=0}^{\infty}\frac{u^{k+2}}{(k+2)!}\\
&\le \frac{u^2}{2}\sum_{k=0}^{\infty}\left(\frac u3\right)^k
=\frac{u^2}{2(1-u/3)}.
\end{aligned}
$$

取

$$
u=\frac{\alpha}{1+\alpha/3},
$$

得到

$$
e^u-1-u-\alpha u
\le
-\frac{\alpha^2}{2(1+\alpha/3)}.
$$

因此

$$
\mathbb P\!\left(\frac1n\sum_{i=1}^n Z_i>t\right)
\le
\exp\!\left(-\frac{nt^2}{2\sigma^2+\frac{2ct}{3}}\right).
$$

对 $-Z_i$ 应用同一结论，再使用 union bound，即得双边 Bernstein 不等式。

### 解释

- 当 $t$ 较小时，分母主要由 $2\sigma^2$ 控制，尾界具有近似高斯型衰减。
- 当 $t$ 较大时，线性项 $2ct/3$ 开始占主导，尾部近似呈指数衰减。
- 与只利用有界性的 Hoeffding 不等式相比，Bernstein 不等式进一步使用了方差信息。

---

## 1.2.4 次高斯变量最大值的期望

设 $Z_1,\dots,Z_n$ 均为零均值、次高斯参数为 $\tau^2$ 的随机变量，即

$$
\mathbb E[e^{\lambda Z_i}]
\le
\exp\!\left(\frac{\tau^2\lambda^2}{2}\right),
\qquad \lambda\in\mathbb R.
$$

这里不要求 $Z_1,\dots,Z_n$ 相互独立。

### 命题：最大值

$$
\mathbb E\left[\max_{1\le i\le n}Z_i\right]
\le
\sqrt{2\tau^2\log n}.
$$

### 证明

对任意 $\lambda>0$，由 Jensen 不等式、$\max_i a_i\le\sum_i a_i$ 以及次高斯性，

$$
\begin{aligned}
\mathbb E\left[\max_i Z_i\right]
&\le \frac1\lambda
\log\mathbb E\left[e^{\lambda\max_i Z_i}\right]\\
&=\frac1\lambda
\log\mathbb E\left[\max_i e^{\lambda Z_i}\right]\\
&\le\frac1\lambda
\log\mathbb E\left[\sum_{i=1}^n e^{\lambda Z_i}\right]\\
&\le\frac1\lambda\log\left(ne^{\tau^2\lambda^2/2}\right)\\
&=\frac{\log n}{\lambda}+\frac{\tau^2\lambda}{2}.
\end{aligned}
$$

右端在

$$
\lambda=\frac{\sqrt{2\log n}}{\tau}
$$

处取得最小值，从而得到结论。

### 绝对值最大值

把

$$
|Z_i|=\max\{Z_i,-Z_i\}
$$

看成 $2n$ 个次高斯变量的最大值，可得

$$
\boxed{
\mathbb E\left[\max_{1\le i\le n}|Z_i|\right]
\le
\sqrt{2\tau^2\log(2n)}
}.
$$

### 使用尾界与 union bound 的另一种证明

记

$$
M=\max_{1\le i\le n}|Z_i|.
$$

由次高斯尾界和 union bound，

$$
\mathbb P(M>t)
\le
\sum_{i=1}^n\mathbb P(|Z_i|>t)
\le
2n\exp\!\left(-\frac{t^2}{2\tau^2}\right).
$$

取

$$
a=\tau\sqrt{2\log(2n)}.
$$

由尾积分公式 $\mathbb E[M]=\int_0^\infty\mathbb P(M>t)\,dt$，

$$
\begin{aligned}
\mathbb E[M]
&\le a+
2n\int_a^\infty
\exp\!\left(-\frac{t^2}{2\tau^2}\right)dt\\
&\le a+
2n\frac{\tau^2}{a}
\exp\!\left(-\frac{a^2}{2\tau^2}\right)\\
&=a+\frac{\tau^2}{a}.
\end{aligned}
$$

所以

$$
\mathbb E[M]
\le
\tau\left(
\sqrt{2\log(2n)}+rac1{\sqrt{2\log(2n)}}
\right)
\le
2\tau\sqrt{2\log(2n)}.
$$

这与精确的 Laplace-transform 证明只相差一个普适常数。

---

## 1.2.5 用求积公式估计期望

设 $X\sim\operatorname{Unif}[0,1]$，需要计算

$$
I=\mathbb E[f(X)]=\int_0^1f(x)\,dx.
$$

取均匀网格

$$
x_i=\frac in,\qquad i=0,1,\dots,n.
$$

梯形公式为

$$
\widehat I
=
\frac1n\left[
\frac12f(x_0)+\sum_{i=1}^{n-1}f(x_i)+\frac12f(x_n)
\right]
=
\frac1{2n}\sum_{i=1}^n\bigl[f(x_{i-1})+f(x_i)\bigr].
$$

它等价于：在每个小区间 $[x_{i-1},x_i]$ 上用端点确定的线性插值函数代替 $f$，再对该插值函数积分。

### 单区间线性插值误差

设 $g:[0,1]\to\mathbb R$，端点线性插值为

$$
\widetilde g(x)=(1-x)g(0)+xg(1).
$$

直接积分可得

$$
\int_0^1\widetilde g(x)\,dx
=
\frac{g(0)+g(1)}2.
$$

若 $g$ 二阶可微，且

$$
|g''(x)|\le L,
$$

则线性插值余项公式给出：对每个 $x\in[0,1]$，存在 $\xi_x\in(0,1)$ 使得

$$
g(x)-\widetilde g(x)
=
\frac{g''(\xi_x)}2x(x-1).
$$

因此

$$
\boxed{
|g(x)-\widetilde g(x)|
\le
\frac L2x(1-x)
}.
$$

### 梯形公式的全局误差

在长度为

$$
h=x_i-x_{i-1}=\frac1n
$$

的小区间上，缩放上述结论得到

$$
|f(x)-\widetilde f_i(x)|
\le
\frac L2(x-x_{i-1})(x_i-x).
$$

于是局部积分误差满足

$$
\begin{aligned}
\left|
\int_{x_{i-1}}^{x_i}f(x)\,dx
-
\frac h2\bigl[f(x_{i-1})+f(x_i)\bigr]
\right|
&\le
\frac L2\int_{x_{i-1}}^{x_i}
(x-x_{i-1})(x_i-x)\,dx\\
&=
\frac{Lh^3}{12}.
\end{aligned}
$$

将 $n$ 个区间相加，得到

$$
\boxed{
|I-\widehat I|
\le
\frac{L}{12n^2}
}.
$$

因此，在二阶导数一致有界时，梯形公式的误差阶为

$$
|I-\widehat I|=O(n^{-2}).
$$

若只假设一阶导数有界，一般只能得到 $O(n^{-1})$ 的误差。

---

## 主要校订

1. Bernstein 不等式的分母应为 $2\sigma^2+2ct/3$，不能把方差项或线性项的系数混写。
2. 次高斯最大值证明中的优化变量应取 $\lambda=\sqrt{2\log n}/\tau$。
3. 对绝对值最大值，应把变量数从 $n$ 改为 $2n$，故出现 $\log(2n)$。
4. 梯形公式的二阶光滑误差为 $L/(12n^2)$；单区间插值误差为 $\frac L2x(1-x)$。
