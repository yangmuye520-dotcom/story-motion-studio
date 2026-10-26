#!/usr/bin/env python3
"""Portable project, asset/style versions and deterministic Canvas export. No network installs."""
import argparse,base64,functools,hashlib,http.server,importlib.util,json,math,os,platform,re,shutil,subprocess,sys,threading
from pathlib import Path
from datetime import datetime,timezone

STYLE_FILES=('style.json','components.js','index.html')
def configure_runtime():
 """Optional host paths stay outside the portable skill; never install packages implicitly."""
 p=Path(os.environ.get('STORY_MOTION_CONFIG') or str(Path.home()/'.codex/story-motion-studio.local.json'))
 if not p.is_file():return {}
 cfg=json.loads(p.read_text(encoding='utf-8'))
 for entry in reversed(cfg.get('pythonPaths',[])):
  if Path(entry).is_dir() and entry not in sys.path:sys.path.insert(0,entry)
 for field,env in [('chrome','CHROME_PATH'),('ffmpeg','FFMPEG_BINARY')]:
  if cfg.get(field):os.environ.setdefault(env,cfg[field])
 return cfg
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def signed(d):return hashlib.sha256(json.dumps(d,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
def local(root,rel):
 p=(root/rel).resolve()
 if not p.is_relative_to(root.resolve()) or p==root.resolve():raise ValueError('Project-relative path required: '+str(rel))
 return p
def ffmpeg():
 if os.environ.get('FFMPEG_BINARY'):return os.environ['FFMPEG_BINARY']
 if shutil.which('ffmpeg'):return shutil.which('ffmpeg')
 try:
  import imageio_ffmpeg
  return imageio_ffmpeg.get_ffmpeg_exe()
 except ImportError:raise RuntimeError('FFmpeg missing: install FFmpeg or imageio-ffmpeg')
def chrome():
 opts=[os.environ.get('CHROME_PATH'),shutil.which('google-chrome'),shutil.which('chromium'),shutil.which('chrome')]
 for env in ['PROGRAMFILES','PROGRAMFILES(X86)','LOCALAPPDATA']:
  if os.environ.get(env):opts.append(str(Path(os.environ[env])/'Google/Chrome/Application/chrome.exe'))
 opts.append('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 return next((p for p in opts if p and Path(p).is_file()),None)
def doctor():
 cfg=configure_runtime()
 try:f=ffmpeg();v=subprocess.check_output([f,'-version'],text=True).splitlines()[0]
 except Exception as e:f=None;v=str(e)
 d={'python':platform.python_version(),'preferredPython':cfg.get('python'),'playwright':bool(importlib.util.find_spec('playwright')),'pillow':bool(importlib.util.find_spec('PIL')),'numpyForOptionalMusic':bool(importlib.util.find_spec('numpy')),'ffmpeg':v,'chrome':chrome(),'networkInstallPerformed':False}
 print(json.dumps(d,ensure_ascii=False,indent=2))
 return d
def upstreams(root):
 root=Path(root) if root else Path(os.environ.get('STORY_MOTION_UPSTREAM') or str(Path.home()/'.codex/skills/video'))
 names=['wtt-code-animation-studio','lemo-opuscar','huashu-art-motion','video-shotcraft','dashi-animationstyle','mg-styles-15','xilo-opus-video']
 print(json.dumps({n:{'path':str(root/n),'exists':(root/n).is_dir(),'skillEntry':(root/n/'SKILL.md').is_file()} for n in names},ensure_ascii=False,indent=2))
def compile_film(root):
 f=read(root/'film.json');fps=f['fps'];w=f['width'];h=f['height'];last=0;sc=[]
 assert isinstance(fps,int) and 1<=fps<=120 and w>=320 and h>=320
 assert f['scenes'],'No scenes'
 for row in f['scenes']:
  s=dict(row);n=round(float(s['duration'])*fps);assert n>0 and s['copy'] and s['purpose'] and s['outcome']
  assert s['events'],'Each scene needs explicit semantic events'
  for e in s['events']:assert 0<=float(e['at'])<n/fps and e['action']
  s.update(startFrame=last,endFrame=last+n);last+=n;sc.append(s)
 t={**f,'scenes':sc,'totalFrames':last,'duration':last/fps};write(root/'timeline.json',t);return t
def style_state(root):
 files=list(STYLE_FILES)+sorted(p.relative_to(root).as_posix() for p in (root/'fonts').rglob('*') if p.is_file())
 return {p:digest(root/p) for p in files}
def check_style(root):
 lock=read(root/'style-baseline.json');assert lock['files']==style_state(root),'Style changed: preserve baseline and propose a new style version'
 assert lock['evidence'].strip(),'Missing real approval/delegation evidence';return lock
def style_lock(root,evidence):
 if (root/'style-baseline.json').exists():return check_style(root)
 assert evidence.strip(),'Approval/delegation evidence required'
 lock={'files':style_state(root),'evidence':evidence,'recordedAt':datetime.now(timezone.utc).isoformat(),'toolCannotVerifyHumanConsent':True}
 write(root/'style-baseline.json',lock);return lock
def export_style(root,target):
 check_style(root);assert not target.exists(),'Style target already exists';target.mkdir(parents=True)
 for name in (*STYLE_FILES,'style-baseline.json'):shutil.copy2(root/name,target/name)
 if (root/'fonts').exists():shutil.copytree(root/'fonts',target/'fonts')
def resolve_style_pack(value):
 """Accept the former skill/styles/id location after moving packs to assets/styles."""
 pack=Path(value).resolve()
 if pack.is_dir():return pack
 if pack.parent.name=='styles':
  migrated=pack.parent.parent/'assets/styles'/pack.name
  if migrated.is_dir():return migrated
 raise FileNotFoundError('Style pack not found: '+str(pack))
def init(root,style_pack):
 from integrations import collect,bind
 collect()
 assert not root.exists(),'New project path must not exist'
 src=Path(__file__).resolve().parent.parent/'assets/starter';assert src.is_dir(),'Use installed skill scripts/studio.py for init'
 shutil.copytree(src,root);(root/'tools').mkdir()
 for n in ['studio.py','music.py','integrations.py','samples.py']:shutil.copy2(Path(__file__).parent/n,root/'tools'/n)
 if style_pack:
  style_pack=resolve_style_pack(style_pack);check_style(style_pack)
  for n in (*STYLE_FILES,'style-baseline.json'):shutil.copy2(style_pack/n,root/n)
  if (style_pack/'fonts').exists():shutil.copytree(style_pack/'fonts',root/'fonts',dirs_exist_ok=True)
  check_style(root)
 compile_film(root);bind(root);print('PROJECT_READY_SEVEN_REQUIRED',str(root))
def manifest(root):
 m=read(root/'assets.json');out=[];seen=set()
 for a in m['assets']:
  assert all(a.get(k) for k in ['path','source','license','useBasis']),a
  assert a['path'] not in seen,'Duplicate asset';seen.add(a['path']);p=local(root,a['path']);assert p.is_file(),str(p)
  assert not any(part.startswith('.') for part in Path(a['path']).parts),'Private/history files cannot be source assets'
  out.append({**a,'sha256':digest(p)})
 return {'assets':sorted(out,key=lambda a:a['path'])}
def check_assets(root):
 current=read(root/'asset-lock.json');assert current['manifest']==manifest(root),'Asset bytes or metadata changed; propose/accept required';return current
def save_version(root,m,evidence):
 hist=root/'.asset-history';hist.mkdir(exist_ok=True);versions=sorted(p for p in hist.glob('v[0-9][0-9][0-9][0-9]') if p.is_dir());v=f'v{len(versions)+1:04}'
 target=hist/v;target.mkdir()
 for a in m['assets']:
  dst=target/'files'/a['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(local(root,a['path']),dst)
 lock={'version':v,'manifest':m,'manifestSha256':signed(m),'evidence':evidence};write(target/'record.json',lock);write(root/'asset-lock.json',lock);return lock
def asset_action(root,action,evidence=None,candidate_sha=None):
 m=manifest(root)
 if action=='check':return check_assets(root)
 if action=='seal':
  assert not (root/'asset-lock.json').exists(),'Existing lock cannot be resealed'
  return save_version(root,m,'Initial project asset selection; no subsequent replacement approval implied')
 old=read(root/'asset-lock.json');before={a['path']:a for a in old['manifest']['assets']};after={a['path']:a for a in m['assets']};diff=[{'path':p,'old':before.get(p),'new':after.get(p)} for p in sorted(before.keys()|after.keys()) if before.get(p)!=after.get(p)]
 if action=='propose':
  assert diff,'No changes';c={'base':old['manifestSha256'],'manifest':m,'diff':diff};write(root/'asset-candidate.json',c);result={'candidateSha256':signed(c),'diff':diff};print(json.dumps(result,ensure_ascii=False,indent=2));return result
 c=read(root/'asset-candidate.json');assert candidate_sha==signed(c),'Candidate hash mismatch';assert c['base']==old['manifestSha256'] and c['manifest']==m,'Candidate stale';assert evidence and evidence.strip(),'Real replacement authorization required'
 lock=save_version(root,m,evidence);write(root/'.asset-history'/lock['version']/'change.json',c);(root/'asset-candidate.json').unlink();return lock
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
def serve(root,export=False):
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)))
 if export:threading.Thread(target=server.serve_forever,daemon=True).start();return server
 import webbrowser
 url=f'http://127.0.0.1:{server.server_port}/index.html';print(url,flush=True);webbrowser.open(url)
 try:server.serve_forever()
 except KeyboardInterrupt:pass
 finally:server.server_close()
def render(root,preview=False,draft=False):
 from integrations import check_sources,check
 check_sources(root)
 from playwright.sync_api import sync_playwright
 from PIL import Image,ImageDraw
 import io
 t=compile_film(root);assets=check_assets(root);style=None
 if not draft:style=check_style(root)
 if not draft and not preview:check(root,True)
 fps=t['fps'];W=t['width'];H=t['height'];F=ffmpeg();(root/'qa').mkdir(exist_ok=True);(root/'previews').mkdir(exist_ok=True)
 server=serve(root,True);errors=[];audits=[];det=[];source={n:digest(root/n) for n in ['film.json','timeline.json','style.json','components.js','index.html','scenes.js','runtime.js']}
 report={'draft':draft,'materialVersion':assets['version'],'style':style,'sourceSha256':source,'rendererSha256':digest(__file__),'audioHumanListening':'not performed','visualFullWatch':'not performed'}
 try:
  with sync_playwright() as p:
   opts={'headless':True};ch=chrome()
   if ch:opts['executable_path']=ch
   browser=p.chromium.launch(**opts);page=browser.new_page(viewport={'width':W,'height':H},device_scale_factor=1);page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(f'http://127.0.0.1:{server.server_port}/index.html?export'+('&draft' if draft else ''));page.wait_for_function('window.__ready===true',timeout=60000);assert page.evaluate('document.fonts.check("600 56px StudioSans")'),'Local font missing'
   def frame(n,fmt='image/jpeg'):
    return base64.b64decode(page.evaluate('(a)=>{renderFrame(a[0]);return document.querySelector("canvas").toDataURL(a[1],.94).split(",")[1]}',[int(n),fmt]))
   sheet=Image.new('RGB',(960,math.ceil(len(t['scenes'])/2)*300),'#eee');draw=ImageDraw.Draw(sheet)
   for i,s in enumerate(t['scenes']):
    for j,r in enumerate([.15,.5,.85]):
     n=s['startFrame']+int((s['endFrame']-s['startFrame'])*r);im=frame(n,'image/png');(root/'previews'/f'{i:02}-{j}.png').write_bytes(im)
     if j==1:sheet.paste(Image.open(io.BytesIO(im)).resize((480,270)),(i%2*480,i//2*300));draw.text((i%2*480+8,i//2*300+275),f'{i} / {n/fps:.2f}s',fill='black')
   sheet.save(root/'previews/contact.jpg')
   for n in range(0,t['totalFrames'],max(1,fps//2)):
    page.evaluate('(n)=>renderFrame(n)',n)
    for a in page.evaluate('window.audit'):
     if a['x']<0 or a['y']<0 or a['x']+a['width']>W or a['y']+a['height']>H:audits.append({'frame':n,**a})
   for n in sorted(set([0,t['totalFrames']//3,t['totalFrames']-1])):
    a=hashlib.sha256(frame(n,'image/png')).hexdigest();frame(t['totalFrames']//2);b=hashlib.sha256(frame(n,'image/png')).hexdigest();det.append(a==b)
   report.update(browserErrors=errors,textBoundsViolations=audits,deterministic=det,fontReady=True)
   preview_path=root/'qa/preview-report.json' if preview or not (root/'qa/preview-report.json').exists() else root/'qa/render-preview-report.json'
   write(preview_path,report);assert not errors and not audits and all(det),'See qa preview report'
   if preview:browser.close();return report
   temp=root/'draft-silent.mp4' if draft else root/'silent.mp4';cmd=[F,'-y','-v','error','-f','image2pipe','-vcodec','mjpeg','-framerate',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(temp)]
   enc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
   try:
    for n in range(t['totalFrames']):
     enc.stdin.write(frame(n))
     if n%(fps*10)==0:print('FRAME',n,'/',t['totalFrames'],flush=True)
    enc.stdin.close();assert enc.wait()==0
   except BaseException:enc.kill();enc.wait();raise
   browser.close()
  assert source=={n:digest(root/n) for n in source},'Sources changed while rendering';check_assets(root)
  if not draft:check_style(root)
  out=root/('draft.mp4' if draft else 'candidate.mp4');audio=t.get('audio')
  if audio:
   ap=local(root,audio);assert any(a['path']==audio for a in assets['manifest']['assets']),'Audio must be sealed as an asset'
   probe=subprocess.run([F,'-hide_banner','-i',str(ap)],capture_output=True,text=True)
   ad=re.search(r'Duration: (\d+):(\d+):([\d.]+)',probe.stderr);assert ad,'Cannot measure input audio duration'
   alen=int(ad[1])*3600+int(ad[2])*60+float(ad[3]);padding=max(0,t['duration']-alen)
   assert padding<.1 or t.get('allowAudioSilencePadding') is True,'Audio too short: explicitly choose padding or provide a full-length track'
   report.update(audioInputDuration=alen,silencePaddingSeconds=padding)
   subprocess.run([F,'-y','-v','error','-i',str(temp),'-i',str(ap),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',f'apad=whole_dur={t["duration"]}','-c:a','aac','-b:a','192k','-t',str(t['duration']),'-movflags','+faststart',str(out)],check=True)
  else:shutil.copy2(temp,out)
  decoded=subprocess.run([F,'-hide_banner','-i',str(out),'-f','null','-'],capture_output=True,text=True,check=True)
  stream=next(s for s in decoded.stderr.splitlines() if 'Video:' in s and 'Stream #' in s)
  dims=re.search(r'(\d{2,5})x(\d{2,5})',stream);rate=re.search(r', ([\d.]+) fps',stream);duration=re.search(r'Duration: (\d+):(\d+):([\d.]+)',decoded.stderr)
  assert dims and list(map(int,dims.groups()))==[W,H] and rate and abs(float(rate[1])-fps)<.01,'Unexpected encoded size/fps'
  actualDuration=int(duration[1])*3600+int(duration[2])*60+float(duration[3]);assert abs(actualDuration-t['duration'])<.1
  report.update(fullDecode=True,totalFrames=t['totalFrames'],duration=actualDuration,size=[W,H],fps=float(rate[1]),voice=t.get('voice',False),audio=audio,output=out.name,outputSha256=digest(out),sevenSkills=check(root,not draft));write(root/'qa'/('draft-report.json' if draft else 'candidate-report.json'),report);print('RENDER_READY_REVIEW_REQUIRED',str(out),flush=True);return report
 finally:server.shutdown();server.server_close()
def main():
 configure_runtime()
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='cmd',required=True)
 sub.add_parser('doctor');u=sub.add_parser('upstreams');u.add_argument('--root')
 q=sub.add_parser('init');q.add_argument('project');q.add_argument('--style-pack')
 for name in ['compile','serve','style-check']:q=sub.add_parser(name);q.add_argument('project')
 q=sub.add_parser('style-lock');q.add_argument('project');q.add_argument('--evidence',required=True)
 q=sub.add_parser('export-style');q.add_argument('project');q.add_argument('target')
 q=sub.add_parser('assets');q.add_argument('project');q.add_argument('action',choices=['seal','check','propose','accept']);q.add_argument('--evidence');q.add_argument('--candidate-sha')
 q=sub.add_parser('render');q.add_argument('project');q.add_argument('--preview',action='store_true');q.add_argument('--draft',action='store_true')
 a=p.parse_args()
 if a.cmd=='doctor':doctor();return
 if a.cmd=='upstreams':upstreams(a.root);return
 root=Path(a.project).resolve()
 if a.cmd=='init':init(root,a.style_pack)
 elif a.cmd=='compile':print('TIMELINE',compile_film(root)['totalFrames'])
 elif a.cmd=='serve':serve(root)
 elif a.cmd=='style-check':print(json.dumps(check_style(root),ensure_ascii=False))
 elif a.cmd=='style-lock':print(json.dumps(style_lock(root,a.evidence),ensure_ascii=False))
 elif a.cmd=='export-style':export_style(root,Path(a.target).resolve())
 elif a.cmd=='assets':print(json.dumps(asset_action(root,a.action,a.evidence,a.candidate_sha),ensure_ascii=False))
 elif a.cmd=='render':render(root,a.preview,a.draft)
if __name__=='__main__':
 try:main()
 except Exception as e:print(f'ERROR: {type(e).__name__}: {e}',file=sys.stderr);sys.exit(1)
