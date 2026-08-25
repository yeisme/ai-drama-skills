---
name: manga-drama-project-starter
description: Use when creating, onboarding, localizing, or safely migrating a manga-drama, short-drama, screenplay-production, or episodic AI drama workspace that composes Auctra text canon with Scaena production state without reusing novel directory layouts.
---

# 漫剧项目启动器

创建精简的 Auctra + Scaena 做剧工作区。默认使用 `en-US`；只有用户显式选择 `zh-CN` 时才生成中文目录。目录配方由本 Skill 持有，Auctra 负责校验和写入 layout manifest，Scaena 只维护 `.scaena/`。

需要目录映射或迁移时先读 [references/workspace-layout.md](references/workspace-layout.md)。

## 交互合同

1. 先确认项目路径、标题、集数、是否已有 Auctra/Scaena 状态和显式 locale；不得根据标题、对白语言或路径名猜 locale。
2. 新项目先展示 Auctra screenplay profile、Scaena lazy layout 与首个阶段 roles，再分别调用两个 owner CLI。
3. 旧项目先读取 owner status 并生成 Auctra migration plan；只有用户明确批准该次计划后才运行 `apply --yes`。
4. 每一步都报告 owner、display path、gate/acceptance 状态和下一条真实命令；目录存在或 provider success 不得描述为内容已接受或 production-ready。

## 工作流

1. 收集项目路径、标题、集数和显式 locale；未提供 locale 时固定为 `en-US`。
2. 用 bundled script 在操作系统临时目录生成 `workspace_recipe.v1`，不得让用户或 Agent 手写 recipe。
3. 初始化 Auctra screenplay project：

```bash
auctra project init <project-path> --title "<title>" --template screenplay --locale en-US --workspace-recipe <recipe.json> --json
```

4. 初始化 Scaena lazy production workspace：

```bash
scaena init <project-path> --title "<title>" --episodes 1 --workspace-layout lazy --json
```

5. 阶段 Skill 只确保当前所需角色：

```bash
auctra project layout ensure <project-path> --role planning_outline --json
auctra project layout ensure <project-path> --role screenplay_scenes --json
```

6. 迁移旧项目时先生成 recipe，再运行 plan；存在任何冲突时停止。无冲突时也必须先向用户展示计划并获得明确批准，才运行 apply：

```bash
auctra project layout plan <project-path> --workspace-recipe <recipe.json> --merge --out <plan.json> --json
auctra project layout apply <project-path> --plan <plan.json> --yes --json
```

## 边界

- 不直接创建、移动或编辑 `.auctra/**`、`.scaena/**`、SQLite、manifest、receipt 或 review decision。
- 不把 `chapters/章节`、分卷或章节表加入做剧 recipe。
- 不根据标题、对话语言或路径名猜 locale。
- Migration collision、case-fold collision 或 stale plan 必须 fail closed；不得改名绕过或覆盖目标文件。
- `selected`、provider success 或目录存在都不等于 accepted/production-ready。
- Scaena 不可用时如实报告 `capability_missing`；Auctra screenplay 项目可以独立初始化，但不得声称完整生产工作区已完成。

## 验证

```bash
python3 scripts/generate_workspace_recipe.py --locale en-US --output <recipe.json>
python3 scripts/generate_workspace_recipe.py --locale zh-CN --output <recipe.json>
python3 scripts/validate_skills.py
```
