# LFTP Ch2监督学习导论

给定一系列观测数据$(x_i,y_i)$,需要推广到未观测数据的位置上去

the main goal of supervised learning is to predict a new y ∈ Y given a new previously unseen
x ∈ X. The unobserved data are usually referred to as the “testing data.”

其中自变量所在的空间$\mathcal X$往往具有可以利用的特定结构,我们不是将$X$映射到一个d维的向量空间，就是隐式使用样本之间的相似度/不相似度。

either by building an explicit mapping from X to a vector space (such as Rd) or implicitly by using a notion of pairwise dissimilarity or similarity between pairs of inputs.

最经典的因变量是分类问题的离散取值，回归问题的实数取值。当然，实际上输出可以是任意具有结构的特征，包括一张的图片（矩阵），一个图，一个文本序列（GPT），这就需要合理安排损失函数。

The most classical examples are binary labels Y = {0, 1} or
Y = {−1, 1}, multicategory classification problems with Y = {1, . . . , k}, and classical
regression with real responses/outputs Y = R.

然而，监督学习往往具有以下的几个困难点

1.噪声：由于因变量和自变量之间并不是支配性的地位。对于离散变量问题，y可能只受X的概率影响，对应的是一个与x有关的分布；对于连续变量的回归问题，$y=f(x)+\varepsilon$,其中$\varepsilon$是一个均值为0的随机变量。而且事实上确实存在未被观测到的隐变量，

2预测对应的函数可能非常复杂

3观测到的变量只有有限个

4输入变量空间可能很大

5训练分布和测试分布可能差别很大

6对于什么是“好”的表现没有明确的规则

## Decision Theory

fixed (testing) distribution p(x,y) on X × Y, with marginal distribution
p(x) on X. Note that we make no assumptions at this point on the input space X.

此处还可以讲的更形式一点，只不过就不管了。

We ignore measurability issues on purpose.

### 损失函数的选取

损失函数实际上就是要找一个ℓ

二分类问题$ℓ(y, z) = 1_{y\neq z} (0–1 loss)$

多分类问题$ℓ(y, z) = 1_{y\neq z} (0–1 loss)$

回归问题:$ℓ(y, z) = (y-z)^2$

对于一个预测的函数， f : X → Y,一个损失函数ℓ : Y × Y → R, 和一个概率分布p on X × Y, f的期望风险被定义为

$$R(f) = \mathbb{E}ℓ(y, f(x))=\int_{X×Y}ℓ(y, f(x))dp(x, y)$$

Be careful with the randomness, or lack thereof, of f: when performing learning
from data, f will depend on the random training data, not on the testing
data, and thus R(f) is typically random because of the dependence on the
training data. 

如果是作为泛函，那么期望风险是一个由f决定的泛函，但是f 是一个依赖于随机变量（训练集）的一个函数。在抽训练集之前，它仍然是随机变量。

此外，由于实际我们只有离散的数据点，所以我们会构造经验风险：

对于一个待预测的函数f : X → Y,一个损失函数: Y × Y → R, and data (xi, yi) ∈ X × Y, i = 1, . . . , n, the empirical risk of f is
defined as
bR(f) =
1
n
Xn
i=1
ℓ(yi, f(xi)).

### Bayes Risk and Bayes Predictor: loss伪全知视角能干到多小

$R(f) = \mathbb Eℓ(y, f(x))= \mathbb E [\mathbb E[ℓ(y, f(x))|x]]$

将其拆解成积分的形式，因此我们可以计算每一个x对应的让风险极小化对应的值$f^*(x)$
```math
f^*(x_0) = argmin_{a\in \mathcal Y}\mathbb E[\ell(a,y)|x=x_0]
```
对应的多分类问题：

$f(x)=argmax_{k\in K} \mathbb P(Y=k|X=x)$

对于回归问题：

$f(x)=\mathbb E (Y|X=x)$

Exercise 2.1 Consider binary classification with Y = {−1, 1} with the loss function
ℓ(−1,−1) = ℓ(1, 1) = 0 and ℓ(−1, 1) = c− > 0 (cost of a false positive), ℓ(1,−1) = c+ > 0
(cost of a false negative). Compute a Bayes predictor at x as a function of E[y|x].

$f(x_0) = l(a,1)P(y=1|x=x_0)+l(a,-1)P(y=-1|x=x_0)$

令$p(x_0) = P(y=1|x=x_0)$

a=1 $c_{+}(1-p)<c_{-}p,1/p<c_-/c_++1)$

a=-1$c_{+}(1-p)>c_{-}p,1/p<c_-/c_++1)$



Exercise 2.2 We consider a learning problem on $X × Y$, with $Y = \mathbb R$ and the absolute
loss defined as $ℓ(y, z) = |y − z|$. Compute a Bayes predictor $f^∗ : X \rightarrow \mathbb R$.
```math
f∗(x′)∈argmin_{z∈R}E[∣y−z∣∣x=x′] = \int |y-z| dP(y|x) = \int 1_{y\le z}(z-y) dP(y|x) +\int 1_{y\ge z}(y-z) dP(y|x) 
```
我们要最小化
```math
\phi(z)=\mathbb E[|Y-z|\mid X=x].
```
先假设条件分布连续，没有原子点。对 $z$ 求导：
```math
\frac{d}{dz}|Y-z|
=
\begin{cases}
1, & Y<z,\\
-1, & Y>z.
\end{cases}
```
所以
```math
\phi'(z)
=
\mathbb P(Y<z\mid X=x)-\mathbb P(Y>z\mid X=x).
```
因为连续分布下
```math
\mathbb P(Y<z\mid X=x)=F_x(z),
```
令$F_x(m)=1/2$，此时$\phi'(m) = 0,z = m$

因此
```math
f^*(x)=\operatorname{median}(Y\mid X=x),P(Y\ge f^*(x)|X=x)=\frac{1}{2}
```
Exercise 2.3 We consider a learning problem on X × Y, with Y = R and the “pinball”
loss $ℓ(y, z) = α(y − z)^+ + (1 − α)(z − y)^+$, for $α ∈ (0, 1)$. Compute a Bayes predictor
f∗ : X → R. Provide an interpretation in terms of quantiles.
```math
\phi(z) = \mathbb E(\ell (Y,a)|X=x)=\int_z^{\infty}\alpha(y-z)dP_x(y)+\int_{-\infty}^z(1-\alpha)(z-y)dP_x(y)
```
对于第一项：
```math
\frac{d}{dz}(Y-z)^+
=
-\mathbf 1_{\{Y>z\}}.
```
对于第二项：
```math
\frac{d}{dz}(z-Y)^+
=
\mathbf 1_{\{Y<z\}}.
```
所以
```math
\phi'(z)
=
-\alpha \mathbb P(Y>z\mid X=x)
+
(1-\alpha)\mathbb P(Y<z\mid X=x).
```
连续分布下，
```math
\mathbb P(Y<z\mid X=x)=F_x(z),
```
因此
```math
\phi'(z)
=
-\alpha(1-F_x(z))
+
(1-\alpha)F_x(z).
```
展开：
```math
\phi'(z)
=
-\alpha+\alpha F_x(z)+F_x(z)-\alpha F_x(z)
=
F_x(z)-\alpha.
```
令导数为 $0$，得到
```math
F_x(z)=\alpha.
```
所以 Bayes predictor 是条件 $\alpha$-分位数：
```math
f^*(x)\in \{z:F_x(z)=\alpha\}.
```
更标准地写：
```math
f^*(x)=Q_\alpha(Y\mid X=x),
```
其中
```math
Q_\alpha(Y\mid X=x)
=
\inf\{z\in\mathbb R:F_x(z)\ge \alpha\}.
```
Exercise 2.4 Characterize Bayes predictors for regression with the “ε-insensitive”
loss defined as $ℓ(y, z) = max\{0, |y − z|-\varepsilon \}$. If for each x, y is supported in an interval
of length less than 2ε, what are the Bayes predictors?
```math
\phi(z) = E(\ell(y,z)|X=x) = \int_{R} 1_{|y-z|>\varepsilon}(|y-z|-\varepsilon)dP_x(y) = \int_{R} 1_{y-\varepsilon>z}(y-z-\varepsilon)dP_x(y)+ \int_{R} 1_{y+\varepsilon<z}(z-y-\varepsilon)dP_x(y)
```
$P(z>y-\varepsilon|X=x)+P(z>y+\varepsilon|X=x)=1,f^*(x)=z$

Exercise 2.5 (Inverting predictions) Consider the binary classification problem with
Y = {−1, 1} and the 0–1 loss. Relate the risk of a prediction f to that of its opposite −f.
Exercise 2.6 (“Chance” predictions) Consider binary classification problems with
the 0–1 loss. What is the risk of a random prediction rule where we predict the two
classes with equal probabilities independent of input x? Address the same question with
multiple categories.
Exercise 2.7 () Consider a random prediction rule where we predict from the proba-
bility distribution of y given x. When is this achieving the Bayes risk?



k-邻域算法

Exercise 2.8 How would the curve move when n increases (assuming the same
balance between classes)?

随着训练样本的增加，test先减后增

随机抽一份训练集 $D_n(p)$，用算法 $A$ 训练出模型 $A(D_n(p))$。那么这个模型的真实风险 $R_p(A(D_n(p)))$ 距离最优 Bayes risk $R_p^*$ 不超过 $\varepsilon$ 的概率至少是 $1-\delta$。

学习理论想证明类似：
```math
R_p(A(D_n(p)))-R_p^*
\le
C\sqrt{\frac{\log(1/\delta)}{n}}
```
with probability at least $1-\delta$。

这时就可以说：
```math
\varepsilon(n,\delta)
=
C\sqrt{\frac{\log(1/\delta)}{n}}.
```
样本数 $n$ 越大，误差界越小；置信度要求越高，即 $\delta$ 越小，误差界通常会稍微变大。

## No Free Lunch

二分类，$Y=\{0,1\}$，0–1 loss：
```math
\ell(y,\hat y)=\mathbf 1_{\{y\ne \hat y\}}.
```
对某个分布 $p$，分类器 $f$ 的风险是
```math
R_p(f)=\mathbb P_p(f(X)\ne Y).
```
也就是测试时分类错误的概率。

$R_p^*$ 是 Bayes risk，即如果你完全知道真实分布 $p$，理论上能达到的最小错误率：
```math
R_p^*=\inf_f R_p(f).
```
学习算法 $A$ 接收训练集
```math
D_n(p)=\{(X_1,Y_1),\dots,(X_n,Y_n)\}
```
并输出一个分类器
```math
A(D_n(p)).
```
所以
```math
\mathbb E\left[R_p(A(D_n(p)))\right]-R_p^*
```
命题说：
```math
\sup_{p\in\mathcal P}
\left\{
\mathbb E\left[R_p(A(D_n(p)))\right]-R_p^*
\right\}> \frac12.
```
意思是：**不管你选什么算法 $A$，只要样本数 $n$ 固定，总能找到一个坏分布 $p$，使得你的期望 excess risk 超过 $1/2$。**

证明的构造大概是这样。

因为 $X$ 无限，所以可以从 $X$ 中挑出 $k$ 个不同点：
```math
1,2,\dots,k.
```
令 $X$ 在这 $k$ 个点上均匀分布：
```math
\mathbb P(X=j)=\frac1k.
```
然后给每个点指定一个标签：
```math
r=(r_1,\dots,r_k)\in\{0,1\}^k,
```
并令
```math
Y=r_X.
```
也就是说，标签是确定性的。因此 Bayes 分类器只要记住这张表就可以零错误：
```math
R_p^*=0.
```
要证明：
```math
\sup_{p\in\mathcal P}
\left\{
\mathbb E\big[R_p(A(D_n(p)))\big]-R_p^*
\right\}
> \frac12.
```
也就是：对任意学习算法 $A$，总能找到一个坏分布 $p$，使得算法的期望 excess risk 至少接近 $1/2$。

因为后面构造的分布满足
```math
R_p^*=0,
```
所以只需要证明
```math
\mathbb E[R_p(A(D_n(p)))]
```
接近 $1/2$。

原文：
```math
\hat f_{D_n}=A(D_n(p)).
```
这里
```math
D_n(p)=\{(x_1,y_1),\dots,(x_n,y_n)\}
```
是训练集。由于当前构造里
```math
y_i=r_{x_i},
```
所以训练集其实是
```math
D_n(p)=\{(x_1,r_{x_1}),\dots,(x_n,r_{x_n})\}.
```
算法 $A$ 看到这个训练集以后，输出分类器：
```math
\hat f_{D_n}.
```
注意：$\hat f_{D_n}$ 是随机的，因为训练集 $D_n$ 是随机的。

原文：
```math
S(r)=\mathbb E\left[R_p(\hat f_{D_n})\right].
```
这里 $p$ 其实依赖于 $r$，更准确写作 $p_r$：
```math
S(r)=\mathbb E_{D_n\sim p_r^n}
\left[
R_{p_r}(\hat f_{D_n})
\right].
```
它表示：当真实标签表是 $r$ 时，算法 $A$ 的期望测试错误率。

因为这个构造下
```math
R_{p_r}^*=0,
```
所以
```math
S(r)
=
\mathbb E[R_{p_r}(\hat f_{D_n})]-R_{p_r}^*.
```
也就是说 $S(r)$ 就是这个问题上的期望 excess risk。

we want to maximize S(r) with respect to r∈{0,1}k.

因为证明目标是找一个坏分布 $p$。而每一个 $r$ 都对应一个分布 $p_r$。所以只要能找到某个 $r$，使得
```math
S(r)
```
很大，就找到坏分布了。

也就是：
```math
\sup_{p\in\mathcal P}
\mathbb E[R_p(A(D_n(p)))]-R_p^*
\ge
\max_{r\in\{0,1\}^k} S(r).
```
原文：
```math
\max_{r\in\{0,1\}^k}S(r)
>
\mathbb E_{r\sim q}[S(r)].
```
严格说，这里应理解为
```math
\max_{r\in\{0,1\}^k}S(r)
\ge
\mathbb E_{r\sim q}[S(r)].
```
含义很简单：一堆数的最大值至少不小于它们的平均值。

这里 $q$ 是 $r$ 上的均匀分布，也就是让
```math
r_1,\dots,r_k
```
彼此独立，并且
```math
\mathbb P(r_j=0)=\mathbb P(r_j=1)=\frac12.
```
这一步是典型的 probabilistic method：

> 如果随机选 $r$ 时平均表现已经很坏，那么至少存在一个具体的 $r$ 也很坏。

原文：
```math
\mathbb E_{r\sim q}[S(r)]
=
\mathbb P(\hat f_{D_n}(x)\ne y)
=
\mathbb P(\hat f_{D_n}(x)\ne r_x).
```
先看
```math
R_p(\hat f_{D_n})
=
\mathbb P(\hat f_{D_n}(x)\ne y).
```
这是 0–1 loss 下风险的定义。

对训练集 $D_n$ 再取期望，就是：
```math
\mathbb E[R_p(\hat f_{D_n})]
=
\mathbb P(\hat f_{D_n}(x)\ne y),
```
其中概率同时包含训练集随机性和测试点随机性。

又因为在构造中
```math
y=r_x
```
几乎必然成立，所以
```math
\mathbb P(\hat f_{D_n}(x)\ne y)
=
\mathbb P(\hat f_{D_n}(x)\ne r_x).
```
原文：
```math
x_1,\dots,x_n,x,r
```
都在取随机性。

具体是：
```math
x_1,\dots,x_n\sim \mathrm{Unif}\{1,\dots,k\}
```
是训练输入；
```math
x\sim \mathrm{Unif}\{1,\dots,k\}
```
是测试输入；
```math
r_1,\dots,r_k\sim \mathrm{Bernoulli}(1/2)
```
是随机标签表。

并且这些对象彼此独立，除了标签由
```math
y_i=r_{x_i},\qquad y=r_x
```
决定。

Dn(p)={(x1,rx1),…,(xn,rxn)}.

意思是算法实际看见的是这些信息：
```math
x_1,\dots,x_n
```
以及对应标签
```math
r_{x_1},\dots,r_{x_n}.
```
它没有看见其他点的标签，比如如果测试点 $x$ 没出现在训练集中，那么 $r_x$ 对算法来说就是未知的。



问题是，算法只有 $n$ 个训练样本。当 $k\gg n$ 时，训练集只覆盖了这 $k$ 个点中的很小一部分。测试点 $X$ 没出现在训练集中的概率是
```math
\mathbb P(X\notin \{X_1,\dots,X_n\})
=
\left(1-\frac1k\right)^n.
```
当 $k\to\infty$ 且 $n$ 固定时，
```math
\left(1-\frac1k\right)^n\to 1.
```
也就是说，测试点几乎一定是训练集中没见过的点。

对于没见过的点，如果标签向量 $r$ 是任意的，算法没有任何信息判断 $r_X$ 是 0 还是 1。于是错误概率至少接近
```math
\frac12\left(1-\frac1k\right)^n.
```
令 $k$ 足够大，就能让这个量任意接近 $1/2$。因此对任意算法，都存在坏分布让它的 excess risk 接近随机猜测水平。书中的证明正是用这种“在 $k$ 个点上构造任意标签表”的方法。
