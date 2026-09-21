# Ch8 稀疏回归与 Lasso：简单笔记

> 状态：`note_unverified`。整理自《L1正则化与稀疏回归》学习稿和《三月七都能看懂的压缩感知》本地发布稿，并对照锁定版 LTFP §8.1、§8.3.1–§8.3.5 核对基本设定。这里只建立 Ch8 主线，不把来源稿中的简写扩成完整证明。

## 1. 高维问题为什么需要稀疏性

在线性模型中，设

```math
y=\Phi\theta^\star+\varepsilon,
\qquad
\Phi\in\mathbb R^{n\times d}.
```

当 $d$ 很大甚至远大于 $n$ 时，不加结构假设就无法稳定估计所有参数。Ch8 假设真实参数只有少数非零分量：

```math
\|\theta^\star\|_0=k\ll d.
```

这里的目标首先是控制预测误差

```math
\frac1n\|\Phi(\widehat\theta-\theta^\star)\|_2^2,
```

它与参数误差 $\|\widehat\theta-\theta^\star\|_2^2$、支撑恢复和符号恢复不是同一个问题。预测准确并不自动意味着选中了完全正确的变量。

## 2. 从 $\ell_0$ 到 $\ell_1$

$\ell_0$ 惩罚直接计算非零坐标数，最贴近稀疏性，但一般需要在大量支撑集之间做组合搜索。Lasso 用凸的 $\ell_1$ 范数替代它：

```math
\widehat\theta
\in\operatorname*{argmin}_{\theta\in\mathbb R^d}
\left\{
\frac1{2n}\|y-\Phi\theta\|_2^2
+\lambda\|\theta\|_1
\right\}.
```

与岭回归的平方 $\ell_2$ 惩罚相比，$\ell_1$ 球有位于坐标轴上的尖角，最优解更容易落在这些尖角上，从而出现精确的零坐标。但几何图像只是直觉；更直接的机制来自非光滑最优性条件。

## 3. 为什么系数能精确变成零

先看一维问题：

```math
\min_{\theta\in\mathbb R}
\frac12(y-\theta)^2+\lambda|\theta|.
```

它的解是软阈值

```math
S_\lambda(y)
=\operatorname{sign}(y)(|y|-\lambda)_+.
```

因此 $|y|\le\lambda$ 时，解不是“接近零”，而是恰好等于零。

对一般 Lasso，记光滑部分

```math
F(\theta)=\frac1{2n}\|y-\Phi\theta\|_2^2.
```

逐坐标最优性条件为

```math
\begin{cases}
\nabla_jF(\widehat\theta)+\lambda\operatorname{sign}(\widehat\theta_j)=0,
&\widehat\theta_j\ne0,\\
|\nabla_jF(\widehat\theta)|\le\lambda,
&\widehat\theta_j=0.
\end{cases}
```

第二行说明：只要损失在某个坐标上的下降动力不足以超过阈值 $\lambda$，该坐标就可以停在零点。特别地，若

```math
\lambda\ge\left\|\frac1n\Phi^\top y\right\|_\infty,
```

则 $\theta=0$ 是 Lasso 的一个最小化解。

## 4. 基本不等式与噪声项

令 $\Delta=\widehat\theta-\theta^\star$。由 $\widehat\theta$ 的最优性，并代入 $y=\Phi\theta^\star+\varepsilon$，得到

```math
\frac1{2n}\|\Phi\Delta\|_2^2
\le
\frac1n\varepsilon^\top\Phi\Delta
+\lambda\bigl(\|\theta^\star\|_1-\|\widehat\theta\|_1\bigr).
```

噪声项由 $\ell_1$ 与 $\ell_\infty$ 的对偶关系控制：

```math
\frac1n\varepsilon^\top\Phi\Delta
\le
\left\|\frac1n\Phi^\top\varepsilon\right\|_\infty
\|\Delta\|_1.
```

这解释了为什么正则化尺度通常与 $\sqrt{\log d/n}$ 有关：需要同时控制 $d$ 个坐标中的最大噪声相关性。

## 5. 慢速率与快速率不是一回事

在几乎不对设计矩阵作额外假设时，Lasso 可以得到量级为

```math
\|\theta^\star\|_1\sqrt{\frac{\log d}{n}}
```

的预测误差控制。这被称为慢速率，因为对 $n$ 的依赖是 $n^{-1/2}$。

若再利用真实支撑 $A=\operatorname{supp}(\theta^\star)$，从基本不等式推出锥条件

```math
\|\Delta_{A^c}\|_1\le3\|\Delta_A\|_1,
```

并且设计矩阵在这个锥上满足受限特征值条件

```math
\frac1n\|\Phi\Delta\|_2^2
\ge\kappa\|\Delta_A\|_2^2,
```

则预测误差可以达到

```math
O\!\left(\frac{\sigma^2k\log d}{n}\right).
```

这类快速率依赖更强的设计条件。若特征高度相关或稀疏先验本身不成立，Lasso 不应被期待自动优于岭回归。

## 6. 与压缩感知的关系

[《三月七都能看懂的压缩感知》](../../algorithms/compressed-sensing.md)使用观测模型 $s=Ax^\star+\varepsilon$ 讨论从少量测量恢复稀疏信号。把 $A$ 看成设计矩阵、$x^\star$ 看成稀疏参数时，它与稀疏回归共享 Lasso 目标、基本不等式、对偶范数和受限条件。

两者强调点不同：压缩感知更关心信号恢复和测量矩阵；统计学习中的 Ch8 更关心预测风险、变量选择、噪声和样本复杂度。不能只因目标函数相似就把两套结论的假设互换。

## 7. 原始学习稿留下的扩展方向

《L1正则化与稀疏回归》还记录了以下方向，但没有给出足以独立核验的完整条件和证明：

- **精确支撑恢复与 irrepresentable condition**：要求非支撑特征不能被支撑特征过强表示；这比预测误差界需要更强条件。
- **Adaptive Lasso**：用初始估计构造不同坐标的权重，减轻统一 $\ell_1$ 收缩带来的偏差。
- **Elastic Net**：同时使用 $\ell_1$ 与平方 $\ell_2$ 惩罚，以结合稀疏性和更稳定的数值性质。
- **广义线性模型**：把平方损失替换为逻辑回归等凸损失；慢速率较容易推广，快速率需要额外分析。
- **去偏 Lasso**：在高维正则估计后增加校正项，用于近似消除收缩偏差。
- **Dantzig selector**：用 $\ell_\infty$ 约束噪声相关性，把估计写成线性规划型问题。

这些内容先作为后续阅读地图，不计为 Ch8 相应命题或习题已经完成。
