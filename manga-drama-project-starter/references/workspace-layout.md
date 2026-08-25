# 漫剧工作区角色

初始化只物化 base roles，其余目录由阶段 Skill 通过 `auctra project layout ensure` 创建。

| machine role | en-US | zh-CN | base |
| --- | --- | --- | --- |
| `screenplay_root` | `screenplay/` | `剧本/` | yes |
| `planning_outline` | `screenplay/outline/` | `剧本/大纲/` | no |
| `story_bible_characters` | `screenplay/characters/` | `剧本/人物/` | no |
| `story_bible_world` | `screenplay/world/` | `剧本/设定/` | no |
| `story_continuity` | `screenplay/continuity/` | `剧本/连续性/` | no |
| `screenplay_episodes` | `screenplay/episodes/` | `剧本/分集/` | no |
| `screenplay_scenes` | `screenplay/scenes/` | `剧本/场景/` | no |
| `materials` | `materials/` | `素材/` | yes |
| `review_exports` | `reviews/` | `审稿/` | yes |
| `exports` | `exports/` | `导出/` | yes |

迁移映射：`outline/` 与 `大纲/` 进入 outline role，`人物/`、`设定/`、`伏笔/`、`scenes/` 分别进入 characters、world、continuity、scenes。未知目录保持原位。
