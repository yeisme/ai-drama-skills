# DEK v1 指针（`ai-drama-skills`）

本仓是 `yeisme/ai-drama-skills` 独立仓库。做剧执行内核（Drama Execution Kernel, DEK v1）的**规范设计真源**在聚合仓 `yeisme/yeisme-agent-my-skills`：

- 抽象设计：`https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/abstract-design.md`
- 执行单元设计：`https://github.com/yeisme/yeisme-agent-my-skills/blob/main/docs/drama-execution-kernel/execution-units.md`
- 合同 C1 / C2 / C3 与接入说明：同目录 `contracts/` 与 `integration.md`

本仓落地的 DEK skill：

| Skill | 职责 |
| --- | --- |
| `ai-drama-action-receipt` | 冻结引用、幂等授权、结果词汇与 UNKNOWN 恢复（C1） |
| `ai-drama-remote-operations` | owner HTTP 服务 + remote profile + 控制中心投影对齐 |

`ai-drama-router` 仍是唯一语义入口，新增 `execution_lane` 轴按需选中上述 skill；`ai-drama-production-orchestrator` 统一引用收据词汇。**不要在本仓复制或改写设计正文**，避免与聚合仓出现两份不同口径。

各 SKILL.md 里的设计链接使用绝对 URL，因此本仓被单独 clone 时仍可访问规范位置。
