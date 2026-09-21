# Ch7.3–7.4 核的表示、列采样与随机特征

> 状态：`note_unverified`。由《ch7.3.pdf》3 页、《7.4.3 Random Feature.pdf》第 1、8 页，以及 2026-09-09《Ch7.2-7.3.pdf》的第 6–7 页整理。新增《Ch4.3-4.4补充.pdf》4 页（学习日期 2026-09-11，跨午夜于 2026-09-12 导入），按正文接续现有章节。对应 §7.3.1–§7.3.3、§7.4.1–§7.4.4；原稿 §7.6.1 的线性估计器视角已移至 [Ch7.6 笔记](ch7.6-ridge-theory.md)。

本篇只覆盖上述小节，不表示 §7.3–7.4 全部已有笔记。 表示定理的证明、核构造与新增 Mercer 习题笔记见 [Ch7.2 核基础](ch7.2-representer-kernel-foundations.md)。

### Ch7.3.1 多项式核与特征维数

来源：《ch7.3.pdf》第 2 页；教材印刷页 186–187。

下面考虑多项式核，对正整数 $s$，

```math
k(x,x')=(x^\top x')^s
=\sum_{\alpha_1+\cdots+\alpha_d=s}
\frac{s!}{\alpha_1!\cdots\alpha_d!}
\prod_{j=1}^d(x_jx_j')^{\alpha_j}.
```

每个多重指标 $\alpha\in\mathbb N^d$ 对应一个单项式特征，系数可拆到两边的平方根中。这些特征张成 $s$ 次齐次多项式空间；

并且可以用二项式定理^4 显式展开如下：

```math
\binom{s}{\alpha_1, \dots, \alpha_d} \underbrace{(x_1^{\alpha_1} \cdots x_d^{\alpha_d})((x'_1)^{\alpha_1} \cdots (x'_d)^{\alpha_d})}_{},
```

我们有显式特征映射：$\phi(x) = \left( \binom{s}{\alpha_1, \dots, \alpha_d}^{1/2} x_1^{\alpha_1} \cdots x_d^{\alpha_d} \right)_{\alpha_1 + \cdots + \alpha_d = s}$，而函数集是 $\mathbb{R}^d$ 上 $s$ 次齐次^5 多项式的集合，其维数为 $\binom{d + s - 1}{s}$。

**Ex7.3**，考虑非齐次核核 $k(x, x') = (1 + x^\top x')^s$ 对应所有满足 $\alpha_1 + \cdots + \alpha_d \leqslant s$ 的单项式 $x_1^{\alpha_1} \cdots x_d^{\alpha_d}$ 的集合。并证明特征空间的维数为 $\binom{d + s}{s}$。

已有展开为$k(x,x')=(1+x^\top x')^s=\sum_{k=0}^s\binom sk(x^\top x')^k.$对应多重指标条件 $\sum_i\alpha_i\le s$。

记录 $d=1$ 时共有 $s+1$ 个特征，使用归纳法证明后续部分：

已知$d\le k$时，已有特征空间的维数为$\binom{d+s}{s}$

考虑d=k+1时，对应的是满足$\alpha_1+\alpha_2+\cdots+\alpha_k+\alpha_{k+1}\le s$

可以选取$\alpha_{k+1}=0,1,\cdots,s$分别对应$\sum_{j=0}^s\binom{k+j}{j}$的求和结果，根据归纳法，可知求和结果确实是

$\binom{k+1+s}{s}=\binom{k+1+s}{k+1}$



### 7.3.2平移不变核与 Fourier 变换

来源：《ch7.3.pdf》第 1 页；教材 §7.3.3，印刷页 191–192。

#### Fouier变换记号

全文统一采用

```math
\widehat f(\omega)=\int_{\mathbb R^d}f(x)e^{-i\omega^\top x}\,dx,
\qquad
f(x)=\frac1{(2\pi)^d}\int_{\mathbb R^d}\widehat f(\omega)e^{i\omega^\top x}\,d\omega.
```

在适用上述反演与 Parseval 的条件下，

```math
\|f\|_{L^2(\mathbb R^d)}^2
=\frac1{(2\pi)^d}\int_{\mathbb R^d}|\widehat f(\omega)|^2\,d\omega.
```

平移不变核写作 $k(x,x')=g(x-x')$。这里用 $g$ 表示核剖面，避免与 [Ch6](ch6.1-6.3-local-averaging.md) 的平滑密度 $q$ 混淆。

#### 周期 Fourier 特征的起步

来源：原稿第 6 页；教材印刷页 187–188。

在 $\mathcal X=[0,1]$ 上讨论 $k(x,x')=q(x-x')$，其中 q 作 1 周期延拓。原稿从 Fourier 系数的加权惩罚出发：

```math
f(x)=\sum_{m\in\mathbb Z}\widehat f_m e^{2\pi imx},
\qquad\|f\|_c^2=\sum_{m\in\mathbb Z}c_m|\widehat f_m|^2,\quad c_m>0.
```

采用双线性配对的记法，可令

```math
\theta_m=\sqrt{c_m}\widehat f_m,
\qquad\psi_m(x)=\frac1{\sqrt{c_m}}e^{2\pi imx},
\qquad f(x)=\sum_m\theta_m\psi_m(x),
\qquad\|\theta\|_{\ell^2}^2=\|f\|_c^2.
```

> **记号整理：** 原稿 θ 式出现 $|\widehat f_m|$，会丢失符号或相位，这里恢复系数本身。上式直接采用原稿的配对和式；若改写为复 Hilbert 内积，须随内积的共轭约定调整分量，不能将两种配对混写。

**原始状态：只写到特征分量。** 周期核的最终求和式、特征逐点平方可和条件和具体核例子没有继续写。这里保留停止位置。

所以这和平移不变核有什么关系呢？



**Exercise 7.6**：Mercer 核与 ℓ² 特征 

来源：pdf 7.2-7.3第 7 页；教材印刷页 190。

给定概率分布 P、$L^2(P)$ 的可数标准正交基 $(\phi_i)_{i\in I}$ 及可和的正序列 $(\lambda_i)$。原稿考虑

```math
k(x,x')=\sum_{i\in I}\lambda_i\phi_i(x)\phi_i(x').
```

已有的正定性计算整理为

```math
\begin{aligned}
\alpha^\top K\alpha
&=\sum_{j,k=1}^n\alpha_j\alpha_k\sum_{i\in I}\lambda_i\phi_i(x_j)\phi_i(x_k)\\
&=\sum_{i\in I}\lambda_i\left(\sum_{j=1}^n\alpha_j\phi_i(x_j)\right)^2\ge0.
\end{aligned}
```

并有对称性 $k(x,x')=k(x',x)$。原稿明确选择了序列空间及特征分量：

```math
\mathcal H=\ell^2(I),\qquad
\Phi(x)=(\sqrt{\lambda_i}\phi_i(x))_{i\in I},\qquad
k(x,x')=\langle\Phi(x),\Phi(x')\rangle_{\ell^2(I)}.
```

**原始状态：正定性推导和特征表示已写，条件待核对。** 原稿末行误将特征序列排成求和，已按前文恢复为序列。上述表示需在所讨论点满足 $\sum_i\lambda_i|\phi_i(x)|^2<\infty$；原稿没有讨论该逐点条件、基函数代表元或交换求和的适用范围。这里只标出尚未展开处，不追加证明。

### Ch 7.3.3.$\mathbb R^d$上的平移不变核

**Proposition 7.4**：Bochner 定理

在通常的连续性条件下，连续平移不变核正定，当且仅当其剖面是非负有限 Borel 测度的逆 Fourier 变换。按上面的归一化写作

```math
g(x-x')=\frac1{(2\pi)^d}\int e^{i\omega^\top(x-x')}\,d\mu(\omega),\qquad \mu\ge0.
```

原稿写出的方向是由这个表示证明正定性。对有限样本及实系数 $\alpha_i$，

```math
\begin{aligned}
\alpha^\top K\alpha
&=\sum_{j,k}\alpha_j\alpha_k g(x_j-x_k)\\
&=\frac1{(2\pi)^d}\int\sum_{j,k}\alpha_j\alpha_k
e^{i\omega^\top x_j}\overline{e^{i\omega^\top x_k}}\,d\mu(\omega)\\
&=\frac1{(2\pi)^d}\int\left|\sum_j\alpha_je^{i\omega^\top x_j}\right|^2d\mu(\omega)
\ge0.
\end{aligned}
```

反方向目前只考虑“正定函数 → 正定分布 → Fourier 变换是正测度”的路线，未展开证明，保留为简写。



其中，当 $g,\widehat g$ 均可积时，判据为 $\forall \omega\in\mathbb R^d,\widehat g(\omega)\ge0$。

所以为什么这样就可以推出是正定核呢？我们根据Prop 7.3，试着把$k(x,x')=g(x-x')$写成内积的形式

我们先考虑一个傅里叶变换的形式：
```math
k(x,x')=g(x-x')\\=\frac1{(2\pi)^d}\int_{\mathbb R^d}\widehat{g}(\omega)e^{i\omega^\top(x-x')}d\omega \\=\frac1{(2\pi)^d}\int_{\mathbb R^d}\sqrt{\widehat{g}(\omega)}e^{i\omega^\top x}(\sqrt{\widehat{g}(\omega)}e^{i\omega^\top x'})^*d\omega\\=\langle\phi_{\omega}(x),\phi_{\omega}(x')\rangle_{\mathcal{H}}
```
由非负谱密度得到复值特征

```math
\phi_\omega(x)=(2\pi)^{-d/2}\sqrt{\widehat g(\omega)}e^{i\omega^\top x},
\qquad
k(x,x')=\int\phi_\omega(x)\overline{\phi_\omega(x')}\,d\omega.
```

所以指标$\omega$不可数怎么办？这里应理解为 $L^2$ 型函数空间，而非有限维特征数组；不能仅凭形式积分就宣称完成了再生性质的证明。

如果给定一个$\mathcal{H}$上的一个元素$f=f(x)=\int\phi_\omega(x)\theta_\omega\,d\omega$，这是$\omega$可数对应的求和进行的拓展

则形式上：

```math
\theta_\omega=(2\pi)^{-d/2}\frac{\widehat f(\omega)}{\sqrt{\widehat g(\omega)}},
\qquad
\|f\|_{\mathcal H}^2:=\|\theta\|_{L_2(\omega)}^2
=\frac1{(2\pi)^d}\int\frac{|\widehat f(\omega)|^2}{\widehat g(\omega)}\,d\omega.
```

但是我们还需要验证这样的定义范数操作，可以保证这还是一个RKHS，

保持再生核性质$\langle f,k(\cdot,x)\rangle_{\mathcal{H}}=f(x)$

固定 $x$，令 $k_x(t)=k(t,x)=q(t-x)$。对变量 $t$ 做 Fourier 变换：

```math
\widehat{k_x}(\omega) =e^{-i\omega^\top x}\widehat q(\omega).
```

于是

```math
\begin{aligned} \langle f,k_x\rangle_{\mathcal H} &=\frac1{(2\pi)^d} \int \frac{\widehat f(\omega) \overline{e^{-i\omega^\top x}\widehat q(\omega)}} {\widehat q(\omega)}\,d\omega\\ &=\frac1{(2\pi)^d} \int\widehat f(\omega)e^{i\omega^\top x}\,d\omega\\ &=f(x). \end{aligned}
```

**分母中的 $\widehat q$ 正好抵消核带来的 $\widehat q$，剩下 Fourier 反演，取出了 $f(x)$。** 这就是这套范数与核相匹配的关键。



#### Fourier 范数与 Sobolev 空间

来源：原稿第 1 页；教材印刷页 192–193，式 (7.4)–(7.5)。

平移不变核 $k(x,x')=q(x-x')$ 对应的平方范数为

```math
\|f\|_{\mathcal H}^2
=\frac1{(2\pi)^d}\int_{\mathbb R^d}
\frac{|\widehat f(\omega)|^2}{\widehat q(\omega)}\,d\omega.
```

原稿从一阶 Sobolev 范数出发，将函数与导数的平方积分联系到 Fourier 权重。统一维度后写作

```math
\int_{\mathbb R^d}(|f(x)|^2+\|\nabla f(x)\|_2^2)\,dx
=\frac1{(2\pi)^d}\int_{\mathbb R^d}
(1+\|\omega\|_2^2)|\widehat f(\omega)|^2\,d\omega.
```

因此 $\widehat q(\omega)=(1+\|\omega\|_2^2)^{-1}$ 给出这一范数的候选谱权重。不过要成为这里的有限值核，还须满足谱密度可积；一阶情形只适用于 $d=1$。原稿开头将此直接连到一般维度的指数核，需与后面的一般指数核公式区分。

##### 指数核

对 $q(x-x')=\exp(-\|x-x'\|_2/r)$，$r>0$，有

```math
\widehat q(\omega)
=\frac{2^d\pi^{(d-1)/2}\Gamma((d+1)/2)\,r^d}
{(1+r^2\|\omega\|_2^2)^{(d+1)/2}}.
```

其倒数给出的 Sobolev 阶数为 $(d+1)/2$：$d$ 为奇数时是整数阶，$d$ 为偶数时是分数阶。原稿的这一关系已写出。

当 $d=1$ 时，原稿继续得到

```math
\widehat q(\omega)=\frac{2r}{1+r^2\omega^2},
\qquad
\|f\|_{\mathcal H}^2
=\frac1{2r}\int_{\mathbb R}|f(x)|^2\,dx
+\frac r2\int_{\mathbb R}|f'(x)|^2\,dx.
```

##### Gaussian 核与 Matérn 核

Gaussian 核及其 Fourier 变换为

```math
q(x-x')=e^{-\|x-x'\|_2^2/r^2},
\qquad
\widehat q(\omega)=(\pi r^2)^{d/2}e^{-r^2\|\omega\|_2^2/4}.
```

所以

```math
\|f\|_{\mathcal H}^2
=\frac{(\pi r^2)^{-d/2}}{(2\pi)^d}
\int_{\mathbb R^d}e^{r^2\|\omega\|_2^2/4}|\widehat f(\omega)|^2\,d\omega.
```

原稿概括为“对应各阶导数”，并提出有限阶 Sobolev 空间的比较问题。这里保留概念记录，不补写指数权重展开的证明。原稿范数式中的 Gaussian 常数遗漏了负指数，已按其前一行的 $\widehat q$ 修正。

原稿还记录：$H^0=L^2$ 不是这里的 RKHS；$s=1$ 只有在 $d=1$ 时满足条件。教材对应的 Matérn 谱密度为 $\widehat q(\omega)\propto r^d(1+r^2\|\omega\|_2^2)^{-s}$，条件是 $s>d/2$。原稿列出的核例子如下，令 $\rho=\|x-x'\|_2/r$：

```math
\begin{aligned}
s&=(d+1)/2: & k(x,x')&=e^{-\rho},\\
s&=(d+3)/2: & k(x,x')&\propto(1+\sqrt3\rho)e^{-\sqrt3\rho},\\
s&=(d+5)/2: & k(x,x')&\propto(1+\sqrt5\rho+5\rho^2/3)e^{-\sqrt5\rho}.
\end{aligned}
```

这些例子采用教材各自的带宽参数化。原稿末尾记录：这里讨论的核对应的 $\mathcal H$ 在 $L^2(\mathbb R^d)$ 中稠密；未写证明。

##### $L^2$ 中点值不连续：原稿的尖峰例子

原稿取 $x_0=1/2$，构造

```math
f_n(t)=\max\{1-n|t-x_0|,0\}.
```

并写出

```math
\int_{\mathbb R}f_n(t)^2\,dt=\frac{2}{3n}\longrightarrow0,
\qquad f_n(x_0)=1.
```

假设点值能由某个固定 $k_{x_0}\in L^2$ 表示，原稿尝试用 Cauchy–Schwarz 得到矛盾。其末行将因子写成了 $\sqrt{3/(2n)}$；按前面的积分应为 $\sqrt{2/(3n)}$，两者都趋于零。原稿前面还写了“$\sup f_n\to\infty$”，但这个具体例子的峰值恒为 $1$；此处以明确写出的构造为准。

**状态：** 尖峰构造和矛盾思路已写；$L^2$ 等价类上的点值定义问题未展开，不能将这一页当作完整的函数空间构造证明。

## Ch7.4.1 表示定理与核岭回归计算

来源：《ch7.3.pdf》第 3 页；教材 §7.4.1。

对于目标

```math
\min_{f\in\mathcal H}\frac1n\sum_i\ell(y_i,f(x_i))+\frac\lambda2\|f\|_{\mathcal H}^2,
```

表示定理允许在 $f=\sum_i\alpha_i k(\cdot,x_i)$ 中寻找解，转成

```math
\min_{\alpha\in\mathbb R^n}\frac1n\sum_i\ell(y_i,(K\alpha)_i)+\frac\lambda2\alpha^\top K\alpha.
```

平方损失取 $\ell(y,z)=\frac12(y-z)^2$，目标和一阶条件为

```math
\frac1{2n}\|y-K\alpha\|_2^2+\frac\lambda2\alpha^\top K\alpha,
\qquad
\frac1nK(K\alpha-y)+\lambda K\alpha=0.
```

可取 $\alpha=(K+n\lambda I)^{-1}y$。如果把它视为一般的 $\alpha$ 优化问题，Hessian 含 $K(K+n\lambda I)/n$；当 $K$ 低秩或接近低秩时，参数化仍可能病态。实际求解应使用线性方程，不需要显式求逆。

> 原稿一阶条件漏写过 $\alpha$，并在另一页把 RKHS 正则项混写成 $\|K\alpha\|^2$。这里按同一个目标函数统一为 $\alpha^\top K\alpha$；不把相互矛盾的草式继续串接。

## Ch7.4.2 列采样 {#5-742}

选取 $I\subset V=\{1,\ldots,n\}$，$|I|=m\ll n$。$K(A,B)$ 表示选取 A 行、B 列。若 $K(I,I)$ 可逆，原稿使用

```math
\widetilde K=K(V,I)K(I,I)^{-1}K(I,V).
```

它只需所选列及其交叉子矩阵。列可随机选择；其特征来自已有训练输入。

### Exercise 7.8：原稿已有投影解释与分块草算 {#ex-7-8}

原稿：“将每个 $\phi(x_j)$，$j\notin I$，最优地近似为 $\phi(x_i)$，$i\in I$，的线性组合。”

令 $J=V\setminus I$，已有分块乘法整理为

```math
\begin{bmatrix}K(I,I)\\K(J,I)\end{bmatrix}
K(I,I)^{-1}
\begin{bmatrix}K(I,I)&K(I,J)\end{bmatrix}
=\begin{bmatrix}
K(I,I)&K(I,J)\\
K(J,I)&K(J,I)K(I,I)^{-1}K(I,J)
\end{bmatrix}.
```

> **原始完成状态：简写，未展开。** 原稿右下角裁切的矩阵项按同一乘法恢复；没有继续补最优投影的变分论证，也没有补不可逆情形。

## Ch7.4.3 随机特征 {#6-743}

来源：《7.4.3 Random Feature.pdf》第 1 页；教材印刷页 198。

若核有积分表示

```math
k(x,x')=\int_V\phi(x,v)\phi(x',v)\,d\tau(v),
```

其中 $\tau$ 为概率分布，则可独立抽样 $v_1,\ldots,v_m\sim\tau$，用经验平均近似：

```math
\widehat k(x,x')=\frac1m\sum_{j=1}^m\phi(x,v_j)\phi(x',v_j),
\qquad
\widehat\phi(x)=\frac1{\sqrt m}(\phi(x,v_1),\ldots,\phi(x,v_m))^\top.
```

原稿单样本损失式按其经验风险语境整理为

```math
\min_{\beta\in\mathbb R^m}\frac1n\sum_i\ell(y_i,\widehat\phi(x_i)^\top\beta)
+\frac\lambda2\|\beta\|_2^2.
```

原稿的两个例子是平移不变核的 Fourier 表示，以及随机权重神经元 $\phi(x,v)=\sigma(v^\top x)$。后者括号附近的“2 状”笔迹按教材对应例子判断为误辨，不保留为额外的平方。Fourier 指数也统一回本篇开头的约定。

### 平移不变核的谱采样

来源：原稿第 2 页；教材 §7.4.3，印刷页 198。原稿标题“Ch4.4.3”按正文校正为 §7.4.3。

对平移不变核，由

```math
k(x,x')=\frac1{(2\pi)^d}\int_{\mathbb R^d}
\widehat q(\omega)e^{i\omega^\top(x-x')}\,d\omega,
\qquad
q(0)=\frac1{(2\pi)^d}\int_{\mathbb R^d}\widehat q(\omega)\,d\omega,
```

将谱密度归一化。假设 $\widehat q\ge0$ 可积且 $q(0)>0$，令

```math
d\nu(\omega)=\frac{\widehat q(\omega)}{(2\pi)^dq(0)}\,d\omega,
\qquad
\phi(x,\omega)=\sqrt{q(0)}e^{i\omega^\top x}.
```

于是

```math
k(x,x')=\mathbb E_{\omega\sim\nu}
\left[\phi(x,\omega)\overline{\phi(x',\omega)}\right].
```

**状态：** 从谱积分到概率采样的推导已写。复值乘积所需的共轭与归一化条件在整理时明确标出；本页没有实值余弦特征的推导。

### Exercise 7.10：Mercer 核的随机特征 {#ex-7-10}

原稿明确标注 Ex7.10，并使用 Ex7.6 的表示

```math
k(x,x')=\sum_{i\in I}\lambda_i\phi_i(x)\phi_i(x').
```

记 $S=\sum_i\lambda_i$。按原稿的抽样权重，令

```math
\mathbb P(J=i)=\lambda_i/S,
\qquad
\psi_J(x)=\sqrt S\,\phi_J(x).
```

则其已写出的期望计算为

```math
\mathbb E[\psi_J(x)\psi_J(x')]
=\sum_i\frac{\lambda_i}{S}
(\sqrt S\phi_i(x))(\sqrt S\phi_i(x'))
=k(x,x').
```

原稿也画出了多个独立采样分量组成的向量 $(\psi_1(x),\ldots,\psi_m(x))$，但没有在该向量前写 $1/\sqrt m$，也没有明确写出向量内积的经验平均。这里仅将已经写出的单次随机特征及其期望整理完整。

**状态：** 已有抽样分布与期望恒等式，不再是“仅题意”。原稿的 $\psi_i=\phi_{J_i}$ 与后面的 $\sqrt S$ 不一致，按前后两处期望式补齐 $\sqrt S$；逐点收敛条件、有限维向量的归一化尚待核验。前述级数需在 $\sum_i\lambda_i|\phi_i(x)|^2<\infty$ 的点讨论，见本篇前面的 Ex7.6 条件记录。

## Ch7.4.4 对偶算法

来源：原稿第 3 页；教材 §7.4.4，印刷页 199，式 (7.9)。

原稿提出的问题是：$\theta$ 可能属于无限维空间，如何优化？先写

```math
\min_{\theta\in\mathcal H}
\frac1n\sum_i\ell(y_i,\langle\phi(x_i),\theta\rangle)
+\frac\lambda2\|\theta\|^2.
```

引入 $u_i=\langle\phi(x_i),\theta\rangle$，记 $\ell_i(u)=\ell(y_i,u)$，构造

```math
L(u,\theta,\alpha)
=\frac1n\sum_i\ell_i(u_i)+\frac\lambda2\|\theta\|^2
+\lambda\sum_i\alpha_i(u_i-\langle\phi(x_i),\theta\rangle),
\qquad
D(\alpha)=\inf_{u,\theta}L(u,\theta,\alpha).
```

原稿写出了原问题最小值与 $\sup_\alpha D(\alpha)$ 相等；这里需保留凸性与强对偶适用条件，不能把它当作任意损失下的恒等式。

对 $\theta$ 求导，原稿得到

```math
\lambda\theta-\lambda\sum_i\alpha_i\phi(x_i)=0,
\qquad \theta=\sum_i\alpha_i\phi(x_i).
```

代回后得到

```math
\max_{\alpha\in\mathbb R^n}D(\alpha),
\qquad
D(\alpha)
=\frac1n\sum_i\inf_{u_i}
\{\ell_i(u_i)+n\lambda\alpha_i u_i\}
-\frac\lambda2\alpha^\top K\alpha.
```

**状态：** 一般对偶目标与参数恢复关系已写。原稿最后一式的 $\lambda_i$ 统一为前文的正则参数 $\lambda$；未追加凸共轭推导或一般损失的求解算法。

### 平方损失的尝试与 Ex7.11 断点

来源：原稿第 4 页；教材印刷页 196、199–200。

原稿明确从**不带 $1/2$** 的平方损失开始：

```math
\ell_i(u_i)=(y_i-u_i)^2,
\qquad
u_i=y_i-\frac{n\lambda}{2}\alpha_i.
```

但下一行将内层最小值写成

```math
n\lambda\alpha_i y_i-\frac{n^2\lambda^2}{2}\alpha_i^2,
```

继而写出

```math
D(\alpha)=\lambda\alpha^\top y
-\frac{n\lambda^2}{2}\alpha^\top\alpha
-\frac\lambda2\alpha^\top K\alpha.
```

**系数问题：** 按本页开头的损失和 $u_i$，内层二次项系数应为 $n^2\lambda^2/4$；上面写出的 $1/2$ 属于另一种损失归一化。原稿在此混用了 $(y-u)^2$ 与教材 $\tfrac12(y-u)^2$，不能将这条推导直接标为正确。

原稿随后尝试将最大化改写成最小化，写出了含 $K+n\lambda I$ 的目标，但仍将它记为“$\min D$”；应区分 $D$ 与 $-D$。其下一行又写成 $\alpha=(K+\lambda I)^{-1}y$，与上一行缺少一个 $n$，并注明“引入梯度下降即可”。这些不一致保留为待修订项，不在本次导入中替换成完整正确解答。

### Exercise 7.11 {#ex-7-11}

原稿明确标注 Ex7.11 (a)，再次写下

```math
\min_\alpha\frac\lambda2\alpha^\top(K+n\lambda I)\alpha
-\lambda\alpha^\top y,
```

然后写“条件数：由于 $K$”并停止。

**状态：** (a) 有对偶目标草稿，条件数计算与原问题比较未写；(b) 正规方程及矩阵求逆引理的比较未写。这里的目标对应教材带 $1/2$ 的平方损失；不将前面的混合归一化推导视为其证明，也不把此前对话中的解答算作本次手写作答。


下一篇：[Ch7.5 泛化保证与逼近误差](ch7.5-generalization.md)。
