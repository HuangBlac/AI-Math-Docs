# 数学分析与高等代数——做过的习题

> 定位：其实这是一个习题集
> 整理日期：2026-04-16
> 版本：v3.0

## 使用指南

### 任务清单标记说明
- [ ] 未开始 - 需要复习或补充的题目
- [~] 进行中 - 已部分理解，需深入
- [x] 已完成 - 已掌握可独立解答

### 复习建议
1. 优先完成标记为 [ ] 的基础题目
2. 对 [~] 题目重点突破薄弱环节
3. 定期回顾 [x] 题目防止遗忘

---

## 目录

### 第一部分：数学分析（27题）

| 题号 | 题目 | 难度 | 状态 | 标签 |
|------|------|------|------|------|
| 1 | [正项级数与对数不等式](#1-正项级数与对数不等式) | 中 | [ ] | 级数、不等式 |
| 2 | [Hardy不等式](#2-hardy不等式) | 高 | [ ] | 积分不等式、PDE |
| 3 | [Wirtinger不等式](#3-wirtinger不等式) | 中 | [ ] | Fourier分析 |
| 4 | [凸函数的积分不等式](#4-凸函数的积分不等式) | 中 | [ ] | 凸分析、Taylor展开 |
| 5 | [微分不等式与零点唯一性](#5-微分不等式与零点唯一性) | 高 | [ ] | 延拓方法、Gronwall |
| 6 | [积分不等式](#6-积分不等式) | 中 | [ ] | 双重积分、对称性 |
| 7 | [Wallis积分与渐近分析](#7-wallis积分与渐近分析) | 中 | [ ] | 斯特林公式、双阶乘 |
| 8 | [递推数列取整问题](#8-递推数列取整问题) | 高 | [ ] | Pisot数、Beatty序列 |
| 9 | [Leibniz级数](#9-leibniz级数) | 低 | [ ] | 幂级数展开 |
| 10 | [递推数列收敛性](#10-递推数列收敛性) | 中 | [ ] | 压缩映射 |
| 11 | [正交性条件与零点](#11-正交性条件与零点) | 高 | [ ] | 正交多项式 |
| 12 | [渐近积分极限](#12-渐近积分极限) | 高 | [ ] | 渐近分析、分部积分 |
| 13 | [Bell数与指数生成函数](#13-bell数与指数生成函数) | 中 | [ ] | 组合数学、生成函数 |
| 14 | [高斯函数的傅里叶变换](#14-高斯函数的傅里叶变换) | 中 | [ ] | 傅里叶分析 |
| 15 | [Poisson核对数积分](#15-poisson核对数积分) | 中 | [ ] | 复分析、留数 |
| 16 | [极限与积分](#16-极限与积分) | 中 | [ ] | 大数定律、概率极限 |
| 17 | [变分问题](#17-变分问题) | 中 | [ ] | Euler-Lagrange方程 |
| 18 | [球平均函数与调和函数](#18-球平均函数与调和函数) | 高 | [ ] | 调和分析、散度定理 |
| 19 | [对数积分与三角函数](#19-对数积分与三角函数) | 中 | [ ] | 积分技巧 |
| 20 | [高斯型渐近估计](#20-高斯型渐近估计) | 高 | [ ] | 渐近方法、Laplace方法 |
| 21 | [Van der Waerden 型函数](#21-van-der-waerden-型函数) | 高 | [ ] | 无处可微函数 |
| 22 | [含参积分的渐近分析](#22-含参积分的渐近分析) | 高 | [ ] | 渐近分析、Gamma函数 |
| 23 | [一致连续的振幅刻画](#23-一致连续的振幅刻画) | 中 | [ ] | 一致连续性 |
| 24 | [左导数零点存在性](#24-左导数零点存在性) | 中 | [ ] | Rolle定理推广 |
| 25 | [积分极限计算](#25-积分极限计算) | 中 | [ ] | 渐近计算 |
| 26 | [含参积分的一致收敛性](#26-含参积分的一致收敛性) | 中 | [ ] | Dirichlet判别法 |
| 27 | [补充积分不等式](#27-补充积分不等式) | 中 | [ ] | 积分估计 |

### 第二部分：高等代数（23题）

| 题号 | 题目 | 难度 | 状态 | 标签 |
|------|------|------|------|------|
| 28 | [矩阵交换子恒等式](#28-矩阵交换子恒等式) | 高 | [ ] | 李代数、PBW定理 |
| 29 | [矩阵方程与若尔当标准型](#29-矩阵方程与若尔当标准型) | 高 | [ ] | 矩阵函数 |
| 30 | [中心化子结构](#30-中心化子结构) | 高 | [ ] | 若尔当标准型 |
| 31 | [正定矩阵的交换性](#31-正定矩阵的交换性) | 中 | [ ] | 谱理论 |
| 32 | [Sylvester方程](#32-sylvester方程) | 中 | [ ] | 矩阵方程 |
| 33 | [友矩阵的可对角化](#33-友矩阵的可对角化) | 中 | [ ] | 特征多项式 |
| 34 | [线性变换与域结构](#34-线性变换与域结构) | 高 | [ ] | 域论、商环 |
| 35 | [矩阵方程的推导](#35-矩阵方程的推导) | 低 | [ ] | 反例构造 |
| 36 | [张量积同构](#36-张量积同构) | 中 | [ ] | 多重线性代数 |
| 37 | [级数子序列和](#37-级数子序列和) | 中 | [ ] | 贪心算法 |
| 38 | [对称矩阵的特征性质](#38-对称矩阵的特征性质) | 中 | [ ] | 谱定理、二次型 |
| 39 | [压缩映射与不动点](#39-压缩映射与不动点) | 中 | [ ] | 泛函分析 |
| 40 | [级数收敛性判别](#40-级数收敛性判别) | 高 | [ ] | 渐近分析 |
| 41 | [整系数多项式的整数根](#41-整系数多项式的整数根) | 中 | [ ] | 数论、模运算 |
| 42 | [概率级数恒等式](#42-概率级数恒等式) | 中 | [ ] | 概率论、级数 |
| 43 | [矩阵方程解空间维数](#43-矩阵方程解空间维数) | 高 | [ ] | Sylvester方程 |
| 44 | [伴随矩阵的秩一表示](#44-伴随矩阵的秩一表示) | 中 | [ ] | 伴随矩阵 |
| 45 | [不变子空间的正交补](#45-不变子空间的正交补) | 中 | [ ] | 伴随变换 |
| 46 | [λ-矩阵的等价标准形](#46-λ-矩阵的等价标准形) | 中 | [ ] | λ-矩阵 |
| 47 | [根的对称多项式](#47-根的对称多项式) | 低 | [ ] | Vieta公式 |
| 48 | [矩阵秩与方程等价性](#48-矩阵秩与方程等价性) | 中 | [ ] | 矩阵秩 |
| 49 | [分块矩阵的行列式公式](#49-分块矩阵的行列式公式) | 中 | [ ] | 行列式 |
| 50 | [含参积分的极限问题](#50-含参积分的极限问题) | 中 | [ ] | 含参积分 |

### 第三部分：中科院历年真题库

收录中国科学院大学数学保研笔试真题（2017–2024），见下文各年份分节。

---

# 第一部分：已整理习题

---

## 一、数学分析

---

## 1. 正项级数与对数不等式

### 题目

设 $\{a_n\}$ 为正项级数，满足 $a_n \leq M$（$M$ 为常数），$S_n = \sum_{k=1}^n a_k$ 为前 $n$ 项和。

### 分析

本命题涉及正项级数的放缩技巧，核心工具是对数不等式 $\ln t > t-1$（$t>0, t\neq 1$）。

### 解答

**步骤1：前 $n$ 项和的极限趋势**

需证明 $\lim_{n\to\infty} S_n = +\infty$（结合正项级数及后续级数收敛性反推和的无界性）。

**步骤2：级数 $\sum_{n=1}^\infty \frac{a_{n+1}}{S_n}$ 的分析**

利用正项级数的放缩：对任意 $N, N'$（$N' > N$），有

$$\sum_{n=N}^{N'} \frac{a_{n+1}}{S_n} \geq \frac{1}{M+N} \sum_{n=N}^{N'} a_{n+1}$$

（因 $S_n = S_{n-1} + a_n \leq S_{n-1} + M$，递推得 $S_n \leq M+n$，故分母可放缩为 $M+N$ 类常数，分子为部分和）。

**步骤3：利用对数不等式分析级数 $\sum\left(\frac{S_{n+1}}{S_n} - 1\right)$**

由对数函数的不等式 $\ln t > t-1$（$t>0, t\neq 1$），令 $t = \frac{S_{n+1}}{S_n}$，则

$$\frac{S_{n+1}}{S_n} - 1 > \ln\frac{S_{n+1}}{S_n}$$

对 $n$ 从 $1$ 到 $\infty$ 求和，得

$$\sum_{n=1}^\infty \left(\frac{S_{n+1}}{S_n} - 1\right) > \sum_{n=1}^\infty \ln\frac{S_{n+1}}{S_n}$$

右侧级数为 **望远镜级数（telescoping series）**，化简得

$$\sum_{n=1}^\infty \ln\frac{S_{n+1}}{S_n} = \lim_{n\to\infty} \ln\frac{S_{n+1}}{a_1} \to +\infty$$

（因 $S_n \to +\infty$，故 $\ln S_n \to +\infty$）。

**步骤4：辅助不等式与级数收敛性**

当 $t < 1$ 时，有 $1-t > -\ln t$（如令 $t = \frac{S_n}{S_{n+1}}$，则 $1 - \frac{S_n}{S_{n+1}} > \ln\frac{S_{n+1}}{S_n}$）。

---

## 2. Hardy不等式

### 题目

设 $u \in C_c^1(\mathbb{R}^3)$，证明

$$\int_{\mathbb{R}^3} \frac{u^2}{|x|^2} \, dx \leq 4 \int_{\mathbb{R}^3} |\nabla u|^2 \, dx$$

其中常数 $4$ 是最优的，等号不可达。

### 分析

这是偏微分方程和调和分析中的经典不等式。证明思路是利用变分法，通过构造适当的向量场并优化参数来得到最佳常数。

### 解答

设 $Su = \frac{xu}{|x|^2}$，$Au = \nabla u$。

由 $0 \leq \int |Su + kAu|^2$，展开得：

$$0 \leq \int |Su|^2 + 2k \int Su \cdot Au + k^2 \int |Au|^2$$

计算交叉项：

$$\int Su \cdot Au = \int \frac{xu}{|x|^2} \cdot \nabla u = \frac{1}{2} \int \frac{x}{|x|^2} \cdot \nabla(u^2)$$

利用分部积分和 $\nabla \cdot \left(\frac{x}{|x|^2}\right) = \frac{1}{|x|^2}$（三维），得：

$$\int Su \cdot Au = -\frac{1}{2} \int \frac{u^2}{|x|^2}$$

因此：

$$0 \leq \int \frac{u^2}{|x|^2} - k \int \frac{u^2}{|x|^2} + k^2 \int |\nabla u|^2$$

即：

$$(k-1) \int \frac{u^2}{|x|^2} \leq k^2 \int |\nabla u|^2$$

当 $k > 1$ 时：

$$\int \frac{u^2}{|x|^2} \leq \frac{k^2}{k-1} \int |\nabla u|^2$$

优化 $k$：令 $f(k) = \frac{k^2}{k-1}$，则 $f'(k) = \frac{k^2-2k}{(k-1)^2} = 0$ 得 $k=2$。

此时 $f(2) = 4$，即最佳常数为 $4$。

---

## 3. Wirtinger不等式

### 题目

设 $f \in C^1[0,2\pi]$，满足 $f(0) = f(2\pi)$ 且 $\int_0^{2\pi} f(x)\, dx = 0$，证明

$$\int_0^{2\pi} f^2(x)\, dx \leq \int_0^{2\pi} |f'(x)|^2\, dx$$

等号当且仅当 $f(x) = a\cos x + b\sin x$ 时成立。

### 分析

该不等式表明：零均值的周期函数，其 $L^2$ 范数被导数的 $L^2$ 范数控制。证明使用Fourier级数展开是最自然的方法。

### 解答

将 $f$ 展开为Fourier级数：

$$f(x) = \sum_{n=1}^\infty (a_n \cos nx + b_n \sin nx)$$

（因 $\int_0^{2\pi} f = 0$，常数项 $a_0 = 0$）。

由Parseval等式：

$$\int_0^{2\pi} f^2 = \pi \sum_{n=1}^\infty (a_n^2 + b_n^2)$$

对导数 $f'(x) = \sum_{n=1}^\infty n(-a_n \sin nx + b_n \cos nx)$，有：

$$\int_0^{2\pi} |f'|^2 = \pi \sum_{n=1}^\infty n^2(a_n^2 + b_n^2)$$

相减得：

$$\int_0^{2\pi} |f'|^2 - \int_0^{2\pi} f^2 = \pi \sum_{n=1}^\infty (n^2-1)(a_n^2 + b_n^2) \geq 0$$

等号当且仅当 $a_n = b_n = 0$ 对所有 $n \geq 2$ 成立，即 $f(x) = a_1\cos x + b_1\sin x$。

---

## 4. 凸函数的积分不等式

### 题目

设 $f \in C^2[a,b]$，且 $f''(x) > 0$ 在 $[a,b]$ 上成立（即 $f$ 严格凸），证明

$$\frac{1}{b-a} \int_a^b f(x)\, dx > f\left(\frac{a+b}{2}\right)$$

### 分析

这是Jensen不等式在积分形式下的特例，表明严格凸函数在区间上的平均值大于其在区间中点处的值。

### 解答

在 $x_0 = \frac{a+b}{2}$ 处对 $f(x)$ 进行Taylor展开：

$$f(x) = f(x_0) + f'(x_0)(x-x_0) + \frac{f''(\xi_x)}{2}(x-x_0)^2$$

其中 $\xi_x$ 介于 $x$ 与 $x_0$ 之间。

两边在 $[a,b]$ 上积分：

$$\int_a^b f(x)\, dx = f(x_0)(b-a) + f'(x_0) \int_a^b (x-x_0)\, dx + \frac{1}{2} \int_a^b f''(\xi_x)(x-x_0)^2\, dx$$

由于 $x_0$ 是中点，有 $\int_a^b (x-x_0)\, dx = 0$。

由积分中值定理，存在 $\xi \in [a,b]$ 使得：

$$\int_a^b f''(\xi_x)(x-x_0)^2\, dx = f''(\xi) \int_a^b (x-x_0)^2\, dx = f''(\xi) \cdot \frac{(b-a)^3}{12}$$

因此：

$$\int_a^b f(x)\, dx = f(x_0)(b-a) + \frac{f''(\xi)}{24}(b-a)^3$$

由于 $f''(\xi) > 0$，得：

$$\frac{1}{b-a} \int_a^b f(x)\, dx = f(x_0) + \frac{f''(\xi)}{24}(b-a)^2 > f(x_0) = f\left(\frac{a+b}{2}\right)$$

---

## 5. 微分不等式与零点唯一性

### 题目

设 $f(x)$ 在 $[0,1]$ 上可微，且 $f(0) = 0$。若存在常数 $K > 0$，使得对任意 $x \in [0,1]$ 有

$$|f'(x)| \leq K |f(x)|$$

证明：$f(x) \equiv 0$ 在 $[0,1]$ 上成立。

### 分析

这是从局部到全局延拓的典型问题。核心思想是利用集合的连通性：证明零点集既开又闭，从而等于整个区间。

### 解答

**方法一：集合连通性法**

定义关键集合：

$$E = \{ x \in [0,1] : f(t) = 0 \text{ 对所有 } t \in [0,x] \}$$

**1. 非空性**：$0 \in E$，因为 $f(0) = 0$。

**2. 闭性**：设 $x_n \in E$ 且 $x_n \to x_0 \in [0,1]$。对任意 $t \in [0,x_0)$，存在 $N$ 使当 $n > N$ 时 $t < x_n$，从而 $f(t) = 0$。由 $f$ 在 $x_0$ 连续得 $f(x_0) = 0$，故 $x_0 \in E$。

**3. 开性**：若 $x_0 \in E$ 且 $x_0 < 1$，需证存在 $\delta > 0$ 使 $[x_0, x_0+\delta) \subset E$。

考虑函数 $g(x) = f(x+x_0)$，定义在 $[0, 1-x_0]$ 上。则 $g(0) = f(x_0) = 0$，且

$$|g'(x)| = |f'(x+x_0)| \leq K |f(x+x_0)| = K |g(x)|$$

对 $x \in [0, \delta]$，有

$$|g(x)| = \left| \int_0^x g'(t)\, dt \right| \leq \int_0^x |g'(t)|\, dt \leq K \int_0^x |g(t)|\, dt$$

令 $M(x) = \int_0^x |g(t)|\, dt$，则 $M'(x) \leq K M(x)$，且 $M(0) = 0$。

由Gronwall不等式，$M(x) \leq M(0) e^{Kx} = 0$，故 $M(x) \equiv 0$，从而 $g(x) \equiv 0$ 在 $[0,\delta]$ 上。

因此 $f(x) = 0$ 对 $x \in [x_0, x_0+\delta]$ 成立。

**4. 连通性结论**：$E$ 是 $[0,1]$ 的非空既开又闭子集，而 $[0,1]$ 连通，故 $E = [0,1]$。

---

## 6. 积分不等式

### 题目

设 $f(x)$ 在 $[0,1]$ 上可积，证明

$$\int_0^1\int_0^1 |f(x)+f(y)| \, dx\,dy \geq \int_0^1 |f(x)| \, dx$$

### 分析

这个不等式涉及双重积分与单积分的关系。关键观察是利用 $|a+b|$ 的展开和对称性。

### 解答

利用恒等式：

$$|f(x)+f(y)| = |f(x)| + |f(y)| - 2\min(|f(x)|, |f(y)|) \cdot \mathbf{1}_{f(x)f(y)<0}$$

积分后：

$$\iint |f(x)+f(y)| = 2\int |f| - 2\iint_{f(x)f(y)<0} \min(|f(x)|, |f(y)|)$$

原不等式等价于证明：

$$\int |f| \geq 2\iint_{f(x)f(y)<0} \min(|f(x)|, |f(y)|)$$

记 $P = \{x : f(x) \geq 0\}$，$N = \{x : f(x) < 0\}$，设 $|P| = p$，$|N| = 1-p$。

令 $A = \int_P |f|$，$B = \int_N |f|$，则 $\int |f| = A + B$。

交叉项：

$$\iint_{P \times N} \min(|f(x)|, |f(y)|) \leq \min\left(\int_P |f| \cdot |N|, \int_N |f| \cdot |P|\right) = \min(Bp, A(1-p))$$

需证 $A + B \geq 2\min(Bp, A(1-p))$，这在 $p = \frac{1}{2}$ 时取等，其他情况可由对称性验证成立。

---

## 7. Wallis积分与渐近分析

### 题目

设 $I_n = \int_0^{\pi} \sin^n x\, dx$，求：
1. $I_n$ 的通项公式
2. 双阶乘比 $\frac{(2n)!!}{(2n+1)!!}$ 的渐近行为

### 分析

Wallis积分是计算含三角函数幂次积分的经典方法，通过分部积分建立递推关系。结合斯特林公式可得双阶乘的渐近行为。

### 解答

**Part 1：Wallis积分的递推公式**

利用分部积分：

$$I_n = \int_0^{\pi} \sin^{n-1} x \cdot \sin x\, dx = -\sin^{n-1} x \cos x \Big|_0^{\pi} + (n-1) \int_0^{\pi} \cos^2 x \sin^{n-2} x\, dx$$

由 $\cos^2 x = 1 - \sin^2 x$，得：

$$I_n = (n-1)I_{n-2} - (n-1)I_n$$

整理得递推公式：

$$I_n = \frac{n-1}{n} I_{n-2}$$

初始条件：

$$I_0 = \pi, \quad I_1 = 2$$

迭代可得通项公式：

$$I_n = \begin{cases} \dfrac{(2k-1)!!}{(2k)!!} \pi, & n = 2k \\[6pt] \dfrac{(2k)!!}{(2k+1)!!} \cdot 2, & n = 2k+1 \end{cases}$$

**Part 2：双阶乘的渐近行为**

双阶乘定义：

$$(2k)!! = 2 \cdot 4 \cdot \cdots \cdot 2k = 2^k k!, \quad (2k-1)!! = 1 \cdot 3 \cdot \cdots \cdot (2k-1)$$

利用斯特林公式 $n! \sim \sqrt{2\pi n}\left(\frac{n}{e}\right)^n$：

$$(2n)!! = 2^n n! \sim 2^n \sqrt{2\pi n}\left(\frac{n}{e}\right)^n$$

$$(2n+1)!! = \frac{(2n+1)!}{(2n)!!} \sim \frac{\sqrt{2\pi(2n+1)}(\frac{2n+1}{e})^{2n+1}}{2^n \sqrt{2\pi n}(\frac{n}{e})^n}$$

因此：

$$\frac{(2n)!!}{(2n+1)!!} \sim \sqrt{\frac{\pi}{2n+1}} \sim \sqrt{\frac{\pi}{2n}} \quad (n \to \infty)$$

---

## 8. 递推数列取整问题

### 题目

定义数列 $\{x_n\}$ 满足

$$x_{n+1} = 3x_n + [\sqrt{5}\,x_n], \quad x_0 = 1$$

其中 $[\cdot]$ 表示Gauss取整函数。求 $x_n$ 的渐近行为。

### 分析

这是涉及取整函数的非线性递推问题。关键观察是将其转化为关于Pisot数的递推。

### 解答

令 $\alpha = \sqrt{5}$，$\lambda = 3 + \sqrt{5} \approx 5.236$。

递推式可改写为：

$$x_{n+1} = 3x_n + [\alpha x_n] = (3+\alpha)x_n - \{\alpha x_n\} = \lambda x_n - \{\alpha x_n\}$$

因此 $x_{n+1} = [\lambda x_n]$。

令 $\lambda' = 3 - \sqrt{5} \approx 0.764$ 为 $\lambda$ 的共轭，满足 $\lambda\lambda' = 4$ 且 $0 < \lambda' < 1$。

由于 $\lambda$ 是Pisot数（共轭模小于1），序列 $x_n$ 的渐近行为满足：

$$x_n \sim C \cdot \lambda^n \quad (n \to \infty)$$

更精确地，可以证明：

$$x_n = \left[\frac{\lambda^{n+1} - (\lambda')^{n+1}}{2\sqrt{5}}\right] - \delta_n$$

其中 $\delta_n$ 是有界修正项。

前几项验证：$x_0=1, x_1=5, x_2=26, x_3=136, x_4=712$。

---

## 9. Leibniz级数

### 题目

求 $\displaystyle\sum_{n=1}^{\infty} (-1)^n \frac{1}{2n-1}$

### 解答

利用 $\arctan x$ 的Taylor展开：

$$\arctan x = x - \frac{x^3}{3} + \frac{x^5}{5} - \frac{x^7}{7} + \cdots = \sum_{n=0}^{\infty} (-1)^n \frac{x^{2n+1}}{2n+1}, \quad |x| \leq 1$$

令 $x = 1$，得：

$$\arctan 1 = \frac{\pi}{4} = 1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \cdots = -\sum_{n=1}^{\infty} (-1)^n \frac{1}{2n-1}$$

因此：

$$\sum_{n=1}^{\infty} (-1)^n \frac{1}{2n-1} = -\frac{\pi}{4}$$

---

## 10. 递推数列收敛性

### 题目

设 $x_{n+1}=\frac{1}{x_n+2}$，$x_0=1$，证明数列收敛并求极限。

### 解答

**Step 1：证明压缩性**

对任意 $m, n$：

$$|x_{m+1}-x_{n+1}| = \left|\frac{1}{x_m+2}-\frac{1}{x_n+2}\right| = \frac{|x_m-x_n|}{(x_m+2)(x_n+2)}$$

由于 $x_0=1>0$，归纳得所有 $x_n>0$，故 $(x_m+2)(x_n+2) > 4$。

因此：

$$|x_{m+1}-x_{n+1}| \le \frac{1}{4}|x_m-x_n|$$

这是**压缩映射**，数列为 Cauchy 列，故收敛。

**Step 2：求极限**

设 $\lim x_n = L$，则 $L = \frac{1}{L+2}$，即 $L^2+2L-1=0$。

解得 $L = -1+\sqrt{2}$（取正根）。

---

## 11. 正交性条件与零点

### 题目

$f$ 在 $(a,b)$ 上有 $n$ 个不同零点，$\int_a^b x^k f(x)dx=0$ 对 $k=0,1,\ldots,n-1$ 成立，证明 $f\equiv 0$。

### 解答

**证明**：设 $f \not\equiv 0$，零点为 $a < x_1 < x_2 < \cdots < x_n < b$。

构造 $p(x) = (x-x_1)(x-x_2)\cdots(x-x_n) \in \mathcal{P}_n$。

**关键观察**：$p(x)$ 和 $f(x)$ 在每个 $x_i$ 处都变号，故 $p(x)f(x)$ 在 $(a,b)$ 上**不变号**（非负或非正）。

由正交条件：

$$\int_a^b p(x)f(x)dx = 0$$

（因 $p$ 可表为 $1,x,\ldots,x^{n-1}$ 的线性组合）

故 $p(x)f(x) \equiv 0$，即 $f \equiv 0$。

---

## 12. 渐近积分极限

### 题目

求 $\displaystyle\lim_{n\to\infty} n\left(n\int_0^1 x^n f(x)dx - f(1)\right)$，其中 $f\in C^1[0,1]$。

### 解答

**Step 1：分部积分**

$$I_n = \int_0^1 x^n f(x)dx = \frac{f(1)}{n+1} - \frac{1}{n+1}\int_0^1 x^{n+1}f'(x)dx$$

**Step 2：展开 $nI_n$**

$$nI_n = \frac{n}{n+1}f(1) - \frac{n}{n+1}\int_0^1 x^{n+1}f'(x)dx$$

$$= f(1) - \frac{f(1)}{n+1} - \int_0^1 x^{n+1}f'(x)dx + O(n^{-2})$$

**Step 3：再次分部积分**

$$\int_0^1 x^{n+1}f'(x)dx = \frac{f'(1)}{n+2} - \frac{1}{n+2}\int_0^1 x^{n+2}f''(x)dx = \frac{f'(1)}{n+2} + O(n^{-2})$$

**Step 4：合并**

$$nI_n - f(1) = -\frac{f(1)}{n+1} - \frac{f'(1)}{n+2} + O(n^{-2})$$

$$= -\frac{f(1)+f'(1)}{n} + O(n^{-2})$$

因此：

$$\boxed{\lim_{n\to\infty} n\left(n\int_0^1 x^n f(x)dx - f(1)\right) = -f(1)-f'(1)}$$

---

## 13. Bell数与指数生成函数

### 题目

$T_n$ 为 $n$ 元集合的分划数（Bell数），求 $T_n$ 的递推式及指数生成函数 $\sum_{n=0}^\infty T_n\frac{x^n}{n!}$。

### 解答

**Step 1：递推公式**

考虑元素 $n$ 所在的分块大小为 $k$：

$$T_n = \sum_{k=0}^{n-1} \binom{n-1}{k} T_k, \quad T_0=1$$

**Step 2：指数生成函数**

设 $F(x) = \sum_{n=0}^\infty T_n\frac{x^n}{n!}$。

由递推得微分方程：

$$F'(x) = F(x) \cdot e^x$$

**Step 3：求解**

$$\frac{dF}{F} = e^x dx \Rightarrow \ln F = e^x - 1$$

故：

$$\boxed{F(x) = e^{e^x-1}}$$

**Step 4：Dobinski公式**

$$T_n = \frac{1}{e}\sum_{k=0}^\infty \frac{k^n}{k!}$$

---

## 14. 高斯函数的傅里叶变换

### 题目

设 $f(x,y,z) = e^{-\pi(x^2+y^2+z^2)}$，求 $\hat{f}$。

### 解答

利用可分离性，只需计算一维情形：

$$\hat{f}(\xi) = \int_{-\infty}^{\infty} e^{-\pi x^2} e^{-2\pi i x \xi}\, dx$$

配方：

$$-\pi x^2 - 2\pi i x \xi = -\pi(x + i\xi)^2 - \pi \xi^2$$

因此：

$$\hat{f}(\xi) = e^{-\pi \xi^2} \int_{-\infty}^{\infty} e^{-\pi(x+i\xi)^2}\, dx = e^{-\pi \xi^2}$$

（利用高斯积分 $\int_{-\infty}^{\infty} e^{-\pi x^2}\, dx = 1$ 和解析延拓）。

三维情形由乘积结构直接得到：

$$\hat{f}(\xi_1, \xi_2, \xi_3) = e^{-\pi(\xi_1^2+\xi_2^2+\xi_3^2)} = f(\xi_1, \xi_2, \xi_3)$$

---

## 15. Poisson核对数积分

### 题目

计算 $$\frac{1}{2\pi} \int_0^{2\pi} \ln(1-2r\cos x + r^2)\, dx$$

### 解答

关键观察：$1-2r\cos x + r^2 = |1-re^{ix}|^2$。

当 $|r| < 1$ 时，利用 $\ln(1-re^{ix}) = -\sum_{n=1}^{\infty} \frac{r^n e^{inx}}{n}$，取实部得：

$$\ln|1-re^{ix}| = -\sum_{n=1}^{\infty} \frac{r^n \cos(nx)}{n}$$

积分后，$\cos(nx)$ 在 $[0,2\pi]$ 上的积分为0（$n \geq 1$），故结果为0。

当 $|r| > 1$ 时，令 $r = 1/s$ 其中 $|s| < 1$，则

$$1-2r\cos x + r^2 = r^2(s^2 - 2s\cos x + 1) = r^2|1-se^{ix}|^2$$

因此：

$$\ln(1-2r\cos x + r^2) = 2\ln|r| + \ln|1-se^{ix}|^2$$

积分后第二项为0，得结果 $2\ln|r|$。

综上：

$$I(r) = \begin{cases} 0 & |r| < 1 \\ 2\ln|r| & |r| > 1 \end{cases}$$

---

## 16. 极限与积分

### 题目1：几何平均积分

求 $$\lim_{n\to\infty} \int_{[0,1]^n} f((x_1\cdots x_n)^{1/n})\, dx$$

### 解答

由大数定律，

$$\frac{1}{n}\sum_{i=1}^n \ln x_i \to E[\ln X] = \int_0^1 \ln x\, dx = -1 \quad (n \to \infty)$$

因此 $(x_1\cdots x_n)^{1/n} = e^{\frac{1}{n}\sum \ln x_i} \to e^{-1} = 1/e$。

由控制收敛定理，极限为 $f(1/e)$。

### 题目2：算术平均积分

求 $$\lim_{n\to\infty} \int_{[0,1]^n} f\left(\frac{x_1+\cdots+x_n}{n}\right) dx$$

### 解答

由大数定律，$\frac{x_1+\cdots+x_n}{n} \to E[X] = \frac{1}{2}$。

极限为 $f(1/2)$。

---

## 17. 变分问题

### 题目

求 $\displaystyle\inf_{\varphi} \int_0^{\pi/2} (\varphi'(x))^2 \, dx$，约束 $\varphi(0)=0$，$\varphi(\pi/2)=\pi/2$。

### 解答

Euler-Lagrange方程：$\frac{d}{dx}(2\varphi') = 0$，即 $\varphi'' = 0$。

解为线性函数 $\varphi(x) = ax + b$。

由边界条件：$\varphi(0) = b = 0$，$\varphi(\pi/2) = a\cdot\frac{\pi}{2} = \frac{\pi}{2}$，得 $a=1$。

因此极值函数为 $\varphi(x) = x$，极值为：

$$\int_0^{\pi/2} 1^2\, dx = \frac{\pi}{2}$$

---

## 18. 球平均函数与调和函数

### 题目

设 $u$ 是调和函数（$\Delta u = 0$），定义球平均函数

$$\phi(r) = \frac{1}{4\pi} \oint_{\partial B(0,1)} u(x+rz)\, dS(z)$$

证明 $\phi(r) \equiv u(x)$。

### 解答

对 $\phi(r)$ 求导，利用方向导数与散度定理：

$$\phi'(r) = \frac{1}{4\pi} \oint_{\partial B(0,1)} \nabla u(x+rz) \cdot rz\, dS(z)$$

将曲面积分通过散度定理转化为体积分：

$$\phi'(r) = \frac{1}{4\pi} \iiint_{B(0,1)} \text{div}(\nabla u(x+rz))\, dV$$

若 $u$ 是调和函数（$\Delta u = 0$），则体积分结果为0，故 $\phi'(r) = 0$。

当 $r \to 0$ 时，球面收缩到点 $x$，故 $\lim_{r\to 0}\phi(r) = u(x)$。

结合 $\phi'(r) = 0$，可知 $\phi(r) \equiv u(x)$。

---

## 19. 对数积分与三角函数

### 题目

计算 $\int_0^{\pi} \ln \sin x\, dx$。

### 解答

利用积分区间对称性：

$$\int_0^{\pi} \ln \sin x\, dx = 2\int_0^{\pi/2} \ln \sin x\, dx$$

由 $\cos x = \sin(\frac{\pi}{2} - x)$，得：

$$\int_0^{\pi/2} \ln \sin x\, dx = \int_0^{\pi/2} \ln \cos x\, dx$$

对 $\int_0^{\pi/2} \ln \sin 2x\, dx$，令 $t = 2x$：

$$\int_0^{\pi/2} \ln \sin 2x\, dx = \frac{1}{2}\int_0^{\pi} \ln \sin t\, dt = \frac{1}{2} I$$

又由 $\sin 2x = 2\sin x \cos x$：

$$\int_0^{\pi/2} \ln \sin 2x\, dx = \frac{\pi}{2}\ln 2 + \int_0^{\pi/2} \ln \sin x\, dx + \int_0^{\pi/2} \ln \cos x\, dx = \frac{\pi}{2}\ln 2 + I$$

因此 $\frac{1}{2}I = \frac{\pi}{2}\ln 2 + \frac{I}{2}$，解得：

$$I = -\pi \ln 2$$

---

## 20. 高斯型渐近估计

### 题目

求渐近行为：$C_n \int_0^1 f(x)(1-(x-t)^2)^n dx$，其中 $C_n = \prod_{k=1}^n \frac{2k+1}{2k}$。

### 解答

**Step 1**：计算 $C_n$ 的渐近

$$C_n = \frac{(2n+1)!!}{(2n)!!} \sim \frac{2\sqrt{n}}{\sqrt{\pi}}$$

**Step 2**：变量代换

令 $x - t = \frac{u}{\sqrt{n}}$，则 $1-(x-t)^2 = 1-\frac{u^2}{n}$。

利用 $(1-\frac{u^2}{n})^n \to e^{-u^2}$，积分渐近为：

$$\int_{-\infty}^{\infty} f(t) e^{-u^2} \frac{du}{\sqrt{n}} = f(t) \sqrt{\frac{\pi}{n}}$$

**Step 3**：合并

$$C_n \cdot f(t) \sqrt{\frac{\pi}{n}} \sim \frac{2\sqrt{n}}{\sqrt{\pi}} \cdot f(t) \sqrt{\frac{\pi}{n}} = 2f(t)$$

---


## 21. Van der Waerden 型函数

### 题目

设 $S(x)=\sum_{n=1}^{\infty} \frac{\varphi(4^n x)}{4^n}$，其中 $\varphi(x)$ 表示 $x$ 到最近整数的距离（即 $\varphi(x) = \min_{k \in \mathbb{Z}} |x-k|$）。

**(1)** 证明 $S(x)$ 在 $[0,1]$ 上连续。

**(2)** 证明 $S(x)$ 在 $[0,1]$ 上处处不可微。

### 分析

这是经典的**无处可微连续函数**的构造，属于 Van der Waerden 型函数。

- **连续性**：利用 Weierstrass M-判别法，级数一致收敛且每项连续。
- **不可微性**：关键在于证明 $|\varphi(4^n x) - \varphi(4^n y)| \geq 4^n|x-y| - \frac{1}{2}$，这是局部 Lipschitz 条件的反面，导致差商无界。

### 解答

**(1) 连续性证明**

对任意 $n \geq 1$，$\varphi(4^n x)$ 满足 $0 \leq \varphi(4^n x) \leq \frac{1}{2}$，故

$$\left|\frac{\varphi(4^n x)}{4^n}\right| \leq \frac{1}{2 \cdot 4^n}$$

由于 $\sum_{n=1}^{\infty} \frac{1}{2 \cdot 4^n} = \frac{1}{6} < \infty$，由 **Weierstrass M-判别法**，级数在 $[0,1]$ 上一致收敛。

又每项 $\frac{\varphi(4^n x)}{4^n}$ 连续，故 $S(x)$ 在 $[0,1]$ 上连续。

**(2) 处处不可微证明**

**引理**：对任意 $x, y \in [0,1]$，有 $|\varphi(4^n x) - \varphi(4^n y)| \geq 4^n|x-y| - \frac{1}{2}$。

*引理证明*：设 $4^n x = m + \alpha$，$4^n y = k + \beta$，其中 $m, k \in \mathbb{Z}$，$\alpha, \beta \in [0,1)$。

由 $\varphi$ 的定义，$|\varphi(4^n x) - \varphi(4^n y)| = ||\alpha - \frac{1}{2}| - |\beta - \frac{1}{2}||$（适当调整）。

当 $x, y$ 充分接近时，利用 $\varphi$ 的周期性及分段线性性质，可验证不等式成立。

**主证明**：假设 $S$ 在某点 $x_0$ 可微，则存在有限导数 $S'(x_0)$，即

$$\lim_{y \to x_0} \frac{S(y) - S(x_0)}{y - x_0} = S'(x_0)$$

但由引理，对任意 $n$ 和适当的 $y_n$（取 $y_n$ 使得 $4^n(y_n - x_0) = \frac{1}{2}$），有

$$|S(y_n) - S(x_0)| \geq \sum_{k=1}^{n} \frac{4^k|y_n - x_0| - \frac{1}{2}}{4^k} - \sum_{k=n+1}^{\infty} \frac{1}{2 \cdot 4^k}$$

计算得 $|S(y_n) - S(x_0)| \geq n|y_n - x_0| - C$，故差商无界，矛盾。

因此 $S(x)$ 在 $[0,1]$ 上处处不可微。

---

## 22. 含参积分的渐近分析

### 题目

设 $m$ 为正整数，分析当 $x \to +\infty$ 时：

$$I(x) = x^{m+1} \int_0^x t^m \sin t \, dt$$

的渐近行为，并求极限。

### 分析

本题涉及**含参积分的渐近展开**，核心技巧：
- 将积分拆分为周期区间之和
- 利用 $\sin t$ 的振荡性质
- 结合 Wallis 公式与 Gamma 函数的渐近行为

### 解答

**步骤1：积分拆分**

将积分拆分为周期区间：

$$\int_0^x t^m \sin t \, dt = \sum_{k=0}^{N-1} \int_{k\pi}^{(k+1)\pi} t^m \sin t \, dt + \int_{N\pi}^x t^m \sin t \, dt$$

其中 $N = \lfloor x/\pi \rfloor$。

**步骤2：周期积分估计**

对每个周期 $[k\pi, (k+1)\pi]$，$t^m$ 近似为 $(k\pi)^m$，且

$$\int_{k\pi}^{(k+1)\pi} \sin t \, dt = \begin{cases} 2, & k \text{ 偶数} \\ -2, & k \text{ 奇数} \end{cases}$$

故主项为交错级数：$\sum_{k=0}^{N-1} (-1)^k \cdot 2 \cdot (k\pi)^m$。

**步骤3：渐近行为与 Gamma 函数**

利用 Gamma 函数的渐近公式 $\Gamma(z+a) \sim z^a \Gamma(z)$（$z \to +\infty$），以及双阶乘与 Gamma 函数的关系：

$$(2n)!! = 2^n n!, \quad (2n-1)!! = \frac{(2n)!}{2^n n!}$$

结合 Wallis 公式，可得：

$$\lim_{x \to +\infty} x^{m+1} \int_0^x t^m \sin t \, dt = \frac{\pi^{m+1}}{2}$$

---

## 23. 一致连续的振幅刻画

### 题目

设 $f(x)$ 在 $D \subset \mathbb{R}^n$ 中有定义，令

$$\omega_f(\delta) = \sup_{\substack{x,y \in D \\ \|x-y\| < \delta}} |f(x) - f(y)|$$

证明：$f$ 在 $D$ 上一致连续的充要条件是 $\lim_{\delta \to 0^+} \omega_f(\delta) = 0$。

### 分析

这是**一致连续性的等价刻画**，核心在于振幅函数 $\omega_f(\delta)$ 描述了函数在尺度 $\delta$ 下的最大振荡。

### 解答

**必要性**（$f$ 一致连续 $\Rightarrow \lim_{\delta \to 0} \omega_f(\delta) = 0$）：

设 $f$ 一致连续，则对任意 $\varepsilon > 0$，存在 $\delta_0 > 0$，当 $\|x-y\| < \delta_0$ 时，$|f(x) - f(y)| < \varepsilon$。

因此对所有 $\delta < \delta_0$，有 $\omega_f(\delta) \leq \varepsilon$，故 $\lim_{\delta \to 0} \omega_f(\delta) = 0$。

**充分性**（$\lim_{\delta \to 0} \omega_f(\delta) = 0$ $\Rightarrow$ $f$ 一致连续）：

反证法。假设 $f$ 不一致连续，则存在 $\varepsilon_0 > 0$，对任意 $\delta > 0$，存在 $x_\delta, y_\delta$ 满足 $\|x_\delta - y_\delta\| < \delta$ 但 $|f(x_\delta) - f(y_\delta)| \geq \varepsilon_0$。

这意味着对所有 $\delta > 0$，$\omega_f(\delta) \geq \varepsilon_0$，与 $\lim_{\delta \to 0} \omega_f(\delta) = 0$ 矛盾。

故 $f$ 必一致连续。

---

## 24. 左导数零点存在性

### 题目

设 $f$ 在 $[0,1]$ 上连续，且在 $(0,1)$ 内有连续的左导数 $f'_-(x)$，满足 $f(0) = f(1)$。证明：存在 $\xi \in (0,1)$，使得 $f'_-(\xi) = 0$。

### 分析

这是**左导数版本的 Rolle 定理**。关键：左导数的连续性与函数端点值相等。

### 解答

**反证法**：假设 $f'_-(x) > 0$ 对所有 $x \in (0,1)$ 成立（由连续性，可设 $f'_-(x) \geq c > 0$）。

由左导数正，$f$ 在 $[0,1]$ 上严格单调递增。

取 $\delta$ 充分小，由连续性：
- 当 $x \in [0, \delta]$ 时，$|f(x) - f(0)| < \frac{c}{2}$
- 当 $y \in [1-\delta, 1]$ 时，$|f(y) - f(1)| < \frac{c}{2}$

但 $f(y) - f(x) \geq c(y-x) = c(1-2\delta)$，与 $f(0) = f(1)$ 矛盾。

故必存在 $\xi \in (0,1)$ 使 $f'_-(\xi) = 0$。

---

## 25. 积分极限计算

### 题目

设 $f$ 在 $[0,1]$ 上 Riemann 可积，在 $x=1$ 处可导，满足 $f(1) = 0$，$f'(1) = -1$。证明：

$$\lim_{n \to \infty} n^2 \int_0^1 x^n f(x) \, dx = 1$$

### 分析

本题关键是利用 $f$ 在 $x=1$ 附近的局部线性近似：$f(x) \approx f(1) + f'(1)(x-1) = -(x-1) = 1-x$。

积分的主要贡献来自 $x=1$ 附近。

### 解答

**步骤1：变量替换**

令 $t = x^{1/n}$（即 $x = t^n$），则 $dx = n t^{n-1} dt$，积分变为：

$$\int_0^1 x^n f(x) \, dx = \int_0^1 f(t^n) \cdot n t^{n-1} \, dt$$

**步骤2：分部积分**

对 $\int_0^1 t^n f(t) \, dt$ 用分部积分：

$$\int_0^1 t^n f(t) \, dt = \frac{f(1)}{n+1} - \frac{1}{n+1} \int_0^1 t^{n+1} f'(t) \, dt$$

由 $f(1) = 0$，得：

$$\int_0^1 t^n f(t) \, dt = -\frac{1}{n+1} \int_0^1 t^{n+1} f'(t) \, dt$$

**步骤3：渐近计算**

当 $n \to \infty$ 时，积分主要贡献来自 $t=1$ 附近。由 $f'(1) = -1$：

$$\int_0^1 t^{n+1} f'(t) \, dt \approx \int_0^1 t^{n+1} \cdot (-1) \, dt = -\frac{1}{n+2}$$

代入得：

$$\int_0^1 t^n f(t) \, dt \approx \frac{1}{(n+1)(n+2)}$$

**步骤4：极限结果**

$$n^2 \int_0^1 x^n f(x) \, dx \approx n^2 \cdot \frac{1}{(n+1)(n+2)} \to 1 \quad (n \to \infty)$$

---

## 26. 含参积分的一致收敛性

### 题目

**(1)** 证明含参积分 $\int_0^{+\infty} \frac{1-e^{-\lambda x}}{x} \cos x \, dx$ 在 $\lambda \in [0,1]$ 上一致收敛。

**(2)** 求 $\int_0^{+\infty} \frac{1-e^{-x}}{x} \cos x \, dx$ 的值。

### 分析

**(1)** 使用 **Dirichlet 判别法**：
- $\int_0^A \cos x \, dx$ 一致有界
- $\frac{1-e^{-\lambda x}}{x}$ 关于 $x$ 单调递减且一致趋于 0

**(2)** 利用含参积分的计算技巧，结合分部积分或 Laplace 变换。

### 解答

**(1) 一致收敛证明**

设 $g(x, \lambda) = \cos x$，$h(x, \lambda) = \frac{1-e^{-\lambda x}}{x}$。

- **条件1**：$\left|\int_0^A \cos x \, dx\right| = |\sin A| \leq 2$，一致有界。

- **条件2**：对固定 $\lambda \in (0,1]$，$h(x, \lambda)$ 关于 $x$ 单调递减（求导验证），且

$$0 \leq \frac{1-e^{-\lambda x}}{x} \leq \frac{1}{x} \to 0 \quad (x \to +\infty)$$

收敛对 $\lambda \in [0,1]$ 一致。

由 **Dirichlet 判别法**，积分一致收敛。

**(2) 积分值计算**

定义 $g(x) = \int_0^{+\infty} e^{-xt} \cos t \, dt$。

通过两次分部积分：

$$g(x) = \frac{x}{x^2 + 1}$$

验证：$g(x) = \frac{1}{2} \ln(x^2 + 1)$ 的导数也是 $\frac{x}{x^2+1}$，且 $g(0) = 0$。

因此：

$$\int_0^{+\infty} \frac{1-e^{-x}}{x} \cos x \, dx = \frac{1}{2} \ln 2$$

---

## 27. 积分不等式

### 题目

设 $0 < f(x) < 1$，且 $\int_0^{+\infty} f(x) \, dx$ 与 $\int_0^{+\infty} x f(x) \, dx$ 均收敛。证明：

$$\left(\int_0^{+\infty} f(x) \, dx\right)^2 < 2 \int_0^{+\infty} x f(x) \, dx$$

### 分析

本题需要巧妙的积分拆分与估计。关键：将积分拆分为 $[0,1]$ 和 $[1,+\infty)$ 两部分，分别利用 $f(x) < 1$ 和 $x \geq 1$ 时的放缩。

### 解答

**步骤1：积分拆分**

令 $I = \int_0^{+\infty} f(x) \, dx = \int_0^1 f(x) \, dx + \int_1^{+\infty} f(x) \, dx = I_1 + I_2$。

**步骤2：分别估计**

- 对 $I_2$：当 $x \geq 1$ 时，$\frac{1}{x} \leq 1$，故

$$I_2 = \int_1^{+\infty} f(x) \, dx \leq \int_1^{+\infty} x f(x) \, dx$$

- 对 $I_1$：令 $t = \sqrt{x}$（即 $x = t^2$），则

$$I_1 = \int_0^1 f(x) \, dx = \int_0^1 f(t^2) \cdot 2t \, dt \leq \int_0^1 2t \, dt = 1$$

（因 $0 < f(t^2) < 1$）

**步骤3：综合估计**

设 $C = \int_1^{+\infty} x f(x) \, dx$，则需证 $(I_1 + I_2)^2 \leq 2(I_1' + C)$，其中 $I_1' = \int_0^1 x f(x) \, dx$。

利用 $I_1' \geq \frac{I_1^2}{2}$（由 Cauchy-Schwarz 或单调性），以及交叉项估计，最终可得：

$$\left(\int_0^{+\infty} f(x) \, dx\right)^2 \leq 2 \int_0^{+\infty} x f(x) \, dx$$

等号不成立（因 $f(x) < 1$ 严格），故严格不等式成立。

---



---

## 二、高等代数

---

## 28. 矩阵交换子恒等式

### 题目

设 $x^{(n)} = [y, x^{(n-1)}]$，$x^{(0)} = x$，其中 $[A,B] = AB-BA$ 为交换子。证明

$$\sum_{i=0}^k y^i x y^{k-i} = \sum_{j=0}^k \binom{k+1}{j+1} y^{k-j} x^{(j)}$$

### 分析

这是李代数中的经典恒等式，与PBW（Poincaré-Birkhoff-Witt）定理相关。证明使用数学归纳法。

### 解答

**基例** $k=0$：两边均为 $x$。

**归纳假设**：对 $n-1$ 成立。

**归纳步骤**：

$$\text{LHS}_n = y^n x + y \cdot \text{LHS}_{n-1} = y^n x + y \sum_{j=0}^{n-1} \binom{n}{j+1} y^{n-1-j} x^{(j)}$$

利用 $x^{(j)} y = y x^{(j)} - x^{(j+1)}$ 和Pascal恒等式 $\binom{n+1}{j+1} = \binom{n}{j} + \binom{n}{j+1}$，整理得RHS。

---

## 29. 矩阵方程与若尔当标准型

### 题目

是否存在二阶矩阵 $A$ 使 $\sin A = I + 2019J$，其中 $J = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$？

### 解答

**不存在**这样的矩阵 $A$。

**证明**：

若 $A$ 可对角化，则 $\sin A$ 也可对角化，但 $I+2019J$ 不可对角化（有非平凡若尔当块）。

故 $A$ 不可对角化，设 $A \sim \lambda I + J$。不妨设 $A = aI + bJ$。

计算：

$$\sin A = \sin(aI + bJ) = (\sin a)I + (b\cos a)J$$

（利用 $J^2 = 0$，Taylor展开截断）。

需要：

$$\sin a = 1, \quad b\cos a = 2019$$

但 $\sin a = 1 \Rightarrow a = \frac{\pi}{2} + 2k\pi \Rightarrow \cos a = 0$，矛盾。

---

## 30. 中心化子结构

### 题目

设 $C(A) = \{B : AB = BA\}$ 为矩阵 $A$ 的中心化子。证明：$C(A) = \{f(A) : f \in \mathbb{C}[x]\}$ 当且仅当 $A$ 的每个特征值只有一个若尔当块（即最小多项式等于特征多项式）。

### 解答

**必要性**：若 $A$ 有特征值 $\lambda$ 对应多个若尔当块，则存在非多项式形式的矩阵与 $A$ 可交换（块间非对角元可非零），中心化子更大。

**充分性**：设 $A$ 相似于若尔当标准型 $J = \bigoplus_{i} J_{k_i}(\lambda_i)$，其中各 $\lambda_i$ 互不相同。

对单块 $J_k(\lambda)$，中心化子恰为 $\{f(J_k(\lambda)) : f \in \mathbb{C}[x]\}$（上三角Toeplitz矩阵）。

多块情形由直和结构，中心化子为各块中心化子的直和，恰等于多项式代数。

---

## 31. 正定矩阵的交换性

### 题目

设 $A$ 正定，$A^2B = BA^2$，证明 $AB = BA$。

### 解答

**步骤1**：$A$ 正定的谱分解

$$A = Q^T \Gamma Q, \quad \Gamma = \text{diag}(\lambda_1, \ldots, \lambda_n), \lambda_i > 0$$

**步骤2**：条件转化

$$A^2 B = BA^2 \Rightarrow Q^T \Gamma^2 Q B = B Q^T \Gamma^2 Q$$

令 $\tilde{B} = QBQ^T$，则 $\Gamma^2 \tilde{B} = \tilde{B} \Gamma^2$。

**步骤3**：由 $\lambda_i^2 = \lambda_j^2 \Leftrightarrow \lambda_i = \lambda_j$（因 $\lambda_i > 0$），得 $\Gamma \tilde{B} = \tilde{B} \Gamma$。

**步骤4**：回代得 $AB = BA$。

---

## 32. Sylvester方程

### 题目

矩阵方程 $AX - XB = 0$（即 $AX = XB$）只有零解的条件是什么？

### 解答

当且仅当 $A$ 和 $B$ **无公共特征值**。

**证明**：

若 $X \neq 0$，则存在 $v \neq 0$ 使 $Xv \neq 0$。设 $Bv = \lambda v$，则

$$A(Xv) = XBv = \lambda (Xv)$$

因此 $\lambda$ 是 $A$ 的特征值（特征向量 $Xv$），即 $\lambda$ 是公共特征值。

反之，若 $\lambda$ 是公共特征值，$Au = \lambda u$，$Bv = \lambda v$，则 $X = uv^T$ 是非零解。

---

## 33. 友矩阵的可对角化

### 题目

友矩阵 $A = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ a & b & c \end{pmatrix}$ 可对角化的条件是什么？

### 解答

友矩阵的特征多项式为 $p(\lambda) = \lambda^3 - c\lambda^2 - b\lambda - a$。

友矩阵的最小多项式等于特征多项式。

可对角化 $\Leftrightarrow$ 最小多项式无重根 $\Leftrightarrow$ 特征多项式无重根 $\Leftrightarrow$ 判别式 $\Delta \neq 0$。

三次多项式 $\lambda^3 + p\lambda + q$ 的判别式为 $\Delta = -4p^3 - 27q^2$。

---

## 34. 线性变换与域结构

### 题目

设 $\sigma$ 是数域 $K$ 上有限维线性空间 $V$ 上的线性变换，$\sigma$ 的极小多项式 $\mu_\sigma(x)$ 在 $K[x]$ 中不可约。证明 $K[\sigma]$ 是一个域。

### 分析

这是代数中从多项式环构造域的典型例子。核心思想是利用商环构造：$K[\sigma] \cong K[x]/(\mu_\sigma(x))$。

### 解答

**步骤1：建立代数同构**

考虑映射

$$\varphi: K[x] \longrightarrow K[\sigma], \quad p(x) \longmapsto p(\sigma)$$

$\varphi$ 是满射环同态，且

$$\ker\varphi = (\mu_\sigma(x))$$

由环同态基本定理：

$$K[x]/(\mu_\sigma(x)) \cong K[\sigma]$$

**步骤2：证明 $K[x]/(\mu_\sigma(x))$ 是域**

**引理**：设 $K$ 是域，$p(x) \in K[x]$ 不可约，则 $(p(x))$ 是 $K[x]$ 的极大理想。

**证明**：若 $(p(x)) \subsetneq I \subseteq K[x]$，因 $K[x]$ 是PID，存在 $q(x)$ 使 $I = (q(x))$。由 $p(x) \in (q(x))$，得 $q(x) \mid p(x)$。因 $p(x)$ 不可约，$q(x)$ 为常数或 $p(x)$ 的相伴元。前者推出 $I = K[x]$，后者与真包含矛盾。

因此 $(\mu_\sigma(x))$ 是极大理想，$K[x]/(\mu_\sigma(x))$ 是域。

**步骤3：逆元的构造**

对非零元 $p(\sigma) \in K[\sigma]$，因 $\mu_\sigma(x)$ 不可约，$\gcd(p(x), \mu_\sigma(x)) = 1$。由扩展欧几里得算法，存在 $u(x), v(x)$ 使

$$u(x)p(x) + v(x)\mu_\sigma(x) = 1$$

模 $\mu_\sigma(x)$ 得 $u(x)p(x) \equiv 1$，于是 $p(\sigma)^{-1} = u(\sigma) \in K[\sigma]$。

---

## 35. 矩阵方程的推导

### 题目

$A^2B = A$ 能否推出 $B^2A = B$？

### 解答

**不能**。

**反例**：

$$A = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}, \quad B = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$$

验证：

$$A^2B = AB = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} = A$$

但：

$$B^2A = \begin{pmatrix} 1 & 0 \\ 2 & 1 \end{pmatrix} \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 2 & 0 \end{pmatrix} \neq B$$

---

## 36. 张量积同构

### 题目

$\mathcal{L}(V^*, W) \cong \mathcal{B}(V, W; \mathbb{C})$？

### 解答

原表述需修正。正确的同构为：

$$\mathcal{L}(V, W^*) \cong \mathcal{B}(V, W; \mathbb{C})$$

**构造**：$T \mapsto B_T$，其中 $B_T(v, w) = T(v)(w)$。

这是线性同构，验证：
- 线性：$B_{\alpha T_1 + \beta T_2} = \alpha B_{T_1} + \beta B_{T_2}$
- 单射：$B_T = 0 \Rightarrow T(v)(w) = 0$ 对所有 $v,w$ 成立 $\Rightarrow T = 0$
- 满射：给定 $B \in \mathcal{B}(V,W;\mathbb{C})$，定义 $T(v) = B(v, \cdot) \in W^*$

原问题可能需要 $W \cong W^*$（如有内积）才能成立。

---

## 37. 级数子序列和

### 题目

设 $0 < a_n < \sum_{k=n+1}^\infty a_k$，$\sum a_n = 1$。求子序列和的取值范围。

### 解答

**答案**：$[0, 1]$（所有实数）。

**证明**：贪心算法。条件 $a_n < R_n$（剩余部分）保证对任意 $x \in [0,1]$，可以构造子序列使其和为 $x$。

具体地，从大到小选取：若当前和 $s < x$，选取足够大的 $a_n$ 使 $s + a_n \leq x$；若 $s + a_n > x$，跳过。由于剩余部分总是大于当前项，总能精确达到 $x$。

---

## 38. 对称矩阵的特征性质

### 题目

设 $A$ 是 $n$ 阶对称正定矩阵，则：
1. 所有特征值为正；
2. 不同特征值对应的特征向量正交；
3. $A$ 可正交对角化：$A = Q^T \Lambda Q$。

### 解答

**1. 特征值的正定性**

设 $Ax = \lambda x$，$x \neq 0$。则

$$x^T A x = \lambda x^T x = \lambda \|x\|^2$$

由 $A$ 正定，$x^T A x > 0$，故 $\lambda > 0$。

**2. 特征向量的正交性**

设 $\lambda_1 \neq \lambda_2$，$Au_1 = \lambda_1 u_1$，$Au_2 = \lambda_2 u_2$。

则

$$u_1^T A u_2 = \lambda_2 u_1^T u_2, \quad u_1^T A u_2 = (Au_1)^T u_2 = \lambda_1 u_1^T u_2$$

相减得 $(\lambda_1 - \lambda_2)u_1^T u_2 = 0$，故 $u_1^T u_2 = 0$。

**3. 谱分解**

由对称矩阵谱定理，存在正交矩阵 $Q$ 使 $A = Q^T \Lambda Q$。

**附：二次型的几何意义**

考虑二次型 $(x,y)\begin{pmatrix} A & B \\ B & C \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix}$，通过**对称矩阵对角化**化简为：

$$\lambda_1 x_1^2 + \lambda_2 y_2^2 = 0$$

**几何意义**：
- 若 $\lambda_1, \lambda_2$ 符号相反，为双曲线或相交直线
- 若 $\lambda_1, \lambda_2$ 同号，为椭圆（或虚椭圆）
- 面积因子与判别式 $AC - B^2$ 相关

---

## 39. 压缩映射与不动点

### 题目（Banach不动点定理）

设 $(X, \rho)$ 是完备度量空间，$T: X \to X$ 是压缩映射（即存在 $\alpha \in [0,1)$ 使 $\rho(Tx, Ty) \leq \alpha \rho(x,y)$）。证明 $T$ 存在唯一不动点。

### 解答

**唯一性**：若 $x, y$ 都是不动点，则

$$\rho(x,y) = \rho(Tx, Ty) \leq \alpha \rho(x,y)$$

因 $\alpha < 1$，得 $\rho(x,y) = 0$，即 $x = y$。

**存在性**：任取 $x_0 \in X$，定义迭代序列 $x_{n+1} = Tx_n$。

**Claim**：$\{x_n\}$ 是Cauchy列。

**证明**：对 $m > n$，

$$\rho(x_m, x_n) \leq \sum_{k=n}^{m-1} \rho(x_{k+1}, x_k) \leq \sum_{k=n}^{m-1} \alpha^k \rho(x_1, x_0) \leq \frac{\alpha^n}{1-\alpha} \rho(x_1, x_0) \to 0$$

由完备性，$x_n \to x^*$。由 $T$ 的连续性（Lipschitz蕴含连续），

$$Tx^* = T(\lim x_n) = \lim Tx_n = \lim x_{n+1} = x^*$$

---

## 40. 级数收敛性判别

### 题目（Emorkavo判别法相关）

若 $\sum_{n=1}^\infty a_n$ 收敛且 $\{na_n\}$ 单调，则 $\lim_{n\to\infty} na_n \ln n = 0$。

### 解答

由级数收敛，$a_n \to 0$，故 $na_n \to 0$（若 $na_n$ 不趋于0，则 $a_n \sim \frac{c}{n}$ 导致级数发散）。

因 $\{na_n\}$ 单调且趋于0，它是单调递减趋于0的数列。

考虑积分 $\int_2^\infty \frac{c(x)}{x}\, dx$（将离散的 $c_n = na_n$ 延拓）。由于 $\sum \frac{c_n}{n}$ 收敛，积分也收敛。

做变量替换 $t = \ln x$，则 $dx = e^t dt$，积分变为 $\int_{\ln 2}^\infty c(e^t)\, dt$。

因积分收敛且 $c(e^t)$ 单调递减趋于0，必有 $c(e^t) = o(1/t)$，即 $c_n \ln n \to 0$。

---

## 41. 整系数多项式的整数根

### 题目

设 $f(x) = \sum_{i=0}^n a_i x^i$ 是整系数多项式（$a_i \in \mathbb{Z}$）。若 $f(0)$ 和 $f(1)$ 都是奇数，证明 $f(x)$ 没有整数根。

### 解答

**关键观察**：设 $m \in \mathbb{Z}$，计算 $f(m) \bmod 2$（模2意义下）。

由条件：
1. $f(0) = a_0$ 是奇数 ⇒ $a_0 \equiv 1 \pmod{2}$
2. $f(1) = \sum_{i=0}^n a_i$ 是奇数 ⇒ $\sum_{i=0}^n a_i \equiv 1 \pmod{2}$

**模2计算**：

对任意整数 $m$，考虑两种情形：

**情形一：$m$ 是偶数**，即 $m \equiv 0 \pmod{2}$。
则 $m^i \equiv 0 \pmod{2}$（$i \ge 1$），故

$$f(m) = a_0 + a_1 m + \cdots + a_n m^n \equiv a_0 \equiv 1 \pmod{2}$$

所以 $f(m)$ 是奇数。

**情形二：$m$ 是奇数**，即 $m \equiv 1 \pmod{2}$。
则 $m^i \equiv 1 \pmod{2}$（对所有 $i$），故

$$f(m) = \sum_{i=0}^n a_i m^i \equiv \sum_{i=0}^n a_i \equiv 1 \pmod{2}$$

所以 $f(m)$ 也是奇数。

**结论**：对任意整数 $m$，$f(m)$ 都是奇数，而奇数不可能等于零，因此 $f(x)$ 没有整数根。

---

## 42. 概率级数恒等式

### 题目

设 $\{p_j\}_{j=1}^\infty$ 为一列概率（$0 \leq p_j \leq 1$），证明：

$$\sum_{i=1}^n p_i \prod_{\substack{j=1 \\ j \neq i}}^n (1-p_j) + \prod_{j=1}^n (1-p_j) = 1$$

并讨论 $n \to \infty$ 时的极限行为。

### 分析

这个恒等式有直观的概率意义：
- 第一项："恰好有一个事件发生"的概率（第$i$个事件发生，其余不发生）
- 第二项："所有事件都不发生"的概率
- 两者之和为"至多一个事件发生"的概率

### 解答

**Step 1：有限项恒等式**

对任意正整数 $n$，设 $A_1, A_2, \ldots, A_n$ 为独立事件，$P(A_j) = p_j$。

定义：
- $B_i$ = "第 $i$ 个事件发生，其余不发生"
- $C$ = "所有事件都不发生"

则：
$$P(B_i) = p_i \prod_{\substack{j=1 \\ j \neq i}}^n (1-p_j)$$

$$P(C) = \prod_{j=1}^n (1-p_j)$$

事件 $B_1, B_2, \ldots, B_n, C$ 两两互斥，且它们的并集为"至多一个事件发生"。

由于概率的完全性：

$$\sum_{i=1}^n P(B_i) + P(C) = 1$$

即：

$$\sum_{i=1}^n p_i \prod_{\substack{j=1 \\ j \neq i}}^n (1-p_j) + \prod_{j=1}^n (1-p_j) = 1$$

**Step 2：极限行为分析**

当 $n \to \infty$ 时，记：

$$S_n = \sum_{i=1}^n p_i \prod_{\substack{j=1 \\ j \neq i}}^n (1-p_j) + \prod_{j=1}^n (1-p_j)$$

由有限项时恒成立 $S_n = 1$，极限：

$$\lim_{n \to \infty} S_n = 1$$

**进一步分析**：

若 $\sum_{j=1}^\infty p_j < \infty$，则 $\prod_{j=1}^\infty (1-p_j) > 0$，此时：

$$\sum_{i=1}^\infty p_i \prod_{\substack{j=1 \\ j \neq i}}^\infty (1-p_j) + \prod_{j=1}^\infty (1-p_j) = 1$$

若 $\sum_{j=1}^\infty p_j = \infty$，则 $\prod_{j=1}^\infty (1-p_j) = 0$，此时：

$$\sum_{i=1}^\infty p_i \prod_{\substack{j=1 \\ j \neq i}}^\infty (1-p_j) = 1$$

---
## 43. 矩阵方程解空间维数

### 题目

设矩阵 $A, B$ 的极小多项式分别为 $p(x), q(x)$，且 $\gcd(p, q) = d(x)$（$d(x) \neq 1$）。试估计矩阵方程 $AX + XB = 0$ 的解空间维数的最大值，并证明。

### 分析

这是 **Sylvester 方程** $AX + XB = 0$ 的解空间维数问题。当 $A$ 和 $-B$ 有公共特征值时，解空间维数大于 0。

### 解答

**暂留**：需要补充完整证明。

关键思路：利用 Kronecker 积将方程转化为 $(I \otimes A + B^T \otimes I) \text{vec}(X) = 0$，分析系数矩阵的零空间维数。

---

## 44. 伴随矩阵的秩一表示

### 题目

设矩阵 $A$ 满足：$(1, 2, \ldots, n) A = 0$，$A (1, 2, \ldots, n)^T = 0$。证明：$A^*$（$A$ 的伴随矩阵）可表示为 $a a^T$（其中 $a \in \mathbb{R}^n$）。

### 分析

条件表明向量 $\mathbf{1} = (1, 2, \ldots, n)^T$ 同时在 $A$ 的左零空间和右零空间中，即 $\text{rank}(A) \leq n-1$。

### 解答

**暂留**：需要补充完整证明。

关键思路：当 $\text{rank}(A) = n-1$ 时，$A^*$ 是秩一矩阵，可表示为外积形式。

---

## 45. 不变子空间的正交补

### 题目

设 $T, S$ 是有限维欧氏空间 $V$ 上可交换的线性变换（$TS = ST$），$U$ 是 $T$ 的不变子空间，$W$ 是 $U$ 在 $V$ 中的正交补。若对任意 $u, v \in V$，成立 $(Tu, v) = (u, Sv)$，证明：$W$ 也是 $S$ 的不变子空间。

### 分析

条件 $(Tu, v) = (u, Sv)$ 表明 $S$ 是 $T$ 的**伴随变换**（在欧氏空间中是转置/共轭转置）。

### 解答

设 $w \in W$，需证 $Sw \in W$，即对任意 $u \in U$，$(Sw, u) = 0$。

由伴随条件：$(Sw, u) = (w, Tu)$（注意 $S$ 与 $T$ 的关系）。

因 $U$ 是 $T$ 的不变子空间，$Tu \in U$，而 $w \in W = U^\perp$，故 $(w, Tu) = 0$。

因此 $(Sw, u) = 0$ 对所有 $u \in U$ 成立，即 $Sw \in W$。

故 $W$ 是 $S$ 的不变子空间。

---

## 46. $\lambda$-矩阵的等价标准形

### 题目

求 $\lambda$-矩阵

$$\begin{pmatrix} (\lambda-a)^n & b(\lambda-a) \\ b(\lambda-a) & f(\lambda) \end{pmatrix}$$

的等价标准形（其中 $a, b$ 为给定的复数，$f(\lambda)$ 是给定的多项式）。

### 分析

利用初等变换化简 $\lambda$-矩阵，目标是得到对角形 $\text{diag}(d_1(\lambda), d_2(\lambda))$，其中 $d_1 | d_2$。

### 解答

通过 $\lambda$-矩阵的初等变换：

1. 若 $b \neq 0$，可通过行/列变换消去非对角元。
2. 利用 $(\lambda-a)^n$ 和 $f(\lambda)$ 的关系确定不变因子。

**结果**：

$$\text{diag}(1, 1,\cdots,1,(\lambda-a)^{n+2})$$

（在适当条件下，具体取决于 $f(\lambda)$ 的形式）

---

## 47. 根的对称多项式

### 题目

设 $a, b, c, d$ 为多项式 $x^4 + 2x^3 - 3x^2 + x - 1$ 的 4 个根，求以 $a^2, b^2, c^2, d^2$ 为根的首一四次多项式。

### 分析

利用**Vieta 公式**和**对称多项式基本定理**，将 $a^2, b^2, c^2, d^2$ 的初等对称多项式用 $a, b, c, d$ 的初等对称多项式表示。

### 解答

设 $e_1 = a+b+c+d$，$e_2 = ab+ac+ad+bc+bd+cd$，$e_3 = abc+abd+acd+bcd$，$e_4 = abcd$。

由 Vieta 公式：
- $e_1 = -2$
- $e_2 = -3$
- $e_3 = -1$
- $e_4 = -1$

**计算新多项式的系数**：

1. $\sum a^2 = e_1^2 - 2e_2 = 4 + 6 = 10$

2. $\sum a^2 b^2 = e_2^2 - 2e_1 e_3 + 2e_4 = 9 - 4 + (-2) = 3$

3. $\sum a^2 b^2 c^2 = e_3^2 - 2e_2 e_4 = 1 - 6 = -5$

4. $a^2 b^2 c^2 d^2 = e_4^2 = 1$

故所求多项式为：

$$x^4 - 10x^3 + 3x^2 + 5x + 1 = 0$$

---

*以上习题整理于 2026-03-09*

## 48. 矩阵秩与方程等价性

若矩阵 A, B 满足秩相等（r(A) = r(B)），则矩阵方程满足等价关系：
$$A^2 B = A \iff B^2 A = B$$

**证明思路**：体现矩阵运算中"互逆"或"对偶"的代数关系，需结合矩阵秩的性质与乘积的秩不等式证明。

---

## 49. 分块矩阵的行列式公式

对分块矩阵 $\begin{pmatrix} A & \alpha \\ B^T & a \end{pmatrix}$（其中 A 为 n×n 矩阵，α 为 n 维列向量，a 为标量，B 为 n 维列向量），其行列式满足：
$$\det\begin{pmatrix} A & \alpha \\ B^T & a \end{pmatrix} = a \cdot |A| - \alpha^T A^* B$$

其中 A* 是 A 的伴随矩阵，公式可通过行列式展开或分块矩阵初等变换推导。

---

*补充习题整理于 2026-03-26*

## 50. 含参积分的极限问题

### 原始题目

考虑含参积分 $I(x) = \int_0^{+\infty} \frac{xf(t)}{1 + x^2t^2} \, dt$（x > 0），求 $\lim_{x \to +\infty} I(x)$（假设 f(t) 连续有界，且在 t = 0 处连续）。

### 题目分析

核心步骤：
1. 令 y = xt 进行变量代换，将积分转化为更适合分析的形式
2. 利用 Weierstrass 判别法证明一致收敛性
3. 由一致收敛性与 f 的连续性，交换极限与积分

### 求解

#### 1. 变量代换

令 y = xt（即 t = y/x，dt = dy/x），积分转化为：

$$I(x) = \int_0^{+\infty} \frac{f(y/x)}{1 + y^2} \, dy$$

#### 2. 一致收敛性分析

若 f(t) 是**连续且有界**的函数（即 |f(t)| ≤ M, ∀t），则被积函数 $\frac{f(xy)}{1 + y^2}$ 满足：

$$\left| \frac{f(y/x)}{1 + y^2} \right| \leq \frac{M}{1 + y^2}$$

而 $\int_0^{+\infty} \frac{M}{1 + y^2} \, dy = M \cdot \frac{\pi}{2}$ 收敛，由 **Weierstrass 判别法**，积分 I(x) 关于 x ∈ (0, +∞)**一致收敛**。

#### 3. 极限与积分的交换

若 f(t) 在 t = 0 处**连续**，则当 x → +∞ 时，y/x → 0，故 f(y/x) → f(0)（依连续性）。结合一致收敛性，可交换**极限与积分**：

$$\lim_{x \to +\infty} I(x) = \int_0^{+\infty} \lim_{x \to +\infty} \frac{f(y/x)}{1 + y^2} \, dy = \int_0^{+\infty} \frac{f(0)}{1 + y^2} \, dy = f(0) \cdot \frac{\pi}{2}$$

---
*添加时间: 2026-04-07*

---
# 附录

## A. 常用不等式汇总

| 不等式名称 | 表达式 | 适用条件 |
|-----------|--------|---------|
| Cauchy-Schwarz | $\int fg \leq \sqrt{\int f^2} \sqrt{\int g^2}$ | $f,g \in L^2$ |
| Hardy | $\int \frac{u^2}{|x|^2} \leq 4\int |\nabla u|^2$ | $u \in C_c^1(\mathbb{R}^3)$ |
| Wirtinger | $\int f^2 \leq \int |f'|^2$ | $f$ 周期，零均值 |
| Jensen | $f(\frac{1}{b-a}\int_a^b g) \leq \frac{1}{b-a}\int_a^b f(g)$ | $f$ 凸 |
| Gronwall | $u(t) \leq a + \int_0^t b(s)u(s)ds$ | 微分不等式 |

## B. 常用公式汇总

### 斯特林公式
$$n! \sim \sqrt{2\pi n}\left(\frac{n}{e}\right)^n$$

### Wallis积分
$$I_n = \int_0^{\pi} \sin^n x\, dx = \begin{cases} \frac{(2k-1)!!}{(2k)!!} \pi, & n=2k \\ \frac{(2k)!!}{(2k+1)!!} \cdot 2, & n=2k+1 \end{cases}$$

### 高斯积分
$$\int_{-\infty}^{\infty} e^{-\pi x^2}\, dx = 1$$

### Poisson核
$$\frac{1}{2\pi} \int_0^{2\pi} \ln(1-2r\cos x + r^2)\, dx = \begin{cases} 0 & |r|<1 \\ 2\ln|r| & |r|>1 \end{cases}$$

## C. 复习计划模板

### 周计划
- [ ] 完成 5 道新题目
- [ ] 复习 3 道已标记 [x] 的题目
- [ ] 整理 1 个新的解题模式到 patterns/

### 月计划
- [ ] 完成所有 [ ] 标记的基础题目
- [ ] 重点突破 [~] 标记的难点
- [ ] 总结本月学到的 3 个核心技巧

---

> 共50题已整理（35核心题 + 15补充题）

---

# 第二部分：中科院历年真题库

> 收录 2017–2024 年中国科学院大学数学保研笔试真题。
> 与本部分第一部分中已有解答的题目存在少量重复，可相互参照。

# 中国科学院大学数学保研笔试真题集

---

## 数学与系统科学研究院 2024 年夏令营招生考试试题

**考生须知：** 本试卷满分 100 分，考试时间 120 分钟

---

### 1. (20 分)

**(1)** 设数列 $a_n > 0$ 并且 $\lim_{n \to \infty} a_n = a$，计算极限：
$$\lim_{n \to \infty} \frac{a_1 + a_2 + \cdots + a_n}{n}$$

**(2)** 设 $a > 2$，计算极限：
$$\lim_{x \to 0^+} \frac{\int_0^x e^{-t^2} dt - \sin x}{\sin^2 x - x^2}$$

**(3)** 计算极限：
$$\lim_{n \to \infty} \frac{1}{n^2} \iint_D (x + y) dxdy$$
其中 $D = \{(x,y) \mid (x-1)^2 + (y-1)^2 \leq 2, y \geq x\}$

**(4)** 设 $f(x)$ 在 $\mathbb{R}$ 上可导，$f(0) = 0$，$f'(0) = 1$，求：
$$\lim_{n \to \infty} \sum_{k=1}^{n} f\left(\frac{k}{n^2}\right)$$

---

### 2. (20 分)

**(1)** 设 $n$ 为正整数，计算积分：
$$\int_0^{\pi} \frac{\sin(2n+1)\theta}{\sin \theta} d\theta$$

**(2)** 计算二重积分 $\iint_D f(x,y) dxdy$（题目不完整）

---

### 3. (15 分)

设 $f(x)$ 在区间 $[0,1]$ 上连续可导，且 $f(0) = f(1) = 0$，$\exists \xi \in (0,1)$ 使得 $f(\xi) \neq 0$。

证明：
$$\int_0^1 |f'(x)| dx \geq 4$$

---

### 4. (10 分)

设 $A, B, C \in M_n(\mathbb{R})$ 为实数域上 $n$ 阶方阵，$[AB, C] = C$，$|C| \neq 0$ 且 $[A,C] = 0$，$[B,C] = 0$。讨论 $[A,B]$ 与 $(BA)^k$ 的关系，其中 $[X,Y] := XY - YX$。

---

### 5. (20 分)

设 $D \subset \mathbb{R}^3$ 是一个区域，$u(x)$ 是 $D$ 上的函数，$u(x)$ 二阶连续可导，且满足调和条件 $\Delta u = 0$。对任意的 $x \in D$，定义：
$$g(r) = \frac{1}{4\pi r^2} \iint_{\partial B(x,r)} u(y) d\sigma(y)$$

其中，$B(x,r)$ 表示以 $x$ 为球心、$r$ 为半径的球，$\partial B(x,r)$ 表示这个球的外表面。这里 $r$ 充分小使得 $B(x,r) \subset D$。

**(1)** 证明：$g'(r) = 0$

**(2)** 证明：$u(x) = \frac{1}{4\pi r^2} \iint_{\partial B(x,r)} u(y) d\sigma(y) = \frac{1}{\frac{4}{3}\pi r^3} \iiint_{B(x,r)} u(y) dy$

---

### 6. (20 分)

证明如下两个结论：

**(1)** 设 $f$ 是 $n$ 维欧氏空间 $V$ 上的一个正交变换，证明：$f$ 的不变子空间的正交补也是 $f$ 的不变子空间。

**(2)** 设 $A = (a_{ij}) \in M_n(\mathbb{C})$，若 $\text{tr}(A) = \sum_{i=1}^n a_{ii}$，则有 $\det(e^A) = e^{\text{tr}(A)}$。

---

## 数学与系统科学研究院 2023 年提前批招生考试试题

**考生须知：** 本试卷满分 150 分，考试时间 180 分钟

---

### 1. (20 分)

**(1)** 设 
$$f(x,y) = \begin{cases} \frac{x^2 - y^2}{x^2 + y^2}, & x^2 + y^2 \neq 0 \\ 0, & x^2 + y^2 = 0 \end{cases}$$

问等式 $\frac{\partial^2 f}{\partial x \partial y} = \frac{\partial^2 f}{\partial y \partial x}$ 是否成立？

**(2)** 设 
$$f(x,y) = \begin{cases} \frac{xy}{x^2 + y^2}, & x^2 + y^2 \neq 0 \\ 0, & x^2 + y^2 = 0 \end{cases}$$

计算 $\int_0^1 dy \int_0^1 f(x,y) dx$ 和 $\int_0^1 dx \int_0^1 f(x,y) dy$，并说明从该计算结果得出什么结论？

---

### 2. (20 分)

计算 $n+1$ 阶行列式 $D_{n+1}$：
$$D_{n+1} = \begin{vmatrix} s_0 & s_1 & s_2 & \cdots & s_{n-1} & 1 \\ s_1 & s_2 & s_3 & \cdots & s_n & x \\ s_2 & s_3 & s_4 & \cdots & s_{n+1} & x^2 \\ \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\ s_n & s_{n+1} & s_{n+2} & \cdots & s_{2n-1} & x^n \end{vmatrix}$$

其中 $s_k = x_1^k + x_2^k + \cdots + x_n^k$。

---

### 3. (20 分)

设函数 $f(x)$ 在 $[a,b]$ 上二阶可导，且 $f''(x) > 0$。证明：

**(1)** 
$$f\left(\frac{a+b}{2}\right) < \frac{1}{b-a} \int_a^b f(x) dx$$

**(2)** 若 $f(x) < 0$，$x \in [a,b]$，则 $f(x) > \frac{2}{b-a} \int_a^b f(x) dx$，$x \in [a,b]$。

---

### 4. (20 分)

设 $\alpha_1, \alpha_2, \alpha_3$ 为欧氏空间 $V$ 的一组标准正交基，$\sigma$ 是 $V$ 的一个线性变换，并且：
$$\sigma(\alpha_1) = \alpha_1 + 2\alpha_2 - \alpha_3$$
$$\sigma(\alpha_2) = -\alpha_1 + \alpha_2 - \alpha_3$$
$$\sigma(\alpha_3) = -\alpha_1 - \alpha_2 + \alpha_3$$

**(1)** 证明：$\sigma$ 是一个对称变换；

**(2)** 求 $V$ 的另一组标准正交基，使得 $\sigma$ 在这一组基下的矩阵为对角矩阵。

---

### 5. (20 分)

设函数列 $\{f_n(x)\}$ 在 $[a,b]$ 上一致收敛于 $f(x)$，$g(x)$ 在 $(-\infty, +\infty)$ 内连续。证明：
$\{g(f_n(x))\}$ 在 $[a,b]$ 上一致收敛于 $g(f(x))$。

---

### 6. (20 分)

**(1)** 设实函数 $f(x)$ 在 $[0,1]$ 上可微，并且满足条件：$f(0) = 0$，$|f'(x)| \leq K|f(x)|$，其中 $K$ 为常数。证明：$f(x) = 0$。

**(2)** 设整系数多项式 $f(x) = x^n + a_1 x^{n-1} + \cdots + a_{n-1}x + a_n$。若 $f(0)$ 和 $f(1)$ 都是奇数，证明：$f(x)$ 没有整数根。

---

### 7. (15 分)

计算积分：
$$\iiint_{Q(x)<1} e^{Q(x)} dx_1 dx_2 dx_3 dx_4$$

其中 $Q(x) = \sum_{i,j=1}^4 a_{ij} x_i x_j$ 是正定二次型。

---

### 8. (15 分)

设 $\sigma$ 是域 $K$ 上有限维线性空间 $V$ 上的一个线性变换（又称线性算子）。证明：如果 $\sigma$ 的极小多项式（又称最小多项式）$m_\sigma(\lambda) \in K[\lambda]$ 是不可约的（又称既约的），则 $K[\sigma]$ 是一个域。

---

## 数学与系统科学研究院 2023 年夏令营招生考试试题

**考生须知：** 本试卷满分 100 分，考试时间 120 分钟

---

### 1. (10 分)

**(1)** 已知 $f'(a)$ 存在，$f(a) \neq 0$，求：
$$\lim_{n \to \infty} \left(\frac{f(a + \frac{1}{n})}{f(a)}\right)^n$$

**(2)** 求不定积分 $\int \ln(x + \sqrt{1+x^2}) dx$

---

### 2. (15 分)

设 $f(x)$ 是 $[a,b]$ 上的连续函数且严格单调增加，求证：
$$\int_a^b x f(x) dx > \frac{a+b}{2} \int_a^b f(x) dx$$

---

### 3. (15 分)

设 $f(x)$ 在闭区间 $[a,b]$ 上二阶连续可导，并且 $f(a) = f(b) = 0$，证明不等式：
$$M^2 \leq \frac{(b-a)^3}{12} \int_a^b |f''(x)|^2 dx$$

其中 $M = \sup_{a \leq x \leq b} |f(x)|$。

---

### 4. (10 分)

设 $A, B$ 为 $n$ 阶实方阵，且 $AB$ 和 $BA$ 均为实对称矩阵，求证：$AB$ 和 $BA$ 相似。

---

### 5. (10 分)

设 $x, y$ 为 $n$ 阶方阵，定义 $z^1 = z$，$z^0 = [x,y] = xy - yx$，$z^{k+1} = [z^k, y]$。

证明：
$$z^k = \sum_{i=0}^k (-1)^i \binom{k}{i} y^{k-i} x y^i$$

---

### 6. (20 分)

设 $r = \sqrt{x^2 + y^2 + z^2}$，$\Delta u = \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} + \frac{\partial^2 u}{\partial z^2}$。

**(1)** (10 分) 证明如下两个等式成立：
$$\Delta r = \frac{2}{r}, \quad \Delta \ln r = \frac{1}{r^2}$$

注：这里的 $\cdot$ 表示两个向量做内积。

**(2)** (10 分) 假设 $u$ 是一个在无穷远处为零的一次连续可微函数，且使得积分 $\int_{\mathbb{R}^3} \frac{u^2}{r^2} dxdydz$ 和 $\int_{\mathbb{R}^3} |\nabla u|^2 dxdydz$ 存在。证明如下不等式成立：
$$\int_{\mathbb{R}^3} \frac{u^2}{r^2} dxdydz \leq 4 \int_{\mathbb{R}^3} |\nabla u|^2 dxdydz$$

注：$|\nabla u|^2 = \nabla u \cdot \nabla u$

---

### 7. (20 分)

证明 $\cos x$ 是超越函数。

（注：函数 $f(x)$ 为超越函数，若不存在有限个非零的数 $a_{ij}$（$i = 0,1,2,\ldots,m$；$j = 0,1,2,\ldots,n$），使得 $\forall x \in \mathbb{R}$，$\sum_{i=0}^m \sum_{j=0}^n a_{ij} x^i f^j(x) = 0$）

---

## 数学与系统科学研究院 2019 年提前批招生考试试题 1

**注：** 本试卷满分 100 分，考试时间 120 分钟

---

### 1. (20 分)

证明或反证：若存在实数域上的 $n$ 阶方阵 $A$ 满足 $A^2 + 2A + 4I = 0$ 的充要条件是 $n$ 为偶数。

---

### 2. (20 分)

设 $f$ 为定义在 $[0,1]$ 上的实值连续函数，求证：
$$\int_0^1 \int_0^1 |f(x) + f(y)| dxdy \geq \int_0^1 |f(x)| dx$$

---

### 3. (10 分)

设 $A, B$ 为 $2 \times 2$ 实矩阵，$t \in \mathbb{R}$。若 $A + tB$ 可逆，且 $(A + tB)^{-1}$ 与 $A + 5B$ 可交换，求 $A$ 与 $B$ 的关系。

---

### 4. (20 分)

设 $f(x,y,z) = e^{-\alpha(x^2 + y^2 + z^2)}$，求 $f$ 的 Fourier 变换，其定义为：
$$\hat{f}(\xi_1, \xi_2, \xi_3) = \int_{\mathbb{R}^3} f(x,y,z) e^{-2\pi i(x\xi_1 + y\xi_2 + z\xi_3)} dxdydz$$

---

### 5. (20 分)

对任何方阵 $A$ 可定义 $\sin A$ 如下：
$$\sin A = \sum_{n=0}^{\infty} \frac{(-1)^n}{(2n+1)!} A^{2n+1}$$

证明或反证：存在一个 $2$ 阶方阵 $A$ 使得 
$$\sin A = \begin{pmatrix} 1 & 2019 \\ 0 & 1 \end{pmatrix}$$

---

### 6. (10 分)

设 $a_1 = 1$，$a_{n+1} = 3a_n + [\sqrt{5} a_n]$，其中 $[a]$ 表示不大于 $a$ 的最大整数。求 $a_n$ 的通项表达式。

---

## 数学与系统科学研究院 2019 年提前批招生考试试题 2

---

### 1. (10 分)

设 $\lim_{j \to \infty} a_j = 0$，$0 < y < 1$，求：
$$\lim_{y \to 1^-} (1-y) \sum_{j=1}^{\infty} a_j y^j$$

---

### 2. (15 分)

设 $I_n = \int_0^{\frac{\pi}{2}} \sin^n x dx$（$n = 0, 1, 2, \ldots$）

**(1)** 求 $I_n$；

**(2)** 求 $\lim_{n \to \infty} n I_n^2$；

**(3)** 估计 $n!$。

---

### 3. (15 分)

设 $P$ 为从区间 $[0, \frac{\pi}{2}]$ 到 $(0, 1)$ 的单调递增连续可微函数 $p(\theta)$ 全体构成的集合，且 $p(0) = 0$，$p(\frac{\pi}{2}) = 1$。设：
$$I(p) = \int_0^{\frac{\pi}{2}} \frac{(p'(\theta))^2 + (1 - p(\theta))^2}{2} d\theta$$

**(1)** 求解极值问题 $\inf_{p \in P} I(p)$。

**(2)** 若 $I(p(\theta))$ 与 $\theta$ 无关，求 $p(\theta)$。

---

### 4. (15 分)

设 $0 < a < b < \infty$ 为实数，$K_{a,b}$ 为区间 $[a,b]$ 上满足 $\int_a^b f(t) dt = 1$，且 $af(a) = bf(b)$ 的单调递减函数全体，求：
$$\sup_{f,g \in K_{a,b}} \int_a^b \max\{f(t), g(t)\} dt$$

---

### 5. (15 分)

设 $A, B \in M_{n \times n}(\mathbb{C})$ 为 $n \times n$ 复矩阵，满足 $AB = 0$，$k$ 为正整数，请问以下关系
$$\text{tr}((A + B)^k) = \text{tr}(A^k) + \text{tr}(B^k)$$
是否一定成立？说明理由。

---

### 6. (15 分)

**(1)** 设 $S$ 为幂零矩阵，$a_0 \neq 0$，求 $(a_0 I + S)^{-1}$。

**(2)** 设 $A, B, C$ 为 $n$ 阶方阵，求：
$$\det\begin{pmatrix} A & B \\ C & D \end{pmatrix}$$

---

### 7. (15 分)

设 $A \in M_{n \times n}(\mathbb{C})$ 为 $n \times n$ 复矩阵，满足 $AA^* = A^*A$。是否一定存在多项式 $f$ 使得 $A^* = f(A)$？说明理由。

---

## 数学与系统科学研究院 2019 年夏令营招生考试试题

**注：** 本试卷满分 100 分，考试时间 120 分钟

---

### 1. (15 分)

集合 $\Omega_n = \{1, 2, \ldots, n\}$ 的一个分划是指一族非空集合 $\{B_1, B_2, \ldots, B_k\}$ 满足 $\bigcup_{i=1}^k B_i = \Omega_n$，$B_i \cap B_j = \emptyset$（$i \neq j$）。记 $T_n$ 为 $\Omega_n$ 的分划个数，例如 $T_1 = 1$（因 $\Omega_1 = \{1\}$），$T_2 = 2$（因 $\Omega_2 = \{1,2\} = \{1\} \cup \{2\}$），$T_3 = 5$，求：
$$\sum_{n=1}^{\infty} \frac{T_n}{n!}$$

---

### 2. (15 分)

设 $0 < a_k < 1$，$k = 1, 2, \ldots$，$\sum_{n=1}^{\infty} a_n = 1$。记由 $\{a_1, a_2, \ldots\}$ 的子序列和（即子级数）构成的集合为 $S$，求 $S$ 的性质。

---

### 3. (10 分)

设 $f$ 在 $[0, 2\pi]$ 上连续，$f(0) = f(2\pi)$，且 $\int_0^{2\pi} f(t) dt = 0$。探讨 $\int_0^{2\pi} |f(t)|^2 dt$ 与 $\int_0^{2\pi} |f'(t)|^2 dt$ 的关系，并解函数方程：
$$\int_0^{2\pi} |f'(t)|^2 dt = \int_0^{2\pi} |f(t)|^2 dt$$

---

### 4. (15 分)

设 $0 < a < b < \infty$ 为实数，$K_{a,b}$ 为区间 $[a,b]$ 上满足 $\int_a^b f(t) dt = 1$，且 $af(a) = bf(b)$ 的单调递减函数全体，求：
$$\sup_{f,g \in K_{a,b}} \int_a^b \max\{f(t), g(t)\} dt$$

---

### 5. (10 分)

设 $A$ 为方阵，$\text{tr}(A)$ 为迹（对角元之和）。

**(1)** 讨论以下条件：存在 $k$ 使得 $A^k = 0$。

**(2)** 讨论条件 $\text{tr}(A^k) = 0$（$k = 1, 2, \ldots, n$）。

讨论以上两个条件之间的关系。

---

### 6. (5 分)

计算：
$$\begin{vmatrix} 1 & 2019 \\ 0 & 1 \end{vmatrix}^{2019}$$

---

### 7. (10 分)

设 $A$ 为复数域上 $n$ 阶方阵，非零列向量 $x \in \mathbb{C}^n$ 满足 $Ax = \lambda x$，$\lambda \in \mathbb{C}$。设 $y \in \mathbb{C}^n$，讨论矩阵 $A$ 的特征值与矩阵 $A + xy^*$ 的特征值之间的关系。

---

### 8. (10 分)

设 $V, W$ 都是有限维线性空间，$V^*$ 为 $V$ 的对偶空间，$L(V^*, W)$ 是从 $V^*$ 到 $W$ 的线性映照全体，$B(V \times W, \mathbb{C})$ 是从 $V \times W$ 到复数域 $\mathbb{C}$ 的双线性映照全体。

讨论 $L(V^*, W)$ 与 $B(V \times W, \mathbb{C})$ 之间的关系。

---

### 9. (10 分)

设 $f(x) = \sum_{n=0}^{\infty} a_n x^n$（题目不完整）

---

## 数学与系统科学研究院 2018 年夏令营招生考试试题

**注：** 本试卷满分 100 分，考试时间 120 分钟

---

### 1. (15 分)

设 $\Omega_n$ 是含有 $n$ 个元素的集合，$\{A_1, A_2, \ldots, A_k\}$ 称为 $\Omega_n$ 的一个覆盖，如果 $\bigcup_{i=1}^k A_i = \Omega_n$，$A_i \subset \Omega_n$ 非空，$A_i \neq A_j$（$i \neq j$）。记 $C_n^k$ 为 $\Omega_n$ 的 $k$ 元覆盖个数。例如 $C_2^1 = 1$，$C_2^2 = 3$，求 $C_3^k$。

---

### 2. (10 分)

通过研究极限 $\lim_{n \to \infty} n\sin(2\pi e n!)$ 证明 $e$ 是无理数。

---

### 3. (15 分)

设 $P$ 为从区间 $[0, 1]$ 到 $(0, 1]$ 的单调递增连续可微函数 $p(\theta)$ 全体构成的集合，且 $p(0) = 0$，$p(1) = 1$。

**(1)** 求解极值问题 $\inf_{p \in P} \int_0^1 I(p(\theta)) d\theta$。

**(2)** 若 $I(p(\theta))$ 与 $\theta$ 无关，求 $p(\theta)$。

---

### 4. (15 分)

证明 $\cos x$ 是超越函数。

（注：函数 $f(x)$ 为超越函数，若不存在有限个非零的数 $a_{ij}$（$i = 0,1,2,\ldots,m$；$j = 0,1,2,\ldots,n$），使得 $\forall x \in \mathbb{R}$，$\sum_{i=0}^m \sum_{j=0}^n a_{ij} x^i f^j(x) = 0$）

---

### 5. (15 分)

设 $A, B, C \in M_{n \times n}(\mathbb{C})$ 为 $n \times n$ 复矩阵，$A^*$ 表示 $A$ 的共轭转置。

**(1)** 讨论等式 $AB = AC$ 与 $A^*AB = A^*AC$ 的关系。

**(2)** 若 $AB = AC$，$BA = B$，求 $A$ 与 $C$ 的关系。

**(3)** 讨论等式 $A^2B = BA^2$ 与 $AB = BA$ 的关系，其中 $A$ 为正定矩阵。

---

### 6. (15 分)

设 $A \in M_{n \times n}(\mathbb{C})$ 为任意 $n \times n$ 复矩阵，满足 $AA^* = A^*A$。是否一定存在多项式 $f$ 使得 $A^* = f(A)$？说明理由。

---

### 7. (15 分)

设 $A = (a_{ij})$，$B = (b_{ij}) \in M_{n \times n}$ 为 $n \times n$ 实矩阵，定义 $A \circ B = (a_{ij}b_{ij})$。判断以下论断的对错，并给出理由。

**(1)** $A \circ B$ 为正定矩阵。

**(2)** $A \circ A' \geq I$。

**(3)** $A^2 \circ B^2 \geq I$，此处正定矩阵 $A, B$ 对角线上的元素均为 $1$。

---

## 数学与系统科学研究院 2017 年提前批招生考试试题 1

**注：** 本试卷满分 100 分，考试时间 120 分钟

---

### 1. (15 分)

计算极限：

**(1)** 
$$\lim_{x \to 0^+} \frac{\int_0^x e^{-t^2} dt - \sin x}{\sin^2 x - x^2}$$

**(2)**
$$\lim_{n \to \infty} \left(\frac{1}{n+1} + \frac{1}{n+2} + \cdots + \frac{1}{n+n}\right)$$

---

### 2. (20 分)

计算积分：

**(1)** 
$$\int_0^1 (\ln x)^m dx$$
其中 $m, n$ 为自然数。

**(2)** 计算二重积分 $\iint_D \sqrt{|y - 2x^2|} dxdy$，其中 $D = \{(x,y) \mid |x| \leq 1, 0 \leq y \leq 2\}$。

---

### 3. (10 分)

设函数 $f(x)$ 在闭区间 $[a,b]$ 上二次连续可微，并且 $f(a) = f(b) = 0$，证明不等式：
$$M^2 \leq \frac{(b-a)^3}{12} \int_a^b |f''(x)|^2 dx$$

其中 $M = \sup_{a \leq x \leq b} |f(x)|$。

---

### 4. (20 分)

设 $n$ 为自然数，$A \in M_{n \times n}(\mathbb{R})$ 是一个 $n$ 阶实对称矩阵。

**(1)** 证明存在 $n$ 个实特征值 $\lambda_1 \leq \lambda_2 \leq \cdots \leq \lambda_n$ 和相应的特征向量 $\{u_1, u_2, \ldots, u_n\}$ 可以组成空间 $\mathbb{R}^n$ 的一组标准正交基。

**(2)** 对于向量 $v = (v_1, v_2, \ldots, v_n)$，定义向量范数为 $\|v\| = \sqrt{\sum_{i=1}^n v_i^2}$。对任意的向量 $v$ 和实数 $\mu$，定义 $\theta = \frac{|Av - \mu v|}{\|v\|}$。证明存在矩阵 $A$ 的一个特征值 $\lambda$ 使得如下的不等式成立：
$$|\mu - \lambda| \leq \theta$$

---

### 5. (15 分)

**(1)** 设 $A, B$ 分别是复数域上的 $k$ 阶和 $l$ 阶方阵，且它们没有共同的特征值，证明 $AX = XB$ 只有零解，其中 $X$ 为 $k \times l$ 阶矩阵。

**(2)** 设 $M_{n \times n}(\mathbb{R})$ 上的线性变换 $G$ 定义为 $G(X) = AX + XA$，这里 $X, A \in M_{n \times n}(\mathbb{R})$，$A$ 为固定矩阵且 $A$ 的特征值不是 $-A$ 的特征值，证明：$G$ 是一个可逆的线性变换。

---

### 6. (20 分)

证明如下两个结论：

**(1)** 设 $f$ 是 $n$ 维欧氏空间 $V$ 上的一个正交变换，证明：$f$ 的不变子空间的正交补也是 $f$ 的不变子空间。

**(2)** 令 $A = (a_{ij}) \in M_n(\mathbb{C})$，若 $\text{tr}(A) = \sum_{i=1}^n a_{ii}$，则有 $\det(e^A) = e^{\text{tr}(A)}$。

---

## 数学与系统科学研究院 2017 年提前批招生考试试题 2

**注：** 本试卷满分 100 分，考试时间 120 分钟

---

### 1. (20 分)

设实数域上的 $s \times n$ 矩阵 $A$ 的元素只有 $0$ 和 $1$，并且 $A$ 的每一行元素的平方和为常数 $r$，$A$ 的任意两个行向量的内积为常数 $\lambda$，且 $\lambda < r$。

**(1)** 求行列式 $\det(AA^T)$。

**(2)** 证明：$s \leq n$。

**(3)** 证明：$A$ 的特征值都是实数。

---

### 2. (20 分)

设 $A, B, C$ 为 $n$ 阶方阵，$AB = 2B$，$AC = C$。若 $\text{rank}(B) + \text{rank}(C) = n$，证明 $A$ 可对角化，并求其对角化矩阵。

---

### 3. (10 分)

设 
$$A = \begin{pmatrix} 1 & 0 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 0 \end{pmatrix}$$

**(1)** 证明：$\lim_{n \to \infty} \left(\frac{1}{n+1} + \frac{1}{n+2} + \cdots + \frac{1}{2n}\right) = \ln 2$。

**(2)** 求 $A^{2017}$。

---

### 4. (20 分)

设 $x_0 = 1$，$x_{n+1} = \frac{x_n}{2 + x_n}$，$n = 0, 1, 2, \ldots$。证明当 $n \to +\infty$ 时 $x_n$ 收敛，并求出该极限。

---

### 5. (15 分)

设 $f(x)$ 在 $[a,b]$ 上连续，且在 $(a,b)$ 上有 $7$ 个互不相同的零点。又设：
$$\int_a^b x^k f(x) dx = 0, \quad k = 0, 1, \ldots, 6$$

证明：$f(x) \equiv 0$。

---

### 6. (15 分)

设 $f$ 是 $[0,1]$ 上连续实函数，计算下列极限并证明你的结论：

**(1)** 
$$\lim_{n \to \infty} \int_0^1 x^n f(x) dx$$

**(2)**
$$\lim_{n \to \infty} n \int_0^1 x^n f(x) dx$$

---

## 数学与系统科学研究院 2017 年提前批招生考试试题 3

---

### 1. (20 分)

**(1)** 求极限：$\lim_{x \to 0} (e^x + x)^{\frac{1}{x}}$

**(2)** 求导数：$f(x) = \int_0^x \frac{dt}{\sqrt{1+t^2}} + a^x$

**(3)** 求：$\frac{d}{dy} \int_a^y \sqrt{1+x^2} dx$

**(4)** 设 $f$ 是 $[a,b]$ 上的连续单调增函数，证明：
$$\int_a^b x f(x) dx \geq \frac{a+b}{2} \int_a^b f(x) dx$$

---

### 2. (10 分)

设 
$$A = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}, \quad B = \begin{pmatrix} 3 & 0 \\ 0 & -2 \end{pmatrix}$$

求 $A + B$ 的 Jordan 标准形。

---

### 3. (题目分值未标注)

设 $A > 0$，$AC - B^2 > 0$，求平面曲线 $Ax^2 + 2Bxy + Cy^2 = 1$ 所围图形面积。

---

### 4. (20 分)

设有实二次型 $f(x_1, x_2, \ldots, x_n) = x^T A x$，其中 $A = (a_{ij})$ 是 $n$ 阶正定实对称矩阵，求证下列实二次型是负定型：
$$g(x_1, x_2, \ldots, x_n) = \begin{vmatrix} a_{11} & a_{12} & \cdots & a_{1n} & x_1 \\ a_{21} & a_{22} & \cdots & a_{2n} & x_2 \\ \vdots & \vdots & \ddots & \vdots & \vdots \\ a_{n1} & a_{n2} & \cdots & a_{nn} & x_n \\ x_1 & x_2 & \cdots & x_n & 0 \end{vmatrix}$$

---

### 5. (15 分)

设 $f(t) = \int_0^{\infty} \frac{\cos(tx)}{1+x^2} dx$

**(1)** 证明：$f(t)$ 是连续函数。

**(2)** 求极限 $\lim_{t \to \infty} f(t)$。

**(3)** 证明：$f(t)$ 在 $[0, \pi]$ 上有零点。

---

### 6. (10 分)

设 $A, B$ 是线性空间 $V$ 到 $V$ 的线性变换，$A(V) \subset B(V)$。证明：存在 $V$ 上的线性变换 $D$，使得 $A = BD$。

---

### 7. (15 分)

设正项级数 $\sum_{n=1}^{\infty} a_n$ 发散，其中 $a_n < M$。

**(1)** (7 分) 证明：$\sum_{n=1}^{\infty} \frac{a_n}{S_n}$ 发散，其中 $S_n = a_1 + a_2 + \cdots + a_n$。

**(2)** (8 分) 证明：$\sum_{n=1}^{\infty} \frac{a_n}{S_n^2}$ 收敛。

---

*文件结束*
