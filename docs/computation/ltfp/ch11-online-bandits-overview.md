# Ch11 从在线学习到多臂赌博机（概览）

> 状态：`note_unverified`。本页整合两份无文字层手写稿：`《Ch11概览.pdf》`（2 页，导入于 2026-09-20 至 2026-09-21）与 `《Ch11.1.1-Ch11.1.3.pdf》`（4 页，导入于 2026-09-22）。两份材料均未说明学习日期。新增材料展开了 §11.1.1–11.1.3 的投影 SGD、强凸速率和镜像下降草稿；这些内容仍未逐条核验，也不等于已掌握。

## 1. 从随机优化转向在线决策

原稿先对比 Ch5 的随机梯度下降与在线学习。传统随机优化常考察一次训练结束后的期望次优性

```math
\mathbb E[F(\theta_T)]-\inf_\theta F(\theta),
```

而在线场景中，决策、信息收集和损失发生在同一序列里。在第 $t$ 轮，算法依据过去信息选出 $\theta_{t-1}$，承受 $F_t(\theta_{t-1})$，随后获得反馈并更新。相对于一个事后固定决策的平均遗憾可写为

```math
\overline R_T
=\frac1T\sum_{t=1}^T F_t(\theta_{t-1})
-\inf_{\theta\in\mathcal C}\frac1T\sum_{t=1}^T F_t(\theta).
```

原稿列出的分析路线是：

- 一般凸函数：在有界凸域和有界（次）梯度条件下使用投影梯度法；
- 强凸函数：利用额外曲率，把平均遗憾改善到 $O(\log T/T)$ 量级；
- 镜像下降：用非欧几里得几何适配约束集合。

页末只写了 “online-to-batch conversion” 标题，没有给出随机抽取/平均迭代点、独立测试样本或期望风险之间的转换证明。

### 1.1 §11.1 的设置（新增材料）

新增 PDF 第 1 页把 §11.1 的对象补充为：一列凸函数 $F_s:\mathbb R^d\to\mathbb R$、约束集 $C\subseteq\mathbb R^d$、初始点 $\theta_0\in C$，以及由这些对象产生的序列 $(\theta_s)_{s\ge1}$。在第 $s$ 轮，算法在 $\theta_{s-1}$ 处接收 $F_s$ 的次梯度信息。原稿指出直接使用精确次梯度的计算代价可能很高，因此改用满足条件无偏性的随机估计量：

```math
\mathbb E[g_s\mid\mathcal F_{s-1}]
=F_s'(\theta_{s-1}).
```

这里将原稿中写得像 $F_{s-1}$ 的条件信息记号整理为过滤族 $\mathcal F_{s-1}$。第 1 页还留下了 `oblivious adversary` 和 `adaptive adversary` 两个空标题，没有写定义或比较；不据教材内容替原稿补写这两段。

### 1.1.1 凸情形：投影 SGD

新增材料第 2 页从投影递推开始：

```math
\theta_s=\Pi_C(\theta_{s-1}-\gamma_s g_s),
```

其中 $\gamma_s>0$，$\Pi_C$ 是到 $C$ 的正交投影。原稿采用梯度平方有界条件 $\|g_s\|_2^2\le B^2$，并在页 2–3 写出了对任意 $\theta\in C$ 的距离递推：

```math
\begin{aligned}
\|\theta_s-\theta\|_2^2
&\le \|\theta_{s-1}-\theta\|_2^2
-2\gamma_s g_s^\top(\theta_{s-1}-\theta)+\gamma_s^2B^2,\\
\mathbb E\bigl[\|\theta_s-\theta\|_2^2\mid\mathcal F_{s-1}\bigr]
&\le \|\theta_{s-1}-\theta\|_2^2
-2\gamma_s\bigl(F_s(\theta_{s-1})-F_s(\theta)\bigr)
+\gamma_s^2B^2.
\end{aligned}
```

整理原稿的下一步，令 $\delta_s=\mathbb E\|\theta_s-\theta\|_2^2$，对 $s=1,\ldots,t$ 求和并对递减步长使用 Abel 求和，可得到：

```math
\begin{aligned}
&\frac1t\sum_{s=1}^t\mathbb E\bigl[F_s(\theta_{s-1})\bigr]
-\frac1t\sum_{s=1}^tF_s(\theta)\\
&\qquad\le \frac{\operatorname{diam}(C)^2}{2t\gamma_t}
+\frac{B^2}{2t}\sum_{s=1}^t\gamma_s.
\end{aligned}
```

原稿随后取 $\gamma_s=\operatorname{diam}(C)/(B\sqrt{s})$，落到与锁定教材命题 11.1 一致的速率：

```math
\frac1t\sum_{s=1}^t\mathbb E\bigl[F_s(\theta_{s-1})\bigr]
-\inf_{\theta\in C}\frac1t\sum_{s=1}^tF_s(\theta)
\le \frac{3B\operatorname{diam}(C)}{2\sqrt t}.
```

这里使用了有界直径；因此教材命题中的 $C$ 是紧凸集。原稿页 2–3 已写出主要证明链和最终常数，但没有单独写出“命题 11.1”标题，故在覆盖表中记为相关结论的隐含记录，而不是已核验的正式命题证明。

### 1.1.2 强凸情形

第 3 页明确写出 `Prop 11.2 Online learning with strongly convex`，并记录了“向目标函数加入 $\mu/2\|\theta\|_2^2$”以及步长

```math
\gamma_s=\frac1{\mu s}.
```

原稿的距离递推在强凸不等式下变为带曲率项的形式；按原稿已写出的望远镜求和，整理后的核心单步界是

```math
\mathbb E\bigl[F_s(\theta_{s-1})-F_s(\theta)\bigr]
\le \frac{\mu(s-1)}2\mathbb E\|\theta_{s-1}-\theta\|_2^2
-\frac{\mu s}2\mathbb E\|\theta_s-\theta\|_2^2
+\frac{B^2}{2\mu s}.
```

求和后，原稿给出的结论与教材式（11.6）一致：

```math
\frac1t\sum_{s=1}^t\mathbb E\bigl[F_s(\theta_{s-1})\bigr]
-\inf_{\theta\in C}\frac1t\sum_{s=1}^tF_s(\theta)
\le \frac{B^2(1+\log t)}{2\mu t}.
```

原稿保留了完整的“强凸项—步长—调和级数”主线，但没有说明无噪声/自适应对手等扩展，也没有单独核验每个条件；本段状态仍为 `note_unverified`。

### 1.1.3 在线镜像下降

第 4 页转向镜像下降。原稿写出更新式和 Bregman 散度：

```math
\theta_t=\mathop{\arg\min}_{\theta\in C}
\left\{g_t^\top(\theta-\theta_{t-1})
+\frac1\gamma D_\Phi(\theta,\theta_{t-1})\right\},
```

```math
D_\Phi(\theta,\eta)
=\Phi(\theta)-\Phi(\eta)-\nabla\Phi(\eta)^\top(\theta-\eta).
```

当 $\Phi(\theta)=\frac12\|\theta\|_2^2$ 时，Bregman 散度退化为欧氏距离平方的一半，更新恢复为投影梯度下降（常数因子可吸收到步长中）。原稿还用一维函数

```math
\Phi(x)=x\log x-x
```

提示指数型更新 $x_{t+1}=x_t\exp(-\eta g_t)$；这只是例子，没有展开单纯形上的归一化步骤。

原稿先写出目标速率

```math
\frac1t\sum_{s=1}^t\mathbb E\bigl[F_s(\theta_{s-1})-F_s(\theta)\bigr]
\le \frac{D_\Phi(\theta,\theta_0)}{\gamma t}
+\frac{B^2\gamma}{2\mu},
```

随后利用更新的最优性条件和 $\Phi$ 的 $\mu$-强凸性，推到关键单步不等式：

```math
D_\Phi(\theta,\theta_t)-D_\Phi(\theta,\theta_{t-1})
\le \frac{\gamma^2\|g_t\|_*^2}{2\mu}
-\gamma g_t^\top(\theta_{t-1}-\theta).
```

第 4 页停在这一步，没有完成条件期望、望远镜求和与最终界之间的完整连接。因而这里只记录“镜像映射—Bregman 更新—单步界”的部分推导，不把最终速率当作原稿已经证明的结论。

## 2. 零阶凸优化中的随机方向

原稿在 “Ch11.2 固定凸函数 $F$，随机选一个方向” 下写出差分估计

```math
g=\frac{F(\theta+\delta z)-F(\theta)}{\delta}\,z,
\qquad
F_\delta(\theta)=\mathbb E_z F(\theta+\delta z).
```

这记录了用函数值替代梯度的核心想法，但原稿没有说明 $z$ 的分布、维度归一化以及 $g$ 对哪个平滑目标无偏。因而这里只保留为估计器草式；不能从该页直接断言 $\mathbb E[g]=\nabla F(\theta)$ 或 $\nabla F_\delta(\theta)$。

## 3. 多臂赌博机：只有问题定义

原稿第二页写道：有若干台收益未知的机器，每轮只选择一台，并且只能看到所选机器的收益。这正是多臂赌博机中的部分反馈设置，核心困难是探索与利用之间的权衡。

> **编号校正：** 原稿页眉写成 “Ch12.3.3 Multi-Bandits”。按锁定教材目录和正文，该内容属于 Ch11 §11.3 “Multiarmed Bandits”；§11.3.3 是更具体的 “Optimism in the Face of Uncertainty”。本页没有写 UCB、置信区间、探索后承诺算法或遗憾界，因此不计为 §11.3.3 的完整覆盖。

## 4. 当前完成边界

- §11.1：已有问题设置、平均遗憾与三类方法的概览；新增材料记录 §11.1.1–11.1.3 的主要推导，但均为 `note_unverified`。
- §11.1.1：投影 SGD 的递推、Abel 求和和 $O(B\operatorname{diam}(C)/\sqrt t)$ 界已有记录；命题 11.1 在原稿中属于隐含对应。
- §11.1.2：命题 11.2 的标题、步长、强凸递推和 $B^2(1+\log t)/(2\mu t)$ 界已有记录；未逐条核验。
- §11.1.3：镜像映射、Bregman 更新和单步不等式已有记录；最终望远镜求和未完成。
- §11.2：有单个随机方向差分式；关键分布与尺度条件未写。
- §11.3：只有 bandit 的一句定义；算法和分析均未写。
- 原稿没有 Exercise 的作答记录；除页 3 的命题 11.2 外，没有明确写出 Proposition 编号。
