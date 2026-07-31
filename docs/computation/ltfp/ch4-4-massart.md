第 4 章 · 经验风险最小化与统计学习理论

Chaining链式法，主要用于经验误差估计之中对于Rademacher复杂度，也就是用来估计
```math
R_n(\mathcal H) =\mathbb E_\varepsilon\left[
\sup_{h\in\mathcal H}
\frac1n\sum_{i=1}^n \varepsilon_i h(z_i)
\right]
```
如果对于有限的函数类，那么$R_n(\mathcal H)$可以被这么估计

Bach 书里 4.4.4 正是这样引入 covering number：用有限个函数 $f_1,\dots,f_m$ 近似整个函数类；如果每个 $f$ 都能被某个 $f_i$ 以误差 $\varepsilon$ 近似，那么 $m(\varepsilon)$ 就是 covering number。

单层 $\varepsilon$-net 会得到类似：
```math
\text{误差}
\lesssim
\varepsilon
+
\sqrt{\frac{\log N(\varepsilon,\mathcal H)}{n}}.
```
问题是：这个 bound 往往不够精细。书里也指出，单纯的 covering number argument 可能不够，需要更精细的 covering number 计算或者更高级工具，例如 chaining。

Massart lemma:

固定样本 $z_1,\dots,z_n$。令
```math
v_j=(h_j(z_1),\dots,h_j(z_n))\in\mathbb R^n.
```
经验 Rademacher complexity 是
```math
\widehat R_n(\mathcal H)
=
\mathbb E_\varepsilon
\left[
\max_{1\le j\le m}
\frac1n\sum_{i=1}^n \varepsilon_i h_j(z_i)
\right].
```
记
```math
X_j=\frac1n\sum_{i=1}^n \varepsilon_i h_j(z_i)
=
\frac1n\langle \varepsilon,v_j\rangle.
```
所以要证明的是
```math
\mathbb E_\varepsilon\max_j X_j
\le
R\sqrt{\frac{2\log m}{n}}.
```

------

## 第一步：用 log-sum-exp 控制 max

对任意 $\lambda>0$，有
```math
\max_j X_j
=
\frac1\lambda \log e^{\lambda\max_j X_j}
=
\frac1\lambda \log \max_j e^{\lambda X_j}.
```
而
```math
\max_j e^{\lambda X_j}
\le
\sum_{j=1}^m e^{\lambda X_j}.
```
所以
```math
\max_j X_j
\le
\frac1\lambda
\log\left(
\sum_{j=1}^m e^{\lambda X_j}
\right).
```
取期望：
```math
\mathbb E\max_j X_j
\le
\frac1\lambda
\mathbb E
\log\left(
\sum_{j=1}^m e^{\lambda X_j}
\right).
```
再用 Jensen，因为 $\log$ 是凹函数：
```math
\mathbb E\log Y
\le
\log \mathbb E Y.
```
于是
```math
\mathbb E\max_j X_j
\le
\frac1\lambda
\log
\left(
\sum_{j=1}^m \mathbb E e^{\lambda X_j}
\right).
```
所以现在只要控制每个
```math
\mathbb E e^{\lambda X_j}.
```

------

## 第二步：证明每个 $X_j$ 是 sub-Gaussian

固定 $j$，有
```math
X_j
=
\frac1n\sum_{i=1}^n \varepsilon_i h_j(z_i).
```
由于 $\varepsilon_i$ 独立，
```math
\mathbb E_\varepsilon e^{\lambda X_j}
=
\prod_{i=1}^n
\mathbb E_{\varepsilon_i}
\exp\left(
\frac{\lambda}{n}\varepsilon_i h_j(z_i)
\right).
```
因为 $\varepsilon_i=\pm1$ 等概率，
```math
\mathbb E_{\varepsilon_i}
e^{t\varepsilon_i}
=
\frac{e^t+e^{-t}}2
=
\cosh(t).
```
并且有基本不等式
```math
\cosh(t)\le e^{t^2/2}.
```
所以
```math
\mathbb E_{\varepsilon_i}
\exp\left(
\frac{\lambda}{n}\varepsilon_i h_j(z_i)
\right)
\le
\exp\left(
\frac{\lambda^2 h_j(z_i)^2}{2n^2}
\right).
```
连乘得到
```math
\begin{aligned}
\mathbb E_\varepsilon e^{\lambda X_j}
&\le
\prod_{i=1}^n
\exp\left(
\frac{\lambda^2 h_j(z_i)^2}{2n^2}
\right)\\
&=
\exp\left(
\frac{\lambda^2}{2n^2}
\sum_{i=1}^n h_j(z_i)^2
\right).
\end{aligned}
```
由假设
```math
\frac1n\sum_{i=1}^n h_j(z_i)^2\le R^2,
```
即
```math
\sum_{i=1}^n h_j(z_i)^2\le nR^2.
```
所以
```math
\mathbb E_\varepsilon e^{\lambda X_j}
\le
\exp\left(
\frac{\lambda^2R^2}{2n}
\right).
```
这说明每个 $X_j$ 都是尺度约为 $R/\sqrt n$ 的 sub-Gaussian 变量。

------

## 第三步：代回 max 的上界

有
```math
\sum_{j=1}^m \mathbb E e^{\lambda X_j}
\le
m\exp\left(
\frac{\lambda^2R^2}{2n}
\right).
```
因此
```math
\begin{aligned}
\mathbb E\max_j X_j
&\le
\frac1\lambda
\log
\left[
m\exp\left(
\frac{\lambda^2R^2}{2n}
\right)
\right]\\
&=
\frac{\log m}{\lambda}
+
\frac{\lambda R^2}{2n}.
\end{aligned}
```
这个不等式对任意 $\lambda>0$ 成立，所以现在优化 $\lambda$。

令
```math
\frac{\log m}{\lambda}
=
\frac{\lambda R^2}{2n},
```
得到
```math
\lambda^2
=
\frac{2n\log m}{R^2},
```
即
```math
\lambda
=
\frac{\sqrt{2n\log m}}{R}.
```
代入：
```math
\mathbb E\max_j X_j
\le
R\sqrt{\frac{2\log m}{n}}.
```
于是
```math
\boxed{
\widehat R_n(\mathcal H)
\le
R\sqrt{\frac{2\log m}{n}}.
}
```
再对样本 $D$ 取期望，得到理论 Rademacher complexity：
```math
\boxed{
R_n(\mathcal H)
\le
R\sqrt{\frac{2\log m}{n}}.
}
```
Dudley积分不等式

先估计$\hat R_D(\mathcal H)$,然后在对样本D取期望，就能得到实际的Rademacher复杂度。

可以把它拆成：$R_n(\mathcal H)=\mathbb E_D\left[\underbrace{\mathbb E_\varepsilon\left[\sup_{h\in\mathcal H}\frac1n\sum_{i=1}^n\varepsilon_i h(z_i)\right]}_{\widehat R_D(\mathcal H)}\right]$





