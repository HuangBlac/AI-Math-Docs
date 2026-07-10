LFTP：Rademacher复杂度

为什么要引入这个东西：

因为我们估计$\mathcal R(f)-\mathcal R(\hat{f})$,已经将其转化为了$sup_{f\in\mathcal{F}}\mathcal R(f)-\mathcal{\hat R}(f)$这个统计量的估计

也就是要讨论对于一个函数类（取决于不同的学习算法，例如神经网络函数类，决策树学习类，线性回归函数类）
$$
sup E(h(z))-\frac{1}{n}\sum_{i=1}^n h(z_i)
$$
我们可以通过定义函数类$\mathcal H$的复杂度,数据类$D = \{z1, . . . , zn\}$,复杂度$R_n(\mathcal H)$
$$
R_n(\mathcal H) = E_{ε,D}[sup_{h∈\mathcal{H}}\frac{1}{n}\sum^n_{i=1}ε_ih(zi)]
$$
$h_0 : Z → R, R_n(H + {h_0}) = R_n(H)$因为$R_n(\{h_0\})=E_{ε,D}[\frac{1}{n}\sum^n_{i=1}ε_i h_0(z_i)]=0$

因为单元素函数类没有真正的 supremum 可取：
$$
R_n(\{h_0\})
=
\mathbb E_{z,\varepsilon}
\left[
\sup_{h\in\{h_0\}}
\frac1n\sum_{i=1}^n \varepsilon_i h(z_i)
\right]
=
\mathbb E_{z,\varepsilon}
\left[
\frac1n\sum_{i=1}^n \varepsilon_i h_0(z_i)
\right].
$$
对固定的样本 $z_1,\dots,z_n$，有
$$
\mathbb E_\varepsilon
\left[
\frac1n\sum_{i=1}^n \varepsilon_i h_0(z_i)
\right]
=
\frac1n\sum_{i=1}^n h_0(z_i)\mathbb E[\varepsilon_i]
=0.
$$
所以再对 $z$ 取期望仍然是
$$
R_n(\{h_0\})=0.
$$
同理，经验 Rademacher complexity 也是
$$
\widehat R_n(\{h_0\})
=
\mathbb E_\varepsilon
\left[
\frac1n\sum_{i=1}^n \varepsilon_i h_0(z_i)
\right]
=0.
$$
此外，$R_n(H + H') = R_n(H)+R_n(H'),H+H' = \{h_1+h_2|h_1\in H,h_2\in H'\}$

固定样本 $z_1,\dots,z_n$ 和 Rademacher 符号 $\varepsilon_1,\dots,\varepsilon_n$，定义一个线性泛函
$$
L(h)
=
\frac1n\sum_{i=1}^n \varepsilon_i h(z_i).
$$
Rademacher complexity 里面就是在算
$$
\sup_{h\in\mathcal H}L(h)
$$
然后对样本和 $\varepsilon$ 取期望。

现在看凸包。任取
$$
g\in \operatorname{conv}(\mathcal H),
$$
则存在
$$
h_1,\dots,h_m\in\mathcal H,\qquad
\alpha_j\ge 0,\qquad
\sum_{j=1}^m\alpha_j=1,
$$
使得
$$
g=\sum_{j=1}^m\alpha_j h_j.
$$
于是
$$
\begin{aligned}
L(g)
&=
L\left(\sum_{j=1}^m\alpha_j h_j\right)\\
&=
\sum_{j=1}^m\alpha_j L(h_j)\\
&\le
\sum_{j=1}^m\alpha_j \sup_{h\in\mathcal H}L(h)\\
&=
\sup_{h\in\mathcal H}L(h).
\end{aligned}
$$
所以
$$
\sup_{g\in\operatorname{conv}(\mathcal H)}L(g)
\le
\sup_{h\in\mathcal H}L(h).
$$
反过来，因为
$$
\mathcal H\subset \operatorname{conv}(\mathcal H),
$$
所以显然有
$$
\sup_{g\in\operatorname{conv}(\mathcal H)}L(g)
\ge
\sup_{h\in\mathcal H}L(h).
$$
两边合起来：
$$
\sup_{g\in\operatorname{conv}(\mathcal H)}
\frac1n\sum_{i=1}^n\varepsilon_i g(z_i)
=
\sup_{h\in\mathcal H}
\frac1n\sum_{i=1}^n\varepsilon_i h(z_i).
$$
最后对 $z,\varepsilon$ 取期望，就得到
$$
R_n(\operatorname{conv}(\mathcal H))
=
R_n(\mathcal H).
$$
Massart lemma：

如果这个函数类能够造出界$sup_{h\in \mathcal{H}}\sum_{i=1}^nh(x_i)^2\le R^2$此时$R_n(\mathcal{H})\le\sqrt{\frac{2log m}{n}}R$

接下来，我们可以证明：
$$
E\{sup_{h\in\mathcal H} \{|E(h(z))-\frac{1}{n}\sum_{i=1}^n h(z_i)|\}\}\le2R_n(\mathcal H)
$$
我们分别证明：

$E\{sup_{h\in\mathcal H} \{E(h(z))-\frac{1}{n}\sum_{i=1}^n h(z_i)\}\}\le2R_n(\mathcal H)$,$E\{sup_{h\in\mathcal H} \{\frac{1}{n}\sum_{i=1}^n h(z_i)-E[h(z)]\}\}\le2R_n(\mathcal H)$

考虑一组同分布的数据$\mathcal D'=\{z'_1,z_2'\cdots,z_n'\}$

因此，我们可以将期望转化为需样本的条件期望
$$
E\{sup_{h\in\mathcal H} \{E(h(z))-\frac{1}{n}\sum_{i=1}^n h(z_i)\}\}=E\{sup_{h\in\mathcal H} \{E[\frac{1}{n}\sum_{i=1}^n h(z'_i)|\mathcal D]-\frac{1}{n}\sum_{i=1}^n h(z_i)\}\}\\
\le E[sup_{h\in\mathcal H}E[\frac{1}{n}\sum_{i=1}^nh(z'_i)-h(z_i)|\mathcal D]]\\
\le E[E[sup_{h\in\mathcal H}\frac{1}{n}\sum_{i=1}^nh(z'_i)-h(z_i)|\mathcal D]]\\
\le E[sup_{h\in \mathcal H}\sum_{i=1}^n\{h(z'_i)-h(z_i)\}]
$$
而同理可得，
$$
E[sup_{h\in\mathcal H} \{\frac{1}{n}\sum_{i=1}^n h(z_i)-E(h(z))\}]\le E[sup_{h\in \mathcal H}\sum_{i=1}^n\{h(z_i)-h(z'_i)\}]
$$
接下来，我们又可以根据对称性知道：
$$
E[sup_{h\in \mathcal H}\frac{1}{n}\sum_{i=1}^n\{h(z'_i)-h(z_i)\}]\\
=E[sup_{h\in \mathcal H}\frac{1}{n}\sum_{i=1}^n\varepsilon_i\{h(z'_i)-h(z_i)\}]\\
\le E[sup_{h\in \mathcal H}\frac{1}{n}\sum_{i=1}^n\varepsilon_i\{h(z'_i)-h(z_i)\}]\\
\le E[sup_{h\in \mathcal H}\frac{1}{n}\sum_{i=1}^n\varepsilon_ih(z'_i)]+E[sup_{h\in \mathcal H}\frac{1}{n}\sum_{i=1}^n-\varepsilon_ih(z_i)] \\
\le 2R_n(\mathcal{H})
$$
众所周知，期望可以按照概率被处理，使用集中不等式使用最大值+$\delta$小量可以让不等式按照$1-\delta$概率成立

若
$$
h(z)\in[0,\ell_\infty],
$$
则以概率至少 $1-\delta$，对所有 $h\in\mathcal H$，
$$
\mathbb E[h(z)]
\le
\frac1n\sum_{i=1}^n h(z_i)
+
2R_n(\mathcal H)
+
\frac{\ell_\infty}{\sqrt{2n}}
\sqrt{\log\frac1\delta}.
$$
给定任意函数
$$
a_i:\Theta\to \mathbb R,
$$
以及 1-Lipschitz 函数
$$
\varphi_i:\mathbb R\to \mathbb R,
$$
则
$$
\mathbb E_\varepsilon
\left[
\sup_{\theta\in\Theta}
\left\{
b(\theta)
+
\sum_{i=1}^n \varepsilon_i
\varphi_i(a_i(\theta))
\right\}
\right]
\le
\mathbb E_\varepsilon
\left[
\sup_{\theta\in\Theta}
\left\{
b(\theta)
+
\sum_{i=1}^n \varepsilon_i
a_i(\theta)
\right\}
\right].
$$
它的意思是：

> 对函数值先做一个 1-Lipschitz 变换，不会增加 Rademacher complexity。

因为 Lipschitz 函数不会把距离放大，所以它不会让函数类更容易拟合随机符号：

记
$$
B(\theta)
=
b(\theta)
+
\sum_{i=1}^n \varepsilon_i\varphi_i(a_i(\theta)).
$$
考虑第 $n+1$ 个 Rademacher 符号。对 $\varepsilon_{n+1}$ 显式取期望：
$$
\begin{aligned}
&\mathbb E_{\varepsilon_{n+1}}
\left[
\sup_\theta
\left\{
B(\theta)
+
\varepsilon_{n+1}
\varphi_{n+1}(a_{n+1}(\theta))
\right\}
\right] \\
&=
\frac12
\sup_\theta
\{B(\theta)+\varphi_{n+1}(a_{n+1}(\theta))\}
+
\frac12
\sup_{\theta'}
\{B(\theta')-\varphi_{n+1}(a_{n+1}(\theta'))\}.
\end{aligned}
$$
把两个 supremum 合并成对 $(\theta,\theta')$ 的 supremum：
$$
=
\sup_{\theta,\theta'}
\left\{
\frac{B(\theta)+B(\theta')}{2}
+
\frac{
\varphi_{n+1}(a_{n+1}(\theta))
-
\varphi_{n+1}(a_{n+1}(\theta'))
}{2}
\right\}.
$$
因为 $\varphi_{n+1}$ 是 1-Lipschitz，
$$
\left|
\varphi_{n+1}(u)-\varphi_{n+1}(v)
\right|
\le
|u-v|.
$$
所以
$$
\frac{
\varphi_{n+1}(a_{n+1}(\theta))
-
\varphi_{n+1}(a_{n+1}(\theta'))
}{2}
\le
\frac{
|a_{n+1}(\theta)-a_{n+1}(\theta')|
}{2}.
$$
再利用 supremum 同时包含 $(\theta,\theta')$ 和 $(\theta',\theta)$，可以把绝对值处理成相当于引入一个新的 Rademacher 符号：
$$
\frac{
|a_{n+1}(\theta)-a_{n+1}(\theta')|
}{2}
$$
对应
$$
\varepsilon_{n+1}a_{n+1}(\theta).
$$
于是就把
$$
\varepsilon_{n+1}\varphi_{n+1}(a_{n+1}(\theta))
$$
替换成了
$$
\varepsilon_{n+1}a_{n+1}(\theta).
$$
剩下前 $n$ 项用归纳假设处理。

Proposition 4.4 是：

若 $\varphi_i$ 是 1-Lipschitz 且
$$
\varphi_i(0)=0,
$$
则
$$
\mathbb E_\varepsilon
\left[
\sup_{\theta\in\Theta}
\left|
\sum_{i=1}^n
\varepsilon_i
\varphi_i(a_i(\theta))
\right|
\right]
\le
2
\mathbb E_\varepsilon
\left[
\sup_{\theta\in\Theta}
\left|
\sum_{i=1}^n
\varepsilon_i
a_i(\theta)
\right|
\right].
$$
这里多了 $2$，主要是因为 supremum 里面有绝对值：
$$
\sup_\theta |S_\theta|
=
\max\left\{
\sup_\theta S_\theta,
\sup_\theta (-S_\theta)
\right\}.
$$
要同时控制正方向和负方向，会额外损失一个常数。这个版本常用于绝对值型或对称化后的表达。

我们接下来考虑线性函数类的特殊情况

$f_θ(x)=θ^⊤φ(x),Ω(θ)≤D$,

令设计矩阵
$$
\Phi\in\mathbb R^{n\times d},
$$
第 $i$ 行是
$$
\varphi(x_i)^\top.
$$
则
$$
\begin{aligned}
R_n(\mathcal F)
&=
\mathbb E
\left[
\sup_{\Omega(\theta)\le D}
\frac1n
\sum_{i=1}^n
\varepsilon_i
\theta^\top\varphi(x_i)
\right]\\
&=
\mathbb E
\left[
\sup_{\Omega(\theta)\le D}
\frac1n
\varepsilon^\top \Phi\theta
\right]\\
&=
\mathbb E
\left[
\sup_{\Omega(\theta)\le D}
\frac1n
\theta^\top \Phi^\top\varepsilon
\right].
\end{aligned}
$$
利用对偶范数定义：
$$
\Omega^*(u)
=
\sup_{\Omega(\theta)\le 1}
u^\top \theta.
$$
所以
$$
\sup_{\Omega(\theta)\le D}
\theta^\top u
=
D\Omega^*(u).
$$
于是就有
$$
R_n(\mathcal F)
=
\frac{D}{n}
\mathbb E
\left[
\Omega^*(\Phi^\top\varepsilon)
\right].
$$
不同范数给出不同复杂度：
$$
\Omega=\|\cdot\|_2
\quad\Longrightarrow\quad
R_n(\mathcal F)
\le
\frac{D}{\sqrt n}
\sqrt{\mathbb E\|\varphi(x)\|_2^2}.
$$

$$
\Omega = \|\cdot\|_1
\quad\Longrightarrow\quad
R_n(\mathcal F)
\le
\frac{D}{n}\mathbb E[\|\Phi^T\varepsilon\|_{\infty}]=max_j\{\sum_{i=1}^n\varphi_j(x_i)\varepsilon_i\}
$$

在固定数据 $x_1,\dots,x_n$ 后，这是一个 Rademacher 加权和。由于
$$
|\varphi_j(x_i)|\le R,
$$
所以每个坐标都是 sub-Gaussian，方差代理量满足
$$
\sum_{i=1}^n \varphi_j(x_i)^2
\le
nR^2.
$$
于是最大值满足经典 bound：
$$
\mathbb E_\varepsilon
\max_{1\le j\le d}
|(\Phi^\top\varepsilon)_j|
\le
R\sqrt{2n\log(2d)}.
$$
这里的 $2d$ 来自绝对值：
$$
\max_j |S_j|
=
\max\{S_1,\dots,S_d,-S_1,\dots,-S_d\},
$$
总共有 $2d$ 个 sub-Gaussian 变量取最大。

代回：
$$
R_n(\mathcal F)
\le
\frac{D}{n}
R\sqrt{2n\log(2d)}
=
RD
\sqrt{
\frac{2\log(2d)}{n}
}.
$$
这就是 $\ell_1$ ball 的 Rademacher complexity。它的特点是只出现
$$
\log d
$$
而不是 $d$。这正是稀疏学习中 $\ell_1$ 约束的优势。