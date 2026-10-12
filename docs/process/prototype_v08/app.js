const state = {
  screen: 'home',
  direction: 'B',
  device: 'mobile',
  status: 'error',
  tool: 'none',
  target: '邮箱错误提示',
  brushRect: null,
  acceptedText: '输入有误',
  version: 'v3',
  conceptConfirmed: false,
  demoApproved: false,
  qaChecked: false,
};

const main = document.getElementById('main');
const breadcrumbs = document.getElementById('breadcrumbs');
const toastEl = document.createElement('div');
toastEl.className = 'toast';
toastEl.hidden = true;
document.body.appendChild(toastEl);
let toastTimer;

function toast(message) {
  toastEl.textContent = message;
  toastEl.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toastEl.hidden = true; }, 2800);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]));
}

function tabs(active) {
  return `<nav class="workspace-tabs" aria-label="设计工作区导航">
    <button data-action="overview" class="${active==='overview'?'active':''}">成果总览</button>
    <button data-action="preview" class="${active==='preview'?'active':''}">可运行预览</button>
    <button data-action="demo" class="${active==='demo'?'active':''}">Demo 体验</button>
    <button data-action="review" class="${active==='review'?'active':''}">修订记录</button>
    <button data-action="handoff" class="${active==='handoff'?'active':''}">交付</button>
  </nav>`;
}

function home() {
  return `<div class="home">
    <h1>和 AutoClaw 一起工作</h1>
    <div class="mode-tabs"><button class="active">◉　日常办公</button><button>▣　代码开发</button><button>⚖　法律助手</button><button>◉　金融分析</button></div>
    <div class="composer-wrap"><div class="composer"><textarea aria-label="任务输入" placeholder="输入“/”使用技能"></textarea><div class="composer-foot"><button class="plus" aria-label="添加附件">+</button><button>♢ 默认权限 ﹀</button><button>⌘ Agent 集群</button><button class="auto">Auto ﹀</button><button class="send" data-action="overview" aria-label="进入设计任务">↑</button></div></div><div class="project-choice">▱　默认项目 ﹀</div></div>
    <div class="quick-links"><button data-action="quick"> <span class="star">✦</span> 即梦生图</button><button data-action="quick"><span class="pink">▣</span> PDF 生成</button><button data-action="quick"><span class="blue">▣</span> 行业周报</button></div>
    <div class="ai-note">内容由 AI 生成，请核实关键信息</div>
  </div>`;
}

function miniUi(style) {
  return `<div class="mini-ui ${style}"><div class="mini-side"></div><div class="mini-body"><div class="mini-line"></div><div class="mini-field"></div><div class="mini-field"></div><div class="mini-button"></div></div></div>`;
}

function overview() {
  const cards = [
    ['A','一步完成邀请，流程最短','探索中','alt'],
    ['B','分步填写，错误引导更清楚','优先深化',''],
    ['C','角色先行，适合复杂权限','待验证','violet'],
  ];
  return `<div class="workspace">${tabs('overview')}
    <div class="page-head"><div><h1>邀请成员流程 · 设计成果</h1><p>从需求到可运行界面，继续评审、编辑和交付。</p></div><span class="pill amber">待 PM 确认方向 · 2 条未解决意见</span></div>
    <div class="pills"><span class="pill teal">草图概念中</span><span class="pill">4 个关键状态</span><span class="pill">桌面 / 手机</span><span class="pill">当前工作版 ${state.version}</span></div>
    <div class="direction-grid">${cards.map(([id,description,tag,style])=>`<article class="direction-card ${id==='B'?'featured':''}">${miniUi(style)}<div class="direction-card-head"><h2>方向 ${id}</h2><span class="pill ${id==='B'?'teal':''}">${tag}</span></div><p>${description}</p><button class="btn ${id==='B'?'primary':''}" data-action="preview" data-direction="${id}">${id==='B'?'打开可运行预览':'查看方案'} →</button></article>`).join('')}</div>
    <div class="review-strip"><strong>从方向到 Demo</strong><p>保留 A / C 作为备选。方向 B 的“错误提示位置”尚待微调，确认概念后再验证运行体验。</p><div class="progress-chain">草图收集　→　定义 1–3 个方向　→　概念确认　→　Demo 体验　→　开发交付</div></div>
  </div>`;
}

function phoneMarkup(candidate = false, compact = false) {
  const errorText = candidate ? state.acceptedText === '输入有误' ? '请输入有效的邮箱地址' : state.acceptedText : state.acceptedText;
  const selected = state.tool !== 'none' && !candidate ? 'highlight-target' : '';
  const brush = state.tool === 'brush' && !candidate && !compact ? `<div class="brush-layer" id="brush-layer" aria-label="画笔圈选区域"></div>${state.brushRect ? `<div class="brush-selection" style="left:${state.brushRect.x}%;top:${state.brushRect.y}%;width:${state.brushRect.w}%;height:${state.brushRect.h}%"></div>` : ''}` : '';
  const isSuccess = state.status === 'success' && !compact;
  const isDefault = state.status === 'default' && !compact;
  return `<div class="phone ${compact?'compact':''}" aria-label="手机端邀请成员页面">
    <div class="statusbar"><span>9:41</span><span>●●●　▰</span></div><div class="close-x" data-action="overview">×</div>
    <h3>邀请成员</h3><p class="desc">发送邀请，让成员加入你的团队。</p>
    <label>邮箱地址</label><div class="field ${isDefault||isSuccess?'':'invalid'}">name@example.com</div>
    ${isSuccess?'<div class="mapping" style="margin-top:22px">✓ 邀请已发送，成员可通过邮件加入团队。</div>':isDefault?'':`<div class="error ${selected}" data-action="select-error" style="margin-top:${candidate?8:26}px">${escapeHtml(errorText)}</div>`}
    <div class="secondary">邀请链接将在 7 天后失效</div><div class="primary-cta" style="margin-top:${candidate?24:28}px">${isSuccess?'继续邀请':'发送邀请'}</div>
    <div class="foot">使用即代表同意服务条款与隐私政策</div>${brush}
  </div>`;
}

function desktopMarkup() {
  return `<div class="desktop-preview"><div class="desktop-side"><b>工作空间</b><p>概览</p><p>成员管理</p><p>设置</p></div><div class="desktop-body"><h3>邀请成员</h3><p>发送邀请，让成员加入你的团队。</p><div class="field">name@example.com</div>${state.status==='success'?'<div class="mapping" style="margin-top:14px">✓ 邀请已发送</div>':state.status==='default'?'':`<div class="error">${escapeHtml(state.acceptedText)}</div>`}<div class="primary-cta">${state.status==='success'?'继续邀请':'发送邀请'}</div></div></div>`;
}

function previewPanel() {
  const base = `<div class="context-row">方向 ${state.direction}　/　邀请成员　/　${state.status==='error'?'邮箱错误态':'默认态'}　/　${state.device==='mobile'?'Mobile':'Desktop'}　/　${state.version}</div>`;
  if (state.tool === 'text') return `<h2>文字微调</h2><p>只改当前错误态文案；AI 可以提供表达建议，修改会先进入工作草稿。</p>${base}<label for="text-edit">错误提示文案</label><input id="text-edit" type="text" value="${escapeHtml(state.acceptedText)}"><div class="check-row"><input id="only-state" type="checkbox" checked><span>仅此状态，不改其他实例</span></div><button class="btn" data-action="suggest-text">建议一个更清楚的说法</button><button class="btn primary" data-action="apply-text">应用到工作草稿</button><p class="hint">应用后仍可撤销；PM 阶段确认是另一项决定。</p>`;
  if (state.tool === 'smart' || state.tool === 'brush') return `<h2>界面定域修订</h2><p>先确认 AI 命中的目标，再描述修改与需要保留的部分。</p>${base}<h3>当前目标</h3><div class="mapping">${state.tool==='brush'?'原型模拟识别：错误提示、邮箱输入框、发送按钮':'已选中：邮箱错误提示组件'}<br><small>正式产品须显示真实命中对象；画笔不是代码选区。</small></div><label for="edit-intent">修改意图</label><textarea id="edit-intent">${state.tool==='brush'?'缩短说明并拉开提示与按钮间距，突出主操作':'将错误提示移到邮箱输入框下方，间距更紧凑'}</textarea><label>保留项 / 生效范围</label><div class="check-row"><input type="checkbox" checked><span>只作用于 Mobile 错误态</span></div><div class="check-row"><input type="checkbox" checked><span>保留 Desktop 与成功态</span></div><div class="check-row"><input type="checkbox" checked><span>保留品牌色和页面结构</span></div><div class="warning">可能触及共享样式。生成后仍需检查 Desktop 和其他状态。</div><button class="btn primary" data-action="generate">生成隔离候选</button><button class="btn ghost" data-action="reset-tool">取消本次修订</button>`;
  return `<h2>当前设计</h2><p>方向 ${state.direction} · ${state.version}。在预览中选中文字、元素或使用画笔指出问题。</p>${base}<h3>PM 意见</h3><div class="warning">“错误提示离输入框太远，文案也不够清楚。”<br><small>锚定：邮箱错误态 / Mobile</small></div><h3>建议下一步</h3><button class="btn" data-action="tool-text">改错误文案</button><button class="btn" data-action="tool-smart">精准修改组件</button><button class="btn" data-action="tool-brush">画笔圈选区域</button>`;
}

function preview() {
  return `<div class="workspace">${tabs('preview')}<div class="split-workspace">
    <section class="preview-pane"><div class="preview-top"><div><h2>方向 ${state.direction} · 邀请成员流程</h2><small>${state.version} · 可运行预览</small></div><div class="segmented"><button data-action="device-mobile" class="${state.device==='mobile'?'active':''}">手机</button><button data-action="device-desktop" class="${state.device==='desktop'?'active':''}">桌面</button></div></div>
      <div class="preview-tools"><button class="tool-btn ${state.tool==='none'?'active':''}" data-action="reset-tool">↖ 选择元素</button><button class="tool-btn ${state.tool==='text'?'active':''}" data-action="tool-text">T 改文字</button><button class="tool-btn ${state.tool==='smart'?'active':''}" data-action="tool-smart">✧ 智能编辑</button><button class="tool-btn ${state.tool==='brush'?'active':''}" data-action="tool-brush">◌ 画笔圈选</button><span class="subtle small" style="margin-left:auto">状态：邮箱错误态 ▾</span></div>
      <div class="preview-stage">${state.device==='mobile'?phoneMarkup():desktopMarkup()}</div></section><aside class="right-panel">${previewPanel()}</aside>
    </div></div>`;
}

function compare() {
  return `<div class="workspace">${tabs('preview')}<div class="page-head"><div><h1>修订候选 · 尚未采纳</h1><p>目标：方向 ${state.direction} / 邀请成员 / 邮箱错误态 / Mobile / 错误提示区域</p></div><span class="pill amber">候选 ${state.version}-c1</span></div>
    <div class="split-workspace"><div class="compare-area"><section class="compare-column"><div class="column-head"><strong>原版 ${state.version}</strong><span class="subtle small">当前工作版</span></div>${phoneMarkup(false,true)}</section><section class="compare-column"><div class="column-head"><strong>候选</strong><span class="pill teal">仅此状态</span></div>${phoneMarkup(true,true)}</section></div>
    <aside class="right-panel"><h2>修改影响</h2><p>这是交互原型的模拟候选。正式产品应运行 HTML 并核查受影响状态。</p><ul class="impact-list"><li>错误提示移动到邮箱输入框下方</li><li>沿用工作草稿中已确认的文案</li><li>Mobile 错误态局部间距更新</li><li>Desktop 与成功态：待回归检查</li></ul><div class="warning">共享样式可能影响其他页面；正式产品不得只靠截图宣称安全。</div><button class="btn primary" data-action="accept">采纳为下一工作版</button><button class="btn" data-action="refine">继续限定修改</button><button class="btn ghost danger" data-action="reject">放弃候选，保留 ${state.version}</button></aside></div></div>`;
}

function review() {
  return `<div class="workspace">${tabs('review')}<div class="page-head"><div><h1>方向 ${state.direction} · 阶段评审</h1><p>一次修改已被设计师采纳，是否确认概念由 PM 与设计师共同决定。</p></div><span class="pill ${state.conceptConfirmed?'teal':'amber'}">${state.conceptConfirmed?'概念已确认':'待 PM 确认概念'}</span></div>
    <div class="decision-grid"><section class="decision-card"><h2>本次修订</h2><p>基于 ${state.version}：将 Mobile 错误提示移近邮箱输入框，并明确提示文案。原工作版及放弃的候选仍可回看。</p><div class="pills"><span class="pill teal">设计师已采纳</span><span class="pill">Mobile 错误态</span></div><h3>设计师判断</h3><p>错误信息与出错字段关系更清楚；Desktop 和成功态仍需在真实 Demo 中回归。</p><button class="btn" data-action="preview">返回可运行预览</button></section>
    <section class="decision-card"><h2>PM 方向确认</h2><p>确认本方向的核心路径与原则，保留细节给 Demo 体验评审。这个动作不等于自动批准生产代码。</p><div class="warning">未解决：邀请链接失效后的提示方式；开发需评估真实接口和状态返回。</div><button class="btn primary" data-action="confirm-concept">${state.conceptConfirmed?'查看交付准备':'确认概念并进入 Demo'}</button><button class="btn ghost" data-action="overview">回看其他方向</button></section></div></div>`;
}

function demo() {
  if (!state.conceptConfirmed) return `<div class="workspace">${tabs('demo')}<div class="page-head"><div><h1>先确认草图概念</h1><p>方向尚未确认，运行体验评审会混淆“选方向”和“验体验”。</p></div></div><button class="btn primary" data-action="review">返回概念评审</button></div>`;
  return `<div class="workspace">${tabs('demo')}<div class="page-head"><div><h1>Demo 运行体验评审</h1><p>方向 ${state.direction} · ${state.version}。检查关键路径、错误与成功状态，再决定是否交付开发。</p></div><span class="pill amber">G2 · 待体验确认</span></div>
    <div class="split-workspace"><section class="preview-pane"><div class="preview-top"><div><h2>邀请成员流程</h2><small>可点击原型 · 真实产品须运行生成的 HTML</small></div><div class="segmented"><button data-action="device-mobile" class="${state.device==='mobile'?'active':''}">手机</button><button data-action="device-desktop" class="${state.device==='desktop'?'active':''}">桌面</button></div></div><div class="preview-tools"><div class="segmented"><button data-action="status-default" class="${state.status==='default'?'active':''}">默认态</button><button data-action="status-error" class="${state.status==='error'?'active':''}">错误态</button><button data-action="status-success" class="${state.status==='success'?'active':''}">成功态</button></div><span class="subtle small" style="margin-left:auto">版本 ${state.version}</span></div><div class="preview-stage demo-stage">${state.device==='mobile'?phoneMarkup():desktopMarkup()}</div></section>
    <aside class="right-panel"><h2>体验评审清单</h2><p>PM 判断是否满足需求，设计师检查表现，开发确认接手风险。</p><div class="check-row"><input type="checkbox" checked><span>主要邀请路径可理解</span></div><div class="check-row"><input type="checkbox" checked><span>Mobile 错误提示与输入框关系清楚</span></div><label class="check-row"><input id="demo-qa" type="checkbox" ${state.qaChecked?'checked':''}><span>Desktop / 默认 / 成功态已复核</span></label><div class="warning">原型中的状态切换用于讨论。正式交付必须用真实运行结果完成回归；当前仍有“邀请链接失效”问题未解决。</div><button class="btn primary" data-action="approve-demo" ${state.qaChecked?'':'disabled'}>确认 Demo 并准备交付</button><button class="btn ghost" data-action="review">返回概念决策</button></aside></div></div>`;
}

function handoff() {
  if (!state.demoApproved) return `<div class="workspace">${tabs('handoff')}<div class="page-head"><div><h1>交付尚未开放</h1><p>先完成概念确认和 Demo 体验评审，避免把未验证的工作版交给开发。</p></div></div><button class="btn primary" data-action="${state.conceptConfirmed?'demo':'review'}">${state.conceptConfirmed?'继续 Demo 评审':'返回概念评审'}</button></div>`;
  return `<div class="workspace">${tabs('handoff')}<div class="page-head"><div><h1>固定交付快照</h1><p>开发接收的文件与评审通过的预览指向同一版本。</p></div><span class="pill teal">方向 ${state.direction} · ${state.version} · 概念已确认</span></div>
    <div class="handoff-grid"><section class="decision-card"><h2>交付版本 ${state.version}</h2><p>网页与 UI 草图经局部修订、候选比较、设计师采纳、PM 概念确认和 Demo 体验评审。正式交付还需接入真实 HTML 产物。</p><ul class="file-list"><li><span>可运行 HTML / CSS / JS</span><span>待真实产物接入</span></li><li><span>页面与状态清单</span><span>4 个状态</span></li><li><span>设计资源与约束</span><span>2 个设备</span></li><li><span>评审决定与已知问题</span><span>含 2 条记录</span></li></ul><button class="btn primary" data-action="download-note">下载原型交付说明</button></section>
    <section class="decision-card"><h2>开发接手前需确认</h2><div class="warning">原型只模拟了界面与状态，不包含可合并的生产源码。真实项目需核查组件、接口、权限、可访问性与性能。</div><h3>版本来源</h3><p>方向 B / 工作版 ${state.version} / Mobile 错误态修订 / PM 概念确认。</p><button class="btn" data-action="review">查看评审记录</button><button class="btn ghost" data-action="overview">返回成果总览</button></section></div></div>`;
}

function render() {
  breadcrumbs.textContent = state.screen==='home' ? '' : '任务  /  邀请成员流程  /  Design 工作区';
  document.getElementById('design-task-link').classList.toggle('selected',state.screen!=='home');
  main.innerHTML = ({home,overview,preview,compare,review,demo,handoff}[state.screen] || home)();
  document.querySelector('.prototype-badge')?.remove();
  const badge=document.createElement('div');badge.className='prototype-badge';badge.textContent='可点击原型 · 候选内容为模拟';document.body.appendChild(badge);
}

document.addEventListener('click', event => {
  const control=event.target.closest('[data-action]'); if(!control) return;
  const action=control.dataset.action;
  if(action==='home'){state.screen='home';state.tool='none';}
  else if(action==='overview'){state.screen='overview';state.tool='none';}
  else if(action==='preview'){state.direction=control.dataset.direction||state.direction;state.screen='preview';state.tool='none';}
  else if(action==='review'){state.screen='review';state.tool='none';}
  else if(action==='demo'){state.screen='demo';state.tool='none';}
  else if(action==='handoff'){state.screen='handoff';state.tool='none';}
  else if(action==='tool-text'){state.screen='preview';state.tool='text';}
  else if(action==='tool-smart'||action==='select-error'){state.screen='preview';state.tool='smart';}
  else if(action==='tool-brush'){state.screen='preview';state.tool='brush';state.brushRect=null;}
  else if(action==='reset-tool'){state.tool='none';state.brushRect=null;}
  else if(action==='device-mobile'){state.device='mobile';}
  else if(action==='device-desktop'){state.device='desktop';}
  else if(action==='status-default'){state.status='default';}
  else if(action==='status-error'){state.status='error';}
  else if(action==='status-success'){state.status='success';}
  else if(action==='suggest-text'){const input=document.getElementById('text-edit'); if(input){input.value='请输入有效的邮箱地址';toast('已提供一条建议，可继续编辑后应用');} return;}
  else if(action==='apply-text'){const input=document.getElementById('text-edit');if(input&&!input.value.trim()){toast('请先输入文案');return;}state.acceptedText=input.value.trim();state.tool='none';toast('文案已进入工作草稿，可继续修订');}
  else if(action==='generate'){state.screen='compare';}
  else if(action==='accept'){state.version='v4';state.acceptedText='请输入有效的邮箱地址';state.screen='review';state.tool='none';toast('候选已采纳为 v4；仍待阶段评审');}
  else if(action==='refine'){state.screen='preview';state.tool='smart';toast('已返回修订卡，可继续限定修改范围');}
  else if(action==='reject'){state.screen='preview';state.tool='none';toast('候选已放弃，工作版保持不变');}
  else if(action==='confirm-concept'){state.conceptConfirmed=true;state.screen='demo';state.status='error';toast('概念已确认；现在评审 Demo 运行体验');}
  else if(action==='approve-demo'){if(!state.qaChecked){toast('请先复核其他设备与状态');return;}state.demoApproved=true;state.screen='handoff';toast('Demo 已确认；可固定交付快照');}
  else if(action==='download-note'){const content=`AutoClaw Design 工作区原型交付说明\n方向：${state.direction}\n版本：${state.version}\n状态：${state.conceptConfirmed?'PM 已确认概念':'待 PM 确认'}\n注意：此文件由可点击原型生成，不包含真实 HTML 项目源码。`;const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([content],{type:'text/plain;charset=utf-8'}));a.download='AutoClaw_原型交付说明.txt';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);return;}
  else if(action==='quick'){toast('此快捷入口仅用于还原 AutoClaw 首页');return;}
  render();
});

document.addEventListener('change',event=>{if(event.target.id==='demo-qa'){state.qaChecked=event.target.checked;render();}});

let brushStart=null;
document.addEventListener('pointerdown',event=>{const layer=event.target.closest('#brush-layer');if(!layer)return;const rect=layer.getBoundingClientRect();brushStart={x:(event.clientX-rect.left)/rect.width,y:(event.clientY-rect.top)/rect.height,rect};layer.setPointerCapture(event.pointerId);});
document.addEventListener('pointerup',event=>{const layer=event.target.closest('#brush-layer');if(!layer||!brushStart)return;const r=brushStart.rect;const end={x:(event.clientX-r.left)/r.width,y:(event.clientY-r.top)/r.height};const x=Math.max(0,Math.min(brushStart.x,end.x)),y=Math.max(0,Math.min(brushStart.y,end.y));const w=Math.max(.08,Math.abs(brushStart.x-end.x)),h=Math.max(.05,Math.abs(brushStart.y-end.y));state.brushRect={x:Math.round(x*100),y:Math.round(y*100),w:Math.round(Math.min(w,1-x)*100),h:Math.round(Math.min(h,1-y)*100)};brushStart=null;render();toast('已圈选区域；请核对右侧实际命中的界面元素');});

render();
