---
name: story-motion-studio
description: 协同七个必需视频技能制作故事科普、流程解释与独立结构动画，以统一分镜驱动HyperFrames中文工作台，交付文稿、HTML和MP4；分析或局部修改只完成指定范围
---
# 故事动效工坊 v7

用户入口见 [README](README.md)，新后端与迁移见[HyperFrames 接入](references/hyperframes.md)，协同与验收见[统一分镜](references/shared-production.md)

## 当前范围

完整片实际采用七个来源，不能只列名字。它们是指导资料、代码和工具，不是七个视频模型。每项贡献对应当前镜头与真实成果；不能复制旧片报告、为了调用数量硬塞动作或让七项各产一段再拼接

本用户当前优先精细二维图解、文字、图表和独立对象，不新造人物与环境场景、不追求三维材质，默认中文屏幕讲解、无旁白、免费工具、16:9横屏、画面文字不加句号。用户本次明确要求优先，其余约定见[用户偏好](references/user-preferences.md)

## 新片用 HyperFrames

1. 检查 scripts/integrations.py doctor 与 scripts/hyperframes.py doctor --json，区分必需故障和未采用的可选组件。先读四个官方核心技能 hyperframes、hyperframes-cli、hyperframes-registry、media-use；按需读引用。运行时放技能目录外，固定版本，不隐式升级或调用收费服务
2. 用 hyperframes.py --project PARENT init NEW_NAME 创建新工程，自动绑定七个来源、生成统一计划入口与视觉锁；不覆盖旧目录。explanation.json 是唯一内容源，storyboard.md 由 hf_pipeline.py board 生成。读[讲解质量](references/explainer-quality.md)，写清每镜“讲什么、哪个对象怎样变化、因此明白什么”、事实依据、阅读停留和下一镜承接
3. 用 integrations.py read 读取七项真实资料，按[协同分工](references/shared-production.md)影响同一工程。wtt管信息与时序，lemo管问题推进与回扣，huashu管对象变化，shotcraft管镜头节奏与独立审片，dashi管视觉和阅读，mg锚定实际动效代码，xilo管实际检查与导出证据。先完成共同计划再记录贡献，不能启动多个竞争时间线
4. 默认使用 assets/templates/engineering-2d-v1 的暗色精细二维模板；init 自动复制真实CSS、字体和动作源码并建立锁。读[风格选择](references/approved-styles.md)与[动作模块](references/mechanism-modules.md)，新工程读[自动选动作与跨镜对象](references/action-routing.md)，按资料含义建立contentFacts，选择24项中的family，用MotionActions.add接入唯一暂停时间线；登记objects、每镜objectStates和真实HTML标记，声明跨镜transfers，运行motion.py compile从分镜生成调用块，再运行motion.py trace，不能仅凭对象名称相同认定连续。用户要求柔和渐入渐出或柔和渐显叙事时，读[渐显模块](references/soft-reveal.md)，使用包内SoftReveal接入唯一时间线；用户选择爱情样片或暗色宋体叙事时，读[暗色宋体叙事](references/editorial-serif.md)，将包内视觉层应用到同一HyperFrames工程，按画幅重排并先审核心动作样片，不冒称init自动装配；黑金＋三维结构＋粒子仅为可选风格，浅色冻结参考保留。参考认可不等于新片或新增动作认可，风格变更先做连续样片确认
5. 先交付文稿、统一分镜与连续10秒样片，包含实际对象变化、阅读停留和一次承接。用户确认前止于样片；明确委托直接整片则按委托范围执行。preview 自动应用包内中文界面补丁，不进入预览iframe、不改用户正文、源码或文件名；冷门第三方诊断保留原文
6. 沿同一视觉系统扩展，按拆分归并、队列并发、局部更新、双路对照等知识关系选择动作，不用重复入场代替机制，不要求每片用齐模块。HF每个组合一个暂停GSAP时间线，所有状态由时间确定；查询组件库后按需复用，没有合适项再自己实现。素材本地化并登记来源和许可，指定BGM使用真实来源，不自动继承参考音乐
7. 用 hf_pipeline.py audit 做原生检查、实际运动采样、正反取样一致性和审片图；record 记录七项真实贡献，coverage核对当前版本。candidate 实际渲染并检查尺寸、帧率、帧数、时长、音轨和完整解码。原生警告逐项处理，不用总分掩盖问题
8. 按 content、continuity、readability、export 四项分别独立审查，实际全速观看；有音轨则实际听音。缺少理解测试标 unverified，不把分析音量当试听。检查、候选、素材与分镜绑定当前哈希，修复阻断项后 hf_pipeline.py release 发布final.mp4；integrations.py check/release 会按后端路由。字段和哈希不能证明审美、事实或理解，审查要有具体镜头证据

冲突优先：事实与讲清楚 → 阅读和连续性 → 已认可视觉系统 → 动效表现 → 单项技能一般偏好。不能为了满足七项把画面弄乱

## 既有工程与维护

旧 Canvas 项目继续 studio.py 路线，原角色契约、素材锁与发布检查不降级，不自动迁移。新片不再维护 film.json 等竞争内容源；旧片的 film.json 继续有效

只做分析、文稿或局部修改时完成指定范围，不自动重做整片、发布或上传。修改前检查当前文件和用户已有改动

样例入库才读[样例管理](references/examples.md)。历史失败、执行日志与重运行时留在项目或外部备份，不塞回技能安装目录；轻量汉化补丁和已认可参考保留在assets。未请求时不更新GitHub
