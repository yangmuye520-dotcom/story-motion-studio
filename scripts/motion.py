"""Routing, generated call blocks and object trace; the storyboard stays authoritative."""
import argparse,json,sys
from pathlib import Path
from semantic_motion import suggest,check,catalog,ROOT,compile_actions
p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
s=sub.add_parser('suggest');s.add_argument('facts',type=Path)
s=sub.add_parser('trace');s.add_argument('project',type=Path)
s=sub.add_parser('example');s.add_argument('id',choices=[x['id'] for x in catalog()])
s=sub.add_parser('compile');s.add_argument('project',type=Path)
sub.add_parser('catalog');a=p.parse_args()
if a.command=='suggest':r=suggest(json.loads(a.facts.read_text(encoding='utf-8-sig')));ok=r['recommended'] is not None
elif a.command=='trace':r=check(a.project,json.loads((a.project/'explanation.json').read_text(encoding='utf-8-sig')));ok=r['passed']
elif a.command=='compile':r=compile_actions(a.project);ok=True
elif a.command=='example':
 item=next(x for x in catalog() if x['id']==a.id);r={'config':item['exampleConfig'],'html':(ROOT/'assets/motion-actions-v1'/item['exampleFile']).read_text(encoding='utf-8'),'limits':'Wiring example only; replace generic content, bind tracked objects and author the shot before production'};ok=True
else:r=catalog();ok=True
print(json.dumps(r,ensure_ascii=False,indent=2));sys.exit(0 if ok else 2)
