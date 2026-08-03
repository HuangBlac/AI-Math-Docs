Ch4.4.4Beyond Finitely Many Models through Covering Numbers

我们来回到4.4开始，我们实际上考虑的Estimation error在已经给定一个函数类$\mathcal F$，希望证明在这个有界的函数类之内证明$\mathcal{\hat R}$之中搜索到的$\hat f$代入风险期望损失仍然不大

$\mathcal R(\hat f)-\inf_{f\in\mathcal F}\mathcal R(f)$

如果对于有限的函数类，那么$R_n(\mathcal H)$可以有限组合的情况来组合？

但是对于一个无限的函数类怎么估计呢？

对于简化的情形，我们假设损失函数是正则的，也就是“好”的。例如，损失函数关于第二边缘是G-Lipshcisz-continuous，因此我们section 4.3可以推出的就是对于$f, f′ ∈ F$,满足如下不等式
$$
\mathcal R(f) − \mathcal R(f′)

\le G · \mathbb E

|f(x) − f′(x)|

= G · Δ(f, f′). (4.11)
$$
书里 4.4.4 正是这样引入 covering number：用有限个函数 $f_1,\dots,f_m$ 近似整个函数类；如果每个 $f$ 都能被某个 $f_i$ 以误差 $\varepsilon$ 近似，那么 $m(\varepsilon)$ 就是 covering number。

### 覆盖数

我们假设存在 \(m=m(\varepsilon)\) 个函数\[ f_1,\ldots,f_m, \]使得对于任意 \(f\in\mathcal F\)，都存在某个

\[ i\in\{1,\ldots,m\}, \]满足\[ \Delta(f,f_i)\le\varepsilon, \]其中距离 \(\Delta\) 由公式 (4.11) 定义。

满足上述覆盖条件所需的最小数量 \(m(\varepsilon)\)，称为函数类 \(\mathcal F\) 在精度 \(\varepsilon\) 下的**覆盖数**。

教材随后给出了一个二维例子，展示如何用欧几里得球覆盖一个集合。

覆盖数 \(m(\varepsilon)\) 是关于 \(\varepsilon\) 的单调不增函数。通常，当\[ \varepsilon\to0 \]时，\(m(\varepsilon)\) 会按照\[ \varepsilon^{-d} \]的幂次增长，其中 \(d\) 是底层空间的维数。

具体来说，对于 \(\ell_\infty\) 度量，如果在某种参数化下，函数类 \(\mathcal F\) 被包含在一个 \(d\) 维、半径为 \(c\) 的 \(\ell_\infty\) 球内，那么当 \(c\ge\varepsilon\) 时，可以很容易地用

\[ \left(\frac{c}{\varepsilon}\right)^d \]个边长为 \(2\varepsilon\) 的立方体将它覆盖，如图所示。图中的整体区域边长为 \(2c\)，每个小立方体的边长为 \(2\varepsilon\)。

由于在有限维空间 \(\mathbb R^d\) 中所有范数都是等价的，对于有限维向量空间的任意有界子集，在其他范数下，覆盖数 \(m(\varepsilon)\) 也具有同样的 \(\varepsilon^{-d}\) 阶依赖关系。

因此，当 \(\varepsilon\to0\) 时，

\[ \log m(\varepsilon) \]

按照

\[ d\log\frac1\varepsilon \]

的速度增长。这种对维数 \(d\) 的依赖关系可以推广到所有范数；参见练习 4.8。

Exercise 4.8 Let m(ε) be the covering number of a unit ball of Rd by balls of radius ε for
an arbitrary norm. Using comparisons of volumes, show that
$$
(\frac {1}{\varepsilon})^d\le m(\varepsilon)\le(1+\frac{2}{\varepsilon})^d
$$
首先证明下界：

因为这个m个球的体积和肯定大于覆盖的集合，因此对于单位体积的任何元素，总能给出$m(\varepsilon)^d\ge1$

其次考虑上界，对于covering number的情况，这m个点，每个点两两之间的距离大于$\varepsilon$，那么每个球选取$\frac \varepsilon 2$的小球，两两之间不相交。而这些小球实际上都处在半径为$1+\varepsilon/2$的大球之内：

因此$m(\frac{\varepsilon}{2})^d\le(1+\frac \varepsilon 2)^d$,进而有$m\le(1+\frac 2 \varepsilon)^d$



For some sets (e.g., all Lipschitz-continuous functions with bounded Lipschitz-constant
in d dimensions), logm(ε) grows faster, such as ε−d. See, for instance,Wainwright (2019).

ε-net argument. Given a cover of F, for all f ∈ F, and with (fi)i∈{1,...,m(ε)} being
the associated cover elements, using that both bR and R are G-Lipschitz-continuous with
respect to the distance Δ, we have, for any i ∈ {1, . . . ,m(ε)},
$$
| \mathcal{\hat R}(f)-\mathcal R(f) |\le|\mathcal{\hat R}(f)-\mathcal{\hat R}(f_i)|+|\mathcal{\hat R}(f_i)-\mathcal R(f_i)|+|\mathcal{R}(f)-\mathcal{R}(f_i)|\\
\le 2G\Delta (f,f_i)+|\mathcal{\hat R}(f_i)-\mathcal R(f_i)|\\
\le 2G\varepsilon+\sup_{j\in\{1,\cdots,m(\varepsilon)\}}|\mathcal{\hat R}(f_j)-\mathcal R(f_j)|
$$
我们对于右边项第二项，使用有限函数类的已有结论，可以得到有1 − δ以上概率满足,
$$
\sup_{f∈F}|\mathcal{\hat{R}}(f) −\mathcal R(f)|
\le 2G\varepsilon + ℓ_∞
\sqrt {\frac
{log(2m(ε)))}
{2n}}
+\frac {ℓ_∞}{2n}\sqrt{log \frac 1\delta}
.
$$
而由Ex4.8的结论覆盖数$m(\varepsilon)\sim\varepsilon^{-d}$忽略常数系数，我们可以得到一个上界：$ε +\sqrt{\frac{d log(1/ε)}{n}}$而只要选取$\varepsilon\sim\frac{1}{\sqrt n}$就可以实现一个误差上界：$\sqrt{dlog (n)/n}$

问题是：这个 bound 往往不够精细。书里也指出，单纯的 covering number argument 可能不够，需要更精细的 covering number 计算或者更高级工具，例如 chaining。

Ch4.5 intro

已知样本$z_i=(x_i,y_i)$,$z_1,z_2,\cdots,z_n$为独立同分布抽取的n个样本，$\mathcal H$是函数类$h:\mathcal Z\to \mathbb R$的子集，在本文之中，函数类来自于学习问题：$\mathcal H =\{(x,y)\to\ell (f(x),y),f\in\mathcal F\}$

我们的目标是找到一个上界：$\sup_{f\in\mathcal F}|\mathcal {\hat R}(f)-\mathcal R(f) |$

等价于:
$$
\sup_{h\in\mathcal H}|\mathbb Eh(z)-\frac{1}{n}\sum_{i=1}^n h(z_i)|
$$
引入独立随机符号

\[ \varepsilon_1,\ldots,\varepsilon_n, \qquad \mathbb P(\varepsilon_i=1) = \mathbb P(\varepsilon_i=-1) = \frac12, \]

并且这些随机符号与数据 \(D=\{z_1,\ldots,z_n\}\) 相互独立。

定义

\[ \boxed{ R_n(\mathcal H) = \mathbb E_{D,\varepsilon} \left[ \sup_{h\in\mathcal H} \frac1n \sum_{i=1}^n \varepsilon_i h(z_i) \right]. } \]

对固定的 \(h\)，由于 \(\mathbb E[\varepsilon_i]=0\)，

\[ \mathbb E_\varepsilon \left[ \frac1n\sum_{i=1}^n \varepsilon_i h(z_i) \right] =0. \]

但定义中是先选择能使随机和最大的 \(h\)，再对随机符号取期望：

\[ \mathbb E_\varepsilon \left[ \sup_{h\in\mathcal H}(\cdots) \right]. \]

因此它一般不等于零。这里

\[ \mathbb E\sup_h(\cdots) \neq \sup_h\mathbb E(\cdots). \]

两者顺序的差别正是 Rademacher complexity 能够测量函数类容量的原因。

所以这么一通操作是为了说明什么？首先我们来看引入这个函数类的泛函$R_n$是干什么：

在固定数据 \(z_1,\ldots,z_n\)，每个函数 \(h\) 在样本上的取值可以写成向量

\[ v_h = \bigl(h(z_1),\ldots,h(z_n)\bigr). \]

随机符号也构成向量

\[ \varepsilon = (\varepsilon_1,\ldots,\varepsilon_n). \]

于是

\[ \frac1n\sum_{i=1}^n \varepsilon_i h(z_i) = \frac1n\langle \varepsilon,v_h\rangle. \]

Rademacher complexity 考察的是

\[ \sup_{h\in\mathcal H} \frac1n\langle\varepsilon,v_h\rangle, \]

在观察到一组完全随机的正负标签之后，函数类能从中挑出一个函数，使其函数值与这些随机标签尽可能一致吗？

如果 \(\mathcal H\) 很丰富，它可能找到一个函数满足大致

\[ h(z_i)>0\quad\text{当 }\varepsilon_i=1, \]\[ h(z_i)<0\quad\text{当 }\varepsilon_i=-1. \]

此时内积很大，说明这个函数类连纯噪声都能迎合，因此容量很大，过拟合风险也更高。

反过来，如果所有函数都很受限制，就无法配合随机正负号，随机内积会大量抵消，因此 \(R_n(\mathcal H)\) 较小。

Ex4.9介绍了Rademachester复杂度的一些性质。

### 1. 单调性

如果

\[ \mathcal H\subseteq\mathcal H', \]

证明

\[ R_n(\mathcal H)\le R_n(\mathcal H'). \]

固定 \(D,\varepsilon\)，因为取 supremum 的集合变大了，

\[ \sup_{h\in\mathcal H}L(h) \le \sup_{h\in\mathcal H'}L(h). \]

两边再对 \(D,\varepsilon\) 取期望：

\[ \boxed{ R_n(\mathcal H)\le R_n(\mathcal H'). } \]

这说明：候选函数越多，拟合随机符号的能力不会下降。

------

### 2. Minkowski 和的可加性

定义

\[ \mathcal H+\mathcal H' = \{h+h':h\in\mathcal H,\ h'\in\mathcal H'\}. \]

证明

\[ R_n(\mathcal H+\mathcal H') = R_n(\mathcal H)+R_n(\mathcal H'). \]

利用 \(L\) 的线性性：

\[ L(h+h')=L(h)+L(h'). \]

因此

\[ \begin{aligned} \sup_{g\in\mathcal H+\mathcal H'}L(g) &= \sup_{\substack{h\in\mathcal H\\h'\in\mathcal H'}} \{L(h)+L(h')\}\\ &= \sup_{h\in\mathcal H}L(h) + \sup_{h'\in\mathcal H'}L(h'). \end{aligned} \]

两个函数可以独立选择，所以 supremum 可以拆开。取期望后得到

\[ \boxed{ R_n(\mathcal H+\mathcal H') = R_n(\mathcal H)+R_n(\mathcal H'). } \]

------

### 3. 绝对齐次性

定义

\[ \alpha\mathcal H = \{\alpha h:h\in\mathcal H\}. \]

证明

\[ R_n(\alpha\mathcal H) = |\alpha|R_n(\mathcal H). \]

当 \(\alpha\geq 0\) 时，

\[ \sup_{h\in\mathcal H}L(\alpha h) = \alpha\sup_{h\in\mathcal H}L(h), \]

所以结论直接成立。

当 \(\alpha<0\) 时，

\[ \begin{aligned} R_n(\alpha\mathcal H) &= \mathbb E_{D,\varepsilon} \sup_{h\in\mathcal H} \frac{\alpha}{n} \sum_i\varepsilon_i h(z_i)\\ &= |\alpha| \mathbb E_{D,\varepsilon} \sup_{h\in\mathcal H} \frac1n \sum_i(-\varepsilon_i)h(z_i). \end{aligned} \]

由于

\[ (-\varepsilon_1,\ldots,-\varepsilon_n) \overset{d}{=} (\varepsilon_1,\ldots,\varepsilon_n), \]

所以

\[ \boxed{ R_n(\alpha\mathcal H) = |\alpha|R_n(\mathcal H). } \]

注意这里不能在固定 \(\varepsilon\) 后直接把负数移出 supremum；关键是 Rademacher 符号具有对称分布。

------

### 4. 加上一个固定函数不改变复杂度

若 \(h_0:\mathcal Z\to\mathbb R\)，证明

\[ R_n(\mathcal H+\{h_0\})=R_n(\mathcal H). \]

固定 \(D,\varepsilon\)：

\[ \begin{aligned} \sup_{h\in\mathcal H}L(h+h_0) &= \sup_{h\in\mathcal H} \{L(h)+L(h_0)\}\\ &= \sup_{h\in\mathcal H}L(h)+L(h_0). \end{aligned} \]

取期望：

\[ R_n(\mathcal H+\{h_0\}) = R_n(\mathcal H) + \mathbb E_{D,\varepsilon}L(h_0). \]

而

\[ \begin{aligned} \mathbb E_\varepsilon L(h_0) &= \frac1n\sum_{i=1}^n h_0(z_i)\mathbb E[\varepsilon_i]\\ &=0. \end{aligned} \]

所以

\[ \boxed{ R_n(\mathcal H+\{h_0\}) = R_n(\mathcal H). } \]

直觉是：给整个函数类统一加上同一个“基线函数”，不会改变函数之间的相对灵活性。

也可以证明单函数的一维扩展空间的Rademachester复杂度为0，因为只能选取一个固定的h。

------

### 5. 取凸包不改变复杂度

证明

\[ R_n(\operatorname{conv}(\mathcal H)) = R_n(\mathcal H). \]

任取

\[ g\in\operatorname{conv}(\mathcal H), \]

则存在 \(h_1,\ldots,h_k\in\mathcal H\) 和

\[ \lambda_j\geq0,\qquad \sum_{j=1}^k\lambda_j=1, \]

使得

\[ g=\sum_{j=1}^k\lambda_jh_j. \]

因为 \(L\) 是线性的，

\[ \begin{aligned} L(g) &= \sum_{j=1}^k\lambda_jL(h_j)\\ &\leq \sum_{j=1}^k \lambda_j \sup_{h\in\mathcal H}L(h)\\ &= \sup_{h\in\mathcal H}L(h). \end{aligned} \]

因此

\[ \sup_{g\in\operatorname{conv}(\mathcal H)}L(g) \leq \sup_{h\in\mathcal H}L(h). \]

另一方面，

\[ \mathcal H\subseteq\operatorname{conv}(\mathcal H), \]

所以反向不等式也成立。于是

\[ \boxed{ R_n(\operatorname{conv}(\mathcal H)) = R_n(\mathcal H). } \]

本质原因是：

> 线性函数在凸包上的最大值，一定可以在原集合的极端点上达到或逼近。

这条性质以后分析 boosting、混合模型和两层神经网络时非常重要。

Massart lemma:

设有限函数类

\[ \mathcal H=\{h_1,\ldots,h_m\}, \]

并且几乎处处满足

\[ \frac1n\sum_{i=1}^n h_j(z_i)^2\leq R^2, \qquad j=1,\ldots,m. \]

证明

\[ \boxed{ R_n(\mathcal H) \leq R\sqrt{\frac{2\log m}{n}}. } \]

定义

\[ X_j = \frac1n\sum_{i=1}^n \varepsilon_i h_j(z_i). \]

固定 \(D\) 后，

\[ \widehat R_D(\mathcal H) = \mathbb E_\varepsilon \max_{1\leq j\leq m}X_j. \]

我们需要控制 \(m\) 个随机变量的最大值。

首先使用经典的log-exp-sum技巧
$$
\max_{1\leq j\leq m}X_j\le \frac 1 \lambda log(\sum_{j=1}^m e^{\lambda X_j})
$$
然后求期望，使用Jensen不等式把期望算子给挪到里面：
$$
\mathbb E\max_{1\leq j\leq m}X_j\le \frac 1 \lambda \mathbb Elog(\sum_{j=1}^m e^{\lambda X_j})\le\frac 1 \lambda log(\mathbb E \sum_{j=1}^m e^{\lambda X_j})
$$
关于指数期望，还是比较好算的 ，因为$\varepsilon_i h_j(z_i)$是彼此独立的

\[ \begin{aligned} \mathbb E_\varepsilon e^{\lambda X_j} &= \prod_{i=1}^n \mathbb E_{\varepsilon_i} \exp\left( \frac{\lambda}{n} \varepsilon_i h_j(z_i) \right)\\ &= \prod_{i=1}^n \cosh\left( \frac{\lambda h_j(z_i)}n \right). \end{aligned} \]

利用

\[ \cosh(u)\leq e^{u^2/2}, \]

得到

\[ \begin{aligned} \mathbb E_\varepsilon e^{\lambda X_j} &\leq \exp\left( \frac{\lambda^2}{2n^2} \sum_{i=1}^n h_j(z_i)^2 \right)\\ &\leq \exp\left( \frac{\lambda^2R^2}{2n} \right). \end{aligned} \]

$\frac 1 \lambda \log(\mathbb E \sum_{j=1}^m e^{\lambda X_j})\le \frac 1 \lambda \log(m e^{\frac{\lambda^2R^2}{2n}})=\frac 1 \lambda \log(m)+\frac{\lambda R^2}{2n}$

通过选取$\lambda$让基本不等式成立，得到上界$R\sqrt{\frac{\log m}{n}}$





