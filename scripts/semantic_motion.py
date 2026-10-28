"""Typed content routing and declared object continuity; not semantic or pixel certification."""
import json,math,re
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent.parent
CONTRACT='semantic-motion/v1'
def catalog():return json.loads((ROOT/'assets/motion-actions-v1/catalog.json').read_text(encoding='utf-8'))['items']
def suggest(facts):
 if not isinstance(facts,dict):return {'recommended':None,'missing':['contentFacts must be an object'],'candidates':[]}
 matches=[x for x in catalog() if x['relation']==facts.get('relation')]
 if not matches:return {'recommended':None,'missing':['Describe a supported knowledge relation, or design a reviewed custom action'],'candidates':[]}
 item=matches[0];missing=[k for k in item['requiredFacts'] if k not in facts or facts[k] in [None,'',[]]]
 for k in ['inputCount','outputCount','capacity']:
  if k in facts and (not isinstance(facts[k],int) or isinstance(facts[k],bool) or facts[k]<1):missing.append(k+' must be a positive integer')
 for k in ['independent','sameBaseline','reversible','sameInput','sameCoordinates','identityPreserved','resultUsedNext']:
  if k in item['requiredFacts'] and facts.get(k) is not True:missing.append(k+' must be true')
 if item['id']=='split' and not (facts.get('inputCount')==1 and isinstance(facts.get('outputCount'),int) and facts['outputCount']>1):missing.append('split needs one input and multiple outputs')
 if item['id']=='merge' and not (isinstance(facts.get('inputCount'),int) and isinstance(facts.get('outputCount'),int) and facts['inputCount']>facts['outputCount']>=1):missing.append('merge needs fewer compatible output groups than inputs')
 if 'values' in item['requiredFacts'] and (not isinstance(facts.get('values'),list) or len(facts['values'])<2 or any(not isinstance(x,(int,float)) or isinstance(x,bool) or not math.isfinite(x) for x in facts['values'])):missing.append('values must contain at least two numbers')
 return {'recommended':None if missing else item['id'],'missing':missing,'candidates':[{'id':item['id'],'reason':item['use'],'watch':item['observe'],'avoid':item['limit']}],'limits':'Codex must infer the relation from source meaning; this helper validates supplied facts, not document truth'}
class Nodes(HTMLParser):
 def __init__(self):super().__init__();self.ids={};self.stack=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);sel='#'+a['id'] if a.get('id') else None
  if sel:self.ids[sel]={**a,'__text':''}
  if tag not in ['meta','link','img','input','br','hr','source']:self.stack.append((tag,sel))
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:self.stack=self.stack[:i];break
 def handle_data(self,data):
  for _,sel in self.stack:
   if sel:self.ids[sel]['__text']+=''.join(data.split())

def action_config(shot):
 a=shot['mechanism'];start=a.get('start',0);duration=a.get('duration',shot['duration'])
 if isinstance(start,bool) or isinstance(duration,bool) or not isinstance(start,(int,float)) or not isinstance(duration,(int,float)) or not math.isfinite(start+duration) or start<0 or duration<=0 or start+duration>shot['duration']+.001:raise ValueError('Action must fit inside its composition')
 return {'type':a['family'],'start':start,'duration':duration,'bindings':a['bindings'],'params':a.get('params',{})}
def action_call(shot):return 'MotionActions.add(tl,'+json.dumps(action_config(shot),ensure_ascii=False,separators=(',',':'),allow_nan=False).replace('<','\\u003c')+');'
def action_pattern(sid):return re.compile(r'/\*\s*motion:'+re.escape(sid)+r'\s*\*/(.*?)/\*\s*end-motion:'+re.escape(sid)+r'\s*\*/',re.S)
def compile_actions(root):
 root=Path(root);p=json.loads((root/'explanation.json').read_text(encoding='utf-8-sig'));report=check(root,p,compiled=False)
 if not report['passed']:raise ValueError(str(report['errors']))
 outputs={}
 for shot in p['shots']:
  f=root/shot['composition'];text=outputs.get(f,f.read_text(encoding='utf-8-sig'));pattern=action_pattern(shot['id'])
  if len(pattern.findall(text))!=1:raise ValueError(shot['id']+': exactly one marked motion block required')
  call=action_call(shot);outputs[f]=pattern.sub(lambda m:'/* motion:'+shot['id']+' */\n'+call+'\n/* end-motion:'+shot['id']+' */',text)
 for f,text in outputs.items():f.write_text(text,encoding='utf-8')
 return {'compiled':len(p['shots']),'files':len(outputs),'source':'explanation.json'}
def check(root,plan,compiled=True):
 errors=[];root=Path(root)
 if not plan.get('motionContract'):return {'passed':True,'legacy':True,'errors':[]}
 if plan['motionContract']!=CONTRACT:return {'passed':False,'errors':['Unknown motion contract']}
 def fail(s):errors.append(s)
 registry={}
 for o in plan.get('objects',[]):
  if not isinstance(o,dict) or not o.get('id'):fail('Object registry needs id');continue
  if o['id'] in registry:fail('Duplicate object: '+o['id'])
  registry[o['id']]=o
  if not o.get('label') or not o.get('sourceRef'):fail(o['id']+': label/sourceRef required')
 if not registry:fail('Declare tracked objects')
 def visit(oid,path):
  if oid in path:fail('Object ancestry cycle: '+oid);return
  for par in registry[oid].get('parents',[]):
   if par not in registry:fail(oid+': unknown parent '+par)
   else:visit(par,path+[oid])
 for oid in registry:visit(oid,[])
 cat={x['id']:x for x in catalog()};previous=None;previous_labels={};seen=set();trace=[]
 for shot in plan.get('shots',[]):
  sid=shot.get('id','?');action=shot.get('mechanism',{});kind=action.get('family');entry=cat.get(kind)
  if not entry:fail(sid+': unknown action family');continue
  decision=suggest(action.get('contentFacts',{}))
  if decision['recommended']!=kind:fail(sid+': action/content mismatch or missing facts: '+str(decision['missing']))
  source=shot.get('composition','');file=(root/source).resolve()
  if not source or not file.is_relative_to(root.resolve()) or not file.is_file():fail(sid+': valid local composition required');continue
  source_text=file.read_text(encoding='utf-8-sig');dom=Nodes();dom.feed(source_text)
  if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',sid):fail(sid+': use a stable ASCII shot id')
  if compiled:
   try:
    blocks=action_pattern(sid).findall(source_text)
    if len(blocks)!=1 or blocks[0].strip()!=action_call(shot):fail(sid+': motion call differs from the shared storyboard; run motion.py compile')
   except (KeyError,TypeError,ValueError) as exc:fail(sid+': invalid action config: '+str(exc))
  binds=action.get('bindings',{})
  if not isinstance(binds,dict):fail(sid+': bindings must be an object');binds={}
  for key in entry['bindings']:
   value=binds.get(key);refs=value if isinstance(value,list) else [value]
   if not refs or any(not isinstance(x,str) or x not in dom.ids for x in refs):fail(sid+': missing actual binding '+key)
  states=shot.get('objectStates',[]);lookup={}
  if not isinstance(states,list):fail(sid+': objectStates must be a list');states=[]
  if not states:fail(sid+': objectStates required')
  for st in states:
   if not isinstance(st,dict):fail(sid+': invalid object state');continue
   oid=st.get('objectId');selector=st.get('selector');role=st.get('role');key=(oid,selector)
   if key in lookup:fail(sid+': duplicate object state binding')
   lookup[key]=st
   if oid not in registry:fail(sid+': unregistered object '+str(oid));continue
   if role not in ['input','output','both']:fail(sid+': invalid object role')
   attrs=dom.ids.get(selector,{})
   if attrs.get('data-object-id')!=oid:fail(sid+': HTML object identity differs: '+str(selector))
   if not st.get('state') or attrs.get('data-object-state')!=st.get('state'):fail(sid+': HTML state differs: '+str(selector))
   if not st.get('visualKey') or attrs.get('data-visual-key')!=st.get('visualKey'):fail(sid+': visual identity marker differs: '+str(selector))
   parents=registry[oid].get('parents',[])
   if oid not in seen and parents and not all(p in seen or any(v.get('objectId')==p for v in states) for p in parents):fail(sid+': derived object appears before its source')
   seen.add(oid)
  hand=shot.get('handoff') or {};transfers=hand.get('transfers',[])
  if previous:
   if hand.get('mode')=='chapter-break':
    if not hand.get('reason') or transfers:fail(sid+': chapter break needs reason and no pretend transfers')
   else:
    if hand.get('mode')!='continue' or not transfers:fail(sid+': declare object transfers or an explicit chapter break')
    previous_states={(v.get('objectId'),v.get('selector')):v for v in previous.get('objectStates',[])}
    covered=set()
    for tr in transfers:
     oid=tr.get('objectId');a=previous_states.get((oid,tr.get('fromSelector')));b=lookup.get((oid,tr.get('toSelector')))
     if not a or not b:fail(sid+': transfer has no matching source/destination');continue
     covered.add(oid)
     if a.get('role') not in ['output','both'] or b.get('role') not in ['input','both']:fail(sid+': handoff roles must be output to input')
     if tr.get('mode')=='carry':
      if previous_labels.get(tr.get('fromSelector'),'')!=dom.ids.get(tr.get('toSelector'),{}).get('__text',''):fail(sid+': visible label changes across carry without explanation')
      if a.get('state')!=b.get('state') or a.get('visualKey')!=b.get('visualKey'):fail(sid+': unexplained state/visual change in carry')
     elif tr.get('mode')=='change':
      if not tr.get('reason'):fail(sid+': changed handoff needs a reason')
     else:fail(sid+': transfer mode must be carry or change')
    required={v.get('objectId') for v in previous.get('objectStates',[]) if registry.get(v.get('objectId'),{}).get('carryNext') and v.get('role') in ['output','both']}
    if required-covered:fail(sid+': tracked output disappears: '+str(sorted(required-covered)))
  trace.append({'shot':sid,'action':kind,'objects':states,'handoff':hand});previous=shot;previous_labels={k:v.get('__text','') for k,v in dom.ids.items()}
 return {'passed':not errors,'errors':errors,'legacy':False,'trace':trace,'limits':'Checks source-linked declarations and HTML identity markers, not actual pixels, fact accuracy or viewer comprehension'}
