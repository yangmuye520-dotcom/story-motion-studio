/* Technical seed only. Replace scene content and layout for the actual brief. */
window.renderFrame=function(frame){
 const t=Math.max(0,Math.min((TL.totalFrames-1)/TL.fps,frame/TL.fps));const s=TL.scenes.find(s=>frame>=s.startFrame&&frame<s.endFrame)||TL.scenes[TL.scenes.length-1];const u=t-s.startFrame/TL.fps,p=STYLE.palette;
 ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.fillStyle=p.background;ctx.fillRect(0,0,cv.width,cv.height);window.audit=[];
 label('对象改变状态，故事才向前走',100,125,STYLE.titleSize);
 if(s.id==='move'){
  const z=MotionKit.progress(u,.4,2.2),x=lerp(320,1600,z);segment(320,490,1600,490,p.line,8);circle(x,490,43,p.accent);label(z>.99?'已到达':'前进中',960,675,52,p.accent,'center');label('起点',320,585,36,p.muted,'center');label('终点',1600,585,36,p.muted,'center');window.semanticState={scene:s.id,position:x,arrived:z>.99};
 }else{
  const z=smooth(u/.8),x=lerp(1600,960,z),done=smooth((u-1.2)/.7);circle(x,490,lerp(43,95,z),p.accent);ctx.globalAlpha=done;segment(920,492,950,520,p.background,10);segment(950,520,1015,450,p.background,10);ctx.globalAlpha=1;label(done>.99?'已完成':'正在确认',960,675,52,p.accent,'center');window.semanticState={scene:s.id,position:x,confirmed:done>.99};
 }
 box(100,820,1720,180,'#ffffff99',null);wrap(s.copy,135,900,1640);if(location.search.includes('draft'))label('技术样片 · 风格未确认',1810,1040,27,p.secondary,'right');
};
async function initFilm(){await import("./motion-kit.js");[STYLE,TL]=await Promise.all([fetch('style.json').then(r=>r.json()),fetch('timeline.json').then(r=>r.json())]);cv.width=TL.width;cv.height=TL.height;await document.fonts.load(`600 56px ${STYLE.fontFamily}`);await document.fonts.ready;renderFrame(0);window.__ready=true;return TL}
