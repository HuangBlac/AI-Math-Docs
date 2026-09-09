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

此前覆盖筛查记录了390个 LTFP 笔记原子，均为 `unverified`，当时学习状态账本没有作答事件。2026-09-08 与 2026-09-10 的导入只更新文档与映射，未重建语料库、未重查或写入学习账本；该旧计数不包含本次新页面。本页的覆盖状态不是 mastery 结论。

## 章节总览

题库当前登记154道题，但锁定 PDF 正文中 Ch2 存在 Exercise 2.8，按章节应为155道；该计数问题尚未修复。

| 章节 | 正式章节名 | 笔记覆盖 | Exercise 记录 | Proposition 记录 |
|---|---|---|---|---|
| Ch1 | 数学预备（Mathematical Preliminaries） | 集中不等式、矩阵与微积分材料；部分内容跨到 Ch2/Ch5 | 29道题均无明确习题编号 | P1.1–P1.8 中没有正式编号；有两个未编号命题块，暂按 P1.4/P1.5 候选处理 |
| Ch2 | 监督学习导论（Introduction to Supervised Learning） | Ch2.1–2.5 材料 | 笔记出现2.1–2.8；题库漏记2.8 | P2.1–P2.3 只有隐含论述，没有正式编号 |
| Ch3 | 线性最小二乘回归（Linear Least-Squares Regression） | 3.1–3.9，存在文件范围重叠 | 明确出现3.5–3.10；3.1–3.4未标注 | 明确出现 P3.2、P3.3、P3.6–P3.12 |
| Ch4 | 经验风险最小化（Empirical Risk Minimization） | 4.1.1–4.1.3、4.2–4.5.3；4.1.4缺失 | 仅明确记录 Exercise 4.8 | 仅明确记录 P4.4 |
| Ch5 | 机器学习优化（Optimization for Machine Learning） | 5.1–5.4.1，含 SGD/SVRG 重叠 | 明确出现5.18–5.21、5.26–5.29、5.31–5.34 | 明确出现 P5.6、P5.7、P5.8 |
| Ch6 | 局部平均方法（Local Averaging Methods） | [§6.1–6.3](ch6.1-6.3-local-averaging.md)、[§6.4–6.5](ch6.4-6.5-universal-consistency.md) 已整理，均为 `note_unverified` | 6.2/6.3/6.5 有简写；6.4 仅题号；6.6 构造未写；6.1 为 `source_only` | P6.1、P6.3 明确记录；P6.2 有 k 近邻界但原稿未标编号 |
| Ch7 | 核方法（Kernel Methods） | §7.2、§7.3 核基础/7.3.1/7.3.2（部分）/7.3.3、§7.4.1–7.4.3、§7.5 与 §7.6.1 已整理 | 7.1 有简写、7.2 有错误尝试、7.6 有推导；7.8 有草算；7.10/7.21 仅题意；7.3 有未编号对应草稿，其余 `source_only` | P7.1–P7.4 明确记录（P7.3 反向未完成）；P7.5–P7.8 为 `source_only` |
| Ch8 | 稀疏方法（Sparse Methods） | 无逐章笔记；背景稀疏学习笔记未绑定 Ch8 | 17道题均为 `source_only` | P8.1–P8.6 为 `source_only` |
| Ch9 | 神经网络（Neural Networks） | 原有 Ch9.1–9.2，加 [§9.2–9.3 部分笔记](ch9.2-9.3-variation-norm.md)，均未签认 | 9.2 有部分推导，未收尾；其余为 `source_only`（另有未编号的相关草算） | P9.2 明确记录、验证未完成；P9.1/P9.3 仍无正式编号记录 |

## Ch4 细分映射

`ch4.1-4.4.3.md` 录入了4.1.1、4.1.2、4.1.3，但没有4.1.4 “Relation between Risk and Phi-risk”。因此 Exercise 4.1–4.4 暂无对应笔记。

| 对象 | 教材小节 | 当前状态 |
|---|---|---|
| Exercise 4.1–4.4 | 4.1.4 Relation between Risk and Phi-risk | `source_only`；4.1.4笔记缺失 |
| Exercise 4.5 | 4.4 Estimation Error | `source_only` |
| Exercise 4.6–4.7 | 4.4.3 Easy Case II | `source_only` |
| Exercise 4.8 | 4.4.4 Covering Numbers | 已在 `ch4.4.4-4.5.0.md` 中明确记录 |
| Exercise 4.9 | 4.5 Rademacher Complexity | `source_only` |
| Exercise 4.10–4.11 | 4.5.1 Symmetrization | 有理论材料，未明确标成习题解答 |
| Exercise 4.12–4.13 | 4.5.3–4.5.4 | 有部分理论材料，未明确标成习题解答 |
| Exercise 4.14–4.15 | 4.5.5 | `source_only` |
| Exercise 4.16 | 4.5.6 | `source_only` |
| Proposition 4.1 | 4.1.3 Classification Calibration | 有相关章节，但没有正式 Proposition 编号 |
| Proposition 4.2 | 4.5.1 Symmetrization | 未明确记录 |
| Proposition 4.3 | 4.5.2 Lipschitz Contraction | 未明确记录 |
| Proposition 4.4 | 4.5.3 Contraction Principle | 已明确记录 |
| Proposition 4.5 | 4.5.4 Linear Predictions | 未明确记录 |
| Proposition 4.6 | 4.5.5 Regularized Objectives | 未明确记录 |
| Proposition 4.7 | 4.5.5–4.5.6 Norm-Penalized Estimation | 未明确记录 |

## 2026-09-10 新增 Ch7.2–7.3 原稿

新增来源为用户于 2026-09-09 提供的 7 页手写稿。见[新笔记](ch7.2-7.3-representer-kernel-foundations.md)与[导入记录](handwritten-import-20260910.md)。以下状态更新不改变学习账本，也不表示全节已掌握。

| 对象 | 新来源位置 | 当前内容状态 |
|---|---|---|
| P7.1 | PDF 第 2–3 页 | 有正交分解证明主线与有限维目标 |
| P7.2 | PDF 第 3 页 | 有最小范数插值与 Kα=y 推导 |
| P7.3 | PDF 第 4–5 页 | 正向已写，反向完备化等步骤未写 |
| Ex 7.1 | PDF 第 5 页 | 有表示向量与再生关系的简短作答 |
| Ex 7.2 | PDF 第 5 页 | 有尝试，带符号系数乘不等式一步错误，未代写正确解法 |
| §7.3.2 | PDF 第 6 页 | 新增 Fourier 范数与特征分量，周期核后续未写 |
| Ex 7.6 | PDF 第 7 页 | 有平方和论证与 ℓ² 特征，逐点收敛条件未展开 |

此前的“只找到教材内容”是旧材料范围下的判断，不能继续覆盖这份新原稿。历史导入表保留原日期；当前情况以上表和章节总览为准。

## 2026-09-08 手写材料与习题状态

详细来源与九道已标号习题见[本次导入记录](handwritten-import-20260908.md)。其中“仅题号/题意”只表示原稿提到了题目，不表示有答案；“部分推导”也不升级为 `mastered`。

| 对象 | 可定位内容 | 完成程度 |
|---|---|---|
| P6.1 | [固定分割界](ch6.1-6.3-local-averaging.md) | 有结论与证明框架，部分概率界未展开 |
| Lemma 6.1 / 6.2 | [近邻距离界](ch6.1-6.3-local-averaging.md) | 前者有几何证明草稿，后者仅结论 |
| P6.3 | [核回归误差界](ch6.1-6.3-local-averaging.md) | 有 Bernstein 与偏差—方差计算，已注明系数整理 |
| P7.4 | [Bochner 定理](ch7.3-7.4-kernels-algorithms.md) | 只展开一个方向 |
| P9.2 | [变差范数](ch9.2-9.3-variation-norm.md) | 有范数性质与部分验证，完备性未写 |
| Ex 6.4 / 7.10 / 7.21 | 原题号或简短题意 | 无独立解答 |
| Ex 6.6 | 一阶偏差消去的设想 | 构造与证明未写 |
| Ex 9.2 | 基类界与一层收缩 | 最终递推未完成 |
| 其他断点 | 非齐次维数归纳、延拓 g、Fourier/Sobolev 联系等 | 保留原稿停止位置 |

## 文件范围的特别说明

- `ch1.1-1.2.0-optimization.md` 不是单一教材范围，实际混合了 Ch1 数学预备、风险分解和 Ch5 优化。
- `ch3.1-3.4-linear-basics.md` 正文已经延伸到3.5–3.8，不能只按文件名前缀归入3.1–3.4。
- `ch5.1-5.2-optimization.md` 实际包含非光滑优化、SGD 和 SVRG，属于跨5.1–5.4的综合笔记。
- `ch4.5.1-4.5.3.md` 缺少 Markdown 标题，脚本会把大量内容压成单个检索块；其中 Proposition 4.4 仍可由正文定位。

## 后续数据结构

习题和 Proposition 都应增加显式关联字段，而不是继续依赖文件名前缀：

```json
{
  "id": "P4.4",
  "chapter": 4,
  "section": "4.5.3",
  "title": "Contraction principle - absolute values",
  "note_refs": ["docs/computation/ltfp/ch4.5.1-4.5.3.md:301"],
  "coverage": "proposition_explicit",
  "proof_status": "proof_partial"
}
```

习题对象还应包含 `pdf_page`、`section`、`note_refs` 和 `coverage`；Proposition 对象还应包含 `title`、`proof_status` 和证明出处。
