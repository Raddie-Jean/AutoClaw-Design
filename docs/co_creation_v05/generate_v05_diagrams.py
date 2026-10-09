#!/usr/bin/env python3
"""Generate editable SVG discussion diagrams for the V05 co-creation proposal."""

from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent
NAVY, TEAL, INK = '#12303E', '#09888A', '#203A48'
MUTED, LIGHT, PAPER = '#5B7480', '#E8F5F2', '#F4F8F8'
WHITE, LINE, GOLD = '#FFFFFF', '#D0E1DE', '#C18D47'
ORANGE, ORANGE_BG = '#A45837', '#FFF1E9'
FONT = 'PingFang SC, PingFang TC, Arial, sans-serif'


def r(x, y, w, h, fill=WHITE, rad=0, stroke=None, sw=1):
    edge = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rad}" fill="{fill}"{edge}/>'


def t(x, y, value, size=22, color=INK, weight=400, anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(str(value))}</text>'


def tl(x, y, values, size=21, color=INK, weight=400, dy=33):
    return ''.join(t(x, y + i * dy, value, size, color, weight) for i, value in enumerate(values))


def ln(x1, y1, x2, y2, color=LINE, width=2, dash=None):
    pattern = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{pattern}/>'


def arrow(x1, y, x2, color=TEAL):
    return ln(x1, y, x2, y, color, 3) + f'<path d="M{x2-10} {y-7} L{x2} {y} L{x2-10} {y+7}" fill="none" stroke="{color}" stroke-width="3"/>'


def save(name, w, h, elements):
    markup = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + ''.join(elements) + '</svg>'
    path = ROOT / (name + '.svg')
    path.write_text(markup, encoding='utf-8')
    print(path)


stages = [
    ('01', '需求定义', 'PM + 设计师', ['问题 / 目标用户', '成功标准 / 约束'], 'G0 需求对齐', ['确认“要解决什么”', '避免过早批准 UI'], ['归纳资料冲突', '提出待确认问题']),
    ('02', '思维发散', '设计师 + PM', ['草图 / 流程', '方向 A/B / 参考'], 'G1 草图共评', ['选方向、保留异议', '不等到高保真才评'], ['生成方案变体', '整理锚定反馈']),
    ('03', '方案设计', '设计师主导', ['页面流 / 状态', '组件与交互规则'], '技术预检', ['高风险时邀开发', '提前校验实现边界'], ['补状态清单', '提示技术风险']),
    ('04', 'Demo 展示', '设计师 + PM + 前端', ['可运行 HTML', '关键路径 / 多端态'], 'G2 体验评审', ['PM 认可体验', '前端判断实现路径'], ['候选修改预览', '差异与影响摘要']),
    ('05', '可交付方案', '设计师 + 前端', ['确认版 / 状态表', '资源 / 决策说明'], 'G3 开发接手', ['能复现、能继续做', '固定交付版本'], ['整理交付清单', '检查遗漏与错版']),
    ('06', '微调方案', '三方按需参与', ['开发中新发现', '基线旁的候选变更'], '变更评审', ['小改审影响', '大改回到 G2'], ['比对受影响范围', '保留历史基线']),
    ('07', '上线方案', '前端 + 设计师 + PM', ['实现版本', '偏差 / 验收记录'], 'G4 上线验收', ['确认关键路径', '记录剩余偏差'], ['比对设计与实现', '生成偏差清单']),
]

W, H = 2650, 1330
e = [r(0, 0, W, H, PAPER), r(0, 0, W, 13, TEAL),
     t(70, 99, '七阶段共创旅程｜评审前移，交付有序', 50, NAVY, 700),
     t(70, 151, '共同讨论贯穿全程；G0–G4 是决策记录，不是把所有修改锁进会议。', 25, MUTED),
     r(2165, 89, 410, 58, LIGHT, 30), t(2370, 127, 'V05 · 讨论稿', 22, TEAL, 600, 'middle')]

for i, (num, title, roles, artifacts, gate, decisions, ai) in enumerate(stages):
    x = 65 + i * 371
    y = 208
    head = TEAL if i < 3 else NAVY
    e += [r(x, y, 350, 965, WHITE, 18, LINE, 2),
          r(x, y, 350, 110, head, 18), r(x, y + 77, 350, 33, head),
          t(x + 24, y + 42, num, 21, '#BDE2DE', 700),
          t(x + 24, y + 84, title, 31, WHITE, 700),
          t(x + 24, y + 159, '参与者', 19, TEAL, 700),
          t(x + 24, y + 200, roles, 21, INK, 600),
          ln(x + 24, y + 231, x + 326, y + 231),
          t(x + 24, y + 273, '当阶段产物', 19, TEAL, 700),
          tl(x + 24, y + 313, artifacts, 21, INK, dy=35),
          r(x + 16, y + 410, 318, 230, ORANGE_BG if i in (1, 2, 3, 4) else LIGHT, 14),
          t(x + 30, y + 452, gate, 22, ORANGE if i in (1, 2, 3, 4) else TEAL, 700),
          tl(x + 30, y + 501, decisions, 20, INK, dy=37),
          r(x + 16, y + 658, 318, 198, LIGHT, 14),
          t(x + 30, y + 699, 'AI 辅助', 19, TEAL, 700),
          tl(x + 30, y + 748, ai, 20, INK, dy=36),
          t(x + 24, y + 913, '共创意见 → 候选 → 人确认', 18, MUTED)]
    if i < 6:
        e.append(arrow(x + 352, y + 57, x + 368))

e += [r(65, 1208, 2520, 69, NAVY, 14),
      t(95, 1251, '技术介入原则：方案早期做风险预检；Demo 评审和开发接手由前端正式参与。已确认方案通过版本化变更继续演进。', 23, WHITE, 600)]
save('2026-10-04_七阶段共创旅程图_V05', W, H, e)


W, H = 2280, 1430
e = [r(0, 0, W, H, PAPER), r(0, 0, W, 13, TEAL),
     t(80, 100, '共享设计空间｜信息架构 V05', 51, NAVY, 700),
     t(80, 155, '画布承载探索；评审记录决策；聚焦预览处理精修；版本快照负责交付。', 24, MUTED),
     r(1850, 90, 340, 58, LIGHT, 29), t(2020, 129, 'V05 · 讨论稿', 22, TEAL, 600, 'middle')]

# Entry and decision track.
e += [r(80, 215, 480, 125, WHITE, 18, LINE, 2),
      t(110, 263, '沿用 AutoClaw', 21, TEAL, 700),
      t(110, 307, '项目 → 任务 → 设计空间', 27, NAVY, 700),
      arrow(564, 277, 640),
      r(646, 215, 1554, 125, NAVY, 18),
      t(683, 260, '贯穿阶段的决策轨道', 21, '#B6DAD9', 700),
      t(683, 307, 'G0 需求对齐     →     G1 草图方向     →     G2 Demo 体验     →     G3 开发接手     →     G4 上线验收', 24, WHITE, 600)]

e += [t(80, 410, '同一个共享空间，三种工作方式', 29, NAVY, 700)]

# Three modes.
zones = [
    (80, 450, 1030, '可扩展共创画布', '探索与共同判断',
     ['需求 / 证据卡     草图 / 流程卡', '方向 A/B/C       Demo 入口', '锚定评论 / 分区 / 并排比较'],
     '可平移缩放和扩展；不把所有外部文件强制转为同一种格式'),
    (1130, 450, 515, '聚焦编辑与预览', '选中一件产物后进入',
     ['草图：新方向变体', 'HTML：运行态与设备预览', '修改：原版 / 候选对照'],
     '各格式用合适的编辑器'),
    (1665, 450, 535, '评审与决策面板', '与选中对象同上下文',
     ['PM：问题与方向意见', '设计师：候选与体验判断', '开发：可行性与接手意见'],
     'AI 生成提案；人记录决策'),
]
for x, y, w, head, sub, details, foot in zones:
    e += [r(x, y, w, 495, WHITE, 19, LINE, 2),
          r(x, y, w, 10, TEAL),
          t(x + 30, y + 75, head, 33, NAVY, 700),
          t(x + 30, y + 116, sub, 21, MUTED),
          ln(x + 30, y + 145, x + w - 30, y + 145),
          tl(x + 30, y + 203, details, 23, INK, dy=61),
          r(x + 25, y + 403, w - 50, 58, LIGHT, 13),
          t(x + 39, y + 441, foot, 19 if w < 600 else 22, TEAL, 600)]

e += [r(80, 987, 2120, 157, NAVY, 17),
      t(112, 1040, '锚定式共创提案（MVP 唯一深入的 Feature）', 27, WHITE, 700),
      t(112, 1091, '选中草图 / 流程 / Demo 状态  →  提意见  →  AI 出候选与影响  →  并排审阅  →  负责人采纳 / 调整 / 拒绝', 23, '#DFEFEC'),
      r(80, 1175, 1025, 166, WHITE, 17, LINE, 2),
      r(1125, 1175, 1075, 166, WHITE, 17, LINE, 2),
      t(110, 1228, '产物关系底座', 23, TEAL, 700),
      t(110, 1275, '来源 · 类型 · 对象 ID · 版本 · 状态 · 关联与负责人', 21, INK),
      t(1155, 1228, '已确认基线 / 交付快照', 23, TEAL, 700),
      t(1155, 1275, '设计批准版 → 可运行源码与说明 → 开发接手与上线记录', 21, INK),
      t(80, 1394, '画布是可扩展视图；外部源文件、决策和交付版本各有权威来源。探索不会自动覆盖已批准基线。', 22, MUTED)]
save('2026-10-04_共创空间信息架构图_V05', W, H, e)
