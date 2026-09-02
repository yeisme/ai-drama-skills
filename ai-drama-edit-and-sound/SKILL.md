---
name: ai-drama-edit-and-sound
description: Use when planning AI drama shot order, information release, attention rhythm, pauses, music, ambience, Foley, dialogue, subtitles, timing, or episode assembly review.
---

# AI Drama Edit And Sound

## 目标

把镜头、声音和字幕组织成观众可理解的时间体验。剪辑不是拼接文件，而是控制信息、注意力和情绪回收。

## 工作流

1. 读取 Episode/Scene/Shot refs、DirectorDecisionGraph、`ShotAudioIntent`、dialogue、duration、provider audio policy、capability maturity 和 subtitle constraints；字段合同见 `../ai-drama-router/references/shot-audio-intent-contract.md`，视频模型能力/输出事实见 `../ai-drama-router/references/video-model-capability-index.md` 和命中的独立档案。
2. 标注每个镜头的进入信息、退出问题、情绪强度、节奏和可删性。
3. 设计 cut order、transition、pause、ambience、Foley、music cue、dialogue、silence window 和 subtitle timing，并把 required cue 编译成 Sonora audio refs/mix requirements。
4. 若视频包含 provider 原生音轨，先按 `none | external_assets | video_native | replace_after_generation` 分类。默认使用 `replace_after_generation`，并把原生音轨登记为 `video_native_audio` + `pending_review`；只有独立 evidence 齐全时才提升为 `video_native`，不得静默进入最终 mix。
5. 检查画面动作、声像方向、对白/口型、字幕、裁切点、尾音和总时长同步；视频裁短后必须重新检查音频尾段，不能只看容器时长。
6. 输出 `AssemblyProposal`、`SoundPlan`、native-audio review decision 或 finding，交给 Sonora audio owner 和 Scaena assembly/review owner。

## 质量门槛

- 删除一个镜头或声音后必须能说明损失；
- 声音不能只做装饰，至少承担空间、信息、情绪或转场功能；
- `video_native` 只有在 rights、sync confidence、角色声音、可编辑性和人工审听全部通过后才可进入成片；原生对白镜必须逐句验收：台词文本与剧本一致、角色音色跨镜一致、口型与可懂度达标；任一句失败只回退该句到 Sonora 补配，整镜证据不足时才整镜改为 `replace_after_generation` 或阻塞；
- 视觉 candidate pass 不得自动带过音频；原生音轨和最终 mix 必须有独立 review 状态；
- 纯音频 reference、多语言原生音频或 MOV 容器只属于输入/输出能力；不能从这些事实推断对白准确、声线稳定、最终混音可编辑或交付通过；
- 字幕不能遮挡关键主体，时间线必须可复算；
- 音画冲突、未授权素材、时长超限和空白段落必须阻塞或进入 Review。

## 边界与验证

不拥有音频 bytes、不直接导出最终平台包、不上传、不发布；Sonora 拥有音频资产/策略/mix refs，assembly 和 delivery 由 Scaena 管理。

```bash
python3 scripts/validate_skills.py
```

涉及 Scaena assembly、delivery 或 production acceptance 时，进入 Scaena Owner 仓库运行其公开的 focused integration checks。
