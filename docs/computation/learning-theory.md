# 统计学习理论

!!! note "本页来源与说明"
    本页内容正在从我自己的复习对话（与 ChatGPT/Claude，2026-05~06）中**逐主题蒸馏**而来，含 AI 生成成分，**待我本人校对**。配套精读见 [LFTP Ch4 经验风险最小化](lftp/ch4-erm.md)。

## 内容规划（路线图）

- [x] 概率工具：次高斯与集中不等式 ← 本页已开张
- [ ] 经验风险最小化与一致偏差（见 [LFTP Ch4](lftp/ch4-erm.md)）
- [ ] Rademacher 复杂度与泛化误差界
- [ ] 偏差–方差分解
- [ ] 覆盖数 / 链式法
- [ ] 一致性理论；深度学习中的泛化之谜

---

## 概率工具 · 次高斯与集中不等式

学习理论里几乎所有泛化界，都建立在"经验均值偏离期望的幅度是 $O(1/\sqrt n)$、且尾巴指数衰减"这一事实上。把这件事说精确的统一语言，就是 **次高斯（sub-Gaussian）**。

### 次高斯随机变量

称零均值随机变量 $X$ 是**次高斯的**（参数 $\sigma^2$），若其矩母函数被同方差高斯的矩母函数控制：

$$
\mathbb{E}\,e^{\lambda(X-\mathbb{E}X)} \le e^{\lambda^2\sigma^2/2},\qquad \forall \lambda\in\mathbb{R}.
$$

直觉：**尾巴不比高斯重**。由此可直接导出双边指数尾 $\mathbb{P}(|X-\mathbb{E}X|\ge t)\le 2e^{-t^2/(2\sigma^2)}$。

### 有界 ⟹ 次高斯（Hoeffding 引理）

> **结论**：任意有界随机变量都是次高斯的。若 $a\le X\le b$ 几乎必然，则中心化的 $X-\mathbb{E}X$ 次高斯，且

$$
\mathbb{E}\,e^{\lambda(X-\mathbb{E}X)} \le \exp\!\left(\frac{\lambda^2 (b-a)^2}{8}\right)\qquad(\text{Hoeffding 引理}).
$$

与定义 $e^{\lambda^2\sigma^2/2}$ 对比，可取次高斯参数 $\sigma^2=\dfrac{(b-a)^2}{4}$。

**为什么直觉上成立**：有界变量根本跑不出 $[a,b]$，尾部比高斯还轻，中心化后自然次高斯。（特例 $|X|\le M$ 时可取 $\sigma^2=M^2$。）

!!! warning "两种"次高斯"用法别混"
    一种要求**中心化后** $X-\mathbb{E}X$ 满足条件；另一种直接写 $\mathbb{E}e^{\lambda X}\le e^{C\lambda^2}$，默认 $X$ 已零均值。严谨说法：**任意有界 $X$，其中心化 $X-\mathbb{E}X$ 一定次高斯**；若 $X$ 本就零均值，则 $X$ 自己次高斯。

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
- **Bernstein 不等式**（再把方差用上、对小偏差更紧）——待续。

> **待续**：Bernstein 不等式、Rademacher 复杂度、泛化误差界，将从对应复习对话继续蒸馏补入。
