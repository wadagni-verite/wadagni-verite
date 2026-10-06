"""Voix-off (Kokoro ff_siwis) pour la vidéo « absence de lien » (analyse Me Balley), calée sur motion.html.
CUES = [début, fin, sous-titre, (texte lu si différent)] : écrire « Maître » (jamais « Me ») dans le texte lu.
Usage : python3 build_voix.py <dossier_modèles> <dossier_sortie>"""
import re, sys, json, os, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
models, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
SPEED=1.1
here=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(here,'motion.html'),encoding='utf-8').read()
cues=[(float(a),float(b),s,v or s) for a,b,s,v in re.findall(r'\[([\d.]+),([\d.]+),"(.*?)"(?:,"(.*?)")?\]',src)]
old=[(float(a),float(b)) for a,b in re.findall(r'data-s="([\d.]+)" data-e="([\d.]+)"',src)]
assert not any(re.search(r'\bMe\b',v) for *_,v in cues), "écrire Maître dans le texte lu"
k=Kokoro(os.path.join(models,'kokoro.onnx'),os.path.join(models,'voices.bin'))
def chunk(text,maxc=165):
    o=[];cur=''
    for ph in re.split(r'(?<=[.!?])\s+',text):
        if cur and len(cur)+1+len(ph)>maxc: o.append(cur); cur=ph
        else: cur=(cur+' '+ph).strip()
    return o+[cur]
segs=[];sub_of=[];seg_of=[]
for a,b,s_,v in cues:
    parts=chunk(v); seg_of.append(list(range(len(segs),len(segs)+len(parts)))); segs+=parts
wav=[]
for s_ in segs:
    x,sr=k.create(s_,voice='ff_siwis',speed=SPEED,lang='fr-fr'); wav.append(x)
# groupes : cues contenues dans chaque scène d'origine
groups=[[i for i,(a,b,_,_) in enumerate(cues) if o0<=a<o1] for o0,o1 in old]
assert sorted(i for g in groups for i in g)==list(range(len(cues)))
PRE,GAP,POST=0.7,0.5,0.9
t=0.0; scenes=[]; newcues=[]
for gi,g in enumerate(groups):
    s0=t; c=s0+PRE
    for ci in g:
        d=sum(len(wav[j])/sr for j in seg_of[ci])+0.25*(len(seg_of[ci])-1)
        newcues.append((ci,c,c+d,cues[ci][2])); c+=d+GAP
    end=c-GAP+(1.8 if gi==len(groups)-1 else POST)
    scenes.append((old[gi][0],old[gi][1],s0,end)); t=end
total=t
track=np.zeros(int((total+1)*sr),dtype=np.float32)
for ci,a,b,_ in newcues:
    c=a
    for j in seg_of[ci]:
        x=wav[j].astype(np.float32); st=int(c*sr); track[st:st+len(x)]+=x; c+=len(x)/sr+0.25
sf.write(os.path.join(out,'voix.wav'),track,sr)
nc=[(a,b,s) for _,a,b,s in newcues]
json.dump({'scenes':scenes,'cues':nc,'total':total},open(os.path.join(out,'timeline.json'),'w'),ensure_ascii=False)
js=f"""
const NEWSC={json.dumps(scenes)}, NEWCUES={json.dumps(nc,ensure_ascii=False)}, NEWDUR={total};
const _seekOld=window.seek;
window.seek=function(t){{
  let tau=0; for(const [o0,o1,n0,n1] of NEWSC){{ if(t>=n0&&t<n1){{tau=o0+(t-n0)/(n1-n0)*(o1-o0);break;}} if(t>=n1) tau=o1; }}
  _seekOld(tau);
  const c=NEWCUES.find(c=>t>=c[0]&&t<c[1]+0.3), sub=document.getElementById('sub'), bar=document.getElementById('bar');
  sub.textContent=c?c[2]:''; sub.style.opacity=c?1:0; bar.style.width=(t/NEWDUR*1280)+'px';
}};
window.DUR=NEWDUR; window.CUES=NEWCUES; seek(0);
"""
html=src.replace('</script></body></html>', js+'</script></body></html>')
assert html!=src
open(os.path.join(here,'motion-voix.html'),'w',encoding='utf-8').write(html)
print('durée totale',round(total,1),'s ; scènes',[(round(a,1),round(b,1)) for _,_,a,b in scenes])
