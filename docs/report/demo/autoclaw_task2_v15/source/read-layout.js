() => {
 const num=v=>+(String(v).match(/^-?[0-9.]+/)?.[0]||0); const out=[],W=innerWidth,H=innerHeight;
 const intersect=(a,b)=>({x:Math.max(a.x,b.x),y:Math.max(a.y,b.y),right:Math.min(a.right,b.right),bottom:Math.min(a.bottom,b.bottom)});
 function walk(el,clip){if(el.id==='toast')return; const s=getComputedStyle(el),r=el.getBoundingClientRect();if(s.display==='none'||s.visibility==='hidden'||+s.opacity===0||r.bottom<=clip.y||r.top>=clip.bottom||r.right<=clip.x||r.left>=clip.right)return;
 let c=clip;if(/hidden|auto|scroll/.test(s.overflowX+s.overflowY))c=intersect(clip,{x:r.x,y:r.y,right:r.right,bottom:r.bottom});
 const b={x:r.x,y:r.y,w:r.width,h:r.height,clip:c};
 if(s.backgroundColor!=='rgba(0, 0, 0, 0)'||num(s.borderTopWidth)>0||num(s.borderBottomWidth)>0)out.push({...b,type:'rect',fill:s.backgroundColor,radius:num(s.borderRadius)||0,border:s.borderTopColor,bw:s.borderTopStyle==='none'?0:num(s.borderTopWidth)||0,bottom:s.borderBottomStyle==='none'?0:num(s.borderBottomWidth)||0,bottomColor:s.borderBottomColor,shadow:s.boxShadow});
 if(el.id==='board-grid')out.push({...b,type:'grid'});
 if(el.tagName.toLowerCase()==='svg'){out.push({...b,type:'image',src:'inline:'+el.outerHTML});return}
 if(el.tagName==='IMG'){out.push({...b,type:'image',src:el.getAttribute('src')?.startsWith('data:')?'assets/capture-'+el.getAttribute('alt')+'.svg':el.getAttribute('src')});return}
 if(el.tagName==='INPUT'&&el.type==='range'){out.push({...b,type:'slider',value:+el.value,max:+el.max||100});return}
 if(['INPUT','TEXTAREA','SELECT'].includes(el.tagName)){if(['checkbox','color'].includes(el.type)){out.push({...b,type:'control',checked:el.checked,color:el.value,kind:el.type});return}const t=el.tagName==='SELECT'?el.selectedOptions[0]?.text:(el.value||el.placeholder);out.push({...b,type:'text',x:r.x+num(s.paddingLeft)+1,y:r.y+num(s.paddingTop)+num(s.fontSize)*.85,text:t,font:s.fontFamily,size:num(s.fontSize),weight:s.fontWeight,color:el.value?s.color:'#a3a3a3'});return}
 const children=[...el.childNodes].sort((a,b)=>(a.nodeType===1?num(getComputedStyle(a).zIndex):0)-(b.nodeType===1?num(getComputedStyle(b).zIndex):0));for(const n of children){if(el.tagName==='DETAILS'&&!el.open&&n.nodeName!=='SUMMARY')continue;if(n.nodeType===1)walk(n,c);else if(n.nodeType===3&&n.textContent.trim()){const lines=[];for(let i=0;i<n.textContent.length;i++){const range=document.createRange();range.setStart(n,i);range.setEnd(n,i+1);const q=range.getBoundingClientRect();if(q.width===0||q.bottom<=c.y||q.top>=c.bottom||q.right<=c.x||q.left>=c.right)continue;let l=lines[lines.length-1];if(!l||Math.abs(l.top-q.y)>2){l={top:q.y,x:q.x,y:q.y+q.height*.8,text:''};lines.push(l)}l.text+=n.textContent[i]}for(const l of lines)out.push({type:'text',...l,font:s.fontFamily,size:num(s.fontSize),weight:s.fontWeight,color:s.color,clip:c})}}
 }
 walk(document.body,{x:0,y:0,right:W,bottom:H});return JSON.stringify({width:W,height:H,items:out});
}
