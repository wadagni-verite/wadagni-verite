"""Génère la voix-off (Kokoro, voix française ff_siwis) et une version de la vidéo calée dessus.
Prérequis : pip install kokoro-onnx soundfile ; fichiers kokoro-v1.0.int8.onnx et voices-v1.0.bin
(téléchargeables depuis github.com/thewh1teagle/kokoro-onnx, release model-files-v1.0).
Usage : python3 build_voix.py <dossier_modèles> <dossier_sortie>"""
import re, sys, json, os, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
models, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
SPEED=1.1
src=open(os.path.join(os.path.dirname(__file__),'..','motion.html'),encoding='utf-8').read()
cues=[(float(a),float(b),s) for a,b,s in re.findall(r'\[([\d.]+),([\d.]+),"(.*?)"\]',src)]
k=Kokoro(os.path.join(models,'kokoro.onnx'),os.path.join(models,'voices.bin'))
def chunk(text,maxc=165):
    out=[];cur=''
    for ph in re.split(r'(?<=[.!?])\s+',text):
        if cur and len(cur)+1+len(ph)>maxc: out.append(cur); cur=ph
        else: cur=(cur+' '+ph).strip()
    return out+[cur]
segs=[];seg_of=[]
for a,b,s_ in cues:
    parts=chunk(s_); seg_of.append(list(range(len(segs),len(segs)+len(parts)))); segs+=parts
wav=[]
for s_ in segs:
    x,sr=k.create(s_,voice='ff_siwis',speed=SPEED,lang='fr-fr'); wav.append(x)
# scènes d'origine (début, fin) et cues qu'elles contiennent
old=[(0,11),(11,31),(31,50),(50,64),(64,84),(84,98),(98,118),(118,127)]
groups=[[0],[1,2],[3,4],[5,6],[7,8],[9,10],[11,12],[13]]
groups=[[j for i in g for j in seg_of[i]] for g in groups]
PRE,GAP,POST=0.7,0.4,0.9
t=0.0; scenes=[]; newcues=[None]*len(segs)
for gi,g in enumerate(groups):
    s0=t; c=s0+PRE
    for ci in g:
        d=len(wav[ci])/sr; newcues[ci]=(c,c+d,segs[ci]); c+=d+GAP
    end=c-GAP+(1.6 if gi==len(groups)-1 else POST)
    scenes.append((old[gi][0],old[gi][1],s0,end)); t=end
total=t
track=np.zeros(int((total+1)*sr),dtype=np.float32)
for i,(a,b,s) in enumerate(newcues):
    x=wav[i].astype(np.float32); st=int(a*sr); track[st:st+len(x)]+=x
sf.write(os.path.join(out,'voix.wav'),track,sr)
json.dump({'scenes':scenes,'cues':newcues,'total':total},open(os.path.join(out,'timeline.json'),'w'),ensure_ascii=False)
# page de rendu : mêmes visuels, temps déformé scène par scène, sous-titres sur le temps réel
js=f"""
const NEWSC={json.dumps(scenes)}, NEWCUES={json.dumps(newcues,ensure_ascii=False)}, NEWDUR={total};
const _seekOld=window.seek;
window.seek=function(t){{
  let tau=0; for(const [o0,o1,n0,n1] of NEWSC){{ if(t>=n0&&t<n1){{tau=o0+(t-n0)/(n1-n0)*(o1-o0);break;}} if(t>=n1) tau=o1; }}
  _seekOld(tau);
  const c=NEWCUES.find(c=>t>=c[0]&&t<c[1]+0.3), sub=document.getElementById('sub'), bar=document.getElementById('bar');
  sub.textContent=c?c[2]:''; sub.style.opacity=c?1:0; bar.style.width=(t/NEWDUR*1280)+'px';
}};
window.DUR=NEWDUR; window.CUES=NEWCUES.map(c=>[c[0],c[1],c[2]]); seek(0);
"""
html=src.replace('</script></body></html>', js+'</script></body></html>')
assert html!=src
open(os.path.join(os.path.dirname(__file__),'motion-voix.html'),'w',encoding='utf-8').write(html)
print('durée totale',round(total,1),'s')
