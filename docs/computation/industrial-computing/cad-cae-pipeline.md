# CAD、CAE 与工业软件计算链

这部分整理《并行计算与工业软件》前两页中重复出现的 CAD/CAE 笔记，并补足曲线表示与数值仿真之间的联系。

## 1. CAD 中的边界表示

手写笔记首先记录了 **B-rep（Boundary Representation，边界表示）**。它不直接用体内所有点描述实体，而是用顶点、边、面及其拓扑关系围成一个实体。

一个 CAD 模型因此同时包含：

- **几何信息**：点的位置、曲线和曲面的参数方程；
- **拓扑信息**：哪些边属于哪个面、哪些面围成一个壳、壳是否闭合；
- **容差信息**：数值计算中两个理论上重合的点或边允许多大偏差。

布尔并、交、差并不只是集合运算。软件还需要计算曲面交线、切割原有面片、更新拓扑关系，并处理浮点误差造成的微小裂缝。因此，笔记中的“求交、求并”实际上是几何算法与鲁棒数值计算的结合。

## 2. Bézier 曲线

$n$ 次 Bernstein 基函数为

```math
B_{i,n}(u)=\binom{n}{i}u^i(1-u)^{n-i},
\qquad i=0,\ldots,n,quad u\in[0,1].
```

控制点为 $P_0,\ldots,P_n$ 时，Bézier 曲线写成

```math
C(u)=\sum_{i=0}^{n}P_iB_{i,n}(u).
```

这些基函数满足非负性与单位分解：

```math
B_{i,n}(u)\ge 0,
\qquad
\sum_{i=0}^{n}B_{i,n}(u)=1.
```

所以 $C(u)$ 是控制点的凸组合，曲线位于控制多边形的凸包内。端点还满足 $C(0)=P_0$、$C(1)=P_n$。这让设计者可以直观地移动控制点来修改形状。

Bézier 曲线的局限是**全局影响**：移动一个控制点通常会影响整条曲线。高次数曲线还会带来数值稳定性和形状控制上的困难，这正是 B-spline 出现的背景。

## 3. B-spline 与局部支撑

给定非降节点序列 $u_0\le \cdots\le u_m$，零次 B-spline 基函数定义为

```math
N_{i,0}(u)=
\begin{cases}
1, & u_i\le u<u_{i+1},\\
0, & \text{otherwise}.
\end{cases}
```

高次基函数由 Cox-de Boor 递推得到：

```math
N_{i,p}(u)=
\frac{u-u_i}{u_{i+p}-u_i}N_{i,p-1}(u)
+
\frac{u_{i+p+1}-u}{u_{i+p+1}-u_{i+1}}N_{i+1,p-1}(u),
```

其中分母为零的项按零处理。曲线为

```math
C(u)=\sum_i P_iN_{i,p}(u).
```

与单段 Bézier 曲线相比，B-spline 的关键优势是**局部支撑**：$N_{i,p}$ 只在区间 $[u_i,u_{i+p+1})$ 上非零。移动 $P_i$ 只影响这一小段参数区间，因此更适合复杂工业曲线的局部修改。

## 4. 有理 B-spline 与 NURBS

原笔记记录了带权的有理形式：

```math
C(u)=
\frac{\sum_i w_iP_iN_{i,p}(u)}
{\sum_i w_iN_{i,p}(u)}.
```

把新的有理基函数记为

```math
R_{i,p}(u)=
\frac{w_iN_{i,p}(u)}{\sum_jw_jN_{j,p}(u)},
```

便有 $C(u)=\sum_iP_iR_{i,p}(u)$。这就是 NURBS（Non-Uniform Rational B-Spline）的基本形式。

权重 $w_i$ 控制曲线被控制点 $P_i$“吸引”的程度。有理形式能精确表示圆锥曲线，因此圆、椭圆和自由曲面可以放在同一套表示框架内。“Non-Uniform”表示节点间距不必均匀，使局部参数化更加灵活。

## 5. 从 CAD 到 CAE

原笔记用“打网格、做计算、转化为 $Ax=b$”概括 CAE。展开后可写成：

```math
\widetilde\Omega
\longrightarrow \mathcal M_h
\longrightarrow V_h
\longrightarrow (A,b)
\longrightarrow x
\longrightarrow u_h.
```

各符号的含义是：

1. $\widetilde\Omega$：CAD 提供的近似几何域；
2. $\mathcal M_h$：在几何域上生成的网格；
3. $V_h$：由网格和基函数构成的有限维试探空间；
4. $(A,b)$：离散后得到的矩阵和右端项；
5. $x$：基函数系数；
6. $u_h$：由系数重建的数值解。

以抽象变分问题为例，连续问题是：求 $u\in V$，使

```math
a(u,v)=\ell(v),\qquad \forall v\in V.
```

选取有限维子空间 $V_h=\operatorname{span}\{\phi_1,\ldots,\phi_N\}$，令

```math
u_h=\sum_{j=1}^{N}x_j\phi_j.
```

分别取 $v_h=\phi_i$，便得到

```math
\sum_{j=1}^{N}a(\phi_j,\phi_i)x_j=\ell(\phi_i),
```

也就是

```math
Ax=b,
\qquad
A_{ij}=a(\phi_j,\phi_i),
\qquad
b_i=\ell(\phi_i).
```

这解释了为什么工业仿真最终会落到大型稀疏线性方程组上。矩阵 $A$ 的条件数 $\kappa(A)$ 会影响迭代收敛速度和舍入误差放大程度；网格越细，未知量越多，条件数通常也会恶化，因此需要预条件与并行求解。

## 6. 几何误差不能被忽略

CAD 到 CAE 之间存在一个容易漏掉的误差来源：计算域本身可能已经是对真实几何 $\Omega$ 的近似。总误差可以粗略理解为

```math
\text{total error}
\approx
\text{geometry error}
+\text{discretization error}
+\text{algebraic solver error}
+\text{roundoff error}.
```

如果几何清理、网格质量或边界标记有问题，即使线性方程组被求得很精确，最终物理解仍可能不可靠。这也是工业软件中“前处理”往往占据大量工作的原因。

## 7. 与后续笔记的衔接

- 网格、弱形式、装配和误差估计见[有限元方法：从插值到装配](finite-element-method.md)。
- $Ax=b$ 的数据访问、矩阵乘法和多核/GPU 执行见[并行计算基础](parallel-computing.md)。
