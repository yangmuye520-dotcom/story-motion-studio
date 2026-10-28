/* Existing HTML nodes + one caller-owned paused GSAP timeline, no playback loop */
(function(g){
'use strict';
const E='power2.inOut',list=x=>Array.isArray(x)?x:[x];
const contracts={
 split:['items'],merge:['items','result'],group:['items'],filter:['items'],queue:['items','progress'],parallel:['items','progress','result'],branch:['token','branches'],retry:['token','failure','success'],patch:['old','updated','highlight','unchanged'],diff:['changes','guides'],version:['versions','current'],undo:['before','after','history'],compare:['items','results'],align:['items','guides'],wipe:['clip','divider'],zoom:['detail','overview','guides'],bars:['bars'],sort:['items'],line:['path','marker'],distribution:['items'],trace:['token','nodes'],expand:['parent','details','guides'],morph:['items'],handoff:['carrier']};
function finite(v){return typeof v==='number'&&Number.isFinite(v)}
function positions(v,n,label){if(!Array.isArray(v)||v.length!==n||v.some(p=>!Array.isArray(p)||p.length!==2||!p.every(finite)))throw Error(label+': expected '+n+' [x,y] positions')}
function validate(c){
 if(!contracts[c.type])throw Error('Unknown action: '+c.type);
 if(!finite(c.start)||c.start<0||!finite(c.duration)||c.duration<=0)throw Error('Invalid action timing');
 if(!c.bindings||!c.params)throw Error('bindings and params required');
 for(const key of contracts[c.type])if(!list(c.bindings[key]).length||list(c.bindings[key]).some(x=>typeof x!=='string'||!/^#[A-Za-z][\w-]*$/.test(x)))throw Error('Invalid existing HTML selectors: '+key);
 const b=c.bindings,p=c.params,n=b.items?list(b.items).length:0;
 if(['split','merge','group','filter','queue','parallel','compare','align','sort','distribution','morph'].includes(c.type)){positions(p.from,n,'from');if(c.type!=='distribution')positions(p.to,n,'to')}
 if(['split','merge','group','filter','distribution','morph'].includes(c.type)&&n<2)throw Error('Action needs at least two distinct objects');
 if(new Set(Object.values(b).flat()).size!==Object.values(b).flat().length)throw Error('Do not bind one node to competing roles');
 if(c.type==='merge'){positions(p.via,n,'via')}
 if(['queue','parallel'].includes(c.type)&&list(b.progress).length!==n)throw Error('Each task needs its own progress mark');
 if(c.type==='queue'){if(!Number.isInteger(p.capacity)||p.capacity<1||p.capacity>n)throw Error('Invalid queue capacity');positions(p.slots,p.capacity,'slots')}
 if(c.type==='parallel'){if(p.independent!==true)throw Error('Parallel tasks must be independent');positions(p.stages,n,'stages');if(!Array.isArray(p.work)||p.work.length!==n||p.work.some(x=>!finite(x)||x<=0||x>.35))throw Error('work fractions must be 0 < x <= .35')}
 if(c.type==='branch'){positions(p.destinations,list(b.branches).length,'destinations');if(!Number.isInteger(p.selected)||p.selected<0||p.selected>=p.destinations.length)throw Error('Select exactly one valid branch');positions([p.from,p.junction],2,'branch route')}
 if(['retry','trace'].includes(c.type))positions(p.path,p.path?.length,'path');
 if(['retry','trace'].includes(c.type)&&p.path.length<3)throw Error('Route needs three or more points');
 if(c.type==='patch'&&list(b.unchanged).some(x=>[b.old,b.updated,b.highlight].includes(x)))throw Error('Unchanged nodes must not be modified');
 if(c.type==='compare'&&(n!==2||list(b.results).length!==2||!p.sameInput))throw Error('Compare requires two declared copies of one input');
 if(c.type==='compare')positions(p.stages,2,'stages');
 if(['bars','sort'].includes(c.type)){let count=c.type==='bars'?list(b.bars).length:n;if(!Array.isArray(p.values)||p.values.length!==count||p.values.some(x=>!finite(x)||x<0))throw Error('Invalid numeric values')}
 if(c.type==='bars'&&(!finite(p.baseline)||!finite(p.unit)||p.unit<=0))throw Error('Invalid chart scale');
 if(c.type==='sort'){if(p.values.some((v,i)=>i>0&&p.values[i-1]===undefined))throw Error('Invalid sort values')}
 if(c.type==='wipe'&&(!finite(p.width)||p.width<=0))throw Error('Invalid wipe width');
 if(c.type==='line'){positions(p.points,p.points?.length,'points');if(p.points.length<2)throw Error('Line needs two points');if(!finite(p.length)||p.length<=0)throw Error('Authored pathLength required')}
 if(c.type==='distribution'){positions(p.bucketCenters,p.bucketCenters?.length,'bucketCenters');if(!Array.isArray(p.bucketIds)||p.bucketIds.length!==n||p.bucketIds.some(x=>!Number.isInteger(x)||x<0||x>=p.bucketCenters.length)||!finite(p.gap)||p.gap<=0)throw Error('Distribution needs valid bucket membership and positive spacing')}
 if(c.type==='trace'&&list(b.nodes).length!==p.path.length)throw Error('Trace node count must match route');
 if(c.type==='handoff')positions([p.from,p.to],2,'handoff');
 return c;
}
function add(tl,c){
 validate(c);if(!tl||typeof tl.to!=='function'||typeof tl.fromTo!=='function')throw Error('Pass the existing GSAP timeline');
 const b=c.bindings,p=c.params,A=c.start,D=c.duration,at=x=>A+x*D;
 const show=(nodes,t=.1,d=.1)=>tl.fromTo(nodes,{opacity:0},{opacity:1,duration:d*D},at(t));
 const move=(node,a,z,t=.1,d=.5)=>tl.fromTo(node,{x:a[0],y:a[1]},{x:z[0],y:z[1],duration:d*D,ease:E,immediateRender:false},at(t));
 const many=(a,z,t=.1,d=.5)=>list(b.items).forEach((id,i)=>move(id,a[i],z[i],t+(i*.12/Math.max(1,list(b.items).length-1)),d));
 switch(c.type){
 case 'split':many(p.from,p.to,.08,.48);break;
 case 'merge':list(b.items).forEach((id,i)=>{move(id,p.from[i],p.via[i],.06+i*.02,.25);move(id,p.via[i],p.to[i],.38+i*.02,.25)});show(b.result,.66);break;
 case 'group':many(p.from,p.to,.12,.48);break;
 case 'filter':many(p.from,p.to,.1,.5);break;
 case 'queue':{tl.set(b.progress,{scaleX:0,transformOrigin:'left center'},A);const n=list(b.items).length,waves=Math.ceil(n/p.capacity),span=.78/waves;
  list(b.items).forEach((id,i)=>{let wave=Math.floor(i/p.capacity),slot=i%p.capacity,t=.05+wave*span;move(id,p.from[i],p.slots[slot],t,span*.18);tl.fromTo(b.progress[i],{scaleX:0,transformOrigin:'left center'},{scaleX:1,duration:span*.5*D,ease:'none',immediateRender:false},at(t+span*.18));move(id,p.slots[slot],p.to[i],t+span*.68,span*.18)});break}
 case 'parallel':{tl.set(b.progress,{scaleX:0,transformOrigin:'left center'},A);let finish=Math.max(...p.work)+.25;list(b.items).forEach((id,i)=>{move(id,p.from[i],p.stages[i],.05,.15);tl.fromTo(b.progress[i],{scaleX:0,transformOrigin:'left center'},{scaleX:1,duration:p.work[i]*D,ease:'none',immediateRender:false},at(.2));move(id,p.stages[i],p.to[i],finish,.15)});show(b.result,finish+.16);break}
 case 'branch':list(b.branches).forEach((id,i)=>tl.set(id,{opacity:i===p.selected?1:.25},A));move(b.token,p.from,p.junction,.08,.25);move(b.token,p.junction,p.destinations[p.selected],.35,.3);break;
 case 'retry':{let n=p.path.length-1;for(let i=0;i<n;i++)move(b.token,p.path[i],p.path[i+1],.05+i*.65/n,.65/n);show(b.failure,.24,.08);tl.to(b.failure,{opacity:.2,duration:.08*D},at(.45));show(b.success,.73);break}
 case 'patch':show(b.highlight,.15);tl.to(b.old,{opacity:0,duration:.1*D},at(.3));show(b.updated,.41,.12);break;
 case 'diff':list(b.changes).forEach((id,i)=>show(id,.12+i*.35/Math.max(1,list(b.changes).length-1),.1));show(b.guides,.58);break;
 case 'version':list(b.versions).forEach((id,i)=>show(id,.05+i*.45/Math.max(1,list(b.versions).length-1),.12));show(b.current,.63,.08);break;
 case 'undo':tl.set(b.before,{opacity:1},A);tl.set(b.after,{opacity:0},A);tl.to(b.before,{opacity:0,duration:.1*D},at(.2));show(b.after,.3);show(b.history,.4);tl.to(b.after,{opacity:0,duration:.1*D},at(.6));tl.to(b.before,{opacity:1,duration:.1*D},at(.7));break;
 case 'compare':list(b.items).forEach((id,i)=>{move(id,p.from[i],p.stages[i],.08,.2);move(id,p.stages[i],p.to[i],.33+i*.1,.2);show(b.results[i],.55+i*.1)});break;
 case 'align':many(p.from,p.to,.15,.5);show(b.guides,.1);break;
 case 'wipe':tl.fromTo(b.clip,{attr:{width:0}},{attr:{width:p.width},duration:.6*D,ease:E,immediateRender:false},at(.1));move(b.divider,[0,0],[p.width,0],.1,.6);break;
 case 'zoom':tl.fromTo(b.detail,{opacity:0,scale:.72,transformOrigin:'left center'},{opacity:1,scale:1,duration:.5*D,ease:E},at(.1));show(b.guides,.25);break;
 case 'bars':list(b.bars).forEach((id,i)=>tl.fromTo(id,{attr:{y:p.baseline,height:0}},{attr:{y:p.baseline-p.values[i]*p.unit,height:p.values[i]*p.unit},duration:.45*D,ease:E,immediateRender:false},at(.1+i*.04)));break;
 case 'sort':{const order=p.values.map((v,i)=>i).sort((a,b)=>p.values[b]-p.values[a]||a-b);list(b.items).forEach((id,i)=>move(id,p.from[i],p.to[order.indexOf(i)],.15,.5));break}
 case 'line':tl.set(b.path,{attr:{'stroke-dasharray':p.length,'stroke-dashoffset':p.length}},A);tl.fromTo(b.path,{attr:{'stroke-dasharray':p.length,'stroke-dashoffset':p.length}},{attr:{'stroke-dashoffset':0},duration:.6*D,ease:'none',immediateRender:false},at(.1));for(let i=0;i<p.points.length-1;i++)move(b.marker,p.points[i],p.points[i+1],.1+i*.6/(p.points.length-1),.6/(p.points.length-1));break;
 case 'distribution':{const counts={};const targets=p.bucketIds.map(k=>{const rank=counts[k]||0;counts[k]=rank+1;return [p.bucketCenters[k][0],p.bucketCenters[k][1]-rank*p.gap]});many(p.from,targets,.08,.55);break;}
 case 'trace':for(let i=0;i<p.path.length-1;i++){move(b.token,p.path[i],p.path[i+1],.1+i*.6/(p.path.length-1),.6/(p.path.length-1));tl.fromTo(b.nodes[i],{opacity:.4},{opacity:1,duration:.08*D},at(.1+i*.6/(p.path.length-1)))}tl.to(b.nodes.at(-1),{opacity:1,duration:.08*D},at(.72));break;
 case 'expand':list(b.details).forEach((id,i)=>show(id,.12+i*.45/Math.max(1,list(b.details).length-1),.15));show(b.guides,.1);break;
 case 'morph':list(b.items).forEach((id,i)=>tl.fromTo(id,{attr:{cx:p.from[i][0],cy:p.from[i][1]}},{attr:{cx:p.to[i][0],cy:p.to[i][1]},duration:.6*D,ease:E,immediateRender:false},at(.1)));break;
 case 'handoff':move(b.carrier,p.from,p.to,.1,.6);break;
 }
 const record={type:c.type,start:A,duration:D,bindings:JSON.parse(JSON.stringify(b))};(g.__motionActionCalls=g.__motionActionCalls||[]).push(record);return record;
}
g.MotionActions=Object.freeze({version:'1.0.0',ids:Object.freeze(Object.keys(contracts)),contracts:Object.freeze(contracts),validate,add});
})(window);
