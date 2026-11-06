# 简短版提示词（复制即用）

> 适用场景：本机工具大体已装好、只想快速接一份剧本开做；或把复杂度交给 `ai-drama-bootstrap` Skill 自己展开。完整命令与门禁由 Skill 持有，这段提示词不重复。

---

```text
用 $ai-drama-bootstrap 引导本机做剧环境，然后直接开做。

输入（只填一次，缺失才问我）：
MODE=client  EIKONA_ENDPOINT={{...}}  SCAENA_ENDPOINT={{...}}
KEY_FILE_EIKONA={{/abs/0600/key}}  KEY_FILE_SCAENA={{/abs/0600/key}}
PROJECT={{project:drama-s01}}  STORY_PATH={{/abs/screenplay.txt}}
SURFACE={{cli|mcp|both}}

按顺序做，每步用 --json/--agent 或 MCP structuredContent，绝不解析人类输出：
0) 只读探测缺哪些 CLI、skills，是否已有 MCP host 配置；
0.5) 先明确问一次 cli/mcp/both，不自动推断、「随便」不算选择：
     cli=装 owner CLI + remote connect；mcp=只配 MCP stdio（可不装产品 CLI）；both=两者都配但同一 action_id 只执行一侧；
1) surface=cli|both 才从 https://raw.githubusercontent.com/yeisme/yeisme-dist/main/catalog.json 取实时版本装缺失的 eikona/scaena/auctra；mcp 跳过；
2) 用 npx --yes skills add 从 ai-drama-skills、scaena-skills 装 ai-drama-router、ai-drama-bootstrap、ai-drama-action-receipt、ai-drama-remote-operations、scaena-asset-draw-batch、scaena-bounded-replacement；
3) cli 走 eikona/scaena remote connect + remote doctor；mcp 走 eikona mcp doctor/capabilities/--transport stdio + scaena mcp serve --stdio + mcp doctor，只从 tools/list/inputSchema/资源读参数，远程参考输入必须是 eikona:// URI；
4) 把 STORY_PATH 交给唯一入口 ai-drama-router，带 automation_profile（continuous / stop_before_final_submit=true / unknown_policy=reconcile_readonly），按六阶段推进。

硬约束：key 只给 0600 路径，绝不读取或打印内容；不自动付费、不自动派生子代理、不跑 race；停在正片提交前；UNKNOWN 只读 reconcile；ACCEPTED≠COMPLETED≠REVIEWED；最后给紧凑 receipt（含 surface）+ 精确下一条命令 + 阻塞项。

需要完整命令、方式差异、占位符说明或分层执行时，读 $ai-drama-bootstrap 的 references/surface-choice.md、references/install-and-connect.md、references/bootstrap-prompt-progressive.md。
```

## 与完整版的区别

| 项 | 简短版 | 完整版 |
| --- | --- | --- |
| 命令细节 | 委托给 Skill | 逐条写在提示词里 |
| 每层停止点 | 无，一次跑完 | 无，一次跑完 |
| 门禁文字 | 压缩成一行 | 完整展开 |
| `cli/mcp/both` 询问 | 保留（压缩成一步） | 独立阶段 0.5 完整展开 |
| 适合 | 已装好工具、快速复用 | 新机器、需要审计每一步 |
| 凭据处理 | 相同（只给路径） | 相同 |

简短版**不降低任何安全约束**：付费授权、凭据只读路径、子代理默认关闭、UNKNOWN 不重投、完成分级全部保留。

## 如果只想要更短的一句

```text
用 $ai-drama-bootstrap 按 references/bootstrap-prompt.md 引导本机，输入见提示词顶部占位符；先明确问我一次 cli/mcp/both，不自动推断；停在正片提交前，凭据只给 0600 路径。
```
