# L-Transport 与 L-Projection

## 现状（逐项可查）

**Transport**

- `eikona serve --addr 127.0.0.1:18080 --api-key-file /run/eikona/serve.token` 启动 headless REST `/api/v1`；`eikona serve --config <eikona-service.yaml>` 进入 private-service posture，非 loopback 明文 HTTP 在任何副作用前返回 `TLS_REQUIRED`，`/api/v1/readiness` 报告十维独立 readiness。
- `scaena-api config init --mode gateway --config <abs> --api-key-file <abs> --project-root <abs> --public-base-url http://<lan-ip>:<port>` + `scaena-api serve --config <abs>`。
- 客户端 `eikona remote connect` / `scaena remote connect` 只保存 endpoint、key-file 绝对路径、明文 LAN 许可、project；secret 留在 mode-0600 key file。
- `agent/scaena/docs/commands/remote.md` 的 v1 slice 路由：`remote / upload / mcp / doctor / board`；其余本地生产写返回 `REMOTE_PROFILE_UNSUPPORTED_COMMAND`。主仓 `remote_dispatch.go` 的 `classifyRemoteCommand` 与此一致。

**Projection**

- 控制中心 `GET /api/control-center/v1/work-queue` 返回 `yeisme.work_queue.v1`，按 `scope/owner/object/source/revision` 去重；工作项来自任务、提醒账本、服务观测与 owner typed projection，**不写入 owner 状态**，不创建第二任务真源。
- `yeisme.creative_flow.v1` 五阶段 rail 与 `next_attention`；`yeisme.drama_episode.v1` 的 `read: deferred` / 45s 缓存 / `cache: hit|miss|refresh_limited`。
- `yeisme.control_center.launch_context.v1` 只给安全跳转，不接受任意 URL；Preview 只返回规范化输入、digest、阻断原因和所需审批，**不代表 Owner 已写入**。
- 媒体预览只缓存当前会话已通过 artifact grant 授权的 Blob / Object URL，不缓存 owner 地址 / 凭据 / 原始 payload。

**Artifact**

- root `remote-media-service-access`：candidate-period grant 可立即签发并固定 24h expiry，但必须与 accepted delivery / handoff grant 分离；client-visible capability URL 必须 absolute、revocable、支持 GET/HEAD、无需额外 header，且不写入 durable evidence。
- root `remote-mcp-media-input-contract`：远程 `edit` 的参考图必须是 owner 服务端可解析的 `eikona://artifact/<handle>` 或已批准同机输入；客户端绝对路径（如 `/var/folders/.../T/codex-clipboard-*.png`）必须在 provider 调用前拒绝。

## 目标数据流

```text
远程 CLI / MCP / 控制中心 Inspector
   │ 只提交 OwnerAction{plan_ref, plan_sha256, scope_digest, idempotency_key, confirm_receipt}
   ▼
Owner Action Gate（Eikona 一份、Scaena 一份，各自持有真源与凭据；不合并）
   ├─ 校验 scope digest + plan hash + 写前状态 + lease
   ├─ 签发一次性 capability（进程内，不可从文件字段构造）
   ├─ 执行固定 EU → 权威回读 → receipt（ai-native-cli-output-contract envelope）
   └─ 发 event_cursor（revision 单调递增）
   │
   ├─► 远程 CLI resume / reconcile：只读，绝不重投
   └─► 控制中心 read projection：消费同一 action_id + revision
```

三个变化：N 次 RTT → 一次提交 + 事件流；三层各自的确认 / 缓存 → 一个 receipt；三层轮询 → 一个 event_cursor。

## 三个真实缺口

| ID | 缺口 | 性质 |
| --- | --- | --- |
| G1 | `REMOTE_PROFILE_UNSUPPORTED_COMMAND`：远程生产写没有 typed action 路由 | 待补 `scaena-api` C1 路由；**不得**放开任意本地命令，也不得用 `--no-remote` 绕过 |
| G2 | Eikona `run_id` / Scaena `submission_ref` / 控制中心 `revision` 没有同一个 `action_id` | 待补 C1 receipt 与 `action_id` 映射；控制中心已具备 revision 去重能力 |
| G3 | 替换前无 `identity_equal` 判定、跨入口无共享 `claim_key` | 待补 C3；见 `scaena-bounded-replacement` |

## 状态词汇对齐

| 统一词 | 控制中心现有词 |
| --- | --- |
| `ACCEPTED` | `pending` |
| `COMPLETED` | `complete` |
| `PARTIAL` | `partial` |
| `UNKNOWN` | `unknown` / `not_recorded` |
| `TERMINAL_REJECTED` | `forbidden` / `integrity_failed` |
| 无合同 | `needs_contract` |
| 授权过期 | `expired` |
| 暂时不可读 | `unavailable` / `stale` |

这些词**不可混用**：只读请求失败不重试生成；`not_recorded` 不是读取失败，也不代表可以重新提交生成。

## 禁止

- 不把客户端本地路径、owner 私有路径、runstore 路径写进远程响应；
- 不把 provider key、Authorization header、raw prompt、private tool arguments 写进 stdout / stderr / logs / traces / evidence；
- 不因为网络已允许就跳过 key / action gate；
- 不把私网明文或 operator-managed HTTP profile 描述为 production-ready（readiness 必须保持 `degraded|blocked` 并给出 TLS / reverse-proxy repair action）。
