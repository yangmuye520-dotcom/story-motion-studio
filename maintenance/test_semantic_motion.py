"""Regression checks for content routing and cross-shot identity declarations."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from semantic_motion import catalog,suggest,check,compile_actions
class MotionContractTests(unittest.TestCase):
 def test_all_24_routes_and_missing_facts(self):
  self.assertEqual(len(catalog()),24)
  for x in catalog():
   facts={k:True for k in x['requiredFacts']};facts['relation']=x['relation']
   for key in ['inputCount','outputCount','capacity']:
    if key in facts:facts[key]=2
   if x['id']=='split':facts.update(inputCount=1,outputCount=2)
   if x['id']=='merge':facts.update(inputCount=3,outputCount=1)
   if 'values' in facts:facts['values']=[3,7,5]
   self.assertEqual(suggest(facts)['recommended'],x['id'],x['id'])
   for key in x['requiredFacts']:
    bad=copy.deepcopy(facts);bad.pop(key);self.assertIsNone(suggest(bad)['recommended'],(x['id'],key))
 def test_unknown_relation(self):self.assertIsNone(suggest({'relation':'make-it-cool'})['recommended'])
 def test_identity_and_failure_cases(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d).resolve();assert root.is_relative_to(Path(tempfile.gettempdir()).resolve());shots=[]
   for i in range(2):
    selector='#node'+str(i);(root/f's{i}.html').write_text(f'<g id="node{i}" data-object-id="record-a" data-object-state="ready" data-visual-key="record-blue"></g>',encoding='utf-8')
    shots.append({'id':'shot'+str(i),'composition':f's{i}.html','mechanism':{'family':'handoff','contentFacts':{'relation':'stage-transition','resultUsedNext':True},'bindings':{'carrier':selector}},'objectStates':[{'objectId':'record-a','selector':selector,'state':'ready','visualKey':'record-blue','role':'both'}], 'handoff':None if i==0 else {'mode':'continue','transfers':[{'objectId':'record-a','fromSelector':'#node0','toSelector':'#node1','mode':'carry'}]}})
   p={'motionContract':'semantic-motion/v1','objects':[{'id':'record-a','label':'record','sourceRef':'test fixture','carryNext':True}],'shots':shots}
   self.assertTrue(check(root,p,compiled=False)['passed'])
   node=root/'s1.html';original=node.read_text(encoding='utf-8');node.write_text(original.replace('></g>','>changed label</g>'),encoding='utf-8')
   self.assertTrue(any('visible label' in e for e in check(root,p,compiled=False)['errors']));node.write_text(original,encoding='utf-8')
   mutations=[lambda x:x['shots'][1]['handoff'].update(transfers=[]),lambda x:x['shots'][1]['objectStates'][0].update(state='unexpected'),lambda x:x['shots'][1]['objectStates'][0].update(visualKey='wrong-color'),lambda x:x['shots'][1]['mechanism']['bindings'].update(carrier='#missing'),lambda x:x['objects'][0].update(parents=['missing']),lambda x:x['objects'][0].update(parents=['record-a']),lambda x:x['shots'][1]['mechanism'].update(family='merge')]
   for mutate in mutations:
    q=copy.deepcopy(p);mutate(q);self.assertFalse(check(root,q,compiled=False)['passed'])
   q=copy.deepcopy(p);q['shots'][1]['handoff']={'mode':'chapter-break','reason':'next independent topic','transfers':[]};self.assertTrue(check(root,q,compiled=False)['passed'])
   q['shots'][1]['handoff'].pop('reason');self.assertFalse(check(root,q,compiled=False)['passed'])
 def test_compile_and_config_drift(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d).resolve();assert root.is_relative_to(Path(tempfile.gettempdir()).resolve())
   (root/'one.html').write_text('<g id="node" data-object-id="a" data-object-state="ready" data-visual-key="blue">record</g><script>/* motion:one */ /* end-motion:one */</script>',encoding='utf-8')
   p={'motionContract':'semantic-motion/v1','objects':[{'id':'a','label':'a','sourceRef':'test'}],'shots':[{'id':'one','duration':6,'composition':'one.html','mechanism':{'family':'handoff','contentFacts':{'relation':'stage-transition','resultUsedNext':True},'bindings':{'carrier':'#node'},'params':{'from':[0,0],'to':[1,1]}},'objectStates':[{'objectId':'a','selector':'#node','state':'ready','role':'both','visualKey':'blue'}]}]}
   (root/'explanation.json').write_text(json.dumps(p),encoding='utf-8');self.assertFalse(check(root,p)['passed']);compile_actions(root);self.assertTrue(check(root,p)['passed'])
   f=root/'one.html';f.write_text(f.read_text(encoding='utf-8').replace('"to":[1,1]','"to":[2,2]'),encoding='utf-8');self.assertFalse(check(root,p)['passed']);compile_actions(root);self.assertTrue(check(root,p)['passed'])
 def test_old_projects_are_not_silently_migrated(self):self.assertTrue(check(Path('.'),{'shots':[]})['legacy'])
if __name__=='__main__':unittest.main()
