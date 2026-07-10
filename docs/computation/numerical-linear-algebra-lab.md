# 数值线性代数上机实验

> 计算数学上机实验 · 数值线性代数 ·（作者信息已脱敏）
>
> 本页由课程上机报告整理而来，配套 MATLAB 代码见文末「代码索引」。原报告中的公式多为公式对象，文本抽取时丢失，本页按标准形式重新排版，细节（迭代矩阵写法、复杂度常数等）请对照原报告核对。

围绕"求解 $Ax=b$"这一核心，本实验实现并对比了三类方法：直接法、古典迭代法、特征值算法。

## 一、直接法求解线性方程组

### 1.1 高斯消元（列主元 / 全主元）

通过高斯变换 $L_k$ 逐列将矩阵下三角部分消为零，最终上三角化。**列主元**在每一列选取绝对值最大的元素移到对角位以避免小主元导致的数值不稳定；**全主元**同时在行、列中选主元，稳定性最好但代价更高。

### 1.2 平方根法（Cholesky 分解）

针对对称正定矩阵 $A$，将 $A=LL^\top$。按列计算：先算对角元 $l_{ii}$，再算该列非对角元 $l_{ij}\ (j<i)$。利用对称性，计算量约为 LU 分解的一半。

### 1.3 QR 分解（Householder / Givens）

将 $A=QR$（$Q$ 正交、$R$ 上三角），则 $Ax=b$ 化为 $Rx=Q^\top b$ 的回代。

- **Householder 变换**：$H=I-2\dfrac{vv^\top}{v^\top v}$，是关于超平面的镜射，正交对合。逐列选取反射向量 $v$ 将该列对角线以下元素一次性消零。
- **Givens 变换**：通过平面旋转逐个消元，适合稀疏 / 局部消元。

### 直接法对比

| 方法 | 适用性 | 复杂度 | 精度 |
|---|---|---|---|
| 列主元 LU | 非奇异矩阵 | $O(n^3)$ | 较高（避免小主元） |
| 全主元 LU | 所有矩阵 | $O(n^3)$ + 行列交换 | 最高 |
| Cholesky | 对称正定 | ≈ LU 的一半 | 高（利用对称性） |
| QR | 所有矩阵、超定 / 最小二乘 | $O(n^3)$（常数更大） | 高 |

结论：对称正定优先 Cholesky；一般矩阵用列主元或 QR；对稳定性要求极高时用全主元。

## 二、古典迭代法

将 $A=D-L-U$（$D$ 对角、$L,U$ 分别为严格下 / 上三角），迭代 $x^{(k+1)}=Mx^{(k)}+c$。收敛的充要条件是迭代矩阵谱半径 $\rho(M)<1$（或某诱导范数 $\|M\|<1$）；$A$ 严格对角占优或不可约对角占优时必收敛（充分条件）。

- **Jacobi**：$M_J=D^{-1}(L+U)$。
- **Gauss–Seidel**：$M_{GS}=(D-L)^{-1}U$。
- **SOR（超松弛）**：引入松弛因子 $\omega$，$M_\omega=(D-\omega L)^{-1}\big[(1-\omega)D+\omega U\big]$。$A$ 对称正定时，$0<\omega<2$ 必收敛；存在最佳因子 $\omega_{\mathrm{opt}}$ 使收敛最快。
- **最速下降法**：$x_{k+1}=x_k+\alpha_k r_k$，$r_k=b-Ax_k$，$\alpha_k=\dfrac{r_k^\top r_k}{r_k^\top A r_k}$。$A$ 对称正定时收敛，速率约为 $\big(\tfrac{\kappa-1}{\kappa+1}\big)$，$\kappa$ 为条件数。
- **共轭梯度法**：对称正定下理论上至多 $n$ 步得精确解；收敛速率约 $\big(\tfrac{\sqrt\kappa-1}{\sqrt\kappa+1}\big)$，远快于最速下降。

迭代法每步复杂度 $O(n^2)$，总复杂度 $O(kn^2)$，$k$ 为迭代次数。

## 三、特征值：幂法 / 反幂法 / QR 方法

- **幂法**（最大特征值）：$v_{k+1}=\dfrac{Av_k}{\|Av_k\|}$，特征值由 Rayleigh 商 $\lambda\approx\dfrac{v_k^\top A v_k}{v_k^\top v_k}$ 估计。收敛因子为 $|\lambda_2/\lambda_1|$。
- **反幂法**（最小特征值）：对 $A^{-1}$ 作幂法，收敛因子为最小与次小特征值之比。
- **QR 方法**（全部特征值）：先用 Householder 变换将 $A$ 化为上 Hessenberg 型，再迭代 $A_k=Q_kR_k,\ A_{k+1}=R_kQ_k$，对角元收敛到特征值。**带位移**（$A_k-\sigma_k I=Q_kR_k$）显著加速；**双步隐式 QR** 可达渐近平方 / 立方阶收敛。

## 四、小结

数值线性代数的核心是"计算"——不同于高等代数强调线性空间等概念，这里更关注复杂度、精度、稳定性这些工程级指标。直接法、迭代法、特征值算法看似只是"解 $Ax=b$"的不同路径，但背后的权衡（存储 vs 速度、精确 vs 近似、通用 vs 专用）才是这门课真正的肌肉记忆。

## 代码索引

MATLAB 实现（22 个文件，见 [GitHub 目录 `code/numlinalg/`](https://github.com/HuangBlac/AI-Math-Docs/tree/wiki-experiment/docs/computation/code/numlinalg)）：

**直接法**
- `fullPivotGauss.m` — 全主元高斯消元
- `householder.m` / `househoulder.m` / `householderfenjie.m` / `householdersolve.m` — Householder QR 分解与回代求解
- `givenstransformation.m` / `givenssolution.m` — Givens 变换与求解
- `solve.m` / `solve1.m` / `solve2.m` — 线性方程组求解主程序

**迭代法**
- `Jacobi_solution.m` — Jacobi 迭代
- `GSdiedai.m` — Gauss–Seidel 迭代
- `SOR.m` — 超松弛（SOR）迭代
- `zuisuxiajiang.m` — 最速下降法
- `CG.m` — 共轭梯度法

**特征值**
- `Hessenberge.m` — 上 Hessenberg 化
- `QReigsolving.m` / `eigsolving_qr.m` — QR 迭代求特征值
- `doublestepQR.m` — 双步位移 QR

**辅助**
- `fanshu_juzhen.m` / `fanshu_xiangliang.m` — 矩阵 / 向量范数
- `beginning.m` — 初始化 / 入口
