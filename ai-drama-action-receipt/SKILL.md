---
name: ai-drama-action-receipt
description: Use when a drama production action needs an authorization boundary, an ApprovalWindow, idempotency, bounded retry, an exact ACCEPTED/COMPLETED/REVIEWED vocabulary, a 断线 recovery decision, a GenerationCapability<kind> invocation receipt, or one consistent action receipt across CLI, MCP and the control center. Use for 执行收据、能力调用合同、审批窗口、幂等、自动重试、UNKNOWN 恢复、状态词汇对齐; do not author screenplays, generate media, choose assets, or write owner state.
---

# 做剧动作收据与恢复

本 Skill 是 DEK v1 的**合同层与能力调用收据 owner**，定义并校验 `yeisme.owner_action.v1` 与 `GenerationReceipt`。它把冻结引用、幂等键、审批窗口、提交引用和事件流统一成一套语义，不新增生成能力、不新建第二个 router。

**一个作用**：三类生成（`image|video|audio`）统一为 `GenerationCapability<kind>`；CLI / MCP / HTTP / SDK / 第三方只是 `GenerationBinding`，流程不感知入口。详见 [references/capability-invocation.md](references/capability-invocation.md)。

## 用途

- 判断一次动作是否具备「`ApprovalWindow` + 冻结计划 + scope digest + 幂等键 + 人工确认」资格；
- 消费 `GenerationReceipt`（`capability_id` / `kind` / `binding_ref` / `retry_used` / `approval_ref`），校验一次能力调用是否闭合；
- 把 `ACCEPTED / COMPLETED / BOUND / REVIEWED / TERMINAL_REJECTED / UNKNOWN / PARTIAL` 分开报告，禁止互相冒充；
- 判断可重试错误是否可在 `retry_budget=2` 内自动重试，以及 UNKNOWN 是否只能 `reconcile`；
- 断线、超时、`unknown_accept` 之后给出恢复动作，而不是重提；
- 让远程 CLI、MCP、控制中心消费同一个 `action_id + event_cursor`。

## 真实承载（不新造）

| 抽象 | 现有实现 |
| --- | --- |
| `FrozenRef` | `frozen intent/spec/bundle ref+digest`、`eikona.asset_handoff.v2` 的 `artifact.sha256` / `binding_digest`、`auctra.production_handoff.v1` 的 `canon_digest` |
| `IdempotentGrant` | `eikona review decide --expected-version 0 --idempotency-key OPERATION_KEY --confirm --agent`；Scaena 执行前非空 idempotency key |
| `Outcome` | `submission_ref`、`reconcileVideoProviderTask`、`unknown_accept`；Eikona `replacement_status` 与 `permission: handoff_candidate` |
| `event_cursor` | `eikona events tail <run_id> --json`、`scaena workflow status --agent`、控制中心 `yeisme.work_queue.v1` 签名 cursor |
| `GenerationCapability<kind>` | `image`=Eikona（`eikona generate` / `eikona.execute` / `/api/v1/generate`）、`video`=Scaena/Aigora（`scaena video generate` / `submission_ref`）、`audio`=Sonora（`sonora audio` / `episode-audio` / `audition`） |
| `ApprovalWindow` / `retry_budget` | 一次审批覆盖窗口内全自动；可重试错误最多 2 次，`reconcile` 不消耗预算 |

合同全文：[https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/contracts/owner-action.v1.md](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/contracts/owner-action.v1.md)。

## 输入 / 输出

- 输入：`DramaRoutePlan v1` 的 `stage_plans[]` / `gates[]` / `automation_profile`；`GenerationIntent`（`FrozenRef{ref,digest}` + typed controls）；`ApprovalWindow`；owner CLI 产出的 `GenerationReceipt`。
- 输出：只读的资格结论、`GenerationReceipt` 消费建议、重试/恢复决策。**receipt 本身由 owner CLI 的 `--json` 产出，本 Skill 不手写 JSON/YAML/receipt 文件**。

## 边界

- 不创作、不调 provider、不写 `.scaena` / SQLite / manifest / receipt；
- 不把 `eikona accepted` 写成 `production_ready`，不把 `pending_review` 写成 `export ready`；
- 不建跨 owner 网关、不把 `cli/mcp` 做成流程分支；Eikona 与 Scaena 各自执行自己的 EU；
- 不询问 `cli|mcp|both`；resolver 只选 `executable` binding，`planned/readonly/unavailable` fail-closed；
- 不在 UNKNOWN 写 / 已 `ACCEPTED` / 业务·权限·语义拒绝 / 创意输入变化时重试；`reconcile` 不消耗 `retry_budget`；
- 不返回 provider key、Authorization header、raw payload 或 private prompt。

## 最小流程

1. 从 `DramaRoutePlan` 确定本阶段 `canonical_owner`、`kind`、EU id 与 `automation_profile`。
2. 核对 `ApprovalWindow`（`capability_kinds[]` / `intent_digest` / `binding_allowlist` / `count` / `cost_ceiling` / `retry_budget`）与 `plan_ref + plan_sha256`、`scope_digest`、`idempotency_key`、`confirm_receipt.actor`。
3. 执行前对照 [outcome-recovery.md](references/outcome-recovery.md) 检查未闭合的 UNKNOWN；对照 [capability-invocation.md](references/capability-invocation.md) 判断当前错误是否属于可重试范围、`retry_used` 是否未超限。
4. resolver 只选 `executable` binding；由 owner CLI 执行冻结动作，读取统一 envelope 的 `data` 与 `GenerationReceipt`。
5. 按 `Outcome` 分开报告：已接收 / 已完成 / 已绑定 / 已复核 / 整体完成；把 `binding_ref` / `retry_used` / `event_cursor` 交给下游与控制中心。越界或耗尽交 `needs_decision`。

## 恢复决策

见 [references/outcome-recovery.md](references/outcome-recovery.md) 与 [references/capability-invocation.md](references/capability-invocation.md)。核心两句：

- **UNKNOWN 只读 `reconcile` 原 `action_id`**，不换幂等键、不换模型、不新建 state 路径、不换 owner，且**不消耗重试预算**；
- **可重试错误**（瞬时网络 / 5xx / 429 / 超时且 `mutationAttempted=false` / `binding=unavailable`）在 `retry_budget=2` 内自动重试，每次保持同一 `action_id` + `idempotency_key` + `intent_digest` + `approval_ref`；耗尽交 `needs_decision`。

## 验证

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
scripts/skills.sh validate-runtime
```

## 按需引用

- [references/capability-invocation.md](references/capability-invocation.md)：**能力调用合同**（4 对象、三类 kind、审批窗口、重试规则、receipt 字段）
- [references/outcome-recovery.md](references/outcome-recovery.md)：Outcome 与恢复决策表
- 能力抽象全文：[https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/capability-abstraction.md](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/capability-abstraction.md)
- 抽象全表：[https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/abstract-design.md](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/abstract-design.md)
- EU 目录与 DAG：[https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/execution-units.md](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/execution-units.md)
