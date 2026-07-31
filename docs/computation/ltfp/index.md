# 统计学习理论 (LFTP) 笔记

以 Francis Bach *Learning Theory from First Principles* (LFTP) 为主线的精读笔记。
从第一性原理出发，统一 PAC 学习、Rademacher 复杂度、核方法等经典框架。

---

## Part I — 基础 (Ch1–Ch3)

| 章节 | 笔记 | 状态 |
|------|------|------|
| Ch1 数学基础 | [再论集中不等式](ch1-concentration.md) | ✅ |
| Ch1 数学基础 | [Bernstein 不等式与极大值期望](ch1-bernstein-maximum.md) | ✅ |
| Ch1–Ch2 数学基础 | [优化基础 (整理版)](ch1-2-optimization.md) | ✅ |
| Ch1–Ch2 数学基础 | [优化基础 (手写转录)](ch1-2-optimization-raw.md) | ✅ |
| Ch2 监督学习导论 | [监督学习导论](ch2-supervised-learning.md) | ✅ |
| Ch3 线性最小二乘回归 | [PCA 与主成分回归](ch3-pca-regression.md) | ✅ |

## Part II — 核心理论 (Ch4–Ch9)

| 章节 | 笔记 | 状态 |
|------|------|------|
| Ch4 经验风险最小化 | [经验风险最小化](ch4-erm.md) | ✅ |
| Ch4 经验风险最小化 | [Rademacher 复杂度](ch4-rademacher.md) | ✅ |
| Ch4.4 经验风险最小化 | [Massart 引理与 Dudley 积分](ch4-4-massart.md) | ✅ |
| Ch5 机器学习优化 | [优化简介](ch5-optimization-intro.md) | ✅ |
| Ch5.3 机器学习优化 | [非光滑梯度方法](ch5-3-nonsmooth.md) | ✅ |
| Ch5.3 机器学习优化 | [Exercises 5.22–5.25](ch5-3-exercises.md) | ✅ |
| Ch5.4 机器学习优化 | [随机梯度下降](ch5-4-sgd.md) | ✅ |
| Ch5.4 机器学习优化 | [Exercises 5.29–5.30](ch5-4-exercises.md) | ✅ |
| Ch6 局部平均方法 | — | ❌ 待补 |
| Ch7 核方法 | — | ❌ 待补 |
| Ch8 稀疏方法 | — | ❌ 待补 |
| Ch9 神经网络 | — | ❌ 待补 |

## Part III — 进阶 (Ch10–Ch15)

全书第三部分，涵盖集成学习、在线学习、无监督学习、因果推断等进阶主题，笔记尚未开始。

---

## 背景补充

| 主题 | 说明 |
|------|------|
| [统计学习理论（概念地图）](learning-theory.md) | 概率工具 → 次高斯 → Bayes 最优 → 覆盖数 → Bernstein 快速率；跨章统一视角 |
| [机器学习基础](machine-learning.md) | 监督/无监督学习、泛化、正则化等入门概念 |
| [稀疏学习与特征学习](sparse-feature-learning.md) | L1 正则化、特征选择、字典学习 |
| [数据科学导论](data-science-intro.md) | 数据科学核心方法、FFT、压缩感知 |

---

## 统计计算

统计计算内容已独立为单独专题，见 [统计计算](../stat-computing.md) 与 [统计计算总复习](../stat-computing-review.md)。

---

*最后更新：2026-07-18*
