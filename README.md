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
  - 一维输运方程迎风格式、抛物方程差分与方向分裂实验
  - 凸优化与无约束优化实验
  - [工业计算：CAD、有限元、并行计算与高维问题](docs/computation/industrial-computing/index.md)
- [统计计算](docs/computation/stat-computing.md)
  - Monte Carlo、Bootstrap、MCMC 与统计模拟
- [统计学习理论（LTFP）](docs/computation/ltfp/index.md)
  - Ch1-Ch5：数学基础、监督学习、线性方法、ERM 与优化
  - [阅读映射与覆盖筛查](docs/computation/ltfp/study-map.md)：按正文区分已有记录、未完成推导与待核验内容
  - Ch6：局部平均方法、一致性与高阶光滑性（手写稿整理）
  - Ch7.2–7.5：表示定理、核构造、随机特征与泛化保证（手写稿整理）
  - Ch7.6：核岭回归的算法形式、偏差—方差分解与学习率（待人工签认）
  - Ch8：稀疏回归、Lasso、慢速率与快速率的简单概览
  - Ch9：神经网络的优化、统计误差、宽度极限与变差范数（含未完成习题）
  - Ch11–Ch12：在线学习、多臂赌博机与过参数化模型概览（手写稿整理）
  - [Ch15.1.5 回归下界](docs/computation/ltfp/ch15.1.5-regression-lower-bounds.md)：Fano、参数打包、Ex15.1 参考推导与 Hilbert 空间有限维候选（讲解整理，待核验）
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
python -m pip install -e ".[docs]"
python -m mkdocs serve
```

浏览器访问 <http://127.0.0.1:8000/>。在同一解释器中运行 `python -m mkdocs build --strict` 做构建检查。

站点依赖位于 `pyproject.toml` 的 `docs` 可选依赖组，并由 `uv.lock` 锁定。也可执行 `uv sync --frozen --extra docs`，随后使用 `uv run --frozen --extra docs python -m mkdocs serve`。仅运行 `uv sync --frozen` 不会启用 `docs` 组。

## 自动构建与发布

`.github/workflows/deploy-docs.yml` 在发往 `main` 的 PR 中执行严格构建，并确认 Ch11、Ch12、Ch15.1.5 的页面已生成。PR 不上传发布产物，也没有部署权限。

推送到 `main` 或在 `main` 上手动运行工作流后，构建成功的 `site/` 产物通过官方 Pages actions 发布。发布任务仅获 `pages: write`、`id-token: write` 权限，不写入或覆盖 `gh-pages`，无需个人 token。

首次配置：仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。在 **Settings → Actions → General** 确认允许工作流使用官方 `actions/*`；无需将仓库所有工作流默认设为读写。检查 `github-pages` environment 的部署分支规则允许 `main`；若设置了人工审批，部署需在 Actions 页面批准。

在 **Actions → Build and Deploy Docs** 查看 `Build docs (strict)` 和 `Deploy to GitHub Pages` 的结果。需要重试时在 `main` 上使用 **Run workflow**。构建成功不代表已上线；部署成功后还需访问在线页面核验。

## 导入学习笔记

提供 PDF 后可使用个人技能 `$ltfp-note-import` 完成逐页转录、保留未完成项、导入和本地提交。未配置该技能时，也可按[笔记导入流程](NOTE-IMPORT.md)操作。网页只收录包含学习知识本身的正文笔记；哈希、逐页去向和整理决策等导入审计保存在被 Git 忽略的 `output/`，不进入站点导航。

## 本地学习工具

仓库还包含 `src/ai_math_study/` 与 `tests/`。使用 Python 3.12 或更高版本，执行 `uv sync --frozen` 后可用 `uv run aimath-study --help` 查看命令；工具当前支持 Ch1–Ch9，不能据此推断后续章节的阅读情况。

首次构建语料库前，核对 `study.toml` 中的本地教材路径与锁定 SHA-256。教材、生成内容与学习状态保存在本地；学习工具仍有效的历史设计约束见 `PLAN.md`，使用与开发约定见 `CLAUDE.md`（本地文件，可能不随仓库分发）。笔记存在或站点构建通过均不代表已掌握。

## 参与建设

欢迎通过 Issue、Pull Request 或 QQ 群 `894492975` 提交勘误和内容建议。新增内容最好说明问题背景、前置知识、结论成立条件以及可继续核验的来源。
