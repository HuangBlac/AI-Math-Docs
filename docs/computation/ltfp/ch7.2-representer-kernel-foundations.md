# Ch7.2–7.3 表示定理、核构造与 Mercer 特征

这份笔记围绕一个问题展开：如果特征可以无限多，如何仍然用有限个参数学习？表示定理把优化限制到训练特征张成的空间；核函数提供所需内积；RKHS 则把函数、特征与范数联系起来。

> 状态：`note_unverified`。由 2026-09-09 提供的《Ch7.2-7.3.pdf》7 页整理，2026-09-10 导入。覆盖 §7.2、§7.3 核基础、§7.3.2 的 Fourier 特征起步，以及 Ex 7.1、7.2、7.6。难辨语句据上下文和锁定教材整理；原稿停止的证明和有问题的习题尝试均保留原状。见[本次来源与状态记录](handwritten-import-20260910.md)。

## 1. 从局部平均到核模型

来源：原稿第 1 页。

Nadaraya–Watson 估计是标签的非负加权平均：

```math
\widehat f(x)=\sum_i\widehat w_i(x)y_i,
\qquad
\widehat w_i(x)=\frac{q_h(x-x_i)}{\sum_jq_h(x-x_j)}.
```

其分母为零时的约定和一致性条件见[Ch6 笔记](ch6.1-6.3-local-averaging.md)。原稿回顾的 $O(n^{-2/(d+2)})$ 是相应假设下的风险量级，不能脱离带宽、噪声和正则性条件单独使用。

核模型则先构造 Gram 矩阵 $K_{ij}=k(x_i,x_j)$，再确定展开系数。原稿先以可逆 K 的无正则插值为例：

```math
k_x=(k(x,x_1),\ldots,k(x,x_n))^\top,
\qquad\widehat f(x)=k_x^\top K^{-1}y.
```

这里并不是说所有核学习都使用 $K^{-1}y$。其一般形式是 $\widehat f(x)=\sum_i\alpha_i k(x,x_i)$，系数由损失、正则化或插值条件确定。

## 2. 无限维特征与经验目标

来源：原稿第 1–2 页。

有限维线性模型 $f_\theta(x)=\theta^\top\phi(x)$ 可以推广到 Hilbert 空间：

```math
\phi:\mathcal X\to\mathcal H,
\qquad f_\theta(x)=\langle\theta,\phi(x)\rangle_{\mathcal H}.
```

例如参数可在 $\ell^2$ 中：$\theta=(\theta_1,\theta_2,\ldots)$ 且 $\sum_i|\theta_i|^2<\infty$。真正需要的是 Hilbert 空间结构，而非把所有无限维对象都等同于同一种序列空间。

本文统一采用目标

```math
J_\lambda(\theta)=\frac1n\sum_{i=1}^n
\ell(y_i,\langle\theta,\phi(x_i)\rangle)
+\frac\lambda2\|\theta\|_{\mathcal H}^2,\qquad\lambda>0.
```

原稿曾交替写 λ 和 λ/2，现统一尺度。该目标只通过 n 个训练预测和参数范数访问 θ，这正是表示定理利用的结构。

## 3. Proposition 7.1：表示定理 {#prop-7-1}

来源：原稿第 2–3 页；教材印刷页 181–182（PDF 第 197–198 页）。

考虑

```math
J(\theta)=\Psi\bigl(\langle\theta,\phi(x_1)\rangle,\ldots,
\langle\theta,\phi(x_n)\rangle,\|\theta\|_{\mathcal H}^2\bigr),
```

其中 Ψ 关于最后一个变量严格递增。令

```math
D=\operatorname{span}\{\phi(x_1),\ldots,\phi(x_n)\}.
```

原稿已有的证明整理如下。D 是有限维闭子空间，可以正交分解

```math
\theta=\theta_D+\theta_\perp,\qquad\theta_D\in D,\quad\theta_\perp\in D^\perp.
```

对所有训练输入，

```math
\langle\theta,\phi(x_i)\rangle=\langle\theta_D,\phi(x_i)\rangle,
\qquad\|\theta\|^2=\|\theta_D\|^2+\|\theta_\perp\|^2.
```

于是 $J(\theta_D)\le J(\theta)$，当 $\theta_\perp\ne0$ 时严格变小。去掉正交分量不改变训练预测，却降低范数代价。因此

```math
\inf_{\theta\in\mathcal H}J(\theta)=\inf_{\theta\in D}J(\theta).
```

若极小值存在，最优 θ 必在 D 中，可写为 $\theta=\sum_i\alpha_i\phi(x_i)$。

> **表述校对。** 原稿“在线性组合中取得极小值”整理为下确界相同；极小值的存在性不是表示定理自动保证的。“只有正交分量为零才最优”对应严格递增条件。

### 有限维目标与核技巧

原稿接着代入展开式：

```math
f_\theta(x)=\sum_i\alpha_i\langle\phi(x_i),\phi(x)\rangle
=\sum_i\alpha_i k(x,x_i),
\qquad\|\theta\|_{\mathcal H}^2=\alpha^\top K\alpha.
```

所以学习问题变为

```math
\inf_{\alpha\in\mathbb R^n}\frac1n\sum_i\ell(y_i,(K\alpha)_i)
+\frac\lambda2\alpha^\top K\alpha.
```

算法可以只使用核值，不需要显式列出所有特征。进一步的求解与近似方法见[§7.4 笔记](ch7.3-7.4-kernels-algorithms.md)。

## 4. Proposition 7.2：最小范数插值 {#prop-7-2}

来源：原稿第 3 页；教材印刷页 183。

假设至少存在一个 θ 满足 $y_i=\langle\theta,\phi(x_i)\rangle$。同样分解为 $\theta_D+\theta_\perp$：插值条件只依赖 $\theta_D$，而范数平方是两部分范数平方之和。因此最小范数插值者可以取在 D 中，其系数满足

```math
K\alpha=y.
```

原稿讨论了表示系数可能不唯一。这里不把“存在插值解”偷换成“K 必须可逆”：可逆时可写 $\alpha=K^{-1}y$，一般情形只保留线性方程。若 $K\alpha=y$ 无解，则不存在满足这些标签的插值参数。

## 5. 正定核与 Proposition 7.3 {#prop-7-3}

来源：原稿第 4–5 页；教材印刷页 183–185。

实值对称核 k 称为正定核，是指对任意有限点集，其 Gram 矩阵均半正定：

```math
\forall\alpha\in\mathbb R^n,\qquad
\sum_{i,j}\alpha_i\alpha_j k(x_i,x_j)\ge0.
```

这里“正定核”采用教材术语，不要求每一个 Gram 矩阵都严格正定。

Proposition 7.3 将它与特征表示联系起来：存在 Hilbert 空间 H 和映射 φ，使 $k(x,x')=\langle\phi(x),\phi(x')\rangle$。

### 原稿已展开的一个方向

若已有特征表示，则

```math
\alpha^\top K\alpha
=\left\langle\sum_i\alpha_i\phi(x_i),\sum_j\alpha_j\phi(x_j)\right\rangle
=\left\|\sum_i\alpha_i\phi(x_i)\right\|^2\ge0.
```

### 反向构造写到哪里

原稿先取核截面的有限线性组合

```math
\mathcal H'=\left\{\sum_{i=1}^n\alpha_i k(\cdot,x_i):n<\infty\right\},
```

并定义候选内积

```math
\left\langle\sum_i\alpha_i k(\cdot,x_i),
\sum_j\beta_j k(\cdot,x_j')\right\rangle
=\sum_{i,j}\alpha_i\beta_j k(x_i,x_j').
```

随后记下再生关系

```math
\langle k(\cdot,x),k(\cdot,x')\rangle=k(x,x'),
\qquad\langle k(\cdot,x),f\rangle=f(x).
```

原稿第 5 页页首问：

> 但这样定义的一个内积会对应一个完备的 RKHS 吗？

**原始状态：反向证明未完成。** 候选内积的良定义、零范数条件与完备化步骤均未展开。此处不将 H′ 直接当成已证明完备的 H，也不补写完备化论证。

## 6. Exercise 7.1：有界求值与 Riesz 表示 {#ex-7-1}

来源：原稿第 5 页。题目假设 H 是 X 上实值函数的 Hilbert 空间，且每个求值泛函 $L_x(f)=f(x)$ 有界。

原稿通过表示向量 $g_x$ 写出

```math
f(x)=L_x(f)=\langle f,g_x\rangle_{\mathcal H}.
```

这里调用的是 Riesz 表示定理。原稿令 $k(\cdot,x)=g_x$，并记录

```math
\langle k(\cdot,x),k(\cdot,x')\rangle=k(x',x),
```

最后得出“这是一个 RKHS”。

**原始状态：已有简短作答。** 表示向量和再生关系已写；整理时说明所用定理，不另扩充成一篇证明。

## 7. Exercise 7.2：保留有问题的推导 {#ex-7-2}

来源：原稿第 5 页。目标是证明逐点指数 $k_{\exp}(x,x')=e^{k(x,x')}$ 仍为正定核；这不是矩阵指数 $e^K$。

原稿尝试利用 $e^t\ge1+t$：

```math
\sum_{i,j}\alpha_i\alpha_j e^{k(x_i,x_j)}
\mathrel{\overset{?}{\ge}}
\sum_{i,j}\alpha_i\alpha_j(1+k(x_i,x_j))
=\left(\sum_i\alpha_i\right)^2+\alpha^\top K\alpha\ge0.
```

**原始状态：已有作答尝试，关键一步不成立。** 问号处是整理时标出的断点：$\alpha_i\alpha_j$ 可能为负，不能由逐点不等式直接得到加权总和的不等式。保留已有尝试，不补写正确证明。



## 仍保留的空白

| 对象 | 本次笔记实际写到的程度 |
|---|---|
| §7.2 / P7.1 | 有问题设置、正交分解证明主线与有限维目标 |
| P7.2 | 有最小范数插值与 $K\alpha=y$ 的推导 |
| P7.3 | 正向写出；反向停在候选内积、再生关系及完备性问题 |
| Ex 7.1 | 有 Riesz 表示与再生关系的简短作答 |
| Ex 7.2 | 有尝试，但加权不等式一步错误，未改写成正确答案 |

因此，这批材料把此前 Ch7.2 与 Mercer 特征的笔记缺口向前推进了一步；它不自动意味着整个 Ch7.3 已覆盖，也不改变人工签认或掌握状态。
