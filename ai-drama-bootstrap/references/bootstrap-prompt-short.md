# 简短版提示词（复制即用）

> 适用场景：本机工具大体已装好、只想快速接一份剧本开做；或把复杂度交给 `ai-drama-bootstrap` Skill 自己展开。完整命令与门禁由 Skill 持有，这段提示词不重复。

---

```text
用 $ai-drama-bootstrap 引导本机做剧环境，然后直接开做。

输入（只填一次，缺失才问我）：
MODE=client  EIKONA_ENDPOINT={{...}}  SCAENA_ENDPOINT={{...}}
KEY_FILE_EIKONA={{/abs/0600/key}}  KEY_FILE_SCAENA={{/abs/0600/key}}
PROJECT={{project:drama-s01}}  STORY_PATH={{/abs/screenplay.txt}}
APPROVAL={{一次审批：capability_kinds[]=image|video|audio / count / cost_ceiling / retry_budget=2 / stop_before_final_submit=true}}

按顺序做，每步用 --json/--agent 或 MCP structuredContent，绝不解析人类输出：
0) 只读发现三类 GenerationCapability（image|video|audio）各自的 executable binding；不询问 cli/mcp；
0.5) 取一次 ApprovalWindow 授权，窗口内全自动；
1) 从 catalog.json 取实时版本装缺失的 eikona/scaena/auctra（MCP-only 客户端可跳过）；
2) npx --yes skills add 从 ai-drama-skills、scaena-skills 装 6 个做剧 skills；
3) 为候选 binding 配连接并 doctor；resolver 运行时自动选 executable binding，理由写 receipt.binding_ref；
   远程参考输入必须是 eikona:// URI；planned/readonly 不升级为可写；
4) STORY_PATH 交唯一入口 ai-drama-router，带 automation_profile（continuous / stop_before_final_submit=true /
   unknown_policy=reconcile_readonly / retry_budget=2 / approval_window_ref），按六阶段推进；
   三类生成统一走 GenerationCapability<kind>.invoke()（image=Eikona，video=Scaena/Aigora，audio=Sonora）。

自动重试：可重试错误（瞬时网络/5xx/429/mutationAttempted=false 超时/binding=unavailable）最多 2 次，
每次保持同一 action_id + idempotency_key + intent_digest + approval_ref；UNKNOWN 只 reconcile 且不消耗预算；
已 ACCEPTED / 业务拒绝 / 创意变化禁止重试；耗尽或越界交 needs_decision。

硬约束：key 只给 0600 路径，绝不读取或打印内容；不自动付费、不自动派生子代理、不跑 race；
停在正片提交前；ACCEPTED≠COMPLETED≠REVIEWED；换 binding 不增加权限；
最后给紧凑 receipt（含 approval_ref / binding_ref / retry_used）+ 精确下一条命令 + 阻塞项。

需要完整命令、binding 差异或分层执行时，读 $ai-drama-bootstrap 的 references/surface-choice.md、
references/install-and-connect.md、references/bootstrap-prompt-progressive.md。
```

## 与完整版的区别

| 项 | 简短版 | 完整版 |
| --- | --- | --- |
| 命令细节 | 委托给 Skill | 逐条写在提示词里 |
| 每层停止点 | 无，一次跑完 | 无，一次跑完 |
| 门禁文字 | 压缩成一行 | 完整展开 |
| 审批窗口 | 一步带出 | 独立阶段 0.5 完整展开 |
| 自动重试 | 压缩成一段 | 完整规则 |
| 适合 | 已装好工具、快速复用 | 新机器、需要审计每一步 |
| 凭据处理 | 相同（只给路径） | 相同 |

简短版**不降低任何安全约束**：审批窗口、凭据只读路径、有界重试、子代理默认关闭、UNKNOWN 不重投、完成分级全部保留。两版都**不询问 `cli|mcp|both`**。

## 如果只想要更短的一句

```text
用 $ai-drama-bootstrap 按 references/bootstrap-prompt.md 引导本机，输入见提示词顶部占位符；取一次 ApprovalWindow，窗口内全自动（含 retry_budget=2），不询问 cli/mcp；停在正片提交前，凭据只给 0600 路径。
```
