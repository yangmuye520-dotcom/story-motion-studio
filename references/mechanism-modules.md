# 解释动作模块

当前新工程采用24项统一接口，入口、选用规则和跨镜对象字段见[内容选动作与对象追踪](action-routing.md)

- assets/motion-actions-v1/catalog.json：24项关系、前提、绑定、示例配置
- assets/motion-actions-v1/actions.js：MotionActions.add，沿调用方唯一暂停时间线运行
- assets/motion-actions-v1/examples/：逐项真实HTML调用示例，仅供接线参考，需替换成当前资料与对象登记
- scripts/motion.py：只读推荐、按需查看示例、导出对象追踪结果

v6四类机制源码仍保留在engineering-2d-v1模板中，旧工程不自动迁移；新接口不改变默认暗色视觉
网页展示页用于挑选关系和动作，不把它的示意数据或固定10秒时长直接当新片内容
24项可调用不等于24项都已经获用户逐项验收，新主题仍先做连续样片
