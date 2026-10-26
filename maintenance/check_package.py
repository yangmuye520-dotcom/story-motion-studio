"""Read-only package navigation and resource checks, not a film quality audit."""
import argparse,hashlib,json,re,sys
from pathlib import Path
from urllib.parse import unquote,urlsplit

def check(root):
 errors=[];counts={'markdownLinks':0,'stylePacks':0,'exampleItems':0,'galleryLinks':0}
 def need(path,label):
  if not path.is_file():errors.append(label+': '+str(path.relative_to(root) if path.is_relative_to(root) else path))
 for name in ['README.md','SKILL.md','agents/openai.yaml','scripts/studio.py','scripts/integrations.py','scripts/samples.py','scripts/music.py','assets/starter/index.html','assets/starter/film.json','assets/styles/catalog.json','examples/catalog.json','docs/setup.md','docs/editing.md','docs/structure.md']:
  need(root/name,'missing entry')
 docs=[root/'README.md',root/'SKILL.md',*sorted((root/'docs').glob('*.md')),*sorted((root/'references').glob('*.md'))]
 for f in docs:
  if not f.is_file():continue
  value=f.read_text(encoding='utf-8-sig');value=re.sub(r'```.*?```','',value,flags=re.S)
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',value):
   if urlsplit(target).scheme or target.startswith('#'):continue
   target=unquote(target.split('#')[0].split('?')[0]);counts['markdownLinks']+=1
   if not (f.parent/target).resolve().exists():errors.append('broken markdown link: '+str(f.relative_to(root))+' -> '+target)
 styles=root/'assets/styles/catalog.json'
 if styles.is_file():
  for item in json.loads(styles.read_text(encoding='utf-8'))['items']:
   counts['stylePacks']+=1;d=styles.parent/item['folder']
   for name in ['profile.json','style.json','style-baseline.json','components.js','index.html','motion-reference.js']:need(d/name,'style resource missing')
   if (d/'profile.json').is_file():
    info=json.loads((d/'profile.json').read_text(encoding='utf-8'))
    for key in ['sampleProject','preview','implementation']:
     if not (d/info[key]).resolve().exists():errors.append('broken style profile: '+item['id']+'/'+key)
   if (d/'style-baseline.json').is_file():
    lock=json.loads((d/'style-baseline.json').read_text(encoding='utf-8'))
    for rel,expected in lock['files'].items():
     fp=d/rel
     if not fp.is_file() or hashlib.sha256(fp.read_bytes()).hexdigest()!=expected:errors.append('style baseline mismatch: '+item['id']+'/'+rel)
   need(root/'examples'/item['approvedSample']/'preview.mp4','approved style preview missing')
 cat=root/'examples/catalog.json'
 if cat.is_file():
  data=json.loads(cat.read_text(encoding='utf-8'))
  for item in data['items']:
   counts['exampleItems']+=1
   if item['status'] not in ['candidate','approved','rejected']:errors.append('unknown example status: '+item['id'])
   d=root/'examples'/item['folder']
   for name in ['preview.mp4','poster.png','index.html','scenes.js','sample.json']:need(d/name,'example resource missing')
 for f in [root/'examples/index.html',root/'examples/compare.html']:
  if not f.is_file():continue
  for target in re.findall(r'(?:href|src)="([^"]+)"',f.read_text(encoding='utf-8')):
   if urlsplit(target).scheme or target.startswith('#'):continue
   target=unquote(target.split('#')[0].split('?')[0]);counts['galleryLinks']+=1
   if not (f.parent/target).resolve().exists():errors.append('broken gallery link: '+f.name+' -> '+target)
 return {'passed':not errors,'counts':counts,'errors':errors,'limits':'Navigation, resource presence and style hashes only; no video rendering, full watching, listening or upstream execution certification'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent);a=p.parse_args();result=check(a.root.resolve());print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':sys.exit(main())
