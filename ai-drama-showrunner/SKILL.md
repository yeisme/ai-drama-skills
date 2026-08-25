---
name: ai-drama-showrunner
description: Use when planning an AI drama season, multi-episode arc, episode function, long-term character change, suspense, payoff, production priority, or next-episode handoff.
---

# AI Drama Showrunner

## 目标

管理持续生长的故事生态：世界规则、长线人物变化、季度主题、单集功能、悬念兑现和制作优先级。Showrunner 负责方向和取舍，不直接成为 provider scheduler。

## 工作流

1. 读取 `DramaFormatContract` 和 `episode-planning` 或 `series-development` DramaContextPack；缺失时先返回上游补齐，不自行猜测剧型。
2. 读取 CanonSnapshot、已完成 episode、角色状态和未兑现伏笔。
3. 定义 season/arc promise、episode question、局部 payoff 和末尾 hook。
4. 新写或大幅重写超过 5 集时，不直接排完整集纲：先选 3 个代表性压力场景组成 proof slice，通常覆盖“关系规则被打破”“三角压力迫使站队”“错误选择产生后果”。关系三角不是三个人同场，而是第三方真实改变另外两人的选择成本。
5. 每个 proof-slice episode 只定义一个核心场景合同：entry state、人物目标、不可直说的原因、冲突策略、信息释放、代价和 exit state。交给 Scene Writer 产生至少两个策略差异明确的候选；不能用同义措辞冒充 A/B。
6. proof slice 交付后停止扩写，等待用户明确判断至少两个主要人物的声音。每个场景最多允许一次有界改写；仍不成立时回到场景合同，不靠增加集数掩盖问题。
7. 只有状态变化、结构证据、Dialogue Live Test 和用户声音选择同时通过 expansion gate，才以每批最多 5 集继续；每批重复同一 gate。`full_scale` 需要连续批次证据稳定和用户明确授权。
8. 为进入下一批的每集分配人物变化、冲突升级、信息释放、视觉/声音重点和生产风险。
9. 检查集间因果、悬念债务、角色成长速度和制作资源冲突。
10. 输出 `ShowrunnerPlan` 与 episode proposals，交给 story/episode owner。

## 输出合同

除常规季度/多集规划外，超过 5 集的请求至少输出：

- `proof_slice_reason`：为什么这三集足以暴露人物声音、关系压力与后果；
- `proof_slice_episodes`：每集一个核心场景合同，不是整集终稿；
- `batch_size: 3` 与 `next_batch_max: 5`；
- `candidate_policy`：A/B 至少在策略、信息释放、空间行动、代价或 exit state 中两项不同；
- `expansion_gate`：状态变化、诚实证据、Dialogue Live Test、用户声音选择和一次有界改写状态；
- `unresolved_voice_questions`：尚未由用户确认的主要人物声音问题；
- `artifact_disposition`、`persistence_policy`、`batch_policy` 和 `acceptance_state`。

## 质量门槛

- 每集必须有独立可感知的情绪弧；
- 长线悬念必须标注预计兑现窗口和风险；
- 不能靠新增设定无限延长故事；
- 关键人物变化必须由事件和选择驱动；
- 计划必须能降级成可生产的短集，而不是只在概念层成立。
- proof slice 的三场戏必须各自改变关系、资源、信息或责任状态，不能只重复同一场争吵。
- 三角场景中的第三方必须改变选择成本、信息优势或责任归属，不能只是旁观和劝架。
- 用户未确认声音时，剩余全集保持未生成；未选候选不得成为后续 canonical context。

## 边界与验证

不复制 canonical story、不直接 dispatch provider、不自动接受 episode，也不因用户要求 Markdown 就把试写落到最终项目路径。先运行本仓库的 `python3 scripts/validate_skills.py`；宿主集成必须再通过对应 story、episode 与 production Owner 的合同测试。
