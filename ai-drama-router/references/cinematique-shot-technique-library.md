# 镜头技术提示词库（Cinematique）

官方模板 `promptrepo://official/video/cinematique-shot-techniques-beta@1.0.0-beta.1?locale=en`（模板仓 `data/yeisme-prompt-templates`，solutions/video/cinematique-shot-techniques-beta）。150 条电影拍摄技术提示词，来自 vvsvs.pro/cinematique（Free Tool — Open Source；上游 grokfilm.app by Tetsuo Corp）。**何时读本参考**：`director_plan`、`visual_plan`、`generation` 阶段需要为镜头选择运镜/布光/构图/剪辑/叙事/风格语言，或用户点名某电影技法（"希区柯克变焦""伦勃朗光"）时。

## 库结构

- `assets/techniques/<id>.json`：150 条 spec——分类（Camera Work 41 / Lighting 30 / Composition 21 / Genres & Styles 21 / Editing 17 / Storytelling 12 / VFX 8）、难度（Basic/Intermediate/Advanced）、mood、影史摘要、`[Subject]` 占位提示词模板、`when_to_use`、`directing_the_ai`、三条 `common_mistakes`、`related`。
- `assets/index.json`：选型索引（reindex 脚本生成，禁手写）。
- 合同 7 输入：`technique_id`（150 值 enum）、`technique_name`、`subject`、`technique_prompt_bound`、`target`（image|video）、`extra_directives`、`negative_prompts`。

## 选型规则

1. 从叙事意图出发选技术，不是从"这个运镜酷"出发；`when_to_use` 是裁决依据，`common_mistakes` 是排除依据。
2. **一个镜头只绑一条主技术**（`constraint:single_technique_per_shot`）。要叠加的第二条技术拆到下一镜头。
3. Advanced 技术（vertigo-effect、one-er、long-take 等）对模型执行力要求高；弱模型降级同意图的 Basic/Intermediate 技术。
4. Editing/Storytelling 类（smash-cut、flashback、montage 等）是时间结构与转场语言，服务剪辑计划与镜头编排，不是单镜画面描述；跨镜使用时写进分镜节拍而非单镜 prompt。

## 绑定规则

1. 取 spec `prompt_template`，把 `[Subject]` 替换为具体可拍主体（谁、在哪、做什么）。
2. 除替换外逐字保留——镜头、胶片、灯光语言就是技术本身；顺手润色=改写技术。
3. `target=video` 保留技术运动语言一次且一致；`target=image` 丢弃纯运动语言。
4. 与 `ai-drama-shot-video-generation` 组合时，`technique_prompt_bound` 进该模板的 `camera_spec`/镜头段；与分镜拆解组合时，技术 id + 选型理由（引 `when_to_use`）写进分镜的 camera/lighting 字段。

## 消费与验证

```bash
scaena prompt-asset repository sync
scaena prompt-asset catalog inspect 'promptrepo://official/video/cinematique-shot-techniques-beta@1.0.0-beta.1?locale=en' --json
```

渲染验收对照 review-checklist（同 solution docs）；投递前逐条核 spec `common_mistakes`。

## 扩展与维护

- 加技术：新增 spec（`prompt_template` 必含 `[Subject]`）→ `python3 scripts/cinematique_reindex.py` → 用其输出的 enum 清单重放 `contract input set --name technique_id` → contract refresh + catalog build/validate + repository sync。
- 上游库升级（站方 v0.2+）：同 schema 并入；结构不同另立 solution。
- rights `external-attributed`：再导出技术内容必须保留 spec `source` 署名块；对外商用前确认站方条款。
- beta 转正条件：一次真实剧集「分镜选型→绑定→出图/出片→人审」回执。
