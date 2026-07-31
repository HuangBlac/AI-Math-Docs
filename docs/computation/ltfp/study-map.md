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

当前语料库中，LTFP 笔记贡献390个原子，全部仍为 `unverified`；学习状态账本没有作答事件。因此本页的覆盖状态不是 mastery 结论。

## 章节总览

题库当前登记154道题，但锁定 PDF 正文中 Ch2 存在 Exercise 2.8，按章节应为155道；该计数问题尚未修复。

| 章节 | 正式章节名 | 笔记覆盖 | Exercise 记录 | Proposition 记录 |
|---|---|---|---|---|
| Ch1 | 数学预备（Mathematical Preliminaries） | 集中不等式、矩阵与微积分材料；部分内容跨到 Ch2/Ch5 | 29道题均无明确习题编号 | P1.1–P1.8 中没有正式编号；有两个未编号命题块，暂按 P1.4/P1.5 候选处理 |
| Ch2 | 监督学习导论（Introduction to Supervised Learning） | Ch2.1–2.5 材料 | 笔记出现2.1–2.8；题库漏记2.8 | P2.1–P2.3 只有隐含论述，没有正式编号 |
| Ch3 | 线性最小二乘回归（Linear Least-Squares Regression） | 3.1–3.9，存在文件范围重叠 | 明确出现3.5–3.10；3.1–3.4未标注 | 明确出现 P3.2、P3.3、P3.6–P3.12 |
| Ch4 | 经验风险最小化（Empirical Risk Minimization） | 4.1.1–4.1.3、4.2–4.5.3；4.1.4缺失 | 仅明确记录 Exercise 4.8 | 仅明确记录 P4.4 |
| Ch5 | 机器学习优化（Optimization for Machine Learning） | 5.1–5.4.1，含 SGD/SVRG 重叠 | 明确出现5.18–5.21、5.26–5.29、5.31–5.34 | 明确出现 P5.6、P5.7、P5.8 |
| Ch6 | 局部平均方法（Local Averaging Methods） | 无逐章笔记 | 6道题均为 `source_only` | P6.1–P6.3 为 `source_only` |
| Ch7 | 核方法（Kernel Methods） | 无逐章笔记 | 23道题均为 `source_only` | P7.1–P7.8 为 `source_only` |
| Ch8 | 稀疏方法（Sparse Methods） | 无逐章笔记；背景稀疏学习笔记未绑定 Ch8 | 17道题均为 `source_only` | P8.1–P8.6 为 `source_only` |
| Ch9 | 神经网络（Neural Networks） | 无逐章笔记 | 10道题均为 `source_only` | P9.1–P9.3 为 `source_only` |

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
