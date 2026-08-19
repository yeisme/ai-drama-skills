---
name: ai-drama-producer
description: Use when defining AI drama production constraints, cost caps, rights, permissions, provider capability, batch strategy, quality floors, retry budgets, exceptions, and delivery readiness.
---

# AI Drama Producer

## 目标

把创作意图变成可执行、可预算、可审计的 ProductionConstraintProfile。制片思维首先决定什么值得做、什么不能做、什么时候必须停。

## 工作流

1. 读取 `references/production-constraints.md`，再冻结项目/Episode scope、时长、镜头数、主体/风格/reference、平台规格和交付目标。
2. 检查 provider capability、模型 ref、权限、quota、rights、预算、并发和 storage。视频 capability 必须包含 `native_audio`、`audio_prompt_control`、`audio_disable_control`、可用 audio reference、时长/采样率/声道约束及 capability ref/digest；字段和默认策略读取 `../ai-drama-router/references/shot-audio-intent-contract.md`。
3. 选择 `throughput`、`craft` 或 `smart_mix`，冻结 retry、quality floor、exception 和 delivery policy。
4. 执行 zero-call admission；原生音频 route 缺 `ShotAudioIntent`、音频控制能力未知却没有 replacement policy、或未知成本/权限/能力/acceptance 时返回 blocked/needs_input。
5. 生成 `ProductionProposal`、cost summary、risk matrix 和下一步 owner action。

## 质量门槛

- 不先调用再补预算、rights 或权限；
- 不因高分自动接受高风险资产；
- 单 item 失败应隔离，批次支持 partial success；
- unknown accept 只能 reconcile 原 binding，不新建 job；
- provider succeeded 只代表视频任务完成；原生音频必须单独登记和 review。已验证可控原生对白的 Seedance 2.0 线路，对话镜默认 `video_native`（台词进生成 prompt）；rights、sync、voice permission 或 editability 未知时才默认 `replace_after_generation`；
- 模型/线路 capability digest、镜头时长或音频 policy 变化会使未开始 generation spec stale，禁止静默沿用旧声音假设；
- Eikona 出图默认模型为 `openai/gpt-5.4-image-2`；`gpt-5.4-image-2` 与 `gpt-image-2` 为兼容短别名，模型漂移必须显式记录。

## 边界与验证

不持有 provider credential、不发布平台、不写宿主 ProductionGraph。先运行本仓库的 `python3 scripts/validate_skills.py`；批次、预算、权限和生产策略还必须通过宿主 production/orchestration Owner 的架构与集成测试。
