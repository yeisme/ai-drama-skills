# 渐进式提示词（分层、每层可停）

> 适用场景：不想一次性装完全套；或新机器上要先看清环境再逐层放行；或需要把「安装授权」和「连接授权」分开。每层**独立可发送、独立可停止**，上一层产物是下一层唯一输入，不重复探测、不重复安装。

## 设计原则

- 与 `ai-drama-router/references/skill-resolution-policy.md` 的四态一致：`active` 跳过、`resolved_local_on_demand` 本会话加载（不改持久化配置）、`needs_profile_promotion` 需用户明确授权才持久化、`needs_install_decision` 外部安装独立授权。
- 每层只允许该层声明的写；不因为下一层「可能要用」提前扩大到 workspace / global。
- **不批量激活整套 skills**；Router 仍是唯一语义入口，每层完成后给紧凑 receipt + 精确下一层触发条件。
- 所有安全不变式与完整版相同（凭据只给 0600 路径、不自动付费、不派生子代理、UNKNOWN 只读 reconcile、停在正片提交前）。

## 层与触发条件

| 层 | 名称 | 允许写 | 可停在此处 | 进入下一层的条件 |
| --- | --- | --- | --- | --- |
| L0 | `probe` 只读探测 | 无 | ✅ | 用户确认继续 |
| L0.5 | `surface` 方式确认 | 无（**必须询问**） | ✅ | 用户给出明确 `cli\|mcp\|both` |
| L1 | `skills_only` 装 skills | skills 安装 | ✅ | 用户授权安装 CLI 或连接 |
| L2 | `tools` 装 owner CLI | CLI 二进制 | ✅ | `surface=cli\|both` 且用户授权 |
| L3 | `connect` 配置连接 | profile / MCP 配置 | ✅ | 用户提供 endpoint + key-file 路径 |
| L4 | `handoff` 交 Router | 无（只读交接） | ✅ | 用户提供 `STORY_PATH` |

`mcp` 路径**跳过 L2**（不需要产品 CLI）；`both` 路径 L2 只装 owner 侧服务所需 CLI，MCP 客户端不装 CLI。

---

## L0 · 只读探测（复制这段即可只看环境）

```text
用 $ai-drama-bootstrap 只执行 L0 probe，不做任何安装、连接或写入。
只读运行：command -v node/npx/python3/curl/eikona/scaena/scaena-api/auctra；
eikona --version；scaena --version；eikona setup --agent；scaena doctor --agent；
curl -fsSL https://raw.githubusercontent.com/yeisme/yeisme-dist/main/catalog.json。
输出 probe 报告：缺哪些 CLI、哪些 skills 已 active、catalog 的 latest tag、本机是 owner 侧还是客户端侧、是否已存在 MCP host 配置。
失败项标 unavailable，不猜测、不继续依赖它。报告后停下，等我确认。
```

## L0.5 · 方式确认（**必须询问，不可跳过**）

```text
在继续任何安装之前，先明确问我一次：
「本机会以哪种方式接入做剧工具？cli / mcp / both」
  cli  = 安装 owner CLI，用 remote connect + --json/--agent 命令流
  mcp  = 只配 MCP stdio 服务，由 MCP host 通过 tools/list + inputSchema + 资源调用（可不装产品 CLI）
  both = 先装 CLI 供 owner 侧服务，再配 MCP 给长驻 Agent
不要根据检测到 CLI 或 MCP host 自动推断；「随便 / 你决定 / 用默认」不算明确选择，列出候选再问一次。
把我的明确选择记为 BootstrapReceipt.surface，后续不得静默切换。两条路径的命令与差异见 references/surface-choice.md。
```

## L1 · 只装 skills（已有工具时最常用）

```text
用 $ai-drama-bootstrap 只执行 L1，输入上一层的 probe 报告与 surface。
按 surface 选择安装：
- 共同：npx --yes skills add 从 ai-drama-skills 装 ai-drama-router / ai-drama-bootstrap / ai-drama-action-receipt / ai-drama-remote-operations，从 scaena-skills 装 scaena-asset-draw-batch / scaena-bounded-replacement；
- surface=cli|both 且本机已有 eikona/scaena：eikona setup --agent 预览后 --yes --runtimes agents,codex；scaena setup auto 或 scaena skills install --runtimes auto --yes --agent；scaena skills doctor --agent。
不安装 CLI 二进制、不做 remote connect、不写 profile。skills 已 active 的跳过，不重复启用。
报告 installed|skipped|failed + 版本，停下等我授权下一层。
```

## L2 · 安装 owner CLI（仅 cli / both）

```text
用 $ai-drama-bootstrap 只执行 L2，基于 L0 的 catalog latest 版本，只装本机缺失的 eikona/scaena/auctra：
python3 解析 https://raw.githubusercontent.com/yeisme/yeisme-dist/main/catalog.json 的 products[].latest；
env -u GH_TOKEN -u GITHUB_TOKEN curl -fsSL https://raw.githubusercontent.com/yeisme/yeisme-dist/main/install.sh | bash -s -- <product> <version>
安装后用 --version 核对；不猜版本、不用私有 releases/download URL；已装且可用的跳过。
surface=mcp 时本层整体跳过。报告后停下。
```

## L3 · 配置连接（按 surface 分支）

```text
用 $ai-drama-bootstrap 只执行 L3，基于 surface 分支连接，凭据只给 0600 绝对路径、绝不读取内容：
surface=cli：
  eikona remote connect --endpoint <EIKONA_ENDPOINT> --key-file <KEY_FILE_EIKONA> --allow-private-http --project <PROJECT>
  scaena remote connect --endpoint <SCAENA_ENDPOINT> --key-file <KEY_FILE_SCAENA> --allow-private-http --project <PROJECT>
  eikona remote doctor --agent；scaena remote doctor --json；eikona remote describe --agent
surface=mcp：
  eikona mcp doctor --endpoint <EIKONA_ENDPOINT> --key-file <KEY_FILE_EIKONA> --json
  eikona mcp capabilities --endpoint <EIKONA_ENDPOINT> --key-file <KEY_FILE_EIKONA> --json
  eikona mcp --transport stdio --endpoint <EIKONA_ENDPOINT> --key-file <KEY_FILE_EIKONA>
  scaena mcp serve --stdio --endpoint <SCAENA_ENDPOINT> --key-file <KEY_FILE_SCAENA>
  scaena mcp doctor --json
  然后只从 tools/list / inputSchema / resources/read 读动作参数，不猜名字、不把 planned 当可调用。
surface=both：先 cli  doctor，再 mcp 配置；同一个 action_id 只在一侧执行，不重复生成。
远程 MCP 参考输入必须是 eikona://artifact/... 或 eikona://asset/...，客户端绝对路径一律拒绝。
私网明文 HTTP 的 readiness 保持 degraded|blocked。报告 doctor 结果与阻塞项后停下。
```

## L4 · 交回 Router 开始做剧

```text
用 $ai-drama-bootstrap 只执行 L4：把 STORY_PATH={{...}} 交给唯一语义入口 ai-drama-router，不要自己写剧本/分镜/提示词。
带 automation_profile：mode=continuous、stop_before_final_submit=true、continuous_advance=true、
visual_review_default=text_first、subagents=disabled_unless_explicit、unknown_policy=reconcile_readonly。
按六阶段推进：原文与跨集接续 → 资产/音源缺口 → 导演组件与提示词组装 → raw-first 语义与导演验收 →
写前预检/写入/回读 → 逐集与全范围完成核对。每阶段只在上游 ref+digest 齐全时进入下一段；
已完成阶段不重做；进度询问不暂停；UNKNOWN 只读 reconcile 原 action_id。
抽卡走 scaena-asset-draw-batch，替换走 scaena-bounded-replacement，收据走 ai-drama-action-receipt，
远程链路走 ai-drama-remote-operations。生成/选图/绑定/备案/复核/整体完成分开报告，停在正片提交前。
最后给紧凑 receipt + 精确下一条命令 + 预期副作用 + 停止条件 + 阻塞项。
```

---

## 四态映射（渐进解析，不越级）

| 观测 | 本层动作 | 需要用户授权 |
| --- | --- | --- |
| skill 已 `active` | 跳过，记录 source ref / version / digest | 否 |
| 本地 catalog 可解析且允许 `load_once` | `resolved_local_on_demand`：本会话加载，不改持久化配置 | 否 |
| 同项目高频复用 / owner 启动必须知道 | `needs_profile_promotion`：先 `preview`，再 `apply` | **是**（明确授权持久化） |
| 本地与可信 catalog 都无匹配 | `needs_install_decision`：输出缺失能力 / 固定版本 / 权限假设 / canary scope | **是**（外部安装独立授权） |

L0.5 的 `surface` 选择是 **L1 之前独立的一道授权**，不与安装授权合并；一次选择只覆盖本次 bootstrap，不自动延续到下一会话。

## 合并发送

也可以一次发多层，但仍要保留 L0.5：

```text
用 $ai-drama-bootstrap 按渐进式执行 L0→L0.5→L1→L2→L3，每层给紧凑 receipt；
在 L0.5 停下来明确问一次 cli/mcp/both，收到我的明确选择后再继续；L3 之后停在 handoff 前，等我给 STORY_PATH。
```
