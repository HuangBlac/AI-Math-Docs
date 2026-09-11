# AI-Math-Docs 协作入口

本项目包含 MkDocs 知识库和 `src/ai_math_study/` 学习工具。按实际文件与配置判断工作范围，不根据旧分支说明猜测组件是否存在。

- 先读 `README.md`；LTFP 从 `docs/computation/ltfp/index.md` 与 `study-map.md` 进入。详细技术约定见 `CLAUDE.md`，CLI 历史设计见 `PLAN.md`。
- 笔记导入流程见 `docs/computation/ltfp/note-import.md`。个人环境可调用 `$ltfp-note-import`；未安装该技能时按文档执行。
- 数学正文保留来源、假设与未完成项。教材路径和哈希取自 `study.toml`；译稿、AI 整理与手写材料不代替锁定原文。`note_unverified` 不等于已掌握。
- 新 PDF 是新证据。更新当前覆盖表，不用旧“未找到”结论覆盖新作答；也不把旧 AI 补充算成用户本次完成的证明。
- 行内数学用 `$...$`，行间优先 `math` fenced block。文档变更检查链接、数学格式与严格构建，不运行无关 CLI 全套测试来代替文档检查。
- `pyproject.toml` 目前是学习工具依赖配置，不包含 MkDocs。选用已安装 `mkdocs`、`material`、`pymdownx` 的解释器构建站点；配置方法见 README。
- 保留用户原有修改和暂存状态；仅提交明确授权的相关内容。提交不等于推送，构建不等于发布。
- `output/`、`_ingest/`、`.study/` 是本地材料/审计/学习状态，不自动进入站点或 Git 提交。原始文件不因文档收尾被删除。

本地学习优先级若存在于 `output/ltfp-ch7-mainline-20260909.md`，以用户最新指示和该计划为准。阶段计划只是待办，不自动修改掌握账本；旧计划的截止日不是当前承诺。
