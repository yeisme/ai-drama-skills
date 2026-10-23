# 设计：剧本启动、作者路由与远程交接

## Context

`ai-drama-router` 是唯一做剧入口，现有 `manga-drama-project-starter` 同时承担 recipe/layout 目录策略。批准设计要求目录与创作能力脱钩：Agent 维护普通作者内容和 AGENTS 说明，Auctra/Scaena 各自维护机器状态；剧本 canonical 归 Auctra，生产交接和 ProductionGraph 归已批准 owner。

## Decisions

### 1. Starter 退出 recipe/layout

`manga-drama-project-starter` 的交互改为：

1. 读取已有项目和 owner 状态，不把缺少 `.auctra`/`.scaena` 解释为内容不存在。
2. 只创建当前实际要写的剧本、资料或大纲目录；不生成 workspace recipe、layout manifest、必填 frontmatter 或空目录骨架。
3. 在普通 `AGENTS.md` 写明当前文件、先读什么、正式稿/待审稿/历史区别和继续方法。
4. Auctra/Scaena 机器状态、review、version、receipt、ProductionGraph 仍只能经各 owner service/CLI 修改。

不把 `screenplay` 当一段普通 Markdown 就宣称完整生产；既有 Scene/episode/room/accepted handoff 合同保持。

### 2. 剧本作者动作与最小路由

所有剧本请求先进入 `ai-drama-router`，然后按目标选择一个 primary：

- 启动/项目 intake：starter 只负责普通文件入口和 owner handoff；canonical/production gate 由 owner 检查。
- 资料：`ai-drama-context-pack-builder` 或既有资料/素材方法，最小 `DramaContextPack`，不把历史资料默认带入正文。
- 写作：官方 scene/story/showrunner 模板或已有 scene writer；场景必须可表演，整集正文为主，场景引用整集 AST/source span。
- 审稿/修订：`ai-drama-assessment`、continuity、naturalness 或对应 review 方法按需加载；候选未审不能改 canonical。
- 整理/交接：输出 refs、digest、owner handoff；不调用生产、不冻结资产。

一次只选一个 primary，最多一个兼容约束；不批量启用全套做剧 Skills。剧型/时长/媒介缺失且会改变结构时返回 `needs_format_decision`，不猜平台。

### 3. Local/remote Auctra owner routing

- **本地：** 使用既有 CLI，按 work/ref/discovery 定位文本，候选经 review；accept、apply、saved version、export 分离。Auctra 是 canonical screenplay owner，Scaena 只消费 accepted handoff。
- **远程：** 通过 tools/list、search `input_schema`、authoring capabilities/resource 和 HTTP invoke/input/download；ref 必须 work-scoped，长任务异步 status 回查；不传 owner shell、服务端绝对路径、target directory 或权限字段。客户端无需安装 CLI。
- 生成 ≠ accept；selected ≠ accepted；accepted screenplay ≠ production-ready。服务不可用时报告 `capability_missing`/`unregistered`，不伪造 receipt、不另建同名作品。

具体 action/schema、授权、长任务、输入和完整下载由 Auctra target contract 提供；本 change 不复制 service implementation。

### 4. Owner boundaries

`ai-drama-router` 继续宿主无关；不得出现 Yeisme 私有 profile/runtime 路径或产品 Owner 名称。Auctra 持有 canonical screenplay，Scaena 持有 ProductionGraph/production acceptance，Eikona 持有 visual artifact；本 change 只写 portable guidance 和 handoff。剧本 profile 最终只常驻 router 与 Auctra runtime；宿主 manager 后续按 profile contract 修改。

### 5. Validation

先完成 change artifacts，再由 drama owner 运行 `python3 scripts/validate_skills.py`、`python3 ai-drama-router/scripts/validate_drama_matrix.py` 和 strict change validation。实现阶段不得跑服务、真实生产、付费 provider 或跨 owner 集成；integration dependency 为 root 五 change gate + Auctra service contract。
