"""Check explicit explanation structure, not truth, taste or audience comprehension."""
import argparse,json,re,sys
from pathlib import Path

def check(root):
 errors=[];root=Path(root)
 try:plan=json.loads((root/'explanation.json').read_text(encoding='utf-8-sig'))
 except (OSError,ValueError) as e:return {'structurePassed':False,'errors':[str(e)],'comprehension':'unverified'}
 for key in ['audience','question','takeaway','carrier']:
  if not isinstance(plan.get(key),str) or not plan[key].strip():errors.append('Missing '+key)
 html='\n'.join(p.read_text(encoding='utf-8-sig') for p in root.rglob('*.html') if not any(x in p.parts for x in ['node_modules','.hyperframes']))
 ids=set(re.findall(r'\bid=[\"\x27]([^\"\x27]+)',html));last=0;previous=None
 shots=plan.get('shots',[])
 if not shots:errors.append('No shots')
 for shot in shots:
  label=str(shot.get('id','?'));prefix=label+': '
  for key in ['claim','before','action','after','meaning','object','outObject']:
   if not isinstance(shot.get(key),str) or not shot[key].strip():errors.append(prefix+'missing '+key)
  try:
   start=float(shot['start']);duration=float(shot['duration']);visible=float(shot['visibleSeconds'])
   if abs(start-last)>.02 or duration<=0:errors.append(prefix+'gap, overlap or invalid duration')
   if not 0<visible<=duration:errors.append(prefix+'invalid visibleSeconds')
   claim=shot.get('claim','');units=len(re.findall(r'[\u3400-\u9fff]',claim))+2*len(re.findall(r'[A-Za-z0-9]+',claim))
   if visible<.5+units/4.5:errors.append(prefix+'reading budget too short')
   last=start+duration
   focus=shot.get('focus',[]);end=start
   if not focus:errors.append(prefix+'no primary focus')
   for event in focus:
    fs=float(event['start']);fe=float(event['end'])
    if fs<end-.02 or fs<start or fe>last or fe<=fs:errors.append(prefix+'invalid/overlapping primary focus')
    if event.get('change') not in ['mechanism','comparison','transformation','evidence']:errors.append(prefix+'motion must explain content')
    end=fe
  except (KeyError,ValueError,TypeError):errors.append(prefix+'invalid timing')
  if shot.get('before')==shot.get('after'):errors.append(prefix+'no state change')
  selectors=shot.get('implementation',[])
  if not selectors:errors.append(prefix+'no implementation anchor')
  for selector in selectors:
   if not isinstance(selector,str) or not selector.startswith('#') or selector[1:] not in ids:errors.append(prefix+'missing HTML id '+str(selector))
  if previous:
   hand=shot.get('handoff') or {}
   if hand.get('fromObject')!=previous.get('outObject') or hand.get('toObject')!=shot.get('object') or not hand.get('relation'):errors.append(prefix+'missing causal/object handoff')
  previous=shot
 try:
  if abs(last-float(plan['duration']))>.02:errors.append('Duration does not match shots')
 except (KeyError,ValueError,TypeError):errors.append('Invalid total duration')
 return {'structurePassed':not errors,'errors':errors,'comprehension':'unverified','limits':'Checks declarations, timing and HTML anchors; actual motion, facts and comprehension require separate review'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('project',type=Path);a=p.parse_args();r=check(a.project);print(json.dumps(r,ensure_ascii=False,indent=2));sys.exit(0 if r['structurePassed'] else 2)
