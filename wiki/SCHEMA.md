---
title: Wiki Schema
created: 2026-07-10
updated: 2026-07-10
type: meta
tags: [schema]
---

# Wiki Schema

## Domain
数学、统计学习理论、统计计算、数据科学的个人知识图谱。
主线为 Francis Bach《Learning Theory from First Principles》精读，
辅以统计计算（R/Monte Carlo/MCMC）和机器学习基础。

## Conventions
- 文件名: lowercase-hyphens (e.g. `rademacher-complexity.md`)
- 每个 wiki 页面带 YAML frontmatter
- 使用 `[[wikilinks]]` 链接页面, 每页至少 2 个外链
- 更新页面时 bump `updated` 日期
- 新页面必须加到 `index.md` 对应 section
- 所有操作追加到 `log.md`

## Frontmatter
```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept | entity | comparison | query
tags: [from taxonomy]
sources: [raw/lftp/source-file.md]
confidence: high | medium | low
---
```

## Tag Taxonomy
- 统计学习: erm, rademacher, generalization, pac-learning, bias-variance
- 优化: convex-optimization, gradient-descent, sgd
- 概率: concentration-inequality, hoeffding, mcdiarmid
- 计算: monte-carlo, bootstrap, mcmc, r-language
- 数学: functional-analysis, measure-theory, linear-algebra
- 元: comparison, overview, note, todo

## Page Thresholds
- **建页面**: 概念出现 2+ 篇笔记 OR 是一篇笔记的核心
- **追加**: 概念已被覆盖, 补充即可
- **不建**: 一笔带过的术语
- **拆分**: 页面超 200 行时拆成子话题

## Layer 1: raw/
不可变源材料。从现有笔记复制而来, 标记 ingestion 日期。

## Layer 2: concepts/ entities/ comparisons/ queries/
Agent 维护的 wiki 页面。从 raw/ 提取、交叉引用、综合。

## Layer 3: SCHEMA.md + index.md + log.md
结构约定 + 内容目录 + 操作日志。
