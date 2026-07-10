---
title: 统计计算
created: 2026-07-10
updated: 2026-07-10
type: concept
tags: [monte-carlo, bootstrap, mcmc, r-language]
sources: [raw/lftp/stat-computing-review.md]
confidence: high
---

# 统计计算

用计算机解决统计推断问题的工具箱。核心模块：

## 课程地图

| 模块 | 核心问题 | 工具 |
|------|----------|------|
| 随机数生成 | 从目标分布造样本 | 逆变换法、接受-拒绝法 |
| Monte Carlo 积分 | 积分→期望→数值估计 | 大数定律、方差缩减 |
| 统计模拟 | 评估估计量、区间、检验 | MC 标准误、经验功效 |
| 重抽样 | 偏差/标准误的非参估计 | Bootstrap、Jackknife |
| 数值方法 | 求根、优化、MLE | Newton-Raphson、Fisher Scoring |
| MCMC | 构造平稳分布为目标分布的链 | Metropolis-Hastings、Gibbs |

## 与统计学习的关系

Bootstrap 和 MCMC 是 [[machine-learning|机器学习基础]] 中许多方法的计算基础。
Monte Carlo 积分的思想出现在 [[erm|经验风险最小化]] 的随机梯度下降中。

## 相关

- [[machine-learning|机器学习基础]] — 统计计算是 ML 的计算引擎
- [[data-science|数据科学导论]] — 统计思维与计算方法
