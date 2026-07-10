---
title: Rademacher 复杂度
created: 2026-07-10
updated: 2026-07-10
type: concept
tags: [rademacher, generalization, concentration-inequality]
sources: [raw/lftp/ch4-rademacher.md]
confidence: high
---

# Rademacher 复杂度

Rademacher 复杂度是衡量函数类"表达能力"的核心工具，直接给出 [[erm|经验风险最小化]] 的泛化误差上界。

## 直觉

Rademacher 复杂度衡量函数类对随机噪声的拟合能力——
如果函数类能很好地拟合纯随机标签，说明它过于复杂，泛化会差。

## 数学形式

对于函数类 $\mathcal{F}$ 和样本 $S = \{z_1, \ldots, z_n\}$：

$$\hat{\mathcal{R}}_S(\mathcal{F}) = \mathbb{E}_{\sigma}\left[\sup_{f \in \mathcal{F}} \frac{1}{n}\sum_{i=1}^n \sigma_i f(z_i)\right]$$

其中 $\sigma_i$ 是独立 Rademacher 随机变量 ($\pm 1$ 等概率)。

## 计算工具

- [[massart-dudley|Massart 引理与 Dudley 积分]] — 有限类到无限类的桥梁
- [[concentration-inequality|集中不等式]] — 从经验 Rademacher 到总体 Rademacher 的转化

## 相关

- [[erm|经验风险最小化]] — Rademacher 复杂度给出 ERM 的泛化保证
- [[massart-dudley|Massart 引理与 Dudley 积分]] — 计算 Rademacher 复杂度
- [[supervised-learning|监督学习]] — 泛化理论框架
