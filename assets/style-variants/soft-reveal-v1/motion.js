/* One existing paused GSAP timeline; position is composition-local seconds. */
window.SoftReveal={
 enter(tl,target,at=0,opts={}){const {duration=.8,distance=20,...rest}=opts;tl.fromTo(target,{opacity:0,y:distance},{opacity:1,y:0,duration,ease:'power3.out',...rest},at);return tl},
 exit(tl,target,at,opts={}){const {duration=.5,distance=-12,...rest}=opts;tl.to(target,{opacity:0,y:distance,duration,ease:'power2.inOut',...rest},at);return tl},
 chars(tl,targets,at=0,opts={}){const {duration=.7,stagger=.1,distance=18,...rest}=opts;tl.fromTo(targets,{opacity:0,y:distance},{opacity:1,y:0,duration,stagger,ease:'power3.out',...rest},at);return tl}
};
