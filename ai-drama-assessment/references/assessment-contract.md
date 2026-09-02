# AssessmentContract 与题材化评估

## 1. 合同状态

```text
missing -> drafted -> ready_for_assessment -> ready_for_scoring
                                      \-> needs_human_review
```

- `missing`：缺少评价目标，禁止综合评分。
- `drafted`：Agent 已提出字段，但尚未由用户或 owner 确认。
- `ready_for_assessment`：可以做题材化定性评估。
- `ready_for_scoring`：候选集、rubric、hard gates 和证据策略均已冻结。
- `needs_human_review`：题材承诺冲突、目标受众冲突、权利未知或证据不足。

## 2. 最小字段

```text
AssessmentContractV1 {
  subject_ref
  candidate_digest
  source_revision
  medium                  # screenplay | manga_drama | audio_drama | unspecified
  format_profile          # user-declared profile or unspecified; never inferred from text
  genre_lens              # male_power_fantasy | romance | mystery | ...
  audience
  platform?
  duration?
  episode_scope
  audience_promise
  creator_intent
  evaluation_intent[]     # hook | retention | genre_fit | craft | continuity | production
  anti_goals[]
  comparison_class
  rubric_profile?
  hard_gate_profile
  evidence_policy
  unknowns[]
  rights_state
  canonical_owner
  score_eligibility
  naturalness_profile?    # screenplay_naturalness_v2
  naturalness_lanes[]     # dialogue_liveability | narrative_naturalness | structural_formula_risk
  voice_profile_ref?
  calibration_set_ref?
  style_exemptions[]
  naturalness_score_policy
}
```

`evaluation_intent` 可以有多个，但必须声明主目标。没有主目标时，只允许返回多维定性观察，不允许合成单一总分。

## 3. AI味不是作者来源检测

本合同把用户口中的“AI味”拆成两个可观察但不等价的结果：

| 结果 | 分数方向 | 含义 | 不代表什么 |
| --- | --- | --- | --- |
| `naturalness_score` | 0–4，高为好 | 人物、场景、声音和节奏是否像在具体语境中自然运作 | 不代表一定由人写作 |
| `pattern_risk` | 0–4，高为坏 | 是否出现可定位的模板化、机器式密度或结构重复 | 不代表 AI 来源概率 |

系统不得输出“AI生成概率”、作者归因或检测规避结论。`clean` 只表示没有触发当前 profile 的已配置模式，不能写成“确定是人写”。

## 4. 三条自然度分轨

screenplay v2 使用三条独立 lane，不能把不同来源的 finding 直接混成一分：

| Lane | Owner / 输入 | 重点检查 | 典型证据 |
| --- | --- | --- | --- |
| `dialogue_liveability` | `dialogue-live-test` + Agent | 目标、知识边界、策略变化、可表演性、人物声音差异 | 人物/台词 span、关系和动作 refs |
| `narrative_naturalness` | Auctra `screenplay_naturalness_v1` + naturalness Skill | 句式壳、节奏、空洞评价、解释腔、描写密度 | `VN-R1…R10`、rune span、report digest |
| `structural_formula_risk` | `ai-drama-assessment` + Auctra block/scene refs | 爽点/反转/集尾模板是否连续复用、胜利是否改变状态 | episode/scene refs、重复 beat refs、状态转移 refs |

`screenplay_naturalness_v1` 继续只做叙述/描写层的兼容 preflight；v2 的三 lane 报告走独立评估入口，不改变现有 `quality-check --naturalness` 的含义。

### 类型化表达保护

短句、夸张金句、系统播报、等级宣告、网络口语和快速亮牌，只有在与项目声音合同冲突或形成无功能重复时才进入风险。允许模式写入 `voice_profile_ref`，局部例外使用带 source span 的 `exemption_ref`；豁免不能删除原始 finding，只能影响风险聚合。

## 5. 0–4 行为锚点

每条 lane 都使用同一组可解释锚点，但必须结合 lane 的观察问题：

- `0`：交付残留、占位符、助手话术或严重不可表演/不可理解；只有明确交付红线才可阻断；
- `1`：问题普遍存在，人物/场景替换后仍基本成立，机器式模板主导体验；
- `2`：自然与模板混合，有可定位且需要定向修复的问题；
- `3`：基本自然，偶有解释腔或重复，不影响主要观看目标；
- `4`：人物目标、知识、策略、节奏和声音有持续、可复核的自然证据。

`pattern_risk` 使用同样的锚点但方向相反：`0` 表示未观察到显著风险，`4` 表示风险普遍且影响观看/交付。UI 必须同时显示分数方向，不能只展示一个“AI味 4”。

## 6. 证据、校准与汇总

可比较的自然度分必须绑定三层证据：

1. Auctra 的确定性指标和 source span；
2. Agent/Skill 的上下文诊断与修复目标；
3. 项目声音、已接受人写样本、类型化样本和挑战样本组成的校准集，并经过双人盲标与人工裁决。

任一层缺失时，结果只能是 `unknown` 或低置信度 advisory，不得伪造绝对分。校准集的 0–4 锚点、阈值和豁免由人类最终冻结。

首版按集生成三条 lane 的结果，再对五集使用中位数、范围/IQR、coverage、confidence 和集间波动汇总；不设固定跨项目权重，不生成默认综合总分。项目若确实需要 composite，必须在合同中声明权重、用途和比较类。

自然度默认是建议性门禁。只有助手残留、占位符、严重知识/事实断裂或不可交付内容等明确红线可以阻断；口语、夸张和一般句式重复默认为 advisory。

## 7. 评估层级

| 层级 | 回答什么 | 是否允许数字分 |
| --- | --- | --- |
| L0 Intake | 这是什么、给谁看、希望观众得到什么 | 否 |
| L1 Assessment | 已有文本是否兑现自己的题材承诺 | 可对单维做条件性标记，不合成总分 |
| L2 Craft Evaluation | 在已接受 rubric 下，场景/剧集的具体完成度 | 是，必须绑定 contract/rubric/evidence |
| L3 Candidate Comparison | 同一合同下 A/B/C 哪个更好 | 是，必须同一 CandidateSet |
| L4 Production Readiness | 是否适合当前制作形态、成本和下游交接 | 是，但不是故事质量分 |

L1 的“未发现证据”是 `unknown`，不是 0 分。L3 的胜出也不等于 canonical accept 或 production accept。

## 8. 题材镜头：男频无敌/异能爽剧

建议 `genre_lens=male_power_fantasy` 时观察以下维度。默认不设固定权重，权重必须由目标和平台合同决定。

| 维度 | 观察问题 | 常见误判 |
| --- | --- | --- |
| Promise clarity | 观众是否立即知道主角的核心优势和爽点 | 把“主角很强”误认为故事已经完成 |
| Gratification variety | 胜利是否通过亮牌、规则、智取、反制、资源或关系产生不同快感 | 要求主角必须输一次才算有戏 |
| Opponent credibility | 对手是否有目标、信息、资源和合理误判 | 把反派失败自动当作主角成功证据 |
| Power contract | 明牌、暗牌、等级、能力限制和升级方向是否可追踪 | 只看等级数字，不看使用条件 |
| Agency | 主角是否主动选择目标、策略和出手时机 | 把无敌等同于没有主动性 |
| Consequence | 胜利是否改变资源、关系、身份、责任或下一集目标 | 把“对手震惊”当成完整后果 |
| Hook actionability | 集尾是否迫使下一集采取新行动 | 把单纯新增秘密当成钩子 |
| Audience alignment | 攻击性、羞辱、权力幻想是否符合目标受众 | 用大众伦理偏好覆盖已声明的黑爽合同 |

### 不应自动扣分

- 主角连续赢；
- 主角不承担传统成长型苦难；
- 主角冷酷、毒舌或不服从组织；
- 高概念设定在前两集密集释放；
- 观众明知主角不会死。

### 仍然需要检查

- 赢法是否重复到失去新鲜感；
- 对手是否为了送出爽点而无视已经宣布的规则；
- 主角是否强到让场景目标失去意义；
- 隐藏代价、规则限制或长期任务是否真实存在；
- 每集的爽点是否带来可观察的状态变化。

## 9. 证据与评分

每个 finding 至少绑定 `source_span` 或可复核的 Auctra ref。评分前必须记录：

```text
contract_digest
rubric_digest
candidate_set_digest
evidence_coverage
unknowns[]
hard_gate_state
```

只有 `score_eligibility=eligible` 且 hard gates 通过时，才可按同一 rubric 聚合 0–4 分。聚合使用适用维度的中位数/截尾平均，并报告 IQR、分歧和置信度；不得把未适用维度填成 0，也不得把缺证据填成低分。

## 10. 报告模板

```text
AssessmentReport {
  contract_ref
  subject_ref
  status                 # assessed | needs_contract | needs_human_review
  verdict                # strong_fit | mixed_fit | weak_fit | indeterminate
  promise_summary
  strengths[]
  risks[]
  unknowns[]
  blockers[]
  evidence_refs[]
  naturalness_lanes[]   # lane, naturalness_score, pattern_risk, findings, exemptions
  episode_summaries[]   # per-episode lane results and uncertainty
  aggregate_summary?    # median, IQR, coverage, confidence, variance
  score_eligibility
  next_action
}
```

自然度分轨使用独立报告：

```text
NaturalnessReportV2 {
  contract_ref
  subject_ref
  candidate_digest
  source_revision
  profile_ref
  calibration_digest?
  voice_profile_ref?
  episode_reports[] {
    episode_ref
    lanes[] {
      lane
      status
      naturalness_score?
      pattern_risk?
      coverage
      confidence
      finding_refs[]
      exemption_refs[]
      repair_targets[]
    }
  }
  aggregate_summary
  report_digest
}
```

`verdict` 是题材适配和证据状态的判断，不是市场成功保证。没有真实观众、平台或完播证据时，不得把它写成市场预测。
