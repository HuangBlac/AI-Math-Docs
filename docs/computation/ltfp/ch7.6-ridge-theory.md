# Ch7.6 岭回归的理论分析

这一节研究核岭回归在随机设计和无限维特征空间中的统计误差。推导从一个很具体的问题开始。训练时只能看到经验协方差算子，测试误差却由总体协方差算子决定。要得到学习率，必须把两者联系起来，再分别估计偏差与方差。

> 状态　依照 LFTP §7.6 的 Proposition 7.5 至 Proposition 7.8 与 Lemma 7.1 至 Lemma 7.2 整理。符号和公式已按原书统一，内容仍保留为待人工签认的精读笔记。

## 1. 问题设置

设训练样本 $(x_i,y_i)_{i=1}^n$ 独立同分布，回归模型满足

```math
y_i=f^*(x_i)+\varepsilon_i,
\qquad
\mathbb E[\varepsilon_i\mid x_i]=0,
\qquad
\mathbb E[\varepsilon_i^2\mid x_i]\leq \sigma^2.
```

这里 $f^\star(x)=\mathbb E[Y\mid X=x]$，输入分布记为 $p$。给定核 $k$、对应的 RKHS $\mathcal H$ 和正则化参数 $\lambda>0$，核岭回归求解

```math
\widehat f_\lambda
\in
\arg\min_{f\in\mathcal H}
\left\{
\frac1n\sum_{i=1}^n\bigl(y_i-f(x_i)\bigr)^2
+\lambda\|f\|_{\mathcal H}^2
\right\}.
```

平方损失下，总体超额风险恰好等于 $L^2(p)$ 误差

```math
R(f)-R(f^\star)=\|f-f^\star\|_{L^2(p)}^2.
```

这一章同时出现两个 Hilbert 空间。$\mathcal H$ 控制函数的复杂度，$L^2(p)$ 衡量预测误差。两种范数不能混写。

## 7.6.1 核岭回归作为线性估计量

表示定理给出

```math
\widehat f_\lambda(x)
=\sum_{i=1}^n\alpha_i k(x,x_i),
\qquad
\alpha=(K+n\lambda I)^{-1}y,
```

其中 $K_{ij}=k(x_i,x_j)$。令

```math
q(x)=
\begin{bmatrix}
k(x,x_1)&\cdots&k(x,x_n)
\end{bmatrix}^{\!\top},
```

便有

```math
\widehat f_\lambda(x)
=q(x)^\top(K+n\lambda I)^{-1}y
=\sum_{i=1}^n\widehat w_i(x)y_i,
\qquad
\widehat w(x)=(K+n\lambda I)^{-1}q(x).
```

给定输入样本以后，预测值是响应向量 $y$ 的线性函数。它对输入 $x$ 通常仍是非线性的。训练点上的拟合值满足

```math
\widehat y=H_\lambda y,
\qquad
H_\lambda=K(K+n\lambda I)^{-1}.
```

若 $K=U\operatorname{diag}(\rho_1,\ldots,\rho_n)U^\top$，平滑矩阵的特征值为

```math
\frac{\rho_j}{\rho_j+n\lambda}.
```

大的核特征值方向保留得更多，小特征值方向收缩得更强。局部平均法常要求权重非负且和为 $1$，核岭回归允许负权重。这种更自由的线性组合能够利用函数的高阶光滑性。

实际计算只需完成三步。

1. 由训练输入组成 Gram 矩阵 $K$。
2. 求解线性方程 $(K+n\lambda I)\alpha=y$，无需显式计算逆矩阵。
3. 对新输入 $x$ 计算 $q(x)^\top\alpha$。

直接求解的时间复杂度通常为 $O(n^3)$，存储量为 $O(n^2)$。Ch7.4 的随机特征、Nyström 近似和迭代法用于降低这部分代价。

## 3. 7.6.2 偏差与方差分解

### 3.1 两个协方差算子

令 $\varphi(x)\in\mathcal H$ 为特征映射，并约定

```math
(a\otimes b)f=\langle b,f\rangle_{\mathcal H}a.
```

经验协方差算子与总体协方差算子分别为

```math
\widehat\Sigma
=\frac1n\sum_{i=1}^n\varphi(x_i)\otimes\varphi(x_i),
\qquad
\Sigma
=\mathbb E\bigl[\varphi(X)\otimes\varphi(X)\bigr].
```

对任意 $g\in\mathcal H$，再生性质给出

```math
\|g\|_{L^2(p)}^2
=\langle g,\Sigma g\rangle_{\mathcal H}
=\|\Sigma^{1/2}g\|_{\mathcal H}^2.
\tag{7.18}
```

这条恒等式把预测误差转成了 $\mathcal H$ 中的算子二次型，是后续推导的连接点。

### 3.2 估计量的算子形式

目标函数的一阶最优条件给出

```math
\widehat f_\lambda
=(\widehat\Sigma+\lambda I)^{-1}
\left(\frac1n\sum_{i=1}^ny_i\varphi(x_i)\right).
```

当 $f^\star\in\mathcal H$ 时，$f^\star(x_i)=\langle f^\star,\varphi(x_i)\rangle_{\mathcal H}$，因此

```math
\widehat f_\lambda-f^\star
=
-\lambda(\widehat\Sigma+\lambda I)^{-1}f^\star
+(\widehat\Sigma+\lambda I)^{-1}
\left(\frac1n\sum_{i=1}^n\varepsilon_i\varphi(x_i)\right).
```

第一项由正则化收缩产生，第二项来自观测噪声。条件均值为零使两项的交叉项消失。

### 3.3 方差项

利用噪声的条件独立性、条件方差上界以及式 (7.18)，可以得到

```math
\operatorname{Var}_\lambda
\leq
\frac{\sigma^2}{n}
\mathbb E\operatorname{tr}
\left[
(\widehat\Sigma+\lambda I)^{-1}
\Sigma
(\widehat\Sigma+\lambda I)^{-1}
\widehat\Sigma
\right].
```

又因为

```math
(\widehat\Sigma+\lambda I)^{-1}\widehat\Sigma
\preccurlyeq I,
```

方差进一步满足

```math
\operatorname{Var}_\lambda
\leq
\frac{\sigma^2}{n}
\mathbb E\operatorname{tr}
\left[(\widehat\Sigma+\lambda I)^{-1}\Sigma\right].
\tag{7.19}
```

$\lambda$ 增大时，逆算子受到更强抑制，方差随之下降。

### 3.4 偏差项

同样使用式 (7.18)，平方偏差可以写成

```math
\operatorname{Bias}_\lambda^2
=
\lambda^2
\mathbb E
\left\langle
f^\star,
(\widehat\Sigma+\lambda I)^{-1}
\Sigma
(\widehat\Sigma+\lambda I)^{-1}f^\star
\right\rangle_{\mathcal H}.
\tag{7.22}
```

$\lambda$ 增大时，估计量向零函数收缩得更明显，偏差通常会上升。合并两项便得到 Proposition 7.5 的期望风险上界。

## 7.6.3 经验算子与总体算子的联系

风险表达式里混合出现了 $\widehat\Sigma$ 和 $\Sigma$。假设特征有界

```math
\|\varphi(x)\|_{\mathcal H}\leq R
\qquad \text{几乎处处成立},
```

并记

```math
\kappa_\lambda=\frac{R^2}{\lambda n}.
```

Lemma 7.1 给出两条关键比较式。第一条控制方差

```math
\mathbb E\operatorname{tr}
\left[(\widehat\Sigma+\lambda I)^{-1}\Sigma\right]
\leq
(1+\kappa_\lambda)
\operatorname{tr}
\left[(\Sigma+\lambda I)^{-1}\Sigma\right].
\tag{7.24}
```

第二条控制偏差。对每个 $g\in\mathcal H$ 都有

```math
\mathbb E
\left\langle
g,
(\widehat\Sigma+\lambda I)^{-1}
\Sigma
(\widehat\Sigma+\lambda I)^{-1}g
\right\rangle_{\mathcal H}
\leq
\frac{(1+\kappa_\lambda)^2}{\lambda}
\left\langle
g,
(\Sigma+\lambda I)^{-1}\Sigma g
\right\rangle_{\mathcal H}.
\tag{7.25}
```

证明引入一个独立样本 $x_{n+1}$，把 $n+1$ 个样本组成的算子记为 $C$。Sherman-Morrison 公式把删去一个样本后的逆算子与 $(C+n\lambda I)^{-1}$ 联系起来。样本的可交换性负责平均每个位置，最后用 Jensen 不等式把随机算子替换为它的期望。

$\kappa_\lambda$ 衡量经验算子逼近总体算子时付出的代价。为了让额外常数保持稳定，通常需要 $\lambda n$ 至少与 $R^2$ 同阶。

## 5. 7.6.4 适定情形

当 $f^\star\in\mathcal H$ 时，代入式 (7.24) 和式 (7.25) 可得 Proposition 7.6

```math
\begin{aligned}
\mathbb E\|\widehat f_\lambda-f^\star\|_{L^2(p)}^2
\leq{}&
\frac{\sigma^2}{n}(1+\kappa_\lambda)
\operatorname{tr}\left[(\Sigma+\lambda I)^{-1}\Sigma\right]\\
&+\lambda(1+\kappa_\lambda)^2
\left\langle
f^\star,
\Sigma(\Sigma+\lambda I)^{-1}f^\star
\right\rangle_{\mathcal H}.
\end{aligned}
\tag{7.27}
```

定义有效维数

```math
\mathcal N(\lambda)
=\operatorname{tr}\left[\Sigma(\Sigma+\lambda I)^{-1}\right].
```

若 $\Sigma e_j=\mu_j e_j$，则

```math
\mathcal N(\lambda)
=\sum_j\frac{\mu_j}{\mu_j+\lambda}.
```

每个谱方向贡献一个介于 $0$ 和 $1$ 之间的量。$\mu_j\gg\lambda$ 的方向近似贡献一个完整自由度，$\mu_j\ll\lambda$ 的方向几乎被忽略。无限维 RKHS 因而拥有一个随 $\lambda$ 变化的有限统计维数。

利用 $\operatorname{tr}(\Sigma)\leq R^2$ 和 $\Sigma(\Sigma+\lambda I)^{-1}\preccurlyeq I$，式 (7.27) 可放宽为

```math
\mathbb E\|\widehat f_\lambda-f^\star\|_{L^2(p)}^2
\leq
\frac{\sigma^2R^2}{\lambda n}(1+\kappa_\lambda)
+\lambda(1+\kappa_\lambda)^2\|f^\star\|_{\mathcal H}^2.
```

取 $\lambda\asymp R^2/\sqrt n$ 会给出 $n^{-1/2}$ 量级的无维数上界。在有限 $d$ 维特征空间中还有 $\mathcal N(\lambda)\leq d$，取 $\lambda\asymp R^2/n$ 后可得到

```math
\mathbb E\|\widehat f_\lambda-f^\star\|_{L^2(p)}^2
\lesssim
\frac{\sigma^2d}{n}
+\frac{R^2\|f^\star\|_{\mathcal H}^2}{n}.
```

平方损失还能通过直接的算子集中论证得到高概率界。若进一步假设 $\varepsilon_i^2\leq\sigma^2$ 几乎处处成立，并且

```math
n\geq
\left(\frac43+\frac{8R^2}{\lambda}\right)
\log\frac{14R^2}{\lambda\delta},
```

原书 Proposition 7.7 说明，以至少 $1-\delta$ 的概率有

```math
\|\widehat f_\lambda-f^\star\|_{L^2(p)}^2
\leq
\frac{8\sigma^2R^2}{\lambda n}
+4\lambda\|f^\star\|_{\mathcal H}^2
+\frac{16\sigma^2R^2}{\lambda n}\log\frac{2}{\delta}.
\tag{7.28}
```

## 7.6.5 超出适定情形

实际目标函数可能不属于 $\mathcal H$。只要 $f^\star$ 位于 $\mathcal H$ 在 $L^2(p)$ 中的闭包，核岭回归仍可通过越来越复杂的 RKHS 函数逼近它。

定义正则化逼近误差

```math
\mathcal A(\lambda)
=
\inf_{f\in\mathcal H}
\left\{
\|f-f^\star\|_{L^2(p)}^2
+\lambda\|f\|_{\mathcal H}^2
\right\}.
```

当 $f^\star\in\mathcal H$ 时，Lemma 7.2 给出

```math
\mathcal A(\lambda)
=
\lambda
\left\langle
f^\star,
(\Sigma+\lambda I)^{-1}\Sigma f^\star
\right\rangle_{\mathcal H}.
\tag{7.29}
```

等式右边原来只能在 $\mathcal H$ 中书写，左边的变分形式可以通过极限延伸到 $L^2(p)$ 闭包。Proposition 7.8 随后给出

```math
\mathbb E\|\widehat f_\lambda-f^\star\|_{L^2(p)}^2
\leq
\frac{\sigma^2}{n}(1+\kappa_\lambda)\mathcal N(\lambda)
+(1+\kappa_\lambda)^2\mathcal A(\lambda).
\tag{7.31}
```

这个式子把两种困难分开了。$\mathcal N(\lambda)$ 描述核和输入分布允许噪声进入多少个谱方向，$\mathcal A(\lambda)$ 描述目标函数能以多小的 RKHS 范数得到逼近。

## 7.6.6 平衡偏差与方差

### 7.1 有效维数的谱上界

有界特征使 $\Sigma$ 成为迹类算子。设其非增特征值满足

```math
\mu_m\leq C(m+1)^{-\alpha},
\qquad \alpha>1.
```

那么

```math
\mathcal N(\lambda)
=\sum_{m\geq0}\frac{\mu_m}{\mu_m+\lambda}
\leq
\sum_{m\geq0}\frac{1}{1+\lambda C^{-1}(m+1)^\alpha}
=O(\lambda^{-1/\alpha}).
```

对 $d$ 维区域上的 $s$ 阶 Sobolev RKHS，在输入密度有界等条件下，$\alpha=2s/d$，因此

```math
\mathcal N(\lambda)=O\!\left(\lambda^{-d/(2s)}\right).
```

### 7.2 Sobolev 光滑度下的学习率

设目标函数具有 $t$ 阶 Sobolev 光滑度，RKHS 的阶数为 $s$，并满足 $0<t\leq s$。正则化逼近误差的量级为

```math
\mathcal A(\lambda)=O\!\left(\lambda^{t/s}\right).
```

当 $\kappa_\lambda=O(1)$ 时，风险上界的主要部分化为

```math
\underbrace{\frac1n\lambda^{-d/(2s)}}_{\text{方差}}
+
\underbrace{\lambda^{t/s}}_{\text{偏差}}.
```

令两项同阶

```math
\lambda^{t/s}
\asymp
\frac1n\lambda^{-d/(2s)},
```

可得

```math
\lambda_\star\asymp n^{-2s/(2t+d)},
\qquad
\mathbb E\|\widehat f_{\lambda_\star}-f^\star\|_{L^2(p)}^2
=O\!\left(n^{-2t/(2t+d)}\right).
```

由于前面的经验算子比较要求 $\lambda n$ 不宜小于 $R^2$，这套证明还要求

```math
\frac d2<s,
\qquad
t\leq s\leq t+\frac d2.
```

几个特例能帮助辨认这个速率。

- 当 $t=1$ 时，得到经典的非参数回归速率 $n^{-2/(2+d)}$。
- 当模型适定且 $t=s$ 时，速率为 $n^{-2s/(2s+d)}$。
- $s$ 很大时，适定情形的指数接近 $1$，风险可以接近参数速率 $n^{-1}$。

更光滑的目标函数带来更快的收敛，核的谱衰减决定方差的有效维数。若要让 $\lambda$ 小于 $1/n$，还需要比本节更强的分布或噪声条件。

## 8. 推导主线

```text
Gram 矩阵闭式解
    -> 经验协方差算子表示
    -> L2(p) 风险写成总体算子二次型
    -> 噪声项与收缩项分离
    -> 用 Lemma 7.1 替换经验算子
    -> 有效维数 N(lambda) 与逼近误差 A(lambda)
    -> 选择 lambda 平衡方差和偏差
    -> 得到 n^(-2t/(2t+d))
```

读这一节时最容易混淆三组对象。

| 对象 | 作用 | 常见误区 |
|---|---|---|
| $\widehat\Sigma$ 与 $\Sigma$ | 前者由训练输入产生，后者决定总体预测误差 | 直接把随机设计当作固定设计 |
| $\|\cdot\|_{\mathcal H}$ 与 $\|\cdot\|_{L^2(p)}$ | 前者进入惩罚，后者衡量泛化误差 | 把两个空间中的内积和范数混用 |
| $\mathcal N(\lambda)$ 与 $\mathcal A(\lambda)$ | 前者控制方差，后者控制偏差 | 只看样本量，忽略核谱和目标光滑度 |

## 9. 一页复习

核岭回归的算法解由 $(K+n\lambda I)\alpha=y$ 给出，理论分析则主要在算子层面进行。总体协方差算子把 $L^2(p)$ 风险带入 RKHS。Lemma 7.1 把含 $\widehat\Sigma$ 的随机量换成含 $\Sigma$ 的确定性谱量，额外代价由 $R^2/(\lambda n)$ 控制。适定模型的偏差可直接用 $\|f^\star\|_{\mathcal H}$ 约束，非适定模型改用 $\mathcal A(\lambda)$。最后用有效维数 $\mathcal N(\lambda)$ 表示方差，并选择 $\lambda$ 平衡两项。

## 参考

- Francis Bach, [Learning Theory from First Principles](https://www.di.ens.fr/~fbach/ltfp/), Chapter 7, §7.6.
