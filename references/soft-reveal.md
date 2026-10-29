# 柔和渐显叙事 soft-reveal-v1

用户认可的渐入渐出为主要运动语言，作为新可选风格，视觉沿用暗色宋体叙事，默认工程风格不变
先读editorial-serif.md，字体与theme.css复用editorial-serif-v1，动作源码在assets/style-variants/soft-reveal-v1/motion.js

## 固定运动规则

渐入0.6–0.9秒，渐出0.4–0.6秒；短边1080时位移12–24像素，其他尺寸同比调整
逐字间隔0.08–0.14秒，逐字DOM预先写入HTML，使用transform，不动画letter-spacing
正文仅透明度与轻位移，阅读时静止；模糊仅按需用于少量标题，不能影响正文阅读
前句退场后新句接管，必要的重叠不让两句占据同一位置；阅读时间依据文字量，不统一套固定时长
透明度和运动由同一暂停GSAP时间线驱动，无随机数、CSS自动动画或第二条时间线
从分镜生成文字与时间，不能为调用新模块复制一份正文

## 调用

将motion.js复制到工程assets并在根HTML加载，组合里调用：

```js
SoftReveal.enter(tl,'#heading',0,{duration:.8,distance:20});
SoftReveal.chars(tl,['#char1','#char2'],.3,{stagger:.1});
// 让观众阅读，再退场
SoftReveal.exit(tl,'#heading',3.2,{duration:.5});
```

这些是排版与衔接动作，不替代24项解释关系接口；需要拆分、队列、比较时依旧按内容选择
已有工程要明确应用新风格，不自动覆盖；无配音、无人物环境、音乐来源按当前请求
新片先审10秒连续样片，包含一次渐入、阅读、渐出与下一重点接管
