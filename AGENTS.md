# AI Drama Skills 工作区说明

本仓库是 Yeisme 第一方 AI 做剧 Skills 项目，负责可复用的创作判断、评估流程、路由和 Owner handoff 说明，不负责保存剧本正文、ProductionGraph、资产 bytes、provider 凭据或运行时数据库。

## 目录边界

- 每个 Skill 目录必须包含 `SKILL.md` 与 `agents/openai.yaml`。
- `references/` 只放该 Skill 需要按需读取的规则、量表和示例。
- 本仓库是独立发布源；父级聚合仓库可把它挂载为 Git 子模块，但生成运行副本不在本仓库维护。
- canonical screenplay 归 Auctra，调度/receipt 归 Ordo，视觉 artifact 归 Eikona，ProductionGraph/production acceptance 归 Scaena。

## 设计约束

- `ai-drama-router` 是唯一做剧入口；新 format、genre 或 platform 默认扩展一层 references，不创建竞争 Router。
- 每个 stage 只选择一个 primary Skill、最多一个 compatible constraint，并按需构建一个最小 `DramaContextPack`。
- root 只常驻 `ai-drama-router`；专项 Skills 留在 source layer 或具体 owner/project profile，禁止批量启用全套做剧 Skills。
- `ai-drama-router/` 必须保持宿主无关：不得出现 Yeisme 私有脚本、source/profile/runtime 路径或产品 Owner 名称。
- Agent 负责语义路由；宿主通过 capability adapter 实现确定性发现、预览、启用、回滚和验证。Yeisme 的 adapter 才可调用 `scripts/skills.sh`，不要把自然语言理解写进脚本。
- Skill 输出 proposal、评估和 handoff，不直接修改其他 Owner 的 canonical state。
- 多评委必须盲评、绑定 CandidateSet/rubric/profile 版本，并记录模型相关性簇。
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
