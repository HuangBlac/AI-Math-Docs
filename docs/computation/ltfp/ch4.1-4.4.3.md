# Empirical Risk Minimization——经验风险极小化

算法的意义在于三点：

1我们不知道真正的函数，只是管中窥豹

2实数集真的很大，我们不可能搜索每一个可测函数

3我们没有无限的时间去逐点搜索



Convexification of the risk: For binary classification, optimal predictions can be
achieved with convex surrogates.

对于二分类问题，优化预测可以转化为凸优化问题，convexification凸化

 Risk decomposition: The risk can be decomposed into the sum of the approximation
error (which characterizes the modeling assumptions made by the chosen class of
functions) and the estimation error (which characterizes the effect of having a finite
number of observations).

风险分解，风险可以被分解为：

逼近误差（建模的假设所选取的函数类的逼近效率，主要由逼近理论）

估计误差（由于样本的观测有限，主要由高维概率公式）

Rademacher complexity: To study estimation errors and compute expected uniform
deviations of real-valued outputs, Rademacher complexities, also referred to as
Rademacher averages, are a very flexible and powerful tool that allows obtaining
uniform deviation bounds. This leads to dimension-independent upper bounds on
estimation errors for constrained or penalized linear predictors.

Rademacher复杂度，为了研究估计误差，并计算从实际结果出发的期望均匀偏差

也被称之为一Ramacher averages,是一个获得一致偏差有界的方法，这会导出一个与维度无关的上界。对于有界的线性预测结果。

对于分类问题以及一系列的机器学习问题，实际上就是需要找到一个满足泛函极小化的问题：

$f^* = argmin_f \mathcal{L}(f)=\mathbb{E}_{(X,Y)\sim \mathbb P } l(f(X),Y)$

但是，我们并不知道真实的数据分布，所以实际采用的使用平均值来代替：

In this chapter, we will consider methods based on empirical risk minimization, with a
focus on statistical analysis (i.e., generalization to unseen data);

optimization algorithms to efficiently find approximate minimizers will be studied in chapter 5. Before looking at the necessary probabilistic tools, we will show how problems where the output space is
not a vector space, such as binary classification with Y = {-1, 1}, can be reformulated
as real-valued outputs, with so-called convex surrogates of loss functions.

在这个部分，我们将会考虑基于经验风险最小化的方法，并聚焦于统计的分析方法。

关于如何使用优化算法来高效获得这些近似极小化的主要集中在chapeter 5。在此之间看看必要的概率工具，我们将会展示当目标不是一个向量空间，例如二分类对应的 Y = {-1, 1}时将会出现哪些问题，以及它们实际上可以被重塑为一个实数输出的问题，通过使用所谓的凸化损失函数。

# Ch 4.1 Convexification of the Risk凸化风险

在这个部分，我们将会考虑基于经验风险最小的方法，使用统计分析的方法，例如从未知数据之中进行泛化

那么，对于这个二分类问题的时候，对应的损失函数应该是什么？

实际上就是$l(f(X),Y) =1_{f(X)\neq Y}$只要两者不相等，那么就令其为1

对于二分类问题之中Y只有$\{+1,-1\}$两种，对于这种离散值域的问题，显然就不好做。所以我们需要考虑进行一个操作：凸化。

首先f可以被表示为f(x) = sign(g(x)) ,g(x)为一个可微函数

sign(a) =1 if a > 0 −1 if a < 0.

但是这个sign不太好，它是不连续的，而且实际上也不能这么直接套进去，因为此时在零点没有定义

所以将原问题转化为选取一个g

$\mathcal{L}(g) = argmin_{(X,Y)\sim \mathbb P}P(f(X)\neq Y) = argmin_{(X,Y)\sim \mathbb P}P(sign(g(X))\neq Y) = argmin_{(X,Y)\sim \mathbb P}P(Yg(X)<0)$

实际上就是要找一个Yg(X)异号的概率尽可能小，或者同号的概率尽可能大。

我们重新写成期望的形式：

$E[Φ_{0-1}(yg(x))]$,
```math
Φ_{0-1}(u)= 1 (u<0),1/2(u = 0),0 (u>0)
```
因此原函数依然转化为了选取g使得期望极小化的问题

### Ch4.1.1Convex Surrogates

但是，那个问题没有消失，$Φ_{0-1}$是不连续的，所以我们可以采用集中不同的近似方式，对应不同的模型。

**平方损失** 

$\Phi(u)=(u-1)^2$。因为 $y^2=1$,所以 $\Phi(yg(x))=(y-g(x))^2$,这就退回到了最小二乘回归,预测时取 $g(x)$ 的符号。注意它是图里唯一在 $u>1$ 后又往上翘的——对"分得太对"也会惩罚,这是它和其它(单调不增的)损失的区别。

**Logistic 损失** $\Phi(u)=\log(1+e^{-u})=-\log\sigma(u)$其中$\sigma$ 是 sigmoid，对应逻辑回归,也就是常说的交叉熵;从概率角度看,令 $\mathbb{P}(y=1\mid x)=\sigma(g(x))$,这个风险就是负的条件对数似然(第 14 章细讲)。

**Hinge 损失** $\Phi(u)=\max(1-u,0)$。配上线性预测器就是 SVM,这里的 $yg(x)$ 就是"间隔"一词的出处(几何解释在带菱形的 4.1.2)。

**平方 hinge** $\max(1-u,0)^2$,hinge 的光滑版。

**指数损失** $\Phi(u)=e^{-u}$,boosting / Adaboost 里用的

### Ch4.1.2 Geometric Interpretation of the Support Vector Machine

事实上，Hinge损失对应的实际上就是SVM支持向量机,我们可以考虑支持向量机的几何解释。

支持向量机需要找到一个分离的平面，让正例尽可能在上面而反例尽可能在下面。

距离实际上可以用$\frac{wx_i+b}{\|w\|_2}$表示，其中正号表示与这个超平面法向量$w$方向相同，而负号表示不同。我们希望给定的超平面恰好能够将其分离开来，正例对应正号而反例对应负号。

在分准的基础上，如果实际上就是要让$\frac{y_i(wx_i+b)}{\|w\|_2}$都尽可能大，也就是所有的点都离它尽可能远，那就说明分好了

更具体来说，实际上就是要考虑距离超平面最近的训练样本，它将决定整个分类器的几何间隔：
$$
\gamma(w,b)
=
\min_{1\le i\le n}
\frac{y_i(w^\top x_i+b)}{\|w\|_2}
.
$$
SVM 希望最大化它：
$$
\max_{w,b}
\min_i
\frac{y_i(w^\top x_i+b)}{\|w\|_2}.
$$
然后我们很自然的就可以将其转化为固定分子大于等于1而极小化分母的情况，也就是:
$$
\min_w\frac{1}{2}\|w\|^2_2,s.t,\forall i\in\{1,2,\cdots,n\} y_i(w^\top x_i+b)\ge1
$$
对于这类不等式约束的问题，依然想办法约束条件打包进待优化的目标函数，也就是
$$
\min_w\frac{1}{2}\|w\|^2_2+C\sum_{i=1}^n\xi_i,s.t,\forall i\in\{1,2,\cdots,n\} y_i(w^\top x_i+b)\ge1-\xi_i,\xi\ge0
$$
对于达到边界的样本增加$\xi_i$来约束

然后，我们就可以倒反天罡，将$\xi_i$视作待优化的目标，而那个$\frac{1}{2}\|w\|_2^2$视作正则化参数
$$
\min_w\frac{\lambda}{2}\|w\|^2_2+\frac{1}{n}\sum_{i=1}^n(1-y_i(w^{\top}x_i+b))_{+}
$$
呃呃，然后我们怎么去求解这个问题呢？

拉格朗日对偶：对于要想求解(5)对应的问题，实际上可以构造拉格朗日对偶函数，也就是选取：

实际上就是通过引入$\alpha$对偶项来让不等式变成等式

也就是$\alpha(1-y_i(w^\top x_i+b))=0$,当$\alpha>0$时对应达到支持向量的部分，而$\alpha=0$则是没有达到。

而我们回忆4.1.1所得到的部分，这个hinge损失函数实际上就是对于原始的分类函数的一个“凸化”

我们也就此将不同的分类算法统一起来，例如Logistic，支持向量机。



### 4.1.3 Conditional -risk and Classification Calibration

## Ch4.2误差分解

但我们并不是从真实分布来求取$f^*$这个理论最佳函数，也不是在所有可能的函数空间内

以这个分布问题为例，我们实际上是

我们这里有n个样本$\{(X_i,Y_i)\}$其中，每一个样本都是独立同分布的。
```math
\hat f = argmin_{f\in \mathcal{F}} \frac{1}{n}\sum_{i=1}^n l(f(X_i),Y_i)
```
大数定理告诉我们，频率趋近于概率。但是这毕竟还是有差别，更具体来说，我们可以将其拆成两个部分
```math
\mathcal{L}(\hat f) - \mathcal L({f^*}) = \mathcal{L}(\hat f)  - inf_{f\in \mathcal F} \mathcal L(f)  +  inf_{f\in \mathcal F} \mathcal L(f) - \mathcal L({f^*})
```
前者是由样本所导致的，被称之为估计误差estimation error

后者则是由于$\mathcal{F}$这个函数类不够大导致的，也被称之为逼近误差

Ch4.3 Approximation

我们先来分析一下逼近误差这个成分：

我们对于函数类往往考虑这样的情形，这也符合实际算法的构建：$\mathcal{F} = \{f_{\theta} |\theta\in\Theta\}$

举个例子，神经网络函数空间$\mathcal{NN}(2,100,\theta)，L\le2,W\le 100,|B|\le 10$

表示一个两层，宽度100，神经元绝对值参数小于等于10的网络对应的一个函数空间。而且严格来说，$\Theta$在计算机之中只能取离散的值，例如double,float。

考虑这一点，我们可以将逼近误差进一步的分解：
```math
inf_{\theta \in \Theta} \mathcal L(f) - \mathcal L({f^*}) =inf_{\theta \in \Theta}\mathcal L(f_\theta) - inf_{\theta \in R^n} \mathcal L(f_\theta) + inf_{\theta \in R^n}\mathcal L(f_\theta)- \mathcal L({f^*})
```
事实上，第二个部分是我们单纯依靠提高精度什么的无法解决的，除非我们改变算法本身的结构，也被称之为不可压缩项。

而且，对于固定的模型例如神经网络，或者SVM实际上往往可以被压缩到很小，因为万能逼近定理等操作，但我们的重点先是分析第一块。

我们考虑一个具体的回归情景：

$f_{\theta}(x) = \theta^T\varphi(x)$

因此第一部分的误差可以根据损失函数关于第二边缘G-Lipicisz写成如下的形式
```math
\mathcal L(f_θ)−\mathcal L(f_{θ′})=E[ℓ(y,f_θ(x))−ℓ(y,f_{θ′}(x))]≤GE[∣f_θ(x)−f_{θ′}(x)∣]
```
其次，我们假设$||\theta||_2\le D$

在经典范例 $f_\theta(x) = \theta^\top \varphi(x)$下

预测差表示为 $|f_\theta(x) - f_{\theta'}(x)| = |(\theta-\theta')^\top \varphi(x)| \leq \|\theta-\theta'\|_2\,\|\varphi(x)\|_2$。代回去,约束代价就被压成
```math
\inf_{\theta\in\Theta} R(f_\theta) - \inf_{\theta'\in\mathbb{R}^d} R(f_{\theta'}) \;\leq\; G\,\mathbb{E}\big[\|\varphi(x)\|_2\big]\cdot \inf_{\|\theta\|_2\leq D}\|\theta - \theta_\ast\|_2
```
而对于练习当中认为$||\theta||_1\le D$，依然可以使用Holder不等式
```math
\inf_{\theta\in\Theta} R(f_\theta) - \inf_{\theta'\in\mathbb{R}^d} R(f_{\theta'}) \;\leq\; G\,\mathbb{E}\big[\|\varphi(x)\|_{\infty}\big]\cdot \inf_{\|\theta\|_1\leq D}\|\theta - \theta_\ast\|_1
```


当然，分析完逼近误差之后，我们需要考虑估计误差

估计误差 $R(\hat f) - \inf_{f\in\mathcal{F}} R(f)$ 没法逐点控制,根子在于 $\hat f$ 是从数据里选出来的.

书上的做法就是将其转化为一个一致偏差

**一致偏差**:
```math
R(\hat f) - \inf_{f\in\mathcal{F}} R(f) \;\leq\; 2\sup_{f\in\mathcal{F}} \big|\hat R(f) - R(f)\big|
```
推导过程：
```math
R(\hat f) - \inf_{f\in\mathcal{F}} R(f) = R(\hat f) - R(g_{\mathcal F}) = \underbrace{\{R(\hat f) - \hat R(\hat f)\}}_{\text{①}} + \underbrace{\{\hat R(\hat f) - \hat R(g_{\mathcal F})\}}_{\text{②}} + \underbrace{\{\hat R(g_{\mathcal F}) - R(g_{\mathcal F})\}}_{\text{③}}
```
对于第一项，第三项，都可以被$\sup_{f\in\mathcal{F}}\big(R(f) - \hat R(f)\big)$控制

对于第二项，由于$\hat R(\hat f) \le \hat R(g_{\mathcal F})$,$\hat{f}$是$\hat{R}$的极小化结果

4.4 Estimation Error

记 $H(z_1,\dots,z_n) = \sup_{f\in\mathcal{F}}\big(R(f) - \hat R(f)\big)$。损失有界在 $[0,\ell_\infty]$ 时,**改动单个样本 $z_i$,$H$ 至多变化 $\ell_\infty/n$**(有界差分性质)。于是 McDiarmid 不等式给出集中:以概率 $\geq 1-\delta$,
```math
H - \mathbb{E}[H] \;\leq\; \frac{\ell_\infty}{\sqrt{2n}}\sqrt{\log\tfrac{1}{\delta}}
```
我们接下来需要证明这个不等式，是通过**Doob martingale + Hoeffding 引理 + Chernoff bound** 推出来。

定义 filtration：
```math
\mathcal F_i=\sigma(Z_1,\dots,Z_i),
```
表示“已经看到前 $i$ 个样本”。

定义
```math
M_i=\mathbb E[H\mid Z_1,\dots,Z_i].
```

```math
H-\mathbb EH
=
M_n-M_0
=
\sum_{i=1}^n (M_i-M_{i-1}).
```

记 martingale difference 为
```math
D_i=M_i-M_{i-1}.
```
因此问题变成控制
```math
\sum_{i=1}^n D_i.
```

3. 关键：证明每一步的波动被 $c_i$ 控制

固定前面的变量
```math
Z_1=z_1,\dots,Z_{i-1}=z_{i-1}.
```
考虑函数
```math
\phi_i(z_i)
=
\mathbb E_{Z_{i+1},\dots,Z_n}
\left[
H(z_1,\dots,z_{i-1},z_i,Z_{i+1},\dots,Z_n)
\right].
```
也就是说，$\phi_i(z_i)$ 是在前 $i-1$ 个变量固定、第 $i$ 个变量取值为 $z_i$ 时，对后面的变量取期望。

因为 $H$ 满足 bounded difference 条件，所以只改变第 $i$ 个变量时，
```math
|H(\dots,z_i,\dots)-H(\dots,z_i',\dots)|\le c_i.
```
对后面的随机变量取期望后，这个差距仍然不超过 $c_i$，因此
```math
|\phi_i(z_i)-\phi_i(z_i')|\le c_i.
```
所以 $\phi_i(Z_i)$ 的取值范围长度不超过 $c_i$。

而
```math
M_i=\phi_i(Z_i),
```
因此
```math
D_i
=
M_i-M_{i-1}
=
\phi_i(Z_i)-\mathbb E[\phi_i(Z_i)\mid \mathcal F_{i-1}].
```
它是一个条件均值为零的随机变量，并且它的条件取值范围长度不超过 $c_i$。

也就是说：
```math
\mathbb E[D_i\mid \mathcal F_{i-1}]=0,
```
且在给定 $\mathcal F_{i-1}$ 后，
```math
D_i \in [a_i,b_i],
\qquad b_i-a_i\le c_i.
```
使用 Hoeffding 引理

Hoeffding 引理说：

如果随机变量 $X$ 满足
```math
\mathbb E X=0,
\qquad X\in[a,b],
```
Hoeffding引理：

那么对任意 $\lambda>0$，
```math
\mathbb E e^{\lambda X}
\le
\exp\left(\frac{\lambda^2(b-a)^2}{8}\right).
```
这里对 $D_i$ 使用条件版 Hoeffding 引理：
```math
\mathbb E\left[
e^{\lambda D_i}
\mid
\mathcal F_{i-1}
\right]
\le
\exp\left(
\frac{\lambda^2c_i^2}{8}
\right).
```
控制整体矩母函数

因为
```math
H-\mathbb EH
=
\sum_{i=1}^n D_i,
```
所以
```math
\mathbb E e^{\lambda(H-\mathbb EH)}
=
\mathbb E e^{\lambda\sum_{i=1}^n D_i}.
```
用条件期望一层一层剥掉：
```math
\mathbb E e^{\lambda\sum_{i=1}^n D_i}
=
\mathbb E\left[
e^{\lambda\sum_{i=1}^{n-1}D_i}
\mathbb E(e^{\lambda D_n}\mid \mathcal F_{n-1})
\right].
```
由 Hoeffding 引理，
```math
\mathbb E(e^{\lambda D_n}\mid \mathcal F_{n-1})
\le
\exp\left(
\frac{\lambda^2c_n^2}{8}
\right).
```
于是
```math
\mathbb E e^{\lambda\sum_{i=1}^nD_i}
\le
\exp\left(
\frac{\lambda^2c_n^2}{8}
\right)
\mathbb E e^{\lambda\sum_{i=1}^{n-1}D_i}.
```
不断递推，得到
```math
\mathbb E e^{\lambda(H-\mathbb EH)}
\le
\exp\left(
\frac{\lambda^2}{8}
\sum_{i=1}^n c_i^2
\right).
```
用 Chernoff bound 得到尾界

对任意 $\lambda>0$，
```math
\mathbb P(H-\mathbb EH>t)
=
\mathbb P(e^{\lambda(H-\mathbb EH)}>e^{\lambda t}).
```
由 Markov 不等式，
```math
\mathbb P(H-\mathbb EH>t)
\le
e^{-\lambda t}
\mathbb E e^{\lambda(H-\mathbb EH)}.
```
代入上面的矩母函数界：
```math
\mathbb P(H-\mathbb EH>t)
\le
\exp\left(
-\lambda t
+
\frac{\lambda^2}{8}\sum_{i=1}^n c_i^2
\right).
```
现在对 $\lambda$ 优化。

令
```math
C=\sum_{i=1}^n c_i^2.
```
需要最小化
```math
-\lambda t+\frac{\lambda^2C}{8}.
```
求导：
```math
-t+\frac{\lambda C}{4}=0.
```
所以
```math
\lambda=\frac{4t}{C}.
```
代回去：
```math
-\lambda t+\frac{\lambda^2C}{8}
=
-\frac{4t^2}{C}
+
\frac{16t^2}{C^2}\frac{C}{8}
=
-\frac{4t^2}{C}
+
\frac{2t^2}{C}
=
-\frac{2t^2}{C}.
```
因此
```math
\boxed{
\mathbb P(H-\mathbb EH>t)
\le
\exp\left(
-\frac{2t^2}{\sum_{i=1}^n c_i^2}
\right)
}
```
这就是 McDiarmid 不等式。

我们让这个概率变成$\delta$,就可以得到$t = \frac{\ell_\infty}{\sqrt{2n}}\sqrt{\log(2/\delta)}$

把"高概率界定 $H$"**化简成"只需界定它的期望 $\mathbb{E}[H]=\mathbb{E}[\sup_f(R-\hat R)]$"**,再加一个 $\frac{\ell_\infty}{\sqrt{2n}}\sqrt{\log(2/\delta)}$ 的尾项就够了。

最终我们可以

**4.4.2 二次损失(暖身一):** 取平方损失 $\ell=(y-\theta^\top\varphi(x))^2$ 加 $\|\theta\|_2\leq D$ 的约束。

```math
\hat R(f)-R(f) = \theta^\top\Big(\underbrace{\tfrac1n\textstyle\sum_i \varphi(x_i)\varphi(x_i)^\top - \mathbb{E}[\varphi(x)\varphi(x)^\top]}_{\text{矩阵偏差 } \Delta_2}\Big)\theta \;-\;2\theta^\top\underbrace{\Big(\tfrac1n\textstyle\sum_i y_i\varphi(x_i)-\mathbb{E}[y\varphi(x)]\Big)}_{\text{向量偏差 }\Delta_1} \;+\;\underbrace{\Big(\tfrac1n\textstyle\sum_i y_i^2-\mathbb{E}[y^2]\Big)}_{\text{标量偏差 }\Delta_0}
```
要点在于:**它关于 $\theta$ 是个二次型**(二次项 + 线性项 + 常数)。

偏差展开成三项

- 二次项:$|\theta^\top\Delta_2\,\theta|\leq \|\Delta_2\|_{\text{op}}\|\theta\|_2^2 \leq D^2\|\Delta_2\|_{\text{op}}$(用算子范数,$\|\Delta_2\|_{\text{op}}=\sup_{\|u\|_2=1}\|\Delta_2 u\|_2$);
- 线性项:$|2\theta^\top\Delta_1|\leq 2\|\theta\|_2\|\Delta_1\|_2 \leq 2D\|\Delta_1\|_2$(Cauchy–Schwarz);
- 常数项:就是 $|\Delta_0|$。

合起来:
```math
\sup_{\|\theta\|_2\leq D}\big|R(f)-\hat R(f)\big| \;\leq\; D^2\,\big\|\Delta_2\big\|_{\text{op}} \;+\; 2D\,\big\|\Delta_1\big\|_2 \;+\; \big|\Delta_0\big|
```
**$\theta$ 和 sup 在这一步就被彻底消掉了。**

由于关于 $\theta$ 是二次的,在球上的 sup 能**闭式**算出来(用算子范数),于是只剩三个**非一致**的偏差,每个都是 $O(1/\sqrt n)$,直接拼出 $O(1/\sqrt n)$ 的一致界。

教训:平方损失靠闭式很轻松,但别的损失没有闭式,所以**必须引入新工具**。

(书还提醒:从这节起不再要求损失是凸的)

**4.4.3 有限模型类(暖身二):** $\mathcal{F}$ 有限时,用并集界把 sup 拆开,对每个 $f$ 套 Hoeffding,得到

**第一步,并集界把 sup 拆成逐个。** "存在某个 $f $ 偏差 $\geq t $"这件事,无非是"各个 $f $ 偏差 $\geq t $"这些事件的并,于是概率可加:
```math
\mathbb{P}\Big(\sup_{f\in\mathcal{F}}\big(\hat R(f)-R(f)\big)\geq t\Big) \;\leq\; \sum_{f\in\mathcal{F}}\mathbb{P}\big(\hat R(f)-R(f)\geq t\big)
```
这一步的好处是右边每一项都是**固定的** $f $,sup 的纠缠没了。

**第二步,对每个固定 $f$ 套 Hoeffding。** $\hat R(f)$ 是 $n$ 个有界独立量的平均,期望为 $R(f)$,所以 $\mathbb{P}\big(\hat R(f)-R(f)\geq t\big)\leq \exp(-2nt^2/\ell_\infty^2)$。代回去,$|\mathcal{F}|$ 项一加(连同两侧的因子 2):
```math
\mathbb{P}\Big(\sup_{f\in\mathcal{F}}\big(\hat R(f)-R(f)\big)\geq t\Big) \;\leq\; 2|\mathcal{F}|\exp\!\Big(\frac{-2nt^2}{\ell_\infty^2}\Big)
```
**第三步,令右边 $=\delta $ 反解 $t $。** 得到:以概率 $\geq 1-\delta $,
```math
\sup_{f\in\mathcal{F}}\big(\hat R(f)-R(f)\big) \;\leq\; \frac{\ell_\infty}{\sqrt{2n}}\sqrt{\log\frac{2|\mathcal{F}|}{\delta}} \;\leq\; \ell_\infty\sqrt{\frac{\log(2|\mathcal{F}|)}{2n}} \;+\; \frac{\ell_\infty}{\sqrt{2n}}\sqrt{\log\frac{1}{\delta}}
```



```math
\mathbb{E}\Big[\sup_{f\in\mathcal{F}}\big(\hat R(f) - R(f)\big)\Big] \;\leq\; \ell_\infty\sqrt{\frac{\log(2|\mathcal{F}|)}{2n}}
```
结论很干净:**当 $\log|\mathcal{F}| \ll n$ 时学习就可行**。函数类的"大小"只通过 $\log|\mathcal{F}|$ 进来。这是对一致偏差的第一个通用控制。
