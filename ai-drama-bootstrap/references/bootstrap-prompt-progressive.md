# 渐进式提示词（分层、每层可停）

> 适用场景：不想一次性装完全套；或新机器上要先看清环境再逐层放行；或需要把「安装授权」和「连接授权」分开。每层**独立可发送、独立可停止**，上一层产物是下一层唯一输入，不重复探测、不重复安装。

## 设计原则

- 与 `ai-drama-router/references/skill-resolution-policy.md` 的四态一致：`active` 跳过、`resolved_local_on_demand` 本会话加载（不改持久化配置）、`needs_profile_promotion` 需用户明确授权才持久化、`needs_install_decision` 外部安装独立授权。
- 每层只允许该层声明的写；不因为下一层「可能要用」提前扩大到 workspace / global。
- **不批量激活整套 skills**；Router 仍是唯一语义入口，每层完成后给紧凑 receipt + 精确下一层触发条件。
- **不询问 `cli|mcp|both`**：流程只认 `GenerationCapability<kind>`（`image|video|audio`），binding 由 resolver 自动选。
- 所有安全不变式与完整版相同（审批窗口、凭据只给 0600 路径、`retry_budget=2`、不自动付费、不派生子代理、UNKNOWN 只读 reconcile、停在正片提交前）。

## 层与触发条件

| 层 | 名称 | 允许写 | 可停在此处 | 进入下一层的条件 |
| --- | --- | --- | --- | --- |
| L0 | `discover` 能力发现 | 无 | ✅ | 用户确认继续 |
| L0.5 | `approval` **一次审批窗口** | 无（需明确授权） | ✅ | 用户给出 `ApprovalWindow` |
| L1 | `skills_only` 装 skills | skills 安装 | ✅ | 用户授权准备 binding |
| L2 | `tools` 装 owner CLI | CLI 二进制 | ✅ | 需要 CLI 类 binding 且用户授权 |
| L3 | `connect` 配置候选连接 | profile / MCP 配置 | ✅ | 用户提供 endpoint + key-file 路径 |
| L4 | `handoff` 交 Router | 无（只读交接） | ✅ | 用户提供 `STORY_PATH` |

MCP-only 客户端可跳过 L2；`ApprovalWindow.binding_allowlist` 决定 L2/L3 准备哪些候选 binding，**不是流程分支**。

---

## L0 · 能力发现（复制这段即可只看环境）

```text
用 $ai-drama-bootstrap 只执行 L0 discover，不做任何安装、连接或写入。
只读运行：command -v node/npx/python3/curl/eikona/scaena/scaena-api/auctra/sonora；
eikona --version；scaena --version；eikona setup --agent；scaena doctor --agent；
curl -fsSL https://raw.githubusercontent.com/yeisme/yeisme-dist/main/catalog.json；eikona mcp capabilities --json。
输出 probe 报告：三类 GenerationCapability<kind>（image/video/audio）各自有哪些 executable binding、
declared_operations、ref_mode；缺哪些 CLI、哪些 skills 已 active、catalog 的 latest tag、本机是 owner 侧还是客户端侧。
planned/readonly/unavailable 标 fail-closed，不猜测、不继续依赖它。报告后停下，等我确认。
```

## L0.5 · 一次审批窗口（**不可跳过**）

```text
在继续任何安装之前，向我取得一次明确授权，生成 ApprovalWindow：
  capability_kinds[]       = image | video | audio 白名单
  intent_digest / scope_digest
  binding_allowlist        = 允许自动切换的 executable binding
  count / cost_ceiling
  retry_budget             = 2
  stop_before_final_submit = true
  originality_decision_ref / granted_by / granted_at / raw_authorization_ref
窗口内全自动：自动发现 binding、自动选可执行入口、可重试错误自动重试最多 2 次、连续推进、进度询问不暂停。
免审批只读：probe/discover/tools/list/resources/read/status/reconcile。
必须审批：三类付费生成、绑定/替换/回滚、select/freeze、导出/发布、凭据/连接变更、正片提交、新增 kind 或超预算。
越界或重试耗尽 → needs_decision 交回我。一张窗口可覆盖三类，但付费生成仍按动作留独立凭证。
不要问我 cli/mcp/both；resolver 自动选 binding，理由写 receipt.binding_ref。
把窗口记为 BootstrapReceipt.approval_ref，一次只覆盖本次 bootstrap。
```

## L1 · 只装 skills（已有工具时最常用）

```text
用 $ai-drama-bootstrap 只执行 L1，输入 L0 的 discover 报告与 ApprovalWindow。
npx --yes skills add 从 ai-drama-skills 装 ai-drama-router / ai-drama-bootstrap / ai-drama-action-receipt /
ai-drama-remote-operations，从 scaena-skills 装 scaena-asset-draw-batch / scaena-bounded-replacement。
本机已有 CLI 时：eikona setup --agent 预览后 --yes --runtimes agents,codex；scaena setup auto 或
scaena skills install --runtimes auto --yes --agent；scaena skills doctor --agent。
仅 MCP 的客户端只装云端 skills，不调用 eikona setup / scaena setup。
不安装 CLI 二进制、不做 remote connect、不写 profile。skills 已 active 的跳过。
报告 installed|skipped|failed + 版本，停下等我授权下一层。
```

## L2 · 准备 CLI 类 binding

```text
用 $ai-drama-bootstrap 只执行 L2，基于 L0 的 catalog latest 版本，只装本机缺失的 eikona/scaena/auctra：
python3 解析 https://raw.githubusercontent.com/yeisme/yeisme-dist/main/catalog.json 的 products[].latest；
env -u GH_TOKEN -u GITHUB_TOKEN curl -fsSL https://raw.githubusercontent.com/yeisme/yeisme-dist/main/install.sh | bash -s -- <product> <version>
安装后用 --version 核对；不猜版本、不用私有 releases/download URL；已装且可用的跳过。
binding_allowlist 里没有 CLI 类 binding 时本层整体跳过。报告后停下。
```

## L3 · 配置候选连接

```text
用 $ai-drama-bootstrap 只执行 L3，为 binding_allowlist 里的候选配连接，凭据只给 0600 绝对路径、绝不读取内容：
cli / http / sdk binding：
  eikona remote connect --endpoint <EIKONA_ENDPOINT> --key-file <KEY_FILE_EIKONA> --allow-private-http --project <PROJECT>
  scaena remote connect --endpoint <SCAENA_ENDPOINT> --key-file <KEY_FILE_SCAENA> --allow-private-http --project <PROJECT>
  eikona remote doctor --agent；scaena remote doctor --json；eikona remote describe --agent
mcp binding：
  eikona mcp doctor --endpoint <EIKONA_ENDPOINT> --key-file <KEY_FILE_EIKONA> --json
  eikona mcp capabilities --endpoint <EIKONA_ENDPOINT> --key-file <KEY_FILE_EIKONA> --json
  eikona mcp --transport stdio --endpoint <EIKONA_ENDPOINT> --key-file <KEY_FILE_EIKONA>
  scaena mcp serve --stdio --endpoint <SCAENA_ENDPOINT> --key-file <KEY_FILE_SCAENA>
  scaena mcp doctor --json
  然后只从 tools/list / inputSchema / resources/read 读动作参数，不猜名字、不把 planned 当可调用。
同一个 action_id 只在一个 binding 上执行；换 binding 重试保持同一 idempotency_key / intent_digest。
远程参考输入必须是 eikona://artifact/... 或 eikona://asset/...，客户端绝对路径一律拒绝。
私网明文 HTTP 的 readiness 保持 degraded|blocked。报告 doctor 结果与阻塞项后停下。
```

## L4 · 交回 Router 开始做剧

```text
用 $ai-drama-bootstrap 只执行 L4：把 STORY_PATH={{...}} 交给唯一语义入口 ai-drama-router，不要自己写剧本/分镜/提示词。
带 automation_profile：mode=continuous、stop_before_final_submit=true、continuous_advance=true、
visual_review_default=text_first、subagents=disabled_unless_explicit、unknown_policy=reconcile_readonly、
retry_budget=2、approval_window_ref、binding_policy=auto_executable。
按六阶段推进：原文与跨集接续 → 资产/音源缺口 → 导演组件与提示词组装 → raw-first 语义与导演验收 →
写前预检/写入/回读 → 逐集与全范围完成核对。每阶段只在上游 ref+digest 齐全时进入下一段；
已完成阶段不重做；进度询问不暂停。
三类生成统一走 GenerationCapability<kind>.invoke()（image=Eikona，video=Scaena/Aigora，audio=Sonora），
resolver 自动选 executable binding。
可重试错误自动重试最多 2 次，每次同一 action_id + idempotency_key + intent_digest + approval_ref；
UNKNOWN 只 reconcile 原 action_id 且不消耗预算；已 ACCEPTED / 业务拒绝 / 创意变化禁止重试；耗尽交 needs_decision。
抽卡走 scaena-asset-draw-batch，替换走 scaena-bounded-replacement，收据走 ai-drama-action-receipt，
远程链路走 ai-drama-remote-operations。生成/选图/绑定/备案/复核/整体完成分开报告，停在正片提交前。
最后给紧凑 receipt（含 approval_ref / binding_ref / retry_used）+ 精确下一条命令 + 预期副作用 + 停止条件 + 阻塞项。
```

---

## 四态映射（渐进解析，不越级）

| 观测 | 本层动作 | 需要用户授权 |
| --- | --- | --- |
| skill 已 `active` | 跳过，记录 source ref / version / digest | 否 |
| 本地 catalog 可解析且允许 `load_once` | `resolved_local_on_demand`：本会话加载，不改持久化配置 | 否 |
| 同项目高频复用 / owner 启动必须知道 | `needs_profile_promotion`：先 `preview`，再 `apply` | **是**（明确授权持久化） |
| 本地与可信 catalog 都无匹配 | `needs_install_decision`：输出缺失能力 / 固定版本 / 权限假设 / canary scope | **是**（外部安装独立授权） |

L0.5 的 `ApprovalWindow` 是 **L1 之前独立的一道授权**，不与安装授权合并；窗口内全自动（含自动重试、自动选 binding），越界重新审批；一次窗口只覆盖本次 bootstrap，不自动延续到下一会话。

## 合并发送

也可以一次发多层，但仍要保留 L0.5：

```text
用 $ai-drama-bootstrap 按渐进式执行 L0→L0.5→L1→L2→L3，每层给紧凑 receipt；
在 L0.5 停下来取一次 ApprovalWindow（不问 cli/mcp），收到授权后再继续；L3 之后停在 handoff 前，等我给 STORY_PATH。
```
