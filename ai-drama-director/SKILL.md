---
name: ai-drama-director
description: Use when converting story emotion and character action into blocking, performance direction, space, camera intent, visual rhythm, sound intent, and shot-level directing decisions for an AI drama.
---

# AI Drama Director

## 核心判断

先回答“观众此刻应该理解/感受什么”，再决定人物行动、空间权力、调度、镜头、声音和节奏。不要用“电影感”“高级”“史诗感”替代可执行决策。

## 工作流

1. 从 beat/scene 提取 audience objective、character objective 和 subtext。
2. 设计 blocking：人物位置、视线、行动路线、阻碍、前中后景和空间权力。
3. 选择景别、角度、镜头运动、剪辑点和声音进入点，并写明叙事理由。
4. 为演员/虚拟角色提供行动指令、潜台词、节奏和状态变化。
5. 为每个镜头冻结 `ShotAudioIntent`：逐 cue 标注 ambience、Foley、dialogue、music、motif、silence 的时间窗、空间方向、同步点、lip-sync、provider audio policy、Sonora final mix owner 和验收条件。完整字段读取 `../ai-drama-router/references/shot-audio-intent-contract.md`。
6. 使用 H3、Wan、Seedance、Kling V3 / Omni 或混合参考视频时，读取 `../ai-drama-router/references/video-model-capability-index.md` 和命中的独立档案，冻结 provider-neutral task intent、引用用途/ordinal、ratio/duration policy、workflow profile 和 capability maturity。不要把 provider wire mode 写进导演 canonical artifact；adapter 从中立 policy 推导。
7. 原生对白默认采用 `replace_after_generation`。只有 capability 达到已验证线路、逐句台词/说话人/声线/情绪可控，并且 rights、lip-sync、可编辑性与人工声音验收都有证据时，才把该镜 policy 提升为 `video_native`；视觉通过不能替代声音通过。
8. 输出 `DirectorDecisionGraph`、`ShotIntent`、`ShotAudioIntent` 或 repair proposal，交给视觉/声音/剪辑 owner。

## 质量门槛

- 每个镜头都必须有不可替代的叙事、情绪或关系功能；
- 镜头选择必须能解释观众注意力和信息释放；
- 空间连续性和动作方向不能靠后期猜测；
- 声音不能只写“雨声、音乐、心跳”等标签；每个 required cue 必须有时间、来源、叙事功能和音画同步条件，静音也必须显式设计；
- 视频模型可能生成原生音频时，缺逐镜 `ShotAudioIntent` 必须阻塞 generation；视觉通过不能代替声音通过；
- 分镜/导演方向未获当前用户显式确认前，不得进入任何付费生成（出图、视频、配音）；确认内容至少包括故事脊柱、逐镜节拍、对白主干与时长合同；
- 风格只作为约束，不覆盖人物动机、可读性和连续性；
- 参考导演时只提炼高层原则，不复制具体作品表达。

## 边界与验证

不直接调用 provider、不冻结主体、不接受资产。Director 决定声音叙事意图但不拥有音频资产；音频资产与 mix refs 交给 Sonora，视觉执行交给 Eikona，生产接受与时间线交给 Scaena：

```bash
python3 scripts/validate_skills.py
python3 ai-drama-router/scripts/validate_drama_matrix.py
```
