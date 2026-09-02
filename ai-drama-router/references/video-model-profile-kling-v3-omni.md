# Kling V3 Omni 做剧能力档案

事实源：

- [Kling 官方开发者入口](https://kling.ai/dev)
- owner-pinned relay catalog：channel 60（仅 transport/catalog 事实）

`family=kling_v3_omni`，`variant=v3_omni`，当前 maturity 为 `contract_declared`，且
`production_ready=false`。V3 Omni 与 Kling V3 必须作为两个独立档案、独立家族过滤项。

## 高层能力声明

- 多图参考；
- 元素参考；
- 视频参考。

## 明确 unknown

精确引用上限、时长、分辨率、wire mode、输出容器、音频和视频-only reference 转换规则均为
`unknown`。relay transport 不是生产能力证据。

## 零调用阻断

当输入为 video-only reference，而 owner 未钉版 wire mode 时，必须返回 typed
`owner_capability_unverified`，不得猜成 text-to-video、image-to-video、抽帧或其他转换；阻断
发生在 credential lookup 和 HTTP 之前。
