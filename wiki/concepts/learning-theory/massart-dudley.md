---
title: Massart 引理与 Dudley 积分
created: 2026-07-10
updated: 2026-07-10
type: concept
tags: [rademacher, concentration-inequality, generalization]
sources: [raw/lftp/ch4-4-massart.md]
confidence: high
---

# Massart 引理与 Dudley 积分

这两个工具是将 [[rademacher-complexity|Rademacher 复杂度]] 从有限函数类推广到无限函数类的关键桥梁。

## Massart 引理

对于有限函数类 $\mathcal{F}$，其 Rademacher 复杂度有上界：

$$\hat{\mathcal{R}}_S(\mathcal{F}) \leq \max_{f \in \mathcal{F}} \|f\|_\infty \cdot \sqrt{\frac{2\log|\mathcal{F}|}{n}}$$

核心直觉：函数类越大（$|\mathcal{F}|$ 越大），复杂度越高，但增长速度只是对数级别。

## Dudley 积分

将 Massart 引理推广到无限类：通过"覆盖数"（covering numbers）将无限函数类离散化。

$$\hat{\mathcal{R}}_S(\mathcal{F}) \leq \inf_{\delta > 0} \left(4\delta + 12 \int_{\delta}^{\infty} \sqrt{\frac{\log N(\varepsilon, \mathcal{F}, \|\cdot\|_n)}{n}} d\varepsilon\right)$$

其中 $N(\varepsilon, \mathcal{F}, \|\cdot\|_n)$ 是 $\varepsilon$-覆盖数。

## 意义

这两个结果使得我们可以用**度量熵**（metric entropy）来刻画函数类的复杂度，从而为 ERM 提供可计算的泛化界。

## 相关

- [[rademacher-complexity|Rademacher 复杂度]] — 被量化的对象
- [[erm|经验风险最小化]] — 泛化界的应用场景
- [[concentration-inequality|集中不等式]] — 概率工具
