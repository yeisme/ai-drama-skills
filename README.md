# AI Drama Skills

面向短剧、漫剧、美剧、电影、单元剧、音频剧等形态的开源 AI 做剧 Skills 矩阵。

`ai-drama-router` 是唯一入口。它先识别剧型、类型、阶段、当前 artifact 与最小上下文包，再选择一个 primary Skill 和最多一个兼容约束 Skill。专项 Skills 默认按需加载，不要求一次性安装或激活全部能力。

## 能力分组

- 项目启动：`manga-drama-project-starter`（默认英文、显式中文、Auctra + Scaena lazy workspace）
- 路由与策略：`ai-drama-router`、`ai-drama-format-strategist`、`ai-drama-context-pack-builder`
- 故事与人物：`ai-drama-story-architecture`、`ai-drama-character-engine`、`ai-drama-showrunner`
- 场景与导演：`screenplay-scene-writer`、`ai-drama-director`、`ai-drama-video-reference-director`
- 视觉与声音：`ai-drama-visual-language`、`ai-drama-edit-and-sound`
- 评审与生产：`ai-drama-assessment`、`ai-drama-critic-panel`、`ai-drama-continuity-supervisor`、`ai-drama-producer`、`ai-drama-production-orchestrator`
- Owner 交接：`auctra-ai-drama-panel-handoff`

`ai-drama-assessment` 同时承载“AI味”请求的诚实边界：只评对白活人感、叙述/动作自然度和结构模板风险，输出带 coverage/confidence 的 0–4 行为锚点；不推断作者来源，不主动贴媒介/平台标签，也不生成未经校准的综合分。

## Seedance 2.5 能力参考

涉及 storyboard、reference、keyframe、video generation、原生音频或 assembly
时，先按需读取唯一事实参考包：

- `ai-drama-router/references/seedance-2-5-capability-profile.md`

该参考包只记录官方能力与 provider-neutral 路由约束。它覆盖
`doubao-seedance-2-5-260628` 的 text/reference/frames/edit/extend、图片/视频/音频
引用、4–30 秒与 `-1`、ratio、480p/720p/1080p、mp4/mov、时间戳和音频策略；不安装
或依赖 `sd25-pe`，不把能力声明、fixture 或 provider-smoke 误标为
`production_ready`。Scaena 的运行时映射与当前实现边界见其 Owner 文档。

矩阵一致性规则：

| Stage | Seedance 2.5 只增加的约束 |
| --- | --- |
| `director_plan` | 先冻结 `ShotIntent` + `ShotAudioIntent`；标注 task intent、引用用途和时间窗 |
| `visual_plan` / `reference_video` | 绑定 ordinal、media role、camera/motion/geometry 语义和 source digest |
| `generation` | 先校验 task lock、引用计数、ratio/duration、output/audio policy、rights、cost、stale |
| `evaluation` / `assembly` | 异步成功不等于接受；原生音频独立审听，默认 `replace_after_generation` |
| `cross_owner_run` | 每阶段仍一个 primary、最多一个 constraint；能力 full contract 不等于一次加载全部 Skills |

## 纯原创成片流水线

完整链路由 `ai-drama-production-orchestrator` 编排：

```text
OriginalityDecision
→ Auctra 原创 premise / 人物 / proof slice / accepted screenplay
→ Scaena typed handoff / 分镜拆解 / 用户方向确认
→ 主体依赖波次 / Eikona 抽卡 / human select + freeze
→ 逐镜音画候选 / 连续性与独立音频评审 / production acceptance
→ episode preview / edit timeline variants / cut selection
→ 按缺陷 owner 进行有界精修
→ delivery review / checksummed export package
```

执行矩阵、真实命令、恢复语义和完成条件见 `ai-drama-production-orchestrator/references/original-manga-drama-production-loop.md`。运行前必须读取 `scaena workflow list --agent`；未注册的整集 goal 不能被文档或 Agent 伪装成已实现的一键能力。

## 云端集成

最短安装只需要 Router：

```bash
npx --yes skills add https://github.com/yeisme/ai-drama-skills \
  --skill ai-drama-router \
  --yes
```

可直接把下面这段交给任意开发 Agent：

```text
请从 https://github.com/yeisme/ai-drama-skills 为当前项目集成 AI 做剧 Skills。

先运行：
npx --yes skills add https://github.com/yeisme/ai-drama-skills --skill ai-drama-router --yes

先只安装并读取 ai-drama-router，不要批量安装全部 Skills。根据我要制作的剧型、当前阶段、已有素材和目标产物，选择一个 primary Skill，最多附加一个必要 constraint；需要追加时继续从同一个 URL 按名称安装。快速 demo 走最短可运行路径，正式项目或 MVP 再进入完整但渐进的制作流程；我说不用完整工作流时，只保留当前任务需要的 Skills。完成后报告仓库 URL、安装路径、已启用 Skills、DramaRoutePlan、未启用项、验证结果和下一步。
```

查看仓库提供的全部 Skills：

```bash
npx --yes skills add https://github.com/yeisme/ai-drama-skills --list
```

## 本地验证

```bash
git clone https://github.com/yeisme/ai-drama-skills.git
cd ai-drama-skills
python3 scripts/validate_skills.py
python3 ai-drama-router/scripts/validate_drama_matrix.py
```

宿主负责 catalog、activation、权限和 canonical state；本仓库不绑定某个 profile 脚本或产品数据库。

## 上游视频生产参考

`ai-drama-router/references/upstream-video-production-patterns.md` 固定记录 MoneyPrinterTurbo、video-shotcraft、AI-Youtube-Shorts-Generator、Remotion Skills、FireRed-OpenStoryline、jianying-editor-skill、claude-code-video-toolkit 与 rnskill 的参考 commit、许可证立场、采用模式和禁止边界。

这些项目只在请求命中对应视频场景时按需提供 pattern evidence。Router 不在生产 stage 中联网更新，不整包导入上游运行时，也不让外部项目替代宿主的 canonical owner。更新时先审查 commit diff 和许可证，再为新 route plan 更换固定 snapshot；旧 plan 永远保留旧 lineage。

## 目录约定

每个 Skill 只维护执行所需内容：

```text
<skill-name>/
├── SKILL.md
├── agents/openai.yaml
├── references/        # 可选，按需读取
├── scripts/           # 可选，确定性校验
└── assets/            # 可选，输出资源
```

项目级说明放在本 README、`docs/`、`AGENTS.md` 和 `CLAUDE.md` 中，不在每个 Skill 内复制安装文档。

## 边界

- Skills 输出计划、候选、评估、证据与 typed handoff，不保存第二套剧本或生产数据库。
- 不在 Skill 中记录凭据、原始 provider payload、隐藏系统提示或完整推理过程。
- 具体产品名称只用于可选交接 Skill；`ai-drama-router` 本身保持宿主无关。
- 生产接受、资产冻结、发布和外部调用必须由宿主 Owner 与用户权限门控制。

## License

[MIT](LICENSE)
