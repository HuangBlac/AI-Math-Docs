# LFTP 第 5.3 节：非光滑问题上的梯度方法

> 对应教材：*Learning Theory from First Principles*，§5.3，Definition 5.4、Proposition 5.6、Exercises 5.18–5.21。  
> 本文根据手写笔记重新排版，并依据原教材统一记号、补全证明与修正笔误。

## 1. Lipschitz 连续函数

### Definition 5.4

函数 $F:\mathbb{R}^d\to\mathbb{R}$ 称为关于 $\ell_2$ 范数的 $B$-Lipschitz 连续函数，如果

$$
|F(\eta)-F(\theta)|\le B\|\eta-\theta\|_2,
\qquad \forall \theta,\eta\in\mathbb{R}^d.
$$

在本节中，目标函数只要求**凸**且 **Lipschitz 连续**，不再要求光滑，因此相应问题通常称为非光滑优化。

---

## 2. Exercise 5.18：Lipschitz 连续与梯度有界等价

设 $F$ 可微。证明：

$$
F\text{ 是 }B\text{-Lipschitz}
\quad\Longleftrightarrow\quad
\|F'(\theta)\|_2\le B,
\qquad \forall \theta\in\mathbb{R}^d.
$$

### 2.1 梯度有界推出 Lipschitz 连续

令

$$
\gamma(t)=\theta+t(\eta-\theta),\qquad t\in[0,1].
$$

由微积分基本定理，

$$
F(\eta)-F(\theta)
=
\int_0^1 F'(\gamma(t))^\top(\eta-\theta)\,dt.
$$

因此

$$
\begin{aligned}
|F(\eta)-F(\theta)|
&\le
\int_0^1
\|F'(\gamma(t))\|_2\,\|\eta-\theta\|_2\,dt\\
&\le B\|\eta-\theta\|_2.
\end{aligned}
$$

### 2.2 Lipschitz 连续推出梯度有界

固定 $\theta$ 和单位向量 $v$。由 Lipschitz 连续性，

$$
\left|
\frac{F(\theta+tv)-F(\theta)}{t}
\right|
\le B,
\qquad t\ne 0.
$$

令 $t\to0$，得到

$$
|F'(\theta)^\top v|\le B.
$$

对所有 $\|v\|_2=1$ 取上确界：

$$
\|F'(\theta)\|_2
=
\sup_{\|v\|_2=1}|F'(\theta)^\top v|
\le B.
$$

---

## 3. 从梯度到次梯度

### 3.1 次微分与次梯度

对凸函数 $F:\mathbb{R}^d\to\mathbb{R}$，点 $\theta$ 处的次微分定义为

$$
\partial F(\theta)
=
\left\{
 z\in\mathbb{R}^d:
 F(\eta)\ge F(\theta)+z^\top(\eta-\theta),
 \quad \forall\eta\in\mathbb{R}^d
\right\}.
$$

任意 $z\in\partial F(\theta)$ 称为 $F$ 在 $\theta$ 处的次梯度。

次梯度定义了一条位于函数图像下方的仿射支撑面。非光滑情形下，原来的梯度下降迭代改写为

$$
\theta_t=\theta_{t-1}-\gamma_t g_{t-1},
\qquad g_{t-1}\in\partial F(\theta_{t-1}).
$$

该算法称为**次梯度法**。它一般不是逐步下降法，即 $F(\theta_t)$ 可能暂时增大。

### 3.2 可微凸函数的次微分是单点集

若 $F$ 凸且在 $\theta$ 可微，则凸函数的一阶条件给出

$$
F(\eta)\ge F(\theta)+F'(\theta)^\top(\eta-\theta),
$$

所以 $F'(\theta)\in\partial F(\theta)$。

反过来，若 $g\in\partial F(\theta)$，则对任意方向 $v$ 和 $t>0$，

$$
F(\theta+tv)-F(\theta)\ge t\,g^\top v.
$$

除以 $t$ 并令 $t\downarrow0$：

$$
F'(\theta)^\top v\ge g^\top v.
$$

将 $v$ 替换为 $-v$，得到相反方向的不等式，因此

$$
F'(\theta)^\top v=g^\top v,
\qquad \forall v.
$$

故 $g=F'(\theta)$，即

$$
\partial F(\theta)=\{F'(\theta)\}.
$$

---

## 4. Exercise 5.19：两个典型函数的次微分

### 4.1 绝对值函数

令 $f(\theta)=|\theta|$。则

$$
\partial |\theta|
=
\begin{cases}
\{1\}, & \theta>0,\\[2mm]
[-1,1], & \theta=0,\\[2mm]
\{-1\}, & \theta<0.
\end{cases}
$$

特别地，在不可微点 $0$，左右导数分别为 $-1$ 与 $1$，次微分是二者的凸包。

### 4.2 Hinge loss

令

$$
f(\theta)=(1-y\theta^\top x)_+,
\qquad y\in\{-1,1\},\quad x\in\mathbb{R}^d.
$$

记 $u(\theta)=1-y\theta^\top x$。函数 $h(u)=u_+=\max\{0,u\}$ 的次微分为

$$
\partial h(u)
=
\begin{cases}
\{1\}, & u>0,\\
[0,1], & u=0,\\
\{0\}, & u<0.
\end{cases}
$$

利用仿射复合的次梯度链式法则，得到

$$
\partial f(\theta)
=
\begin{cases}
\{-yx\}, & y\theta^\top x<1,\\[1mm]
\{-\alpha yx:\alpha\in[0,1]\}, & y\theta^\top x=1,\\[1mm]
\{0\}, & y\theta^\top x>1.
\end{cases}
$$

---

## 5. Proposition 5.6：次梯度法的收敛速度

假设：

- $F$ 为凸函数；
- $F$ 是 $B$-Lipschitz 连续的，因此可取 $\|g_t\|_2\le B$；
- $\eta^*$ 是全局最小点；
- $\|\eta^*-\theta_0\|_2\le D$。

使用步长

$$
\gamma_t=\frac{D}{B\sqrt t},
$$

则次梯度迭代满足

$$
\min_{0\le s\le t-1}
\bigl(F(\theta_s)-F(\eta^*)\bigr)
\le
DB\frac{2+\log t}{2\sqrt t}.
$$

### 5.1 基本递推式

令 $g_{t-1}\in\partial F(\theta_{t-1})$。由

$$
\theta_t=\theta_{t-1}-\gamma_tg_{t-1},
$$

可得

$$
\begin{aligned}
\|\theta_t-\eta^*\|_2^2
&=
\|\theta_{t-1}-\eta^*\|_2^2
-2\gamma_tg_{t-1}^\top(\theta_{t-1}-\eta^*)
+\gamma_t^2\|g_{t-1}\|_2^2.
\end{aligned}
$$

次梯度不等式给出

$$
F(\theta_{t-1})-F(\eta^*)
\le
 g_{t-1}^\top(\theta_{t-1}-\eta^*).
$$

因此

$$
2\gamma_t\bigl(F(\theta_{t-1})-F(\eta^*)\bigr)
\le
\|\theta_{t-1}-\eta^*\|_2^2
-
\|\theta_t-\eta^*\|_2^2
+
\gamma_t^2B^2.
$$

### 5.2 求和

对 $s=1,\dots,t$ 求和，得到

$$
2\sum_{s=1}^t
\gamma_s\bigl(F(\theta_{s-1})-F(\eta^*)\bigr)
\le
D^2+B^2\sum_{s=1}^t\gamma_s^2.
$$

于是

$$
\min_{0\le s\le t-1}
\bigl(F(\theta_s)-F(\eta^*)\bigr)
\le
\frac{D^2+B^2\sum_{s=1}^t\gamma_s^2}
{2\sum_{s=1}^t\gamma_s}.
$$

代入 $\gamma_s=D/(B\sqrt s)$，并使用

$$
\sum_{s=1}^t\frac1{\sqrt s}\ge\sqrt t,
\qquad
\sum_{s=1}^t\frac1s\le1+\log t,
$$

得到

$$
\min_{0\le s\le t-1}
\bigl(F(\theta_s)-F(\eta^*)\bigr)
\le
DB\frac{2+\log t}{2\sqrt t}.
$$

相同上界也适用于加权平均迭代

$$
\bar\theta_t
=
\frac{\sum_{s=1}^t\gamma_s\theta_{s-1}}
{\sum_{s=1}^t\gamma_s},
$$

因为由 Jensen 不等式，

$$
F(\bar\theta_t)
\le
\frac{\sum_{s=1}^t\gamma_sF(\theta_{s-1})}
{\sum_{s=1}^t\gamma_s}.
$$

---

## 6. Exercise 5.20：不需要预先知道 $B$ 的归一化次梯度法

考虑迭代

$$
\theta_t
=
\theta_{t-1}
-
\frac{\gamma_t'}{\|g_{t-1}\|_2}g_{t-1},
\qquad
\gamma_t'=\frac{D}{\sqrt t},
$$

其中 $g_{t-1}\in\partial F(\theta_{t-1})$。若 $g_{t-1}=0$，则 $\theta_{t-1}$ 已经是凸函数的全局最小点，可直接停止。

距离递推式为

$$
\begin{aligned}
\|\theta_t-\eta^*\|_2^2
&=
\|\theta_{t-1}-\eta^*\|_2^2
-
2\frac{\gamma_t'}{\|g_{t-1}\|_2}
 g_{t-1}^\top(\theta_{t-1}-\eta^*)
+
(\gamma_t')^2.
\end{aligned}
$$

由次梯度不等式以及 $\|g_{t-1}\|_2\le B$，

$$
2\frac{\gamma_t'}{B}
\bigl(F(\theta_{t-1})-F(\eta^*)\bigr)
\le
\|\theta_{t-1}-\eta^*\|_2^2
-
\|\theta_t-\eta^*\|_2^2
+
(\gamma_t')^2.
$$

求和后得到

$$
\min_{0\le s\le t-1}
\bigl(F(\theta_s)-F(\eta^*)\bigr)
\le
DB\frac{2+\log t}{2\sqrt t}.
$$

算法的步长不含 $B$，但理论上界仍然自然地依赖目标函数的 Lipschitz 常数 $B$。

---

## 7. Exercise 5.21：投影次梯度法

设 $K\subset\mathbb{R}^d$ 是非空闭凸集，定义正交投影

$$
\Pi_K(x)=\arg\min_{z\in K}\|z-x\|_2^2.
$$

### 7.1 投影的最优性条件

令 $p=\Pi_K(x)$。对任意 $z\in K$，线段 $p+t(z-p)$ 仍在 $K$ 中。函数

$$
\phi(t)=\|p+t(z-p)-x\|_2^2
$$

在 $t=0$ 处取最小值，因此

$$
\phi'(0)=2(p-x)^\top(z-p)\ge0.
$$

等价地，

$$
(x-p)^\top(z-p)\le0,
\qquad \forall z\in K.
$$

### 7.2 投影是压缩映射

令

$$
p=\Pi_K(x),\qquad q=\Pi_K(y).
$$

在上面的最优性条件中分别取 $z=q$ 与 $z=p$，得到

$$
(x-p)^\top(q-p)\le0,
$$

$$
(y-q)^\top(p-q)\le0.
$$

两式合并可得

$$
\|p-q\|_2^2
\le
(x-y)^\top(p-q)
\le
\|x-y\|_2\|p-q\|_2.
$$

因此

$$
\boxed{
\|\Pi_K(x)-\Pi_K(y)\|_2
\le
\|x-y\|_2
}.
$$

### 7.3 投影次梯度法的收敛性

考虑

$$
\theta_t
=
\Pi_K\bigl(\theta_{t-1}-\gamma_tg_{t-1}\bigr),
\qquad
 g_{t-1}\in\partial F(\theta_{t-1}).
$$

设 $\eta^*$ 是 $F$ 在 $K$ 上的最小点。由于 $\eta^*\in K$，有 $\Pi_K(\eta^*)=\eta^*$。由投影压缩性，

$$
\begin{aligned}
\|\theta_t-\eta^*\|_2
&\le
\|\theta_{t-1}-\gamma_tg_{t-1}-\eta^*\|_2.
\end{aligned}
$$

平方并展开后，得到与无约束情形完全相同的基本递推式。因此 Proposition 5.6 的收敛保证仍然成立：

$$
\min_{0\le s\le t-1}
\bigl(F(\theta_s)-F(\eta^*)\bigr)
\le
DB\frac{2+\log t}{2\sqrt t}.
$$

---

## 8. 关键结论

1. 非光滑凸优化中，梯度由次梯度替代。
2. 次梯度法的函数值不必单调下降。
3. 一般凸 Lipschitz 问题的典型收敛速度为

   $$
   O\!\left(\frac{BD}{\sqrt t}\right),
   $$

   使用简单递减步长时会多出 $\log t$ 因子。
4. 投影步骤允许处理凸约束，且不改变基本证明结构。
5. 归一化次梯度可以消除算法对未知 Lipschitz 常数 $B$ 的显式依赖。
