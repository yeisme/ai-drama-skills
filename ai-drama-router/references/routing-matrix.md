# AI 做剧阶段与 Artifact 路由矩阵

复杂任务由 `ai-drama-production-orchestrator` 编排；Router 自身不并发写作。每个阶段恰好一个 primary Skill，最多一个 constraint Skill。视频 generation 按需读取 `video-model-capability-index.md` 和命中的独立档案，不把能力参考包变成额外的 primary Skill。

## 全局原创性门禁

阶段矩阵开始前先生成 `OriginalityDecision`：

- `pure_original`：从项目 canon 建立原创故事、角色、对白、视觉身份和声音身份；
- `licensed_adaptation`：只在授权范围内改编；
- `reference_constrained`：只消费维度化约束和 source refs；
- `transformative_research`：只产出研究/差异化证据，不直接成为发行资产。

Story 到 Delivery 的每个 stage 都引用同一 decision lineage。出现 `reference_rights_unknown`、`protected_expression_risk`、`style_identity_leak`、`similarity_review_required` 或 `adaptation_not_authorized` 时，ProductionGraph 必须停在对应 owner gate。

## 阶段矩阵

| `phase` | 当前 artifact / 用户工作 | Primary Skill | 可选 constraint | `context_pack_profile` | Canonical owner |
| --- | --- | --- | --- | --- | --- |
| `intake` | 媒介、剧型、时长、集数、受众、类型承诺 | `ai-drama-format-strategist` | `ai-drama-producer` | `series-development` 或无 | `story_canon_owner` proposal |
| `define` | premise、主题、核心冲突、故事引擎 | `ai-drama-story-architecture` | `ai-drama-character-engine` | `series-development` | `story_canon_owner` |
| `character` | 欲望、恐惧、秘密、关系、知识边界 | `ai-drama-character-engine` | `ai-drama-continuity-supervisor` | `series-development` 或 `episode-planning` | `story_canon_owner` |
| `series_plan` | series bible、季度、pilot、分集、单元结构 | `ai-drama-showrunner` | `ai-drama-story-architecture` | `series-development` / `episode-planning` | `story_canon_owner` |
| `episode_plan` | 本集功能、beat、开场与集尾钩子 | `ai-drama-story-architecture` | `ai-drama-showrunner` | `episode-planning` | `story_canon_owner` |
| `scene_draft` | 场景动作、对白、潜台词和转场 | `screenplay-scene-writer` | `creative-style-lens-builder` | `scene-drafting` | `story_canon_owner` |
| `director_plan` | 表演、调度、空间、镜头和逐镜 `ShotAudioIntent` | `ai-drama-director` | `ai-drama-visual-language` | `director-planning` | story proposal / `production_owner` intent；音频资产仍归 `audio_owner` |
| `visual_plan` | 主体、风格、关键帧、分镜、候选 brief | `ai-drama-visual-language` | `ai-drama-continuity-supervisor` | `visual-production` | `visual_asset_owner` proposal |
| `reference_video` | 参考视频动作、相机、构图、姿态约束 | `ai-drama-video-reference-director` | `ai-drama-continuity-supervisor` | `visual-production` | `production_owner` proposal |
| `assessment` | 评估目标、格式/题材/受众合同、成功标准、定性评估、自然度/AI模式风险三分轨 | `ai-drama-assessment` | `ai-drama-format-strategist` | `review-repair` 或 `series-development` | `story_canon_owner` proposal / `evaluation_owner` evidence |
| `evaluation` | 已冻结合同下的候选盲评、分歧、裁决、修复队列 | `ai-drama-critic-panel` | `ai-drama-producer` | `review-repair` | `evaluation_owner` evidence / artifact owner review |
| `generation` | 成本、权限、视频/原生音频能力、audio policy、批次和 retry admission | `ai-drama-producer` | `ai-drama-continuity-supervisor` | `visual-production` | `production_owner` |
| `assembly` | 剪辑、原生音轨审听/替换、声音、字幕、节奏和时间线 | `ai-drama-edit-and-sound` | `ai-drama-continuity-supervisor` | `assembly-delivery` | `production_owner` / `audio_owner` refs |
| `delivery_review` | 连续性、rights、cost、readiness 和交付 | `ai-drama-continuity-supervisor` | `ai-drama-producer` | `assembly-delivery` | `production_owner` |
| `cross_owner_run` | 完整阶段、pause/resume、typed handoff | `ai-drama-production-orchestrator` | `ai-drama-producer` | 各 stage 独立选择 | production facade + domain owners |

### 视频模型能力约束叠加

H3、Wan、Seedance、Kling V3 / Omni 不创建新的 route。它们只为已有 stage 增加
capability/task-policy 输入：

- `director_plan`：冻结 `ShotIntent`、`ShotAudioIntent`、镜头时长和引用用途；
- `visual_plan` / `reference_video`：保留 media ordinal、camera/motion/geometry 语义和 source digest；
- `generation`：在 credential lookup 前校验 task lock、引用计数、ratio/duration、output/audio policy、rights、cost 和 stale；
- `assembly` / `delivery_review`：原生音轨独立审听，`replace_after_generation` 是未知/未验证能力的默认后置策略；
- `cross_owner_run`：能力 full contract 不等于同时加载全部 Skills，也不等于 provider 或生产就绪。

generation stage 可输出非绑定 `video_model_guidance`。用户合法 exact lock 优先；先按硬能力
过滤。只有唯一匹配时才建议一个 family，多匹配时只列 eligible families，由生产 policy owner
决定。社区 research signal 不得破平局。典型镜头门禁和回退见
`video-model-drama-workflow-matrix.md`。

## 格式修饰规则

`format_profile` 改变 Skill 的工作约束，不创建新的 canonical owner：

- `vertical-short-drama`：每集开场压力、快速状态变化、集尾钩子和可复用场景优先。
- `manga-drama`：视觉可读性、主体连续、动作段、声音与话尾钩子优先。
- `us-hour-drama`：pilot 承诺、A/B/C 线、季度问题和人物长期变化优先。
- `us-half-hour-comedy`：角色缺陷、情境升级、回扣和可重复喜剧引擎优先。
- `procedural-series`：单元程序真实性、每集闭环和角色长线并行。
- `anthology-series`：共享主题/形式约束，不强制共享人物 canon。
- `feature-film`：集中主选择、有限支线、高潮和结尾回收。
- `audio-drama`：声音线索、角色声线、空间声场和可听动作优先。

详细结构由 `ai-drama-format-strategist/references/format-profiles.md` 提供，Router 只引用结果。

## 冲突规则

- format 未定且会改变结构时，`ai-drama-format-strategist` 优先于 Story/Writer。
- 评估请求若没有 `AssessmentContract`，`ai-drama-assessment` 优先于 `ai-drama-critic-panel`；不得直接输出综合分。
- 用户提到“AI味”时，`ai-drama-assessment` 必须把它拆为 `dialogue_liveability`、`narrative_naturalness`、`structural_formula_risk`；不得路由到作者来源检测器。
- 题材不要求的特征必须进入 `anti_goals`；不得用另一题材的失败、成长或道德标准替换当前合同。
- `unknown`、`not_applicable` 与 `defect` 分离；证据缺失只能降低 coverage 或触发 `score_not_applicable`，不能填成 0 分。
- 媒介/平台字段只有用户明示时才冻结；未明示时保持 `format_profile=unspecified`，不得主动贴平台标签。
- Story/episode plan 未接受时，Scene Writer、Director、Visual 不得拥有上游 canonical 决策。
- StyleLens、Continuity、Producer 可以作为约束，但不得与 primary writer 竞争 artifact ownership。
- 跨阶段不等于同时运行所有 Skill；先输出有序 stage plan，再逐阶段解析。
- production/cost/rights blocker 不能被创作质量分或用户一句“继续”覆盖。
- 原创性 blocker 不能被主体 `selected`/`frozen`、高分候选、production acceptance 或 export 请求覆盖。
- `pure_original` 不能通过改名、换脸、换色、同义改写或替换时代背景从单一作品派生。
- 支持或可能生成原生音频的 route 在 `director_plan` 缺少版本化 `ShotAudioIntent` 时不得进入 generation；视觉 pass 不得自动继承为音频 pass。

## 交互模式

- `guided_conversation`：提案、解释、结构化草稿和确认。
- `assisted_batch`：用户确认阶段后，运行有界候选、评估、导入和异常恢复。
- `unattended_batch`：只有明确授权、预算、质量、权限和异常策略冻结后才允许；Skill 激活仍不得在活动 run 中热切换。
