# 接入方式选择（CLI / MCP / both）

> **硬门禁**：阶段 0 只读探测结束、任何安装或连接动作开始之前，Agent **必须向用户明确询问一次** `SURFACE`。不允许根据「检测到 CLI」「检测到 MCP host」「觉得更快」自动推断。模糊表达（`随便` / `你决定` / `用默认` / `推荐即可`）**不算明确选择**，必须列出候选并再问一次。

## 必须问的那句话

```text
本机会以哪种方式接入做剧工具？请明确选择一项：
  cli  — 安装 Eikona/Scaena/Auctra CLI，用 remote connect + --json/--agent 命令流（脚本、CI、批量、可审计命令链）
  mcp  — 只配 MCP stdio 服务，由 MCP host 通过 tools/list + inputSchema + 资源调用（长驻 Agent、本机未装产品 CLI）
  both — 先装 CLI 用于 owner 侧服务与 doctor，再配 MCP 给长驻 Agent；同一动作只执行一侧，不重复生成
```

用户给出**明确具体值**后才继续；`both` 也要明确说出。选择结果写入 `BootstrapReceipt.surface`，后续阶段不得静默切换。

## 两条路径的真实命令

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

### `both` 规则

1. 先按 `cli` 完成 owner 侧服务与 `doctor` 验证（服务与凭据只在 owner 侧）。
2. 再按 `mcp` 配 stdio 给长驻 Agent；MCP 不 shell out 到 CLI、不读 CLI 私有持久化、不复制 provider payload。
3. **同一个 `action_id` 只在一侧执行**；两侧都报告同一 `event_cursor`，不以「两边都成功」当成两次完成。
4. 不因为装了 CLI 就把 MCP 客户端当成已安装 CLI 的宿主。

## 不变式（两种方式都成立）

- key 只给 0600 绝对路径，agent 不读取 / 打印 / 复制内容；
- 不自动付费、不自动发布、不自动派生子代理、不跑 race；
- 不解析人类输出；CLI 用 `--json`/`--agent`/`--events`，MCP 用结构化 `structuredContent`；
- UNKNOWN 只读 `reconcile` 原 `action_id`，不换幂等键、不重投；
- `ACCEPTED ≠ COMPLETED ≠ BOUND ≠ REVIEWED`；停在正片提交前；
- 不把私网明文 / operator-managed HTTP 描述为 production-ready。
