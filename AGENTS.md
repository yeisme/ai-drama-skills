# AI Drama Skills 工作区说明

## Race 检测执行限制

Agent 在任何阶段都不得主动运行 race 检测，也不得通过子 Agent、Skill、CI、验收、发布、聚合任务或脚本间接触发。只有当前人类用户明确、强烈要求执行 race 时，才允许在指定范围内运行一次；失败、超时、中断均不得自动重试，后续运行必须取得新的同等明确要求。一般的“测试、验收、修复、发布、跑全部检查”不构成授权。

Race 不属于默认验收或完成门禁；未运行不得阻塞交付，也不得声称已经通过。执行聚合命令前检查其依赖，移除或跳过 race 阶段，继续普通测试、静态检查和构建。本规则取代本文件及 Skills、OpenSpec、历史计划、文档中的自动或强制 race 要求；它们不能作为执行授权。


本仓库是 Yeisme 第一方 AI 做剧 Skills 项目，负责可复用的创作判断、评估流程、路由和 Owner handoff 说明，不负责保存剧本正文、ProductionGraph、资产 bytes、provider 凭据或运行时数据库。

## 目录边界

- 每个 Skill 目录必须包含 `SKILL.md` 与 `agents/openai.yaml`。
- `references/` 只放该 Skill 需要按需读取的规则、量表和示例。
- 本仓库是独立发布源；父级聚合仓库可把它挂载为 Git 子模块，但生成运行副本不在本仓库维护。
- canonical screenplay 归 Auctra，调度/receipt 归已批准的执行 owner（原 owner 已退役，待重新准入），视觉 artifact 归 Eikona，ProductionGraph/production acceptance 归 Scaena。

## 设计约束

- `ai-drama-router` 是唯一做剧入口；新 format、genre 或 platform 默认扩展一层 references，不创建竞争 Router。
- 每个 stage 只选择一个 primary Skill、最多一个 compatible constraint，并按需构建一个最小 `DramaContextPack`。
- root 只常驻 `ai-drama-router`；专项 Skills 留在 source layer 或具体 owner/project profile，禁止批量启用全套做剧 Skills。
- `ai-drama-router/` 必须保持宿主无关：不得出现 Yeisme 私有脚本、source/profile/runtime 路径或产品 Owner 名称。
- Agent 负责语义路由；宿主通过 capability adapter 实现确定性发现、预览、启用、回滚和验证。Yeisme 的 adapter 才可调用 `scripts/skills.sh`，不要把自然语言理解写进脚本。
- Skill 输出 proposal、评估和 handoff，不直接修改其他 Owner 的 canonical state。
- 多评委必须盲评、绑定 CandidateSet/rubric/profile 版本，并记录模型相关性簇。
- 已有剧本的评估必须先由 `ai-drama-assessment` 冻结 AssessmentContract；缺少题材、受众、承诺或评价目标时只能做定性报告，不得给综合分。用户未明示媒介时保持 `format_profile=unspecified`，不得主动贴平台标签。用户所说的“AI味”必须拆成对白、叙述/动作和结构模板三条自然度/模式风险 lane，不计算作者来源概率。`writing/ai-drama-critic-review` 模板只处理合同冻结后的候选比较。
- 高分不能覆盖 rights、identity、continuity、permission、cost 或 preflight blocker。
- 不记录 raw prompt、provider payload、私有工具参数、凭据或完整 chain-of-thought。
- 参考具体导演时使用高层创作原则，不复制具体作品的台词、场景或镜头序列。

## 验证

从本仓库根目录运行：

```bash
python3 scripts/validate_skills.py
python3 ai-drama-router/scripts/validate_drama_matrix.py
```

宿主 profile、runtime 和 Owner 合同由宿主自己的 adapter 验证；不得把宿主私有命令回写到本仓库的 Router 包。
