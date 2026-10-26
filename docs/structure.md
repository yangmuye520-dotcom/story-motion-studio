> 公开发布版说明：本包仅保留三套无声样例与画面源码，原音轨、第三方原片、被否定历史和生产验证报告不随包发布

# 目录怎么找

普通用户从 `README.md` 开始，Codex 从 `SKILL.md` 开始。制作项目放在你自己的工作目录，避免写进已安装的技能包

```text
story-motion-studio/
├── README.md                  用户入口：怎么开始、能得到什么
├── SKILL.md                   AI入口：约束、流程与按需阅读
├── agents/openai.yaml         Codex技能列表里的显示信息
├── docs/                      用户指南
│   ├── setup.md               依赖配置与换电脑
│   ├── editing.md             播放、改稿、再次导出与排错
│   └── structure.md           当前目录说明
├── references/                AI按任务读取的制作规则
├── scripts/                   稳定命令入口与工具
├── assets/
│   ├── starter/               新工程起点，只有技术示例
│   └── styles/                三套已认可风格资源与清单
├── examples/
│   ├── index.html             样例浏览入口
│   ├── compare.html           原片与样片对照
│   ├── catalog.json           当前分类、状态与认可历史
│   ├── approved/              已认可样例的完整工程
│   ├── candidates/            候选与保留的旧副本
│   └── references/            用户提供的原片及拆解
└── maintenance/               维护检查工具与历史验证记录
```

## 三种资源不要混用

| 位置 | 解决什么问题 | 使用方式 |
|---|---|---|
| `assets/starter` | 怎样创建一个能执行的新工程 | 用 `scripts/studio.py init` 初始化，不把默认样式视为用户认可 |
| `assets/styles` | 怎样复用字体、配色、组件和运动参考 | 读取 profile 与完整认可样例，重写当前故事和数据 |
| `examples/approved` | 已认可的具体镜头怎样实现 | 看视频与源码，不复用旧片的执行记录充当新片证据 |

`candidates` 中保留了认可前副本和被否定旧片，状态以 `catalog.json` 为准，不能只根据文件夹名称判断。历史工程内的 tools、素材锁和报告保留当时版本，不批量改写

## references 阅读导航

| 文件 | 何时读 |
|---|---|
| `roles.md` | 采用七个上游并绑定本片成果 |
| `story.md` | 写讲稿、分镜与镜内事件 |
| `approved-styles.md`、`style.md` | 选择已有风格、复用与锁定 |
| `reference-benchmarks.md` | 对照原有三条参考片 |
| `examples.md` | 入库、认可、否定样例 |
| `production.md` | 运行制作命令 |
| `review.md` | 检查可读性、内容、转场、音轨与交付 |
| `user-preferences.md` | 本机用户当前的内容和画面限制 |

## 本次目录调整

- 新增用户 README 与 docs，制作规则仍放 references
- 根目录 `styles/` 整体移到 `assets/styles/`，更新风格 profile 和文档指向
- `studio.py init --style-pack` 仍能识别本包旧 `styles/<id>` 输入并转向新位置；手工打开文件或其他工具应使用新路径
- 根目录旧 `validation-results.json` 归档到 `maintenance/validation/legacy-results.json`，它只记录旧版测试，不代表当前验证
- 七个上游、已认可样例、候选副本、原片、素材许可与历史证据不删除、不改写

## 维护检查

在技能目录内运行：

```powershell
python maintenance/check_package.py
```

检查文档链接、三个风格资源、基线哈希、样例导航和必需入口。这是结构检查，不是完整视频渲染或审美验收

新增资源时同步它的入口或清单。样例状态通过 `scripts/samples.py` 更新，独立制作项目使用单独目录，避免把运行结果继续堆进根目录
