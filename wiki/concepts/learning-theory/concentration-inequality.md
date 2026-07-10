---
title: 集中不等式
created: 2026-07-10
updated: 2026-07-10
type: concept
tags: [concentration-inequality, hoeffding, mcdiarmid, probability]
sources: [raw/lftp/ch4-rademacher.md, raw/lftp/ch4-4-massart.md]
confidence: high
---

# 集中不等式

集中不等式给出随机变量偏离其期望的概率上界，是统计学习理论的概率基础。

## 主要不等式

- **Hoeffding**: 有界独立随机变量的和集中在均值附近
- **McDiarmid**: Hoeffding 的函数版本，适用于有界差分性质
- **Bernstein**: 同时利用方差信息，在方差小时更紧

## 在统计学习中的应用

- 从经验风险到期望风险的转化依赖集中不等式
- [[rademacher-complexity|Rademacher 复杂度]] 的泛化界证明中大量使用
- [[massart-dudley|Massart 引理与 Dudley 积分]] 本质上也是集中不等式

## 相关
- [[rademacher-complexity|Rademacher 复杂度]] — 集中不等式的直接应用
- [[erm|经验风险最小化]] — 泛化界的概率保证
