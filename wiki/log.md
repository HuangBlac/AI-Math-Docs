# Wiki Log

> 操作日志。追加写入。格式: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive

## [2026-07-10] create | Wiki 初始化

- **分支**: `wiki-experiment`
- **域**: 数学 / 统计学习理论 / 统计计算 / 数据科学
- **目录结构**: SCHEMA.md + index.md + log.md + raw/ + concepts/ + entities/ + comparisons/ + queries/
- **Schema**: 定义了 frontmatter、tag taxonomy、page thresholds

## [2026-07-10] ingest | 从 AI-Math-Docs docs/computation/lftp/ 导入

9 个源文件复制到 `raw/lftp/`:
- ch2-supervised-learning.md (502 行)
- ch4-erm.md (487 行)
- ch4-rademacher.md (465 行)
- ch4-4-massart.md (270 行)
- machine-learning.md (507 行)
- sparse-feature-learning.md (228 行)
- data-science-intro.md (148 行)
- stat-computing-review.md (983 行)
- index.md (mkdocs 总览)

## [2026-07-10] create | 概念页面

从源材料提取 10 个概念页面:
- concepts/learning-theory/supervised-learning.md — 监督学习
- concepts/learning-theory/erm.md — 经验风险最小化
- concepts/learning-theory/rademacher-complexity.md — Rademacher 复杂度
- concepts/learning-theory/massart-dudley.md — Massart 引理与 Dudley 积分
- concepts/learning-theory/machine-learning.md — 机器学习基础
- concepts/learning-theory/sparse-feature-learning.md — 稀疏学习与特征学习
- concepts/learning-theory/bias-variance.md — 偏差-方差分解
- concepts/learning-theory/concentration-inequality.md — 集中不等式
- concepts/statistical-computing/statistical-computing.md — 统计计算
- concepts/statistical-computing/data-science.md — 数据科学导论

所有页面已建立 [[wikilinks]] 交叉引用，index.md 已更新。

## [2026-07-10] ingest | PDF 源材料 + Entity 页面

- `raw/lftp.pdf` (11.6 MB) — LFTP 原书 PDF
- `raw/data-science-ppt.pdf` (32 MB) — 数据科学 PPT
- entities/lftp-book.md — LFTP 精读追踪（含各章进度）
- entities/data-science-course.md — 数据科学课程简介
- index.md 更新为 12 页，新增 Entities 和 Raw Sources 章节
