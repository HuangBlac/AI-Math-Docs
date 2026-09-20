# Ch12 过参数化模型（概览）

> 状态：`note_unverified`。由《Ch12 过参数化模型（概览）.pdf》6 页无文字层手写稿整理；学习日期未说明，导入于 2026-09-20 开始、2026-09-21 完成。原稿覆盖 §12.1–12.3 的问题意识、均值场主线和矩阵分解起步，多个证明只写到提问或中间式。

## 1. 三条主线

原稿把过参数化理解为参数足以完美拟合训练数据的情形，并提出：既然可选的零训练误差解很多，为什么梯度方法得到的解仍可能泛化？随后列出三条分析主线。

### 1.1 隐式偏好

当最小化问题有多个全局极小点时，初始化、参数化和优化动力学会选择其中一个。原稿用 Bregman 投影概括这一选择：

```math
\theta_\infty
\in\operatorname*{argmin}_{\theta\in\Theta^\star}
D_\Phi(\theta,\theta_0),
```

其中 $\Theta^\star$ 是极小点集合。该式适用于原稿所指的镜像流分析，并不是任意梯度算法都自动满足的无条件结论。锁定教材 §12.1 还强调：所选极小点并不必然最有利于泛化；隐式偏好依赖参数化、初始化、步长与算法。

### 1.2 双下降

原稿记录的现象是：随着模型规模增加，测试误差可能先下降，在插值阈值附近因方差放大而上升，进入过参数化区后又下降。随机特征模型可展示完整曲线；Gaussian 输入的线性回归能明确看到 $d\approx n$ 附近的风险爆炸，但这一简单模型本身不提供欠参数区的完整 U 形。

这部分只有现象描述，没有抄写 §12.2 的精确风险公式或假设。

### 1.3 非凸参数化下的全局收敛

原稿提出疑问：神经网络目标非凸，为什么仍能讨论全局收敛？随后转向两类极限或重参数化：

- 单隐层网络的无限宽均值场极限；
- 线性网络到半正定矩阵优化的重参数化。

原稿同时写到 NTK，但没有展开 §12.4 的 lazy regime，也没有比较均值场与 NTK 的缩放、特征学习或适用条件。

## 2. 从有限神经元到概率测度

对单隐层网络，把每个神经元的参数合并为 $v_j=(\eta_j,w_j,b_j)$，并记

```math
\Psi(v_j):x\longmapsto \eta_j\sigma(w_j^\top x+b_j).
```

有限宽预测函数写成经验平均

```math
h_{\mu_m}
=\frac1m\sum_{j=1}^m\Psi(v_j)
=\int_{\mathcal V}\Psi(v)\,d\mu_m(v),
\qquad
\mu_m=\frac1m\sum_{j=1}^m\delta_{v_j}.
```

原稿的求和指标和归一化符号有混用；这里依锁定教材 §12.3.1 统一为宽度 $m$。放开“$m$ 个 Dirac 质量的平均”这一限制后，可在概率测度 $\mu\in\mathcal P(\mathcal V)$ 上研究

```math
F(\mu)=R\!\left(\int_{\mathcal V}\Psi(v)\,d\mu(v)\right).
```

如果 $R$ 对预测函数是凸的，由于 $\mu\mapsto\int\Psi\,d\mu$ 线性，$F$ 对 $\mu$ 是凸泛函。原稿在此提出“最优测度能否取得”的问题，没有给出紧性、下半连续性或存在性证明。

## 3. 粒子梯度流与 Wasserstein 梯度流

令 $V=(v_1,\ldots,v_m)$，

```math
G(V)=R\!\left(\frac1m\sum_{j=1}^m\Psi(v_j)\right).
```

原稿记录带宽度缩放的梯度下降及其连续时间极限：

```math
V_{k+1}=V_k-\gamma_k m\nabla G(V_k),
\qquad
\dot V(t)=-m\nabla G(V(t)).
```

对测度定义平均势

```math
J(v\mid\mu)
=\left\langle
\Psi(v),
R'\!\left(\int\Psi(w)\,d\mu(w)\right)
\right\rangle,
```

则每个粒子的运动为 $\dot v_j=-\nabla_vJ(v_j\mid\mu)$，聚合测度满足连续性方程

```math
\partial_t\mu_t(v)
=\operatorname{div}\!\bigl(\mu_t(v)\nabla_vJ(v\mid\mu_t)\bigr).
```

原稿还写出 Wasserstein 近端形式。将手写分母中难辨的符号依教材整理为时间步长 $\tau$：

```math
\mu_{t+\tau}
\in\operatorname*{argmin}_{\nu\in\mathcal P(\mathcal V)}
\left\{
F(\nu)+\frac1{2\tau}W_2^2(\mu_t,\nu)
\right\}.
```

## 4. Proposition 12.1 与 12.2 的记录程度

### Proposition 12.1：有限粒子到 PDE

原稿记录：在 $R$、$\Psi$ 满足教材所列可微、Lipschitz 等条件，初始粒子位于紧集，且初始经验测度 $\mu_{0,m}$ 弱收敛到 $\mu_0$ 时，有限粒子流对应的 $\mu_{t,m}$ 弱收敛到由 $\mu_0$ 初始化的连续性方程解 $\mu_t$。

这里只写了命题结论和“有限粒子的运动逼近 PDE”；没有证明解的存在唯一性或收敛。

### Proposition 12.2：条件性的全局最优结论

原稿记录教材的非正式结论：若初始分布的支撑覆盖所有方向，$\Psi$ 正二次齐次，并且 Wasserstein 梯度流确实弱收敛到某个分布，那么该极限只能是 $F$ 的全局最优解。

原稿随后尝试用凸性与混合测度写反证，但没有建立“流的极限”所需的驻点条件，也没有完成从方向导数到矛盾的步骤。**原始完成状态：证明未完成。** 此处不把该草算续写成完整证明；同时保留教材本身的限制：命题并未保证流一定收敛，也没有给出有限宽度或运行时间的定量界。

## 5. §12.3.2：线性网络与 PSD 矩阵

原稿最后一页考虑

```math
f(x)=UV^\top x,
\qquad
\min_{U,V}G(UV^\top).
```

令

```math
W=\begin{pmatrix}U\\V\end{pmatrix},
\qquad
WW^\top=
\begin{pmatrix}
UU^\top&UV^\top\\
VU^\top&VV^\top
\end{pmatrix},
```

则 $UV^\top$ 是 PSD 矩阵 $WW^\top$ 的一个块。依教材把目标改写为 $F(W)=G(WW^\top)$ 后，对扰动 $\Delta$ 有

```math
(W+\Delta)(W+\Delta)^\top
=WW^\top+\Delta W^\top+W\Delta^\top+o(\|\Delta\|),
```

并得到

```math
\nabla_WF(W)=2G'(WW^\top)W,
\qquad
\dot W=-\frac12\nabla_WF(W)=-G'(WW^\top)W.
```

原稿在此停止。它没有继续推导 $M=WW^\top$ 的动力学、秩保持、PSD 约束下的最优性条件或 §12.3.3 的全局收敛论证。

## 6. 当前完成边界

- §12.1：有隐式偏好和 Bregman 选择的概念式；没有最小范数或对角线性网络的完整推导。
- §12.2：有双下降现象解释；没有风险公式与证明。
- §12.3.1：均值场、粒子流、PDE 与两个 Proposition 有记录；Proposition 12.2 的证明未完成。
- §12.3.2：矩阵重参数化和梯度式已写；后续全局收敛未写。
- §12.4：只提到 NTK 名称，没有形成笔记覆盖。
- 原稿没有 Exercise 的明确作答记录。
