/* Project-local semantic actions, one caller-owned paused GSAP timeline */
(function(g){
 const ease='power2.inOut';
 function splitMerge(tl,o){
  const {units,bins,results,links}=o;
  units.forEach((id,i)=>{tl.set(id,{x:0,y:i*90},0);tl.to(id,{x:470,y:i*90,duration:.9,ease},.8+i*.3);tl.to(id,{x:960,y:Math.floor(i/2)*220+(i%2)*72,duration:1.1,ease},3.4+i*.2)});
  tl.fromTo(bins,{opacity:0},{opacity:1,duration:.4},.4);
  tl.fromTo(results,{opacity:0},{opacity:1,duration:.6},5.5);
  tl.fromTo(links,{opacity:0},{opacity:1,duration:.4},6.4);
 }
 function queue(tl,o){
  const {jobs,bars}=o;
  jobs.forEach((id,i)=>{const slot=i%3,entry=i<3?1+i*.25:5.7+slot*.25,finish=entry+2.9;
   tl.set(id,{x:0,y:i*72},0);tl.to(id,{x:580,y:slot*126,duration:.7,ease},entry);
   tl.fromTo(bars[i],{scaleX:0,transformOrigin:'left center'},{scaleX:1,duration:2,ease:'none'},entry+.7);
   tl.to(id,{x:1120,y:i*72,duration:.7,ease},finish);
  });
 }
 function patch(tl,o){
  tl.fromTo(o.evidence,{opacity:0,x:-35},{opacity:1,x:0,duration:.65,ease},.8);
  tl.fromTo(o.link,{opacity:0},{opacity:1,duration:.45},2.1);
  tl.fromTo(o.highlight,{opacity:0},{opacity:1,duration:.35},2.8);
  tl.to(o.old,{opacity:0,duration:.45},3.6);
  tl.fromTo(o.updated,{opacity:0},{opacity:1,duration:.6},4.05);
  tl.to(o.highlight,{opacity:.35,duration:.5},5.2);
  // Unchanged sections have no tweens: their content and positions stay fixed
 }
 function compare(tl,o){
  tl.fromTo(o.branches,{opacity:0},{opacity:1,duration:.5},.5);
  o.packets.forEach((id,i)=>{tl.set(id,{x:0},0);tl.to(id,{x:450,duration:1.4,ease},1);tl.to(id,{x:870,duration:i?2:1.1,ease},i?4.0:3.0);tl.to(id,{opacity:0,duration:.15},i?6.0:4.1)});
  tl.fromTo(o.results[0],{opacity:0},{opacity:1,duration:.5},4.2);
  tl.fromTo(o.results[1],{opacity:0},{opacity:1,duration:.5},6.1);
  tl.fromTo(o.mapping,{opacity:0},{opacity:1,duration:.5},7.2);
 }
 g.MechanismMotion=Object.freeze({splitMerge,queue,patch,compare});
})(window);
