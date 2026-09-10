# Ch7.3–7.4 核的表示、列采样与随机特征

> 状态：`note_unverified`。由《ch7.3.pdf》3 页、《7.4.3 Random Feature.pdf》第 1、8 页，以及 2026-09-09《Ch7.2-7.3.pdf》的第 6–7 页整理。对应 §7.3.1–§7.3.3、§7.4.1–§7.4.3，并保留原稿 §7.6.1 的线性估计器视角。来源见 [2026-09-08 导入记录](handwritten-import-20260908.md)与 [2026-09-10 导入记录](handwritten-import-20260910.md)。

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
$$
k(x,x')=g(x-x')\\=\frac1{(2\pi)^d}\int_{\mathbb R^d}\widehat{g}(\omega)e^{i\omega^\top(x-x')}d\omega \\=\frac1{(2\pi)^d}\int_{\mathbb R^d}\sqrt{\widehat{g}(\omega)}e^{i\omega^\top x}(\sqrt{\widehat{g}(\omega)}e^{i\omega^\top x'})^*d\omega\\=\langle\phi_{\omega}(x),\phi_{\omega}(x')\rangle_{\mathcal{H}}
$$
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
\|f\|_{\mathcal H}^2:=\|\theta\|_{L_2(\omega)}
=\frac1{(2\pi)^d}\int\frac{|\widehat f(\omega)|^2}{\widehat g(\omega)}\,d\omega.
```

但是我们还需要验证这样的定义范数操作，可以保证这还是一个RKHS，

保持再生核性质$\langle f,k(\cdot,x)\rangle_{\mathcal{H}}=f(x)$

固定 \(x\)，令 \(k_x(t)=k(t,x)=q(t-x)\)。对变量 \(t\) 做 Fourier 变换：

\[ \widehat{k_x}(\omega) =e^{-i\omega^\top x}\widehat q(\omega). \]

于是

\[ \begin{aligned} \langle f,k_x\rangle_{\mathcal H} &=\frac1{(2\pi)^d} \int \frac{\widehat f(\omega) \overline{e^{-i\omega^\top x}\widehat q(\omega)}} {\widehat q(\omega)}\,d\omega\\ &=\frac1{(2\pi)^d} \int\widehat f(\omega)e^{i\omega^\top x}\,d\omega\\ &=f(x). \end{aligned} \]

**分母中的 \(\widehat q\) 正好抵消核带来的 \(\widehat q\)，剩下 Fourier 反演，取出了 \(f(x)\)。** 这就是这套范数与核相匹配的关键。



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

## 5. 列采样（§7.4.2）

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

## 6. 随机特征（§7.4.3）

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

### Exercise 7.10：仅标题 {#ex-7-10}

原稿仅写：

> Ex 7.10 Mercer 核随机展开

题干、展开式与解答均未写，本次不补。

## 7. 与局部平均方法的联系（原稿 §7.6.1）

来源：《7.4.3 Random Feature.pdf》第 8 页。

令 $k_x=(k(x,x_1),\ldots,k(x,x_n))^\top$，核岭回归可写成

```math
\widehat f_\lambda(x)=k_x^\top(K+n\lambda I)^{-1}y
=\sum_i\widehat w_i(x)y_i,
\qquad
\widehat w(x)=(K+n\lambda I)^{-1}k_x.
```

训练点上的拟合矩阵为 $H_\lambda=K(K+n\lambda I)^{-1}$。这里始终保留 $n\lambda$，原稿在同页混用的 $\lambda$ 不再作为另一套未声明的尺度。

核岭回归也对标签线性，但其权重可以为负，且不一定和为 1。这使它与 Ch6 的非负局部平均不同。

原稿讨论无正则项可能带来的问题，最后停在“exp”，没有写出例子；这里保留为“例子未写”，不补一个反例。

下一篇：[Ch7.5 泛化保证与逼近误差](ch7.5-generalization.md)。
