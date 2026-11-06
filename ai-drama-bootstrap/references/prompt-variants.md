# 提示词版本对照与选择指南

`ai-drama-bootstrap` 提供**三种形态**的引导提示词。三者共用同一套安全不变式与同一份命令真源，差别只在「展开程度」和「是否分层停止」。

| 版本 | 文件 | 长度 | 展开程度 | 每层可停 | 方式询问 |
| --- | --- | --- | --- | --- | --- |
| **完整版** | [bootstrap-prompt.md](bootstrap-prompt.md) | 最长 | 逐条命令 + 全部门禁 | 否（一次跑完） | 独立阶段 0.5 |
| **简短版** | [bootstrap-prompt-short.md](bootstrap-prompt-short.md) | ~20 行 | 委托给 Skill | 否 | 压缩成一步 0.5 |
| **渐进式** | [bootstrap-prompt-progressive.md](bootstrap-prompt-progressive.md) | 分层 | 每层一段可独立发送 | **是** | 独立层 L0.5 |
| 极简一句 | 简短版文件末尾 | 1 行 | 指向完整版 | 否 | 一句带出 |

## 选择指南

| 场景 | 推荐 |
| --- | --- |
| 全新机器、要审计每一步命令、需要留下可复核的安装链 | 完整版 |
| 本机工具已大体装好，只想快速接一份剧本开做 | 简短版 |
| 要把「安装授权」和「连接授权」分开、先看环境再逐层放行 | 渐进式 |
| 长驻 Agent / MCP host、本机不装产品 CLI | 完整版或渐进式，`SURFACE=mcp` |
| 批处理 / CI、要 `--json` 命令链 | 完整版，`SURFACE=cli` |
| 只想确认环境、不做任何写入 | 渐进式 **L0 单独发送** |
| 只想装 skills、不装二进制、不连服务 | 渐进式 **L1 单独发送** |

## 三版共有的硬门禁

1. **`SURFACE` 必须明确询问一次**（`cli` / `mcp` / `both`），不允许自动推断；`随便`、`你决定`、`用默认`、`推荐即可` 不算选择。详见 [surface-choice.md](surface-choice.md)。
2. 凭据只给 mode-0600 绝对路径，agent 不读取 / 打印 / 复制内容，不写进日志、stdout、仓库、evidence 或提示词。
3. 不自动付费生成、不自动发布、不自动派生子代理、不跑 race 检测。
4. 不解析人类输出：CLI 用 `--json` / `--agent` / `--events`，MCP 用 `structuredContent` / `tools/list` / `resources/read`。
5. UNKNOWN 只读 `reconcile` 原 `action_id`，不换幂等键、不重投。
6. `ACCEPTED ≠ COMPLETED ≠ BOUND ≠ REVIEWED ≠ 整体完成`；停在正片提交前。
7. 不把 `eikona accepted` 写成 `production_ready`；`permission` 保持 `handoff_candidate`。
8. 不把客户端绝对路径当远程 MCP 参考输入；私网明文 HTTP 的 readiness 保持 `degraded|blocked`。

## 三版共同的真源

| 内容 | 唯一源 |
| --- | --- |
| 安装 / 连接命令全表 | [install-and-connect.md](install-and-connect.md) |
| CLI vs MCP 命令、差异、不变式 | [surface-choice.md](surface-choice.md) |
| `automation_profile` 与六阶段流程 | 聚合仓 `yeisme-agent-my-skills` → `docs/drama-execution-kernel/automation-core.md` |
| 抽象与执行单元 | 聚合仓 → `docs/drama-execution-kernel/{abstract-design,execution-units}.md` |
| 唯一语义入口 | `ai-drama-router`（`ai-drama.route-plan.v1`） |

## 组合使用

- 用**渐进式**跑完 L0–L3 后，把 L4 换成**简短版**的交接段即可，不重复探测。
- 用**简短版**发现环境比预期复杂时，让 agent 改读**完整版**，不要凭记忆补命令。
- 任何版本遇到 `unavailable` / `needs_contract` / `REMOTE_PROFILE_UNSUPPORTED_COMMAND` / `invalid_reference`，保留已完成阶段、报告具体缺口并停止，不猜测、不重发、不绕过。
