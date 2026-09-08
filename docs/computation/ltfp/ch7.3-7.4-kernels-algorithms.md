# Ch7.3–7.4 核的表示、列采样与随机特征

> 状态：`note_unverified`。由《ch7.3.pdf》3 页及《7.4.3 Random Feature.pdf》第 1、8 页整理。对应 §7.3.1、§7.3.3、§7.4.1–7.4.3，并保留原稿 §7.6.1 的线性估计器视角。来源见[导入记录](handwritten-import-20260908.md)。

本篇只覆盖上述小节，不表示 §7.3–7.4 全部已有笔记。

## 1. 多项式核与特征维数

来源：《ch7.3.pdf》第 2 页；教材印刷页 186–187。

### 1.1 齐次核

对正整数 $s$，

```math
k(x,x')=(x^\top x')^s
=\sum_{\alpha_1+\cdots+\alpha_d=s}
\frac{s!}{\alpha_1!\cdots\alpha_d!}
\prod_{j=1}^d(x_jx_j')^{\alpha_j}.
```

每个多重指标 $\alpha\in\mathbb N^d$ 对应一个单项式特征，系数可拆到两边的平方根中。这些特征张成 $s$ 次齐次多项式空间；原稿记录的维数为

```math
\binom{d+s-1}{s}.
```

原稿以“把 $s$ 分成 $d$ 份”解释计数，并尝试归纳。$d=1$ 时只有一个单项式，原稿难辨的“0/1”据此整理为 1；中间组合数求和没有写成完整证明，不在这里补写。

### 1.2 非齐次核：归纳未完成

已有展开为

```math
k(x,x')=(1+x^\top x')^s
=\sum_{k=0}^s\binom sk(x^\top x')^k.
```

对应多重指标条件 $\sum_i\alpha_i\le s$。原稿记录 $d=1$ 时共有 $s+1$ 个特征，然后写“归纳法证明”“d=k”“d=k+1”，在此停止。

> **原始完成状态：未完成。** 不新增最终组合数公式或归纳步骤；保留原稿尚未收尾的计数讨论。

## 2. 平移不变核与 Fourier 变换

来源：《ch7.3.pdf》第 1 页；教材 §7.3.3，印刷页 191–192。

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

### Proposition 7.4：Bochner 定理

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

反方向原稿只记“正定函数 → 正定分布 → Fourier 变换是正测度”的路线，未展开证明，仍保留为简写。

当 $g,\widehat g$ 均可积时，原稿记录的判据为 $\widehat g(\omega)\ge0$。

## 3. Fourier 特征与 RKHS 范数

由非负谱密度得到复值特征

```math
\phi_\omega(x)=(2\pi)^{-d/2}\sqrt{\widehat g(\omega)}e^{i\omega^\top x},
\qquad
k(x,x')=\int\phi_\omega(x)\overline{\phi_\omega(x')}\,d\omega.
```

若按原稿的积分配对写 $f(x)=\int\phi_\omega(x)\theta_\omega\,d\omega$，则形式上

```math
\theta_\omega=(2\pi)^{-d/2}\frac{\widehat f(\omega)}{\sqrt{\widehat g(\omega)}},
\qquad
\|f\|_{\mathcal H}^2
=\frac1{(2\pi)^d}\int\frac{|\widehat f(\omega)|^2}{\widehat g(\omega)}\,d\omega.
```

原稿的“指标 $\omega$ 不可数”意在提醒，这里应理解为 $L^2$ 型函数空间，而非有限维特征数组；不能仅凭形式积分就宣称完成了再生性质的证明。涉及 $\widehat g=0$ 的地方应限制在谱支撑上并满足有限范数条件；原稿没有展开这些分析细节。

## 4. 表示定理与核岭回归计算

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
