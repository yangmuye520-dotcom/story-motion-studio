"""Complete a local free HyperFrames environment; never overwrite installed skills."""
import argparse,importlib.util,json,os,shutil,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def command(args,**kw):
 return subprocess.run([str(x) for x in args],check=True,**kw)

def save_config(path,cfg):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists():
  backup=path.with_name(path.name+'.before-hyperframes-'+str(time.time_ns()))
  shutil.copy2(path,backup)
 temp=path.with_name(path.name+'.tmp-'+str(time.time_ns()))
 temp.write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf-8');os.replace(temp,path)

def node_tools():
 node=shutil.which('node');npm=shutil.which('npm.cmd' if os.name=='nt' else 'npm')
 if not node or not npm:raise RuntimeError('Node.js 22+ and npm required; use install.ps1 -InstallSystemTools')
 major=int(subprocess.check_output([node,'--version'],text=True).strip().lstrip('v').split('.')[0])
 if major<22:raise RuntimeError('Node.js 22+ required; installed version is older, upgrade explicitly')
 return node,npm

def setup(skills,data,config,check=False,reuse_existing=False):
 import install as base
 skills=Path(skills).resolve();data=Path(data).resolve();config=Path(config).resolve()
 lock=json.loads((ROOT/'hyperframes.lock.json').read_text(encoding='utf-8'))
 if check:return {'runtime':lock['runtime'],'skills':[x['name'] for x in lock['items']],'data':str(data),'config':str(config),'network':False}
 cfg=json.loads(config.read_text(encoding='utf-8'));oldhf=cfg.get('hyperframes',{})
 node,npm=node_tools();env=os.environ.copy();env['PUPPETEER_SKIP_DOWNLOAD']='true'
 runtime=data/'hyperframes';runtime.mkdir(parents=True,exist_ok=True)
 existing=Path(oldhf.get('cli',''))
 if existing.is_file():
  package=existing.parent.parent/'package.json'
  if json.loads(package.read_text(encoding='utf-8'))['version']!=lock['runtime']:raise RuntimeError('Existing HyperFrames version differs; refusing implicit upgrade')
  cli=existing
 else:
  cli=runtime/'node_modules/hyperframes/bin/hyperframes.mjs'
  if not (runtime/'package.json').exists():(runtime/'package.json').write_text('{"private":true}',encoding='utf-8')
  command([npm,'install','--save-exact','hyperframes@'+lock['runtime'],'ffprobe-static@'+lock['ffprobe'],'--no-audit','--no-fund'],cwd=runtime,env=env)
 probe=Path(cfg.get('ffprobe',''))
 ff=Path(cfg.get('ffmpeg',''))
 if not ff.is_file():raise RuntimeError('Configured FFmpeg missing; complete base installation first')
 if not probe.is_file():probe=ff.with_name('ffprobe.exe' if os.name=='nt' else 'ffprobe')
 if not probe.is_file():
  command([npm,'install','--save-exact','ffprobe-static@'+lock['ffprobe'],'--no-audit','--no-fund'],cwd=runtime,env=env)
  probe=Path(subprocess.check_output([node,'-e',"process.stdout.write(require('ffprobe-static').path)"],cwd=runtime,text=True))
 for binary in [ff,probe]:command([binary,'-version'],stdout=subprocess.DEVNULL)
 chrome=Path(cfg.get('chrome',''))
 if not chrome.is_file():raise RuntimeError('Configured Chrome/Chromium missing; complete base installation first')
 records=[]
 for row in lock['items']:
  dest=skills/row['name']
  if dest.exists():
   try:
    base.verify_files(dest,row['requiredSha256']);records.append({'name':row['name'],'status':'locked-existing'})
   except RuntimeError:
    if not reuse_existing:raise
    entry=dest/'SKILL.md'
    if not entry.is_file() or ('name: '+row['name']) not in entry.read_text(encoding='utf-8'):raise RuntimeError('Existing official skill is invalid: '+str(dest))
    records.append({'name':row['name'],'status':'preserved-existing-version','sha256':base.digest(entry)})
    print('Preserving existing skill version: '+row['name'],flush=True)
   continue
  snapshot=base.checkout(row,data/'upstreams',shutil.which('git'))
  base.verify_files(snapshot/row['subdir'],row['requiredSha256'])
  base.safe_copy(snapshot/row['subdir'],dest);records.append({'name':row['name'],'status':'installed-locked'})
 cfg['hyperframes']={**oldhf,'cli':str(cli),'node':node,'version':lock['runtime']};cfg['ffprobe']=str(probe)
 save_config(config,cfg)
 child=os.environ.copy();child['STORY_MOTION_CONFIG']=str(config);child.pop('HYPERFRAMES_CLI',None)
 python=cfg.get('python') or sys.executable
 command([python,skills/'story-motion-studio/scripts/studio_localize.py'],env=child)
 return {'runtime':str(cli),'node':node,'ffprobe':str(probe),'officialSkills':records,'config':str(config)}

def smoke(skills,data,config):
 cfg=json.loads(Path(config).read_text(encoding='utf-8'));env=os.environ.copy()
 env.update(STORY_MOTION_CONFIG=str(config),PYTHONUTF8='1',HYPERFRAMES_NO_TELEMETRY='1',HYPERFRAMES_NO_UPDATE_CHECK='1',HYPERFRAMES_SKIP_SKILLS='1',PUPPETEER_EXECUTABLE_PATH=cfg['chrome'],HYPERFRAMES_FFMPEG_PATH=cfg['ffmpeg'],HYPERFRAMES_FFPROBE_PATH=cfg['ffprobe'])
 env.pop('HYPERFRAMES_CLI',None)
 env['PYTHONPATH']=os.pathsep.join(cfg.get('pythonPaths',[])+([env['PYTHONPATH']] if env.get('PYTHONPATH') else []))
 py=cfg.get('python') or sys.executable;skill=Path(skills)/'story-motion-studio'
 # Borrow only bundled licensed assets, not private videos or prior project config.
 work=Path(tempfile.mkdtemp(prefix='install-smoke-',dir=data));shutil.copytree(skill/'assets/templates/engineering-2d-v1/assets',work/'assets')
 (work/'index.html').write_text('''<!doctype html><html><head><script src="assets/gsap.min.js"></script><style>html,body{margin:0;background:#0a0b0e;color:white}#dot{position:absolute;left:80px;top:80px;width:30px;height:30px;background:#c9a46b}</style></head><body><div id="root" data-composition-id="main" data-duration="1" data-width="640" data-height="360"><div id="dot"></div></div><script>const tl=gsap.timeline({paused:true});tl.to('#dot',{x:300,duration:1,ease:'none'});window.__timelines={main:tl};</script></body></html>''',encoding='utf-8')
 hf=cfg['hyperframes'];cli=[hf['node'],hf['cli']]
 command(cli+['render','--quality','standard','--low-memory-mode','--output','smoke.mp4'],cwd=work,env=env)
 out=work/'smoke.mp4';command([cfg['ffmpeg'],'-v','error','-i',out,'-f','null','-'],env=env)
 probe=json.loads(subprocess.check_output([cfg['ffprobe'],'-v','error','-show_streams','-of','json',out],text=True))
 video=next(x for x in probe['streams'] if x['codec_type']=='video')
 if (video['width'],video['height'])!=(640,360) or abs(float(video['duration'])-1)>.1:raise RuntimeError('Smoke video size/duration mismatch')
 # Serve and execute the actual patched UI in a fresh browser, not merely check files.
 script='''import sys,subprocess,json,socket
from playwright.sync_api import sync_playwright
cli=json.loads(sys.argv[1]);cfg=json.loads(sys.argv[2]);work=sys.argv[3]
with socket.socket() as sock:
 sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
try:
 subprocess.run(cli+['preview','--background','--port',str(port)],cwd=work,check=True)
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path=cfg['chrome'],headless=True)
  try:
   page=b.new_page();page.goto('http://127.0.0.1:'+str(port),wait_until='domcontentloaded')
   page.wait_for_function('window.HFStudioChinese !== undefined && document.querySelectorAll("button").length > 2')
   assert page.evaluate('HFStudioChinese.translate("Export")')=='导出'
   assert page.title()=='HyperFrames 中文工作台'
   assert page.locator('button').filter(has_text='导出').count()>0
  finally:b.close()
finally:subprocess.run(cli+['preview','--stop'],cwd=work,check=True)
'''
 command([py,'-c',script,json.dumps(cli),json.dumps(cfg),str(work)],env=env)
 return {'video':str(out),'duration':1,'decoded':True,'chineseUiExecuted':True,'actualPreviewMenuVerified':True,'limits':'Installation smoke only, not aesthetic or audience comprehension certification'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--skills-dir',type=Path,required=True);p.add_argument('--data-dir',type=Path,required=True);p.add_argument('--config',type=Path,required=True);p.add_argument('--check',action='store_true');a=p.parse_args()
 print(json.dumps(setup(a.skills_dir,a.data_dir,a.config,a.check),ensure_ascii=False,indent=2))
 if not a.check:print(json.dumps(smoke(a.skills_dir,a.data_dir,a.config),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
