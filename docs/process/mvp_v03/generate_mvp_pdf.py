#!/usr/bin/env python3
"""Render the V03 MVP review PDF with embedded PingFang and video evidence."""

from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "2026-10-04_AutoClaw_Design工作区_MVP阅读版_V03.pdf"
FONT_DIR = Path("/Users/jean/Library/Fonts")
for name, filename in [("PF", "PingFang Regular.ttf"), ("PFM", "PingFang Medium.ttf"), ("PFB", "PingFang Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))
pdfmetrics.registerFontFamily("PF", normal="PF", bold="PFB", italic="PF", boldItalic="PFB")

NAVY = colors.HexColor("#122B3B")
INK = colors.HexColor("#1C3543")
MUTED = colors.HexColor("#5F7480")
ACCENT = colors.HexColor("#147D84")
GOLD = colors.HexColor("#D7AA60")
PALE = colors.HexColor("#EFF6F5")
LINE = colors.HexColor("#D8E6E5")
WHITE = colors.white
PW, PH = A4
MARGIN = 43
WIDTH = PW - MARGIN * 2


def sty(name, size, lead, *, color=INK, font="PF", after=0, keep=False):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=lead,
                          textColor=color, spaceAfter=after, keepWithNext=keep,
                          allowWidows=0, allowOrphans=0)


ST = {
    "eye": sty("eye", 10, 15, color=ACCENT, font="PFM", after=9, keep=True),
    "h1": sty("h1", 22, 31, font="PFB", after=15, keep=True),
    "h2": sty("h2", 14, 21, font="PFB", after=9, keep=True),
    "body": sty("body", 11, 19, after=10),
    "small": sty("small", 9.5, 15.5, color=MUTED, after=7),
    "table": sty("table", 9.5, 15),
    "tablebold": sty("tablebold", 9.5, 15, font="PFM"),
    "thead": sty("thead", 9.5, 15, color=WHITE, font="PFB"),
    "caption": sty("caption", 9.0, 14, color=MUTED, after=6),
    "source": sty("source", 9.2, 14, color=ACCENT, after=4),
}


def P(value, kind="body"):
    return Paragraph(value, ST[kind])


def H(value, level=1):
    return P(escape(value), "h1" if level == 1 else "h2")


def T(rows, widths, *, pad=7):
    data = []
    for ri, row in enumerate(rows):
        data.append([P(escape(str(v)).replace("\n", "<br/>"),
                       "thead" if ri == 0 else "tablebold" if ci == 0 else "table")
                     for ci, v in enumerate(row)])
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("LINEBELOW", (0, 0), (-1, -1), .35, LINE),
    ]
    for i in range(2, len(rows), 2):
        commands.append(("BACKGROUND", (0, i), (-1, i), PALE))
    table.setStyle(TableStyle(commands))
    return table


def pic(name, width=WIDTH):
    source = ROOT / "evidence" / name
    from PIL import Image as PILImage
    im = PILImage.open(source)
    return Image(str(source), width=width, height=width * im.height / im.width)


def paired_pics(first, first_caption, second, second_caption):
    w = (WIDTH - 10) / 2
    cells = [[pic(first, w), pic(second, w)],
             [P(first_caption, "caption"), P(second_caption, "caption")]]
    table = Table(cells, colWidths=[w + 5, w + 5], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PW, PH, fill=1, stroke=0)
    canvas.setFillColor(ACCENT)
    canvas.roundRect(MARGIN, PH - 140, 97, 23, 11, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("PFM", 9)
    canvas.drawCentredString(MARGIN + 48.5, PH - 132, "MVP 产品方案 V03")
    canvas.setFillColor(GOLD)
    canvas.rect(MARGIN, PH - 211, 36, 3, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("PFB", 28)
    canvas.drawString(MARGIN, PH - 191, "AutoClaw Design Agent")
    canvas.setFont("PFB", 22)
    canvas.drawString(MARGIN, PH - 253, "从生成结果到可交付版本")
    canvas.setFillColor(colors.HexColor("#D0E2E2"))
    canvas.setFont("PF", 11)
    canvas.drawString(MARGIN, PH - 298, "录屏体验 · 功能取舍 · 用户旅程 · MVP 验收")
    canvas.setStrokeColor(colors.HexColor("#4A6570"))
    canvas.line(MARGIN, 255, PW - MARGIN, 255)
    canvas.setFillColor(WHITE)
    canvas.setFont("PFM", 10.5)
    canvas.drawString(MARGIN, 229, "唯一核心判断")
    canvas.setFillColor(colors.HexColor("#DCE9E8"))
    canvas.setFont("PF", 10)
    canvas.drawString(MARGIN, 200, "复用项目—任务—产物—工作区外壳；")
    canvas.drawString(MARGIN, 179, "用“修订提案”把一次局部修改变成可审、可回退、可交付的版本。")
    canvas.setFillColor(colors.HexColor("#A6C0C1"))
    canvas.setFont("PF", 8.4)
    canvas.drawString(MARGIN, 69, "2026.10.04  /  初版产品方案  /  完整要求与证据见同包 Markdown")
    canvas.restoreState()


def later(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(ACCENT)
    canvas.rect(MARGIN, PH - 44, 18, 3, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont("PFM", 8)
    canvas.drawString(MARGIN + 25, PH - 45, "AUTOCLAW DESIGN WORKSPACE  /  MVP")
    canvas.setStrokeColor(LINE)
    canvas.line(MARGIN, 45, PW - MARGIN, 45)
    canvas.setFont("PF", 7.5)
    canvas.drawString(MARGIN, 30, "2026.10.04  ·  V03  ·  录屏观察与方案推论已区分")
    canvas.drawRightString(PW - MARGIN, 30, f"{doc.page:02d}")
    canvas.restoreState()


story = [Spacer(1, 700), PageBreak()]

story += [P("01 / 先给产品决策", "eye"), H("任务内做成果工作区，而非另造设计软件"),
          P("测试题关注的是 Design 任务完成后，设计师如何查看、预览、继续编辑并交付目前为 HTML 的结果。AutoClaw 已有项目、任务、输出产物和可展开工作区等入口；官网也描述了聊天、评论和画布修改。[S1]"),
          T([["层次", "MVP 决策", "理由"],
             ["承载对象", "一次任务生成的 HTML 项目版本", "预览和开发接手都需同一份运行源文件"],
             ["承载位置", "现有任务内的 Design 工作区", "保留项目/任务归属和原始对话"],
             ["核心动作", "浏览 → 选区 → 候选比较 → 接受版本 → 固定交付", "覆盖题面要求的一条完整链路"],
             ["单点 Feature", "修订提案", "解决修改范围与正式版本不清的问题"]],
            [87, 180, WIDTH - 267]),
          Spacer(1, 15), H("证据强度", 2),
          P("两段用户录屏覆盖通用 AutoClaw 任务和 Lovart 素材画布；2026-10-04 对已安装 AutoClaw 客户端做了只读走查。<b>录屏没有展示 Design Agent 的 HTML 生成任务</b>，因此不能把未看到的版本能力当成不存在。Design Agent 现有能力以官方公开文章为基线，方案差异留待真实任务验证。"),
          P("本 PDF 是 8 页阅读版；完整逐步审查、对象模型、验收情境、来源链接与 9 张证据图在同包 Markdown。", "small"), PageBreak()]

story += [P("02 / AUTOCLAW 录屏与客户端", "eye"), H("通用任务外壳已经给出入口"),
          paired_pics("A01-任务首页与输入框.png", "A01 · 00:20｜项目、任务、连接器与通用输入共存；项目可在发起任务时指定。",
                      "A03-聊天内图片结果.png", "A03 · 01:20｜图片结果在消息里呈现，可放大并继续追问。"),
          Spacer(1, 9),
          T([["观察", "对 Design 工作区的含义"],
             ["项目与任务是现成组织层", "成果应回到产生它的任务；MVP 不增加全局 Design 首页"],
             ["图片结果适合在聊天里消费", "多页面 HTML 需补页面/状态/版本索引；这点仍要真实任务验证"],
             ["客户端有输出产物抽屉", "可用作“设计成果 v1”入口；本次图片任务为空，不推断其他任务"],
             ["客户端可展开浏览器/文件工作区", "有可复用容器；需与 Auto Design 原生画布核对，避免双重预览"]],
            [155, WIDTH - 155]),
          Spacer(1, 8),
          P("连接器列表在独立页面，录屏中主要呈现法律与企业信息服务。MVP 允许设计师用附件或链接提供 Figma 参考，不依赖新增连接器。[A04]", "small"), PageBreak()]

story += [P("03 / LOVART 录屏", "eye"), H("成熟设计工具：先有对象，再有修改"),
          paired_pics("L02-Lovart选区快捷工具.png", "L02 · 00:10｜选中单个素材后，出现对象相关的快捷工具。",
                      "L03-Lovart选区局部指令.png", "L03 · 00:20｜Quick Edit 输入框紧贴选区，修改目标清晰。"),
          Spacer(1, 8),
          P("录像继续显示原素材保留、新候选出现在旁边、可放进 Frame 整理；选中对象后还能使用更多处理和下载工具。[L04][L05] 官方文档另外说明图层历史与 Generated Files 面板。[S2]"),
          T([["可迁移的机制", "不能直接照搬的地方"],
             ["选择对象 → 局部指令 → 新候选 → 比较 → 导出", "HTML 有页面、交互状态、断点与源码；单张素材不具备这些关系"],
             ["保留原稿与候选，避免破坏已认可结果", "网页应保留的是可运行版本，不能只复制静态截图"],
             ["右侧保留 Agent 上下文，工具在对象附近出现", "MVP 应先做目标/状态明确，不堆满画布工具"]],
            [225, WIDTH - 225]),
          P("结论：Lovart 值得借鉴的是“产物对象化”和“候选并存”，不是无限画布本身。", "small"), PageBreak()]

story += [P("04 / 用户旅程与取舍", "eye"), H("把精修的不确定性压到最低"),
          P("典型任务：设计师拿到成员邀请流程 HTML 初稿，需把移动端无效邮箱提示放到字段下方，确认桌面端未受影响，然后交给 PM 和前端。"),
          T([["阶段", "用户要判定什么", "MVP 提供的证据"],
             ["接收", "生成了哪些页面和状态？", "成果总览、主源文件、缺失项、当前版"],
             ["预览", "关键路径可运行吗？", "页面/状态/桌面与移动切换"],
             ["精修", "Agent 改的是我选中的地方吗？", "目标固定的修订提案与候选预览"],
             ["确认", "是否误伤其他断点？", "原版/候选并排、影响清单、接受/拒绝"],
             ["交付", "开发拿到的是同一版吗？", "固定版本、ZIP、运行说明、状态表、已知问题"]],
            [78, 175, WIDTH - 253]),
          Spacer(1, 14), H("路线取舍", 2),
          T([["方案", "判断"],
             ["另开全局 Design 首页", "放弃：重复项目/任务导航，题目重点在任务完成后"],
             ["完整 Lovart 式自由画布", "延后：更适合方向与素材探索，HTML 回写成本高"],
             ["Figma 作为主稿", "放弃：当前主产物是 HTML，转换可能有损"],
             ["任务内成果总览 + HTML 聚焦工作台", "采用：直接服务查看、修改与交付闭环"]],
            [173, WIDTH - 173]), PageBreak()]

story += [P("05 / TASK 1", "eye"), H("工作区只画四个关键状态"),
          T([["状态", "主内容", "关键规则"],
             ["1 成果总览", "页面/状态、方向、资源、文件与当前 v1", "生成完成 ≠ 已可交付；失败项清楚可见"],
             ["2 聚焦预览", "运行 HTML，切断点和交互状态，选中区域", "页面/状态/设备/版本始终可辨"],
             ["3 修订审阅", "v1 与候选并排，文件与受影响范围", "候选标明“尚未应用”；接受后才生效"],
             ["4 交付快照", "指定 v2、源码资源、状态表、运行说明", "快照固定；后续改动不会悄悄更新交付包"]],
            [105, 196, WIDTH - 301]),
          Spacer(1, 14), H("建议的信息架构", 2),
          P("沿用全局「项目 / 任务」；任务内切「对话 / 设计工作区」。工作区顶部始终显示任务、方向、当前版本和交付状态。成果总览负责找结果，聚焦预览负责真实交互；右侧随选择切换 Agent 指令、属性和修订提案。"),
          P("MVP 以页面/状态列表代替自由无限画布。若 Auto Design 现有画布已具备相同能力，则整合现有画布并强化产物与版本状态，而不是重复造一套编辑器。"),
          H("唯一的成功主路径", 2),
          P("任务完成 → 打开设计成果 v1 → 进入移动端错误态 → 选提示区域 → 提出修改 → 看候选 → 接受为 v2 → 导出 v2 开发包。测试题的主屏都围绕这条路径展开。"), PageBreak()]

story += [P("06 / TASK 2", "eye"), H("修订提案：AI 修改先可审，再生效"),
          P("Auto Design 的官网已经描述聊天改结构、评论改局部和画布直接微调。[S1] 本 Feature 不重新命名这些操作，而是在「指令 → 正式版本」之间增加可见的审阅步骤。"),
          T([["状态", "设计师看到什么", "系统规则"],
             ["选区", "v1 / 表单 / 无效邮箱 / Mobile；默认仅此状态", "目标绑定，不让用户反复描述整页"],
             ["生成候选", "正在修改、源版仍可打开", "在隔离项目快照里改 HTML；失败保留 v1"],
             ["待审阅", "双预览、文件变化、预计波及范围", "可继续改、放弃或接受；不得误标为正式"],
             ["已接受 v2", "v2 成为当前版，v1 可回看", "缩略图、预览和导出统一指向 v2"]],
            [96, 206, WIDTH - 302]),
          Spacer(1, 15), H("技术边界决定交互边界", 2),
          P("只对 AutoClaw 自身生成且保留源文件的 HTML 项目开放。DOM→源码定位不稳定时，退化为页面级修改并提示范围扩大；触及全局样式时要显示可能影响所有页面。MVP 不承诺任意 HTML 精准回写、Figma 双向同步或自动合并生产代码。"),
          P("可以用项目快照实现候选/确认版本语义，不必把 Git 分支、复杂冲突合并和多人实时协同一起塞入首版。", "small"), PageBreak()]

story += [P("07 / 交付、验证与待核实", "eye"), H("定义“可交付”，再验证它"),
          T([["最小开发包", "用途"],
             ["src/ + assets/", "可启动的 HTML/CSS/JS 与页面实际引用资源"],
             ["README.md", "运行方法、依赖、模拟数据与设计目标"],
             ["pages-states.md", "页面 × 状态 × 断点、触发方式与未覆盖项"],
             ["changes.md + manifest.json", "接受过的修订、已知问题、task_id 和 version_id"]],
            [169, WIDTH - 169]),
          Spacer(1, 12),
          P("验收测试：设计师能找到全部页面、完成一次局部改动及拒绝/接受；开发者能按 README 复现指定版本与错误态。候选失败时 v1 与此前交付快照不变。建议 5–8 位设计师和 2–3 位开发者做初轮任务测试，这些数字是计划而非结果。"),
          H("必须先核实", 2),
          P("① 真实 Design 任务是否保留完整 HTML 源码；② 当前画布/评论是否已有版本回退；③ 输出产物与浏览器/文件工作区如何关联；④ Figma 输入目前通过附件、链接还是连接器。若已有等价能力，应优化可见性和衔接，不重复建设。"),
          H("主要来源", 2),
          P('<link href="https://autoclaw.zhipuai.cn/blog/product/auto-design-ai-designer/" color="#147D84">[S1] AutoClaw Auto Design 官方介绍</link>', "source"),
          P('<link href="https://www.lovart.art/docs/edit-your-design/customize-your-canvas" color="#147D84">[S2] Lovart Customize Your Canvas</link>', "source"),
          P('<link href="https://docs.pen.dev/design-and-code/design-to-code" color="#147D84">[S3] pen.dev Design ↔ Code</link>', "source"),
          P("用户录屏原件与完整证据图路径见同包 Markdown。该视频未覆盖 HTML Design 任务，故本稿是待验证的 MVP 方案，不是现状测评结论。", "small")]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                        topMargin=62, bottomMargin=61,
                        title="AutoClaw Design Agent 工作区 MVP 产品方案初稿 V03",
                        author="Codex", subject="基于录屏和官方资料的 Design Agent MVP 产品方案")
doc.build(story, onFirstPage=cover, onLaterPages=later)
print(OUT)
