# 上游视频生产模式参考

## 目的

当请求涉及一键出片、电影级镜头配方、长视频切 Shorts、可编程渲染、对话式修改、外部 NLE 或视频生产模板时，用本参考选择一个固定版本的上游 pattern family。上游只提供设计证据，不成为 Skill、canonical owner、provider 或运行时依赖。

生产 stage 必须离线可重放。Router 不能在 stage 中联网发现、安装、更新或热替换上游内容。

固定快照最后核对时间：`2026-08-24 UTC`。

## 参考目录

| upstream_id | repository | commit | license stance | pattern family | adoption mode |
| --- | --- | --- | --- | --- | --- |
| `moneyprinter-turbo` | https://github.com/harry0703/MoneyPrinterTurbo | `110997c15abd1660b00add8e41feefedb3df6a8c` | MIT | `one-click-pipeline-lifecycle` | `pattern-reference` |
| `video-shotcraft` | https://github.com/Vincentwei1021/video-shotcraft | `986427ee909a14dfaa96f6fa6cd7cfaa69b55881` | Apache-2.0 | `cinematic-shot-recipe` | `contract-reimplementation` |
| `ai-youtube-shorts` | https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator | `c30376e94326f8674793c960b482eb532ffbf1f6` | unconfirmed | `long-video-highlight-extraction` | `contract-reimplementation` |
| `remotion-skills` | https://github.com/remotion-dev/skills | `78834e618218fda87f5c7e4c54b5c55357f74d52` | repository license unconfirmed; runtime license is separate | `programmable-renderer-best-practices` | `adapter-canary` |
| `firered-openstoryline` | https://github.com/FireRedTeam/FireRed-OpenStoryline | `c9e945215586f45c12a61c1951ee9a8e9c43a027` | Apache-2.0 | `conversational-edit-proposal` | `pattern-reference` |
| `jianying-editor` | https://github.com/luoluoluo22/jianying-editor-skill | `f421c8a036f4fda888a83b38fc90bb9c00d6faa9` | MIT | `external-nle-draft-handoff` | `adapter-canary` |
| `claude-video-toolkit` | https://github.com/digitalsamba/claude-code-video-toolkit | `c05a0cb7e646da122ded600db5fc97468e8611d9` | MIT | `creator-template-and-review-pack` | `pattern-reference` |
| `rnskill` | https://github.com/Pluviobyte/rnskill | `d4509487ad4585033b3be92b577c2c98c4255c0a` | non-commercial or module-specific review required | `scenario-skill-catalog-research` | `research-only` |

`unconfirmed`、`research-only` 或 non-commercial 状态禁止复制源码、Skill 正文、模板库和媒体资产。只允许观察高层流程并独立设计合同。

## Pattern cards

### `one-click-pipeline-lifecycle`

- 适用：用户给关键词、brief 或主题，希望快速得到可预览视频。
- 借鉴：显式阶段、任务状态、可恢复步骤、缓存、预览与单入口体验。
- 编译：按顺序生成 story proposal、asset requests、audio/subtitle intent、production plan 和 export proposal。
- 禁止：把“一键”解释为自动接受 canonical、付费调用、发布、安装 provider 或跳过人工 gate。

### `cinematic-shot-recipe`

- 适用：产品宣传、App demo、品牌短片、电影化镜头或需要可复用镜头语言。
- 借鉴：intent、duration range、energy、camera、composition、transition affinity、pitfalls 和 validation hints。
- 编译：配方只约束 director/visual proposal，接受后才能进入 production owner 的 shot intent。
- 禁止：复制上游卡片正文、把配方直接当 provider prompt，或让配方覆盖 continuity/rights/cost gate。

### `long-video-highlight-extraction`

- 适用：访谈、播客、演讲、教程或横屏长视频切竖屏短片。
- 借鉴：转写、候选时间段、高光排序、画幅重构、字幕与导出阶段。
- 分工：`video_analysis_owner` 产生带 time span/evidence/confidence 的候选；`production_owner` 只消费 accepted candidate。
- 评分：hook、information density、emotional change、standalone clarity、crop safety；不得伪造精确“爆款概率”。

### `programmable-renderer-best-practices`

- 适用：代码化 composition、字幕动画、数据驱动画面、品牌模板和确定性重渲染。
- 借鉴：composition boundary、duration/fps、asset preload、audio timing、caption layout、render performance 和 smoke render。
- 分工：renderer adapter 只消费 frozen production spec，输出 artifact/manifest/receipt；不拥有 timeline canonical。
- 门禁：依赖与 runtime 许可证、版本、性能、字体/codec 和 deterministic render 均需独立 canary。

### `conversational-edit-proposal`

- 适用：“把第二镜更快”“这里换字幕”“重新生成这一段”等中途微调。
- 借鉴：自然语言到工具节点、局部影响范围、预览、继续对话和撤销心智。
- 编译：先输出 typed proposal/diff、affected refs、cost、stale risk、review gate 和 rollback；owner 接受后才 mutation。
- 禁止：聊天消息直接写 canonical，或让模型运行时生成/覆盖 Skill。

### `external-nle-draft-handoff`

- 适用：把 accepted timeline 送到剪映或其他外部 NLE 继续人工编辑。
- 借鉴：素材、片段、字幕、特效和时间线映射。
- 分工：`production_owner` 生成一向性 draft/export；外部结果回流时作为新 source import、diff 和 review。
- 门禁：固定 OS、应用版本、draft format 和兼容矩阵；UI automation 不得成为 production acceptance 依据。

### `creator-template-and-review-pack`

- 适用：短视频模板、品牌包、场景清单、逐场 review 与交付检查。
- 借鉴：brand tokens、scene template、review rubric、export checklist。
- 编译：作为 ContextPack、input constraint 或 reviewer rubric，不保存第二套项目状态。
- 禁止：模板直接持有 provider credential、发布账号或 canonical asset bytes。

### `scenario-skill-catalog-research`

- 适用：探索选题、改写、动效、质检等候选场景。
- 借鉴：只抽取场景名称、用户 job 和检查维度，形成独立 scenario matrix。
- 禁止：复制 non-commercial Skills、固定工作区路径、宿主特定子 Agent 要求或整套执行链。

## 路由映射

| pattern family | primary Skill | logical owner handoff |
| --- | --- | --- |
| `one-click-pipeline-lifecycle` | 当前阶段对应的最窄 Skill；跨阶段才使用 `ai-drama-production-orchestrator` | story、visual、audio、production、execution owner 分段交接 |
| `cinematic-shot-recipe` | `ai-drama-director` 或 `ai-drama-visual-language` | accepted proposal → `production_owner` |
| `long-video-highlight-extraction` | `ai-drama-edit-and-sound` | `video_analysis_owner` evidence → `production_owner` |
| `programmable-renderer-best-practices` | `ai-drama-edit-and-sound` | frozen timeline/spec → renderer adapter |
| `conversational-edit-proposal` | 受影响 artifact 对应的最窄 Skill | typed proposal → canonical owner review |
| `external-nle-draft-handoff` | `ai-drama-edit-and-sound` | accepted timeline → external editor adapter |
| `creator-template-and-review-pack` | 当前阶段对应的最窄 Skill | ContextPack/rubric → corresponding owner |
| `scenario-skill-catalog-research` | `ai-drama-format-strategist` | exploratory scenario proposal only |

## `input_refs` 记录

命中本参考时，把固定 snapshot 作为现有 `DramaRoutePlan.input_refs[]` 的一个元素：

```text
kind: upstream_pattern
upstream_id: video-shotcraft
repository_url: https://github.com/Vincentwei1021/video-shotcraft
commit: 986427ee909a14dfaa96f6fa6cd7cfaa69b55881
pattern_id: cinematic-shot-recipe
adoption_mode: contract-reimplementation
license_status: Apache-2.0
verified_at: 2026-08-24
```

同一 stage 最多选择一个主要 pattern family。若多个项目支撑同一模式，选一个主要 snapshot，其他只作为证据注记，不把它们堆成多个 primary Skills。

## 更新规则

1. 宿主在生产 stage 之外检查 upstream HEAD、release、license 和相关文件 diff。
2. 只审查已采用 pattern 涉及的变化，不因 star、宣传文案或 provider 数量自动升级。
3. `contract-reimplementation` 只更新本地合同和验收，不复制上游实现。
4. `adapter-canary` 必须重新验证版本、fixture、输出 manifest、失败恢复和 rollback。
5. 新 commit 只进入新的 route plan；旧 plan 保留旧 lineage。
6. 许可证变得不明确、收紧或与商业用途冲突时，保持旧实现隔离并停止继续移植。

## 严格边界

- 上游项目不能替代 primary Skill、compatible constraint 或 logical owner。
- 不从上游导入 provider credential、账号、发布权限、用户私有数据或云端 session。
- 不让外部模板、镜头卡、LLM 分数或自动化结果直接获得 `accepted`。
- 不把未知许可证仓库当作可复制代码源。
- 不在 active production stage 中联网、安装、升级或改变固定 commit。
