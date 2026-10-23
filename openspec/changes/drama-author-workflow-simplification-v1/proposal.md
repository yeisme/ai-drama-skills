# 变更提案：剧本作者工作流简化

## Why

AI Drama Skills 当前的项目启动器仍描述 recipe/layout 物化，且作者侧没有把剧本启动、资料、写作与远程 Auctra owner 路由收敛为自然的作者动作。批准计划要求剧本仍由 `ai-drama-router` 作为唯一入口，canonical screenplay 仍归 Auctra，生产和资产 owner 不变；Skills 只提供最小创作路由和交接指导。

## What Changes

- 将 `manga-drama-project-starter` 改为读现有项目、只创建实际需要的普通目录，并在 AGENTS.md 记录当前文件、先读资料、正式稿/待审稿/历史和继续方法；退出 recipe/layout 生成和自动目录脚本。
- 明确剧本启动、资料整理、写作、审稿、修订与整理仍由 `ai-drama-router` 路由到最窄已有方法，剧本正文唯一 canonical owner 为 Auctra；不把 Markdown 草稿当完整生产状态。
- 在剧本侧运行指导中增加 local/remote Auctra 路径：本地用 CLI，远程只用 tools/list、search schema、capabilities/resource、HTTP 输入/下载与状态回查；客户端不安装 CLI、不访问服务端路径。
- 保留 `ai-drama-router` 宿主无关和 Scaena/Eikona/ProductionGraph 所有权边界；不改变 production owner，不新增第二个场景正文或生产数据库。
- 明确 profile 目标：剧本创作 profile 仅常驻 `ai-drama-router`、`yeisme-auctra-cli-runtime`；profile/runtime 修改交给宿主 manager，非本 change 直接修改。

## Non-Goals

- 不实现 Auctra/Scaena/MCP/HTTP 服务，不修改产品代码、canonical screenplay、ProductionGraph、资产 bytes 或运行数据库。
- 不手改 `.agents/skills`、`.claude/skills` 或 profiles。
- 不删除剧本专项能力；只退出常驻并按需加载。
- 不新增 CLI、存储模型、渲染引擎或第二份场景正文。

## Success Criteria

1. starter 不再要求 recipe/layout，按实际内容工作并写普通 AGENTS 说明。
2. 剧本 startup/material/writing/remote owner 路由和 canonical/production 边界有可执行合同。
3. 所有实现任务未勾选，strict validation 通过后才进入 source implementation。
4. `ai-drama-router` 仍唯一剧本入口，专项 Skills 仍可按需读取。
