---
name: ai-drama-assessment
description: Use when evaluating, scoring, or comparing an existing drama or screenplay whose format, genre promise, audience, evaluation intent, naturalness/AI-pattern criteria, or success criteria have not yet been made explicit; build a genre-conditioned assessment contract and qualitative report first.
---

# AI Drama Assessment

## 定位

这是做剧评估的第一道门，不是编剧、改写器或多评委裁判。它先回答“这是什么类型的作品、希望它达成什么、应当用什么标准判断”，再决定是否允许数字评分。

## 不可违背的顺序

```text
原稿 / 候选
  -> AssessmentContract
  -> 题材化定性评估
  -> score eligibility
  ->（合同已接受时）Rubric + PanelRun
  -> 评分、分歧和人类决定
```

- 缺少 `genre_lens`、`audience`、`audience_promise` 或 `evaluation_intent` 时，不给综合数字分。`medium`/`format_profile` 只有用户明示时才冻结；未明示时保持 `unspecified`，仅将格式/生产维度标记为 `not_applicable`。
- “主角不能输”“必须成长”“必须降低爽度”不是通用标准；是否需要失败、代价或成长，要由题材合同决定。
- `unknown`、`not_applicable` 和 `defect` 必须分开。证据不足不能被当成负分。
- 单候选的第一轮输出是 assessment，不是“质量排名”；没有第二候选时不得伪造比较结论。
- “AI味”默认解释为文本自然度与可观察的机器模式风险，不是作者来源检测，也不输出“由 AI 生成的概率”。
- 自然度低、类型化夸张、网络口语和公式化爽点不是同一件事；必须按分轨和项目声音合同分别记录。

## AssessmentContract 必须冻结

- `subject_ref`、`candidate_digest`、`source_revision`；
- `medium`、`format_profile`、`genre_lens`、`audience`、`platform`、`duration`、`episode_scope`；
- `audience_promise`、`creator_intent`、`evaluation_intent`（例如点击留存、题材兑现、人物、连续性、制作可行性）；
- `anti_goals`（本题材不应被惩罚的特征）；
- `comparison_class`、`rubric_profile`、`hard_gate_profile`；
- `evidence_policy`、`unknowns`、`rights_state`、`canonical_owner`；
- `score_eligibility`：`eligible`、`ineligible` 或 `partial`。
- 自然度评估还必须声明 `naturalness_profile`、`naturalness_lanes`、`voice_profile_ref`、`calibration_set_ref`、`style_exemptions` 和 `naturalness_score_policy`。

合同未被人类或 owner 接受前，评分只能作为草拟建议，不能写成最终评估结论。

## 定性评估顺序

1. **作品承诺**：一句话说明题材承诺、主角快感或情绪回报、观众为什么继续看。
2. **兑现证据**：指出原稿中已经兑现的场景、动作、对白、信息反转和集尾钩子。
3. **机制健康度**：检查爽点/笑点/悬疑/情感等核心机制是否变化、升级并产生后果。
4. **因果与可信度**：检查人物是否依据自己的知识、利益、能力和风险行动；不把“不符合另一题材偏好”误写成逻辑缺陷。
5. **连续性与格式**：检查状态、力量、道具、时空、镜头可拍性和单集承载是否符合已冻结的格式。
6. **风险分层**：分别列出 strength、risk、unknown、blocker，并给出证据引用和影响范围。

## AI味/自然度评估

首版 screenplay 只支持三条独立分轨：

1. `dialogue_liveability`：由 `dialogue-live-test` 检查人物目标、知识边界、策略变化、可表演性和是否替作者讲主题；
2. `narrative_naturalness`：复用 Auctra `screenplay_naturalness_v1` 的确定性证据，并以 v2 增加项目声音和上下文诊断；
3. `structural_formula_risk`：检查“被轻视 → 亮牌 → 对手震惊”等结构模板是否连续重复、是否造成状态不变。

三条分轨分别输出 0–4 行为锚定分、coverage、confidence 和证据 refs。`naturalness_score` 越高越自然；`pattern_risk` 越高风险越大。两者不得合成作者来源概率，也不得默认扣减 genre/craft 分。

以下内容不能自动判为 AI 味：

- 题材要求的短句、夸张金句、系统播报、等级宣告和快速亮牌；
- 主角连续获胜或毒舌、不服从组织规则；
- 项目声音合同已经声明可接受的句式、节奏或口语模式。

如果命中项目级声音合同的允许模式，finding 仍保留，但必须带范围化 `exemption_ref`，从风险聚合中排除，不能静默删除证据。

### 0–4 行为锚点

- `0`：交付残留、占位符、助手话术或严重不可表演/不可理解；只有明确交付红线才可阻断；
- `1`：普遍模板化，人物和场景替换后仍基本成立；
- `2`：自然与模板混合，存在可定位且需要定向修复的问题；
- `3`：基本自然，偶有解释腔或模式重复，不影响主要观看目标；
- `4`：人物目标、知识、策略、节奏和声音有持续可观察证据。

没有足够覆盖或没有校准集时只能返回 `unknown`/低置信度，不得伪造 0 分。

## 男频无敌/异能爽剧的特殊规则

这类题材允许主角连续获胜，也不要求用“主角可能死亡”制造悬念。应评估：

- 每次胜利的兑现方式是否变化，而不是只重复“被轻视 → 亮底牌 → 对手震惊”；
- 观众期待的是哪一种过程答案：亮哪张牌、如何反杀、如何利用规则、付出什么隐藏代价；
- 对手是否有可信的目标、信息和误判，而不是只为送出打脸而降智；
- 力量公开层、隐藏层、限制条件和升级空间是否可追踪；
- 集尾是否改变下一集的目标、关系、责任、资源或代价；
- 主角的攻击性是否符合目标受众和作品的反英雄/黑爽定位。

不因以下特征自动扣分：主角不吃亏、主角不善良、主角不按学校/组织规则行事、开局快速亮出高等级能力。

## 输出

返回：

- `AssessmentContract`：已冻结的评价目标和适用标准；
- `AssessmentReport`：题材化定性结论、证据、strength/risk/unknown/blocker；
- `NaturalnessReport`：三条分轨的 0–4 锚定分、机器模式风险、coverage、confidence、豁免和逐集/汇总波动；
- `EvaluationReadiness`：是否允许进入 rubric/PanelRun；
- `score_eligibility` 与阻断原因；
- 一个 `next_action`，优先补合同或补证据，不直接要求续写。

## Owner 边界

- Agent/本 Skill：建立合同、选择题材镜头、做定性分析并路由下一步。
- Auctra：保存 source ref、revision、digest、确定性自然度证据、场景/状态门禁、review evidence；不替代题材判断或声称作者来源。
- Ordo：合同冻结后执行盲评、评委扇出、相关性簇、聚合、分歧裁决和 repair proposal；不替代人类接受。
- Scaena：只在剧本被接受后判断分镜/生产可行性；不把生产门禁倒推成故事质量分。

## 验证

需要接入 Auctra 时，先运行其真实的源与格式检查，再决定是否提交评估包：

```bash
auctra corpus audit-screenplay --source-file <script.md> --permission owned --json
auctra corpus screenplay-segment --source-file <script.md> --json
auctra screenplay quality-check --body-file <script.md> --profile screenplay_p0.v2 --require-evidence --json
auctra screenplay quality-check --body-file <script.md> --profile screenplay_p0.v2 --require-evidence --naturalness --json
```

这些命令是 preflight，不是题材评分。`--naturalness` 当前只增加叙述/描写层 v1 投影，不包含对白和结构模板分。只有 AssessmentContract ready 后，才可进入 `ai-drama-critic-panel` 的评分链。

目标中的独立 screenplay naturalness 三分轨 operation 尚未注册；在 Auctra owner change 实现前，不得把它写成当前可运行命令。

详细字段、状态和题材镜头见 [assessment-contract.md](references/assessment-contract.md)。
