# Kling V3 做剧能力档案

事实源：

- [Kling 官方开发者入口](https://kling.ai/dev)
- owner-pinned relay catalog：channel 60（仅 transport/catalog 事实）

`family=kling_v3`，`variant=v3`，当前 maturity 为 `contract_declared`，且
`production_ready=false`。

## 已声明事实

- text-to-video；
- image reference；
- first/last frames；
- owner catalog 存在 relay channel 60 声明。

## 明确 unknown

精确时长、分辨率、引用上限、原生音频、多镜头数量和 4K 能力在官方文档或 owner catalog
证据未钉版前保持 `unknown`。产品宣传、relay 注册或社区演示不能把它们提升为确定合同，也
不能提升 maturity。

## 路由规则

只有镜头硬要求落在已声明事实内时才能进入 `eligible_model_families[]`。任何依赖 unknown
字段的 route 都必须返回 capability blocker 或保留其他已验证家族，不做猜测转换。
