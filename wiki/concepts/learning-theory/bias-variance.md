---
title: 偏差-方差分解
created: 2026-07-10
updated: 2026-07-10
type: concept
tags: [bias-variance, generalization]
sources: [raw/lftp/ch4-erm.md]
confidence: high
---

# 偏差-方差分解

预测误差可分解为三项：

$$\text{误差} = \text{偏差}^2 + \text{方差} + \text{不可约噪声}$$

- **偏差**: 模型平均预测与真实值的差距 → 欠拟合
- **方差**: 不同训练集上预测的波动 → 过拟合
- **噪声**: 数据本身的不确定性

这与 [[erm|经验风险最小化]] 中的逼近误差/估计误差分解是同一思想的两种表述。

## 相关
- [[erm|经验风险最小化]] — 逼近误差 vs 估计误差
- [[rademacher-complexity|Rademacher 复杂度]] — 方差的上界刻画
