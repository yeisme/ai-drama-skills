# AI Drama Skills

面向短剧、漫剧、美剧、电影、单元剧、音频剧等形态的开源 AI 做剧 Skills 矩阵。

`ai-drama-router` 是唯一入口。它先识别剧型、类型、阶段、当前 artifact 与最小上下文包，再选择一个 primary Skill 和最多一个兼容约束 Skill。专项 Skills 默认按需加载，不要求一次性安装或激活全部能力。

## 能力分组

- 路由与策略：`ai-drama-router`、`ai-drama-format-strategist`、`ai-drama-context-pack-builder`
- 故事与人物：`ai-drama-story-architecture`、`ai-drama-character-engine`、`ai-drama-showrunner`
- 场景与导演：`screenplay-scene-writer`、`ai-drama-director`、`ai-drama-video-reference-director`
- 视觉与声音：`ai-drama-visual-language`、`ai-drama-edit-and-sound`
- 评审与生产：`ai-drama-critic-panel`、`ai-drama-continuity-supervisor`、`ai-drama-producer`、`ai-drama-production-orchestrator`
- Owner 交接：`auctra-ai-drama-panel-handoff`

## 使用

```bash
git clone https://github.com/yeisme/ai-drama-skills.git
cd ai-drama-skills
python3 scripts/validate_skills.py
python3 ai-drama-router/scripts/validate_drama_matrix.py
```

把需要的 Skill 目录安装到宿主支持的 Skills source 或 runtime 中。宿主负责 catalog、activation、权限和 canonical state；本仓库不绑定某个 profile 脚本或产品数据库。

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
