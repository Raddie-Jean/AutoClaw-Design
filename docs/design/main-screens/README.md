# AutoClaw 主任务界面 V17

修正中间的任务内容：测试1为依据规范生成 AutoClaw 首页 SVG、选中输入卡片并进行局部修改；测试2为固定首页 v1、查阅意见、创建候选、对比采纳并确认解决。两条任务独立。保留原有侧栏、任务对话及产物窗口。

## 在 Figma 编辑：推荐使用原生图层导入

直接拖入 SVG 时，Figma 可能将文字轮廓化，SVG 也不携带 Figma 的原生布局语义。V17 新增原生图层导入，不再把整页控件放在一个矢量底层。

1. 解压完整素材包。
2. Figma 桌面版 → Plugins / 插件 → Development / 开发 → Import plugin from manifest / 从 manifest 导入，选择 figma-plugin/manifest.json。
3. 运行「AutoClaw 原生分组设计稿导入 V17」。
4. 选择 Figma原生图层 中对应测试的 JSON 文件；两张分别导入。
5. 在图层面板展开 Sidebar、任务对话、原生输入框、产物窗口、产物内画布、对象参数或评审记录，即可修改原生文字、矩形、颜色、圆角和尺寸。小图标作为独立矢量导入。建议保留 PingFang SC 字体。

SVG 同时保留，供预览、矢量交换和导出使用。新原生导入结构包含 Text、Rectangle、Ellipse、Line 与分组；小图标仍为可展开的 SVG 矢量；头像与少量彩色资源图标为位图。没有自动布局、组件实例或原型连线。

验证：两张 SVG 已渲染检查；XML、JSON 结构、文字数量一致性及导入插件 JavaScript 语法检查通过。受 Figma 读取额度限制，本轮没有在 Figma 内实际运行插件；文字基线和缺字替代字体仍需导入后确认。旧 V16 文件和 V15 HTML 保持不变。
