4.5.4 Putting Things Together

在这一部分之中，我们使用线性模型函数空间的Rademacher复杂度来对误差进行估计：

Proposition 4.5：

损失函数$\ell$是一个G-Lipschitz连续的函数，函数类$\mathcal F =\{f_\theta(x)=\theta^\top \varphi (x)，\|\theta\|_2\le D\}$，$\mathbb E \|\varphi(x)\|_2^2\le R^2$若$\hat f$是经验损失的最小值，那么满足：
$$
\mathbb E[\mathcal R(\hat f)]\le\inf_{f\in\mathcal F}\mathcal R(f)+\frac{4GRD}{\sqrt n}
$$
首先,根据Radamacher复杂度的控制，以及Lipshictz函数的性质
$$
\mathbb E[\mathcal R(\hat f)]-\inf_{f\in\mathcal F}\mathcal R(f)\le 2[ \sup_{f\in\mathcal F}\mathcal R(f)-\mathcal {\hat R}(f)]
$$

$$
\sup_{f\in\mathcal F}\mathcal R(f)-\mathcal {\hat R}(f)\le 2R_n(\mathcal H)\le2GR_n(\mathcal F)
$$

由4.5.3可知，采用二范数的对偶范数$R_n(\mathcal F)\le \frac{\sqrt{\mathbb E [\|\varphi(x)\|_2^2]}D}{\sqrt n}=\frac {DR}{\sqrt n}$

因此得到一式

但是这还不够，除了Estimation统计误差，我们还需要得到逼近误差，也就是这个$\mathcal F$与真实解的距离

假设真实风险

\[ \mathcal R(f_\theta) \]

在整个参数空间 \(\mathbb R^d\) 上存在最优解

\[ \theta^* \in \arg\min_{\theta\in\mathbb R^d} \mathcal R(f_\theta). \]

但学习算法只允许在半径为 \(D\) 的参数球中搜索：

\[ \|\theta\|_2\leq D. \]

由此产生的逼近误差满足

\[ \begin{aligned} \inf_{\|\theta\|_2\leq D} \mathcal R(f_\theta) - \mathcal R(f_{\theta^*}) &\leq G \inf_{\|\theta\|_2\leq D} \mathbb E \left[ |f_\theta(x)-f_{\theta^*}(x)| \right]\\ &= G \inf_{\|\theta\|_2\leq D} \mathbb E \left[ \left| \varphi(x)^\top(\theta-\theta^*) \right| \right]\\ &\leq G \inf_{\|\theta\|_2\leq D} \|\theta-\theta^*\|_2 \, \mathbb E \left[ \|\varphi(x)\|_2 \right]\\ &\leq GR \inf_{\|\theta\|_2\leq D} \|\theta-\theta^*\|_2. \end{aligned} \]

因此总的超额风险满足

\[ \begin{aligned} \mathbb E \left[ \mathcal R(f_{\hat\theta}) \right] - \mathcal R(f_{\theta^*}) &\leq GR \inf_{\|\theta\|_2\leq D} \|\theta-\theta^*\|_2 + \frac{4GRD}{\sqrt n}\\ &= GR \bigl(\|\theta^*\|_2-D\bigr)_+ + \frac{4GRD}{\sqrt n}, \end{aligned} \]

其中

\[ (a)_+:=\max\{a,0\}. \]

Exercise 4.14，将所选取的函数空间换成$\|\theta\|_1\le D$这样的$L_1$有界的函数类

我们首先来求Radamacher复杂度：

### 习题

考虑一个监督学习问题，其损失函数关于第二个变量是
\(G\)-Lipschitz 连续的。

设线性预测函数为

\[
f_\theta(x)=\theta^\top\varphi(x),
\]

参数满足

\[
\|\theta\|_1\leq D,
\]

且特征映射

\[
\varphi:\mathcal X\to\mathbb R^d
\]

几乎处处满足

\[
\|\varphi(x)\|_\infty\leq R.
\]

分别记预测函数 \(f_\theta\) 的期望风险和经验风险为

\[
\mathcal R(f_\theta)
\qquad\text{和}\qquad
\widehat{\mathcal R}(f_\theta).
\]

设 \(\hat\theta\) 是约束经验风险最小化问题的解：

\[
\hat\theta
\in
\arg\min_{\|\theta\|_1\leq D}
\widehat{\mathcal R}(f_\theta).
\]

证明对应的预测函数 \(f_{\hat\theta}\) 满足

\[
\boxed{
\mathbb E
\left[
\mathcal R(f_{\hat\theta})
\right]
\leq
\inf_{\|\theta\|_1\leq D}
\mathcal R(f_\theta)
+
4GRD
\sqrt{
\frac{2\log(2d)}{n}
}.
}
\]
$R(\mathcal H)\le GRD\sqrt{\frac{2\log(2d)}{n}}$

$\mathbb E[\mathcal R(\hat f)]\le\inf_{f\in\mathcal F}\mathcal R(f)+4R_n(\mathcal H)$,$\inf_f\mathcal R(f)-\mathcal R^*\le GR\inf_{\|\theta\|_1\le D}\|\theta-\theta^*\|_1$
$$
 \begin{aligned} \mathbb E \left[ \mathcal R(f_{\hat\theta}) \right] - \mathcal R(f_{\theta^*}) &\leq GR \inf_{\|\theta\|_1\leq D} \|\theta-\theta^*\|_1 + 4GRD\sqrt{\frac{2\log(2d)}{n}}\\ &= GR \bigl(\|\theta^*\|_2-D\bigr)_+ + 4GRD\sqrt{\frac{2\log(2d)}{n}}, \end{aligned}
$$

### 4.5.5 从约束估计到正则化估计

在实际应用中，与其直接对参数施加范数约束，通常更适合使用范数 \(\Omega(\theta)\) 作为惩罚项。

当约束参数和正则化参数分别变化时，约束形式与正则化形式得到的解集实际上是相同的。但是，采用正则化形式的主要原因是：

- 正则化超参数通常更容易选择；
- 相应的优化问题通常也更容易求解。

本节首先考虑平方 \(\ell_2\) 范数正则化:

此外，由于这里只考虑形式相同的线性预测函数

\[
f_\theta=\varphi(\cdot)^\top\theta,
\qquad
\theta\in\mathbb R^d,
\]

因此简记

\[
\mathcal R(\theta)
=
\mathcal R(f_\theta),
\qquad
\widehat{\mathcal R}(\theta)
=
\widehat{\mathcal R}(f_\theta).
\]

对于正则化参数 \(\lambda>0\)，记 \(\hat\theta_\lambda\) 为下列正则化经验风险最小化问题的一个解：

\[
\boxed{
\hat\theta_\lambda
\in
\arg\min_{\theta\in\mathbb R^d}
\left\{
\widehat{\mathcal R}(\theta)
+
\frac{\lambda}{2}\|\theta\|_2^2
\right\}.
}
\tag{4.17}
\]

等价地，

\[
\hat\theta_\lambda
\in
\arg\min_{\theta\in\mathbb R^d}
\left\{
\widehat{\mathcal R}(f_\theta)
+
\frac{\lambda}{2}\|\theta\|_2^2
\right\}.
\]

如果损失函数始终非负，那么

\[
\frac{\lambda}{2}
\|\hat\theta_\lambda\|_2^2
\leq
\widehat{\mathcal R}(\hat\theta_\lambda)
+
\frac{\lambda}{2}
\|\hat\theta_\lambda\|_2^2
\leq
\widehat{\mathcal R}(0).
\]

因此可以得到

\[
\|\hat\theta_\lambda\|_2
=
O\left(\frac1{\sqrt\lambda}\right).
\]

如果在命题 4.5 的约束型风险界中取$D=O\left(\frac1{\sqrt\lambda}\right),$则得到的超额风险界为$O\left(
\frac1{\sqrt{\lambda n}}
\right).$但这个收敛界并不是最优

Propostion 4.6就是对于超额风险进行改进

考虑线性预测函数

\[ f_\theta(x)=\theta^\top\varphi(x), \qquad \theta\in\mathbb R^d. \]

假设：

1. 损失函数关于预测值是 \(G\)-Lipschitz 连续的：

   \[ |\ell(y,u)-\ell(y,v)| \leq G|u-v|. \]

2. 损失函数关于预测值是凸函数。

3. 特征向量几乎处处有界：

   \[ \|\varphi(x)\|_2\leq R. \]

4. \(\hat\theta_\lambda\) 是正则化经验风险最小化问题的解：

   \[ \boxed{ \hat\theta_\lambda \in \arg\min_{\theta\in\mathbb R^d} \left\{ \widehat{\mathcal R}(\theta) + \frac{\lambda}{2}\|\theta\|_2^2 \right\}. } \]

那么

\[ \boxed{ \mathbb E \left[ \mathcal R(\hat\theta_\lambda) \right] \leq \inf_{\theta\in\mathbb R^d} \left\{ \mathcal R(\theta) + \frac{\lambda}{2}\|\theta\|_2^2 \right\} + \frac{24G^2R^2}{\lambda n}. } \]

这里的期望是关于训练数据集 \(D\) 取的。

本命题的证明主线是：

\[ \boxed{ \text{强凸性定位} \to \text{局部参数球} \to \text{局部 Rademacher complexity} \to \frac{1}{\lambda n}\text{ 快速率}. } \]
