"""Régénère motion-voix.html à partir de motion.html et d'un timeline.json existant (sans refaire la voix). Usage : python3 rebuild_html.py <timeline.json>"""
import json,sys,os
here=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(here,'motion.html'),encoding='utf-8').read()
d=json.load(open(sys.argv[1],encoding='utf-8')); scenes=d['scenes']; nc=d['cues']; total=d['total']
js=f"""
const NEWSC={json.dumps(scenes)}, NEWCUES={json.dumps(nc,ensure_ascii=False)}, NEWDUR={total};
const _seekOld=window.seek;
window.seek=function(t){{
  let tau=0; for(const [o0,o1,n0,n1] of NEWSC){{ if(t>=n0&&t<n1){{tau=o0+(t-n0)/(n1-n0)*(o1-o0);break;}} if(t>=n1) tau=o1; }}
  _seekOld(tau);
  const c=NEWCUES.find(c=>t>=c[0]&&t<c[1]+0.3), sub=document.getElementById('sub'), bar=document.getElementById('bar');
  sub.textContent=c?c[2]:''; sub.style.opacity=c?1:0; bar.style.width=(t/NEWDUR*1080)+'px';
}};
window.DUR=NEWDUR; window.CUES=NEWCUES; seek(0);
"""
html=src.replace('</script></body></html>', js+'</script></body></html>'); assert html!=src
open(os.path.join(here,'motion-voix.html'),'w',encoding='utf-8').write(html)
