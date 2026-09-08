# Ch7.5 泛化保证与逼近误差

> 状态：`note_unverified`。由《7.4.3 Random Feature.pdf》第 2–7 页整理，对应锁定教材印刷页 202–207（PDF 第 218–223 页）。按既有推导整理难辨系数和归一化；Ex 7.21 与延拓构造保留未写状态。

## 1. 两种经验风险问题

设损失对预测值为 $G$-Lipschitz，核满足 $\sup_x k(x,x)\le R^2$，总体风险最小化函数 $f_*\in L^2(P_X)$。讨论约束问题

```math
\widehat f_D^{(c)}\in\arg\min_{\|f\|_{\mathcal H}\le D}
\frac1n\sum_i\ell(y_i,f(x_i))
```

与正则化问题

```math
\widehat f_\lambda^{(r)}\in\arg\min_{f\in\mathcal H}
\left\{\frac1n\sum_i\ell(y_i,f(x_i))+\frac\lambda2\|f\|_{\mathcal H}^2\right\}.
```

Lipschitz 性和 Cauchy–Schwarz 给出

```math
R(f)-R(f_*)\le G\mathbb E|f(X)-f_*(X)|
\le G\|f-f_*\|_{L^2(P_X)}.
```

因此可以用函数逼近误差控制超额风险。

## 2. 约束问题的风险分解

原稿记录的 Rademacher 界为

```math
\mathbb E R(\widehat f_D^{(c)})-R(f_*)
\le\frac{4GRD}{\sqrt n}
+G\inf_{\|f\|_{\mathcal H}\le D}\|f-f_*\|_{L^2(P_X)}.
```

第一项随允许范数 D 增大，第二项则随函数类扩大而减小。对 D 优化相当于

```math
\begin{aligned}
\inf_{D\ge0}\left\{\frac{4GRD}{\sqrt n}+G\inf_{\|f\|_{\mathcal H}\le D}\|f-f_*\|_2\right\}
&=G\inf_{f\in\mathcal H}\left\{\frac{4R\|f\|_{\mathcal H}}{\sqrt n}+\|f-f_*\|_2\right\}\\
&\le G\sqrt{2\inf_{f\in\mathcal H}\left\{\|f-f_*\|_2^2+\frac{16R^2}{n}\|f\|_{\mathcal H}^2\right\}}.
\end{aligned}
```

其中 $\|\cdot\|_2$ 暂指 $L^2(P_X)$ 范数。定义

```math
A(\mu,f_*)=\inf_{f\in\mathcal H}
\left\{\|f-f_*\|_{L^2(P_X)}^2+\mu\|f\|_{\mathcal H}^2\right\}.
```

这个量同时记录逼近精度与所需 RKHS 范数。

### 2.1 三种情况

- 若 $f_*\in\mathcal H$，代入 $f=f_*$ 得 $A(\mu,f_*)\le\mu\|f_*\|_{\mathcal H}^2$，对应 $O(n^{-1/2})$ 的风险界。原稿这里写成等号，整理为代入候选函数所得的上界。
- 若 $f_*\notin\mathcal H$，但属于它在 $L^2(P_X)$ 中的闭包，则 $A(\mu,f_*)\to0$；没有额外条件时不指定速率。
- 若 $f_*$ 不属于该闭包，记 $\Pi f_*$ 为正交投影，则

```math
A(\mu,f_*)=A(\mu,\Pi f_*)+\|f_*-\Pi f_*\|_{L^2(P_X)}^2.
```

第二项是函数类无法消除的误差。

## 3. 正则化问题

原稿记录

```math
\mathbb E R(\widehat f_\lambda^{(r)})-R(f_*)
\le\frac{24G^2R^2}{\lambda n}
+\inf_{f\in\mathcal H}\left\{G\|f-f_*\|_2+\frac\lambda2\|f\|_{\mathcal H}^2\right\}.
```

对上界中的 λ 与 f 联合优化，原稿难辨的系数按同一计算整理为

```math
G\inf_{f\in\mathcal H}\left\{\|f-f_*\|_2+\frac{4\sqrt3R}{\sqrt n}\|f\|_{\mathcal H}\right\}
\le G\sqrt{2\inf_{f\in\mathcal H}\left\{\|f-f_*\|_2^2+\frac{48R^2}{n}\|f\|_{\mathcal H}^2\right\}}.
```

两种问题都归结为研究 $A(\mu,f_*)$。这里是在优化理论上界，不是已经从数据确定了可直接使用的最优参数。

## 4. 平移不变核下的显式逼近量

假设 $P_X$ 有密度，并且

```math
\|f-f_*\|_{L^2(P_X)}^2\le\frac C{r^d}\|f-f_*\|_{L^2(\mathbb R^d)}^2,
\qquad C=r^d\left\|\frac{dP_X}{dx}\right\|_\infty.
```

引入带有尺度归一化的量

```math
\widetilde A(\mu,f_*)=
\inf_{f\in\mathcal H}\left\{r^{-d}\|f-f_*\|_{L^2(\mathbb R^d)}^2+\mu\|f\|_{\mathcal H}^2\right\}.
```

按这一定义，$A(\mu,f_*)\le C\widetilde A(\mu/C,f_*)$；这一步只整理原稿的 C 与 μ 缩放。

设 $k(x,x')=g(x-x')$，采用[上一篇](ch7.3-7.4-kernels-algorithms.md)的 Fourier 约定与范数表达式，有

```math
\widetilde A(\mu,f_*)=
\inf_{\widehat f}\frac1{(2\pi)^d}\int
\left\{r^{-d}|\widehat f(\omega)-\widehat f_*(\omega)|^2
+\mu\frac{|\widehat f(\omega)|^2}{\widehat g(\omega)}\right\}d\omega.
```

原稿已记录逐频率二次优化后的表达式：

```math
\widetilde A(\mu,f_*)=
\frac1{(2\pi r)^d}\int|\widehat f_*(\omega)|^2
\frac{\mu r^d}{\widehat g(\omega)+\mu r^d}\,d\omega.
```

这里的外因子是 $(2\pi r)^{-d}$，与前面的 $r^{-d}$ 一致。原稿后面的 Sobolev 式漏写过 r，本篇统一保留。

## 5. Sobolev 光滑性与 Matérn 核

记归一化 Sobolev 平方范数

```math
S_{t,r}(f_*)^2=\frac1{(2\pi r)^d}\int
(1+r^2\|\omega\|_2^2)^t|\widehat f_*(\omega)|^2\,d\omega<\infty.
```

原稿将逼近量界为

```math
\widetilde A(\mu,f_*)\le S_{t,r}(f_*)^2
\sup_{\omega\in\mathbb R^d}
\left\{\frac{\mu r^d}{\widehat g(\omega)+\mu r^d}
\frac1{(1+r^2\|\omega\|_2^2)^t}\right\}.
```

对谱密度 $\widehat g(\omega)\asymp r^d(1+r^2\|\omega\|_2^2)^{-s}$ 的 Matérn 核，取 $s>d/2$：

- $t\ge s$ 时，$f_*\in\mathcal H$，$\widetilde A(\mu,f_*)\le\mu\|f_*\|_{\mathcal H}^2$。
- $0<t<s$ 时，令 $\theta=t/s$。使用原稿已有的不等式

```math
a+b\ge\theta a+(1-\theta)b\ge a^\theta b^{1-\theta},
```

从而

```math
\frac{\mu r^d}{\widehat g(\omega)+\mu r^d}
\le\frac{\mu r^d}{\widehat g(\omega)^{t/s}(\mu r^d)^{1-t/s}}.
```

与 Sobolev 权重相消后，得到 $\widetilde A(\mu,f_*)=O(\mu^{t/s})$。这整理了原稿第 4 页已写的估计路线。

### Exercise 7.21：只记录题意 {#ex-7-21}

原稿第 5 页只有：

> Ex 7.21 $f^*$ 的同样假设，但使用高斯核，$\widetilde A(\mu,f)$。

其余整页留白。这里不添加高斯核的逼近界或解答。

## 6. 从逼近误差界换成所需范数

原稿第 6 页考虑：已知 $A(\mu,f_*)\le c\mu^\alpha$，$0<\alpha<1$，若希望逼近误差不超过 ε，需要多大的 RKHS 范数？

按原稿的 Lagrange 对偶形式，在相应强对偶条件下，

```math
\begin{aligned}
\inf_{\|f-f_*\|_2\le\varepsilon}\|f\|_{\mathcal H}^2
&=\sup_{\nu\ge0}\{\nu A(\nu^{-1},f_*)-\nu\varepsilon^2\}\\
&\le\sup_{\nu\ge0}\{c\nu^{1-\alpha}-\nu\varepsilon^2\}.
\end{aligned}
```

把原稿与参数 μ 重名的乘子改为 ν。其驻点关系为 $(1-\alpha)c\nu^{-\alpha}=\varepsilon^2$，对应范数平方量级 $\varepsilon^{-2(1-\alpha)/\alpha}$。取 $\alpha=t/s$，范数量级为 $\varepsilon^{1-s/t}$。

原稿没有讨论对偶成立条件或范数下确界是否取到，本篇不扩写这些证明。

## 7. Lipschitz 函数与 Sobolev 空间：延拓仍未写

原稿希望把定义在 $B(0,r)\subset\mathbb R^d$ 上的 D-Lipschitz 函数延拓到整个空间。还假设 $|f(0)|\le rD$，目标是找到 g，使

```math
S_{1,r}(g)^2
=\frac1{r^d}\int_{\mathbb R^d}\bigl(|g(x)|^2+r^2\|\nabla g(x)\|_2^2\bigr)dx
\le c_dr^2D^2.
```

这是原稿第 6–7 页的目标范数，不是已经完成的构造。

原稿第 7 页接着写：

> 为什么可以这么做？！
>
> 我们定义函数 g

**原始完成状态：未完成。** 没有 g 的定义、延拓步骤或范数证明，本次均不补写。

原稿第 6 页末尾的 $O(n^{-1/(d+1)})$ 按上下文整理为：对于一阶 Sobolev 正则性 $t=1$、核阶数 $s=(d+1)/2$，前述 Lipschitz 损失分析给出该量级；若要用于球上的 Lipschitz 函数，仍需先完成这里的延拓步骤。
