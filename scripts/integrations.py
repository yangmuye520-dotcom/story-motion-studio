"""Seven required upstreams, contribution artifacts, and reviewed release. No optional fallback."""
import argparse,json,os,shutil,sys,webbrowser,subprocess
from pathlib import Path
from studio import configure_runtime,read,write,digest,signed,local,compile_film,check_assets,check_style

SPECS={
 'wtt-code-animation-studio':{'role':'内容时序与素材','files':['SKILL.md','references/story-and-timing.md','references/material-review.md'],'artifact':'timeline.json'},
 'lemo-opuscar':{'role':'故事导演','files':['SKILL.md'],'library':['DIRECTOR.md'],'artifact':'story-arc.json'},
 'huashu-art-motion':{'role':'解释动画与对象接续','files':['SKILL.md','references/动画语法/t1_3b1b.md','scripts/storyboard_lint.py'],'artifact':'object-map.json'},
 'video-shotcraft':{'role':'镜头与终检','files':['SKILL.md','references/shots/camera/depth-layer-moves.md','references/final-review.md'],'artifact':'shot-plan.json'},
 'dashi-animationstyle':{'role':'视觉层级与可读性','files':['SKILL.md','knowledge/讲解动画通用规则.md'],'artifact':'visual-contract.json'},
 'mg-styles-15':{'role':'实际动效实现','files':['demos/08-morph/index.html','LICENSE'],'artifact':'scenes.js'},
 'xilo-opus-video':{'role':'确定性渲染与检查','files':['SKILL.md','references/craft-rules.md','scripts/render.py'],'artifact':'qa/preview-report.json'}
}
def locations(root=None):
 cfg=configure_runtime();base=Path(root or os.environ.get('STORY_MOTION_UPSTREAM') or cfg.get('upstreamRoot') or str(Path.home()/'.codex/skills/video'))
 opts=[cfg.get('lemoLibrary'),os.environ.get('LEMO_OPUSCAR_LIBRARY'),str(base/'lemo-opuscar/library'),str(Path.home()/'lemo-opuscar')]
 lib=next((Path(p) for p in opts if p and (Path(p)/'DIRECTOR.md').is_file()),None);return base,lib
def collect(root=None):
 base,lib=locations(root);records={};resolved={};missing=[]
 for name,s in SPECS.items():
  if not (base/name).is_dir():missing.append(name+' / package folder')
  for rel in s['files']:
   key=name+'/'+rel;p=base/name/rel
   if not p.is_file():missing.append(key)
   else:records[key]=digest(p);resolved[key]=p
  for rel in s.get('library',[]):
   key=name+'/library/'+rel;p=lib/rel if lib else None
   if not p or not p.is_file():missing.append(key+' / configure lemoLibrary')
   else:records[key]=digest(p);resolved[key]=p
 if missing:raise RuntimeError('Seven skills are REQUIRED. Missing: '+', '.join(missing))
 return records,resolved
def bind(project,root=None):
 hashes,_=collect(root);target=project/'integration/source-lock.json'
 if target.exists():assert read(target)['sourceSha256']==hashes,'Upstream version changed; preserve previous project and explicitly rebind a new revision'
 else:write(target,{'schema':'seven-skills/v2','sourceSha256':hashes,'allSevenRequired':True})
 if not (project/'integration/contributions.json').exists():write(project/'integration/contributions.json',{'schema':'seven-contributions/v2','records':{}})
 return hashes
def check_sources(project,root=None):
 hashes,_=collect(root);assert read(project/'integration/source-lock.json')['sourceSha256']==hashes,'Upstream missing/changed; existing contribution reports cannot be reused';return hashes
def record(project,name,source_key,quote,artifact,anchor,decision,kind):
 check_sources(project);_,paths=collect();assert name in SPECS and source_key.startswith(name+'/') and source_key in paths
 assert len(quote.strip())>=12 and quote in paths[source_key].read_text(encoding='utf-8'),'Quote must be actual upstream text (12+ characters)'
 assert artifact==SPECS[name]['artifact'],'Expected concrete role artifact: '+SPECS[name]['artifact']
 p=local(project,artifact);assert len(anchor.strip())>=8 and anchor in p.read_text(encoding='utf-8'),'Artifact anchor must exist (8+ characters)'
 assert len(decision.strip())>=16,'Explain a concrete content/implementation decision'
 usage=read(project/'integration/contributions.json');usage['records'][name]={'sourceKey':source_key,'sourceQuote':quote,'sourceSha256':digest(paths[source_key]),'kind':kind,'artifact':artifact,'artifactSha256':digest(p),'anchor':anchor,'decision':decision};write(project/'integration/contributions.json',usage)
def contrast(a,b):
 def lum(s):
  v=[int(s[i:i+2],16)/255 for i in [1,3,5]];v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v];return sum(x*y for x,y in zip(v,[.2126,.7152,.0722]))
 x,y=lum(a),lum(b);return (max(x,y)+.05)/(min(x,y)+.05)
def role_checks(project):
 t=read(project/'timeline.json');ids={s['id'] for s in t['scenes']};last=0
 for s in t['scenes']:assert s['startFrame']==last;last=s['endFrame']
 assert last==t['totalFrames'];check_assets(project)
 arc=read(project/'story-arc.json');assert all(len(arc[k].strip())>=8 for k in ['goal','turn','ending']) and set(arc['sceneIds'])==ids,'Story arc must cover actual scenes'
 objects=read(project/'object-map.json');code=(project/'scenes.js').read_text(encoding='utf-8');assert objects
 assert {x['sceneId'] for x in objects}==ids,'Object map must cover every scene'
 for x in objects:assert x['sceneId'] in ids and x['before']!=x['after'] and x['action'] and x['implementationAnchor'] in code
 lint=read(project/'qa/huashu-native.json');assert lint['returncode']==0 and lint['storyboardSha256']==digest(project/'镜头表.md')
 shots=read(project/'shot-plan.json');assert {s['sceneId'] for s in shots}==ids
 _,sources=collect();assert lint['sourceScriptSha256']==digest(sources['huashu-art-motion/scripts/storyboard_lint.py']),'Native lint script changed'
 for shot in shots:
  assert shot['sourceKey'].startswith('video-shotcraft/') and shot['sourceKey'] in sources
  assert shot['purpose'] and shot['motion'] and shot['implementationAnchor'] in code
 vc=read(project/'visual-contract.json');style=read(project/'style.json');assert vc['bodySize']==style['bodySize'] and vc['bodySize']>=48
 assert contrast(style['palette']['ink'],style['palette']['background'])>=4.5,'Main-text contrast too low'
 assert vc['readSpeedBudget']<=9 and vc['targetViewingWidth']>=360 and vc['scopeNote'],'Record intended viewing size and real review limitations'
 preview=read(project/'qa/preview-report.json');assert not preview['browserErrors'] and not preview['textBoundsViolations'] and all(preview['deterministic'])
 for f,h in preview['sourceSha256'].items():assert digest(project/f)==h,'Preview stale: '+f
 return {'wtt':'compiled timing + asset version checked','lemo':'goal/turn/ending covers actual scenes','huashu':'before/action/after linked to implementation','shotcraft':'shot purposes and source cards linked','dashi':'type contract + contrast checked','mg':'implementation bound by source quote and code SHA','xilo':'actual preview + deterministic checks bound'}
def native_lint(project):
 check_sources(project);_,paths=collect();script=paths['huashu-art-motion/scripts/storyboard_lint.py'];board=project/'镜头表.md'
 result=subprocess.run([sys.executable,'-X','utf8',str(script),str(board)],capture_output=True,text=True,encoding='utf-8')
 write(project/'qa/huashu-native.json',{'sourceScriptSha256':digest(script),'storyboardSha256':digest(board),'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr});print(result.stdout)
 assert result.returncode==0,'Native huashu storyboard lint failed; see qa/huashu-native.json'
def check(project,strict=True):
 check_sources(project);usage=read(project/'integration/contributions.json')['records'];missing=[s for s in SPECS if s not in usage]
 if missing:
  assert not strict,'Missing actual contributions: '+', '.join(missing)
  return {'complete':False,'missing':missing,'note':'Draft only; seven contributions not certified'}
 hashes,paths=collect()
 for name,r in usage.items():
  assert name in SPECS and r['sourceKey'] in paths and r['sourceKey'].startswith(name+'/')
  assert digest(paths[r['sourceKey']])==r['sourceSha256'] and r['sourceQuote'] in paths[r['sourceKey']].read_text(encoding='utf-8')
  p=local(project,r['artifact']);assert r['artifact']==SPECS[name]['artifact'] and digest(p)==r['artifactSha256'] and r['anchor'] in p.read_text(encoding='utf-8'),'Contribution stale: '+name
 result={'complete':True,'requiredSkillCount':7,'roleChecks':role_checks(project),'contributionSha256':digest(project/'integration/contributions.json'),'sourceLockSha256':digest(project/'integration/source-lock.json'),'limits':'Hashes and structural checks do not prove artistic quality or human approval.'};return result
def release(project):
 coverage=check(project,True);assets=check_assets(project);style=check_style(project);r=read(project/'qa/candidate-report.json');video=project/'candidate.mp4';assert digest(video)==r['outputSha256']
 assert r['draft'] is False and r['fullDecode'] and r['output']=='candidate.mp4','Only a successfully rendered candidate can be released'
 assert r['materialVersion']==assets['version'] and r['style']==style and r['sevenSkills']==coverage,'Candidate binding is stale'
 assert not r['browserErrors'] and not r['textBoundsViolations'] and all(r['deterministic'])
 for f,h in r['sourceSha256'].items():assert digest(project/f)==h,'Rendered source changed: '+f
 rv=read(project/'qa/release-review.json');assert rv['videoSha256']==digest(video),'Review is not for latest candidate'
 assert rv['independent'] is True and rv['reviewer'] and rv['verdict']=='pass' and not rv['blockingIssues']
 for k in ['story','withinShotEvents','textReadability','styleConsistency','audioSource']:
  assert len(rv['checks'].get(k,'').strip())>=12,'Review needs concrete observations: '+k
 dst=project/'final.mp4'
 if dst.exists() and digest(dst)!=digest(video):
  hist=project/'.releases'/digest(dst)[:12];hist.mkdir(parents=True,exist_ok=True);shutil.copy2(dst,hist/'final.mp4')
 shutil.copy2(video,dst);write(project/'qa/release-report.json',{'videoSha256':digest(dst),'sevenSkills':coverage,'reviewSha256':digest(project/'qa/release-review.json'),'technicalReportSha256':digest(project/'qa/candidate-report.json'),'limitations':rv.get('limitations',[]) });print('RELEASED',dst)
def main():
 configure_runtime();p=argparse.ArgumentParser(description=__doc__);q=p.add_subparsers(dest='cmd',required=True)
 a=q.add_parser('doctor');a.add_argument('--root')
 a=q.add_parser('bind');a.add_argument('project');a.add_argument('--root')
 a=q.add_parser('read');a.add_argument('--skill',choices=SPECS,required=True)
 a=q.add_parser('record');a.add_argument('project');a.add_argument('--skill',choices=SPECS,required=True)
 for field in ['source-key','quote','artifact','anchor','decision']:a.add_argument('--'+field,required=True)
 a.add_argument('--kind',choices=['guideline-applied','code-adapted','native-tool'],required=True)
 for name in ['check','release','native-lint']:a=q.add_parser(name);a.add_argument('project')
 a=q.add_parser('gallery');a.add_argument('--library')
 a=p.parse_args()
 if a.cmd=='doctor':h,paths=collect(a.root);print(json.dumps({'required':7,'available':7,'sourceFiles':len(h)},indent=2))
 elif a.cmd=='read':
  _,paths=collect()
  for key,path in paths.items():
   if key.startswith(a.skill+'/'):print('\n## '+key+'\n'+path.read_text(encoding='utf-8'))
 elif a.cmd=='gallery':
  lib=Path(a.library) if a.library else Path(__file__).parent.parent/'examples';assert (lib/'index.html').is_file();webbrowser.open((lib/'index.html').resolve().as_uri())
 elif a.cmd=='bind':print('BOUND',len(bind(Path(a.project).resolve(),a.root)))
 elif a.cmd=='record':record(Path(a.project).resolve(),a.skill,a.source_key,a.quote,a.artifact,a.anchor,a.decision,a.kind)
 elif a.cmd=='check':print(json.dumps(check(Path(a.project).resolve()),ensure_ascii=False,indent=2))
 elif a.cmd=='native-lint':native_lint(Path(a.project).resolve())
 elif a.cmd=='release':release(Path(a.project).resolve())
if __name__=='__main__':
 try:main()
 except Exception as e:print(f'ERROR: {type(e).__name__}: {e}',file=sys.stderr);sys.exit(1)
