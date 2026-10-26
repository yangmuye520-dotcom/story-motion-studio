/* Original shared drawing primitives. Keep accepted tokens and geometry here. */
const cv=document.querySelector('canvas'),ctx=cv.getContext('2d');let STYLE,TL;window.audit=[];
const cap=x=>Math.max(0,Math.min(1,x)),smooth=x=>{x=cap(x);return x*x*(3-2*x)},lerp=(a,b,u)=>a+(b-a)*u;
function box(x,y,w,h,fill,stroke){ctx.beginPath();ctx.roundRect(x,y,w,h,STYLE.radius);ctx.fillStyle=fill;ctx.fill();if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=STYLE.lineWidth;ctx.stroke()}}
function label(s,x,y,size=STYLE.bodySize,color=STYLE.palette.ink,align='left'){ctx.font=`600 ${size}px ${STYLE.fontFamily}`;ctx.fillStyle=color;ctx.textAlign=align;ctx.textBaseline='middle';ctx.fillText(s,x,y);let w=ctx.measureText(s).width;window.audit.push({text:s,x:align==='center'?x-w/2:align==='right'?x-w:x,y:y-size*.62,width:w,height:size*1.24})}
function circle(x,y,r,c){ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fillStyle=c;ctx.fill()}
function segment(x1,y1,x2,y2,c,w=STYLE.lineWidth){ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.strokeStyle=c;ctx.lineWidth=w;ctx.stroke()}
function wrap(s,x,y,width,size=STYLE.bodySize){ctx.font=`600 ${size}px ${STYLE.fontFamily}`;let row='',j=0;for(let ch of s){if(ctx.measureText(row+ch).width>width){label(row,x,y+j*size*1.3,size);row='';j++}row+=ch}if(row)label(row,x,y+j*size*1.3,size)}
