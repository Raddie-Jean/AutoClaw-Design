from pathlib import Path
from html import escape

OUT = Path(__file__).parent
W, H = 1600, 900
C = {
    "bg": "#F7F9F7", "paper": "#FFFFFF", "ink": "#17383B",
    "muted": "#60716F", "line": "#DDE6E2", "teal": "#12877D",
    "teal_light": "#E5F4F0", "amber": "#F5AB6E", "amber_light": "#FFF0E3",
    "blue": "#DDEBEF", "violet": "#EEE8F7", "dark": "#122D31",
}
FONT = "'PingFang SC','Noto Sans SC',sans-serif"


class Slide:
    def __init__(self, n, section, title, subtitle="", dark=False):
        self.n = n
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
        self.rect(0, 0, W, H, C["dark"] if dark else C["bg"])
        if not dark:
            self.rect(0, 0, 17, H, C["teal"])
            self.text(89, 56, section.upper(), 21, C["teal"], 700, letter_spacing="2")
            self.text(88, 125, title, 49, C["ink"], 700)
            if subtitle:
                self.text(90, 165, subtitle, 23, C["muted"], 400)
            self.line(88, 788, 1512, 788, C["line"], 2)
            self.text(88, 833, "AutoClaw · Design Agent 工作区 / 方案汇报 V09", 18, C["muted"])
            self.text(1490, 833, f"{n:02d} / 12", 18, C["muted"], anchor="end")

    def rect(self, x, y, w, h, fill, r=0, stroke=None, sw=1):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"' + (f' stroke="{stroke}" stroke-width="{sw}"' if stroke else "") + '/>')

    def line(self, x1, y1, x2, y2, color, sw=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{d}/>')

    def circle(self, x, y, r, fill, stroke=None, sw=1):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"' + (f' stroke="{stroke}" stroke-width="{sw}"' if stroke else "") + '/>')

    def text(self, x, y, value, size=24, color=None, weight=400, anchor="start", letter_spacing=None):
        ls = f' letter-spacing="{letter_spacing}"' if letter_spacing else ""
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{color or C["ink"]}" text-anchor="{anchor}"{ls}>{escape(str(value))}</text>')

    def lines(self, x, y, values, size=24, gap=39, color=None, weight=400):
        for i, v in enumerate(values):
            self.text(x, y + i * gap, v, size, color, weight)

    def pill(self, x, y, w, label, fill=None, color=None, size=19):
        self.rect(x, y, w, 37, fill or C["teal_light"], 18)
        self.text(x + w / 2, y + 26, label, size, color or C["teal"], 700, "middle")

    def card(self, x, y, w, h, title, body, fill=None, accent=None, title_size=29, body_size=23):
        self.rect(x, y, w, h, fill or C["paper"], 19, C["line"])
        if accent:
            self.rect(x, y, 8, h, accent, 4)
        self.text(x + 29, y + 52, title, title_size, C["ink"], 700)
        self.lines(x + 29, y + 100, body, body_size, 36, C["muted"])

    def save(self, name):
        self.parts.append('</svg>')
        (OUT / name).write_text('\n'.join(self.parts), encoding='utf-8')


def arrow(s, x1, y, x2, color=None):
    col = color or C["teal"]
    s.line(x1, y, x2 - 14, y, col, 3)
    s.line(x2 - 25, y - 10, x2 - 14, y, col, 3)
    s.line(x2 - 25, y + 10, x2 - 14, y, col, 3)


# 01 Cover
s = Slide(1, "", "", dark=True)
s.rect(86, 84, 242, 44, C["teal"], 22)
s.text(207, 114, "产品设计测试题 · 汇报稿", 20, C["paper"], 700, "middle")
s.text(87, 247, "从 AI 初稿", 72, C["paper"], 700)
s.text(87, 344, "到可交付方案", 72, C["paper"], 700)
s.rect(87, 397, 907, 8, C["amber"], 4)
s.lines(88, 478, ["Design Agent 工作区设计：", "让设计师看清结果、精准修订，并和 PM / 开发围绕同一版本决策。"], 28, 47, "#CBE2DC")
s.rect(1107, 186, 380, 470, "#24464A", 28)
for i, (a, b) in enumerate([("01", "看清初稿"), ("02", "控制修改"), ("03", "阶段共识"), ("04", "固定交付")]):
    y = 255 + i * 100
    s.circle(1168, y, 27, C["teal"] if i == 1 else "#43676A")
    s.text(1168, y + 8, a, 21, C["paper"], 700, "middle")
    s.text(1223, y + 9, b, 28, C["paper"], 600)
s.text(88, 811, "2026.10.05  ·  基于研究 V01–V07 与可点击原型 V08", 20, "#8EACA8")
s.save("01_封面.svg")

# 02 Process evolution
s = Slide(2, "01 / 过程", "从发散到收敛：我们如何选中这个问题", "每一步都在缩小设计范围，而不是继续堆叠工具。")
stages = [
    ("V01–02", "竞品与产物", "多格式生成与交付"),
    ("V03", "工作区 MVP", "HTML 是主产物"),
    ("V04–05", "旅程与共创", "明确评审先后"),
    ("V06–07", "草图与修订", "三态 + 定域修改"),
    ("V08", "可点击原型", "验证一条主链路"),
]
for i, (v, h, b) in enumerate(stages):
    x = 88 + i * 290
    s.card(x, 255, 266, 232, h, [b], C["paper"], C["teal"] if i == 3 else None, 28, 22)
    s.pill(x + 23, 420, 107, v, C["teal_light"], C["teal"], 18)
    if i < 4:
        arrow(s, x + 269, 370, x + 288)
s.rect(88, 555, 1424, 164, C["dark"], 19)
s.text(122, 606, "最终取舍", 29, C["paper"], 700)
s.lines(122, 649, ["不把无限画布当作 MVP 主功能；不承诺任意 HTML → Figma 无损转换。", "聚焦一次真实工作：AI 初稿 → 局部修订 → 阶段评审 → 固定版本交付。"], 25, 38, "#DCEBE6")
s.save("02_思路演化.svg")

# 03 Evidence
s = Slide(3, "02 / 证据", "研究发现：成熟工具已覆盖生成与局部编辑", "本方案关注的是生成后的控制、决策与交接。")
s.card(88, 224, 446, 383, "AutoClaw：任务与产物入口", ["录屏可见任务、项目、对话与", "连接器；客户端可见产物/工作", "区容器。HTML Design 全链路", "尚未由录屏验证。"], accent=C["teal"])
s.card(577, 224, 446, 383, "Lovart：对象化局部编辑", ["录屏可见选中对象、Quick Edit、", "原稿旁生成候选。启发是先指明", "修改对象，再保留可比较结果。", "不能直接照搬到 HTML 源码。"], accent=C["amber"])
s.card(1066, 224, 446, 383, "外部研究：判断权仍在人", ["Figma 调查与研究支持清晰目标、", "多方向预览、位置化反馈与", "设计开发协作。样本不是", "AutoClaw 目标用户。"], accent=C["teal"])
s.rect(88, 642, 1424, 94, C["amber_light"], 16)
s.text(116, 681, "证据边界", 24, "#A15C25", 700)
s.text(263, 681, "外部数据只支持方向判断；痛点频率和当前产品能力仍需真实 HTML 任务验证。", 23, "#855A3B")
s.text(116, 716, "来源与样本范围见随附 MD 的“研究依据”章节。", 19, "#855A3B")
s.save("03_研究证据.svg")

# 04 Journey
s = Slide(4, "03 / 用户旅程", "从传统串行交接，走向同一方案上的共创", "共创不意味着取消评审；它让评论、修改与版本都落在同一个对象上。")
phases = ["需求定义", "思维发散", "方案设计", "Demo 展示", "可交付方案", "微调方案", "上线方案"]
for i, phase in enumerate(phases):
    x = 88 + i * 204
    s.rect(x, 274, 187, 104, C["paper"], 17, C["line"])
    s.circle(x + 36, 309, 20, C["teal_light"])
    s.text(x + 36, 316, str(i + 1), 21, C["teal"], 700, "middle")
    s.text(x + 20, 357, phase, 23, C["ink"], 700)
    if i < 6:
        arrow(s, x + 188, 326, x + 203)
s.text(90, 456, "关键判断点", 25, C["muted"], 700)
for x, label, body in [(104, "G0 需求对齐", "确认问题"), (513, "G1 概念确认", "选方向"), (922, "G2 Demo 评审", "验体验"), (1331, "G3 开发接手", "复现版本")]:
    s.circle(x, 505, 10, C["amber"])
    s.pill(x - 8, 530, 169, label, C["amber_light"], "#9C5A2D", 18)
    s.text(x + 6, 600, body, 22, C["muted"])
s.rect(88, 660, 1424, 74, C["teal_light"], 16)
s.text(112, 709, "开发提前介入条件：真实接口、权限、复杂状态、跨端一致性、性能或现有代码约束。", 25, C["teal"], 600)
s.save("04_共创旅程.svg")

# 05 Sketch stages
s = Slide(5, "04 / 草图阶段", "草图的三种状态：保留可能性，再逐步收敛", "草图评审要轻量；只有第三态结束才形成进入 Demo 的概念基线。")
cards = [
    ("01", "草图收集", ["PRD 片段、参考、手绘、", "未尝试概念与 AI 生成物", "允许不完整和矛盾并存"], "无需批准；值得深化即可入围"),
    ("02", "定义概念", ["选择 1–3 个方向并排比较", "在原方向上连续局部修订", "PM 与设计师持续讨论"], "保留主方向与备选，细节仍可变"),
    ("03", "概念确定", ["确认核心路径与设计原则", "记录拒绝理由和未决问题", "必要时请开发做技术预检"], "G1：PM + 设计师确认后进 Demo"),
]
for i, (num, title, body, exit_line) in enumerate(cards):
    x = 88 + i * 486
    s.rect(x, 223, 454, 464, C["paper"], 22, C["line"])
    s.circle(x + 55, 284, 29, C["teal"] if i == 2 else C["teal_light"])
    s.text(x + 55, 293, num, 23, C["paper"] if i == 2 else C["teal"], 700, "middle")
    s.text(x + 102, 296, title, 31, C["ink"], 700)
    s.lines(x + 31, 380, body, 24, 46, C["muted"])
    s.line(x + 31, 564, x + 423, 564, C["line"])
    s.text(x + 31, 615, exit_line, 21, C["teal"], 600)
    if i < 2:
        arrow(s, x + 455, 456, x + 483)
s.save("05_草图三态.svg")

# 06 Pain points
s = Slide(6, "05 / 用户问题", "优先解决三处断点，重点放在“改不准”", "它们是基于场景与研究提出的优先级假设，等待目标用户任务测试。")
items = [
    ("H1", "看不全", "初稿覆盖了哪些方向、页面、状态？", "成果总览与覆盖清单", C["blue"]),
    ("H2", "改不准", "AI 是否理解这次只改哪一处？", "界面定域修订 + 候选对比", C["teal_light"]),
    ("H3", "交不清", "PM 和开发拿到的是哪一版？", "固定交付快照与状态表", C["amber_light"]),
]
for i, (code, title, question, response, fill) in enumerate(items):
    x = 88 + i * 486
    s.rect(x, 242, 454, 413, fill, 22)
    s.text(x + 30, 302, code, 24, C["teal"], 700)
    s.text(x + 30, 370, title, 39, C["ink"], 700)
    s.text(x + 30, 427, question, 22, C["muted"])
    s.line(x + 30, 489, x + 424, 489, C["line"])
    s.text(x + 30, 543, "MVP 响应", 19, C["muted"], 700)
    s.text(x + 30, 591, response, 25, C["ink"], 600)
s.pill(650, 695, 302, "H2 是本题的核心 Feature", C["dark"], C["paper"], 20)
s.save("06_痛点排序.svg")

# 07 Core feature
s = Slide(7, "06 / 核心功能", "界面定域修订：一次有边界、可审阅的修改", "文字、点选组件、画笔圈选是三种入口，共用同一张修订卡。")
steps = [
    ("1", "定位上下文", ["方向 / 页面 / 状态", "设备断点 / 基线版本"]),
    ("2", "选目标", ["文字 / 组件 / 画笔", "先显示实际命中对象"]),
    ("3", "说清边界", ["改什么 / 保留什么", "仅此状态或共享实例"]),
    ("4", "生成候选", ["隔离修改源文件", "预览与影响检查"]),
    ("5", "人来决定", ["比较 / 继续限定", "采纳或放弃"]),
]
for i, (n, title, body) in enumerate(steps):
    x = 88 + i * 290
    s.rect(x, 241, 266, 335, C["paper"], 18, C["line"])
    s.circle(x + 45, 292, 26, C["teal"])
    s.text(x + 45, 300, n, 24, C["paper"], 700, "middle")
    s.text(x + 25, 365, title, 29, C["ink"], 700)
    s.lines(x + 25, 428, body, 22, 38, C["muted"])
    if i < 4:
        arrow(s, x + 268, 405, x + 289)
s.rect(88, 628, 1424, 108, C["dark"], 18)
s.text(118, 673, "示例", 23, C["amber"], 700)
s.text(202, 673, "方向 B / 邀请成员 / Mobile 错误态 / v3：把错误提示移近邮箱框，保留桌面与成功态。", 23, C["paper"])
s.text(202, 710, "设计师采纳候选成为 v4；这不等于 PM 已确认概念，也不等于生产代码可直接合并。", 21, "#C8DFD9")
s.save("07_定域修订.svg")

# 08 Review roles
s = Slide(8, "07 / 评审节奏", "把“修改采纳”和“阶段批准”分开", "PM、设计师、开发先后介入，各自判断不同的问题。")
rows = [
    ("工作版修订", "设计师", "候选是否改对、是否越界", "可高频进行；不改批准基线"),
    ("G1 概念确认", "PM + 设计师", "核心路径与原则是否成立", "确认后进入可运行 Demo"),
    ("技术预检", "开发按风险介入", "接口/权限/组件/跨端风险", "高风险项目提前到 G1 前"),
    ("G2 Demo 体验", "PM + 设计师 + 开发", "关键路径、异常态与实现边界", "通过后才能准备交付"),
    ("G3 开发接手", "开发主责", "能否复现同一版本与状态", "不是自动合并生产代码"),
]
s.rect(88, 224, 1424, 70, C["dark"], 15)
for x, t in [(113,"决策"),(431,"参与人"),(734,"判断什么"),(1160,"结果")]:
    s.text(x, 269, t, 23, C["paper"], 700)
for i, (phase, owner, judgement, result) in enumerate(rows):
    y = 307 + i * 84
    s.rect(88, y, 1424, 76, C["paper"] if i % 2 == 0 else "#F0F5F2", 11)
    s.text(113, y + 48, phase, 24, C["ink"], 700)
    s.text(431, y + 48, owner, 23, C["muted"])
    s.text(734, y + 48, judgement, 23, C["muted"])
    s.text(1160, y + 48, result, 21, C["teal"])
s.save("08_评审节奏.svg")

# 09 IA
s = Slide(9, "08 / 信息架构", "沿用 AutoClaw 任务归属，新增 Design 工作区", "工作区按用户判断组织，而不是按 AI 工具名称堆导航。")
s.rect(88, 233, 424, 495, C["paper"], 20, C["line"])
s.text(120, 286, "AutoClaw 现有外壳", 28, C["ink"], 700)
for i, (depth, label) in enumerate([(0,"项目"),(1,"任务：邀请成员流程"),(2,"Design 工作区"),(3,"方向 B / v4"),(4,"页面 × 状态 × 设备")]):
    y = 351 + i * 72
    s.circle(137 + depth * 23, y - 8, 8, C["teal"] if i >= 2 else C["amber"])
    s.text(158 + depth * 23, y, label, 24, C["ink"] if i >= 2 else C["muted"], 600 if i >= 2 else 400)
arrow(s, 515, 465, 586)
views = [
    ("成果总览", "方向、覆盖与未解决项"),
    ("聚焦预览", "运行页面、设备和状态"),
    ("修订审阅", "候选差异、影响与决定"),
    ("交付快照", "确认版本、文件与说明"),
]
for i, (title, desc) in enumerate(views):
    x = 606 + (i % 2) * 450
    y = 250 + (i // 2) * 225
    s.card(x, y, 420, 196, title, [desc], C["paper"], C["teal"] if i == 2 else None, 29, 21)
s.rect(606, 697, 870, 49, C["teal_light"], 12)
s.text(632, 729, "关键约束：预览确认版本 ID = 交付快照版本 ID", 21, C["teal"], 700)
s.save("09_信息架构.svg")

# 10 Prototype
s = Slide(10, "09 / 原型", "已落地一条从初稿到交付的可点击主路径", "用“邀请成员流程”的 Mobile 错误态验证信息结构和决策顺序。")
screens = [
    ("01", "成果总览", "A/B/C 三方向"),
    ("02", "可运行预览", "文字 / 智能 / 画笔"),
    ("03", "候选比较", "原版 vs 隔离候选"),
    ("04", "阶段评审", "G1 概念 → G2 Demo"),
    ("05", "固定交付", "版本与未决问题"),
]
for i, (n, title, body) in enumerate(screens):
    x = 88 + i * 290
    s.rect(x, 268, 265, 342, C["paper"], 18, C["line"])
    s.rect(x + 22, 294, 221, 156, C["teal_light"], 12)
    s.rect(x + 41, 321, 69, 14, "#B7D9D0", 5)
    s.rect(x + 41, 350, 180, 13, "#CEE6DF", 5)
    s.rect(x + 41, 377, 155, 13, "#CEE6DF", 5)
    s.rect(x + 41, 408, 98, 20, C["teal"], 7)
    s.text(x + 22, 492, n, 22, C["teal"], 700)
    s.text(x + 22, 535, title, 27, C["ink"], 700)
    s.text(x + 22, 573, body, 20, C["muted"])
    if i < 4:
        arrow(s, x + 267, 435, x + 287)
s.rect(88, 654, 1424, 83, C["amber_light"], 15)
s.text(118, 707, "原型边界：候选修改和状态切换为交互模拟；真实 AI、HTML 源文件回写与生产交付尚待验证。", 23, "#885936")
s.save("10_原型链路.svg")

# 11 MVP boundary
s = Slide(11, "10 / MVP 取舍", "先验证闭环，再扩大格式与画布能力", "可交付的含义是“版本明确、可复现、信息完整”，不是自动上线。")
columns = [
    ("P0 · 现在做", C["teal_light"], ["AutoClaw 自生成 HTML", "页面/状态/断点索引", "文字与元素定域修改", "受限画笔 + 命中确认", "候选比较 / 采纳 / 放弃", "固定版本交付快照"]),
    ("P1 · 下一步", C["blue"], ["对象锚定的异步评论", "1–3 方向并排评审", "跨页面回归清单", "约束模板与负责人", "技术风险提前提醒"]),
    ("后续 · 暂不承诺", C["amber_light"], ["无限画布全功能", "任意外部网页原位修改", "Figma ↔ HTML 无损双向同步", "图片/视频统一精准编辑", "自动合并生产仓库"]),
]
for i, (title, fill, body) in enumerate(columns):
    x = 88 + i * 486
    s.rect(x, 230, 454, 492, fill, 21)
    s.text(x + 28, 286, title, 30, C["ink"], 700)
    for j, item in enumerate(body):
        y = 343 + j * 61
        s.circle(x + 37, y - 8, 7, C["teal"] if i == 0 else C["muted"])
        s.text(x + 56, y, item, 22, C["ink"])
s.save("11_MVP边界.svg")

# 12 Validation
s = Slide(12, "11 / 验证与下一步", "把方案变成可检验的产品判断", "下一轮先用真实 Auto Design HTML 任务核对现状，再测设计与研发接力。")
s.card(88, 225, 678, 383, "设计师任务测试 · 建议 5–8 人", ["能否找到全部页面、状态和当前版？", "能否在不重述整页需求时完成两次微调？", "能否识别候选的越界变化并正确回退？", "能否区分“采纳修订”和“确认方案”？"], accent=C["teal"], body_size=22)
s.card(834, 225, 678, 383, "开发接手测试 · 建议 2–3 人", ["能否按说明运行同一 HTML 版本？", "能否独立复现 Mobile 错误态与成功态？", "是否看得见接口、权限和未解决问题？", "需要追问哪些关键假设？"], accent=C["amber"], body_size=22)
s.rect(88, 648, 1424, 93, C["dark"], 16)
s.text(118, 687, "汇报结论", 23, C["amber"], 700)
s.text(255, 688, "AI 负责生成候选与提示影响；设计师、PM、开发围绕同一版本作出不同阶段的决定。", 24, C["paper"])
s.text(118, 722, "先跑通一条“看清 → 改准 → 审准 → 交清”的 HTML 主链路，再判断是否需要无限画布与跨格式同步。", 21, "#D1E2DE")
s.save("12_验证计划.svg")

print(f"Generated 12 SVG pages in {OUT}")
