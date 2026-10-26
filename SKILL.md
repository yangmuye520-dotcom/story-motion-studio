---
name: story-motion-studio
description: 协同七个必需的本地视频技能制作故事型科普、流程解释和独立结构代码动画，复用已认可样例并交付文稿、分镜、HTML与MP4。用于“故事动效工坊”“七个技能一起用”“按固定样例做视频”；只要文稿或分析时完成相应阶段，不假称七项已全执行。
---

# 故事动效工坊 v2.3

用户用法见 [README](README.md)，本文件是AI执行入口。维护包结构时读[目录说明](docs/structure.md)，用户安装或迁移时读[环境指南](docs/setup.md)

## 必须保留的制作约束

- 每条完整成片必须有七个上游的实际贡献，同一工程采用方法、代码和必要工具；缺项不能退回独立生产模式，也不把指南应用说成执行了整套引擎
- 当前用户不允许新造环境场景，采用独立对象、图表、文字和结构；三维不扩展成环境。先读[当前用户约定](references/user-preferences.md)，其中保留范围及被叫停项目
- 已有本片要求直接采用。默认选择见用户约定，用户明确修改优先；只做文稿、分析或局部修改时止于对应范围，不为凑七项运行无关工具
- 素材和审片记录如实描述来源、授权依据与实际检查范围，技术成功不等于用户认可或审美通过

## 1. 检查依赖，建立项目

读取需求、附件、参考及现有工程，区分本片要求和历史选择

- `python <技能目录>/scripts/integrations.py doctor`：核对七包真实文件、lemo实际`DIRECTOR.md`与mg源码；空目录不算齐全
- `python <技能目录>/scripts/studio.py doctor`：探测运行环境。缺项先定位或恢复，准确说明受影响阶段，不静默替换必要来源
- 新片用 `studio.py init <新项目>` 创建独立目录并绑定来源；不覆盖已有工程或成片
- 保存 `brief.md`，时长按内容、动作和阅读预算决定

完成：目标明确、实际依赖齐全、新项目和`integration/source-lock.json`可用

## 2. 内容设计与七项采用

制作前读[七项契约](references/roles.md)和[内容分镜](references/story.md)。用 `integrations.py read --skill <完整包名>` 读取真实资料，再按上游指针选择相关细节

- 讲稿和分镜保存到`script.md`、`storyboard.md`、`TREATMENT.md`；关键断言映射到`sources.md`，区分事实、示意与未知
- 科普围绕具体问题解释机制并回到应用；流程片追踪同一输入的连续变化。无配音时主叙述仍完整，辅助标签不承载关键论证
- `film.json`作为时序源，compile生成`timeline.json`。每镜明确目的、前态、动作、后态、构图、承接、图文对应与阅读时间；漂移、缩放和粒子不等于新增信息
- 另写huashu格式镜头表并实际执行`integrations.py native-lint <项目>`，修正红灯，主叙述和短标签不混用以规避检查
- 七项分别留下契约规定的实际成果，用`integrations.py record`绑定真实片段、具体决策、成果定位和哈希；`execution.md`区分指南应用、代码适配与原生工具执行

完成：故事和知识闭合，七项可从真实来源追到当前成果；缺项、空记录或源码变化未重查不能正式交付

## 3. 样例选择与固定风格

读[已认可风格](references/approved-styles.md)和[风格锁](references/style.md)，打开`examples/index.html`查看样例与真实状态

- 三套已认可资源在`assets/styles/`，完整工程在`examples/approved/`。读取profile并观看对应preview，再参考实际镜内代码和依赖；不只复制配色
- 指定哪套就沿用哪套；未指定则按内容选择已有认可风格并简述理由。没有认可方向时先出连续短样，用户明确委托代选按委托执行，沉默不算认可
- 沿用原三条参考时读[参考基准](references/reference-benchmarks.md)，用`examples/compare.html`对照。原片是参考材料，不当作本包生成结果
- 字体、配色、组件、运动与转场沿用，故事、数据与构图按本片改写。用户认可或明确委托后style-lock/export-style，风格包放`assets/styles/<id>`，保留依据与版本
- 入库或改变样例状态时读[样例管理](references/examples.md)，用samples.py记录真实决定，保留否定历史，旧技术片不自动升为认可样板

完成：风格依据可观看且可追溯，当前画面遵守最新限制，旧贡献记录不冒充新片执行

## 4. 预览、导出与独立终检

执行前读[制作命令](references/production.md)和[验收](references/review.md)

- 素材记录来源、许可与使用依据，首锁assets seal；后续替换走propose、现有真实授权、accept并保留历史。指定BGM实际取用核验，收费先说明获授权
- renderFrame只依赖时间与固定素材，主体动作对应讲解，读字稳定、对象连续。真人或真实运动需要对应素材或模型，不承诺代码绘图肉眼难辨
- `render --preview --draft`检查过程关键帧；`render --draft`仅为技术片，准确记录七项缺失和候选状态
- 当前七项、素材与风格通过后，正式render只生成`candidate.mp4`，不直接发布final
- 按video-shotcraft要求，委派未参与制作的审查者实际审当前候选，不提供预设结论。release-review记录视频哈希、具体观察、阻断项、实际抽样和观看/试听范围
- 修复阻断项，重渲或复审受影响部分；`integrations.py release`通过当前来源、成果、版本与独立审片校验后才发布`final.mp4`

完成：真实MP4、可改完整工程、文稿分镜、来源许可、七项采用、素材历史、风格依据和检查报告可交付；链接先验证，localhost仅本机使用

用户反馈继续回到对应源头修订，HTML与MP4的使用和排错见[运行修改指南](docs/editing.md)

公开发布版：样例为去音轨展示副本，不含原片与历史报告；认可记录仅表示原用户的视觉选择，新用户先用连续短样校准，不推定其认可
