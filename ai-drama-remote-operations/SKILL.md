---
name: ai-drama-remote-operations
description: Use when remote users draw assets, manage production state or replace media over owner HTTP services plus a remote CLI, when a remote profile blocks a production write, or when the control center read projection disagrees with CLI readback. Use for 远程抽卡、remote connect、REMOTE_PROFILE_UNSUPPORTED_COMMAND、控制中心投影对齐、artifact grant; do not build a cross-owner gateway, store provider keys on clients, or write owner state locally.
---

# 做剧远程服务操作与投影对齐

本 Skill 覆盖当前实际部署形态：Eikona / Scaena 以 HTTP 服务运行，远程用户通过 `remote connect` 的 secret-free profile 连接，控制中心做只读可视化。它解决「三层各读一次」与「远程生产写入口过窄」两个问题。

## 真实承载

| 入口 | 现有命令 / 合同 |
| --- | --- |
| Eikona owner 服务 | `eikona serve --addr ... --api-key-file ...`（`/api/v1`）、`eikona remote connect`、`eikona remote doctor --agent` |
| Scaena owner 服务 | `scaena-api config init --mode gateway ...` / `scaena-api serve --config ...`、`scaena remote connect --endpoint ... --key-file ... --project ...`、`scaena remote doctor --json` |
| 远程 profile | `~/.scaena/remote-profile.json`（`scaena.remote_profile.v1`，mode 0600），只存 endpoint / key-file 绝对路径 / 明文 LAN 许可 / project |
| 控制中心投影 | `yeisme.work_queue.v1`（签名 cursor、revision 去重）、`yeisme.creative_flow.v1`、`yeisme.drama_episode.v1`、`yeisme.control_center.launch_context.v1` |
| artifact 交付 | path-free `eikona://` URI、短期 capability URL、24h candidate grant 与 accepted delivery grant 分离 |

详见 [references/transport-and-projection.md](references/transport-and-projection.md)。

## 已知缺口（必须如实报告）

`agent/scaena/docs/commands/remote.md` 明确 v1 slice 只路由 `remote / upload / mcp / doctor / board`；本地生产写（`init`、`workflow run`、storyboard/video generation、export）在 remote profile 激活时返回 `REMOTE_PROFILE_UNSUPPORTED_COMMAND`。因此：

- **不得**把 `--no-remote` 当作绕过 owner 的常规路径（会在客户端落第二份 owner state）；
- 远程抽卡 / 资产管理应通过 owner 侧 `yeisme.owner_action.v1` typed action 提交，而不是放开任意本地命令；
- 该 typed action 路由当前是待补能力，报告为 `needs_contract`，不虚构为已实现。

## 输入 / 输出

- 输入：`DramaRoutePlan` 的执行阶段、上游 EU 的 `FrozenRef`、用户明确授权原文、已配置的 remote profile。
- 输出：一个 `OwnerAction` 提交建议 + 统一 receipt 的消费方式；**不产生 owner 写入、不保存凭据**。

## 边界

- **不建跨 owner 凭据 / 生产网关**（root `owner-hosted-remote-profile` 已判 `reject-now`）；Eikona 与 Scaena 各自执行自己的 EU。
- 不把 `remote profile` 里的 key-file 内容、provider key、Authorization header 写进日志 / evidence / stdout。
- 不把客户端绝对路径当远程参考输入（root `remote-mcp-media-input-contract`：使用 owner 服务端可解析的 artifact URI）。
- 不把控制中心 Preview 当 Owner 已写入；不缓存 owner 地址 / 凭据 / 原始 payload。
- 不在客户端落 `.scaena` / SQLite / manifest / receipt。

## 最小流程

1. `scaena remote doctor --json` / `eikona remote doctor --agent` 验证可达与授权。
2. 由 `ai-drama-router` 选定 EU，取得 `plan_ref + plan_sha256 + scope_digest + idempotency_key + confirm_receipt`。
3. 提交 `OwnerAction` 到对应 owner `/api/v1`；owner 侧执行 EU。
4. 读取统一 envelope 的 `data.action_id` / `outcome` / `event_cursor`，交给 `ai-drama-action-receipt` 判定。
5. 控制中心按 `action_id + revision` 去重渲染 `yeisme.work_queue.v1` / `yeisme.creative_flow.v1`；缓存由 `event_cursor` 驱动。
6. 人工门禁（select / freeze / 替换确认）如需在控制中心落，只发一条窄 receipt，不持有 domain state。

## 验证

```bash
scaena remote doctor --json
eikona remote doctor --agent
scripts/skills.sh validate-profiles
```

## 按需引用

- C1 合同：[https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/contracts/owner-action.v1.md](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/contracts/owner-action.v1.md)
- 抽象与 EU：[https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/README.md](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/README.md)
