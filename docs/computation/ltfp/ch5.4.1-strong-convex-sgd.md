# LTFP Ch5 §5.4.1：强凸问题下的随机梯度下降

> 本文由手写 PDF 整理而成。Proposition 5.8 与 Exercises 5.31--5.34 的符号和常数已根据 LTFP 第 5.4.1 节校正。Exercise 5.34 在原笔记中没有完成，文末给出一条可直接验证但常数未优化的尾平均收敛界。

## 1. 问题设定

考虑正则化目标函数

$$
G(\theta)=F(\theta)+\frac\mu2\|\theta\|_2^2,
\qquad \mu>0,
$$

其中 $F:\mathbb R^d\to\mathbb R$ 凸且 $B$-Lipschitz。因而任意次梯度满足

$$
\|g\|_2\le B.
$$

设 $G$ 的唯一极小点为 $\theta^*$，并从 $\theta_0=0$ 开始迭代。

随机次梯度 $g_t(\theta_{t-1})$ 满足：

- **(H-1) 无偏性**

$$
\mathbb E[g_t(\theta_{t-1})\mid\theta_{t-1}]
\in\partial F(\theta_{t-1});
$$

- **(H-2) 有界性**

$$
\|g_t(\theta_{t-1})\|_2^2\le B^2
\quad\text{a.s.}
$$

SGD 递推为

$$
\boxed{
\theta_t
=
\theta_{t-1}
-
\gamma_t\bigl(g_t(\theta_{t-1})+\mu\theta_{t-1}\bigr)
}.
$$

---

# 2. Proposition 5.8：$O((1+\log t)/t)$ 收敛率

## 2.1 命题

取

$$
\gamma_t=\frac1{\mu t},
$$

并定义均匀平均迭代点

$$
\overline\theta_t
=
\frac1t\sum_{s=1}^t\theta_{s-1}.
$$

则

$$
\boxed{
\mathbb E\bigl[G(\overline\theta_t)-G(\theta^*)\bigr]
\le
\frac{2B^2(1+\log t)}{\mu t}
}.
$$

## 2.2 迭代点有界

递推可写成

$$
\theta_t
=(1-\mu\gamma_t)\theta_{t-1}
+
\mu\gamma_t\left(-\frac1\mu g_t(\theta_{t-1})\right).
$$

当 $\gamma_t=1/(\mu t)$ 时，$\mu\gamma_t=1/t\in(0,1]$。因此 $\theta_t$ 是

$$
\theta_{t-1}
\quad\text{与}\quad
-\frac1\mu g_t(\theta_{t-1})
$$

的凸组合。

由于

$$
\left\|-\frac1\mu g_t(\theta_{t-1})\right\|_2
\le\frac B\mu,
$$

并且 $\theta_0=0$，归纳得到

$$
\boxed{
\|\theta_t\|_2\le\frac B\mu
}.
$$

从而

$$
\|\mu\theta_{t-1}\|_2\le B
$$

以及

$$
\boxed{
\|g_t(\theta_{t-1})+\mu\theta_{t-1}\|_2^2
\le(2B)^2=4B^2
}.
$$

此外，由 $G$ 在 $\theta^*$ 处的最优性，存在 $g^*\in\partial F(\theta^*)$ 使

$$
g^*+\mu\theta^*=0.
$$

故

$$
\|\theta^*\|_2\le\frac B\mu.
$$

## 2.3 单步距离递推

记

$$
a_t=\mathbb E\|\theta_t-\theta^*\|_2^2.
$$

展开平方：

$$
\begin{aligned}
a_t
={}&a_{t-1}
-2\gamma_t\mathbb E\left[
(g_t(\theta_{t-1})+\mu\theta_{t-1})^\top
(\theta_{t-1}-\theta^*)
\right]\\
&+\gamma_t^2
\mathbb E\|g_t(\theta_{t-1})+\mu\theta_{t-1}\|_2^2.
\end{aligned}
$$

由无偏性以及上面的 $4B^2$ 界，

$$
a_t
\le
a_{t-1}
-2\gamma_t\mathbb E\left[
G'(\theta_{t-1})^\top(\theta_{t-1}-\theta^*)
\right]
+4\gamma_t^2B^2.
$$

## 2.4 使用强凸性

$G$ 是 $\mu$-强凸函数，所以

$$
G(\theta_{t-1})-G(\theta^*)
+
\frac\mu2\|\theta_{t-1}-\theta^*\|_2^2
\le
G'(\theta_{t-1})^\top(\theta_{t-1}-\theta^*).
$$

代入上一步，得到基本不等式

$$
\boxed{
\gamma_t\mathbb E[G(\theta_{t-1})-G(\theta^*)]
\le
\frac12\bigl[(1-\mu\gamma_t)a_{t-1}-a_t\bigr]
+2\gamma_t^2B^2
}.
$$

等价地，

$$
\boxed{
\mathbb E[G(\theta_{t-1})-G(\theta^*)]
\le
\frac12(\gamma_t^{-1}-\mu)a_{t-1}
-
\frac12\gamma_t^{-1}a_t
+2\gamma_tB^2
}.
$$

## 2.5 代入 $\gamma_t=1/(\mu t)$ 并求和

此时

$$
\gamma_t^{-1}=\mu t,
$$

所以

$$
\mathbb E[G(\theta_{t-1})-G(\theta^*)]
\le
\frac\mu2\left[(t-1)a_{t-1}-ta_t\right]
+
\frac{2B^2}{\mu t}.
$$

从 $t=1$ 到 $t=T$ 求和，距离项望远镜消去：

$$
\sum_{t=1}^T
\mathbb E[G(\theta_{t-1})-G(\theta^*)]
\le
\frac{2B^2}{\mu}
\sum_{t=1}^T\frac1t.
$$

利用

$$
\sum_{t=1}^T\frac1t\le1+\log T,
$$

得到

$$
\frac1T\sum_{t=1}^T
\mathbb E[G(\theta_{t-1})-G(\theta^*)]
\le
\frac{2B^2(1+\log T)}{\mu T}.
$$

最后由凸性与 Jensen 不等式，

$$
G(\overline\theta_T)
\le
\frac1T\sum_{t=1}^TG(\theta_{t-1}),
$$

故命题成立。

## 2.6 结论与注意事项

- 与一般凸问题的 $O(1/\sqrt t)$ 相比，强凸性将速率提高到 $O((\log t)/t)$。
- 步长依赖强凸参数 $\mu$。当 $\mu$ 很小时，$1/(\mu t)$ 在早期可能过大，数值波动明显。
- 加权平均可以去掉对数因子，见 Exercise 5.32。
- 对一般随机一阶 oracle，$O(B^2/(\mu t))$ 在常数意义下是最优阶。

---

# 3. Exercise 5.31：带加性噪声的随机二次型

## 3.1 问题

考虑

$$
F(\theta)=\frac12\theta^\top H\theta-c^\top\theta,
$$

其中 $H\in\mathbb R^{d\times d}$ 对称正定。最优点为

$$
\theta^*=H^{-1}c.
$$

迭代为

$$
\theta_t
=
\theta_{t-1}
-
\gamma\bigl(F'(\theta_{t-1})+\varepsilon_t\bigr),
$$

其中

$$
\mathbb E[\varepsilon_t]=0,
\qquad
\mathbb E[\varepsilon_t\varepsilon_t^\top]=C,
$$

且各 $\varepsilon_t$ 独立。

令

$$
e_t=\theta_t-\theta^*,
\qquad
A=I-\gamma H.
$$

因为

$$
F'(\theta)=H(\theta-\theta^*),
$$

所以

$$
\boxed{
e_t=Ae_{t-1}-\gamma\varepsilon_t
}.
$$

## 3.2 非平均迭代点的精确风险

展开递推：

$$
e_t=A^te_0-
\gamma\sum_{k=1}^tA^{t-k}\varepsilon_k.
$$

二次函数的超额目标为

$$
F(\theta_t)-F(\theta^*)
=\frac12e_t^\top He_t.
$$

由于噪声独立且均值为零，交叉项消失，因此

$$
\boxed{
\begin{aligned}
\mathbb E[F(\theta_t)-F(\theta^*)]
={}&\frac12e_0^\top H A^{2t}e_0\\
&+\frac{\gamma^2}{2}
\sum_{k=1}^t
\operatorname{tr}\left(
H A^{2(t-k)}C
\right).
\end{aligned}
}.
$$

若

$$
0<\gamma<\frac2{\lambda_{\max}(H)},
$$

则 $\rho(A)<1$，初始化项趋于零，并且

$$
\sum_{j=0}^\infty A^{2j}=(I-A^2)^{-1}.
$$

于是稳态误差为

$$
\begin{aligned}
\lim_{t\to\infty}
\mathbb E[F(\theta_t)-F(\theta^*)]
&=
\frac{\gamma^2}{2}
\operatorname{tr}\left[H(I-A^2)^{-1}C\right]\\
&=
\boxed{
\frac\gamma2
\operatorname{tr}\left[(2I-\gamma H)^{-1}C\right]
}.
\end{aligned}
$$

因此使用常数步长时，非平均迭代点一般不会收敛到零误差，而是在最优点附近形成稳态分布；稳态超额风险为 $O(\gamma)$。

## 3.3 平均迭代点

定义

$$
\overline\theta_t
=\frac1t\sum_{s=0}^{t-1}\theta_s,
\qquad
\overline e_t=\overline\theta_t-\theta^*.
$$

利用

$$
\sum_{s=0}^{t-1}A^s
=(I-A^t)(I-A)^{-1}
=\frac1\gamma(I-A^t)H^{-1},
$$

可得

$$
\boxed{
\overline e_t
=
\frac1{\gamma t}H^{-1}(I-A^t)e_0
-
\frac1t\sum_{k=1}^{t-1}
H^{-1}(I-A^{t-k})\varepsilon_k
}.
$$

因此

$$
\begin{aligned}
\mathbb E[F(\overline\theta_t)-F(\theta^*)]
={}&
\frac1{2\gamma^2t^2}
 e_0^\top(I-A^t)H^{-1}(I-A^t)e_0\\
&+
\frac1{2t^2}
\sum_{k=1}^{t-1}
\operatorname{tr}\left[
(I-A^{t-k})^2H^{-1}C
\right].
\end{aligned}
$$

若进一步取

$$
0<\gamma\le\frac1{\lambda_{\max}(H)},
$$

则 $0\preceq A\preceq I$，从而

$$
0\preceq(I-A^m)^2\preceq I.
$$

所以

$$
\boxed{
\mathbb E[F(\overline\theta_t)-F(\theta^*)]
\le
\frac{e_0^\top H^{-1}e_0}{2\gamma^2t^2}
+
\frac{\operatorname{tr}(H^{-1}C)}{2t}
}.
$$

平均迭代后，初始化偏差为 $O(t^{-2})$，噪声方差为 $O(t^{-1})$。

---

# 4. Exercise 5.32：线性加权平均去除对数因子

仍采用 Proposition 5.8 的假设，但令

$$
\gamma_t=\frac{2}{\mu(t+1)}.
$$

定义加权平均

$$
\boxed{
\overline\theta_t
=
\frac{2}{t(t+1)}
\sum_{s=1}^t s\theta_{s-1}
}.
$$

由基本不等式

$$
\Delta_s
:=
\mathbb E[G(\theta_{s-1})-G(\theta^*)]
\le
\frac12(\gamma_s^{-1}-\mu)a_{s-1}
-
\frac12\gamma_s^{-1}a_s
+2\gamma_sB^2,
$$

代入 $\gamma_s=2/[\mu(s+1)]$：

$$
\Delta_s
\le
\frac\mu4\left[(s-1)a_{s-1}-(s+1)a_s\right]
+
\frac{4B^2}{\mu(s+1)}.
$$

两边乘以 $s$：

$$
s\Delta_s
\le
\frac\mu4\left[s(s-1)a_{s-1}-s(s+1)a_s\right]
+
\frac{4B^2s}{\mu(s+1)}.
$$

从 $s=1$ 到 $t$ 求和，距离项完全望远镜消去，并且

$$
\frac{s}{s+1}\le1.
$$

于是

$$
\sum_{s=1}^t s\Delta_s
\le
\frac{4B^2t}{\mu}.
$$

由凸性，

$$
\mathbb E[G(\overline\theta_t)-G(\theta^*)]
\le
\frac{2}{t(t+1)}
\sum_{s=1}^ts\Delta_s.
$$

因此

$$
\boxed{
\mathbb E[G(\overline\theta_t)-G(\theta^*)]
\le
\frac{8B^2}{\mu(t+1)}
}.
$$

线性权重 $s$ 与特定步长配合，使距离项严格望远镜消去，从而去除了 $\log t$。

---

# 5. Exercise 5.33：SGD 等于样本均值

考虑

$$
F(\theta)=\frac12\mathbb E\|\theta-z\|_2^2.
$$

使用样本 $z_t$ 构造随机梯度

$$
g_t(\theta)=\theta-z_t.
$$

取步长

$$
\gamma_t=\frac1t.
$$

SGD 递推为

$$
\begin{aligned}
\theta_t
&=\theta_{t-1}-\frac1t(\theta_{t-1}-z_t)\\
&=\frac{t-1}{t}\theta_{t-1}+\frac1tz_t.
\end{aligned}
$$

当 $t=1$ 时，$\theta_1=z_1$。若归纳假设

$$
\theta_{t-1}=\frac1{t-1}\sum_{s=1}^{t-1}z_s,
$$

则

$$
\theta_t
=
\frac1t\sum_{s=1}^{t-1}z_s+\frac1tz_t
=
\boxed{
\frac1t\sum_{s=1}^tz_s
}.
$$

因此该 SGD 递推正是在线样本均值算法。

---

# 6. Exercise 5.34：不依赖预先精确选择阶段的步长

考虑

$$
\boxed{
\gamma_t=\frac1{B^2\sqrt t+\mu t}
}.
$$

该步长有两个渐近区域：

- 当 $t\ll(B^2/\mu)^2$ 时，$\gamma_t\approx1/(B^2\sqrt t)$，类似一般凸问题的 $t^{-1/2}$ 步长；
- 当 $t\gg(B^2/\mu)^2$ 时，$\gamma_t\approx1/(\mu t)$，自动进入强凸问题的 $t^{-1}$ 区域。

## 6.1 基本递推

令

$$
q_t=\gamma_t^{-1}=B^2\sqrt t+\mu t,
\qquad
a_t=\mathbb E\|\theta_t-\theta^*\|_2^2,
$$

以及

$$
\Delta_t=\mathbb E[G(\theta_{t-1})-G(\theta^*)].
$$

由 Proposition 5.8 的单步分析，

$$
\boxed{
\Delta_t
\le
\frac12(q_t-\mu)a_{t-1}
-
\frac12q_ta_t
+
\frac{2B^2}{q_t}
}.
$$

将 $q_t=\mu t+B^2\sqrt t$ 展开：

$$
\Delta_t
\le
\frac\mu2\left[(t-1)a_{t-1}-ta_t\right]
+
\frac{B^2}{2}\sqrt t\,(a_{t-1}-a_t)
+
\frac{2B^2}{B^2\sqrt t+\mu t}.
$$

困难来自第二个加权差分项，它不再直接望远镜消去。

## 6.2 尾段分析

令

$$
m=\left\lceil\max\left\{1,\left(\frac{B^2}{\mu}\right)^2\right\}\right\rceil.
$$

对 $t\ge m$，有

$$
\frac{B^2}{\mu(\sqrt t+\sqrt{t+1})}\le\frac12.
$$

对 $s=m,\ldots,T$ 求和，并对

$$
\sum_{s=m}^T\sqrt s\,(a_{s-1}-a_s)
$$

使用 Abel 求和公式：

$$
\begin{aligned}
\sum_{s=m}^T\sqrt s\,(a_{s-1}-a_s)
={}&\sqrt m\,a_{m-1}
+
\sum_{s=m}^{T-1}(\sqrt{s+1}-\sqrt s)a_s\\
&-\sqrt T\,a_T.
\end{aligned}
$$

由于 $G$ 为 $\mu$-强凸，

$$
\Delta_{s+1}
\ge\frac\mu2a_s.
$$

因此

$$
\frac{B^2}{2}(\sqrt{s+1}-\sqrt s)a_s
\le\frac12\Delta_{s+1},
\qquad s\ge m.
$$

把该项移到左侧，可得一条常数未优化的尾和界：

$$
\boxed{
\sum_{s=m}^T\Delta_s
\le
[\mu(m-1)+B^2\sqrt m]a_{m-1}
+
\frac{4B^2}{\mu}
\log\frac{eT}{m}
}.
$$

又因为

$$
\|\theta_t\|_2\le\frac B\mu,
\qquad
\|\theta^*\|_2\le\frac B\mu,
$$

所以

$$
a_{m-1}\le\frac{4B^2}{\mu^2}.
$$

定义尾平均

$$
\widetilde\theta_{m:T}
=
\frac1{T-m+1}
\sum_{s=m}^T\theta_{s-1}.
$$

由凸性，

$$
\boxed{
\begin{aligned}
\mathbb E[G(\widetilde\theta_{m:T})-G(\theta^*)]
\le{}&
\frac{4B^2[\mu(m-1)+B^2\sqrt m]}
{\mu^2(T-m+1)}\\
&+
\frac{4B^2}{\mu(T-m+1)}
\log\frac{eT}{m}.
\end{aligned}
}.
$$

对固定 $B$ 与 $\mu$，当越过约

$$
(B^2/\mu)^2
$$

次迭代的过渡尺度后，该界为

$$
O\left(\frac{B^2\log T}{\mu T}\right),
$$

而早期步长具有一般凸问题的 $t^{-1/2}$ 行为。这说明该步长不需要从一开始就在 $1/\sqrt t$ 与 $1/(\mu t)$ 两种方案之间作硬选择。

> **说明：** 上述尾平均界沿用了手写笔记中的“先越过过渡点，再吸收 Abel 求和余项”的思路，常数并未优化。Exercise 5.34 的核心是展示步长在早期一般凸区域和后期强凸区域之间的自适应过渡。
