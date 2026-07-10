---
title: 稀疏学习与特征学习
created: 2026-07-10
updated: 2026-07-10
type: concept
tags: [sparse-learning, feature-selection, regularization]
sources: [raw/lftp/sparse-feature-learning.md]
confidence: medium
---

# 稀疏学习与特征学习

高维数据中，真正重要的特征往往只占少数。稀疏学习就是找到这些特征。

## 核心思想

通过正则化（如 $\ell_1$ 范数）迫使模型只使用少数特征：

$$\min_{\beta} \sum_{i=1}^n \ell(y_i, \beta^T x_i) + \lambda \|\beta\|_1$$

## 关键概念

- **LASSO**: $\ell_1$ 正则化线性回归，自动做特征选择
- **Ridge**: $\ell_2$ 正则化，收缩但不选择
- **Elastic Net**: $\ell_1 + \ell_2$ 混合
- **特征选择 vs 特征提取**: 前者保留原始特征，后者（如 PCA）生成新特征

## 与统计学习理论的关系

稀疏性假设可以显著降低 [[rademacher-complexity|Rademacher 复杂度]]，
从而在 [[erm|经验风险最小化]] 框架下获得更好的泛化保证。

## 相关

- [[erm|经验风险最小化]] — 加了正则化的 ERM 就是稀疏学习
- [[rademacher-complexity|Rademacher 复杂度]] — 稀疏性的泛化优势
- [[machine-learning|机器学习基础]] — 概念在 ML 中的位置
