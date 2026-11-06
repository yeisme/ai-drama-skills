---
name: ai-drama-remote-operations
description: Use when remote users draw assets, manage production state or replace media over owner HTTP services, MCP stdio or any GenerationBinding, when a remote profile blocks a production write, or when the control center read projection disagrees with CLI readback. Use for 远程抽卡、binding 发现、remote connect、REMOTE_PROFILE_UNSUPPORTED_COMMAND、控制中心投影对齐、artifact grant; do not build a cross-owner gateway, ask cli/mcp as a flow branch, store provider keys on clients, or write owner state locally.
---

# 做剧远程服务操作与投影对齐

本 Skill 覆盖当前实际部署形态：Eikona / Scaena / Sonora 以 owner 服务运行，远程用户通过 `remote connect`、MCP stdio 或 HTTP 接入，控制中心做只读可视化。它解决「三层各读一次」与「远程生产写入口过窄」两个问题。

**一个作用**：三类生成统一为 `GenerationCapability<kind>`（`image|video|audio`）；本 Skill 负责 `GenerationBinding` 的发现、连接准备与投影对齐，**不询问 `cli|mcp|both` 作为流程分支**，resolver 自动选 `executable` binding，理由写 `receipt.binding_ref`。审批由 `ApprovalWindow` 一次覆盖，可重试错误在 `retry_budget=2` 内自动重试；详见 `ai-drama-action-receipt/references/capability-invocation.md`。

## 真实承载

| 入口 | 现有命令 / 合同 |
| --- | --- |
| Eikona owner 服务 | `eikona serve --addr ... --api-key-file ...`（`/api/v1`）、`eikona remote connect`、`eikona remote doctor --agent` |
| Scaena owner 服务 | `scaena-api config init --mode gateway ...` / `scaena-api serve --config ...`、`scaena remote connect --endpoint ... --key-file ... --project ...`、`scaena remote doctor --json` |
| 远程 profile | `~/.scaena/remote-profile.json`（`scaena.remote_profile.v1`）、`~/.eikona/remote-profile.json`（`eikona.remote_profile.v1`），mode 0600，只存 endpoint / key-file 绝对路径 / 明文 LAN 许可 / project |
| MCP binding | `eikona mcp capabilities --json`、`eikona mcp doctor --json`、`tools/list` / `inputSchema` / `resources/read`、`scaena mcp serve --stdio`、`scaena mcp doctor --json` |
| audio / video binding | `sonora` CLI（`audio` / `episode-audio` / `audition`）、`scaena video generate`、`scaena video model list --json` |
| 控制中心投影 | `yeisme.work_queue.v1`（签名 cursor、revision 去重）、`yeisme.creative_flow.v1`、`yeisme.drama_episode.v1`、`yeisme.control_center.launch_context.v1` |
| artifact 交付 | path-free `eikona://` URI、短期 capability URL、24h candidate grant 与 accepted delivery grant 分离 |

详见 [references/transport-and-projection.md](references/transport-and-projection.md)。

## 已知缺口（必须如实报告）

`agent/scaena/docs/commands/remote.md` 明确 v1 slice 只路由 `remote / upload / mcp / doctor / board`；本地生产写（`init`、`workflow run`、storyboard/video generation、export）在 remote profile 激活时返回 `REMOTE_PROFILE_UNSUPPORTED_COMMAND`。因此：

- **不得**把 `--no-remote` 当作绕过 owner 的常规路径（会在客户端落第二份 owner state）；
- 远程抽卡 / 资产管理应通过 owner 侧 `yeisme.owner_action.v1` typed action 提交，而不是放开任意本地命令；
- 该 typed action 路由当前是待补能力，报告为 `needs_contract`，不虚构为已实现。

## 输入 / 输出

- 输入：`DramaRoutePlan` 的执行阶段、`GenerationIntent`（`FrozenRef` + typed controls）、`ApprovalWindow`、已配置的候选 binding 与连接。
- 输出：一个 `CapabilityInvocation` 提交建议 + `GenerationReceipt` 的消费方式（含 `binding_ref` / `retry_used` / `event_cursor`）；**不产生 owner 写入、不保存凭据**。

## 边界

- **不建跨 owner 凭据 / 生产网关**（root `owner-hosted-remote-profile` 已判 `reject-now`）；Eikona / Scaena / Sonora 各自执行自己的 EU。
- **不询问 `cli|mcp|both`、不把入口做成流程分支**；`planned/readonly/unavailable` fail-closed；换 binding 不增加权限、不消耗额外审批。
- 可重试错误只在 `retry_budget=2` 内自动重试；UNKNOWN 只 `reconcile` 原 `action_id` 且不消耗预算；越界或耗尽交 `needs_decision`。
- 不把 `remote profile` 里的 key-file 内容、provider key、Authorization header 写进日志 / evidence / stdout。
- 不把客户端绝对路径当远程参考输入（root `remote-mcp-media-input-contract`：使用 owner 服务端可解析的 artifact URI）。
- 不把控制中心 Preview 当 Owner 已写入；不缓存 owner 地址 / 凭据 / 原始 payload。
- 不在客户端落 `.scaena` / SQLite / manifest / receipt。

## 最小流程

1. 对候选 binding 做只读 `discover()`：`scaena remote doctor --json` / `eikona remote doctor --agent` / `eikona mcp capabilities --json` / `scaena mcp doctor --json`；只保留 `executable`。
2. 由 `ai-drama-router` 选定 EU 与 `kind`，取得 `ApprovalWindow`、`plan_ref + plan_sha256`、`scope_digest`、`idempotency_key`。
3. resolver 自动选一个 `executable` binding（理由记入 `receipt.binding_ref`），提交 `CapabilityInvocation`；owner 侧执行 EU。
4. 可重试错误按 `retry_budget=2` 自动重试（同一 `action_id` / `idempotency_key` / `intent_digest` / `approval_ref`），UNKNOWN 只 `reconcile`；越界或耗尽交 `needs_decision`。
5. 读取统一 envelope 的 `data.action_id` / `outcome` / `binding_ref` / `retry_used` / `event_cursor`，交给 `ai-drama-action-receipt` 判定。
6. 控制中心按 `action_id + revision` 去重渲染 `yeisme.work_queue.v1` / `yeisme.creative_flow.v1`；缓存由 `event_cursor` 驱动。
7. 人工门禁（select / freeze / 替换确认）如需在控制中心落，只发一条窄 receipt，不持有 domain state。

## 验证

```bash
scaena remote doctor --json
eikona remote doctor --agent
scripts/skills.sh validate-profiles
```

## 按需引用

- 能力调用合同：`ai-drama-action-receipt/references/capability-invocation.md`
- 能力抽象全文：[https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/capability-abstraction.md](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/capability-abstraction.md)
- C1 合同：[https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/contracts/owner-action.v1.md](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/contracts/owner-action.v1.md)
- 抽象与 EU：[https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/README.md](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/README.md)
