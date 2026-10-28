/* Deterministic SVG demonstrations, not a second production timeline */
window.MotionLibrary=(()=>{
 const C={ink:'#e7eef8',muted:'#a3b4ca',blue:'#a9c1ff',teal:'#87e4db',gold:'#e3b16c',line:'#425870',panel:'#101c2c',result:'#0f222a'};
 const clamp=x=>Math.max(0,Math.min(1,x)),p=(t,a=1,d=3)=>{let x=clamp((t-a)/d);return x*x*(3-2*x)},mix=(a,b,x)=>a+(b-a)*x;
 const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
 const txt=(x,y,s,color='ink',size=22)=>`<text x="${x}" y="${y}" fill="${C[color]||color}" font-size="${size}">${esc(s)}</text>`;
 const box=(x,y,w,h,color='line',fill='panel')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="5" fill="${C[fill]||fill}" stroke="${C[color]||color}" stroke-width="1.7"/>`;
 const line=(x,y,X,Y,c='line',sw=2)=>`<path d="M${x},${y}L${X},${Y}" stroke="${C[c]||c}" stroke-width="${sw}" fill="none"/>`;
 const path=(d,c='line',sw=2,extra='')=>`<path d="${d}" fill="none" stroke="${C[c]||c}" stroke-width="${sw}" ${extra}/>`;
 const dot=(x,y,r=7,c='gold')=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${C[c]||c}"/>`;
 const group=(s,opacity=1)=>`<g opacity="${opacity}">${s}</g>`;
 const chip=(x,y,s,c='blue',w=180)=>box(x,y,w,48,c)+txt(x+13,y+31,s,c,20);
 const lerpPoint=(a,b,q)=>[mix(a[0],b[0],q),mix(a[1],b[1],q)];
 const items=[];
 function add(id,title,cat,use,observe,limit,fn,integrated=false){items.push({id,title,cat,use,observe,limit,fn,integrated,duration:10})}
 const grid=()=>[120,240,360,480,600,720,840].map(x=>line(x,50,x,390,'#152232',1)).join('')+line(60,390,900,390,'#243447',1);
 add('split','原文拆分','数据整理','解释一份输入怎样拆成多个处理单元','原文中的四段保持文字与颜色，依次移出','切块不等于摘要，片段数量仅作示意',(t)=>{
  let q=p(t,1,4),s=box(70,65,260,300)+txt(82,42,'来源原文','blue')+txt(600,42,'规则切块','teal');
  ['项目概况','测试方式','部署环境','维护约定'].forEach((a,i)=>{let u=p(t,1+i*.35,2);s+=chip(mix(92,600,u),mix(90+i*63,70+i*77,u),a,i%2?'teal':'blue',210)});
  return s+group(txt(75,425,'同一份原文 → 四个可追溯片段','gold'),q)
 },true);
 add('merge','证据归并','数据整理','解释相关片段如何整理成同主题结果','四条来源进入两组，条目身份没有丢失','不能把不相容的证据强行归并，也不意味着删除来源',(t)=>{
  let s=group(box(560,70,330,140,'teal','result')+box(560,260,330,140,'teal','result'),p(t,3,1));
  ['pytest','pytest -q','预发布','staging'].forEach((a,i)=>{let u=p(t,1+i*.3,3);s+=chip(mix(75,580,u),mix(65+i*83,85+Math.floor(i/2)*190+i%2*61,u),a,'blue',220)});
  return s+txt(72,43,'原始证据','blue')+txt(560,43,'同主题成组','teal')+group(txt(75,445,'保留来源，不把归并等同于删除','gold'),p(t,5,1))
 },true);
 add('group','按属性分类','数据整理','类别、聚类、标签与分桶','六个对象按已有属性进入三列','颜色表示示例属性，不代表模型自动分类必然准确',(t)=>{
  let s='';['A类','B类','C类'].forEach((x,i)=>s+=group(box(95+i*280,85,220,265)+txt(125+i*280,65,x,'muted'),p(t,1,1)));
  for(let i=0;i<6;i++){let c=i%3,u=p(t,1.2+i*.15,3),a=[130+(i*137)%620,120+(i*73)%230],b=[205+c*280,165+Math.floor(i/3)*110];let v=lerpPoint(a,b,u);s+=dot(...v,27,['blue','teal','gold'][c])+txt(v[0]-15,v[1]+7,`${'ABC'[c]}${Math.floor(i/3)+1}`,'#0a101a',18)}return s
 });
 add('filter','条件筛选','数据整理','解释什么被保留、什么被排除','同一批条目经过条件后进入不同区域','未匹配不等于错误或无价值，只是不符合本次条件',(t)=>{
  let s=box(390,120,150,180)+txt(410,165,'条件','blue')+txt(410,210,'保留 A', 'blue')+txt(680,60,'匹配','teal')+txt(680,305,'本次排除','gold');
  for(let i=0;i<4;i++){let yes=i%2===0,u=p(t,1+i*.3,2),v=p(t,3.4+i*.2,2),x=mix(mix(70,405,u),690,v),y=mix(80+i*82,yes?90+Math.floor(i/2)*70:325+Math.floor(i/2)*60,v);s+=chip(x,y,yes?'A 条目':'B 条目',yes?'teal':'gold',160)}return s
 });
 add('queue','队列与补位','流程控制','等待、占用处理槽和完成释放','前一批移出后，后一批才进入三个槽位','三个槽位仅为示意，实际容量以材料为准',(t)=>{
  let s=txt(65,42,'等待','blue')+txt(400,42,'处理槽 × 3','blue')+txt(740,42,'完成','teal');for(let i=0;i<3;i++)s+=box(390,65+i*110,210,90);
  for(let i=0;i<6;i++){let k=i%3,a=i<3?1:5.2,u=p(t,a+k*.18,.8),v=p(t,a+2.2+k*.18,.8),x=mix(mix(65,410,u),735,v),y=mix(mix(65+i*53,85+k*110,u),65+i*53,v);s+=chip(x,y,`任务 ${i+1}`,v>.5?'teal':'blue',155);let r=clamp((t-a-.8)/1.35);s+=`<rect x="${x+8}" y="${y+41}" width="${139*r}" height="3" fill="${C.teal}"/>`}return s
 },true);
 add('parallel','拆解并行与汇合','流程控制','把一个问题拆为几项独立子任务，再合并结果','三条路径可同时推进，汇合等待各自完成','不是所有任务都能并行，动画速度不是性能数据',(t)=>{
  let s=chip(55,190,'原始任务','blue',160)+chip(750,190,'合并结果','teal',155);[100,210,320].forEach((y,i)=>{s+=path(`M215 214H290V${y}H360M590 ${y}H680V214H750`)+box(360,y-35,230,70)+txt(385,y+7,['查资料','做校验','提取字段'][i],'blue');let a=p(t,1,.9),b=p(t,2,1.3+i*.5),c=p(t,5,1.2),x=mix(mix(215,470,a),750,c);s+=dot(x,mix(214,y,a)*(1-c)+214*c,7,c>.5?'teal':'gold');s+=line(375,y+23,375+190*b,y+23,'teal',3)});return s+group(txt(290,415,'先完成子任务，再汇合为一份结果','teal'),p(t,6,1))
 });
 add('branch','条件分支','流程控制','解释不同条件为什么进入不同路径','每次只点亮满足条件的一路，另一路保持暗色','两条分支存在，不代表一次执行全部分支',(t)=>{
  const second=t>=5,z=second?t-5:t;let s=chip(55,190,second?'条目不存在':'条目已存在','blue',180)+box(365,165,180,100)+txt(390,222,'存在吗','blue')+path('M235 214H365M545 214H620V110H735M620 214V325H735');s+=chip(735,85,'更新旧条目',second?'line':'teal',175)+chip(735,300,'创建新条目',second?'teal':'line',175)+txt(630,95,'是','muted',18)+txt(630,350,'否','muted',18);let u=p(z,.8,2);s+=dot(mix(245,725,u),mix(214,second?325:110,p(z,1.8,1)),8);return s+txt(55,420,second?'第二种输入：只走新建分支':'第一种输入：只走更新分支','gold')
 });
 add('retry','失败后重试','流程控制','解释失败、回退、重试成功的过程','同一请求返回等待区，再次进入处理','重试次数与退避策略必须由实际机制决定',(t)=>{
  let q=p(t,.7,1.5),r=p(t,2.5,1.7),u=p(t,4.6,2),s=chip(65,170,'请求 A','blue',170)+box(420,150,190,100)+txt(450,210,'处理')+path('M235 193H420M515 250V335H150V218','line')+path('M610 193H755');let x,y;
  if(t<2.5){x=mix(240,510,q);y=195}else if(t<4.6){x=mix(510,150,r);y=195+140*Math.sin(Math.PI*r)}else{x=mix(150,780,u);y=195}
  s+=dot(x,y,9,t>6.7?'teal':'gold')+txt(405,110,t>6.7?'第二次成功':t>2.2?'第一次失败':'首次尝试',t>6.7?'teal':'gold')+group(chip(755,170,'成功结果','teal',160),p(t,6.7,.5));return s
 });
 add('patch','原位局部更新','修订与状态','新增证据只修订一个字段或段落','中间一行替换，上下两段不移动','更新与整篇重写不同，未触及内容应保留',(t)=>{
  let q=p(t,3,1),s=box(425,55,465,330)+txt(450,105,'已有文档','blue')+txt(450,165,'项目采用 Python')+txt(450,330,'部署到预发布环境')+group(box(445,202,420,62,'teal','result'),p(t,2,.5));s+=group(txt(460,244,'测试命令 pytest'),1-q)+group(txt(460,244,'测试命令 pytest -q','teal'),q)+group(chip(55,200,'新证据：增加 -q','gold',295)+line(350,224,425,232,'gold'),p(t,.6,1));return s
 },true);
 add('diff','逐行差异对照','修订与状态','对照修订前后，定位增删改','对应行用线连接，修改行单独标记','高亮只标发生变化的行，不暗示其余行也被重写',(t)=>{
  let s=box(70,65,340,290)+box(550,65,340,290)+txt(90,45,'修改前','muted')+txt(570,45,'修改后','teal');let a=['环境：预发布','命令：pytest','提交前检查'],b=['环境：预发布','命令：pytest -q','提交前检查'];a.forEach((v,i)=>{let y=125+i*85;s+=txt(90,y,v,'ink',21)+group(txt(570,y,b[i],i===1?'teal':'ink',21),p(t,1+i*.8,.6))+group(line(415,y-8,545,y-8,i===1?'gold':'line'),p(t,2+i*.4,.6))});return s+group(txt(75,420,'只有第二行发生修改','gold'),p(t,4,1))
 });
 add('version','版本沿革','修订与状态','解释内容演化与来源历史','新版本向前出现，旧版本仍保留','不能把历史保留误画成同时生效',(t)=>{
  let s='';['v1 初始记录','v2 增加证据','v3 修订结论'].forEach((a,i)=>{let q=p(t,i*1.8,.8);s+=group(box(70+i*285,105,245,225,i===2?'teal':'line')+txt(90+i*285,155,a,i===2?'teal':'blue',20)+txt(90+i*285,225,['pytest','pytest -q','采用新约定'][i],'ink',20),q);if(i<2)s+=group(line(315+i*285,215,355+i*285,215),p(t,1.3+i*1.8,.6))});return s+group(txt(70,410,'当前采用 v3，v1 与 v2 仍是历史来源','gold'),p(t,5,1))
 });
 add('undo','状态回退','修订与状态','解释撤销、回滚与恢复基线','状态从A到B，再沿记录恢复A','演示回退不等于自动恢复数据库或删除历史',(t)=>{
  let changed=t>2&&t<6,s=box(285,100,390,230,changed?'teal':'blue')+txt(320,155,'当前设置','muted')+txt(320,225,changed?'测试命令 pytest -q':'测试命令 pytest',changed?'teal':'blue',25)+path('M665 315C730 420 230 420 295 315','gold');s+=txt(340,405,t>6?'撤销完成，恢复基线':'保留可撤销的修改记录','gold',20)+txt(70,65,t<2?'01 修改前':t<6?'02 应用修改':'03 撤销修改','muted');return s
 });
 add('compare','同输入双路对照','对比与视角','比较两种流程或输出形态','两个明确的输入副本分别走两条路径','必须同条件比较，动画用时不代表真实耗时',(t)=>{
  let s=txt(60,45,'同一个问题 · 两份输入副本','gold');['记忆列表','综合回答'].forEach((a,i)=>{let y=125+i*180;s+=chip(60,y-25,'怎么运行测试','blue',210)+line(270,y,700,y)+box(370,y-42,200,85)+txt(395,y+8,i?'检索＋综合':'检索','blue',22)+group(chip(700,y-25,a,'teal',190),p(t,3.5+i*1.5,.7));let q=p(t,1,2.3+i*1.4);s+=dot(mix(285,690,q),y,7)});return s
 },true);
 add('align','字段对应与对齐','对比与视角','解释两个表、两种格式怎样映射','字段顺序不同但名称对应，随后整理对齐','位置靠近不代表语义相同，需要明确映射',(t)=>{
  let a=['来源','内容','时间','类型'],order=[2,0,3,1],q=p(t,3,2),s=txt(80,50,'来源字段','blue')+txt(655,50,'目标字段','teal');a.forEach((v,i)=>{let j=order.indexOf(i),y=100+i*80,Y=mix(100+j*80,100+i*80,q);s+=chip(80,y,v,'blue',200)+chip(655,Y,v,'teal',200)+group(line(280,y+24,655,Y+24,'gold'),p(t,.7+i*.25,.8))});return s
 });
 add('wipe','同位置前后揭示','对比与视角','设计对比、过滤前后、前后状态','分界线揭示同一位置上的另一个状态','只适合能在同一坐标比较的内容，不代替解释因果',(t,uid)=>{
  let q=p(t,1,5),x=90+780*q,s=box(90,75,780,300)+txt(120,125,'处理前','muted')+txt(120,205,'来源未标记')+txt(120,285,'字段未校验');s+=`<defs><clipPath id="${uid}wipe"><rect x="90" y="75" width="${780*q}" height="300"/></clipPath></defs><g clip-path="url(#${uid}wipe)">`+box(90,75,780,300,'teal','result')+txt(120,125,'处理后','teal')+txt(120,205,'已关联来源 document A')+txt(120,285,'字段格式已校验')+'</g>'+line(x,65,x,385,'gold',3);return s
 });
 add('zoom','整体到局部放大','对比与视角','从系统概览切入某个模块的内部','左侧全貌保留，焦点连接到右侧细节','是图解放大，不是复杂三维摄影或真实显微影像',(t)=>{
  let s=box(60,105,280,240)+txt(80,145,'整体系统','blue');for(let i=0;i<4;i++)s+=box(85+i%2*120,170+Math.floor(i/2)*75,105,55,i===3?'gold':'line');let q=p(t,1.2,2.5);s+=group(path('M310 275L485 115M310 315L485 365','gold')+box(485,90,405,300,'gold')+txt(510,135,'选中模块的内部','gold')+chip(515,185,'输入 → 校验','blue',340)+chip(515,265,'处理 → 输出','teal',340),q);return s
 });
 add('bars','数值形成柱图','数据表达','比较几组明确数值','柱高和数值对应，逐步建立同一尺度','示意数据 3、7、5、9，不是外部统计结论',(t)=>{
  let vals=[3,7,5,9],s=line(110,350,880,350)+line(110,80,110,350);vals.forEach((n,i)=>{let h=n*25*p(t,.7+i*.3,2.2),x=190+i*170;s+=`<rect x="${x}" y="${350-h}" width="80" height="${h}" fill="${i===3?C.teal:C.blue}"/>`+txt(x+20,390,'ABCD'[i],'muted')+group(txt(x+25,335-h,n,i===3?'teal':'blue'),p(t,2.8,.5))});return s
 });
 add('sort','按数值重新排序','数据表达','解释排序、排名和重排前后的关系','同一柱形只换位置，高度与数值不变','排序不代表原始数据发生变化',(t)=>{
  let vals=[3,7,5,9],target=[3,1,2,0],s=line(80,350,900,350),q=p(t,1.2,3.5);vals.forEach((n,i)=>{let x=160+mix(i,target[i],q)*185,h=n*25;s+=`<rect x="${x}" y="${350-h}" width="85" height="${h}" fill="${i===3?C.teal:C.blue}"/>`+txt(x+20,390,'ABCD'[i],'muted')+txt(x+23,330-h,n,'blue')});return s+txt(80,55,q>.95?'按数值从高到低排序':'四组原始数据','muted')
 });
 add('line','曲线逐点构建','数据表达','解释随时间积累的测量或事件序列','曲线按已有数据点形成，不凭空漂移','线条插值不代表未采样时刻有真实观测',(t)=>{
  let points=[2,3,2,5,7,6].map((v,i)=>[120+i*145,350-v*35]),s=line(100,350,890,350)+line(100,60,100,350),q=clamp((t-1)/5)*5;
  points.forEach((a,i)=>{if(i<q){s+=dot(...a,5,'blue')+txt(a[0]-8,385,String(i+1),'muted',18)}if(i<5&&q>i){let b=lerpPoint(a,points[i+1],clamp(q-i));s+=line(...a,...b,'blue',4)}});let idx=Math.min(4,Math.floor(q)),cur=lerpPoint(points[idx],points[idx+1],clamp(q-idx));return s+dot(...cur,8,'gold')+txt(105,45,'示意序列：2、3、2、5、7、6','muted')
 });
 add('distribution','个体汇成分布','数据表达','把离散样本整理成频次分布','同一批36个点从原排列进入11个桶','示例来自两骰36种组合，桶的数量对应和数2到12',(t)=>{
  let counts=[1,2,3,4,5,6,5,4,3,2,1],s=txt(65,45,'36种等可能组合 → 和数频次','blue'),i=0;counts.forEach((n,b)=>{s+=txt(130+b*65,385,String(b+2),'muted',17);for(let j=0;j<n;j++,i++){let a=[160+i%6*27,95+Math.floor(i/6)*35],z=[140+b*65,345-j*26],q=p(t,1+i*.035,3.2),v=lerpPoint(a,z,q);s+=dot(...v,8,b===5?'teal':'blue')}});return s
 });
 add('trace','沿路径追踪来源','连续性与结构','解释一条数据经过哪些环节','同一信号留下可追踪的路径和记录','路线必须对应真实步骤，不能用光点掩盖内容',(t)=>{
  const pts=[[115,215],[345,215],[575,215],[805,215]],labels=['原文','片段','事实','引用'],q=clamp((t-1)/5)*3;let s='';pts.forEach((a,i)=>{if(i<3)s+=line(a[0],130,pts[i+1][0],130);s+=line(a[0],130,a[0],155);s+=box(a[0]-70,a[1]-60,140,120,i<=q?'teal':'line')+txt(a[0]-36,a[1]+8,labels[i],i<=q?'teal':'muted');if(i<q)s+=group(txt(65+i*220,390,'✓ '+labels[i],'gold',20),1)});let k=Math.min(2,Math.floor(q)),v=lerpPoint(pts[k],pts[k+1],clamp(q-k));return s+dot(v[0],v[1]-85,8,'gold')
 });
 add('expand','局部展开层级','连续性与结构','解释父模块与内部子结构','原模块仍在，内部字段在旁边展开','展开的是结构关系，不暗示额外后台动作已经执行',(t)=>{
  let s=box(60,135,210,180)+txt(85,185,'一条记忆','blue')+txt(85,240,'记录 A','muted');['内容','来源','时间'].forEach((a,i)=>{let q=p(t,1+i*.5,1.5),y=75+i*120;s+=group(path(`M270 225H405V${y+35}H550`)+chip(550,y,a,'teal',320),q)});return s+group(txt(65,410,'保留整体对象，再展开其中的字段','gold'),p(t,4,1))
 });
 add('morph','同一批点连续形变','连续性与结构','解释集合保持身份、布局发生变化','40个点从矩形边界移动成圆，数量不变','这是二维形变示意，不是物理过程或真实三维材质',(t)=>{
  let q=p(t,1,4),pts=[],s=txt(65,45,'40个点 · 身份与数量保持不变','blue');for(let i=0;i<40;i++){let a=i/40*Math.PI*2,r=150/Math.max(Math.abs(Math.cos(a)),Math.abs(Math.sin(a))),x=480+Math.cos(a)*mix(r,160,q),y=225+Math.sin(a)*mix(r,160,q);pts.push([x,y])}s+=path('M'+pts.map(v=>v.join(',')).join('L')+'Z','line');pts.forEach((v,i)=>s+=dot(...v,5,i===0?'gold':'teal'));return s
 });
 add('handoff','结果接成下一镜输入','连续性与结构','让观众顺着同一个对象理解下一步','记录A留在画面中，角色从上一阶段结果变为下一阶段输入','承接必须有内容关系，不为连贯强行连接无关镜头',(t)=>{
  let q=p(t,2.5,3),s=group(box(65,85,345,280)+txt(90,135,'上一步：整理完成','blue'),1-q)+group(box(530,85,365,280)+txt(555,135,'下一步：建立引用','teal'),q);s+=chip(mix(145,585,q),200,'同一条记录 A','gold',220)+group(txt(555,310,'使用刚才得到的结果','teal'),p(t,5.5,1));return s
 });
 function render(id,t,uid='main-'){let m=items.find(x=>x.id===id)||items[0];return `<rect width="960" height="480" fill="#0a101a"/>`+grid()+m.fn(Math.max(0,Math.min(m.duration,t)),uid)}
 return {items,render,categories:['数据整理','流程控制','修订与状态','对比与视角','数据表达','连续性与结构']};
})();
