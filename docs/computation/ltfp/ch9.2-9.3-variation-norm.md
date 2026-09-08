# Ch9.2–9.3 深层复杂度草算与变差范数

> 状态：`note_unverified`。由《习题.pdf》4 页中的 LTFP 内容整理。重复的 Ex 9.2 草算合并；原稿混入的 KV cache 段落不纳入本篇。难辨记号按锁定教材 §9.2–9.3 梳理，未完成证明保持原状。

本篇接[Ch9.1–9.2 神经网络理论](ch9.1-9.2-neural-networks.md)，只记录本次原稿新增或重复出现的推导，不代表 §9.3 已全部覆盖。

## 1. 极大值期望的补充计算

来源：原稿第 4 页。该段没有明确写习题编号；其 $\ell_\infty$ 输入界与教材 §9.2.3 的另一类参数约束有关，这里不替原稿补标为已作答的 Exercise 9.1。

设 $\|x_i\|_\infty\le R$，定义增广向量与坐标平均

```math
z_i=(x_i^\top,R)^\top\in\mathbb R^{d+1},
\qquad S_k=\frac1n\sum_{i=1}^n\varepsilon_i z_{ik},
\quad k=1,\ldots,d+1,
```

其中 $\varepsilon_i$ 为独立 Rademacher 符号。原稿先控制单个坐标：

```math
\mathbb E_\varepsilon S_k^2
=\frac1{n^2}\sum_i z_{ik}^2\le\frac{R^2}{n},
\qquad
\mathbb E_\varepsilon e^{\pm\lambda S_k}\le e^{\lambda^2R^2/(2n)}.
```

独立性消去了交叉项。这里把原稿误写成等号的有界项整理成不等号。记 $p=d+1$，则

```math
\mathbb E e^{\lambda\max_k|S_k|}
\le\sum_{k=1}^p\bigl(\mathbb E e^{\lambda S_k}+\mathbb E e^{-\lambda S_k}\bigr)
\le2p\,e^{\lambda^2R^2/(2n)}.
```

取对数并用 Jensen 不等式：

```math
\mathbb E\max_k|S_k|
\le\frac{\log(2p)}\lambda+\frac{\lambda R^2}{2n}.
```

原稿 λ 的取值被划改，没有确定下来；已写的最终量级为

```math
\mathbb E\max_k|S_k|\le\frac{2R\sqrt{\log(2(d+1))}}{\sqrt n}.
```

原稿另记录“统计误差 $8GRD\sqrt{\log(2(d+1))}/\sqrt n$”。G、D 对应损失 Lipschitz 常数与输出系数范数，但该页未重新写清整个函数类及全部常数传递步骤。保留这一结果记录，不据此认定该题已完整证明。

## 2. Exercise 9.2：深层网络的 Rademacher 复杂度 {#ex-9-2}

来源：原稿第 3 页及第 4 页下半部。原稿用 n 同时表示样本数和层数，这里分别用 n 和 ℓ。

### 2.1 函数类与基类

```math
\mathcal F_0=\{x\mapsto\theta^\top x:\|\theta\|_2\le D_0\},
```

```math
\mathcal F_{\ell+1}
=\left\{x\mapsto\sum_{j=1}^{m_{\ell+1}}\theta_j\sigma(f_j(x)):
\|\theta\|_1\le D_{\ell+1},\ f_j\in\mathcal F_\ell\right\}.
```

原稿写明 $\sigma$ 为 1-Lipschitz，并在推导中使用 $\sigma(0)=0$。对固定输入 $\|x_i\|_2\le R$，采用带绝对值的经验 Rademacher 复杂度

```math
\mathcal R_n(\mathcal F)=\mathbb E_\varepsilon\sup_{f\in\mathcal F}
\left|\frac1n\sum_i\varepsilon_i f(x_i)\right|.
```

两页重复的基类计算整理为

```math
\begin{aligned}
\mathcal R_n(\mathcal F_0)
&=D_0\mathbb E_\varepsilon\left\|\frac1n\sum_i\varepsilon_i x_i\right\|_2\\
&\le D_0\sqrt{\mathbb E_\varepsilon\left\|\frac1n\sum_i\varepsilon_i x_i\right\|_2^2}
\le\frac{D_0R}{\sqrt n}.
\end{aligned}
```

### 2.2 原稿已经写到的收缩步骤

原稿利用 $\sum_j|\theta_j|\le D_{\ell+1}$，将一层的线性组合控制到单个前层函数的激活值。其后已有的收缩不等式为

```math
D_{\ell+1}\mathbb E_\varepsilon\sup_{f\in\mathcal F_\ell}
\left|\frac1n\sum_i\varepsilon_i[\sigma(f(x_i))-\sigma(0)]\right|
\le2D_{\ell+1}\mathbb E_\varepsilon\sup_{f\in\mathcal F_\ell}
\left|\frac1n\sum_i\varepsilon_i f(x_i)\right|.
```

原稿在下一行只写了

> $R_n(F_{n+1})$

另一页的重复起笔也停在 $R_n(F_{k+1})$。

**原始完成状态：未完成。** 没有整理出完整逐层递推、归纳过程和最终层数乘积界。保留上面的已写步骤，不把它续算成完整答案。

## 3. 一维逼近与无限宽表示

来源：原稿第 3 页下半部。原稿的主线是：一维连续分段线性函数可以逼近连续函数；有限神经元对应离散权重，把宽度放开后可用测度描述。

对于 ReLU $\sigma(t)=t_+$，写作

```math
f(x)=\int_K\sigma(w^\top x+b)\,d\nu(w,b).
```

有限宽情形 $\nu=\sum_j\eta_j\delta_{(w_j,b_j)}$，其总变差对应合并同位置原子后的输出系数绝对值之和。神经网络可以通过调整 $(w,b)$ 自适应地寻找方向；原稿以此对比固定特征。

原稿还记录“近似 Carathéodory 定理、Frank–Wolfe”，以及有限宽逼近的量级

```math
\|f_m-g\|_{L^2}\lesssim\frac{R\gamma_1(g)}{\sqrt m}.
```

> 原稿没有指定这行 $L^2$ 的完整测度设置、原子归一化常数或构造算法。这里保留为工具与量级记录，不扩成新证明。

## 4. 变差范数与 Proposition 9.2

来源：原稿第 1 页；教材 §9.3.2，印刷页 258–259。原稿该页页眉写“9.3.4”，但范数与向量空间内容属于 §9.3.2，整理时按内容归位。

为明确原稿中 $\gamma_1$ 的含义，采用教材记号：对紧参数集合 K 上的有限总变差符号测度，在所有表示 f 的测度中取

```math
\gamma_1(f)=\inf_{\nu:\ f(x)=\int_K\sigma(w^\top x+b)d\nu(w,b)}\|\nu\|_{\mathrm{TV}},
\qquad \mathcal F_1=\{f:\gamma_1(f)<\infty\}.
```

这是对原稿已用概念的定义澄清。Proposition 9.2 说明在相应紧性条件下 $\mathcal F_1$ 是向量空间、$\gamma_1$ 是其上的范数。

原稿列出绝对齐次性、非负性及三角不等式：

```math
\gamma_1(af)=|a|\gamma_1(f),\qquad\gamma_1(f)\ge0,
\qquad\gamma_1(f_1+f_2)\le\gamma_1(f_1)+\gamma_1(f_2).
```

最后一项难辨的“$\gamma_2$”据整段统一为 $\gamma_1$。原稿已有验证思路：若 $\nu_1,\nu_2$ 分别表示 $f_1,f_2$，则

```math
f_1+f_2=\int_K\sigma(w^\top x+b)\,d(\nu_1+\nu_2)(w,b),
\qquad
\|\nu_1+\nu_2\|_{\mathrm{TV}}\le\|\nu_1\|_{\mathrm{TV}}+\|\nu_2\|_{\mathrm{TV}}.
```

原稿没有继续把对表示取下确界的步骤和范数正定性写全，保留为部分验证。

### 完备性：原稿只提出要求

> 证明 $(F,\gamma_1)$ 是一个 Banach 空间（完备）。

其后没有证明。本次不新增 Cauchy 列、极限测度或完备性论证。

## 5. §9.3.4 用 Fourier 变换联系多维光滑性

来源：原稿第 2 页；教材印刷页 263–264。原稿标题“将多维变成一维”指把 $e^{i\omega^\top x}$ 看成沿方向 ω 的一维振荡，再由 Fourier 积分组合各方向。

在适用 Fourier 反演且所需加权积分有限的条件下，原稿记下

```math
\gamma_1(f)\le\frac1{(2\pi)^d}\int_{\mathbb R^d}
|\widehat f(\omega)|\gamma_1(x\mapsto e^{i\omega^\top x})\,d\omega.
```

按教材式 (9.13)–(9.14) 的原子归一化，半径 R 的球上对应的后续界为

```math
\gamma_1(f)\le\frac{2}{R(2\pi)^d}\int_{\mathbb R^d}
|\widehat f(\omega)|(1+2R^2\|\omega\|_2^2)\,d\omega.
```

> **系数整理说明：** 原稿的前因子漏记了 $1/R$；此处已直接查看锁定教材印刷页 264 的式 (9.14)，据该范数约定恢复。没有把式 (9.13) 的一维构造证明补进原稿。

原稿另写出 Sobolev 范数的 Fourier 形式与导数形式的对应关系（整数 s，常数依赖 d、s 和 Fourier 约定）：

```math
\int|\widehat f(\omega)|^2(1+\|\omega\|_2^2)^s\,d\omega
\asymp\sum_{|\alpha|\le s}\|\partial^\alpha f\|_{L^2}^2.
```

页尾只写“f 是一个……”便停止。**原始完成状态：未完成。** 没有把这两个不同的 Fourier 加权积分连接成完整充分条件或逼近定理，本次不继续推导。
