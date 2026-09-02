---
name: ai-drama-critic-panel
description: Use when comparing AI drama story, shot, keyframe, audio, or episode candidates after an AssessmentContract is frozen; run parallel blind judges, rubric scoring, disagreement analysis, adjudication, repair proposals, and human review gates.
---

# AI Drama Critic Panel

## 目标

把“哪个好”变成同一 CandidateSet、同一题材承诺和同一 RubricProfile 内可比较、可解释、可复盘的推荐。评委负责 advisory assessment，Scaena 负责最终 production decision。它不是第一轮“这篇作品怎么样”的入口；没有 `AssessmentContract` 时必须退回 `ai-drama-assessment`。

## 评委角色

- Story：主题、钩子、因果、信息释放；
- Character：人物主动性、选择、代价、关系和情绪；
- Director/Visual：调度、镜头理由、主体身份、构图和可读性；
- Continuity：人物、服装、道具、空间、时间、动作和声音；
- Producer/Risk：时长、成本、rights、capability、交付风险。

## 工作流

1. 冻结 `AssessmentContract`、CandidateSet、CanonSnapshot、DirectorProfile、RubricProfile、JudgePanelProfile、seed、成本策略与适用的 capability/task-policy digest；若合同要求自然度，额外冻结 `naturalness_profile`、三条 lane、voice/calibration/exemption refs 和 report digests；Seedance 2.5 候选按需读取 `../ai-drama-router/references/seedance-2-5-capability-profile.md`。
2. 并行执行盲评；评委不可读取其他评委分数。
3. 同一 model family 标记为 correlation cluster；生成者自评不得成为决定性证据。
4. 用 0–4 anchored score 逐维评分，记录证据、coverage、indeterminate 和 blocker。
5. hard gates 先于软分；每维用中位数/截尾平均聚合，记录 IQR/分歧。
6. 近分候选做 pairwise comparison；Sol 输出排名和 `RepairProposal`。
7. 超出阈值、证据不足或 blocker 未决时输出 `needs_human_review`。

评分前置条件：`format_profile`、`genre_lens`、`audience_promise`、`evaluation_intent`、`anti_goals` 和 `score_eligibility=eligible` 必须存在。若自然度是目标，三条 lane 的证据、coverage、confidence 和校准 digest 也必须齐备。题材不要求的“主角失败/传统成长/道德正确”不能作为隐含扣分项。

## 初始阈值

P0 可从以下校准起点开始：hard gates 全通过、总分至少 80/100、关键维度至少 3/4、evidence coverage 至少 0.8、分歧不超过 1.0。未经 gold set 和人工标签校准，不得晋级 production policy。

## 禁止

- 不把简单多数票当作独立证据；
- 不跨 CandidateSet、rubric 或 profile 版本比较总分；
- 不把推荐直接写成 selected、production_accepted 或 export；
- 不把 `naturalness_score` 或 `pattern_risk` 暗扣到 genre/craft 分，也不把它解释成作者来源概率；
- 不把官方能力、fixture success、provider succeeded、1080p/MOV 或原生音频存在当作质量/声音/production hard gate 已通过；
- 不无限 reroll；
- 不写 raw prompt、provider payload 或完整 chain-of-thought。

## 验证

先在本仓库运行 `python3 scripts/validate_skills.py`。接入宿主后，再运行 Ordo、视觉资产 Owner 与 production Owner 各自文档声明的候选集、评估和 handoff 合同测试；本 Skill 不假设这些 Owner 的本地路径或技术栈。
