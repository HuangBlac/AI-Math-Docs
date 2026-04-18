# 三月七都能看懂的压缩感知

# 一 引入

三月七：没人觉得这个照相机真的很诡异吗？明明现实世界的点是无穷多的，但照相机却只有那么几个像素，拍出来的照片居然和真实世界看上去相差无几……但我觉得这不是什么大事，也不好意思去去问了列车长和丹恒他们。

长夜月：其实，你所思考的并不是一个容易的问题，正是顶级数学家的最新一批科研成果，压缩感知。它意味着对于稀疏的真实图像，我们只需要少量的采样点。

而且利用这个原理，我们可以制作不需要2000万像素，只需要一个点的相机

三月七：一个点的相机？那是怎么拍照的？

长夜月：让我们先来回顾一下照相机的原理：对于真实世界包含无穷维的信息，实际上就是一个很高维度的向量。而经过光线处理和聚焦，最终变成一个个像素点。而这也相当于另一个向量，每个分量就代表一个像素。而这个过程会被看成线性的，意思是一个原像变大两倍，像也变大两倍

三月七:那要想拍出真实的照片岂不是很难，得每个点都如实的记录下来？

长夜月：没错，根据奈奎斯特-香农采样定理，采样点的密度必须得是真实信号最高频率的两倍才能无失真重建

三月：呃，也就是说，要想把一张开拓者的照片完全拍摄清楚，要把每个原子都给扫描清楚？不对不对，上次贝罗伯格的简笔画，明明画的这么潦草，还是能一眼认出来，这是不是意味着……

长夜月：你的直觉很敏锐，事实上，真实信号往往具有“稀疏性”，意味着你拍一张照片，绝大多数的位置都其实是背景。
$$
s = Ax
$$
对应到之前拍照的问题，实际上我们自动”补全”了一个最好的信号，而这个补全的逻辑，就是在已知观测s和感知矩阵A的前提下，寻找最稀疏的x。

s是我们所看到的照片三月，A是你拍照时用到的一个照相机。我们求解一个稀疏信号即可。

三月七：等下，本姑娘明明就不是全是空荡荡的白噪声，我脸上的细节很多的！

长夜月：那我来纠正一下，因为在某一组基下你的表示是稀疏的。我们完全只用抓住几个关键细节，例如粉白渐变短发，圆脸，活泼就能够还原三月八九不离十。我们的假设中，就蕴含了x在一个已知的摄像机下是“稀疏”的，大部分元素都是零。

三月七：我明白了，就相当于压缩感知你作为一个画师，看到了一张潦草的画，并且根据对我的了解，画出一张三月

长夜月：对的，使用更数学的角度，就是要在已知s,A和让x非零元素尽可能多的情况下求解这个线性方程组。

三月七：感觉像是线性代数的内容，只是这个让非零元素尽可能多……伤脑筋。而且我怎么知道你这么推测的这张画像就和我真正的三月很像呢？以及给你的这张图片如果太潦草的话也不行吧。

长夜月：这就是我们接下来要讨论的内容，我们需要给出s这个观测值的维数n，x的维数d,x的非零元个数k与误差的关系，并且介绍应用，单点相机

## 二、L0问题：稀疏约束下的误差分析

### 基本设定

三月七：我们上一节说压缩感知的核心就是"稀疏"，那具体怎么数学上定义呢？

长夜月：设真实信号是 $x^* \in \mathbb{R}^d$，它的稀疏度定义为非零元个数：
$$
\|x^*\|_0 = |\{i : x^*_i \neq 0\}| = s
$$

我们通过感知矩阵 $A \in \mathbb{R}^{n \times d}$（其中 $n \ll d$）获得观测：
$$
s = Ax^* + \varepsilon
$$
其中 $\varepsilon \sim \mathcal{N}(0, \sigma^2 I)$ 是高斯噪声。

所要求解的是：
$$
\hat{x} = \arg\min_{x \in \mathbb{R}^d, \|x\|_0 \leq s} \|Ax - s\|_2^2
$$

即在所有稀疏度不超过 $s$ 的向量中，找与观测最接近的。

---

### L0 问题能计算吗

三月：所以这样求解的结果就是真正的解了吗？我怎么感觉求不出来真实解呢？

长夜月：我们不需要找到 $\hat{x}$ 本身，但是我们可以通过严谨的误差分析，来推理出真实的误差可以被噪声的强度，照片的维度，真实的维度给控制住，而且这个误差不会很大，即使我们采样点很少——当然，实际上这个不等式是“按概率的”，以很大可能成立：这来自于误差的分析框架。

那我们来进入正题

---

### 第一步：基本不等式

因为 $\hat{x}$ 是最小化点（在稀疏度约束下），所以：
$$
\|A\hat{x} - s\|_2^2 \leq \|Ax^* - s\|_2^2 = \|\varepsilon\|_2^2
$$

令 $\Delta = \hat{x} - x^*$ 是估计误差。注意 $\Delta$ 的稀疏度最多 $2s$——因为 $\hat{x}$ 和 $x^*$ 各自最多 $s$ 个非零元。

代入 $s = Ax^* + \varepsilon$：
$$
\|A\hat{x} - (Ax^* + \varepsilon)\|_2^2 = \|A\Delta + \varepsilon\|_2^2 \leq \|\varepsilon\|_2^2
$$

展开平方项：
$$
\|A\Delta + \varepsilon\|_2^2 = \|A\Delta\|_2^2 + 2\langle A\Delta, \varepsilon \rangle + \|\varepsilon\|_2^2
$$

代回不等式，消去 $\|\varepsilon\|_2^2$ 得**基本不等式**：
$$
\|A\Delta\|_2^2 + 2\langle A\Delta, \varepsilon \rangle \leq 0
$$

移项：
$$
\|A\Delta\|_2^2 \leq -2\langle A\Delta, \varepsilon \rangle \leq 2|\langle A\Delta, \varepsilon \rangle|
$$

---

### 第二步：RIP 条件与基本不等式，控制左边项：

三月七：好耶，我们控制住了这个…… $\|A\Delta\|_2$，我在这就把A当常数就行了对吧？只需要证明右边这一项很小对吧……等等，右边好像是个随机变量，我们是不是要证明这个随机变量很大的概率很小就行了？

长夜月： 先回答你第一个问题，这个感知矩阵该怎么选的问题。一般这个A会是一个系数矩阵，很接近单位矩阵，我们可以给出这样一个条件：

对任意 $2s$-稀疏向量 $u$（$\|u\|_0 \leq 2s$），有：
$$
(1 - \delta_{2s})\|u\|_2^2 \leq \|Au\|_2^2 \leq (1 + \delta_{2s})\|u\|_2^2
$$

其中 $\delta_{2s} \in (0, 1)$ 是 RIP 常数，通常要求 $\delta_{2s} < 1$。

关键观察：$\Delta = \hat{x} - x^*$ 是 $2s$-稀疏的（$\|\Delta\|_0 \leq 2s$），所以 RIP 条件对 $\Delta$ 成立。取下界：
$$
\|\Delta\|_2^2 \leq \frac{1}{1 - \delta_{2s}}\|A\Delta\|_2^2
$$

三月：我们之前学过特征值，或者说奇异值吧。”特征值”是衡量一个矩阵在某个方向上拉伸程度的，

长夜月：对！特征值衡量的是矩阵对向量的拉伸程度，而这里$\delta_{2s}$ 越小，$A$ 越接近"等距变换"。$\delta_{2s} = 0$ 时 $A$ 在稀疏子空间上就是正交变换。

从 RIP 下界代入基本不等式 $\|A\Delta\|_2^2 \leq -2\langle A\Delta, \varepsilon \rangle$：

$$
(1 - \delta_{2s})\|\Delta\|_2^2 \leq -2\langle A\Delta, \varepsilon \rangle \leq 2|\langle A\Delta, \varepsilon \rangle|
$$

两边除以 $1 - \delta_{2s}$（因为 $\delta_{2s} < 1$）：
$$
\|\Delta\|_2^2 \leq \frac{2}{1 - \delta_{2s}}|\langle A\Delta, \varepsilon \rangle|
$$

三月：现在只剩下噪声项 $|\langle A\Delta, \varepsilon \rangle|$ 需要控制了。

长夜月：没错，这是随机项。用**集中不等式**来控制它。

---

### 第三步：集中不等式控制噪声项

三月：集中不等式，就是说变量集中在一个特定的区域内，“很大”的概率很低？

长夜月：把 $\Delta$ 看作固定的，$\varepsilon$ 看作随机。$\langle A\Delta, \varepsilon \rangle = \Delta^\top(A^\top\varepsilon)$ 是高斯随机变量的线性组合——因此它是高斯的，均值为 0，方差为 $\sigma^2\|A\Delta\|_2^2$。

定义 $\mathcal{B}_{2s}$ 为所有 $2s$-稀疏的单位向量集合。设 $\|\Delta\|_2 > 0$（否则误差为 0），令 $u = \frac{\Delta}{\|\Delta\|_2} \in \mathcal{B}_{2s}$，则：
$$
|\langle A\Delta, \varepsilon \rangle| = \|\Delta\|_2 \left|\langle A u, \varepsilon \rangle\right|
$$

关键问题：控制 $\sup_{u \in \mathcal{B}_{2s}} |\langle A u, \varepsilon \rangle|$。

使用**覆盖方法**：用有限个向量覆盖 $\mathcal{B}_{2s}$，然后用联合界。覆盖数的上界是 $\mathcal{N} \leq \left(\frac{3}{\rho}\right)^{2s}$。对每个固定的覆盖向量 $u$，$\langle A u, \varepsilon \rangle \sim \mathcal{N}(0, \sigma^2\|Au\|_2^2)$。

用标准高斯尾概率界（在概率 $1 - \delta$ 下）：
$$
\sup_{u \in \mathcal{B}_{2s}} |\langle A u, \varepsilon \rangle| \leq C_0\sigma\sqrt{\log\left(\frac{d}{\delta}\right)}
$$
其中 $C_0$ 是只依赖 $\delta_{2s}$ 的常数。

因此：
$$
|\langle A\Delta, \varepsilon \rangle| \leq \|\Delta\|_2 \cdot C_0\sigma\sqrt{\log\left(\frac{d}{\delta}\right)}
$$

代回误差不等式，在概率 $1 - \delta$ 下：
$$
\|\Delta\|_2^2 \leq \frac{2C_0\sigma}{1 - \delta_{2s}}\|\Delta\|_2\sqrt{\log\left(\frac{d}{\delta}\right)}
$$

两边除以 $\|\Delta\|_2$ 得到最终**L0 误差界**：
$$
\|\hat{x} - x^*\|_2 \leq \frac{C_0\sigma}{1 - \delta_{2s}}\sqrt{\log\left(\frac{d}{\delta}\right)}
$$

---

### 误差界的含义

三月：这个结果说明了什么？

长夜月：几个关键点：

1. **误差只依赖稀疏度 $s$**：通过 $\delta_{2s}$ 间接依赖，**不直接依赖信号维度 $d$**——这是压缩感知的核心优势：即使 $d$ 极大，只要信号稀疏，误差仍然可控

2. **对维度 $d$ 只有对数依赖** $\log d$——高维下的"免费午餐"

3. **$\delta_{2s}$ 越小（感知矩阵越"好"），误差越小**：当 $\delta_{2s} \to 0$ 时，误差趋于 0

4. **噪声水平 $\sigma$ 线性影响**：噪声越大，误差越大



## 三、Lasso问题：从L0到L1

### 为什么要引入L1优化？

三月：所以上一节我们用L0范数约束来求解压缩感知问题，直接数”非零元的个数”这个操作听上去很好啊。为什么就是不行呢？

长夜月：问题不来自于数学，而来自于**计算复杂度**。L0优化需要在所有 $\binom{d}{k}$ 个可能的支撑集中搜索（$d$ 是信号维度，$k$ 是稀疏度），这是NP难的——简单来说，就是即使你拥有全宇宙最强大的计算机，也未必能在有限时间内找到答案。

三月：那能不能换一种约束方式，但仍然让变量变稀疏？

长夜月：好问题。考虑二维情形：L0约束要求非零元个数 $\leq k$，等价于坐标轴上只取有限个点。而L1约束 $\|x\|_1 \leq R$ 对应的是一个**菱形**，L2约束 $\|x\|_2 \leq R$ 对应的是一个**圆**。

关键观察：菱形的顶点恰好落在坐标轴上——也就是说，L1约束天然倾向于把解”推”到坐标轴上，让某些分量恰好为零。而L2约束的圆没有棱角，不具备这种稀疏诱导性。

长夜月：没错。于是我们将压缩感知问题从
$$
\text{L0}: \quad \min \|x\|_0 \quad \text{s.t.} \quad \|Ax - s\|_2 \leq \varepsilon
$$
松驰为
$$
\text{L1 (Lasso)}: \quad \hat{x} = \arg\min_x \left( \frac{1}{2n}\|Ax - s\|_2^2 + \lambda\|x\|_1 \right)
$$

三月七：不过，我这里倒还要问一个和正则项没关系的问题，为什么残差用的是L2范数而不是L1？这是不是也可以带来什么稀疏性

长夜月：这里的 $\|Ax - s\|_2^2$ 不是正则项，而是来自测量误差的统计性质。我们假设观测 $s = Ax^* + \varepsilon$，其中 $\varepsilon \sim \mathcal{N}(0, \sigma^2 I)$。高斯噪声下的最大似然估计自然给出L2损失。

而L1罚项才是用来形成稀疏性的。

但这个损失确实也会因问题而异：例如某些图像还原问题，就会加上图像的导数信息L1范数来作为损失，让得到的图象是光滑的……我跟你说得着这个吗

---

### L1优化是不是仍然足够好？——误差估计

三月：我懂了……但用L1替代L0，会不会引入额外误差？我们求出来的 $\hat{x}$ 和真实信号 $x^*$ 会不会因此就谬以千里了？

长夜月：这正是核心问题。我们再次来一步步推导Lasso的误差界。

#### 第一步：基本不等式

设 $\hat{x}$ 是 Lasso 的解，$x^*$ 是真实稀疏信号，令 $\Delta = \hat{x} - x^*$。因为 $\hat{x}$ 是最小化点，所以：
$$
\frac{1}{2n}\|A\hat{x} - s\|_2^2 + \lambda\|\hat{x}\|_1 \leq \frac{1}{2n}\|Ax^* - s\|_2^2 + \lambda\|x^*\|_1
$$

把 $s = Ax^* + \varepsilon$ 代入，展开左边：
$$
\frac{1}{2n}\|A\Delta + \varepsilon\|_2^2 + \lambda\|\hat{x}\|_1 \leq \frac{1}{2n}\|\varepsilon\|_2^2 + \lambda\|x^*\|_1
$$

展开平方项 $\|A\Delta + \varepsilon\|_2^2 = \|A\Delta\|_2^2 + 2\langle A\Delta, \varepsilon \rangle + \|\varepsilon\|_2^2$，消去 $\|\varepsilon\|_2^2$ 得：
$$
\frac{1}{2n}\|A\Delta\|_2^2 + \frac{1}{n}\langle A\Delta, \varepsilon \rangle + \lambda\|\hat{x}\|_1 \leq \lambda\|x^*\|_1
$$

移项得到**基本不等式**：
$$
\frac{1}{2n}\|A\Delta\|_2^2 + \lambda\|\hat{x}\|_1 \leq \lambda\|x^*\|_1 - \frac{1}{n}\langle A\Delta, \varepsilon \rangle
$$

#### 第二步：支撑集分解

三月七：上面这一串多了一个$$\lambda||\hat{x}||_1-||x^*||_1$$欸，说不定这样就会……

长夜月：你在替陶哲轩担心什么（流汗），还记得我们的题目背景：稀疏性吗

设 $A^*$ 是 $x^*$ 的真实支撑集（非零元的索引集），$|A^*| = s$（稀疏度）。将 $\Delta$ 拆分为 $\Delta_{A^*}$ 和 $\Delta_{(A^*)^c}$。

关键观察——L1范数分解：
$$
\|\hat{x}\|_1 = \|\Delta_{A^*} + x^*_{A^*}\|_1 + \|\Delta_{(A^*)^c}\|_1
$$

由三角不等式：
$$
\|x^*\|_1 - \|\hat{x}\|_1 = \|x^*_{A^*}\|_1 - \|\Delta_{A^*} + x^*_{A^*}\|_1 - \|\Delta_{(A^*)^c}\|_1
$$

再次用三角不等式 $\|\Delta_{A^*} + x^*_{A^*}\|_1 \geq \|x^*_{A^*}\|_1 - \|\Delta_{A^*}\|_1$，所以：
$$
\|x^*\|_1 - \|\hat{x}\|_1 \leq \|\Delta_{A^*}\|_1 - \|\Delta_{(A^*)^c}\|_1
$$

代回基本不等式：
$$
\frac{1}{2n}\|A\Delta\|_2^2 + \lambda\|\Delta_{(A^*)^c}\|_1 \leq \lambda\|\Delta_{A^*}\|_1 - \frac{1}{n}\langle A\Delta, \varepsilon \rangle
$$

#### 第三步：控制噪声项

三月： $\langle A\Delta, \varepsilon \rangle$ 我倒是会处理了！它是用那个……那个……集成，集成战略？

长夜月：集中不等式，我再次演示一遍：

因为 $\varepsilon$ 是次高斯的，所以 $A^\top\varepsilon$ 的每个分量也是次高斯的。可以用Hoeffding不等式证明，在概率 $1-\delta$ 下：
$$
\frac{1}{n}\|A^\top\varepsilon\|_\infty \leq \lambda_0 := \sigma\sqrt{\frac{2\log(2d/\delta)}{n}}
$$

于是 $-\frac{1}{n}\langle A\Delta, \varepsilon \rangle = -\frac{1}{n}\Delta^\top A^\top\varepsilon \leq \|\Delta\|_1 \cdot \frac{1}{n}\|A^\top\varepsilon\|_\infty \leq \lambda_0\|\Delta\|_1$。

（看一眼被公式哄睡着了的三月）无奈，在这一页笔记上补充上Holder不等式$$p=1,q=\infty$$的使用

由此可以代入得到：
$$
\frac{1}{2n}\|A\Delta\|_2^2 + \lambda\|\Delta_{(A^*)^c}\|_1 \leq \lambda\|\Delta_{A^*}\|_1 + \lambda_0\|\Delta\|_1
$$

#### 第四步：选择 $\lambda$，得到支撑集约束

接下来我们就是利用稀疏性处理掉这个额外引入的项

取正则化参数 $\lambda = 2\lambda_0 = 2\sigma\sqrt{\frac{2\log(2d/\delta)}{n}}$，则 $\lambda_0 = \lambda/2$，所以：
$$
\frac{1}{2n}\|A\Delta\|_2^2 + \lambda\|\Delta_{(A^*)^c}\|_1 \leq \lambda\|\Delta_{A^*}\|_1 + \frac{\lambda}{2}\left(\|\Delta_{A^*}\|_1 + \|\Delta_{(A^*)^c}\|_1\right)
$$

整理得：
$$
\frac{1}{2n}\|A\Delta\|_2^2 + \frac{\lambda}{2}\|\Delta_{(A^*)^c}\|_1 \leq \frac{3\lambda}{2}\|\Delta_{A^*}\|_1
$$

左边两项都是非负的，所以：
$$
\|\Delta_{(A^*)^c}\|_1 \leq 3\|\Delta_{A^*}\|_1
$$

三月七（猛地惊醒）这就是说，支撑集外的误差被支撑集内的误差控制了？

长夜月：对！这就是稀疏估计的**集中性**：L1正则化不会在非支撑集上产生太大的误差。用 $\ell_2$ 范数表述就是（由 Cauchy-Schwarz，$\|\Delta_{A^*}\|_1 \leq \sqrt{s}\|\Delta_{A^*}\|_2$）：
$$
\|\Delta_{(A^*)^c}\|_2 \leq \|\Delta_{(A^*)^c}\|_1 \leq 3\|\Delta_{A^*}\|_1 \leq 3\sqrt{s}\|\Delta_{A^*}\|_2
$$

因此 $\|\Delta\|_2 \leq \|\Delta_{A^*}\|_2 + \|\Delta_{(A^*)^c}\|_2 \leq (1 + 3\sqrt{s})\|\Delta_{A^*}\|_2$。

#### 第五步：RE条件与最终误差界

三月：可是 $\|\Delta_{A^*}\|_2$ 本身怎么控制？

长夜月：这需要对感知矩阵 $A$ 附加一个条件——**限制特征值条件（Restricted Eigenvalue, RE）**：

对满足 $\|\Delta_{(A^*)^c}\|_1 \leq 3\|\Delta_{A^*}\|_1$ 的所有 $\Delta$，有：
$$
\frac{1}{n}\|A\Delta\|_2^2 \geq \gamma^2\|\Delta\|_2^2
$$

其中 $\gamma > 0$ 是限制特征值常数。这个条件要求 $A$ 在”稀疏方向”上的最小奇异值有正的下界——直觉上，感知矩阵需要能区分不同的稀疏信号。

三月：RIP条件和RE条件是什么关系？

长夜月：RIP条件更强：它要求对所有 $s$-稀疏向量 $u$，
$$
(1-\delta_s)\|u\|_2^2 \leq \|Au\|_2^2 \leq (1+\delta_s)\|u\|_2^2
$$
RIP蕴含RE（取 $\gamma^2 = 1 - \delta_{2s}$），但RE更弱、更容易验证。在高维统计中通常只需RE就够了。

结合RE条件和前面的不等式 $\frac{1}{2n}\|A\Delta\|_2^2 \leq \frac{3\lambda}{2}\|\Delta_{A^*}\|_1 \leq \frac{3\lambda\sqrt{s}}{2}\|\Delta_{A^*}\|_2$：

$$
\frac{\gamma^2}{2}\|\Delta\|_2^2 \leq \frac{1}{2n}\|A\Delta\|_2^2 \leq \frac{3\lambda\sqrt{s}}{2}\|\Delta_{A^*}\|_2 \leq \frac{3\lambda\sqrt{s}}{2}\|\Delta\|_2
$$

两边消去 $\|\Delta\|_2$，得到最终**Lasso 误差界**：
$$
\|\hat{x} - x^*\|_2 \leq \frac{3\lambda\sqrt{s}}{\gamma^2} = \frac{3\sigma\sqrt{s}}{\gamma^2}\sqrt{\frac{2\log(2d/\delta)}{n}}
$$

三月：这个结果的含义是什么？

长夜月：注意几个关键点：
1. **误差随样本量 $n$ 增大而衰减**，速率为 $1/\sqrt{n}$
2. **误差只依赖稀疏度 $s$**，不依赖信号维度 $d$——这是压缩感知的核心优势：即使 $d$ 极大，只要信号稀疏（$s$ 小），误差仍然可控
3. **对维度 $d$ 只有对数依赖** $\log d$——这是高维统计的”免费午餐”
4. $\gamma$ 越大（感知矩阵越”好”），误差越小

---

### L1优化怎么求解？近端梯度下降

三月七：所以，引入L1正则项之后问题变得简单了吗？

长夜月：变简单了——但也没有完全变简单。L0问题是NP难的，而L1问题不但在求解上没有问题，而且是一个**凸优化问题**，意味着一定可以求解。但L1范数不可微，所以普通的梯度下降不能直接用。

三月七：不可微？（扔掉手中的《最优化理论》）那我之前学的那些一阶优化条件完全没用了？在0那个点连导数都没有

长夜月：没有导数就需要创造导数所以我们引入一个关键工具——**次微分**。我们这里考虑凸函数，即使不可微，我们也可以定义”次梯度”：如果对所有的 $y$ 都有
$$
f(y) \geq f(x) + z^\top (y - x)
$$
那么 $z$ 就叫做 $f$ 在 $x$ 处的次微分，记作 $z \in \partial f(x)$。

次微分有两个好性质：
- **线性组合**：$\partial(\lambda f + \gamma g)(x) = \lambda\,\partial f(x) + \gamma\,\partial g(x)$
- **可微时退化为梯度**：若 $f$ 可微且凸，则 $\partial f(x) = \{\nabla f(x)\}$

三月：我感觉就是在曲线“下方”所有过这一点的“切平面”，就是只在这一点相交为例的。这和微分确实很像啊，毕竟都像是求切线。

但是次微分对于不可微函数时可以是不唯一的。比如说绝对值x在原点处，很多直线都在这下方。

所以优化条件就变成了 $0 \in \partial f(x^*)$？

长夜月：对！以绝对值函数为例，根据定义 $|y| \geq |x| + z(y - x)$ 对所有 $y$：
- $x > 0$ 时：取 $z = 1$，右边 $= x + (y-x) = y \leq |y|$，所以 $\partial|x| = \{1\}$
- $x < 0$ 时：取 $z = -1$，同理 $\partial|x| = \{-1\}$
- $x = 0$ 时：$|y| \geq zy$ 对所有 $y$ 成立，需要 $-1 \leq z \leq 1$，所以 $\partial|x| = [-1, 1]$

三月：在0处次微分是一个区间而不是一个点，这就能让0成为最优解的条件……

长夜月：所以对于回到我们的压缩感知问题：
$$
\hat{x} = \arg\min_{x} \left( \frac{1}{2n}\|Ax - s\|_2^2 + \lambda\|x\|_1 \right)
$$

光滑项的梯度是 $\frac{1}{n}A^\top(Ax - s)$，L1项的次微分是 $\lambda\,\partial\|x\|_1$（逐分量：$\partial\|x\|_1 = \partial|x_1| \times \cdots \times \partial|x_d|$）。一阶最优性条件：
$$
\frac{1}{n}A^\top(A\hat{x} - s) + \lambda\,\partial\|\hat{x}\|_1 \ni 0
$$

三月：$\partial\|x\|_1$ 不是一个单值函数，怎么求解？

长夜月：这就是**近端梯度下降（Proximal Gradient Descent）**出场的时候了。核心思路是：先对光滑项走一步梯度，再对L1项做”近端算子”处理。

先看一维辅助问题：$f(x) = \frac{1}{2}(x - t)^2 + \lambda|x|$，求 $0 \in \partial f(x^*)$：
- $x > 0$：$\partial f(x) = (x - t) + \lambda$
- $x < 0$：$\partial f(x) = (x - t) - \lambda$
- $x = 0$：$\partial f(0) = [-t - \lambda,\; -t + \lambda]$

解就是**软阈值算子** $S_\lambda(t)$：
$$
S_\lambda(t) = \begin{cases}
0, & |t| \leq \lambda \\
t - \lambda, & t \geq \lambda \\
t + \lambda, & t \leq -\lambda
\end{cases}
$$

三月：当 $|t|$ 比 $\lambda$ 小的时候，直接被”压缩”到0了——这就是L1正则化能产生稀疏解的原因！

长夜月：完全正确。回到一般问题，引入步长 $\tau > 0$，迭代公式为：
$$
x^{(k+1)} = S_{\lambda\tau}\!\left(x^{(k)} - \tau \cdot \frac{1}{n}A^\top(Ax^{(k)} - s)\right)
$$

每一步先沿光滑项的负梯度方向走一步（步长 $\tau$），再用软阈值算子把小的分量归零。等价的不动点形式是：
$$
x^* = S_{\lambda\tau}\!\left(x^* - \tau \cdot \frac{1}{n}A^\top(Ax^* - s)\right)
$$

三月：为什么这个不动点就是最优解？这看上去都不搭吧？

长夜月：一变量变成多变量的你就不会了？那好吧，我们来仔细推导一下。

首先，最优性条件本身是次微分的直接推论。因为目标函数 $f(x) = \frac{1}{2n}\|Ax-s\|_2^2 + \lambda\|x\|_1$ 是两个凸函数之和，一阶最优性条件是：
$$
0 \in \nabla\left(\frac{1}{2n}\|Ax-s\|_2^2\right)\Big|_{x^*} + \lambda\,\partial\|x^*\|_1
= \frac{1}{n}A^\top(Ax^*-s) + \lambda\,\partial\|x^*\|_1
$$

由于 $\|x\|_1 = \sum_{i=1}^d |x_i|$ 是逐分量可分的，次微分也是逐分量的。设 $d_j = \frac{1}{n}[A^\top(Ax^*-s)]_j$，则对每个分量 $j$：

- 若 $x^*_j > 0$：$\partial|x^*_j| = \{1\}$，条件要求 $d_j + \lambda = 0$，即 $d_j = -\lambda$
- 若 $x^*_j < 0$：$\partial|x^*_j| = \{-1\}$，条件要求 $d_j - \lambda = 0$，即 $d_j = \lambda$
- 若 $x^*_j = 0$：$\partial|x^*_j| = [-1,1]$，条件要求 $d_j \in [-\lambda, \lambda]$，即 $|d_j| \leq \lambda$

三月：这和我之前算的一维情况完全对应上了！

长夜月：没错。现在我们来验证不动点。令 $t_j = x^*_j - \tau d_j$，不动点方程说 $x^*_j = S_{\lambda\tau}(t_j)$。

**情况1：$x^*_j > 0$**
此时 $d_j = -\lambda$，所以 $t_j = x^*_j + \tau\lambda > \tau\lambda$。
软阈值算子：$S_{\lambda\tau}(t_j) = t_j - \lambda\tau = x^*_j$。

**情况2：$x^*_j < 0$**
此时 $d_j = \lambda$，所以 $t_j = x^*_j - \tau\lambda < -\tau\lambda$。
软阈值算子：$S_{\lambda\tau}(t_j) = t_j + \lambda\tau = x^*_j$。

**情况3：$x^*_j = 0$**
此时 $|d_j| \leq \lambda$，所以 $|t_j| = |\tau d_j| \leq \tau\lambda$。
软阈值算子：$S_{\lambda\tau}(t_j) = 0 = x^*_j$。

三月：三种情况都成立！所以不动点和最优性条件完全等价！

长夜月：正是如此。至于迭代为什么能收敛到不动点，因为目标函数是凸的，只要步长 $\tau$ 足够小（$\tau < 2n/\|A^\top A\|$），近端梯度迭代就能保证收敛到全局最优解。

三月：L1正则项还可以做分布式优化？

长夜月：是的，由于 $\|x\|_1 = \sum_i |x_i|$ 可以逐分量分解，软阈值算子也可以逐分量独立计算：$x_i^{(k+1)} = S_{\lambda\tau}(d_i^{(k)})$，因此天然适合并行和分布式实现。

## 单点像素照相机

长夜月：醒醒，小三月

三月七：欸，我睡着了吗？我明明是回答了好多的问题的

长夜月扶额：你大概只有在梦里才懂这么多……

不过没有关系，现在我们可以讲到你感兴趣的部分了，就是那个单点相机

三月七：哦，对的对的。（擦干净口水），所以这个单点相机，实际上也是由很多个采样点的操作吧？

长夜月：你在梦里也不算完全没有长进。所谓单点相机，实际上就是有若干个微小的光学镜片，每调整一次角度，就将其反射到采样点。每采样一次，就相当于制造了一个w^Tx.

三月七：我知道，这个采样的次数会远远小于镜片的数目而且这个矩阵是一个稀疏矩阵。

长夜月：是的，然后问题被转化为了一个之前讲的压缩感知问题



##### 彩蛋

让三月七去讲压缩感知？这到底算博识君的义务教育还是啊哈的一时兴起？对此，一位不相干白发轮椅人士只是唐突的在此插了个广告：关注知乎浅草真纪以及她的专栏，今后会发更多的AI4Math，会有更多角色出场，一些不完整的公式会由小号补充



