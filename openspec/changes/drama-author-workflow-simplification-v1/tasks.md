# 实施任务

本清单属于 `CONTRACT` 阶段的可执行后续计划；所有实现任务当前均为 `[ ]`，不得在本阶段勾选。根五 change strict gate 通过后，才允许进入 AI Drama Skills source 实现。禁止修改运行副本、profiles、Auctra/Scaena 产品代码、ProductionGraph、资产或其它 owner 合同。

## 1. Starter 退出 recipe/layout（可与 2 并行）

- [x] 1.1 **PHASE:** `BACKEND`；**OWNER:** ai-drama source writer；**IMPLEMENTED:** starter now reads existing project/owner status, creates only needed ordinary author guidance, and no longer generates recipe/layout; obsolete starter reference and generator removed.
- [x] 1.2 **PHASE:** `BACKEND`；**OWNER:** ai-drama source writer；**IMPLEMENTED:** README and starter state canonical screenplay/review/production boundaries and natural author entry.

## 2. 剧本作者方法与唯一入口

- [x] 2.1 **PHASE:** `BACKEND`；**OWNER:** ai-drama router source writer；**IMPLEMENTED:** router documents five author actions, one primary/one constraint, format decision, canonical episode text and scene source spans.
- [x] 2.2 **PHASE:** `BACKEND`；**OWNER:** ai-drama source writer；**IMPLEMENTED:** canon boundary reference documents Auctra/Scaena/Eikona ownership and local/remote handoff gates.

## 3. 远程 authoring 与自然词

- [x] 3.1 **PHASE:** `CONTRACT`；**OWNER:** ai-drama source writer；**IMPLEMENTED:** starter/router guidance documents remote discovery, scoped refs, queued status, typed failures and no-CLI client boundary.
- [x] 3.2 **PHASE:** `BACKEND`；**OWNER:** ai-drama source writer；**IMPLEMENTED:** author-facing starter/router text uses natural terms and preserves machine protocol identifiers.

## 4. Profile/sync 交接与 strict 校验

- [ ] 4.1 **PHASE:** `CONTRACT`；**OWNER:** ai-drama source writer + host manager handoff；**OWNED PATHS:** 本 change tasks/spec evidence；**SHARED READ PATHS:** `.skills/profiles/targets/**`（只读）、creative/novel changes；**FORBIDDEN PATHS:** 直接编辑 profile/runtime copies。**依赖:** 1–3.2；**变更:** 记录剧本创作 profile 最终常驻 `ai-drama-router`、`yeisme-auctra-cli-runtime`；专项 writer、编码、目录生成和其它细分方法按需，宿主后续用 manager 修改；**验收:** profile mutation 为 integration dependency，不在本 change 发生；**FOCUSED_VERIFICATION:** `scripts/skills.sh validate-profiles`（后续 integration，本 CONTRACT 不执行）；**EVIDENCE_TARGET:** tasks 与 handoff；**STOP_CONDITION:** owner 边界可执行即停；**INTEGRATION_DEPENDENCY:** root 五 change gate 后执行。

- [ ] 4.2 **PHASE:** `CONTRACT`；**OWNER:** ai-drama source writer；**OWNED PATHS:** 本 change `proposal.md`、`design.md`、`tasks.md`、`specs/drama-author-workflow/spec.md`；**SHARED READ PATHS:** design、service contract；**FORBIDDEN PATHS:** implementation code/runtime copies/profiles。**依赖:** 1–4.1；**变更:** 保持所有 checkbox `[ ]`，补齐 owner、paths、依赖、验收、verification、evidence、stop condition、integration dependency；**验收:** strict 通过；规格覆盖 starter、唯一 router、剧本方法、local/remote guidance、owner boundary 与 profile handoff；**FOCUSED_VERIFICATION:** `cd .skills/yeisme/ai-drama && openspec validate drama-author-workflow-simplification-v1 --strict --no-interactive`；**EVIDENCE_TARGET:** change directory 与最终结构化输出；**STOP_CONDITION:** strict 通过后结束 CONTRACT；**INTEGRATION_DEPENDENCY:** root 五 change gate 后才能开始 source implementation。

## 依赖、状态与范围锁

依赖图：`1.1 → 1.2`；`2.1 → 2.2`；`3.1` 等待 Auctra target contract；`3.2` 依赖 1.1/2.1；`4.2` 收尾。当前实现已完成 starter source、router/owner handoff、local/remote guidance、自然词和 source validators；profile/runtime sync、真实服务、生产、付费 provider 与跨 owner 旅程仍为 integration dependency。