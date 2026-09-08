# AI & Math

应用数学与人工智能交叉方向的开放知识库。从基础数学、数值计算和统计学习理论出发，逐步连接到科学机器学习与 AI4Math 前沿。

**在线阅读：<https://huangblac.github.io/AI-Math-Docs/>**

## 内容目录

- [序言与学习路线](docs/index.md)
- [基础数学](docs/math/index.md)
  - 数学分析、高等代数、测度论与概率论
  - 微分方程、泛函分析、数理统计、多元统计与因果推断
- [计算数学](docs/computation/index.md)
  - 数值线性代数、数值分析与数值微分方程
  - 凸优化与无约束优化实验
  - [工业计算：CAD、有限元、并行计算与高维问题](docs/computation/industrial-computing/index.md)
- [统计计算](docs/computation/stat-computing.md)
  - Monte Carlo、Bootstrap、MCMC 与统计模拟
- [统计学习理论（LTFP）](docs/computation/ltfp/index.md)
  - Ch1-Ch5：数学基础、监督学习、线性方法、ERM 与优化
  - Ch6：局部平均方法、一致性与高阶光滑性（手写稿整理）
  - Ch7.3–7.5：核表示、随机特征与泛化保证（手写稿整理）
  - Ch9：神经网络的优化、统计误差、宽度极限与变差范数（含未完成习题）
- [算法介绍](docs/algorithms/index.md)
  - 神经网络、决策树、贝叶斯学习、深度学习与压缩感知
- [AI4Math 前沿](docs/ai4math/index.md)
  - 论文阅读、算法实验、PINN 系列与研究札记

## 当前重点

- 建立从经典数值方法到科学机器学习的连续学习路线；
- 以 *Learning Theory from First Principles* 为主线整理统计学习理论；
- 记录 PINN、神经 PDE 求解器及其与有限元等经典方法的关系；
- 将手写笔记、课程材料和实验结果整理为可检索、可校正的 Markdown。

## 本地预览

```bash
uv sync --frozen
uv run mkdocs serve
```

浏览器访问 <http://127.0.0.1:8000/>。

## 参与建设

欢迎通过 Issue、Pull Request 或 QQ 群 `894492975` 提交勘误和内容建议。新增内容最好说明问题背景、前置知识、结论成立条件以及可继续核验的来源。
