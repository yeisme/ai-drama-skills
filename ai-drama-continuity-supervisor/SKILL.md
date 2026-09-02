---
name: ai-drama-continuity-supervisor
description: Use when checking or repairing AI drama continuity across characters, identity, costume, props, space, time, action direction, lighting, sound, subtitles, and episode versions.
---

# AI Drama Continuity Supervisor

## 目标

把连续性当成 production gate，而不是生成后凭感觉检查。跨镜头的角色、服装、道具、空间、时间、动作、光线、声音和字幕必须能从事实 refs 推导。

## 工作流

1. 读取 `references/continuity-evidence.md`，再读取 CanonSnapshot、SubjectVersion、StyleVersion、Scene/Shot refs 和已接受 artifact。使用 Seedance 2.5 时还读取 `../ai-drama-router/references/seedance-2-5-capability-profile.md`，把 task policy、reference ordinal、source range、output/audio policy 与 capability maturity 纳入 evidence。
2. 建立 continuity matrix：事实、来源、适用镜头、前后状态和检查结果。
3. 区分 `pass`、`warn`、`block`、`unknown`、`stale`，不要把 unknown 当 pass。
4. 给出最小 repair proposal：重新绑定、局部重抽、改镜头、改时间线或请求人工确认。
5. 输出 finding/evidence，不直接修改 canonical state 或接受资产。

## 必须阻塞

- 主体身份或服装无法确认；
- 关键道具、伤口、位置、时间或动作方向冲突；
- subject/style/reference/preflight 版本过期；
- artifact 缺少 digest、来源或 owner receipt；
- 音画字幕时间无法复算。
- task mode、ratio/duration lock、reference ordinal/count 或 capability digest 与生成 receipt 不一致；
- provider 原生音轨尚未独立审听，却被 visual pass 或 container success 带成 audio pass。

## 验证

```bash
python3 scripts/validate_skills.py
```

涉及 Scaena continuity、artifact lineage 或 production gate 时，进入 Scaena Owner 仓库运行其公开的 focused architecture 与 integration checks。
