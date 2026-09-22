# LTFP 阅读映射与覆盖筛查

本页把 LTFP 锁定教材、章节笔记、Exercise 题库和 Proposition 记录放在同一张地图上。它用于判断“资料是否存在”和“是否已经掌握”，两者不等价。

## 判定口径

| 标记 | 含义 |
|---|---|
| `source_only` | 锁定 PDF 中存在，但当前笔记没有对应记录 |
| `note_unverified` | 笔记中有内容，但尚未经过教材逐条核验 |
| `proposition_explicit` | 笔记明确写出 Proposition 编号 |
| `proposition_implicit` | 笔记有相关结论，但没有写出正式编号 |
| `missing` | 目前没有可定位的笔记内容 |
| `attempted` / `mastered` | 有作答或评分证据；不能由笔记文件名推断 |

此前覆盖筛查记录了390个 LTFP 笔记原子，均为 `unverified`，当时学习状态账本没有作答事件。这是历史快照，不是当前账本查询结果。旧原子计数不覆盖后续新增或修订内容。2026-09-20 的文档核对只确认笔记可定位性，未重建语料库、未重查或写入学习账本。本页的覆盖状态不是 mastery 结论。

## 章节总览

题库当前登记154道题，但锁定 PDF 正文中 Ch2 存在 Exercise 2.8，按章节应为155道；该计数问题尚未修复。

| 章节 | 正式章节名 | 笔记覆盖 | Exercise 记录 | Proposition 记录 |
|---|---|---|---|---|
| Ch1 | 数学预备（Mathematical Preliminaries） | 集中不等式、矩阵与微积分材料；部分内容跨到 Ch2/Ch5 | 29道题均无明确习题编号 | P1.1–P1.8 中没有正式编号；有两个未编号命题块，暂按 P1.4/P1.5 候选处理 |
| Ch2 | 监督学习导论（Introduction to Supervised Learning） | Ch2.1–2.5 材料 | 笔记出现2.1–2.8；题库漏记2.8 | P2.1–P2.3 只有隐含论述，没有正式编号 |
| Ch3 | 线性最小二乘回归（Linear Least-Squares Regression） | 3.1–3.9，存在文件范围重叠 | 明确出现3.5–3.10；3.1–3.4未标注 | 明确出现 P3.2、P3.3、P3.6–P3.12 |
| Ch4 | 经验风险最小化（Empirical Risk Minimization） | 4.1.1–4.1.3、4.2–4.5.6；4.1.4 缺失；4.6 仅提纲，4.7 有补充草稿 | 4.8、4.11、4.13、4.14 有记录；4.12 有关联推导，4.15 仅提及未完成 | P4.2–P4.6 有编号与内容；P4.6 证明未完成；P4.7 仅编号与概述 |
| Ch5 | 机器学习优化（Optimization for Machine Learning） | 5.1–5.4.1，含 SGD/SVRG 重叠 | 明确出现5.18–5.21、5.26–5.29、5.31–5.34 | 明确出现 P5.6、P5.7、P5.8 |
| Ch6 | 局部平均方法（Local Averaging Methods） | [§6.1–6.3](ch6.1-6.3-local-averaging.md)、[§6.4–6.5](ch6.4-6.5-universal-consistency.md) 已整理，均为 `note_unverified` | 6.2/6.3/6.5 有简写；6.4 仅题号；6.6 构造未写；6.1 为 `source_only` | P6.1、P6.3 明确记录；P6.2 有 k 近邻界但原稿未标编号 |
| Ch7 | 核方法（Kernel Methods） | §7.2、§7.3 核基础/7.3.1/7.3.2（部分）/7.3.3、§7.4.1–7.4.4、§7.5 与 §7.6.1 已整理；原有 §7.6 理论笔记保留待签认 | 7.1 有简写、7.2 有错误尝试、7.6 有推导；7.8 有草算；7.10 有随机特征推导、7.11 有未完成草稿、7.21 仅题意；7.3 有未编号对应草稿，其余 `source_only` | P7.1–P7.4 明确记录（P7.3 反向未完成）；P7.5–P7.8 已记录但未核验 |
| Ch8 | 稀疏方法（Sparse Methods） | [稀疏回归与 Lasso 概览](ch8-sparse-regression-overview.md)：§8.1 问题设置、§8.3.1 软阈值与最优性、慢/快速率主线 | 无明确习题作答；Ex 8.5–8.9 只涉及正文背景，仍为 `source_only` | P8.3/P8.4 的速率结论有概览，未形成正式 Proposition 证明；其余 `source_only` |
| Ch9 | 神经网络（Neural Networks） | 原有 Ch9.1–9.2，加 [§9.2–9.3 部分笔记](ch9.2-9.3-variation-norm.md)，均未签认 | 9.2 有部分推导，未收尾；其余为 `source_only`（另有未编号的相关草算） | P9.2 明确记录、验证未完成；P9.1/P9.3 仍无正式编号记录 |
| Ch10 | 集成学习（Ensemble Learning） | 无逐章笔记 | `source_only` | `source_only` |
| Ch11 | 从在线学习到多臂赌博机（From Online Learning to Bandits） | [§11.1–11.3 概览](ch11-online-bandits-overview.md)：§11.1.1–11.1.3 有投影 SGD、强凸速率和镜像下降推导草稿；§11.2.1–11.2.2 有高斯平滑、光滑/非光滑零阶优化界；§11.3 仅 bandit 定义 | 无明确习题作答 | P11.2/P11.4 明确写出；P11.1/P11.3/P11.5 为隐含对应，均未核验 |
| Ch12 | 过参数化模型（Overparameterized Models） | [§12.1–12.3 概览](ch12-overparameterized-overview.md)：隐式偏好、双下降、均值场与线性网络起步；§12.4 仅提名 | 无明确习题作答 | P12.1/P12.2 有结论记录；P12.2 证明未完成 |
| Ch13–Ch15 | 结构化预测、概率方法、下界 | 无逐章笔记 | `source_only` | `source_only` |

## Ch4 细分映射

`ch4.1-4.4.3.md` 录入了4.1.1、4.1.2、4.1.3，但没有4.1.4 “Relation between Risk and Phi-risk”。因此 Exercise 4.1–4.4 暂无对应笔记。

| 对象 | 教材小节 | 当前状态 |
|---|---|---|
| Exercise 4.1–4.4 | 4.1.4 Relation between Risk and Phi-risk | `source_only`；4.1.4笔记缺失 |
| Exercise 4.5 | 4.4 Estimation Error | `source_only` |
| Exercise 4.6–4.7 | 4.4.3 Easy Case II | `source_only` |
| Exercise 4.8 | 4.4.4 Covering Numbers | 已在 `ch4.4.4-4.5.0.md` 中明确记录 |
| Exercise 4.9 | 4.5 Rademacher Complexity | `source_only` |
| Exercise 4.10 | 4.5.1 Symmetrization | 有理论材料，未明确标成习题解答 |
| Exercise 4.11 | 4.5.1 Symmetrization | [Rademacher 笔记](ch4.5.1-4.5.3.md)有明确题号及 Gaussian/Rademacher 比较推导；待核验 |
| Exercise 4.12 | 4.5.3–4.5.4 | 同篇有 ℓ¹ 球复杂度推导，且在 Ex4.13 末明确引用 4.12；没有独立题号标题 |
| Exercise 4.13 | 4.5.3–4.5.4 | 同篇有明确题号、题意与推导；待核验 |
| Exercise 4.14 | 4.5.4 | [风险界笔记](ch4.5.4-4.5.6.md)有题意与推导；末行将 ℓ¹ 距离写成 ℓ² 范数表达式，保留待核验 |
| Exercise 4.15 | 4.5.5 | 同篇明确提及证明未完成，不能再列为 `source_only` |
| Exercise 4.16 | 4.5.6 | `source_only` |
| Proposition 4.1 | 4.1.3 Classification Calibration | 有相关章节，但没有正式 Proposition 编号 |
| Proposition 4.2 | 4.5.1 Symmetrization | [Rademacher 笔记](ch4.5.1-4.5.3.md)有编号、结论与推导；原文拼作 `Propostion4.2`，待核验 |
| Proposition 4.3 | 4.5.2 Lipschitz Contraction | 同篇明确记录编号、结论与推导；待核验 |
| Proposition 4.4 | 4.5.3 Contraction Principle | 已明确记录 |
| Proposition 4.5 | 4.5.4 Linear Predictions | [风险界笔记](ch4.5.4-4.5.6.md)有编号、结论与推导；待核验 |
| Proposition 4.6 | 4.5.5 Regularized Objectives | 同篇有编号、假设、风险界与证明主线；正文注明证明未完成 |
| Proposition 4.7 | 4.5.5–4.5.6 Norm-Penalized Estimation | 同篇有编号及一般范数惩罚的简短概述；未写完整命题或证明 |

## Ch7.6 细分映射

`ch7.6-ridge-theory.md` 已覆盖核岭回归的算法形式、总体风险的偏差—方差分解、经验算子与总体算子的比较，以及有效维数和逼近误差。该文件仍是待人工签认的精读笔记，因此下表只记录“可定位”，不把它提升为已验证或已掌握。

| 对象 | 教材小节 | 当前状态 |
|---|---|---|
| Proposition 7.5 | 7.6.2 Bias-Variance Decomposition | `proposition_explicit`；待教材逐条核验 |
| Lemma 7.1 | 7.6.3 Relating Empirical and Population Operators | 已明确记录；待教材逐条核验 |
| Proposition 7.6 | 7.6.4 Well-Specified Case | `proposition_explicit`；待教材逐条核验 |
| Proposition 7.7 | 7.6.4 Well-Specified Case | `proposition_explicit`；待教材逐条核验 |
| Lemma 7.2 | 7.6.5 Beyond the Well-Specified Case | 已明确记录；待教材逐条核验 |
| Proposition 7.8 | 7.6.5 Beyond the Well-Specified Case | `proposition_explicit`；待教材逐条核验 |
| Exercise 7.1–7.23 | Ch7 各节 | 当前 7.1 有简写、7.2 有错误尝试、7.6 有推导、7.8 有草算，7.10 有随机特征推导、7.11 有未完成草稿、7.21 仅题意；7.3 有未编号对应草稿，其余 `source_only`，§7.6 理论笔记不等同于习题作答 |

## Ch11 细分映射

当前手写材料补充了 §11.1.1–11.1.3 的在线优化推导，以及 §11.2.1–11.2.2 的零阶凸优化推导，均为 `note_unverified`。§11.2.2 停在 Proposition 11.5 的核心上界，尚未完成参数优化；§11.3 仍只有问题定义。

| 对象 | 教材小节 | 当前状态 |
|---|---|---|
| Proposition 11.1 | 11.1.1 Convex Case | `proposition_implicit`；投影 SGD、距离递推、Abel 求和与最终速率有对应草稿，未逐条核验 |
| Proposition 11.2 | 11.1.2 Strongly Convex Case | `proposition_explicit`；步长 $\gamma_s=1/(\mu s)$、强凸望远镜项与对数速率有记录，未逐条核验 |
| Proposition 11.3 | 11.1.3 Online Mirror Descent | `proposition_implicit`；镜像更新和单步 Bregman 界有记录，最终望远镜求和未完成 |
| Exercise 11.1–11.2 | 11.1.1–11.1.3 | `source_only`；原稿没有习题作答 |
| Lemma 11.2 | 11.2.1 Smooth Stochastic Gradient Descent | 明确记录；用高斯分部积分说明随机差分对 $\nabla F_\delta$ 无偏，未逐条核验 |
| Proposition 11.4 | 11.2.1 Smooth Stochastic Gradient Descent | `proposition_explicit`；平滑偏差、估计量二阶矩、收敛上界与 $O(dt^{-1/3})$ 量级主线有记录，未逐条核验 |
| Lemma 11.3 | 11.2.2 Nonsmooth Stochastic Gradient Descent | 明确记录；$F_\delta$ 的 Lipschitz、光滑性和近似误差界有记录，未逐条核验 |
| Proposition 11.5 | 11.2.2 Nonsmooth Stochastic Gradient Descent | `proposition_implicit`；原稿写到核心上界，未继续完成无噪声/有噪声参数优化 |
| Exercise 11.3–11.6 | 11.2–11.3 | `source_only`；原稿没有习题作答 |

## 文件范围的特别说明

- `ch1.1-1.2.0-optimization.md` 不是单一教材范围，实际混合了 Ch1 数学预备、风险分解和 Ch5 优化。
- `ch3.1-3.4-linear-basics.md` 正文已经延伸到3.5–3.8，不能只按文件名前缀归入3.1–3.4。
- `ch5.1-5.2-optimization.md` 实际包含非光滑优化、SGD 和 SVRG，属于跨5.1–5.4的综合笔记。
- `ch4.5.1-4.5.3.md` 缺少文首和主要小节的规范标题，已有“第一部分”“第二部分”等局部标题；不能只按标题判断覆盖。P4.2–P4.4 与 Ex4.11/4.13 可从正文定位。
- Ch4 的“有记录”按 2026-09-20 的正文核对更新，仅确认可定位性，不将整理稿中的 AI 补充认定为原稿独立证明。

## 后续数据结构

习题和 Proposition 都应增加显式关联字段，而不是继续依赖文件名前缀：

```json
{
  "id": "P4.4",
  "chapter": 4,
  "section": "4.5.3",
  "title": "Contraction principle - absolute values",
  "note_refs": ["docs/computation/ltfp/ch4.5.1-4.5.3.md:505"],
  "coverage": "proposition_explicit",
  "proof_status": "proof_partial"
}
```

习题对象还应包含 `pdf_page`、`section`、`note_refs` 和 `coverage`；Proposition 对象还应包含 `title`、`proof_status` 和证明出处。
