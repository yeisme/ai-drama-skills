# 视频模型社区研究快照（2026-09-01）

`signal_type=research_signal`。本快照只在用户明确请求“比较、社区趋势、研究”时加载；正常做剧
路由、eligible family、suggested family、capability maturity 和 `production_ready` 均不得消费
这些值。

## 查询与观察

观察日期：2026-09-01。GitHub 使用 exact-code 搜索；YouTube 使用各模型名称的搜索结果前 8 条
聚合播放量。数值是时间点观察，不是总体份额或质量排名。

| 平台 | 查询式/样本 | H3 | Wan | Seedance | Kling V3 | Kling Omni |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| GitHub exact code | exact family/model token | 18,944 | 543 | 358 | 5,616 | 1,808 |
| YouTube | 搜索结果前 8 条播放量聚合 | 246,734 | 96,230 | 550,984 | 1,276,941 | 未单独拆分 |

MiniMax-H3 官方仓库的同日观察值为 7,625 stars / 507 forks。

## 可用性与偏差

- Bilibili：只保留主题标签与重复上传、课程 SEO、标题蹭词偏差；不生成跨平台排名。
- Twitter/X：认证检查失败，未形成可复核样本。
- Reddit：当前环境无可用登录态 backend。
- 小红书：当前环境无可用 backend。
- 赞助内容、联盟营销、课程引流、查询词、语言、地域、发布时间与搜索排序都会改变样本。
- GitHub exact-code 命中可能包含 README、vendor、镜像、教程和重复引用；star/fork 会持续变化。
- YouTube 播放量偏向发布时间更早、标题优化和频道体量，不能推导模型质量、生产稳定性或成本。

## 禁止用途

不得用本快照：

- 给模型家族排序、评分或破能力平局；
- 提升 `contract_declared`、`local_fixture_verified` 或 `production_ready`；
- 生成 exact model、channel、价格、credential 或 provider payload；
- 替代官方文档、owner-pinned catalog、离线 fixture 或 provider canary evidence。
