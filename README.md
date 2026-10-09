# AutoClaw Design Agent · GitHub 资料包

这是一份可独立放进 GitHub 仓库的静态资料包，整理了 AI Native Design 工作区测试题的研究过程、方案汇报、交互原型和 HTML 产物架构。

## 从哪里看

- [资料首页](docs/index.html)：推荐阅读顺序和所有入口。
- [方案汇报 V09](docs/report_v09/index.html)：完整文稿、12 页汇报画板和内嵌 Demo。
- [功能架构 V10](docs/architecture_v10/index.html)：HTML 产物管理、精准调优与 8 张交互框架图。
- [可点击原型 V08](docs/prototype_v08/index.html)：模拟从初稿到候选审阅、阶段评审和交付。
- [过程资料索引](docs/process.html)：V01–V07 调研、用户旅程、MVP 与功能定义。

`docs/` 内同时保留原始 MD、PDF、SVG、PNG 和原型代码。浏览器阅读用的 `.html` 是对应 MD 的静态副本；资料包进入独立仓库后，修改 `docs/` 内的原始 MD，可安装 `requirements.txt` 后运行仓库根目录的 `build_release.py` 重新生成阅读页。直接预览现有站点不需要安装依赖。

## 放入 GitHub

1. **解压资料包**，把本目录中的 `README.md`、`build_release.py`、`docs/` 等文件放进新仓库根目录；不要只上传 ZIP。
2. 在仓库中提交并推送文件。仓库的 Pages 发布源可设置为默认分支的 `/docs`，入口就是 `docs/index.html`。[GitHub 官方配置说明](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。
3. 若仅需多设备同步资料，不需要对外网页，可以只使用仓库文件，不启用 Pages。

**发布前检查可公开范围。**GitHub 官方说明：GitHub Pages 站点即使来自私有仓库，也可能作为公开网页被访问。本包包含测试题截图与产品录屏的截帧；请先确认这些材料适合公开，再启用 Pages。Figma 源稿仍是外部链接，其访问权限由原 Figma 文件控制。

## 范围与版本

| 目录 | 内容 |
|---|---|
| `docs/report_v09/` | 当前方案汇报与 SVG 画板 |
| `docs/architecture_v10/` | 最新功能架构、信息结构和线框 |
| `docs/prototype_v08/` | 可点击交互原型及截图 |
| `docs/md/`、`docs/pdf/` | 研究 V01–V02 |
| `docs/mvp_v03/` 至 `docs/feature_v07/` | 观察证据、旅程、共创流程、草图三态、定域修订定义 |
| `docs/input/` | 用户提供的题目截图 |

未纳入与本题无关的 `black_friday_gift/`、`imagegen/`、`ui_750x1624/`、旧版重复 ZIP 和临时浏览器文件。另一个面试资料目录中的原始录屏约 124 MB，未放入这份网页资料包；本包保留此前整理的截图和观察记录。个人求职资料 PDF 也未纳入。

## 本地预览

在本目录运行 `python3 -m http.server 8767`，然后访问 `http://127.0.0.1:8767/docs/`。页面不需要构建工具或云端 API；外部研究与 Figma 链接需要联网。

分享前可运行 `python3 verify_release.py` 检查站内链接与 SVG 文件。

## 交付性质

V08 是交互模拟，V09–V10 是方案与线框，不代表 AutoClaw 当前已实现 HTML 定域回写、真实视觉回归或生产代码交付。各文档分别标出已观察事实、方案假设和待验证问题。
