"""Local pinned HyperFrames adapter. Does not install software or certify film quality."""
import argparse,json,os,shutil,subprocess,sys
from pathlib import Path
import studio

VERSION='0.8.207'
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--project',type=Path,default=Path.cwd())
 p.add_argument('command',choices=['doctor','init','check','snapshot','preview','render','timeline','catalog','localize'])
 p.add_argument('args',nargs=argparse.REMAINDER)
 a=p.parse_args();cfg=studio.configure_runtime();hf=cfg.get('hyperframes',{})
 cli=Path(os.environ.get('HYPERFRAMES_CLI') or hf.get('cli',''))
 if not cli.is_file():p.error('HyperFrames runtime missing; read references/hyperframes.md and configure hyperframes.cli')
 package=cli.parent.parent/'package.json'
 if not package.is_file() or json.loads(package.read_text(encoding='utf-8')).get('version')!=VERSION:
  p.error('Expected pinned HyperFrames '+VERSION+'; review upgrade before changing the pin')
 node=hf.get('node') or shutil.which('node')
 if not node:p.error('Node.js missing; read setup guide')
 env=os.environ.copy();ff=Path(studio.ffmpeg());probe=ff.with_name('ffprobe.exe' if os.name=='nt' else 'ffprobe')
 env.update(HYPERFRAMES_FFMPEG_PATH=str(ff),HYPERFRAMES_NO_TELEMETRY='1',HYPERFRAMES_NO_UPDATE_CHECK='1',HYPERFRAMES_SKIP_SKILLS='1')
 env['PATH']=str(ff.parent)+os.pathsep+env.get('PATH','')
 if probe.is_file():env['HYPERFRAMES_FFPROBE_PATH']=str(probe)
 chrome=studio.chrome()
 if chrome:env['PUPPETEER_EXECUTABLE_PATH']=chrome
 root=a.project.resolve()
 if not root.is_dir():p.error('Project directory does not exist')
 if a.command=='localize':
  import studio_localize
  print(json.dumps(studio_localize.apply(),ensure_ascii=False,indent=2));return 0
 if a.command=='preview':
  import studio_localize
  studio_localize.apply()
 if a.command=='check':
  from explanation_check import check
  report=check(root);print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
  if not report['structurePassed']:return 2
 args=list(a.args)
 if args[:1]==['--']:args=args[1:]
 if a.command=='render':
  if '--output' not in args:args+=['--output','candidate.mp4']
  output=args[args.index('--output')+1]
  if Path(output).name=='final.mp4':p.error('Render to candidate.mp4; final requires seven-source evidence and independent review')
 if a.command=='init':
  if not args or args[0].startswith('-'):p.error('init requires a NEW project name')
  if (root/args[0]).exists():p.error('Refusing to overwrite existing project')
  args+=['--non-interactive','--skip-skills']
 result=subprocess.run([str(node),str(cli),a.command,*args],cwd=root,env=env)
 if result.returncode==0 and a.command=='init':
  new=root/args[0]
  studio.write(new/'pipeline.json',{'backend':'hyperframes','version':VERSION,'status':'draft','sevenSourceReleaseRequired':True})
  import integrations
  integrations.bind(new)
  import hf_pipeline
  hf_pipeline.seed(new)
 return result.returncode
if __name__=='__main__':sys.exit(main())
