# MiniMax H3 做剧能力档案

事实源：

- [MiniMax Video Generation](https://platform.minimax.io/docs/guides/video-generation)
- [MiniMax-H3 官方仓库](https://github.com/MiniMax-AI/MiniMax-H3)

`family=minimax_h3`，`variant=h3`，当前最高 maturity 为 `local_fixture_verified`。
本档案不声明远端 quota、价格、可用性或 `production_ready`。

## 能力合同

- 输出时长 4–15 秒，整数；分辨率 768P / 2K。
- first/last-frame 共 0–2 张；reference images ≤9、videos ≤3、audios ≤3，混合素材总数 ≤12。
- reference video 总时长 ≤15 秒；reference audio 总时长 ≤15 秒。
- text、reference、frames 是普通生成 task policy；first/last-frame 归 `frames`，不得与普通
  reference 混用。
- generation topology 固定为：可选 `context-ir` → 必需 768P `generate` → 可选 2K
  `regenerate`。
- 2K regeneration 必须绑定 source task、原输入 digest、source resolution=768P 和唯一
  `base_video`；它不是普通 create retry，也不得接受已漂移输入。

## 做剧适用能力

- 动作、相机、构图、声音节奏等混合参考；
- 首尾帧之间的可控过渡；
- 先以 768P 通过导演/连续性审查，再对入选镜头做 2K 精修。

## 门禁与回退

- 混合引用、总时长或 frame/reference 互斥不合法时，联网前阻断。
- 2K lineage 不完整时返回 typed blocker，不降级为普通 retry。
- 若无需混合参考或 2K lineage，保留其他 eligible family，Router 不因社区热度优先 H3。
