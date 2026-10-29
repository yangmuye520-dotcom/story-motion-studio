# HyperFrames 本地制作路线

新二维讲解工程优先 HyperFrames 0.8.207，负责 HTML 组合、统一时间线、可视预览、浏览器检查与 MP4 渲染。它不替代七个上游来源，不负责凭空保证文案、审美或事实准确

完整片仍逐项读取七个来源并记录当前贡献；四个新增核心技能 hyperframes、hyperframes-cli、hyperframes-registry、media-use 负责实现、命令、组件检索和素材规则。先读对应 SKILL.md，再按需读引用，不机械加载整个资料库

旧 Canvas 工程继续使用原 studio.py 路线，不自动转换、不混用时间线。新工程通过 scripts/hyperframes.py 创建与操作。每个组合只有一个暂停 GSAP 时间线，所有状态从时间决定；遵守工程 AGENTS.md 和官方格式

init 同时装配默认暗色二维模板、字体、24项统一动作接口及旧版四类源码，见[模板与动作](mechanism-modules.md)，旧项目不自动改动

## 统一安装入口

新电脑执行README的一键安装命令；已有技能和本机配置时执行install.ps1 -InstallSystemTools -CompleteExisting
安装器固定运行时和官方技能来源，准备FFprobe，应用汉化并执行1秒导出解码与中文UI脚本验证
不覆盖已有技能，保留其他本机字段；新电脑运行时在~/.codex/story-motion-studio-runtime/hyperframes，已有配置可保留旧路径
下列手动配置用于排障或自定义位置，不再要求普通用户单独完成第二轮安装

## 手动配置

需要 Node.js、Chrome、FFmpeg、FFprobe。只安装本地免费核心，不安装付费云端、语音模型或头像服务。运行时放技能目录外，固定版本并保留 package-lock.json

在独立运行时目录执行 npm install --save-exact hyperframes@0.8.207，先设置 PUPPETEER_SKIP_DOWNLOAD=true 可复用已有 Chrome。新电脑另用 skill-installer 安装 heygen-com/hyperframes 仓库 skills/ 下上述四个核心技能，并按原安装器安装七个必需来源

合并（不要覆盖已有字段） ~/.codex/story-motion-studio.local.json 中的 hyperframes 对象：cli 指向运行时 node_modules/hyperframes/bin/hyperframes.mjs，node 指向 node 可执行文件。也支持 HYPERFRAMES_CLI 环境变量。运行时不会塞进技能包，也不会隐式自动升级

## 制作命令

在技能 scripts 目录，以下 PROJECT 均为工程绝对路径，PARENT 为已有父目录

```text
python hyperframes.py --project PARENT init NEW_NAME
python hyperframes.py --project PROJECT doctor --json
python hyperframes.py --project PROJECT catalog --query flowchart --json
python explanation_check.py PROJECT
python hyperframes.py --project PROJECT check --json
python hyperframes.py --project PROJECT snapshot --review --json -o review
python hyperframes.py --project PROJECT preview --background --port 8783
python hyperframes.py --project PROJECT render --quality looks --low-memory-mode --output candidate.mp4
```

catalog 子命令以固定版本 help 为准，检索无结果时可按内容自己实现，不冒称使用了库组件。doctor 可能因可选模型或内存警告显示未全绿，区分必需故障与不采用的可选能力

预览交付 http://localhost:实际端口/#project/实际工程名，确认服务器返回200并保持运行。源码 index.html 不能当成 Studio 预览链接

工程至少保留 index.html、compositions/、assets/、explanation.json 与文稿分镜；计划与真实动画应一致。bridge check 先检查讲解结构，再调用原生检查。render 默认只生成候选，不认证成片，不自动发布

## 正式验收与发布

读[统一分镜与四项验收](shared-production.md)，用 hf_pipeline.py 的 audit、coverage、candidate、release。integrations.py check/release 会按 pipeline.json 路由到新后端，旧 Canvas 路线保留

## 包内中文界面

assets/studio-zh/ 携带410项界面词条、动态诊断翻译和独立补丁。hyperframes.py preview 自动调用 studio_localize.py，localize 命令可单独应用。备份在运行时 node_modules 下的 .story-motion-ui-backup/0.8.207，升级版本先检查兼容性；不翻译终端、代码、用户正文和未覆盖的第三方错误

运行时与四个官方核心技能仍按前文安装，技能只携带轻量补丁与样片，不能把目录复制误称重依赖已安装。新电脑配置完成后汉化不再依赖本机 visualizations 路径

新计划的semantic-motion/v1选用、对象登记与转场规则见[动作路由](action-routing.md)，初始化将统一接口与目录复制到工程assets，旧项目不静默迁移
