# 固定视觉系统

本文件以下是旧Canvas风格锁路线，新HyperFrames默认采用[暗色二维模板](approved-styles.md)和hf_pipeline初始化锁，不套用下述Canvas初始化命令

随包starter仅验证技术；此前深色文件框影片被用户评价“不好看、没看懂”，不能将旧片、推荐项、技术成功算作审美认可。首次需短样和明确决定，已有认可直接沿用。

锁定style.json中的颜色、字体、字号、线条、布局与motion；components.js的组件/动作；index.html中的舞台和字体入口。scenes.js允许故事和物件变化，但复用tokens/组件。哈希不能识别所有绕过tokens的代码，因此仍需样片对照。

`python tools/studio.py style-lock . --evidence "真实用户认可/明确代选委托及位置"`

工具只保存文字和哈希，不验证人类授权真实性；执行者负责。已有锁变更后拒绝覆盖，保留旧包并建新版，不能删除锁装作首锁。

`python tools/studio.py export-style . <新风格包目录>`

`python <技能目录>/scripts/studio.py init <新项目> --style-pack <已认可风格包>`

风格包只带锁定样式、组件、页面、字体与认可记录，不含上片故事/音乐。新风格还应记录声音氛围、布局与转场，而不只是换颜色。用户明确要求改画风才进入新版选择。

需要跨新对话发现时，认可后的包导出到本技能的assets/styles/<风格名>-v1，并保留认可短样与依据。此时才创建该目录；随包不放虚假的“已认可”风格。多个版本以用户最新选择为准，不覆盖旧包。
