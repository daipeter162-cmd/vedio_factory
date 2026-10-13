from pathlib import Path
import numpy as np
import wave
root=Path(__file__).resolve().parent;sr=48000;dur=30;n=sr*dur
t=np.arange(n)/sr;audio=np.zeros((n,2),dtype=np.float64)
chords=[[130.8128,164.8138,195.9977],[110,130.8128,164.8138],[87.3071,110,130.8128],[97.9989,123.4708,146.8324],[130.8128,164.8138,195.9977],[110,130.8128,164.8138]]
for j,chord in enumerate(chords):
 start=j*5;end=min(dur,start+7);ix=np.arange(int(start*sr),int(end*sr));tt=ix/sr-start
 env=np.minimum(tt/1.5,1)*np.minimum((end-start-tt)/2,1)
 for k,f in enumerate(chord):
  sig=(np.sin(2*np.pi*f*tt)+.2*np.sin(2*np.pi*2*f*tt))*.027*env
  audio[ix,0]+=sig;audio[ix,1]+=np.sin(2*np.pi*f*tt+.12)*.027*env
 for k in range(7):
  st=start+.8+k*.66;ix=np.arange(int(st*sr),min(n,int((st+3)*sr)));tt=ix/sr-st;f=chord[k%3]*2
  sig=(np.sin(2*np.pi*f*tt)+.18*np.sin(2*np.pi*f*2*tt))*np.exp(-tt*2)*np.minimum(tt/.015,1)*.065
  audio[ix,0]+=sig*(.88 if k%2 else 1);audio[ix,1]+=sig*(1 if k%2 else .88)
fade=np.minimum(t/2,1)*np.minimum((dur-t)/3,1);audio*=fade[:,None]
assert np.max(np.abs(audio))<1
with wave.open(str(root/'ambience.wav'),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((audio*32767).astype('<i2').tobytes())
print('Audio generated',dur,'seconds, peak',np.max(np.abs(audio)))
