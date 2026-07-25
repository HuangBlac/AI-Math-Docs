# 你真的了解线性算法了吗？

## Intro：总介绍

为什么称这是一个线性算法

原本的目标是极小化一个期望风险，$\mathcal R (f) = \mathbb E[\ell(f(x),y)]$

其中x,y符合联合分布$p = p(x,y)$,损失函数一般选用恒正，凸且光滑可微的$\ell (a,y)=(a-y)^2$

理论上将风险极小化的目标函数$f^*(x) = \mathbb E(y|x)$，这样的f确实是让期望风险极小化的方法。

但是有两个问题，就是我们并不知道联合分布是什么，所以我们并不能找不到的；其次这个f到底在哪，我们应该如何去表示这个东西也是不知道的。

所以这里我们要做两个处理：

首先，我们需要假设函数是由若干个隐特征线性组合而成的，也就是假设所有的函数都属于这样一个函数类，这就是所谓算法“线性性质”的由来，是因为这个函数类关于参数$\theta$是线性的，但是关于特征X并不是线性的。

$\mathcal F = \{\varphi(x)^T\theta|\theta\in R^d,\varphi:\mathcal X\rightarrow R^d\}$

虽然我们并不知道什么是比较好的$\varphi$，或许是平方，三次方，或者指数；也不知道这个d要取多少，但总归经过了这样一个参数化的过程，我们可以明确的挑一个$\theta$出来

然而，我们原本是想好好的求一个好的参数$\mathcal R(f_{\theta^*})= argmin_{f\in\mathcal F_{\theta}}\mathcal R(f)$但是我们不知道联合分布是什么，就是期望求不出来。

我们需要换成经验风险，所谓经验风险，就是根据已有的n组数据$\{(x_i,y_i)\}$来的统计量来代替对期望的估计：

$\hat{\mathcal{R}}(f) =\frac{1}{n} \sum_{i=1}^n\ell(f(x_i),y_i)$

极小化这个目标函数$\hat f = argmin_{f\in \mathcal F_{\theta}}\hat {\mathcal{R}}(f)$

这样其实就转化为了一个最小二乘问题$min_{\theta\in R^d}||A\theta-y||_2^2$

其中$A = (\phi(x_1),\phi(x_2),\cdots,\phi(x_n))^T,\theta\in R^d,y = (y_1,y_2,\cdots,y_n)^T$

这就是所谓线性回归算法问题的由来，基本就是来自于二次损失函数的第一性原理，以及出于一些实际算法求解的考虑的一些降级处理。搞清楚了哪些是最初的假设，哪些是“我们实际不知道”而向现实做出的妥协。

但是，以下问题是我们仍然需要知道的：

1. 最小二乘问题数学上能不能求解，计算上怎么求解：

首先，非常幸运的是，这个最小二乘问题$argmin_{\theta\in R^d}||\Phi \theta-y||_2^2$在$\Phi$是列满秩的时候才行，观测的样本量一定要比特征数目要更少

实际上有解析解，可以写成：
$$
\hat \theta = (\Phi^T\Phi)^{-1}\Phi y
$$
至于如何验证这一点，则是可以将其看成一个优化的问题，将原本的问题转化为一个二次型极小化：

$\varphi(\theta) = ||\Phi \theta-y||_2^2$

对于$\varphi(x)$进行求导，$\varphi'(\theta) = \Phi^T(\Phi\theta - y),\varphi''(\theta) = \Phi^T\Phi$

最优性条件要求一阶导数为零，而且列满秩的条件将会对应$\Phi^T\Phi$可逆，因此$\Phi^T\Phi\theta = \Phi y$,$\hat\theta = (\Phi^T\Phi)^{-1}\Phi y$

而由于此时Hesse阵是正定矩阵，满足二阶最优性条件，准确来说此时这是一个凸函数，极小点就是最小值

注：严格来讲，$\theta$是一个向量所以不能这么写，应该写成一个梯度$\nabla$和Hesse阵$\nabla^2$。但由于一阶，二阶的情况可以简单拓展，就直接使用一次二次导数

当然，这实际上还有一个更鲜明的解释：所谓的求的预测向量就是真实分布空间

Proposition 3.2 预测向量 $\hat y =Φ\hat θ = Φ(Φ^⊤Φ)^{−1}\Phi^⊤y$ 这样得到，这实际上可以写成$y\in R^n$  到像空间$Im(\Phi)⊂ R^n$ 的一个正交投影，即不改变长度。

听上去很符合直觉，毕竟预测就是根据已知去找到了一个预测空间，找到了一双发现真相的眼睛；预测的结果实际上就是用这个方法去“看”真相，那就是有一个畸变，相当于就是把真相投影到了现实之中。而一个好的投影就应该还原，一根一米长的棍子不会就变成1cm,一个正方形不会变成一个长方形甚至是三角形。

论证部分：

其实就是要证明矩阵$\Pi = Φ(Φ^⊤Φ)^{−1}Φ^⊤ \in R^{n×n}$是一个在像空间$Im(\Phi)$正交矩阵.

对于任意的$x \in Im(\Phi)=\{\Phi a|a\in R^d\}$只需证明$\Pi x = x$即可，要证明这是一个正交投影矩阵就是满足：

 $Φ\hat{θ} = argmin_{z∈im\Phi} ||y − z||_2^2$

首先我们可以证明如下两点

$(1)\forall u \in Im(\Phi),\Pi u = u$(投影矩阵)

$(2)u′ \in Im(Φ)^⊥, Φ^⊤u′ = 0$

对于(1)考虑$u = \Phi a$，$\Pi \Phi a=\Phi(Φ^⊤Φ)^{−1}Φ^⊤\Phi a=\Phi a=u$由此

而(2)的证明过程就是

考虑$\Pi u′ = Φ(Φ^⊤Φ)^{−1}(Φ^⊤u′) = 0$

再此基础上,考虑辅助的变量$\forall z\in Im\Phi,\|y-\Pi y\|^2_2 = (y-\Pi y,y -z +z - \Pi y) =  (y-\Pi y,y-z)+(y-\Pi y,z-\Pi y) = (y-\Pi y,y-z)\le \|y-\Pi y\| \cdot\|y-z\|$

因此$\forall z \in Im(\Phi),\|y-\Pi y\| \le \|y-z\|$,也就是 $Φ\hat{θ} = argmin_{z∈im\Phi} ||y − z||_2^2$

这实际上就是意味着选取像空间之中距离y最接近的一个向量。

所以最小二乘问题居然作为算法界最高的山，应该如何去将其求解。

这基本上对应两种求解思路：

利用矩阵性质去求解：QR方法

首先将$\Phi$ 分解为$\Phi=QR$其中$Q \in R^{n×d}$的列向量正交，满足$Q^⊤Q = I$而且$R ∈ R^{d×d}$ 是上三角矩阵，下三角为零，这相比于矩阵求逆速度要更快，虽然实际上都是$O(n^3)$的数量级，但系数变小了。

而且这样的话，$Φ⊤Φ = R^⊤Q^⊤QR = R^⊤R$ , 就自发的形成了一个以R为因子的Cholesky分解，关于已有的半正定矩阵$Φ^⊤Φ \in R^d$. One then has, since R is
invertible,
(Φ⊤Φ)ˆθ = Φ⊤y ⇔ R⊤Q⊤QRˆθ = R⊤Q⊤y ⇔ R⊤Rˆθ = R⊤Q⊤y ⇔ Rˆθ = Q⊤y.
It only remains to solve a triangular linear system, which is easy. The overall running
time complexity remains O(d3). The conjugate gradient algorithm can also be used (see
Golub and Loan, 1996, for details).

直接将其看作一个函数极小化问题然后去求解：梯度下降算法

We can bypass the need for matrix inversion or factorization using
gradient descent (GD). It consists in approximately minimizing bR by taking an initial
point θ0 ∈ Rd and iteratively going toward the minimizer by following the opposite of the
gradient:
θt = θt−1 − γbR′(θt−1) for t > 1,
where γ > 0 is the step size. When these iterates converge, they do toward the OLS
estimator since a fixed-point θ satisfies bR′(θ) = 0. We will study such algorithms in
chapter 5, with running-time complexities going down to linear in d, e.g., O(nd).



Fixed design：输入点固定，只有输出有噪声

固定设计中，把
$$
x_1,\ldots,x_n
$$
看成提前给定的确定性点。

例如，在一维区间上人为选定均匀网格：
$$
x_i=\frac{i}{n}.
$$
然后输出按照某个随机机制生成，例如
$$
y_i=f^*(x_i)+\varepsilon_i,
$$
其中噪声 $\varepsilon_i$ 是随机的。

因此：

- $x_i$ 不随机；
- $y_i$ 随机；
- 估计量 $\hat\theta$ 因为依赖于 $y_i$，所以仍然是随机的。

我们只评价模型在原来的这些输入点上的预测效果。例如定义
$$
R_{\mathrm{fix}}(\theta)
=
\frac1n\sum_{i=1}^n
\mathbb E\left[
\bigl(y_i^{\mathrm{new}}-\phi(x_i)^\top\theta\bigr)^2
\right],
$$
其中 $y_i^{\mathrm{new}}$ 表示在同一个输入 $x_i$ 上重新产生的一个独立输出。

关键在于：测试时输入仍然是
$$
x_1,\ldots,x_n,
$$
只是输出噪声重新抽样。

因此固定设计研究的是 **within-sample prediction**，而不是对新输入点的推广。

固定输入点可以对应一个离散概率分布：
$$
\widehat p_X
=
\frac1n\sum_{i=1}^n\delta_{x_i},
$$
其中 $\delta_{x_i}$ 是集中在 $x_i$ 上的点质量。

从这个分布中抽取输入，相当于：
$$
P(x=x_i)=\frac1n.
$$
于是，对任意函数 $g$，
$$
\mathbb E_{x\sim\widehat p_X}[g(x)]
=
\frac1n\sum_{i=1}^n g(x_i).
$$
所以固定设计下的平均预测误差
$$
\frac1n\sum_{i=1}^n
\bigl(f(x_i)-f^*(x_i)\bigr)^2
$$
也可以写成
$$
\mathbb E_{x\sim\widehat p_X}
\left[
\bigl(f(x)-f^*(x)\bigr)^2
\right].
$$
Proposition 3.3 (风险的分解对于固定最小二乘法的设计) Under the linear
model and fixed design assumptions made in this section, for any θ ∈ Rd, we have R∗ = σ2
and

$\mathcal R(θ) − \mathcal R^∗ = \|θ − θ^∗\|_{\hat \Sigma}^2$其中$\hat Σ = \frac 1
nΦ^⊤Φ$数据矩阵的归一化的协方差$\|θ\|^2_{\hat \Sigma}= θ^⊤\hatΣθ$. 如果$\hat \theta$是一个随机变量 

整理后的公式是
$$
\mathbb E\!\left[R(\widehat{\theta})\right]-R^*
=
\underbrace{
\left\|\mathbb E[\widehat{\theta}]-\theta^*\right\|_2^2
}_{\text{Bias：偏差平方}}
+
\underbrace{
\mathbb E\!\left[
\left\|\widehat{\theta}-\mathbb E[\widehat{\theta}]\right\|_2^2
\right]
}_{\text{Variance：方差}}.
$$
它是参数估计误差的 **偏差—方差分解**。

3.6 正则化的线性最小二乘法

对于正则化参数 $\lambda>0$，我们将岭最小二乘估计量 $\hat{\theta}_\lambda$ 定义为以下优化问题的极小化解：
$$
\hat{\theta}_\lambda \in argmin_{\theta\in\mathbb{R}^d}\{ \frac{1}{n}\|y-\Phi\theta\|_2^2
 +
 \lambda\|\theta\|_2^2 \}.
$$
岭回归估计量可以通过闭式公式求出。需要注意的是，此时我们不再要求矩阵 $\Phi^\top\Phi$ 可逆。

Proposition 3.6我们回忆$\hat Σ = \frac{1}{n}Φ^⊤Φ ∈ R^{d×d}.$我们可有$\hatθ_λ =\frac{1}{n}(\hat Σ + λI)^{−1}Φ^⊤y.$
证明过程，我们可以参考命题3.1的证明过程，只需要让$f_{\lambda}(\theta) = \frac{1}{n}\|y-\Phi\theta\|_2^2 +\lambda\|\theta\|_2^2$

满足$f'(\hat\theta_{\lambda}) = -\Phi^T(y-\Phi\theta)+\lambda\theta=(\hat\Sigma+\lambda I)\theta-\frac{1}{n}\Phi^T y$

而且有二阶导数$\frac{1}{n}\Phi^T\Phi +\lambda I$

只要二阶导数矩阵正定，就可以满足凸性，而且此时这个矩阵是可逆的。实际上就是要让$\lambda$足够大就好，不需要数据生成的协方差矩阵非得满足什么非得具有很好的性质，即“分得很开”。

Exercise 3.5 使用矩阵可逆引理，说明论述3.6给出的Ridge Regression岭回归的估计也可以被写成，$\hat θ_λ = (Φ^⊤Φ+nλI)^{−1}Φ^⊤y = Φ^⊤(ΦΦ^⊤ + nλI)^{−1}y.$这样在计算上有什么优势：

求解过程：

已知：

关键是下面这种矩阵恒等式：
$$
\left(\Phi^\top\Phi+aI_d\right)^{-1}\Phi^\top
=
\Phi^\top\left(\Phi\Phi^\top+aI_n\right)^{-1},
$$
其中 $a>0$。本题只需要令
$$
(\Phi^{\top}\Phi+aI_d)\Phi^{\top}(\Phi\Phi^{\top}+aI_n)^{-1}=\Phi^\top(\Phi\Phi^\top+aI_n)(\Phi\Phi^{\top}+aI_n)^{-1}=\Phi^\top
$$
因此：
$$
\Phi^{\top}(\Phi\Phi^{\top}+aI_n)^{-1}=(\Phi^{\top}\Phi+aI_d)^{-1}\Phi^\top
$$
当然，也可以用矩阵求逆公式：

$(A+UCV)^{-1} = A^{-1}-A^{-1}U(C^{-1}+VA^{-1}U)^{-1}VA^{-1}$

首先考虑一种特定的结构$A=I$时，证明，$(I+UCV)^{-1} = I - U(C^{-1}+VU)^{-1}V$

由于$(I+UCV)^{-1}=I-UMV,O = UCV -(I+UCV)UMV=U(C-(I+CVU)M)V,M = (C^{-1}+VU)^{-1}$

然后我们将原本的改为：

$(A+UCV)^{-1} = A^{-1}(I+UCVA^{-1})^{-1}=A^{-1}(I-U(C^{-1}+VA^{-1}U)^{-1}VA^{-1})=A^{-1}-A^{-1}U(C^{-1}+VA^{-1}U)VA^{-1}$

当然在这里是比较简单的情景：

$(aI+\Phi^{T}\Phi)^{-1}\Phi^\top = \frac{1}{a}I- \frac{1}{a}\Phi^\top(aI+\Phi\Phi^\top)^{-1}\Phi=a^{-1}\Phi^\top(I-(aI+\Phi\Phi^\top)^{-1}\Phi\Phi^\top)=a^{-1}\Phi^\top(aI+\Phi\Phi^\top)^{-1}((aI+\Phi\Phi^\top)-\Phi\Phi^\top)=a^{-1}\Phi^\top(aI+\Phi\Phi^\top)^{-1}aI=\Phi^\top(aI+\Phi\Phi^\top)^{-1}$

由于维数从原本的d维（数据的维数）变成了n维（样本的维数）

在矩阵求逆方面，这个三次方的操作就会少很多，计算量显著减少

Proposition 3.7:对于如下的线性模型假设（和固定模型假设）岭回归最小二乘法估计 $\hatθ_λ = \frac1
n(\hat Σ + λI)^{−1}Φ^⊤y$有如下的经验估计
$$
E \mathcal R(\hat θ_λ) − \mathcal R^∗ = λ^2θ_*^{T} (\hat Σ + λI)^{−2}\hatΣθ_∗ +
\frac {σ^2}n tr[\hatΣ^2(\hatΣ + λI)^{−2}].
$$
证明过程：

实际上就是进行一个误差分解，分解为bias偏差，记作B；方差var，记作V，参考Proposition3.3
$$
B = \left\|\mathbb E[\widehat{\theta}]-\theta^*\right\|_{\hat \Sigma}^2 = \|\mathbb E[\frac1
n(\hat Σ + λI)^{−1}Φ^⊤(\Phi \theta^*+\varepsilon)]-\theta^*\|_{\hat \Sigma}^2 = \|\mathbb E[\frac1
n(\hat Σ + λI)^{−1}Φ^⊤\Phi \theta^*]-\theta^*\|_2^2=\|\mathbb E[(\hat Σ + λI)^{−1}\lambda \theta^*]\|_{\hat \Sigma}^2=\|(\hat Σ + λI)^{−1}\lambda \theta^*\|_{\hat \Sigma}^2=λ^2θ_*^{T} (\hat Σ + λI)^{−2}\hatΣθ_∗
$$

$$
V = \mathbb E
\left\|\widehat{\theta}-\mathbb E[\widehat{\theta}]\right\|_{\hat \Sigma}^2=\mathbb E
\left\|\frac1
n(\hat Σ + λI)^{−1}Φ^⊤(\Phi \theta^*+\varepsilon)-\mathbb E[\frac1
n(\hat Σ + λI)^{−1}Φ^⊤(\Phi \theta^*+\varepsilon)]\right\|_{\hat \Sigma}^2=\mathbb E
\|\frac1 n(\hat Σ + λI)^{−1}Φ^⊤\varepsilon \|_{\hat \Sigma}^2=tr[\frac1 n(\hat Σ + λI)^{−2}Φ^⊤\Phi\hat \Sigma \mathbb E \varepsilon^\top\varepsilon]=\frac{\sigma^2}{n}tr[(\hat Σ + λI)^{−2}\hat Σ^2]
$$


$$
B+V = \frac1 n(\hatΣ+λI)^{−1}Φ^⊤Φθ^∗ \le λ^2θ_*^{T} (\hat Σ + λI)^{−2}\hatΣθ_∗ +
\frac {σ^2}n tr[\hatΣ^2(\hatΣ + λI)^{−2}]
$$


Proposition 3.8 (Choice of regularization parameter) 设经验协方差矩阵为$\widehat{\Sigma}=\frac1n\Phi^\top\Phi.$取正则化参数$\lambda^*
=
\frac{
\sigma\sqrt{\operatorname{tr}(\widehat{\Sigma})}
}{
\|\theta^*\|_2\sqrt n
}$则有$\mathbb E\left[R(\widehat{\theta}_{\lambda^*})\right]-R^*
\leq
\frac{
\sigma\sqrt{\operatorname{tr}(\widehat{\Sigma})}\,
\|\theta^*\|_2
}{
\sqrt n
}.$

我们已经利用如下事实得到了前面的结论：矩阵$(\widehat{\Sigma}+\lambda I)^{-2}\lambda\widehat{\Sigma}$的所有特征值都不超过 $\frac12$。

事实上，设 $\mu$ 是 $\widehat{\Sigma}$ 的任意一个特征值，则上述矩阵对应的特征值为$\frac{\lambda\mu}{(\mu+\lambda)^2}.$

而$\frac{\lambda\mu}{(\mu+\lambda)^2}
\leq \frac12$等价于$(\mu+\lambda)^2\geq 2\lambda\mu.$对于 $\widehat{\Sigma}$ 的所有特征值 $\mu\geq 0$，上述不等式都成立。

偏差项满足

$$
\begin{aligned}
B
&=
\lambda^2 {\theta^*}^{\top}
(\widehat{\Sigma}+\lambda I)^{-2}
\widehat{\Sigma}\theta^* \
&=
\lambda {\theta^*}^{\top}
(\widehat{\Sigma}+\lambda I)^{-2}
\lambda\widehat{\Sigma}\theta^* \
&\leq
\frac{\lambda}{2}|\theta^*|_2^2.
\end{aligned}
$$

类似地，对于方差项，有
$$
\begin{aligned}
V
&=
\frac{\sigma^2}{n}
\operatorname{tr}
\left[
\widehat{\Sigma}^2
(\widehat{\Sigma}+\lambda I)^{-2}
\right] \
&=
\frac{\sigma^2}{\lambda n}
\operatorname{tr}
\left[
\widehat{\Sigma}
\lambda\widehat{\Sigma}
(\widehat{\Sigma}+\lambda I)^{-2}
\right] \
&\leq
\frac{\sigma^2\operatorname{tr}(\widehat{\Sigma})}
{2\lambda n}.
\end{aligned}
$$
因此，
$$
\mathbb E\left[R(\widehat{\theta}_{\lambda})\right]-R^*
\leq
\frac{\lambda}{2}\|\theta^*\|_2^2
+
\frac{\sigma^2\operatorname{tr}(\widehat{\Sigma})}
{2\lambda n}
\le
\sigma\|\theta^*\|_2\sqrt{\frac{tr(\hat \Sigma)}{n}}
$$
Exercise 3.6 计算经验风险，若使用$θ^⊤Λθ$替换原本的正则项$λ\|θ\|_2^2$其中$Λ\in R^{d×d}$是一个正定矩阵

Exercise 3.7 () Consider the “leave-one-out” estimator θ−i
λ ∈ Rd obtained, for each
i ∈ {1, . . . , n}, by minimizing 1
n
P
j6=i(yj − θ⊤ϕ(xj ))2 + λkθk22
. Given the matrix H =
Φ(Φ⊤Φ + nλI)−1Φ⊤ ∈ Rn×n, and its diagonal h = diag(H) ∈ Rn, show that
1
n
Xn
i=1
(yi − ϕ(xi)⊤θ−i
λ )2 =
1
nk(I − Diag(h))−1(I − H)yk22
,
where Diag(h) denotes the diagonal matrix with h as its diagonal. Hint: use Woodbury
matrix identities from section 1.1.3.

3.7.下界估计

在固定设计、线性模型正确设定、噪声为高斯噪声时，不论使用什么估计方法，最坏情况下的期望超额风险都不可能小于$\frac{d\sigma^2}{n}$

固定设计模型为
$$
y=\Phi\theta^*+\varepsilon,
\qquad
\varepsilon\sim\mathcal N(0,\sigma^2I_n),
$$
其中：

- $\Phi\in\mathbb R^{n\times d}$ 是给定的设计矩阵；
- $\theta^*\in\mathbb R^d$ 是未知参数；
- $y\in\mathbb R^n$ 是观测数据。

定义经验协方差矩阵
$$
\widehat\Sigma=\frac1n\Phi^\top\Phi.
$$
在模型正确设定时，任意参数估计值 $\theta$ 的超额风险是
$$
R_{\theta^*}(\theta)-R^*
=
\|\theta-\theta^*\|_{\widehat\Sigma}^2.
$$
现在不再只考虑 OLS 或 Ridge，而是考虑**任何估计器**
$$
A:\mathbb R^n\to\mathbb R^d,
\qquad
\widehat\theta=A(y).
$$
它可以是线性的、非线性的、有偏的，都没有关系。教材研究的是
$$
\inf_A\sup_{\theta^*\in\mathbb R^d}
\mathbb E_\varepsilon
\left[
R_{\theta^*}\bigl(A(\Phi\theta^*+\varepsilon)\bigr)-R^*
\right].
$$
这里：

- $\sup_{\theta^*}$：对估计器来说最不利的真实参数；
- $\inf_A$：在所有可能的估计算法中选择最好的一个。

这就是该问题的 **minimax risk**。

接下来我们逐步梳理证明：

首先，我们将选择$\theta^*\sim \mathcal N\left(0,\frac{\sigma^2}{\lambda n}I_d\right),\lambda>0$的一个先验分布来选取，选取参数使得最大化风险大小的会大于等于在这个先验正态分布下的风险大小
$$
\sup_{\theta^*\in\mathbb R^d}
\mathbb E_\varepsilon
\left[
R_{\theta^*}\bigl(A(\Phi\theta^*+\varepsilon)\bigr)
\right]
\ge
\mathbb E_{\theta^*\sim
\mathcal N(0,\frac{\sigma^2}{\lambda n}I)}
\mathbb E_\varepsilon
\left[
R_{\theta^*}\bigl(A(\Phi\theta^*+\varepsilon)\bigr)
\right].
$$
记
$$
\widehat\Sigma=\frac1n\Phi^\top\Phi,
\qquad
\|u\|_{\widehat\Sigma}^2=u^\top\widehat\Sigma u,
$$
并取先验
$$
\theta^*\sim\mathcal N\left(0,\frac{\sigma^2}{\lambda n}I_d\right),
\qquad
\varepsilon\sim\mathcal N(0,\sigma^2I_n),
$$
二者相互独立。教材先证明平方损失下最优的 Bayes 估计器是后验均值；由于后验为高斯分布，后验均值等于后验众数，而后验众数恰好给出 Ridge 估计器；然后证明这个估计器对应的误差就是$\frac{d\sigma^2}{n}$

记minimax 超额风险
$$
\mathcal M
:=
\inf_A
\sup_{\theta^*\in\mathbb R^d}
\mathbb E_{\varepsilon}
\left[
R_{\theta^*}\bigl(A(\Phi\theta^*+\varepsilon)\bigr)
\right]
-R^*.
$$
因此有不等式
$$
\mathcal M
\ge
\inf_A
\mathbb E_{\theta^*\sim
\mathcal N(0,\frac{\sigma^2}{\lambda n}I)}
\mathbb E_\varepsilon
\left[
R_{\theta^*}\bigl(A(\Phi\theta^*+\varepsilon)\bigr)
\right]-R^*.
$$
然后我们可以得到经验风险的衡量，这是一个与$R_{\theta^*}(\theta)= \mathbb E\|\Phi(\theta^*-\theta)+\widetilde\varepsilon\|_2^2=\mathbb E\|\Phi(\theta^*-\theta)\|_2^2+\mathbb E\|\widetilde\varepsilon\|_2^2$

这样拆分是因为交叉项均值为零，所以我们真实打包进入风险的$\hat\theta=A(y)=A(\Phi\theta^*+\varepsilon)$

由平方损失极小化的要求，实际上就是要让$min\mathbb E_{\theta}\|\Phi(\theta^*-\theta)\|_2^2$

$\hat \theta_{A} = \mathbb E(\theta^*|y)$条件期望就是在平方意义下的最佳逼近

所以就转化为了:
$$
\inf_A
\mathbb E_{\theta^*\sim
\mathcal N(0,\frac{\sigma^2}{\lambda n}I)}
\mathbb E_\varepsilon
\left[
R_{\theta^*}\bigl(A(\Phi\theta^*+\varepsilon)\bigr)
\right]=\mathbb E_{\theta^*\sim
\mathcal N(0,\frac{\sigma^2}{\lambda n}I)}
\mathbb E_\varepsilon
\left[
R_{\theta^*}\bigl(A^*(\Phi\theta^*+\varepsilon)\bigr)
\right] 
$$
进而就进一步得到了:
$$
\mathbb E_{\theta^*\sim
\mathcal N(0,\frac{\sigma^2}{\lambda n}I)}
\mathbb E_\varepsilon
\left[
R_{\theta^*}\bigl(A^*(\Phi\theta^*+\varepsilon)\bigr)
\right]-R^*
=
\mathbb E_{\theta^*\sim
\mathcal N(0,\frac{\sigma^2}{\lambda n}I)}
\mathbb E_\varepsilon
\left\|
A^*(\Phi\theta^*+\varepsilon)-\theta^*
\right\|_{\widehat\Sigma}^2.
$$
其中这一步实际上还需要再仔细推理一下：

首先$R^*= E\|\widetilde\varepsilon\|_2^2$就可以直接打包进前面的风险，消掉一个常数

问题就转化为$R_{\theta……*}$

2. 应该如何选取这个$\phi(x)$，我们应该如何把这个代码写出来



3. 我们刚才的那一顿牺牲不可行性操作到底“牺牲”了多少，误差分析。有什么东西是我们无论如何也决定不了的，那就是随机性的问题，在噪声作用下



4. 由于我们的笨蛋计算机和笨蛋数据我们不得不再次做一些取舍：加入正则性条件，生成稀疏性

5. 有没有已经写好的库，应该如何实现代码，并且再一个看上去更像回事的数据集上进行处理

6. 如果我们处理的不是回归问题，我们要求输出分类问题。我们在看上去更像一个问题的数据集上运行我们的数据，我们再装腔作势分析一波。

7. 当我们优化的时候到底发生了什么？就纯粹的梯度下降

8. 深度线性神经网络的优化：虽然看上去与单层等价，但是优化的效果上不等价；虽然这样做

假设真实的问题$y_i = \varphi(x_i)^⊤θ^∗ + ε_i$.

线性回归的闭式解，最小二乘问题

加入正则项的分析，稀疏学习（参考）

误差分析的CRLB下界，为什么这是一个最佳估计？

线性回归问题：算法实现，Softmax

逻辑回归，使用软阈值分类：

最小二乘算法更详细的分析：

PCA主成分分析：



## 附录与参考资料

李沐：动手学深度学习，第三四章

ai-engineering-from-scratch

LTFP：从第一性原理出发的学习理论

Learning Mechanics：There Will Be a Scientific Theory of Deep Learning

