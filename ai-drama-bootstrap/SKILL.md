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
| 0 | `probe` 环境探测 | 只读，`--agent` / `--json` | 缺什么、已有什么、owner 侧还是客户端侧 |
| 1 | `install_tools` 安装 owner CLI | 写（用户已授权） | 从 `catalog.json` 取实时版本，不硬编码 |
| 2 | `install_skills` 安装做剧 skills | 写（用户已授权） | 4 个独立仓入口 + owner CLI 自带 skills lock |
| 3 | `connect` 配置连接 | 写（secret-free profile） | `remote connect` + `doctor` 验证 |
| 4 | `handoff` 交回 Router | 只读交接 | 剧本/小说路径 + `automation_profile` |

顺序以 [bootstrap-prompt.md](references/bootstrap-prompt.md) 为准：先有 CLI，才能用 `eikona setup` / `scaena setup` 装各自精确版本的 skills lock。

## 真实命令入口

完整命令与占位符见 [references/install-and-connect.md](references/install-and-connect.md)，核心几条：

```bash
npx --yes skills add https://github.com/yeisme/ai-drama-skills --skill ai-drama-router --yes
eikona setup --agent
eikona setup --yes --runtimes agents,codex
scaena doctor --agent
eikona remote connect --endpoint <origin> --key-file <abs 0600 key> --allow-private-http --project <id>
scaena remote connect --endpoint <origin> --key-file <abs 0600 key> --allow-private-http --project <id>
eikona remote doctor --agent
scaena remote doctor --json
```

工具安装从公开镜像取**实时版本**，不写死 tag：

```bash
curl -fsSL https://raw.githubusercontent.com/yeisme/yeisme-dist/main/catalog.json
env -u GH_TOKEN -u GITHUB_TOKEN curl -fsSL https://raw.githubusercontent.com/yeisme/yeisme-dist/main/install.sh | bash -s -- <product> <version>
```

## 输入 / 输出

- 输入（由人类在提示词里填或交互补一次）：`EIKONA_ENDPOINT`、`SCAENA_ENDPOINT`、`KEY_FILE`（绝对路径，mode 0600）、`PROJECT`、`STORY_PATH`（剧本/小说文件）。
- 输出：一份紧凑的 `BootstrapReceipt`（`probe` / `install` / `connect` / `handoff` 四段状态 + Router 的下一动作），**不含凭据值**。

## 边界（必须遵守）

- **不与 Router 竞争入口**：`ai-drama-router` 仍是唯一语义入口；本 Skill 在阶段 4 之后不再做任何路由判断。
- **不发明命令**：遵守 `skill-resolution-policy.md`，只使用已发布 CLI 的真实命令面；宿主未声明的能力返回 `needs_contract`，不猜测路径或包名。
- **不持有凭据**：不读取、不打印、不复制 key-file 内容；不把 secret 写进仓库、日志、stdout、stderr、evidence 或提示词正文；不创建 shell 凭据脚本。profile sidecar 只存 endpoint / key-file 绝对路径 / 明文 LAN 许可 / project。
- **不自动付费**：`eikona setup` 不 probe provider、不生成；准备任务停在正片提交前（`stop_before_final_submit: true`）。
- **不派生子代理、不跑 race 检测**（root 硬限制）。
- **不解析人类输出**：一律 `--json` / `--agent` / `--events`。
- **不用 `--no-remote` 绕过 owner**：远程 profile 激活时生产写返回 `REMOTE_PROFILE_UNSUPPORTED_COMMAND`，如实报告为 typed action 缺口。

## 自动化核心流程

环境就绪后，Router 按 [DEK automation-core](https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/automation-core.md) 的 `automation_profile` 与六阶段 stage_plan 连续推进：已授权阶段不重复索要授权、进度询问不暂停、UNKNOWN 只读 reconcile、逐集与全范围完成核对、停在正片提交前。

## 按需引用

- [bootstrap-prompt.md](references/bootstrap-prompt.md)：**可复制的主提示词**（唯一可复制源）
- [install-and-connect.md](references/install-and-connect.md)：命令与占位符全表
