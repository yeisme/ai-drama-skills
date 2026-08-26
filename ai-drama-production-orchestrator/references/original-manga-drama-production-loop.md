# 纯原创漫剧端到端生产循环

## 结果

把“一个原创想法”推进为“可验证、可恢复、可精修、可导出的成片包”，同时保持：

- Auctra 是故事、人物和剧本 canon owner；
- Scaena 是 ProductionGraph、分镜接受、主体资格、镜头候选、装配、交付与导出 owner；
- Eikona 是图片/视觉 artifact 生成 owner，默认模型固定为 `openai/gpt-5.4-image-2`；
- Sonora 是独立音频 artifact 与 mix owner；
- Ordo 只编排并行候选、评委和 evidence，不成为业务 canon；
- 每个自动步骤都能停在 gate、保存 receipt、从失败点恢复，并把缺陷路由回真正 owner。

本流程描述可执行的细粒度命令组合，不假装当前已经存在一个万能命令。

## 先检查当前能力

每次运行先读取本地真实命令面：

```bash
auctra --help
scaena --help
scaena workflow list --agent
scaena asset draw --help
```

只有 `scaena workflow list --agent` 明确列出的 goal 才能通过 `workflow run` 调用。若未列出 `shortdrama.episode-production`，返回 `workflow_goal_unavailable`，继续使用本文的阶段命令，不得伪造“一键整集”成功。

## 17 阶段能力账本

| # | 阶段 | Primary / Owner | 输入 → 输出 | Gate | 当前成熟度 |
| --- | --- | --- | --- | --- | --- |
| 1 | 路由与剧型 | Router | 用户目标 → `DramaRoutePlan` | format、scope | current |
| 2 | 原创性决策 | Router | source/rights refs → `OriginalityDecision` | rights、similarity | current Skill contract |
| 3 | 项目初始化 | Auctra + Scaena | route plan → 两侧 local workspace | 路径、locale、profile | current |
| 4 | 原创故事引擎 | Auctra | premise → story architecture / character canon | owner review | current |
| 5 | proof slice | Auctra | series intent → 3 集核心场景 A/B 候选 | voice selection | current |
| 6 | 剧本 canon | Auctra | selected candidate → accepted screenplay revision | screenplay acceptance | current |
| 7 | 生产交接 | Auctra → Scaena | accepted revision → handoff receipt | digest / stale | current |
| 8 | 分镜拆解 | Scaena | screenplay handoff → breakdown candidate | source mapping | current |
| 9 | 分镜方向确认 | Scaena + human | story spine / beats / dialogue / visual / duration → accepted breakdown | 当前用户确认 | current |
| 10 | 主体清单与依赖波次 | Scaena | accepted breakdown → asset slots / briefs / waves | readiness | current |
| 11 | 抽卡、选卡、冻结 | Scaena + Eikona + human | brief → DrawSession → selected/frozen subject version | paid call、human-only select/freeze | current |
| 12 | 逐镜计划与生成 | Scaena + Eikona/video provider | shot intent + frozen subjects → shot candidates | cost、duration、audio policy | current bounded commands |
| 13 | 音画评审与生产接受 | Scaena + Sonora + critic | candidates → selected / consistency / audio / production accepted | independent audio review | current |
| 14 | 整集拼接与剪辑 | Scaena | accepted segments → preview / edit plan / timelines / cuts | cut selection | current |
| 15 | 缺陷分类与精修 | owning domain | defect → successor candidate / new cut / repair receipt | bounded repair | partial；`enhance run` v1 为 fixture-only |
| 16 | 交付审查 | Scaena | selected cut + provenance → delivery-ready graph | rights、continuity、cost | current |
| 17 | 成片包导出 | Scaena | delivery-ready graph → checksummed export package | explicit confirm | current |

“全自动整集 goal、真实 provider enhancement、所有异常无人值守恢复”仍是 target，不得在文档或运行回执中标为 current。

## 阶段 A：纯原创 Auctra canon

### 初始化 screenplay 项目

```bash
auctra project init <project-path> \
  --title "<title>" \
  --template screenplay \
  --locale zh-CN \
  --json
```

把 `originality_mode=pure_original`、`originality_decision_ref`、类型/剧型合同和禁用参考写入 Auctra 可接受的项目/brief 流程。不要手写 Auctra 的结构化状态文件。

### proof slice 与场景候选

新写或大幅重写超过 5 集时，先创建 3 个代表集的核心场景；每个场景产生 A/B 策略候选：

```bash
auctra scratch create \
  --kind screenplay_scene \
  --title "第1集核心场" \
  --ttl 24h \
  --json

auctra scratch candidate add <scratch-ref> \
  --candidate candidate:a \
  --body-file <candidate-a.md> \
  --json

auctra scratch validate <scratch-ref> \
  --candidate candidate:a \
  --profile screenplay_p0.v2 \
  --require-evidence \
  --json

auctra scratch present <scratch-ref> --candidate candidate:a --json
auctra scratch select <scratch-ref> --candidate candidate:a --json
```

用户选择人物声音后才 promote；选择不等于 canonical acceptance：

```bash
auctra scratch promote <scratch-ref> \
  --candidate candidate:a \
  --project <project-path> \
  --unit <screenplay-unit-id> \
  --json

auctra review accept <review-item-id> \
  --path <project-path> \
  --json
```

故事结构、人物、对白或场景因果需要精修时，回到新的 scratch/rewrite candidate 和 review；不得直接改写已接受 revision。

## 阶段 B：Auctra → Scaena typed handoff

```bash
auctra production handoff inspect \
  --path <project-path> \
  --target scaena \
  --json

auctra production handoff export \
  --path <project-path> \
  --target scaena \
  --to <handoff.json> \
  --json

scaena handoff auctra inspect \
  --project <project-path> \
  --from <handoff.json> \
  --json

scaena handoff auctra import \
  --project <project-path> \
  --from <handoff.json> \
  --confirm \
  --json
```

handoff 必须携带 revision/digest、accepted screenplay refs、originality decision ref 和 source mapping。任何 digest 漂移返回 stale，不能静默导入旧稿。

## 阶段 C：分镜拆解与方向门禁

使用 Scaena 的真实命令面完成：

```bash
scaena storyboard source import --help
scaena storyboard breakdown run --help
scaena storyboard breakdown show --help
scaena storyboard breakdown revise --help
scaena storyboard breakdown patch --help
scaena storyboard breakdown accept --help
scaena storyboard breakdown export --help
```

Agent 必须先呈现用户可以直接判断的五项内容：

1. 故事脊柱与本集状态变化；
2. 逐镜节拍、入点和出点；
3. 对白主干与 `ShotAudioIntent`；
4. 视觉基调、主体连续性和禁用风格身份；
5. 每镜与整集时长合同。

未获得当前用户确认前，不得进入任何付费图片、视频或配音生成。结构/语义/source mapping 缺陷用 `breakdown revise`；允许的局部字段修复用 typed `breakdown patch`；只有 accepted breakdown 可进入主体抽卡。

## 阶段 D：主体抽卡与冻结

### 依赖波次

- Wave 1：主角 identity、核心 style；
- Wave 2：三视图、表情、姿态等 derived views；
- Wave 3：场景、道具、服装；
- 后续波次必须通过 `--requires` 引用已冻结的上游 slot。

每个 slot 同时只能有一个 active DrawSession，默认最多记录 5 个候选。第 6 个候选触发 exhausted；先修 brief，再新建 session。

### 真实 DrawSession 命令

```bash
scaena asset draw plan \
  --project <project-path> \
  --asset <asset-ref> \
  --brief <brief-ref> \
  --wave 1 \
  --json

scaena asset draw start \
  --project <project-path> \
  --asset <asset-ref> \
  --session <draw-session-ref> \
  --json
```

Eikona 生成视觉候选时使用 canonical 模型：

```bash
eikona generate <visual-brief> \
  --model openai/gpt-5.4-image-2 \
  --json
```

把 Eikona receipt 和 digest 登记回 Scaena；`record` 不代替 provider call：

```bash
scaena asset draw record \
  --project <project-path> \
  --asset <asset-ref> \
  --session <draw-session-ref> \
  --eikona-run <eikona-run-ref> \
  --digest sha256:<64-hex> \
  --json

scaena asset draw select \
  --project <project-path> \
  --asset <asset-ref> \
  --candidate <candidate-ref> \
  --action accept \
  --actor <human-actor-ref> \
  --reason "<reason>" \
  --json

scaena asset draw freeze \
  --project <project-path> \
  --asset <asset-ref> \
  --confirm \
  --json

scaena asset draw status --project <project-path> --asset <asset-ref> --agent
scaena asset draw path --project <project-path> --asset <asset-ref> --seq <n> --agent
```

select 和 freeze 必须由 human actor 完成。`selected`/`frozen` 只证明主体版本稳定，不等于 production-admitted、shot-accepted 或 export-ready。候选文件路径由 Scaena 分配，Agent 不手建 `assets/.../draws/...`。

## 阶段 E：逐镜生成与接受

每个镜头必须固定：

- screenplay/shot intent revision；
- frozen SubjectVersion refs；
- StyleLens 与 originality decision refs；
- duration、frame/aspect、movement、camera、negative constraints；
- `ShotAudioIntent`、provider audio capability 和 replacement policy；
- cost/retry budget、idempotency key 和 review gates。

生成后状态只能按顺序推进：

```text
generated
→ assessed_visual + assessed_audio
→ recommended
→ human_review
→ selected
→ consistency_review
→ audio_review
→ production_accepted
```

provider success、审美高分、主体冻结或视觉 pass 都不能跳过独立音频 review 和 production acceptance。

## 阶段 F：自动拼接、剪辑和选版

先生成可核对的整集预览：

```bash
scaena video episode-preview \
  --project <project-path> \
  --episode <episode-ref> \
  --segment-asset <asset-1> \
  --segment-duration-ms <ms-1> \
  --segment-asset <asset-2> \
  --segment-duration-ms <ms-2> \
  --output previews/<episode>.mp4 \
  --confirm \
  --json
```

再生成至少一个 edit plan 和有界 timeline variants：

```bash
scaena edit plan \
  --project <project-path> \
  --graph <workflow-graph-ref> \
  --platform douyin \
  --target-duration 75 \
  --json

scaena edit timeline \
  --project <project-path> \
  --plan <edit-plan-ref> \
  --variant fast-hook \
  --json

scaena edit render \
  --project <project-path> \
  --timeline <timeline-ref> \
  --profile preview \
  --output previews/<episode>-cut.mp4 \
  --confirm \
  --json

scaena edit score --project <project-path> --cut <cut-ref> --json
scaena edit select --project <project-path> --cut <cut-ref> --json
```

自动评分只产生 recommendation。最终 cut selection、字幕/音轨接受和 production acceptance 仍走显式 gate。

## 阶段 G：精修缺陷路由

精修不是对最终文件反复覆盖。先分类，再回 owner 产生 successor：

| 缺陷 | Owner | 正确修复 |
| --- | --- | --- |
| 人物动机、因果、对白、钩子 | Auctra | 新 scratch/rewrite candidate → review → accepted revision → stale 下游重建 |
| 分镜结构、语义、source mapping | Scaena storyboard | `revise` |
| 允许的镜头字段、时长、映射 | Scaena storyboard | typed `patch` |
| 人脸、服装、画风、场景身份漂移 | Scaena asset + Eikona | 新 derived/draw candidate → human select/freeze |
| 单镜动作、镜头或画面失败 | Scaena generation | 只重生成受影响 shot |
| 原生音频、对白、Foley、mix 失败 | Sonora/audio owner | replacement audio/mix revision → independent review |
| 节奏、字幕、转场、混音平衡 | Scaena edit | 新 timeline/cut → score → select |
| 分辨率、去噪、插帧、画面增强 | Scaena enhance | 只对 selected candidate 创建 successor；当前 v1 `enhance run` 为 fixture-only |
| codec、checksum、manifest、package | Scaena delivery/export | technical repair，不重写故事 |

同一失败最多执行一个有界 repair loop；仍失败时返回 typed blocker、保留 evidence，并由用户或 Owner 决定是否扩大成本/范围。不得无限 reroll。

## 阶段 H：交付与成片导出

导出前验证：

- screenplay、breakdown、SubjectVersion、shot、audio mix 和 edit cut refs 都未 stale；
- continuity、rights/originality、watermark/logo、cost 和 delivery review 通过；
- selected cut 已 production accepted；
- manifest、codec、duration、checksum 和 provenance 完整；
- export/publish 是单独授权，不能从前序 `--confirm` 推断。

`export package` 不带 `--confirm` 时用于 draft 计划/预检，当前命令不支持 `--dry-run`。根据 command help，draft `--to` 会写 manifest；它是 CLI 管理的本地结构化写入，不是零写入预览：

```bash
scaena export package \
  --project <project-path> \
  --profile douyin \
  --to <output-path> \
  --json

scaena export package \
  --project <project-path> \
  --profile douyin \
  --to <output-path> \
  --confirm \
  --json
```

导出完成只表示成片包已生成，不自动发布到平台。

## 自动化恢复合同

每个 stage 保存：

```text
stage_kind
owner
input_refs[]
input_digests[]
output_refs[]
receipt_ref
evidence_refs[]
attempt
cost
status
blocker?
next_action
```

- transient failure：相同幂等键最多重试既定次数；
- deterministic quality failure：进入一次 owner-specific repair；
- stale：只失效未开始或依赖已变更输入的后代；
- unknown accept：查询 owner receipt，不重复提交；
- pause/resume：保留 pinned Skill、model、context 和 provider lineage；
- external side effect：在 provider charge、freeze、production accept、export 和 publish 前重新检查授权。

## 完成定义

只有以下全部成立才返回 `complete`：

1. Auctra screenplay revision 已 accepted；
2. Scaena breakdown 已 accepted，且付费生成前存在用户分镜方向确认；
3. 必需主体已 human-selected 并 frozen；
4. 每个使用中的镜头已完成 visual、audio、continuity 和 production acceptance；
5. 选定 edit cut 已通过 delivery review；
6. originality/rights/provenance 没有 blocker；
7. export package 有 receipt、manifest、checksum 和 evidence refs；
8. 用户要求的实际文件已导出；若用户还要求发布，则另有明确发布授权和 receipt。
