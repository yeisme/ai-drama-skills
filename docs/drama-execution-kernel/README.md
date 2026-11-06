# DEK v1 指针（`ai-drama-skills`）

本仓是 `yeisme/ai-drama-skills` 独立仓库。做剧执行内核（Drama Execution Kernel, DEK v1）的**规范设计真源**在聚合仓 `yeisme/yeisme-agent-my-skills`：

- 抽象设计：`https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/abstract-design.md`
- 执行单元设计：`https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/execution-units.md`
- 自动化做剧核心流程：`https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/automation-core.md`
- 合同 C1 / C2 / C3 与接入说明：同目录 `contracts/` 与 `integration.md`

本仓落地的 DEK skill：

| Skill | 职责 |
| --- | --- |
| `ai-drama-bootstrap` | Router 之前的环境准备层；可复制主提示词在 `ai-drama-bootstrap/references/bootstrap-prompt.md` |
| `ai-drama-action-receipt` | 冻结引用、幂等授权、结果词汇与 UNKNOWN 恢复（C1） |
| `ai-drama-remote-operations` | owner HTTP 服务 + remote profile + 控制中心投影对齐 |

## 引导提示词（`ai-drama-bootstrap/references/`）

| 文件 | 用途 |
| --- | --- |
| `bootstrap-prompt.md` | 完整版：逐条命令 + 全部门禁 |
| `bootstrap-prompt-short.md` | 简短版：~20 行，委托给 Skill |
| `bootstrap-prompt-progressive.md` | 渐进式：L0 探测 / L0.5 审批窗口 / L1 skills / L2 工具 / L3 连接 / L4 交接，每层可停 |
| `prompt-variants.md` | 三版对照与选择指南 |
| `surface-choice.md` | **binding 参考**（已降级）：CLI / MCP / HTTP / SDK 命令与差异，不再是流程门禁 |
| `install-and-connect.md` | 安装与连接真实命令全表 |

所有版本共有的机制：**不再询问 `cli|mcp|both`**；流程只认 `GenerationCapability<kind>`（`image|video|audio`），resolver 自动选 `executable` binding。凡 agent 发起的非只读动作都要审批，但用一次 `ApprovalWindow` 实现窗口内全自动（含 `retry_budget=2` 自动重试、自动换 binding、连续推进）；越界或耗尽交 `needs_decision`。UNKNOWN 只 `reconcile` 不消耗预算；凭据只给 0600 路径；不自动付费、不派生子代理、停在正片提交前。完整设计见聚合仓 `docs/drama-execution-kernel/capability-abstraction.md`。

`ai-drama-router` 仍是唯一语义入口，新增 `execution_lane` 轴按需选中上述 skill；`ai-drama-production-orchestrator` 统一引用收据词汇。**不要在本仓复制或改写设计正文**，避免与聚合仓出现两份不同口径。

各 SKILL.md 里的设计链接使用绝对 URL，因此本仓被单独 clone 时仍可访问规范位置。
