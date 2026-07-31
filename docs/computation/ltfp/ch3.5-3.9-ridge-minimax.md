# LTFP Ch3 §3.5-3.9：岭回归与极小极大下界

> 本文由手写 PDF 整理而成。符号、命题编号与主要推导按照 Francis Bach 的 *Learning Theory from First Principles*（LTFP）第 3 章校正。原笔记中跳过的定义、缺失的中间步骤和若干矩阵次序问题已补全。

## 0. 统一记号

设特征映射为 $\varphi:X\to\mathbb R^d$，设计矩阵为

$$
\Phi=
\begin{bmatrix}
\varphi(x_1)^\top\\
\vdots\\
\varphi(x_n)^\top
\end{bmatrix}
\in\mathbb R^{n\times d},
$$

并记非中心经验协方差矩阵为

$$
\widehat\Sigma=\frac1n\Phi^\top\Phi\in\mathbb R^{d\times d}.
$$

对于半正定矩阵 $M$，记

$$
\|u\|_M^2=u^\top M u.
$$

---

# 3.5 Fixed Design Setting

## 3.5.1 模型与风险分解

在固定设计情形中，$\Phi$ 被视为确定矩阵，随机性仅来自噪声。假设

$$
y=\Phi\theta^*+\varepsilon,
\qquad
\mathbb E[\varepsilon]=0,
\qquad
\mathbb E[\varepsilon\varepsilon^\top]=\sigma^2 I_n.
$$

固定设计风险为

$$
R(\theta)=\mathbb E_y\left[\frac1n\|y-\Phi\theta\|_2^2\right].
$$

将 $y=\Phi\theta^*+\varepsilon$ 代入，得到

$$
\begin{aligned}
R(\theta)
&=\frac1n\mathbb E\|\Phi(\theta^*-\theta)+\varepsilon\|_2^2\\
&=\frac1n\|\Phi(\theta-\theta^*)\|_2^2
  +\frac1n\mathbb E\|\varepsilon\|_2^2\\
&=(\theta-\theta^*)^\top\widehat\Sigma(\theta-\theta^*)+\sigma^2.
\end{aligned}
$$

因此

$$
R^*=\sigma^2,
\qquad
R(\theta)-R^*=\|\theta-\theta^*\|_{\widehat\Sigma}^2.
$$

若估计量 $\widehat\theta$ 是随机的，则通常的偏差--方差分解给出

$$
\mathbb E[R(\widehat\theta)]-R^*
=
\|\mathbb E[\widehat\theta]-\theta^*\|_{\widehat\Sigma}^2
+
\mathbb E\|\widehat\theta-\mathbb E[\widehat\theta]\|_{\widehat\Sigma}^2.
$$

## 3.5.2 OLS 的统计性质

当 $\widehat\Sigma$ 可逆时，OLS 估计量为

$$
\widehat\theta
=(\Phi^\top\Phi)^{-1}\Phi^\top y
=\frac1n\widehat\Sigma^{-1}\Phi^\top y.
$$

由 $y=\Phi\theta^*+\varepsilon$，

$$
\widehat\theta-\theta^*
=(\Phi^\top\Phi)^{-1}\Phi^\top\varepsilon.
$$

因此

$$
\mathbb E[\widehat\theta]=\theta^*,
\qquad
\operatorname{Var}(\widehat\theta)
=\sigma^2(\Phi^\top\Phi)^{-1}
=\frac{\sigma^2}{n}\widehat\Sigma^{-1}.
$$

于是

$$
\begin{aligned}
\mathbb E[R(\widehat\theta)]-R^*
&=\mathbb E\|\widehat\theta-\theta^*\|_{\widehat\Sigma}^2\\
&=\operatorname{tr}\!\left(
\widehat\Sigma\operatorname{Var}(\widehat\theta)
\right)\\
&=\frac{\sigma^2}{n}\operatorname{tr}(I_d)
=\frac{\sigma^2d}{n}.
\end{aligned}
$$

---

# 3.6 Ridge Least-Squares Regression

## 3.6.1 定义与闭式解

给定 $\lambda>0$，岭回归估计量定义为

$$
\widehat\theta_\lambda
\in\arg\min_{\theta\in\mathbb R^d}
\left\{
\frac1n\|y-\Phi\theta\|_2^2+\lambda\|\theta\|_2^2
\right\}.
$$

一阶最优性条件为

$$
\frac2n\Phi^\top(\Phi\widehat\theta_\lambda-y)
+2\lambda\widehat\theta_\lambda=0,
$$

因此

$$
\widehat\theta_\lambda
=\frac1n(\widehat\Sigma+\lambda I)^{-1}\Phi^\top y
=(\Phi^\top\Phi+n\lambda I)^{-1}\Phi^\top y.
$$

利用矩阵求逆引理，还可以写成

$$
\widehat\theta_\lambda
=\Phi^\top(\Phi\Phi^\top+n\lambda I)^{-1}y.
$$

当 $d\gg n$ 时，后一形式只需求逆 $n\times n$ 矩阵，计算上更合适。

## 3.6.2 Proposition 3.7：岭回归的偏差--方差分解

由

$$
\widehat\theta_\lambda
=(\widehat\Sigma+\lambda I)^{-1}\widehat\Sigma\theta^*
+\frac1n(\widehat\Sigma+\lambda I)^{-1}\Phi^\top\varepsilon,
$$

可得

$$
\mathbb E[\widehat\theta_\lambda]
=(\widehat\Sigma+\lambda I)^{-1}\widehat\Sigma\theta^*
=\theta^*-\lambda(\widehat\Sigma+\lambda I)^{-1}\theta^*.
$$

### 偏差项

$$
\begin{aligned}
B
&=\|\mathbb E[\widehat\theta_\lambda]-\theta^*\|_{\widehat\Sigma}^2\\
&=\lambda^2\theta^{*\top}
(\widehat\Sigma+\lambda I)^{-1}
\widehat\Sigma
(\widehat\Sigma+\lambda I)^{-1}\theta^*.
\end{aligned}
$$

由于 $\widehat\Sigma$ 与 $(\widehat\Sigma+\lambda I)^{-1}$ 可交换，也可写成

$$
B=\lambda^2\theta^{*\top}
(\widehat\Sigma+\lambda I)^{-2}
\widehat\Sigma\theta^*.
$$

### 方差项

随机部分为

$$
\widehat\theta_\lambda-
\mathbb E[\widehat\theta_\lambda]
=\frac1n(\widehat\Sigma+\lambda I)^{-1}\Phi^\top\varepsilon.
$$

因此

$$
\begin{aligned}
V
&=\mathbb E\left\|
\widehat\theta_\lambda-
\mathbb E[\widehat\theta_\lambda]
\right\|_{\widehat\Sigma}^2\\
&=\frac{\sigma^2}{n}
\operatorname{tr}\left[
\widehat\Sigma^2(\widehat\Sigma+\lambda I)^{-2}
\right].
\end{aligned}
$$

综上，

$$
\boxed{
\mathbb E[R(\widehat\theta_\lambda)]-R^*
=
\lambda^2\theta^{*\top}(\widehat\Sigma+\lambda I)^{-2}
\widehat\Sigma\theta^*
+
\frac{\sigma^2}{n}
\operatorname{tr}\left[
\widehat\Sigma^2(\widehat\Sigma+\lambda I)^{-2}
\right]
}.
$$

## 3.6.3 Proposition 3.8：正则化参数的理论选择

对任意标量特征值 $u\ge 0$，有

$$
\frac{\lambda u}{(u+\lambda)^2}\le\frac12.
$$

因此

$$
B
=\lambda\theta^{*\top}
\left[\lambda\widehat\Sigma(\widehat\Sigma+\lambda I)^{-2}\right]
\theta^*
\le \frac\lambda2\|\theta^*\|_2^2.
$$

同理，

$$
\begin{aligned}
V
&=\frac{\sigma^2}{\lambda n}
\operatorname{tr}\left[
\widehat\Sigma\,
\lambda\widehat\Sigma(\widehat\Sigma+\lambda I)^{-2}
\right]\\
&\le \frac{\sigma^2\operatorname{tr}(\widehat\Sigma)}{2\lambda n}.
\end{aligned}
$$

故

$$
\mathbb E[R(\widehat\theta_\lambda)]-R^*
\le
\frac\lambda2\|\theta^*\|_2^2
+
\frac{\sigma^2\operatorname{tr}(\widehat\Sigma)}{2\lambda n}.
$$

右端是 $a\lambda+b/\lambda$ 型。取

$$
\boxed{
\lambda^*
=
\frac{\sigma\sqrt{\operatorname{tr}(\widehat\Sigma)}}
{\|\theta^*\|_2\sqrt n}
}
$$

得到

$$
\boxed{
\mathbb E[R(\widehat\theta_{\lambda^*})]-R^*
\le
\frac{
\sigma\sqrt{\operatorname{tr}(\widehat\Sigma)}\|\theta^*\|_2
}{\sqrt n}
}.
$$

该 $\lambda^*$ 优化的是风险上界，不一定是真实期望风险的精确最优值。

## 3.6.4 Exercise 3.6：一般二次正则项

考虑

$$
\widehat\theta_\Lambda
\in\arg\min_\theta
\left\{
\frac1n\|y-\Phi\theta\|_2^2+\theta^\top\Lambda\theta
\right\},
$$

其中 $\Lambda\in\mathbb R^{d\times d}$ 对称正定。则

$$
\boxed{
\widehat\theta_\Lambda
=(\widehat\Sigma+\Lambda)^{-1}\frac1n\Phi^\top y
}.
$$

其偏差向量为

$$
\mathbb E[\widehat\theta_\Lambda]-\theta^*
=-(\widehat\Sigma+\Lambda)^{-1}\Lambda\theta^*.
$$

因此偏差项为

$$
\boxed{
B_\Lambda
=
\theta^{*\top}\Lambda(\widehat\Sigma+\Lambda)^{-1}
\widehat\Sigma
(\widehat\Sigma+\Lambda)^{-1}\Lambda\theta^*
}.
$$

方差项为

$$
\boxed{
V_\Lambda
=
\frac{\sigma^2}{n}
\operatorname{tr}\left[
\widehat\Sigma(\widehat\Sigma+\Lambda)^{-1}
\widehat\Sigma(\widehat\Sigma+\Lambda)^{-1}
\right]
}.
$$

> **修正说明：** 当 $\Lambda$ 与 $\widehat\Sigma$ 不可交换时，不能把上式随意合并为 $(\widehat\Sigma+\Lambda)^{-2}\widehat\Sigma^2$。只有两者可交换时才可这样简化。

## 3.6.5 Exercise 3.7：留一法公式

对每个 $i$，定义

$$
\widehat\theta_\lambda^{-i}
\in\arg\min_\theta
\left\{
\frac1n\sum_{j\ne i}(y_j-\theta^\top\varphi(x_j))^2
+\lambda\|\theta\|_2^2
\right\}.
$$

记

$$
H=\Phi(\Phi^\top\Phi+n\lambda I)^{-1}\Phi^\top,
\qquad
h=\operatorname{diag}(H).
$$

令

$$
A=\Phi^\top\Phi+n\lambda I,
\qquad
b=\Phi^\top y,
\qquad
\phi_i=\varphi(x_i).
$$

则

$$
\widehat\theta_\lambda=A^{-1}b,
$$

而删去第 $i$ 个样本后，

$$
\widehat\theta_\lambda^{-i}
=(A-\phi_i\phi_i^\top)^{-1}(b-\phi_i y_i).
$$

由 Sherman--Morrison 公式，

$$
(A-\phi_i\phi_i^\top)^{-1}
=A^{-1}+\frac{A^{-1}\phi_i\phi_i^\top A^{-1}}
{1-\phi_i^\top A^{-1}\phi_i}.
$$

又因为

$$
h_i=\phi_i^\top A^{-1}\phi_i,
\qquad
\widehat y_i=\phi_i^\top\widehat\theta_\lambda=(Hy)_i,
$$

整理可得

$$
\widehat\theta_\lambda^{-i}
=\widehat\theta_\lambda
+\frac{A^{-1}\phi_i}{1-h_i}(\widehat y_i-y_i).
$$

故

$$
\boxed{
 y_i-\phi_i^\top\widehat\theta_\lambda^{-i}
=
\frac{y_i-\widehat y_i}{1-h_i}
=
\frac{[(I-H)y]_i}{1-h_i}
}.
$$

平方并求和得到

$$
\boxed{
\frac1n\sum_{i=1}^n
(y_i-\phi_i^\top\widehat\theta_\lambda^{-i})^2
=
\frac1n
\left\|
(I-\operatorname{Diag}(h))^{-1}(I-H)y
\right\|_2^2
}.
$$

---

# 3.7 Lower Bound

## 3.7.1 极小极大问题

为证明固定设计下 OLS 的 $\sigma^2d/n$ 风险是不可改进的，进一步假设

$$
\varepsilon\sim\mathcal N(0,\sigma^2I_n).
$$

对于真实参数 $\theta^*$，记

$$
R_{\theta^*}(\theta)-R^*
=\|\theta-\theta^*\|_{\widehat\Sigma}^2.
$$

任意估计算法可以写成映射

$$
A:\mathbb R^n\to\mathbb R^d,
\qquad
\widehat\theta=A(y).
$$

目标是研究

$$
\inf_A\sup_{\theta^*\in\mathbb R^d}
\mathbb E_\varepsilon
\left[
R_{\theta^*}(A(\Phi\theta^*+\varepsilon))-R^*
\right].
$$

## 3.7.2 用先验平均下界化最坏情形

选择高斯先验

$$
\theta^*\sim\mathcal N\left(0,\frac{\sigma^2}{\lambda n}I_d\right),
\qquad \lambda>0.
$$

对任意 $A$，都有

$$
\sup_{\theta^*}
\mathbb E_\varepsilon[\text{excess risk}]
\ge
\mathbb E_{\theta^*}\mathbb E_\varepsilon[\text{excess risk}].
$$

因此

$$
\inf_A\sup_{\theta^*}\mathbb E_\varepsilon[\text{excess risk}]
\ge
\inf_A
\mathbb E_{\theta^*,\varepsilon}
\|A(y)-\theta^*\|_{\widehat\Sigma}^2.
$$

给定 $y$ 后，使条件平方损失最小的估计量是后验均值

$$
A^*(y)=\mathbb E[\theta^*\mid y].
$$

## 3.7.3 后验均值等于岭回归

似然与先验分别满足

$$
p(y\mid\theta^*)
\propto
\exp\left(-\frac{\|y-\Phi\theta^*\|_2^2}{2\sigma^2}\right),
$$

$$
p(\theta^*)
\propto
\exp\left(-\frac{\lambda n\|\theta^*\|_2^2}{2\sigma^2}\right).
$$

因此后验密度为

$$
p(\theta^*\mid y)
\propto
\exp\left[
-\frac{
\|y-\Phi\theta^*\|_2^2+n\lambda\|\theta^*\|_2^2
}{2\sigma^2}
\right].
$$

后验为高斯分布，所以后验均值等于后验众数。后验众数正是岭回归解：

$$
\boxed{
A^*(y)
=(\Phi^\top\Phi+n\lambda I)^{-1}\Phi^\top y
}.
$$

## 3.7.4 贝叶斯风险计算

将

$$
A^*(y)-\theta^*
=(\Phi^\top\Phi+n\lambda I)^{-1}\Phi^\top\varepsilon
-n\lambda(\Phi^\top\Phi+n\lambda I)^{-1}\theta^*
$$

代入。由于 $\varepsilon$ 与 $\theta^*$ 独立且均值为零，交叉项为零。计算偏差与方差后得到

$$
\inf_A
\mathbb E_{\theta^*,\varepsilon}
\|A(y)-\theta^*\|_{\widehat\Sigma}^2
=
\frac{\sigma^2}{n}
\operatorname{tr}\left[
(\widehat\Sigma+\lambda I)^{-1}\widehat\Sigma
\right].
$$

若 $\Phi$ 满列秩，则令 $\lambda\downarrow0$，有

$$
(\widehat\Sigma+\lambda I)^{-1}\widehat\Sigma\to I_d.
$$

因此

$$
\boxed{
\inf_A\sup_{\theta^*\in\mathbb R^d}
\mathbb E_\varepsilon
\left[
R_{\theta^*}(A(\Phi\theta^*+\varepsilon))-R^*
\right]
\ge \frac{\sigma^2d}{n}
}.
$$

OLS 恰好达到同样的上界，因而在该固定设计、高斯噪声、最坏参数意义下是极小极大最优的。

若 $\Phi$ 不满列秩，上述极限为

$$
\frac{\sigma^2}{n}\operatorname{rank}(\Phi).
$$

---

# 3.8 Random Design Analysis

## 3.8.1 随机设计模型

现在 $(x_i,y_i)$ 为 i.i.d. 样本，并假设

$$
y_i=\varphi(x_i)^\top\theta^*+\varepsilon_i,
$$

其中 $\varepsilon_i$ 与 $x_i$ 独立，且

$$
\mathbb E[\varepsilon_i]=0,
\qquad
\mathbb E[\varepsilon_i^2]=\sigma^2.
$$

定义总体非中心协方差矩阵

$$
\Sigma=\mathbb E[\varphi(x)\varphi(x)^\top].
$$

## 3.8.2 Proposition 3.9：随机设计风险

对独立测试样本 $(x_0,y_0)$，

$$
\begin{aligned}
R(\theta)
&=\mathbb E[(y_0-\theta^\top\varphi(x_0))^2]\\
&=\mathbb E[((\theta^*-\theta)^\top\varphi(x_0)+\varepsilon_0)^2]\\
&=(\theta-\theta^*)^\top\Sigma(\theta-\theta^*)+\sigma^2.
\end{aligned}
$$

故

$$
\boxed{
R^*=\sigma^2,
\qquad
R(\theta)-R^*=\|\theta-\theta^*\|_\Sigma^2
}.
$$

固定设计与随机设计的关键差别是：风险中的矩阵由 $\widehat\Sigma$ 换成了 $\Sigma$。

## 3.8.3 Proposition 3.10：随机设计下 OLS 风险

条件于训练输入 $x_1,\ldots,x_n$，有

$$
\widehat\theta
=\theta^*+\frac1n\widehat\Sigma^{-1}\Phi^\top\varepsilon.
$$

因此

$$
\begin{aligned}
\mathbb E[R(\widehat\theta)]-R^*
&=\mathbb E\|\widehat\theta-\theta^*\|_\Sigma^2\\
&=\frac{\sigma^2}{n}
\mathbb E\operatorname{tr}(\Sigma\widehat\Sigma^{-1}).
\end{aligned}
$$

即

$$
\boxed{
\mathbb E[R(\widehat\theta)]-R^*
=
\frac{\sigma^2}{n}
\mathbb E\left[\operatorname{tr}(\Sigma\widehat\Sigma^{-1})\right]
}.
$$

这里的期望同时包含训练输入与噪声的随机性。

## 3.8.4 Exercise 3.8：随机设计下岭回归

条件于 $\Phi$，

$$
\widehat\theta_\lambda-\theta^*
=-\lambda(\widehat\Sigma+\lambda I)^{-1}\theta^*
+
\frac1n(\widehat\Sigma+\lambda I)^{-1}\Phi^\top\varepsilon.
$$

因此

$$
\boxed{
\begin{aligned}
\mathbb E[R(\widehat\theta_\lambda)]-R^*
={}&\lambda^2\mathbb E\left[
\theta^{*\top}(\widehat\Sigma+\lambda I)^{-1}
\Sigma
(\widehat\Sigma+\lambda I)^{-1}\theta^*
\right]\\
&+\frac{\sigma^2}{n}\mathbb E\left[
\operatorname{tr}\left(
(\widehat\Sigma+\lambda I)^{-2}\Sigma\widehat\Sigma
\right)
\right].
\end{aligned}
}.
$$

> 第二项的写法利用了迹的循环不变性，以及 $\widehat\Sigma$ 与 $(\widehat\Sigma+\lambda I)^{-1}$ 可交换；$\Sigma$ 一般不与它们交换。

## 3.8.5 Gaussian Designs 与 Wishart 分布

假设

$$
\varphi(x)\sim\mathcal N(0,\Sigma).
$$

令

$$
z=\Sigma^{-1/2}\varphi(x)\sim\mathcal N(0,I_d),
$$

并令 $Z\in\mathbb R^{n\times d}$ 的每一行为 $z_i^\top$。则

$$
\Phi=Z\Sigma^{1/2},
$$

从而

$$
\widehat\Sigma
=\frac1n\Sigma^{1/2}Z^\top Z\Sigma^{1/2}.
$$

因此

$$
\operatorname{tr}(\Sigma\widehat\Sigma^{-1})
=n\operatorname{tr}((Z^\top Z)^{-1}).
$$

注意

$$
\mathbb E[Z^\top Z]=nI_d.
$$

函数 $M\mapsto\operatorname{tr}(M^{-1})$ 在正定锥上是凸的，所以 Jensen 不等式给出

$$
\mathbb E\operatorname{tr}((Z^\top Z)^{-1})
\ge
\operatorname{tr}\left((\mathbb E[Z^\top Z])^{-1}\right)
=\frac dn.
$$

但这是下界，方向不能用于证明所需的风险上界。

由于

$$
Z^\top Z\sim W_d(n,I_d)
$$

服从 Wishart 分布，并且当 $n>d+1$ 时

$$
\mathbb E[(Z^\top Z)^{-1}]
=\frac1{n-d-1}I_d,
$$

所以

$$
\mathbb E\operatorname{tr}((Z^\top Z)^{-1})
=\frac d{n-d-1}.
$$

最终得到精确风险

$$
\boxed{
\mathbb E[R(\widehat\theta)]-R^*
=\frac{\sigma^2d}{n-d-1}
=\frac{\sigma^2d/n}{1-(d+1)/n}
},
\qquad n>d+1.
$$

当 $n\to\infty$ 且 $d$ 固定时，它渐近等价于 $\sigma^2d/n$；当 $d/n$ 接近 $1$ 时，风险会显著放大。

## 3.8.6 Proposition 3.11：矩阵 Bernstein 不等式

设 $M_1,\ldots,M_n\in\mathbb R^{d\times d}$ 为独立对称随机矩阵，满足

$$
\mathbb E[M_i]=0,
\qquad
\lambda_{\max}(M_i)\le b
\quad\text{a.s.}
$$

定义

$$
\tau^2
=\lambda_{\max}\left(
\frac1n\sum_{i=1}^n\mathbb E[M_i^2]
\right).
$$

则对所有 $t\ge0$，

$$
\boxed{
\mathbb P\left(
\lambda_{\max}\left(\frac1n\sum_{i=1}^nM_i\right)\ge t
\right)
\le
 d\exp\left(
-\frac{nt^2/2}{\tau^2+bt/3}
\right)
}.
$$

### 推导骨架

矩阵情形不能直接把 $\exp(s\sum_iM_i)$ 分解成乘积。关键工具是 Tropp 型矩阵 Laplace 变换界：

$$
\mathbb E\operatorname{tr}\exp\left(s\sum_{i=1}^nM_i\right)
\le
\operatorname{tr}\exp\left(
\sum_{i=1}^n\log\mathbb E e^{sM_i}
\right).
$$

由 $\lambda_{\max}(M_i)\le b$ 和 $\mathbb E[M_i]=0$，可得矩阵 mgf 上界

$$
\log\mathbb E e^{sM_i}
\preceq
\frac{e^{sb}-sb-1}{b^2}\mathbb E[M_i^2].
$$

于是

$$
\mathbb P\left(
\lambda_{\max}\left(\sum_iM_i\right)\ge nt
\right)
\le
 d\inf_{s>0}
\exp\left[
-nst+\frac{n\tau^2}{b^2}(e^{sb}-sb-1)
\right].
$$

优化得到 Bennett 形式

$$
 d\exp\left[-\frac{n\tau^2}{b^2}h\left(\frac{bt}{\tau^2}\right)\right],
$$

其中

$$
h(u)=(1+u)\log(1+u)-u.
$$

再使用

$$
h(u)\ge\frac{u^2}{2(1+u/3)},
\qquad u\ge0,
$$

即得到上述 Bernstein 形式。

## 3.8.7 Proposition 3.12：经验协方差的下谱界

设

$$
\Sigma=\mathbb E[\varphi(x)\varphi(x)^\top]
$$

可逆，并假设存在 $\rho>0$，使得

$$
\boxed{
\mathbb E\left[
\varphi(x)^\top\Sigma^{-1}\varphi(x)
\,\varphi(x)\varphi(x)^\top
\right]
\preceq \rho d\,\Sigma
}.
$$

令

$$
z=\Sigma^{-1/2}\varphi(x).
$$

则

$$
\mathbb E[zz^\top]=I,
\qquad
\mathbb E[\|z\|_2^2zz^\top]\preceq\rho dI.
$$

取

$$
M_i=I-z_iz_i^\top.
$$

有

$$
\mathbb E[M_i]=0,
\qquad
\lambda_{\max}(M_i)\le1,
$$

且

$$
\mathbb E[M_i^2]
=
\mathbb E[\|z_i\|_2^2z_iz_i^\top]-I
\preceq\rho dI.
$$

由矩阵 Bernstein，

$$
\mathbb P\left(
\lambda_{\max}\left(
I-\frac1n\sum_{i=1}^nz_iz_i^\top
\right)\ge t
\right)
\le
 d\exp\left[-\frac{nt^2/2}{\rho d+t/3}\right].
$$

取 $t=3/4$。若

$$
\boxed{
n\ge5\rho d\log\frac d\delta
},
$$

则以至少 $1-\delta$ 的概率，

$$
\frac1n\sum_{i=1}^nz_iz_i^\top\succeq\frac14I.
$$

等价地，

$$
\boxed{
\Sigma^{-1/2}\widehat\Sigma\Sigma^{-1/2}
\succeq\frac14I
}.
$$

在该事件上，

$$
\widehat\Sigma^{-1}
\preceq4\Sigma^{-1},
$$

所以条件于训练输入的 OLS 超额风险满足

$$
\frac{\sigma^2}{n}
\operatorname{tr}(\Sigma\widehat\Sigma^{-1})
\le
\frac{4\sigma^2d}{n}.
$$

---

# 3.9 Principal Component Analysis

## 3.9.1 PCA 的优化问题

给定 $\Phi\in\mathbb R^{n\times d}$，希望找到一个 $k$ 维线性子空间，使所有特征向量到该子空间的投影误差最小。

用列正交矩阵

$$
V\in\mathbb R^{d\times k},
\qquad
V^\top V=I_k
$$

表示该子空间。投影矩阵为 $VV^\top$，于是 PCA 求解

$$
\min_{V^\top V=I_k}
\|\Phi-\Phi VV^\top\|_F^2.
$$

展开：

$$
\begin{aligned}
\|\Phi-\Phi VV^\top\|_F^2
&=\operatorname{tr}\left[(\Phi-\Phi VV^\top)^\top
(\Phi-\Phi VV^\top)\right]\\
&=\operatorname{tr}(\Phi^\top\Phi)
-\operatorname{tr}(V^\top\Phi^\top\Phi V).
\end{aligned}
$$

因此等价于

$$
\max_{V^\top V=I_k}
\operatorname{tr}(V^\top\Phi^\top\Phi V).
$$

若

$$
\widehat\Sigma
=Q\operatorname{Diag}(\lambda_1,\ldots,\lambda_d)Q^\top,
\qquad
\lambda_1\ge\cdots\ge\lambda_d,
$$

则最优 $V$ 可取为前 $k$ 个特征向量

$$
V_k=[q_1,\ldots,q_k].
$$

最小重构误差为

$$
\boxed{
\min_{V^\top V=I_k}
\|\Phi-\Phi VV^\top\|_F^2
=n\sum_{j=k+1}^d\lambda_j
}.
$$

若使用奇异值分解

$$
\Phi=U\operatorname{Diag}(s_1,\ldots,s_r)V^\top,
$$

则 $\lambda_j=s_j^2/n$，PCA 重构矩阵为

$$
\Phi V_kV_k^\top
=U_k\operatorname{Diag}(s_1,\ldots,s_k)V_k^\top.
$$

## 3.9.2 Exercise 3.9：低秩分解与交替最小化

考虑

$$
\min_{A\in\mathbb R^{n\times k},\,D\in\mathbb R^{k\times d}}
\|\Phi-AD\|_F^2.
$$

因为 $\operatorname{rank}(AD)\le k$，该问题等价于寻找 $\Phi$ 的最佳秩 $k$ 逼近。由 Eckart--Young 定理，最优乘积为

$$
\boxed{
A^*D^*=U_k\operatorname{Diag}(s_1,\ldots,s_k)V_k^\top
=\Phi V_kV_k^\top
}.
$$

分解 $(A^*,D^*)$ 本身不唯一：对任意可逆 $T\in\mathbb R^{k\times k}$，

$$
A^*D^*=(A^*T)(T^{-1}D^*).
$$

### 交替最小化更新

固定 $D_t$，最小化 $\|\Phi-AD_t\|_F^2$：

$$
\boxed{
A_t=\Phi D_t^\top(D_tD_t^\top)^{-1}
},
$$

假设 $D_t$ 满行秩。

固定 $A_t$，最小化 $\|\Phi-A_tD\|_F^2$：

$$
\boxed{
D_{t+1}=(A_t^\top A_t)^{-1}A_t^\top\Phi
},
$$

假设 $A_t$ 满列秩。

### 行空间的演化

令

$$
C=\Phi^\top\Phi.
$$

代入 $A_t$ 后可化为

$$
D_{t+1}=L_tD_tC,
$$

其中 $L_t\in\mathbb R^{k\times k}$ 可逆。因此左乘 $L_t$ 不改变行空间，故

$$
\operatorname{row}(D_{t+1})
=
\operatorname{row}(D_tC).
$$

递推得到

$$
\operatorname{row}(D_t)
=
\operatorname{row}(D_0C^t).
$$

这正是对子空间进行的幂迭代。

设

$$
C=V
\begin{bmatrix}
\Lambda_1&0\\
0&\Lambda_2
\end{bmatrix}
V^\top,
$$

其中 $\Lambda_1=\operatorname{Diag}(s_1^2,\ldots,s_k^2)$。写成

$$
D_0V=[B_1\;B_2].
$$

只要 $B_1$ 可逆，就有

$$
\operatorname{row}(D_0C^t)
=
\operatorname{row}\left(
[I\;E_t]V^\top
\right),
$$

其中

$$
E_t
=\Lambda_1^{-t}B_1^{-1}B_2\Lambda_2^t.
$$

若存在谱隙 $s_k>s_{k+1}$，则

$$
\|E_t\|_{\mathrm{op}}
\le
\|B_1^{-1}B_2\|_{\mathrm{op}}
\left(\frac{s_{k+1}^2}{s_k^2}\right)^t
\longrightarrow0.
$$

于是

$$
\operatorname{row}(D_t)\to\operatorname{span}(v_1,\ldots,v_k),
$$

从而

$$
A_tD_t
=\Phi P_{\operatorname{row}(D_t)}
\longrightarrow
\Phi V_kV_k^\top.
$$

“几乎所有初始化”来自条件 $\det(B_1)\ne0$：使 $B_1$ 奇异的初始化构成测度为零的代数集合。

若 $s_k=s_{k+1}$，最优主子空间不唯一；算法仍可收敛到某个最优的主不变子空间，但不能要求收敛到唯一指定的 $\operatorname{span}(v_1,\ldots,v_k)$。

## 3.9.3 Exercise 3.10：K-means 的交替更新

考虑

$$
\min_{A,D}\|\Phi-AD\|_F^2,
$$

其中

$$
A\in\{0,1\}^{n\times k},
\qquad
\sum_{j=1}^kA_{ij}=1,
$$

而 $D\in\mathbb R^{k\times d}$ 的第 $j$ 行 $d_j^\top$ 表示第 $j$ 个聚类中心。

目标函数展开为

$$
\|\Phi-AD\|_F^2
=
\sum_{i=1}^n\sum_{j=1}^k
A_{ij}\|\varphi(x_i)-d_j\|_2^2.
$$

### 固定 $D$ 更新 $A$

每个样本分配给最近的中心：

$$
\boxed{
A_{ij}=1
\quad\Longleftrightarrow\quad
j\in\arg\min_{\ell\in\{1,\ldots,k\}}
\|\varphi(x_i)-d_\ell\|_2^2
}.
$$

### 固定 $A$ 更新 $D$

对每个非空簇，中心取簇内均值：

$$
\boxed{
d_j
=
\frac{\sum_{i=1}^nA_{ij}\varphi(x_i)}
{\sum_{i=1}^nA_{ij}}
}.
$$

若某个簇为空，则分母为零，需要重新初始化该中心或采用其他空簇处理规则。

## 3.9.4 PCA 后的最小二乘回归

取 PCA 的前 $k$ 个特征向量组成 $V\in\mathbb R^{d\times k}$，使用降维特征矩阵 $\Phi V$。考虑

$$
\min_{\eta\in\mathbb R^k}
\|y-\Phi V\eta\|_2^2.
$$

闭式解为

$$
\widehat\eta
=(V^\top\Phi^\top\Phi V)^{-1}V^\top\Phi^\top y,
$$

预测向量为

$$
\widehat y_{
m PCA}
=
\Phi V(V^\top\Phi^\top\Phi V)^{-1}V^\top\Phi^\top y.
$$

在固定设计线性模型 $y=\Phi\theta^*+\varepsilon$ 下，

$$
\begin{aligned}
\frac1n\mathbb E_\varepsilon
\|\widehat y_{\rm PCA}-\Phi\theta^*\|_2^2
={}&\frac{\sigma^2k}{n}\\
&+\frac1n\left\|
\Phi V(V^\top\Phi^\top\Phi V)^{-1}
V^\top\Phi^\top\Phi\theta^*
-\Phi\theta^*
\right\|_2^2.
\end{aligned}
$$

由于 $V$ 由 $\widehat\Sigma$ 的特征向量组成，

$$
\widehat\Sigma V=VD,
\qquad
V^\top\widehat\Sigma V=D,
$$

因此偏差项化简为

$$
\theta^{*\top}(I-VV^\top)
\widehat\Sigma
(I-VV^\top)\theta^*.
$$

于是

$$
\boxed{
\frac1n\mathbb E_\varepsilon
\|\widehat y_{\rm PCA}-\Phi\theta^*\|_2^2
=
\frac{\sigma^2k}{n}
+
\theta^{*\top}(I-VV^\top)
\widehat\Sigma
(I-VV^\top)\theta^*
}.
$$

若 $\lambda_{k+1}$ 是 $\widehat\Sigma$ 的第 $k+1$ 大特征值，则

$$
\theta^{*\top}(I-VV^\top)
\widehat\Sigma
(I-VV^\top)\theta^*
\le
\lambda_{k+1}\|\theta^*\|_2^2.
$$

又因为

$$
\lambda_{k+1}
\le\frac{\operatorname{tr}(\widehat\Sigma)}{k+1}
\le\frac{\operatorname{tr}(\widehat\Sigma)}k,
$$

所以

$$
\boxed{
\frac1n\mathbb E_\varepsilon
\|\widehat y_{\rm PCA}-\Phi\theta^*\|_2^2
\le
\frac{\sigma^2k}{n}
+
\frac{\operatorname{tr}(\widehat\Sigma)}k\|\theta^*\|_2^2
}.
$$

最小化 $ak+b/k$ 型上界，理论上应选

$$
\boxed{
k^*
\approx
\frac{\|\theta^*\|_2
\sqrt{n\operatorname{tr}(\widehat\Sigma)}}{\sigma}
}.
$$

代入后得到与岭回归同阶的界

$$
\boxed{
\frac1n\mathbb E_\varepsilon
\|\widehat y_{\rm PCA}-\Phi\theta^*\|_2^2
\lesssim
\frac{\sigma\|\theta^*\|_2
\sqrt{\operatorname{tr}(\widehat\Sigma)}}{\sqrt n}
}.
$$

PCA 是“硬截断”小特征值方向；岭回归则对各特征方向进行连续的“软收缩”。
