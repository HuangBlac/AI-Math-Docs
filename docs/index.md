# AI & Math

> 从数学基础、数值计算与统计学习出发，理解人工智能如何参与科学问题。

这里是一份面向数学系学生和交叉研究初学者的开放知识库。它不试图收集所有名词，而是想建立一条可以实际行走的路线：从分析、代数和概率开始，经过数值方法、优化与学习理论，最终抵达 PINN、神经算子和 AI4Math 等研究问题。

[从基础数学开始](math/index.md){ .md-button .md-button--primary }
[查看学习地图](#reading-paths){ .md-button }

---

## 在这里可以学什么

<div class="grid cards" markdown>

-   :material-function-variant:{ .lg .middle } **基础数学**

    ---

    数学分析、高等代数、测度论、概率论、微分方程、泛函分析与统计学。这里提供后续理论真正会用到的语言和工具。

    [进入基础数学](math/index.md)

-   :material-calculator:{ .lg .middle } **计算数学**

    ---

    数值线性代数、数值分析、数值 PDE、凸优化，以及从 CAD、有限元到并行求解的工业计算链。

    [进入计算数学](computation/index.md) · [工业计算专题](computation/industrial-computing/index.md)

-   :material-chart-line:{ .lg .middle } **统计计算**

    ---

    Monte Carlo、Bootstrap、MCMC 与统计模拟。重点不只是调用函数，而是理解随机计算为什么有效、误差从哪里来。

    [进入统计计算](computation/stat-computing.md)

-   :material-book-open-page-variant:{ .lg .middle } **统计学习理论**

    ---

    以 *Learning Theory from First Principles* 为主线，整理集中不等式、经验风险、Rademacher 复杂度、优化与神经网络理论。

    [进入 LTFP 笔记](computation/ltfp/index.md)

-   :material-robot:{ .lg .middle } **算法介绍**

    ---

    从模型结构理解神经网络、决策树、贝叶斯方法、深度学习与压缩感知，并连接到背后的数学假设。

    [进入算法介绍](algorithms/index.md)

-   :material-flask:{ .lg .middle } **AI4Math 前沿**

    ---

    论文阅读、算法复现与研究札记，重点关注 PINN、科学机器学习以及 AI 求解微分方程的能力边界。

    [进入 AI4Math](ai4math/index.md)

</div>

## 三条阅读路线 {#reading-paths}

不必从第一页顺序读到最后。根据当前目标选择一条路线，会比“把所有先修课学完再开始”更实际。

### 1. 数学系学生进入机器学习

```text
概率论与数理统计
  -> 机器学习基础
  -> 凸优化
  -> LTFP 统计学习理论
  -> 神经网络与 AI4Math
```

[概率论](math/probability.md) → [机器学习基础](computation/ltfp/machine-learning.md) → [凸优化](computation/optimization.md) → [LTFP 总览](computation/ltfp/index.md)

这条路线回答的是：损失函数、泛化、正则化和优化为什么能够组成一套学习系统。

### 2. 从数值计算进入科学机器学习

```text
数值线性代数
  -> 数值微分方程
  -> 有限元与稀疏方程组
  -> 并行计算
  -> PINN 与神经 PDE 求解器
```

[数值线性代数](computation/num-linalg.md) → [数值微分方程](computation/num-pde.md) → [有限元方法](computation/industrial-computing/finite-element-method.md) → [PINN 概览](ai4math/pinn-overview.md)

这条路线关注：一个连续方程怎样变成可计算对象，以及神经方法与经典离散方法究竟在什么地方不同。

### 3. 带着研究问题快速进入

```text
问题背景
  -> 一篇专题总览
  -> 必要的数学与算法补充
  -> 论文、实验与反例
```

如果已经在做具体课题，可以直接从 [AI4Math 论文](ai4math/papers.md)、[算法实例](ai4math/examples.md) 或 [PINN 讨论班讲义](ai4math/pinn-seminar.md) 开始，再沿页面链接回补基础。

## 最近值得读的专题

| 专题 | 你会得到什么 |
|---|---|
| [工业计算：从几何建模到并行求解](computation/industrial-computing/index.md) | 把 CAD、有限元、稀疏矩阵和并行硬件串成一条完整计算链 |
| [Ch9.1-9.2 神经网络理论](computation/ltfp/ch9.1-9.2-neural-networks.md) | 从优化误差、统计误差与逼近误差理解宽度极限和 Rademacher 界 |
| [学习理论概念地图](computation/ltfp/learning-theory.md) | 在逐章推导之外，理解概率工具、复杂度与泛化界之间的关系 |
| [PINN 概览与拷打](ai4math/pinn-overview.md) | 同时看到 PINN 的基本方法、适用场景和常见失败原因 |

## 为什么还要维护知识库

大语言模型让答案变得容易获得，但“该问什么、答案依赖哪些前提、不同方法之间怎样连接”仍然需要领域结构。对一个陌生方向，如果缺少基本地图，问答很容易停留在术语解释，公式、算法和实际问题彼此分离。

这个项目因此更关心三件事：

1. **建立路径**：说明一个主题从哪些基础出发，又通向哪些问题；
2. **保留推导**：不仅给结论，也记录关键公式、假设和误差来源；
3. **连接实践**：把理论和可运行实验、工业计算及研究论文放在同一张地图上。

这不是一部已经完成的百科全书。很多页面来自课程笔记、手写转录、论文阅读和实验复盘，内容会随着学习持续校正。比“看起来什么都有”更重要的是：每一条路径最终能够被验证、复现或继续追问。

## 如何参与

如果你发现公式、表述或链接存在问题，或者希望补充某条学习路径，欢迎直接修改项目内容。也可以加入 QQ 群 `894492975` 交流选题和勘误。

在提交内容时，建议尽量说明：

- 这段内容解决什么问题；
- 需要哪些前置知识；
- 公式或结论成立的条件；
- 可以继续阅读或验证的来源。

---

*持续建设中 · 最后更新：2026 年 8 月* · [关于本站](about/backstage.md)
