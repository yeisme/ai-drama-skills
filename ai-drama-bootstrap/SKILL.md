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
| 0 | `probe` 能力发现 | 只读，`--agent` / `--json` / `tools/list` | 三类 `GenerationCapability<kind>` 各自的 `executable` binding、`declared_operations`、`ref_mode` |
| 0.5 | `approval` **一次审批** | 无写，需用户明确授权 | `ApprovalWindow`（`capability_kinds[]` / `intent_digest` / `binding_allowlist` / `count` / `cost_ceiling` / `retry_budget=2`），记入 `BootstrapReceipt.approval_ref` |
| 1 | `install_tools` 准备候选 binding | 写（窗口内授权） | 从 `catalog.json` 取实时版本安装缺失 CLI；MCP-only 绑定不装 CLI |
| 2 | `install_skills` 安装做剧 skills | 写（窗口内授权） | 6 个独立仓入口；有 CLI 时另加 owner CLI 的 skills lock |
| 3 | `connect` 配置连接 | 写（secret-free profile / MCP stdio 配置） | 为候选 binding 配好连接 + `doctor` 验证；resolver 在运行时自动选 |
| 4 | `handoff` 交回 Router | 只读交接 | 剧本/小说路径 + `automation_profile`（含 `approval_window_ref` / `retry_budget`） |

顺序以 [bootstrap-prompt.md](references/bootstrap-prompt.md) 为准：**不再询问 `cli|mcp|both`**。流程只认 `GenerationCapability<kind>`（`image|video|audio`），resolver 自动选 `executable` binding，理由写入 `receipt.binding_ref`。

## 审批窗口（硬约束）

阶段 0 之后、任何安装或连接之前，用户给**一次带边界的审批**，生成 `ApprovalWindow`；窗口内全自动：自动发现 binding、自动选可执行入口、**可重试错误自动重试最多 2 次**（同 `action_id` / `idempotency_key` / `intent_digest`）、连续推进、进度询问不暂停。

- 免审批只读：`probe` / `discover` / `tools/list` / `resources/read` / `status` / `reconcile`；
- 必须审批：三类付费生成、绑定 / 替换 / 回滚、`select` / `freeze`、导出 / 发布、凭据 / 连接变更、正片提交、新增 kind 或超预算；
- 越界（新 kind / 超预算 / `intent_digest` 漂移 / 新增动作 / 正片提交）或重试耗尽 → `needs_decision` 交回人；
- UNKNOWN 只 `reconcile` 且不消耗重试预算；已 `ACCEPTED` / 业务拒绝 / 创意输入变化禁止重试；
- 一张窗口可覆盖三类，但付费生成仍按动作留独立凭证；换 binding 不增加权限。

完整设计见聚合仓 `docs/drama-execution-kernel/capability-abstraction.md`；CLI / MCP / HTTP 命令差异见 [references/surface-choice.md](references/surface-choice.md)（**binding 参考，非流程门禁**）。

## 真实命令入口

完整命令与占位符见 [references/install-and-connect.md](references/install-and-connect.md)。以下是**候选 binding 的准备命令**，不是二选一分支；resolver 在运行时按 `discover()` 结果自动选：

```bash
# 共同：云端 skills
npx --yes skills add https://github.com/yeisme/ai-drama-skills --skill ai-drama-router --yes

# binding: cli / http / sdk
eikona setup --agent
eikona setup --yes --runtimes agents,codex
scaena doctor --agent
eikona remote connect --endpoint <origin> --key-file <abs 0600 key> --allow-private-http --project <id>
scaena remote connect --endpoint <origin> --key-file <abs 0600 key> --allow-private-http --project <id>
eikona remote doctor --agent
scaena remote doctor --json

# binding: mcp（客户端不需要产品 CLI）
eikona mcp doctor --endpoint <origin> --key-file <abs 0600 key> --json
eikona mcp capabilities --endpoint <origin> --key-file <abs 0600 key> --json
eikona mcp --transport stdio --endpoint <origin> --key-file <abs 0600 key>
scaena mcp serve --stdio --endpoint <origin> --key-file <abs 0600 key>
scaena mcp doctor --json

# 三类能力的真实调用入口（由 GenerationCapability<kind>.invoke() 统一）
eikona generate --model openai/gpt-image-2.5-sunburst --quality high --size WxH --agent   # image
scaena video generate ... --json                                                        # video
sonora audio / episode-audio / audition / generate / handoff ...                       # audio
```

工具安装从公开镜像取**实时版本**，不写死 tag：

```bash
curl -fsSL https://raw.githubusercontent.com/yeisme/yeisme-dist/main/catalog.json
env -u GH_TOKEN -u GITHUB_TOKEN curl -fsSL https://raw.githubusercontent.com/yeisme/yeisme-dist/main/install.sh | bash -s -- <product> <version>
```

## 输入 / 输出

- 输入（由人类在提示词里填或交互补一次）：`APPROVAL`（一次 `ApprovalWindow` 授权）、`MODE`、`EIKONA_ENDPOINT`、`SCAENA_ENDPOINT`、`KEY_FILE`（绝对路径，mode 0600）、`PROJECT`、`STORY_PATH`（剧本/小说文件）、`RUNTIMES`。
- 输出：一份紧凑的 `BootstrapReceipt`（`probe` / `approval` / `install` / `connect` / `handoff` 五段状态 + `binding_ref` / `retry_used` + Router 的下一动作），**不含凭据值**。

## 边界（必须遵守）

- **不与 Router 竞争入口**：`ai-drama-router` 仍是唯一语义入口；本 Skill 在阶段 4 之后不再做任何路由判断。
- **必须有 `ApprovalWindow`**：阶段 0.5 的一次审批覆盖窗口内全部自动化；不逐动作弹窗，但越界必须重新审批；不询问 `cli/mcp` 作为流程分支。
- **有界自动重试**：`retry_budget=2`，只对瞬时网络 / 5xx / 429 / `mutationAttempted=false` 超时 / `binding=unavailable` 重试；UNKNOWN 只 `reconcile`、已受理 / 业务拒绝 / 创意变化禁止重试；耗尽交 `needs_decision`。
- **不发明命令**：遵守 `skill-resolution-policy.md`，只使用已发布 CLI 的真实命令面；宿主未声明的能力返回 `needs_contract`，不猜测路径或包名。
- **不持有凭据**：不读取、不打印、不复制 key-file 内容；不把 secret 写进仓库、日志、stdout、stderr、evidence 或提示词正文；不创建 shell 凭据脚本。profile sidecar 只存 endpoint / key-file 绝对路径 / 明文 LAN 许可 / project。
- **不自动付费**：`eikona setup` 不 probe provider、不生成；准备任务停在正片提交前（`stop_before_final_submit: true`）。
- **不派生子代理、不跑 race 检测**（root 硬限制）。
- **不解析人类输出**：一律 `--json` / `--agent` / `--events`。
- **不用 `--no-remote` 绕过 owner**：远程 profile 激活时生产写返回 `REMOTE_PROFILE_UNSUPPORTED_COMMAND`，如实报告为 typed action 缺口。

## 自动化核心流程

环境就绪后，Router 按 [DEK automation-core](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/automation-core.md) 的 `automation_profile` 与六阶段 stage_plan 连续推进：已授权阶段不重复索要授权、进度询问不暂停、可重试错误按 `retry_budget=2` 自动重试、UNKNOWN 只读 reconcile（不消耗预算）、逐集与全范围完成核对、停在正片提交前。三类能力统一走 [GenerationCapability<kind>](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/capability-abstraction.md)。

## 按需引用

| 文件 | 用途 |
| --- | --- |
| 聚合仓 `docs/drama-execution-kernel/HANDOFF.md` | **总览与交接**：版本、真源表、Skills/合同状态、后续路线 |
| [prompt-variants.md](references/prompt-variants.md) | **三版对照与选择指南**（先读这个选版本） |
| [bootstrap-prompt.md](references/bootstrap-prompt.md) | 完整版：逐条命令 + 全部门禁 |
| [bootstrap-prompt-short.md](references/bootstrap-prompt-short.md) | 简短版：~20 行，委托给 Skill |
| [bootstrap-prompt-progressive.md](references/bootstrap-prompt-progressive.md) | 渐进式：L0 能力发现 / L0.5 审批窗口 / L1 skills / L2 工具 / L3 连接 / L4 交接，每层可独立发送、可停 |
| [surface-choice.md](references/surface-choice.md) | **binding 参考**（已降级）：CLI / MCP / HTTP / SDK 命令与差异，不再是流程门禁 |
| [install-and-connect.md](references/install-and-connect.md) | 安装与连接命令全表、占位符、已知缺口 |
