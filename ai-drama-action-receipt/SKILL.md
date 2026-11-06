---
name: ai-drama-action-receipt
description: Use when a drama production action needs an authorization boundary, idempotency, an exact ACCEPTED/COMPLETED/REVIEWED vocabulary, a断线 recovery decision, or one consistent action receipt across CLI, MCP and the control center. Use for 执行收据、幂等、UNKNOWN 恢复、状态词汇对齐; do not author screenplays, generate media, choose assets, or write owner state.
---

# 做剧动作收据与恢复

本 Skill 是 DEK v1 的合同层，定义并校验 `yeisme.owner_action.v1`。它把 Auctra / Scaena / Eikona / Aigora / 控制中心已经存在的冻结引用、幂等键、提交引用和事件流统一成一套语义，不新增生成能力。

## 用途

- 判断一次动作是否具备「冻结计划 + scope digest + 幂等键 + 人工确认」资格；
- 把 `ACCEPTED / COMPLETED / BOUND / REVIEWED / TERMINAL_REJECTED / UNKNOWN / PARTIAL` 分开报告，禁止互相冒充；
- 断线、超时、`unknown_accept` 之后给出恢复动作，而不是重提；
- 让远程 CLI、MCP、控制中心消费同一个 `action_id + event_cursor`。

## 真实承载（不新造）

| 抽象 | 现有实现 |
| --- | --- |
| `FrozenRef` | `frozen intent/spec/bundle ref+digest`、`eikona.asset_handoff.v2` 的 `artifact.sha256` / `binding_digest`、`auctra.production_handoff.v1` 的 `canon_digest` |
| `IdempotentGrant` | `eikona review decide --expected-version 0 --idempotency-key OPERATION_KEY --confirm --agent`；Scaena 执行前非空 idempotency key |
| `Outcome` | `submission_ref`、`reconcileVideoProviderTask`、`unknown_accept`；Eikona `replacement_status` 与 `permission: handoff_candidate` |
| `event_cursor` | `eikona events tail <run_id> --json`、`scaena workflow status --agent`、控制中心 `yeisme.work_queue.v1` 签名 cursor |

合同全文：[https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/contracts/owner-action.v1.md](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/contracts/owner-action.v1.md)。

## 输入 / 输出

- 输入：`DramaRoutePlan v1` 的 `stage_plans[]` / `gates[]`；上游 EU 的 `FrozenRef{ref, digest}`；用户明确授权原文。
- 输出：只读的资格结论与 `action_id` 消费建议。**receipt 本身由 owner CLI 的 `--json` 产出，本 Skill 不手写 JSON/YAML/receipt 文件**。

## 边界

- 不创作、不调 provider、不写 `.scaena` / SQLite / manifest / receipt；
- 不把 `eikona accepted` 写成 `production_ready`，不把 `pending_review` 写成 `export ready`；
- 不建跨 owner 网关；Eikona 与 Scaena 各自执行自己的 EU；
- 不返回 provider key、Authorization header、raw payload 或 private prompt。

## 最小流程

1. 从 `DramaRoutePlan` 确定本阶段 `canonical_owner` 与 EU id。
2. 核对 `plan_ref + plan_sha256`、`scope_digest`、`idempotency_key`、`confirm_receipt.actor`。
3. 执行前对照 [outcome-recovery.md](references/outcome-recovery.md) 的恢复决策表检查是否有未闭合的 UNKNOWN。
4. 由 owner CLI 执行冻结动作，读取统一 envelope 的 `data`。
5. 按 `Outcome` 分开报告：已接收 / 已完成 / 已绑定 / 已复核 / 整体完成，并把 `event_cursor` 交给下游与控制中心。

## 恢复决策

见 [references/outcome-recovery.md](references/outcome-recovery.md)。核心一句：**UNKNOWN 只读 reconcile 原 `action_id`，不换幂等键、不换模型、不新建 state 路径、不换 owner**。

## 验证

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
scripts/skills.sh validate-runtime
```

## 按需引用

- 抽象全表：[https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/abstract-design.md](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/abstract-design.md)
- EU 目录与 DAG：[https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/execution-units.md](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/execution-units.md)
