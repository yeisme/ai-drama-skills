---
name: manga-drama-project-starter
description: Use when starting or onboarding a manga-drama, short-drama, screenplay, or episodic AI drama project while keeping ordinary author files separate from Auctra and Scaena state.
---

# 漫剧项目启动器

创建清晰的剧本作者入口。Auctra 持有 canonical screenplay，Scaena 持有生产状态；本 Skill 不用目录存在证明内容已接受或已可生产。

## 交互合同

1. 先读取已有项目、普通作者文件、`AGENTS.md` 和 Auctra/Scaena owner 状态；缺少 `.auctra` 或 `.scaena` 不等于内容不存在。
2. 只为当前实际要写的剧本、资料或大纲创建普通目录，不生成空骨架。
3. 在普通 `AGENTS.md` 写明当前文件、先读什么、正式稿/待审稿/历史怎样区别和如何继续。
4. 普通 Markdown、README 和作者说明可由 Agent 维护；Auctra/Scaena 的机器状态、review、version、receipt、ProductionGraph 和交接只能通过各自 owner service/CLI 修改。
5. 每一步报告 canonical owner、当前 review/acceptance gate 和下一条真实命令；格式或媒介不明且会改变结构时返回 `needs_format_decision`。

## 工作流

1. 读取现有项目与 owner 状态，保留未知目录和历史资料原位。
2. 按这次任务创建最小普通目录，更新 `AGENTS.md` 的阅读顺序和继续方法。
3. 所有剧本请求进入 `ai-drama-router`；资料、写作、审稿、修订和整理只选一个 primary，最多一个必要 constraint。
4. 整集正文是唯一 canonical screenplay；场景引用整集 AST/source span，不另写第二份场景正文。
5. 候选先进入 Auctra review；selected 不等于 accepted，accepted screenplay 也不等于 production-ready。只有 accepted handoff 才交给 Scaena。

## 本地与远程交接

本地使用已安装 Auctra CLI 和对应 Scaena owner CLI；远程使用 MCP `tools/list`、search 的 `input_schema`、capabilities/resource 与 HTTP invoke/input/download。远程客户端无需安装 CLI，不传服务端绝对路径、target directory、shell 或 actor 字段；ref 必须受 work scope 约束，长任务用原 run ref status 回查。生成、accept、apply、saved version、export/download 和 production acceptance 分开；服务不可用或能力未注册时返回 `capability_missing`/`unregistered`，不伪造 receipt、不另建同名作品。

## 边界

- 不生成 `workspace_recipe.v1`、`layout.v3`、layout manifest、必填 frontmatter 或完整空目录骨架。
- 不运行 layout plan/apply/ensure 作为写作前置；历史 layout 文件不决定作者文件位置。
- 不把普通 Markdown 当成完整生产剧本；既有 episode/scene/room/accepted handoff 合同保持。
- Auctra 不调用 Scaena，不修改 `.scaena`，不生成镜头或资产；Eikona 只拥有视觉 artifact；Scaena 负责 ProductionGraph、生产接受、装配和交付。
- 不直接创建、移动或编辑 `.auctra/**`、`.scaena/**`、SQLite、manifest、receipt 或 review decision。

## 验证

```bash
python3 scripts/validate_skills.py
python3 ai-drama-router/scripts/validate_drama_matrix.py
```
