# LFTP 第 5.3 节：Exercises 5.22–5.25

> 对应教材：*Learning Theory from First Principles*，§5.3，Exercises 5.22–5.25。  
> 本文根据手写笔记整理，按原题顺序补全推导，并修正记号与若干计算笔误。

## Exercise 5.22：Mirror Descent 与 Bregman 散度

设 $F:\mathbb{R}^d\to\mathbb{R}$ 可微，$\psi:\mathbb{R}^d\to\mathbb{R}$ 严格凸。

---

### 1. 欧氏梯度下降是一个局部模型的精确极小化

考虑关于 $\eta$ 的函数

$$
Q(\eta)
=
F(\theta)
+F'(\theta)^\top(\eta-\theta)
+\frac1{2\gamma}\|\eta-\theta\|_2^2.
$$

其中前两项构成 $F$ 在 $\theta$ 处的一阶近似，二次项限制更新不能离 $\theta$ 太远。

对 $\eta$ 求梯度：

$$
Q'(\eta)
=
F'(\theta)+\frac1\gamma(\eta-\theta).
$$

令 $Q'(\eta)=0$，得到

$$
\boxed{
\eta=\theta-\gamma F'(\theta)
}.
$$

由于

$$
Q''(\eta)=\frac1\gamma I\succ0,
$$

该驻点是唯一全局最小点。因此普通梯度下降等价于极小化“线性化目标 + 欧氏二次近端项”。

---

### 2. Bregman 散度的非负性

定义

$$
D_\psi(\eta,\theta)
=
\psi(\eta)-\psi(\theta)-\psi'(\theta)^\top(\eta-\theta).
$$

由凸函数的一阶条件，

$$
\psi(\eta)
\ge
\psi(\theta)+\psi'(\theta)^\top(\eta-\theta),
$$

因此

$$
\boxed{D_\psi(\eta,\theta)\ge0}.
$$

若 $\psi$ 严格凸，则当 $\eta\ne\theta$ 时，一阶支撑不等式严格成立，所以

$$
D_\psi(\eta,\theta)=0
\quad\Longleftrightarrow\quad
\eta=\theta.
$$

注意：Bregman 散度一般不对称，也通常不满足三角不等式，因此并不是度量。

---

### 3. 一般 Bregman 几何下的更新

考虑

$$
\eta
\in
\arg\min_{\zeta}
\left\{
F(\theta)
+F'(\theta)^\top(\zeta-\theta)
+\frac1\gamma D_\psi(\zeta,\theta)
\right\}.
$$

去掉与 $\zeta$ 无关的常数后，等价于极小化

$$
F'(\theta)^\top\zeta
+
\frac1\gamma
\left[
\psi(\zeta)-\psi'(\theta)^\top\zeta
\right].
$$

一阶最优性条件为

$$
F'(\theta)
+
\frac1\gamma
\bigl(\psi'(\eta)-\psi'(\theta)\bigr)
=0.
$$

即

$$
\boxed{
\psi'(\eta)
=
\psi'(\theta)-\gamma F'(\theta)
}.
$$

若 $\psi$ 只定义在开凸集 $K\subset\mathbb{R}^d$ 上，并且

$$
\psi':K\to\mathbb{R}^d
$$

是双射，则右端

$$
u=\psi'(\theta)-\gamma F'(\theta)
$$

对应唯一的

$$
\eta=(\psi')^{-1}(u)\in K.
$$

因为目标关于 $\eta$ 严格凸，该点就是唯一全局最小点。这就是 Mirror Descent 的基本更新形式。

---

### 4. 负熵势函数给出乘法更新

取定义域 $K=\mathbb{R}_{++}^d$，并令

$$
\psi(\theta)
=
\sum_{i=1}^d\theta_i\log\theta_i.
$$

其梯度为

$$
\psi'(\theta)_i=1+\log\theta_i.
$$

Mirror Descent 条件给出

$$
1+\log\eta_i
=
1+\log\theta_i-
\gamma F_i'(\theta).
$$

因此

$$
\boxed{
\eta_i
=
\theta_i\exp\bigl(-\gamma F_i'(\theta)\bigr)
}.
$$

写成向量形式：

$$
\boxed{
\theta_{t+1}
=
\theta_t\odot
\exp\bigl(-\gamma_tF'(\theta_t)\bigr)
},
$$

其中 $\odot$ 和指数均按坐标作用。

这里没有自动出现归一化因子；只有当额外约束 $\theta$ 位于概率单纯形时，才需要在乘法更新后归一化。

---

## Exercise 5.23：均匀平均迭代的无对数收敛界

沿用 Exercise 5.21 的假设。设 $K$ 是闭凸集，直径为

$$
D=\sup_{x,y\in K}\|x-y\|_2,
$$

且 $F$ 为凸的 $B$-Lipschitz 函数。考虑投影次梯度法

$$
\theta_s
=
\Pi_K\bigl(\theta_{s-1}-\gamma_sg_{s-1}\bigr),
\qquad
\gamma_s=\frac{D}{B\sqrt s},
$$

以及均匀平均

$$
\bar\theta_t
=
\frac1t\sum_{s=0}^{t-1}\theta_s.
$$

目标是证明

$$
\boxed{
F(\bar\theta_t)-F(\theta^*)
\le
\frac{3BD}{2\sqrt t}
}.
$$

### 1. 基本不等式

投影的非扩张性给出

$$
2\gamma_s
\bigl(F(\theta_{s-1})-F(\theta^*)\bigr)
\le
\|\theta_{s-1}-\theta^*\|_2^2
-
\|\theta_s-\theta^*\|_2^2
+
\gamma_s^2B^2.
$$

记

$$
a_s=\|\theta_s-\theta^*\|_2^2.
$$

由于 $\theta_s,\theta^*\in K$，有 $0\le a_s\le D^2$。两边除以 $\gamma_s$ 并求和：

$$
2\sum_{s=1}^t
\bigl(F(\theta_{s-1})-F(\theta^*)\bigr)
\le
\sum_{s=1}^t\frac{a_{s-1}-a_s}{\gamma_s}
+
B^2\sum_{s=1}^t\gamma_s.
$$

### 2. Abel 求和处理非等步长项

由于 $\gamma_s$ 递减，$1/\gamma_s$ 递增，并且

$$
\begin{aligned}
\sum_{s=1}^t\frac{a_{s-1}-a_s}{\gamma_s}
&=
\frac{a_0}{\gamma_1}
+
\sum_{s=1}^{t-1}
\left(
\frac1{\gamma_{s+1}}-rac1{\gamma_s}
\right)a_s
-
\frac{a_t}{\gamma_t}\\
&\le
D^2\left[
\frac1{\gamma_1}
+
\sum_{s=1}^{t-1}
\left(
\frac1{\gamma_{s+1}}-rac1{\gamma_s}
\right)
\right]\\
&=
\frac{D^2}{\gamma_t}
=BD\sqrt t.
\end{aligned}
$$

另一方面，

$$
B^2\sum_{s=1}^t\gamma_s
=BD\sum_{s=1}^t\frac1{\sqrt s}
\le2BD\sqrt t.
$$

故

$$
2\sum_{s=1}^t
\bigl(F(\theta_{s-1})-F(\theta^*)\bigr)
\le3BD\sqrt t.
$$

除以 $2t$：

$$
\frac1t\sum_{s=1}^t
\bigl(F(\theta_{s-1})-F(\theta^*)\bigr)
\le
\frac{3BD}{2\sqrt t}.
$$

最后利用凸性和 Jensen 不等式：

$$
F(\bar\theta_t)
\le
\frac1t\sum_{s=1}^t F(\theta_{s-1}),
$$

得到结论。

---

## 固定 horizon 的常数步长

若预先知道总迭代次数 $T$，采用常数步长 $\gamma$，则基本不等式直接给出

$$
F(\bar\theta_T)-F(\theta^*)
\le
\frac{D^2}{2\gamma T}
+
\frac{\gamma B^2}{2}.
$$

右侧关于 $\gamma$ 的最优选择是

$$
\gamma=\frac{D}{B\sqrt T},
$$

从而

$$
\boxed{
F(\bar\theta_T)-F(\theta^*)
\le
\frac{BD}{\sqrt T}
}.
$$

它去掉了 $\log T$，但步长依赖预先指定的 horizon $T$，因此本身不是 anytime 算法。

---

## Exercise 5.24：Doubling trick

第 $k$ 个阶段运行 $2^k$ 次次梯度迭代，并在整个阶段使用常数步长

$$
\gamma_k
=
\frac{D}{B\sqrt{2^k}},
\qquad k=0,1,2,\dots.
$$

对一个完整的、长度为 $N=2^k$ 的阶段，常数步长结论给出

$$
\min_{\text{该阶段内 }s}
\bigl(F(\theta_s)-F(\theta^*)\bigr)
\le
\frac{BD}{\sqrt N}.
$$

现在任取总迭代时刻 $t\ge2$。设当前处于第 $k$ 个阶段。前一个完整阶段的长度为

$$
N=2^{k-1}.
$$

由于当前阶段结束前总迭代数小于 $2^{k+1}$，有

$$
t<2^{k+1}=4N,
\qquad	ext{所以}\qquad
N>\frac t4.
$$

因此截至时刻 $t$ 已观察到的最佳函数值满足

$$
\begin{aligned}
\min_{0\le s<t}
\bigl(F(\theta_s)-F(\theta^*)\bigr)
&\le
\frac{BD}{\sqrt N}\\
&\le
\frac{2BD}{\sqrt t}.
\end{aligned}
$$

对 $t=1$ 的情形可直接并入常数。因此 doubling trick 构造了一个 anytime 算法，并保持

$$
\boxed{
O\!\left(\frac{BD}{\sqrt t}\right)
}
$$

的收敛速度。若使用随机次梯度，上述函数值相应替换为期望函数值。

---

## Exercise 5.25：正则化 Logistic Regression 与 SVM 的全部常数

假设

$$
y_i\in\{-1,1\},
\qquad
\|x_i\|_2\le R,
\qquad
\theta_0=0.
$$

统一考虑

$$
F(\theta)
=
\frac1n\sum_{i=1}^n
\Phi(y_i\theta^\top x_i)
+
\frac\lambda2\|\theta\|_2^2,
$$

其中

- Logistic loss：$\Phi(u)=\log(1+e^{-u})$；
- Hinge loss：$\Phi(u)=(1-u)_+$。

两种损失都满足其次梯度关于 $u$ 的绝对值不超过 $1$。因此单个样本损失关于 $\theta$ 的次梯度范数不超过 $R$。

### 1. 最优解范数的驻点估计

最优性条件为

$$
0
\in
\frac1n\sum_{i=1}^n
\partial_\theta\Phi(y_i\theta^{*\top}x_i)
+
\lambda\theta^*.
$$

数据损失部分的平均次梯度范数至多为 $R$，所以

$$
\lambda\|\theta^*\|_2\le R.
$$

因此

$$
\boxed{
D=\|\theta^*-\theta_0\|_2
=\|\theta^*\|_2
\le\frac R\lambda
}.
$$

### 2. 最优解范数的函数值估计

由于 $F(\theta^*)\le F(0)$，

$$
\frac\lambda2\|\theta^*\|_2^2
\le
F(0).
$$

对 Logistic regression，$F(0)=\log2$，故

$$
D_{\mathrm{log}}
\le
\sqrt{\frac{2\log2}{\lambda}}.
$$

对 SVM，$F(0)=1$，故

$$
D_{\mathrm{svm}}
\le
\sqrt{\frac2\lambda}.
$$

综合两种估计，可取

$$
\boxed{
D_{\mathrm{log}}
=
\min\left\{
\frac R\lambda,
\sqrt{\frac{2\log2}{\lambda}}
\right\}
},
$$

$$
\boxed{
D_{\mathrm{svm}}
=
\min\left\{
\frac R\lambda,
\sqrt{\frac2\lambda}
\right\}
}.
$$

### 3. Lipschitz 常数 $B$

正则项使 $F$ 在整个 $\mathbb{R}^d$ 上并非全局 Lipschitz。严谨做法是在包含最优解的球

$$
K_D=\{\theta:\|\theta\|_2\le D\}
$$

上使用投影次梯度法。

对 $\theta\in K_D$，任一次梯度 $g(\theta)$ 满足

$$
\|g(\theta)\|_2
\le
R+\lambda\|\theta\|_2
\le
R+\lambda D.
$$

因此可取

$$
\boxed{B=R+\lambda D}.
$$

使用较简单的 $D\le R/\lambda$，得到统一常数

$$
\boxed{B\le2R}.
$$

### 4. 步长和优化误差

固定 horizon $T$ 时，取

$$
\gamma
=
\frac{D}{B\sqrt T}.
$$

则

$$
F(\bar\theta_T)-F(\theta^*)
\le
\frac{BD}{\sqrt T}.
$$

使用统一估计 $D=R/\lambda$、$B=2R$，得到

$$
\boxed{
\gamma
=
\frac1{2\lambda\sqrt T}
},
$$

以及

$$
\boxed{
F(\bar\theta_T)-F(\theta^*)
\le
\frac{2R^2}{\lambda\sqrt T}
}.
$$

使用 anytime 步长

$$
\gamma_t
=
\frac1{2\lambda\sqrt t}
$$

时，Proposition 5.6 给出

$$
\min_{0\le s<t}
\bigl(F(\theta_s)-F(\theta^*)\bigr)
\le
\frac{R^2}{\lambda}
\frac{2+\log t}{\sqrt t}.
$$

Logistic loss 实际上是光滑的，可以用第 5.2 节的光滑优化分析得到更快结果；本题是在第 5.3 节的统一非光滑框架下计算常数。
