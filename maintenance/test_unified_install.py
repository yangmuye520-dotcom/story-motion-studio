"""Installer safety tests: isolated paths, conflict protection and config preservation."""
import argparse,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import install,install_hyperframes as hf
class InstallerTests(unittest.TestCase):
 def test_config_backup_preserves_custom_fields(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'config.json';old={'custom':{'keep':True}};p.write_text(json.dumps(old))
   hf.save_config(p,{**old,'hyperframes':{'version':'0.8.207'}})
   self.assertEqual(json.loads(p.read_text())['custom'],old['custom'])
   backups=list(Path(d).glob('*.before-hyperframes-*'));self.assertEqual(len(backups),1);self.assertEqual(json.loads(backups[0].read_text()),old)
 def test_plan_check_has_no_files_or_network(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   with patch.object(install,'http_bytes',side_effect=AssertionError('network')):
    result=hf.setup(root/'skills',root/'data',root/'cfg',check=True)
   self.assertFalse(result['network']);self.assertEqual(list(root.iterdir()),[])
 def test_existing_official_skill_blocks_fresh_install(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'skills/hyperframes').mkdir(parents=True)
   a=argparse.Namespace(skills_dir=root/'skills',data_dir=root/'data',config=root/'cfg',complete_existing=False)
   with self.assertRaisesRegex(RuntimeError,'NOT be overwritten'):install.plan(a,install.load_lock())
 def test_old_node_rejected_before_install(self):
  with patch.object(hf.shutil,'which',return_value='node'),patch.object(hf.subprocess,'check_output',return_value='v20.0.0'):
   with self.assertRaisesRegex(RuntimeError,'22'):hf.node_tools()
if __name__=='__main__':unittest.main()
