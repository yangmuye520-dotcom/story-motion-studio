> 公开发布版说明：本包仅保留三套无声样例与画面源码，原音轨、第三方原片、被否定历史和生产验证报告不随包发布

# 安装依赖与换电脑使用

这里说明制作环境，普通用户可直接让 Codex 代为检查。检查命令不会自动安装或下载

## 当前默认路线

新项目使用HyperFrames和暗色精细二维模板，仍需七个上游来源
统一安装器负责七项、基础Python/浏览器工具、Node.js检查、固定HyperFrames、四个官方核心技能和中文补丁；已有安装用-CompleteExisting补齐，详见README
中文补丁随本技能携带，默认模板与四类动作无需另找外部视频，但运行工具本身仍须安装
单独播放MP4不需要以上制作环境

## 三种使用情况

| 你要做什么 | 需要什么 |
|---|---|
| 观看 MP4 | 普通视频播放器 |
| 播放已有 HTML | 完整工程、浏览器；新工程用HyperFrames，旧Canvas用本地HTTP服务 |
| 按总技能重新制作或导出 | 本技能、七个上游、实际资料库与运行工具 |

## 技能目录

推荐保留下面的相对结构，技能根目录可以迁移：

```text
skills/
├── story-motion-studio/
└── video/
    ├── wtt-code-animation-studio/
    ├── lemo-opuscar/
    ├── huashu-art-motion/
    ├── video-shotcraft/
    ├── dashi-animationstyle/
    ├── mg-styles-15/
    └── xilo-opus-video/
```

- lemo 入口之外，还需实际 Lemo-Opuscar 资料库，其中有 `DIRECTOR.md`
- mg 需要实际 demo 源码；本机这个来源没有 `SKILL.md` 也可以作为必要源码库使用
- 只创建七个空目录不能通过检查，必须读取真实来源并为新片记录实际贡献

## 本地工具

| 工具 | 用途 |
|---|---|
| Python | 运行编译、检查、渲染和素材管理脚本 |
| Playwright 与 Chrome | 自动控制浏览器，按帧绘图与取图 |
| Pillow | 生成预览联系表等检查材料 |
| FFmpeg | 视频编码、音频处理与封装 |
| NumPy | 可选的本地合成音乐工具 |

基础 Python 包约束见[starter/requirements.txt](../assets/starter/requirements.txt)。外部语音或其他上游原生工具的依赖，按实际选用路线另查，不在这里承诺已全部配置

在本技能目录内运行：

```powershell
python scripts/integrations.py doctor
python scripts/studio.py doctor
```

第一条核对七个来源和 lemo 实际库，第二条报告运行环境。`doctor` 是探测，不能代替真实浏览器启动、短片导出或音质验证

若命令提示找不到 Python，让 Codex 找到可用解释器或按当前机器情况配置，不把别人的绝对路径原样复制过来

## 本机配置

默认读取 `~/.codex/story-motion-studio.local.json`，也可用环境变量 `STORY_MOTION_CONFIG` 指定配置文件。下列是字段示意，不是可直接粘贴的真实路径：

```json
{
  "upstreamRoot": "<七个上游所在的video目录>",
  "lemoLibrary": "<含DIRECTOR.md的实际库目录>",
  "python": "<推荐Python解释器路径>",
  "pythonPaths": ["<额外Python依赖目录>"],
  "chrome": "<chrome可执行文件路径>",
  "ffmpeg": "<ffmpeg可执行文件路径>"
}
```

`python` 仅作推荐路径记录，脚本不会自动切换解释器。`chrome`、`ffmpeg` 和 `pythonPaths` 用于定位现有依赖

还支持 `STORY_MOTION_UPSTREAM`、`LEMO_OPUSCAR_LIBRARY`、`CHROME_PATH`、`FFMPEG_BINARY` 等覆盖项。需要核对优先级时查看 `scripts/studio.py` 和 `scripts/integrations.py`

本机配置留在机器上，不放进技能包。Windows 路径在 JSON 中使用 `/` 或转义后的 `\`

## 新机器验证顺序

1. 复制本技能、七个来源和 lemo 实际库
2. 恢复当前机器的工具路径与所需依赖
3. 运行两个 doctor，补齐缺项
4. 打开样例视频，验证现有 HTML 可运行
5. 新建独立测试项目，完成短样预览与导出
6. 再进行完整制作，沿用实际来源记录与审片流程

重新制作仍需七个来源，样例中的旧记录不能当作新片的执行证明

## 样例资源与分享

`examples` 包含完整工程和本地参考原片，因此体积较大。不要随意删掉字体、vendor 或素材来压缩体积，可能破坏预览与复用

给别人看结果通常发送 MP4 即可。要传工程则带齐素材和来源说明；第三方参考原片、音乐以及本机私有配置不自动纳入公开分享


## HyperFrames 新工程

新工程的执行、安装与发布边界读[HyperFrames 接入](../references/hyperframes.md)，内容与画面对应读[讲解质量](../references/explainer-quality.md)。七项实际贡献仍必需；旧 Canvas 验收字段不可伪造或冒充新后端的检查结果
