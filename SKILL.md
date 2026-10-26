---
name: story-motion-studio
description: 协同七个必需视频技能制作故事科普、流程解释与独立结构代码动画，内置三套视觉样板，无需每次提供外部参考，交付文稿、分镜、HTML与MP4；分析或局部修改只完成指定范围
---
# 故事动效工坊 v3

用户入口见 [README](README.md)，迁移环境读[安装指南](docs/setup.md)，修改工程读[修改指南](docs/editing.md)

## 范围与必需来源

完整成片必须实际采用七个来源，职责和证据格式见[七项契约](references/roles.md)。技能是指导资料、示例和工具，不是七个视频模型；真实记录方法应用、代码适配与工具执行，不以旧片记录冒充新片执行

本用户使用独立对象、文字、图表、粒子与结构，不生成人物和环境场景；默认中文屏幕叙述、无配音、免费工具、16:9横屏。其他偏好和适用范围见[用户约定](references/user-preferences.md)，本次明确要求优先

## 制作

1. 读取需求和现有材料，运行 scripts/integrations.py doctor 与 scripts/studio.py doctor，核对七个来源和渲染环境；新项目用 studio.py init 创建，不覆盖旧工程
2. 读[内容设计](references/story.md)，用 integrations.py read 读取七项真实资料，按职责做当前内容。文稿与分镜可以合在 storyboard.md，资料见 sources.md；film.json 为时序源，compile生成 timeline.json。七项必需成果和来源记录保留，独立交接文档、重复文稿和执行日志按需要生成，不默认堆积
3. 读[内置风格](references/approved-styles.md)与[运动质量](references/motion-quality.md)。没有外部参考也直接从内置三套中选择：默认黑金为主视觉，结构/粒子服务机制解释；用户点名风格优先。init 不指定风格时使用黑金，提供 motion-kit.js 与动作参考源码，故事与构图仍需按内容实现
4. 先完成连续10秒，包含阅读停留、实质对象变化与一次承接，交付讲稿、分镜和短样。用户确认前止于样片；明确委托直接做完整片则按委托范围执行。内置认可不冒充新片认可
5. 沿用同一视觉与运动系统制作整片。风格和素材锁按[制作命令](references/production.md)处理；指定BGM需实际来源，收费先说明，不自动继承样例音轨
6. 按[验收](references/review.md)检查连续段、转场、阅读、乱序绘制、字体、音轨和完整解码，正式render生成candidate.mp4。按video-shotcraft要求，由未参与制作的审查者实际检查候选，修复阻断项后通过 integrations.py release 发布final.mp4

完成标准：内容讲清楚、动作对应机制、七项当前贡献可追溯、连续画面和音轨实际检查、MP4可播放、HTML工程自包含。检查未覆盖的部分如实说明，技术通过不等于审美认可

样例入库时才读[样例管理](references/examples.md)，修改视觉体系时才读[风格锁](references/style.md)。历史失败项目和中间素材留在项目或外部归档，不塞回技能安装目录
