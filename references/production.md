# v2 制作入口

1. `python scripts/integrations.py doctor`：七包必须齐，lemo入口之外还需真实DIRECTOR.md。
2. `python scripts/studio.py doctor`：依赖探测；不自动付费或全局安装。本机配置~/.codex/story-motion-studio.local.json可含python、pythonPaths、chrome、ffmpeg、upstreamRoot、lemoLibrary，不随包分发。
3. `studio.py init <新项目>`：先检查七包，创建统一工程并绑定来源；复制工具后可在项目tools中运行，但仍依赖那七个来源。
4. 按roles写文稿/故事弧/对象表/镜头计划/视觉契约，真实运行`integrations.py native-lint <项目>`。
5. `studio.py compile <项目>`：film→timeline；素材记录来源许可，`assets <项目> seal/check/propose/accept`沿用版本机制。
6. `studio.py render <项目> --preview --draft`：过程关键帧；`--draft`完整技术片，尚未通过七项时准确标缺失，不算最终片。
7. 用integrations.py record登记七份实际贡献；`integrations.py check <项目>`检查成果、来源、原生lint、图文对比度、当前预览。
8. 用户认可风格/明确委托后style-lock，`studio.py render <项目>`只输出candidate.mp4待审，不直接输出final。
9. 独立审当前candidate，release-review.json必须含videoSha256、reviewer、independent:true、verdict:pass、blockingIssues:[]、checks五项具体观察、limitations。字段不自动证明人类/代理真实性，执行者负责实际发生。
10. `integrations.py release <项目>`验证当前文件/七项/审片后才发布final.mp4；旧正式片保存.releases版本。

本包原创音乐工具music.py可选；用户指定音乐优先。严格复用原AAC需另用stream copy与payload核验，本包默认AAC编码不能宣称原编码不变。音轨短于片长不能静默补静音，必须明确选择。无配音不调用TTS。

原生huashu工具若报红，查实际问题；其短屏上字与主叙述分开，不把完整字幕藏进短标签字段骗检查。其他上游整套引擎没跑就不要说跑过。

samples.py管理样例库；portable bundle仍不含七包，换电脑需装齐并绑定真实版本。Windows兼容由本包适配，原包脚本失败不能冒充原生成功。
