# 有限元方法：从插值到装配

这篇整理《有限元算法的零散笔记》7 页内容，并吸收《并行计算与工业软件》中“网格 $\to V_h\to Ax=b$”的线索。原笔记跨越插值、正交多项式、Sobolev 空间、Galerkin 方法、误差估计、单元映射、装配与自适应计算，下面按有限元实际工作流重排。

## 1. 先从插值开始

设 $f:[a,b]\to\mathbb R$，已知互异节点 $x_0,\ldots,x_n$ 上的值 $f(x_i)$。插值问题要求构造次数不超过 $n$ 的多项式 $p_n$，使

```math
p_n(x_i)=f(x_i),\qquad i=0,\ldots,n.
```

### 1.1 Lagrange 基函数

定义

```math
\ell_k(x)=\prod_{\substack{0\le j\le n\\j\ne k}}
\frac{x-x_j}{x_k-x_j}.
```

它满足 $\ell_k(x_i)=\delta_{ik}$，因此

```math
p_n(x)=\sum_{k=0}^{n}f(x_k)\ell_k(x).
```

这里的核心思想后来会原样出现在有限元中：用一组在节点上具有 Kronecker 性质的局部基函数表示未知函数，系数就是节点自由度。

### 1.2 插值余项与 Runge 现象

若 $f\in C^{n+1}[a,b]$，则对每个 $x$，存在 $\xi_x\in(a,b)$ 使

```math
f(x)-p_n(x)=
\frac{f^{(n+1)}(\xi_x)}{(n+1)!}
\prod_{i=0}^{n}(x-x_i).
```

增加全局多项式次数并不保证在等距节点上处处改善逼近；端点附近可能发生强烈振荡，这就是 Runge 现象。有限元常采用“网格变细 + 每个单元低阶多项式”，以局部化误差和形状变化。

### 1.3 最佳逼近与正规方程

插值要求逐点相等，而 $L^2$ 最佳逼近选择 $p\in V_n=\operatorname{span}\{\phi_0,\ldots,\phi_n\}$ 最小化

```math
\|f-p\|_{L^2(a,b)}^2.
```

令 $p=\sum_ja_j\phi_j$，一阶最优性条件给出

```math
\sum_j(\phi_j,\phi_i)a_j=(f,\phi_i),
\qquad i=0,\ldots,n.
```

这已经具有 $Ax=b$ 的形式。有限元只是把全局基函数换成由网格产生的局部基函数，并把内积推广为 PDE 对应的双线性形式。

## 2. 正交多项式与 Gauss 求积

原笔记记录了三项递推形式。对权函数 $\rho(x)>0$，可构造正交多项式

```math
\phi_{k+1}(x)=(x-\alpha_k)\phi_k(x)-\beta_k\phi_{k-1}(x),
```

其中系数由加权内积 $\langle f,g\rangle_\rho=\int_a^b f(x)g(x)\rho(x)\,dx$ 决定。

以 $n$ 个节点 $x_i$ 及权重 $w_i$ 构造 Gauss 求积：

```math
\int_a^b\rho(x)f(x)\,dx
\approx
\sum_{i=1}^{n}w_if(x_i).
```

当节点取为 $n$ 次正交多项式的零点时，该公式对次数不超过 $2n-1$ 的多项式精确。有限元装配需要反复计算单元积分；把积分映射到参考单元后，Gauss 求积可以用少量函数值高效完成积分。

## 3. Sobolev 空间与弱导数

PDE 的经典解要求导数逐点存在，但含尖角的区域、分片材料系数或低正则右端项往往不满足这种光滑性。有限元因此工作在允许弱导数的 Sobolev 空间中。

### 3.1 测试函数与分布导数

记

```math
C_c^\infty(\Omega)=
\{\varphi\in C^\infty(\Omega):\operatorname{supp}\varphi\Subset\Omega\}.
```

若 $u\in L^1_{\mathrm{loc}}(\Omega)$，并存在 $g\in L^1_{\mathrm{loc}}(\Omega)$ 使

```math
\int_\Omega u\,\partial_i\varphi\,dx
=-
\int_\Omega g\varphi\,dx,
\qquad \forall\varphi\in C_c^\infty(\Omega),
```

则称 $g$ 是 $u$ 的第 $i$ 个弱导数。

### 3.2 Sobolev 空间

```math
W^{m,p}(\Omega)=
\{u\in L^p(\Omega):D^\alpha u\in L^p(\Omega),\ |\alpha|\le m\}.
```

当 $p=2$ 时写作 $H^m(\Omega)$。$H_0^1(\Omega)$ 是 $C_c^\infty(\Omega)$ 在 $H^1$ 范数下的闭包，可理解为具有零 Dirichlet 边界迹的函数空间。

## 4. 从强形式到弱形式

考虑 Poisson 问题

```math
\begin{cases}
-\Delta u=f, & x\in\Omega,\\
u=0, & x\in\partial\Omega.
\end{cases}
```

取 $v\in H_0^1(\Omega)$，乘以 $v$ 并分部积分：

```math
\int_\Omega\nabla u\cdot\nabla v\,dx
=
\int_\Omega fv\,dx.
```

定义

```math
a(u,v)=\int_\Omega\nabla u\cdot\nabla v\,dx,
\qquad
\ell(v)=\int_\Omega fv\,dx.
```

弱问题为：求 $u\in V=H_0^1(\Omega)$，使

```math
a(u,v)=\ell(v),\qquad \forall v\in V.
```

弱形式只要求一阶弱导数存在，比强形式所需的二阶导数要求低；同时边界条件自然地进入函数空间或边界积分。

## 5. Galerkin 离散与矩阵系统

在网格 $\mathcal T_h$ 上选有限元空间 $V_h\subset V$，Galerkin 方法求 $u_h\in V_h$，使

```math
a(u_h,v_h)=\ell(v_h),
\qquad \forall v_h\in V_h.
```

若 $V_h=\operatorname{span}\{\phi_1,\ldots,\phi_N\}$，令 $u_h=\sum_jU_j\phi_j$，便得到

```math
AU=b,
\qquad
A_{ij}=\int_\Omega\nabla\phi_j\cdot\nabla\phi_i\,dx,
\qquad
b_i=\int_\Omega f\phi_i\,dx.
```

线性 $P_1$ 三角形单元的基函数只在与对应节点相邻的少量单元上非零。因此，若节点 $i$ 与 $j$ 不共享单元，$A_{ij}=0$。有限元矩阵天然是稀疏矩阵。

## 6. Galerkin 正交性与 Céa 引理

连续问题减去离散问题得到

```math
a(u-u_h,v_h)=0,
\qquad \forall v_h\in V_h.
```

这称为 Galerkin 正交性。若双线性形式满足连续性与强制性：

```math
|a(w,v)|\le M\|w\|_V\|v\|_V,
\qquad
a(v,v)\ge \alpha\|v\|_V^2,
```

则 Céa 引理给出

```math
\|u-u_h\|_V
\le
\frac{M}{\alpha}
\inf_{v_h\in V_h}\|u-v_h\|_V.
```

这说明有限元误差由两部分决定：

1. 离散空间 $V_h$ 能把真解逼近得多好；
2. 连续问题本身的稳定常数 $M/\alpha$。

当 $a$ 对称且能量范数定义为 $\|v\|_a=\sqrt{a(v,v)}$ 时，$u_h$ 是 $u$ 在 $V_h$ 中的能量正交投影，因而具有最佳逼近性质。

## 7. 插值误差与有限元误差

令 $I_hu$ 为节点插值。对形状规则的网格和足够光滑的 $u$，线性元通常满足

```math
\|u-I_hu\|_{L^2(\Omega)}\le Ch^2|u|_{H^2(\Omega)},
```

```math
\|u-I_hu\|_{H^1(\Omega)}\le Ch|u|_{H^2(\Omega)}.
```

将 $v_h=I_hu$ 代入 Céa 引理，便得到 Poisson 问题的典型能量误差估计

```math
\|u-u_h\|_{H^1(\Omega)}\le Ch|u|_{H^2(\Omega)}.
```

若再使用对偶问题（Aubin-Nitsche 技巧），并满足椭圆正则性，可把 $L^2$ 误差提高到 $O(h^2)$。

## 8. 参考单元与仿射映射

实际网格含许多三角形或四面体。程序通常只在一个参考单元 $\widehat K$ 上定义基函数，再通过映射搬到实际单元 $K$。

对仿射映射

```math
x=F_K(\widehat x)=B_K\widehat x+b_K,
```

若 $\widehat u=u\circ F_K$，则梯度满足

```math
\nabla_xu=B_K^{-T}\nabla_{\widehat x}\widehat u,
```

积分换元为

```math
\int_K g(x)\,dx
=
\int_{\widehat K}g(F_K(\widehat x))|\det B_K|\,d\widehat x.
```

这解释了原笔记中 $B_K^{-1}$、$\det(B_K)$ 与 Sobolev 半范数缩放同时出现的原因。网格若含极扁、极尖单元，$B_K$ 的条件会变差，误差常数和代数系统条件数也会恶化。因此误差估计通常要求网格族具有形状规则性。

## 9. 局部装配

对每个单元 $K$，先形成局部刚度矩阵和载荷向量：

```math
A_{ij}^{(K)}=
\int_K\nabla\phi_j^{(K)}\cdot\nabla\phi_i^{(K)}\,dx,
\qquad
b_i^{(K)}=
\int_Kf\phi_i^{(K)}\,dx.
```

再通过局部自由度到全局自由度的映射，把它们累加到 $A$ 和 $b$ 中。这一步称为装配。

不同单元的局部积分可以并行计算，但若两个单元向同一个全局矩阵位置写入，就会发生写冲突。工程实现常用图着色、线程私有缓冲、原子累加或分区装配来解决。

## 10. 求解器、预条件与自适应网格

装配后得到的大型稀疏系统往往不能直接用稠密消元。对对称正定问题，常用共轭梯度法；更一般问题可用 GMRES。预条件器 $M^{-1}$ 的目的不是改变解，而是让

```math
M^{-1}AU=M^{-1}b
```

更容易迭代求解。多重网格通过在不同尺度上传递误差，对椭圆问题尤其有效。

自适应有限元循环通常写作

```text
SOLVE -> ESTIMATE -> MARK -> REFINE
```

- **SOLVE**：在当前网格上求解；
- **ESTIMATE**：用残量等指标估计各单元误差；
- **MARK**：标记误差贡献大的单元；
- **REFINE**：局部加密并保持网格协调。

这比无差别地细化全域更节省自由度。原笔记还提到“打网格在高维中困难”：随着维数增加，规则网格自由度大致按每维节点数的幂增长，形成维数灾难。低秩张量、Monte Carlo、神经网络试探空间等路线另见[逆问题与高维计算札记](inverse-high-dimensional.md)。

## 11. 一维小例子：两单元 Poisson 方程

在 $[0,1]$ 上解

```math
-u''=1,
\qquad u(0)=u(1)=0.
```

取节点 $0,\frac12,1$，只有中间节点是未知自由度。对应帽函数

```math
\phi_1(x)=
\begin{cases}
2x, & 0\le x\le \frac12,\\
2(1-x), & \frac12\le x\le1.
\end{cases}
```

于是

```math
A_{11}=\int_0^1(\phi_1')^2\,dx=4,
\qquad
b_1=\int_0^1\phi_1\,dx=\frac12.
```

线性系统只有一个方程 $4U_1=\frac12$，故 $U_1=\frac18$。精确解为 $u(x)=\frac12x(1-x)$，在 $x=\frac12$ 处也等于 $\frac18$。这个例子完整展示了“网格 - 基函数 - 积分 - 矩阵 - 系数 - 近似解”的链条。

## 12. 与其他页面的边界

- CAD 曲线、曲面与 CAE 前处理见[CAD、CAE 与工业软件计算链](cad-cae-pipeline.md)。
- 装配和稀疏求解在硬件上的执行见[并行计算基础](parallel-computing.md)。
- 有限差分、CFL 条件和其他 PDE 数值方法仍保留在[数值微分方程](../num-pde.md)中。
