# Ch6.4–6.5 普遍一致性与高阶光滑性

> 状态：`note_unverified`。由《Ch6局部平均值算法.pdf》第 19–23 页整理，对应锁定教材印刷页 174–178。接[局部平均方法与一致性分析](ch6.1-6.3-local-averaging.md)。习题未写的部分保持留白。

## 1. 从 Lipschitz 函数推广到平方可积函数

前一节在 $f_*$ 为 $B$-Lipschitz 时，用 $\mathcal E_n\le B^2D_n+\sigma^2V_n$ 控制误差。若只知道 $f_*\in L^2(P_X)$，可以先用 Lipschitz 函数 $g$ 逼近它，再分别控制逼近误差和局部平均误差。

沿用前一节的 $D_n,V_n$，要求

```math
D_n\to0,\qquad V_n\to0.
```

还需要存在与 $n$ 无关的常数 $c$，使任意非负可积函数 $h$ 满足

```math
\int\mathbb E\left[\sum_i\widehat w_i(x)h(x_i)\right]dP_X(x)
\le c\int h(x)dP_X(x).
```

这对应教材式 (6.13)。原稿的“任意可积 h”在这里明确为非负函数；后面实际代入的是平方误差。

## 2. 三项分解

固定 $\varepsilon>0$，选取一个 $B(\varepsilon)$-Lipschitz 函数 $g$，使

```math
\|f_*-g\|_{L^2(P_X)}\le\varepsilon.
```

原稿把函数差拆成

```math
f_*(x_i)-f_*(x)
=[f_*(x_i)-g(x_i)]+[g(x_i)-g(x)]+[g(x)-f_*(x)].
```

由 $(a+b+c)^2\le3a^2+3b^2+3c^2$、权重和为 1 及 Jensen 不等式，积分后的三项分别可界为：

1. 样本位置上的逼近误差：$3c\varepsilon^2$。
2. Lipschitz 函数的局部偏差：$3B(\varepsilon)^2D_n$。
3. 测试位置上的逼近误差：$3\varepsilon^2$。

因此

```math
\mathcal E_n\le3(c+1)\varepsilon^2+3B(\varepsilon)^2D_n+\sigma^2V_n.
```

先固定 $\varepsilon$，让 $n\to\infty$，得到

```math
\limsup_{n\to\infty}\mathcal E_n\le3(c+1)\varepsilon^2.
```

再令 $\varepsilon\downarrow0$，便得到 $\mathcal E_n\to0$。顺序不能倒过来，因为 $B(\varepsilon)$ 可能在 $\varepsilon\to0$ 时增长。原稿写作“sup”的极限句据此前后文整理为“limsup”。

原稿使用了 Lipschitz 函数在 $L^2(P_X)$ 中稠密这一事实，但没有证明该稠密性；这里仍将它作为所用事实记录。

## 3. Exercise 6.5：已有计算，最后联系未展开 {#ex-6-5}

来源：原稿第 21 页。原稿首先记录

```math
\mathbb E\left[\frac1{1+Z_1+\cdots+Z_n}\right]\le\frac1{(n+1)p}.
```

从随后的二项展开可辨，这里 $Z_i$ 为独立 Bernoulli$(p)$ 随机变量，$p>0$。已有计算整理为

```math
\begin{aligned}
\sum_{k=0}^n\binom nk\frac{p^k(1-p)^{n-k}}{k+1}
&=\frac1{(n+1)p}\sum_{k=0}^n\binom{n+1}{k+1}p^{k+1}(1-p)^{n-k}\\
&=\frac{1-(1-p)^{n+1}}{(n+1)p}
\le\frac1{(n+1)p}.
\end{aligned}
```

第二个等号对应原稿已写但涂改较重的“1 减去一项”，由同一二项求和辨认恢复。

原稿又记下单元计数

```math
N_j=\sum_{t=1}^n\mathbf1_{\{x_t\in A_j\}},
```

以及最后的结论

```math
\int\mathbb E\left[\sum_i\widehat w_i(x)h(x_i)\right]dP_X(x)
\le2\int h(x)dP_X(x).
```

> **原始完成状态：简写，未展开。** 二项求和部分已经写出；由它到权重积分不等式的条件化、交换求和及空单元处理没有写全。保留这一断点，不补齐中间证明。

## 4. 更高光滑性为何可能改善速率

来源：原稿第 22–23 页，对应 §6.5。若 $f_*$ 有二阶光滑性，在测试点附近有

```math
f_*(x_i)-f_*(x)
=\nabla f_*(x)^\top(x_i-x)+O(\|x_i-x\|^2).
```

原稿的想法是让加权的一阶项抵消：

```math
\nabla f_*(x)^\top\sum_i\widehat w_i(x)(x_i-x)\approx0.
```

若能做到，使未平方的偏差达到 $O(h^2)$，则平方偏差为 $O(h^4)$；若方差仍为 $O(1/(nh^d))$，平衡得

```math
h\asymp n^{-1/(d+4)},\qquad
\mathcal E_n=O(n^{-4/(d+4)}).
```

这些是**一阶项能够消去之后**的条件性速率计算，不能据此断言任意局部平均估计器自动达到该速率。

### Exercise 6.6：构造未写 {#ex-6-6}

原稿第 22 页写：

> Ex 6.6 如何做到这一步
>
> 但是

之后没有权重构造、估计器定义或相应证明。第 23 页只继续写了 $O(h^4)$、$O(1/(nh^d))$ 以及平衡速率。本次保留这些内容，不补完 Exercise 6.6。
