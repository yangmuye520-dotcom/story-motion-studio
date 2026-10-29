# story-motion-studio · 代码讲解视频工坊

把主题或Markdown资料做成连续动态图解，交付 **MP4＋可修改HTML工程＋文稿分镜与来源**
默认中文屏幕讲解、无配音、16:9横屏、1080p、30fps，使用HyperFrames本地预览与导出

[查看风格展示](https://yangmuye814.github.io/story-motion-studio/examples/) · [浏览24项解释动作](https://yangmuye814.github.io/story-motion-studio/examples/motion-library/) · [中文工作台操作手册](docs/chinese-workbench.md)

## 有哪些模板，能稳定输出什么

| 模板或风格 | 适合内容 | 可复用的表现 |
|---|---|---|
| 暗色精细二维 · 默认工程模板 | 流程教学、机制科普、系统与数据解释 | 固定字体与语义色，点线图解、对象追踪、拆分归并、队列并发、局部更新和对照 |
| 柔和渐显叙事 · 可选视觉与动作层 | 情感、观点、概念讲解 | 暗色宋体、细线、稳定渐入渐出、轻位移、逐字错峰、阅读停留 |
| 暗色宋体叙事 · 可选视觉层 | 文字叙事与概念展开 | 冷暖强调、镜内分阶段变化、重点交接与结论汇聚 |
| 浅色精细二维 · 冻结参考 | 明亮清晰的流程讲解 | 保留原二维参考，选择后另建视觉锁 |
| 黑金结构粒子 · 历史样板组合 | 空间结构、聚合与状态变化 | 黑金讲解、独立三维结构和粒子，可按内容选用 |

**稳定复用的是视觉规范、确定性时间线和动作接口，不是任意主题一次出高质量成片**
可选视觉层由Codex应用到同一工程并重排，不是每种风格都有独立init参数
新内容仍先做连续样片，检查内容、连续动作、可读性和实际导出
擅长文字、图表和独立对象解释，不保证逼真实拍、人物舞蹈或动物运动
默认不生成人物或环境场景，不用图片轮播代替讲解

[风格选择细则](references/approved-styles.md) · [渐显动作参数](references/soft-reveal.md) · [内容选动作规则](references/action-routing.md)

## 需要安装什么

| 依赖 | 用途 | 安装方式 |
|---|---|---|
| story-motion-studio | 统一分镜、风格、协作和验收 | 下方安装命令 |
| 七个来源：xilo-opus-video、lemo-opuscar、mg-styles-15、dashi-animationstyle、huashu-art-motion、wtt-code-animation-studio、video-shotcraft | 共同完善同一条视频；mg包含实际动效源码，lemo需实际资料库 | 安装器按锁定提交下载 |
| hyperframes、hyperframes-cli、hyperframes-registry、media-use | HyperFrames制作规范、命令、组件和素材规则 | 第二步让Codex补齐 |
| Git、Python 3.10+、浏览器、基础Python环境与FFmpeg | 下载、绘图和编码 | 第一步安装器准备或定位 |
| Node.js、HyperFrames 0.8.207、Chrome、FFprobe | 新后端运行、检查与导出 | 第二步检查补齐 |

七个来源是指导资料与代码，不是七个视频模型，不各做一段再拼接
默认本地免费工具；AI账户和外部素材可能另有费用，涉及收费先说明

### 第一步：一键安装总技能＋七个来源

Windows PowerShell执行；先查看[安装脚本](install.ps1)，需要可访问GitHub的网络

```powershell
$setup = Join-Path $env:TEMP ("story-motion-" + [guid]::NewGuid().ToString("N") + ".ps1")
Invoke-WebRequest "https://raw.githubusercontent.com/yangmuye814/story-motion-studio/main/install.ps1" -OutFile $setup
powershell -ExecutionPolicy Bypass -File $setup -InstallSystemTools
```

默认位置：`~/.codex/skills/story-motion-studio`，七个来源在`~/.codex/skills/video`
缺少Git/Python时尝试winget安装，可能出现系统提示；无winget先手动安装Git和Python
已有目录或配置时停止防覆盖，**不要当作更新命令重复运行**
只检查安装计划：`python install.py --check`，不联网、不写文件

### 第二步：补齐HyperFrames和中文工作台

**当前一键安装器尚未包含HyperFrames全部依赖**，安装后新开Codex对话发送：

```text
检查story-motion-studio环境，读取references/hyperframes.md
补齐Node.js、Chrome、FFmpeg/FFprobe和hyperframes@0.8.207
安装hyperframes、hyperframes-cli、hyperframes-registry、media-use四个官方技能
运行时放技能目录外，合并本机配置，不覆盖已有字段或隐式升级
应用包内中文补丁，通过中文入口启动，实际检查中文菜单并导出短片
只使用免费本地功能，报告仍缺少的项目
```

完成标准：来源能读取、中文预览能打开、MP4实际导出并可播放，不以文件复制或doctor通过代替验证
[安装路径和配置字段](references/hyperframes.md) · [迁移说明](docs/setup.md)

## 中文工作台怎么打开

仓库已包含 **410项中文词条、界面与报错翻译补丁、中文启动脚本**，运行时另行安装
这是固定版本的本地中文适配，不是官方全量中文发行版，未覆盖第三方诊断保留原文

在PowerShell执行，工程路径替换为自己的已有HyperFrames工程：

```powershell
$skill = Join-Path $env:USERPROFILE ".codex\skills\story-motion-studio"
powershell -ExecutionPolicy Bypass -File "$skill\scripts\preview-zh.ps1" -Project "D:\videos\my-project" -Port 8793
```

打开终端实际输出的地址，服务保持运行；工作台用于预览和编辑，修改后需重新导出MP4
仍是英文时按Ctrl+F5，并核对是否打开了另一端口或另一份运行时
直接npm run dev、其他npx运行时或桌面应用不保证经过本技能汉化入口

**详细安装、配置、启动、刷新、英文界面排查与停止服务，见[中文工作台操作手册](docs/chinese-workbench.md)**

## 开始制作

把下面提示词发给Codex，填写方括号：

```text
使用story-motion-studio制作视频
主题或MD完整路径：[内容]
观众：[谁来看]
看完能够：[理解什么]
重点回答：[核心问题]
时长与画幅：[例如90秒、16:9]
风格：[暗色精细二维／柔和渐显叙事／其他可选风格]
声音：无配音，用中文屏幕文字讲解
BGM：[真实音频或视频路径，没有则先不加]

实际读取七个必需来源，共同完善唯一分镜
按内容选动作，保留跨镜对象与来源，不为特效数量堆动作
通过HyperFrames中文工作台实现、预览与导出
画面文字不加句号，保证阅读时间
先给讲稿、分镜和包含核心动作的10秒连续样片，确认后制作整片
交付MP4、素材齐全HTML工程、文稿分镜、来源和七项实际贡献说明
只使用免费工具，涉及收费先说明
```

流程：资料→讲稿与唯一分镜→HTML与暂停时间线→连续样片→确认扩展→四项检查→MP4和工程
动作依据内容自动选用，缺少容量、数值或比较前提时先补信息，不虚构结论
音乐按本次提供素材使用，不继承参考片音轨，JPG缩略图没有音轨

修改时指出时间段、问题和保留部分，例如：`第20到35秒增加阅读停留，保留其他镜头和BGM，先给局部预览`
[修改工程](docs/editing.md) · [制作与验收规范](references/shared-production.md) · [AI执行入口](SKILL.md)
