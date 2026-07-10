---
title: 经验风险最小化
created: 2026-07-10
updated: 2026-07-10
type: concept
tags: [erm, generalization, convex-optimization]
sources: [raw/lftp/ch4-erm.md]
confidence: high
---

# 经验风险最小化 (ERM)

ERM 是监督学习的核心范式。算法的意义在于三点：

1. 不知道真正的函数，只是管中窥豹
2. 实数集很大，不可能搜索每一个可测函数
3. 没有无限时间逐点搜索

## 关键概念

### 凸化 (Convexification)
二分类问题中，最优预测可以通过凸替代损失转化为凸优化。

### 风险分解
$$\text{风险} = \text{逼近误差} + \text{估计误差}$$

- **逼近误差**: 函数类的逼近效率，由逼近理论刻画
- **估计误差**: 有限样本带来的误差，由高维概率控制

### 与 Rademacher 复杂度的关系

ERM 的泛化性能由 [[rademacher-complexity|Rademacher 复杂度]] 给出上界。
具体地，通过 [[massart-dudley|Massart 引理与 Dudley 积分]] 可以将 Rademacher 复杂度转化为可计算的量。

## 相关

- [[supervised-learning|监督学习]] — ERM 的框架背景
- [[rademacher-complexity|Rademacher 复杂度]] — ERM 的泛化保证
- [[massart-dudley|Massart 引理与 Dudley 积分]] — Rademacher 复杂度的计算工具
