# GenerationBinding 参考（CLI / MCP / HTTP / SDK）

> **状态：已降级为参考，不再是流程门禁。** 流程只认 `GenerationCapability<kind>`（`image|video|audio`）；CLI / MCP / HTTP / SDK / 本地 / 第三方都是它的 `GenerationBinding`。resolver 按 `discover()` 自动选 `executable` binding，选择理由写入 `receipt.binding_ref`，**不询问 `cli|mcp|both`**。
>
> 凡 agent 发起的非只读动作仍要审批，但改为一次 `ApprovalWindow`（`capability_kinds[]` / `intent_digest` / `binding_allowlist` / `count` / `cost_ceiling` / `retry_budget=2`）覆盖窗口内全自动；窗口内允许自动重试最多 2 次、自动换 binding。越界或耗尽交 `needs_decision`。完整设计见聚合仓 `docs/drama-execution-kernel/capability-abstraction.md`。

## binding 候选

| binding | `surface` | 何时被选中 |
| --- | --- | --- |
| Eikona CLI | `cli` | 脚本 / CI / 批量 / 需要完整命令族与可审计命令链 |
| Eikona MCP | `mcp` | 长驻 Agent、本机未装产品 CLI、只需 `eikona.search` + `eikona.execute` allowlisted |
| Eikona HTTP `/api/v1` / SDK | `http` / `sdk` | 服务化调用、OpenAI-compatible Images API 同步兼容 |
| Scaena / Aigora / Sonora owner service | `owner_service` | video / audio 生成与生产写入 |
| 本地 `codex:imagegen` | `local` | 同机临时图片 |
| 第三方产品 | `third_party` | 验过四条等价准则后才纳管，默认 `needs_contract` |

`planned / readonly / unavailable` 一律 fail-closed；`DeniedActionError` 对未知与无权限返回相同，停止重估而非枚举探测。

## 各 binding 的真实命令

### CLI 路径

```bash
eikona setup --agent
eikona setup --yes --runtimes agents,codex
scaena setup auto 2>/dev/null || scaena skills install --runtimes auto --yes --agent
eikona remote connect --endpoint <EIKONA_ENDPOINT> --key-file <KEY_FILE_EIKONA> --allow-private-http --project <PROJECT>
scaena remote connect --endpoint <SCAENA_ENDPOINT> --key-file <KEY_FILE_SCAENA> --allow-private-http --project <PROJECT>
eikona remote doctor --agent
scaena remote doctor --json
```

profile：`~/.eikona/remote-profile.json`（`eikona.remote_profile.v1`）、`~/.scaena/remote-profile.json`（`scaena.remote_profile.v1`），mode 0600，只存 endpoint / key-file 绝对路径 / 明文 LAN 许可 / project。

### MCP 路径

```bash
eikona mcp doctor --endpoint <EIKONA_ENDPOINT> --key-file <KEY_FILE_EIKONA> --json
eikona mcp capabilities --endpoint <EIKONA_ENDPOINT> --key-file <KEY_FILE_EIKONA> --json
eikona mcp --transport stdio --endpoint <EIKONA_ENDPOINT> --key-file <KEY_FILE_EIKONA>
scaena mcp serve --stdio --endpoint <SCAENA_ENDPOINT> --key-file <KEY_FILE_SCAENA>
scaena mcp inventory --local-project ./demo --json
scaena mcp doctor --json
```

工具面（以 `tools/list` / `inputSchema` 实际返回为准，不猜名字、不复数化、不枚举未声明 action）：

- Eikona：`eikona.search`（只读卡片）、`eikona.execute`（一次一个 allowlisted `action` + `args`）；`actions.describe` 查精确参数、`models.list` 查实时路由与 `start_here`；`assets.handoff` 返回 `eikona.asset_handoff.v2`；`workflow.submit_scaena_request` 提交 Scaena visual request。
- Scaena：`scaena mcp serve --stdio` 由官方 Go SDK 驱动，`tools/list` 只暴露 live backing 返回的 **executable descriptors**；planned / readonly / unavailable 不进可执行列表，也不假装可调用。
- 资源：`eikona://artifact/<handle>`、`eikona://asset/<id>`、`eikona://lineage/runs/<run_id>/artifacts/<artifact_id>`、`scaena://input/capabilities`。

MCP 输入文件（**与 CLI 的关键差异**）：

- 远程 MCP 的参考图 / 遮罩 / 输入必须是 owner 服务端可解析的 `eikona://artifact/...` 或 `eikona://asset/...`；客户端绝对路径（`/var/folders/...`、`/Users/...`、Windows 盘符、UNC）在 provider 调用前拒绝 `invalid_reference`。
- 客户端文件先走 `asset.upload.begin` → client PUT → `asset.upload.complete`，得到 `eikona://asset/<id>` 再引用。
- 同机 CLI 的 `eikona edit --input ./local.png` 本地路径仍然合法，不要把这个规则套到本机 CLI 上。
- 区分 **MCP 控制面**（tools/list / resources/read）、**客户端文件访问**、**HTTP 数据传输**；不把客户端路径当远端可读文件，不虚构上传动作，不把 planned/readonly 升级为可写。

已知缺口：`--transport http` 目前只投影监听地址（`--allow-remote` 只是确认非 loopback 投影，不是 TLS / production-ready 证据）；Scaena Streamable HTTP 为 `blocked`；`scaena remote` 生产写在 remote profile 下返回 `REMOTE_PROFILE_UNSUPPORTED_COMMAND`。这些一律如实报告为 `needs_contract`，不绕过。

## 差异对照

| 维度 | `cli` | `mcp` |
| --- | --- | --- |
| 本机是否需要产品 CLI | 需要（从 `yeisme-dist` 安装） | **不需要**；MCP 客户端从 tools/list / inputSchema / 资源取得动作与恢复合同 |
| 发现方式 | `setup --agent` / `doctor --agent` / CLI help | `tools/list` / `inputSchema` / `resources/read`；CLI help/doctor/capabilities 只是已安装客户端的可选路径 |
| 连接配置 | `remote connect` secret-free profile sidecar | `--endpoint` + `--key-file` 传给 stdio 进程 / MCP host 配置 |
| 凭据 | 0600 key-file；profile 不含 secret | 同一 0600 key-file；key 内容按请求读取，不进 logs / errors / evidence |
| 参考输入 | 同机本地路径合法 | 必须 `eikona://` URI 或已批准同机输入 |
| 动作面 | 完整 CLI 命令族（`generate` / `asset draw` / `workflow` / `export`…） | `eikona.search` + `eikona.execute` allowlisted action；planned 不进 tools/list |
| 输出 | `ai-native-cli-output-contract` envelope（`--json` / `--agent` / `--events`） | MCP `structuredContent` / resource；**不建第二份真源**，不 shell out 到 CLI |
| 失败投影 | `failed` / `unknown_accept` + `reconcile` | worker 已 claim 且失败必须投影 `failed`，不得继续 `queued`；`wait` 是有界观察 |
| 典型缺口 | `REMOTE_PROFILE_UNSUPPORTED_COMMAND` | Streamable HTTP blocked、planned inventory 不可调用 |
| 适合 | 脚本、CI、批量、可审计命令链、控制中心 CLI 回读 | 长驻 Agent、无 CLI 的远程客户端、控制中心只读发现面 |

### 多 binding 并存

1. owner 侧服务与 `doctor` 验证由 CLI / HTTP binding 完成（服务与凭据只在 owner 侧）。
2. MCP stdio 给长驻 Agent 用；MCP 不 shell out 到 CLI、不读 CLI 私有持久化、不复制 provider payload。
3. **同一个 `action_id` 只在一个 binding 上执行**；resolver 选择理由写入 `receipt.binding_ref`，换 binding 重试仍保持同一 `action_id` / `idempotency_key` / `intent_digest`，不以「两边都成功」当成两次完成。
4. 不因为装了 CLI 就把 MCP 客户端当成已安装 CLI 的宿主。

## 不变式（所有 binding 都成立）

- key 只给 0600 绝对路径，agent 不读取 / 打印 / 复制内容；
- 不自动付费、不自动发布、不自动派生子代理、不跑 race；
- 不解析人类输出；CLI 用 `--json`/`--agent`/`--events`，MCP 用结构化 `structuredContent`；
- UNKNOWN 只读 `reconcile` 原 `action_id`，不换幂等键、不重投；
- `ACCEPTED ≠ COMPLETED ≠ BOUND ≠ REVIEWED`；停在正片提交前；
- 不把私网明文 / operator-managed HTTP 描述为 production-ready。
