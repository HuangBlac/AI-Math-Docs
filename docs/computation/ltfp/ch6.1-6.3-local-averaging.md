# Ch6.1–6.3 局部平均方法与一致性分析

局部平均方法把训练标签加权组合成预测。分割估计、近邻和 Nadaraya–Watson 核回归使用不同的权重，但它们的误差都可以拆成两部分：邻域过大引起的偏差，以及有效样本过少引起的方差。

> 状态：`note_unverified`。由《Ch6局部平均值算法.pdf》第 1–19 页整理，重复页合并，符号按锁定教材 §6.1–6.3 统一。正文中的明显抄写错误已整理；习题保留原有作答程度，不补写未完成部分。来源与校对范围见[导入记录](handwritten-import-20260908.md)。

## 1. 预测器与条件分布

设 $(x_i,y_i)_{i=1}^n$ 独立同分布，输入边缘分布记为 $P_X$。平方损失下的目标函数是

```math
f_*(x)=\mathbb E[Y\mid X=x],
\qquad
R(f)-R(f_*)=\|f-f_*\|_{L^2(P_X)}^2.
```

一般损失下，最优预测由条件分布决定：

```math
f_*(x)\in\arg\min_z\int\ell(y,z)\,dP(y\mid x).
```

用样本构造条件分布的估计

```math
\widehat P(dy\mid x)=\sum_{i=1}^n\widehat w_i(x)\delta_{y_i}(dy),
\qquad \widehat w_i(x)\ge0,
\qquad \sum_{i=1}^n\widehat w_i(x)=1.
```

这里 $\delta_{y_i}$ 是集中在标签 $y_i$ 上的点质量。平方损失给出

```math
\widehat f(x)=\sum_{i=1}^n\widehat w_i(x)y_i.
```

“线性估计器”指它对标签向量 $y$ 线性；权重依赖输入，因此预测对 $x$ 通常非线性。以下权重只依赖训练输入和测试点，不依赖训练标签。

### 原稿中的分类与 logistic 损失回顾

0–1 损失下，预测条件概率最大的类别。样本加权版本为

```math
\widehat c(x)\in\arg\max_{a\in\mathcal Y}
\sum_{i=1}^n\widehat w_i(x)\mathbf1_{\{y_i=a\}}.
```

对于 $Y\in\{-1,1\}$，设 $\eta=P(Y=1\mid X=x)$，$0<\eta<1$。logistic 条件风险为

```math
L_x(z)=\eta\log(1+e^{-z})+(1-\eta)\log(1+e^z).
```

原稿第 2–3 页求导的有效步骤整理为

```math
L_x'(z)=\frac{(1-\eta)e^z-\eta}{1+e^z}=0,
\qquad e^z=\frac\eta{1-\eta},
\qquad z=\log\frac\eta{1-\eta}.
```

原稿把最小风险与最优函数都写成过 $R^*$；这里分别使用风险值 $R(f_*)$ 和函数 $f_*$，删除未成立的对数草算等号。

## 2. 三种权重

### 2.1 分割估计器（§6.2.2）

将输入空间分成互不重叠的单元 $\mathcal X=\bigcup_{j\in J}A_j$，令 $A(x)$ 为包含 $x$ 的单元，$N_A=\sum_i\mathbf1_{\{x_i\in A\}}$。非空单元内

```math
\widehat w_i(x)=\frac{\mathbf1_{\{x_i\in A(x)\}}}{N_{A(x)}},
\qquad
\widehat f(x)=\frac1{N_{A(x)}}\sum_{x_i\in A(x)}y_i.
```

空单元时取所有训练标签的平均，即 $\widehat w_i(x)=1/n$。这一约定已出现在原稿第 10 页的方差计算中；第 4 页未完成的“加号尾项”不另造一项。

非空单元的示性函数 $\mathbf1_{\{x\in A_j\}}$ 可作为特征，预测在各单元内为常数。按单元重排训练点后，拟合矩阵 $H_{ij}=\widehat w_j(x_i)$ 是块对角矩阵，每一块为

```math
H_j=\frac1{N_{A_j}}\mathbf1_{N_{A_j}}\mathbf1_{N_{A_j}}^\top.
```

### 2.2 k 近邻（§6.2.3）

按距离排序：

```math
\Delta(x_{i_1(x)},x)\le\cdots\le\Delta(x_{i_n(x)},x),
\qquad
\widehat w_i(x)=\frac1k\mathbf1_{\{i\in\{i_1(x),\ldots,i_k(x)\}\}}.
```

距离相同采用固定规则打破平局。训练输入互异、最近邻包含自身时，$k=1$ 给出 $H=I$；$k=n$ 时 $H=\mathbf1\mathbf1^\top/n$。

### 2.3 Nadaraya–Watson 核回归（§6.2.4）

令 $q\ge0$ 且 $\int q=1$，定义带宽为 $h$ 的平滑核

```math
q_h(u)=h^{-d}q(u/h),
\qquad
\widehat w_i(x)=\frac{q_h(x-x_i)}{\sum_{j=1}^nq_h(x-x_j)}.
```

分母为零时同样采用全样本平均。常见形状为 $q(u)\propto\mathbf1_{\{\|u\|\le1\}}$ 或 $q(u)\propto e^{-\|u\|_2^2/2}$。原稿第 1 页指数权重分子、分母的范数次幂不一致，这里统一使用同一个 $q_h$。

此处的核用于局部加权；[Ch7 的正定核](ch7.3-7.4-kernels-algorithms.md)用于定义特征内积，两种要求不同。

## 3. 统一的偏差—方差分解

假设

```math
\mathbb E[(Y-f_*(X))^2\mid X]\le\sigma^2,
\qquad
|f_*(x)-f_*(x')|\le B\Delta(x,x').
```

给定训练输入，误差可写为

```math
\widehat f(x)-f_*(x)
=\sum_i\widehat w_i(x)[y_i-f_*(x_i)]
+\sum_i\widehat w_i(x)[f_*(x_i)-f_*(x)].
```

第一项条件均值为零，第二项在给定输入后确定。因此

```math
\begin{aligned}
\mathbb E[(\widehat f(x)-f_*(x))^2\mid x_1,\ldots,x_n]
&=\left(\sum_i\widehat w_i(x)[f_*(x_i)-f_*(x)]\right)^2\\
&\quad+\sum_i\widehat w_i(x)^2\operatorname{Var}(Y_i\mid x_i)\\
&\le B^2\sum_i\widehat w_i(x)\Delta(x_i,x)^2
+\sigma^2\sum_i\widehat w_i(x)^2.
\end{aligned}
```

最后一步用权重非负、和为 1，以及 Jensen 不等式。这里的“偏差项”已经是平方偏差。

记

```math
D_n=\int\mathbb E\sum_i\widehat w_i(x)\Delta(x_i,x)^2\,dP_X(x),
\qquad
V_n=\int\mathbb E\sum_i\widehat w_i(x)^2\,dP_X(x).
```

则总体均方误差 $\mathcal E_n\le B^2D_n+\sigma^2V_n$。$D_n$ 衡量参与平均的样本距离有多远；$V_n$ 衡量权重集中程度。逐点恒等式

```math
\sum_i\widehat w_i(x)^2
=\frac1n+\sum_i\left(\widehat w_i(x)-\frac1n\right)^2
```

整理了原稿第 8 页对“偏离均匀权重”的说明。

### Exercise 6.2：原稿只有简写 {#ex-6-2}

原稿第 9 页写“$f_*(x)=E[Y\mid X]$，考虑二分类问题”，然后将分类超额风险界为回归误差的 $L^1$ 范数，再界为 $L^2$ 范数，最后代入 $(B^2D_n+\sigma^2V_n)^{1/2}$。

原稿没有明确分类决策函数、标签编码和损失条件，且 $f^*,f_*$ 混用。这里保留这条解题路线，不把缺失条件和分类校准步骤补成完整答案。

## 4. 固定分割：Proposition 6.1

来源：原稿第 9–10 页；教材印刷页 165–168（PDF 第 181–184 页）。在上述假设及空单元约定下，

```math
\mathcal E_n\le
\left(\frac{B^2}{2}\operatorname{diam}(\mathcal X)^2+8\sigma^2\right)\frac{|J|}{n}
+B^2\max_{j\in J}\operatorname{diam}(A_j)^2.
```

### 原稿已有的证明框架

单元内的平方权重和是

```math
\sum_i\widehat w_i(x)^2
=\frac{\mathbf1_{\{N_A>0\}}}{N_A}+\frac1n\mathbf1_{\{N_A=0\}}.
```

以 $p_A=P_X(A)$ 记单元概率。把非空事件按 $N_A\le np_A/2$ 和 $N_A>np_A/2$ 拆开，加上空单元事件。原稿对三部分分别记下 $5/(np_A)$、$2/(np_A)$、$1/(np_A)$ 的粗界；乘 $p_A$ 并对单元求和，得到 $V_n\le8|J|/n$。

偏差方面，非空单元内距离至多为 $\operatorname{diam}(A)$，空单元时至多为 $\operatorname{diam}(\mathcal X)$。原稿最终得到

```math
D_n\le\max_j\operatorname{diam}(A_j)^2
+\frac{|J|}{2n}\operatorname{diam}(\mathcal X)^2.
```

> 原稿未展开三部分概率界的完整常数推导，保留为证明框架。

规则网格尺度为 $h$ 时，$|J|\asymp h^{-d}$、单元直径为 $O(h)$，因此误差量级为 $1/(nh^d)+B^2h^2$。平衡两项得到 $h\asymp n^{-1/(d+2)}$，均方误差为 $O(n^{-2/(d+2)})$。

## 5. k 近邻的距离界

来源：原稿第 11–12 页；教材印刷页 168–170。

### Lemma 6.1：最近邻距离

设输入分布的支撑 $\mathcal X\subset\mathbb R^d$ 紧，距离取 $\ell_\infty$，$D=\operatorname{diam}(\mathcal X)$。对于 $n+1$ 个独立样本，最后一点到其最近邻的平方距离满足

```math
\mathbb E\Delta(X_{n+1},X_{(n+1)})^2
\le\begin{cases}4D^2n^{-2/d},&d\ge2,\\2D^2/n,&d=1.\end{cases}
```

原稿的证明从交换性出发。记 $R_i=\|x_i-x_{(i)}\|_\infty$，把单个测试点的期望换成 $n+1$ 点的平均。半径 $R_i/2$ 的开球两两不交，它们的总体积不超过 $(2D)^d$，故

```math
\sum_{i=1}^{n+1}R_i^d\le(2D)^d.
```

$d\ge2$ 时，Jensen 不等式给出

```math
\left(\frac1{n+1}\sum_iR_i^2\right)^{d/2}
\le\frac1{n+1}\sum_iR_i^d
\le\frac{(2D)^d}{n+1}.
```

$d=1$ 时，由 $R_i\le D$ 和 $\sum_iR_i\le2D$ 得平均平方距离不超过 $2D^2/(n+1)$。原稿未讨论重合点及零半径的细节。

### Lemma 6.2：第 k 近邻距离

原稿只记录结论，没有单独证明：

```math
\mathbb E\Delta(X_{n+1},X_{i_k(X_{n+1})})^2
\le\begin{cases}8D^2(2k/n)^{2/d},&d\ge2,\\8D^2k/n,&d=1.\end{cases}
```

由于 $\sum_i\widehat w_i^2=1/k$，在 $d\ge2$ 时得到

```math
\mathcal E_n\le\frac{\sigma^2}{k}+8B^2D^2(2k/n)^{2/d}.
```

取 $k\asymp n^{2/(d+2)}$，两项都为 $O(n^{-2/(d+2)})$。该推导使用 $\ell_\infty$ 距离；换成其他范数时需相应保留范数等价常数。

### Exercise 6.3：原稿已有简短作答 {#ex-6-3}

原文题意：“证明 Bayes 风险为 0，1 近邻是一致。”

原稿令 $\sigma=0$，用 $B^2$ 乘最近邻距离平方期望控制误差，再写“当 $n\to\infty$，上界 $\to0$”。前面一行常数和指数有改写。

这是一条在当前 Lipschitz 框架内的零噪声解题路线；原稿没有另写一般情形的完整证明，此处不补写。

## 6. 核回归：从卷积直觉到联合控制

来源：原稿第 13–18 页；教材 §6.3.3，印刷页 170–173。

令 $\widehat P_n=n^{-1}\sum_i\delta_{x_i}$。核加权分子可写成

```math
\frac1n\sum_iq_h(x-x_i)g(x_i)
=\int q_h(x-z)g(z)\,d\widehat P_n(z).
```

若 $P_X$ 有密度 $p$，固定 $h$ 时，该经验平均对应总体卷积 $[q_h*(pg)](x)$。分母对应 $m_h(x)=(q_h*p)(x)$。

### 6.1 渐近直觉及其限制

对固定 $x,h$，大数定律提示

```math
n\sum_i\widehat w_i(x)^2
\longrightarrow\frac{(q_h^2*p)(x)}{(q_h*p)(x)^2}.
```

再令 $h$ 变小，在适当局部正则条件下，平方权重和的量级为

```math
\sum_i\widehat w_i(x)^2\sim\frac1{nh^dp(x)}\int q(u)^2\,du.
```

偏差分子通过 $z=x-hu$ 换元：

```math
\int q_h(x-z)\|x-z\|_2^2p(z)\,dz
=h^2\int q(u)\|u\|_2^2p(x-hu)\,du.
```

这提示 $\sigma^2/(nh^d)+B^2h^2$ 的权衡，但原稿第 15 页指出三个缺口：$h=h_n$ 随样本数变化；随机分母可能过小；固定点渐近不能直接对总体分布积分。下面的非渐近计算保留这三个问题。

### 6.2 Proposition 6.3：按证明整理的误差界

设 $q$ 为有界非负概率密度，$c_q=\int q(u)\|u\|_2^2du<\infty$；输入密度 $p$ 有界、支撑 $\mathcal X$ 有界。定义

```math
C_h=\int_{\mathcal X}\frac{p(x)}{m_h(x)}\,dx,
\qquad m_h(x)=(q_h*p)(x).
```

当分母定义良好且 $C_h<\infty$ 时，由原稿和教材证明中的两项上界合并得到

```math
\mathcal E_n\le C_h\left[
\frac{8\|q\|_\infty}{nh^d}
\left(\sigma^2+\frac{B^2}{2}\operatorname{diam}(\mathcal X)^2\right)
+2B^2h^2\|p\|_\infty c_q\right].
```

> **系数整理说明。** 锁定教材印刷页 172 的式 (6.11) 把两处偏差系数印成 $B$，但下一页证明明确在加权距离项外乘 $B^2$；原稿也混写 $B$、$B^2$，并在合并时漏掉过直径平方和密度上界。上式依据已有偏差—方差推导统一为 $B^2$，不是逐字照抄式 (6.11)。本次没有认定作者已经发布勘误。

### 6.3 Bernstein 控制随机分母

固定 $x$，写 $M=\|q\|_\infty$、$m=m_h(x)>0$、$Z_i=q_h(x-x_i)$。则

```math
0\le Z_i\le Mh^{-d},\qquad \mathbb EZ_i=m,
\qquad \mathbb EZ_i^2\le Mh^{-d}m.
```

原稿使用的单侧 Bernstein 界为

```math
P\left(\frac1n\sum_iZ_i\le m-\varepsilon\right)
\le\exp\left(-\frac{n\varepsilon^2}{2\mathbb EZ_i^2+(2/3)Mh^{-d}\varepsilon}\right).
```

取 $\varepsilon=m/2$，定义坏事件 $A=\{n^{-1}\sum_iZ_i\le m/2\}$，得到

```math
P(A)\le\exp\left(-\frac{3nh^dm}{28M}\right)
\le\frac{28M}{3e\,nh^dm}
\le\frac{4M}{nh^dm}.
```

这里使用 $e^{-t}\le1/(et)$。常数 $28/3$ 来自 $\varepsilon=m/2$ 的代入，保留了原稿第 16–17 页的计算。

### 6.4 方差与偏差分别在两个事件上估计

坏事件上 $\sum_i\widehat w_i^2\le1$；好事件上 $\sum_iZ_i\ge nm/2$，故

```math
\mathbb E\left[\mathbf1_{A^c}\sum_i\widehat w_i^2\right]
\le\frac4{n^2m^2}\sum_i\mathbb EZ_i^2
\le\frac{4M}{nh^dm}.
```

加上坏事件得到 $\mathbb E\sum_i\widehat w_i^2\le8M/(nh^dm)$，积分后乘 $\sigma^2$ 即方差界。

令 $D=\operatorname{diam}(\mathcal X)$。同样分事件控制加权距离：

```math
\begin{aligned}
\mathbb E\sum_i\widehat w_i(x)\|x-x_i\|_2^2
&\le D^2P(A)+\frac2m\mathbb E[q_h(x-X)\|x-X\|_2^2]\\
&\le\frac{4MD^2}{nh^dm}
+\frac{2h^2\|p\|_\infty c_q}{m}.
\end{aligned}
```

对 $P_X$ 积分再乘 $B^2$，与方差界相加得到上面的合并式。若 $\sup_{h\downarrow0}C_h<\infty$，取 $h\asymp n^{-1/(d+2)}$ 得到 $O(n^{-2/(d+2)})$。**$C_h$ 的有界性是额外要求，不由这个带宽选择自动保证。**

### Exercise 6.4：原稿留白 {#ex-6-4}

原稿第 19 页仅写：

> 但是
>
> Ex 6.4

题号下没有题干和解答。第 18 页相邻的 $C_h$ 换元草算不能视为这道题已经完成。此处只把前文卷积记号统一为

```math
(q_h*p)(x)=\int_{\mathbb R^d}q(u)p(x-hu)\,du,
```

不补充 $C_h$ 有界的证明、边界假设或反例。

## 7. 继续阅读

下一部分：[Ch6.4–6.5 普遍一致性与高阶光滑性](ch6.4-6.5-universal-consistency.md)。所有习题状态见[覆盖映射](study-map.md)。
