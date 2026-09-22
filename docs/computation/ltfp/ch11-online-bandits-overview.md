# Ch11 从在线学习到多臂赌博机（概览）

> 状态：`note_unverified`。本页整合三份无文字层手写稿：`《Ch11概览.pdf》`（2 页，导入于 2026-09-20 至 2026-09-21）、`《Ch11.1.1-Ch11.1.3.pdf》`（4 页，导入于 2026-09-22）与 `《Ch11.2 零阶凸优化.pdf》`（7 页，导入于 2026-09-22）。材料均未说明学习日期。现有正文覆盖 §11.1.1–11.1.3 的投影 SGD、强凸速率与镜像下降草稿，以及 §11.2.1–11.2.2 的高斯平滑和收敛界；这些内容仍未逐条核验，也不等于已掌握。

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

## 2. 零阶凸优化

零阶方法只查询函数值，不直接获得梯度。若允许沿每个坐标方向各查询一次，一个自然的有限差分估计是

```math
\widehat{F}'(\theta)
=\sum_{i=1}^d
\frac{F(\theta+\delta e_i)-F(\theta)}{\delta}e_i.
```

当 $F$ 的梯度是 $L$-Lipschitz 时，各坐标的差分误差至多为 $L\delta/2$，因此

```math
\|\widehat{F}'(\theta)-F'(\theta)\|_2^2
\le \frac{dL^2\delta^2}{4}.
```

这一方案每步需要 $d+1$ 次函数查询。为了把查询次数降到与维数无关，原稿改为随机选取方向 $z_t$，并考虑带噪声的函数值差：

```math
\theta_t=\theta_{t-1}
-\gamma\frac{F(\theta_{t-1}+\delta z_t)-F(\theta_{t-1})+\varepsilon_t}{\delta}z_t,
\qquad
\mathbb E[\varepsilon_t^2]=2\sigma^2.
```

若使用带符号的坐标方向，需要取 $z_t\in\{\pm\sqrt d\,e_i\}$ 才有 $\mathbb E[z_tz_t^\top]=I$；后续推导则使用 $z_t\sim\mathcal N(0,I)$。原稿在这两种方向之间切换时省略了部分尺度说明，这里按推导所需条件补齐记号。

### 2.1 高斯平滑与无偏估计

定义高斯平滑后的目标

```math
F_\delta(\theta)
=\mathbb E_{z\sim\mathcal N(0,I)}F(\theta+\delta z).
```

原稿在 Lemma 11.2 中利用高斯分部积分，写出

```math
\mathbb E_z\left[
\frac{F(\theta+\delta z)-F(\theta)}{\delta}z
\right]
=\nabla F_\delta(\theta).
```

因此随机差分不是原目标梯度 $\nabla F(\theta)$ 的精确无偏估计，而是平滑目标梯度 $\nabla F_\delta(\theta)$ 的无偏估计。$\delta$ 越小，平滑偏差越小；但噪声项的二阶矩含有 $2\sigma^2d/\delta^2$，会随 $\delta\to0$ 爆炸。这是后续参数选择必须平衡的两部分。

### 2.2 光滑情形：偏差、二阶矩与 Proposition 11.4

若 $F$ 凸且 $L$-smooth，高斯平滑满足

```math
0\le F_\delta(\theta)-F(\theta)
\le \frac{L\delta^2d}{2}.
```

对无噪声随机差分

```math
g(\theta,z)=\frac{F(\theta+\delta z)-F(\theta)}{\delta}z,
```

原稿利用高斯矩界得到

```math
\mathbb E\|g(\theta,z)\|_2^2
\le \frac{15}{2}L^2\delta^2d^3
+6d\|\nabla F(\theta)\|_2^2.
```

这里用到的是 $\mathbb E\|z\|_2^6=d(d+2)(d+4)\le15d^3$ 等上界；不能把中间的矩阵不等式改写成对所有维数都成立的等式。

令 $\bar\theta_t=t^{-1}\sum_{s=0}^{t-1}\theta_s$。原稿页 4–5 记录了 Proposition 11.4 的递推与望远镜求和：若 $\gamma\le1/(24dL)$，则

```math
\mathbb E[F(\bar\theta_t)]-F(\theta^*)
\le \frac{\|\theta_0-\theta^*\|_2^2}{\gamma t}
+2L\delta^2d^2
+\frac{4d\gamma\sigma^2}{\delta^2}.
```

无噪声时可取 $\gamma=1/(24dL)$ 并让 $\delta$ 尽量小，得到 $O(d/t)$ 的界。存在函数值噪声时，固定步长会留下由偏差和噪声共同决定的误差底；若针对时域取 $\gamma\asymp t^{-2/3}/(dL)$ 并同步平衡 $\delta$，原稿记录的量级为 $O(dt^{-1/3})$。这些是草稿中的推导路线，尚未逐行签认。

### 2.3 非光滑情形：Lemma 11.3 与未完成的 Proposition 11.5

当 $F$ 只是 $B$-Lipschitz 时，仍以 $F_\delta$ 代替 $F$。原稿明确记录 Lemma 11.3：$F_\delta$ 仍是 $B$-Lipschitz，并且是 $(B\sqrt d/\delta)$-smooth；同时

```math
|F_\delta(\theta)-F(\theta)|
\le B\delta\sqrt d.
```

将同一个随机差分估计代入标准随机梯度递推，原稿最终停在

```math
\mathbb E[F(\bar\theta_t)]-F(\theta^*)
\le \frac{\|\theta_0-\theta^*\|_2^2}{2\gamma t}
+4\gamma B^2d^2
+\frac{\gamma\sigma^2d}{\delta^2}
+2B\delta\sqrt d.
```

这对应 Proposition 11.5 的核心上界，但原稿没有明确写出命题标题，也没有继续完成无噪声/有噪声时的参数优化。因此本页只保留到该不等式，不用教材后续内容替原稿补完速率。

## 3. 多臂赌博机：只有问题定义

原稿第二页写道：有若干台收益未知的机器，每轮只选择一台，并且只能看到所选机器的收益。这正是多臂赌博机中的部分反馈设置，核心困难是探索与利用之间的权衡。

> **编号校正：** 原稿页眉写成 “Ch12.3.3 Multi-Bandits”。按锁定教材目录和正文，该内容属于 Ch11 §11.3 “Multiarmed Bandits”；§11.3.3 是更具体的 “Optimism in the Face of Uncertainty”。本页没有写 UCB、置信区间、探索后承诺算法或遗憾界，因此不计为 §11.3.3 的完整覆盖。

## 4. 当前完成边界

- §11.1：已有问题设置、平均遗憾与三类方法的概览；新增材料记录 §11.1.1–11.1.3 的主要推导，但均为 `note_unverified`。
- §11.1.1：投影 SGD 的递推、Abel 求和和 $O(B\operatorname{diam}(C)/\sqrt t)$ 界已有记录；命题 11.1 在原稿中属于隐含对应。
- §11.1.2：命题 11.2 的标题、步长、强凸递推和 $B^2(1+\log t)/(2\mu t)$ 界已有记录；未逐条核验。
- §11.1.3：镜像映射、Bregman 更新和单步不等式已有记录；最终望远镜求和未完成。
- §11.2.1：高斯平滑、Lemma 11.2、光滑情形的偏差和二阶矩界，以及 Proposition 11.4 的收敛界与速率主线已有记录；尺度记号经过整理，结论仍未逐条核验。
- §11.2.2：Lemma 11.3 和 Proposition 11.5 的核心上界已有记录；原稿停在上界，没有完成参数优化与最终速率。
- §11.3：只有 bandit 的一句定义；算法和分析均未写。
- 原稿没有 Exercise 的作答记录；明确写出的编号包括 Proposition 11.2、Proposition 11.4、Lemma 11.2 与 Lemma 11.3，其余按正文对应关系记录。
