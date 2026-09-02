# Seedance 2.5 做剧能力参考包

这是保留文件名的兼容入口，也是五个独立模型档案中的 Seedance 档案。多模型过滤、非绑定建议
和其他家族入口见 `video-model-capability-index.md`；典型镜头工作流见
`video-model-drama-workflow-matrix.md`。

本参考只提供可追溯事实和路由约束，不是 provider SDK 或 Scaena canonical state。

官方事实源：

- [Seedance 2.5 提示词指南](https://docs.volcengine.com/docs/82379/2607689?lang=zh)
- [Seedance 2.5 API 与约束说明](https://docs.volcengine.com/docs/82379/2607688?lang=zh)

## 能力快照

| 项目 | 事实 |
| --- | --- |
| canonical model | `doubao-seedance-2-5-260628` |
| modes | `text`、`reference`、`frames`、`edit`、`extend` |
| media | `reference_image`、`reference_video`、`reference_audio`、`first_frame`、`last_frame` |
| limits | 总引用 50；图片 30；视频 10；音频 10；first/last 各至多 1 |
| duration | 4–30 秒；部分模式允许 `-1` |
| ratios | `adaptive`、`21:9`、`16:9`、`4:3`、`1:1`、`3:4`、`9:16` |
| resolutions | `480p`、`720p`、`1080p`；1080p 需要单独证据 |
| output | `mp4`、`mov`；edit/extend 需要连续性时优先 MOV |
| audio | 可关闭、原生、多语言原生和纯音频参考均可作为能力事实；最终 mix 仍需独立 policy/review |

`family=seedance`，`variant=2.5`，当前最高 maturity 为 `local_fixture_verified`；
`production_ready` 只能由 production owner 的真实证据提升。

## 模式锁定

- `text`：不带媒体。
- `reference`：使用非 first/last 引用；ratio/duration 可配置。
- `frames`：只使用 first/last frame，ratio=`adaptive`，duration 为允许值。
- `edit`：需要 `reference_video`，ratio=`adaptive`，duration=`-1`。
- `extend`：需要 `reference_video`，ratio=`adaptive`，duration 为允许值或 `-1`。

Ark 的 `omni_reference_task_type` 是适配器 wire hint。Router 只输出 provider-neutral 的 task intent/lock facts，不把该字段写进 `DramaRoutePlan` 的必填业务输入。异步 `TaskTypeMismatch`/`TaskTypeConstraint` 要进入 typed failure/reconcile，不得自动重发。

## 做剧路由规则

1. `director_plan` 先冻结 `ShotIntent` 与版本化 `ShotAudioIntent`；原生音频 capability 不得替代声音意图。
2. `visual_plan` 说明每个 reference 的用途（identity/action/style/camera/geometry/audio），保持 ordinal 与 `@图片N/@视频N/@音频N` 一致。
3. `reference_video` 只绑定明确镜头和语义角色；`.blend` 不是 provider 输入，必须先成为有权利的 MP4/MOV asset ref。
4. `generation` 先做 capability、task lock、counts、rights、cost、idempotency 和 stale preflight；不满足时返回 `blocked`，不调用 provider。
5. 原生音频默认 `replace_after_generation`。只有 rights、sync、声线、lip-sync、可编辑性和人工声音审听齐全时才可使用 `video_native`。
6. `edit/extend/frames` 的异步成功只代表任务完成；必须回到 Scaena CAS、continuity、audio review 和 production acceptance。

## 成熟度标签

```text
contract_declared
local_fixture_verified
provider_canary_verified
production_ready
```

Skills 可以为所有官方能力生成完整合同和离线测试计划，但未有真实 owner evidence 时不得输出 `production_ready`。能力全量覆盖不等于一次加载或一次生成所有模式。

## 提示词与时间轴

推荐结构：`subject + action/event + scene/environment + visual style + camera/cuts + sound`。

- 每个引用写明用途，不把“素材存在”当作语义。
- 时间戳使用当前 clip 的相对时间；从零开始、连续无 gap/overlap、末段等于 clip duration。
- 多网格少于 15 个 panel、使用简单线稿时更适合作为布局参考；它不能替代严格 keyframe。
- 负面约束、静音、字幕、对白与音画同步写入镜头/音频合同，不交给 provider 自由补全。

## 外部 Skill 边界

火山文档推荐的 `sd25-pe` 是可选外部资料入口。本仓库不安装、不依赖、不在 production run 中联网热加载它；需要时由宿主先完成来源、版本、许可证和 activation 决策。
