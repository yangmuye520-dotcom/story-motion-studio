# 四类解释动作模块

可运行源码：[模板](../assets/templates/engineering-2d-v1/index.html)、[动作函数](../assets/templates/engineering-2d-v1/assets/mechanism-motion.js)
模板是48秒无声演示，风格来自已认可10秒暗色样片，四个新动作示例仍需按实际主题审查，不能称为用户已认可整片

| family | 适用关系 | 同一对象怎样变化 | 不可误用 |
|---|---|---|---|
| split-merge | 原文切块、分类、证据归并 | 原片段离开原位置，按主题分组，同组进入结果框，保留来源身份 | 不能暗示所有来源必然合并、合并后删除原证据或固定一对一 |
| queue-concurrency | 等待、资源占用、完成释放 | 同一任务进入有限槽位，进度结束后离开，后续任务才补位 | 槽位数和保留槽语义要来自资料，示例的三槽不代表真实系统配置 |
| local-patch | 增量更新、证据驱动修订 | 新证据指向已有段落，目标旧文被替换，其余段落保持原位 | 未触及文本不可整体消失重写，不能把追加和替换混为一事 |
| dual-compare | 两算法、两系统、同输入不同路径 | 同一输入的明确副本进入两路，分别经过步骤，按同一维度比较结果 | 不能把演示用时当性能实测，两路不同输入不能称同条件对照 |

当关系不适合四类时可用 transfer（传递）、mapping（字段对应）或 custom（自定义机制），写清选择理由，不强行套模块

## 实现

根页面加载 `assets/gsap.min.js`、`assets/engineering-2d.css`、`assets/mechanism-motion.js`
组合模板声明所有对象、文字和稳定ID，脚本创建唯一暂停GSAP时间线，向对应函数传入该时间线及选择器，之后注册到 window.__timelines
参考四个 compositions/*.html 中的真实调用；函数不调用play、requestAnimationFrame、定时器或随机数
需要调参数时在项目内做明确版本修改、重建锁和连续样片，不能删除锁伪装未修改

## 分镜字段示例

```json
"mechanism": {
  "family": "local-patch",
  "selectionReason": "本镜解释新增证据只修订文档的一部分",
  "observableChange": "新证据指向测试命令行，旧值被新值替换，上下两段不移动",
  "readingHold": "替换完成后停留，给观众比较修改前后"
}
```

字段只约束计划完整性，仍须在真正HTML动画和导出帧里核对是否发生，不能仅填字段就宣称采用
