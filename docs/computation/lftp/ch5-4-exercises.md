# LFTP 第 5.4 节：Exercises 5.29–5.30

> 对应教材：*Learning Theory from First Principles*，§5.4，Exercises 5.29–5.30。  
> 本文根据手写笔记整理，并依据原题修正重要性采样方向、SVM 损失函数及常数。

## Exercise 5.29：非均匀采样与重要性采样

设

$$
F:\mathbb{R}^d\times\mathcal Z\to\mathbb{R}
$$

关于第一个变量是凸函数，并且存在次梯度 $F'(\theta,z)$ 满足

$$
\|F'(\theta,z)\|_2\le B(z).
$$

目标函数为

$$
\bar F(\theta)
=
\mathbb E_{z\sim p}[F(\theta,z)].
$$

但样本从分布 $q$ 中抽取。记

$$
r(z)=\frac{dq}{dp}(z),
$$

于是 $dq=r\,dp$ 且

$$
\mathbb E_p[r(z)]=1.
$$

假设在 $B(z)>0$ 的区域上 $r(z)>0$。算法使用重要性加权随机次梯度

$$
g_t
=
\frac{1}{r(z_t)}F'(\theta_{t-1},z_t),
\qquad z_t\overset{\mathrm{i.i.d.}}\sim q,
$$

并更新

$$
\theta_t=\theta_{t-1}-\gamma_tg_t.
$$

---

### 1. 无偏性

条件于 $\theta_{t-1}$，

$$
\begin{aligned}
\mathbb E_q[g_t\mid\theta_{t-1}]
&=
\int_{\mathcal Z}
\frac{F'(\theta_{t-1},z)}{r(z)}\,dq(z)\\
&=
\int_{\mathcal Z}
\frac{F'(\theta_{t-1},z)}{r(z)}r(z)\,dp(z)\\
&=
\int_{\mathcal Z}F'(\theta_{t-1},z)\,dp(z)\\
&\in
\partial\bar F(\theta_{t-1}).
\end{aligned}
$$

在可微且可交换微分与积分时，右侧就是 $\bar F'(\theta_{t-1})$。因此重要性加权后的随机次梯度仍然无偏。

---

### 2. 二阶矩常数

有

$$
\begin{aligned}
\mathbb E_q\bigl[\|g_t\|_2^2\mid\theta_{t-1}\bigr]
&\le
\int
\frac{B(z)^2}{r(z)^2}\,dq(z)\\
&=
\int
\frac{B(z)^2}{r(z)}\,dp(z).
\end{aligned}
$$

定义

$$
\widetilde B(q)^2
=
\mathbb E_p\left[\frac{B(z)^2}{r(z)}\right].
$$

于是 Proposition 5.7 可以直接应用，只需把原来的统一梯度界 $B$ 替换为 $\widetilde B(q)$。

若 $\|\theta_0-\theta^*\|_2\le D$，固定 horizon $T$ 并选择

$$
\gamma
=
\frac{D}{\widetilde B(q)\sqrt T},
$$

则均匀平均迭代满足

$$
\boxed{
\mathbb E[\bar F(\bar\theta_T)]-\bar F(\theta^*)
\le
\frac{D\widetilde B(q)}{\sqrt T}
}.
$$

若采用递减步长

$$
\gamma_t
=
\frac{D}{\widetilde B(q)\sqrt t},
$$

则得到 anytime 上界

$$
\mathbb E[\bar F(\bar\theta_t)]-\bar F(\theta^*)
\le
D\widetilde B(q)
\frac{2+\log t}{2\sqrt t}.
$$

---

### 3. 最优采样分布

需要在约束

$$
r(z)\ge0,
\qquad
\mathbb E_p[r(z)]=1
$$

下最小化

$$
\mathbb E_p\left[\frac{B(z)^2}{r(z)}\right].
$$

由 Cauchy–Schwarz 不等式，

$$
\begin{aligned}
\bigl(\mathbb E_p[B(z)]\bigr)^2
&=
\left(
\mathbb E_p\left[
\frac{B(z)}{\sqrt{r(z)}}\sqrt{r(z)}
\right]
\right)^2\\
&\le
\mathbb E_p\left[\frac{B(z)^2}{r(z)}\right]
\mathbb E_p[r(z)]\\
&=
\mathbb E_p\left[\frac{B(z)^2}{r(z)}\right].
\end{aligned}
$$

等号成立当且仅当

$$
\frac{B(z)}{\sqrt{r(z)}}
\propto
\sqrt{r(z)},
$$

即

$$
\boxed{
r^*(z)=\frac{B(z)}{\mathbb E_p[B(z)]}}.
$$

因此

$$
\boxed{
\frac{dq^*}{dp}(z)
=
\frac{B(z)}{\mathbb E_p[B(z)]}
},
$$

且最优二阶矩常数为

$$
\boxed{
\widetilde B(q^*)=\mathbb E_p[B(z)]
}.
$$

若使用原分布 $q=p$，则 $r\equiv1$，常数为

$$
\widetilde B(p)
=
\sqrt{\mathbb E_p[B(z)^2]}.
$$

最优重要性采样将 RMS 常数

$$
\sqrt{\mathbb E[B^2]}
$$

降低为算术平均常数

$$
\mathbb E[B].
$$

改进因子为

$$
\frac{\sqrt{\mathbb E[B^2]}}{\mathbb E[B]}
\ge1.
$$

当 $B(z)$ 在少量样本上非常大、在多数样本上较小时，该比值可以很大，因此非均匀采样会显著改善收敛常数。

---

### 4. 应用于经验风险上的 SVM

考虑无正则项的经验 hinge risk

$$
\bar F(\theta)
=
\frac1n\sum_{i=1}^n
(1-y_i\theta^\top x_i)_+.
$$

令 $p$ 是 $\{1,\dots,n\}$ 上的均匀分布，并定义

$$
F(\theta,i)
=(1-y_i\theta^\top x_i)_+.
$$

可取样本次梯度

$$
s_i(\theta)
\in
\partial_\theta F(\theta,i),
$$

其中

$$
s_i(\theta)
=
\begin{cases}
-y_ix_i, & y_i\theta^\top x_i<1,\\
-\alpha y_ix_i,\ \alpha\in[0,1], & y_i\theta^\top x_i=1,\\
0, & y_i\theta^\top x_i>1.
\end{cases}
$$

因此

$$
B(i)=\|x_i\|_2.
$$

最优抽样概率为

$$
\boxed{
q_i^*
=
\frac{\|x_i\|_2}{\sum_{j=1}^n\|x_j\|_2}
}.
$$

若某些 $\|x_i\|_2=0$，相应损失关于 $\theta$ 为常数，可从随机梯度采样集合中忽略；其余样本按上述概率归一化。

由于 $p_i=1/n$，对应的密度比为

$$
r_i^*
=
\frac{q_i^*}{p_i}
=nq_i^*
=
\frac{\|x_i\|_2}{\bar R},
$$

其中

$$
\bar R
=
\frac1n\sum_{j=1}^n\|x_j\|_2.
$$

若抽到索引 $i_t$，重要性加权次梯度为

$$
\boxed{
 g_t
=
\frac{\bar R}{\|x_{i_t}\|_2}
 s_{i_t}(\theta_{t-1})
}.
$$

它的范数至多为 $\bar R$。因此：

- 均匀采样的二阶矩常数为

  $$
  R_{\mathrm{rms}}
  =
  \sqrt{\frac1n\sum_{i=1}^n\|x_i\|_2^2};
  $$

- 最优重要性采样的常数为

  $$
  R_{\mathrm{avg}}
  =
  \frac1n\sum_{i=1}^n\|x_i\|_2.
  $$

于是收敛界从

$$
\frac{DR_{\mathrm{rms}}}{\sqrt T}
$$

改善为

$$
\boxed{
\frac{DR_{\mathrm{avg}}}{\sqrt T}
}.
$$

若目标还包含 $\lambda\|\theta\|_2^2/2$，可将 $\lambda\theta$ 确定性地加入每次更新；重要性采样只作用于数据损失部分。

---

## Exercise 5.30：非凸光滑函数上的 SGD

设 $F:\mathbb{R}^d\to\mathbb{R}$ 是 $L$-smooth，但不要求凸。考虑常数步长 SGD：

$$
\theta_t
=
\theta_{t-1}-\gamma g_t,
$$

并假设

$$
\mathbb E[g_t\mid\theta_{t-1}]
=
F'(\theta_{t-1}),
$$

以及

$$
\mathbb E[\|g_t\|_2^2\mid\theta_{t-1}]
\le B^2.
$$

几乎处处有界 $\|g_t\|_2\le B$ 是上述条件的充分条件。

---

### 1. 单步下降不等式

由 $L$-smooth 性，

$$
F(\theta_t)
\le
F(\theta_{t-1})
+F'(\theta_{t-1})^\top(\theta_t-\theta_{t-1})
+
\frac L2\|\theta_t-\theta_{t-1}\|_2^2.
$$

代入

$$
\theta_t-\theta_{t-1}=-\gamma g_t,
$$

得到

$$
F(\theta_t)
\le
F(\theta_{t-1})
-
\gamma F'(\theta_{t-1})^\top g_t
+
\frac{L\gamma^2}{2}\|g_t\|_2^2.
$$

条件于 $\theta_{t-1}$ 取期望：

$$
\begin{aligned}
\mathbb E[ F(\theta_t)\mid\theta_{t-1}]
&\le
F(\theta_{t-1})
-
\gamma F'(\theta_{t-1})^\top
\mathbb E[g_t\mid\theta_{t-1}]\\
&\qquad
+
\frac{L\gamma^2}{2}
\mathbb E[\|g_t\|_2^2\mid\theta_{t-1}]\\
&\le
F(\theta_{t-1})
-
\gamma\|F'(\theta_{t-1})\|_2^2
+
\frac{LB^2\gamma^2}{2}.
\end{aligned}
$$

再次取全期望，得到

$$
\boxed{
\mathbb E[F(\theta_t)]
\le
\mathbb E[F(\theta_{t-1})]
-
\gamma\mathbb E\|F'(\theta_{t-1})\|_2^2
+
\frac{LB^2\gamma^2}{2}
}.
$$

这里的关键无偏性计算是

$$
\begin{aligned}
\mathbb E\bigl[F'(\theta_{t-1})^\top g_t\bigr]
&=
\mathbb E\left[
F'(\theta_{t-1})^\top
\mathbb E[g_t\mid\theta_{t-1}]
\right]\\
&=
\mathbb E\|F'(\theta_{t-1})\|_2^2.
\end{aligned}
$$

---

### 2. 平均梯度平方范数

将单步不等式移项：

$$
\gamma
\mathbb E\|F'(\theta_{s-1})\|_2^2
\le
\mathbb E[F(\theta_{s-1})]
-
\mathbb E[F(\theta_s)]
+
\frac{LB^2\gamma^2}{2}.
$$

对 $s=1,\dots,t$ 求和，函数值项望远镜消去：

$$
\gamma\sum_{s=1}^t
\mathbb E\|F'(\theta_{s-1})\|_2^2
\le
F(\theta_0)-\mathbb E[F(\theta_t)]
+
\frac{LB^2\gamma^2t}{2}.
$$

由于

$$
\mathbb E[F(\theta_t)]
\ge
\inf_{\eta\in\mathbb{R}^d}F(\eta),
$$

得到

$$
\boxed{
\frac1t\sum_{s=1}^t
\mathbb E\|F'(\theta_{s-1})\|_2^2
\le
\frac{F(\theta_0)-\inf_\eta F(\eta)}{\gamma t}
+
\frac{LB^2\gamma}{2}
}.
$$

非凸问题中不能用函数值次优性刻画全局最优解，因此这里控制的是梯度范数，即逼近一阶驻点。

---

### 3. 步长优化

记

$$
\Delta_0
=
F(\theta_0)-\inf_\eta F(\eta).
$$

上界为

$$
\frac{\Delta_0}{\gamma t}
+
\frac{LB^2\gamma}{2}.
$$

对 $\gamma$ 优化可取

$$
\gamma^*
=
\sqrt{\frac{2\Delta_0}{LB^2t}},
$$

从而

$$
\boxed{
\frac1t\sum_{s=1}^t
\mathbb E\|F'(\theta_{s-1})\|_2^2
\le
\sqrt{\frac{2LB^2\Delta_0}{t}}
}.
$$

等价地，若从 $\{0,\dots,t-1\}$ 中均匀随机选取一个迭代编号 $S$，则

$$
\mathbb E\|F'(\theta_S)\|_2^2
=O(t^{-1/2}).
$$

这意味着梯度范数本身的一般保证为 $O(t^{-1/4})$；本题直接证明的量是梯度范数的平方。
