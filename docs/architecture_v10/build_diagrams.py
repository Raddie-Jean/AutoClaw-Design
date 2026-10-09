from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
INK = '#1B3436'
MUTED = '#607472'
TEAL = '#11867D'
LIGHT = '#E8F4F1'
LINE = '#D8E2DE'
PAPER = '#F6F8F7'
WHITE = '#FFFFFF'
AMBER = '#FFF0D8'


class SVG:
    def __init__(self, title, subtitle, w=1600, h=900):
        self.w, self.h = w, h
        self.s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
                  f'<rect width="{w}" height="{h}" fill="{PAPER}"/>',
                  f'<rect x="0" y="0" width="12" height="{h}" fill="{TEAL}"/>']
        self.text(54, 68, title, 38, True)
        self.text(55, 109, subtitle, 19, False, MUTED)

    def rect(self, x, y, w, h, fill=WHITE, stroke=LINE, r=16, sw=1):
        self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, value, size=20, bold=False, color=INK, anchor='start'):
        self.s.append(f'<text x="{x}" y="{y}" font-family="PingFang SC, Noto Sans SC, Microsoft YaHei, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" text-anchor="{anchor}">{escape(value)}</text>')

    def lines(self, x, y, values, size=18, gap=32, color=MUTED):
        for i, value in enumerate(values):
            self.text(x, y+i*gap, value, size, False, color)

    def line(self, x1, y1, x2, y2, color=LINE, sw=2, dash=''):
        self.s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" {f"stroke-dasharray={chr(34)+dash+chr(34)}" if dash else ""}/>')

    def arrow(self, x1, y1, x2, y2, color=TEAL):
        self.line(x1,y1,x2,y2,color,3)
        import math
        a = math.atan2(y2-y1,x2-x1)
        p1=(x2-12*math.cos(a-.55),y2-12*math.sin(a-.55))
        p2=(x2-12*math.cos(a+.55),y2-12*math.sin(a+.55))
        self.s.append(f'<polyline points="{p1[0]},{p1[1]} {x2},{y2} {p2[0]},{p2[1]}" fill="none" stroke="{color}" stroke-width="3"/>')

    def pill(self, x, y, label, fill=LIGHT, color=TEAL, w=None):
        w = w or (len(label)*19+28)
        self.rect(x,y,w,35,fill,fill,17)
        self.text(x+14,y+24,label,16,True,color)
        return w

    def card(self, x, y, w, h, title, items=(), accent=False):
        self.rect(x,y,w,h,WHITE,LINE,17)
        if accent: self.rect(x,y,7,h,TEAL,TEAL,3)
        self.text(x+26,y+45,title,24,True)
        self.lines(x+26,y+86,items,18,30)

    def footer(self, n):
        self.line(54,self.h-60,self.w-54,self.h-60)
        self.text(54,self.h-25,'AutoClaw · Design 工作区 / 功能与交互 V10',16,False,MUTED)
        self.text(self.w-55,self.h-25,f'{n} / 08',16,False,MUTED,'end')

    def save(self, name, n):
        self.footer(n)
        self.s.append('</svg>')
        (ROOT/name).write_text('\n'.join(self.s),encoding='utf-8')


def architecture():
    a=SVG('01  功能架构｜从初稿到可交付版本','以设计师的判断顺序组织功能；文件、版本和评审在整条链路中保持同源。')
    names=[('成果总览',['方向与覆盖','未完成状态 / 待处理项']),('预览与编辑',['可运行 HTML','定域目标 / 修订卡']),('修订审阅',['候选差异','影响检查 / 采纳']),('版本与评审',['G1 概念 / G2 Demo','意见与决定']),('交付',['G3 固定快照','复现入口 / 源码包'])]
    xs=[55,366,677,988,1299]
    for i,(t,ls) in enumerate(names):
        a.card(xs[i],205,246,232,t,ls, i==2)
        if i<4:a.arrow(xs[i]+250,321,xs[i+1]-8,321)
    a.rect(55,495,1490,104,LIGHT,LIGHT,16)
    a.text(83,538,'贯穿能力',23,True,TEAL)
    a.text(244,538,'定位上下文  ·  文件引用  ·  候选与版本  ·  评论/决策  ·  权限与来源',22)
    a.text(83,574,'方向 × 页面 × 状态 × 设备 × 版本',18,False,MUTED)
    a.card(55,645,460,125,'唯一可编辑主稿',['HTML / CSS / JS + 引用资源'])
    a.card(568,645,460,125,'外部参考',['PRD / Figma / 截图 / 规范'])
    a.card(1081,645,464,125,'派生交付',['ZIP / 截图 / PDF，引用固定版本'])
    a.save('01_功能架构.svg','01')


def files():
    a=SVG('02  文件关系｜先认主稿，再谈多格式管理','格式可以共存，但编辑权威、来源与版本关系必须明确。')
    a.card(55,192,355,162,'参考资料  Reference',['PRD / Figma 链接 / 截图','只读引用；记录来源'])
    a.card(55,430,355,162,'设计资产  Asset',['图片 / 字体 / 图标','显示是否被源项目引用'])
    a.rect(492,220,630,342,WHITE,TEAL,22,2)
    a.pill(521,246,'可运行主产物  ·  唯一编辑基线')
    a.text(522,333,'HTML / CSS / JS + 依赖资源',30,True)
    a.text(522,388,'方向 B  →  工作版 v3  →  页面 × 状态 × 设备',22)
    a.rect(523,423,560,97,PAPER,LINE,12)
    a.text(542,458,'候选 v3-c1',21,True)
    a.text(542,489,'隔离生成 / 对比 / 采纳为 v4 或放弃',18,False,MUTED)
    a.card(1206,190,340,161,'预览与截图',['由版本生成','可回到同一运行状态'])
    a.card(1206,410,340,161,'交付快照  G3',['固定 version_id','源码 / 状态表 / 决策'])
    a.arrow(412,275,486,275)
    a.arrow(412,512,486,512)
    a.arrow(1128,320,1198,270)
    a.arrow(1128,472,1198,480)
    a.rect(55,660,1490,108,LIGHT,LIGHT,14)
    a.text(82,704,'同源约束',23,True,TEAL)
    a.text(245,704,'reviewed_preview.version_id  =  snapshot.version_id  =  export.derived_from_version',21)
    a.text(82,741,'外部网页 / Figma 不在 MVP 中无损回写 HTML；PNG 与 PDF 是派生物，不充当可编辑源。',18,False,MUTED)
    a.save('02_文件关系与版本.svg','02')


def flow():
    a=SVG('03  状态流｜一次局部修订到固定交付','示例：Mobile 邮箱错误态的提示位置需要微调，同时保持 Desktop 与成功态。')
    top=[('01 找到状态','方向 B / 页面 / 错误态 / Mobile'),('02 指定目标','点文字 / DOM / 画笔锚点'),('03 确认边界','命中对象 / 范围 / 保留项'),('04 隔离候选','v3-c1；不覆盖 v3')]
    xs=[55,438,821,1204]
    for i,(title,desc) in enumerate(top):
        a.card(xs[i],199,342,150,title,[desc],i==2)
        if i<3:a.arrow(xs[i]+344,272,xs[i+1]-8,272)
    lower=[('05 审阅影响','原版 / 候选；源码 / 相关状态'),('06 采纳工作版','通过 → v4；越界 → 继续限定 / 放弃'),('07 阶段评审','G1 概念 → G2 Demo'),('08 交付快照','G3 / 同一版本 / 可复现包')]
    for i,(title,desc) in enumerate(lower):
        x=1204-i*383
        a.card(x,485,342,150,title,[desc],i==0)
        if i<3:a.arrow(x-7,560,x-41,560)
    a.arrow(1375,351,1375,476)
    a.rect(55,700,1490,85,AMBER,AMBER,14)
    a.text(82,735,'分歧处理',22,True)
    a.text(260,735,'画笔无法命中 → 页面级建议；共享样式越界 → 扩大影响检查；评审后改稿 → 需复核。',20)
    a.text(82,767,'“采纳候选”只更新工作版，不等于 PM 确认或可交付。',18,False,MUTED)
    a.save('03_核心交互状态流.svg','03')


def shell(a,active,title,breadcrumb='项目  /  邀请成员流程  /  Design 工作区'):
    a.rect(30,150,214,680,'#F0F2F1','#F0F2F1',16)
    a.text(55,190,'AutoClaw',23,True)
    a.text(55,245,'任务',18,True,MUTED)
    a.text(55,282,'邀请成员流程',18,False)
    a.line(48,306,224,306)
    nav=['成果总览','预览与编辑','修订审阅','版本与评审','交付']
    for i,n in enumerate(nav):
        y=338+i*56
        if n==active:a.rect(45,y-29,183,42,LIGHT,LIGHT,10)
        a.text(62,y,n,18,n==active,TEAL if n==active else MUTED)
    a.text(275,164,breadcrumb,16,False,MUTED)
    a.text(275,213,title,30,True)


def overview():
    a=SVG('04  成果总览｜从哪继续设计','线框：先呈现方向和覆盖，再进入具体的可运行状态。',1600,960)
    shell(a,'成果总览','设计成果总览')
    a.pill(1260,175,'工作版 v3',w=152)
    a.rect(275,244,995,126,WHITE,LINE)
    a.text(300,279,'方向',20,True)
    for i,(d,t) in enumerate([('A','信息优先'),('B','引导优先 · 当前'),('C','极简路线')]):
        x=301+i*315
        a.rect(x,298,291,49,LIGHT if d=='B' else PAPER,TEAL if d=='B' else LINE,9)
        a.text(x+17,330,f'{d}  {t}',18,d=='B')
    a.rect(275,391,995,348,WHITE,LINE)
    a.text(300,432,'页面 × 状态 × 设备覆盖',22,True)
    labels=['页面 / 状态','Desktop','Mobile','当前状态']
    for x,t in zip([300,690,886,1070],labels):a.text(x,484,t,17,True,MUTED)
    rows=[('邀请成员 · 默认','已预览','已预览','可编辑'),('邀请成员 · 邮箱错误','已预览','待修订','进入 →'),('邀请成员 · 成功','已预览','未生成','补齐状态')]
    for i,row in enumerate(rows):
        y=537+i*62
        a.line(300,y-27,1237,y-27)
        for x,t in zip([300,690,886,1070],row):a.text(x,y,t,18,t in ['待修订','进入 →'],TEAL if t in ['待修订','进入 →'] else INK)
    a.rect(1292,244,263,244,WHITE,LINE)
    a.text(1313,285,'待处理',21,True)
    a.lines(1313,328,['候选 1 项待审阅','PM 意见 2 条','Mobile 成功态未生成'],17,42)
    a.rect(1292,506,263,233,WHITE,LINE)
    a.text(1313,546,'文件与资料',21,True)
    a.lines(1313,589,['主稿：index.html','资源：8 个引用中','PRD / Figma / 截图','查看文件关系 →'],17,37)
    a.rect(275,763,1280,79,LIGHT,LIGHT,12)
    a.text(300,810,'下一步：打开 Mobile 邮箱错误态，在运行预览中调整提示组件。',20,True,TEAL)
    a.save('04_成果总览线框.svg','04')


def editor():
    a=SVG('05  预览与定域编辑｜先确认改谁和改到哪','线框：编辑工具贴着 HTML 预览；修订卡始终显示目标、范围与保留项。',1600,960)
    shell(a,'预览与编辑','预览与编辑')
    a.rect(275,242,1280,54,WHITE,LINE,10)
    a.text(296,277,'方向 B   /   邀请成员   /   邮箱错误态   /   Mobile 390   /   工作版 v3',17,True)
    a.rect(275,313,889,528,WHITE,LINE)
    a.rect(296,332,848,44,PAPER,LINE,8)
    a.text(312,361,'选择元素',17,True,TEAL)
    a.text(452,361,'改文字',17)
    a.text(566,361,'画笔圈选',17)
    a.text(712,361,'评论',17)
    a.text(994,361,'源文件 ▾',16,False,MUTED)
    a.rect(476,402,465,399,PAPER,LINE,20)
    a.text(512,446,'邀请成员',26,True)
    a.text(512,482,'输入邮箱，发送邀请链接',17,False,MUTED)
    a.rect(512,518,393,52,WHITE,LINE,9)
    a.text(528,551,'name@example.com',17,False,MUTED)
    a.rect(505,585,405,60,LIGHT,TEAL,8,2)
    a.text(519,622,'请输入有效的邮箱地址',17,True,TEAL)
    a.rect(512,678,393,51,TEAL,TEAL,9)
    a.text(709,711,'发送邀请',17,True,WHITE,'middle')
    a.rect(1184,313,371,528,WHITE,LINE)
    a.text(1208,354,'修订卡',22,True)
    a.text(1208,378,'属性微调   |   AI 指令（当前）',15,True,TEAL)
    a.text(1208,397,'目标',16,True,MUTED)
    a.rect(1207,411,322,67,LIGHT,LIGHT,8)
    a.lines(1221,438,['邮箱错误提示 · DOM 命中','仅 Mobile / 错误态'],16,25,INK)
    a.text(1208,516,'要修改',16,True,MUTED)
    a.rect(1207,530,322,72,PAPER,LINE,8)
    a.lines(1221,559,['移到输入框正下方，','缩小空隙。'],17,24,INK)
    a.text(1208,636,'保持不变',16,True,MUTED)
    a.rect(1207,650,322,62,PAPER,LINE,8)
    a.text(1221,687,'Desktop、成功态、品牌样式',16)
    a.rect(1207,738,322,56,TEAL,TEAL,8)
    a.text(1368,773,'确认范围并生成候选',17,True,WHITE,'middle')
    a.save('05_预览与定域编辑线框.svg','05')


def compare():
    a=SVG('06  候选审阅｜看见越界，再做决定','线框：候选不是正式稿；视觉、源码和受影响视图必须同时可见。',1600,960)
    shell(a,'修订审阅','候选 v3-c1 · 待审阅')
    a.pill(1320,175,'尚未采纳',AMBER,INK,150)
    a.rect(275,244,1280,54,WHITE,LINE,10)
    a.text(297,279,'方向 B / 邀请成员 / 邮箱错误态 / Mobile 390    基线 v3  ↔  候选 v3-c1',17,True)
    for x,t in [(275,'原版 v3'),(753,'候选 v3-c1')]:
        a.rect(x,316,456,366,WHITE,LINE)
        a.text(x+22,351,t,21,True)
        a.rect(x+88,373,280,278,PAPER,LINE,11)
        a.text(x+110,417,'邀请成员',21,True)
        a.rect(x+110,445,235,37,WHITE,LINE,5)
        a.text(x+122,470,'name@example.com',14,False,MUTED)
        y=552 if x==275 else 493
        a.rect(x+105,y,245,40,LIGHT,TEAL,5)
        a.text(x+116,y+26,'请输入有效的邮箱地址',14,True,TEAL)
        a.rect(x+110,605,235,35,TEAL,TEAL,5)
    a.rect(1231,316,324,366,WHITE,LINE)
    a.text(1252,352,'影响检查',21,True)
    a.lines(1252,391,['✓ 错误态 Mobile 已运行','✓ 成功态未见变化','! Desktop 需人工复核','✓ 资源引用正常'],17,44)
    a.rect(275,701,868,133,WHITE,LINE)
    a.text(297,740,'源文件变动',19,True)
    a.text(297,779,'invite.css  ·  错误提示布局 +12 / -3 行',17)
    a.text(297,811,'变更仅来自候选；点击可查看具体差异。',16,False,MUTED)
    a.rect(1163,701,392,133,WHITE,LINE)
    a.text(1185,740,'决定',19,True)
    a.pill(1185,768,'继续限定',PAPER,INK,108)
    a.pill(1302,768,'放弃',PAPER,INK,76)
    a.pill(1388,768,'采纳为 v4',TEAL,WHITE,139)
    a.save('06_候选审阅线框.svg','06')


def handoff():
    a=SVG('07  交付快照｜让评审所见可被开发复现','线框：交付不是一个下载按钮；版本、状态和未决问题同屏说明。',1600,960)
    shell(a,'交付','交付快照 · G3')
    a.rect(275,244,1280,112,LIGHT,LIGHT)
    a.text(300,284,'方向 B / 固定版本 v4 / G2 Demo 已确认',22,True,TEAL)
    a.text(300,322,'评审预览 v4  =  快照 v4  =  导出来源 v4',19,True)
    a.pill(1325,271,'复制预览链接',WHITE,TEAL,182)
    a.rect(275,377,605,316,WHITE,LINE)
    a.text(300,420,'交付内容',22,True)
    a.lines(300,467,['✓ 可运行 HTML / CSS / JS','✓ 被引用的图片、图标、字体','✓ 页面 × 状态 × 断点清单','✓ 运行与复现说明','✓ G1/G2 决定及已知问题'],19,43)
    a.rect(900,377,655,316,WHITE,LINE)
    a.text(926,420,'接手检查',22,True)
    a.lines(926,467,['前端：复现 Mobile 错误态','前端：检查 Desktop 与成功态','前端：核对数据、接口、路由、权限','未解决：键盘焦点顺序待工程核查'],19,43)
    a.rect(275,716,1280,103,WHITE,LINE)
    a.text(299,756,'版本来源：工作版 v4 ← 已采纳候选 v3-c1 ← 基线 v3',18)
    a.text(299,790,'任何后续修改都创建新工作版；已确认 G2 不会静默覆盖。',17,False,MUTED)
    a.rect(1250,732,277,55,TEAL,TEAL,8)
    a.text(1388,767,'下载交付包 ZIP',17,True,WHITE,'middle')
    a.save('07_交付快照线框.svg','07')


def file_drawer():
    a=SVG('08  文件与引用抽屉｜格式多，但每件东西有明确身份','线框：从预览打开文件面板；按用途找文件，选择后看来源、版本、引用与允许的动作。',1600,960)
    shell(a,'预览与编辑','预览与编辑')
    a.rect(275,242,1280,54,WHITE,LINE,10)
    a.text(296,277,'方向 B / 邀请成员 / 邮箱错误态 / Mobile 390 / 工作版 v4',17,True)
    a.rect(275,314,560,523,WHITE,LINE)
    a.text(299,358,'当前可运行预览',21,True)
    a.rect(351,389,410,403,PAPER,LINE,15)
    a.text(386,446,'邀请成员',26,True)
    a.rect(387,491,338,48,WHITE,LINE,7)
    a.text(404,523,'name@example.com',17,False,MUTED)
    a.rect(387,556,338,42,LIGHT,TEAL,6)
    a.text(403,583,'请输入有效的邮箱地址',16,True,TEAL)
    a.rect(387,658,338,45,TEAL,TEAL,7)
    a.text(556,688,'发送邀请',16,True,WHITE,'middle')
    a.rect(853,314,702,523,WHITE,LINE)
    a.text(877,358,'文件与引用',22,True)
    a.text(1426,358,'关闭 ×',16,False,MUTED)
    a.rect(877,385,289,420,PAPER,LINE,10)
    groups=[('主稿与运行资源',['● index.html  ·  入口','  invite.css  ·  已引用','  flow.js  ·  已引用']),('参考资料',['  邀请流程 PRD  ·  外链','  Figma 旧稿  ·  外链']),('候选与版本',['  工作版 v4','  候选 v3-c1  ·  已采纳']),('派生导出',['  Mobile 错误态.png'])]
    y=416
    for title,items in groups:
        a.text(895,y,title,17,True)
        y+=29
        for item in items:
            a.text(895,y,item,15,False,TEAL if item.startswith('●') else MUTED)
            y+=27
        y+=15
    a.text(1191,418,'选中 · index.html',21,True)
    a.line(1191,435,1528,435)
    a.lines(1191,473,['身份：可运行主稿入口','来源：AutoClaw 本任务生成','所属：方向 B / 工作版 v4','引用：invite.css、flow.js、8 个资源','关联：3 个状态 × 2 个设备'],17,39)
    a.rect(1191,670,335,105,LIGHT,LIGHT,10)
    a.text(1208,703,'可执行操作',17,True,TEAL)
    a.text(1208,737,'打开预览  ·  查看变更  ·  下载源文件',15)
    a.text(877,824,'选择 PNG 时改为“回到生成它的预览”；选择 Figma 时显示“打开来源”。',15,False,MUTED)
    a.save('08_文件与引用抽屉线框.svg','08')


for fn in [architecture, files, flow, overview, editor, compare, handoff, file_drawer]:
    fn()
