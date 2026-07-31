# Plan: LFTP 前九章可验证学习系统修复与落地
_Locked via grill - by Codex + 黄南樵; revised after adversarial review round 1_

## Goal

在 2026 年 9 月 5 日前，以本地锁定版 `wiki/raw/lftp.pdf`（SHA-256 `DDEBA8166E4DC2AEDC0B863E67AF9891178A5E13F3316FD672D49CD59E486DEA`）为最高权威，完成 LFTP 前九章（Parts I-II）的可验证学习。当前以 DeepSeek V4 跑通模型功能，同时保持 provider 可替换；交付重点是可信教材结构、中文精读、经原页核验后的 96 道无菱形必做 Exercise 闭环、证据化出题判分和内容安全的笔记整理。代码、配置、迁移和测试进入仓库；教材摘录、中文衍生内容、模型结果和学习记录只存放在被 Git 忽略的 `.study/`。

## Approach

1. **Phase 0：先建立可学习的最短关键路径**
   - 截止 2026-07-14，由 Codex 完成工程工作，不占用用户 160 小时学习预算；用户最多投入 2 小时抽查章节边界、Exercise 编号和 Ch1-Ch2 核心公式。Phase 0 的 154/96 inventory 只能标为 `provisional`，不能在两小时内虚报全部人工核验。
   - Phase 0 只交付：锁定 PDF 验证、Ch1-Ch9 结构与 154 题清单、可用的中文检索、独立学习状态账本、8 周任务和基础 CLI。
   - 硬门：PDF 哈希与 488 页正确；Parts/Ch1-Ch9 边界抽查通过；provisional 154/96 清单生成；两次摄取 canonical digest 相同；中文 golden queries 全部命中；重建 corpus 后学习状态不丢失。任一失败则系统不得标为 ready，也不得启动 AI 判分。
   - 7/12-7/18 即使 Gate B 尚未完成，学习使用锁定 PDF、人工 Exercise ledger 和本地 Markdown 继续，不依赖 AI。inventory 按当前周逐章核验：W1 完成 Ch1-Ch2，随后每周在进入该章前签认该章 Exercise；全书 154/96 只在九章均签认后升级为 `verified`。
   - 2026-07-15 至 07-18 完成 Gate B：DeepSeek provider 契约、证据包防篡改、1 道题与 1 次判分的在线冒烟、人工复核阻断。`organize`、AI 精读扩写和交互菜单是非关键增强，可在学习开始后增量交付，失败不得阻塞阅读、Exercise 记录和本地检索。

2. **保护现场并建立基线**
   - 保留用户对 `wiki/.obsidian/workspace.json`、`wiki/entities/lftp-book.md` 及其他无关文件的修改。
   - 审查现有 `src/ai_math_study`、`tests`、`study.toml`、`lftp_learning/` 和生成残留；仅保留满足新契约的实现，删除或隔离旧骨架前必须证明归属和替代关系。
   - 记录当前命令、测试、Ruff、Mypy、Windows 中文控制台和 Git 状态，区分新增回归与仓库既有失败。

3. **从锁定 PDF 重建 Ch1-Ch9 真值清单**
   - 使用“节号 + 印刷页 + PDF 页”三重锚点。范围固定为 Ch1 Mathematical Preliminaries、Ch2 Introduction to Supervised Learning、Ch3 Linear Least-Squares Regression、Ch4 Empirical Risk Minimization、Ch5 Optimization for Machine Learning、Ch6 Local Averaging Methods、Ch7 Kernel Methods、Ch8 Sparse Methods、Ch9 Neural Networks；Ch10 Ensemble Learning 属于 Part III，不得混入。
   - 修复 Ch7 的 7.4.1-7.4.6、7.6.1-7.6.6 和 Ch9 缺失的 9.3.6；逐项复核全部标题与页码。
   - 逐题识别真实 Definition、Proposition、Lemma、Exercise 和菱形标记，不以连续编号猜测。前九章当前源对齐结果共 154 道 Exercise、其中 96 道无菱形；Exercise 1.14 已由印刷页 12 / PDF 页 28 视觉确认带单菱形，其余清单仍按周签认。
   - PDF 抽取文本只用于检索。公式、特殊符号和菱形不得仅凭抽取文本标为已核验。

4. **建立分层、不可变、可重放的 corpus**
   - 使用 Python 3.12、SQLite FTS5 trigram（不可用时采用通过 golden recall 的确定性中文分词）、JSONL manifest 和稳定哈希；不得继续使用无法匹配普通中文子串的裸 `unicode61`。
   - 核心库只 allowlist 锁定 PDF、`docs/computation/ltfp` 和 `wiki/raw/lftp` 的 LFTP 笔记。先修库只 allowlist 相关线代、概率、分析、优化材料；默认出题判分不得用先修库单独支撑结论。
   - 数据库分别持久化 `corpus_tier`、`authority`、`verification_state`、`evidence_type`、`formula_uncertain`，不得合并这些维度。权威顺序为锁定 PDF > 经原页确认的派生内容 > 用户笔记/AI 内容；冲突进入 review queue。
   - 内容去重与 provenance 分离：规范化内容只存一份，通过多对多 source-facet/locator 表保存每个路径、层级、权威、核验状态和哈希；选代表文本不得删除其他来源事实或降低权威。
   - 摄取先固定输入快照与哈希，在临时 generation 目录完成 SQLite、JSONL、manifest 后验证，再持有跨进程锁原子切换单一 `CURRENT` 指针。失败 generation 不可见，旧 generation 可回滚；输入在哈希后变化则拒绝整次构建。
   - 知识原子保存稳定 `claim_id`、章节/节号、类型、中英术语、陈述、假设、量词、依赖、目标结论、三重锚点/Markdown 行号、来源版本与哈希、五个证据维度和误解标签。

   **产物矩阵：**

   | 产物 | Git | 规则 |
   |---|---:|---|
   | 解析器、schema、迁移、测试、PDF SHA、聚合不变量 | 是 | 不含教材摘录、译文、答案或截图 |
   | `wiki/raw/lftp.pdf` | 保持仓库现状，不复制/重打包 | 校验固定 SHA；保留书名、作者、MIT Press 来源与许可证说明；任何发布动作另行人工审查 |
   | 章节/Exercise 明细 manifest、索引、公式卡 | 否 | 位于 `.study/corpus/<generation>/`，可由锁定 PDF 确定性重建 |
   | 中文重述、题目、答案、判分、学习记录 | 否 | 本地私有，不进入 MkDocs，也不由工具写回 tracked 文件 |
   | 人工签认 | 否 | 存入 `state.sqlite3`，绑定 generation/hash、时间和签认状态 |

5. **把学习状态与 corpus 生命周期分开**
   - corpus generation 不可变；单独建立有迁移版本的 `.study/state.sqlite3`。
   - state 保存 Exercise 状态、attempt、完整重写、诊断、公式签认、人工复核、答案释放资格、每周小时和进度事件。
   - attempts/events append-only；更正通过新事件表达，不覆盖历史。每个事件引用固定 `corpus_generation`、claim/evidence ID 和哈希；漂移时进入复核，不自动迁移成绩。
   - 题目、rubric 和模型评分默认 `draft/provisional`。只有人工批准且证据全部解析成功才能影响 mastery；`manual_review=true` 不推进进度、不释放参考答案。
   - 每个 `.study/corpus/<generation_id>/corpus.sqlite3` 是单一 generation 拓扑，使用 `STRICT` 表（运行时 SQLite 支持时）和版本化迁移。核心 DDL 契约为：`generations(generation_id TEXT PRIMARY KEY, manifest_digest TEXT NOT NULL UNIQUE, pdf_sha256 TEXT NOT NULL, extractor_version TEXT NOT NULL, canonicalizer_version TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('building','ready','retired')), created_at TEXT NOT NULL)`；`contents(content_id TEXT PRIMARY KEY, content_sha256 TEXT NOT NULL UNIQUE, normalized_text TEXT NOT NULL)`；`source_facets(facet_id TEXT PRIMARY KEY, generation_id TEXT NOT NULL REFERENCES generations, content_id TEXT NOT NULL REFERENCES contents, tier TEXT NOT NULL CHECK(...), authority TEXT NOT NULL CHECK(...), verification TEXT NOT NULL CHECK(...), evidence_type TEXT NOT NULL CHECK(...), formula_uncertain INTEGER NOT NULL CHECK(formula_uncertain IN (0,1)), logical_path TEXT NOT NULL, locator_json TEXT NOT NULL, locator_hash TEXT NOT NULL, UNIQUE(generation_id,logical_path,locator_hash))`；`claims(claim_id TEXT PRIMARY KEY, generation_id TEXT NOT NULL REFERENCES generations, content_id TEXT NOT NULL REFERENCES contents, kind TEXT NOT NULL CHECK(...), chapter INTEGER, section TEXT, anchor_json TEXT NOT NULL, statement_zh TEXT NOT NULL DEFAULT '', statement_en TEXT NOT NULL DEFAULT '', UNIQUE(generation_id,claim_id))`。
   - provenance 关系由 `claim_facets(claim_id TEXT NOT NULL REFERENCES claims ON DELETE CASCADE, facet_id TEXT NOT NULL REFERENCES source_facets ON DELETE CASCADE, relation TEXT NOT NULL CHECK(relation IN ('origin','mirror','supports','contradicts')), PRIMARY KEY(claim_id,facet_id,relation))` 表示，禁止按共同 `content_id` 推断 claim-locator 关系。
   - 中文检索采用 generation 内的 `claim_search(search_id INTEGER PRIMARY KEY, claim_id TEXT NOT NULL UNIQUE REFERENCES claims, statement_zh TEXT NOT NULL, statement_en TEXT NOT NULL, terms TEXT NOT NULL)` 与外部内容 FTS5 trigram 表 `claims_fts(statement_zh,statement_en,terms,content='claim_search',content_rowid='search_id',tokenize='trigram')`，由迁移定义 insert/update/delete triggers 并在 doctor 中执行 rebuild/一致性检查。
   - corpus 只保存不可变检测记录：`review_items(review_id TEXT PRIMARY KEY, generation_id TEXT NOT NULL REFERENCES generations, target_type TEXT NOT NULL CHECK(target_type IN ('generation','claim','facet','claim_facet')), target_id TEXT NOT NULL, reason TEXT NOT NULL CHECK(...), payload_json TEXT NOT NULL, payload_hash TEXT NOT NULL, detected_at TEXT NOT NULL, UNIQUE(generation_id,target_type,target_id,reason,payload_hash))`。`target_id` 按类型保存 generation/claim/facet ID，或 canonical `claim_id|facet_id|relation`；应用层与 doctor 校验多态目标存在。不得在 corpus 保存 status/resolved_at。
   - review 的 resolved/dismissed/重新打开全部作为 `state.sqlite3` 中引用 `review_id` 与 generation 的 append-only/CAS 事件；查询时把 state fold 作为 overlay，不修改 generation。所有同库 FK 在 `PRAGMA foreign_keys=ON` 下由 migration/doctor 验证。
   - state 至少包含：`events(event_id UUID PK, idempotency_key UNIQUE, aggregate_type, aggregate_id, aggregate_version, event_type CHECK, corpus_generation, evidence_snapshot_json, evidence_snapshot_hash, payload_json, created_at, UNIQUE(aggregate_type,aggregate_id,aggregate_version))` 与 `schema_migrations(version PK, checksum, applied_at)`。
   - 事件写入使用 `BEGIN IMMEDIATE`：读取当前 aggregate version，校验 expected version，插入 `version+1`；唯一冲突返回稳定 `STATE_CONFLICT`，相同 idempotency key + 相同 payload 返回原结果，不同 payload 返回 `IDEMPOTENCY_MISMATCH`。fold 严格按 aggregate version，缺号/重复即 corruption；答案释放与 mastery 也通过同一 CAS 事务，不能双重释放。
   - 每个 state 引用的 generation 自动 pin；attempt 同时保存 canonical evidence snapshot/hash。GC 只删除未被 state 引用、非最近两个且超过 30 天的 generation。
   - 每次迁移先复制 state DB 到 `.study/backups/`，在副本执行迁移、`foreign_key_check`、`integrity_check` 和 fold 验证，通过后原子切换；保留最近 7 个备份。提供 `state doctor/backup/restore`，restore 也先验证并保留当前副本。

   **稳定 ID 公式：**
   - semantic manifest 使用 RFC 8785/JCS canonical JSON，并在序列化前强制 I-JSON：UTF-8、无重复 object key、数字必须可按 IEEE-754 有限值无歧义表示、拒绝 NaN/Infinity、字符串按 Unicode code point 保真。只包含 `schema_version`、PDF SHA/page count、extractor/canonicalizer version、按 logical relative path/role 排序的输入 SHA/size/tier/authority、按 ID 排序的 claim/content/facet/anchor 摘要、按 Exercise ID 排序的菱形 inventory。明确排除 `generation_id`、`created_at`、绝对路径、临时目录、机器名和运行时统计；这些只进入非语义 sidecar。
   - `manifest_digest = sha256(JCS(semantic_manifest))`，`generation_id = 'gen-' || manifest_digest`。数据库与 JSONL 构建完后重算 semantic manifest；相同输入/版本必须得到相同 generation_id，任何语义字段变化必须得到新 generation。
   - manifest 记录并固定 `extractor_version` 与 `canonicalizer_version`；语义变化必须创建新 namespace，不得复用旧 ID。
   - `content_id = sha256(canonicalizer_version || canonical_utf8_bytes)`。
   - PDF `claim_id = sha256(namespace || pdf_sha256 || printed_page || pdf_page || section || kind || normalized_bbox || content_sha256 || duplicate_ordinal)`；`duplicate_ordinal` 只在相同页面/section/kind/content/bbox 冲突时按固定视觉坐标排序产生，禁止使用 PyMuPDF block index。
   - Exercise 使用显式 `lftp:<pdf_sha256>:exercise:<chapter>.<number>`；Markdown claim 使用 `namespace || source_file_sha256 || heading_path || paragraph_content_sha256 || duplicate_ordinal`。升级 extractor 后保留旧 generation 与 ID 映射报告。

6. **使用能力感知的 DeepSeek provider**
   - 不使用即将退役的 `deepseek-chat` / `deepseek-reasoner`。建立按 provider + role 索引的 profile，显式包含 model、thinking、reasoning effort、timeout、retry、token/费用预算。
   - 中文重述、普通出题、Planner、Section Workers 使用 `deepseek-v4-flash` 并显式关闭 thinking；证明题、反例题、grader、critic 使用 `deepseek-v4-pro` 并显式开启 thinking。未来 OpenAI profile 独立配置，绝不沿用 DeepSeek slug。
   - DeepSeek JSON mode 只负责传输；本地用 JSON Schema/Pydantic 严格验证结构和语义不变量，并通过 mock server 契约测试精确 outbound payload。
   - 总 deadline 180 秒、全局最多 3 次网络调用；初始请求、HTTP 重试、`length` 再生成、非法 schema fresh generation 全部消耗同一个 attempt counter、deadline 和预留费用预算，不存在旁路第四次调用。每次 timeout 为 `min(55 秒, remaining_deadline - 已预留 backoff - 5 秒收尾预算)`，不足 10 秒不再发起。调用间 full-jitter 上限为 1 秒、2 秒。发起每次调用前预留该次最坏输入/输出/reasoning token 费用，超预算不调用。
   - HTTP/finish 表：408/429/500/502/503/504 与 `insufficient_system_resource` 可按上述预算重试；400/401/403/404/422 不重试；402 立即 `BUDGET_EXHAUSTED`；`stop` 进入 schema 校验；`length` 仅在预算允许时用更高输出上限重新生成一次；`content_filter`/refusal 直接人工复核。未知状态 fail closed。
   - 非法输出仅允许本地移除 UTF-8 BOM 与传输层首尾空白，不修补 JSON 字段或数学内容；仍非法则丢弃，并从原始不可变请求 fresh generation 一次，不能把坏输出回填给模型。
   - 费用使用版本化 price snapshot：provider/model、effective_at、USD/百万 input/output/cache/reasoning tokens、汇率来源/日期和 CNY 上限；实际 usage（含 reasoning tokens）回填。价格或汇率缺失则不进行在线冒烟。
   - `--local-only` 使用根本没有网络实现的 `LocalOnlyProvider`，不能只靠布尔标志。无 Key 时摄取、检索、审计、格式化、进度和离线测试均可运行。
   - 外发前展示字段、字符/token 数、脱敏结果和费用上限，首次或策略变化后要求明确同意。原始 EvidencePacket 保持不变；另建 `OutboundPacket`，其 digest 覆盖转换后文本，并保存仅本地可见的 source-ID -> outbound-ID/transformation map。
   - 默认扫描疑似密钥、令牌、邮箱、电话和身份证号；若命中公式、教材证据或 rubric 支撑文本，整次外发转人工复核，不自动遮盖。只允许对非证据型用户备注做显式红action；grader 的 support graph 必须绑定实际发送的 outbound evidence hash。只发送最小片段，不上传整本 PDF、整章或知识库。

7. **生成离线九章骨架与按周精读包**
   - Ch1-Ch9 全部生成不依赖 API 的目录、页码、术语槽位、命题/练习清单、菱形、公式队列和来源导航；AI 精读只按当前周生成。
   - 每节硬性包含三重锚点、中英术语、中文忠实重述、定义/假设/量词/结论、证明依赖、例子/边界/反例、Exercise 导航、误解、自检、证据编号和核验状态。
   - 不做整章逐页完整翻译。AI 内容初始为待核验；只有对齐锁定 PDF 才标为教材一致。
   - 核心公式生成原页截图、LaTeX 转写和页码核验卡；用户确认后才升级。未核验公式不能成为扣分的唯一依据。

8. **实现内容守恒的 `format` 与显式 `organize`**
   - 剪贴板/标准输入默认只在内存预览；用户选择“保存原文”后才写 `.study/inbox/`。单次默认上限 2 MiB、默认保留 30 天并提供清理命令；私有目录要求仅当前用户可访问，权限无法确认时拒绝外发。
   - `format` 使用自研保守 byte-span scanner 保存原始 UTF-8 slice；`markdown-it-py` 只做变更前后 CommonMark 语义校验，不作为无损 CST。edit allowlist 只能在已识别、非保护区 span 之间插入/替换格式字节。先实现原型门：对 fixture corpus 与 Hypothesis 生成的 UTF-8/畸形 Markdown，零操作必须 100% byte-exact round trip，保护区 slice 必须永不改变；原型未通过则不实现自动 edit。
   - LLM 只能返回引用节点 ID 的格式操作，不能返回改写全文。重渲染后要求每个内容单元恰好一次、正文/标点/公式/代码哈希及顺序不变、非白名单 AST 语义节点不变；代码和公式内部逐字节不变。无法证明守恒则 fail closed。
   - `organize` 显式启用 Planner -> Workers -> Critic -> 确定性组装，但 V1 只写 `.study/proposals/` / `.study/organized/`，工具禁止写回 tracked 文件。用户若要采用内容，只能在工具外人工复制；新增 raw HTML、远程 URL、MkDocs snippets/include、脚本/事件属性或其他 active construct 时仍拒绝导出。
   - 所有 root、PDF、语料、输出路径执行 realpath containment，拒绝 `..`、symlink、junction 或解析后逃出项目/显式 allowlist 的路径。
   - V1 格式化只允许写入用户指定的、不存在的新输出文件，绝不 replace 现有用户路径。先在同目录用 `O_CREAT|O_EXCL` 创建唯一私有 `.partial` 文件，完整写入、flush、fsync 并关闭；发布只允许从该 fully synced 同卷临时文件执行原子 no-replace hard-link（POSIX `link(temp,dest)`；Windows `CreateHardLinkW`）。目标存在返回 `OUTPUT_EXISTS`；文件系统不支持可靠 hard-link/no-replace 则返回 `ATOMIC_PUBLISH_UNSUPPORTED`，绝不 fallback 为直接创建并复制最终目标。成功 link 后 fsync 目录（平台支持时）并删除临时链接；crash 最多遗留 `.partial` 或已完整 final，不产生截断 final。
   - corpus/state/`.study` 内部操作采用 `portalocker` 的 OS-backed exclusive lock；锁文件为 `.study/locks/<sha256(realpath-or-resource-id)>.lock`，多锁按哈希字典序获取，10 秒超时返回 `LOCK_TIMEOUT`，文件句柄覆盖整个事务/指针切换并由 OS 在进程退出时释放。用两个独立 Windows 进程验证互斥、超时、排他发布和 crash release。

9. **构造不可篡改、语义受审的 EvidencePacket**
   - canonical packet digest 覆盖 corpus generation、excerpt、authority、tier、verification、evidence type、formula uncertainty、locator 和顺序。
   - 每次加载重算 entry 哈希与 packet ID，并解析到固定 corpus generation；任何差异在模型调用前 fail closed。
   - 合法证据 ID 不代表语义相关。rubric 保存“评分项 -> 支撑 claim/evidence”的 support graph；题面、答案、rubric 经人工批准前保持 draft。
   - 每个评分项至少有一条已核验核心证据。公式不确定的抽取文本不能单独支撑扣分。
   - 判分器只选择预定义等级，程序重算总分；每项反馈包含答案位置、理由、修正和出处，不宣称形式验证。
   - 首次未通过不给完整答案，第二次给证明骨架，完整重写后才可查看参考答案。引用漂移、冲突、grader/critic 分歧、证据不足、公式/量词不可靠、空答案、伪造页码或 injection 均进入人工复核；复核前不推进 mastery。

10. **执行 8 周、每周 20 小时学习计划**
    - W1（7/12-7/18）：全九章诊断、Ch1-Ch2；W2（7/19-7/25）：Ch3；W3（7/26-8/1）：Ch4；W4（8/2-8/8）：Ch5；W5（8/9-8/15）：Ch6；W6（8/16-8/22）：Ch7；W7（8/23-8/29）：Ch8；W8（8/30-9/5）：Ch9 与跨章总结。
    - 常规每周 17 小时新内容、3 小时错题；最后一周 14 小时 Ch9、6 小时总结。诊断通过可压缩讲解，但不跳过章节地图、核心假设、来源和必做 Exercise。
    - 每章诊断 1 证明、1 反例、2 补洞；综合至少 80/100 且无致命误解，权重为 45/25/20/10。
    - 96 道无菱形 Exercise 全部留下有效作答并检查，最终为“通过”或“已纠正”；首次可错，但必须完整重写。单菱形只选核心证明链相关题，双菱形及以上仅导航。
    - 每周按实际小时、Exercise 闭环、诊断和复核积压预测期限；缺口 >4 小时标黄，>20 小时标红。落后时依次暂停笔记美化、缩短补充解释、减少单菱形、取消额外生成题；核心正文、96 题、核心公式、诊断和致命误解清零不可压缩。

11. **提供够用的中文 CLI**
    - 保留可测试子命令，并增加 `aimath-study start`，串联教材检查、本周任务、粘贴格式修复、笔记 proposal、出题、判分、进度和复核队列。
    - 修复中文源码/输出乱码和 Windows GBK 控制台的菱形崩溃；数据始终存真实 Unicode，显示层可安全替代。
    - V1 不开发 Web/桌面 UI；菜单不得挤占内容正确性。

12. **使用量化验收门和受限在线冒烟**
    - 固定命令：`uv sync --frozen`、`uv run ruff check src tests`、`uv run mypy src`、`uv run pytest -q`。
    - 版本化 `tests/fixtures/retrieval_zh_v1.json`，仅含查询与预期 section/Exercise ID（不含教材摘录）；golden recall 必须 100%。属性测试 seeds 固定为 `[0, 1, 7, 42, 20260712]`。
    - 并发测试包含同步 barrier 控制的确定性交错，以及 20 次独立多进程 randomized stress（每次记录 seed、PID、临时目录和调度事件）；不能用同一 seed 简单重复冒充调度覆盖。摄取连续 2 次比较 canonical digest。
    - 154/96 inventory 必须展示逐章差异，并由用户签认 generation/hash 后才能标为 verified。
    - 模型调用写脱敏 telemetry：provider/profile、thinking、请求/证据哈希、attempt、延迟、token usage、费用、终止状态和错误码；不保存密钥、完整答案或未脱敏外发正文。
    - DeepSeek 冒烟：1 道题、1 个短答案判分、1 段短笔记。总输入 <=20,000 tokens、输出 <=4,000 tokens、费用 <=人民币 5 元；无 usage/无法估价则停止。非法 schema、429、超时等路径用 scripted fake/mock 注入，不要求在线模型故意失败。
    - Windows 回归覆盖中文用户名、UTF-8/BOM、默认控制台、菱形、无 API Key。默认命令不得修改用户源文件。
    - 最终交付运行说明、验收报告、已知限制、`.study/` 数据说明和第一周任务。

## Key decisions & tradeoffs

- 锁定 PDF 是最高权威；来源权威、语料层级、核验状态、证据类型和公式不确定性分别建模。
- 当前使用 DeepSeek V4：Flash 非思考处理日常任务，Pro 思考模式处理证明、反例、判分和 critic；旧 `deepseek-chat` 不进入实现。
- 先交付不会阻塞阅读的 Phase 0；笔记组织和 AI 扩写不得占据学习关键路径。
- 8 周约 160 小时，诊断调节讲解深度，但不豁免核心正文和 96 道无菱形 Exercise。
- `format` 宁可拒绝也不暗改内容；`organize` 只生成 proposal，应用必须人工确认。
- corpus 不可变、state append-only；重建索引不能销毁学习历史。
- 题目、rubric、模型成绩先为 provisional，证据与人工门未通过时不能推进 mastery。
- 核心库与先修库隔离；界面、AI 扩写和笔记美化让位于内容真值与闭环。

## Risks / open questions

- 96 道必做题加九章正文仍偏紧；周报必须尽早报告真实缺口，不能降低门槛。
- DeepSeek V4 的账号可用性、限流、usage 和 thinking 行为需由契约测试与在线冒烟确认。
- PDF 数学抽取不可靠；用户公式签认可能成为瓶颈。
- 154/96 必须逐题人工签认，不能把自动统计当最终真值。
- DeepSeek 会接收用户批准的最小片段；即使脱敏仍存在供应商留存和数据地域风险，首次外发必须直示。
- Windows 文件锁、ACL、junction 和控制台编码需要真实环境回归，不能只用 mock。
- MkDocs 既有失败与本项目新增回归必须分别报告。

## Out of scope

- Ch10-Ch15 / Part III；逐页完整中文翻译；公开发布教材衍生内容。
- Web/桌面 UI、向量数据库、常驻服务。
- GPT-5.6 在线依赖或原生 multi-agent beta。
- Lean/Coq 形式验证或宣称 LLM 判分等同形式验证。
- 自动修改不确定公式、自动覆盖用户笔记、静默模型降级。
- 验收阶段批量生成九章 AI 内容。
