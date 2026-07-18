# 统计计算总复习

> 目标：先把整门课压缩成一套“看到题目就知道该套哪个模板”的复习工具。本文优先服务期末复习，暂不追求教材式完整。

## 使用方式

1. 先看“课程地图”，知道整门课在做什么。
2. 复习时优先按“模板”而不是按章节推进。
3. 每个模板至少做到三件事：
   - 知道什么时候用
   - 能说出核心公式
   - 能闭卷写出最小 R 代码骨架

---

# 0. 课程地图

| 模块 | 核心问题 | 典型章节 |
|---|---|---|
| R 基础 | 怎么读写数据、作图、调用基础统计函数 | Ch1 |
| 随机变量生成 | 怎样从目标分布中造样本 | Ch2 |
| Monte Carlo 积分 | 怎样把积分写成期望并数值估计 | Ch3 |
| Monte Carlo 统计模拟 | 怎样评估估计量、区间和检验 | Ch4 |
| 重抽样 | 怎样用 Bootstrap / Jackknife 估计偏差、标准误和区间 | Ch5 |
| 数值方法与 MLE | 怎样求根、优化、做数值极大似然估计 | Ch6 |
| MCMC 方法 | 怎样构造以目标分布为平稳分布的马尔科夫链 | Ch7 |

考试复习优先级建议：

1. Ch2–Ch5：必须熟练
2. Ch6–Ch7：标准算法题，适合通过代码模板拿分
3. Ch1：基础保底，最后扫清语法

---

# 1. R 基础速查

## 1.1 文件读写

```r
x = 1:100
write(x, file = "x.txt")
rm(x)
x = scan("x.txt")

sink("x.txt")
print(x)
sink()
```

```r
dat = read.csv("2015city.csv", header = TRUE)
write.csv(dat, "out.csv", row.names = FALSE)
```

## 1.2 常见构造命令

```r
rep(1:5, each = 5)
rep(1:5, times = 5)
seq(1, 10, by = 2)
sample(1:10, size = 5, replace = TRUE)
```

## 1.3 常见图形与统计命令

```r
hist(x, prob = TRUE)
barplot(x)
qqnorm(x); qqline(x)
fit = lm(Murder ~ Population + Illiteracy + Income + Frost, data = dat)
summary(fit)
```

---

# 2. 模板 A：逆变换法

## 适用场景

- 已知分布函数 \(F(x)\)
- 能显式求出 \(F^{-1}(u)\)
- 常用于连续型分布，也可处理简单离散分布

## 核心思想

若 \(U \sim U(0,1)\)，则

\[
X = F^{-1}(U)
\]

服从目标分布 \(F\)。

## 最小代码模板

```r
r.target = function(n) {
  u = runif(n)
  x = F_inv(u)
  return(x)
}
```

## 典型例子：指数分布

若 \(X \sim \mathrm{Exp}(\lambda)\)，则

\[
F(x)=1-e^{-\lambda x}, \qquad X = -\frac{\log U}{\lambda}.
\]

```r
myrexp = function(n, lambda) {
  u = runif(n)
  x = -log(u) / lambda
  return(x)
}
```

## 常见变式

- Pareto 分布
- Geometric 分布
- Logarithmic 分布
- 离散分布的累积分布逆变换

## 易错点

- 先确认 \(U\) 的定义域是 \((0,1)\)
- 求逆时不要把参数放错
- 离散型分布通常不是普通代数求逆，而是比较累计概率

---

# 3. 模板 B：接受-拒绝法

## 适用场景

- 目标密度 \(f(x)\) 不方便直接抽样
- 能找到容易抽样的 proposal density \(g(x)\)
- 存在常数 \(M\)，使 \(f(x) \le M g(x)\)

## 核心思想

1. 先从 \(g\) 中生成候选样本 \(Y\)
2. 再生成 \(U \sim U(0,1)\)
3. 若

\[
U \le \frac{f(Y)}{M g(Y)},
\]

则接受 \(Y\)

## 最小代码模板

```r
r.ar = function(n) {
  y = numeric(n)
  k = 0
  while (k < n) {
    cand = rg(1)
    u = runif(1)
    if (u <= f(cand) / (M * g(cand))) {
      k = k + 1
      y[k] = cand
    }
  }
  return(y)
}
```

## 典型题型

- 用接受-拒绝法生成 Beta 分布样本
- 已知某个多项式型密度，在区间上用均匀分布作 proposal

## 易错点

- 没有真正检查 \(M\) 是否足够大
- 接受概率里少写了 \(g(y)\)
- proposal 的支持集必须覆盖目标分布支持集

---

# 4. 模板 C：变换法、混合分布与多元正态

## 4.1 变换法

## 适用场景

- 已知一个容易抽样的变量 \(Y\)
- 目标变量可写成 \(X = h(Y)\)

## 最小代码模板

```r
r.target = function(n) {
  y = rbase(n)
  x = h(y)
  return(x)
}
```

## 典型例子

```r
# 对数正态：若 Y ~ N(mu, sigma^2)，则 X = exp(Y)
x = exp(rnorm(n, mean = mu, sd = sigma))
```

## 4.2 混合分布

若

\[
X \sim pF_1 + (1-p)F_2,
\]

则可先抽类别，再按类别抽样。

```r
k = rbinom(n, size = 1, prob = p)
x = numeric(n)
x[k == 1] = rnorm(sum(k == 1), mean = 0, sd = 1)
x[k == 0] = rnorm(sum(k == 0), mean = 3, sd = 1)
```

## 4.3 多元正态

若 \(Z \sim N(0, I)\)，且 \(R R^T = \Sigma\)，则

\[
X = \mu + ZR
\]

服从 \(N(\mu, \Sigma)\)。

### Cholesky 版本

```r
rmvn.chol = function(n, mu, Sigma) {
  d = length(mu)
  Q = chol(Sigma)
  Z = matrix(rnorm(n * d), nrow = n, ncol = d)
  X = Z %*% Q + matrix(mu, n, d, byrow = TRUE)
  return(X)
}
```

## 易错点

- Cholesky 里注意 R 的矩阵方向
- 混合分布必须“先抽类别，再抽条件分布”
- 多元正态题常要求比较 eigen / SVD / Cholesky 三种分解

---

# 5. 模板 D：Monte Carlo 积分

## 适用场景

- 积分难以解析计算
- 能把积分写成某个随机变量函数的期望

## 核心思想

若 \(X \sim p(x)\)，则

\[
\theta = \int g(x) p(x) dx = E[g(X)]
\]

于是

\[
\hat\theta = \frac1m \sum_{i=1}^m g(X_i)
\]

且

\[
\widehat{\mathrm{Var}}(\hat\theta)=\frac{s_g^2}{m}.
\]

## 最小代码模板

```r
m = 10000
x = rsample(m)
g = target_function(x)
theta.hat = mean(g)
var.hat = var(g) / m
se.hat = sd(g) / sqrt(m)
```

## 区间积分常见改写

\[
\int_a^b h(x) dx = (b-a) E[h(U)], \quad U \sim U(a,b).
\]

```r
u = runif(m, min = a, max = b)
theta.hat = (b - a) * mean(h(u))
```

## 易错点

- 忘记乘区间长度 \((b-a)\)
- 估计量和估计量方差混淆
- hit-or-miss 与普通 MC 的估计对象不同

---

# 6. 模板 E：方差缩减

## 6.1 对偶变量法

## 适用场景

- 积分函数具有一定单调性
- 可以让两个样本负相关

## 核心思想

用 \(U\) 与 \(1-U\) 配对，构造

\[
\hat\theta = \frac12 \bigl(g(U)+g(1-U)\bigr).
\]

```r
u = runif(m / 2)
v = 1 - u
gv = c(g(u), g(v))
theta.hat = mean(gv)
```

## 6.2 控制变量法

若已知 \(E[B]\)，用

\[
T = A + c(B - E[B])
\]

其中最优系数

\[
c^* = -\frac{\mathrm{Cov}(A,B)}{\mathrm{Var}(B)}.
\]

```r
u = runif(m)
A = g(u)
B = h(u)
c.star = -cov(A, B) / var(B)
T = A + c.star * (B - EB)
theta.hat = mean(T)
```

## 6.3 重要抽样

若

\[
\theta = \int g(x) dx = \int \frac{g(x)}{f(x)} f(x) dx,
\]

则从 \(f\) 抽样：

```r
x = rf(m)
w = g(x) / f(x)
theta.hat = mean(w)
```

## 6.4 分层抽样

把区域分层后，各层分别抽样，再加权平均。

```r
k = 10
T = numeric(k)
for (j in 1:k) {
  u = runif(m / k, min = (j - 1) / k, max = j / k)
  T[j] = mean(g(u))
}
theta.hat = mean(T)
```

## 易错点

- 对偶变量法不是“变量变两个”，而是要形成负相关
- 控制变量法里控制变量的期望必须已知
- 重要抽样选的 proposal 要和 integrand 形状接近，否则未必降方差

---

# 7. 模板 F：Monte Carlo 统计模拟

## 7.1 估计量的 MSE

```r
m = 1000
est = numeric(m)
for (j in 1:m) {
  x = rsample(n)
  est[j] = statistic(x)
}
mse.hat = mean((est - theta)^2)
```

## 7.2 置信区间覆盖率

```r
m = 1000
cover = numeric(m)
for (j in 1:m) {
  x = rsample(n)
  ci = construct_ci(x)
  cover[j] = (theta >= ci[1] & theta <= ci[2])
}
coverage = mean(cover)
```

## 7.3 第一类错误率

```r
m = 1000
reject = numeric(m)
for (j in 1:m) {
  x = sample_under_H0(n)
  reject[j] = as.integer(test_statistic(x) > critical_value)
}
type1.error = mean(reject)
```

## 7.4 功效

```r
m = 1000
reject = numeric(m)
for (j in 1:m) {
  x = sample_under_H1(n)
  reject[j] = as.integer(test_statistic(x) > critical_value)
}
power = mean(reject)
```

## 易错点

- 覆盖率必须在真实参数固定的前提下重复抽样
- 第一类错误率要在 \(H_0\) 下模拟
- 功效要在 \(H_1\) 下模拟
- `mean(logical_vector)` 本质上就是经验概率

---

# 8. 模板 G：Bootstrap 与 Jackknife

## 8.1 Bootstrap 点估计、偏差、标准误

## 适用场景

- 已有样本 \(x_1,\dots,x_n\)
- 统计量 \(\hat\theta = t(x)\) 的解析分布不好求

## 核心思想

对原样本有放回重抽样，得到

\[
\hat\theta_1^*, \dots, \hat\theta_B^*.
\]

然后估计

\[
\widehat{\mathrm{bias}} = \bar\theta^* - \hat\theta,
\qquad
\widehat{se}_B = sd(\hat\theta_1^*,\dots,\hat\theta_B^*).
\]

## 最小代码模板

```r
theta = function(x) {
  # return statistic of x
}

B = 2000
n = length(x)
theta.hat = theta(x)
theta.b = numeric(B)

for (b in 1:B) {
  ind = sample(1:n, size = n, replace = TRUE)
  xb = x[ind]
  theta.b[b] = theta(xb)
}

bias.hat = mean(theta.b) - theta.hat
se.hat = sd(theta.b)
```

## 8.2 三种常见 Bootstrap 区间

```r
alpha = 0.05

# Normal
ci.normal = c(
  theta.hat - qnorm(1 - alpha / 2) * se.hat,
  theta.hat + qnorm(1 - alpha / 2) * se.hat
)

# Percentile
ci.perc = quantile(theta.b, c(alpha / 2, 1 - alpha / 2))

# Basic
q = quantile(theta.b, c(alpha / 2, 1 - alpha / 2))
ci.basic = c(2 * theta.hat - q[2], 2 * theta.hat - q[1])
```

## 8.3 Bootstrap-t 区间

### 核心算法

1. 原样本上算 \(\hat\theta\)
2. 外层 Bootstrap 第 \(b\) 次，得到样本 \(x_b^*\) 与统计量 \(\hat\theta_b^*\)
3. 在 \(x_b^*\) 上再做内层 Bootstrap，估计 \(se_b^*\)
4. 构造

\[
t_b^* = \frac{\hat\theta_b^* - \hat\theta}{se_b^*}
\]

5. 取 \(t_b^*\) 分位数反推区间

```r
boot.t.ci = function(x, B = 500, R = 100, level = 0.95, statistic) {
  x = as.matrix(x)
  n = nrow(x)
  stat = numeric(B)
  se = numeric(B)

  boot.se = function(dat, R, statistic) {
    m = nrow(dat)
    th = replicate(R, {
      ind = sample(1:m, size = m, replace = TRUE)
      statistic(dat[ind, , drop = FALSE])
    })
    sd(th)
  }

  for (b in 1:B) {
    ind = sample(1:n, size = n, replace = TRUE)
    xb = x[ind, , drop = FALSE]
    stat[b] = statistic(xb)
    se[b] = boot.se(xb, R = R, statistic = statistic)
  }

  stat0 = statistic(x)
  se0 = sd(stat)
  t.stats = (stat - stat0) / se
  alpha = 1 - level
  q = quantile(t.stats, c(alpha / 2, 1 - alpha / 2), type = 1)
  ci = rev(stat0 - q * se0)
  return(ci)
}
```

## 8.4 Jackknife

```r
n = length(x)
theta.jack = numeric(n)
for (i in 1:n) {
  theta.jack[i] = theta(x[-i])
}

bias.jack = (n - 1) * (mean(theta.jack) - theta.hat)
se.jack = ((n - 1) / sqrt(n)) * sd(theta.jack)
```

## 易错点

- Bootstrap 是“对样本再抽样”，不是对分布重新抽样
- Jackknife 是“每次删一个”
- Bootstrap-t 是双层 Bootstrap，别和普通 percentile 区间混掉
- `drop = FALSE` 对矩阵型数据很有用

---

# 9. 模板 H：数值方法与 MLE

## 9.1 二分法

```r
bisection = function(f, a, b, eps = 1e-8, maxit = 1000) {
  stopifnot(f(a) * f(b) < 0)
  for (it in 1:maxit) {
    mid = (a + b) / 2
    if (abs(f(mid)) < eps) break
    if (f(a) * f(mid) < 0) {
      b = mid
    } else {
      a = mid
    }
  }
  return(mid)
}
```

## 9.2 Brent 法

```r
uniroot(f, lower = a, upper = b)$root
```

## 9.3 Newton 法

```r
newton = function(f, df, x0, eps = 1e-8, maxit = 1000) {
  x = x0
  for (it in 1:maxit) {
    x.new = x - f(x) / df(x)
    if (abs(x.new - x) < eps) break
    x = x.new
  }
  return(x.new)
}
```

## 9.4 一维优化

```r
optimize(f, lower = a, upper = b, maximum = TRUE)
```

## 9.5 MLE

```r
mlogL = function(theta) {
  # return negative log-likelihood
}

library(stats4)
fit = mle(mlogL, start = list(theta = theta0))
summary(fit)
```

## 易错点

- `mle` 默认做的是极小化负对数似然
- Newton 法依赖导数，初值不好时可能发散
- `uniroot` 要求区间端点异号

---

# 10. 模板 I：马尔科夫链蒙特卡罗（MCMC）

## 10.1 为什么使用 MCMC

当目标分布 \(\pi(x)\) 很难直接抽样时，可以构造一条马尔科夫链

\[
X_1, X_2, \dots, X_m,
\]

使它的平稳分布为 \(\pi\)。链运行足够久后，保留下来的样本可近似看作来自目标分布，并用

\[
\frac{1}{m}\sum_{t=1}^m h(X_t)
\]

估计 \(E_\pi[h(X)]\)。

MCMC 样本通常有相关性，不是独立同分布样本。因此需要关注 burn-in、混合速度、自相关和有效样本量。

## 10.2 一般 Metropolis-Hastings 方法

### 适用场景

- 目标密度 \(\pi(x)\) 只知道到一个比例常数
- 能从提议分布 \(q(y\mid x)\) 中抽样
- 提议分布可以不对称

### 核心算法

已知当前状态 \(X_t=x\)：

1. 从 \(q(y\mid x)\) 生成候选值 \(Y=y\)
2. 计算接受概率

\[
\alpha(x,y)
=\min\left\{1,
\frac{\pi(y)q(x\mid y)}
{\pi(x)q(y\mid x)}
\right\}
\]

3. 生成 \(U\sim U(0,1)\)
4. 若 \(U\le \alpha(x,y)\)，令 \(X_{t+1}=y\)；否则令 \(X_{t+1}=x\)

目标密度中的未知归一化常数会在比值中约掉。

### 最小代码模板

```r
mh = function(m, x0, target, proposal, dproposal) {
  x = numeric(m)
  x[1] = x0
  accepted = 0

  for (i in 2:m) {
    current = x[i - 1]
    cand = proposal(current)

    log.r = log(target(cand)) + log(dproposal(current, cand)) -
      log(target(current)) - log(dproposal(cand, current))

    if (log(runif(1)) <= min(0, log.r)) {
      x[i] = cand
      accepted = accepted + 1
    } else {
      x[i] = current
    }
  }

  return(list(chain = x, accept.rate = accepted / (m - 1)))
}
```

用对数接受比 `log.r` 比直接计算密度乘积更稳定，可以减少上溢和下溢。

## 10.3 Metropolis 方法：对称随机游走

若提议分布满足

\[
q(y\mid x)=q(x\mid y),
\]

则提议密度约掉，接受概率简化为

\[
\alpha(x,y)=\min\left\{1,\frac{\pi(y)}{\pi(x)}\right\}.
\]

常见对称提议为

\[
Y\mid X_t=x\sim N(x,b^2).
\]

### 标准 Cauchy 分布示例

目标密度为

\[
\pi(x)=\frac{1}{\pi(1+x^2)}.
\]

```r
target = function(x) dcauchy(x)

m = 10000
b = 2
x = numeric(m)
x[1] = 0
accepted = 0

for (i in 2:m) {
  cand = rnorm(1, mean = x[i - 1], sd = b)
  alpha = min(1, target(cand) / target(x[i - 1]))

  if (runif(1) <= alpha) {
    x[i] = cand
    accepted = accepted + 1
  } else {
    x[i] = x[i - 1]
  }
}

accept.rate = accepted / (m - 1)
sample.after.burnin = x[(0.2 * m + 1):m]
```

### 步长 \(b\) 的影响

- \(b\) 太小：接受率高，但链移动慢，相邻样本高度相关
- \(b\) 太大：候选值经常落入低密度区，拒绝率高，链长时间不动
- 比较生成器时不能只看接受率，还要看轨迹、自相关和有效样本量

## 10.4 Independence Metropolis-Hastings

若提议分布与当前状态无关，即

\[
q(y\mid x)=g(y),
\]

则接受概率为

\[
\alpha(x,y)
=\min\left\{1,
\frac{\pi(y)g(x)}
{\pi(x)g(y)}
\right\}.
\]

### 最小代码模板

```r
independence_mh = function(m, x0, target, proposal, dproposal) {
  x = numeric(m)
  x[1] = x0
  accepted = 0

  for (i in 2:m) {
    cand = proposal()
    current = x[i - 1]
    alpha = min(
      1,
      target(cand) * dproposal(current) /
        (target(current) * dproposal(cand))
    )

    if (runif(1) <= alpha) {
      x[i] = cand
      accepted = accepted + 1
    } else {
      x[i] = current
    }
  }

  return(list(chain = x, accept.rate = accepted / (m - 1)))
}
```

独立提议 \(g\) 应尽量接近目标分布 \(\pi\)，并覆盖目标分布的重要区域和尾部。否则链可能混合很慢。

## 10.5 Rayleigh 分布的 MH 题型

Rayleigh 分布密度为

\[
\pi(x)=
\begin{cases}
\dfrac{x}{\sigma^2}\exp\left(-\dfrac{x^2}{2\sigma^2}\right), & x\ge 0,\\
0, & x<0.
\end{cases}
\]

可使用一般 MH 方法，并选择只在正数范围取值的提议分布。例如题目指定

\[
Y\mid X_t=x\sim \operatorname{Gamma}(x,1),
\]

则接受概率必须保留正向与反向提议密度：

\[
\alpha(x,y)
=\min\left\{1,
\frac{\pi(y)g(x\mid y)}
{\pi(x)g(y\mid x)}
\right\}.
\]

```r
rayleigh = function(x, sigma) {
  ifelse(
    x >= 0,
    x / sigma^2 * exp(-x^2 / (2 * sigma^2)),
    0
  )
}

# Gamma(shape = current, rate = 1) proposal
cand = rgamma(1, shape = current, rate = 1)
alpha = min(
  1,
  rayleigh(cand, sigma) * dgamma(current, shape = cand, rate = 1) /
    (rayleigh(current, sigma) * dgamma(cand, shape = current, rate = 1))
)
```

注意：`rchisq(1, df = current)` 并不等于
`rgamma(1, shape = current, rate = 1)`；卡方分布对应的 Gamma 参数为
`shape = current / 2, rate = 1 / 2`。以当前状态作为 Gamma 的形状参数时，
初始值也必须严格大于 0。

## 10.6 Burn-in 与生成器表现诊断

### 常用诊断代码

```r
burn = floor(0.2 * m)
y = x[(burn + 1):m]

# 轨迹图：看链是否稳定、是否长时间不动
plot(x, type = "l")

# 自相关图：衰减越快通常越好
acf(y)

# 边际分布与目标密度
hist(y, prob = TRUE, breaks = "Scott")
curve(target(x), add = TRUE)

# 样本分位数与理论分位数比较
qqplot(qcauchy(ppoints(length(y))), sort(y))
abline(0, 1)
```

### 比较两个 MCMC 生成器

至少比较以下指标：

1. 接受率与拒绝率
2. 轨迹图是否快速进入稳定区域
3. 链是否频繁移动，是否出现长时间重复值
4. 自相关衰减速度
5. 直方图、QQ 图与目标分布的吻合程度
6. Monte Carlo 估计是否稳定

## 10.7 第七章习题分类

| 题型 | 应使用的模板 | 比较重点 |
|---|---|---|
| Rayleigh，改变 \(\sigma\) | 一般 MH | 参数变化对混合与接受率的影响 |
| Rayleigh，Gamma 状态依赖提议 | 一般 MH | 不能约掉提议密度 |
| 标准 Cauchy，对称随机游走提议 | Metropolis | 步长与自相关 |
| 标准 Cauchy，独立提议 | Independence MH | 提议分布与目标分布的匹配程度 |
| 混合正态中混合比例 \(p\) 的估计 | Independence MH / 贝叶斯后验抽样 | 后验均值、轨迹与直方图 |

## 易错点

- 一般 MH 中漏写反向提议密度 \(q(x\mid y)\)
- 只有提议分布对称时，才能把接受概率简化为 \(\pi(y)/\pi(x)\)
- Independence MH 不是“每一步都接受的独立抽样”，它仍然需要接受-拒绝判断
- 比值大于 1 时应使用 `min(1, ratio)`
- 拒绝候选值后必须保留当前状态，不能丢掉这一轮
- burn-in 是丢弃前段样本，不是让样本变成独立样本
- MCMC 样本有相关性，样本量大不等于有效样本量大
- 画理论密度或 QQ 图时，参数必须与生成样本时的参数一致
- 密度乘积很小时优先计算对数接受比
- 状态依赖 Gamma 提议的形状参数必须大于 0，不能从 0 开始链

---

# 11. 复习优先级与下一步

## 最先闭卷复写的模板

1. 逆变换法
2. 接受-拒绝法
3. Monte Carlo 积分
4. 控制变量 / 重要抽样
5. 覆盖率 / 第一类错误率 / 功效
6. Bootstrap 点估计、区间、Bootstrap-t
7. MH / Metropolis / Independence MH

## 建议的复习动作

- 第 1 轮：看懂模板
- 第 2 轮：对照 PDF 习题，把每道题归类到模板
- 第 3 轮：不看答案，闭卷写模板
- 第 4 轮：做一页“常错点清单”

## 这份文档后续可以继续补的内容

- 每个模板再追加 1 个代表题
- 给 Ch2–Ch7 各做一页“章节摘要”
- 另开一页“R 常用函数速查表”
- 把真正考试会用到的代码进一步压成更短的速记版 
