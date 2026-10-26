/* Original deterministic motion helpers. Times are seconds; space is world units. */
(function(root){
  'use strict';
  const clamp=x=>Math.max(0,Math.min(1,x));
  const mix=(a,b,t)=>a+(b-a)*t;
  const ease=x=>{x=clamp(x);return x*x*x*(x*(x*6-15)+10)};
  function progress(t,start,duration){if(!(duration>0))throw Error('Positive duration required');return ease((t-start)/duration)}
  function seed(id,salt=0){let x=(Math.imul(id+1,1597334677)^Math.imul(salt+1,3812015801))>>>0;x^=x>>>16;x=Math.imul(x,2246822507)>>>0;return (x>>>0)/4294967296}
  function points(count,shape='ring',salt=1){
    if(!Number.isInteger(count)||count<1||count>4096)throw Error('Particle count must be 1..4096');
    return Array.from({length:count},(_,id)=>{
      let a=id*2.399963229728653,r=Math.sqrt((id+.5)/count);
      if(shape==='grid'){let n=Math.ceil(Math.sqrt(count));return {id,x:(id%n-(n-1)/2)/n*2,y:(Math.floor(id/n)-(n-1)/2)/n*2,z:0}}
      if(shape==='sphere'){let y=1-2*(id+.5)/count,q=Math.sqrt(1-y*y);return{id,x:Math.cos(a)*q,y,z:Math.sin(a)*q}}
      if(shape==='ring')return{id,x:Math.cos(a),y:Math.sin(a),z:0};
      if(shape==='disc')return{id,x:Math.cos(a)*r,y:Math.sin(a)*r,z:(seed(id,salt)-.5)*.08};
      throw Error('Unknown particle shape');
    });
  }
  function morph(from,to,p){
    if(from.length!==to.length)throw Error('Stable particle count required');
    p=clamp(p);return from.map((a,i)=>{let b=to[i];if(a.id!==b.id)throw Error('Stable particle IDs required');return{id:a.id,x:mix(a.x,b.x,p),y:mix(a.y,b.y,p),z:mix(a.z,b.z,p)}});
  }
  function project(p,c={}){
    const yaw=c.yaw||0,pitch=c.pitch||0;
    const x=p.x*Math.cos(yaw)-p.z*Math.sin(yaw),z=p.x*Math.sin(yaw)+p.z*Math.cos(yaw);
    const y=p.y*Math.cos(pitch)-z*Math.sin(pitch),depth=p.y*Math.sin(pitch)+z*Math.cos(pitch);
    const distance=c.distance??5,focal=c.focal??900,near=c.near??.25,d=distance-depth;
    if(d<=near)return null;
    return{id:p.id,x:(c.cx??960)+focal*x/d,y:(c.cy??540)+focal*y/d,depth,scale:focal/d};
  }
  function projected(items,camera){return items.map(p=>project(p,camera)).filter(Boolean).sort((a,b)=>a.depth-b.depth||a.id-b.id)}
  function fitText(ctx,text,maxWidth,maxSize=60,minSize=32,family='StudioSans',weight=500){
    let size=maxSize;for(;size>minSize;size-=1){ctx.font=`${weight} ${size}px ${family}`;if(ctx.measureText(text).width<=maxWidth)break}
    ctx.font=`${weight} ${size}px ${family}`;return {size,fits:ctx.measureText(text).width<=maxWidth};
  }
  function dot(ctx,p,r=4,color='#d9b973'){
    ctx.save();ctx.fillStyle=color;ctx.beginPath();ctx.arc(p.x,p.y,r,0,Math.PI*2);ctx.fill();ctx.restore();
  }
  root.MotionKit=Object.freeze({clamp,mix,ease,progress,seed,points,morph,project,projected,fitText,dot});
})(typeof window==='undefined'?globalThis:window);
