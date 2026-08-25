# 创作 artifact 生命周期

## 目的

把“写什么格式”“文本目前是什么身份”“放在哪里”“能否继续扩写”“是否已经被接受”拆开。它们是五个不同问题，任何一个都不能替另一个作答。

## 独立字段

```text
output_format:
  markdown | screenplay | fountain | plain_text | host_native | other

artifact_disposition:
  preview | candidate | canonical_proposal | export

persistence_policy:
  chat_only | os_temp | review_workspace | canonical

batch_policy:
  proof_slice | bounded_batch | full_scale

acceptance_state:
  unreviewed | selected | accepted
```

`output_format` 只描述交付形态。用户说“写成 Markdown”时，不得据此推断需要写入仓库、项目目录、review workspace 或 canonical owner。

## 状态语义

- `preview`：用于判断方向，不保证进入候选集。
- `candidate`：可被比较、选择或修订，但仍不是 canonical。
- `canonical_proposal`：已准备交给 story owner 审核的提案；没有 owner receipt 时仍非 canonical。
- `export`：从已获授权的 source 生成交付物；export 本身不改变 source acceptance。
- `unreviewed`：用户或 owner 尚未选择。
- `selected`：用户选择了一个候选，可进入 review；不等于接受为 canonical。
- `accepted`：只有 canonical owner 的显式 accept action/receipt 可以产生。

## 默认决策

| 请求 | disposition | persistence | batch | acceptance |
| --- | --- | --- | --- | --- |
| 单个方向试写 | `preview` 或 `candidate` | `chat_only` | `bounded_batch` | `unreviewed` |
| 超过 5 集的新写/大改 | `candidate` | `chat_only`、`os_temp` 或 `review_workspace` | `proof_slice` | `unreviewed` |
| 用户选择 candidate B | `candidate` 或 `canonical_proposal` | `review_workspace` | 保持当前值 | `selected` |
| story owner 明确接受 | owner 决定 | `canonical` | 可进入下一批 | `accepted` |
| 用户只要求 Markdown | 保持原值 | 保持原值 | 保持原值 | 保持原值 |

## Proof slice expansion gate

超过 5 集时，默认先完成 3 集 proof slice，每集一个核心场景、至少两个策略差异明确的候选。只有同时满足以下条件，才可进入每批最多 5 集的 `bounded_batch`：

1. 每个核心场景都有可观察的 entry→exit 状态变化；
2. 确定性结构检查没有 blocking finding，语义证据缺失如实标为 inconclusive；
3. Dialogue Live Test 显示至少两个主要人物的声音不可互换，并出现策略变化、回避、打断或动作承担信息；
4. 用户明确选择或认可至少两个主要人物的声音；
5. 每个场景最多执行一次有界改写；仍不成立则返回 scene contract；
6. 未选候选继续保持 `chat_only`、`os_temp` 或 `review_workspace`，不得进入 canonical context。

`full_scale` 只在连续批次证据稳定且用户明确授权时可用，不能由“继续”“全部写完”或文件格式要求自动触发。

## Owner action

- `keep_preview`：留在当前临时位置。
- `request_selection`：呈现候选差异并等待用户选择。
- `promote_for_review`：把 selected candidate 交给宿主 review workspace；仍为 pending review。
- `accept_canonical`：仅 canonical owner 可执行。
- `export_from_accepted`：从 accepted source 导出。
- `discard_unaccepted`：只清理精确指向的未接受 artifact，不触碰 canonical。

## 禁止推断

- Markdown 文件存在 ≠ 用户认可内容。
- 用户选中 ≠ story owner 接受。
- 聊天历史、模型记忆或已删除文件 ≠ accepted source。
- 评分为 `ready` 但没有绑定证据 ≠ expansion gate 已通过。
- A/B 只有同义措辞差异 ≠ 两个候选。
