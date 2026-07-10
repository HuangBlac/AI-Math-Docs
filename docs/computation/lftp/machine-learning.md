# 机器学习

## 监督学习的期望损失与最优性推导

### 监督学习的基本设定

- 输入空间：\( x \in \mathbb{R}^d \)（高维，\( d \gg 1 \)）；输出空间：\( y \in \mathbb{R}^k \)；
- 样本：\( (X_i, Y_i) \)（\( i=1,2,\dots,m \)），来自**联合分布 \( p(x,y) \)**；
- 目标：确定函数 \( f: \mathbb{R}^d \to \mathbb{R}^k \)，使对输入 \( x \)，输出 \( f(x) \) 尽可能接近真实标签 \( y \)。

### 损失函数与期望损失

- **损失函数**：衡量预测值与真实值的差异，记为 \( \ell: y \times y \to \mathbb{R} \)（如分类任务中，\( \ell(\hat{y}, y) = 0 \) 当且仅当 \( \hat{y} = y \)，否则为正）；
- **期望损失**：函数 \( f \) 的整体性能，定义为
  \[
  L(f) = \mathbb{E}_{(X,Y) \sim p} \left[ \ell(f(X), Y) \right]
  \]
  （对所有样本的损失取期望，反映泛化性能）。

### 最优函数的存在性与最优性

定义**条件期望下的最优函数**：
\[
f^*(x) = \arg\min_{a \in \mathbb{R}^k} \mathbb{E}\left[ \ell(a, Y) \,\big|\, X = x \right]
\]
（对每个输入 \( x \)，选择使"给定 \( X=x \) 时 \( Y \) 的条件损失期望最小"的 \( a \) 作为 \( f^*(x) \)）。

**最优性证明**：对任意函数 \( f \)，有
\[
L(f) \geq L(f^*)
\]
推导：利用期望的塔式性质（重期望公式），
\[
\begin{align*}
L(f) &= \mathbb{E}_X \left[ \mathbb{E}_Y \left[ \ell(f(X), Y) \,\big|\, X \right] \right] \\
&\geq \mathbb{E}_X \left[ \min_{a} \mathbb{E}_Y \left[ \ell(a, Y) \,\big|\, X \right] \right] \\
&= \mathbb{E}_X \left[ \mathbb{E}_Y \left[ \ell(f^*(X), Y) \,\big|\, X \right] \right] = L(f^*)
\end{align*}
\]
（对每个 \( X=x \)，内层期望在 \( a=f^*(x) \) 时取到最小值，故整体期望满足不等式）。

---

## 监督学习与非参数估计的核心框架

### 监督学习的基础设定

- **分布建模**：将输入 \( X \) 与输出 \( Y \) 的关系建模为 \( \mathcal{X} \times \mathcal{Y} \) 上的**联合分布 \( \mathbb{P} \)**，即 \( (X,Y) \sim \mathbb{P} \)。
- **模型假设**：
  - 参数模型：假设 \( \mathbb{P} \in \{\mathbb{P}_\theta: \theta \in \Theta\} \)（\( \Theta \subset \mathbb{R}^d \) 为参数空间）；
  - 非参数模型：不预设分布的参数形式，更具一般性。

### 风险最小化与目标函数

- **损失函数**：选择 \( \ell: \mathcal{Y} \times \mathcal{Y} \to \mathbb{R} \)，衡量预测值与真实值的差异（如回归用平方损失 \( \ell(a,y) = \frac{1}{2}(a - y)^2 \)，分类用指示损失 \( \ell(a,y) = \mathbb{1}_{a \neq y} \)）。
- **总体风险**：目标是最小化**期望损失**（泛化风险）：
  \[
  f^* = \arg\min_{\text{可测 } f} \mathcal{L}(f) = \mathbb{E}_{(X,Y) \sim \mathbb{P}} \left[ \ell(f(X), Y) \right]
  \]
- **任务特例**：
  - 回归：\( \mathcal{Y} = \mathbb{R} \)，\( f^*(x) = \mathbb{E}[Y \mid X = x] \)（条件期望为最优预测）；
  - 分类：\( \mathcal{Y} = [K] = \{1,\dots,K\} \)，\( f^*(x) = \arg\max_{k \in [K]} \mathbb{P}(Y = k \mid X = x) \)（后验概率最大类为最优类别）。

### 经验风险最小化（ERM）

给定训练数据 \( (X_1,Y_1),\dots,(X_n,Y_n) \stackrel{\text{iid}}{\sim} \mathbb{P} \)，定义**经验风险**：
\[
\hat{\mathcal{L}}(f) = \frac{1}{n} \sum_{i=1}^n \ell(f(X_i), Y_i)
\]
ERM 是找函数 \( \hat{f} \in \mathcal{F} \)（假设空间）最小化经验风险：
\[
\hat{f} = \arg\min_{f \in \mathcal{F}} \hat{\mathcal{L}}(f)
\]
（例：平方损失+线性假设空间时，ERM 等价于最小二乘法）。

### 非参数估计的误差分解

- **问题设定**：从数据 \( Z_1,\dots,Z_n \stackrel{\text{iid}}{\sim} \mu_Z \) 估计 \( f^* \)，通过 ERM 选 \( \hat{f} \in \mathcal{F} \)，再用求解器 \( \mathcal{A}(\tau) \) 输出近似解 \( f_{\mathcal{A}(\tau)} \)（满足 \( \hat{\mathcal{L}}(f_{\mathcal{A}(\tau)}) \leq \hat{\mathcal{L}}(\hat{f}) + \tau \)）。
- **Excess Risk 分解**：目标是约束 \( \mathcal{E}(f_{\mathcal{A}(\tau)}) = \mathcal{L}(f_{\mathcal{A}(\tau)}) - \mathcal{L}(f^*) \)，分解为三部分：
  - \( \varepsilon_{\text{sta}} \)：**统计误差**（经验风险与总体风险的偏差）；
  - \( \varepsilon_{\text{app}} \)：**逼近误差**（假设空间 \( \mathcal{F} \) 对 \( f^* \) 的近似能力）；
  - \( \varepsilon_{\text{opt}} \)：**优化误差**（求解器与 ERM 最优解的偏差）。

具体分解式：
\[
\mathcal{L}(f_{\mathcal{A}(\tau)}) - \mathcal{L}(f^*) = \underbrace{[\mathcal{L}(f_{\mathcal{A}(\tau)}) - \hat{\mathcal{L}}(f_{\mathcal{A}(\tau)})]}_{\text{统计误差}} + \underbrace{[\hat{\mathcal{L}}(f_{\mathcal{A}(\tau)}) - \hat{\mathcal{L}}(\hat{f})]}_{\text{优化误差}} + \underbrace{[\hat{\mathcal{L}}(\hat{f}) - \mathcal{L}(\hat{f})]}_{\text{统计误差}} + \underbrace{[\mathcal{L}(\hat{f}) - \mathcal{L}(f^*)]}_{\text{逼近误差}}
\]

---

## 压缩感知与微分方程数值解

### 压缩感知的优化模型

考虑**压缩感知**问题：在观测 \( y = \Psi x + \varepsilon \)（\( \Psi \) 为感知矩阵，\( \varepsilon \) 为噪声）下，最小化稀疏性度量 \( \|x\|_1 \)，即
\[
\min \|x\|_1 \quad \text{约束} \quad y = \Psi x + \varepsilon
\]
引入**正则化项**（平衡稀疏性与拟合度），转化为无约束优化：
\[
\min \|x\|_1 + \lambda \|y - \Psi x\|_2^2
\]
（\( \lambda > 0 \) 为正则化参数）。

**求解思路**：构造拉格朗日函数
\[
\mathcal{L}(x, \lambda) = \|x\|_1 + \lambda^T (y - \Psi x)
\]
并通过**对偶问题**或梯度类方法（如ISTA/FISTA）求解。



## 次高斯分布（Sub-Gaussian Distribution）

### 1. 次高斯分布的定义与尾部估计

**次高斯分布**（sub-Gaussian）的核心是**矩生成函数（MGF）的指数上界**：若随机变量 X 满足存在 σ² > 0，使得对所有 s ∈ ℝ，

$$\mathbb{E}(e^{sX}) \leq \exp\left(\frac{\sigma^2 s^2}{2}\right)$$

则称 X 服从参数为 σ² 的次高斯分布，记为 X ~ sub-G(σ²)。

**尾部估计**：由 Markov 不等式（P(X > t) ≤ P(e^{sX} > e^{st}) ≤ e^{-st} E(e^{sX})），结合 MGF 的上界，取最优 s 可得：

$$P(X > t) \leq \exp\left(-\frac{t^2}{2\sigma^2}\right)$$

同理对双侧尾部 P(|X| > t)，可得 P(|X| > t) ≤ 2exp(-t²/(2σ²))，体现 "次高斯分布尾部指数衰减" 的性质。

### 2. 次高斯分布的线性不变性

若 X ~ sub-G(σ²)，则对任意向量 u，线性组合 u^T X 仍服从次高斯分布：

$$u^T X \sim \text{sub-G}(\sigma^2 \|u\|_2^2)$$

（体现次高斯性在 "线性变换下保持" 的特点，是高维概率中处理随机向量的关键性质）。

### 3. Hoeffding 引理：有界随机变量的次高斯性

对**有界随机变量** X ∈ [a, b]，定义矩生成函数的对数 ψ(s) = log E(e^{sX})，则：

- 一阶导数：ψ'(s) = E(e^{sX}) / E(Xe^{sX}) = E_α(X)（其中 dα = e^{sX} dP / E(e^{sX}) 是 "倾斜测度"）；

- 二阶导数：ψ''(s) = Var_α(X)（倾斜测度下的方差），且由 X 有界 [a, b]，得方差上界：

  $$\text{Var}_\alpha(X) \leq \frac{(b-a)^2}{4}$$

- 因此，ψ(s) 作为凸函数，满足**上界估计**：

  $$\psi(s) \leq \frac{(b-a)^2 s^2}{4}$$

  即 E(e^{sX}) ≤ exp((b-a)²s²/4)，故有界随机变量是次高斯分布（参数 σ² = (b-a)²/4）。

---
*添加时间: 2026-04-07*

---

## 次高斯随机变量的最大值与覆盖定理

### 1. 最大值的期望与大偏差（次高斯情形）

设 Z = max_{1≤i≤N} X_i，其中 X_i 是次高斯随机变量（满足 E[e^{sX_i}] ≤ exp(σ_i² s²/2)），则：

#### 期望估计（MGF 技巧）

由 Jensen 不等式和 MGF（矩生成函数），

$$\mathbb{E}[Z] = \frac{1}{s} \mathbb{E}[\log e^{sZ}] \leq \frac{1}{s} \log \mathbb{E}[e^{sZ}]$$

再由 "最大值的 MGF ≤ 各变量 MGF 之和"（E[e^{sZ}] = E[max_i e^{sX_i}] ≤ ∑_i E[e^{sX_i}]），结合次高斯 MGF 的上界，得：

$$\mathbb{E}[Z] \leq \frac{1}{s} \log N + \frac{1}{2s} \sum \sigma_i^2 s$$

取最优 s = √(2 log N) / σ（假设 σ_i = σ），化简得**期望上界**：

$$\mathbb{E}[Z] \leq \sigma\sqrt{2\log N}$$

#### 大偏差界

由 Union 界（联合界），

$$P(Z > t) = P(\max_i X_i > t) \leq \sum_i P(X_i > t)$$

再由次高斯变量的尾部界 P(X_i > t) ≤ exp(-t²/(2σ²))，得：

$$P(Z > t) \leq N \exp\left(-\frac{t^2}{2\sigma^2}\right)$$

### 2. 有限覆盖定理：将 "无限" 转化为 "有限"

考虑高维空间中 "无限个方向 θ" 的最大值 max_{θ∈B_2} θ^T X（B_2 是欧氏单位球），需通过**有限覆盖**将其转化为 "有限个方向 z∈N" 的最大值：

#### 覆盖数（packing 数）

存在有限点集 N ⊂ B_2，使得对任意 θ ∈ B_2，存在 z ∈ N 满足 ‖θ - z‖_2 ≤ ε。覆盖数满足上界：

$$N(B_2, \|\cdot\|_2, \varepsilon) \leq \left(\frac{3}{\varepsilon}\right)^d$$

（d 是空间维度，体现 "高维空间中用有限点覆盖单位球" 的可能性）。

#### 最大值的期望估计（覆盖后）

由覆盖的近似性，max_{θ∈B_2} θ^T X ≤ max_{z∈N} z^T X + ε‖X‖_2。结合次高斯性（若 X 是次高斯向量，‖X‖_2 的期望可控），最终可得：

$$\mathbb{E}\left[\max_{\theta \in B_2} \theta^T X\right] \leq \sigma\sqrt{2\log N}$$

（将 "无限方向的最大值" 转化为 "有限覆盖点的最大值"，实现高维问题的有限化处理）。

---
*添加时间: 2026-04-07*

---

## 稀疏参数估计

### 1. 稀疏性假设与基本估计式

假设真实参数 θ* 是**稀疏的**，即非零元个数 ‖θ*‖_0 = s ≪ n（n 为样本量）。对估计量 θ̂_k，核心推导涉及：

- **二次型上界**：利用柯西不等式或凸性，有

  $$\|X(\hat{\theta}_{t+s} - \theta^*)\|_2^2 \leq 2\varepsilon^T X(\hat{\theta}_{t+s} - \theta^*)$$

  （将范数平方转化为线性型，便于结合期望或概率分析）；

- **残差平方和**：观测值与拟合值的残差平方和为 ‖Y - Xθ‖_2²，是衡量拟合优度的核心指标。

### 2. 估计量的概率界（1-δ 置信）

在概率 1-δ 下，估计量 θ̂_k 与真实参数 θ* 的偏差满足上界：

$$\|\hat{\theta}_k - \theta^*\| \leq \frac{\sigma^2 k}{n} \log\left(\frac{2ke}{d}\right) + \frac{\sigma^2 k}{n} \log\left(\frac{1}{\delta}\right) + \frac{\sigma^2}{n} \log\left(\frac{16}{\delta}\right)$$

（其中 σ² 是噪声方差，d 是参数维度，k 是迭代或模型复杂度相关指标。该界体现 "偏差随样本量 n 增大而减小，随稀疏度 s、维度 d 增大而增大" 的规律）。

### 3. 风险（均方误差）的定义

定义估计量 θ̂ 的**风险**（均方误差）为：

$$\mathcal{E}(\hat{\theta}) = \mathbb{E}_{X,Y}\left[\|\hat{\theta} - \theta^*\|_{\tilde{E}[Z]}^2\right] = \mathbb{E}_Y\left[\|\hat{\theta} - \theta^*\|_{\tilde{E}}^2\right]$$

（对数据 X, Y 取期望，衡量 "估计量与真实参数的平均偏差"，是统计学习中评估模型性能的核心指标。当样本量足够大时，风险的阶为 O(sσ²/n)，体现 "稀疏性加速收敛" 的特点）。

---
*添加时间: 2026-04-07*

---

## 高维统计学习与稀疏估计

### 1. 约束最小二乘估计的误差分析

考虑线性模型 Y=Xθ*+ε（ε 是噪声，假设次高斯分布），θ̂_k 是参数 θ* 的估计量。核心估计式：

- 残差范数控制：∥Xθ̂_k−Y∥_2² ≤ ∥Xθ*−Y∥_2² = 4∥ε∥_2²（体现估计的 "残差不增性"）；
- 噪声的变换：定义 ε̃_i = X_i^T ε（将原始噪声 ε 变换为与特征 X_i 相关的新噪声项）。

### 2. 集中不等式的应用（次高斯噪声）

对次高斯分布的随机变量，利用**集中不等式**控制 "线性变换后的噪声上界"：

$$P\left(-\frac{s}{a}\tilde{\varepsilon}^T u > nt\right) \leq 2d\exp\left(-\frac{2nt^2}{\sigma^2}\right)$$

（d 为特征维度，σ 是次高斯参数，通过指数尾部衰减控制概率）。

令该概率上界为 δ，解指数不等式得**阈值 t**：

$$t = \sigma\sqrt{\frac{1}{2n}\log\frac{2d}{\delta}}$$

### 3. 参数估计的误差界

结合残差与集中不等式，推导**估计误差的 ℓ2 范数界**：

$$\|\hat{\theta}_k - \theta^*\|_2^2 \leq \frac{\sigma^2}{n}\log d$$

在**概率 1−δ** 下，进一步得到 "归一化误差" 的上界，最终误差界可简化为与 (log(d/δ))/n 同阶（体现 "高维下误差随对数维度和样本量的衰减"）。

### 4. 误差分解与支撑集约束

设 Δ=θ̂−θ*，A* 为 θ* 的**真实支撑集**（非零元的索引集）。通过正则化的稀疏诱导性，可得**支撑集补集的误差约束**：

$$\|\Delta_{A^c}\|_2 \leq 3\|\Delta_A\|_2$$

（即 "非支撑集上的误差被支撑集上的误差控制"，体现稀疏估计的 "集中性"）。

### 5. 正则化参数的选择

为保证高维下的概率集中性，正则化参数 λ 需满足：

$$\lambda = 2\sigma\sqrt{\frac{2\ln(2d/\delta)}{n}}$$

### 6. Lasso 误差界

结合支撑集约束与 Lasso 目标函数的最优性，最终推导**估计误差的上界**：

$$\|\hat{\theta} - \theta^*\|_2 \lesssim \frac{\sigma\sqrt{|A^*| \cdot 2\ln(2d/\delta)}}{\gamma\sqrt{n}}$$

（γ>0 为与特征矩阵 X 相关的 "强制性常数"，|A*| 是真实支撑集的大小，体现 "误差随样本量 n 增大而衰减，随稀疏度 |A*|、对数维度 ln(2d/δ) 增大而增大"）

---
*添加时间: 2026-04-08*

---

## VC 维与打散数的概念

### 1. VC 维与打散数的定义

- **打散数 $\Pi_{\mathcal{H}}(m)$**：假设类 $\mathcal{H}$ 对 $m$ 个样本能实现的"不同标签划分的数量"。
  $$\Pi_{\mathcal{H}}(m) = |\{(h(x_1), h(x_2), \cdots, h(x_m)) \mid x_i \in \mathcal{X}, h \in \mathcal{H}\}|$$

- **VC 维 $\text{VC}(\mathcal{H})$**：最大的 $m$ 使得 $\Pi_{\mathcal{H}}(m) = 2^m$（即能"完全打散" $m$ 个样本的所有 $2^m$ 种标签组合）。

### 2. 区间分类器的打散分析

考虑**区间分类器**（判断 $x$ 是否在区间 $[\alpha,\beta]$ 内），分析其对不同样本数 $m$ 的打散能力：

- 当 $m=2$：可验证 $\Pi_{\mathcal{H}}(2) = 4 = 2^2$（能完全打散 2 个样本的所有 4 种标签组合），故 $\text{VC}(\mathcal{H}) \geq 2$。
- 当 $m=3$：计算得 $\Pi_{\mathcal{H}}(3) = 7 < 2^3 = 8$（无法完全打散 3 个样本的所有 8 种标签组合），因此 $\text{VC}(\mathcal{H}) = 2$。

### 3. 单峰函数与假设空间的拓展

进一步假设"单峰函数"形式 $h(x; \alpha, b) = \text{sign}(\cdots)$（$x \in [a,b]$），通过分析这类函数对样本的划分能力，可推广到更一般的假设空间，验证其 VC 维是否与区间结构相关（核心逻辑："区间的线性划分能力限制了打散数的增长"）。

---
*添加时间: 2026-04-11*


---

## 凸优化与 L1 正则化

### L1 问题的优化

考虑优化问题：
$$
x^* = \arg\min_{x \in \mathbb{R}^n} \left( \frac{1}{2n} \| A x - b \|^2 + \lambda \| x \|_1 \right)
$$

### Proximal 算子

**L1 正则化的 Proximal 算子**（软阈值算子）：
$$
S_\lambda(t) = \begin{cases} 
0, & |t| \leq \lambda \
t - \lambda, & t \geq \lambda \
t + \lambda, & t \leq -\lambda 
\end{cases}
$$

**不动点算法**：
$$
x^* = S_\lambda \left( x^* + \frac{1}{n} A^\top (b - A x^*) \right)
$$

**迭代形式**：
$$
x^{(k+1)} = S_\lambda \left( x^{(k)} + A^\top (b - A x^{(k)}) \right)
$$

### 次微分理论

**凸函数的次微分**（不要求连续）：
$$
f(y) \geq f(x) + z^\top (y - x), \forall y
$$
其中 $z$ 称为次微分。

**绝对值函数的次微分**：
- $x > 0$ 时：$\partial |x| = \{1\}$
- $x < 0$ 时：$\partial |x| = \{-1\}$
- $x = 0$ 时：$\partial |x| = [-1, 1]$

### 凸优化的一阶条件

**优化条件**：
$$
\arg\min_{x \in \mathbb{R}^n} f(x) \iff 0 \in \partial f(x^*)
$$

**例子**：$f(x) = \frac{1}{2}(x - t)^2 + \lambda |x|$
- $x > 0$ 时：$\partial f(x) = (x - t) + \lambda$
- $x < 0$ 时：$\partial f(x) = (x - t) - \lambda$
- $x = 0$ 时：$\partial f(0) = [-t - \lambda, -t + \lambda]$

**解**：
- 若 $|t| \leq \lambda$，则 $x^* = 0$
- 若 $t > \lambda$，则 $x^* = t - \lambda$
- 若 $t < -\lambda$，则 $x^* = t + \lambda$

即 $x^* = S_\lambda(t)$

### L1 正则化的次微分

$$
\| x \|_1 \text{ 的次微分性质：} \| y \|_1 \geq \| x \|_1 + \langle z, y - x \rangle
$$

其中 $z$ 是 $\| \cdot \|_1$ 在 $x$ 处的次微分。

逐项分析：
$$
\sum_i (|y_i| - |x_i|) \geq \sum_i z_i (y_i - x_i)
$$

即 $|y_i| - |x_i| - z_i (y_i - x_i) \geq 0$，其中 $z_i \in \partial |x_i|$

### 光滑项的梯度

$$
\frac{\partial}{\partial x} \left( \frac{1}{2n} \| A x - b \|^2 \right) = \frac{1}{n} A^\top (A x - b)
$$

### 优化的一阶条件

**次梯度为 0**：
$$
\frac{1}{n} A^\top (A x^* - b) + \lambda \partial \| x^* \|_1 = 0
$$

### 凸集上的优化

**凸集上的凸函数优化**：
$$
g(x) = f(x) + \mathbb{1}_C(x)
$$
其中 $\mathbb{1}_C$ 是凸集 $C$ 的示性函数。

若 $x \notin C$，则 $\partial g = \emptyset$。

---

## 法锥与对偶范数

### 法锥定义

**法锥**：
$$
N_C(x) = \{ z \mid \langle z, y - x \rangle \leq 0, \forall y \in C \}
$$

### 最优性条件

**凸集约束优化**：
$$
-\nabla f(x^*) \in N_C(x^*)
$$
（若 $0 \in C$，$C$ 为凸锥）

### 对偶范数

**对偶范数定义**：
$$
\| x \|_* = \sup_{\|y\| \leq 1} \langle x, y \rangle
$$

对于矩阵 $A = U \Sigma V^\top$（奇异值分解），其谱范数的对偶范数为核范数。

### L2 正则化的优化

**优化问题**：
$$
\frac{1}{2n} \| A x - b \|_2^2 + \lambda \| x \|_2
$$

**一阶条件**：
$$
\frac{1}{n} A^\top (A x^* - b) + \lambda \partial \| x^* \|_2 = 0
$$

### 辅助函数方法

**辅助函数**：
$$
H(x) = \frac{1}{2} \| x - d^* \|^2 + \lambda \| x \|_2
$$

最优性条件：
$$
0 \in \partial H(x) \iff \exists (x - d^*) + \lambda \partial \| x \|_2 = 0
$$

---

## 优化器总结

### 梯度下降类方法

1. **SGD**：$\theta_{t+1} = \theta_t - \eta_t \nabla L(\theta_t)$
2. **动量法**：$m_t = \beta m_{t-1} + (1-\beta)\nabla L(\theta_t)$
3. **AdaGrad**：自适应学习率，适合稀疏数据
4. **Adam**：结合动量和自适应学习率

### 二阶优化方法

1. **Newton 法**：使用二阶信息，收敛快但计算量大
2. **共轭梯度**：避免显式计算 Hessian 矩阵

### Proximal 梯度法

针对非光滑正则项（如 L1）：
$$
x^{(k+1)} = \text{prox}_{\lambda r} \left( x^{(k)} - \eta \nabla f(x^{(k)}) \right)
$$

其中 $\text{prox}_{\lambda r}(x) = \arg\min_y \left( r(y) + \frac{1}{2\lambda} \|y - x\|^2 \right)$
---
*添加时间: 2026-04-15*
