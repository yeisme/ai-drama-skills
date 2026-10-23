# AI Drama Skills

面向短剧、漫剧、美剧、电影、单元剧、音频剧等形态的开源 AI 做剧 Skills 矩阵。

`ai-drama-router` 是唯一入口。它先识别剧型、类型、阶段、当前 artifact 与最小上下文包，再选择一个 primary Skill 和最多一个兼容约束 Skill。专项 Skills 默认按需加载，不要求一次性安装或激活全部能力。

## 能力分组

做剧前先按[目标优先制作](ai-drama-router/references/goal-first-production.md)选择这轮路线。故事试写、动作 demo、单集成片与模块化资产库需要不同的证据和资产范围；快速 demo 不默认要求完整资产库。

- 项目启动：`manga-drama-project-starter`（普通作者文件入口；Auctra canonical screenplay，Scaena production state）
- 路由与策略：`ai-drama-router`、`ai-drama-context-pack-builder`
- 视觉与声音：`ai-drama-director`、`ai-drama-visual-language`、`ai-drama-edit-and-sound`
- 评审与生产：`ai-drama-assessment`、`ai-drama-continuity-supervisor`、`ai-drama-producer`、`ai-drama-production-orchestrator`
- Owner 交接：`auctra-ai-drama-panel-handoff`

所有剧本请求先走 `ai-drama-router`。启动、资料、写作、审稿、修订和整理只选一个主要方法，最多附加一个必要约束；剧型或时长缺失且会改变结构时返回 `needs_format_decision`。

## Owner 边界

Auctra 持有故事、人物和 canonical screenplay；Scaena 持有 ProductionGraph、分镜接受、生产接受、装配和交付；Eikona 持有图片/视觉 artifact；Skill 只输出 proposal、评估和 typed handoff。accepted screenplay 不等于 production-ready，selected 不等于 accepted。

## 本地与远程

本地使用各 owner 的 CLI；远程使用已发现的 MCP `tools/list`、`input_schema`、capabilities/resource 和 HTTP input/download。远程客户端无需安装 CLI 或访问服务端路径，不传 shell、绝对路径或 actor 字段；服务不可用或能力未注册时如实返回 `capability_missing`/`unregistered`，不伪造 receipt。

## 本地验证

```bash
python3 scripts/validate_skills.py
python3 ai-drama-router/scripts/validate_drama_matrix.py
```
