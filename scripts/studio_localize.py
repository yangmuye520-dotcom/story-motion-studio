"""Apply the bundled Chinese Studio UI patch to the configured, pinned runtime."""
import argparse,hashlib,json,re,shutil
from pathlib import Path
import studio

def apply():
 cfg=studio.configure_runtime();cli=Path(cfg.get('hyperframes',{}).get('cli',''));package=cli.parent.parent
 assert cli.is_file(),'Configure HyperFrames runtime first'
 assert studio.read(package/'package.json')['version']=='0.8.207','Review UI patch compatibility before upgrading'
 assets=Path(__file__).resolve().parent.parent/'assets/studio-zh'
 target=package/'dist/studio';entry=target/'index.html';backup=package.parent/'.story-motion-ui-backup/0.8.207';backup.mkdir(parents=True,exist_ok=True)
 if not (backup/'index.html').exists():shutil.copy2(entry,backup/'index.html')
 pairs={line.split('|',1)[0]:line.split('|',1)[1] for line in (assets/'labels.txt').read_text(encoding='utf-8').splitlines() if '|' in line}
 js=(assets/'overlay.js').read_text(encoding='utf-8').replace('__DICTIONARY__',json.dumps(pairs,ensure_ascii=False))
 css=(assets/'style.css').read_text(encoding='utf-8')
 for name,text in [('studio-zh.js',js),('studio-zh.css',css)]:
  dest=target/'assets'/name
  if not dest.exists() or dest.read_text(encoding='utf-8')!=text:dest.write_text(text,encoding='utf-8')
 text=entry.read_text(encoding='utf-8').replace('<html lang="en">','<html lang="zh-CN">').replace('<title>HyperFrames Studio</title>','<title>HyperFrames 中文工作台</title>')
 if '/assets/studio-zh.js' not in text:text=text.replace('</head>','<script defer src="/assets/studio-zh.js?v=1"></script>\n<link rel="stylesheet" href="/assets/studio-zh.css?v=1">\n</head>')
 for name,body in [('studio-zh.js',js),('studio-zh.css',css)]:text=re.sub('/assets/'+re.escape(name)+r'\?v=[^"\s]+','/assets/'+name+'?v='+hashlib.sha256(body.encode()).hexdigest()[:10],text)
 if text!=entry.read_text(encoding='utf-8'):entry.write_text(text,encoding='utf-8')
 return {'language':'zh-CN','version':'0.8.207','entries':len(pairs),'backup':str(backup),'projectFilesChanged':False,'limits':'Unmapped third-party diagnostics keep original details; this is a local UI overlay'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.parse_args();print(json.dumps(apply(),ensure_ascii=False,indent=2))
