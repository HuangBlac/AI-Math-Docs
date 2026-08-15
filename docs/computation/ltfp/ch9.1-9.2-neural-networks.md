# Ch9.1-9.2 神经网络：优化、统计误差与宽度极限

这篇由扫描手写稿《Ch9.1-9.2》8 页整理而来。笔记的主线不是神经网络工程结构，而是用学习理论的三种误差解释两层网络，并讨论有限宽网络、无限宽测度模型和 Rademacher 复杂度。

> 状态：手写转录与结构化补充。公式符号已统一；个别常数依赖教材采用的 Rademacher 复杂度定义，理解时应关注关于样本量、维度和范数的依赖关系。

## 1. 神经网络的三类误差

监督学习通常求解正则化经验风险最小化：

```math
\widehat f\in\arg\min_{f\in\mathcal F}
\frac1n\sum_{i=1}^{n}\ell(y_i,f(x_i))+\Omega(f).
```

总体风险为 $R(f)=\mathbb E[\ell(Y,f(X))]$，经验风险为 $\widehat R_n(f)$。相对某个理想预测器 $f^\star$，超额风险可按“插入中间项”的方式理解为

```math
R(\widetilde f)-R(f^\star)
=
\underbrace{R(\widetilde f)-R(\widehat f)}_{\text{优化误差}}
+
\underbrace{R(\widehat f)-\inf_{f\in\mathcal F}R(f)}_{\text{统计误差}}
+
\underbrace{\inf_{f\in\mathcal F}R(f)-R(f^\star)}_{\text{逼近误差}}.
```

- **优化误差**：算法没有把经验目标优化到足够小；
- **统计误差**：有限样本的经验风险与总体风险之间存在偏差；
- **逼近误差**：函数类 $\mathcal F$ 本身不能完全表示目标。

这三个误差之间存在权衡。扩大网络通常会降低逼近误差，却可能增大函数类复杂度和优化难度。

## 2. 线性模型、核方法与神经网络

### 2.1 线性预测

给定特征映射 $\varphi:\mathcal X\to\mathbb R^d$，线性模型为

```math
f_\theta(x)=\theta^\top\varphi(x).
```

当损失与正则项为凸函数时，优化通常较容易，统计复杂度也能由 $\theta$ 和 $\varphi(x)$ 的范数控制。缺点是特征映射预先固定，模型只能在给定特征空间中学习线性组合。

### 2.2 核方法

若 $\varphi(x)$ 落在 Hilbert 空间 $\mathcal H$ 中，只通过

```math
k(x,x')=\langle\varphi(x),\varphi(x')\rangle_{\mathcal H}
```

访问特征内积，就得到核方法。它能隐式使用高维甚至无限维特征，并保持凸优化结构。但朴素核算法需要存储和处理 $n\times n$ Gram 矩阵，训练成本可能达到 $O(n^3)$，存储成本为 $O(n^2)$。

### 2.3 两层网络

两层标量输出网络可写为

```math
f_m(x)=\sum_{j=1}^{m}\eta_j\sigma(w_j^\top x+b_j).
```

它与核方法的区别在于隐藏特征 $\sigma(w_j^\top x+b_j)$ 也参与学习。代价是参数之间相互耦合，目标一般非凸，还存在神经元置换、缩放等多种参数化对称性。

## 3. ReLU 的正齐次性与归一化

ReLU 激活 $\sigma(t)=\max(t,0)$ 满足

```math
\sigma(\lambda t)=\lambda\sigma(t),
\qquad \lambda\ge0.
```

因此

```math
\eta_j\sigma(w_j^\top x+b_j)
=
(\eta_jq_j)\,
\sigma\!\left(
\frac{w_j^\top x+b_j}{q_j}
\right)
```

对任意 $q_j>0$ 都表示同一个神经元。若输入满足 $\|x\|\le R$，可以取

```math
q_j=\sqrt{\|w_j\|_2^2+b_j^2/R^2},
```

把隐藏参数归一化，再用输出权重吸收尺度。这样，网络容量可以用归一化后输出系数的 $\ell_1$ 总量控制：

```math
\sum_{j=1}^{m}|\widetilde\eta_j|\le D.
```

这种表示揭示了一个重要不变量：只限制网络宽度或某一层参数并不足以刻画函数复杂度，必须处理缩放对称性。

## 4. 从有限宽网络到测度表示

令单个神经元参数为 $w$，其特征记为 $\phi(w)(x)$。有限宽网络可以写成经验测度的积分：

```math
\mu_m=\frac1m\sum_{j=1}^{m}\delta_{w_j},
\qquad
f_{\mu_m}(x)=\int\phi(w)(x)\,d\mu_m(w).
```

当 $m\to\infty$ 时，把离散参数集合放宽为概率测度 $\mu$：

```math
f_\mu(x)=\int\phi(w)(x)\,d\mu(w),
\qquad
F(\mu)=R(f_\mu).
```

这样，原本随宽度增长的有限维参数优化，被改写为概率测度空间上的优化。有限宽网络对应粒子近似，神经元参数就是粒子位置。

## 5. 梯度流与 Wasserstein 视角

普通梯度流在参数向量上写成

```math
\dot w_j=-\nabla_{w_j}G(w_1,\ldots,w_m).
```

测度极限中，粒子分布满足连续性方程

```math
\partial_t\mu_t
+\nabla\cdot(\mu_tv_t)=0,
```

速度场由目标泛函的一阶变分决定。形式上可写为

```math
v_t(w)=-\nabla_w\frac{\delta F}{\delta\mu}(\mu_t)(w).
```

Wasserstein 距离度量的是把一份概率质量搬运成另一份所需的最小代价，因此适合描述神经元分布如何随训练移动。

这个视角的价值是把宽度 $m$ 从核心表达中移除，并让“粒子系统 $\to$ 连续分布”的极限可被分析。但它并不自动解决非凸性：要证明全局收敛，通常还需要初始化、齐次性、测度支撑以及泛函几何结构等额外条件。

## 6. 为什么会出现 Frank-Wolfe

若无限宽模型写成某个原子集合的凸包或带总变差约束的测度优化，Frank-Wolfe 方法每一步寻找一个最能降低目标的新原子，再更新已有原子的凸组合。对神经网络而言，这相当于逐步添加神经元。

因此，有限宽网络可被看成无限宽凸表示的稀疏近似。在目标足够光滑时，典型函数值误差可按 $O(1/m)$ 衰减；转成函数 $L^2$ 距离时常出现 $O(1/\sqrt m)$ 量级。具体速率依赖目标几何与范数，不能仅凭“网络更宽”直接断言。

## 7. 两层网络的 Rademacher 复杂度

给定样本 $S=(x_1,\ldots,x_n)$，经验 Rademacher 复杂度定义为

```math
\widehat{\mathfrak R}_S(\mathcal F)
=
\mathbb E_\varepsilon
\left[
\sup_{f\in\mathcal F}
\frac1n\sum_{i=1}^{n}\varepsilon_if(x_i)
\right],
```

其中 $\varepsilon_i$ 独立且等概率取 $\pm1$。

对 $G$-Lipschitz 损失，收缩不等式把损失类的复杂度控制为预测函数类复杂度的常数倍。经验风险最小化的期望统计误差典型地满足

```math
\mathbb E\!left[R(\widehat f)-\inf_{f\in\mathcal F}R(f)\right]
\lesssim
4G\,\mathfrak R_n(\mathcal F),
```

其中常数随定义约定略有不同。

## 8. 归一化两层 ReLU 网络的复杂度界

考虑函数类

```math
\mathcal F=
\left\{
x\mapsto\sum_{j=1}^{m}\eta_j\sigma(w_j^\top x+b_j):
\sum_j|\eta_j|\le D,
\ \|w_j\|_2^2+b_j^2/R^2\le1
\right\},
```

并假设 $\|x_i\|_2\le R$。利用输出系数的 $\ell_1$ 约束，关于多个神经元的上确界会退化为关于单个归一化神经元的上确界；再用 ReLU 收缩性和 Cauchy-Schwarz，可得量级

```math
\mathfrak R_n(\mathcal F)
\lesssim
\frac{DR}{\sqrt n}.
```

这个界不显含输入维数，是因为使用了 $\ell_2$ 参数约束和 $\ell_2$ 输入半径。

若改用 $\ell_1$ 权重约束和 $\ell_\infty$ 输入界，需控制 Rademacher 向量各坐标的最大值，最终出现

```math
\mathfrak R_n(\mathcal F)
\lesssim
DR\sqrt{\frac{\log d}{n}}.
```

$\sqrt{\log d}$ 来自 $d$ 个次高斯坐标最大值的期望，而不是简单地“网络参数越多就线性变差”。这也是范数选择影响维度依赖的典型例子。

## 9. 深层网络的递推界

设第 0 层是线性函数类 $\mathcal F_0$，第 $\ell+1$ 层由第 $\ell$ 层函数经过激活并做范数受控的线性组合得到。若第 $\ell+1$ 层的权重范数上界为 $D_{\ell+1}$，激活函数是 Lipschitz 且 $\sigma(0)=0$，则收缩不等式给出形式上的递推：

```math
\mathfrak R_n(\mathcal F_{\ell+1})
\lesssim
c_\sigma D_{\ell+1}
\mathfrak R_n(\mathcal F_\ell).
```

逐层展开得到

```math
\mathfrak R_n(\mathcal F_L)
\lesssim
\left(\prod_{\ell=1}^{L}c_\sigma D_\ell\right)
\mathfrak R_n(\mathcal F_0).
```

它解释了为什么深层网络的简单范数界经常出现层范数乘积，也说明仅靠这种粗界可能随深度迅速变松。更精细的理论会利用谱范数、路径范数、间隔或数据相关结构。

## 10. Ch9.3 逼近误差的入口

手写稿最后转入逼近误差。ReLU 是连续分段线性函数，一层网络可以组合出复杂的分段线性函数；在合适的积分表示下，无限宽网络写成

```math
f(x)=\int\sigma(w^\top x+b)\,d\nu(w,b).
```

有限宽网络就是用有限个原子近似该积分。其逼近能力取决于表示测度的总变差、输入域、目标函数正则性以及采用的误差范数。这里应区分两件事：

- **万能逼近**说明“宽度足够大时可以逼近”；
- **逼近速率**说明“要达到误差 $\varepsilon$ 需要多大宽度”。

前者是定性存在性，后者才决定高维中是否实际可行。

## 11. 本章概念地图

```text
有限宽两层网络
  |- 非凸参数优化
  |- 正齐次性与归一化
  |- 范数控制 -> Rademacher 复杂度 -> 统计误差
  |
  `- 宽度 m -> 无穷
       |- 经验测度 -> 概率测度
       |- 粒子梯度流 -> Wasserstein 梯度流
       `- 无限宽表示 -> 有限原子近似 -> 逼近误差
```

这与前面章节的关系是：Ch4 提供经验过程和 Rademacher 工具，Ch5 提供优化算法与收敛视角，Ch9 把二者用于可学习特征的神经网络。
