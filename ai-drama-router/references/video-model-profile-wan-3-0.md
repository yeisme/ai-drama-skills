# Wan 3.0 做剧能力档案

事实源：

- [Wan 3.0 API](https://help.aliyun.com/zh/model-studio/wan3-video-generation-api-reference)
- [Wan 3.0 指南](https://help.aliyun.com/zh/model-studio/wan3-video-generation-guide)

`family=wan`，`variant=3.0`，当前最高 maturity 为 `local_fixture_verified`。Wan 使用单一
All-in-One async endpoint，provider 可自动判断任务意图；Scaena 仍必须在联网前拒绝明显
非法的素材组合。

## 能力合同

- prompt ≤20,000 字符；输出时长 2–30 秒；480P / 720P / 1080P。
- 支持 text、first/last frames、multimodal reference、file、link、edit、extend。
- reference images ≤10、videos ≤5 且总时长 ≤15 秒、audios ≤5 且总时长 ≤15 秒；混合素材
  总数 ≤20。
- `reference_*`/file/link 与 first/last-frame 互斥；file 与 link 互斥，并且最多一个。
- `prompt_extend` 是 canonical 输入和 wire 字段。旧 `enable-thinking` 只在新字段未显式设置时
  作为兼容别名；wire 不发送 undocumented `enable_thinking`。

## 做剧适用能力

- 20–30 秒长镜、复杂多模态参考；
- 从文档或网页上下文形成视频 brief；
- 视频 edit/extend 与自动意图路由。

## 门禁与回退

- edit/extend 需要 reference video；frames 只接受 first/last；text 不接受媒体。
- file/link 未启用 `prompt_extend` 时阻断。
- provider 自动判断不等于可跳过本地 task policy；非法组合必须保持 0 credential lookup、
  0 HTTP。
