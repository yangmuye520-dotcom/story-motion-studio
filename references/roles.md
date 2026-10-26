# 七项必须执行的契约

七包都必需。root由STORY_MOTION_UPSTREAM或本机配置upstreamRoot指定，默认用户技能根/video；lemo实际库由lemoLibrary或LEMO_OPUSCAR_LIBRARY指定。mg没有SKILL.md也可用，但必须有实际demo源码。

| 来源 | 实际读什么 | 必须做什么 | 输出 |
|---|---|---|---|
| wtt | story-and-timing.md、material-review.md | 按阅读/动作编译整数帧，保存素材历史 | timeline.json、素材锁 |
| lemo | 实际库DIRECTOR.md | 主体目标、具体转折、结尾回扣，三者对应当前镜头 | story-arc.json、TREATMENT.md |
| huashu | t1_3b1b语法或适合内容的原卡、原生storyboard_lint.py | 对象接续写入源码；原生lint真实运行 | object-map.json、镜头表.md、qa/huashu-native.json |
| shotcraft | 实际采用的shots配方或final-review.md审片原则 | 适合内容的镜头动机/运动，独立审片 | shot-plan.json、release-review.json |
| dashi | 讲解动画通用规则.md | 确定实际字阶/语义色/观看尺寸/阅读预算，对比度检查 | visual-contract.json |
| mg | demos/08-morph/index.html或确切选用demo | 形变、点映射、固定时间函数等可定位实现 | scenes.js |
| xilo | craft-rules.md及对应渲染源码 | 实际关键帧、乱序一致、连续段与完整解码 | qa/preview-report.json、candidate-report.json |

用法：`integrations.py read --skill <包名>`读真实资料；再`record <项目> --skill <包名> --source-key <来源键> --quote <真实12字以上片段> --artifact <表中成果> --anchor <成果内8字以上定位> --decision <本片具体决策> --kind guideline-applied|code-adapted|native-tool`。

引用片段必须真实存在，成果内容和哈希必须对应当前版本。源码改了就重新检查、更新受影响记录。source-lock.json只存来源标识和哈希，不夹带本机路径。

结构/哈希不能证明模型确实理解或画面好看，七项报告仍需人工/独立审查核对语义。技能是工作流和代码包，不是七个API模型；仅采用某项方法就如实说方法应用，不声称运行全部渲染器。

本包维护单一渲染后端，七项通过适配共同影响同一工程。用户指定的风格与声音优先，产品配方不强行改变科普题材，不因某包通常带配音就新增旁白。
