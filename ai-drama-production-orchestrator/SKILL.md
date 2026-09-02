---
name: ai-drama-production-orchestrator
description: Use when coordinating a complete original AI drama or manga-drama pipeline from Auctra story and screenplay canon through Scaena storyboard breakdown, subject-card drawing, shot generation, episode assembly, defect-routed refinement, delivery review, and final export, with Eikona/Sonora/Ordo handoffs, originality and rights gates, bounded retries, receipts, evidence, and honest current-capability checks.
---

# AI Drama Production Orchestrator

## 目标

编排“做剧”闭环，而不是成为新的领域数据库。以 `DramaRoutePlan` 为入口，每个阶段只加载一个 primary Skill、最多一个 constraint Skill和一个最小 `DramaContextPack`；所有状态变化使用 typed refs、版本、digest、Owner receipt 和显式下一动作。

## 必读参考

- 纯原创 Auctra → Scaena → 抽卡 → 逐镜 → 拼接 → 精修 → 导出的执行矩阵、真实命令和完成条件：`references/original-manga-drama-production-loop.md`。
- canonical owner、revision 和 mutation boundary：`../ai-drama-router/references/canon-boundary.md`。
- 原创性、参考素材、权利与相似性 gate：`../ai-drama-router/references/originality-and-reference-policy.md`。
- 逐镜音频意图：`../ai-drama-router/references/shot-audio-intent-contract.md`。
- H3、Wan、Seedance、Kling V3 / Omni 的 task mode、引用、时间轴、音频/输出、topology 和 maturity：`../ai-drama-router/references/video-model-capability-index.md`，再按需读取独立档案。
- 成本、权限和生产约束：`../ai-drama-producer/references/production-constraints.md`。

## 三种运行模式

- `guided_conversation`：提案和确认优先；
- `assisted_batch`：阶段性确认后运行有界批次；
- `unattended_batch`：只有成本、权限、质量、异常策略和 kill switch 冻结后才可启用。

## 工作流

1. 消费 `ai-drama-router` 的 `DramaRoutePlan` 与 `OriginalityDecision`；若剧型/类型/原创性未冻结，先完成对应 gate，不得直接进入 Writer 或 provider。
2. 检查 `auctra --help`、`scaena --help` 和 `scaena workflow list --agent`。只调用当前真实存在的命令或已注册 goal；没有 `shortdrama.episode-production` 时不得声称“一键整集”已经可用。
3. 编译 CreativeBrief、CanonSnapshot、DirectorProfile、ProductionConstraintProfile 和 capability ledger；把 current、partial、target 明确分开。
4. 在 Auctra 中完成原创 premise、人物、proof slice、剧本候选、评审、accepted screenplay revision 和 Scaena handoff。选择候选不等于 canonical acceptance。
5. 在 Scaena 中导入 handoff、拆解分镜，并在任何付费生成前显式呈现和确认故事脊柱、逐镜节拍、对白主干、视觉基调与时长合同。
6. 建立主体依赖波次；通过 DrawSession plan/start、Eikona 生成、record、human-only select/freeze 完成抽卡。`selected`/`frozen` 不等于 shot/production/export acceptance。
7. 视频路线可能生成原生音频时，把 `screenplay/dialogue → ShotAudioIntent → capability/policy → video-native registration or Sonora render → sound review → Scaena assembly` 建成显式 stage handoff。默认 `replace_after_generation`；只有独立证据齐全才允许 `video_native`。
8. 视频 generation stage 绑定 provider-neutral task policy、reference ordinal/count、ratio/duration lock、output/audio policy、workflow profile 和 capability maturity，并携带 `binding_mode=non_binding` 的 family guidance；provider wire hint 由 adapter 推导。全量合同/fixture 支持不等于 live/production ready，社区信号不得改变路由。
9. 为每个 stage 生成最小、版本化、可失效的 `DramaContextPack`；不得把上一个阶段的全量上下文原样传给所有下游。
10. 逐镜生成候选，按 visual、audio、continuity、human review 和 production acceptance 顺序推进。Ordo 可运行有界并行候选/评委并保存 evidence，但不获得 owner 权限。
11. 用 Scaena episode preview、edit plan/timeline/render/score/select 完成拼接与选版；自动评分只生成 recommendation。
12. 先分类缺陷，再回 Auctra、storyboard、asset/Eikona、shot generation、Sonora、edit 或 delivery owner 产生 successor。每个失败只允许一个有界 repair loop；不得无限 reroll 或覆盖最终文件。
13. 处理 pause/resume、partial failure、unknown accept、Skill/context drift 和 stale invalidation。只使受影响的未开始后代 stale。
14. 只在 Scaena 明确选择、连续性检查、独立音频 review、production acceptance、originality/rights review、delivery review 与用户要求的 export receipt 全部存在后结束。Export 不自动等于 publish。

## 阶段计划

每个 `stage_plan` 至少固定：`stage_kind`、`context_pack_ref/digest`、`originality_decision_ref`、一个 `primary_skill`、可选 `constraint_skill`、Owner、input/output contract、gates、receipt/evidence refs 和 next action。未开始阶段可因 Skill/context drift 标为 stale；运行中或已完成 Owner job 保留原 pinned lineage。

## 状态不变量

```text
generated → assessed_visual + assessed_audio → recommended → human_review → selected
→ consistency_review → audio_review → production_accepted → assembled
```

禁止 `assessed → selected`、`recommended → production_accepted`、视觉 pass 自动继承音频 pass，和“provider succeeded 即交付”。

## 当前能力边界

- 当前默认运行方式是细粒度阶段命令和已注册 workflow 的组合。
- `scaena enhance run` v1 只允许 fixture 驱动验证，不能宣称真实付费 enhancement provider 已接通。
- 全自动整集 goal、全异常无人值守恢复和平台发布是 target；缺少真实命令、receipt 或用户授权时返回 blocker。

## 验证

```bash
cd agent/ordo
bun run test
cd ../../agent/scaena
task test:architecture
task test:integration
```
