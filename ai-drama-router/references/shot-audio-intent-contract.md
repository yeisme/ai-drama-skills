# ShotAudioIntent 音频前置合同

## 为什么必须在分镜阶段冻结

支持原生音频的视频模型会同时决定动作、声音发生点、空间方向、对白节奏和静音窗口。若分镜只描述画面，provider 会自行补全声音；生成成功也无法证明音画同步、角色声音、版权或最终混音可用。因此音频不是 assembly 阶段临时补丁，而是 `director_plan` 的必需输入。

## 最小合同

每个进入视频生成的镜头必须有版本化 `ShotAudioIntent`，至少包含：

```text
schema_version
shot_ref
duration_ms
dialogue_span_refs[]
audio_cue_refs[]              # ambience | foley | dialogue | music | motif | silence
silence_window_refs[]
lip_sync
provider_audio_policy         # none | external_assets | video_native | replace_after_generation
native_audio_prompt_ref
native_audio_prompt_digest
final_mix_owner_ref           # logical audio/mix owner binding
acceptance_gate_refs[]
```

持久化 handoff 只保存 refs、版本、digest、policy 和审查状态，不保存 raw provider prompt、音频字节、signed URL 或 provider payload。内容正文留在 canonical prompt/audio-plan owner。

每个 cue 必须有 `start_ms`、`end_ms`、语义角色、空间/同步要求和 required 标记。对白 cue 必须绑定 accepted dialogue span；需要口型时必须显式 `lip_sync=true`。静音也是 cue，不能靠“没有声音描述”推断。

## Provider capability snapshot

Producer 在 generation admission 前必须冻结 provider-neutral 音频能力：

```text
native_audio              supported | unsupported | unknown
audio_prompt_control      structured | inline_prompt | unsupported | unknown
audio_disable_control     supported | unsupported | unknown
audio_reference_control   supported | unsupported | unknown
duration/sample_rate/channels constraints when known
capability_ref/digest
```

能力未知不等于不生成声音。若 route 曾观察到原生音频但不能可靠关闭或控制，按 `native_audio=supported`、控制能力 `unknown/unsupported` 处理，并默认选择 `replace_after_generation`。

## 原生对白主线（已验证原生音频线路）

对白的第一生产路径可以是视频模型的原生音频能力，而不是默认后期 TTS。对已验证支持可控原生对白的线路，Director 把逐句台词、说话人、音色描述与情绪写进受控的声音设计输入，policy 取 `video_native`，该镜不需要 audio owner 预生产配音。原生对白镜仍需逐句通过 review：台词文本一致、角色音色跨镜一致、口型与可懂度、rights/版权；任一句失败只回退该句到 audio owner 补配，不推翻整镜。

audio owner 在原生对白主线下的默认职责收窄为：配乐、SFX/ambience、最终混音、原生音轨登记与审听证据、失败句补配。`replace_after_generation` 保留为两类回退：能力未验证/不可控的 route，以及 `video_native` review 失败的镜头。

## Policy 语义

- `none`：明确要求视频没有生产音频；缺字段不能推断为 none。
- `external_assets`：生成前已绑定 audio owner 的音频 refs，provider 只消费允许的引用。
- `video_native`：计划保留视频模型原生音频；必须单独通过同步、对白、角色声音、版权、可编辑性和人工审听门禁。已验证原生对白线路的对话镜可走本 policy，台词进入受控的声音设计输入。
- `replace_after_generation`：原生音频只作样片/动作同步参考，最终由 audio owner 的资产和 mixdown 替换。原生音轨仍需登记 parent video ref 和 review 状态，不能静默进入 export。仅用于能力未验证/不可控 route 或 `video_native` review 失败的镜头。

当 rights、sync confidence、voice permission、editability 或 review 任一未知时，`video_native` 必须逐句降为 audio owner 补配或整镜降为 `replace_after_generation`，或返回 blocker。

## Owner 流程

```text
accepted screenplay/dialogue refs
  -> Director freezes ShotAudioIntent and cue timing
  -> Producer freezes model audio capability and policy
  -> video generation produces picture + optional native audio
  -> audio owner registers video_native_audio or renders voice/SFX/music/mix refs
  -> Edit/Sound reviews A/V sync, dialogue, silence and duration
  -> production timeline owner binds refs/policy/review state into timeline
  -> assembly/export gate
```

Canonical ownership：Director/scene owner 决定叙事声音意图；audio owner 拥有音频资产、声音策略和 mix refs；production timeline owner 拥有 ProductionGraph、时间线、接受和导出；模型路由 Owner 拥有 capability/任务/成本事实。

## Episode 级 audio-owner 投影

逐镜 `ShotAudioIntent` 是创作源，不能再手工维护一份独立 Episode audio plan。进入音频生产阶段时，由同一源生成一个由宿主声明 schema 的版本化 audio-owner handoff：

```text
ShotAudioIntent source
  -> review CSV/Markdown
  -> video-native prompt ref/digest
  -> host-declared audio-intent schema
       -> audio-owner compiler
          -> EpisodeAudioPlan + SFXCuePlan + SilenceWindowPlan
```

handoff 只传 shot/cue/timeline refs、offset、tags、空间/sync、brief refs/digests、provider policy/capability、dialogue spans 与 acceptance refs，不传 brief/provider prompt 正文。`ambience|foley|motif` 编译为 SFX；`music` 绑定已有 MusicCuePlan；`dialogue` 绑定 LanguagePlan；`silence` 是 mix constraint，不是 SFX/audio asset。audio plan 必须绑定 source handoff ref/digest，production timeline owner 只消费 audio refs/readiness。

## Stale 与失败条件

以下变化必须使尚未开始的音频/视频 generation spec 或 assembly proposal stale：镜头时长、动作相位、对白 span、cue 时间、lip-sync、provider audio policy、capability digest、audio plan/mix revision。

以下情况 fail closed：

- 原生音频 route 缺少 `ShotAudioIntent`；
- cue 超出镜头时长或对白没有 accepted span；
- `replace_after_generation` 没有 audio-owner replacement route；
- `video_native` 缺 rights/sync/voice/review 证据；
- 视频裁切后音频时长、尾帧或字幕不对齐；
- 视觉 pass 被误当成音频 pass。
