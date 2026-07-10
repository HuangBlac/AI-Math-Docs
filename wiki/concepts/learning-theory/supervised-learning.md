---
title: 监督学习
created: 2026-07-10
updated: 2026-07-10
type: concept
tags: [erm, generalization, pac-learning, bias-variance]
sources: [raw/lftp/ch2-supervised-learning.md]
confidence: high
---

# 监督学习

给定观测数据 $(x_i, y_i)$，目标是预测未见数据上的 $y$。核心困难：

1. **噪声**: $y$ 只受 $x$ 的概率影响，$y = f(x) + \varepsilon$
2. **函数复杂**: 真实映射可能极其复杂
3. **样本有限**: 只能看到有限观测
4. **维度大**: 输入空间可能高维
5. **分布偏移**: 训练和测试分布可能不同
6. **评价模糊**: "好" 的表现没有唯一标准

## 核心思想

监督学习的理论基础是通过 [[erm|经验风险最小化]] 来逼近真实风险。
关键分解：**风险 = 逼近误差 + 估计误差**。

- [[erm|经验风险最小化]] 处理逼近误差
- [[rademacher-complexity|Rademacher 复杂度]] 量化估计误差的上界

## 相关

- [[erm|经验风险最小化]] — 核心框架
- [[rademacher-complexity|Rademacher 复杂度]] — 泛化误差界
- [[bias-variance|偏差-方差分解]] — 误差的另一种视角
