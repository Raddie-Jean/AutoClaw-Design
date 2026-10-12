#!/usr/bin/env python3
"""Create discussion-ready SVG/PNG journey and information architecture diagrams."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAVY = '#142E3D'
INK = '#203B49'
MUTED = '#627986'
TEAL = '#087F85'
LIGHT = '#E9F5F3'
PAPER = '#F5F8F8'
WHITE = '#FFFFFF'
LINE = '#CFDFDF'
RISK = '#A84F43'
RISK_BG = '#FFF0EB'
GOLD = '#D49B51'
FONT = "PingFang SC, PingFang TC, Arial, sans-serif"


def rect(x, y, w, h, fill, radius=0, stroke=None, sw=1):
    edge = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"{edge}/>'


def line(x1, y1, x2, y2, color=LINE, width=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{d}/>'


def txt(x, y, value, size=22, color=INK, weight=400, anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(str(value))}</text>'


def lines(x, y, values, size=21, color=INK, weight=400, leading=34):
    return ''.join(txt(x, y + i * leading, value, size, color, weight) for i, value in enumerate(values))


def svg(width, height, pieces):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">' + ''.join(pieces) + '</svg>'


def save(name, width, height, pieces):
    source = svg(width, height, pieces)
    svg_file = ROOT / f'{name}.svg'
    svg_file.write_text(source, encoding='utf-8')
    print(svg_file)


stages = [
    dict(title='接收初稿', action=['打开已完成任务，', '找到 Design 结果'], thought=['“我拿到的', '到底是什么？”'], pain=['聊天结果可见，', '但多页面 HTML 的完整性', '还需要实测。'], solution=['任务内成果入口', '确认版本与缺失项', '同屏可见'], evidence='V03 录屏观察'),
    dict(title='清点覆盖', action=['对照 PRD，检查页面、', '流程与错误/成功态'], thought=['“有没有漏掉', '关键页面或状态？”'], pain=['跨多屏预览与比较', '容易丢失全局线索。'], solution=['页面 × 状态清单', '生成/待复核/缺失标记', '快速进入对应页面'], evidence='E2 · 24 人 GenUI 研究'),
    dict(title='真实预览', action=['走 Desktop/Mobile', '关键交互路径'], thought=['“看起来对，', '操作起来也对吗？”'], pain=['静态缩略图难以说明', '交互、异常与断点。'], solution=['可运行 HTML 预览', '页面/状态/设备切换', '版本持续可见'], evidence='题面 HTML 产物逻辑'),
    dict(title='定位精修', action=['选中移动端错误提示，', '提出具体修改'], thought=['“AI 明白', '我说的是哪里吗？”'], pain=['自由指令可能没有绑定', '页面、状态和选区；', '影响范围不明。'], solution=['目标锚定的修改卡', '默认“仅此状态”', '展示预计影响范围'], evidence='E3 · 21 人反馈研究'),
    dict(title='审阅确认', action=['比较原版和候选，', '排查误伤后接受'], thought=['“这份候选', '能成为正式版吗？”'], pain=['试验结果与正式版本', '若混在一起，容易误用。'], solution=['原版/候选并排', '接受/拒绝/继续改', '确认后形成 v2'], evidence='E1 · 自主决策信号'),
    dict(title='移交复现', action=['固定 v2，交给 PM', '与前端复现'], thought=['“对方拿到的是', '我确认的那版吗？”'], pain=['版本、状态、约束不清，', '前端需自行猜测意图。'], solution=['固定交付快照', '源码+状态表+说明', '已知问题同包交接'], evidence='E4 · 52% 假设差异'),
]

parts = [rect(0, 0, 2400, 1300, PAPER), rect(0, 0, 2400, 15, TEAL),
         txt(78, 98, '设计师用户旅程｜从 AI 生成初稿到开发接手', 46, NAVY, 700),
         txt(78, 151, '主场景：移动端邀请流程错误态精修  ·  方案推论 / 外部数据 / 产品观察分开标注', 23, MUTED),
         rect(1780, 82, 548, 60, LIGHT, 30),
         txt(2054, 121, 'V04 · 2026.10.04 · 讨论稿', 22, TEAL, 600, 'middle')]

for i, d in enumerate(stages):
    x = 78 + i * 382
    y = 215
    parts += [rect(x, y, 360, 970, WHITE, 20, LINE, 2),
              rect(x, y, 360, 112, NAVY if i in (3, 4, 5) else TEAL, 20),
              rect(x, y + 78, 360, 34, NAVY if i in (3, 4, 5) else TEAL),
              txt(x + 28, y + 46, f'0{i+1}', 22, '#B8DFDD', 600),
              txt(x + 28, y + 87, d['title'], 31, WHITE, 700),
              txt(x + 27, y + 163, '设计师动作', 19, TEAL, 700),
              lines(x + 27, y + 201, d['action'], 21, INK, leading=34),
              line(x + 27, y + 260, x + 333, y + 260),
              txt(x + 27, y + 303, '心里问题', 19, TEAL, 700),
              lines(x + 27, y + 341, d['thought'], 21, INK, 600, 34),
              rect(x + 16, y + 411, 328, 180, RISK_BG, 14),
              txt(x + 30, y + 450, '待验证的风险', 19, RISK, 700),
              lines(x + 30, y + 492, d['pain'], 20, INK, leading=31),
              rect(x + 16, y + 608, 328, 233, LIGHT, 14),
              txt(x + 30, y + 647, '工作区应提供', 19, TEAL, 700),
              lines(x + 30, y + 691, d['solution'], 20, INK, leading=34),
              line(x + 27, y + 865, x + 333, y + 865),
              txt(x + 27, y + 905, '依据', 18, MUTED, 600),
              txt(x + 27, y + 941, d['evidence'], 19, MUTED)]
    if i < 5:
        arrow_x = x + 364
        parts += [line(arrow_x, y + 56, arrow_x + 14, y + 56, TEAL, 3),
                  f'<path d="M {arrow_x+7} {y+49} L {arrow_x+16} {y+56} L {arrow_x+7} {y+63}" fill="none" stroke="{TEAL}" stroke-width="3"/>']

parts += [txt(78, 1240, '优先处理 ④ → ⑤ → ⑥：修改范围、正式版本、交付一致性。严重度是方案假设，不是 AutoClaw 用户发生率。', 22, NAVY, 600)]
save('2026-10-04_设计师用户旅程图_V04', 2400, 1300, parts)


W, H = 2100, 1280
parts = [rect(0, 0, W, H, PAPER), rect(0, 0, W, 15, TEAL),
         txt(85, 100, 'Design 工作区｜信息架构草案', 48, NAVY, 700),
         txt(85, 155, '从已有任务进入，按“找结果 → 看实物 → 审修改 → 定交付”组织', 24, MUTED),
         rect(1685, 88, 330, 58, LIGHT, 29), txt(1850, 127, 'V04 · 讨论稿', 22, TEAL, 600, 'middle')]

# The entry model follows the existing AutoClaw task structure.
entry = [
    (85, 'AutoClaw 全局', ['项目', '任务']),
    (755, '当前 Design 任务', ['对话与输出产物', '设计成果 v1 卡片']),
    (1425, '设计工作区', ['成果总览（默认）', '可运行 HTML 项目']),
]
for x, head, rows in entry:
    parts += [rect(x, 215, 585, 165, WHITE, 18, LINE, 2),
              rect(x, 215, 585, 48, NAVY, 18), rect(x, 245, 585, 18, NAVY),
              txt(x + 23, 249, head, 22, WHITE, 600),
              txt(x + 25, 308, rows[0], 24, INK, 600),
              txt(x + 25, 347, rows[1], 24, INK)]
for x in (690, 1360):
    parts += [line(x, 297, x + 43, 297, TEAL, 4),
              f'<path d="M{x+31} 286 L{x+47} 297 L{x+31} 308" fill="none" stroke="{TEAL}" stroke-width="4"/>']

parts += [txt(85, 458, '任务内四个工作状态', 28, NAVY, 700),
          txt(2005, 458, '主路径', 21, TEAL, 600, 'end')]

workspace = [
    ('01', '成果总览', '我得到了什么？', ['方向 / 页面 / 状态', '资源与源文件', '生成异常与缺失项'], '默认进入'),
    ('02', '聚焦预览', '这版真的可用吗？', ['可运行 HTML', '页面 / 状态 / 设备', '选区与局部指令'], '当前确认版'),
    ('03', '修订审阅', '候选能成为主稿吗？', ['原版 ↔ 候选对比', '受影响页面 / 文件', '接受 / 拒绝 / 继续改'], '仅有候选时出现'),
    ('04', '交付快照', '别人能复现这版吗？', ['固定 version_id', '源码 / 资源 / 说明', '状态表 / 已知问题'], '只交付确认版'),
]
for i, (num, head, question, details, foot) in enumerate(workspace):
    x = 85 + i * 500
    parts += [rect(x, 490, 470, 420, WHITE, 20, LINE, 2),
              rect(x, 490, 470, 9, TEAL),
              txt(x + 27, 550, num, 21, TEAL, 700),
              txt(x + 27, 605, head, 32, NAVY, 700),
              txt(x + 27, 656, question, 21, MUTED),
              line(x + 27, 683, x + 443, 683),
              lines(x + 27, 733, details, 22, INK, leading=45),
              rect(x + 22, 853, 426, 39, LIGHT, 12),
              txt(x + 235, 881, foot, 19, TEAL, 600, 'middle')]
    if i < 3:
        ax = x + 472
        parts += [line(ax, 700, ax + 20, 700, TEAL, 3),
                  f'<path d="M{ax+11} 694 L{ax+21} 700 L{ax+11} 706" fill="none" stroke="{TEAL}" stroke-width="3"/>']

parts += [rect(85, 958, 1970, 115, NAVY, 16),
          txt(115, 1004, '全程固定上下文', 22, '#A9DBD9', 700),
          txt(115, 1045, '任务名   /   方向   /   当前确认版本   /   候选状态   /   交付状态', 25, WHITE, 600),
          rect(85, 1097, 952, 125, WHITE, 16, LINE, 2),
          rect(1057, 1097, 998, 125, WHITE, 16, LINE, 2),
          txt(112, 1140, '辅助上下文（随当前工作状态切换）', 20, TEAL, 700),
          txt(112, 1181, '输入资料 · Agent 对话 · 文件 · 修改记录', 22, INK),
          txt(1085, 1140, '内容对象（不是导航栏）', 20, TEAL, 700),
          txt(1085, 1181, 'HTML 项目 → 确认版本 → 固定交付快照', 22, INK),
          txt(85, 1254, '约束：候选先审阅再生效；预览正式版与交付包始终引用同一 version_id。', 22, MUTED)]
save('2026-10-04_Design工作区信息架构图_V04', W, H, parts)
