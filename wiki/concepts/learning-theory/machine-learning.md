---
title: 机器学习基础
created: 2026-07-10
updated: 2026-07-10
type: concept
tags: [overview, model, training]
sources: [raw/lftp/machine-learning.md]
confidence: high
---

# 机器学习基础

机器学习的三要素：**模型、策略、算法**。

## 主要范式

- **监督学习**: 有标注数据，学习 $f: X \to Y$。见 [[supervised-learning|监督学习]]
- **无监督学习**: 无标注，发现数据结构
- **半监督学习**: 部分标注
- **强化学习**: 通过与环境交互学习策略

## 核心问题

1. **泛化**: 训练集表现好 $\neq$ 测试集表现好 — [[erm|经验风险最小化]]
2. **过拟合**: 模型太复杂，记住了噪声 — [[rademacher-complexity|Rademacher 复杂度]] 给出理论上界
3. **偏差-方差权衡**: 简单模型高偏差低方差，复杂模型反之

## 相关

- [[supervised-learning|监督学习]] — 监督学习理论
- [[erm|经验风险最小化]] — 学习范式
- [[sparse-feature-learning|稀疏学习与特征学习]] — 高维场景
- [[statistical-computing|统计计算]] — 计算工具
