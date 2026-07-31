# Plan Review Log: LFTP 前九章可验证学习系统修复与落地
Act 1 (grill) complete - plan locked with the user. MAX_ROUNDS=5.

## Review prerequisite attempt - not counted as Round 1

- Codex CLI: `0.136.0`
- Authentication: logged in with ChatGPT
- Safety: initial review was launched with `-s read-only`
- Thread started: `019f515e-f309-7ef3-a7f3-cfe35d2ebd99`
- Result: no critique and no verdict were produced. The turn failed after retries because the configured default model `gpt-5.6-sol` requires a newer Codex version.
- Decision: stop without changing models or fabricating convergence. Upgrade the Codex app/CLI, then restart Act 2 with a fresh read-only review session; this failed prerequisite attempt does not consume one of the five review rounds.
- Resolution: with user authorization, upgraded the npm-installed `@openai/codex` from `0.136.0` to stable `0.144.1`; authentication and the existing `ultra` reasoning configuration now load successfully. Formal Round 1 starts in a fresh session.

## Round 1 - Codex

The plan is not implementation-ready. Material blockers remain:

1. **No viable critical path.** The 160-hour schedule begins July 12 and allocates all eight weeks to study, while the substantial rebuild has no engineering budget or readiness milestone. **Fix:** Add a time-boxed Phase 0 with an acceptance gate, or reduce V1 to a verified manifest, attempt ledger, manual review, and basic CLI while deferring note organization and AI enrichment.
2. **The artifact policy prevents reproducible bootstrapping.** All textbook-derived material is ignored, but reproducible ingestion needs a canonical manifest, and the CC BY-NC-ND boundary is unspecified. **Fix:** Define an artifact matrix and either version metadata-only truth or specify deterministic rebuild from the hash-locked PDF.
3. **Core/supplement isolation is not representable.** Current config ingests all `docs`/`wiki`; schema lacks corpus tier and retrieval cannot demand verified core evidence. **Fix:** Add an allowlisted source registry and persist tier, authority, and verification separately.
4. **Deduplication can silently downgrade authority.** Path-selected representative dedup can replace a verified source facet with a user-note facet. **Fix:** Deduplicate content separately from source facets with many-to-many provenance.
5. **Evidence bundles are editable without detection.** Packet and entry hashes are not fully recomputed/resolved on load. **Fix:** Canonically hash every relevant field and resolve against a pinned corpus generation before model calls.
6. **Formula verification disappears before grading.** Evidence packets omit verification/formula uncertainty, so corrupted PDF extraction may support deductions. **Fix:** Carry evidence type and verification into packets and require verified per-rubric support.
7. **Mutable learning state has no persistence design.** Corpus rebuild can destroy attempts and grades overwrite prior output. **Fix:** Create separately migrated `state.sqlite3` with append-only events referencing immutable generations.
8. **Crash and concurrency safety are incomplete.** Corpus artifacts publish independently and note apply has a final check/replace race. **Fix:** Build immutable input generations behind one locked pointer and lock note targets through replacement.
9. **Chinese retrieval is broken.** FTS5 `unicode61` does not match ordinary Chinese substrings. **Fix:** Use trigram/deterministic segmentation plus a golden recall suite.
10. **Provider routing cannot express the plan.** Current contract lacks thinking/effort and provider-specific role profiles. **Fix:** Add capability-aware profiles and exact outbound contract tests.
11. **Retry and offline guarantees are unspecified.** No error matrix, backoff, deadline, budget behavior, or hard network-free provider exists. **Fix:** Specify a retry state machine, use scripted fault injection, and enforce local-only structurally.
12. **Evidence IDs do not establish semantic support.** Valid but irrelevant IDs can pass; provisional/manual-review grades may still affect learning state. **Fix:** Require human-approved support graphs and prohibit provisional state transitions/answer release.
13. **Note guarantees exceed validator power.** Whitespace can change CommonMark semantics and organize can introduce active constructs or conflict with `.study`-only output. **Fix:** Use CST allowlisted edits and keep organize preview-only until human approval with active-construct checks.
14. **Raw capture and outbound privacy are unsafe.** Paste retention, quotas, permissions, redaction, consent, and path containment are missing. **Fix:** Add outbound preview/consent, secret/PII redaction, retention/size controls, private permissions, and realpath containment across traversal links.
15. **Acceptance and observability are non-measurable.** Gates lack commands, repetitions and budgets; telemetry lacks usage/cost/outcome. **Fix:** Publish exact gates, stress counts, a signed inventory, and redacted per-call telemetry.

VERDICT: REVISE

### Codex's response

- Accepted all 15 findings because each mapped to a concrete repository or lifecycle failure.
- Added Phase 0 (July 14) and Gate B (July 18), with note organization and AI enrichment removed from the study critical path.
- Added an explicit artifact matrix and deterministic local rebuild policy that versions no textbook excerpts or translated content.
- Added separate corpus dimensions, many-to-many provenance, immutable generations, a locked `CURRENT` pointer, and an append-only `state.sqlite3`.
- Strengthened EvidencePacket canonical hashing, corpus-generation resolution, formula verification propagation, per-rubric support graphs, and provisional-grade blocking.
- Switched Chinese search to trigram/verified segmentation and added a 100% golden recall gate.
- Defined provider role profiles, V4 thinking modes, retry/error/deadline/budget behavior, a network-incapable local-only provider, and deterministic fault injection.
- Restricted `format` to CST allowlisted edits; made `organize` proposal-first with active-Markdown checks, human confirmation, path containment, retention, redaction and cross-process locking.
- Added exact quality commands, ten-run stress gates, inventory signatures, telemetry fields, and hard online-smoke budgets.
- Rejected no substantive Round 1 finding. Also corrected an unexpected drift that had changed the locked V4 decision back to legacy `deepseek-chat` while the review was running.

## Round 2 - Codex

Most prior findings are addressed. Eleven material gaps remain:

1. Phase 0 gives the user an impossible two-hour budget to sign 154 exercises and formula cards, while W1 precedes Gate B. Fix: make inventory provisional, budget verification realistically, and provide a manual PDF/ledger fallback.
2. The artifact matrix omits the currently tracked source PDF and contradicts the `.study` rule by allowing model output into tracked notes. Fix: add PDF/license/attribution policy and prohibit tracked-file writes or define a precise human-acceptance exception.
3. Corpus/state schemas are field lists rather than integrity contracts. Fix: define keys, checks, migrations, event identity, idempotency, aggregate versions and deterministic folds with CAS.
4. Stable IDs are extractor-dependent. Fix: define ID preimages, pin extractor/canonicalizer versions and namespace semantic changes.
5. Referenced generations lack retention/recovery. Fix: pin generations, snapshot evidence and define backup, restore, migration rollback, integrity checks and GC.
6. Retry timing is inconsistent/incomplete. Fix: allocate remaining deadline, cover HTTP/finish reasons, reserve worst-case retry cost, and version price/FX snapshots.
7. Structure repair is ambiguous and could mutate meaning. Fix: allow only lossless transport normalization; otherwise fresh-generate from the immutable request.
8. Redaction breaks frozen evidence. Fix: separately hash outbound packets and abort when redaction touches evidence/math.
9. Cross-platform locking has no chosen implementation/protocol. Fix: select an OS-backed primitive and define lock naming, order, timeout, lifetime and Windows two-process tests.
10. CommonMark byte conservation lacks a parser choice/prototype. Fix: choose a source-span-preserving parser/scanner and prove round trips before edit operations.
11. Numeric gates have undefined fixtures/seeds. Fix: version metadata-only golden query expectations, publish seeds, and combine deterministic barriers with randomized multi-process stress.

VERDICT: REVISE

### Codex's response

- Made Phase 0 inventory provisional, added a manual PDF/ledger fallback, and moved full verification into the week each chapter is studied.
- Added the source PDF/license row and prohibited all V1 tool writes to tracked files; organize exports only to `.study`.
- Added concrete corpus/state table constraints, event idempotency and CAS fold rules, stable error codes, migration-copy validation, backups, restore and generation GC pins.
- Defined all stable-ID preimages, pinned extractor/canonicalizer namespaces, removed block-index identity, and required mapping reports on upgrades.
- Replaced the retry sketch with a deadline-feasible attempt allocation, HTTP/finish table, fresh-generation rule, worst-case budget reservation and versioned price/FX snapshots.
- Split original and outbound packet identities; redaction touching evidence or mathematics now blocks for review.
- Chose `portalocker` for internal OS-backed locks, specified lock naming/order/timeout/handle lifetime and Windows process tests; removed unsafe in-place note overwrite from V1.
- Chose a custom lossless byte-span scanner plus `markdown-it-py` semantic validation, gated by fixture and Hypothesis byte-round-trip prototypes.
- Defined a metadata-only Chinese recall fixture, exact seeds, barrier interleavings and 20 independent randomized multi-process stress runs.

## Round 3 - Codex

Most Round 2 findings are resolved. Four material blockers remain:

1. Corpus DDL lacks `claim_facets`, generation-scoped FTS/indexing and a concrete review queue, so provenance can cross-attach. Fix: provide complete typed migration topology and foreign keys.
2. `generation_id` and canonical manifest identity are undefined. Fix: define canonical serialization, exclude volatile fields and derive the generation ID from its digest.
3. HTTP retry, `length` regeneration and invalid-schema generation can exceed the stated three calls. Fix: make every network call share one global counter/deadline/cost budget.
4. “New output only” still races a non-cooperating writer. Fix: publish with OS-level exclusive-create semantics and never replace an existing path.

VERDICT: REVISE

### Codex's response

- Added concrete generation-local DDL with typed/nullability/check contracts for generations, contents, facets and claims; added `claim_facets`, external-content trigram FTS tables/triggers, review items, complete foreign keys and doctor checks.
- Defined RFC 8785/JCS semantic manifest fields and exclusions; `generation_id` is now exactly `gen-<sha256(canonical semantic manifest)>`.
- Declared one global maximum of three network calls covering initial requests, HTTP retries, length regeneration and schema regeneration, all sharing deadline and cost reservation.
- Defined non-overwriting output publication through same-directory private temp files plus POSIX hard-link/Windows `CreateHardLinkW` or `CREATE_NEW`; existing destinations fail and are never replaced.

## Round 4 - Codex

Three material blockers remain:

1. Immutable corpus still contains mutable review status/resolution. Fix: keep detection immutable and overlay resolution from state events.
2. Review uniqueness uses nullable claim/facet targets, which SQLite UNIQUE does not enforce as intended. Fix: use non-null target type/ID or partial unique indexes.
3. Windows `CREATE_NEW` copy fallback can crash after publishing a truncated final. Fix: require atomic same-volume no-replace link/rename and fail closed when unavailable.

VERDICT: REVISE

### Codex's response

- Replaced mutable corpus review status with immutable, non-null `target_type/target_id` detection records; all resolution/dismissal/reopen decisions are append-only state events overlaid at query time.
- Replaced nullable uniqueness with `(generation,target_type,target_id,reason,payload_hash)` and defined canonical compound target IDs.
- Removed the Windows direct-copy fallback. Publication now requires a fully synced same-volume `.partial` file plus POSIX `link`/Windows `CreateHardLinkW`; unsupported filesystems fail closed and cannot expose truncated finals.
- Also made RFC 8785 identity explicitly enforce I-JSON constraints.

## Round 5 - Codex

No material implementation blockers remain.

- Corpus topology now preserves provenance, generation-scoped search, and immutable review detections with state-event resolution overlays.
- Generation identity correctly applies RFC 8785/JCS with I-JSON constraints and excludes volatile fields.
- Retry, evidence, privacy, locking, crash publication, state CAS/recovery, Markdown safety, and quantitative acceptance gates are sufficiently defined and fail closed where platform guarantees are unavailable.

The remaining items in “Risks / open questions” are execution risks covered by explicit validation gates, not unresolved design decisions.

VERDICT: APPROVED

### Codex's response

- Accepted the approval without further plan changes.
- Act 2 converged at the MAX_ROUNDS boundary: five formal review rounds, with the final round approved.
