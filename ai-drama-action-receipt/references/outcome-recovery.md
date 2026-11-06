# Outcome 与恢复决策表

## 状态词汇（禁止互相冒充）

| 状态 | 含义 | 允许的下游 |
| --- | --- | --- |
| `ACCEPTED` | owner 返回了稳定 `action_id` / `submission_ref` / `run_id` | 只能进入 `reconcile` / 状态查询 |
| `COMPLETED` | 有权威 `readback_ref`，且回读一致 | 进入下一 EU |
| `BOUND` | `eikona replace` / `assets apply` 回读 `replacement_status: applied`、`binding_digest` 一致 | 仍不等于 review 通过 |
| `REVIEWED` | `review decide` / `production review` / accepted handoff 已记录 | 仍不等于 `production_admitted` |
| `PRODUCTION_ADMITTED` | Scaena 生产准入（稳定性矩阵 + 人工准入） | 不等于一集成片可交付 |
| `EXPORT_READY` | `release readiness` 门全过 | 才可 `export package --confirm` |
| `TERMINAL_REJECTED` | 明确业务 / 权限 / 校验拒绝 | 交回判断职责，不自动重试 |
| `UNKNOWN` | `unknown_accept`、超时、断线、响应不可解析 | **只读** |
| `PARTIAL` | 部分动作完成（如上传成功绑定失败） | 由新的冻结计划续做，不重发已完成动作 |

Eikona `permission: handoff_candidate` 明确表示「Eikona accepted ≠ Scaena production-ready」；`replacement_status: not_applied|staged|applied` 与 `feedback_status` 是独立维度。

## 恢复决策表

| 观测 | 证据要求 | 动作 |
| --- | --- | --- |
| `COMPLETED` + `readback_ref` 一致 | 稳定 id、原响应、计划、当前完整回读 | 无动作，进入下游 EU |
| `TERMINAL_REJECTED` | 明确 `error.code` / `data.reason` | 交回对应判断职责；不改参数绕过 |
| `UNKNOWN` 且有稳定 `action_id` | 原 id 存在 | `reconcile` 只读原任务；不换 key、不换模型、不创建替代任务 |
| `UNKNOWN` 且无稳定 id | 无 | 报告缺证据；不编造 id、不持续猜测、不重提写命令 |
| `mutation_attempted=false` 且原账本完整 | 原 plan/dispatch/result/ledger、原租约已释放、无提交事件 | 沿用原 `idempotency_key` 的未发送续行语义；不生成新 action |
| 超时 / 断线但可能已提交 | 无 | 不自动重试；只有此前已实际取得任务 id 才用 status 回查 |
| `PARTIAL` | 分阶段结果 | 新冻结计划只做缺失阶段，复用已保存的稳定 id |
| 新失败 | 新返回的失败 id | 以新 id 建立下一轮证据，保留此前全部记录 |

## 跨入口一致性

- `action_id` 是 Eikona `run_id` / Scaena `submission_ref` / 控制中心 `revision` 的唯一映射键；三者不得各查一次得出不同结论。
- 控制中心 `yeisme.work_queue.v1` 按 `scope/owner/object/source/revision` 去重；Preview allowlist 不产生 Owner 写入。
- `eikona events tail <run_id> --json` 的 NDJSON 位置、`scaena workflow status --agent` 的位置作为 `event_cursor`；缓存由 cursor 驱动，不由三层轮询驱动。

## 禁止

- 不把「命令退出 0」「已接收」「本地 state 文件存在」推断为「正在生成」或「已完成」；
- 不把 `OBSERVED_MATCHED` 伪装成 `COMPLETED`；
- 不删锁、不新建 state 路径、不换 run-dir 绕过未知；
- 不把技术证据刷新写成新的语义复核结论。
