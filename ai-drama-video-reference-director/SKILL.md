---
name: ai-drama-video-reference-director
description: Use when turning a Blender-rendered MP4/MOV or another reference video into shot-level motion, camera, composition, pose, or geometry constraints for Scaena AI manga-drama production, including Seedance reference-video generation, input-bundle validation, continuity review, and owner handoff; keep rights, provider calls, canonical state, and production acceptance behind explicit gates.
---

# AI 做剧视频参考导演

## 使用场景

把“这段 Blender 视频的动作/镜头很好，想让生成视频沿用”转成可审阅、可重放、可交接的镜头参考方案。适用于：

- Blender 预演视频作为镜头运动、动作节奏、构图或姿态参考；
- Seedance 2.5 的 `reference_video`、`edit`、`extend` 或同类视频参考请求；
- Scaena 单镜头 `ShotIntent`、`ShotGenerationSpec`、`VideoInputBundle` 的规划与门禁；
- 生成结果与参考视频之间的动作、相机、主体和连续性复核。

不要把 `.blend` 文件当作视频输入。先在 Blender 中渲染为有权利使用的 MP4/MOV，再进入本流程。

## 输入与输出

输入至少包括：项目/集/镜头 refs、已接受的剧本或镜头意图、参考视频文件或已登记的 asset ref、参考用途、时长/画幅/权限和生成策略。

输出一个不写 canonical state 的 handoff：

```text
status
shot_ref
reference_asset_refs
reference_roles
trim_or_segment
input_bundle_ref
input_bundle_digest
capability_ref
generation_plan
continuity_checks
owner_action
blocking_findings
next_command
```

## 工作流

1. 读取当前项目、ProductionGraph、`ShotIntent`、主体/风格版本、权限和最近 blocker。参考视频只能绑定到明确镜头，不允许以“全片参考”绕过镜头意图。
2. 识别参考语义：`camera`、`motion`、`composition`、`pose`、`geometry`。参考视频含音轨时还必须声明 `mute`、`reference_only`、`preserve_candidate` 或 `replace_after_generation`；不得因为视频有声音就把参考音轨当作 canonical audio。视觉角色详见 [reference-video-contract.md](references/reference-video-contract.md)，声音合同见 `../ai-drama-router/references/shot-audio-intent-contract.md`，Seedance 2.5 mode/lock/limit 见 `../ai-drama-router/references/seedance-2-5-capability-profile.md`。
3. 登记本地媒体。优先使用 Scaena CLI 生成 asset ref、digest、媒体探测事实、权限和 review 状态；不得手写 `.scaena`、数据库行或证据元数据。
4. 编译冻结的输入 bundle proposal：保留 asset refs/digests、角色、ordinal、裁剪段、时长、画幅、provider-neutral task policy、模型 capability maturity、audio/output policy、成本策略和来源 lineage；参考视频裁切后重新核对音频时长/尾音，不要把 `omni_reference_task_type`、临时 URL、signed URL、API key 或 provider payload 写入持久化状态。
5. 先做 zero-call admission：检查格式、时长、大小、权限、主体/风格版本、capability、引用数量、mode/media 组合、ratio/duration lock、output、预算和幂等键。缺任何一项就返回 `needs_input`、`needs_contract` 或 `blocked`，不要先调用后补手续。
6. 生成时优先走 Scaena/Aigora 的 owner bridge。只有用户明确授权的 live canary 才允许直接执行 Seedance provider smoke；“provider 成功”只代表任务完成，不代表 Scaena 接受。
7. 将输出登记为 CAS-backed、`pending_review` 的候选，绑定输入 bundle digest 和生成 receipt。原生音轨单独登记为 `video_native_audio` 或标记 replacement required；调用 `$ai-drama-continuity-supervisor` 检查动作相位、相机路径、构图、主体身份、服装/道具、空间、时间和声音连续性。
8. 将结果交给 `$scaena-production-operator` 或对应 Owner action；只有 Scaena 的显式 review/production acceptance 才能进入 assembly/export。需要节奏和声音时，再交给 `$ai-drama-edit-and-sound`。

## 当前实现判断

- 直接 Seedance Ark adapter 可以验证部分视频 URL reference 和任务模式，但这不等于 Scaena 生产链已经完整支持官方全部引用、纯音频、1080p/MOV 或 production admission。
- 若当前版本没有稳定的 `VideoReferenceBinding`、视频 `VideoInputBundle`、媒体探测、CAS 下载/导入或 worker reconcile 合同，输出 `needs_contract`，并把缺口交给 `agent/scaena` 的 OpenSpec；不要发明不存在的 CLI。
- 当前可用的本地登记入口形如：

  ```bash
  export SCAENA_REPO=/path/to/scaena
  cd "$SCAENA_REPO"
  go run ./cmd/scaena asset ingest <reference-video.mp4> \
    --project <project-path> \
    --role reference_video \
    --permission owned \
    --review-status accepted \
    --json
  ```

- 需要 live provider canary 时，先确认 `ARK_API_KEY` 已通过用户级凭据配置提供；不要在命令、日志或 handoff 中回显凭据。生产任务仍应通过 owner bridge，不要把这条 smoke 命令当作生产入口。

## 边界

- 不保存或修改 Auctra canonical screenplay、Scaena ProductionGraph、SubjectVersion、production acceptance、assembly 或 export 状态。
- 不把“参考视频中的所有内容”默认复制到生成结果；必须声明参考角色、镜头段和允许偏差。
- 不把 Blender 场景文件、原始 provider payload、完整 prompt、signed URL、凭据或完整模型推理写入 skill、项目状态或证据。
- 不在没有权限、预算、capability 和人工 review 策略时发起付费调用、批量 reroll 或外部发布。
- 不用 synthetic fixture、单帧相似度或 provider success 代替动作/镜头/主体连续性和生产接受。

## 验证

先运行本仓库 Skill 与路由矩阵校验：

```bash
python3 scripts/validate_skills.py
python3 ai-drama-router/scripts/validate_drama_matrix.py
```

实现或排查 Scaena 视频参考能力时，至少运行相关 focused checks；不要把没有真实 provider 调用的测试描述成 live evidence：

```bash
export SCAENA_REPO=/path/to/scaena
cd "$SCAENA_REPO"
go test ./internal/bridge/seedance ./internal/bridge/seedanceark ./internal/bridge/videomodels ./internal/video
go test ./internal/cli -run 'Video|LiveVideo|Seedance' -count=1
go test ./tests/integration -run 'VideoRun|VideoInputBundle|SingleShot' -count=1
```

涉及 Studio/worker 或稳定公共合同的变更，先建立或更新 `agent/scaena/openspec/changes/<change-id>/`，再进入实现；验证运行必须保留项目规定的脱敏 evidence。
