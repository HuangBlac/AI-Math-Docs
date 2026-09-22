# 统计学习理论 (LTFP) 笔记

以 Francis Bach *Learning Theory from First Principles* (LTFP) 为主线的精读笔记。
从第一性原理出发，统一 PAC 学习、Rademacher 复杂度、核方法等经典框架。

表中状态仅描述笔记材料是否存在及其缺口；✅ 表示已有笔记，不表示逐条核验或个人掌握。历史整理稿可能包含 AI 补充，不能据此认定原稿已完成证明。

---

## Part I — 基础 (Ch1–Ch3)

| 章节 | 笔记 | 状态 |
|------|------|------|
| Ch1 数学基础 | [再论集中不等式](ch1.2.2-1.2.3-concentration.md) | ✅ |
| Ch1 数学基础 | [Bernstein 不等式与极大值期望](ch1.2.1-bernstein-maximum.md) | ✅ |
| Ch1–Ch5 跨章基础 | [风险分解、优化与数学预备](ch1.1-1.2.0-optimization.md) | ⚠️ 跨章 |
| Ch2 监督学习导论 | [监督学习导论（Ch2.1–2.5）](ch2.1-2.5-supervised-learning.md) | ✅ |
| Ch3 线性最小二乘回归 | [线性方法基础](ch3.1-3.4-linear-basics.md)、[岭回归与极小极大下界](ch3.5-3.9-ridge-minimax.md) | 已有笔记；文件范围重叠，待核验 |
| Ch3 线性最小二乘回归 | [PCA 与主成分回归（§3.9）](ch3.9-pca-regression.md) | ✅ |

## Part II — 核心理论 (Ch4–Ch9)

| 章节 | 笔记 | 状态 |
|------|------|------|
| Ch4.1–4.4.3 经验风险最小化 | [风险凸化与误差分解](ch4.1-4.4.3.md) | ⚠️ 4.1.4 缺失 |
| Ch4.4.4–4.5 经验风险最小化 | [覆盖数与 Rademacher 导入](ch4.4.4-4.5.0.md) | ⚠️ 习题稀缺 |
| Ch4.5.1–4.5.3 经验风险最小化 | [Rademacher 复杂度](ch4.5.1-4.5.3.md) | ⚠️ 标题待补 |
| Ch4.5.4–4.5.6 经验风险最小化 | [风险界与正则化估计](ch4.5.4-4.5.6.md) | 已有笔记；P4.6 证明未完成、P4.7 仅概述 |
| Ch4.6–4.7 经验风险最小化 | [模型选择与补充推导](<ch4.6-4.7 model selection.md>) | §4.6 仅提纲；§4.7 有 Gaussian/Rademacher 比较草稿 |
| Ch5 机器学习优化 | [优化简介（跨 §5.1–5.4）](ch5.1-5.2-optimization.md) | ✅ |
| Ch5.3 机器学习优化 | [非光滑梯度方法](ch5.3-nonsmooth.md) | ✅ |
| Ch5.4 机器学习优化 | [随机梯度下降（§5.4）](ch5.4.0-sgd.md) | ✅ |
| Ch5.4.1 机器学习优化 | [强凸 SGD](ch5.4.1-strong-convex-sgd.md) | 已有笔记；Ex5.34 原稿未完成，整理稿含补充 |
| Ch6.1–6.3 局部平均方法 | [估计器与一致性分析](ch6.1-6.3-local-averaging.md) | 🔶 手写稿整理；习题保留原状 |
| Ch6.4–6.5 局部平均方法 | [普遍一致性与高阶光滑性](ch6.4-6.5-universal-consistency.md) | 🔶 手写稿整理；构造未补完 |
| Ch7.2–7.3 核方法 | [表示定理、核构造与 Mercer 特征](ch7.2-representer-kernel-foundations.md) | 🔶 新手写稿；P7.3 反向未完、Ex 7.2 有误 |
| Ch7.3–7.4 核方法 | [核表示、列采样与随机特征](ch7.3-7.4-kernels-algorithms.md) | 🔶 已接续 Sobolev、随机特征与对偶补充；Ex7.11 未完成 |
| Ch7.5 核方法 | [泛化保证与逼近误差](ch7.5-generalization.md) | 🔶 手写稿整理；延拓未完成 |
| Ch7.6 核方法 | [岭回归的理论分析](ch7.6-ridge-theory.md) | 🔶 待人工签认 |
| Ch8 稀疏方法 | [稀疏回归与 Lasso：简单笔记](ch8-sparse-regression-overview.md) | 🔶 已有概览；快速率条件与扩展方向待深入 |
| Ch9.1-9.2 神经网络 | [优化、统计误差与宽度极限](ch9.1-9.2-neural-networks.md) | 🔶 手写稿整理 |
| Ch9.2–9.3 神经网络 | [深层复杂度草算与变差范数](ch9.2-9.3-variation-norm.md) | 🔶 部分小节；Ex 9.2 未完成 |

## 习题与 Proposition 映射

章节、习题和 Proposition 的覆盖状态见 [LTFP 阅读映射与覆盖筛查](study-map.md)。该页区分教材原题、笔记中的明确编号、隐含结论和已验证掌握，不能把文件存在直接当作学习完成。

## Part III — 进阶 (Ch10–Ch15)

按当前锁定教材，第三部分为 Ch10 集成学习、Ch11 在线学习与多臂赌博机、Ch12 过参数化模型、Ch13 结构化预测、Ch14 概率方法、Ch15 下界。

| 章节 | 笔记 | 状态 |
|------|------|------|
| Ch10 集成学习 | — | ❌ 待补 |
| Ch11 在线学习与多臂赌博机 | [在线优化、零阶估计与多臂赌博机概览](ch11-online-bandits-overview.md) | 🔶 2 页概览 + 4 页 §11.1.1–11.1.3 推导 + 7 页 §11.2.1–11.2.2 推导；Proposition 11.5 参数优化未完成，bandit 仅定义 |
| Ch12 过参数化模型 | [隐式偏好、双下降与均值场概览](ch12-overparameterized-overview.md) | 🔶 6 页概览；P12.2 证明与矩阵流后续未完成 |
| Ch13 结构化预测 | — | ❌ 待补 |
| Ch14 概率方法 | — | ❌ 待补 |
| Ch15 下界 | — | ❌ 待补 |

---

## 背景补充

| 主题 | 说明 |
|------|------|
| [稀疏学习与特征学习](sparse-feature-learning.md) | L1 正则化、特征选择、字典学习 |

---

## 统计计算

统计计算内容已独立为单独专题，见 [统计计算](../stat-computing.md) 与 [统计计算总复习](../stat-computing-review.md)。

---

*最后更新：2026-09-22（补充 Ch11 §11.2.1–11.2.2 零阶凸优化笔记；未新增掌握认证）*
