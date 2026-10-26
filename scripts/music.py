"""Small original deterministic score; not a voice or commercial music service."""
from pathlib import Path
import argparse,json,wave
def main():
 from studio import configure_runtime
 configure_runtime()
 import numpy as np
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('project');p.add_argument('--seconds',type=float,required=True);a=p.parse_args();assert 0<a.seconds<=1800
 root=Path(a.project).resolve();out=root/'audio/music.wav';assert not out.exists(),'Refusing to overwrite; use a new candidate filename/workspace and asset review';out.parent.mkdir(exist_ok=True)
 sr=24000;N=round(a.seconds*sr);track=np.zeros((N,2),np.float32);hz=lambda m:440*2**((m-69)/12)
 def add(at,freq,dur,amp,pan):
  start=round(at*sr);count=min(round(dur*sr),N-start)
  if count<=0:return
  t=np.arange(count)/sr;env=np.minimum(t/.02,1)*np.exp(-t*2.8);s=(np.sin(2*np.pi*freq*t)+.2*np.sin(4*np.pi*freq*t))*env*amp
  track[start:start+count,0]+=s*(.65-pan*.2);track[start:start+count,1]+=s*(.65+pan*.2)
 chords=[[57,60,64],[53,57,60],[48,55,60],[55,59,62]]
 for k in range(int(a.seconds*2)):
  c=chords[(k//8)%4];add(k*.5,hz(c[k%3]+12),1.5,.13,(-1)**k*.6)
  if k%2==0:add(k*.5,hz(c[0]-12),.8,.19,0)
 tt=np.arange(N)/sr;track*=np.minimum(tt,1)[:,None]*np.minimum((a.seconds-tt)/1.5,1)[:,None];peak=float(np.max(np.abs(track)));track*=.65/max(peak,.001)
 with wave.open(str(out),'wb') as w:w.setparams((2,2,sr,0,'NONE','not compressed'));w.writeframes((track*32767).astype('<i2').tobytes())
 (out.parent/'music-origin.json').write_text(json.dumps({'origin':'Original additive synthesis','duration':a.seconds,'sampleRate':sr,'thirdPartyRecording':False,'voice':False,'humanListening':'not performed'},indent=2),encoding='utf-8')
 print(out)
if __name__=='__main__':main()
