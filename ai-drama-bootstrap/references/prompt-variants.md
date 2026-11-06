# 提示词版本对照与选择指南

`ai-drama-bootstrap` 提供**三种形态**的引导提示词。三者共用同一套安全不变式与同一份命令真源，差别只在「展开程度」和「是否分层停止」。

| 版本 | 文件 | 长度 | 展开程度 | 每层可停 | 审批窗口 |
| --- | --- | --- | --- | --- | --- |
| **完整版** | [bootstrap-prompt.md](bootstrap-prompt.md) | 最长 | 逐条命令 + 全部门禁 | 否（一次跑完） | 独立阶段 0.5 完整展开 |
| **简短版** | [bootstrap-prompt-short.md](bootstrap-prompt-short.md) | ~20 行 | 委托给 Skill | 否 | 一步带出 |
| **渐进式** | [bootstrap-prompt-progressive.md](bootstrap-prompt-progressive.md) | 分层 | 每层一段可独立发送 | **是** | 独立层 L0.5 |
| 极简一句 | 简短版文件末尾 | 1 行 | 指向完整版 | 否 | 一句带出 |

三版都**不询问 `cli|mcp|both`**；入口差异由 resolver 自动选择 `executable` binding。

## 选择指南

| 场景 | 推荐 |
| --- | --- |
| 全新机器、要审计每一步命令、需要留下可复核的安装链 | 完整版 |
| 本机工具已大体装好，只想快速接一份剧本开做 | 简短版 |
| 要把「安装授权」和「连接授权」分开、先看环境再逐层放行 | 渐进式 |
| 长驻 Agent / MCP host、本机不装产品 CLI | 完整版或渐进式，`binding_allowlist` 只列 MCP 类 binding |
| 批处理 / CI、要 `--json` 命令链 | 完整版，`binding_allowlist` 只列 CLI 类 binding |
| 只想确认环境、不做任何写入 | 渐进式 **L0 单独发送** |
| 只想装 skills、不装二进制、不连服务 | 渐进式 **L1 单独发送** |

## 三版共有的机制

1. **不询问 `cli|mcp|both`**：流程只认 `GenerationCapability<kind>`（`image|video|audio`），resolver 自动选 `executable` binding，理由写 `receipt.binding_ref`。[surface-choice.md](surface-choice.md) 已降级为 binding 参考。
2. **一次 `ApprovalWindow` = 一个自动化窗口**：绑定 `capability_kinds[]` / `intent_digest` / `binding_allowlist` / `count` / `cost_ceiling` / `retry_budget=2` / `stop_before_final_submit`；窗口内全自动，越界重新审批；凡 agent 发起的非只读动作都要审批，但不逐动作弹窗。
3. **有界自动重试**：可重试错误最多 2 次，每次同一 `action_id` + `idempotency_key` + `intent_digest` + `approval_ref`；UNKNOWN 只 `reconcile` 且不消耗预算；已 `ACCEPTED` / 业务拒绝 / 创意变化禁止重试；耗尽交 `needs_decision`。
4. 凭据只给 mode-0600 绝对路径，agent 不读取 / 打印 / 复制内容，不写进日志、stdout、仓库、evidence 或提示词。
5. 不自动付费生成、不自动发布、不自动派生子代理、不跑 race 检测；付费生成与正片提交仍是独立新授权。
6. 不解析人类输出：CLI 用 `--json` / `--agent` / `--events`，MCP 用 `structuredContent` / `tools/list` / `resources/read`。
7. `ACCEPTED ≠ COMPLETED ≠ BOUND ≠ REVIEWED ≠ 整体完成`；停在正片提交前；换 binding 不增加权限。
8. 不把 `eikona accepted` 写成 `production_ready`；`permission` 保持 `handoff_candidate`。
9. 不把客户端绝对路径当远程参考输入；`planned/readonly/unavailable` 不升级为可写；私网明文 HTTP 的 readiness 保持 `degraded|blocked`。

## 三版共同的真源

| 内容 | 唯一源 |
| --- | --- |
| 安装 / 连接命令全表 | [install-and-connect.md](install-and-connect.md) |
| CLI / MCP / HTTP / SDK 命令与差异（binding 参考） | [surface-choice.md](surface-choice.md) |
| 能力抽象、三类合同、重试、审批窗口 | 聚合仓 `yeisme-agent-my-skills` → `docs/drama-execution-kernel/capability-abstraction.md` |
| `automation_profile` 与六阶段流程 | 聚合仓 `yeisme-agent-my-skills` → `docs/drama-execution-kernel/automation-core.md` |
| 抽象与执行单元 | 聚合仓 → `docs/drama-execution-kernel/{abstract-design,execution-units}.md` |
| 唯一语义入口 | `ai-drama-router`（`ai-drama.route-plan.v1`） |

## 组合使用

- 用**渐进式**跑完 L0–L3 后，把 L4 换成**简短版**的交接段即可，不重复探测。
- 用**简短版**发现环境比预期复杂时，让 agent 改读**完整版**，不要凭记忆补命令。
- 任何版本遇到 `unavailable` / `needs_contract` / `REMOTE_PROFILE_UNSUPPORTED_COMMAND` / `invalid_reference`，保留已完成阶段、报告具体缺口并停止，不猜测、不重发、不绕过。
