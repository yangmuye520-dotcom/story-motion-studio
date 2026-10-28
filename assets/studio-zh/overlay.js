/* Local Chinese UI overlay, 2026-10-27. Does not change composition sources or iframe contents. */
(() => {
 'use strict';
 const dict=__DICTIONARY__;
 const phrases=[
 ['Failed to add composition to timeline','无法将动画组合加入时间线'],
 ['Composition source has no valid data-composition-duration','组合源文件缺少有效时长声明 data-composition-duration'],
 ['Failed to load compositions','动画组合加载失败'],['Failed to load project','项目加载失败'],
 ['Failed to save','保存失败'],['Failed to render','渲染失败'],['Failed to export','导出失败'],
 ['Failed to add','添加失败'],['Failed to update','更新失败'],['Failed to delete','删除失败'],
 ['Failed to upload','上传失败'],['Failed to fetch','无法连接本地服务'],
 ['has timing attributes but no class="clip".','带有时序属性，但缺少 class="clip"'],
 ['The runtime still hides it outside its time range, but Studio and the GSAP clip-ownership rules use .clip to recognise a clip, so leaving it off makes the element harder to edit and to lint.','运行时仍会在时间范围外隐藏该元素，但编辑器和GSAP通过 .clip 识别片段；缺少它会影响编辑和代码检查'],
 ['lint findings, warnings only','项检查结果，仅含警告'],['lint finding','项检查结果'],
 ['Switch to dark theme','切换深色主题'],['Switch to light theme','切换浅色主题'],
 ['Loading preview','正在加载预览'],['Preparing render','正在准备渲染'],
 ['Waiting for preview server… run','正在等待本地预览服务，请运行'],
 ['3D rotation. Arrow keys rotate X/Y, Shift+arrows roll Z, Alt for fine steps; drag to rotate, scroll to change depth','三维旋转：方向键调整X/Y轴，Shift＋方向键调整Z轴，Alt微调；拖动旋转，滚动调整深度'],
 ];
 const keywords={'composition':'动画组合','timeline':'时间线','project':'项目','asset':'素材','render':'渲染','file':'文件','keyframe':'关键帧','animation':'动画','selection':'选区','element':'元素','clip':'片段'};
 function translate(text){
  if(typeof text!=='string'||!/[A-Za-z]/.test(text))return text;
  const lead=text.match(/^\s*/)[0],tail=text.match(/\s*$/)[0],s=text.trim();
  if(dict[s])return lead+dict[s]+tail;
  if(s.includes('\n'))return text.split('\n').map(translate).join('\n');
  let t=s;
  for(const [a,b]of phrases)t=t.split(a).join(b);
  t=t.replace(/^Close (.+)$/,(_,x)=>'关闭'+translate(x));
  t=t.replace(/^Open composition (.+)$/,(_,x)=>'打开组合 '+x);
  t=t.replace(/^Render (.+)$/,(_,x)=>'渲染 '+x);
  t=t.replace(/^Add (.+) to timeline at playhead$/,(_,x)=>'将 '+x+' 添加到播放头位置');
  t=t.replace(/^(Hide|Show) track (\d+)$/,(_,a,n)=>(a==='Hide'?'隐藏':'显示')+'轨道 '+n);
  t=t.replace(/^Previous (.+) keyframe$/,(_,x)=>'上一个 '+x+' 关键帧');
  t=t.replace(/^Next (.+) keyframe$/,(_,x)=>'下一个 '+x+' 关键帧');
  t=t.replace(/^Convert (.+) to keyframes$/,(_,x)=>'将 '+x+' 转为关键帧');
  t=t.replace(/^Timeline tool: (.+)$/,(_,x)=>'时间线工具：'+translate(x));
  t=t.replace(/^Preview volume: (.+)$/,(_,x)=>'预览音量：'+x);
  t=t.replace(/^(\d+) effects?$/,(_,n)=>n+' 个效果');
  t=t.replace(/^(\d+) lint findings?$/,(_,n)=>n+' 项检查结果');
  t=t.replace(/^(.+) opened$/,(_,x)=>translate(x)+'已打开');
  t=t.replace(/^(.+) closed$/,(_,x)=>translate(x)+'已关闭');
  t=t.replace(/^(\d+) warnings?$/,(_,n)=>n+' 项警告');
  t=t.replace(/^(\d+) errors?$/,(_,n)=>n+' 项错误');
  t=t.replace(/^(.+), ([\d.]+) to ([\d.]+) seconds$/,(_,label,a,b)=>translate(label)+'，'+a+'至'+b+'秒');
  t=t.replace(/^Motion keyframe at ([\d.]+)s$/,(_,n)=>n+'秒处的动效关键帧');
  t=t.replace(/^Auto · (.+)$/,(_,n)=>'自动 · '+n);
  t=t.replace(/^(Renders|Assets|Layers|Variables) \((\d+)\)$/,(_,label,n)=>translate(label)+' ('+n+')');
  t=t.replace(/^(\d+) · (Thin|Extra Light|Light|Regular|Medium|Semi Bold|Bold|Extra Bold|Black)$/,(_,n,label)=>n+' · '+(label==='Medium'?'中等字重':translate(label)));
  t=t.replace(/^fill set · (.+)$/,(_,n)=>'已设置填充 · '+n);
  if(t===s&&/^Failed to /i.test(s)){
   t=s.replace(/^Failed to (load|save|add|update|delete|remove|render|export|import|fetch|parse|read|write|open|create|copy|apply)/i,(_,verb)=>({load:'加载',save:'保存',add:'添加',update:'更新',delete:'删除',remove:'移除',render:'渲染',export:'导出',import:'导入',fetch:'获取',parse:'解析',read:'读取',write:'写入',open:'打开',create:'创建',copy:'复制',apply:'应用'}[verb.toLowerCase()]+'失败：'));
   for(const[k,v]of Object.entries(keywords))t=t.replace(new RegExp('\\b'+k+'s?\\b','gi'),v);
  }
  return lead+t+tail;
 }
 const excluded='script,style,code,pre,textarea,iframe,[contenteditable="true"],.cm-editor,.monaco-editor,[data-hf-no-translate]';
 function skip(el){return !el||!!el.closest(excluded)}
 function localize(root){
  if(root.nodeType===3){if(!skip(root.parentElement)){const t=translate(root.nodeValue);if(t!==root.nodeValue)root.nodeValue=t}return}
  if(root.nodeType!==1||skip(root))return;
  const nodes=[root,...root.querySelectorAll('*')];
  for(const el of nodes){
   if(skip(el))continue;
   for(const key of ['title','aria-label','placeholder','data-tooltip','aria-description']){
    const value=el.getAttribute(key);if(value){const t=translate(value);if(t!==value)el.setAttribute(key,t)}
   }
   for(const n of el.childNodes)if(n.nodeType===3){const value=n.nodeValue,t=translate(value);if(t!==value){n.nodeValue=t;if(/failed|error|invalid|no valid/i.test(value)&&!el.getAttribute('data-zh-original')){el.setAttribute('data-zh-original',value);el.setAttribute('title','原始技术信息：'+value)}}}
  }
 }
 let pending=new Set(),scheduled=false;
 const observer=new MutationObserver(records=>{
  for(const r of records){if(r.type==='characterData')pending.add(r.target);else if(r.type==='attributes')pending.add(r.target);else for(const node of r.addedNodes)pending.add(node)}
  if(!scheduled&&pending.size){scheduled=true;requestAnimationFrame(flush)}
 });
 function watch(){observer.observe(document.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['title','aria-label','placeholder','data-tooltip','aria-description']})}
 function flush(){scheduled=false;observer.disconnect();for(const node of pending)if(node.isConnected)localize(node);pending.clear();watch()}
 function start(){document.documentElement.lang='zh-CN';document.title='HyperFrames 中文工作台';localize(document.body);watch();window.HFStudioChinese={version:'0.8.207-zh1',translate};}
 window.HFStudioChinese={version:'0.8.207-zh1',translate};
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
