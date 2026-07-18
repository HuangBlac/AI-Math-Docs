# LFTP Chapter 5 §5.4：随机梯度下降

> 对应 *Learning Theory from First Principles* 第 5 章 §5.4 Stochastic Gradient Descent，以及习题 5.26--5.29。
>
> 本文由手写扫描稿整理，并统一了符号、补足了推导、纠正了若干关键笔误。

---

## 1. 为什么需要 SGD

机器学习中的经验目标通常写成

$$
F(\theta)
=
\frac1n\sum_{i=1}^n\ell\bigl(y_i,f_\theta(x_i)\bigr)+\Omega(\theta).
$$

普通梯度下降每次需要计算完整梯度 $F'(\theta_{t-1})$，因而要访问全部 $n$ 个样本。SGD 用计算成本更低的随机梯度估计

$$
g_t(\theta_{t-1})
$$

代替完整梯度，并要求

$$
\boxed{
\mathbb E\bigl[g_t(\theta_{t-1})\mid\mathcal F_{t-1}\bigr]
=F'(\theta_{t-1})
}
$$

其中 $\mathcal F_{t-1}$ 表示前 $t-1$ 次迭代产生的全部随机信息。

SGD 递推为

$$
\boxed{
\theta_t=\theta_{t-1}-\gamma_tg_t(\theta_{t-1})
}.
$$

### 经验风险最小化

若

$$
F(\theta)=\frac1n\sum_{i=1}^n\ell_i(\theta),
$$

则在每次迭代中独立、均匀地抽取

$$
i(t)\sim\operatorname{Unif}\{1,\dots,n\},
$$

并令

$$
g_t(\theta)=\ell_{i(t)}'(\theta).
$$

于是

$$
\mathbb E[g_t(\theta)]=\frac1n\sum_{i=1}^n\ell_i'(\theta)=F'(\theta).
$$

> **校订：** 不能把这里直接写成 $i(t)=t\bmod n$。循环顺序访问不是“每一步使用新鲜独立随机性”的无偏抽样，需用随机重排等另一套分析。

### Mini-batch

若每轮独立抽取 $m$ 个样本，则

$$
\widetilde g_t(\theta)
=
\frac1m\sum_{j=1}^m g_t^{(j)}(\theta).
$$

它仍然无偏，但每轮计算成本约增加为原来的 $m$ 倍。

### 期望风险最小化

若

$$
F(\theta)=\mathbb E_{(x,y)}\bigl[\ell(y,f_\theta(x))\bigr],
$$

则每次取一个新的独立样本 $(x_t,y_t)$，并令

$$
g_t(\theta)=\nabla_\theta\ell(y_t,f_\theta(x_t)).
$$

在允许交换求导与期望的条件下，$g_t$ 是 $F'$ 的无偏估计。

单次遍历数据时，该分析可以直接给出泛化误差界。实际训练常进行多轮遍历，此时通常需要显式正则化或 early stopping 来控制过拟合。

### 基本假设

- **(H-1) 无偏性**

  $$
  \mathbb E[g_t(\theta_{t-1})\mid\mathcal F_{t-1}]
  =F'(\theta_{t-1}).
  $$

- **(H-2) 随机梯度有界**

  $$
  \|g_t(\theta_{t-1})\|_2^2\le B^2
  \qquad\text{a.s.}
  $$

SGD 一般不是逐步下降算法：$F(\theta_t)$ 可以上升，但适当平均后可获得期望收敛保证。

---

## 2. 命题 5.7：凸 Lipschitz 目标上的 SGD

设：

1. $F$ 为凸函数且是 $B$-Lipschitz；
2. $F$ 存在极小点 $\theta_*$；
3. $\|\theta_0-\theta_*\|_2\le D$；
4. 随机梯度满足 (H-1)、(H-2)。

取

$$
\gamma_t=\frac{D}{B\sqrt t},
$$

并定义加权平均迭代点

$$
\bar\theta_t
=
\frac{\sum_{s=1}^t\gamma_s\theta_{s-1}}
{\sum_{s=1}^t\gamma_s}.
$$

则

$$
\boxed{
\mathbb E\bigl[F(\bar\theta_t)-F(\theta_*)\bigr]
\le
DB\frac{2+\log t}{2\sqrt t}
}.
$$

### 证明：基本递推

展开平方：

$$
\begin{aligned}
\mathbb E\|\theta_t-\theta_*\|_2^2
&=
\mathbb E\|\theta_{t-1}-\gamma_tg_t(\theta_{t-1})-\theta_*\|_2^2\\
&=
\mathbb E\|\theta_{t-1}-\theta_*\|_2^2
-2\gamma_t\mathbb E\bigl[g_t(\theta_{t-1})^\top(\theta_{t-1}-\theta_*)\bigr]\\
&\qquad+
\gamma_t^2\mathbb E\|g_t(\theta_{t-1})\|_2^2.
\end{aligned}
$$

利用条件无偏性，

$$
\begin{aligned}
&\mathbb E\bigl[g_t(\theta_{t-1})^\top(\theta_{t-1}-\theta_*)\bigr]\\
&\quad=
\mathbb E\left[
\mathbb E[g_t(\theta_{t-1})\mid\mathcal F_{t-1}]^\top
(\theta_{t-1}-\theta_*)
\right]\\
&\quad=
\mathbb E\bigl[F'(\theta_{t-1})^\top(\theta_{t-1}-\theta_*)\bigr].
\end{aligned}
$$

再由 (H-2)，

$$
\mathbb E\|\theta_t-\theta_*\|_2^2
\le
\mathbb E\|\theta_{t-1}-\theta_*\|_2^2
-2\gamma_t\mathbb E\bigl[F'(\theta_{t-1})^\top(\theta_{t-1}-\theta_*)\bigr]
+\gamma_t^2B^2.
$$

凸性给出

$$
F(\theta_{t-1})-F(\theta_*)
\le
F'(\theta_{t-1})^\top(\theta_{t-1}-\theta_*),
$$

所以

$$
\boxed{
\gamma_t\mathbb E\bigl[F(\theta_{t-1})-F(\theta_*)\bigr]
\le
\frac12\left(
\mathbb E\|\theta_{t-1}-\theta_*\|_2^2
-
\mathbb E\|\theta_t-\theta_*\|_2^2
\right)
+
\frac{\gamma_t^2B^2}{2}
}.
$$

### 求和与平均

从 $s=1$ 到 $t$ 求和，距离项望远镜消去：

$$
\sum_{s=1}^t\gamma_s
\mathbb E\bigl[F(\theta_{s-1})-F(\theta_*)\bigr]
\le
\frac{D^2}{2}
+
\frac{B^2}{2}\sum_{s=1}^t\gamma_s^2.
$$

由凸性，

$$
F(\bar\theta_t)
\le
\frac{\sum_{s=1}^t\gamma_sF(\theta_{s-1})}
{\sum_{s=1}^t\gamma_s},
$$

因此

$$
\boxed{
\mathbb E[F(\bar\theta_t)-F(\theta_*)]
\le
\frac{D^2+B^2\sum_{s=1}^t\gamma_s^2}
{2\sum_{s=1}^t\gamma_s}
}.
$$

对 $\gamma_s=D/(B\sqrt s)$，利用

$$
\sum_{s=1}^t\frac1s\le1+\log t,
\qquad
\sum_{s=1}^t\frac1{\sqrt s}\ge\sqrt t,
$$

得到命题中的结论。

### 固定步长版本

若预先知道总迭代次数 $T$，取固定步长

$$
\gamma=\frac{D}{B\sqrt T},
$$

并使用均匀平均

$$
\bar\theta_T=\frac1T\sum_{s=1}^T\theta_{s-1},
$$

则

$$
\mathbb E[F(\bar\theta_T)-F(\theta_*)]
\le
\frac{D^2}{2\gamma T}+rac{\gamma B^2}{2}
=
\frac{DB}{\sqrt T}.
$$

---

## 3. 习题 5.26：SGD 的高概率界

考虑投影 SGD：

$$
\theta_t
=
\Pi_D\bigl(\theta_{t-1}-\gamma_tg_t\bigr),
$$

其中 $\Pi_D$ 是到以原点为中心、半径为 $D$ 的 $\ell_2$ 球的正交投影，并假设 $\theta_*$ 也在该球中。

定义

$$
z_t
=-\gamma_t(\theta_{t-1}-\theta_*)^\top
\bigl[g_t-F'(\theta_{t-1})\bigr].
$$

### 鞅差性质

由条件无偏性，

$$
\mathbb E[z_t\mid\mathcal F_{t-1}]=0.
$$

投影保证

$$
\|\theta_{t-1}-\theta_*\|_2\le2D.
$$

同时

$$
\|F'(\theta_{t-1})\|_2
=
\left\|\mathbb E[g_t\mid\mathcal F_{t-1}]\right\|_2
\le B,
$$

因而

$$
\|g_t-F'(\theta_{t-1})\|_2\le2B.
$$

所以

$$
\boxed{|z_t|\le4\gamma_tBD}.
$$

### 一步不等式

由投影的非扩张性，

$$
\begin{aligned}
\|\theta_t-\theta_*\|_2^2
&\le
\|\theta_{t-1}-\gamma_tg_t-\theta_*\|_2^2\\
&\le
\|\theta_{t-1}-\theta_*\|_2^2
-2\gamma_tF'(\theta_{t-1})^\top(\theta_{t-1}-\theta_*)
+\gamma_t^2B^2+2z_t.
\end{aligned}
$$

结合凸性，

$$
\boxed{
\gamma_t\bigl[F(\theta_{t-1})-F(\theta_*)\bigr]
\le
\frac12\left(
\|\theta_{t-1}-\theta_*\|_2^2
-
\|\theta_t-\theta_*\|_2^2
\right)
+
\frac{\gamma_t^2B^2}{2}
+z_t
}.
$$

> **校订：** 这里必须是逐路径的不等式，距离项外不应写期望；否则无法与随机的 $z_t$ 放在同一个一步递推中。

### 使用 Azuma 不等式

记

$$
S_1=\sum_{s=1}^t\gamma_s,
\qquad
S_2=\sum_{s=1}^t\gamma_s^2.
$$

Azuma 不等式给出：以至少 $1-\delta$ 的概率，

$$
\sum_{s=1}^t z_s
\le
4BD\sqrt{2S_2\log(1/\delta)}.
$$

因此

$$
\boxed{
F(\bar\theta_t)-F(\theta_*)
\le
\frac{2D^2}{S_1}
+
\frac{B^2S_2}{2S_1}
+
4BD\frac{\sqrt{S_2}}{S_1}
\sqrt{2\log\frac1\delta}
}.
$$

若 $\gamma_t\equiv\gamma$，则

$$
\boxed{
F(\bar\theta_T)-F(\theta_*)
\le
\frac{2D^2}{\gamma T}
+
\frac{\gamma B^2}{2}
+
\frac{4DB}{\sqrt T}\sqrt{2\log\frac1\delta}
}.
$$

---

## 4. SGD 与完整梯度下降的计算量比较

对线性预测和 Lipschitz 损失，统计误差通常为

$$
O\!\left(\frac{GRD}{\sqrt n}\right).
$$

若对经验风险使用完整梯度下降：

- 每次完整梯度需要访问 $n$ 个样本；
- 为使优化误差降到与统计误差相同的量级，通常取 $t\asymp n$；
- 总计约访问 $n^2$ 个单样本梯度。

若使用 SGD：

- 每次只访问一个单样本梯度；
- 进行 $t=n$ 次更新即可达到同阶的 $O(n^{-1/2})$ 上界；
- 总计只需约 $n$ 次单样本梯度访问。

因此，在大样本、只需统计精度的情形下，SGD 通常更合适；若要求极高的优化精度，完整梯度法或方差缩减方法可能更有优势。

---

## 5. 习题 5.27：Mini-batch SGD

令

$$
\widetilde g_t
=
\frac1m\sum_{j=1}^m g_t^{(j)},
$$

其中条件于 $\mathcal F_{t-1}$，$g_t^{(1)},\dots,g_t^{(m)}$ 是相互独立、同分布的随机梯度。

### 无偏性

$$
\mathbb E[\widetilde g_t\mid\mathcal F_{t-1}]
=
\frac1m\sum_{j=1}^m
\mathbb E[g_t^{(j)}\mid\mathcal F_{t-1}]
=F'(\theta_{t-1}).
$$

### 有界性

由平方范数的凸性，

$$
\left\|\frac1m\sum_{j=1}^m g_t^{(j)}\right\|_2^2
\le
\frac1m\sum_{j=1}^m\|g_t^{(j)}\|_2^2
\le B^2.
$$

因此，在仅有 (H-1)、(H-2) 时，命题 5.7 原样成立，但最坏情形收敛界不会自动出现 $m$ 倍改进。

若进一步假设条件方差有界，

$$
\mathbb E\bigl[
\|g_t-F'(\theta_{t-1})\|_2^2
\mid\mathcal F_{t-1}
\bigr]
\le\sigma^2,
$$

则

$$
\mathbb E\bigl[
\|\widetilde g_t-F'(\theta_{t-1})\|_2^2
\mid\mathcal F_{t-1}
\bigr]
\le\frac{\sigma^2}{m}.
$$

不过，在一般非光滑分析中，$\|F'(\theta_{t-1})\|^2$ 仍然存在，故仅有方差缩小还不足以保证整体上界按 $1/m$ 改进。光滑性可将这一确定性梯度项吸收到下降项中，这正是习题 5.28 中 mini-batch 能改进界的原因。

---

## 6. 习题 5.28：光滑随机函数上的 SGD

设 $f_t:\mathbb R^d\to\mathbb R$ 是独立同分布的凸 $L$-smooth 随机函数，

$$
F(\theta)=\mathbb E[f_t(\theta)],
$$

且 $F$ 存在极小点 $\theta_*$。考虑

$$
\theta_t=\theta_{t-1}-\gamma_tf_t'(\theta_{t-1}).
$$

记

$$
\sigma_*^2=\mathbb E\|f_t'(\theta_*)\|_2^2.
$$

注意：一般并没有 $f_t'(\theta_*)=0$；只有

$$
\mathbb E[f_t'(\theta_*)]=F'(\theta_*)=0.
$$

### 控制随机梯度的二阶矩

由

$$
\|a+b\|^2\le2\|a\|^2+2\|b\|^2
$$

和凸 $L$-smooth 函数的 co-coercivity，

$$
\|f_t'(x)-f_t'(y)\|_2^2
\le
L\bigl(f_t'(x)-f_t'(y)\bigr)^\top(x-y),
$$

得到

$$
\begin{aligned}
\|f_t'(\theta_{t-1})\|_2^2
&\le
2\|f_t'(\theta_{t-1})-f_t'(\theta_*)\|_2^2
+2\|f_t'(\theta_*)\|_2^2\\
&\le
2L\bigl(f_t'(\theta_{t-1})-f_t'(\theta_*)\bigr)^\top
(\theta_{t-1}-\theta_*)
+2\|f_t'(\theta_*)\|_2^2.
\end{aligned}
$$

取期望，并使用 $F'(\theta_*)=0$，可得

$$
\mathbb E\|f_t'(\theta_{t-1})\|_2^2
\le
2L\mathbb E\bigl[F'(\theta_{t-1})^\top(\theta_{t-1}-\theta_*)\bigr]
+2\sigma_*^2.
$$

### 主递推

展开平方并代入上式：

$$
\boxed{
\begin{aligned}
\mathbb E\|\theta_t-\theta_*\|_2^2
&\le
\mathbb E\|\theta_{t-1}-\theta_*\|_2^2\\
&\quad-
2\gamma_t(1-\gamma_tL)
\mathbb E\bigl[F'(\theta_{t-1})^\top(\theta_{t-1}-\theta_*)\bigr]\\
&\quad+
2\gamma_t^2\sigma_*^2.
\end{aligned}
}.
$$

### 显式收敛率

取固定步长 $0<\gamma\le1/(2L)$，并定义

$$
\bar\theta_T=\frac1T\sum_{s=1}^T\theta_{s-1}.
$$

由凸性

$$
F(\theta)-F(\theta_*)
\le F'(\theta)^\top(\theta-\theta_*),
$$

对主递推求和可得

$$
\mathbb E[F(\bar\theta_T)-F(\theta_*)]
\le
\frac{D^2}{2\gamma(1-\gamma L)T}
+
\frac{\gamma\sigma_*^2}{1-\gamma L},
$$

其中 $D=\|\theta_0-\theta_*\|_2$。由于 $\gamma\le1/(2L)$，

$$
\mathbb E[F(\bar\theta_T)-F(\theta_*)]
\le
\frac{D^2}{\gamma T}+2\gamma\sigma_*^2.
$$

取

$$
\gamma
=
\frac{D}{2LD+\sigma_*\sqrt{2T}},
$$

则自动有 $\gamma\le1/(2L)$，且

$$
\boxed{
\mathbb E[F(\bar\theta_T)-F(\theta_*)]
\le
\frac{2LD^2}{T}
+
\frac{2\sqrt2D\sigma_*}{\sqrt T}
}.
$$

因此收敛率为 $O(T^{-1/2})$；当最优点处无随机噪声，即 $\sigma_*=0$ 时，可得到 $O(T^{-1})$。

### Mini-batch 的改进

若每轮使用 $m$ 个独立随机函数的平均

$$
\widetilde f_t
=
\frac1m\sum_{j=1}^m f_{t,j},
$$

则

$$
\mathbb E\|\widetilde f_t'(\theta_*)\|_2^2
=
\frac{\sigma_*^2}{m},
$$

因为 $\mathbb E[f_{t,j}'(\theta_*)]=F'(\theta_*)=0$ 且各项独立。因此

$$
\boxed{
\mathbb E[F(\bar\theta_T)-F(\theta_*)]
\lesssim
\frac{LD^2}{T}
+
\frac{D\sigma_*}{\sqrt{mT}}
}.
$$

这解释了为什么 mini-batch 在光滑情形中能够改进迭代次数意义下的收敛常数。

---

## 7. 习题 5.29：非均匀抽样

设 $F(\theta,z)$ 关于 $\theta$ 为凸函数，并存在次梯度 $F'(\theta,z)$ 满足

$$
\|F'(\theta,z)\|_2\le B(z).
$$

目标是最小化

$$
\Phi(\theta)=\mathbb E_{z\sim p}[F(\theta,z)].
$$

实际从分布 $q$ 中抽样。设

$$
r(z)=\frac{dq}{dp}(z).
$$

定义重要性加权随机梯度

$$
g_t
=
\frac1{r(z_t)}F'(\theta_{t-1},z_t),
\qquad z_t\sim q.
$$

则

$$
\begin{aligned}
\mathbb E_q[g_t\mid\theta_{t-1}]
&=
\int\frac1{r(z)}F'(\theta_{t-1},z)\,dq(z)\\
&=
\int F'(\theta_{t-1},z)\,dp(z)\\
&\in\partial\Phi(\theta_{t-1}),
\end{aligned}
$$

因此该估计仍然无偏。

### 基于几乎处处上界的收敛率

令

$$
M(q)
=
\operatorname*{ess\,sup}_{z}
\frac{B(z)}{r(z)}.
$$

则 $\|g_t\|_2\le M(q)$。若 $\|\theta_0-\theta_*\|\le D$，固定步长 SGD 满足

$$
\mathbb E[\Phi(\bar\theta_T)-\Phi(\theta_*)]
\le
\frac{D^2}{2\gamma T}
+
\frac{\gamma M(q)^2}{2}.
$$

取

$$
\gamma=\frac{D}{M(q)\sqrt T},
$$

得到

$$
\boxed{
\mathbb E[\Phi(\bar\theta_T)-\Phi(\theta_*)]
\le
\frac{DM(q)}{\sqrt T}
}.
$$

### 最优抽样分布

由于 $B(z)\le M(q)r(z)$，积分后得到

$$
\mathbb E_p[B(z)]\le M(q)\mathbb E_p[r(z)]=M(q).
$$

下界由

$$
r_*(z)=\frac{B(z)}{\mathbb E_p[B(z)]}
$$

达到。此时

$$
\frac{B(z)}{r_*(z)}=\mathbb E_p[B(z)]
$$

为常数，因此

$$
\boxed{M(q_*)=\mathbb E_p[B(z)]}.
$$

相比之下，若 $q=p$，则 $r\equiv1$，

$$
M(p)=\operatorname*{ess\,sup}_zB(z).
$$

当 $B(z)$ 很不均匀时，按 $B(z)$ 成比例抽样可把常数从最大值降为平均值。

### 二阶矩版本

利用命题 5.7 中“几乎处处有界可替换为二阶矩有界”的备注，也可定义

$$
C(q)^2
=
\mathbb E_p\left[\frac{B(z)^2}{r(z)}\right].
$$

由 Cauchy--Schwarz，

$$
\bigl(\mathbb E_p[B]\bigr)^2
\le
\mathbb E_p\left[\frac{B^2}{r}\right]\mathbb E_p[r]
=C(q)^2,
$$

同样由 $r_*(z)\propto B(z)$ 取得最小值。

### 应用于线性 SVM

对经验 hinge loss，令 $z=i\in\{1,\dots,n\}$，$p_i=1/n$，

$$
\ell_i(\theta)=\max\{0,1-y_i x_i^\top\theta\}.
$$

其次梯度满足

$$
\|\ell_i'(\theta)\|_2\le\|x_i\|_2,
$$

所以可取

$$
B_i=\|x_i\|_2.
$$

最优抽样概率为

$$
\boxed{
q_i
=
\frac{\|x_i\|_2}{\sum_{j=1}^n\|x_j\|_2}
}.
$$

并对抽到的次梯度乘以重要性权重

$$
\frac{p_i}{q_i}=rac{1/n}{q_i}.
$$

均匀抽样的最坏界常数为

$$
\max_i\|x_i\|_2,
$$

而最优非均匀抽样将其降为

$$
\frac1n\sum_{i=1}^n\|x_i\|_2.
$$

---

## 主要校订

1. 扫描稿后半部分对应的是 **Chapter 5 §5.4**，不是 Chapter 4。
2. 经验风险 SGD 应使用均匀随机、有放回抽样；$i(t)=t\bmod n$ 不满足这里采用的无偏独立抽样假设。
3. 命题 5.7 的平均点是 $\sum_s\gamma_s\theta_{s-1}/\sum_s\gamma_s$。
4. 习题 5.26 的一步高概率递推应为逐路径不等式，距离项不应带期望。
5. 习题 5.27 中，仅由随机梯度有界不能推出 mini-batch 自动改善最坏情形收敛率。
6. 习题 5.28 中一般只有 $F'(\theta_*)=\mathbb E[f_t'(\theta_*)]=0$，不能写成每个 $f_t'(\theta_*)=0$。
7. 非均匀抽样的梯度权重应为 $1/(dq/dp)$，最优密度满足 $dq/dp\propto B(z)$。
