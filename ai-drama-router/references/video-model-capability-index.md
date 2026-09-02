# 视频模型做剧能力索引

本索引把视频模型的官方能力事实编译成 provider-neutral 做剧约束。它只服务于
`DramaRoutePlan.stage_plans[phase=generation].video_model_guidance`，不选择 exact model、
channel、价格、credential、provider payload 或 production attempt；这些事实归生产模型目录
与运行时 policy owner。

## 按需档案

| 模型家族 | 档案 | 已冻结的主要能力 | 当前 maturity 上限 |
| --- | --- | --- | --- |
| `minimax_h3` | `video-model-profile-minimax-h3.md` | 4–15 秒、混合参考、首尾帧、768P→2K 分阶段精修 | `local_fixture_verified` |
| `wan` | `video-model-profile-wan-3-0.md` | 2–30 秒、All-in-One async、文件/网页、edit/extend、`prompt_extend` | `local_fixture_verified` |
| `seedance` | `seedance-2-5-capability-profile.md` | 4–30 秒/auto、50 个全模态参考、edit/extend/frames、原生音频 | `local_fixture_verified` |
| `kling_v3` | `video-model-profile-kling-v3.md` | text、image reference、first/last frames | `contract_declared` |
| `kling_v3_omni` | `video-model-profile-kling-v3-omni.md` | 多图、元素、视频参考的高层能力声明 | `contract_declared` |

只有当前镜头的硬能力、用户偏好或研究请求命中时才加载对应档案。普通做剧路由不加载
`video-model-community-research-2026-09-01.md`。

## 非绑定路由规则

1. 用户给出的合法 exact lock 优先。Router 可校验它是否满足硬约束，但不得覆盖、替换或
   改写为另一个 exact ID。
2. 先按 `required_capabilities[]`、任务模式、时长、分辨率、引用种类/数量、音频与 topology
   过滤家族。
3. 只有用户偏好或硬能力要求产生唯一匹配时，才填写 `suggested_model_family`。
4. 多个家族同时满足时，只填写 `eligible_model_families[]`，由生产 policy owner 决策；不得用
   社区热度、播放量、star、营销宣传或未经钉版的质量印象破平局。
5. `binding_mode` 固定为 `non_binding`。Skill 不输出 channel、价格、credential、provider
   payload、生产 readiness 或伪造 exact ID。
6. `smart_auto` 是合法合同意图；宿主 bridge 未声明支持时，返回 `smart_auto_bridge_unsupported`
   blocker，不伪装为已有 production route。
7. capability 缺失或为 `unknown` 时 fail closed。特别是 Kling V3 Omni 的 video-only reference
   若没有 owner-pinned wire mode，返回 `owner_capability_unverified`。

## 音频默认

即使档案声明原生音频，做剧默认仍为 `replace_after_generation`。只有 rights、逐句对白与
声线控制、同步、可编辑性和人工审听证据齐全，才允许 production owner 把单镜提升为
`video_native`。

## 工作流

典型镜头的 artifact、能力、门禁、证据和回退路径见
`video-model-drama-workflow-matrix.md`。模型能力不会改变“每阶段一个 primary、最多一个
constraint”的 Router 不变量。
