# LFTP 优化 — Ch1, Ch2 手写笔记

> 云端视觉模型转录 · 待人工校对

## 第 1 页

```math
\begin{aligned}
R(f) &= E[l(y, f(x))] \\
F(\theta) &= \frac{1}{n} \sum_{i=1}^{n} l(y_i, f_\theta(x_i)) + \Omega(\theta) \\
R(f_\theta^*) - \inf_{\theta \in \mathbb{R}^d} R(f_\theta) &= R(f_\theta^*) - \hat{R}(f_\theta^*) + \hat{R}(f_\theta^*) - \hat{R}(f_\theta^*) + \hat{R}(f_\theta^*) - R(f_\theta^*) \\
&= \tilde{R} \\
&\leq 2 \sup_{f \in \mathcal{F}_0} |R(f) - \hat{R}(f)| + \hat{R}(f_\theta^*) - \hat{R}(f_\theta^*) \\
&\quad \text{(err(sta))} \quad \text{(err(cpt))} \\
R(f_\theta^*) - \inf_{\theta \in \mathbb{R}^d} \hat{R}(f_\theta) &\leq \sup_{f \in \mathcal{F}} |R(f) - \hat{R}(f)| \text{ 统计误差, 可以被 } 2 \operatorname{Rad}(\mathcal{F}_0) \text{ 控制} \\
\mathcal{F}_0 &\text{为有限类 } \sqrt{}, \text{无限类, 先用有限覆盖变成有界类, 结论为 } \mathfrak{D}\left(\frac{1}{\eta}\right) \\
f_\theta^* &\text{不一定是 } R(f) \text{ 泛函极小, 它是用优化算法 } GD/SGD \text{ 求出的 } f_\theta^*, \text{ 事实上, 由于误差分解.} \\
\hat{R}(f_\theta^*) - \inf_{\theta \in \mathbb{R}^d} \hat{R}(f_\theta^*) &\text{ err(cpt)} \text{ 与 err(sta) 同阶即} \\
\text{但, } \theta_t &\text{ 往往对应带正则的 } f_\theta \text{ 的下降, 而且多少步才让统计与优化近似?} \\
GD: F(\theta_t) - F^* &= \mathcal{O}\left(\frac{1}{t}\right) \text{ 一般凸问题 } \mathcal{O}\left(e^{-t}\right) \text{ 强凸光滑} \\
SGD &\quad \mathcal{O}\left(\frac{1}{\sqrt{t}}\right), \text{ 弱凸光滑 } \mathcal{O}\left(\frac{1}{t}\right) \\
\text{还有一个问题: } \inf_{\theta \in \mathbb{R}^d} R(f_\theta^*) - \inf_{f \in \mathcal{F}} R(f) &= \text{ 这是逼近误差, 得到三部分} \\
&\quad \text{(err(approximation))} \\
\text{回到重点 - 优化误差计算}
\end{aligned}
```

## 第 2 页

**优化误差：**

```math
F(\theta) = \frac{1}{n} \sum_{i=1}^{n} \ell(y_i, f_\theta(x_i)) + \Omega(\theta)
```

```math
\theta_t = \theta_{t-1} - \eta \nabla F(\theta)
```

```math
F(\theta) = \frac{1}{2n} \| \phi \theta - y \|_2^2
```

```math
F'(\theta_{t+1}) = 0 \quad (\text{Fermat lemma})
```

```math
F'(\theta) = \frac{1}{n} \phi^\top (\phi \theta - y)
```

```math
\theta_t = \theta_{t-1} - \frac{\eta}{n} \phi^\top \phi (\theta_{t-1} - y)
```

```math
\tilde{\theta}_t = \theta_t - \eta n_* = \theta_{t-1} - \theta_* - \frac{\eta}{n} \phi^\top \phi (\theta_{t-1} - y)
```

```math
= (I - \frac{\eta}{n} \phi^\top \phi)(\theta_{t-1} - \eta n_*)
```

```math
\theta_t - \eta n_* = (I - \eta H)^t (\theta_{t-1} - \eta n_*)
```

```math
\| \theta_t - \eta n_* \|_2^2 = \| (I - \eta H)^t (\theta_{t-1} - \eta n_*) \|_2^2
```

```math
\| (I - \eta H)^t (\theta_{t-1} - \eta n_*) \|_2^2 \leq \lambda_{\max}(I - \eta H)^{2t} \| \theta_{t-1} - \eta n_* \|_2^2
```

```math
\lambda_{\max}((I - \eta H)^t)^2 \leq \left( \frac{1 - \eta \lambda}{1 + \eta \lambda} \right)^{2t}
```

```math
\frac{2}{n} \leq \frac{2}{L} \quad \text{and} \quad 1 - \frac{2}{K} \leq 1
```

```math
\alpha = \frac{2}{\mu + L}, \quad \text{此时} \quad \| I - \alpha \lambda I \|_2 \leq \frac{|L - \mu|}{\mu + L} \leq \frac{K - 1}{K}
```

```math
(1 - \frac{1}{K})^{2t} \leq \exp(-\frac{t}{K})
```

**Lipschitz - 梯度：**

```math
F(\theta_{t+1}) \geq F(\theta_t) + F'(\theta_t)^\top (\theta_{t+1} - \theta_t)
```

```math
F(\theta) - F(\theta_{t+1}) \leq F'(\theta_t)^\top (\theta_{t+1} - \theta)
```

**强凸性：**

```math
F(\eta) \geq F(\theta) + F'(\theta)^\top (\eta - \theta) + \frac{\mu}{2} \| \eta - \theta \|_2^2
```

## 第 3 页

**Lojasiewicz's inequality**

```math
\|F'(\theta)\|_2^2 \geq 2\mu(F(\theta) - F(\theta^*))
```

```math
F(\theta) - F(\theta^*) \geq F'(\theta)(\theta - \eta) + \frac{1}{2}\mu\|\theta - \eta\|^2
```

```math
\theta \geq F(\eta) + \frac{1}{\mu}F'(\theta)
```

```math
\|F'(\theta)\|_2 \cdot \|\theta - \eta\| \geq \frac{1}{2}\mu\|\theta - \eta\|^2
```

```math
\tilde{\eta} = \theta - \frac{1}{\mu}F'(\theta)
```

```math
F(\tilde{\eta}) \geq F(\theta) + F'(\theta)^T(-\frac{1}{\mu}F'(\theta)) + \frac{1}{2}\mu\|\theta - \frac{1}{\mu}F'(\theta)\|^2
```

```math
= F(\theta) - \frac{1}{2\mu}\|F'(\theta)\|^2
```

```math
f(\theta) \leq F(\tilde{\eta})
```

如果有 $K = \frac{1}{\mu}$，那么套用线性有指数下降

**引理 1.1 数分高代复习**

```math
\text{Ex. 1.1 } (I + 2\lambda_n 1_n 1_n^T) \text{ 可逆且 } (I + 2\lambda_n 1_n 1_n^T)^{-1} = (I - \frac{2\lambda_n}{1 + n\lambda_n} 1_n 1_n^T)
```

已知 $A = I + \alpha 1_n 1_n^T$，$A$ 特征值 $\lambda$；

```math
\det(\lambda I - I - \alpha 1_n 1_n^T) = (\lambda - 1)^{n-1}(\lambda - 1 - n\alpha)
```

当 $1 + n\alpha \neq 0$，$A$ 没有零特征值，$I + \alpha 1_n 1_n^T$ 可逆。

其次 $(I + \alpha 1_n 1_n^T)^{-1} = I - \frac{\alpha}{1 + n\alpha} 1_n 1_n^T$

用引理 $(I + BB^T)^{-1} = I - B(I + B^TB)^{-1}B^T$

**分块矩阵求逆：**

```math
\begin{pmatrix} A & B \\ C & D \end{pmatrix}^{-1}
```

## 第 4 页

**优化误差：**

```math
F(\theta) = \frac{1}{n} \sum_{i=1}^{n} \ell(y_i, f_\theta(x_i)) + \Omega(\theta)
```

```math
\theta_{t+1} = \theta_t - 2 \nabla F(\theta_t)
```

```math
F(\theta) = \frac{1}{2n} \| \Phi \theta - y \|^2
```

```math
F'(\theta_+) = 0 \quad (\text{Fermat lemma})
```

```math
F'(\theta) = \frac{1}{n} \Phi^\top (\Phi \theta - y)
```

```math
\theta_{t+1} = \theta_{t+1} - \frac{\alpha}{n} \Phi^\top \Phi (\theta_{t+1} - y)
```

```math
= (I - \frac{\alpha}{n} \Phi^\top \Phi) (\theta_{t+1} - \eta_+)
```

```math
\theta_t - \eta_+ = (I - \alpha H)^t (\theta_{t+1} - \eta_+)
```

```math
\| \theta_t - \eta_+ \|^2 = \| (I - \alpha H)^t (\theta_{t+1} - \eta_+) \|^2
```

```math
\| (\theta_0 - \eta_+)^T (I - \alpha H)^t (\theta_{t+1} - \eta_+) \| \leq \lambda_{\max} (I - \alpha H)^{2t} \| \theta_0 - \eta_+ \|^2
```

```math
\lambda_{\max} (I - \alpha H)^{2t} \leq \left( \frac{1 - \alpha \lambda}{1 + \alpha \lambda} \right)^{2t}
```

```math
\alpha = \frac{2}{\mu + L}, \quad \text{此时} \quad \| I - \alpha \lambda I \|^2 \leq \frac{L - \mu}{\mu + L} \left( 1 - \frac{1}{K} \right)
```

```math
(1 - \frac{1}{K})^{2t} \leq \exp(-\kappa t)
```

**Lipschitz 梯度：**

```math
F(\theta_+) \leq F(\theta) + F'(\theta)^T (\theta_+ - \theta) + \frac{L}{2} \| \theta_+ - \theta \|^2
```

**强凸性：**

```math
F(\eta) \geq F(\theta) + F'(\theta)^T (\eta - \theta) + \frac{\mu}{2} \| \eta - \theta \|^2
```

## 第 5 页

**分块矩阵求逆公式：**

```math
(MA)^{-1} = A^{-1}(D - CA^{-1}B)^{-1} = D^{-1} + D^{-1}C(A - BD^{-1}C)^{-1}BD^{-1}
```

```math
(WD)^{-1} = (A - BD^{-1}C)^{-1} \approx A^{-1} + A^{-1}B(D - CA^{-1}B)^{-1}CA^{-1}
```

```math
\det\begin{pmatrix} A & B \\ C & D \end{pmatrix} = \det A \det(MA) = \det D \det(M/D)
```

```math
M = \begin{pmatrix} A & B \\ C & D \end{pmatrix} = \begin{pmatrix} I & 0 \\ CA^{-1} & I \end{pmatrix} \begin{pmatrix} A & 0 \\ 0 & M/A \end{pmatrix} \begin{pmatrix} I & A^{-1}B \\ 0 & I \end{pmatrix}
```

```math
M^{-1} = \begin{pmatrix} A & B \\ C & D \end{pmatrix}^{-1} = \begin{pmatrix} I & -A^{-1}B \\ 0 & I \end{pmatrix} \begin{pmatrix} A^{-1} & 0 \\ 0 & (MA)^{-1} \end{pmatrix} \begin{pmatrix} I & 0 \\ -CA^{-1} & I \end{pmatrix}
```

当 $A$ 可逆

**SVD 与特征分解：**

```math
X = U\Sigma V^{T}
```

```math
\begin{pmatrix} O & X \\ X^{T} & O \end{pmatrix}
```

## 第 6 页

**SVD 特征向量构造：**

```math
M = \begin{pmatrix} O & X \\ X^T & O \end{pmatrix}, \quad X = U \Sigma V^T
```

```math
M(u_i) = \begin{pmatrix} X v_i \\ X^T u_i \end{pmatrix} = \sigma_i \begin{pmatrix} u_i \\ v_i \end{pmatrix}
```

```math
M(-v_i) = \begin{pmatrix} -X v_i \\ X^T u_i \end{pmatrix} = -\sigma_i \begin{pmatrix} -u_i \\ v_i \end{pmatrix}
```

```math
XX^T = U \Sigma^2 U^T = \frac{n}{n-1} \hat{\sigma}^2 u_i u_i^T \quad \text{特征向量}(u_i)
```

```math
X^T X = V \Sigma^2 V^T = \sum \sigma_i v_i v_i^T \quad \text{特征向量}(v_i)
```

**二次优化：**

```math
F(\theta) = \frac{1}{2} \theta^T A \theta - b^T \theta
```

```math
F'(\theta) = \frac{1}{2} (A + A^T) \theta - b
```

```math
F''(\theta) = \frac{1}{2} (A + A^T)
```

**线性回归：**

```math
F(\theta) = \frac{1}{2n} \| y - X \theta \|^2 = \frac{1}{n} (y^T y - 2 y^T X \theta + \theta^T X^T X \theta)
```

```math
F'(\theta) = -\frac{1}{n} X^T (y - X \theta)
```

```math
F''(\theta) = \frac{1}{n} X^T X
```

**逻辑回归：**

```math
F(\theta) = \frac{1}{n} \sum \log(1 + \exp(-y_i (X \theta)_i))
```

```math
\frac{\partial F}{\partial \theta_j} = \frac{1}{n} \sum_{i=1}^n \frac{-y_i x_{ij}}{1 + \exp(-y_i (X \theta)_i)}
```

## 第 7 页

**逻辑回归梯度与 Hessian：**

```math
F(\theta) = \sum_{i=1}^{n} \log(1 + \exp(-y_i \langle x_i, \theta \rangle))
```

```math
\phi(t) = \log(1 + \exp(t)), \quad \phi'(t) = \frac{1}{1 + e^{-t}} = \sigma(t)
```

```math
F'(\theta) = -\frac{1}{n} X^T g, \quad g_i = -\frac{y_i}{1 + \exp(-y_i \langle x_i, \theta \rangle)}
```

```math
F''(\theta) = \frac{1}{n} X^T \operatorname{diag}(g_1(\theta), \ldots, g_n(\theta)) X
```

利用 $y_i^2 = 1$ 和 sigmoid 导数性质：

```math
F''(\theta) = \frac{1}{n} X^T \operatorname{diag}(\sigma(-y_i \langle x_i, \theta \rangle) \sigma(y_i \langle x_i, \theta \rangle)) X
```

**矩阵微积分：**

```math
\operatorname{tr}(A A^T) = \operatorname{tr}(A^T A)
```

```math
f(X) = \operatorname{tr}(A^T X), \quad f'(X) = A
```

```math
\frac{\partial}{\partial X} X^T A X = (A + A^T) X
```

```math
f(A) = X^T A X, \quad f'(A) = X X^T
```

## 第 8 页

**矩阵微积分（续）：**

```math
f(CX) = \operatorname{tr}(CX^T A CX) = \operatorname{tr}(A X X^T)
```

```math
\frac{d(X X^T)}{dX} = A X + A^T X
```

```math
d(A X B) = A (dX) B, \quad \text{导数为 } A^T X B^T + A X B
```

```math
0 = d(X \cdot X^{-1}) = (dX) X^{-1} + X d(X^{-1})
```

```math
d(X^{-1}) = -X^{-1} (dX) X^{-1}
```

**行列式导数：**

```math
\frac{d(\det(X))}{dt} = \det(X) \operatorname{tr}(X^{-1} dX)
```

```math
f(X) = \log \det X, \quad f'(X) = X^{-1}
```

## 第 9 页

**概率不等式（尾部 bound）：**

$t \in [0, 1)$ 时：

```math
\frac{1}{x} - \frac{x}{\sqrt{n}} \geq \frac{1}{4}e^{-t}, \quad t \geq 0
```

由于 $f(t) = \frac{1}{x} - \frac{x}{\sqrt{n}} - \frac{1}{4}e^{-t}$

```math
f'(t) = -\frac{1}{\sqrt{n}} + \frac{1}{2}te^{-t}
```

$f$ 在 $[0, n]$ 上递减。

$t > 1$ 时，尾部积分估计：

```math
a(t) = \int_{t}^{\infty} \phi(x) dx = \frac{1}{t} \phi(t) - \int_{t}^{\infty} \frac{1}{x^2} \phi(x) dx
```

```math
\int_{t}^{\infty} \phi(x) dx \geq \frac{t}{1+t} \phi(t)
```

验证等价条件：

```math
\frac{t}{\sqrt{2\pi}(1+t)} e^{-\frac{1}{2}t^2} = \frac{1}{4}e^{-t^2} \iff \frac{4t}{\sqrt{2\pi}(1+t)} e^{\frac{1}{2}t^2} \geq 1
```

