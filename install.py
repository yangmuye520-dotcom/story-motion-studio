#!/usr/bin/env python3
"""Install the seven required sources and an isolated code-animation runtime."""
import argparse,hashlib,json,os,re,shutil,subprocess,sys,venv,urllib.request,urllib.parse,time,concurrent.futures,uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MEDIA_EXCLUDES=['!*.mp4','!*.mov','!*.webm','!*.wav','!*.mp3','!*.flac','!*.zip','!*.blend']
def run(args,**kwargs):
 print('+ '+str(args[0])+' '+str(args[1]),flush=True)
 return subprocess.run([str(a) for a in args],check=True,**kwargs)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_files(root,expected):
 for rel,sha in expected.items():
  p=(root/rel).resolve()
  if not p.is_relative_to(root.resolve()) or not re.fullmatch('[0-9a-f]{64}',sha):raise ValueError('Invalid file lock')
  if not p.is_file() or digest(p)!=sha:raise RuntimeError('Required source missing/changed: '+str(p))
def load_lock(root=ROOT):
 lock=json.loads((root/'upstreams.lock.json').read_text(encoding='utf-8'))
 names={x['name'] for x in lock['items']}
 if len(lock['items'])!=7 or len(names)!=7:raise ValueError('Exactly seven upstreams required')
 for row in lock['items']:
  if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',row['repo']) or not re.fullmatch('[a-f0-9]{40}',row['commit']):raise ValueError('Invalid repository lock')
  if not re.fullmatch('[a-z0-9-]+',row['name']):raise ValueError('Invalid skill name')
  part=Path(row['subdir'])
  if part.is_absolute() or '..' in part.parts:raise ValueError('Invalid source directory')
 return lock

def plan(args,lock):
 codex=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex'))).resolve()
 skills=(args.skills_dir or codex/'skills').resolve();data=(args.data_dir or codex/'story-motion-studio-runtime').resolve()
 config=(args.config or Path.home()/'.codex/story-motion-studio.local.json').resolve()
 targets=[skills/'story-motion-studio']+[skills/'video'/x['name'] for x in lock['items']]
 conflicts=[str(p) for p in targets+[config] if p.exists()]
 if conflicts:raise RuntimeError('Existing files will NOT be overwritten. Back up/move them or select a fresh destination:\n'+'\n'.join(conflicts))
 if data==skills or data.is_relative_to(skills/'story-motion-studio'):raise ValueError('Runtime data must stay outside the installed skill')
 return skills,data,config,targets

def http_bytes(url):
 for attempt in range(3):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'story-motion-studio installer','Accept':'application/vnd.github+json'})
   with urllib.request.urlopen(req,timeout=35) as response:return response.read()
  except Exception:
   if attempt==2:raise
   time.sleep(attempt+1)

def checkout(row,cache,git):
 # The Git tree binds raw file paths and blob IDs to a fixed commit, no default-branch drift
 d=cache/(row['repo'].replace('/','--')+'-'+row['commit'][:12]+'-http')
 marker=d/'.story-motion-source.json'
 tree=json.loads(http_bytes('https://api.github.com/repos/'+row['repo']+'/git/trees/'+row['commit']+'?recursive=1'))
 if tree.get('truncated'):raise RuntimeError('Upstream tree truncated, refusing incomplete install')
 extensions={'.md','.py','.js','.mjs','.cjs','.json','.yaml','.yml','.txt','.html','.css','.sh','.ps1','.ts','.tsx','.jsx','.glsl','.vert','.frag','.svg'}
 entries=[]
 for item in tree['tree']:
  rel=item['path'];part=Path(rel)
  if item['type']!='blob' or item.get('mode')=='120000':continue
  if part.is_absolute() or '..' in part.parts:raise ValueError('Unsafe upstream path')
  if row['subdir'] and row['name']!='lemo-opuscar' and not (rel.startswith(row['subdir']+'/') or rel.upper().startswith(('LICENSE','NOTICE','COPYING'))):continue
  if any(p in {'node_modules','.git','__pycache__'} for p in part.parts):continue
  if part.suffix.lower() not in extensions and not part.name.upper().startswith(('LICENSE','NOTICE','COPYING')):continue
  if item.get('size',0)>25*1024*1024:continue
  entries.append(item)
 if not entries:raise RuntimeError('No upstream source files found')
 expected={'repo':row['repo'],'commit':row['commit'],'format':'text-source-snapshot/v1'}
 if d.exists():
  if not marker.is_file() or json.loads(marker.read_text(encoding='utf-8'))!=expected:raise RuntimeError('Unexpected upstream cache, inspect it first: '+str(d))
 else:
  d.mkdir(parents=True)
  with marker.open('x',encoding='utf-8') as out:json.dump(expected,out)
 def file_ok(path,item):
  if not path.is_file():return False
  data=path.read_bytes();return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['sha']
 def fetch(item):
  path=(d/item['path']).resolve()
  if not path.is_relative_to(d.resolve()):raise ValueError('Unsafe upstream path')
  if path.exists():
   if file_ok(path,item):return
   raise RuntimeError('Modified upstream cache file, refusing overwrite: '+str(path))
  url='https://raw.githubusercontent.com/'+row['repo']+'/'+row['commit']+'/'+urllib.parse.quote(item['path'])
  data=http_bytes(url)
  if hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=item['sha']:raise RuntimeError('Git blob hash mismatch: '+item['path'])
  path.parent.mkdir(parents=True,exist_ok=True);temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.part')
  with temp.open('xb') as out:out.write(data)
  temp.rename(path)
 print('Downloading source snapshot: '+row['repo']+' ('+str(len(entries))+' text/code files, large media excluded)',flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(fetch,entries))
 return d

def find_chrome():
 opts=[os.environ.get('CHROME_PATH'),shutil.which('chrome'),shutil.which('google-chrome'),shutil.which('chromium')]
 for name in ['PROGRAMFILES','PROGRAMFILES(X86)','LOCALAPPDATA']:
  if os.environ.get(name):opts.append(str(Path(os.environ[name])/'Google/Chrome/Application/chrome.exe'))
 opts.append('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 return next((str(Path(p).resolve()) for p in opts if p and Path(p).is_file()),None)
def runtime(data):
 env=data/'venv';venv.EnvBuilder(with_pip=True).create(env)
 py=env/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
 run([py,'-m','pip','install','--disable-pip-version-check','-r',ROOT/'requirements-install.txt'])
 chrome=find_chrome()
 if not chrome:
  run([py,'-m','playwright','install','chromium'])
  chrome=subprocess.check_output([str(py),'-c','from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()'],text=True).strip()
 ffmpeg=subprocess.check_output([str(py),'-c','import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())'],text=True).strip()
 site=subprocess.check_output([str(py),'-c','import site,json; print(json.dumps(site.getsitepackages()))'],text=True)
 return py,chrome,ffmpeg,json.loads(site)
def safe_copy(src,dst):
 def ignore(folder,names):
  return [n for n in names if n in {'.git','__pycache__','.venv','tests','.story-motion-source.json'} or n.endswith(('.pyc','.local.json')) or (Path(folder)/n).is_symlink()]
 shutil.copytree(src,dst,ignore=ignore)

def install(args):
 if sys.version_info<(3,10):raise RuntimeError('Python 3.10 or newer required')
 lock=load_lock();skills,data,config,targets=plan(args,lock)
 print('Target skills: '+str(skills));print('Runtime/config: '+str(data)+' / '+str(config))
 if args.check:
  print('PLAN OK, no installation or network requests performed');return
 git=shutil.which('git')
 if not git:raise RuntimeError('Git missing; run install.ps1 -InstallSystemTools on Windows with winget')
 cache=data/'upstreams';sources={};lemo=None
 for row in lock['items']:
  repo=checkout(row,cache,git);src=repo/row['subdir'];verify_files(src,row['requiredSha256']);sources[row['name']]=src
  if 'libraryRequiredSha256' in row:verify_files(repo,row['libraryRequiredSha256']);lemo=repo
 if lemo is None:raise RuntimeError('Lemo actual library missing')
 if args.skip_runtime:py,chrome,ff,sites=Path(sys.executable),find_chrome(),None,[]
 else:py,chrome,ff,sites=runtime(data)
 # Check conflicts again after downloads before writing any installed skill/config
 plan(args,lock)
 skills.mkdir(parents=True,exist_ok=True)
 safe_copy(ROOT,targets[0])
 for row in lock['items']:
  dst=skills/'video'/row['name'];dst.parent.mkdir(parents=True,exist_ok=True);safe_copy(sources[row['name']],dst)
 cfg={'python':str(py),'pythonPaths':sites,'upstreamRoot':str(skills/'video'),'lemoLibrary':str(lemo),'managedBy':'story-motion-studio installer'}
 if chrome:cfg['chrome']=chrome
 if ff:cfg['ffmpeg']=ff
 config.parent.mkdir(parents=True,exist_ok=True)
 with config.open('x',encoding='utf-8') as out:json.dump(cfg,out,ensure_ascii=False,indent=2)
 env=os.environ.copy();env['STORY_MOTION_CONFIG']=str(config);env['PYTHONUTF8']='1'
 run([py,targets[0]/'scripts/integrations.py','doctor'],env=env)
 if not args.skip_runtime:
  run([py,targets[0]/'scripts/studio.py','doctor'],env=env)
  # Launch a real browser and draw one frame, not only package-presence checks
  code='from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(headless=True,executable_path='+repr(chrome)+'); page=b.new_page(); page.set_content("<canvas id=c width=64 height=64></canvas>"); assert page.evaluate("(()=>{let c=document.querySelector(\'canvas\'); c.getContext(\'2d\').fillRect(0,0,10,10);return c.toDataURL().startsWith(\'data:image/png\')})()"); b.close(); p.stop()'
  run([py,'-c',code],env=env)
 receipt={'status':'sources-only' if args.skip_runtime else 'runtime-and-sources-checked','upstreamLockSha256':digest(ROOT/'upstreams.lock.json'),'config':str(config),'skills':str(skills),'limitations':'No full film generated, no narration model installed, no aesthetic or listening review performed'}
 (data/'install-receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
 print('SOURCES ONLY - runtime not installed' if args.skip_runtime else 'INSTALL COMPLETE - seven sources and browser runtime checked')
 print('Skill is available to Codex on the next turn. Start with a short sample, not a full unreviewed film.')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--skills-dir',type=Path);p.add_argument('--data-dir',type=Path);p.add_argument('--config',type=Path);p.add_argument('--check',action='store_true');p.add_argument('--skip-runtime',action='store_true',help='Advanced sources-only install; not a complete runtime')
 try:install(p.parse_args())
 except Exception as e:print('INSTALL STOPPED: '+str(e),file=sys.stderr);return 1
 return 0
if __name__=='__main__':sys.exit(main())
