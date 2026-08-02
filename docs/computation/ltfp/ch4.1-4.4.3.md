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
$$
\min_w\frac{1}{2}\|w\|^2_2+C\sum_{i=1}^n\xi_i-\sum_{i=1}^n\alpha_i(y_i(w^\top x_i+b)-1+\xi_i)-\sum_{i=1}^n \beta_i\xi_i
$$
然后我们将目标转化为优化$w,b,\xi_i$关于这些变量求偏导要为0得到极小值

$C=\alpha_i+\beta_i,w=\sum_{i=1}^n \alpha_iy_ix_i,\sum_{i=1}^n\alpha_iy_i=0$

重新带入原始式子，得到：
$$
\max_{\alpha_i}\sum_{i=1}^n\alpha_i-\sum_{i=1}^n\sum_{j=1}^n\alpha_i\alpha_jy_iy_jx_i^\top x_j\\
\sum_{i=1}^n\alpha_iy_i=0
$$


也就是$\alpha(1-y_i(w^\top x_i+b))=0$,当$\alpha>0$时对应达到支持向量的部分，而$\alpha=0$则是没有达到。

而我们回忆4.1.1所得到的部分，这个hinge损失函数实际上就是对于原始的分类函数的一个“凸化”

我们也就此将不同的分类算法统一起来，例如Logistic，支持向量机。



### 4.1.3 Conditional $\Phi$-risk and Classification Calibration

\(\text{二分类} \rightarrow 0\text{-}1\text{ 风险} \rightarrow \text{Bayes 分类器} \rightarrow \text{替代损失} \rightarrow \text{条件替代风险} \rightarrow \text{分类校准}.\)

对于二分类，实际上就是已知X=x,预测$Y\in\{-1,1\}$

通常先学习一个实值评分函数

\[ g:\mathcal X\to\mathbb R, \]

再根据符号进行分类：

\[ f_g(x)=\operatorname{sign}(g(x)). \]

这里：

- \(g(x)>0\)：预测 \(+1\)；
- \(g(x)<0\)：预测 \(-1\)；
- \(|g(x)|\) 可以理解为预测的确信程度或分类间隔。

注意：真正用于分类的是 \(\operatorname{sign}(g(x))\)，而不是 \(g(x)\) 的精确数值。

分类正确等价于$Yg(X)>0$

因为：

- 若 \(Y=+1\)，正确分类要求 \(g(X)>0\)；
- 若 \(Y=-1\)，正确分类要求 \(g(X)<0\)。

所以可以将 \(Yg(X)\) 称为“带符号间隔”：

\[ \text{margin}=Yg(X). \]

可以选取一个风险衡量:\(\mathcal R(g) = \mathbb E\big[\Phi_{0-1}(Yg(X))\big].\)

其中

\[ \Phi_{0-1}(u)= \begin{cases} 1,&u<0,\\[2mm] \frac12,&u=0,\\[2mm] 0,&u>0. \end{cases} \]

若我们选取$η(x) = P(y = 1|x) \in [0, 1]$, 我们有期望计算$E[y|x] = 2η(x)−1$,

我们固定一个x，对于不同的分类器，就可以得到一个分数g(x)，记作u

### 如果 \(u>0\)

我们预测 \(+1\)。只有 \(Y=-1\) 时出错，所以条件错误率为

\[ 1-\eta(x). \]

### 如果 \(u<0\)

我们预测 \(-1\)。只有 \(Y=+1\) 时出错，所以条件错误率为

\[ \eta(x). \]

### 如果 \(u=0\)

随机选择正负标签，错误率为

\[ \frac12. \]

因此，固定 \(x\) 后的条件 \(0\text{-}1\) 风险是

\[ C_{\eta(x)}(u)= \begin{cases} 1-\eta(x),&u>0,\\[1mm] \frac12,&u=0,\\[1mm] \eta(x),&u<0. \end{cases} \]

正如2.2.3部分计算的贝叶斯风险（最佳风险)等于
$$
\mathcal R^∗ = E[min(η(x), 1 − η(x))] = E[\frac1
2 − \frac1
2 |E[y|x]|]

,
$$

$$
f_∗(x) = sign(2η(x) − 1) = sign(E[y|x])
$$

往往采取逼近$g(x)=E(y|x)$

在实际算法之中，往往使用$\Phi(u)$代替$\Phi_{0-1}(u)$

其中\[ u=Yg(X) \]是分类间隔。

理想情况下，我们真正想最小化的是 \(0\text{-}1\) 风险：\[ \mathcal R(g) = \mathbb E\big[\Phi_{0-1}(Yg(X))\big]. \]

但是这是一个间断函数，非光滑而且非凸，几乎处处导数为零。使得我们想要梯度下降优化g会使得g的变化速度被$\Phi_{0-1}(u)$的导数被直接吃掉，于是我们就只能做一些替代。



平方损失

在讨论一般的函数 $\Phi$ 之前，我们先考察平方损失，因为在这种情况下，论证较为简单。

事实上，正如第 2 章中所看到的，此时使期望 $\Phi$-风险最小的函数为
$$
g(x)=\mathbb E[Y\mid X=x]=2\eta(x)-1.
$$
对 $g(x)$ 取符号，就能得到最优的分类预测。

因此，在二分类问题中使用平方损失，可以在总体分布层面得到最优预测。

一般损失

为了研究平方损失以外的一般 $\Phi$-风险所产生的影响，我们首先固定一个给定的 $x$，考察该点处的条件风险。

与 $0\text{-}1$ 损失的情形相同，使 $\Phi$-风险最小的函数 $g$，可以通过对每个 $x$ 分别进行最小化来确定。

此时，只要知道条件概率
$$
\eta(x)=\mathbb P(Y=1\mid X=x),
$$
就足以刻画该点 $x$​ 处的最优预测，以及由此产生的超额风险。固定 \(X=x\) 后，标签只有两种可能，因此使用替代损失 \(\Phi(Yu)\) 的条件期望是





Def 4.1:条件$\Phi-Risk$

\[ C_\xi^\Phi(u) = \xi\Phi(u)+(1-\xi)\Phi(-u), \]

以及

\[ C_\xi(u) = \xi\Phi_{0-1}(u)+(1-\xi)\Phi_{0-1}(-u). \]

由条件期望公式，

\[ \mathcal R_\Phi(g) =\mathbb E[\Phi(Yg(X))] =\mathbb E_X\!\left[C_{\eta(X)}^\Phi(g(X))\right]. \]

所以在不限制函数类的总体情形下，最小化 \(R_\Phi(g)\) 可以逐个 \(x\) 地研究：

\[ g^*(x)\in\arg\min_{u\in\mathbb R}C_{\eta(x)}^\Phi(u). \]

这正是定义条件替代风险的核心用途。

定义解释：

\(\xi=\eta(x)=P(Y=1\mid X=x).\)表示条件概率

为什么有时是u,有时是-u？因为u其实代入的是x的分数g(x)，而在$\Phi_{0-1}$里面代入的其实是$Yg(X)$，是一个大于零输出0，小于零输出1的函数，并且希望让这个东西极小，$\xi$是输出的量表示预测的错误率。

但是我们如果要优化0-1函数就做不到这一点，虽然它是最符合原始二分类意义的方法，但是它间断；导数处处为 0无法是使用基于梯度的优化算法来操作，使用bp会导致梯度消失；而且非凸，不能使用凸优化的性质，所以要使用$C_{\xi}^{\Phi}$来代替。

所以，什么情况选取的这个$\Phi$可以实现分类呢？这也就是下面这个命题所证明的

Proposition 4.1：设 \(\Phi:\mathbb R\to\mathbb R\) 是一个凸函数。替代损失函数 \(\Phi\) 是分类校准的，当且仅当 \(\Phi\) 在 \(0\) 点可微，并且

\[ \Phi'(0)<0. \]

必要性证明：\(\Phi\text{ 分类校准} \Longrightarrow \Phi\text{ 在 }0\text{ 处可微且 }\Phi'(0)<0.\)

首先证明在0点可微$\Phi'(0_+)=\Phi'(0_-)$

先证明Φ是凸函数时 \(C_\xi^\Phi\) 也是凸函数，因为$C(u)$其实是$\Phi(u)$与$\Phi(-u)$的凸组合，而这两个函数实际上都是凸函数，因此$C_{\xi}^\Phi(u)$也是凸函数

$\Phi'(0_+)=\lim_{h\to0_+}\frac{\Phi(h)-\Phi(0)}{h},\Phi'(0_-)=\lim_{h\to0_-}=\frac{\Phi(h)-\Phi(0)}{h}$

对于凸函数，实际上右导数大于等于左导数，

那么$\Phi'(0_+)-\Phi'(0_-)\ge0，C_\xi^{\Phi '}(0_+)\ge C_\xi^{\Phi '}(0_-)$

接下来，根据分类校正方法：$\Phi$

现在假设 \(\Phi\) 已经分类校准。

当\[ \xi>\frac12 \]

时，Bayes 最优预测为 \(+1\)。分类校准要求

\[ \arg\min_u C_\xi^\Phi(u)\subset\mathbb R_+^*. \]

根据条件 (a)：

\[ (C_\xi^\Phi)'(0+)<0. \]

也就是

\[ \xi\Phi'(0+) - (1-\xi)\Phi'(0-) <0. \]

现在令

\[ \xi\downarrow\frac12. \]

因为原来是不等式严格小于零，取极限后只能得到小于等于零：

\[ \frac12\Phi'(0+) - \frac12\Phi'(0-) \le0. \]

即

\[ \boxed{ \Phi'(0+)-\Phi'(0-)\le0. } \]

最终可以推出在0点可微

既然左右导数相等，统一记为

\[ \Phi'(0). \]

于是条件风险在零点的导数变成

\[ \begin{aligned} (C_\xi^\Phi)'(0) &= \xi\Phi'(0)-(1-\xi)\Phi'(0)\\ &= (2\xi-1)\Phi'(0). \end{aligned} \]

当 \(\xi>1/2\) 时，分类校准要求

\[ (C_\xi^\Phi)'(0)<0. \]

所以

\[ (2\xi-1)\Phi'(0)<0. \]

由于

\[ 2\xi-1>0, \]

只能得到

\[ \boxed{\Phi'(0)<0.} \]

因此我们证明了必要性：

\[ \Phi\text{ 分类校准} \Longrightarrow \Phi\text{ 在 }0\text{ 处可微且 }\Phi'(0)<0. \]

充分性现在反过来假设：\[ \Phi\text{ 在 }0\text{ 处可微},\Phi'(0)<0. \]

那么\[ (C_\xi^\Phi)'(0) = (2\xi-1)\Phi'(0). \]

当 \(\xi>1/2\) 时：

\[ (C_\xi^\Phi)'(0)<0. \]

根据 (a)，条件风险的极小点严格位于正半轴，因此预测 \(+1\)。

当 \(\xi<1/2\) 时：

\[ (C_\xi^\Phi)'(0)>0. \]

根据 (b)，极小点严格位于负半轴，因此预测 \(-1\)。

两种情况都与 Bayes 分类器一致，所以 \(\Phi\) 分类校准。

### 4.1.4 Relation between Risk and $\Phi$-risk

在这一部分之中主要研究使用$\Phi$-risk来代替会有什么影响，经过了这么一番替代之后有什么好处？

上一节我们已经证明了：

\[ \mathcal R_\Phi(g)=\mathcal R_\Phi^* \quad\Longrightarrow\quad \mathcal R(g)=\mathcal R^*. \]

或者从条件风险来看：

\[ u\in\arg\min C_\xi^\Phi \quad\Longrightarrow\quad u\in\arg\min C_\xi. \]

实中我们几乎不可能精确达到

\[ \mathcal R_\Phi(g)=\mathcal R_\Phi^*. \]

由于有限样本、模型限制和优化误差，我们通常只能得到

\[ \mathcal R_\Phi(g)-\mathcal R_\Phi^* \le \varepsilon. \]

这时需要回答：

> 替代风险距离最优值还有 \(\varepsilon\)，真正的分类风险距离 Bayes 风险还有多远？

4.1.4 首先要证明的是,

\[ \boxed{ \mathcal R(g)-\mathcal R^* \le H\!\left( \mathcal R_\Phi(g)-\mathcal R_\Phi^* \right). } \]

它回答的是“两个优化问题距离终点的关系”。

当然，已知$\mathcal R^{\Phi}$实际上就是关于$C_{\xi}^{\Phi}$求期望，只需证明：
$$
\forall u\in \mathbb R,G[C_\xi(u)-\inf_{u'}C_\xi(u')]\le C_\xi^\Phi(u)-\inf_{u'}C_\xi^\Phi(u')
$$
其中G是一个凸函数

如果我们已经有（15），那么就可以
$$
G[\mathcal R(g)-\mathcal R_*]\le G\mathbb E[C_\xi(u)-\inf_{u'}C_\xi(u')]\le \mathbb E G[C_\xi(u)-\inf_{u'}C_\xi(u')]\le\mathbb EG[C_\xi^\Phi(u)-\inf_{u'}C_\xi^\Phi(u')]\le\mathbb EG[C_\xi^\Phi(u)-\inf_{u'}C_\xi^\Phi(u')] =\mathcal R^\Phi(g)-\mathcal R^{\Phi}_*
$$

要想计算最终目标，可以先计算\[ \Delta_{01}(\xi,u) = C_\xi(u)-\inf_{u'\in\mathbb R}C_\xi(u'), \]

即固定正类概率 \(\xi\) 后，当前分数 \(u\) 比最优分类多付出了多少 \(0\text{-}1\) 风险。

## 1. 先写出 \(C_\xi(u)\)

条件 \(0\text{-}1\) 风险为\[ C_\xi(u) = \xi\Phi_{0-1}(u) + (1-\xi)\Phi_{0-1}(-u). \]

由于

\[ \Phi_{0-1}(u)= \begin{cases} 1,&u<0,\\ \frac12,&u=0,\\ 0,&u>0, \end{cases} \]

所以

\[ \boxed{ C_\xi(u)= \begin{cases} \xi,&u<0,\\[1mm] \frac12,&u=0,\\[1mm] 1-\xi,&u>0. \end{cases} } \]

## 2. 当 \(\xi=1/2\)

此时

\[ C_{1/2}(u)=\frac12,\qquad\forall u. \]

因此

\[ \inf_{u'}C_{1/2}(u')=\frac12 \]

并且

\[ \boxed{ C_{1/2}(u)-\inf_{u'}C_{1/2}(u')=0. } \]

这是因为正负标签概率相同，任何预测都一样好。

## 3. 当 \(\xi>1/2\)

此时正类更可能出现，所以应当选择 \(u>0\)，预测 \(+1\)。

对于 \(u>0\)：

\[ C_\xi(u)=1-\xi. \]

因此最小条件风险为

\[ \boxed{ \inf_{u'}C_\xi(u')=1-\xi, } \]

并且在整个正半轴 \(\mathbb R_+^*\) 上取得。

分别计算超额风险。

### 当 \(u>0\)

预测方向正确：

\[ \Delta_{01}(\xi,u) = (1-\xi)-(1-\xi)=0. \]

### 当 \(u<0\)

预测方向错误：

\[ \Delta_{01}(\xi,u) = \xi-(1-\xi) = 2\xi-1. \]

### 当 \(u=0\)

随机预测：

\[ \Delta_{01}(\xi,0) = \frac12-(1-\xi) = \xi-\frac12. \]

所以

\[ \boxed{ \Delta_{01}(\xi,u)= \begin{cases} 2\xi-1,&u<0,\\[1mm] \xi-\frac12,&u=0,\\[1mm] 0,&u>0. \end{cases} } \]

这正好可以写成

\[ \boxed{ \Delta_{01}(\xi,u) = (2\xi-1)\Phi_{0-1}(u). } \]

因为 \(\Phi_{0-1}(u)\) 在负、零、正三种情况下分别为 \(1,\frac12,0\)。

进一步，

\[ \Phi_{0-1}(u)\le\mathbf1_{\{u\le0\}}, \]

因此

\[ \boxed{ \Delta_{01}(\xi,u) \le (2\xi-1)\mathbf1_{\{u\le0\}}. } \]

在 \(u=0\) 时，左边只有 \((2\xi-1)/2\)，右边是 \(2\xi-1\)，所以是上界而非等式。

## 4. 当 \(\xi<1/2\)

此时负类更可能出现，正确方向是 \(u<0\)。

最小条件风险为

\[ \inf_{u'}C_\xi(u')=\xi. \]

同理可得

\[ \Delta_{01}(\xi,u) = (1-2\xi)\Phi_{0-1}(-u). \]

即

\[ \Delta_{01}(\xi,u)= \begin{cases} 0,&u<0,\\[1mm] \frac12-\xi,&u=0,\\[1mm] 1-2\xi,&u>0. \end{cases} \]

并且

\[ \Delta_{01}(\xi,u) \le (1-2\xi)\mathbf1_{\{-u\le0\}} = (1-2\xi)\mathbf1_{\{u\ge0\}}. \]

## 5. 把两种情况统一起来

令

\[ \alpha=2\xi-1. \]

那么：

- \(\alpha>0\)：Bayes 方向为正；
- \(\alpha<0\)：Bayes 方向为负；
- \(\alpha=0\)：两类概率相同。

当前分数 \(u\) 与 Bayes 方向不一致，等价于

\[ \alpha u\le0. \]

因此两种情况可以统一写成

\[ \boxed{ \Delta_{01}(\xi,u) = |2\xi-1|\, \Phi_{0-1}\bigl((2\xi-1)u\bigr). } \]

进一步得到

\[ \boxed{ \Delta_{01}(\xi,u) \le |2\xi-1|\, \mathbf1_{\{(2\xi-1)u\le0\}}. } \]

然后我们就去考虑，使用$\Phi$来代替之后的误差变成什么样了呢？

首先我们来看简单的平方损失的情况：

$C^{\Phi}_{\xi}(u)=\xi(1-u)^2+(1-\xi)(1+u)^2=u^2-2(2\xi-1)u+1$
$$
C^{\Phi}_{\xi}(u)-\inf_{u'}C_\xi^\Phi(u')=(u-2\xi+1)^2\ge(|2\xi-1|\,  \mathbf1_{\{(2\xi-1)u\le0\}})^2
$$
因此，有如下的控制
$$
\mathcal R(g)-\mathcal R^*\le(\mathcal R_\Phi(g)-\mathcal R_\Phi^*)^{1/2}
$$
而对于一般的光滑替代函数 Smooth Surrogates，$\Phi(u)=a(u)-u$

其中$a$要是一个偶函数，凸函数，而且满足$a''(u)\le\beta$

令

\[ f_\alpha(u)=a(u)-\alpha u. \]

它仍然是 \(\beta\)-smooth，并且

\[ f_\alpha'(u)=a'(u)-\alpha. \]

对任意凸的 \(\beta\)-smooth 函数，都有

\[ f_\alpha(u)-\inf_{u'}f_\alpha(u') \ge \frac{1}{2\beta}|f_\alpha'(u)|^2. \]

代入 \(f_\alpha\)，得到原文的式 (4.9)：

\[ a(u)-\alpha u -\inf_{u'}\{a(u')-\alpha u'\} \ge \frac{1}{2\beta}|\alpha-a'(u)|^2. \]

直观上，它表示：如果当前位置的梯度还很大，那么该点与最优值的差距不可能很小。

### Ex 4.1

在本节已有假设的基础上，进一步假设 \(a(0)=0\)。证明：如果 \(a^*\) 是 \(a\) 的 Fenchel 共轭函数，那么对于任意函数 \(g:\mathcal X\to\mathbb R\)，都有

\[
a^*\bigl(\mathcal R(g)-\mathcal R^*\bigr)
\le
\mathcal R_\Phi(g)-\mathcal R_\Phi^*.
\]

Fenchel 共轭的定义为

\[
a^*(\alpha)=\sup_{u\in\mathbb R}\{\alpha u-a(u)\}.
\]

由于 \(a\) 是凸偶函数且 \(a(0)=0\)，所以 \(a(u)\ge 0\)。相应地，\(a^*\) 也是凸偶函数，满足 \(a^*(0)=0\)，并在 \([0,+\infty)\) 上单调不减。

固定 \(x\)，令

\[
\alpha=2\xi-1,\qquad \xi=\mathbb P(Y=1\mid X=x).
\]

条件代理风险为

\[
C_\xi^\Phi(u)=a(u)-\alpha u.
\]

由 Fenchel 共轭的定义，

\[
\inf_v\{a(v)-\alpha v\}
=-\sup_v\{\alpha v-a(v)\}
=-a^*(\alpha).
\]

所以条件代理超额风险为

\[
\Delta_\Phi(\xi,u)
=C_\xi^\Phi(u)-\inf_vC_\xi^\Phi(v)
=a(u)-\alpha u+a^*(\alpha).
\]

如果预测方向错误，即 \(\alpha u\le0\)，那么 \(a(u)-\alpha u\ge0\)，于是

\[
\Delta_\Phi(\xi,u)\ge a^*(\alpha)=a^*(|\alpha|).
\]

同时，条件 \(0\!-\!1\) 超额风险满足

\[
0\le\Delta_{01}(\xi,u)
\le |\alpha|\mathbf 1_{\{\alpha u\le0\}}.
\]

利用 \(a^*\) 在非负半轴上的单调性可得

\[
a^*\bigl(\Delta_{01}(\xi,u)\bigr)
\le \Delta_\Phi(\xi,u).
\]

预测方向正确时 \(\Delta_{01}=0\)，该不等式同样成立。最后利用 Jensen 不等式，

\[
\begin{aligned}
a^*\bigl(\mathcal R(g)-\mathcal R^*\bigr)
&=a^*\bigl(\mathbb E[\Delta_{01}]\bigr)\\
&\le\mathbb E\bigl[a^*(\Delta_{01})\bigr]\\
&\le\mathbb E[\Delta_\Phi]\\
&=\mathcal R_\Phi(g)-\mathcal R_\Phi^*.
\end{aligned}
\]



### Ex 4.2

设

\[ \Phi:\mathbb R\to\mathbb R \]

是一个凸函数，并且在 \(0\) 点可微，满足

\[ \Phi'(0)<0. \]

定义函数

\[ G(z) = \Phi(0) - \inf_{u\in\mathbb R} \left\{ \frac{1+z}{2}\Phi(u) + \frac{1-z}{2}\Phi(-u) \right\}. \]

证明：

1. \(G\) 是凸函数；
2. \(G(0)=0\)；
3. 对任意函数 \(g:\mathcal X\to\mathbb R\)，都有\[ \boxed{ G\!\left(\mathcal R(g)-\mathcal R^*\right) \le \mathcal R_\Phi(g)-\mathcal R_\Phi^*. } \]

其中：

- \(\mathcal R(g)\) 是分类器 \(g\) 的 \(0\!-\!1\) 风险；
- \(\mathcal R^*\) 是最优的 \(0\!-\!1\) 风险，即 Bayes 风险；
- \(\mathcal R_\Phi(g)\) 是由替代损失 \(\Phi\) 定义的风险；
- \(\mathcal R_\Phi^*\) 是最优替代风险。

最后，求指数损失

\[ \Phi(u)=e^{-u} \]

所对应的函数 \(G\)。



一、为什么这样定义 \(G\)？

令

\[ \xi=P(Y=1\mid X=x), \qquad z=2\xi-1. \]

那么

\[ \xi=\frac{1+z}{2}, \qquad 1-\xi=\frac{1-z}{2}. \]

所以条件代理风险可以写成

\[ C_\xi^\Phi(u) = \frac{1+z}{2}\Phi(u) + \frac{1-z}{2}\Phi(-u). \]

因此

\[ \inf_u C_\xi^\Phi(u) = \inf_u \left\{ \frac{1+z}{2}\Phi(u) + \frac{1-z}{2}\Phi(-u) \right\}. \]

于是

\[ \boxed{ G(z)=\Phi(0)-\inf_u C_\xi^\Phi(u). } \]

它衡量的是：

> 使用没有分类方向的分数 \(u=0\)，相比最优条件分数，多付出了多少代理风险。

而 \(z=|2\xi-1|\) 越大，分类越确定，使用错误方向的代价应该越大。

------

## 二、证明 \(G\) 是凸函数

记

\[ F_u(z) = \frac{1+z}{2}\Phi(u) + \frac{1-z}{2}\Phi(-u). \]

展开：

\[ F_u(z) = \frac{\Phi(u)+\Phi(-u)}2 + \frac z2\bigl[\Phi(u)-\Phi(-u)\bigr]. \]

对于固定的 \(u\)，这是关于 \(z\) 的仿射函数。

令

\[ M(z)=\inf_uF_u(z). \]

仿射函数族的下确界是凹函数。具体地，对 \(0\le\lambda\le1\)，

\[ \begin{aligned} M(\lambda z_1+(1-\lambda)z_2) &=\inf_u \left[ \lambda F_u(z_1)+(1-\lambda)F_u(z_2) \right]\\ &\ge \lambda\inf_uF_u(z_1) +(1-\lambda)\inf_uF_u(z_2)\\ &=\lambda M(z_1)+(1-\lambda)M(z_2). \end{aligned} \]

所以 \(M\) 是凹函数，进而

\[ \boxed{G(z)=\Phi(0)-M(z)} \]

是凸函数。

此外，换元 \(u\mapsto -u\) 可得

\[ M(-z)=M(z), \]

所以 \(G\) 还是偶函数。

------

## 三、证明 \(G(0)=0\)

当 \(z=0\) 时，

\[ M(0) = \inf_u\frac{\Phi(u)+\Phi(-u)}2. \]

由 \(\Phi\) 的凸性，

\[ \frac{\Phi(u)+\Phi(-u)}2 \ge \Phi\left(\frac{u+(-u)}2\right) =\Phi(0). \]

而在 \(u=0\) 时取等号，所以

\[ M(0)=\Phi(0). \]

因此

\[ \boxed{G(0)=0}. \]

又因为 \(G\) 凸且为偶函数，所以 \(0\) 是其最小点，且 \(G\) 在 \([0,1]\) 上单调不减。

------

## 四、证明逐点的校准不等式

要证明

\[ G\bigl(\Delta_{01}(\xi,u)\bigr) \le \Delta_\Phi(\xi,u), \]

其中

\[ \Delta_\Phi(\xi,u) = C_\xi^\Phi(u)-\inf_vC_\xi^\Phi(v). \]

仍令

\[ z=2\xi-1. \]

### 情况一：分类方向正确

如果

\[ zu>0, \]

则预测符号与 Bayes 分类方向一致，因此

\[ \Delta_{01}(\xi,u)=0. \]

于是

\[ G(\Delta_{01})=G(0)=0 \le \Delta_\Phi. \]

### 情况二：分类方向错误

如果

\[ zu\le0, \]

由 \(\Phi\) 的凸性，

\[ \begin{aligned} C_\xi^\Phi(u) &= \frac{1+z}{2}\Phi(u) + \frac{1-z}{2}\Phi(-u)\\ &\ge \Phi\left( \frac{1+z}{2}u + \frac{1-z}{2}(-u) \right)\\ &=\Phi(zu). \end{aligned} \]

由于题设

\[ \Phi'(0)<0, \]

凸函数在 \(0\) 点的支撑线给出

\[ \Phi(zu) \ge \Phi(0)+\Phi'(0)zu. \]

而 \(zu\le0\)、\(\Phi'(0)<0\)，所以

\[ \Phi'(0)zu\ge0. \]

因此

\[ C_\xi^\Phi(u)\ge\Phi(zu)\ge\Phi(0). \]

所以

\[ \begin{aligned} \Delta_\Phi(\xi,u) &=C_\xi^\Phi(u)-M(z)\\ &\ge\Phi(0)-M(z)\\ &=G(z)=G(|z|). \end{aligned} \]

同时条件 \(0\!-\!1\) 超额风险满足

\[ 0\le\Delta_{01}(\xi,u)\le|z|. \]

由于 \(G\) 在非负半轴单调不减，

\[ G(\Delta_{01}(\xi,u)) \le G(|z|) \le\Delta_\Phi(\xi,u). \]

所以两种情况合起来，

\[ \boxed{ G(\Delta_{01}(\xi,u)) \le \Delta_\Phi(\xi,u). } \]

------

## 五、提升到总体风险

我们有

\[ \mathcal R(g)-\mathcal R^* = \mathbb E[\Delta_{01}] \]

以及

\[ \mathcal R_\Phi(g)-\mathcal R_\Phi^* = \mathbb E[\Delta_\Phi]. \]

利用 \(G\) 的凸性和 Jensen 不等式，

\[ \begin{aligned} G[\mathcal R(g)-\mathcal R^*] &=G(\mathbb E[\Delta_{01}])\\ &\le\mathbb E[G(\Delta_{01})]\\ &\le\mathbb E[\Delta_\Phi]\\ &=\mathcal R_\Phi(g)-\mathcal R_\Phi^*. \end{aligned} \]

最终得到

\[ \boxed{ G[\mathcal R(g)-\mathcal R^*] \le \mathcal R_\Phi(g)-\mathcal R_\Phi^*. } \]

这道题的证明链条就是

\[ \boxed{ \Phi\text{ 凸} \Rightarrow G\text{ 凸} \Rightarrow G(\text{条件 }0\!-\!1\text{ 超额风险}) \le \text{条件代理超额风险} \Rightarrow \text{总体风险界}. } \]

题目的最后一步是对 exponential loss \(\Phi(u)=e^{-u}\) 显式计算 \(G\)，结果是

\[ \boxed{G(z)=1-\sqrt{1-z^2}}. \]

### Ex 4.3

假设存在 \(\varepsilon\in(0,1)\)，使得几乎处处都有

\[
|2\eta(x)-1|\ge\varepsilon.
\]

设 \(\Phi:\mathbb R\to\mathbb R\) 是本节所考虑的光滑、凸且具有分类校准性的替代损失，并且

\[
\Phi(v)=a(v)-v.
\]

证明：对于任意函数 \(g:\mathcal X\to\mathbb R\)，都有

\[
\boxed{
\mathcal R(g)-\mathcal R(g_*)
\le
\frac{\varepsilon}{a^*(\varepsilon)}
\left[\mathcal R_\Phi(g)-\mathcal R_\Phi^*\right].
}
\]

这里仍将 \(a\) 归一化为 \(a(0)=0\)，这不改变超额风险。固定 \(x\)，记

\[
z=2\eta(x)-1,\qquad u=g(x).
\]

由 Ex 4.1 的计算，条件代理超额风险为

\[
\Delta_\Phi(x)=a(u)-zu+a^*(z).
\]

若预测方向错误，即 \(zu\le0\)，则 \(a(u)\ge0\)、\(-zu\ge0\)，并且 \(a^*\) 是偶函数，所以

\[
\Delta_\Phi(x)\ge a^*(|z|).
\]

因为 \(a^*\) 凸且 \(a^*(0)=0\)，对任意 \(t\ge\varepsilon\)，令 \(\lambda=\varepsilon/t\)，有

\[
\begin{aligned}
a^*(\varepsilon)
&=a^*\bigl(\lambda t+(1-\lambda)0\bigr)\\
&\le\lambda a^*(t)+(1-\lambda)a^*(0)
=\frac{\varepsilon}{t}a^*(t).
\end{aligned}
\]

因此

\[
a^*(t)\ge\frac{a^*(\varepsilon)}{\varepsilon}t,
\qquad t\ge\varepsilon.
\]

题设保证 \(|z|\ge\varepsilon\)，而条件 \(0\!-\!1\) 超额风险满足

\[
\Delta_{01}(x)
\le |z|\mathbf 1_{\{zu\le0\}}.
\]

所以在预测错误时，

\[
\Delta_\Phi(x)
\ge a^*(|z|)
\ge\frac{a^*(\varepsilon)}{\varepsilon}|z|
\ge\frac{a^*(\varepsilon)}{\varepsilon}\Delta_{01}(x).
\]

预测正确时 \(\Delta_{01}(x)=0\)，同一不等式仍成立。对 \(X\) 取期望，得到

\[
\mathcal R_\Phi(g)-\mathcal R_\Phi^*
\ge
\frac{a^*(\varepsilon)}{\varepsilon}
\bigl[\mathcal R(g)-\mathcal R(g_*)\bigr].
\]

整理即得题目结论。这里的间隔条件排除了 \(\eta(x)\) 接近 \(1/2\) 的困难样本，因此将一般的非线性校准界加强成了线性风险界。

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
