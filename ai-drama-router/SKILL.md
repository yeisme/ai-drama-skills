---
name: ai-drama-router
description: Use when a user asks to create, adapt, develop, write, evaluate, reroll, storyboard, style-reference, produce, review, or hand off any AI drama, short-drama, manga-drama, television, film, procedural, anthology, comedy, or audio-drama project and the format matrix, minimal context pack, narrowest task-role Skill, activation decision, originality constraint, canonical owner, or next production stage must be selected.
---

# AI 做剧矩阵路由器

## 目标

作为所有“做剧”请求的唯一入口，把用户意图编译成一个可执行的 `DramaRoutePlan`。先确定剧型、类型、阶段、artifact 和上下文，再选择一个 primary Skill、最多一个 compatible constraint Skill，以及按需加载或启用决策。

Router 不代写完整剧本、不成为新的创作数据库，也不为一次任务批量安装整套 Skills。

## 参考资料

- 需要识别 canonical owner、revision 和 mutation boundary 时读取 `references/canon-boundary.md`。
- 需要按阶段和 artifact 选择工作 Skill 时读取 `references/routing-matrix.md`。
- 需要评估已有剧本、先定评价目标再评分时读取 `../ai-drama-assessment/references/assessment-contract.md`，并先选择 `ai-drama-assessment`。
- 需要判断 active、local on-demand、persistent activation、missing 或 external install 时读取 `references/skill-resolution-policy.md`。
- 需要生成稳定输出或映射到宿主运行时计划时读取 `references/drama-route-plan-contract.md`。
- 需要区分预览/候选/canonical proposal、聊天/临时/review workspace/canonical 持久化、试写/批次扩写和 selected/accepted 时读取 `references/artifact-lifecycle.md`。
- 请求声称纯原创、改编、参考某作品/创作者、使用外部素材，或准备生产/发行时，读取 `references/originality-and-reference-policy.md`，先生成 refs-only `OriginalityDecision`。
- 视频模型可能生成原生音频，或任务涉及对白、环境、Foley、音乐、静音和最终混音时，读取 `references/shot-audio-intent-contract.md`。
- 请求进入视频 generation、比较视频模型，或涉及 H3、Wan、Seedance、Kling V3 / Omni 时，先读取 `references/video-model-capability-index.md`，再只加载命中硬能力的独立档案；Seedance 旧入口 `references/seedance-2-5-capability-profile.md` 继续兼容。
- 需要在短对白、动作/相机参考、首尾帧、关键帧、edit/extend、20–30 秒长镜、2K 精修、原生音频和后置替换之间选择工作流时，读取 `references/video-model-drama-workflow-matrix.md`。
- 只有用户明确请求社区比较、趋势或研究时，才读取 `references/video-model-community-research-2026-09-01.md`；社区信号不得参与默认路由、模型平局、maturity 或 production readiness。
- 请求涉及一键出片、产品宣传、电影级镜头卡、长视频切 Shorts、可编程渲染、对话式剪辑、外部 NLE 或视频生产模板时，读取 `references/upstream-video-production-patterns.md`，只选择固定 commit 的一个主要 pattern family。
- 需要校验美剧、竖屏短剧、漫剧、电影和已有剧本请求时读取 `references/route-examples.md`。

## 路由流程

1. 识别十五个轴：`medium`、`format_profile`、`genre_lens`、`phase`、`artifact`、`task_role`、`evidence_state`、`canonical_owner`、`activation_scope`、`artifact_disposition`、`persistence_policy`、`batch_policy`、`acceptance_state`、`originality_mode`、`assessment_state`。
2. 生成或读取 `OriginalityDecision`。用户要求纯原创时固定为 `pure_original`；涉及改编、作品/创作者参考或外部素材时必须记录来源、权利依据、排除项、差异化约束和相似性 review gate。缺失时返回 `needs_originality_decision`，不得把“原创”当作无证据的标签。
3. 剧型、单集时长、季/集形态或类型承诺不明确，且会改变结构判断时，选择 `ai-drama-format-strategist` 作为 primary；不要让 Writer 猜承载形态。
4. 用户要求“评估/打分/看看好不好”或提到“AI味”但没有冻结 `AssessmentContract` 时，先选择 `ai-drama-assessment`；只输出题材化定性评估、自然度/机器模式风险分轨和缺失字段，不给未经合同批准的综合数字分。不要把通用 P0 生产门禁当作题材质量评分，也不要推断作者来源或平台标签。
5. 读取已有 CanonSnapshot、revision/digest、当前 artifact、最近 blocker 和权限/成本状态。跨项目知识只消费宿主声明的 Owner refs 或权限感知 ContextPack，不直接遍历私有状态。
6. 根据阶段选择一个 `context_pack_profile`。除纯 intake 外，需要 owner/project 历史的工作先调用 `ai-drama-context-pack-builder` 准备最小上下文。
7. 若目标视频 route 支持、可能支持或曾观察到原生音频，`director_plan` 必须先产出版本化 `ShotAudioIntent`；缺失时返回 `needs_audio_intent`，不得把声音留给 provider 自由补全。
8. 用户点名导演、作品、流派、情绪或视觉风格时，先使用 `creative-style-lens-builder` 生成原创 `StyleLens`；人名只保留在 source refs，不把 persona identity 传给 writer/provider。
9. 若请求命中上游视频生产模式，只选择一个主要 pattern family，把 repository、固定 commit、license status、adoption mode 和 verified date 记录进现有 `input_refs[]`。上游 pattern 不得成为 primary Skill 或 canonical owner，也不得在当前 stage 中联网刷新。
10. 新写或大幅重写超过 5 集时，将 `batch_policy` 设为 `proof_slice`：先选 3 个能检验人物声音、冲突策略和后果的代表集，每集只写一个核心场景并产生 A/B 策略候选。用户未确认主要人物声音前，不生成剩余全集。
11. 选择一个 primary Skill。只有连续性、风格、生产约束或明确输入依赖需要时，增加一个 compatible constraint Skill。
12. generation stage 需要视频模型能力时，生成 `binding_mode=non_binding` 的 `video_model_guidance`：先按硬约束过滤，合法 exact lock 优先；仅在硬能力或用户偏好产生唯一匹配时给出一个 suggested family。多个家族满足时只给 eligible families，交给生产 policy owner；不得按社区热度破平局。
13. 按 `active → resolved_local_on_demand → needs_profile_promotion → needs_install_decision` 顺序解析 Skill。一次性任务默认停在 local on-demand，不执行持久化 activation。
14. 若项目高频需要该 Skill，生成宿主无关的 `SkillActivationPlan`。宿主声明了启用适配器时可交给该适配器；未声明时只返回 proposal。没有当前用户的明确启用/安装授权时不得执行持久化变更。
15. 独立决定输出格式、artifact disposition、persistence 和 acceptance。“写成 Markdown”只设置输出格式；未评审 preview/candidate 默认 `unreviewed`，只能留在聊天、操作系统临时目录或宿主 review workspace，不得写最终项目路径。
16. 生成 Owner handoff、gates 和下一动作。在 provider call、canonical 修改、主体冻结、持久化 activation、production acceptance、export 或 publish 前停在对应 gate。**分镜/导演方向门禁**：任何付费资产生成（出图、视频、配音）之前，必须把分镜方向——故事脊柱、逐镜节拍、对白主干、视觉基调、时长合同——以用户能直接判断的形式显式呈现并获得当前用户确认；未确认不得进入生成阶段。

## 无项目随手视频路由（projectless quick）

用户只想要一条个人视频（没有剧项目、没有 ProductionGraph）时，不进入做剧矩阵：
路由 `scaena-local-video-operator`，只使用已发布的 quick 命令面
（`scaena video quick`，第一切片 plan + admission）。费用必须显式确认
（`--confirm` 或已保存的有上限 quick approval policy）；产物写入用户数据根
（`~/.scaena/`），永远 `production_ready=false`。用户提出做剧（分镜、剧集、
装配、交付）时立即回到标准做剧路由（`scaena-production-operator`），
quick 产物进项目必须显式 capture 走 pending review。

## 核心路由

| 用户意图 | Primary Skill | 可选约束 |
| --- | --- | --- |
| 创建、初始化、本地化或迁移漫剧/短剧/剧本生产项目 | `manga-drama-project-starter` | `ai-drama-producer` |
| 选择短剧/漫剧/美剧/电影/音频剧形态、时长、集数和类型契约 | `ai-drama-format-strategist` | `ai-drama-producer` |
| 一句话想法、主题、冲突、beat、结尾钩子 | `ai-drama-story-architecture` | `ai-drama-character-engine` |
| 角色动机、秘密、关系、知识边界和行动模拟 | `ai-drama-character-engine` | `ai-drama-continuity-supervisor` |
| 季度、多集、pilot、单元案、A/B/C 线和长期回报 | `ai-drama-showrunner` | `ai-drama-story-architecture` |
| 可拍场景、动作、对白、潜台词和转场 | `screenplay-scene-writer` | `creative-style-lens-builder` |
| 把情绪变成表演、调度、空间、镜头和声音意图 | `ai-drama-director` | `ai-drama-visual-language` |
| Blender/动作/相机参考视频、Seedance `reference_video` 入参 | `ai-drama-video-reference-director` | `ai-drama-continuity-supervisor` |
| 主体、风格、关键帧、分镜和视觉候选 | `ai-drama-visual-language` | `ai-drama-continuity-supervisor` |
| 节奏、剪辑、声音、字幕和 assembly | `ai-drama-edit-and-sound` | `ai-drama-continuity-supervisor` |
| 评估目标、题材镜头、评分资格与定性报告 | `ai-drama-assessment` | `ai-drama-format-strategist` |
| 多候选评分、争议、选优和有限修复 | `ai-drama-critic-panel` | `ai-drama-producer` |
| 成本、权限、预算、批次、retry 和 delivery readiness | `ai-drama-producer` | `ai-drama-critic-panel` |
| 跨故事、评估、视觉、声音和生产 Owner 运行与恢复 | `ai-drama-production-orchestrator` | `ai-drama-producer` |

## 输出

返回 `DramaRoutePlan`，至少包含：

- `goal`、`medium`、`format_profile`、`genre_lens`、`originality_mode`、`originality_decision_ref`；
- `phase`、`artifact`、`task_role`、`context_pack_profile`；
- `assessment_contract_ref`、`assessment_state`、`score_eligibility`；
- 可选 `naturalness_profile`、`naturalness_lanes`、`naturalness_report_refs`、`naturalness_score_policy`；
- `output_format`、`artifact_disposition`、`persistence_policy`、`batch_policy`、`acceptance_state`；
- `primary_skill`、可选 `compatible_skill`、可选 `style_lens_skill`；
- `resolution_status`、`skill_sources`、可选 `activation_plan`；
- `input_refs`、`missing_inputs`、`canonical_owner`、可选 `owner_binding`、`gates`；
- `owner_action`、`next_action`、`status`。

generation stage 可选增加 `video_model_guidance`：`binding_mode=non_binding`、
`required_capabilities[]`、`eligible_model_families[]`、可选 `suggested_model_family`、
`suggestion_basis[]`、`workflow_profile_ref/digest`。它不包含 exact model、channel、价格、
credential 或 provider payload。

复杂跨阶段请求还应输出有序 `stage_plans`；每个 stage 仍只有一个 primary 和最多一个 constraint。

## 严格失败条件

- `needs_format_decision`：承载形态不清且会改变结构。
- `needs_assessment_contract`：要求评估或评分，但题材、受众、承诺、意图或成功标准未冻结；媒介未明示时保持 `unspecified`，不单独触发该错误。
- `score_not_applicable`：只有定性观察或证据不足，禁止合成综合数字分。
- `assessment_not_comparable`：候选、题材镜头、rubric 或评价目标不在同一比较类中。
- `naturalness_not_comparable`：自然度缺少三层证据、校准集或一致的 lane/profile，禁止跨项目比较。
- `author_source_inference_forbidden`：请求把自然度或机器模式风险解释成作者来源概率。
- `needs_originality_decision`：没有选择原创性模式，或纯原创声明缺少可追溯 OriginalityDecision。
- `reference_rights_unknown` / `adaptation_not_authorized`：参考或改编的权利依据不足。
- `protected_expression_risk` / `style_identity_leak` / `similarity_review_required`：受保护表达、身份泄漏或相似性风险尚未解除。
- `needs_context`：关键 canon、人物、连续性或生产事实缺失。
- `needs_audio_intent`：原生音频 route 或音频相关镜头缺少逐镜 cue、policy、final mix owner 或验收门禁。
- `needs_style_lens`：点名人物/作品风格但没有维度化原创约束。
- `writer_conflict`：多个 writer 声称同一 canonical artifact。
- `needs_install_decision`：本地 source 不存在，或需要外部代码/工具。
- `activation_not_authorized`：需要持久化 activation，但用户未明确授权。
- `needs_voice_acceptance`：proof slice 已交付，但主要人物声音尚未由用户明确选择或认可。
- `needs_expansion_gate`：状态变化、证据、Dialogue Live Test、用户选择或有界改写条件尚未满足，不得扩大批次。
- `stale`：revision、digest、permission、StyleLens、SubjectVersion 或 production constraint 已变化。
- `external_side_effect`：付费调用、生产接受、导出、发布或外部 mutation 缺少授权。

## 边界

- 不把自然语言理解编码进 shell、CLI 或宿主适配器；Agent 读取 Skill 描述和 references 后选择，宿主能力只负责确定性查找、预览、持久化、回滚和验证。
- 不同时激活一组相互竞争的 writers；canonical 文本由宿主绑定的 story owner 维护。
- 不复制导演/作品 persona skill 的身份卡、表达 DNA、典型片段、专名、台词、口头禅或独特桥段。
- 不把改名、换脸、换色、同义改写或替换时代背景当作原创；纯原创必须由项目 canon、维度化 StyleLens 和 refs-only provenance 证明。
- 不让“继续”“一键”自动等价于外部安装、付费调用、接受资产、冻结主体、导出或发布。
- 不把 Markdown、文件名或“帮我写完”解释为 canonical acceptance；`selected` 也不等于 `accepted`。
- 不把已删除、未选、被拒绝或仅存在于聊天记忆的文本重新注入 canonical context。
- 不把上游仓库、镜头卡、模板、renderer 或 NLE 适配器变成新的 canonical owner；许可证未知或非商业限制时只允许独立研究与重实现。
- 不在生产会话中联网发现、安装、更新或热替换 Skill；已开始阶段固定 Skill lineage。

## 验证

从本 Skill 目录运行独立验证；它不依赖任何宿主仓库命令：

```bash
python3 scripts/validate_drama_matrix.py
```
