# Canon Boundary Reference

AI Drama Skills 只消费和产生带版本的 refs、proposal 与 evidence，不拥有剧本、资产或生产状态。

## Logical owner map

| 内容 | Canonical owner | Skill 可做的事 |
| --- | --- | --- |
| story world、beat、character state、screenplay revision | `story_canon_owner` | 读取 revision，提出新 proposal 或 handoff |
| DirectorScenePlan、creative StoryboardPlan、ShotAudioIntent | `story_canon_owner` planning state | 从 accepted screenplay 提出 planning candidate，等待 Auctra review 后导出 handoff |
| panel run、judge task、receipt、adjudication | `evaluation_owner` | 提交有界任务，读取结果和恢复证据 |
| visual artifact、subject/style/reference version | `visual_asset_owner` | 生成 visual brief、candidate proposal、评估请求 |
| production graph、production acceptance、assembly、delivery | `production_owner` | 请求状态转换，读取 gate 结果和交付证据 |
| audio artifact、voice、sound mix refs | `audio_owner` | 生成声音 proposal，读取已接受版本 |
| Skill routing、rubric guidance、director principles | `skill_source_owner` | 维护执行指导，不写业务事实 |

## Boundary rules

- 每个 handoff 必须携带 `owner`、`revision`、`digest`、`scope`、`created_at` 和来源 evidence ref。
- 任一输入 revision、subject/style version、权限、preflight 或生产状态改变后，依赖它的 proposal、score 和 recommendation 必须标记 `stale`，不能继续晋级。
- Skill 不得直接覆写 canonical screenplay、ProductionGraph、asset bytes 或 production acceptance；必须调用所属 Owner 的 typed action。
- Creative storyboard 与 production storyboard 必须分离：前者由 Auctra/story owner 审阅，后者只在 accepted handoff 后由 Scaena/production owner 创建。
- 聊天 transcript、模型记忆和未落 receipt 不能作为事实来源或交付依据。

## Host binding

Router 默认输出逻辑 Owner role。宿主可以通过 `owner_binding` 将逻辑 role 映射为本地 service、CLI、API、MCP tool 或 application action。未声明绑定时保留逻辑 role 并返回 handoff proposal，不猜测产品名、路径或命令。


## 作者侧交接

- 本地创作使用已安装 Auctra/Scaena CLI；远程创作先发现 `tools/list`、`input_schema`、capabilities/resource 和 HTTP input/download，客户端不安装 CLI、不传服务端路径、shell 或 actor。
- Auctra 负责 canonical screenplay、revision、digest、review 和 accepted handoff；Scaena 只消费 accepted handoff 并拥有 ProductionGraph、生产接受、装配和交付；Eikona 负责 visual artifact。
- `generate`、`accept`、`apply`、saved version、export/download、production acceptance 是不同 gate。未注册能力返回 `capability_missing`/`unregistered`，不伪造 receipt；远程长任务用原 run ref status 回查。
宿主绑定不得改变以下语义：唯一 canonical owner、版本化 refs、typed mutation、stale invalidation 和 fail-closed gate。
