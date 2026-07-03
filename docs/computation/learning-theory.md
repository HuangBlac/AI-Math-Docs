# 统计学习理论

!!! note "本页来源与说明"
    本页内容正在从我自己的复习对话（与 ChatGPT/Claude，2026-05~06）中**逐主题蒸馏**而来，含 AI 生成成分，**待我本人校对**。配套精读见 [LFTP Ch4 经验风险最小化](lftp/ch4-erm.md)。

## 内容规划（路线图）

- [x] 概率工具：次高斯与集中不等式 ← 本页已开张
- [x] Bayes 最优预测器（条件均值 / Bayes 分类器 / 超额风险）
- [x] 分布间的差异：KL 散度 vs 范数
- [ ] 经验风险最小化与一致偏差（见 [LFTP Ch4](lftp/ch4-erm.md)）
- [ ] Rademacher 复杂度与泛化误差界
- [ ] 偏差–方差分解
- [x] 覆盖数 + Bernstein 条件 → 快速率 $\log\mathcal{N}/n$ ← 本页已补
- [ ] Rademacher 复杂度 / 链式法
- [ ] 一致性理论；深度学习中的泛化之谜

---

## 概率工具 · 次高斯与集中不等式

学习理论里几乎所有泛化界，都建立在"经验均值偏离期望的幅度是 $O(1/\sqrt n)$、且尾巴指数衰减"这一事实上。把这件事说精确的统一语言，就是 **次高斯（sub-Gaussian）**。

### 次高斯随机变量

称零均值随机变量 $X$ 是**次高斯的**（参数 $\sigma^2$），若其矩母函数被同方差高斯的矩母函数控制：

$$
\mathbb{E}\,e^{\lambda(X-\mathbb{E}\,X)} \le e^{\lambda^2\sigma^2/2},\qquad \forall \lambda\in\mathbb{R}.
$$

直觉：**尾巴不比高斯重**。由此可直接导出双边指数尾 $\mathbb{P}\,(|X-\mathbb{E}\,X|\ge t)\le 2e^{-t^2/(2\sigma^2)}$。

### 有界 ⟹ 次高斯（Hoeffding 引理）

> **结论**：任意有界随机变量都是次高斯的。若 $a\le X\le b$ 几乎必然，则中心化的 $X-\mathbb{E}\,X$ 次高斯，且

$$
\mathbb{E}\,e^{\lambda(X-\mathbb{E}\,X)} \le \exp\!\left(\frac{\lambda^2 (b-a)^2}{8}\right)\qquad(\text{Hoeffding 引理}).
$$

与定义 $e^{\lambda^2\sigma^2/2}$ 对比，可取次高斯参数 $\sigma^2=\dfrac{(b-a)^2}{4}$。

**为什么直觉上成立**：有界变量根本跑不出 $[a,b]$，尾部比高斯还轻，中心化后自然次高斯。（特例 $|X|\le M$ 时可取 $\sigma^2=M^2$。）

!!! warning "两种"次高斯"用法别混"
    一种要求**中心化后** $X-\mathbb{E}\,X$ 满足条件；另一种直接写 $\mathbb{E}\,e^{\lambda X}\le e^{C\lambda^2}$，默认 $X$ 已零均值。严谨说法：**任意有界 $X$，其中心化 $X-\mathbb{E}\,X$ 一定次高斯**；若 $X$ 本就零均值，则 $X$ 自己次高斯。

### 证明心法：log-MGF + 指数倾斜

Hoeffding 引理的证法是研究 **log-矩母函数** $\psi(s)=\log\mathbb{E}\,e^{sX}$，目标 $\psi(s)\le \dfrac{s^2(b-a)^2}{8}$。取 log 后导数结构很好：

$$
\psi'(s)=\frac{\mathbb{E}[Xe^{sX}]}{\mathbb{E}[e^{sX}]},\qquad
\psi''(s)=\frac{\mathbb{E}[X^2e^{sX}]}{\mathbb{E}[e^{sX}]}-\left(\frac{\mathbb{E}[Xe^{sX}]}{\mathbb{E}[e^{sX}]}\right)^2 .
$$

**关键观察**：$\psi''(s)$ 恰是某个新测度 $Q$ 下 $X$ 的方差。这个 $Q$ 由**指数倾斜（exponential tilting / Esscher 变换）**给出：

$$
dQ = \frac{e^{sX}}{\mathbb{E}[e^{sX}]}\,dP.
$$

它把原测度按权重 $e^{sX}/\mathbb{E}[e^{sX}]$（总积分为 1）重新加权——$s>0$ 时偏向 $X$ 大的地方，$s<0$ 时偏向小的地方。**不是改变随机变量本身，而是改变看待它的概率权重**。于是在 $Q$ 下 $\mathbb{E}_Q[f(X)]=\dfrac{\mathbb{E}[f(X)e^{sX}]}{\mathbb{E}[e^{sX}]}$，故 $\psi''(s)=\mathrm{var}_Q(X)$。因为 $X\in[a,b]$，任何测度下方差 $\le \left(\dfrac{b-a}{2}\right)^2$，所以 $\psi''(s)\le \dfrac{(b-a)^2}{4}$；配上 $\psi(0)=\psi'(0)=0$ 积分两次即得结论。

### 在学习理论里的位置

次高斯 + Hoeffding 引理是上层一切集中不等式的地基：

- **Hoeffding 不等式**（有界 i.i.d. 均值的指数尾）——把单变量的次高斯性对独立和相加；
- **McDiarmid 不等式**（有界差分函数的集中）——见 [LFTP Ch4 的完整鞅证明](lftp/ch4-erm.md)，它正是用条件版 Hoeffding 引理逐步剥矩母函数得到的；
- **Bernstein 不等式**（再把方差用上、对小偏差更紧）——见下节的快速率应用。

---

## 估计误差的快速率 · Bernstein 条件 + 覆盖数

!!! note "来源"
    整理自我对一页讲义放缩过程的复盘（原题为手写讲义图，已据推导复述）。承接 [LFTP Ch4](lftp/ch4-erm.md) 的覆盖数一节。

[LFTP Ch4](lftp/ch4-erm.md) 用覆盖数把无限类的一致偏差控住，得到的是**慢速率** $\sqrt{\log\mathcal{N}/n}$。但若损失再满足一个 **Bernstein 条件（间隔条件）**——方差被超额风险控制——速率能提升到 $\log\mathcal{N}/n$（快一个平方）。

**目标**：控制统计误差 $\mathcal{E}_{sta}=\mathbb{E}\big[\sup_{f\in\mathcal{F}}\tfrac1n\sum_i G(f,Z_i)\big]$，其中超额损失 $g(f,z)=\ell(f,z)-\ell(f^*,z)$，并令 $G(f,z)=\mathbb{E}[g(f,Z)]-2g(f,z)$。

**① 覆盖数：无限类 → 有限网。** 取 $\|\cdot\|_\infty$ 下的 $\delta$-网 $\mathcal{C}=\{\tilde f_1,\dots,\tilde f_{\mathcal{N}}\}$。损失 $\lambda$-Lipschitz $\Rightarrow |g(f,z)-g(\tilde f,z)|\le\lambda\delta$，从而 $|G(f,z)-G(\tilde f,z)|\le 3\lambda\delta$，于是 sup 转嫁给最近代表，代价 $3\lambda\delta$：

$$
\mathbb{P}\big[\max_{f\in\mathcal{F}}\tfrac1n\textstyle\sum_i G(f,Z_i)>t\big]\le \mathbb{P}\big[\max_{\tilde f\in\mathcal{C}}\tfrac1n\textstyle\sum_i G(\tilde f,Z_i)>t-3\lambda\delta\big].
$$

**② 固定 $\tilde f$，中心化。** 由 $G(\tilde f,Z_i)=\mathbb{E}[g]-2g_i$ 整理，要控制的是零均值和 $\tfrac1n\sum_i X_i$，其中 $X_i=\mathbb{E}[g]-g_i$，阈值 $u=\tfrac t2+\tfrac12\mathbb{E}[g]$。

**③ Bernstein 条件（关键）。** 有界性给 $|X_i|\le b=4\lambda B$；间隔条件 $c\|\tilde f-f^*\|^2\le\mathbb{E}[g]$ 配 Lipschitz 给

$$
\sigma^2=\mathrm{Var}(g)\le \mathbb{E}[g^2]\le \lambda^2\,\mathbb{E}\|\tilde f-f^*\|^2\le \frac{\lambda^2}{c}\,\mathbb{E}[g].
$$

**方差被期望（超额风险）控制** —— 这是快速率的全部秘密。

**④ Bernstein 不等式。** $\displaystyle\mathbb{P}\big[\tfrac1n\sum_i X_i>u\big]\le \exp\!\Big(-\frac{nu^2}{2(\sigma^2+bu)}\Big).$

**⑤ 二次指数 → 线性指数。** 因 $\sigma^2\lesssim \tfrac{\lambda^2}{c}u$，分母 $2(\sigma^2+bu)\le Cu$ 被线性化，于是 $\tfrac{nu^2}{2(\sigma^2+bu)}\ge\tfrac{nu}{C}$，配 $u\ge t/2$：

$$
\mathbb{P}\big[\tfrac1n\textstyle\sum_i G(\tilde f,Z_i)>t\big]\le \exp\!\Big(-\frac{nt}{16\lambda B+4\lambda^2/c}\Big),\qquad C:=16\lambda B+\tfrac{4\lambda^2}{c}.
$$

**指数从 $e^{-nt^2}$ 型变成 $e^{-nt}$ 型** —— 这一步就是把 $\sqrt{\ }$ 速率换成线性速率。

**⑥ Union bound + 尾积分。** 对 $\mathcal{C}$ 并集得 $\mathbb{P}[\cdot>t]\le \mathcal{N}\exp(-n(t-3\lambda\delta)/C)$。用 $\mathbb{E}[Z]\le a+\int_a^\infty\mathbb{P}[Z>t]\,dt$，取 $a=3\lambda\delta+\tfrac{C\log\mathcal{N}}{n}$、$\delta=1/n$，积分项恰化为 $C/n$，得

$$
\boxed{\ \mathcal{E}_{sta}\le \frac{(16\lambda B+4\lambda^2/c)(\log\mathcal{N}+1)+3\lambda}{n}\ }\qquad\Longrightarrow\qquad \mathcal{E}_{sta}\lesssim \frac{\log\mathcal{N}}{n}.
$$

**一句话**：$\text{统计误差}\approx\dfrac{\text{模型复杂度}\ (\log\mathcal{N})}{\text{样本量}\ n}$。能拿到 $1/n$（而非 $1/\sqrt n$）全靠 Bernstein 条件 $\mathrm{Var}(g)\lesssim\mathbb{E}[g]$ 把方差与超额风险绑定。

---

## Bayes 最优预测器：理论最优 $f^*$ 长什么样

ERM 想逼近的理论最优是 $f^*=\arg\min_f \mathcal{L}\,(f)$，$\mathcal{L}\,(f)=\mathbb{E}_{(X,Y)\sim P}[\ell(f(X),Y)]$。**关键技巧**：总体风险按塔式法则拆成逐点条件风险

$$
\mathcal{L}\,(f)=\mathbb{E}_X\big[\,\mathbb{E}[\ell(f(x),Y)\mid X=x]\,\big],
$$

当 $\mathcal{F}$ 足够大（含所有可测函数）时，最小化整体积分 $\iff$ 对每个 $x$ 逐点最优化：

$$
f^*(x)=\arg\min_{a}\ \mathbb{E}[\ell(a,Y)\mid X=x].
$$

最优预测随损失而变：

| 损失 $\ell(a,y)$ | 最优 $f^*(x)$ | 名称 |
|---|---|---|
| 平方 $\tfrac12(a-y)^2$ | $\mathbb{E}[Y\mid X=x]$ | 条件均值 |
| 绝对值 $\lvert a-y\rvert$ | 条件中位数 | |
| 0-1 $\mathbf{1}_{a\neq y}$ | $\mathbf{1}[\eta(x)\ge\tfrac12],\ \eta(x)=\mathbb{P}\,(Y{=}1\mid x)$ | Bayes 分类器 |

**平方损失的证明**（配方）：令 $m(x)=\mathbb{E}[Y\mid x]$，则

$$
\mathbb{E}[(a-Y)^2\mid x]=(a-m(x))^2+\underbrace{\mathbb{E}[(Y-m(x))^2\mid x]}_{\text{与 }a\text{ 无关}},
$$

故 $a=m(x)$ 时最小。**0-1 损失**：预测 1 的风险是 $1-\eta(x)$、预测 0 的风险是 $\eta(x)$，比大小即得 Bayes 分类器。

!!! note "$f^*$ 不一定是"真实函数""
    仅当 $Y=f_0(X)+\varepsilon$ 且 $\mathbb{E}[\varepsilon\mid X]=0$ 时 $f^*=f_0$；否则 $f^*$ 只是该损失下的最优预测。分类里更没有"真标签函数"——同一 $x$ 下 $Y$ 本就随机。衡量学到的 $\hat f$ 差多少，用**超额风险** $\mathcal{E}\,(\hat f)=\mathcal{L}\,(\hat f)-\mathcal{L}\,(f^*)$。

## 分布间的差异：为何用 KL 散度而非范数

> **一句话**：范数把概率分布当**函数**比几何距离；KL 把它当**信息源**比编码/似然代价。

可以对密度构造范数（$\|p-q\|_1$ 对应 total variation，$\|p-q\|_2$ 等），但：

- **概率分布集不是线性空间**：$p+q$ 积分为 2、$p-q$ 可为负，都不再是密度。它更像凸集。
- **KL 来自"用错分布编码的额外代价"**：$D_{\mathrm{KL}}(P\|Q)=\int p\log\tfrac{p}{q}$。
- **最大似然 $\equiv$ 最小化 KL**：$D_{\mathrm{KL}}(P_{\mathrm{data}}\|Q_\theta)=\mathbb{E}[\log p_{\mathrm{data}}]-\mathbb{E}[\log q_\theta]$，首项与 $\theta$ 无关，故 $\min_\theta \mathrm{KL}\iff \max_\theta \mathbb{E}_{P_{\mathrm{data}}}[\log q_\theta]$。这是范数没有的统计意义。
- **对致命错误敏感**：$p(x)>0$ 而 $q(x)=0$ 时 $D_{\mathrm{KL}}=+\infty$；KL 关心比值 $p/q$ 而非绝对差 $p-q$。
- **非对称是特性**：$D_{\mathrm{KL}}(P\|Q)$（forward，mode-covering）vs $D_{\mathrm{KL}}(Q\|P)$（reverse，mode-seeking）——变分推断/生成模型常据此选向。
- $D_{\mathrm{KL}}(P\|Q)=0\iff P=Q$（密度意义下几乎处处相等）。

其它分布距离各有所长：**TV**（与 $L^1$ 相关）、**Wasserstein**（最优传输）、**Hellinger**（更像几何距离）、**MMD**（核嵌入）。统计推断/最大似然天然对应 KL；几何比较、测度收敛则用范数/度量。

> **待续**：Rademacher 复杂度、泛化误差界、偏差–方差分解，将从对应复习对话继续蒸馏补入。
> **关联（凸优化，归 [optimization](optimization.md)）**：LASSO 次梯度、软阈值算子 $S_\lambda$、proximal gradient/ISTA、$\ell_\infty$ 范数次梯度、下半连续/闭函数/下水平集——来自同批复习对话，待整合到优化页。
