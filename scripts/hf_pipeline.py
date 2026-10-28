"""One storyboard, seven traceable contributions and four separate HyperFrames review axes."""
import argparse,hashlib,json,re,shutil,subprocess,sys
from html.parser import HTMLParser
from pathlib import Path
import studio,integrations
from explanation_check import check as explanation_check

SKILL=Path(__file__).resolve().parent.parent
ROLES={'wtt-code-animation-studio':'timing','lemo-opuscar':'story','huashu-art-motion':'mechanism','video-shotcraft':'shots','dashi-animationstyle':'visual','mg-styles-15':'implementation','xilo-opus-video':'verification'}
def read(p):return studio.read(p)
def write(p,v):return studio.write(p,v)
def sha(p):return studio.digest(p)
def state(root):
 files=[]
 for p in root.rglob('*'):
  if not p.is_file():continue
  rel=p.relative_to(root);parts=rel.parts
  if any(x.startswith('.') or x in ['node_modules','qa','tools'] or x.startswith('review') for x in parts):continue
  if rel.as_posix() in ['candidate.mp4','final.mp4']:continue
  if p.suffix.lower() in ['.html','.js','.css','.svg','.ttf','.woff','.woff2','.wav','.mp3','.png','.jpg','.mp4'] or rel.as_posix() in ['explanation.json','visual-system.json','style-lock.json','integration/hf-contributions.json','integration/source-lock.json','assets/motion-catalog.json']:
   files.append(rel.as_posix())
 return {name:sha(root/name) for name in sorted(files)}
def seed(root):
 assert not (root/'explanation.json').exists(),'Storyboard exists; do not overwrite'
 import hf_template
 profile,template_assets=hf_template.install(root)
 legacy=root/'integration/contributions.json'
 if legacy.exists() and read(legacy).get('records')=={}:legacy.unlink()
 write(root/'style-lock.json',{'profileSha256':sha(root/'visual-system.json'),'referenceVideoSha256':profile['referenceVideoSha256'],'templateId':hf_template.DEFAULT,'templateAssets':template_assets,'approval':'user selected the dark fine 2D look as default on 2026-10-28; modules and new films still need review'})
 write(root/'explanation.json',{'schema':'shared-storyboard/v1','motionContract':'semantic-motion/v1','objects':[],'audience':'','question':'','takeaway':'','carrier':'','duration':0,'fps':30,'width':1920,'height':1080,'shots':[]})
 write(root/'integration/hf-contributions.json',{'schema':'seven-shared/v1','records':{}})
def plan(root):
 report=explanation_check(root);assert report['structurePassed'],str(report['errors'])
 class VisibleText(HTMLParser):
  def __init__(self):super().__init__();self.skip=0;self.parts=[]
  def handle_starttag(self,tag,attrs):
   if tag in ['script','style']:self.skip+=1
  def handle_endtag(self,tag):
   if tag in ['script','style']:self.skip=max(0,self.skip-1)
  def handle_data(self,text):
   if not self.skip:self.parts.append(text)
 parser=VisibleText()
 for html in root.rglob('*.html'):
  if not any(x in html.parts for x in ['node_modules','qa','.hyperframes']):parser.feed(html.read_text(encoding='utf-8-sig'))
 visible=re.sub(r'\s+','',''.join(parser.parts))
 p=read(root/'explanation.json');ids=[s['id'] for s in p['shots']];assert len(ids)==len(set(ids)),'Duplicate shot id'
 for s in p['shots']:
  for k in ['evidence','reading','transition']:
   assert isinstance(s.get(k),str) and s[k].strip(),s['id']+': missing '+k
  assert re.sub(r'\s+','',s['claim']) in visible,s['id']+': displayed claim missing from actual HTML'
  assert '。' not in s['claim'],'User preference: no full stops in displayed copy'
  for link in s['implementation']:
   assert link.startswith('#'),'Use stable HTML ids'
 assert p.get('fps') in [24,25,30,50,60] and p.get('width',0)>0 and p.get('height',0)>0
 system=read(root/'visual-system.json');lock=read(root/'style-lock.json')
 assert sha(root/'visual-system.json')==lock['profileSha256'],'Visual system changed; needs explicit style revision and new sample approval'
 assert system['referenceVideoSha256']==lock['referenceVideoSha256']
 if lock.get('templateId')=='engineering-2d-v1':
  for rel,value in lock.get('templateAssets',{}).items():
   assert sha(root/rel)==value,'Shared template changed; create explicit style/module revision: '+rel
  allowed={'split-merge','queue-concurrency','local-patch','dual-compare','transfer','mapping','custom'}
  if p.get('motionContract')=='semantic-motion/v1':
   from semantic_motion import catalog
   allowed={x['id'] for x in catalog()}
  for shot in p['shots']:
   action=shot.get('mechanism',{})
   assert action.get('family') in allowed,shot['id']+': choose an explanation action family'
   for key in ['selectionReason','observableChange','readingHold']:
    assert isinstance(action.get(key),str) and action[key].strip(),shot['id']+': missing mechanism '+key
 return p
def board(root):
 p=plan(root);rows=['# 统一分镜表','', '本表由 explanation.json 生成，改内容请修改该文件后重新生成，不维护第二份分镜','', '| 镜头/时间 | 讲什么 | 对象与变化 | 因此明白什么 | 承接与阅读 | 实现 |','|---|---|---|---|---|---|']
 for s in p['shots']:
  cols=[s['id']+' / '+str(s['start'])+'–'+str(s['start']+s['duration'])+'秒',s['claim'],s['object']+'：'+s['before']+' → '+s['action']+' → '+s['after'],s['meaning']+'；依据：'+s['evidence'],s['transition']+'；阅读：'+s['reading'],'、'.join(s['implementation'])]
  if p.get('motionContract'):
   cols[2]+='；动作：'+s['mechanism']['family']+'；对象ID：'+','.join(x['objectId'] for x in s['objectStates'])
  rows.append('| '+' | '.join(str(c).replace('|','／').replace('\n',' ') for c in cols)+' |')
 (root/'storyboard.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
def record(root,skill,source_key,quote,shots,artifact,anchor,decision):
 integrations.check_sources(root);_,sources=integrations.collect();p=plan(root)
 assert skill in ROLES and source_key in sources and source_key.startswith(skill+'/')
 text=sources[source_key].read_text(encoding='utf-8');assert len(quote.strip())>=12 and quote in text,'Quote must come from actual source'
 ids={s['id'] for s in p['shots']};assert shots and set(shots)<=ids,'Contribution must target real shots'
 target=studio.local(root,artifact);assert target.is_file() and len(anchor)>=8 and anchor in target.read_text(encoding='utf-8'),'Missing real artifact anchor'
 assert len(decision.strip())>=16,'Explain actual choice; listing skill name is insufficient'
 if skill in list(ROLES)[:5]:assert artifact=='explanation.json','Design roles must change the ONE shared storyboard'
 if skill=='mg-styles-15':assert target.suffix in ['.html','.js'],'Implementation role must anchor actual code'
 if skill=='xilo-opus-video':assert artifact=='qa/hf-audit.json','Verification role must use real native audit'
 data=read(root/'integration/hf-contributions.json');data['records'][skill]={'role':ROLES[skill],'shotIds':shots,'sourceKey':source_key,'sourceQuote':quote,'sourceSha256':sha(sources[source_key]),'artifact':artifact,'artifactSha256':sha(target),'anchor':anchor,'decision':decision,'planSha256':sha(root/'explanation.json')};write(root/'integration/hf-contributions.json',data)
def coverage(root):
 integrations.check_sources(root);p=plan(root);_,sources=integrations.collect();r=read(root/'integration/hf-contributions.json')['records']
 assert set(r)==set(ROLES),'All seven actual contributions required'
 for name,row in r.items():
  assert row['role']==ROLES[name] and row['sourceKey'].startswith(name+'/')
  assert sha(sources[row['sourceKey']])==row['sourceSha256'] and row['sourceQuote'] in sources[row['sourceKey']].read_text(encoding='utf-8')
  assert sha(root/row['artifact'])==row['artifactSha256'] and row['anchor'] in (root/row['artifact']).read_text(encoding='utf-8')
  assert row['planSha256']==sha(root/'explanation.json'),'Storyboard changed; refresh affected contribution evidence'
  assert set(row['shotIds'])<={s['id'] for s in p['shots']}
 return {'complete':True,'count':7,'planSha256':sha(root/'explanation.json'),'contributionsSha256':sha(root/'integration/hf-contributions.json')}
def native(root,*args):
 cmd=[sys.executable,'-X','utf8',str(SKILL/'scripts/hyperframes.py'),'--project',str(root),*args]
 r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace')
 if r.returncode:raise RuntimeError((r.stdout+r.stderr)[-5000:])
 return r
def audit(root):
 p=plan(root);before=state(root);r=native(root,'check','--json')
 reports=sorted((root/'.hyperframes/artifacts/checks').glob('*.json'),key=lambda x:x.stat().st_mtime)
 assert reports,'Native check report missing';report=read(reports[-1]);assert report['ok'] and not report.get('browserSkipped'),'Native browser checks did not pass'
 assert report['layout'].get('samples') and report['craft'].get('samples',0)>0,'Browser sampling missing'
 assert report['motion'].get('enabled') and report['motion'].get('samples',0)>0,'Add actual motion assertions; disabled motion checks do not count as pass'
 qa=root/'qa';qa.mkdir(exist_ok=True);shutil.copy2(reports[-1],qa/'hf-native-check.json')
 (qa/'hf-check.log').write_text(r.stdout+r.stderr,encoding='utf-8')
 times=[round(p['duration']*n,3) for n in [.15,.5,.85]]
 native(root,'snapshot','--at',','.join(map(str,times)),'--no-end','--json','-o','qa/seek-forward')
 native(root,'snapshot','--at',','.join(map(str,reversed(times))),'--no-end','--json','-o','qa/seek-reverse')
 from PIL import Image
 def pixels(folder):
  result={}
  for f in folder.glob('frame-*.png'):
   t=float(re.search(r'-at-([\d.]+)s',f.name).group(1));im=Image.open(f).convert('RGB');result[t]=hashlib.sha256(im.tobytes()).hexdigest()
  return result
 a=pixels(qa/'seek-forward');b=pixels(qa/'seek-reverse');assert len(a)==len(b)==3 and a==b,'Random-access frame mismatch'
 native(root,'snapshot','--review','--json','-o','qa/review')
 assert state(root)==before,'Source changed during audit; rerun'
 warnings={k:v.get('findings',[]) for k,v in report.items() if isinstance(v,dict) and v.get('warningCount',0)}
 write(qa/'hf-audit.json',{'backend':'hyperframes','sourceSha256':before,'nativeReportSha256':sha(qa/'hf-native-check.json'),'nativePassed':True,'seekPixels':a,'deterministicSamples':3,'warnings':warnings,'screenshots':{f.relative_to(root).as_posix():sha(f) for f in (qa/'review').glob('*') if f.suffix in ['.jpg','.png']},'limits':'Native checks and three repeated-time frames do not certify comprehension, full-speed flow or listening'})
 print('AUDIT PASSED: native checks, repeat-time pixels and review sheets; semantic review still required')
def candidate(root):
 p=plan(root);cov=coverage(root);audit_report=read(root/'qa/hf-audit.json');current=state(root)
 # Recording contributions changes the evidence file, not render inputs; compare all other inputs.
 def without_records(d):return {k:v for k,v in d.items() if k!='integration/hf-contributions.json'}
 assert without_records(current)==without_records(audit_report['sourceSha256']),'Audit stale'
 before=current;native(root,'render','--quality','looks','--low-memory-mode','--output','candidate.mp4')
 assert state(root)==before,'Inputs changed during render'
 ff=Path(studio.ffmpeg());probe=ff.with_name('ffprobe.exe' if sys.platform=='win32' else 'ffprobe');video=root/'candidate.mp4'
 data=json.loads(subprocess.check_output([str(probe),'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)],text=True))
 v=next(s for s in data['streams'] if s['codec_type']=='video');assert [v['width'],v['height']]==[p['width'],p['height']]
 assert int(v['nb_read_frames'])==round(p['duration']*p['fps']) and abs(float(data['format']['duration'])-p['duration'])<.12
 rate=v['r_frame_rate'].split('/');assert abs(float(rate[0])/float(rate[1])-p['fps'])<.001
 if p.get('audioRequired',True):assert any(s['codec_type']=='audio' for s in data['streams']),'Expected audio track missing'
 subprocess.run([str(ff),'-v','error','-xerror','-i',str(video),'-f','null','-'],check=True,capture_output=True)
 write(root/'qa/hf-candidate.json',{'backend':'hyperframes','videoSha256':sha(video),'sourceSha256':before,'coverage':cov,'auditSha256':sha(root/'qa/hf-audit.json'),'fullDecode':True,'duration':float(data['format']['duration']),'frames':int(v['nb_read_frames']),'reviewStatus':'pending'})
 review=root/'qa/hf-review.json'
 if not review.exists():write(review,{'videoSha256':sha(video),'candidateReportSha256':sha(root/'qa/hf-candidate.json'),'independent':False,'reviewer':'','blockingIssues':['Review not performed'],'fullSpeedWatch':False,'audioListening':False,'audienceTest':'unverified','warningDecisions':{},'axes':{k:{'status':'pending','observations':'','evidence':[]} for k in ['content','continuity','readability','export']}})
 print('CANDIDATE RENDERED; independent four-axis review required')
def release(root):
 coverage(root);r=read(root/'qa/hf-candidate.json');video=root/'candidate.mp4'
 assert r['sourceSha256']==state(root) and r['videoSha256']==sha(video) and r['fullDecode'],'Candidate stale'
 assert r['auditSha256']==sha(root/'qa/hf-audit.json'),'Audit changed'
 rv=read(root/'qa/hf-review.json');assert rv['videoSha256']==sha(video) and rv['candidateReportSha256']==sha(root/'qa/hf-candidate.json'),'Review stale'
 assert rv['independent'] is True and rv['reviewer'] and not rv['blockingIssues']
 for axis in ['content','continuity','readability','export']:
  row=rv['axes'][axis];assert row['status']=='pass' and len(row['observations'].strip())>=20,axis+' not reviewed'
  assert row['evidence'] and all(studio.local(root,x).is_file() for x in row['evidence']),axis+' evidence missing'
 assert rv['fullSpeedWatch'] is True,'Continuous motion requires actual full-speed review'
 if read(root/'explanation.json').get('audioRequired',True):assert rv['audioListening'] is True,'Sound must be actually heard'
 assert isinstance(rv['audienceTest'],str) and rv['audienceTest'],'State real audience test or explicitly unverified'
 warnings=read(root/'qa/hf-audit.json')['warnings'];ack=rv.get('warningDecisions',{})
 for section,findings in warnings.items():
  for finding in findings:assert len(ack.get(section+':'+finding['code'],'').strip())>=20,'Unresolved warning'
 dst=root/'final.mp4'
 if dst.exists() and sha(dst)!=sha(video):
  hist=root/'.releases'/sha(dst)[:12];hist.mkdir(parents=True,exist_ok=True);shutil.copy2(dst,hist/'final.mp4')
 shutil.copy2(video,dst);write(root/'qa/hf-release.json',{'videoSha256':sha(dst),'reviewSha256':sha(root/'qa/hf-review.json'),'candidateSha256':sha(root/'qa/hf-candidate.json'),'audienceTest':rv['audienceTest']});print('RELEASED',dst)
def main():
 studio.configure_runtime();p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['seed','board','plan','record','coverage','audit','candidate','release']);p.add_argument('project',type=Path)
 for key in ['skill','source-key','quote','artifact','anchor','decision']:p.add_argument('--'+key)
 p.add_argument('--shots',nargs='+');a=p.parse_args();root=a.project.resolve()
 if a.command=='record':record(root,a.skill,a.source_key,a.quote,a.shots,a.artifact,a.anchor,a.decision)
 else:
  result=globals()[a.command](root)
  if result is not None:print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print(type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
