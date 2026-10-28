"""Copy the approved look and runnable semantic modules into a NEW HF project."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parent.parent
DEFAULT='engineering-2d-v1'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def install(project):
 template=ROOT/'assets/templates'/DEFAULT
 lock=json.loads((template/'template-lock.json').read_text(encoding='utf-8'))
 for rel,value in lock['files'].items():
  assert digest(template/rel)==value,'Bundled template changed: '+rel
 for name in ['assets','compositions']:
  shutil.copytree(template/name,project/name,dirs_exist_ok=True)
 shutil.copy2(template/'index.html',project/'index.html')
 for source,target in [('actions.js','motion-actions.js'),('catalog.json','motion-catalog.json')]:
  shutil.copy2(ROOT/'assets/motion-actions-v1'/source,project/'assets'/target)
 entry=project/'index.html';text=entry.read_text(encoding='utf-8')
 text=text.replace('</head>','<script src="assets/motion-actions.js"></script></head>')
 entry.write_text(text,encoding='utf-8')
 profile=json.loads((template/'profile.json').read_text(encoding='utf-8'))
 (project/'visual-system.json').write_text(json.dumps(profile,ensure_ascii=False,indent=2),encoding='utf-8')
 return profile, {rel:digest(project/rel) for rel in ['assets/engineering-2d.css','assets/mechanism-motion.js','assets/fonts/StudioSans.ttf','assets/motion-actions.js','assets/motion-catalog.json']}
