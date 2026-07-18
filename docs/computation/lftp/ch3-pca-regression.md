# PCA与主成分回归

**User:** Anonymous  
**Created:** 7/14/2026 18:45:23  
**Updated:** 7/14/2026 20:00:04  
**Exported:** 7/16/2026 21:26:19  
**Link:** [https://chatgpt.com/g/g-p-6a0d1885e500819197c7a046e3acab38/c/6a56133f-a4e8-83ea-a825-3aa5c25b46c9](https://chatgpt.com/g/g-p-6a0d1885e500819197c7a046e3acab38/c/6a56133f-a4e8-83ea-a825-3aa5c25b46c9)  

## Prompt:
2026/7/14 18:45:18

PCA and least-squares regression (). While regularization is a common way to
avoid overfitting for least-squares regression (as shown in section 3.6), performing PCA
and then unregularized OLS provides an alternative with similar behavior. That is, we
now consider the feature vector ΦV ∈ Rn×k, and minimize ky − ΦV ηk22
with respect
to η ∈ Rk, with solution η = (V ⊤Φ⊤ΦV )−1V ⊤Φ⊤y, leading to the prediction vector
ΦV η = ΦV (V ⊤Φ⊤ΦV )−1V ⊤Φ⊤y ∈ Rn.
If we assume the linear model y = Φθ∗ + ε as in section 3.5, we can compute the
excess risk of the estimator based on PCA as follows (using E[ε] = 0 and E[εε⊤] = σ2I):
1
n
Eε

kΦV η − Φθ∗k22

=
σ2k
n
+
1
n

ΦV (V ⊤Φ⊤ΦV )−1V ⊤Φ⊤Φθ∗ − Φθ∗
 
2
2
=
σ2k
n
+ θ⊤
∗
bΣ
θ∗ − θ⊤
∗
bΣ
V (V ⊤bΣV )−1V ⊤bΣθ∗
using that bΣ = 1
nΦ⊤Φ. We can then use that the columns of V are eigenvectors of bΣ so
that bΣV = V D and V ⊤bΣV = D, for a diagonal matrix D ∈ Rk×k, leading to
1
n
Eε

kΦV η − Φθ∗k22

=
σ2k
n
+ θ∗
bΣ
θ∗ − θ⊤
∗ V DV ⊤θ∗ =
σ2k
n
+ θ∗
bΣ
θ∗ − θ⊤
∗ V V ⊤bΣV V ⊤θ∗
=
σ2k
n
+ θ⊤
∗ (I − V V ⊤)bΣ(I − V V ⊤)θ∗.
Since V is composed of the eigenvectors of bΣ with the k largest eigenvalues, the matrix
(I − V V ⊤)bΣ(I − V V ⊤) has all of its eigenvalues less than λk+1, where λk+1 is the
(k+1)th-largest eigenvalue of bΣ, which is less than 1/(k+1) times tr[bΣ] (the sum of all
the eigenvalues). Thus, the excess risk of OLS after PCA is less than
σ2k
n
+ kθ∗k22
tr[bΣ]
k
,
which is similar to equation (3.6) (for ridge regression). A good value of k is then the
closest integer to kθ∗k2 · (tr[bΣ])1/2√n/σ, leading, up to constants, to the same excess risk
than for ridge regression, with the identification k ∼ 1
λ tr[bΣ].

## Response:
2026/7/14 18:45:22

> **解释PCA硬阈值与岭回归软缩减**
>
>
> **解释并优化PCA硬阈值与岭回归软缩减**
>
> 
>
> 思考了 35s

这一段的核心是：

> **先用 PCA 保留数据变化最大的 $k$ 个方向，再在这个 $k$ 维子空间里做不带正则项的 OLS。**

这称为 **principal component regression，PCR（主成分回归）**。它与 ridge regression 都通过压制“不稳定方向”降低方差：PCR 是直接丢弃，ridge 是连续收缩。该推导位于教材第 3.9 节。`lftp.pdf` `lftp.pdf`

---

## 1. PCA 后到底在回归什么

原始设计矩阵为

$$
\Phi\in\mathbb R^{n\times d},
\qquad
\widehat\Sigma=\frac1n\Phi^\top\Phi.
$$

设经验协方差矩阵的特征值分解为

$$
\widehat\Sigma
=
U\operatorname{Diag}(\lambda_1,\ldots,\lambda_d)U^\top,
\qquad
\lambda_1\ge\lambda_2\ge\cdots\ge\lambda_d\ge0.
$$

取前 $k$ 个特征向量：

$$
V=[u_1,\ldots,u_k]\in\mathbb R^{d\times k}.
$$

原始特征向量是 $\phi(x)\in\mathbb R^d$，PCA 后的新特征是

$$
V^\top\phi(x)\in\mathbb R^k.
$$

对整个数据矩阵而言，新设计矩阵是

$$
\Phi V\in\mathbb R^{n\times k}.
$$

于是我们求解

$$
\widehat\eta
=
\arg\min_{\eta\in\mathbb R^k}
\|y-\Phi V\eta\|_2^2,
$$

其闭式解为

$$
\widehat\eta
=
(V^\top\Phi^\top\Phi V)^{-1}V^\top\Phi^\top y.
$$

对应预测向量

$$
\widehat y
=
\Phi V\widehat\eta.
$$

---

## 2. 把预测写成一个投影

定义

$$
P_k
=
\Phi V(V^\top\Phi^\top\Phi V)^{-1}V^\top\Phi^\top.
$$

那么

$$
\widehat y=P_k y.
$$

$P_k$ 是到子空间

$$
\operatorname{Im}(\Phi V)\subseteq\mathbb R^n
$$

的正交投影。因此

$$
P_k^\top=P_k,\qquad P_k^2=P_k,\qquad \operatorname{rank}(P_k)=k.
$$

这说明 PCR 实际上是：

1. 只允许预测向量落在前 $k$ 个主成分生成的子空间中；
2. 将 $y$ 正交投影到该子空间。

---

## 3. 代入线性模型

假设固定设计模型

$$
y=\Phi\theta_*+\varepsilon,
$$

其中

$$
\mathbb E[\varepsilon]=0,
\qquad
\mathbb E[\varepsilon\varepsilon^\top]=\sigma^2I_n.
$$

记无噪声的真实响应向量为

$$
\mu=\Phi\theta_*.
$$

PCR 的预测误差为

$$
\widehat y-\mu
=
P_k(\mu+\varepsilon)-\mu
=
-(I-P_k)\mu+P_k\varepsilon.
$$

其中：

- $-(I-P_k)\mu$ 是因为只保留前 $k$ 个主成分造成的系统误差；
- $P_k\varepsilon$ 是投影后的噪声。

平方并取期望：

$$
\begin{aligned}
\mathbb E_\varepsilon
\|\widehat y-\mu\|_2^2
&=
\|(I-P_k)\mu\|_2^2
+
\mathbb E\|P_k\varepsilon\|_2^2\\
&\quad
-2\mathbb E\langle (I-P_k)\mu,P_k\varepsilon\rangle.
\end{aligned}
$$

交叉项为零，因为

$$
\mathbb E[\varepsilon]=0.
$$

所以得到了标准的偏差-方差分解：

$$
\frac1n
\mathbb E_\varepsilon
\|\widehat y-\Phi\theta_*\|_2^2
=
\underbrace{
\frac1n\mathbb E\|P_k\varepsilon\|_2^2
}_{\text{variance}}
+
\underbrace{
\frac1n\|(I-P_k)\Phi\theta_*\|_2^2
}_{\text{bias}}.
$$

---

## 4. 为什么方差等于 $\sigma^2k/n$

利用迹公式，

$$
\begin{aligned}
\mathbb E\|P_k\varepsilon\|_2^2
&=
\mathbb E[\varepsilon^\top P_k^\top P_k\varepsilon]\\
&=
\mathbb E[\varepsilon^\top P_k\varepsilon]\\
&=
\operatorname{tr}\!\left(
P_k\mathbb E[\varepsilon\varepsilon^\top]
\right)\\
&=
\sigma^2\operatorname{tr}(P_k).
\end{aligned}
$$

由于 $P_k$ 是秩为 $k$ 的正交投影，

$$
\operatorname{tr}(P_k)=k.
$$

因此

$$
\boxed{
\frac1n\mathbb E\|P_k\varepsilon\|_2^2
=
\frac{\sigma^2k}{n}.
}
$$

直观上，每保留一个自由方向，就要付出约

$$
\frac{\sigma^2}{n}
$$

的方差代价；保留 $k$ 个方向就是 $\sigma^2k/n$。

---

## 5. 偏差项如何变成矩阵形式

偏差项为

$$
\frac1n\|(I-P_k)\Phi\theta_*\|_2^2.
$$

由于 $P_k$ 是正交投影，

$$
(I-P_k)^\top(I-P_k)=I-P_k.
$$

所以

$$
\begin{aligned}
\frac1n\|(I-P_k)\Phi\theta_*\|_2^2
&=
\frac1n
\theta_*^\top\Phi^\top(I-P_k)\Phi\theta_*\\
&=
\theta_*^\top\widehat\Sigma\theta_*
-
\frac1n\theta_*^\top\Phi^\top P_k\Phi\theta_*.
\end{aligned}
$$

再代入 $P_k$，得到

$$
\frac1n\Phi^\top P_k\Phi
=
\widehat\Sigma V
(V^\top\widehat\Sigma V)^{-1}
V^\top\widehat\Sigma.
$$

因此偏差为

$$
\boxed{
\theta_*^\top\widehat\Sigma\theta_*
-
\theta_*^\top
\widehat\Sigma V
(V^\top\widehat\Sigma V)^{-1}
V^\top\widehat\Sigma
\theta_*.
}
$$

于是总风险是

$$
\frac1n
\mathbb E_\varepsilon
\|\widehat y-\Phi\theta_*\|_2^2
=
\frac{\sigma^2k}{n}
+
\theta_*^\top\widehat\Sigma\theta_*
-
\theta_*^\top
\widehat\Sigma V
(V^\top\widehat\Sigma V)^{-1}
V^\top\widehat\Sigma\theta_*.
$$

---

## 6. 为什么利用特征向量后会简化

因为 $V$ 的列是 $\widehat\Sigma$ 的前 $k$ 个特征向量，所以

$$
\widehat\Sigma V=VD,
$$

其中

$$
D=\operatorname{Diag}(\lambda_1,\ldots,\lambda_k).
$$

同时

$$
V^\top\widehat\Sigma V=D.
$$

因此

$$
\begin{aligned}
\widehat\Sigma V
(V^\top\widehat\Sigma V)^{-1}
V^\top\widehat\Sigma
&=
VD D^{-1}DV^\top\\
&=
VDV^\top.
\end{aligned}
$$

所以偏差项化为

$$
\theta_*^\top
(\widehat\Sigma-VDV^\top)
\theta_*.
$$

又因为 $VV^\top$ 是前 $k$ 个特征方向上的投影，而且它与 $\widehat\Sigma$ 可交换，

$$
\widehat\Sigma-VDV^\top
=
(I-VV^\top)\widehat\Sigma(I-VV^\top).
$$

所以

$$
\boxed{
\frac1n
\mathbb E_\varepsilon
\|\widehat y-\Phi\theta_*\|_2^2
=
\frac{\sigma^2k}{n}
+
\theta_*^\top
(I-VV^\top)
\widehat\Sigma
(I-VV^\top)
\theta_*.
}
$$

---

## 7. 在特征坐标下看最清楚

把真实参数展开为

$$
\theta_*=\sum_{j=1}^d a_j u_j.
$$

PCR 保留 $u_1,\ldots,u_k$，丢弃 $u_{k+1},\ldots,u_d$。因此

$$
(I-VV^\top)\theta_*
=
\sum_{j>k}a_j u_j.
$$

于是偏差精确等于

$$
\boxed{
\sum_{j=k+1}^d\lambda_j a_j^2.
}
$$

所以整个风险的精确表达式是

$$
\boxed{
\frac1n
\mathbb E_\varepsilon
\|\widehat y-\Phi\theta_*\|_2^2
=
\frac{\sigma^2k}{n}
+
\sum_{j>k}\lambda_j a_j^2.
}
$$

这比教材后面的粗略上界更有解释力：

- 保留的每个方向贡献方差 $\sigma^2/n$；
- 丢弃第 $j$ 个方向造成偏差 $\lambda_j a_j^2$。

---

## 8. 为什么偏差不超过 $\lambda_{k+1}\|\theta_*\|^2$

由于对所有 $j>k$，

$$
\lambda_j\le\lambda_{k+1},
$$

所以

$$
\sum_{j>k}\lambda_j a_j^2
\le
\lambda_{k+1}\sum_{j>k}a_j^2
\le
\lambda_{k+1}\|\theta_*\|_2^2.
$$

也可以从算子范数角度说：

$$
\left\|
(I-VV^\top)\widehat\Sigma(I-VV^\top)
\right\|_{\mathrm{op}}
=
\lambda_{k+1}.
$$

因此

$$
\theta_*^\top
(I-VV^\top)\widehat\Sigma(I-VV^\top)
\theta_*
\le
\lambda_{k+1}\|\theta_*\|_2^2.
$$

---

## 9. 为什么 $\lambda_{k+1}\le \operatorname{tr}(\widehat\Sigma)/(k+1)$

由于特征值按降序排列，

$$
\lambda_1,\ldots,\lambda_{k+1}
\ge
\lambda_{k+1}.
$$

于是

$$
(k+1)\lambda_{k+1}
\le
\sum_{j=1}^{k+1}\lambda_j
\le
\sum_{j=1}^d\lambda_j
=
\operatorname{tr}(\widehat\Sigma).
$$

所以

$$
\lambda_{k+1}
\le
\frac{\operatorname{tr}(\widehat\Sigma)}{k+1}
\le
\frac{\operatorname{tr}(\widehat\Sigma)}{k}.
$$

最终得到较粗但简洁的风险界：

$$
\boxed{
\frac1n
\mathbb E_\varepsilon
\|\widehat y-\Phi\theta_*\|_2^2
\le
\frac{\sigma^2k}{n}
+
\frac{\|\theta_*\|_2^2\operatorname{tr}(\widehat\Sigma)}{k}.
}
$$

这里第一项随 $k$ 增大，第二项随 $k$ 减小，正是偏差-方差权衡。

---

## 10. 最优的 $k$ 怎么算

记

$$
A=\frac{\sigma^2}{n},
\qquad
B=\|\theta_*\|_2^2\operatorname{tr}(\widehat\Sigma).
$$

需要近似最小化

$$
Ak+\frac{B}{k}.
$$

将 $k$ 暂时视作正实数，求导：

$$
A-\frac{B}{k^2}=0.
$$

所以

$$
k^2=\frac BA,
$$

即

$$
\boxed{
k_*
=
\frac{\|\theta_*\|_2
\sqrt{\operatorname{tr}(\widehat\Sigma)}
\sqrt n}{\sigma}.
}
$$

实际需要取最接近的可行整数，并满足

$$
1\le k\le \operatorname{rank}(\Phi).
$$

此时风险量级为

$$
\boxed{
\frac{\sigma\|\theta_*\|_2
\sqrt{\operatorname{tr}(\widehat\Sigma)}}{\sqrt n}
}
$$

差一个常数因子 $2$。

实际中 $\theta_*$ 和 $\sigma$ 未知，因此 $k$ 通常通过验证集或交叉验证选择。

---

## 11. 与 ridge regression 的对应关系

ridge 的粗略风险界通常具有形式

$$
\lambda\|\theta_*\|_2^2
+
\frac{\sigma^2}{n}
\frac{\operatorname{tr}(\widehat\Sigma)}{\lambda}.
$$

PCR 的界是

$$
\frac{\sigma^2k}{n}
+
\frac{\|\theta_*\|_2^2\operatorname{tr}(\widehat\Sigma)}{k}.
$$

令

$$
\boxed{
k\sim\frac{\operatorname{tr}(\widehat\Sigma)}{\lambda},
}
$$

则

$$
\frac{\sigma^2k}{n}
\sim
\frac{\sigma^2}{n}
\frac{\operatorname{tr}(\widehat\Sigma)}{\lambda},
$$

而

$$
\frac{\|\theta_*\|^2\operatorname{tr}(\widehat\Sigma)}{k}
\sim
\lambda\|\theta_*\|^2.
$$

因此两者的风险界具有相同结构。

但它们的谱处理方式不同：

$$
\text{PCR:}\qquad
g_j=
\begin{cases}
1,&j\le k,\\
0,&j>k,
\end{cases}
$$

是**硬截断**；

而 ridge 对第 $j$ 个特征方向的收缩因子大致为

$$
\text{ridge:}\qquad
g_j=\frac{\lambda_j}{\lambda_j+\lambda},
$$

是**软收缩**。

---

## 12. 这一结果的实质

PCR 的思想可以压缩成一句话：

$$
\boxed{
\text{保留更多主成分}
\Rightarrow
\text{偏差下降，但方差上升。}
}
$$

不过需要注意，PCA 只观察输入 $\Phi$，不观察响应 $y$。它认为“输入方差小的方向不重要”，但对预测而言未必成立：某个低方差方向可能恰好有很大的真实系数 $a_j$。这种风险正体现在精确偏差

$$
\sum_{j>k}\lambda_j a_j^2
$$

中。因此 PCR 是一种无监督的谱正则化方法，而不是必然最优的监督降维方法。

## Prompt:
2026/7/14 18:56:59

所以这是对于数据进行处理了吗？我们已经有n个样本，每个样本的维度是d。我们需要将其转化为n个维度为k的向量，方法就是找一个d*k的矩阵，但是我们怎样找到这样的矩阵呢？我们是希望找到一个协方差矩阵对应的信息尽可能变换。

## Response:
2026/7/14 18:57:01

对，这里首先是在对特征数据做降维处理。

你原来有

$$
\Phi\in\mathbb R^{n\times d},
$$

其中第 $i$ 行是第 $i$ 个样本的 $d$ 维特征：

$$
\phi(x_i)^\top\in\mathbb R^{1\times d}.
$$

我们要找一个矩阵

$$
V\in\mathbb R^{d\times k},
$$

把每个 $d$ 维样本映射成 $k$ 维：

$$
z_i=V^\top\phi(x_i)\in\mathbb R^k.
$$

把所有样本放在一起，就是

$$
Z=\Phi V\in\mathbb R^{n\times k}.
$$

关键问题确实是：**这个 $V$ 怎样选？**

---

## 1. PCA 希望保留什么

PCA 的标准目标不是保留所有意义上的“信息”，而是：

> 在所有 $k$ 维线性子空间中，找到一个使投影后数据总方差最大的子空间。

通常先把数据中心化：

$$
X=\Phi-\mathbf 1\bar\phi^\top,
\qquad
\bar\phi=\frac1n\sum_{i=1}^n\phi(x_i).
$$

然后定义经验协方差矩阵

$$
\widehat\Sigma
=
\frac1nX^\top X
\in\mathbb R^{d\times d}.
$$

在教材的固定设计回归分析中，有时直接使用非中心化矩阵

$$
\widehat\Sigma=\frac1n\Phi^\top\Phi,
$$

但标准 PCA 通常先中心化。`lftp.pdf`

---

## 2. 先找一个方向

假设先只想降到一维，即 $k=1$。

我们找一个单位向量

$$
v\in\mathbb R^d,
\qquad
\|v\|_2=1.
$$

第 $i$ 个样本投影到该方向后得到

$$
z_i=v^\top x_i.
$$

所有投影值的经验方差是

$$
\frac1n\sum_{i=1}^n(v^\top x_i)^2.
$$

由于数据已经中心化，这等于

$$
\begin{aligned}
\frac1n\sum_{i=1}^n(v^\top x_i)^2
&=
\frac1n\sum_{i=1}^n
v^\top x_ix_i^\top v\\
&=
v^\top
\left(
\frac1n\sum_{i=1}^n x_ix_i^\top
\right)v\\
&=
v^\top\widehat\Sigma v.
\end{aligned}
$$

因此 PCA 要解的是

$$
\max_{\|v\|_2=1}
v^\top\widehat\Sigma v.
$$

根据 Rayleigh 商的结论，最大值是

$$
\lambda_1,
$$

最优方向 $v$ 是 $\widehat\Sigma$ 最大特征值对应的特征向量：

$$
\widehat\Sigma v_1=\lambda_1v_1.
$$

所以，第一主成分方向就是

$$
v_1=\text{协方差矩阵最大特征值对应的特征向量}.
$$

---

## 3. 找 $k$ 个方向

现在需要一个 $d\times k$ 矩阵

$$
V=[v_1,\ldots,v_k].
$$

为了避免重复记录同一个方向的信息，要求这些方向标准正交：

$$
V^\top V=I_k.
$$

投影后的数据为

$$
Z=XV.
$$

它的经验协方差矩阵为

$$
\frac1nZ^\top Z
=
\frac1nV^\top X^\top XV
=
V^\top\widehat\Sigma V.
$$

投影后所有 $k$ 个方向的总方差是该矩阵的迹：

$$
\operatorname{tr}(V^\top\widehat\Sigma V).
$$

因此 PCA 求解

$$
\boxed{
\max_{V\in\mathbb R^{d\times k}}
\operatorname{tr}(V^\top\widehat\Sigma V)
\quad
\text{s.t.}\quad
V^\top V=I_k.
}
$$

该问题的解就是取协方差矩阵的前 $k$ 个特征向量：

$$
\boxed{
V=[v_1,\ldots,v_k],
}
$$

其中

$$
\widehat\Sigma v_j=\lambda_jv_j,
\qquad
\lambda_1\ge\lambda_2\ge\cdots\ge\lambda_d.
$$

换言之，步骤是：

$$
\Phi
\longrightarrow
\widehat\Sigma=\frac1n\Phi^\top\Phi
\longrightarrow
\text{求前 }k\text{ 个特征向量}
\longrightarrow
V
\longrightarrow
\Phi V.
$$

---

## 4. 为什么是协方差矩阵的特征向量

设完整特征值分解为

$$
\widehat\Sigma
=
U
\begin{pmatrix}
\lambda_1&&\\
&\ddots&\\
&&\lambda_d
\end{pmatrix}
U^\top,
$$

其中

$$
U=[v_1,\ldots,v_d].
$$

这意味着在坐标系 $v_1,\ldots,v_d$ 下，数据在不同方向上的方差分别是

$$
\lambda_1,\lambda_2,\ldots,\lambda_d.
$$

因此：

- $v_1$ 是数据变化最大的方向；
- $v_2$ 是与 $v_1$ 正交的方向中变化最大的方向；
- $v_3$ 是与前两个方向正交时变化最大的方向；
- 依此类推。

选取前 $k$ 个方向，就是保留方差最大的 $k$ 个方向。

投影后的协方差矩阵变成

$$
V^\top\widehat\Sigma V
=
\operatorname{Diag}(\lambda_1,\ldots,\lambda_k).
$$

这还说明 PCA 后的不同坐标彼此不相关。

---

## 5. “保留最大方差”等价于“重构误差最小”

PCA 还可以从另一个角度理解。

投影后的低维坐标是

$$
Z=XV.
$$

把它映射回原空间，得到

$$
\widetilde X=ZV^\top=XV V^\top.
$$

其中 $VV^\top$ 是到所选 $k$ 维子空间的正交投影。

我们希望重构数据尽可能接近原始数据：

$$
\min_{V^\top V=I_k}
\|X-XVV^\top\|_F^2.
$$

可以推导出

$$
\|X-XVV^\top\|_F^2
=
\|X\|_F^2
-
n\operatorname{tr}(V^\top\widehat\Sigma V).
$$

由于 $\|X\|_F^2$ 是常数，最小化重构误差等价于最大化保留方差：

$$
\boxed{
\min\|X-XVV^\top\|_F^2
\quad\Longleftrightarrow\quad
\max\operatorname{tr}(V^\top\widehat\Sigma V).
}
$$

最小重构误差为

$$
n\sum_{j=k+1}^d\lambda_j.
$$

也就是说，丢掉的总方差就是后面那些特征值之和。

---

## 6. 在回归问题中的完整流程

原模型是

$$
y=\Phi\theta_*+\varepsilon.
$$

PCA 首先把设计矩阵降维：

$$
\Phi\in\mathbb R^{n\times d}
\quad\longrightarrow\quad
\Phi V\in\mathbb R^{n\times k}.
$$

然后在新特征上做 OLS：

$$
\widehat\eta
=
\arg\min_{\eta\in\mathbb R^k}
\|y-\Phi V\eta\|_2^2.
$$

此时预测函数可以写成

$$
\widehat y=\Phi V\widehat\eta.
$$

如果想写回原来的 $d$ 维参数形式，可以令

$$
\widehat\theta_{\mathrm{PCR}}=V\widehat\eta.
$$

那么

$$
\widehat\theta_{\mathrm{PCR}}
\in\operatorname{span}\{v_1,\ldots,v_k\}.
$$

所以 PCR 实际上限制参数只能位于前 $k$ 个主成分张成的子空间中。

---

## 7. 一个重要修正：最大方差不一定等于对预测最有用

PCA 选择 $V$ 时只使用 $\Phi$，完全不看 $y$。因此它保留的是：

$$
\text{输入数据中变化最大的方向},
$$

而不一定是

$$
\text{对预测 }y\text{ 最有用的方向}.
$$

例如二维数据中：

$$
\lambda_1=100,\qquad \lambda_2=0.1.
$$

PCA 若降到一维，会选择第一个方向。但如果真实关系是

$$
y=20x_2+\varepsilon,
$$

而 $y$ 几乎不依赖 $x_1$，那么低方差的第二个方向反而是预测的关键。PCA 可能会把它丢掉。

因此更准确地说：

$$
\boxed{
\text{PCA 保留的是最大输入方差，而不是必然保留最大预测信息。}
}
$$

这也是 PCR 的局限：它是一种先无监督降维、再监督回归的方法。

---

最终，寻找 $V$ 的方法可以概括为：

$$
\boxed{
\begin{aligned}
&1.\ \text{中心化数据 }X;\\
&2.\ \text{计算 }\widehat\Sigma=\frac1nX^\top X;\\
&3.\ \text{对 }\widehat\Sigma\text{ 做特征值分解};\\
&4.\ \text{取最大 }k\text{ 个特征值对应的特征向量};\\
&5.\ V=[v_1,\ldots,v_k],\quad Z=XV.
\end{aligned}
}
$$

这里的 $V$ 不是通过回归拟合得到的，而是通过设计矩阵自身的协方差结构计算出来的。

## Prompt:
2026/7/14 19:30:38

Thus, minimizing kΦ−ΦV V ⊤k2
F is equivalent to maximizing tr

V ⊤Φ⊤ΦV

with respect
to a matrix V ∈ Rd×k with orthonormal columns. Given an eigenvalue decomposition of
the noncentered empirical covariance matrix bΣ = 1
nΦ⊤Φ = U Diag(λ)U⊤, with U ∈ Rd×d
orthogonal and λ a vector with nonincreasing components, an optimal V is obtained by
taking the first k columns of U; that is, a basis of the principal subspace of dimension k.
Such a basis can be computed by various algorithms from numerical algebra (Golub and
Loan, 1996). See exercise 3.9 for a simple alternating optimization algorithm.

## Response:
2026/7/14 19:30:53

这段是在严格说明：**PCA 的“最小重构误差”问题，最终等价于选择协方差矩阵最大的 $k$ 个特征值对应的特征向量。** `lftp.pdf`

设

$$
\Phi\in\mathbb R^{n\times d},\qquad
V\in\mathbb R^{d\times k},\qquad
V^\top V=I_k.
$$

其中 $V$ 的列张成一个 $k$ 维子空间。

---

## 1. $\Phi VV^\top$ 是什么

因为 $V^\top V=I_k$，矩阵

$$
P=VV^\top\in\mathbb R^{d\times d}
$$

是到子空间 $\operatorname{span}(V)$ 上的正交投影矩阵。

对于第 $i$ 个样本行向量 $\phi_i^\top$，它的低维坐标是

$$
\phi_i^\top V\in\mathbb R^{1\times k},
$$

再映射回原来的 $d$ 维空间：

$$
\phi_i^\top VV^\top.
$$

因此

$$
\Phi VV^\top
$$

就是所有样本投影到这个 $k$ 维子空间之后的重构结果。

所以

$$
\|\Phi-\Phi VV^\top\|_F^2
$$

衡量的是所有样本的总重构误差：

$$
\|\Phi-\Phi VV^\top\|_F^2
=
\sum_{i=1}^n
\|\phi_i-VV^\top\phi_i\|_2^2.
$$

PCA 希望选择一个 $k$ 维子空间，使这个误差最小。

---

## 2. 为什么最小化重构误差等价于最大化迹

令

$$
A=\Phi^\top\Phi.
$$

由于 $P=VV^\top$ 满足

$$
P^\top=P,\qquad P^2=P,
$$

有

$$
\Phi-\Phi VV^\top=\Phi(I-P).
$$

于是

$$
\begin{aligned}
\|\Phi-\Phi VV^\top\|_F^2
&=
\operatorname{tr}
\left[
(\Phi(I-P))^\top\Phi(I-P)
\right]\\
&=
\operatorname{tr}
\left[
(I-P)\Phi^\top\Phi(I-P)
\right].
\end{aligned}
$$

展开：

$$
\begin{aligned}
\|( \Phi-\Phi P)\|_F^2
&=
\operatorname{tr}(A)
-2\operatorname{tr}(AP)
+\operatorname{tr}(PAP).
\end{aligned}
$$

对于最后一项，利用迹的循环性质和 $P^2=P$：

$$
\operatorname{tr}(PAP)
=
\operatorname{tr}(APP)
=
\operatorname{tr}(AP).
$$

因此

$$
\|\Phi-\Phi VV^\top\|_F^2
=
\operatorname{tr}(A)-\operatorname{tr}(AP).
$$

而

$$
\operatorname{tr}(AP)
=
\operatorname{tr}(\Phi^\top\Phi VV^\top)
=
\operatorname{tr}(V^\top\Phi^\top\Phi V).
$$

所以

$$
\boxed{
\|\Phi-\Phi VV^\top\|_F^2
=
\operatorname{tr}(\Phi^\top\Phi)
-
\operatorname{tr}(V^\top\Phi^\top\Phi V).
}
$$

第一项

$$
\operatorname{tr}(\Phi^\top\Phi)=\|\Phi\|_F^2
$$

与 $V$ 无关。因此

$$
\boxed{
\min_{V^\top V=I_k}
\|\Phi-\Phi VV^\top\|_F^2
\iff
\max_{V^\top V=I_k}
\operatorname{tr}(V^\top\Phi^\top\Phi V).
}
$$

含义是：

> 最小化丢掉的能量，等价于最大化保留下来的能量。

---

## 3. 这个迹表示什么

设

$$
V=[v_1,\ldots,v_k].
$$

那么

$$
\begin{aligned}
\operatorname{tr}(V^\top\Phi^\top\Phi V)
&=
\sum_{j=1}^k
v_j^\top\Phi^\top\Phi v_j\\
&=
\sum_{j=1}^k
\|\Phi v_j\|_2^2.
\end{aligned}
$$

除以 $n$ 后：

$$
\frac1n
\operatorname{tr}(V^\top\Phi^\top\Phi V)
=
\sum_{j=1}^k
v_j^\top\widehat\Sigma v_j,
$$

其中

$$
\widehat\Sigma=\frac1n\Phi^\top\Phi.
$$

它表示数据在 $v_1,\ldots,v_k$ 这些方向上的总二阶能量。若数据已经中心化，就是总方差。

---

## 4. 为什么选择前 $k$ 个特征向量

对经验协方差矩阵作特征值分解：

$$
\widehat\Sigma
=
U\operatorname{Diag}(\lambda_1,\ldots,\lambda_d)U^\top,
$$

其中

$$
\lambda_1\ge\lambda_2\ge\cdots\ge\lambda_d\ge0.
$$

记

$$
U=[u_1,\ldots,u_d].
$$

令

$$
W=U^\top V.
$$

由于 $U$ 是正交矩阵，且 $V^\top V=I_k$，所以

$$
W^\top W
=
V^\top UU^\top V
=
I_k.
$$

目标函数变成

$$
\begin{aligned}
\operatorname{tr}(V^\top\widehat\Sigma V)
&=
\operatorname{tr}
\left(
V^\top U\operatorname{Diag}(\lambda)U^\top V
\right)\\
&=
\operatorname{tr}
\left(
W^\top\operatorname{Diag}(\lambda)W
\right).
\end{aligned}
$$

把 $W$ 的第 $i$ 行记作 $w_i^\top$，则

$$
\operatorname{tr}
\left(
W^\top\operatorname{Diag}(\lambda)W
\right)
=
\sum_{i=1}^d
\lambda_i\|w_i\|_2^2.
$$

定义

$$
\alpha_i=\|w_i\|_2^2.
$$

这些数满足

$$
0\le\alpha_i\le1,
\qquad
\sum_{i=1}^d\alpha_i=k.
$$

于是问题变成：

$$
\max
\sum_{i=1}^d\lambda_i\alpha_i
$$

满足

$$
0\le\alpha_i\le1,\qquad \sum_i\alpha_i=k.
$$

由于

$$
\lambda_1\ge\lambda_2\ge\cdots\ge\lambda_d,
$$

显然应当把全部“权重”放在最大的 $k$ 个特征值上：

$$
\alpha_1=\cdots=\alpha_k=1,
\qquad
\alpha_{k+1}=\cdots=\alpha_d=0.
$$

因此最大值为

$$
\boxed{
\lambda_1+\cdots+\lambda_k.
}
$$

对应的一个最优解是

$$
\boxed{
V=[u_1,\ldots,u_k].
}
$$

这就是前 $k$ 个主成分方向。

这个结果也称为 **Ky Fan 最大值原理**：

$$
\max_{V^\top V=I_k}
\operatorname{tr}(V^\top\widehat\Sigma V)
=
\sum_{j=1}^k\lambda_j.
$$

---

## 5. 最小重构误差是多少

总能量是

$$
\operatorname{tr}(\Phi^\top\Phi)
=
n\sum_{j=1}^d\lambda_j.
$$

保留下来的最大能量是

$$
n\sum_{j=1}^k\lambda_j.
$$

因此最小重构误差为

$$
\boxed{
\min_{V^\top V=I_k}
\|\Phi-\Phi VV^\top\|_F^2
=
n\sum_{j=k+1}^d\lambda_j.
}
$$

也就是说：

- 前 $k$ 个特征值代表保留的信息量；
- 后 $d-k$ 个特征值之和代表丢失的信息量。

常见的解释方差比例是

$$
\frac{\lambda_1+\cdots+\lambda_k}
{\lambda_1+\cdots+\lambda_d}.
$$

例如该比例达到 $95\%$，就表示前 $k$ 个主成分保留了约 $95\%$ 的总方差。

---

## 6. $V$ 是否唯一

严格来说，最优的是一个子空间，而不一定是唯一的基。

若

$$
\lambda_k>\lambda_{k+1},
$$

则前 $k$ 维主子空间是唯一的，但它的正交基可以旋转。任何

$$
V=U_kQ,
$$

其中

$$
U_k=[u_1,\ldots,u_k],
\qquad
Q\in\mathbb R^{k\times k},\quad Q^\top Q=I_k,
$$

都会给出相同的投影：

$$
VV^\top
=
U_kQQ^\top U_k^\top
=
U_kU_k^\top.
$$

因此 PCA 真正确定的是

$$
\operatorname{span}\{u_1,\ldots,u_k\},
$$

而不是某一组绝对唯一的坐标轴。

---

## 7. 非中心化协方差的含义

教材这里使用

$$
\widehat\Sigma=\frac1n\Phi^\top\Phi,
$$

称为非中心化经验协方差矩阵。

这意味着数据被投影到一个**经过原点的线性子空间**上：

$$
\Phi\approx\Phi VV^\top.
$$

标准 PCA 通常先计算样本均值

$$
\bar\phi=\frac1n\sum_{i=1}^n\phi_i,
$$

再中心化：

$$
X=\Phi-\mathbf 1\bar\phi^\top,
$$

然后对

$$
\frac1nX^\top X
$$

做特征值分解。这相当于寻找一个不一定经过原点、而是经过样本均值的仿射子空间。

在这里，教材为了与线性回归中的

$$
\widehat\Sigma=\frac1n\Phi^\top\Phi
$$

保持统一，因此使用非中心化版本。核心数学推导不变。

## Prompt:
2026/7/14 19:35:20

Given Φ ∈ Rn×d, we consider minimizing kΦ− ADk2
F with respect to
D ∈ Rk×d and A ∈ Rn×k. Show that the optimal solution is such that AD is the data
matrix after performing PCA. Using the singular value decomposition of Φ, show that
an alternating minimization algorithm that iteratively minimizes kΦ−ADk2
F with respect
to A, and then D, converges to the global optimum for almost all initializations of D;
compute the corresponding updates.

## Response:
2026/7/14 19:35:28

> **计算交替最小化PCA更新**
>
>
> **计算PCA更新并提取文件中题目**
>
> 
>
> 思考了 45s

这道题的关键是把交替最小化识别成一个 **block power method（子空间幂迭代）**。虽然

$$
\min_{A,D}\|\Phi-AD\|_F^2
$$

对 $(A,D)$ 联合来看是非凸的，但其子空间迭代会把 $D$ 的行空间推向 $\Phi^\top\Phi$ 的前 $k$ 个特征子空间。题目见教材 Exercise 3.9。`lftp.pdf`

设

$$
\Phi\in\mathbb R^{n\times d},\qquad
A\in\mathbb R^{n\times k},\qquad
D\in\mathbb R^{k\times d},
$$

并假设 $k\le \operatorname{rank}(\Phi)$。

---

# 1. 为什么全局最优解就是 PCA

令

$$
B=AD.
$$

由于 $A$ 有 $k$ 列、$D$ 有 $k$ 行，

$$
\operatorname{rank}(AD)\le k.
$$

反过来，任意秩不超过 $k$ 的矩阵 $B\in\mathbb R^{n\times d}$，都可以写成 $B=AD$。因此

$$
\min_{A,D}\|\Phi-AD\|_F^2
=
\min_{\operatorname{rank}(B)\le k}\|\Phi-B\|_F^2.
$$

这就是最佳秩 $k$ 矩阵逼近问题。

设 $\Phi$ 的奇异值分解为

$$
\Phi
=
U\Sigma W^\top
=
\sum_{j=1}^r\sigma_j u_jw_j^\top,
$$

其中

$$
\sigma_1\ge\sigma_2\ge\cdots\ge\sigma_r>0,
\qquad r=\operatorname{rank}(\Phi).
$$

记

$$
U_k=[u_1,\ldots,u_k],\qquad
W_k=[w_1,\ldots,w_k],
$$

以及

$$
\Sigma_k=\operatorname{Diag}(\sigma_1,\ldots,\sigma_k).
$$

根据 Eckart-Young 定理，最佳秩 $k$ 逼近为

$$
\boxed{
\Phi_k=U_k\Sigma_kW_k^\top
}
$$

且最小目标值为

$$
\boxed{
\min_{A,D}\|\Phi-AD\|_F^2
=
\sum_{j>k}\sigma_j^2.
}
$$

另一方面，

$$
\Phi W_kW_k^\top
=
U\Sigma W^\top W_kW_k^\top
=
U_k\Sigma_kW_k^\top.
$$

所以

$$
\boxed{
\Phi_k=\Phi W_kW_k^\top.
}
$$

而 $W_k$ 正是

$$
\Phi^\top\Phi
=
W\Sigma^\top\Sigma W^\top
$$

最大的 $k$ 个特征值对应的特征向量。因此 $\Phi W_kW_k^\top$ 就是 PCA 投影后再重构得到的数据矩阵。

注意：

- PCA 的降维坐标是 $\Phi W_k\in\mathbb R^{n\times k}$；
- $AD\in\mathbb R^{n\times d}$ 对应的是重构矩阵
  $$
  (\Phi W_k)W_k^\top.
  $$

一种全局最优分解是

$$
A_*=U_k\Sigma_k,\qquad D_*=W_k^\top.
$$

但 $A,D$ 本身并不唯一。对任意可逆矩阵 $R\in\mathbb R^{k\times k}$，

$$
A_*D_*=(A_*R)(R^{-1}D_*).
$$

真正唯一或重要的是乘积 $AD$ 以及它对应的子空间。

---

# 2. 固定 $D$，更新 $A$

定义

$$
F(A,D)=\|\Phi-AD\|_F^2.
$$

固定 $D$，对 $A$ 求导：

$$
\nabla_A F
=
2(AD-\Phi)D^\top.
$$

令梯度为零：

$$
(AD-\Phi)D^\top=0,
$$

即

$$
A(DD^\top)=\Phi D^\top.
$$

若 $D$ 满行秩，则 $DD^\top$ 可逆，所以

$$
\boxed{
A^{(t+1)}
=
\Phi(D^{(t)})^\top
\left[D^{(t)}(D^{(t)})^\top\right]^{-1}.
}
$$

用伪逆可以统一写成

$$
A^{(t+1)}=\Phi(D^{(t)})^\dagger.
$$

固定 $D$ 后，对应的乘积是

$$
\begin{aligned}
A^{(t+1)}D^{(t)}
&=
\Phi(D^{(t)})^\top
\left[D^{(t)}(D^{(t)})^\top\right]^{-1}
D^{(t)}\\
&=
\Phi P_{\operatorname{row}(D^{(t)})},
\end{aligned}
$$

其中

$$
P_{\operatorname{row}(D)}
=
D^\top(DD^\top)^{-1}D
$$

是到 $D$ 的行空间的正交投影。

所以 $A$-更新的含义是：

> 将 $\Phi$ 投影到当前 $D$ 所表示的 $k$ 维特征子空间上。

---

# 3. 固定 $A$，更新 $D$

固定 $A$，对 $D$ 求导：

$$
\nabla_D F
=
2A^\top(AD-\Phi).
$$

令其为零：

$$
A^\top A D=A^\top\Phi.
$$

若 $A$ 满列秩，则

$$
\boxed{
D^{(t+1)}
=
\left[(A^{(t+1)})^\top A^{(t+1)}\right]^{-1}
(A^{(t+1)})^\top\Phi.
}
$$

也可以写成

$$
D^{(t+1)}=(A^{(t+1)})^\dagger\Phi.
$$

此时

$$
A^{(t+1)}D^{(t+1)}
=
P_{\operatorname{col}(A^{(t+1)})}\Phi,
$$

即将 $\Phi$ 投影到 $A^{(t+1)}$ 的列空间。

---

# 4. 把两个更新合起来

令

$$
M=\Phi^\top\Phi\in\mathbb R^{d\times d}.
$$

暂时省略迭代下标，记

$$
G=DD^\top,\qquad H=DMD^\top.
$$

由 $A$-更新，

$$
A=\Phi D^\top G^{-1}.
$$

因此

$$
A^\top A
=
G^{-1}D\Phi^\top\Phi D^\top G^{-1}
=
G^{-1}HG^{-1}.
$$

于是

$$
(A^\top A)^{-1}
=
GH^{-1}G.
$$

同时

$$
A^\top\Phi
=
G^{-1}D\Phi^\top\Phi
=
G^{-1}DM.
$$

代入 $D$-更新：

$$
\begin{aligned}
D_{\mathrm{new}}
&=
(A^\top A)^{-1}A^\top\Phi\\
&=
GH^{-1}G\,G^{-1}DM\\
&=
GH^{-1}DM.
\end{aligned}
$$

即

$$
\boxed{
D^{(t+1)}
=
D^{(t)}(D^{(t)})^\top
\left[
D^{(t)}M(D^{(t)})^\top
\right]^{-1}
D^{(t)}M.
}
$$

前面的矩阵

$$
D^{(t)}(D^{(t)})^\top
\left[
D^{(t)}M(D^{(t)})^\top
\right]^{-1}
$$

是可逆的 $k\times k$ 矩阵。左乘可逆矩阵不改变行空间，因此

$$
\boxed{
\operatorname{row}(D^{(t+1)})
=
\operatorname{row}(D^{(t)}M).
}
$$

递推可得

$$
\boxed{
\operatorname{row}(D^{(t)})
=
\operatorname{row}\left(D^{(0)}M^t\right).
}
$$

这正是对

$$
M=\Phi^\top\Phi
$$

执行的子空间幂迭代。

---

# 5. 利用 SVD 证明它收敛到前 $k$ 个主成分

由 SVD，

$$
M=\Phi^\top\Phi
=
W\Lambda W^\top,
$$

其中

$$
\Lambda
=
\operatorname{Diag}(\sigma_1^2,\ldots,\sigma_d^2).
$$

将其分块：

$$
W=[W_1\;W_2],
$$

其中

$$
W_1=W_k\in\mathbb R^{d\times k},
$$

并令

$$
\Lambda=
\begin{pmatrix}
\Lambda_1&0\\
0&\Lambda_2
\end{pmatrix},
$$

其中

$$
\Lambda_1
=
\operatorname{Diag}(\sigma_1^2,\ldots,\sigma_k^2).
$$

把初始化在奇异向量坐标系下写成

$$
D^{(0)}W=[B_1\;B_2],
$$

其中

$$
B_1=D^{(0)}W_1\in\mathbb R^{k\times k}.
$$

于是

$$
\begin{aligned}
D^{(0)}M^t
&=
D^{(0)}
W
\begin{pmatrix}
\Lambda_1^t&0\\
0&\Lambda_2^t
\end{pmatrix}
W^\top\\
&=
[B_1\Lambda_1^t\;\;B_2\Lambda_2^t]W^\top.
\end{aligned}
$$

若 $B_1$ 可逆，可以左乘可逆矩阵

$$
\Lambda_1^{-t}B_1^{-1},
$$

而不改变行空间。因此该行空间等价于

$$
\left[
I_k\;\;
\Lambda_1^{-t}B_1^{-1}B_2\Lambda_2^t
\right]W^\top.
$$

若在第 $k$ 个奇异值处存在谱隙

$$
\sigma_k>\sigma_{k+1},
$$

那么

$$
\begin{aligned}
\left\|
\Lambda_1^{-t}B_1^{-1}B_2\Lambda_2^t
\right\|_{\mathrm{op}}
&\le
\|B_1^{-1}B_2\|_{\mathrm{op}}
\frac{\sigma_{k+1}^{2t}}{\sigma_k^{2t}}\\
&=
\|B_1^{-1}B_2\|_{\mathrm{op}}
\left(
\frac{\sigma_{k+1}}{\sigma_k}
\right)^{2t}
\longrightarrow0.
\end{aligned}
$$

所以

$$
\operatorname{row}(D^{(t)})
\longrightarrow
\operatorname{span}\{w_1^\top,\ldots,w_k^\top\}.
$$

也就是

$$
\boxed{
\operatorname{col}\big((D^{(t)})^\top\big)
\longrightarrow
\operatorname{span}\{w_1,\ldots,w_k\}.
}
$$

这正是 PCA 的主子空间。

收敛速度由谱隙控制，几何收敛因子约为

$$
\boxed{
\left(\frac{\sigma_{k+1}}{\sigma_k}\right)^2.
}
$$

谱隙越大，收敛越快。

---

# 6. 为什么是“almost all initializations”

上面的条件是

$$
B_1=D^{(0)}W_1
$$

必须可逆，即初始化的行空间必须在前 $k$ 个右奇异方向上有完整的非零分量。

不满足条件意味着

$$
\det(D^{(0)}W_1)=0.
$$

这是关于 $D^{(0)}$ 各元素的一个非零多项式方程，其解集是 Lebesgue 测度为零的集合。

因此，如果 $D^{(0)}$ 来自任意连续随机分布，那么

$$
\mathbb P\bigl(\det(D^{(0)}W_1)=0\bigr)=0.
$$

这就是“对几乎所有初始化”的含义。

例如 $k=1$ 时，它就是普通幂迭代：

$$
d^{(t+1)}
\quad\text{的方向等于}\quad
d^{(t)}\Phi^\top\Phi.
$$

只要初始向量不恰好与第一右奇异向量正交，就会收敛到第一主成分。

---

# 7. 乘积 $AD$ 收敛到 PCA 重构

在 $A$-更新后，

$$
A^{(t+1)}D^{(t)}
=
\Phi P_{\operatorname{row}(D^{(t)})}.
$$

由于

$$
P_{\operatorname{row}(D^{(t)})}
\longrightarrow
W_kW_k^\top,
$$

所以

$$
A^{(t+1)}D^{(t)}
\longrightarrow
\Phi W_kW_k^\top
=
\Phi_k.
$$

同样，

$$
\operatorname{col}(A^{(t+1)})
=
\operatorname{col}\left(\Phi(D^{(t)})^\top\right)
\longrightarrow
\operatorname{span}(U_k),
$$

因此完整一轮更新后，

$$
A^{(t+1)}D^{(t+1)}
=
P_{\operatorname{col}(A^{(t+1)})}\Phi
\longrightarrow
U_kU_k^\top\Phi
=
\Phi_k.
$$

最终

$$
\boxed{
A^{(t)}D^{(t)}
\longrightarrow
U_k\Sigma_kW_k^\top
=
\Phi W_kW_k^\top.
}
$$

于是目标函数收敛到全局最小值

$$
\boxed{
\|\Phi-A^{(t)}D^{(t)}\|_F^2
\longrightarrow
\sum_{j>k}\sigma_j^2.
}
$$

严格来说，由于分解存在

$$
(A,D)\mapsto(AR,R^{-1}D)
$$

的不唯一性，通常保证的是：

- $D^{(t)}$ 的行空间收敛；
- $A^{(t)}$ 的列空间收敛；
- 乘积 $A^{(t)}D^{(t)}$ 收敛到全局最优 PCA 重构；

而不必要求两个因子分别收敛到某一组固定、唯一的 $A_*,D_*$。

---

## 最终算法

从几乎任意满行秩 $D^{(0)}$ 开始，重复：

$$
\boxed{
A^{(t+1)}
=
\Phi(D^{(t)})^\top
\left[
D^{(t)}(D^{(t)})^\top
\right]^{-1}
}
$$

以及

$$
\boxed{
D^{(t+1)}
=
\left[
(A^{(t+1)})^\top A^{(t+1)}
\right]^{-1}
(A^{(t+1)})^\top\Phi.
}
$$

其本质不是普通的“碰巧有效的非凸优化”，而是隐藏地执行

$$
\operatorname{row}(D^{(t+1)})
=
\operatorname{row}\bigl(D^{(t)}\Phi^\top\Phi\bigr),
$$

即对经验协方差矩阵进行子空间幂迭代，因此会找到 PCA 的主子空间。

## Prompt:
2026/7/14 19:41:09

本题是要求解什么？

## Response:
2026/7/14 19:41:12

本题不是单纯要求“算出一个 $A,D$”；它要求你证明一个完整结论：

> **用低秩矩阵分解 $AD$ 逼近数据矩阵 $\Phi$，其全局最优结果正是 PCA 的秩 $k$ 重构；而且交替最小化 $A,D$ 实际上会收敛到这个 PCA 解。** `lftp.pdf`

---

## 一、给定了什么，要求解什么

给定数据矩阵

$$
\Phi\in\mathbb R^{n\times d},
$$

其中有 $n$ 个样本，每个样本是 $d$ 维。

现在寻找两个矩阵

$$
A\in\mathbb R^{n\times k},
\qquad
D\in\mathbb R^{k\times d},
$$

使得

$$
AD\in\mathbb R^{n\times d}
$$

尽可能接近原数据矩阵 $\Phi$：

$$
\boxed{
\min_{A,D}\|\Phi-AD\|_F^2.
}
$$

由于

$$
\operatorname{rank}(AD)\le k,
$$

这其实是在问：

$$
\boxed{
\text{如何用一个秩不超过 }k\text{ 的矩阵，最好地逼近 }\Phi？
}
$$

这里 $A,D$ 的意义可以理解为：

- $A$：每个样本的 $k$ 维低维表示；
- $D$：把 $k$ 维表示映射回 $d$ 维原空间的基或解码矩阵；
- $AD$：降维后再重构的数据。

对于第 $i$ 个样本，

$$
\phi_i^\top\approx a_i^\top D,
$$

其中 $a_i^\top$ 是 $A$ 的第 $i$ 行，即样本的 $k$ 维编码。

---

## 二、本题第一部分要求证明什么

题目先要求证明：

$$
\min_{A,D}\|\Phi-AD\|_F^2
$$

的最优乘积 $AD$，就是 PCA 对数据进行 $k$ 维投影后再重构得到的矩阵。

设 $\Phi$ 的 SVD 为

$$
\Phi=U\Sigma V^\top.
$$

取前 $k$ 个奇异方向：

$$
U_k,\qquad \Sigma_k,\qquad V_k.
$$

则最佳秩 $k$ 逼近是

$$
\boxed{
AD=\Phi_k=U_k\Sigma_kV_k^\top.
}
$$

同时

$$
\Phi_k=\Phi V_kV_k^\top.
$$

这正是 PCA：

1. 降维：
   $$
   A=\Phi V_k=U_k\Sigma_k\in\mathbb R^{n\times k};
   $$

2. 重构：
   $$
   AD=(\Phi V_k)V_k^\top.
   $$

所以可以取

$$
\boxed{
A_*=\Phi V_k=U_k\Sigma_k,
\qquad
D_*=V_k^\top.
}
$$

题目并不是说 $A,D$ 唯一。实际上对任意可逆矩阵 $R\in\mathbb R^{k\times k}$，

$$
A_*D_*=(A_*R)(R^{-1}D_*).
$$

因此真正要求找到的是最优乘积 $AD$，而不是唯一的两个因子。

---

## 三、第二部分要求求出交替最小化更新

题目接着规定一种算法：

1. 固定 $D$，最小化关于 $A$ 的目标；
2. 固定新的 $A$，最小化关于 $D$ 的目标；
3. 不断重复。

你需要计算这两个子问题的闭式解。

### 固定 $D$，求 $A$

$$
A_{t+1}
=
\arg\min_A\|\Phi-AD_t\|_F^2.
$$

正规方程为

$$
A_{t+1}D_tD_t^\top=\Phi D_t^\top,
$$

所以

$$
\boxed{
A_{t+1}
=
\Phi D_t^\top(D_tD_t^\top)^{-1}.
}
$$

### 固定 $A_{t+1}$，求 $D$

$$
D_{t+1}
=
\arg\min_D\|\Phi-A_{t+1}D\|_F^2.
$$

正规方程为

$$
A_{t+1}^\top A_{t+1}D_{t+1}
=
A_{t+1}^\top\Phi,
$$

所以

$$
\boxed{
D_{t+1}
=
(A_{t+1}^\top A_{t+1})^{-1}
A_{t+1}^\top\Phi.
}
$$

如果矩阵不满秩，可以将逆替换成 Moore-Penrose 伪逆。

---

## 四、第三部分要求证明算法为什么收敛到 PCA

这是本题真正有难度的部分。

要证明上述交替最小化并非只收敛到某个局部最优点，而是对于几乎所有初始化 $D_0$，其乘积收敛到

$$
\Phi_k=U_k\Sigma_kV_k^\top.
$$

核心是证明，完成一轮 $A,D$ 更新以后，$D$ 的行空间满足

$$
\boxed{
\operatorname{row}(D_{t+1})
=
\operatorname{row}(D_t\Phi^\top\Phi).
}
$$

因此递推得到

$$
\operatorname{row}(D_t)
=
\operatorname{row}\bigl(D_0(\Phi^\top\Phi)^t\bigr).
$$

这就是对矩阵

$$
\Phi^\top\Phi
$$

执行子空间幂迭代。

而 $\Phi^\top\Phi$ 的特征向量正是 $\Phi$ 的右奇异向量：

$$
\Phi^\top\Phi
=
V\Sigma^2V^\top.
$$

因此，只要初始化 $D_0$ 在前 $k$ 个右奇异方向上不是恰好完全缺失，迭代就会把其行空间推向

$$
\operatorname{span}\{v_1,\ldots,v_k\}.
$$

最后

$$
AD\longrightarrow
\Phi V_kV_k^\top
=
U_k\Sigma_kV_k^\top.
$$

---

## 五、“almost all initializations”是什么意思

它不是说任何初始化都可以。

例如 $k=1$，假设初始化向量刚好与第一主成分 $v_1$ 正交，那么乘以 $\Phi^\top\Phi$ 后，它仍然可能没有 $v_1$ 分量，于是不会收敛到第一主成分。

但这种“恰好正交”的初始化构成一个测度为零的集合。

所以随机初始化时，概率为 $1$ 地满足收敛条件。这就是

$$
\text{for almost all initializations of }D.
$$

---

## 六、本题可以压缩为三个任务

### 任务 1：识别优化问题

证明

$$
\min_{A,D}\|\Phi-AD\|_F^2
=
\min_{\operatorname{rank}(B)\le k}\|\Phi-B\|_F^2.
$$

所以这是最佳秩 $k$ 逼近问题。

### 任务 2：求全局最优解

利用 SVD/Eckart-Young 定理证明

$$
\boxed{
A_*D_*=U_k\Sigma_kV_k^\top
=
\Phi V_kV_k^\top,
}
$$

即 PCA 重构。

### 任务 3：分析算法

计算交替更新

$$
A_{t+1}
=
\Phi D_t^\top(D_tD_t^\top)^{-1},
$$

$$
D_{t+1}
=
(A_{t+1}^\top A_{t+1})^{-1}A_{t+1}^\top\Phi,
$$

并证明它在子空间层面等价于幂迭代，从而收敛到 PCA 主子空间。

因此，本题的重点不是“如何直接计算 PCA”，而是展示一个重要现象：

$$
\boxed{
\text{PCA}
=
\text{最佳低秩矩阵分解}
=
\text{交替最小二乘的全局极限}.
}
$$

## Prompt:
2026/7/14 19:42:38

先翻译题目？

## Response:
2026/7/14 19:42:45

题目翻译如下：

> 给定数据矩阵
> $$
> \Phi\in\mathbb R^{n\times d},
> $$
> 考虑关于
> $$
> D\in\mathbb R^{k\times d},\qquad A\in\mathbb R^{n\times k}
> $$
> 最小化
> $$
> \|\Phi-AD\|_F^2.
> $$
>
> 证明：最优解满足 $AD$ 等于对数据矩阵 $\Phi$ 进行 PCA 后得到的重构数据矩阵。
>
> 利用 $\Phi$ 的奇异值分解，证明如下交替最小化算法：每一步先固定 $D$，关于 $A$ 最小化
> $$
> \|\Phi-AD\|_F^2,
> $$
> 再固定 $A$，关于 $D$ 最小化该目标函数；对于几乎所有 $D$ 的初始值，该算法都收敛到全局最优解。
>
> 最后，计算上述两个交替最小化步骤对应的更新公式。 `lftp.pdf`

其中：

- $\|\cdot\|_F$ 是 Frobenius 范数；
- “几乎所有初始值”指除了一个测度为零的特殊初始化集合之外；
- $A$ 可以理解为 $n$ 个样本的 $k$ 维编码；
- $D$ 可以理解为从 $k$ 维空间重构到 $d$ 维空间的矩阵；
- 因此 $AD$ 是对原数据矩阵 $\Phi$ 的秩至多为 $k$ 的近似。

## Prompt:
2026/7/14 19:59:21

如何证明B = \Phi VV^T就是rank(B)\le k条件下的极小呢？虽然我们可以证明rank B\le k的情况下一定可以分解成AD，因此双条件的优化一定可以转化为\Phi与B在F范数平方下的极小，但是我对于为什么\Phi VV^T就是那个最小的B，虽然我知道它确实很小，是从SVD出发的，但我只是知道在已有\PhiDE的情况下，D,E一定是V的前k个行向量。

## Response:
2026/7/14 19:59:24

你缺的正是中间这一步：

> 对任意秩不超过 $k$ 的矩阵 $B$，先固定它的行空间。  
> 在相同行空间内，最接近 $\Phi$ 的矩阵一定不是任意的 $B$，而是 $\Phi$ 在该行空间上的正交投影。

然后再问：哪个 $k$ 维行空间最好？答案才是前 $k$ 个右奇异向量张成的空间。这就是 Eckart-Young 定理在这里的一种直接证明。`lftp.pdf`

为避免与题目中的 $V$ 淆乱，设

$$
\Phi=U\Sigma W^\top
$$

是 SVD，右奇异向量记为

$$
W=[w_1,\ldots,w_d],
\qquad
\sigma_1\ge\cdots\ge\sigma_d\ge0.
$$

我们要证明

$$
\min_{\operatorname{rank}(B)\le k}\|\Phi-B\|_F^2
$$

的一个最优解是

$$
B_*=\Phi W_kW_k^\top,
\qquad
W_k=[w_1,\ldots,w_k].
$$

---

# 1. 任取一个 $\operatorname{rank}(B)\le k$ 的矩阵

令

$$
\mathcal S=\operatorname{row}(B)\subseteq\mathbb R^d
$$

是 $B$ 的行空间，因此

$$
\dim\mathcal S=\operatorname{rank}(B)\le k.
$$

设 $P_{\mathcal S}$ 是到 $\mathcal S$ 的正交投影矩阵。

因为 $B$ 的每一行都属于 $\mathcal S$，所以将 $B$ 的每一行投影到 $\mathcal S$ 后不变：

$$
B=B P_{\mathcal S}.
$$

把误差分解为

$$
\Phi-B
=
\Phi(I-P_{\mathcal S})
+
\bigl(\Phi P_{\mathcal S}-B\bigr).
$$

这里：

- $\Phi(I-P_{\mathcal S})$ 的每一行属于 $\mathcal S^\perp$；
- $\Phi P_{\mathcal S}-B$ 的每一行属于 $\mathcal S$。

因此两个矩阵在 Frobenius 内积下正交：

$$
\left\langle
\Phi(I-P_{\mathcal S}),
\Phi P_{\mathcal S}-B
\right\rangle_F=0.
$$

于是由勾股定理，

$$
\boxed{
\|\Phi-B\|_F^2
=
\|\Phi(I-P_{\mathcal S})\|_F^2
+
\|\Phi P_{\mathcal S}-B\|_F^2.
}
$$

所以必然有

$$
\boxed{
\|\Phi-B\|_F^2
\ge
\|\Phi-\Phi P_{\mathcal S}\|_F^2.
}
$$

等号当且仅当

$$
B=\Phi P_{\mathcal S}.
$$

这说明：一旦 $B$ 的行空间 $\mathcal S$ 已经确定，在所有行空间包含于 $\mathcal S$ 的矩阵中，最佳选择是

$$
B_{\mathcal S}=\Phi P_{\mathcal S}.
$$

因此我们不再需要对所有 $B$ 优化，而只需要在所有不超过 $k$ 维的子空间 $\mathcal S$ 中寻找最佳投影：

$$
\min_{\operatorname{rank}(B)\le k}\|\Phi-B\|_F^2
=
\min_{\dim\mathcal S\le k}
\|\Phi-\Phi P_{\mathcal S}\|_F^2.
$$

这就是关键桥梁。

---

# 2. 把子空间写成 $V$ 的列空间

若 $\dim\mathcal S=k$，取 $\mathcal S$ 的一组标准正交基：

$$
V=[v_1,\ldots,v_k]\in\mathbb R^{d\times k},
\qquad
V^\top V=I_k.
$$

那么正交投影矩阵为

$$
P_{\mathcal S}=VV^\top.
$$

所以现在的问题变成

$$
\min_{V^\top V=I_k}
\|\Phi-\Phi VV^\top\|_F^2.
$$

并且一旦最佳 $V$ 找到，最佳低秩矩阵就是

$$
B_*=\Phi VV^\top.
$$

注意：这里尚未说明 $V$ 是前 $k$ 个右奇异向量，只是把任意 $k$ 维子空间参数化了。

---

# 3. 最小重构误差等价于最大保留能量

由于 $P=VV^\top$ 满足

$$
P^\top=P,\qquad P^2=P,
$$

有

$$
\begin{aligned}
\|\Phi-\Phi VV^\top\|_F^2
&=
\|\Phi(I-P)\|_F^2\\
&=
\operatorname{tr}\bigl((I-P)\Phi^\top\Phi(I-P)\bigr)\\
&=
\operatorname{tr}(\Phi^\top\Phi)
-
\operatorname{tr}(V^\top\Phi^\top\Phi V).
\end{aligned}
$$

因此

$$
\min_{V^\top V=I_k}
\|\Phi-\Phi VV^\top\|_F^2
$$

等价于

$$
\boxed{
\max_{V^\top V=I_k}
\operatorname{tr}(V^\top\Phi^\top\Phi V).
}
$$

第一项

$$
\operatorname{tr}(\Phi^\top\Phi)=\|\Phi\|_F^2
$$

是固定的。

---

# 4. 为什么最优子空间是前 $k$ 个右奇异向量

由 SVD，

$$
\Phi^\top\Phi
=
W\Sigma^\top\Sigma W^\top
=
W\operatorname{Diag}(\sigma_1^2,\ldots,\sigma_d^2)W^\top.
$$

令

$$
Z=W^\top V.
$$

因为 $W$ 是正交矩阵，

$$
Z^\top Z
=
V^\top WW^\top V
=
I_k.
$$

于是

$$
\begin{aligned}
\operatorname{tr}(V^\top\Phi^\top\Phi V)
&=
\operatorname{tr}
\left(
Z^\top\operatorname{Diag}(\sigma_1^2,\ldots,\sigma_d^2)Z
\right).
\end{aligned}
$$

记 $Z$ 的第 $i$ 行为 $z_i^\top$，则

$$
\operatorname{tr}(V^\top\Phi^\top\Phi V)
=
\sum_{i=1}^d\sigma_i^2\|z_i\|_2^2.
$$

令

$$
\alpha_i=\|z_i\|_2^2.
$$

因为 $Z^\top Z=I_k$，所以

$$
0\le\alpha_i\le1,
\qquad
\sum_{i=1}^d\alpha_i
=
\operatorname{tr}(ZZ^\top)
=
\operatorname{tr}(Z^\top Z)
=
k.
$$

现在问题变成

$$
\max
\sum_{i=1}^d\sigma_i^2\alpha_i,
$$

满足

$$
0\le\alpha_i\le1,
\qquad
\sum_i\alpha_i=k.
$$

由于

$$
\sigma_1^2\ge\sigma_2^2\ge\cdots\ge\sigma_d^2,
$$

显然最大值在

$$
\alpha_1=\cdots=\alpha_k=1,
\qquad
\alpha_{k+1}=\cdots=\alpha_d=0
$$

处取得。

因此

$$
\max_{V^\top V=I_k}
\operatorname{tr}(V^\top\Phi^\top\Phi V)
=
\sum_{i=1}^k\sigma_i^2.
$$

一个最优选择是

$$
\boxed{
V=W_k=[w_1,\ldots,w_k].
}
$$

---

# 5. 因此最佳 $B$ 是什么

代回

$$
B_*=\Phi VV^\top,
$$

得到

$$
\boxed{
B_*=\Phi W_kW_k^\top.
}
$$

由 SVD，

$$
\begin{aligned}
\Phi W_kW_k^\top
&=
U\Sigma W^\top W_kW_k^\top\\
&=
U_k\Sigma_kW_k^\top.
\end{aligned}
$$

所以

$$
\boxed{
B_*
=
U_k\Sigma_kW_k^\top
=
\sum_{i=1}^k\sigma_i u_iw_i^\top.
}
$$

这就是截断 SVD，也就是 PCA 重构矩阵。

最小误差为

$$
\boxed{
\|\Phi-B_*\|_F^2
=
\sum_{i=k+1}^d\sigma_i^2.
}
$$

---

# 6. 你的已有认识差在哪一步

你已经知道：

$$
\Phi=U\Sigma W^\top
$$

以后，保留前 $k$ 个奇异方向会得到一个很小的误差。但仍需要排除一种可能：

> 会不会存在某个右奇异向量并不与 $\Phi$ 对齐的、很奇怪的秩 $k$ 矩阵 $B$，误差更小？

上面的证明通过两步排除了它：

1. 对任意 $B$，只保留它的行空间 $\mathcal S$，并用
   $$
   \Phi P_{\mathcal S}
   $$
   代替 $B$，误差只会更小；

2. 在所有 $k$ 维子空间中，前 $k$ 个右奇异向量张成的子空间保留的能量最大。

因此并不是先假定 $B$ 的奇异向量必须等于 $\Phi$ 的奇异向量，而是证明：

$$
\boxed{
\text{任意 }B
\;\longrightarrow\;
\text{其行空间上的正交投影}
\;\longrightarrow\;
\text{前 }k\text{ 个右奇异子空间}.
}
$$

这才完整证明了全局最优性。



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)