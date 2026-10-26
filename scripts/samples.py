"""Local example library with actual previews, projects, provenance and approval history."""
import argparse,html,json,shutil,sys,webbrowser,subprocess
from pathlib import Path
from studio import read,write,digest,configure_runtime,ffmpeg
from integrations import check
def lib_path(value=None):return Path(value).resolve() if value else Path(__file__).resolve().parent.parent/'examples'
def catalog(lib):
 if not (lib/'catalog.json').exists():write(lib/'catalog.json',{'schema':'story-motion-examples/v2','items':[],'history':[]})
 return read(lib/'catalog.json')
def gallery(lib):
 c=catalog(lib);cards=[]
 for i in sorted(c['items'],key=lambda item: {'candidate':0,'approved':1,'rejected':2}[item['status']]):
  folder=i['folder'];status={'candidate':'待选样例','approved':'已认可样板','rejected':'已否定样例'}[i['status']]
  cards.append(f'''<article data-status="{i['status']}"><video controls preload="metadata" poster="{folder}/poster.png" src="{folder}/preview.mp4"></video><section><small>{status} · {html.escape(i['category'])}</small><h2>{html.escape(i['title'])}</h2><p>{html.escape(i['description'])}</p><p class="note">{html.escape(i['limits'])}</p><a href="{folder}/index.html">打开动画工程</a><a href="{folder}/sample.json">来源与七项采用记录</a><a href="{folder}/scenes.js">画面源码</a></section></article>''')
 body='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>故事动效工坊 · 样例库</title><style>*{box-sizing:border-box}body{margin:0;background:#edeae3;color:#25312f;font:16px system-ui,"Microsoft YaHei",sans-serif}header,main{max-width:1350px;margin:auto;padding:32px}header small{letter-spacing:.15em;color:#496e60}h1{font-size:42px;margin:18px 0}header p{max-width:850px;line-height:1.8}nav{display:flex;gap:12px;flex-wrap:wrap}button{border:1px solid #84988e;border-radius:30px;background:transparent;padding:10px 20px;cursor:pointer;font:inherit}button.active{background:#2b5446;color:white}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:26px;padding-top:0}article{background:#fff;border-radius:18px;overflow:hidden;border:1px solid #d4d9d1}video{display:block;width:100%;background:#e8e6df;aspect-ratio:16/9}section{padding:24px}h2{font-size:23px}p{line-height:1.8}small,.note{color:#68796f}.note{font-size:13px}a{display:block;margin-top:12px;color:#286650}#empty{padding:32px;display:none}</style><header><small>STORY MOTION STUDIO / EXAMPLE LIBRARY</small><h1>先看效果，再选样板。</h1><p>这里保存可看的视频、可改的源码和七个技能的采用证据。待选不等于认可；只有你明确认可的样板，才用于固定后续风格。技术通过也不等于审美通过。</p><nav><button class="active" data-filter="all">全部样例</button><button data-filter="candidate">待选</button><button data-filter="approved">已认可</button><button data-filter="rejected">已否定</button></nav></header><main>'''+''.join(cards)+'''</main><div id="empty">此分类暂无样例。当前没有推定用户已认可的风格。</div><script>document.querySelectorAll('button').forEach(b=>b.onclick=()=>{document.querySelectorAll('button').forEach(x=>x.classList.remove('active'));b.classList.add('active');let n=0;document.querySelectorAll('article').forEach(x=>{let yes=b.dataset.filter==='all'||x.dataset.status===b.dataset.filter;x.hidden=!yes;if(yes)n++});document.querySelector('#empty').style.display=n?'none':'block'})</script></html>'''
 if (lib/'compare.html').exists():body=body.replace('<nav>','<p><a href="compare.html">原片与新样片对照</a></p><nav>',1)
 (lib/'index.html').write_text(body,encoding='utf-8')
def add(project,lib,sid,title,category,description):
 assert sid and all(c.islower() or c.isdigit() or c=='-' for c in sid),'Use lowercase sample id'
 c=catalog(lib);assert not any(x['id']==sid for x in c['items']),'Sample id exists'
 coverage=check(project,True);video=project/'draft.mp4';assert video.is_file(),'Candidate sample needs a rendered draft'
 render=read(project/'qa/draft-report.json');assert render['draft'] is True and render['fullDecode'] and render['output']=='draft.mp4'
 assert render['outputSha256']==digest(video) and render['sevenSkills']==coverage,'Sample video/contribution binding stale'
 for f,h in render['sourceSha256'].items():assert digest(project/f)==h,'Sample source changed: '+f
 subprocess.run([ffmpeg(),'-v','error','-i',str(video),'-f','null','-'],capture_output=True,check=True)
 folder=Path('candidates')/sid;dst=lib/folder;assert not dst.exists()
 shutil.copytree(project,dst,ignore=shutil.ignore_patterns('__pycache__','*.pyc','draft-silent.mp4','silent.mp4','candidate.mp4','final.mp4','draft.mp4'))
 shutil.copy2(video,dst/'preview.mp4');previews=sorted((project/'previews').glob('*-1.png'));assert previews;shutil.copy2(previews[0],dst/'poster.png')
 info={'id':sid,'title':title,'category':category,'description':description,'status':'candidate','folder':folder.as_posix(),'limits':'原创技术候选；尚未获用户认可，未进行人工完整试听。','videoSha256':digest(video),'sevenSkills':coverage,'contributions':read(project/'integration/contributions.json')['records']}
 write(dst/'sample.json',info);c['items'].append({k:v for k,v in info.items() if k not in ['sevenSkills','contributions']});write(lib/'catalog.json',c);gallery(lib)
def decide(lib,sid,status,evidence):
 assert evidence.strip(),'Real user decision required';c=catalog(lib);i=next(x for x in c['items'] if x['id']==sid)
 assert i['status']=='candidate','Only pending candidate decisions supported; create a new version for later changes'
 before=dict(i)
 if status=='approved':
  src=lib/i['folder'];target=lib/'approved'/(sid+'-v1');assert not target.exists();shutil.copytree(src,target);i['folder']=target.relative_to(lib).as_posix()
 i['status']=status;i['decisionEvidence']=evidence;i['limits']='已记录用户决定；原预览保留制作时的技术候选标记，认可不等于正式成片验收。' if status=='approved' else '已否定，保留作为避免重复采用的记录。'
 c['history'].append({'before':before,'after':dict(i),'toolCannotVerifyHumanConsent':True});write(lib/'catalog.json',c);write(lib/i['folder']/'decision.json',{'status':status,'evidence':evidence})
 info=read(lib/i['folder']/'sample.json');info.update(status=status,decisionEvidence=evidence,limits=i['limits']);write(lib/i['folder']/'sample.json',info);gallery(lib)
def main():
 configure_runtime();p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='cmd',required=True)
 a=s.add_parser('add');a.add_argument('project');a.add_argument('--id',required=True);a.add_argument('--title',required=True);a.add_argument('--category',required=True);a.add_argument('--description',required=True);a.add_argument('--library')
 for name in ['approve','reject']:
  a=s.add_parser(name);a.add_argument('id');a.add_argument('--evidence',required=True);a.add_argument('--library')
 a=s.add_parser('gallery');a.add_argument('--library')
 a=p.parse_args();lib=lib_path(a.library)
 if a.cmd=='add':add(Path(a.project).resolve(),lib,a.id,a.title,a.category,a.description)
 elif a.cmd in ['approve','reject']:decide(lib,a.id,'approved' if a.cmd=='approve' else 'rejected',a.evidence)
 else:gallery(lib);webbrowser.open((lib/'index.html').as_uri())
if __name__=='__main__':
 try:main()
 except Exception as e:print(f'ERROR: {type(e).__name__}: {e}',file=sys.stderr);sys.exit(1)
