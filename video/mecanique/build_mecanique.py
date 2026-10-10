# -*- coding: utf-8 -*-
"""Usage : python3 build_mecanique.py <dossier_modèles|-> <dossier_sortie> [--est]
Deux passes : (1) voix Kokoro par cue -> durées ; (2) génération du HTML avec les instants absolus + effets sonores."""
import sys,os,re,json,math
import numpy as np
models,out=sys.argv[1],sys.argv[2]; EST='--est' in sys.argv
os.makedirs(out,exist_ok=True)
here=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,here)
import lib, spec_mecanique as sp
from lib import voice
SPEED=1.0; PRE,GAP,POST=.7,.45,.9
cues=[]  # (scene index, sub, voice text)
for si,sc in enumerate(sp.SC):
    for sub,vo in sc['cues']:
        v=voice(vo or sub); assert not re.search(r'\bMe\b',v),v
        cues.append((si,sub,v))
# audit : "notaire" sans nom
bad=[sub for _,sub,_ in cues if re.search(r'\bnotaire\b(?! Félix)',sub)]
print('mentions « notaire » sans nom :',len(bad),bad[:3])
wavs=[];sr=24000
if not EST:
    from kokoro_onnx import Kokoro
    import soundfile as sf
    k=Kokoro(os.path.join(models,'kokoro.onnx'),os.path.join(models,'voices.bin'))
    def chunk(text,maxc=165):
        o=[];cur=''
        for ph in re.split(r'(?<=[.!?:])\s+',text):
            if cur and len(cur)+1+len(ph)>maxc: o.append(cur); cur=ph
            else: cur=(cur+' '+ph).strip()
        return o+[cur]
    import hashlib
    os.makedirs(os.path.join(out,'cache'),exist_ok=True)
    def synth(p):
        h=os.path.join(out,'cache',hashlib.md5((p+str(SPEED)).encode()).hexdigest()+'.npy')
        if os.path.exists(h): return np.load(h)
        x,_=k.create(p,voice='ff_siwis',speed=SPEED,lang='fr-fr'); np.save(h,x); return x
    for _,_,v in cues:
        parts=[]
        for p in chunk(v):
            parts.append(synth(p))
        gap=np.zeros(int(.25*sr),dtype=np.float32)
        w=parts[0]
        for p in parts[1:]: w=np.concatenate([w,gap,p])
        wavs.append(w.astype(np.float32))
    durs=[len(w)/sr for w in wavs]
else:
    durs=[len(v)/15.0+.3 for _,_,v in cues]
# timeline
t=0.0;T=[];ci=0;timeline=[]
for si,sc in enumerate(sp.SC):
    s=t;c=s+(sc.get('pre') or PRE);cs=[];ce=[]
    for _ in sc['cues']:
        cs.append(c);ce.append(c+durs[ci]);timeline.append((c,c+durs[ci],cues[ci][1],ci));c+=durs[ci]+GAP;ci+=1
    end=max(c-GAP+(1.8 if si==len(sp.SC)-1 else POST),s+sc['minlen'])
    T.append(dict(s=s,e=end,c=cs,ce=ce,fx=[]));t=end
total=t
body=''
for sc,Tt in zip(sp.SC,T):
    body+=lib.scene(sc['id'],sc['tag'],sc['bg'],Tt,sc['build'](Tt))
CUES=[[round(a,3),round(b,3),sub] for a,b,sub,_ in timeline]
html=lib.CSS+body+'<div id="sub"></div><div id="bar"></div></div>\n<script>\nconst CUES='+json.dumps(CUES,ensure_ascii=False)+f';\nconst DUR={total:.3f};\n'+lib.JS+'</script></body></html>'
open(os.path.join(here,'motion-voix.html'),'w',encoding='utf-8').write(html)
json.dump({'total':total,'scenes':[(sc['id'],round(x['s'],2),round(x['e'],2)) for sc,x in zip(sp.SC,T)],'cues':CUES},open(os.path.join(out,'timeline.json'),'w'),ensure_ascii=False)
print('durée',round(total,1),'s =',round(total/60,1),'min ; scènes',len(T),'; cues',len(CUES))
if EST: sys.exit(0)
# piste audio : voix + effets
track=np.zeros(int((total+2)*sr),dtype=np.float32)
for (a,b,_,i) in timeline:
    w=wavs[i];st=int(a*sr);track[st:st+len(w)]+=w
rng=np.random.default_rng(7)
def add(at,x,g=1.0):
    st=int(at*sr);x=(x*g).astype(np.float32);track[st:st+len(x)]+=x[:max(0,len(track)-st)]
def env(n,tau): return np.exp(-np.arange(n)/(tau*sr))
def thump(f=55,dur=.5,tau=.11):
    n=int(dur*sr);tt=np.arange(n)/sr;x=np.sin(2*np.pi*f*tt)*env(n,tau);x[:int(.006*sr)]*=np.linspace(0,1,int(.006*sr));return x
def click():
    n=int(.12*sr);tt=np.arange(n)/sr;nz=rng.standard_normal(n)*env(n,.012);return .6*nz+.5*np.sin(2*np.pi*230*tt)*env(n,.03)
for T_ in T:
    for kind,at in T_['fx']:
        if kind=='heart': add(at,thump(),.9);add(at+.36,thump(48,.5,.14),.7)
        elif kind=='click': add(at,click(),.5);add(at+.09,click(),.3)
        elif kind=='thud': add(at,thump(70,.4,.09),.7);add(at,click(),.25)
        elif kind=='unlock': add(at,click(),.5);add(at+.35,thump(90,.5,.12),.4)
peak=np.max(np.abs(track));
if peak>.97: track*=.97/peak
sf.write(os.path.join(out,'voix.wav'),track,sr)
print('wav ok')
