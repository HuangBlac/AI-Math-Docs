# 经验风险最小化（Empirical Risk Minimization）

!!! info "出处与说明"
    Francis Bach, *Learning Theory from First Principles*（简称 **LFTP**），第 4 章。
    本页整理自我自己的学习笔记（`学习笔记/数据科学/LTFP Ch4.md`），迁移到站点时只修正了公式渲染、页面结构与个别拼写，推导与讲法保持原样。
    整理日期：2026-06-25。

## 总起：算法的意义

算法的意义在于三点：

1. 我们不知道真正的函数，只是管中窥豹；
2. 实数集真的很大，我们不可能搜索每一个可测函数；
3. 我们没有无限的时间去逐点搜索。

本章三条主线（章节提要）：

- **Convexification of the risk**：对于二分类问题，优化预测可以转化为凸优化问题（convexification，凸化）。
- **Risk decomposition（风险分解）**：风险可以被分解为
    - **逼近误差**（approximation error）：建模假设、所选函数类的逼近效率，主要由逼近理论刻画；
    - **估计误差**（estimation error）：由于样本观测有限，主要由高维概率工具刻画。
- **Rademacher complexity（Rademacher 复杂度）**：为研究估计误差、计算实值输出的期望一致偏差，Rademacher 复杂度（也叫 Rademacher averages）是一个非常灵活有力的工具，能给出一致偏差界，并导出对（约束或惩罚的）线性预测器**与维度无关**的估计误差上界。

## 从理论最优到经验风险

对于分类问题以及一系列机器学习问题，本质上就是要找一个满足泛函极小化的解：

$$
f^* = \arg\min_{f}\ \mathcal{L}\,(f) = \mathbb{E}_{(X,Y)\sim\mathbb{P}}\, \ell(f(X),Y).
$$

但我们并不知道真实的数据分布，所以实际采用平均值来代替期望。

> In this chapter, we will consider methods based on empirical risk minimization, with a focus on statistical analysis (i.e., generalization to unseen data); optimization algorithms to efficiently find approximate minimizers will be studied in chapter 5. Before looking at the necessary probabilistic tools, we will show how problems where the output space is not a vector space, such as binary classification with $Y=\{-1,1\}$, can be reformulated as real-valued outputs, with so-called convex surrogates of loss functions.

## 4.1 风险的凸化（Convex Surrogates）

对二分类问题，对应的损失函数本应是 0-1 损失：

$$
\ell(f(X),Y) = \mathbf{1}_{f(X)\neq Y},
$$

只要两者不相等就记为 1。但 $Y$ 只有 $\{+1,-1\}$ 两种取值，这种离散值域不好优化，所以需要做一个操作：**凸化**。

首先 $f$ 可以表示为 $f(x)=\operatorname{sign}(g(x))$，其中 $g$ 为可微函数，

$$
\operatorname{sign}(a)=1\ \text{if}\ a>0,\qquad \operatorname{sign}(a)=-1\ \text{if}\ a<0.
$$

但 $\operatorname{sign}$ 不连续，而且在零点没有定义，不能直接套进去。于是把原问题转化为选取 $g$：

$$
\mathcal{L}\,(g) = \arg\min\ \mathbb{P}\big(f(X)\neq Y\big) = \arg\min\ \mathbb{P}\big(\operatorname{sign}(g(X))\neq Y\big) = \arg\min\ \mathbb{P}\big(Yg(X)<0\big).
$$

实际上就是要让 $Yg(X)$ 异号的概率尽可能小（同号的概率尽可能大）。重新写成期望形式：

$$
\mathbb{E}\big[\Phi_{0\text{-}1}(yg(x))\big],\qquad
\Phi_{0\text{-}1}(u)=\begin{cases}1, & u<0,\\[2pt] \tfrac12, & u=0,\\[2pt] 0, & u>0.\end{cases}
$$

因此原问题依然转化为选取 $g$ 使期望极小化。但 $\Phi_{0\text{-}1}$ 不连续，所以我们可以采用不同的近似方式，对应不同的模型：

**平方损失** $\Phi(u)=(u-1)^2$。因为 $y^2=1$，所以 $\Phi(yg(x))=(y-g(x))^2$，这就退回到了最小二乘回归，预测时取 $g(x)$ 的符号。注意它是图里唯一在 $u>1$ 后又往上翘的——对"分得太对"也会惩罚，这是它和其它（单调不增的）损失的区别。

**Logistic 损失** $\Phi(u)=\log(1+e^{-u})=-\log\sigma(u)$，其中 $\sigma$ 是 sigmoid，对应逻辑回归，也就是常说的交叉熵；从概率角度看，令 $\mathbb{P}\,(y=1\mid x)=\sigma(g(x))$，这个风险就是负的条件对数似然（第 14 章细讲）。

**Hinge 损失** $\Phi(u)=\max(1-u,0)$。配上线性预测器就是 SVM，这里的 $yg(x)$ 就是"间隔"一词的出处（几何解释在带菱形的 4.1.2）。

**平方 hinge** $\max(1-u,0)^2$，hinge 的光滑版。

**指数损失** $\Phi(u)=e^{-u}$，boosting / AdaBoost 里用的。

事实上，Hinge 损失对应的就是 SVM 支持向量机。

## 4.2–4.3 风险分解与逼近误差

我们并不是从真实分布求理论最佳函数 $f^*$，也不是在所有可能的函数空间内搜索。我们有 $n$ 个样本 $\{(X_i,Y_i)\}$，每个样本独立同分布，实际求的是

$$
\hat f = \arg\min_{f\in\mathcal{F}}\ \frac1n\sum_{i=1}^n \ell(f(X_i),Y_i).
$$

大数定理告诉我们频率趋近于概率，但毕竟有差别。更具体地，可以把超额风险拆成两部分：

$$
\mathcal{L}\,(\hat f) - \mathcal{L}\,(f^*) = \underbrace{\mathcal{L}\,(\hat f) - \inf_{f\in\mathcal{F}}\mathcal{L}\,(f)}_{\text{估计误差 estimation error}} + \underbrace{\inf_{f\in\mathcal{F}}\mathcal{L}\,(f) - \mathcal{L}\,(f^*)}_{\text{逼近误差 approximation error}}.
$$

前者由样本有限导致（估计误差），后者由函数类 $\mathcal{F}$ 不够大导致（逼近误差）。

### 先分析逼近误差

对函数类往往考虑这样的情形（也符合实际算法的构建）：$\mathcal{F}=\{f_\theta\mid \theta\in\Theta\}$。

举个例子，神经网络函数空间 $\mathcal{NN}\,(2,100,\theta)$：$L\le 2,\ W\le 100,\ |B|\le 10$，表示一个两层、宽度 100、参数绝对值 $\le 10$ 的网络对应的函数空间。严格来说，$\Theta$ 在计算机里只能取离散值（如 double、float）。考虑这一点，逼近误差可以进一步分解：

$$
\inf_{\theta\in\Theta}\mathcal{L}\,(f_\theta) - \mathcal{L}\,(f^*)
= \underbrace{\inf_{\theta\in\Theta}\mathcal{L}\,(f_\theta) - \inf_{\theta\in\mathbb{R}^n}\mathcal{L}\,(f_\theta)}_{\text{可优化部分}}
+ \underbrace{\inf_{\theta\in\mathbb{R}^n}\mathcal{L}\,(f_\theta) - \mathcal{L}\,(f^*)}_{\text{不可压缩项}}.
$$

第二部分单纯靠提高精度无法解决，除非改变算法结构本身，被称为**不可压缩项**。而对固定模型（如神经网络、SVM），第二项往往可以压得很小（万能逼近定理等），所以重点先分析第一块。

考虑一个具体的回归情景 $f_\theta(x)=\theta^\top\varphi(x)$。第一部分误差可以借助损失函数关于第二个变量 $G$-Lipschitz 写成：

$$
\mathcal{L}\,(f_\theta)-\mathcal{L}\,(f_{\theta'}) = \mathbb{E}\big[\ell(y,f_\theta(x))-\ell(y,f_{\theta'}(x))\big]\le G\,\mathbb{E}\big[|f_\theta(x)-f_{\theta'}(x)|\big].
$$

再假设 $\|\theta\|_2\le D$。在经典范例 $f_\theta(x)=\theta^\top\varphi(x)$ 下，预测差为 $|f_\theta(x)-f_{\theta'}(x)| = |(\theta-\theta')^\top\varphi(x)|\le \|\theta-\theta'\|_2\,\|\varphi(x)\|_2$。代回去，约束代价被压成

$$
\inf_{\theta\in\Theta} R(f_\theta) - \inf_{\theta'\in\mathbb{R}^d} R(f_{\theta'}) \;\leq\; G\,\mathbb{E}\big[\|\varphi(x)\|_2\big]\cdot \inf_{\|\theta\|_2\leq D}\|\theta - \theta_\ast\|_2.
$$

练习中若假设 $\|\theta\|_1\le D$，依然可以用 Hölder 不等式：

$$
\inf_{\theta\in\Theta} R(f_\theta) - \inf_{\theta'\in\mathbb{R}^d} R(f_{\theta'}) \;\leq\; G\,\mathbb{E}\big[\|\varphi(x)\|_{\infty}\big]\cdot \inf_{\|\theta\|_1\leq D}\|\theta - \theta_\ast\|_1.
$$

## 4.4 估计误差：一致偏差

估计误差 $R(\hat f)-\inf_{f\in\mathcal{F}}R(f)$ 没法逐点控制，根子在于 $\hat f$ 是从数据里选出来的。书上的做法是把它转化为一个**一致偏差**：

$$
R(\hat f) - \inf_{f\in\mathcal{F}} R(f) \;\leq\; 2\sup_{f\in\mathcal{F}} \big|\hat R(f) - R(f)\big|.
$$

推导过程（记 $g_{\mathcal{F}}$ 为 $\mathcal{F}$ 内的最优）：

$$
R(\hat f) - R(g_{\mathcal{F}}) = \underbrace{\{R(\hat f) - \hat R(\hat f)\}}_{①} + \underbrace{\{\hat R(\hat f) - \hat R(g_{\mathcal{F}})\}}_{②} + \underbrace{\{\hat R(g_{\mathcal{F}}) - R(g_{\mathcal{F}})\}}_{③}.
$$

①、③ 都可以被 $\sup_{f\in\mathcal{F}}\big(R(f)-\hat R(f)\big)$ 控制；② 中由于 $\hat f$ 是 $\hat R$ 的极小化结果，$\hat R(\hat f)\le \hat R(g_{\mathcal{F}})$，所以 $②\le 0$。

### McDiarmid 不等式（完整证明）

记 $H(z_1,\dots,z_n)=\sup_{f\in\mathcal{F}}\big(R(f)-\hat R(f)\big)$。损失有界在 $[0,\ell_\infty]$ 时，**改动单个样本 $z_i$，$H$ 至多变化 $\ell_\infty/n$**（有界差分性质）。于是 McDiarmid 不等式给出集中：以概率 $\geq 1-\delta$，

$$
H - \mathbb{E}[H] \;\leq\; \frac{\ell_\infty}{\sqrt{2n}}\sqrt{\log\tfrac{1}{\delta}}.
$$

下面用 **Doob martingale + Hoeffding 引理 + Chernoff bound** 证明它。

**第 1 步 · 设置鞅。** 定义 filtration $\mathcal{F}_i=\sigma(Z_1,\dots,Z_i)$（表示"已经看到前 $i$ 个样本"），并令 $M_i=\mathbb{E}[H\mid Z_1,\dots,Z_i]$。则

$$
H-\mathbb{E}\,H = M_n-M_0 = \sum_{i=1}^n (M_i-M_{i-1}),\qquad D_i := M_i-M_{i-1}.
$$

问题变成控制 $\sum_{i=1}^n D_i$。

**第 2 步 · 每步波动被 $c_i$ 控制。** 固定 $Z_1=z_1,\dots,Z_{i-1}=z_{i-1}$，考虑

$$
\phi_i(z_i) = \mathbb{E}_{Z_{i+1},\dots,Z_n}\big[H(z_1,\dots,z_{i-1},z_i,Z_{i+1},\dots,Z_n)\big],
$$

即在前 $i-1$ 个变量固定、第 $i$ 个取 $z_i$ 时对后面的变量取期望。因为 $H$ 满足 bounded difference 条件，只改第 $i$ 个变量时 $|H(\dots,z_i,\dots)-H(\dots,z_i',\dots)|\le c_i$，对后面取期望后差距仍不超过 $c_i$，故 $|\phi_i(z_i)-\phi_i(z_i')|\le c_i$。而 $M_i=\phi_i(Z_i)$，因此

$$
D_i = \phi_i(Z_i)-\mathbb{E}[\phi_i(Z_i)\mid\mathcal{F}_{i-1}],\qquad \mathbb{E}[D_i\mid\mathcal{F}_{i-1}]=0,\quad D_i\in[a_i,b_i],\ b_i-a_i\le c_i.
$$

**第 3 步 · 使用 Hoeffding 引理。** 若 $\mathbb{E}\,X=0,\ X\in[a,b]$，则对任意 $\lambda>0$，$\mathbb{E}\,e^{\lambda X}\le\exp\!\big(\tfrac{\lambda^2(b-a)^2}{8}\big)$。对 $D_i$ 用条件版：

$$
\mathbb{E}\big[e^{\lambda D_i}\mid\mathcal{F}_{i-1}\big]\le \exp\!\left(\frac{\lambda^2 c_i^2}{8}\right).
$$

**第 4 步 · 控制整体矩母函数。** 用条件期望一层层剥：

$$
\mathbb{E}\,e^{\lambda\sum_{i=1}^n D_i} = \mathbb{E}\Big[e^{\lambda\sum_{i=1}^{n-1}D_i}\,\mathbb{E}\,(e^{\lambda D_n}\mid\mathcal{F}_{n-1})\Big]\le \exp\!\left(\frac{\lambda^2 c_n^2}{8}\right)\mathbb{E}\,e^{\lambda\sum_{i=1}^{n-1}D_i}.
$$

不断递推：

$$
\mathbb{E}\,e^{\lambda(H-\mathbb{E}\,H)}\le \exp\!\left(\frac{\lambda^2}{8}\sum_{i=1}^n c_i^2\right).
$$

**第 5 步 · Chernoff bound 取尾界。** 由 Markov，$\mathbb{P}\,(H-\mathbb{E}\,H>t)\le e^{-\lambda t}\,\mathbb{E}\,e^{\lambda(H-\mathbb{E}\,H)}\le \exp\!\big(-\lambda t+\tfrac{\lambda^2}{8}C\big)$，其中 $C=\sum_i c_i^2$。对 $\lambda$ 优化，$-t+\tfrac{\lambda C}{4}=0\Rightarrow\lambda=\tfrac{4t}{C}$，代回得 $-\tfrac{2t^2}{C}$。因此

$$
\boxed{\ \mathbb{P}\,(H-\mathbb{E}\,H>t)\le \exp\!\left(-\frac{2t^2}{\sum_{i=1}^n c_i^2}\right)\ }
$$

这就是 McDiarmid 不等式。

它把"高概率界定 $H$"**化简成"只需界定它的期望 $\mathbb{E}[H]=\mathbb{E}[\sup_f(R-\hat R)]$"**，再加一个 $\frac{\ell_\infty}{\sqrt{2n}}\sqrt{\log(2/\delta)}$ 的尾项就够了。整章剩下的内容，本质都是在用越来越精的工具界定这一个期望。

### 4.4.2 二次损失（暖身一）

取平方损失 $\ell=(y-\theta^\top\varphi(x))^2$ 加 $\|\theta\|_2\leq D$ 的约束：

$$
\hat R(f)-R(f) = \theta^\top\Big(\underbrace{\tfrac1n\textstyle\sum_i \varphi(x_i)\varphi(x_i)^\top - \mathbb{E}[\varphi(x)\varphi(x)^\top]}_{\text{矩阵偏差 } \Delta_2}\Big)\theta - 2\theta^\top\underbrace{\Big(\tfrac1n\textstyle\sum_i y_i\varphi(x_i)-\mathbb{E}[y\varphi(x)]\Big)}_{\text{向量偏差 }\Delta_1} + \underbrace{\Big(\tfrac1n\textstyle\sum_i y_i^2-\mathbb{E}[y^2]\Big)}_{\text{标量偏差 }\Delta_0}.
$$

要点：**它关于 $\theta$ 是个二次型**（二次项 + 线性项 + 常数）。偏差展开成三项：

- 二次项：$|\theta^\top\Delta_2\theta|\leq \|\Delta_2\|_{\text{op}}\|\theta\|_2^2 \leq D^2\|\Delta_2\|_{\text{op}}$（$\|\Delta_2\|_{\text{op}}=\sup_{\|u\|_2=1}\|\Delta_2 u\|_2$）；
- 线性项：$|2\theta^\top\Delta_1|\leq 2\|\theta\|_2\|\Delta_1\|_2 \leq 2D\|\Delta_1\|_2$（Cauchy–Schwarz）；
- 常数项：就是 $|\Delta_0|$。

合起来：

$$
\sup_{\|\theta\|_2\leq D}\big|R(f)-\hat R(f)\big| \;\leq\; D^2\,\|\Delta_2\|_{\text{op}} + 2D\,\|\Delta_1\|_2 + |\Delta_0|.
$$

**$\theta$ 和 sup 在这一步就被彻底消掉了。** 由于关于 $\theta$ 是二次的，在球上的 sup 能**闭式**算出来，于是只剩三个**非一致**的偏差，每个都是 $O(1/\sqrt n)$，直接拼出 $O(1/\sqrt n)$ 的一致界。

教训：平方损失靠闭式很轻松，但别的损失没有闭式，所以**必须引入新工具**。（书还提醒：从这节起不再要求损失是凸的。）

### 4.4.3 有限模型类（暖身二）

$\mathcal{F}$ 有限时，用并集界把 sup 拆开，对每个 $f$ 套 Hoeffding。

**第一步，并集界把 sup 拆成逐个。** "存在某个 $f$ 偏差 $\geq t$"，无非是各个 $f$ 偏差 $\geq t$ 这些事件的并，于是概率可加：

$$
\mathbb{P}\Big(\sup_{f\in\mathcal{F}}\big(\hat R(f)-R(f)\big)\geq t\Big) \;\leq\; \sum_{f\in\mathcal{F}}\mathbb{P}\big(\hat R(f)-R(f)\geq t\big).
$$

**第二步，对每个固定 $f$ 套 Hoeffding。** $\hat R(f)$ 是 $n$ 个有界独立量的平均，期望为 $R(f)$，所以 $\mathbb{P}\big(\hat R(f)-R(f)\geq t\big)\leq \exp(-2nt^2/\ell_\infty^2)$。代回去（连同两侧因子 2）：

$$
\mathbb{P}\Big(\sup_{f\in\mathcal{F}}\big(\hat R(f)-R(f)\big)\geq t\Big) \;\leq\; 2|\mathcal{F}|\exp\!\Big(\frac{-2nt^2}{\ell_\infty^2}\Big).
$$

**第三步，令右边 $=\delta$ 反解 $t$。** 以概率 $\geq 1-\delta$，

$$
\sup_{f\in\mathcal{F}}\big(\hat R(f)-R(f)\big) \;\leq\; \frac{\ell_\infty}{\sqrt{2n}}\sqrt{\log\frac{2|\mathcal{F}|}{\delta}} \;\leq\; \ell_\infty\sqrt{\frac{\log(2|\mathcal{F}|)}{2n}} + \frac{\ell_\infty}{\sqrt{2n}}\sqrt{\log\frac{1}{\delta}}.
$$

取期望即

$$
\mathbb{E}\Big[\sup_{f\in\mathcal{F}}\big(\hat R(f) - R(f)\big)\Big] \;\leq\; \ell_\infty\sqrt{\frac{\log(2|\mathcal{F}|)}{2n}}.
$$

结论很干净：**当 $\log|\mathcal{F}|\ll n$ 时学习就可行**。函数类的"大小"只通过 $\log|\mathcal{F}|$ 进来。这是对一致偏差的第一个通用控制。

### 4.4.4 无限类 → 覆盖数（♦）

无限的 $\mathcal{F}$ 用有限的 **ε-网**近似——在伪距离 $\Delta(f,f')=\mathbb{E}|f-f'|$ 下，用 $m(\varepsilon)$ 个 ε-球盖住 $\mathcal{F}$，$m(\varepsilon)$ 就是覆盖数。

有了覆盖，就能把任意 $f$ 的偏差转嫁给离它最近的代表 $f_i$。用 $\hat R$ 和 $R$ 都对 $\Delta$ 是 $G$-Lipschitz，做一个"三段跳"：

$$
\hat R(f) - R(f) = \underbrace{\hat R(f)-\hat R(f_i)}_{\leq\, G\Delta(f,f_i)} + \big(\hat R(f_i)-R(f_i)\big) + \underbrace{R(f_i)-R(f)}_{\leq\, G\Delta(f,f_i)} \;\leq\; 2G\,\Delta(f,f_i) + \big(\hat R(f_i)-R(f_i)\big).
$$

取离 $f$ 最近的代表（$\Delta(f,f_i)\leq\varepsilon$），再对所有 $f$ 取 sup：

$$
\sup_{f\in\mathcal{F}}\big(\hat R(f)-R(f)\big) \;\leq\; 2G\varepsilon + \underbrace{\sup_{j\in\{1,\dots,m(\varepsilon)\}}\big(\hat R(f_j)-R(f_j)\big)}_{\text{有限类，套 4.4.3}}.
$$

右边第二项只剩 $m(\varepsilon)$ 个代表——**有限了**，直接套 4.4.3 的并集界，把 $|\mathcal{F}|$ 换成 $m(\varepsilon)$。于是以概率 $\geq 1-\delta$：

$$
\sup_{f\in\mathcal{F}}\big(\hat R(f)-R(f)\big) \;\leq\; 2G\varepsilon + \ell_\infty\sqrt{\frac{\log(2m(\varepsilon))}{2n}} + \frac{\ell_\infty}{\sqrt{2n}}\sqrt{\log\frac1\delta}.
$$

这里出现了一个**张力**，全在那两项的反向变化上：$\varepsilon$ 调小 → 第一项 $2G\varepsilon$ 变小，但覆盖数 $m(\varepsilon)\sim\varepsilon^{-d}$ 变大，第二项的 $\log m(\varepsilon)\sim d\log(1/\varepsilon)$ 变大。要权衡的量大致是

$$
\varepsilon + \sqrt{\frac{d\log(1/\varepsilon)}{n}}.
$$

取 $\varepsilon\propto 1/\sqrt n$，得到速率约 $\sqrt{\tfrac{d}{n}\log n}$（$d$ 维时通常 $m(\varepsilon)\sim\varepsilon^{-d}$，故 $\log m(\varepsilon)\sim d\log(1/\varepsilon)$）。

这正是它属于菱形可跳过内容的原因：不用链式法（chaining）等更精的工具就会损失这个 $\log$ 因子，而 **4.5 的 Rademacher 复杂度**能做得更干净。

---

!!! note "进度"
    本页到 4.4.4（覆盖数）为止，对应我目前的学习进度。4.5 Rademacher 复杂度及之后待续。
