# 中文工作台安装与操作手册

## 仓库内容与操作步骤

**中文补丁和启动入口已随本仓库发布，换电脑也能使用；HyperFrames运行时通过安装下载，不随仓库打包**

| 仓库内文件 | 用途 |
|---|---|
| [中文词条](../assets/studio-zh/labels.txt) | 410项界面翻译 |
| [界面与报错翻译](../assets/studio-zh/overlay.js) | 翻译菜单、提示及已覆盖的动态报错 |
| [中文样式](../assets/studio-zh/style.css) | 中文界面排版适配 |
| [汉化应用脚本](../scripts/studio_localize.py) | 备份并修改已配置的固定版本运行时 |
| [中文启动入口](../scripts/preview-zh.ps1) | 应用补丁后启动本地预览 |

这是针对HyperFrames 0.8.207的本地中文适配，不是官方全量汉化发行版
未覆盖的第三方诊断保留原文，不翻译用户正文、代码和工程文件名

### 1 安装并检查环境

新电脑先完成[README的安装步骤](../README.md#需要安装什么)
仅下载本仓库不能直接打开工作台，需要Python、Node.js、Chrome、FFmpeg/FFprobe及已配置的固定运行时
已有环境不重复运行防覆盖安装器

可以直接向Codex发送：

```text
检查story-motion-studio的HyperFrames环境
按references/hyperframes.md补齐免费依赖，使用hyperframes@0.8.207
核对本机配置中hyperframes.cli指向的实际运行时
应用仓库自带的中文界面补丁，不升级运行时
新建测试工程，验证中文菜单和MP4导出
```

### 2 启动一个已有工程

在PowerShell执行以下命令，修改工程路径；技能安装到自定义位置时也要修改技能路径

```powershell
$skill = Join-Path $env:USERPROFILE ".codex\skills\story-motion-studio"
$project = "D:\videos\my-project"
powershell -ExecutionPolicy Bypass -File "$skill\scripts\preview-zh.ps1" -Project $project -Port 8793
```

`$project`必须是已存在的HyperFrames工程目录，不是MP4文件或任意空文件夹
命令先应用中文补丁，再启动后台预览；打开终端实际输出的Studio地址，服务需保持运行
预览地址通常形如`http://localhost:8793/#project/工程名`，以本次输出为准

也可让Codex代做：`使用本技能中文启动入口打开当前工程，检查中文菜单是否实际生效，并给我可访问的预览地址`

### 3 从新主题开始制作

```text
使用story-motion-studio
选择柔和渐显叙事
主题：[内容或MD完整路径]
通过本技能的中文HyperFrames入口预览，不直接启动其他运行时
先给讲稿、统一分镜和包含核心讲解动作的10秒样片
确认后再制作整片，交付MP4与完整HTML工程
```

[柔和渐显的固定参数和调用方式](../references/soft-reveal.md)
工作台中可以预览和编辑同一工程，修改后需重新导出，已有MP4不会自动更新

### 4 已有工作台仍是英文时

1. 先确认打开的是本次中文启动命令输出的地址，旧端口可能属于其他运行时
2. 在该页面按Ctrl+F5强制刷新，清除旧页面缓存
3. 让Codex核对`~/.codex/story-motion-studio.local.json`中的`hyperframes.cli`；若设置了`HYPERFRAMES_CLI`，环境变量优先
4. 仅重新应用补丁，可在技能目录执行：

```powershell
python .\scripts\studio_localize.py
```

5. 再用中文入口启动工程，实际检查标题“HyperFrames 中文工作台”和“属性检查器、导出、代码检查”等菜单

不要以补丁文件存在就认定汉化成功，需检查实际页面加载了studio-zh.js并显示中文
直接使用npm run dev、另装的npx运行时或桌面应用，可能没有经过本技能的汉化入口，不能保证自动中文化
版本不匹配时脚本会停止，需要先核对兼容性，不要删除版本检查强行应用

### 5 常见提示与停止服务

| 提示或现象 | 操作 |
|---|---|
| 找不到python | 先确认Python安装和当前终端PATH，或让Codex定位解释器 |
| HyperFrames runtime missing | 按HyperFrames配置说明设置本机运行时路径 |
| Expected pinned HyperFrames / 版本不匹配 | 使用0.8.207，其他版本需先验证补丁兼容性 |
| 端口占用 | 改用空闲端口，并打开新输出的地址 |
| localhost拒绝连接 | 预览服务未运行或已退出，重新使用中文入口启动 |
| 少数错误仍是英文 | 当前词条未覆盖，保留原文用于定位，不代表全部汉化失效 |

需要停止后台服务时，在本技能目录执行，路径替换为实际工程目录：

```powershell
python .\scripts\hyperframes.py --project "D:\videos\my-project" preview --stop
```

汉化前的备份保存在运行时node_modules下的`.story-motion-ui-backup/0.8.207`，本机配置和备份不上传仓库
