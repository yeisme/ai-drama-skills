# 原创性与参考素材策略

## 目的

做剧路由必须先声明原创性模式，再允许 Story、Screenplay、Director、Visual、Audio 或 Delivery 阶段工作。`OriginalityDecision` 只保存可追溯引用、判断和限制，不保存受保护作品全文、原始提示词、provider payload 或完整内部推理。

## 原创性模式

| `originality_mode` | 允许的输入 | 默认动作 |
| --- | --- | --- |
| `pure_original` | 用户原创 premise、事实资料、公共领域事实/通用母题（不继承具体叙事表达）、抽象类型和技术约束 | 从空白 canon 建立人物、世界、情节、对白、视觉和声音身份 |
| `licensed_adaptation` | 有明确授权范围和权利凭据的原作 | 记录授权边界；超出范围的元素按原创重新设计 |
| `reference_constrained` | 构图、节奏、镜头语法、色彩、材质、工艺等可拆解参考 | 只提取维度化约束，不复制角色身份、独特桥段、台词或可识别表达 |
| `transformative_research` | 用于批评、比较、研究的作品或资料 | 产出研究证据与差异化约束，不直接进入可发行 canonical asset |

## OriginalityDecision 最小合同

```text
schema_version: ai-drama.originality-decision.v1
originality_mode
decision_ref
source_refs[]
rights_basis_refs[]
protected_expression_exclusions[]
identity_exclusions[]
similarity_risk: low | medium | high | unknown
differentiation_constraints[]
review_gate
owner
status
```

`source_refs[]`、`rights_basis_refs[]` 和 `decision_ref` 必须是 refs-only。若来源权利、公共领域状态或授权范围未知，不能把状态标为 `ready`。

## `pure_original` 硬规则

### 故事与剧本

- premise、角色关系、人物秘密、世界规则、关键转折、结局机制和标志性对白必须从当前项目 canon 生长。
- 类型惯例可以使用，但不得把现成作品的人物功能、场景顺序、独特冲突链或结局替换少量名词后复用。
- “改名、换脸、换颜色、同义改写、颠倒性别或时代”不构成原创。

### 导演与视觉

- 可以引用景别、镜头运动、光比、材质、色相、节奏密度等抽象维度。
- 不得向 writer 或 provider 传递在世创作者 persona identity、受保护角色身份、logo、水印、独特服装组合或可识别的标志性画面复刻要求。
- `StyleLens` 只保留维度、范围、禁区和来源 refs；专名不进入生成提示。

### 声音

- 角色声线、音乐主题、环境声和 Foley 由项目自身的 `ShotAudioIntent` 与 audio owner 定义。
- 不得要求模仿可识别演员、歌手、角色声纹、旋律或录音；第三方素材必须带权利和许可 refs。

### 交付

- export 前必须复核来源、授权、相似性、logo/watermark、人物身份和音乐权利。
- `selected`、`frozen`、高质量分或用户一句“继续”都不能替代原创性/权利 gate。

## 相似性检查

以下任一情况将 `similarity_risk` 提升为 `medium` 或 `high`，并要求独立 review：

- 角色外形、服装、道具、构图、对白、剧情链或声音中出现多项同时接近同一来源；
- 候选依赖单一作品，而不是来自多个抽象维度或项目 canon；
- 用户要求“像某作品一样，但不要被看出来”；
- 参考素材的权利、来源或公共领域状态无法验证；
- 自动评估只给出审美分，没有 provenance 或差异化证据。

修复动作必须回到对应 owner 产生新的 successor candidate；不得在原文件上做表面替换后继续交付。

## 失败状态

- `needs_originality_decision`：没有选择原创性模式。
- `reference_rights_unknown`：参考素材权利或许可状态未知。
- `protected_expression_risk`：请求依赖受保护的独特表达。
- `style_identity_leak`：人物、作品或创作者身份进入 writer/provider 指令。
- `similarity_review_required`：相似性风险需要人工或独立 review。
- `adaptation_not_authorized`：改编缺少有效授权范围。

这些 blocker 不能被质量分、成本授权、主体冻结、production acceptance 或 export 请求覆盖。
