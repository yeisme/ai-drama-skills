# AI 做剧矩阵路由示例

## 1. 美式犯罪悬疑剧

请求：开发 8 集美式犯罪悬疑剧，每集约 50 分钟，先完成 pilot 和 series bible。

```text
format_profile: us-hour-drama
genre_lens.primary: crime-mystery
originality_mode: pure_original
originality_decision_ref: originality:crime-pilot:v1
phase: series_plan
artifact: series_bible
context_pack_profile: series-development
primary_skill: ai-drama-showrunner
compatible_skill: ai-drama-story-architecture
canonical_owner: story_canon_owner
```

不应加载 Director、Visual、Edit/Sound 或 Production Orchestrator，直到进入对应阶段。

## 2. 竖屏复仇短剧

请求：做 60 集竖屏复仇短剧，优化人物、对白、爽点和钩子。

若集长、受众和核心类型未定：先路由 `ai-drama-format-strategist`。合同接受后：

```text
format_profile: vertical-short-drama
originality_mode: pure_original
originality_decision_ref: originality:revenge-proof-slice:v1
phase: proof_slice
artifact: three_episode_core_scene_candidates
context_pack_profile: series-development
primary_skill: ai-drama-showrunner
compatible_skill: ai-drama-story-architecture
artifact_disposition: candidate
persistence_policy: chat_only
batch_policy: proof_slice
acceptance_state: unreviewed
owner_action: request_selection
next_action: 为三集各写一个核心场景的 A/B 策略候选；用户确认主要人物声音前停止
```

不应先写 60 集，也不应把前 10 集集纲视为已经接受。三集通过状态变化、证据、Dialogue Live Test 和用户声音选择后，下一批最多扩写 5 集。

## 3. AI 漫剧镜头生产

请求：已有接受的场景稿，把第三场做成 8 镜头的漫剧分镜和关键帧方案。

```text
format_profile: manga-drama
phase: director_plan
artifact: shot_intent_set
context_pack_profile: director-planning
primary_skill: ai-drama-director
compatible_skill: ai-drama-visual-language
canonical_owner: story_canon_owner proposal / production_owner intent
```

导演提案接受后，下一 stage 才以 `ai-drama-visual-language` 为 primary。

## 4. 电影想法

请求：一个失忆消防员发现自己可能参与纵火，帮我先搭电影结构。

```text
format_profile: feature-film
originality_mode: pure_original
originality_decision_ref: originality:firefighter-feature:v1
phase: define
artifact: story_architecture
context_pack_profile: series-development
primary_skill: ai-drama-story-architecture
compatible_skill: ai-drama-character-engine
```

## 5. 一次性缺少 active Skill

目标 Skill 在宿主可信本地 catalog 中存在但未 active：

```text
resolution_status: resolved_local_on_demand
activation_plan: absent
```

直接按需读取 source，不执行持久化 activation。

## 6. 高频项目启用

用户明确要求为当前创作项目长期启用 `ai-drama-showrunner`：

```text
resolution_status: needs_profile_promotion
activation_plan.authorization_state: approved_current_request
activation_plan.activation_scope: project
activation_plan.preview_action: required
```

宿主先通过 activation adapter 预览；确认 scope、版本和冲突后再 apply。Router 不生成宿主命令，也不把 project 级能力扩大到 workspace/global。

## 7. 外部 Skill 缺失

本地 source 没有必需能力：

```text
resolution_status: needs_install_decision
status: blocked
```

列出普通 Agent fallback 和候选来源；不得在做剧 production run 中联网下载或热安装。

## 8. 宿主没有启用适配器

目标 Skill 需要持久化启用，但宿主没有声明 `skill_activation.preview/apply`：

```text
resolution_status: needs_profile_promotion
activation_plan.status: adapter_unavailable
status: needs_activation_decision
```

返回 proposal 和手工下一步，不猜测命令或配置文件。

## 9. 用户要求写 Markdown 文件

请求：把这版短剧试写成 Markdown 给我。

```text
output_format: markdown
artifact_disposition: candidate
persistence_policy: chat_only
batch_policy: bounded_batch
acceptance_state: unreviewed
owner_action: request_selection
```

Markdown 只是格式。若用户没有明确授权写入项目或选择候选，Router 不应创建最终项目文件，也不能把该文件当作 canonical source。

## 10. 用户选择候选，但尚未接受为 canonical

请求：第二版人物更像活人，就用 B。

```text
artifact_disposition: canonical_proposal
persistence_policy: review_workspace
acceptance_state: selected
owner_action: promote_for_review
status: needs_input
```

`selected` 允许进入 owner review，不允许直接写 canonical。只有 owner 的显式 accept receipt 才能将状态推进为 `accepted`。

## 11. 纯原创竖屏漫剧全链路

请求：从零做一部纯原创 12 集竖屏漫剧，由故事 canon owner 建立剧本，再交给 production owner 做分镜、主体候选、拼接、精修和成片导出。

```text
goal: pure_original_vertical_manga_drama
format_profile: manga-drama
originality_mode: pure_original
originality_decision_ref: originality:vertical-manga-drama:v1
artifact: end_to_end_production_run
primary_skill: ai-drama-production-orchestrator
compatible_skill: ai-drama-producer
canonical_owner: story_canon_owner + production_owner
artifact_disposition: canonical_proposal
persistence_policy: review_workspace
batch_policy: proof_slice
acceptance_state: unreviewed
stage_plans:
  - story_canon_and_screenplay
  - storyboard_breakdown_and_acceptance
  - subject_candidate_select_and_freeze
  - shot_generation_and_review
  - episode_assembly
  - owner_routed_refinement
  - production_delivery_review_and_export
gates:
  - originality_and_rights
  - screenplay_acceptance
  - storyboard_direction_confirmation
  - paid_provider_confirmation
  - human_subject_selection_and_freeze
  - shot_quality_and_audio_review
  - edit_cut_selection
  - delivery_and_export_confirmation
```

该计划不把“一键”解释为已有的单命令 goal。Orchestrator 先检查宿主声明的 capability registry，只调用真实存在的细粒度 capability 或已注册 workflow；完整 episode production goal 未注册时返回 capability gap，而不是伪造自动化。任何相似性风险都返回 `similarity_review_required`，并回到对应 owner 产生 successor candidate。
