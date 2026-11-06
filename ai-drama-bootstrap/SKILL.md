---
name: ai-drama-bootstrap
description: Use when bootstrapping a new machine or session for AI drama production: install the drama skills and owner CLIs, configure remote connections to Eikona/Scaena HTTP services, verify readiness, then hand off to ai-drama-router with a screenplay or novel. Use for 一键做剧、安装 skills、remote connect、网关配置、添加剧本直接开做; do not author content, generate media, hold credentials, or compete with ai-drama-router as the semantic entry point.
---

# 做剧环境引导（Bootstrap）

本 Skill 是 `ai-drama-router` **之前**的一次性环境准备层：把一台新机器/新会话变成「可以接一份剧本或小说直接开做」的状态，然后立即把控制权交回 Router。它不创作、不生成、不做语义路由，也不持有任何凭据。

用户粘贴 [bootstrap-prompt.md](references/bootstrap-prompt.md) 的提示词，即视为**对本次安装与连接动作的明确授权**；但凭据仍必须由人类通过私密渠道单独提供，agent 只读 key-file 路径。

## 五个阶段

| # | 阶段 | 性质 | 交接 |
| --- | --- | --- | --- |
| 0 | `probe` 环境探测 | 只读，`--agent` / `--json` | 缺什么、已有什么、owner 侧还是客户端侧、是否已有 MCP host 配置 |
| 0.5 | `surface` **方式确认** | 无写，**必须询问** | 用户明确 `cli` / `mcp` / `both`，记入 `BootstrapReceipt.surface` |
| 1 | `install_tools` 安装 owner CLI | 写（用户已授权），`mcp` 跳过 | 从 `catalog.json` 取实时版本，不硬编码 |
| 2 | `install_skills` 安装做剧 skills | 写（用户已授权） | 6 个独立仓入口；`cli\|both` 另加 owner CLI 的 skills lock |
| 3 | `connect` 配置连接 | 写（secret-free profile / MCP stdio 配置） | 按 `surface` 分支 + `doctor` 验证 |
| 4 | `handoff` 交回 Router | 只读交接 | 剧本/小说路径 + `automation_profile` |

顺序以 [bootstrap-prompt.md](references/bootstrap-prompt.md) 为准：先有 CLI，才能用 `eikona setup` / `scaena setup` 装各自精确版本的 skills lock；`surface=mcp` 时跳过阶段 1 与 owner CLI 的 setup。

## 接入方式门禁（硬约束）

阶段 0 之后、任何安装或连接之前，**必须向用户明确询问一次** `SURFACE`：

- `cli`：安装 owner CLI，用 `remote connect` + `--json` / `--agent` 命令流；
- `mcp`：只配 MCP stdio 服务，由 MCP host 通过 `tools/list` + `inputSchema` + 资源调用，**客户端不需要产品 CLI**；
- `both`：先装 CLI 供 owner 侧服务与 doctor，再配 MCP 给长驻 Agent，同一 `action_id` 只在一侧执行。

不允许根据「检测到 CLI / MCP host」自动推断；`随便` / `你决定` / `用默认` / `推荐即可` 不算明确选择，须列出候选再问一次。完整命令、差异表与不变式见 [references/surface-choice.md](references/surface-choice.md)。

## 真实命令入口

完整命令与占位符见 [references/install-and-connect.md](references/install-and-connect.md)。按 `SURFACE` 分支，核心几条：

```bash
# 共同：云端 skills
npx --yes skills add https://github.com/yeisme/ai-drama-skills --skill ai-drama-router --yes

# surface=cli|both
eikona setup --agent
eikona setup --yes --runtimes agents,codex
scaena doctor --agent
eikona remote connect --endpoint <origin> --key-file <abs 0600 key> --allow-private-http --project <id>
scaena remote connect --endpoint <origin> --key-file <abs 0600 key> --allow-private-http --project <id>
eikona remote doctor --agent
scaena remote doctor --json

# surface=mcp（不需要产品 CLI）
eikona mcp doctor --endpoint <origin> --key-file <abs 0600 key> --json
eikona mcp capabilities --endpoint <origin> --key-file <abs 0600 key> --json
eikona mcp --transport stdio --endpoint <origin> --key-file <abs 0600 key>
scaena mcp serve --stdio --endpoint <origin> --key-file <abs 0600 key>
scaena mcp doctor --json
```

工具安装从公开镜像取**实时版本**，不写死 tag：

```bash
curl -fsSL https://raw.githubusercontent.com/yeisme/yeisme-dist/main/catalog.json
env -u GH_TOKEN -u GITHUB_TOKEN curl -fsSL https://raw.githubusercontent.com/yeisme/yeisme-dist/main/install.sh | bash -s -- <product> <version>
```

## 输入 / 输出

- 输入（由人类在提示词里填或交互补一次）：`SURFACE`（**必须明确询问**）、`MODE`、`EIKONA_ENDPOINT`、`SCAENA_ENDPOINT`、`KEY_FILE`（绝对路径，mode 0600）、`PROJECT`、`STORY_PATH`（剧本/小说文件）、`RUNTIMES`。
- 输出：一份紧凑的 `BootstrapReceipt`（`probe` / `surface` / `install` / `connect` / `handoff` 五段状态 + Router 的下一动作），**不含凭据值**。

## 边界（必须遵守）

- **不与 Router 竞争入口**：`ai-drama-router` 仍是唯一语义入口；本 Skill 在阶段 4 之后不再做任何路由判断。
- **必须询问 `SURFACE`**：阶段 0.5 是独立授权，不与安装授权合并；不自动推断、不接受模糊表达、不静默切换。
- **不发明命令**：遵守 `skill-resolution-policy.md`，只使用已发布 CLI 的真实命令面；宿主未声明的能力返回 `needs_contract`，不猜测路径或包名。
- **不持有凭据**：不读取、不打印、不复制 key-file 内容；不把 secret 写进仓库、日志、stdout、stderr、evidence 或提示词正文；不创建 shell 凭据脚本。profile sidecar 只存 endpoint / key-file 绝对路径 / 明文 LAN 许可 / project。
- **不自动付费**：`eikona setup` 不 probe provider、不生成；准备任务停在正片提交前（`stop_before_final_submit: true`）。
- **不派生子代理、不跑 race 检测**（root 硬限制）。
- **不解析人类输出**：一律 `--json` / `--agent` / `--events`。
- **不用 `--no-remote` 绕过 owner**：远程 profile 激活时生产写返回 `REMOTE_PROFILE_UNSUPPORTED_COMMAND`，如实报告为 typed action 缺口。

## 自动化核心流程

环境就绪后，Router 按 [DEK automation-core](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/automation-core.md) 的 `automation_profile` 与六阶段 stage_plan 连续推进：已授权阶段不重复索要授权、进度询问不暂停、UNKNOWN 只读 reconcile、逐集与全范围完成核对、停在正片提交前。

## 按需引用

| 文件 | 用途 |
| --- | --- |
| [prompt-variants.md](references/prompt-variants.md) | **三版对照与选择指南**（先读这个选版本） |
| [bootstrap-prompt.md](references/bootstrap-prompt.md) | 完整版：逐条命令 + 全部门禁 |
| [bootstrap-prompt-short.md](references/bootstrap-prompt-short.md) | 简短版：~20 行，委托给 Skill |
| [bootstrap-prompt-progressive.md](references/bootstrap-prompt-progressive.md) | 渐进式：L0 / L0.5 / L1 / L2 / L3 / L4，每层可独立发送、可停 |
| [surface-choice.md](references/surface-choice.md) | CLI / MCP / both 方式门禁、命令差异、不变式 |
| [install-and-connect.md](references/install-and-connect.md) | 安装与连接命令全表、占位符、已知缺口 |
