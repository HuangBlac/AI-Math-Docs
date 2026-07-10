# 数据科学优化：旧事重提

在这轮笔记中，我们试着回忆本学期《数据科学导论》PPT 中与优化有关的内容，主要包括：

- 梯度下降（Gradient Descent, GD）的下降性质、收敛速度及其所需条件；
- 随机梯度下降（Stochastic Gradient Descent, SGD）的基本不等式、期望界与高概率界；
- 强凸条件下 SGD 的收敛；
- 方差缩减方法 SVRG。

实际深度学习中还经常使用 AdamW 与 Muon，不过本文暂不展开。

---

## 1. 梯度下降

### 1.1 算法定义

设目标函数为

$$
\min_{x\in\mathbb R^d} f(x).
$$

给定初始点 $x_0$，梯度下降迭代为

$$
x_{k+1}=x_k-\alpha_k\nabla f(x_k),
\qquad k=0,1,\ldots,
$$

其中 $\alpha_k>0$ 为步长。

为什么选择负梯度方向作为下降方向？

关键在于：如果 $\nabla f$ 是 $L$-Lipschitz 连续的，即
$$
\|\nabla f(x)-\nabla f(y)\|_2\le L\|x-y\|_2,
$$

注：对于二阶可微的情况下，这等价于Hesse阵的2范数小于等于L

那么由下降引理（descent lemma），对任意 $x,y\in\mathbb R^d$，都有
$$
f(y)
\le
f(x)+\langle \nabla f(x),y-x\rangle
+\frac L2\|y-x\|_2^2.
$$

令

$$
y=x-\alpha\nabla f(x),
$$

则

$$
\begin{aligned}
f(y)
&\le
f(x)-\alpha\|\nabla f(x)\|_2^2
+\frac{L\alpha^2}{2}\|\nabla f(x)\|_2^2\\
&=
f(x)-\alpha\left(1-\frac{L\alpha}{2}\right)
\|\nabla f(x)\|_2^2.
\end{aligned}
$$

因此，只要下降的步长足够小，在此处可以写为$0<\alpha_k<\frac{2}{L}$

就有

$$
f(x_{k+1})\le f(x_k).
$$

### 1.2 梯度范数的次线性收敛

将上面的下降不等式应用于梯度下降，并对 $k<t$ 求和：

$$
\begin{aligned}
\sum_{k<t}
\alpha_k\left(1-\frac{L\alpha_k}{2}\right)
\|\nabla f(x_k)\|_2^2
&\le
\sum_{k<t}\bigl(f(x_k)-f(x_{k+1})\bigr)\\
&=f(x_0)-f(x_t).
\end{aligned}
$$

若取常数步长

$$
\alpha_k=\alpha\in\left(0,\frac{2}{L}\right),
$$

则

$$
\begin{aligned}
\min_{k<t}\|\nabla f(x_k)\|_2^2
&\le
\frac1t\sum_{k<t}\|\nabla f(x_k)\|_2^2\\
&\le
\frac{2}{t\alpha(2-\alpha L)}
\bigl(f(x_0)-f(x_t)\bigr)\\
&\le
\frac{2}{t\alpha(2-\alpha L)}
\bigl(f(x_0)-f(x^*)\bigr).
\end{aligned}
$$

对 $\alpha$ 优化可得 $\alpha=1/L$，于是

$$
\boxed{
\min_{k<t}\|\nabla f(x_k)\|_2^2
\le
\frac{2L}{t}\bigl(f(x_0)-f(x^*)\bigr)
}.
$$

这里并没有使用凸性。因此，对一般光滑非凸函数，梯度下降至少可以保证在 $O(1/t)$ 的意义下找到近似驻点。

### 1.3 MM 算法视角

梯度下降也可以放在 MM（Majorization-Minimization）框架中理解。构造代理函数

$$
M(x,y)
=
f(x)+\langle\nabla f(x),y-x\rangle
+\frac L2\|y-x\|_2^2.
$$

由下降引理，

$$
M(x,y)\ge f(y),
\qquad
M(x,x)=f(x).
$$

然后令

$$
x_{k+1}\in\arg\min_y M(x_k,y).
$$

对 $M(x_k,y)$ 关于 $y$ 求最小值，便得到

$$
x_{k+1}=x_k-\frac1L\nabla f(x_k).
$$

---

当然，我们关于梯度下降算法，例如牛顿法，拟牛顿法等部分放在了优化对应的部分，还附上了一些数值实验。



## 2. 不要求凸性时的函数值收敛

### 2.1 一个广义星凸条件

假设存在 $\gamma>0$，使得

$$
\langle\nabla f(x),x-x^*\rangle
\ge
\gamma\bigl(f(x)-f(x^*)\bigr).
\tag{1}
$$

由 Cauchy--Schwarz 不等式，

$$
\gamma\bigl(f(x)-f(x^*)\bigr)
\le
\langle\nabla f(x),x-x^*\rangle
\le
\|\nabla f(x)\|_2\|x-x^*\|_2.
$$

采用步长 $1/L$：

$$
x_{k+1}=x_k-\frac1L\nabla f(x_k).
$$

记

$$
\varepsilon_k=f(x_k)-f(x^*),
$$

并定义初始水平集半径

$$
R=
\max_{f(x)\le f(x_0)}\|x-x^*\|_2.
$$

由于函数值单调下降，所有 $x_k$ 都位于该水平集内。因此，由条件 (1)，

$$
\varepsilon_k
\le
\frac1\gamma\|x_k-x^*\|_2\|\nabla f(x_k)\|_2
\le
\frac R\gamma\|\nabla f(x_k)\|_2.
$$

另一方面，由下降引理，

$$
f(x_{k+1})
\le
f(x_k)-\frac1{2L}\|\nabla f(x_k)\|_2^2.
$$

于是

$$
\varepsilon_{k+1}
\le
\varepsilon_k-
\frac1{2L}
\left(\frac{\gamma\varepsilon_k}{R}\right)^2.
$$

即

$$
\varepsilon_k-\varepsilon_{k+1}
\ge
\frac{\gamma^2}{2LR^2}\varepsilon_k^2.
$$

由于 $\varepsilon_{k+1}\le\varepsilon_k$，

$$
\begin{aligned}
\frac1{\varepsilon_{k+1}}-
\frac1{\varepsilon_k}
&=
\frac{\varepsilon_k-\varepsilon_{k+1}}
{\varepsilon_k\varepsilon_{k+1}}\\
&\ge
\frac{\varepsilon_k-\varepsilon_{k+1}}
{\varepsilon_k^2}\\
&\ge
\frac{\gamma^2}{2LR^2}.
\end{aligned}
$$

若 $x^*$ 是可微函数的极小点，则 $\nabla f(x^*)=0$。再由 $L$-光滑性，

$$
\varepsilon_0
=f(x_0)-f(x^*)
\le
\frac L2\|x_0-x^*\|_2^2
\le
\frac{LR^2}{2}.
$$

对 $k=0,\ldots,t-1$ 求和：

$$
\begin{aligned}
\frac1{\varepsilon_t}
&\ge
\frac1{\varepsilon_0}
+\frac{t\gamma^2}{2LR^2}\\
&\ge
\frac{2}{LR^2}
+\frac{t\gamma^2}{2LR^2}\\
&=
\frac{\gamma^2t+4}{2LR^2}.
\end{aligned}
$$

因此

$$
\boxed{
f(x_t)-f(x^*)
\le
\frac{2LR^2}{\gamma^2t+4}
=O\left(\frac1t\right)
}.
$$

### 2.2 PL 条件与线性收敛

若希望函数值线性收敛，并不一定需要强凸性。一个常用条件是 Polyak--Łojasiewicz（PL）条件：存在 $m>0$，使得

$$
\|\nabla f(x)\|_2^2
\ge
2m\bigl(f(x)-f(x^*)\bigr),
\qquad \forall x.
$$

结合步长 $1/L$ 时的下降不等式，

$$
f(x_{k+1})
\le
f(x_k)-\frac1{2L}\|\nabla f(x_k)\|_2^2,
$$

可得

$$
f(x_{k+1})-f(x^*)
\le
\left(1-\frac mL\right)
\bigl(f(x_k)-f(x^*)\bigr).
$$

因此

$$
\boxed{
f(x_k)-f(x^*)
\le
\left(1-\frac mL\right)^k
\bigl(f(x_0)-f(x^*)\bigr)
}.
$$

PL 条件不蕴含凸性。例如，PPT 中给出的非凸例子是

$$
f(x)=x^2+3\sin^2 x.
$$

PL 条件对于分析过参数化深度学习中的 GD 与 SGD 很重要。

---

## 3. 不可微优化与近端梯度

对于不可微但凸的函数，可以用次梯度代替梯度。例如，ReLU 在 $x=0$ 处不可微，但存在次梯度。

需要注意的是，即使每一层所使用的函数本身是凸函数，函数复合后也未必保持凸性。因此，神经网络的整体优化问题通常仍然是非凸的。

考虑复合优化问题

$$
\min_{x\in\mathbb R^d} F(x)
=
\min_{x\in\mathbb R^d}\bigl(f(x)+h(x)\bigr),
$$

其中 $f$ 光滑，$h$ 可以不可微。近端梯度下降为

$$
\boxed{
x_{k+1}
=
\operatorname{Prox}_{\alpha_k h}
\bigl(x_k-\alpha_k\nabla f(x_k)\bigr)
},
$$

其中

$$
\operatorname{Prox}_{\alpha h}(v)
:=
\arg\min_x
\left\{
 h(x)+\frac1{2\alpha}\|x-v\|_2^2
\right\}.
$$

---

## 4. 近似梯度与 SGD 的基本不等式

考虑凸优化问题

$$
\min_{x\in\mathbb R^d}f(x),
$$

并采用近似梯度迭代

$$
x_{k+1}=x_k-\alpha_k g_k,
$$

其中 $g_k$ 是 $\nabla f(x_k)$ 的近似。

### 4.1 Key step

取常数步长 $\alpha_k=\alpha$。对任意比较点 $z$，

$$
\begin{aligned}
\|x_{k+1}-z\|_2^2
&=
\|x_k-\alpha g_k-z\|_2^2\\
&=
\|x_k-z\|_2^2
-2\alpha\langle g_k,x_k-z\rangle
+\alpha^2\|g_k\|_2^2\\
&=
\|x_k-z\|_2^2
+2\alpha
\langle g_k-\nabla f(x_k)+\nabla f(x_k),z-x_k\rangle
+\alpha^2\|g_k\|_2^2.
\end{aligned}
$$

由凸性，

$$
\langle\nabla f(x_k),z-x_k\rangle
\le
f(z)-f(x_k).
$$

定义误差项

$$
\varepsilon_k
:=
\langle g_k-\nabla f(x_k),z-x_k\rangle.
$$

于是

$$
\|x_{k+1}-z\|_2^2
\le
\|x_k-z\|_2^2
+2\alpha\bigl(f(z)-f(x_k)+\varepsilon_k\bigr)
+\alpha^2\|g_k\|_2^2.
$$

整理得到基本不等式：

$$
\boxed{
f(x_k)
\le
f(z)
+\frac{\|x_k-z\|_2^2}{2\alpha}
-\frac{\|x_{k+1}-z\|_2^2}{2\alpha}
+\varepsilon_k
+\frac\alpha2\|g_k\|_2^2
}.
$$

### 4.2 平均迭代点的误差界

设

$$
G=
\max_k\max\bigl\{
\|g_k\|_2,
\|\nabla f(x_k)\|_2
\bigr\},
$$

并取

$$
\alpha=\frac c{\sqrt t}.
$$

定义平均迭代点

$$
\bar x_t=\frac1t\sum_{k<t}x_k.
$$

将基本不等式对 $k<t$ 求和，再利用凸性，得到

$$
\begin{aligned}
f(\bar x_t)
&\le
\frac1t\sum_{k<t}f(x_k)\\
&\le
f(z)
+\frac{\|x_0-z\|_2^2}{2c\sqrt t}
+\frac{cG^2}{2\sqrt t}
+\frac1t\sum_{k<t}\varepsilon_k.
\end{aligned}
$$

---

## 5. SGD 的鞅差误差项

SGD 中假设随机梯度满足无偏性：

$$
\mathbb E\!\left[g_k\mid\mathcal F_{k-1}\right]
=
\nabla f(x_k),
$$

其中 $\mathcal F_{k-1}$ 表示第 $k$ 次采样前的历史信息。

由于 $x_k$ 对 $\mathcal F_{k-1}$ 可测，

$$
\begin{aligned}
\mathbb E\!\left[\varepsilon_k\mid\mathcal F_{k-1}\right]
&=
\mathbb E\!\left[
\langle g_k-\nabla f(x_k),z-x_k\rangle
\mid\mathcal F_{k-1}
\right]\\
&=
\left\langle
\mathbb E\!\left[g_k-\nabla f(x_k)
\mid\mathcal F_{k-1}\right],
 z-x_k
\right\rangle\\
&=0.
\end{aligned}
$$

因此 $\{\varepsilon_k\}$ 是鞅差序列，并且

$$
\mathbb E[\varepsilon_k]=0.
$$

若

$$
D=\max_k\|x_k-z\|_2,
$$

则

$$
\begin{aligned}
|\varepsilon_k|
&\le
\|g_k-\nabla f(x_k)\|_2\|z-x_k\|_2\\
&\le
2GD
=:B.
\end{aligned}
$$

### 5.1 高概率界

由条件 Hoeffding 引理，

$$
\mathbb E\!\left[e^{\lambda\varepsilon_k}
\mid\mathcal F_{k-1}\right]
\le
\exp\left(\frac{\lambda^2B^2}{2}\right).
$$

递推可得

$$
\mathbb E\exp\left(
\lambda\sum_{k<t}\varepsilon_k
\right)
\le
\exp\left(\frac{\lambda^2tB^2}{2}\right).
$$

因此，对任意 $s>0$，

$$
\begin{aligned}
\mathbb P\left(
\sum_{k<t}\varepsilon_k\ge s
\right)
&\le
\exp\left(-\lambda s+
\frac{\lambda^2tB^2}{2}\right)\\
&\le
\exp\left(-\frac{s^2}{2tB^2}\right),
\end{aligned}
$$

其中最后一步取

$$
\lambda=\frac{s}{tB^2}.
$$

令右端等于 $\delta$，则以至少 $1-\delta$ 的概率，

$$
\sum_{k<t}\varepsilon_k
\le
B\sqrt{2t\log\frac1\delta}.
$$

取 $z=x^*$，可得

$$
\boxed{
f(\bar x_t)-f^*
\le
\frac{\|x_0-x^*\|_2^2}{2c\sqrt t}
+\frac{cG^2}{2\sqrt t}
+B\sqrt{\frac{2\log(1/\delta)}{t}}
}
$$

以至少 $1-\delta$ 的概率成立。

### 5.2 期望界

由塔式法则，

$$
\mathbb E[\varepsilon_k]
=
\mathbb E\!\left[
\mathbb E[\varepsilon_k\mid\mathcal F_{k-1}]
\right]
=0.
$$

因此

$$
\boxed{
\mathbb E\bigl[f(\bar x_t)-f^*\bigr]
\le
\frac{\|x_0-x^*\|_2^2}{2c\sqrt t}
+\frac{cG^2}{2\sqrt t}
}.
$$

这给出了凸情形下 SGD 的典型 $O(t^{-1/2})$ 收敛率。

---

## 6. SGD 在经验风险最小化中的形式

### 6.1 有限样本 ERM

经验风险最小化可以写成

$$
\min_x f(x),
\qquad
f(x)=\sum_{i=1}^n f_i(x),
$$

其中

$$
f_i(x)
=
\frac1n\ell\bigl(Y_i,\phi_x(X_i)\bigr),
$$

且 $(X_i,Y_i)$ 是来自分布 $P$ 的 i.i.d. 样本。

在第 $k$ 次迭代中，以概率

$$
\mathbb P(i_k=j)=p_j
$$

抽取样本指标 $i_k$，并令

$$
g_k
=
\frac{\nabla f_{i_k}(x_k)}{p_{i_k}}.
$$

则

$$
\mathbb E[g_k\mid x_k]
=
\sum_{j=1}^np_j
\frac{\nabla f_j(x_k)}{p_j}
=
\nabla f(x_k).
$$

### 6.2 总体风险最小化

总体风险写为

$$
\min_x f(x)
=
\mathbb E_{(X,Y)\sim P}
\bigl[\ell(\phi_x(X),Y)\bigr].
$$

第 $k$ 次迭代抽取

$$
(X_k,Y_k)\sim P,
$$

并令

$$
g_k
=
\nabla_x\ell\bigl(\phi_{x_k}(X_k),Y_k\bigr).
$$

---

## 7. 强凸条件下的 SGD

假设：

1. $f$ 是 $m$-强凸函数；
2. $\nabla f$ 是 $L$-Lipschitz 连续的；
3. 随机梯度满足

$$
\mathbb E\|g(x)\|_2^2
\le
G^2+M_f\|\nabla f(x)\|_2^2.
$$

取常数步长 $\alpha_k=\alpha$。有

$$
\begin{aligned}
\|x_{k+1}-x^*\|_2^2
&=
\|x_k-\alpha g_k-x^*\|_2^2\\
&=
\|x_k-x^*\|_2^2
-2\alpha\langle g_k,x_k-x^*\rangle
+\alpha^2\|g_k\|_2^2.
\end{aligned}
$$

对于 $m$-强凸且 $L$-光滑的函数，有强化余单调不等式

$$
\boxed{
\langle\nabla f(x)-\nabla f(y),x-y\rangle
\ge
\frac{mL}{m+L}\|x-y\|_2^2
+
\frac1{m+L}
\|\nabla f(x)-\nabla f(y)\|_2^2
}.
$$

令 $y=x^*$，并使用 $\nabla f(x^*)=0$，得到

$$
\langle\nabla f(x_k),x_k-x^*\rangle
\ge
\frac{mL}{m+L}\|x_k-x^*\|_2^2
+
\frac1{m+L}\|\nabla f(x_k)\|_2^2.
$$

对递推式取期望：

$$
\begin{aligned}
\mathbb E\|x_{k+1}-x^*\|_2^2
&\le
\left(1-\frac{2mL\alpha}{m+L}\right)
\mathbb E\|x_k-x^*\|_2^2\\
&\quad
+\alpha^2G^2\\
&\quad
+\left(
\alpha^2M_f-
\frac{2\alpha}{m+L}
\right)
\mathbb E\|\nabla f(x_k)\|_2^2.
\end{aligned}
$$

若选择

$$
0<\alpha
\le
\frac{2}{(m+L)M_f},
$$

则最后一项非正。又因为 $L\ge m$，

$$
\frac{2mL}{m+L}\ge m,
$$

从而

$$
\mathbb E\|x_{k+1}-x^*\|_2^2
\le
(1-\alpha m)
\mathbb E\|x_k-x^*\|_2^2
+\alpha^2G^2.
$$

递推得到

$$
\boxed{
\mathbb E\|x_k-x^*\|_2^2
\le
(1-\alpha m)^k\|x_0-x^*\|_2^2
+
\frac{\alpha G^2}{m}
}.
$$

这说明：使用常数步长时，SGD 在初期呈线性收敛，但最终只能收敛到一个半径由 $\alpha G^2/m$ 控制的噪声邻域。若要继续提高精度，就需要减小步长或降低方差。

### 7.1 GD 与 SGD 的计算复杂度比较

在强凸有限和问题中，令条件数

$$
\kappa=\frac Lm.
$$

典型复杂度可概括为：

| 方法 | 迭代复杂度 | 单次迭代成本 | 总计算成本 |
|---|---:|---:|---:|
| GD | $O\!\left(\kappa\log\frac1\varepsilon\right)$ | $O(n)$ | $O\!\left(n\kappa\log\frac1\varepsilon\right)$ |
| SGD | $O\!\left(\frac1\varepsilon\right)$ | $O(1)$ | $O\!\left(\frac1\varepsilon\right)$ |

因此，当样本量 $n$ 很大且只要求中等精度时，SGD 往往更有吸引力。粗略地说，当

$$
\frac1\varepsilon
<
n\kappa\log\frac1\varepsilon
$$

时，SGD 的总计算量可能小于 GD。

---

## 8. 方差缩减：SVRG

### 8.1 控制变量思想

设

$$
Z_\theta
=
X-\theta\bigl(Y-\mathbb E[Y]\bigr).
$$

则

$$
\operatorname{Var}(Z_\theta)
=
\operatorname{Var}(X)
+\theta^2\operatorname{Var}(Y)
-2\theta\operatorname{Cov}(X,Y).
$$

如果 $Y$ 与 $X$ 正相关，并且 $\mathbb E[Y]$ 容易计算，就可以通过适当选择 $\theta$ 降低方差。

SVRG（Johnson--Zhang, 2013）使用

$$
X=
\frac{\nabla f_{i_k}(x_k)}{p_{i_k}},
\qquad
Y=
\frac{\nabla f_{i_k}(\tilde x)}{p_{i_k}},
\qquad
\theta=1,
$$

其中 $\tilde x$ 是外层循环中保存的快照点，并且

$$
\mathbb E[Y]=\nabla f(\tilde x).
$$

### 8.2 SVRG 算法

考虑

$$
\min_x F(x)
=
f(x)+h(x),
\qquad
f(x)=\sum_{i=1}^n f_i(x).
$$

给定内层迭代次数 $T$。在第 $s$ 个 epoch：

1. 从上一 epoch 的内层点中选取快照

   $$
   \tilde x_{s-1}=x_{s-1,j},
   \qquad
   j\sim\operatorname{Unif}\{0,\ldots,T-1\}.
   $$

2. 计算全梯度

   $$
   \tilde g_s=\nabla f(\tilde x_{s-1}).
   $$

3. 令

   $$
   x_{s,0}=\tilde x_{s-1}.
   $$

4. 对 $k=0,\ldots,T-1$：

   - 以概率 $\mathbb P(i_k=j)=p_j$ 抽取 $i_k$；
   - 计算

     $$
     g_{s,k}
     =
     \frac{\nabla f_{i_k}(x_{s,k})}{p_{i_k}},
     \qquad
     \tilde g_{s,k}
     =
     \frac{\nabla f_{i_k}(\tilde x_{s-1})}{p_{i_k}};
     $$

   - 更新

     $$
     \boxed{
     x_{s,k+1}
     =
     \operatorname{Prox}_{\alpha h}
     \left(
     x_{s,k}
     -\alpha
     \bigl(g_{s,k}-\tilde g_{s,k}+\tilde g_s\bigr)
     \right)
     }.
     $$

每个 epoch 大约需要 $n+2T$ 次分量梯度计算。

### 8.3 线性收敛结论

假设：

- 每个 $f_i$ 都是凸函数；
- 每个 $\nabla f_i$ 都是 $L$-Lipschitz 连续的；
- $f$ 是 $m$-强凸函数；
- 暂取 $h=0$。

若 $T$ 足够大，并且

$$
\rho
=
\frac{1}{m\alpha(1-2L\alpha)T}
+
\frac{2L\alpha}{1-2L\alpha}
<1,
$$

则

$$
\boxed{
\mathbb E\bigl[f(\tilde x_s)-f^*\bigr]
\le
\rho^s
\bigl(f(\tilde x_0)-f^*\bigr)
}.
$$

例如，选择

$$
T\ge\frac{9L}{m}=9\kappa,
\qquad
\alpha=\frac1{6L},
$$

可得

$$
0<\rho<\frac56.
$$

因此达到精度 $\varepsilon$ 需要

$$
O\left(\log\frac1\varepsilon\right)
$$

个 epoch。若 $T\asymp\max\{n,\kappa\}$，总计算成本为

$$
\boxed{
O\left(
(n+\kappa)
\log\frac1\varepsilon
\right)
}.
$$

相比之下，GD 的复杂度为

$$
O\left(
n\kappa\log\frac1\varepsilon
\right).
$$

---

## 9. SVRG 收敛证明梗概

为简化记号，令

$$
G_{s,k}
=
g_{s,k}-\tilde g_{s,k}+\tilde g_s,
$$

则内层更新为

$$
x_{s,k+1}=x_{s,k}-\alpha G_{s,k}.
$$

定义

$$
\varepsilon_{s,k}
=
\langle
G_{s,k}-\nabla f(x_{s,k}),
 x^*-x_{s,k}
\rangle.
$$

由构造可知

$$
\mathbb E\!\left[G_{s,k}\mid\mathcal F_{s,k}\right]
=
\nabla f(x_{s,k}),
\qquad
\mathbb E[\varepsilon_{s,k}]=0.
$$

由前面的 key step，

$$
\begin{aligned}
\mathbb E\|x_{s,k+1}-x^*\|_2^2
&\le
\mathbb E\|x_{s,k}-x^*\|_2^2
+2\alpha
\mathbb E\bigl[f(x^*)-f(x_{s,k})\bigr]\\
&\quad
+\alpha^2\mathbb E\|G_{s,k}\|_2^2.
\end{aligned}
$$

SVRG 的核心是证明方差界

$$
\boxed{
\mathbb E\|G_{s,k}\|_2^2
\le
4L\,
\mathbb E\left[
 f(x_{s,k})-f(x^*)
 +f(\tilde x_{s-1})-f(x^*)
\right]
}.
$$

于是

$$
\begin{aligned}
\mathbb E\|x_{s,k+1}-x^*\|_2^2
&\le
\mathbb E\|x_{s,k}-x^*\|_2^2\\
&\quad
-2\alpha(1-2L\alpha)
\mathbb E\bigl[f(x_{s,k})-f^*\bigr]\\
&\quad
+4L\alpha^2
\mathbb E\bigl[f(\tilde x_{s-1})-f^*\bigr].
\end{aligned}
$$

对 $k=0,\ldots,T-1$ 求和，并使用

$$
x_{s,0}=\tilde x_{s-1}
$$

以及强凸性给出的

$$
\|\tilde x_{s-1}-x^*\|_2^2
\le
\frac2m
\bigl(f(\tilde x_{s-1})-f^*\bigr),
$$

可得

$$
\begin{aligned}
2\alpha(1-2L\alpha)T\,
\mathbb E\bigl[f(\tilde x_s)-f^*\bigr]
&\le
\left(
\frac2m+4LT\alpha^2
\right)
\mathbb E\bigl[f(\tilde x_{s-1})-f^*\bigr].
\end{aligned}
$$

两边除以 $2\alpha(1-2L\alpha)T$，便得到

$$
\mathbb E\bigl[f(\tilde x_s)-f^*\bigr]
\le
\rho\,
\mathbb E\bigl[f(\tilde x_{s-1})-f^*\bigr],
$$

其中

$$
\rho
=
\frac{1}{m\alpha(1-2L\alpha)T}
+
\frac{2L\alpha}{1-2L\alpha}.
$$

只要 $\rho<1$，就得到按 epoch 计算的线性收敛。

### 9.1 方差界的标准推导

在均匀采样或适当归一化的记号下，可将 $G_{s,k}$ 写成

$$
\begin{aligned}
G_{s,k}
&=
\bigl(\nabla f_{i_k}(x_{s,k})-
\nabla f_{i_k}(x^*)\bigr)\\
&\quad
-
\bigl(\nabla f_{i_k}(\tilde x_{s-1})-
\nabla f_{i_k}(x^*)\bigr)\\
&\quad
+\nabla f(\tilde x_{s-1}).
\end{aligned}
$$

利用

$$
\|a+b\|_2^2\le2\|a\|_2^2+2\|b\|_2^2
$$

以及

$$
\mathbb E\|Z-\mathbb E Z\|_2^2
\le
\mathbb E\|Z\|_2^2,
$$

可得

$$
\begin{aligned}
\mathbb E\|G_{s,k}\|_2^2
&\le
2\mathbb E
\|\nabla f_{i_k}(x_{s,k})-
\nabla f_{i_k}(x^*)\|_2^2\\
&\quad
+2\mathbb E
\|\nabla f_{i_k}(\tilde x_{s-1})-
\nabla f_{i_k}(x^*)\|_2^2.
\end{aligned}
$$

对凸且 $L$-光滑的 $f_i$，有

$$
\|\nabla f_i(x)-\nabla f_i(x^*)\|_2^2
\le
2L\left(
 f_i(x)-f_i(x^*)
-\langle\nabla f_i(x^*),x-x^*\rangle
\right).
$$

对 $i$ 取期望并利用 $\nabla f(x^*)=0$，最终得到

$$
\mathbb E\|G_{s,k}\|_2^2
\le
4L\,
\mathbb E\left[
 f(x_{s,k})-f(x^*)
 +f(\tilde x_{s-1})-f(x^*)
\right].
$$