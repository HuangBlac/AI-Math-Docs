# 统计学习理论 (LFTP) 笔记

以 Francis Bach *Learning Theory from First Principles* (LFTP) 为主线的精读笔记。
从第一性原理出发，统一 PAC 学习、Rademacher 复杂度、核方法等经典框架。

---

## Part I — 基础 (Ch1–Ch3)

| 章节 | 笔记 | 状态 |
|------|------|------|
| Ch1 数学基础 | [再论集中不等式](ch1.2.2-1.2.3-concentration.md) | ✅ |
| Ch1 数学基础 | [Bernstein 不等式与极大值期望](ch1.2.1-bernstein-maximum.md) | ✅ |
| Ch1–Ch5 跨章基础 | [风险分解、优化与数学预备](ch1.1-1.2.0-optimization.md) | ⚠️ 跨章 |
| Ch2 监督学习导论 | [监督学习导论（Ch2.1–2.5）](ch2.1-2.5-supervised-learning.md) | ✅ |
| Ch3 线性最小二乘回归 | [PCA 与主成分回归（§3.9）](ch3.9-pca-regression.md) | ✅ |

## Part II — 核心理论 (Ch4–Ch9)

| 章节 | 笔记 | 状态 |
|------|------|------|
| Ch4.1–4.4.3 经验风险最小化 | [风险凸化与误差分解](ch4.1-4.4.3.md) | ⚠️ 4.1.4 缺失 |
| Ch4.4.4–4.5 经验风险最小化 | [覆盖数与 Rademacher 导入](ch4.4.4-4.5.0.md) | ⚠️ 习题稀缺 |
| Ch4.5.1–4.5.3 经验风险最小化 | [Rademacher 复杂度](ch4.5.1-4.5.3.md) | ⚠️ 标题待补 |
| Ch5 机器学习优化 | [优化简介（§5.1–5.2）](ch5.1-5.2-optimization.md) | ✅ |
| Ch5.3 机器学习优化 | [非光滑梯度方法](ch5.3-nonsmooth.md) | ✅ |
| Ch5.4 机器学习优化 | [随机梯度下降（§5.4）](ch5.4.0-sgd.md) | ✅ |
| Ch5.4.1 机器学习优化 | [强凸 SGD](ch5.4.1-strong-convex-sgd.md) | ✅ |
| Ch6.1–6.3 局部平均方法 | [估计器与一致性分析](ch6.1-6.3-local-averaging.md) | 🔶 手写稿整理；习题保留原状 |
| Ch6.4–6.5 局部平均方法 | [普遍一致性与高阶光滑性](ch6.4-6.5-universal-consistency.md) | 🔶 手写稿整理；构造未补完 |
| Ch7.2–7.3 核方法 | [表示定理、核构造与 Mercer 特征](ch7.2-representer-kernel-foundations.md) | 🔶 新手写稿；P7.3 反向未完、Ex 7.2 有误 |
| Ch7.3–7.4 核方法 | [核表示、列采样与随机特征](ch7.3-7.4-kernels-algorithms.md) | 🔶 已接续 Sobolev、随机特征与对偶补充；Ex7.11 未完成 |
| Ch7.5 核方法 | [泛化保证与逼近误差](ch7.5-generalization.md) | 🔶 手写稿整理；延拓未完成 |
| Ch7.6 核方法 | [岭回归的理论分析](ch7.6-ridge-theory.md) | 🔶 待人工签认 |
| Ch8 稀疏方法 | — | ❌ 待补 |
| Ch9.1-9.2 神经网络 | [优化、统计误差与宽度极限](ch9.1-9.2-neural-networks.md) | 🔶 手写稿整理 |
| Ch9.2–9.3 神经网络 | [深层复杂度草算与变差范数](ch9.2-9.3-variation-norm.md) | 🔶 部分小节；Ex 9.2 未完成 |

## 习题与 Proposition 映射

章节、习题和 Proposition 的覆盖状态见 [LTFP 阅读映射与覆盖筛查](study-map.md)。该页区分教材原题、笔记中的明确编号、隐含结论和已验证掌握，不能把文件存在直接当作学习完成。

本次手写材料的页码来源、符号校对与未完成题目见 [2026-09-08 导入记录](handwritten-import-20260908.md)。 新增 Ch7.2–7.3 笔记见 [2026-09-10 导入记录](handwritten-import-20260910.md)。

2026-09-11 的 4 页补充实际属于 Ch7，原文件名含 Ch4。见[导入记录](handwritten-import-20260911.md)；新稿状态为 `note_unverified`。

## Part III — 进阶 (Ch10–Ch15)

按当前锁定教材，第三部分为 Ch10 集成学习、Ch11 在线学习与多臂赌博机、Ch12 过参数化模型、Ch13 结构化预测、Ch14 概率方法、Ch15 下界。

| 章节 | 笔记 | 状态 |
|------|------|------|
| Ch10 集成学习 | — | ❌ 待补 |
| Ch11 在线学习与多臂赌博机 | [在线优化、零阶估计与多臂赌博机概览](ch11-online-bandits-overview.md) | 🔶 2 页概览；bandit 仅定义，无算法分析 |
| Ch12 过参数化模型 | [隐式偏好、双下降与均值场概览](ch12-overparameterized-overview.md) | 🔶 6 页概览；P12.2 证明与矩阵流后续未完成 |
| Ch13 结构化预测 | — | ❌ 待补 |
| Ch14 概率方法 | — | ❌ 待补 |
| Ch15 下界 | — | ❌ 待补 |

2026-09-20 至 09-21 导入的 Ch11 与 Ch12 原稿页码、编号校正和未完成项见[导入记录](handwritten-import-20260920-ch11-ch12.md)；两篇均为 `note_unverified`。

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

*最后更新：2026-09-21（导入 Ch11–Ch12 概览，未新增掌握认证）*
