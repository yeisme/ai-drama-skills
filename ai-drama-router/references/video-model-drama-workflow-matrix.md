# 视频模型做剧工作流矩阵

矩阵只表达所需 artifact、能力和门禁。模型家族先按硬约束过滤；多个家族满足时不得用社区
热度破平局。

| scenario id | 做剧任务 | required artifact | required capabilities | gate / evidence | fallback |
| --- | --- | --- | --- | --- | --- |
| `short_dialogue_shot` | 短对白镜 | accepted screenplay、ShotIntent、ShotAudioIntent | 4–15 秒、可声明声音策略 | dialogue/voice rights、lip-sync、独立 audio review | `replace_after_generation` + Sonora 补配 |
| `action_camera_reference` | 动作/相机参考 | reference-video analysis、motion/camera digest | video reference、ordinal preservation | rights、总时长、camera/motion semantic review | H3/Seedance/Wan eligible；否则重做 reference brief |
| `first_last_frames` | 首尾帧 | first/last visual refs | frames task policy、ratio lock | frame count、画幅一致、continuity review | 单首帧或普通 reference route |
| `keyframe_storyboard` | 关键帧分镜 | keyframe plan、panel refs | multi-image/keyframe reference | panel ordinal、主体/构图一致性 | 分镜拆镜或 first/last route |
| `video_edit_extend` | 视频 edit/extend | source video revision/digest、edit intent | edit/extend、source lock | ratio/duration lock、source rights、typed task policy | 重生成 successor，不静默改普通 create |
| `long_take_20_30s` | 20–30 秒长镜 | accepted long-take ShotIntent | 20–30 秒、1080P 可选 | 节奏/连续性/预算/质量验证 | 拆为多个 4–15 秒镜头后 assembly |
| `h3_2k_refinement` | 2K 精修 | selected 768P task、原输入 digest、base video | staged 768P→2K regeneration | lineage 完整、输入未漂移 | 保留 768P accepted candidate |
| `native_audio_candidate` | 原生音频候选 | ShotAudioIntent、voice/rights refs | native/prompt/reference audio | 逐句、声线、同步、可编辑性、人工审听 | `replace_after_generation` |
| `post_replace_audio` | 后置替换 | muted/replaceable picture lock、Sonora mix refs | audio disable 或可替换原生轨 | picture lock、sync points、final mix review | 阻断 delivery，不接受未审音轨 |

每个 scenario 仍由现有 Router stage 选择一个 primary Skill 和最多一个 constraint Skill；模型
档案与工作流矩阵只是 generation guidance，不占用额外 Skill 槽位。
