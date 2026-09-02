---
name: ai-drama-producer
description: Use when defining AI drama production constraints, cost caps, rights, permissions, provider capability, batch strategy, quality floors, retry budgets, exceptions, and delivery readiness.
---

# AI Drama Producer

## 目标

把创作意图变成可执行、可预算、可审计的 ProductionConstraintProfile。制片思维首先决定什么值得做、什么不能做、什么时候必须停。

## 工作流

1. 读取 `references/production-constraints.md`，再冻结项目/Episode scope、时长、镜头数、主体/风格/reference、平台规格和交付目标。
2. 检查 provider capability、模型 ref、权限、quota、rights、预算、并发和 storage。视频 capability 必须分别表达 `native_audio`、`audio_prompt_control`、`audio_disable_control`、audio reference、task mode/lock、引用上限、时长/画幅/分辨率/output 约束及 capability ref/digest；音频字段读取 `../ai-drama-router/references/shot-audio-intent-contract.md`，多模型事实与非绑定路由读取 `../ai-drama-router/references/video-model-capability-index.md`。
3. 选择 `throughput`、`craft` 或 `smart_mix`，冻结 retry、quality floor、exception 和 delivery policy。
4. 执行 zero-call admission；原生音频 route 缺 `ShotAudioIntent`、音频控制能力未知却没有 replacement policy、或未知成本/权限/能力/acceptance 时返回 blocked/needs_input。
5. 生成 `ProductionProposal`、cost summary、risk matrix 和下一步 owner action。

## 质量门槛

- 不先调用再补预算、rights 或权限；
- 不因高分自动接受高风险资产；
- 单 item 失败应隔离，批次支持 partial success；
- unknown accept 只能 reconcile 原 binding，不新建 job；
- provider succeeded 只代表视频任务完成；原生音频必须单独登记和 review。默认 policy 是 `replace_after_generation`；只有线路 capability、逐句可控性、rights、sync、voice permission、editability 和人工审听全部有证据时才可提升为 `video_native`；
- `contract_declared`、`local_fixture_verified`、`provider_canary_verified` 和 `production_ready` 必须分开；50 引用、纯音频、多语言、1080p 或 MOV 出现在官方文档或 fixture 中，不代表远端配额、真实质量或 production admission 已通过；
- 模型/线路 capability digest、镜头时长或音频 policy 变化会使未开始 generation spec stale，禁止静默沿用旧声音假设；
- 社区热度、star、播放量和营销样本只允许作为按需研究信号，不得改变 eligible/suggested family、成熟度、预算或 production admission；
- Eikona 出图默认模型为 `openai/gpt-5.4-image-2`；`gpt-5.4-image-2` 与 `gpt-image-2` 为兼容短别名，模型漂移必须显式记录。

## 边界与验证

不持有 provider credential、不发布平台、不写宿主 ProductionGraph。先运行本仓库的 `python3 scripts/validate_skills.py`；批次、预算、权限和生产策略还必须通过宿主 production/orchestration Owner 的架构与集成测试。
