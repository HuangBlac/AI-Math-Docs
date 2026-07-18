# LFTP 笔记整理：风险分解、优化与数学预备知识

> 来源：手写 PDF《LFTP优化-Ch1，Ch2》共 9 页。  
> 整理说明：第 2 页与第 4 页内容重复，以下只保留一次；对明显的符号遗漏、转置和正负号问题按上下文进行了校正。

## 目录

1. [学习问题中的三类误差](#1-学习问题中的三类误差)
2. [最小二乘问题上的梯度下降](#2-最小二乘问题上的梯度下降)
3. [凸性、光滑性、强凸性与 PL 不等式](#3-凸性光滑性强凸性与-pl-不等式)
4. [线性代数技巧](#4-线性代数技巧)
5. [向量与矩阵函数求导](#5-向量与矩阵函数求导)
6. [标准高斯尾概率的上下界](#6-标准高斯尾概率的上下界)

---

## 1. 学习问题中的三类误差

### 1.1 风险与正则化经验目标

给定预测函数 $f$，总体风险为

```math
R(f)=\mathbb E\bigl[\ell(y,f(x))\bigr].
```

对参数化模型 $f_\theta$，训练时常考虑

```math
F(\theta)
=
\frac1n\sum_{i=1}^n \ell\bigl(y_i,f_\theta(x_i)\bigr)
+\Omega(\theta),
```

其中 $\Omega(\theta)$ 是正则项。若暂时不考虑正则项，则经验风险记为

```math
\widehat R(f)
=
\frac1n\sum_{i=1}^n \ell(y_i,f(x_i)).
```

设模型类为

```math
\mathcal F_\Theta=\{f_\theta:\theta\in\Theta\}.
```

### 1.2 估计误差：统计误差与优化误差

令

```math
\theta^*\in\arg\min_{\theta\in\Theta}R(f_\theta),
```

而 $\widehat\theta$ 是算法实际返回的参数，不一定精确最小化经验风险。则

```math
\begin{aligned}
R(f_{\widehat\theta})-R(f_{\theta^*})
={}&
\bigl[R(f_{\widehat\theta})-\widehat R(f_{\widehat\theta})\bigr]\\
&+\bigl[\widehat R(f_{\widehat\theta})-\widehat R(f_{\theta^*})\bigr]\\
&+\bigl[\widehat R(f_{\theta^*})-R(f_{\theta^*})\bigr].
\end{aligned}
```

因此

```math
R(f_{\widehat\theta})-\inf_{\theta\in\Theta}R(f_\theta)
\le
2\sup_{f\in\mathcal F_\Theta}
\left|R(f)-\widehat R(f)\right|
+
\left[
\widehat R(f_{\widehat\theta})
-
\inf_{\theta\in\Theta}\widehat R(f_\theta)
\right].
```

右侧分为两部分：

- **统计误差** $\displaystyle \operatorname{err}_{\mathrm{stat}} = 2\sup_{f\in\mathcal F_\Theta} \left|R(f)-\widehat R(f)\right|.$

- **优化误差** $\displaystyle \operatorname{err}_{\mathrm{opt}} = \widehat R(f_{\widehat\theta}) - \inf_{\theta\in\Theta}\widehat R(f_\theta).$

统计误差通常由函数类复杂度控制。对有限函数类可以使用集中不等式与并合界；对无限函数类，可使用覆盖数或 Rademacher 复杂度。经过对称化后，常出现形如

```math
2\operatorname{Rad}_n(\mathcal F_\Theta)
```

的控制项，典型样本尺度为 $O(n^{-1/2})$。

实际训练中，$f_{\widehat\theta}$ 往往是由 GD 或 SGD 在有限步后得到的，而不是经验风险的精确极小点。用于泛化误差分析时，通常没有必要把优化误差压得远小于统计误差；令二者达到同一数量级即可。

### 1.3 逼近误差

相对于所有可测预测函数的最优风险，还存在

```math
\operatorname{err}_{\mathrm{approx}}
=
\inf_{\theta\in\Theta}R(f_\theta)
-
\inf_{f}R(f).
```

于是总超额风险可以概括为

```math
\boxed{
R(f_{\widehat\theta})-\inf_f R(f)
\le
\operatorname{err}_{\mathrm{stat}}
+
\operatorname{err}_{\mathrm{opt}}
+
\operatorname{err}_{\mathrm{approx}}.
}
```

三者的含义分别是：

- 统计误差：有限样本导致经验风险偏离总体风险；
- 优化误差：有限计算步数导致未能精确求解经验优化问题；
- 逼近误差：模型类本身不够丰富。

### 1.4 常见优化收敛速度

在相应的标准假设下，常见量级为：

| 算法与条件 | 典型收敛速度 |
|---|---:|
| GD，凸且光滑 | $F(\theta_t)-F^*=O(t^{-1})$ |
| GD，强凸且光滑 | $F(\theta_t)-F^*=O(\rho^t)$，$0<\rho<1$ |
| SGD，一般凸问题 | $O(t^{-1/2})$ |
| SGD，强凸问题 | $O(t^{-1})$ |

---

## 2. 最小二乘问题上的梯度下降

考虑

```math
F(\theta)=\frac1{2n}\|\Phi\theta-y\|_2^2.
```

其梯度和 Hessian 为

```math
\nabla F(\theta)
=
\frac1n\Phi^\top(\Phi\theta-y),
\qquad
\nabla^2F(\theta)
=
H:=\frac1n\Phi^\top\Phi.
```

梯度下降迭代为

```math
\theta_t
=
\theta_{t-1}-\alpha\nabla F(\theta_{t-1}).
```

设 $\theta_*$ 为一个极小点，则 $\nabla F(\theta_*)=0$。因此

```math
\begin{aligned}
\theta_t-\theta_*
&=
\theta_{t-1}-\theta_*
-
\alpha\frac1n\Phi^\top\Phi(\theta_{t-1}-\theta_*)\\
&=(I-\alpha H)(\theta_{t-1}-\theta_*).
\end{aligned}
```

递推得到

```math
\theta_t-\theta_*
=(I-\alpha H)^t(\theta_0-\theta_*).
```

若 $H$ 的特征值位于 $[\mu,L]$，其中 $0<\mu\le L$，则

```math
\|\theta_t-\theta_*\|_2^2
\le
\max_{\lambda\in[\mu,L]}|1-\alpha\lambda|^{2t}
\|\theta_0-\theta_*\|_2^2.
```

### 最优常步长

取

```math
\alpha=\frac{2}{\mu+L},
```

可以平衡区间两端的收缩因子：

```math
\max_{\lambda\in[\mu,L]}|1-\alpha\lambda|
=
\frac{L-\mu}{L+\mu}.
```

令条件数

```math
\kappa=\frac{L}{\mu},
```

则

```math
\|\theta_t-\theta_*\|_2^2
\le
\left(\frac{\kappa-1}{\kappa+1}\right)^{2t}
\|\theta_0-\theta_*\|_2^2.
```

进一步，

```math
\left(\frac{\kappa-1}{\kappa+1}\right)^{2t}
\le
\left(1-\frac1\kappa\right)^{2t}
\le
\exp\left(-\frac{2t}{\kappa}\right).
```

因此条件数越大，收敛越慢；当 $\kappa$ 有界时，梯度下降呈线性（几何）收敛。

---

## 3. 凸性、光滑性、强凸性与 PL 不等式

### 3.1 凸函数

若 $F$ 可微，则凸性等价于

```math
F(\eta)
\ge
F(\theta)
+
\nabla F(\theta)^\top(\eta-\theta).
```

取 $\eta=\theta_*$ 可得

```math
F(\theta)-F(\theta_*)
\le
\nabla F(\theta)^\top(\theta-\theta_*).
```

### 3.2 $L$-光滑

$F$ 为 $L$-光滑，意味着

```math
F(\eta)
\le
F(\theta)
+
\nabla F(\theta)^\top(\eta-\theta)
+
\frac L2\|\eta-\theta\|_2^2.
```

### 3.3 $\mu$-强凸

$F$ 为 $\mu$-强凸，意味着

```math
F(\eta)
\ge
F(\theta)
+
\nabla F(\theta)^\top(\eta-\theta)
+
\frac\mu2\|\eta-\theta\|_2^2.
```

### 3.4 Łojasiewicz / Polyak–Łojasiewicz 不等式

强凸函数满足

```math
\boxed{
\|\nabla F(\theta)\|_2^2
\ge
2\mu\bigl(F(\theta)-F^*\bigr).
}
```

证明：由强凸性，对任意 $\eta$，

```math
F(\eta)
\ge
F(\theta)
+
\nabla F(\theta)^\top(\eta-\theta)
+
\frac\mu2\|\eta-\theta\|_2^2.
```

右侧关于 $\eta$ 的二次函数在

```math
\widetilde\eta
=
\theta-\frac1\mu\nabla F(\theta)
```

处取最小值。代入得

```math
F(\widetilde\eta)
\ge
F(\theta)-\frac1{2\mu}\|\nabla F(\theta)\|_2^2.
```

更直接地，对上式两端关于 $\eta$ 取下确界：

```math
F^*
\ge
F(\theta)-\frac1{2\mu}\|\nabla F(\theta)\|_2^2,
```

整理即得结论。

---

## 4. 线性代数技巧

### 4.1 秩一扰动矩阵的逆

设 $\mathbf 1_n\in\mathbb R^n$ 为全 1 向量，且

```math
1+n\alpha\ne0.
```

则

```math
\boxed{
(I+\alpha\mathbf 1_n\mathbf 1_n^\top)^{-1}
=
I-
\frac{\alpha}{1+n\alpha}
\mathbf 1_n\mathbf 1_n^\top.
}
```

理由是：

- 在 $\operatorname{span}\{\mathbf 1_n\}$ 上，矩阵的特征值为 $1+n\alpha$；
- 在 $\mathbf 1_n^\perp$ 上，特征值为 $1$。

也可以直接将候选逆矩阵与原矩阵相乘验证。

这是 Sherman–Morrison / Woodbury 公式的一个特例。

### 4.2 Schur 补与分块矩阵求逆

设

```math
M=
\begin{pmatrix}
A&B\\
C&D
\end{pmatrix}.
```

若 $A$ 可逆，定义 $A$ 的 Schur 补

```math
M/A=D-CA^{-1}B.
```

若 $D$ 可逆，定义 $D$ 的 Schur 补

```math
M/D=A-BD^{-1}C.
```

#### 以 $A$ 为主块的分解

若 $A$ 与 $M/A$ 均可逆，则

```math
M
=
\begin{pmatrix}
I&0\\
CA^{-1}&I
\end{pmatrix}
\begin{pmatrix}
A&0\\
0&M/A
\end{pmatrix}
\begin{pmatrix}
I&A^{-1}B\\
0&I
\end{pmatrix}.
```

因此

```math
M^{-1}
=
\begin{pmatrix}
I&-A^{-1}B\\
0&I
\end{pmatrix}
\begin{pmatrix}
A^{-1}&0\\
0&(M/A)^{-1}
\end{pmatrix}
\begin{pmatrix}
I&0\\
-CA^{-1}&I
\end{pmatrix},
```

即

```math
\boxed{
M^{-1}
=
\begin{pmatrix}
A^{-1}+A^{-1}B(M/A)^{-1}CA^{-1}
&-A^{-1}B(M/A)^{-1}\\
-(M/A)^{-1}CA^{-1}
&(M/A)^{-1}
\end{pmatrix}.
}
```

#### 以 $D$ 为主块的公式

若 $D$ 与 $M/D$ 均可逆，则

```math
\boxed{
M^{-1}
=
\begin{pmatrix}
(M/D)^{-1}
&-(M/D)^{-1}BD^{-1}\\
-D^{-1}C(M/D)^{-1}
&D^{-1}+D^{-1}C(M/D)^{-1}BD^{-1}
\end{pmatrix}.
}
```

#### Woodbury 型恒等式

比较上述两个分块逆公式，可得

```math
(A-BD^{-1}C)^{-1}
=
A^{-1}
+A^{-1}B(D-CA^{-1}B)^{-1}CA^{-1},
```

以及

```math
(D-CA^{-1}B)^{-1}
=
D^{-1}
+D^{-1}C(A-BD^{-1}C)^{-1}BD^{-1}.
```

常用特例为

```math
\boxed{
(I+BB^\top)^{-1}
=
I-B(I+B^\top B)^{-1}B^\top.
}
```

右乘 $B$ 后还有

```math
(I+BB^\top)^{-1}B
=
B(I+B^\top B)^{-1}.
```

### 4.3 分块行列式

在上述可逆条件下，

```math
\boxed{
\det M
=
\det(A)\det(M/A)
=
\det(D)\det(M/D).
}
```

### 4.4 高斯向量的条件均值与条件协方差

若联合高斯向量

```math
\begin{pmatrix}x\\y\end{pmatrix}
\sim
\mathcal N\left(
\begin{pmatrix}\mu_x\\\mu_y\end{pmatrix},
\begin{pmatrix}
\Sigma_{xx}&\Sigma_{xy}\\
\Sigma_{yx}&\Sigma_{yy}
\end{pmatrix}
\right),
```

则给定 $x=x'$ 后，

```math
\boxed{
\mu_{y\mid x'}
=
\mu_y+
\Sigma_{yx}\Sigma_{xx}^{-1}(x'-\mu_x),
}
```

```math
\boxed{
\Sigma_{y\mid x}
=
\Sigma_{yy}
-
\Sigma_{yx}\Sigma_{xx}^{-1}\Sigma_{xy}.
}
```

条件协方差正是一个 Schur 补。

### 4.5 SVD 与特征值分解

设 $X$ 的薄 SVD 为

```math
X=U\Sigma V^\top
=
\sum_{i=1}^r\sigma_i u_i v_i^\top.
```

于是

```math
XX^\top
=U\Sigma^2U^\top
=
\sum_{i=1}^r\sigma_i^2u_i u_i^\top,
```

```math
X^\top X
=V\Sigma^2V^\top
=
\sum_{i=1}^r\sigma_i^2v_i v_i^\top.
```

因此：

- $u_i$ 是 $XX^\top$ 的特征向量，特征值为 $\sigma_i^2$；
- $v_i$ 是 $X^\top X$ 的特征向量，特征值为 $\sigma_i^2$。

再考虑对称扩张

```math
\mathcal M
=
\begin{pmatrix}
0&X\\
X^\top&0
\end{pmatrix}.
```

由 $Xv_i=\sigma_i u_i$、$X^\top u_i=\sigma_i v_i$，有

```math
\mathcal M
\frac1{\sqrt2}
\begin{pmatrix}u_i\\v_i\end{pmatrix}
=
\sigma_i
\frac1{\sqrt2}
\begin{pmatrix}u_i\\v_i\end{pmatrix},
```

```math
\mathcal M
\frac1{\sqrt2}
\begin{pmatrix}u_i\\-v_i\end{pmatrix}
=
-\sigma_i
\frac1{\sqrt2}
\begin{pmatrix}u_i\\-v_i\end{pmatrix}.
```

因此 $\mathcal M$ 的非零特征值为奇异值 $\sigma_i$ 及其相反数 $-\sigma_i$。

---

## 5. 向量与矩阵函数求导

以下使用 Frobenius 内积

```math
\langle A,B\rangle_F=\operatorname{tr}(A^\top B),
```

并通过

```math
df(X)=\langle \nabla_X f(X),dX\rangle_F
```

识别梯度。

### 5.1 二次型

设

```math
F(\theta)
=
\frac12\theta^\top A\theta-b^\top\theta.
```

则

```math
\boxed{
\nabla F(\theta)
=
\frac12(A+A^\top)\theta-b,
}
```

```math
\boxed{
\nabla^2F(\theta)
=
\frac12(A+A^\top).
}
```

若 $A=A^\top$，则简化为

```math
\nabla F(\theta)=A\theta-b,
\qquad
\nabla^2F(\theta)=A.
```

### 5.2 最小二乘

```math
F(\theta)
=
\frac1{2n}\|y-X\theta\|_2^2.
```

展开为

```math
F(\theta)
=
\frac1{2n}
\left(
 y^\top y-2y^\top X\theta+\theta^\top X^\top X\theta
\right).
```

因此

```math
\boxed{
\nabla F(\theta)
=
-\frac1nX^\top(y-X\theta)
=
\frac1nX^\top(X\theta-y),
}
```

```math
\boxed{
\nabla^2F(\theta)
=
\frac1nX^\top X.
}
```

### 5.3 Logistic 回归

令 $x_i^\top$ 为 $X$ 的第 $i$ 行，$y_i\in\{-1,1\}$，并定义

```math
F(\theta)
=
\frac1n\sum_{i=1}^n
\log\left(1+\exp(-y_ix_i^\top\theta)\right).
```

记

```math
\varphi(t)=\log(1+e^t),
\qquad
\varphi'(t)=\sigma(t)=\frac1{1+e^{-t}},
```

以及

```math
\varphi''(t)
=
\sigma(t)\sigma(-t).
```

对第 $i$ 项求导：

```math
\nabla_\theta
\varphi(-y_ix_i^\top\theta)
=
-y_i\sigma(-y_ix_i^\top\theta)x_i.
```

定义 $g\in\mathbb R^n$：

```math
g_i
=-y_i\sigma(-y_ix_i^\top\theta),
```

则

```math
\boxed{
\nabla F(\theta)
=
\frac1nX^\top g.
}
```

再定义

```math
h_i
=
\sigma(y_ix_i^\top\theta)
\sigma(-y_ix_i^\top\theta),
```

则

```math
\boxed{
\nabla^2F(\theta)
=
\frac1nX^\top\operatorname{Diag}(h)X.
}
```

由于 $h_i\ge0$，Hessian 半正定，所以 Logistic 回归目标是凸函数。

### 5.4 常见迹函数

#### 线性迹函数

若

```math
f(X)=\operatorname{tr}(A^\top X),
```

则

```math
df=\operatorname{tr}(A^\top dX)
=\langle A,dX\rangle_F,
```

故

```math
\boxed{\nabla_X f(X)=A.}
```

若

```math
f(X)=\operatorname{tr}(AXB),
```

利用迹的循环不变性，

```math
df
=\operatorname{tr}(A\,dX\,B)
=\operatorname{tr}(BA\,dX),
```

故

```math
\boxed{
\nabla_X f(X)=A^\top B^\top.
}
```

#### 矩阵二次型

若

```math
f(X)=\operatorname{tr}(X^\top AX),
```

则

```math
\boxed{
\nabla_X f(X)=AX+A^\top X.
}
```

若 $A$ 对称，则

```math
\nabla_X f(X)=2AX.
```

更一般地，若

```math
f(X)=\operatorname{tr}(X^\top A X B),
```

则

```math
\boxed{
\nabla_X f(X)=AXB+A^\top X B^\top.
}
```

### 5.5 逆矩阵的微分

由

```math
XX^{-1}=I
```

两侧求微分：

```math
(dX)X^{-1}+X\,d(X^{-1})=0.
```

因此

```math
\boxed{
d(X^{-1})
=-X^{-1}(dX)X^{-1}.
}
```

### 5.6 $\operatorname{tr}(AX^{-1})$ 的梯度

令

```math
f(X)=\operatorname{tr}(AX^{-1}).
```

则

```math
\begin{aligned}
df
&=\operatorname{tr}\bigl(A\,d(X^{-1})\bigr)\\
&=-\operatorname{tr}\bigl(AX^{-1}(dX)X^{-1}\bigr)\\
&=-\operatorname{tr}\bigl(X^{-1}AX^{-1}dX\bigr).
\end{aligned}
```

所以一般情形下

```math
\boxed{
\nabla_X f(X)
=-X^{-\top}A^\top X^{-\top}.
}
```

若 $A$ 与 $X$ 均为对称矩阵，则

```math
\boxed{
\nabla_X\operatorname{tr}(AX^{-1})
=-X^{-1}AX^{-1}.
}
```

### 5.7 行列式与对数行列式

Jacobi 公式为

```math
\boxed{
d\det X
=
\det X\,\operatorname{tr}(X^{-1}dX).
}
```

可由

```math
\det(X+tH)
=
\det X\,\det(I+tX^{-1}H)
```

以及

```math
\left.\frac{d}{dt}\det(I+tB)\right|_{t=0}
=\operatorname{tr}(B)
```

得到。

因此

```math
\boxed{
\nabla_X\det X
=
\det(X)X^{-\top}.
}
```

进一步，

```math
d\log\det X
=
\operatorname{tr}(X^{-1}dX),
```

故

```math
\boxed{
\nabla_X\log\det X
=X^{-\top}.
}
```

若变量限制在可逆对称矩阵上，则分别写为

```math
\nabla_X\det X=\det(X)X^{-1},
\qquad
\boxed{
\nabla_X\log\det X=X^{-1}.
}
```

---

## 6. 标准高斯尾概率的上下界

设

```math
Z\sim\mathcal N(0,1),
\qquad
\phi(x)=\frac1{\sqrt{2\pi}}e^{-x^2/2}.
```

目标是证明，对任意 $t>0$，

```math
\boxed{
\frac14e^{-t^2}
\le
\mathbb P(Z>t)
\le
 e^{-t^2/2}.
}
```

### 6.1 上界

对任意 $s>0$，由 Chernoff 方法，

```math
\mathbb P(Z>t)
=
\mathbb P(e^{sZ}>e^{st})
\le
 e^{-st}\mathbb E[e^{sZ}].
```

标准高斯的矩母函数为

```math
\mathbb E[e^{sZ}]=e^{s^2/2}.
```

因此

```math
\mathbb P(Z>t)
\le
\exp\left(-st+\frac{s^2}{2}\right).
```

取 $s=t$ 得

```math
\mathbb P(Z>t)
\le
 e^{-t^2/2}.
```

### 6.2 下界：$0\le t\le1$

因为 $\phi(x)\le\phi(0)=1/\sqrt{2\pi}$，所以

```math
\mathbb P(Z>t)
=
\frac12-\int_0^t\phi(x)\,dx
\ge
\frac12-\frac{t}{\sqrt{2\pi}}.
```

只需证明

```math
\frac12-\frac{t}{\sqrt{2\pi}}
\ge
\frac14e^{-t^2}.
```

定义

```math
f(t)
=
\frac12-\frac{t}{\sqrt{2\pi}}
-
\frac14e^{-t^2}.
```

则

```math
f'(t)
=-\frac1{\sqrt{2\pi}}
+
\frac t2e^{-t^2}.
```

函数 $te^{-t^2}$ 在 $t=1/\sqrt2$ 处达到最大值 $1/\sqrt{2e}$，故

```math
\frac t2e^{-t^2}
\le
\frac1{2\sqrt{2e}}
<
\frac1{\sqrt{2\pi}}.
```

所以 $f'(t)<0$。于是 $f$ 在 $[0,1]$ 上递减，而

```math
f(1)
=
\frac12-\frac1{\sqrt{2\pi}}-\frac1{4e}>0.
```

故 $f(t)>0$，从而

```math
\mathbb P(Z>t)
\ge
\frac14e^{-t^2},
\qquad 0\le t\le1.
```

### 6.3 下界：$t>1$

记

```math
Q(t)=\mathbb P(Z>t)=\int_t^\infty\phi(x)\,dx.
```

利用 $\phi'(x)=-x\phi(x)$，分部积分得

```math
\begin{aligned}
Q(t)
&=
\int_t^\infty \frac1x\,x\phi(x)\,dx\\
&=-\int_t^\infty\frac1x\phi'(x)\,dx\\
&=
\frac{\phi(t)}{t}
-
\int_t^\infty\frac{\phi(x)}{x^2}\,dx.
\end{aligned}
```

当 $x\ge t$ 时，$x^{-2}\le t^{-2}$，因此

```math
Q(t)
\ge
\frac{\phi(t)}t-\frac{Q(t)}{t^2}.
```

整理得到经典 Mills 比下界

```math
\boxed{
Q(t)
\ge
\frac{t}{1+t^2}\phi(t)
=
\frac{t}{\sqrt{2\pi}(1+t^2)}e^{-t^2/2}.
}
```

最后只需验证，对 $t\ge1$，

```math
\frac{t}{\sqrt{2\pi}(1+t^2)}e^{-t^2/2}
\ge
\frac14e^{-t^2}.
```

等价于

```math
G(t)
:=
\frac{4t}{\sqrt{2\pi}(1+t^2)}e^{t^2/2}
\ge1.
```

其对数导数为

```math
\frac{d}{dt}\log G(t)
=
\frac1t-\frac{2t}{1+t^2}+t
=
\frac{1+t^4}{t(1+t^2)}>0.
```

所以 $G$ 在 $[1,\infty)$ 上递增，并且

```math
G(1)
=
\sqrt{\frac{2e}{\pi}}>1.
```

故对所有 $t>1$，同样有

```math
\mathbb P(Z>t)
\ge
\frac14e^{-t^2}.
```

综上，

```math
\boxed{
\frac14e^{-t^2}
\le
\mathbb P(Z>t)
\le
 e^{-t^2/2},
\qquad t>0.
}
```
