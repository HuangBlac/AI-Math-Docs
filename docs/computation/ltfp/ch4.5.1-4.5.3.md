LTFP: Ch 4.5.1Rademacher复杂度

所以我们折腾半天引出这样一个量是为了说明什么呢？

接下来，我们可以证明

Propostion4.2

```math
E\{\sup_{h\in\mathcal H} \{|E(h(z))-\frac{1}{n}\sum_{i=1}^n h(z_i)|\}\}\le2R_n(\mathcal H)
```
这其实就是说明Estimation error统计误差可以被Rademacher复杂度给控制住。

我们分别证明：

$E\{\sup_{h\in\mathcal H} \{E(h(z))-\frac{1}{n}\sum_{i=1}^n h(z_i)\}\}\le2R_n(\mathcal H)$,$E\{sup_{h\in\mathcal H} \{\frac{1}{n}\sum_{i=1}^n h(z_i)-E[h(z)]\}\}\le2R_n(\mathcal H)$

考虑一组同分布的数据$\mathcal D'=\{z'_1,z_2'\cdots,z_n'\}$

因此，我们可以将期望转化为虚样本的条件期望
```math
E\{\sup_{h\in\mathcal H} \{E(h(z))-\frac{1}{n}\sum_{i=1}^n h(z_i)\}\}=E\{\sup_{h\in\mathcal H} \{E[\frac{1}{n}\sum_{i=1}^n h(z'_i)|\mathcal D]-\frac{1}{n}\sum_{i=1}^n h(z_i)\}\}\\
\le E[\sup_{h\in\mathcal H}E[\frac{1}{n}\sum_{i=1}^nh(z'_i)-h(z_i)|\mathcal D]]\\
\le E[E[\sup_{h\in\mathcal H}\frac{1}{n}\sum_{i=1}^nh(z'_i)-h(z_i)|\mathcal D]]\\
\le E[sup_{h\in \mathcal H}\sum_{i=1}^n\{h(z'_i)-h(z_i)\}]
```
而同理可得，
```math
E[sup_{h\in\mathcal H} \{\frac{1}{n}\sum_{i=1}^n h(z_i)-E(h(z))\}]\le E[sup_{h\in \mathcal H}\sum_{i=1}^n\{h(z_i)-h(z'_i)\}]
```
接下来，我们又可以根据对称性知道：
```math
E[sup_{h\in \mathcal H}\frac{1}{n}\sum_{i=1}^n\{h(z'_i)-h(z_i)\}]\\
=E[sup_{h\in \mathcal H}\frac{1}{n}\sum_{i=1}^n\varepsilon_i\{h(z'_i)-h(z_i)\}]\\
\le E[sup_{h\in \mathcal H}\frac{1}{n}\sum_{i=1}^n\varepsilon_i\{h(z'_i)-h(z_i)\}]\\
\le E[sup_{h\in \mathcal H}\frac{1}{n}\sum_{i=1}^n\varepsilon_ih(z'_i)]+E[sup_{h\in \mathcal H}\frac{1}{n}\sum_{i=1}^n-\varepsilon_ih(z_i)] \\
\le 2R_n(\mathcal{H})
```
不过，Radamacher复杂度是衡量函数类对于随机变量的逼近能力，那么能否使用别的随机变量呢？

答案是可以的，下面我们介绍$G_n(\mathcal H)$，这也便是Ex4.11

Exercise4.11:

考虑\(g_i\sim N(0,1)\)是彼此独立的标准 Gaussian 随机变量。

\(G_n(\mathcal H) = \mathbb E_{D,g} \left[ \sup_{h\in\mathcal H} \frac1n\sum_{i=1}^ng_i h(z_i) \right].\)



目标是证明

\[ \boxed{ R_n(\mathcal H) \leq \sqrt{\frac{\pi}{2}}G_n(\mathcal H) } \]

\[ \boxed{ G_n(\mathcal H) \leq \sqrt{2\log(2n)}R_n(\mathcal H). } \]

首先证明1，考虑$g_i=\sigma_i|g_i|$其中$\sigma_i$表示$-1,+1$随机取值的随机变量

## 第一部分

标准 Gaussian 随机变量可以分解成

\[ g_i=\sigma_i|g_i|, \]

其中符号 \(\sigma_i\) 与幅度 \(|g_i|\) 相互独立，并且

\[ \mathbb E|g_i| = \sqrt{\frac2\pi}. \]

因此

\[ G_n(\mathcal H) = \mathbb E_{D,\sigma,|g|} \left[ \sup_{h\in\mathcal H} \frac1n\sum_{i=1}^n \sigma_i|g_i|h(z_i) \right]. \]

固定 \(D,\sigma\)。关于向量

\[ a=(|g_1|,\ldots,|g_n|), \]

函数

\[ a\longmapsto \sup_{h\in\mathcal H} \frac1n\sum_i\sigma_i a_i h(z_i) \]

是若干线性函数的 supremum，因此是凸函数。由 Jensen 不等式，

\[ \begin{aligned} &\mathbb E_{|g|} \left[ \sup_{h\in\mathcal H} \frac1n\sum_i \sigma_i|g_i|h(z_i) \right]\\ &\qquad\geq \sup_{h\in\mathcal H} \frac1n\sum_i \sigma_i\mathbb E|g_i|h(z_i)\\ &\qquad= \sqrt{\frac2\pi} \sup_{h\in\mathcal H} \frac1n\sum_i \sigma_i h(z_i). \end{aligned} \]

再对 \(D,\sigma\) 取期望：

\[ G_n(\mathcal H) \geq \sqrt{\frac2\pi}R_n(\mathcal H). \]

整理得到

\[ \boxed{ R_n(\mathcal H) \leq \sqrt{\frac\pi2}G_n(\mathcal H). } \]

仍然使用分解

\[ g_i=\sigma_i|g_i|. \]

令

\[ M=\max_{1\leq i\leq n}|g_i|. \]

当 \(M>0\) 时定义

\[ c_i=\frac{|g_i|}{M}, \]

于是 \(0\leq c_i\leq1\)，并且

\[ |g_i|=Mc_i. \]

固定 \(D\) 和 Gaussian 幅度，由齐次性和上面的 contraction 性质，

\[ \begin{aligned} &\mathbb E_\sigma \left[ \sup_{h\in\mathcal H} \frac1n\sum_i \sigma_i|g_i|h(z_i) \right]\\ &= M\, \mathbb E_\sigma \left[ \sup_{h\in\mathcal H} \frac1n\sum_i \sigma_i c_i h(z_i) \right]\\ &\leq M\, \mathbb E_\sigma \left[ \sup_{h\in\mathcal H} \frac1n\sum_i \sigma_i h(z_i) \right]. \end{aligned} \]

由于 \(M\) 与数据 \(D\) 独立，取期望后得到

\[ G_n(\mathcal H) \leq \mathbb E[M]R_n(\mathcal H). \]

现在只需证明

\[ \mathbb E[M] \leq \sqrt{2\log(2n)}. \]

## 第二部分

仍然使用分解

\[ g_i=\sigma_i|g_i|. \]

令

\[ M=\max_{1\leq i\leq n}|g_i|. \]

当 \(M>0\) 时定义

\[ c_i=\frac{|g_i|}{M}, \]

于是 \(0\leq c_i\leq1\)，并且

\[ |g_i|=Mc_i. \]

固定 \(D\) 和 Gaussian 幅度，由齐次性和上面的 contraction 性质，

\[ \begin{aligned} &\mathbb E_\sigma \left[ \sup_{h\in\mathcal H} \frac1n\sum_i \sigma_i|g_i|h(z_i) \right]\\ &= M\, \mathbb E_\sigma \left[ \sup_{h\in\mathcal H} \frac1n\sum_i \sigma_i c_i h(z_i) \right]\\ &\leq M\, \mathbb E_\sigma \left[ \sup_{h\in\mathcal H} \frac1n\sum_i \sigma_i h(z_i) \right]. \end{aligned} \]

由于 \(M\) 与数据 \(D\) 独立，取期望后得到

\[ G_n(\mathcal H) \leq \mathbb E[M]R_n(\mathcal H). \]

现在只需证明

\[ \mathbb E[M] \leq \sqrt{2\log(2n)}. \]

### 控制 Gaussian 最大值

对任意 \(\lambda>0\)，

\[ e^{\lambda M} \leq \sum_{i=1}^n \left( e^{\lambda g_i}+e^{-\lambda g_i} \right). \]

利用 Jensen 不等式以及标准 Gaussian 的矩母函数

\[ \mathbb E e^{\lambda g_i} = e^{\lambda^2/2}, \]

可得

\[ \begin{aligned} \mathbb E[M] &\leq \frac1\lambda \log\mathbb E[e^{\lambda M}]\\ &\leq \frac1\lambda \log\left( 2n e^{\lambda^2/2} \right)\\ &= \frac{\log(2n)}{\lambda} + \frac{\lambda}{2}. \end{aligned} \]

选择

\[ \lambda=\sqrt{2\log(2n)}, \]

得到

\[ \mathbb E[M] \leq \sqrt{2\log(2n)}. \]

最终

\[ \boxed{ G_n(\mathcal H) \leq \sqrt{2\log(2n)} R_n(\mathcal H). } \]

综合两边：

\[ \boxed{ \sqrt{\frac2\pi}\,R_n(\mathcal H) \leq G_n(\mathcal H) \leq \sqrt{2\log(2n)}\,R_n(\mathcal H). } \]

这说明 Gaussian complexity 与 Rademacher complexity 本质上测量同一种函数类容量；二者至多相差一个 \(\sqrt{\log n}\) 因子。

经验Radamacher复杂度

我们之前得到的是$\mathbb E_{\mathcal D}\sup_{h\in\mathcal H}\abs{\mathbb E(h(z))-\frac 1 n \sum_{i=1}^n h(z_i)}$在期望的意义下被Radamacher复杂度给控制住，那么，对于任意选取的样本量能否稳定控制呢？

$\mathbb E(h(z))\le \frac 1 n\sum_{i=1}^n h(z_i)+2R_n(\mathcal H)+\frac {\ell_∞}{\sqrt{2n}} \sqrt{\log(\frac 1 \delta)}$

记$\Phi (z_1,z_2,\cdots,z_n)=\sup_{h\in\mathcal H}\mathbb E(h(z))- \frac 1 n\sum_{i=1}^n h(z_i)$

由Proposition 4.2$\mathbb E_{z_i}\Phi(z_1,z_2,\cdots,z_n)\le 2R_n(\mathcal H)$

只需证：$\mathbb P(\Phi (z_1,z_2,\cdots,z_n))-\mathbb E\Phi (z_1,z_2,\cdots,z_n)\le t)\le\exp\left( -\frac{2nt^2}{\ell_\infty^2} \right)=\delta$

这是McDiarmid不等式可知，因为现在只替换第 \(j\) 个样本：

\[ D=(z_1,\ldots,z_j,\ldots,z_n), \]\[ D^{(j)}=(z_1,\ldots,z_j',\ldots,z_n). \]

对任意固定的 \(h\)，两个经验平均之差满足

\[ \begin{aligned} |P_nh-P_n^{(j)}h| &= \frac1n|h(z_j)-h(z_j')|\\ &\leq \frac{\ell_\infty}{n}. \end{aligned} \]

而 supremum 也不会放大这个差异，因此

\[ |\Phi(D)-\Phi(D^{(j)})| \leq \frac{\ell_\infty}{n}. \]

所以 McDiarmid 不等式中的有界差分常数是

\[ c_j=\frac{\ell_\infty}{n}. \]

于是

\[ \sum_{j=1}^n c_j^2 = n\frac{\ell_\infty^2}{n^2} = \frac{\ell_\infty^2}{n}. \]



经验Radamacher复杂度：

我们把固定在当前观测数据 \(D\) 上的内层量定义为经验 Rademacher complexity：

\[ \boxed{ \widehat R_D(\mathcal H) = \mathbb E_\varepsilon \left[ \sup_{h\in\mathcal H} \frac1n\sum_i\varepsilon_i h(z_i) \right]. } \]

于是

\[ R_n(\mathcal H) = \mathbb E_D[\widehat R_D(\mathcal H)]. \]

再对 \(\widehat R_D(\mathcal H)\) 使用一次 McDiarmid，就能用实际数据上的 \(\widehat R_D\) 替换未知的 \(R_n\)。典型结果是：以至少 \(1-\delta\) 的概率，

\[ \boxed{ Ph \leq P_nh + 2\widehat R_D(\mathcal H) + \frac{3\ell_\infty}{\sqrt{2n}} \sqrt{\log\frac{2}{\delta}} } \]

同时对所有 \(h\in\mathcal H\) 成立。也就是说，引入经验 Rademacher complexity 的目的，是把依赖未知数据分布的理论复杂度界，变成可以从当前样本估计的数据依赖界。





Proposition 4.3 (Contraction principle–Lipschitz-continuous functions)

在接下来，我们介绍一个比较好的性质，也就是收缩性。因为我们现在处理的函数类是损失函数$\ell(f(x),y)$而我们已知的实际上是目标函数，例如这里的f，属于线性函数类。如果我们可以简单的用一个常数来掩盖掉。

直接计算

\[ R_n(\ell\circ\mathcal F) = \mathbb E \sup_{f\in\mathcal F} \frac1n\sum_i \varepsilon_i\ell(y_i,f(x_i)) \]

往往很困难，因为损失函数 \(\ell\) 是非线性的。

命题 4.3 就是用来“去掉”这个非线性的。

Proposition4.3:

给定任意函数$a_i:\Theta\to \mathbb R,$以及 1-Lipschitz 函数$\varphi_i:\mathbb R\to \mathbb R,$则

```math
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
```
它的意思是：

> 对函数值先做一个 1-Lipschitz 变换，不会增加 Rademacher complexity。

因为 Lipschitz 函数不会把距离放大，所以它不会让函数类更容易拟合随机符号：

下面，我们给出证明过程

可以采用归纳法来进行证明，首先对于n=0时就没有1-Lipschitz变换的事。

我们已知：$\forall k\le n$
$$
\mathbb E_\varepsilon
\left[
\sup_{\theta\in\Theta}
\left\{
b(\theta)
+
\sum_{i=1}^k \varepsilon_i
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
\sum_{i=1}^k \varepsilon_i
a_i(\theta)
\right\}
\right].
$$
下证k=n+1的情况：

首先记$B(\theta)
=
b(\theta)
+
\sum_{i=1}^n \varepsilon_i\varphi_i(a_i(\theta)).$

考虑第 $n+1$ 个 Rademacher 符号。对 $\varepsilon_{n+1}$ 显式取期望：
```math
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
```
把两个 supremum 合并成对 $(\theta,\theta')$ 的 supremum：
```math
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
```
因为 $\varphi_{n+1}$ 是 1-Lipschitz，
```math
\left|
\varphi_{n+1}(u)-\varphi_{n+1}(v)
\right|
\le
|u-v|.
```
所以
```math
\frac{
\varphi_{n+1}(a_{n+1}(\theta))
-
\varphi_{n+1}(a_{n+1}(\theta'))
}{2}
\le
\frac{
|a_{n+1}(\theta)-a_{n+1}(\theta')|
}{2}.
```
再利用 supremum 同时包含 $(\theta,\theta')$ 和 $(\theta',\theta)$，可以把绝对值处理成相当于引入一个新的 Rademacher 符号：
```math
\frac{
|a_{n+1}(\theta)-a_{n+1}(\theta')|
}{2}
```
对应
```math
\varepsilon_{n+1}a_{n+1}(\theta).
```
于是就把
```math
\varepsilon_{n+1}\varphi_{n+1}(a_{n+1}(\theta))
```
替换成了
```math
\varepsilon_{n+1}a_{n+1}(\theta).
```
剩下前 $n$ 项用归纳假设处理。

所以这么折腾半天时为了干什么呢？

考虑监督学习问题。假设对于几乎所有数据，以及所有 \(i\in\{1,\ldots,n\}\)，损失函数关于预测值的映射$u_i\longmapsto \ell(y_i,u_i)$都是 \(G\)-Lipschitz 连续的，即

\[
\left|
\ell(y_i,u)-\ell(y_i,v)
\right|
\leq
G|u-v|,
\qquad
\forall u,v\in\mathbb R.
\]

这一条件可以用于回归问题，也可以用于第 4.1 节介绍的二分类凸替代损失。

在给定数据集

\[
D=\{(x_1,y_1),\ldots,(x_n,y_n)\}
\]

的条件下，将命题 4.3 的收缩原理应用于

\[
b=0,
\]

\[
\Theta
=
\left\{
\bigl(f(x_1),\ldots,f(x_n)\bigr):
f\in\mathcal F
\right\}
\subseteq\mathbb R^n,
\]

\[
a_i(\theta)=\theta_i,
\]

以及

\[
\phi_i(u_i)=\ell(y_i,u_i).
\]

由于 \(u_i\mapsto\ell(y_i,u_i)\) 是 \(G\)-Lipschitz 连续的，由收缩原理可得

\[
\boxed{
\mathbb E_{\varepsilon}
\left[
\left.
\sup_{f\in\mathcal F}
\frac1n
\sum_{i=1}^n
\varepsilon_i
\ell\bigl(y_i,f(x_i)\bigr)
\,\right|\,D
\right]
\leq
G\,
\mathbb E_{\varepsilon}
\left[
\left.
\sup_{f\in\mathcal F}
\frac1n
\sum_{i=1}^n
\varepsilon_i f(x_i)
\,\right|\,D
\right].
}
\]

等价地，用经验 Rademacher complexity 表示为

\[
\boxed{
\widehat R_D(\ell\circ\mathcal F)
\leq
G\,\widehat R_D(\mathcal F).
}
\]

最后对数据 \(D\) 取期望，得到总体 Rademacher complexity 的关系：

\[
\boxed{
R_n(\ell\circ\mathcal F)
\leq
G\,R_n(\mathcal F).
}
\]

严格对应命题 4.3 的 1-Lipschitz 条件时，可以定义归一化函数

\[
\widetilde\phi_i(u)
=
\frac{\ell(y_i,u)}{G}.
\]

此时 \(\widetilde\phi_i\) 是 1-Lipschitz 的。应用命题 4.3 后再提出系数 \(G\)，即可得到上述不等式。

因此，命题 4.3 表明：损失函数至多将预测函数类的 Rademacher complexity 放大 \(G\) 倍。



Proposition 4.4 

若 $\varphi_i$ 是 1-Lipschitz 且$\varphi_i(0)=0,$则

```math
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
```
这里多了 $2$，主要是因为 supremum 里面有绝对值：
```math
\sup_\theta |S_\theta|
=
\max\left\{
\sup_\theta S_\theta,
\sup_\theta (-S_\theta)
\right\}.
```
要同时控制正方向和负方向，会额外损失一个常数。这个版本常用于绝对值型或对称化后的表达。

可以在函数值集合中加入零向量

\[ a_i(\theta_0)=0, \qquad i=1,\ldots,n. \]

因为

\[ \varphi_i(0)=0, \]

所以加入 \(\theta_0\) 后，左边和右边的绝对值 supremum 都不会改变。与此同时，

\[ S_\varphi(\theta_0)=0, \]

因此

\[ \sup_\theta S_\varphi(\theta)\geq0, \qquad \sup_\theta(-S_\varphi(\theta))\geq0. \]

所以可以使用

\[ \max\{A,B\}\leq A+B \qquad(A,B\geq0), \]

得到

\[ \sup_\theta|S_\varphi(\theta)| \leq \sup_\theta S_\varphi(\theta) + \sup_\theta(-S_\varphi(\theta)). \]

取期望：

\[ \begin{aligned} \mathbb E_\varepsilon \sup_\theta|S_\varphi(\theta)| &\leq \mathbb E_\varepsilon \sup_\theta \sum_{i=1}^n \varepsilon_i\varphi_i(a_i(\theta))\\ &\quad+ \mathbb E_\varepsilon \sup_\theta \sum_{i=1}^n (-\varepsilon_i)\varphi_i(a_i(\theta)). \end{aligned} \]

由于

\[ (-\varepsilon_1,\ldots,-\varepsilon_n) \overset d= (\varepsilon_1,\ldots,\varepsilon_n), \]

上面两项相等，因此\[ \mathbb E_\varepsilon \sup_\theta|S_\varphi(\theta)| \leq 2\, \mathbb E_\varepsilon \sup_\theta \sum_{i=1}^n \varepsilon_i\varphi_i(a_i(\theta)). \tag{1} \]

然后就可以使用Proposition 4.3

Ch4.5.3

我们接下来考虑线性函数类的特殊情况$\mathcal F=\{f_θ(x)=θ^⊤φ(x),Ω(θ)≤D\}$,

令设计矩阵$\Phi\in\mathbb R^{n\times d},$第 $i$ 行是$\varphi(x_i)^\top$.

则
```math
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
```
利用对偶范数定义：$\Omega^*(u)
=
\sup_{\Omega(\theta)\le 1}
u^\top \theta.$所以$\sup_{\Omega(\theta)\le D}
\theta^\top u
=
D\Omega^*(u).$

于是就有$R_n(\mathcal F)
=
\frac{D}{n}
\mathbb E
\left[
\Omega^*(\Phi^\top\varepsilon)
\right].$

不同范数给出不同复杂度：

当$\Omega =\|\cdot\|_2,\Omega^*=\|\cdot\|_2$因此原式变成：
$$
R_n(\mathcal F)
=
\frac{D}{n}
\mathbb E
\left[
\Omega^*(\Phi^\top\varepsilon)
\right]\le\frac{D}{n}\sqrt{
\mathbb E
\left[
\|\Phi^\top\varepsilon)
\|_2^2\right]}=\frac D n\sqrt{ \mathbb E\tr(\Phi\Phi^\top\varepsilon\varepsilon^\top)}=
$$
由于 \(\Phi\) 的第 \(i\) 行是 \(\varphi(x_i)^\top\)，

\[ \operatorname{tr}(\Phi^\top\Phi) = \|\Phi\|_{\mathrm F}^2 = \sum_{i=1}^n \|\varphi(x_i)\|_2^2. \]

原文中类似

\[ (\Phi\Phi^\top)_i \]

的记法应当更准确地写成对角元素

\[ (\Phi\Phi^\top)_{ii}. \]

因为

\[ (\Phi\Phi^\top)_{ii} = \varphi(x_i)^\top\varphi(x_i) = \|\varphi(x_i)\|_2^2. \]

最后，由于 \(x_1,\ldots,x_n\) 同分布，

\[ \sum_{i=1}^n \mathbb E \|\varphi(x_i)\|_2^2 = n\, \mathbb E \|\varphi(x)\|_2^2. \]

所以最终得到

\[ \boxed{ R_n(\mathcal F) \leq \frac{D}{\sqrt n} \sqrt{ \mathbb E \|\varphi(x)\|_2^2 }. } \]



Ex4.12 $\Omega = \|\cdot\|_1,$

首先，根据定义，可以得到：

$R_n(\mathcal F)
\le
\frac{D}{n}\mathbb E[\|\Phi^T\varepsilon\|_{\infty}]=\max_j\{\sum_{i=1}^n\varphi_j(x_i)\varepsilon_i\}$

在固定数据 $x_1,\dots,x_n$ 后，这是一个 Rademacher 加权和。由于$|\varphi_j(x_i)|\le R,$

所以每个坐标都是 sub-Gaussian，方差代理量满足
```math
\sum_{i=1}^n \varphi_j(x_i)^2
\le
nR^2.
```
于是最大值满足经典 bound：
```math
\mathbb E_\varepsilon
\max_{1\le j\le d}
|(\Phi^\top\varepsilon)_j|
\le
R\sqrt{2n\log(2d)}.
```
这是通过经典的log-exp-sum得到

这里的 $2d$ 来自绝对值：

```math
\max_j |S_j|
=
\max\{S_1,\dots,S_d,-S_1,\dots,-S_d\},
```
总共有 $2d$ 个 sub-Gaussian 变量取最大。

代回：
```math
R_n(\mathcal F)
\le
\frac{D}{n}
R\sqrt{2n\log(2d)}
=
RD
\sqrt{
\frac{2\log(2d)}{n}
}.
```
这就是 $\ell_1$ ball 的 Rademacher complexity。它的特点是只出现
```math
\log d
```
而不是 $d$。这正是稀疏学习中 $\ell_1$ 约束的优势。

Exercise 4.13设$p\in(1,2],$并令 \(q\) 为 \(p\) 的 Hölder 共轭指数，即
\[
\frac1p+\frac1q=1.
\]

假设几乎处处有$\|\varphi(x)\|_q\leq R.$考虑线性预测函数类$\mathcal F
=
\left\{
f_\theta(x)=\theta^\top\varphi(x):
\Omega(\theta)\leq D
\right\},$

其中$\Omega(\theta)=\|\theta\|_p.$

证明该函数类的 Rademacher complexity 满足

\[
\boxed{
R_n(\mathcal F)
\leq
\frac{RD}{\sqrt n}\,
\frac1{\sqrt{p-1}}.
}
\]

提示：使用 Exercise 1.25 的结论。

最后，取

\[
p
=
1+\frac1{\log(2d)},
\]

恢复 Exercise 4.12 中的结果。

解：取\[ Z_i=\varepsilon_i\varphi(x_i). \]

固定数据 \(x_1,\ldots,x_n\) 后，因为\[ \mathbb E_\varepsilon[\varepsilon_i]=0, \]

所以\[ \mathbb E_\varepsilon[Z_i]=0. \]

同时\[ \|Z_i\|_q = |\varepsilon_i|\|\varphi(x_i)\|_q = \|\varphi(x_i)\|_q \leq R. \]

\[ S_n=Z_1+\cdots+Z_n. \]

对于满足L-smooth的函数$f(u)=\|u\|_q^2,L=q-1$

\(L=q-1, \sigma^2=R^2,\)

\[ f(S_{n-1}+Z_n) \leq f(S_{n-1}) + \nabla f(S_{n-1})^\top Z_n + \frac L2\Omega(Z_n)^2. \]

对历史信息 \(Z_1,\ldots,Z_{n-1}\) 做条件期望。

\[ \mathbb E_\varepsilon \left[ \left\| \sum_{i=1}^n \varepsilon_i\varphi(x_i) \right\|_q^2 \right] \leq n(q-1)R^2. \]

取平方根并使用 Jensen 不等式：

\[ \mathbb E_\varepsilon \left\| \sum_{i=1}^n \varepsilon_i\varphi(x_i) \right\|_q \leq R\sqrt{n(q-1)}. \]

代入线性函数类的 Rademacher complexity：

\[ \begin{aligned} R_n(\mathcal F) &= \frac Dn \mathbb E \left\| \sum_{i=1}^n \varepsilon_i\varphi(x_i) \right\|_q\\ &\leq \frac{RD}{\sqrt n}\sqrt{q-1}. \end{aligned} \]

因为

\[ \frac1p+\frac1q=1 \quad\Longrightarrow\quad q-1=\frac1{p-1}, \]

最终得到

\[ \boxed{ R_n(\mathcal F) \leq \frac{RD}{\sqrt n\sqrt{p-1}}. } \]
