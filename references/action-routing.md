# 内容选动作、统一调用与跨镜对象

新工程使用 semantic-motion/v1，旧工程没有该字段时保持旧检查，不自动迁移
24项接口、按关系推荐和对象追踪是一套制作约束，不是24种风格，也不要求每片用齐

## 先解释关系，再选择动作

Codex先读资料，写出每镜要证明的关系和真实前提，再用 motion.py suggest 验证候选
工具按结构化 relation 和前提选择，不根据标题关键词猜测，不替代资料核实，不自动改写分镜
新片默认自动选动作，用户只需审讲稿、分镜和连续样片；用户指定动作时仍需检查是否符合该镜内容

```json
{"relation":"waiting","capacity":3}
```

此输入推荐queue；未知容量不可随意编成3，缺前提则补查资料或换一种不作此承诺的讲法

```text
python scripts/motion.py suggest facts.json
python scripts/motion.py example queue
python scripts/motion.py compile PROJECT
python scripts/motion.py trace PROJECT
```

| 内容关系 relation | 动作ID |
|---|---|
| decomposition / consolidation / classification / selection | split / merge / group / filter |
| waiting / independent-tasks / conditional / recovery | queue / parallel / branch / retry |
| targeted-change / difference / history / reversal | patch / diff / version / undo |
| alternatives / correspondence / same-position / detail-scale | compare / align / wipe / zoom |
| magnitude / ranking / ordered-series / frequency | bars / sort / line / distribution |
| provenance / hierarchy / layout-change / stage-transition | trace / expand / morph / handoff |

每项需要哪些事实、哪些HTML绑定和可运行配置，在 assets/motion-actions-v1/catalog.json
按需用example读取所选接口及真实HTML，不必把24段都加载进上下文
连续采用同一种动作可以合理，但要检查内容关系是否真的相同，不按轮换或特效数量评分
无适合关系时重新设计并显式扩展catalog与接口、做样片和验证，不静默退化为卡片入场

## 统一调用

新工程初始化会复制 motion-actions.js、motion-catalog.json，并在根页加载接口
所有元素事先写在HTML里并使用唯一ID，调用方只提供一个已存在的暂停GSAP时间线

```js
const tl = gsap.timeline({paused:true});
/* motion:shot-2 */
MotionActions.add(tl, {
  type:'handoff', start:0, duration:6,
  bindings:{carrier:'#record-a-in-shot-2'},
  params:{from:[850,200],to:[1100,300]}
});
/* end-motion:shot-2 */
window.__timelines['shot-2'] = tl;
```

动作不会创建第二条时间线、播放循环或动态DOM，不运行资料中的命令
start与duration限定该动作区间，区间末尾保留阅读停留；配置示例是起点，镜长按资料、阅读与实际变化决定
各动作参数不同，统一的是外层接口，不把所有动作硬压成同一种位移动画
分布动作根据bucketIds与bucketCenters计算堆叠，排序保持对象的值不变，队列释放后才补位，局部更新不操作unchanged节点
坐标均相对被操作节点所在的父坐标系，标记初态应与from一致，不能跨不同坐标系直接混用
SVG圈的morph更新cx/cy，line与wipe需要预先声明pathLength或clipPath，参考实际example

## 一份分镜中的动作字段

mechanism除已有selectionReason、observableChange、readingHold外，写入：

```json
{
  "family":"handoff",
  "contentFacts":{"relation":"stage-transition","resultUsedNext":true},
  "bindings":{"carrier":"#record-a-in-shot-2"},
  "params":{"from":[850,200],"to":[1100,300]}
}
```

composition指向当前组合HTML，bindings须能在该文件中找到，不能借别的镜头同名ID通过
实际调用由motion.py compile从同一份分镜生成，组合里预留与镜头ID一致的motion标记块；只改写标记块，不覆盖用户其他HTML和时间线代码
先在分镜填写bindings与params，再compile，之后运行check；调用与计划不一致会被拦住，不维护两份动作参数
校验绑定和字段不等于已证明像素运动正确

## 对象登记与来源

顶层objects登记逻辑对象，ID不随镜头改变；sourceRef指实际材料或明确的示例依据
派生对象用parents指向来源，复制、切块与合并产生的新对象不能偷偷沿用旧对象ID
原对象继续存在、只是位置或内容修订时保持逻辑ID，DOM节点每镜仍使用不同且唯一的ID

```json
"objects":[
  {"id":"record-a","label":"记录A","sourceRef":"材料中的来源定位","carryNext":true},
  {"id":"chunk-a","label":"片段A","sourceRef":"同一来源的切块","parents":["record-a"]}
]
```

每镜objectStates声明objectId、selector、state、role、visualKey，role为input、output或both
对应HTML节点写data-object-id、data-object-state、data-visual-key，状态节点应只包含对应状态的可见内容，避免一个大容器同时混入前后文案
visualKey是约定的视觉身份标记，CSS实际颜色、几何和字号仍要看帧，字段本身不能证明它们相同

## 跨镜承接

```json
"handoff":{
  "fromObject":"记录A","toObject":"记录A","relation":"上一镜结果进入下一步",
  "mode":"continue",
  "transfers":[{
    "objectId":"record-a",
    "fromSelector":"#record-a-in-shot-1",
    "toSelector":"#record-a-in-shot-2",
    "mode":"carry"
  }]
}
```

carry要求上一镜输出与下一镜输入身份、状态、视觉标记及节点文字一致
有意改变状态、缩写标签或视觉身份时使用change并写reason，实际说明变化，不用这个字段掩盖跳变
carryNext标记的输出不可在下一镜无说明消失；章节重新开始可使用mode=chapter-break、reason和空transfers，不假造继承关系
保留旧版fromObject、toObject、relation用于人读承接，机器追踪以对象ID和真实节点为准

motion.py trace从同一explanation.json派生检查结果，不是第二份内容源
新增对象的父来源、注册、角色、HTML标记和承接会检查；有缺失就修正资料或分镜，不补虚假的来源

## 验证与边界

检查三层：内容关系与前提、真实HTML绑定与对象身份、实际连续画面
原生check与snapshot负责运行和布局，跨镜看末帧与首帧的对象位置、尺寸、文字和语义色，必要时比较对象区域的像素
实际正常速度观看、阅读和观众理解仍单独记录，不将目录、字段、哈希或接口运行成功当作成片质量保证
