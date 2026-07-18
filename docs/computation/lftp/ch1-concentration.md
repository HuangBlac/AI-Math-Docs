# Ch1 再论集中不等式

## 1. 三个不等式放在一起

### Hoeffding

设 $Z_i\in[a_i,b_i]$ 相互独立，则
$$
\mathbb P\left(
\left|
\sum_{i=1}^n(Z_i-\mathbb EZ_i)
\right|>t
\right)
\le
2\exp\left(
-\frac{2t^2}{\sum_{i=1}^n(b_i-a_i)^2}
\right).
$$
它只利用每个随机变量的取值范围。

证明方式：

首先使用Markov不等式，将问题转化为对于$E(e^{s(Z-EZ_i)})$的控制，然后构造对数

使用对数矩母函数，求一次，二次导数，然后做概率测度的变换，将其转化为一个方差的控制。

不失一般性，可以考虑随机变量处于[0,1]

------

### McDiarmid

设
$$
F=f(Z_1,\dots,Z_n),
$$
且改变第 $i$ 个输入最多使函数值改变 $c_i$：
$$
|f(z)-f(z^{(i)})|\le c_i.
$$
那么
$$
\mathbb P\left(
|F-\mathbb EF|>t
\right)
\le
2\exp\left(
-\frac{2t^2}{\sum_{i=1}^n c_i^2}
\right).
$$
它不要求 $f$ 是求和，只要求每一个样本对最终结果的影响有限。

其中Amuza不等式是其中的一个特殊情况，其核心在于构造Doob-鞅，一系列的随机变量，然后证明每个部分的指数期望都可以被控制住，进而再次使用Markov不等式。



------

### Bernstein

设
$$
\mathbb EZ_i=0,\qquad |Z_i|\le c,
$$
记
$$
V=\sum_{i=1}^n\operatorname{Var}(Z_i).
$$
则
$$
\mathbb P\left(
\left|\sum_{i=1}^nZ_i\right|>t
\right)
\le
2\exp\left(
-\frac{t^2}{2V+\frac{2ct}{3}}
\right).
$$
它同时使用：
$$
\text{真实方差 }V
\qquad\text{和}\qquad
\text{绝对上界 }c.
$$

------

## 2. Hoeffding 是 McDiarmid 的特殊情况

取
$$
f(Z_1,\dots,Z_n)=\sum_{i=1}^n Z_i.
$$
如果 $Z_i\in[a_i,b_i]$，只替换第 $i$ 个变量，则
$$
\left|
f(z)-f(z^{(i)})
\right|
=
|z_i-z_i'|
\le b_i-a_i.
$$
所以 McDiarmid 中
$$
c_i=b_i-a_i.
$$
代入后得到
$$
\mathbb P\left(
\left|
\sum_iZ_i-\mathbb E\sum_iZ_i
\right|>t
\right)
\le
2\exp\left(
-\frac{2t^2}{\sum_i(b_i-a_i)^2}
\right),
$$
正好就是 Hoeffding。

因此：
$$
\boxed{
\text{对线性求和而言，McDiarmid 基本就是 Hoeffding。}
}
$$
McDiarmid 的优势不是在这个情况下给出更小的界，而是允许研究非线性统计量。

------

## 3. McDiarmid 比 Hoeffding 一般在哪里

例如在学习理论中常研究
$$
F(S)
=
\sup_{h\in\mathcal H}
\left|
\widehat R_S(h)-R(h)
\right|.
$$
这里
$$
\widehat R_S(h)
=
\frac1n\sum_{i=1}^n\ell(h,Z_i),
$$
但外面还有一个关于 $h$ 的上确界。因此 $F(S)$ 本身不是简单的随机变量平均。

假设损失满足
$$
0\le \ell(h,z)\le 1.
$$
把样本 $Z_i$ 换成 $Z_i'$，对于任意 $h$，
$$
\left|
\widehat R_S(h)-\widehat R_{S'}(h)
\right|
\le\frac1n.
$$
上确界的变化也不超过 $1/n$，所以
$$
c_i=\frac1n.
$$
McDiarmid 给出
$$
\mathbb P\left(
|F(S)-\mathbb EF(S)|>t
\right)
\le
2e^{-2nt^2}.
$$
Hoeffding 无法直接处理这个 $F(S)$，因为它不是固定的独立随机变量之和。

所以 McDiarmid 回答的是：

> 一个复杂的样本统计量，只要对单个样本不敏感，是否仍然集中？

答案是肯定的。

------

## 4. McDiarmid 和 Bernstein 谁更精确

在随机变量求和的情况下，McDiarmid 通常和 Hoeffding 一样，只利用最坏情况变化，而 Bernstein 还利用方差。因此如果方差很小，Bernstein 通常更精确。

假设
$$
Z_i\in[-c,c],
\qquad
\sigma^2=\frac1n\sum_i\operatorname{Var}(Z_i).
$$
对于平均值
$$
\overline Z=\frac1n\sum_iZ_i,
$$
Hoeffding 或 McDiarmid 给出
$$
\mathbb P(|\overline Z-\mathbb E\overline Z|>t)
\le
2\exp\left(-\frac{nt^2}{2c^2}\right).
$$
Bernstein 给出
$$
\mathbb P(|\overline Z-\mathbb E\overline Z|>t)
\le
2\exp\left(
-\frac{nt^2}{2\sigma^2+\frac{2ct}{3}}
\right).
$$
当
$$
\sigma^2\ll c^2
$$
且 $t$ 不大时，Bernstein 的分母近似为
$$
2\sigma^2,
$$
远小于 Hoeffding 或 McDiarmid 的
$$
2c^2.
$$
因此 Bernstein 明显更强。

------

## 5. 一个极端例子

设
$$
X_i\sim\operatorname{Bernoulli}(p),
\qquad
Z_i=X_i-p.
$$
虽然 $X_i\in[0,1]$，但
$$
\operatorname{Var}(X_i)=p(1-p).
$$
当 $p=0.001$ 时，
$$
p(1-p)\approx0.001.
$$
Hoeffding 和 McDiarmid 只知道区间长度是 $1$，因此都给出
$$
2e^{-2nt^2}.
$$
Bernstein 对小 $t$ 近似给出
$$
2\exp\left(
-\frac{nt^2}{2p(1-p)}
\right)
\approx
2e^{-500nt^2}.
$$
差别巨大。

原因是：

- Hoeffding/McDiarmid 认为每个样本都可能在整个区间内剧烈波动；
- Bernstein 知道 $X_i$ 几乎总是 $0$，实际方差很小。