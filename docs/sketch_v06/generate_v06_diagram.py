#!/usr/bin/env python3
"""Create the sketch-stage and cumulative-edit discussion diagram."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME = "2026-10-04_草图三态与精准微调链路_V06"
W, H = 2280, 1370
NAVY = "#173340"
INK = "#24404B"
TEAL = "#087F7D"
MUTED = "#5E7480"
PAPER = "#F5F8F7"
WHITE = "#FFFFFF"
LINE = "#D5E3E1"
LIGHT = "#E7F4F0"
GOLD = "#B57635"
GOLD_BG = "#FFF3E6"
FONT = "PingFang SC, PingFang TC, Arial, sans-serif"


def rect(x, y, w, h, fill=WHITE, radius=0, stroke=None, sw=1):
    border = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"{border}/>'


def text(x, y, s, size=23, color=INK, weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(s)}</text>')


def lines(x, y, values, size=23, color=INK, dy=37, weight=400):
    return "".join(text(x, y + i * dy, value, size, color, weight) for i, value in enumerate(values))


def arrow(x1, y, x2, color=TEAL):
    return (f'<path d="M{x1} {y} H{x2}" stroke="{color}" stroke-width="3" fill="none"/>'
            f'<path d="M{x2-12} {y-8} L{x2} {y} L{x2-12} {y+8}" stroke="{color}" stroke-width="3" fill="none"/>')


e = [rect(0, 0, W, H, PAPER), rect(0, 0, W, 12, TEAL),
     text(72, 96, "草图三态 × 可累积精准微调", 49, NAVY, 700),
     text(72, 148, "先保留可能性，再选 1–3 个方向深化；概念确认后才进入运行体验。", 25, MUTED),
     rect(1920, 87, 288, 56, LIGHT, 28), text(2064, 124, "V06 · 讨论稿", 21, TEAL, 600, "middle")]

stages = [
    (72, "01  草图收集", ["资料、参考、未试概念", "自由发散并保留来源"], "不需要批准", LIGHT, TEAL),
    (615, "02  定义概念", ["选出 1–3 个方向", "局部精修、并排比较"], "允许细节继续变化", LIGHT, TEAL),
    (1158, "03  概念确定", ["PM + 设计师共同确认", "记录保留原则与待验证点"], "G1 概念确认", GOLD_BG, GOLD),
    (1701, "04  Demo 体验", ["验证关键路径与运行状态", "必要时带原因退回 02"], "进入下轮体验评审", LIGHT, TEAL),
]
for x, title, body, gate, bg, accent in stages:
    e += [rect(x, 217, 506, 288, WHITE, 18, LINE, 2),
          rect(x, 217, 506, 11, accent, 5),
          text(x + 28, 278, title, 31, NAVY, 700),
          lines(x + 28, 331, body, 23, INK, 39),
          rect(x + 24, 423, 458, 54, bg, 12),
          text(x + 40, 459, gate, 22, accent, 600)]
for x in (580, 1123, 1666):
    e.append(arrow(x, 359, x + 31))

e += [text(72, 573, "状态 02 中的关键循环：在同一概念上继续，而不是整图重来", 33, NAVY, 700),
      text(72, 614, "示例：方向 B 的袖口改为品牌绿；手势、背景、光影已认可，应持续保留。", 22, MUTED)]

steps = [
    (72, "① 选择目标", ["方向 B / 已接受 V3", "点选袖口或框选区域"]),
    (506, "② 表达意图", ["改成品牌绿", "锁定手势、背景、光影"]),
    (940, "③ 生成候选", ["图层：直接改属性", "位图：区域生成 + 合成"]),
    (1374, "④ 比较差异", ["原版 / 候选并排", "标记越界变化与边缘问题"]),
    (1808, "⑤ 人来决定", ["接受 → 成为 V4", "拒绝 → V3 不变"]),
]
for x, title, body in steps:
    e += [rect(x, 664, 399, 307, WHITE, 17, LINE, 2),
          rect(x, 664, 399, 77, NAVY, 17), rect(x, 721, 399, 20, NAVY),
          text(x + 24, 714, title, 27, WHITE, 700),
          lines(x + 25, 797, body, 22, INK, 45),
          rect(x + 24, 894, 351, 47, LIGHT, 10),
          text(x + 40, 926, "保留本次修改的上下文", 19, TEAL, 600)]
for x in (474, 908, 1342, 1776):
    e.append(arrow(x, 823, x + 26))

e += [rect(72, 1014, 2135, 150, NAVY, 17),
      text(104, 1065, "可累积，不等于锁死", 27, WHITE, 700),
      text(104, 1110, "接受 V4 后，下次修改默认以 V4 为底稿；旧版和被拒候选仍可回看。若要整体重构，创建新方向分支。", 23, "#E3F0ED"),
      rect(72, 1203, 1036, 92, WHITE, 14, LINE, 2),
      text(98, 1241, "设计价值", 21, TEAL, 700),
      text(98, 1275, "少重复提示，少丢失满意部分，保留探索空间", 22, INK),
      rect(1130, 1203, 1077, 92, WHITE, 14, LINE, 2),
      text(1156, 1241, "技术边界", 21, GOLD, 700),
      text(1156, 1275, "位图选区内部与边缘仍需人审；视频跨帧编辑暂缓", 22, INK),
      text(72, 1338, "原则：候选先预览，设计师采纳后才推进概念版本；PM 在概念确认时参与决策。", 22, MUTED)]

markup = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(e) + "</svg>"
path = ROOT / f"{NAME}.svg"
path.write_text(markup, encoding="utf-8")
print(path)
