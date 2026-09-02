# AI Drama Skills

本模块把剧型策略、上下文包、导演、编剧、人物、连续性、评估和制片判断拆成可路由的第一方 Skills。用户入口保持为 `ai-drama-router`，专项 Skills 默认按需加载。对已有剧本的评估必须先经过 `ai-drama-assessment` 建立题材化 `AssessmentContract`，再进入 `ai-drama-critic-panel`；没有合同不得给综合分。用户所说的“AI味”拆为对白、叙述/动作和结构模板三条自然度/模式风险 lane，不输出作者来源概率；媒介标签只有用户明示时才冻结。

`ai-drama-router` 是可移植核心，只定义 `DramaRoutePlan`、逻辑 Owner、渐进解析状态和宿主 capability contract，不包含 Yeisme 私有命令、目录或产品绑定。Yeisme 的 source/profile/runtime 规则属于宿主 adapter，不进入 Router 包。

Skill 是执行指导，不是第二套故事数据库。实现或修改跨项目合同时，应回到宿主仓库与对应 Owner 的正式设计/契约流程；本仓库只保存可复用的 Skill 工作法。

共享约束引用：

- `ai-drama-router/references/canon-boundary.md`
- `ai-drama-router/references/routing-matrix.md`
- `ai-drama-assessment/references/assessment-contract.md`
- `ai-drama-router/references/skill-resolution-policy.md`
- `ai-drama-router/references/drama-route-plan-contract.md`
- `ai-drama-router/references/upstream-video-production-patterns.md`
- `ai-drama-format-strategist/references/format-profiles.md`
- `ai-drama-context-pack-builder/references/context-pack-profiles.md`
- `ai-drama-producer/references/production-constraints.md`
- `ai-drama-continuity-supervisor/references/continuity-evidence.md`
- `ai-drama-router/references/seedance-2-5-capability-profile.md`

Seedance 2.5 的官方能力只维护一份做剧参考包；Scaena 在其 Owner 仓库的
`docs/protocols/seedance-2-5-capability-profile.md` 记录 runtime 映射。两边都必须保留
官方链接，不把未实现的 provider 能力写成当前命令。

独立 Router 包验证：

```bash
cd ai-drama-router
python3 scripts/validate_drama_matrix.py
```

仓库级结构验证：

```bash
python3 scripts/validate_skills.py
```
