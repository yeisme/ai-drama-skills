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
| `bootstrap-prompt-progressive.md` | 渐进式：L0 探测 / L0.5 方式确认 / L1 skills / L2 CLI / L3 连接 / L4 交接，每层可停 |
| `prompt-variants.md` | 三版对照与选择指南 |
| `surface-choice.md` | **方式门禁**：`cli` / `mcp` / `both` 必须明确询问，含两条路径命令与差异 |
| `install-and-connect.md` | 安装与连接真实命令全表 |

所有版本共有的硬门禁：阶段 0 之后、任何安装或连接之前明确询问一次 `SURFACE`，不自动推断、不接受模糊表达；凭据只给 0600 路径；不自动付费、不派生子代理、UNKNOWN 只读 reconcile、停在正片提交前。

`ai-drama-router` 仍是唯一语义入口，新增 `execution_lane` 轴按需选中上述 skill；`ai-drama-production-orchestrator` 统一引用收据词汇。**不要在本仓复制或改写设计正文**，避免与聚合仓出现两份不同口径。

各 SKILL.md 里的设计链接使用绝对 URL，因此本仓被单独 clone 时仍可访问规范位置。
