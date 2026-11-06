# 能力调用合同（GenerationCapability / Receipt）

> 唯一真源：聚合仓 `yeisme-agent-my-skills` → `docs/drama-execution-kernel/capability-abstraction.md`。本文是 `ai-drama-action-receipt` 的按需速查，不复制全文。

## 一个作用

`GenerationCapability<kind>`，`kind = image | video | audio`。CLI / MCP / HTTP / SDK / 本地 / 第三方都只是 `GenerationBinding`；流程不感知入口，**不询问 `cli|mcp|both`**，resolver 只选 `discover() = executable` 的 binding，理由写 `receipt.binding_ref`。

## 四个对象

| 对象 | 内容 |
| --- | --- |
| `GenerationIntent` | `FrozenRef{ref,digest}` + typed controls + `IdempotentGrant` + `approval_ref` |
| `GenerationCapability<kind>` | `invoke(intent) -> GenerationReceipt`，`role = generator` |
| `GenerationBinding` | `discover()` / `adapt()` / `normalize()` / `reconcile()`；`surface` 只是标签 |
| `GenerationReceipt` | `action_id, kind, run_ref, artifact_refs[], outcome, readback_ref, event_cursor, binding_ref, retry_used, approval_ref, capability_id` |

**等价准则四条**（同时满足才算同一个作用，与协议/产品无关）：同一 Intent、同一 Receipt 形状、同一 IdempotentGrant/cost/redaction、可被同一 `reconcile` 只读恢复。不满足 → `needs_contract`。

**换 binding 不增加权限**：成本、授权、幂等、回读、脱敏在 Capability 层。

## 三类 kind 速查

| kind | 真实入口 | receipt 锚 | 特有门禁 |
| --- | --- | --- | --- |
| `image` | `eikona generate --model openai/gpt-image-2.5-sunburst --quality high --size WxH --agent`；`eikona.execute{action:generate,...}`；`POST /api/v1/generate` | `run_id` + `eikona://artifact/<handle>` + `eikona.asset_handoff.v2`（`handoff_candidate`） | 远程参考输入必须 `eikona://` URI；像素 size、禁 `--size 2k`；不重复描述已有资产服装颜色 |
| `video` | `scaena video generate`；`scaena video model list --json`；`workflow.submit_scaena_request` | `submission_ref` + Aigora execution receipt + `pending_review` | 必须有 `ShotAudioIntent`；`video_request_constraints.cjs`；`durationPolicy=fixed\|map` 绑定 `directorDurationSec`；`unknown_accept` 只 reconcile |
| `audio` | `sonora` CLI：`audio` / `episode-audio` / `audition` / `generate` / `handoff` / `candidates` / `cue` / `audio-readiness` | audio owner 注册项 + `audition` 审听证据 + `final_mix` ref | 逐镜 `ShotAudioIntent`；`video_native` 缺 rights/sync/voice/review 必须降级补配或 `replace_after_generation`；Sonora 默认不是逐句对白第一生产者 |

## 审批窗口

```text
ApprovalWindow
  capability_kinds[] / intent_digest / binding_allowlist
  count / cost_ceiling / retry_budget = 2
  stop_before_final_submit = true
  originality_decision_ref / granted_by / granted_at / raw_authorization_ref
```

- **一次审批 = 一个自动化窗口**：窗口内全自动（自动发现、自动选 binding、自动重试、连续推进），不逐动作弹窗。
- 免审批只读：`probe` / `discover` / `tools/list` / `resources/read` / `status` / `reconcile`。
- 必须审批：三类付费生成、绑定/替换/回滚、`select`/`freeze`、导出/发布、凭据/连接变更、正片提交、新增 kind 或超预算。
- 越界（`intent_digest` 漂移 / 新 kind / 超预算 / 新增动作 / 正片提交）或重试耗尽 → `needs_decision`。
- 一张窗口可覆盖三类，但**付费生成仍按动作留独立凭证**；「继续」/ 进度询问不重置也不扩大授权。

## 有界重试（`retry_budget = 2`）

| | 规则 |
| --- | --- |
| 可重试 | 瞬时网络 / 5xx / 429 / 超时且 `mutationAttempted=false`；`binding=unavailable` 换另一个 executable binding；能力发现漂移 |
| 禁止重试 | UNKNOWN 写、`ACCEPTED`/付费已受理、业务/权限/语义拒绝、创意输入变化、模型/正文/时长/渠道变化 |
| 每次不变 | 同一 `action_id` + `idempotency_key` + `intent_digest` + `approval_ref`；换 binding 记理由；不新建 state、不改预算 |
| 耗尽 | `needs_decision` 交回人，保留全部尝试证据 |
| 重试 ≠ 重投 | `reconcile` 只读查原 `action_id`，不消耗预算、不产生第二次 provider submit |

`retry_used` 写入 receipt；只读 `reconcile` / `discover` 不消耗预算；预算可由 `ApprovalWindow` 覆盖。

## 与 C1 的关系

`yeisme.owner_action.v1` 是跨 owner 动作收据，本轮增加了 `capability_id` / `kind` / `binding_ref` / `retry_used` / `approval_ref` 五个字段。`GenerationReceipt` 是 `GenerationCapability.invoke()` 的输出，作为 `action_id` 的 `readback_ref` / `data` 被 C1 消费；两者共用同一 `Outcome` 词汇与 `event_cursor`，不建第二真源。

## 禁止

- 不把 `cli/mcp` 或产品名做成流程分支或必答问题；
- 不把 `planned/readonly/unavailable` 升级为可写，不虚构上传动作；
- 不把客户端绝对路径当远程可读文件；不把 `eikona accepted` 写成 `production_ready`；
- 不自动付费、不自动发布、不派生子代理、不跑 race；UNKNOWN 不重投。
