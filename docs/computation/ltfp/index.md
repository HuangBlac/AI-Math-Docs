# 统计学习理论（LTFP）笔记

以 Francis Bach 的 *Learning Theory from First Principles*（LTFP）为主线，整理从集中不等式、监督学习、经验风险最小化到核方法、稀疏方法和神经网络理论的学习记录。

这张页面只回答两个问题：当前有哪些可读的正文，以及每部分还缺什么。详细的 Exercise、Proposition 和 `source_only` / `note_unverified` 映射见[阅读映射与覆盖筛查](study-map.md)。

## 状态口径

| 标记 | 含义 |
|---|---|
| ✅ | 已有相对完整的正文记录，但不自动表示逐条核验或掌握 |
| 🔶 | 手写稿或概览整理，仍有未完成推导、错误尝试或待核验内容 |
| ⚠️ | 有正文，但范围重叠、缺口或结构问题需要继续处理 |
| ❌ | 当前没有对应的逐章正文笔记 |

`note_unverified` 只表示“笔记材料已经存在，尚未逐条核验”；文件存在、构建通过和 Git 提交都不等于 `mastered`。

## 阅读主线

```text
数学预备与集中不等式
  → 监督学习与风险
  → 线性方法与岭回归
  → 经验风险最小化
  → 优化
  → 局部平均方法
  → 核方法
  → 稀疏方法
  → 神经网络
  → 在线学习与多臂赌博机
  → 过参数化模型
```

Ch10、Ch13–Ch15 已列入锁定教材的章节顺序，但目前还没有对应的逐章正文笔记。

## Part I — 基础（Ch1–Ch3）

| 章节 | 正文入口 | 当前范围与缺口 |
|---|---|---|
| Ch1 数学基础 | [再论集中不等式](ch1.2.2-1.2.3-concentration.md)、[Bernstein 不等式与极大值期望](ch1.2.1-bernstein-maximum.md) | ✅；另有跨 Ch1–Ch5 的风险分解、优化和数学预备材料 |
| Ch2 监督学习导论 | [监督学习导论（Ch2.1–2.5）](ch2.1-2.5-supervised-learning.md) | ✅；题库中的 Exercise 2.8 尚未纳入章节计数 |
| Ch3 线性最小二乘回归 | [线性方法基础](ch3.1-3.4-linear-basics.md)、[岭回归与极小极大下界](ch3.5-3.9-ridge-minimax.md)、[PCA 与主成分回归（§3.9）](ch3.9-pca-regression.md) | ⚠️ 已覆盖 3.1–3.9，但文件范围有重叠；习题和 Proposition 以覆盖表为准 |

## Part II — 核心理论（Ch4–Ch9）

| 章节 | 正文入口 | 当前范围与缺口 |
|---|---|---|
| Ch4 经验风险最小化 | [风险凸化与误差分解](ch4.1-4.4.3.md)、[覆盖数与 Rademacher 导入](ch4.4.4-4.5.0.md)、[Rademacher 复杂度](ch4.5.1-4.5.3.md)、[风险界与正则化估计](ch4.5.4-4.5.6.md)、[模型选择与补充推导](<ch4.6-4.7 model selection.md>) | ⚠️ 4.1.4 缺失；§4.6 仅提纲；P4.6 证明未完成，P4.7 仅概述 |
| Ch5 机器学习优化 | [优化简介（跨 §5.1–5.4）](ch5.1-5.2-optimization.md)、[非光滑梯度方法](ch5.3-nonsmooth.md)、[随机梯度下降（§5.4）](ch5.4.0-sgd.md)、[强凸 SGD](ch5.4.1-strong-convex-sgd.md) | ✅/⚠️；已覆盖到 §5.4.1，但 Ex5.34 原稿未完成，整理稿含补充 |
| Ch6 局部平均方法 | [估计器与一致性分析](ch6.1-6.3-local-averaging.md)、[普遍一致性与高阶光滑性](ch6.4-6.5-universal-consistency.md) | 🔶 手写稿整理；Exercise 6.4 留白，Exercise 6.6 构造未写 |
| Ch7 核方法 | [表示定理、核构造与 Mercer 特征](ch7.2-representer-kernel-foundations.md)、[核表示、列采样与随机特征](ch7.3-7.4-kernels-algorithms.md)、[泛化保证与逼近误差](ch7.5-generalization.md)、[岭回归的理论分析](ch7.6-ridge-theory.md) | 🔶 §7.2–7.6.1 有整理稿；P7.3 反向未完，Ex7.2 有误，Ch7.6 待人工签认 |
| Ch8 稀疏方法 | [稀疏回归与 Lasso：简单笔记](ch8-sparse-regression-overview.md) | 🔶 有问题设置、软阈值、慢/快速率主线；快速率条件和扩展方向待深入 |
| Ch9 神经网络 | [优化、统计误差与宽度极限](ch9.1-9.2-neural-networks.md)、[复杂度与变差范数](ch9.2-9.3-variation-norm.md) | 🔶 有 §9.1–9.3 的部分整理；Exercise 9.2 未完成，部分结论未签认 |

## Part III — 进阶（Ch10–Ch15）

锁定教材的第三部分顺序为：Ch10 集成学习、Ch11 在线学习与多臂赌博机、Ch12 过参数化模型、Ch13 结构化预测、Ch14 概率方法、Ch15 下界。

| 章节 | 正文入口 | 当前范围与缺口 |
|---|---|---|
| Ch10 集成学习 | — | ❌ 待补 |
| Ch11 在线学习与多臂赌博机 | [在线优化、零阶估计与多臂赌博机概览](ch11-online-bandits-overview.md) | 🔶 已有 2 页概览、4 页 §11.1 推导和 7 页 §11.2 推导；镜像下降证明及 Proposition 11.5 的参数优化未完成，§11.3 仅有 bandit 定义 |
| Ch12 过参数化模型 | [隐式偏好、双下降与均值场概览](ch12-overparameterized-overview.md) | 🔶 有 6 页概览；P12.2 证明和线性网络后的矩阵流未完成，§12.4 仅提名 |
| Ch13 结构化预测 | — | ❌ 待补 |
| Ch14 概率方法 | — | ❌ 待补 |
| Ch15 下界 | — | ❌ 待补 |

## 覆盖映射与背景补充

- [习题与 Proposition 映射](study-map.md)：按章节记录正文覆盖、题号、命题编号和完成边界。
- [稀疏学习与特征学习](sparse-feature-learning.md)：L1 正则化、特征选择与字典学习的跨章节补充。

---

*最后更新：2026-09-22（补充 Ch11 §11.2.1–11.2.2 零阶凸优化笔记；未新增掌握认证）*
