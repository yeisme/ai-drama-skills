---
name: ai-drama-production-orchestrator
description: Use when coordinating a DramaRoutePlan across AI drama format, context, story, screenplay, directing, visual, evaluation, continuity, audio, and production stages owned by Auctra, Ordo, Eikona, Scaena, Sonora, or related services with typed handoffs, bounded parallelism, approvals, retries, receipts, evidence, and guided-to-unattended maturity.
---

# AI Drama Production Orchestrator

## 目标

编排“做剧”闭环，而不是成为新的领域数据库。以 `DramaRoutePlan` 为入口，每个阶段只加载一个 primary Skill、最多一个 constraint Skill和一个最小 `DramaContextPack`；所有状态变化使用 typed refs、版本、digest、Owner receipt 和显式下一动作。

## 三种运行模式

- `guided_conversation`：提案和确认优先；
- `assisted_batch`：阶段性确认后运行有界批次；
- `unattended_batch`：只有成本、权限、质量、异常策略和 kill switch 冻结后才可启用。

## 工作流

1. 消费 `ai-drama-router` 的 `DramaRoutePlan`；若剧型/类型未冻结，先完成 `ai-drama-format-strategist`，不得直接进入 Writer 或 provider。
2. 读取 `ai-drama-router/references/canon-boundary.md` 与 `ai-drama-producer/references/production-constraints.md`，编译 CreativeBrief、CanonSnapshot、DirectorProfile 和 ProductionConstraintProfile。
3. 视频路线可能生成原生音频时，读取 `ai-drama-router/references/shot-audio-intent-contract.md`；把 `screenplay/dialogue → ShotAudioIntent → capability/policy → video-native registration or Sonora render → sound review → Scaena assembly` 建成显式 stage handoff。
4. 为每个 stage 调用 `ai-drama-context-pack-builder` 生成最小、版本化、可失效的上下文包；不得把上一个阶段的全量上下文原样传给所有下游。
5. 逐阶段调度 Story/Character/Showrunner/Scene Writer/Director/Visual/Critic/Continuity/Edit/Sound/Producer Skills。Skill 未 active 时按需读取本地 source；production run 中不得安装、更新或热切换。
6. 在 Ordo 中执行并行候选和评委任务，保存 attempt/receipt/evidence。
7. 把 Auctra screenplay、Eikona artifact、Sonora audio refs/mix refs 和评估推荐交给对应 Owner；不跨边界写入。视频原生音频只登记 parent video、policy 和 review facts，不伪装成已接受 mix。
8. 处理 review、repair、pause、resume、partial failure、unknown accept、Skill/context drift 和 stale invalidation。镜头时长、对白 span、audio cue、provider audio policy、capability digest 或 Sonora mix revision 变化时，只使受影响的未开始后代 stale。
9. 读取 `ai-drama-continuity-supervisor/references/continuity-evidence.md`；只在 Scaena 明确选择、连续性检查、独立音频 review、production acceptance 和 delivery review 后结束。

## 阶段计划

每个 `stage_plan` 至少固定：`stage_kind`、`context_pack_ref/digest`、一个 `primary_skill`、可选 `constraint_skill`、Owner、input/output contract、gates 和 next action。未开始阶段可因 Skill/context drift 标为 stale；运行中或已完成 Owner job 保留原 pinned lineage。

## 状态不变量

```text
generated → assessed_visual + assessed_audio → recommended → human_review → selected
→ consistency_review → audio_review → production_accepted → assembled
```

禁止 `assessed → selected`、`recommended → production_accepted`、视觉 pass 自动继承音频 pass，和“provider succeeded 即交付”。

## 验证

```bash
cd agent/ordo
bun run test
cd ../../agent/scaena
task test:architecture
task test:integration
```
