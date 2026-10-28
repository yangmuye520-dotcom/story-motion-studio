# 七项围绕同一张分镜表工作

explanation.json 是唯一内容源；storyboard.md 由 hf_pipeline.py board 生成，不手工维护另一份台本。视频文字来自同一份 claim，写入 HTML 后用实际预览核对。每镜包括：

| 字段 | 要回答的问题 |
|---|---|
| id/start/duration/visibleSeconds | 哪一镜，何时出现，留多久阅读 |
| claim | 这一镜讲什么，画面文字不加句号 |
| object/outObject | 追踪哪个对象，给下一镜留下什么 |
| before/action/after | 原来怎样，怎样改变，最后怎样 |
| meaning/evidence | 观众因此理解什么，有什么资料或可见证据 |
| handoff/transition | 与上一镜的因果或对象关系，如何连续承接 |
| reading/focus | 怎么安排阅读，一次突出哪个变化 |
| implementation | 实际 HTML 元素 id；不能只在文档声称有动画 |

保留 explanation_check 的结构字段；HF 完整流程增加 evidence、reading、transition、fps、width、height，audioRequired 默认为true。参考 scripts/hf_pipeline.py 的 plan 校验；初始空计划不能通过检查

## 分工及冲突处理

| 来源 | 修改同一份计划的哪些部分 |
|---|---|
| wtt | claim、时序、阅读安排、素材事实；不能另起动画工程 |
| lemo | question、takeaway、carrier、每镜推进与回扣；不强塞虚构故事 |
| huashu | object、before/action/after、meaning、handoff；具体到真实元素 |
| shotcraft | focus、transition、镜头动机，最后安排独立审片 |
| dashi | 实际可读字阶、语义色和布局，与锁定视觉系统一致 |
| mg | 对应镜头的真实 HTML/JS 动效代码；不另行决定整片画风 |
| xilo | 原生检查、乱序取样、实际导出与解码证据；不再开第二套渲染器 |

五项设计贡献都锚定 explanation.json；MG锚定真实实现代码，xilo锚定真实 qa/hf-audit.json。每项记录真实上游引用、当前镜头id、具体决策与成果哈希；不复制旧片采用记录。所有计划修改完成后再记录，计划变更会使旧记录失效

七项都要贡献，但不要求七项都在画面里加东西。需要删除不合适的炫技动作时，删除理由也可成为有依据的设计决策；不能只写“用了某技能”刷贡献

冲突优先级：事实正确与讲解清楚 → 阅读与对象承接 → 已认可视觉系统 → 动效表现 → 各技能的一般偏好。以真实样片比较解决，不以调用数、动画数量、技术总分评价质量

## 已认可的默认二维模板

默认工程使用 assets/templates/engineering-2d-v1，profile和10秒无声参考绑定哈希，CSS、字体和动作入口在init时复制并锁定
原浅色参考保留，黑金结构粒子为可选风格，详情见[风格选择](approved-styles.md)
每镜增加 mechanism.family、selectionReason、observableChange、readingHold，含义和调用见[动作模块](mechanism-modules.md)
新模板计划检查要求这些字段与模板资产存在且匹配，实际动作、跨镜承接和理解仍需真实观看，不能靠字段假通过
旧项目没有templateId时不强行迁移，新项目不能跳过模板装配又声称已沿用默认

## 新工程命令

```text
python hyperframes.py --project PARENT init NEW_NAME
# 填写 NEW_NAME/explanation.json，编写对应 HTML 动画
python hf_pipeline.py board PROJECT
# 先读七个真实来源，在同一分镜完成贡献
python hf_pipeline.py audit PROJECT
python hf_pipeline.py record PROJECT --skill NAME --source-key KEY --quote QUOTE --shots s1 s2 --artifact FILE --anchor ANCHOR --decision DECISION
python hf_pipeline.py coverage PROJECT
python hf_pipeline.py candidate PROJECT
# 实际独立审查后填写 qa/hf-review.json
python hf_pipeline.py release PROJECT
```

来源 KEY 从 integrations.py read 得到。设计五项的 FILE=explanation.json，mg为实际代码文件，xilo为qa/hf-audit.json。引用至少12字，锚点至少8字，决策至少16字；字段长度只是防空记录，不证明决策好坏

## 四项独立验收

- content：事实、讲解顺序、每镜新增信息、结论回扣；来源可核实，没有编造理解测试
- continuity：真实全速连续观看，查看镜内变化和镜间承接，字幕遮住后仍有机制的画面证据
- readability：实际观看尺寸下核对字号、对比度、阅读停留和焦点；不能只看源码字号
- export：实际MP4时长、尺寸、帧率、帧数、音轨与完整解码，候选与审查哈希一致

qa/hf-review.json 要有 videoSha256、candidateReportSha256、independent=true、reviewer、blockingIssues=[]、fullSpeedWatch、audioListening、audienceTest，以及 axes 下上述四项各自的 status/observations/evidence。observations 写具体镜头事实，evidence 为项目内真实文件路径列表。未做目标观众测试写 unverified；不得写成已通过。带音轨时必须有人或具备听音能力的审查者实际听过，不能由音量分析代替

有原生警告时按 section:code 在 warningDecisions 逐项记录保留理由，不能整体忽略。任何阻断项、过期素材/代码/分镜/贡献、缺失审查、未做完整观看或音轨未听都会阻止正式发布；仍可交付明确标记的候选，不能把候选冒称终版

自动程序只能核对证据一致性和技术约束，不能证明审美与观众理解。分镜/审查JSON不能凭声明通过而冒充真实执行

## v7动作与对象契约

新初始化计划带semantic-motion/v1，动作按资料关系选择，24项接口及跨镜对象字段见[动作路由](action-routing.md)
explanation_check会接入semantic_motion检查，board与trace都从同一分镜生成；旧计划不自动改成新契约
