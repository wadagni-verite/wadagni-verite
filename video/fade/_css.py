CSS = '''
:root{--navy:#0a1f44;--gold:#d4af37;--ink:#f8fafc;--mute:#94a3b8}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:#050d1f;font-family:'DejaVu Sans',sans-serif;color:var(--ink)}
#stage{position:relative;width:1920px;height:1080px;background:radial-gradient(ellipse at 30% 20%,#12306b 0%,#0a1f44 45%,#050d1f 100%)}
.el{position:absolute;opacity:0}
.title{font-family:'DejaVu Serif',serif;font-size:100px;line-height:1.15;font-weight:700}
.subtitle{font-family:'DejaVu Serif',serif;font-size:44px;color:var(--gold);font-style:italic}
.colhead{font-size:30px;letter-spacing:.1em;color:var(--gold);text-transform:uppercase}.colhead.wide{text-align:center}
.vbar{width:2px;background:rgba(199,210,254,.5)}
.attente{font-size:90px;color:var(--mute);text-align:center}
.card{width:230px;text-align:center;background:rgba(255,255,255,.07);border:3px solid var(--gold);border-radius:16px;padding:12px 8px}
.card .dd{font-size:72px;font-weight:800;line-height:1.0}.card .mm{font-size:30px;letter-spacing:.08em;color:var(--gold);margin-top:4px}.card .yy{font-size:28px;color:var(--mute)}.card .lb{font-size:22px;color:#e2e8f0;margin-top:8px;line-height:1.2}
.card.sm{width:250px}
.card.big{width:420px;padding:30px 10px}.card.big .dd{font-size:180px}.card.big .mm{font-size:60px}.card.big .yy{font-size:56px}
.pic{position:relative;background:#fff;border:4px solid var(--gold);border-radius:6px;overflow:hidden;box-shadow:0 14px 40px rgba(0,0,0,.6)}
.pic img{display:block;width:100%}
.hl{position:absolute;background:rgba(212,175,55,.35);border:2px solid rgba(212,175,55,.9)}
.cap{font-size:21px;line-height:1.3;color:var(--mute);margin-top:10px}.cap2{font-size:22px;color:var(--mute)}
.counter{font-weight:800;color:var(--gold);text-align:center;white-space:nowrap}
.counter .cu{font-size:56px;margin-left:20px;color:#fff;font-weight:600;letter-spacing:.06em}
.csub{font-size:26px;color:#cbd5e1;font-weight:400;white-space:normal;margin-top:6px}
.quote{font-family:'DejaVu Serif',serif;font-size:34px;line-height:1.3;background:rgba(255,255,255,.07);border-left:6px solid var(--gold);padding:14px 22px}
.quote.wide{font-size:30px}
.num{color:var(--gold);font-weight:700}
.ocre{color:var(--gold)}
.ocrebox{border-left-color:#ef4444}
.ctext{font-size:28px;line-height:1.4;color:#e2e8f0}.ctext.small{font-size:24px;color:var(--mute)}
.nm{font-size:34px;font-family:'DejaVu Serif',serif;padding:8px 14px;background:rgba(255,255,255,.07);border-left:6px solid var(--gold)}
.trait{position:absolute;height:4px;background:var(--gold);transform-origin:left}
.grow{transform-origin:left}
.vide{border:4px dashed rgba(199,210,254,.6);color:var(--mute);font-size:38px;display:flex;align-items:center;justify-content:center;text-align:center;padding:30px}
.date3{font-family:'DejaVu Serif',serif;font-size:44px;font-weight:700;text-align:center;line-height:1.2}.date3 small{font-size:24px;font-weight:400;color:var(--mute);font-family:'DejaVu Sans'}
.date3.vide{border:4px dashed rgba(199,210,254,.6);padding:10px;font-size:90px;color:var(--gold)}.date3.vide small{color:#cbd5e1}
.frl2{height:3px;background:#c7d2fe}
.ocretext{color:#d4af37}\n.vide2{border:4px dashed rgba(199,210,254,.6);color:#e2e8f0;font-size:30px;text-align:center;padding:22px;line-height:1.4}.vide2 b{color:#d4af37}
.mail{background:#fff;color:#111;border:4px solid var(--gold);border-radius:6px;padding:20px 26px;font-size:23px;line-height:1.4;box-shadow:0 14px 40px rgba(0,0,0,.6)}.mail .mh{font-weight:700;font-size:22px;display:flex;justify-content:space-between;border-bottom:1px solid #ccc;padding-bottom:8px;margin-bottom:10px}.mail .mh span{font-weight:400;color:#666}.mail .ms{font-size:34px;font-weight:800;margin:10px 0 14px}.mail p{margin:0 0 12px}.mail .rep{background:#eef2ff;border-left:5px solid #4f46e5;padding:10px 14px;margin-top:10px}
.qa{font:800 130px DejaVu Serif,serif;color:#ef4444;letter-spacing:.04em}.bigq{font-family:'DejaVu Serif',serif;font-size:44px;line-height:1.3}
.bigtext{font-family:'DejaVu Serif',serif;font-size:42px;line-height:1.3;font-weight:700}
.quest{font-family:'DejaVu Serif',serif;font-size:40px;line-height:1.25}
.url{font-size:64px;text-align:center;font-family:'DejaVu Serif',serif;color:#fff}.finsmall{font-size:30px;text-align:center;color:var(--mute)}
.precis{font-size:24px;line-height:1.6;color:#cbd5e1}
.bandeau{left:0;bottom:0;width:1920px;height:88px;background:rgba(0,0,0,.7);color:#fff;font-size:26px;line-height:1.3;padding:12px 60px;z-index:50}
.trow{min-height:128px;align-items:start;display:grid;grid-template-columns:250px 1fr 230px;gap:18px;font-size:24px;line-height:1.3;background:rgba(255,255,255,.07);border-left:6px solid var(--gold);padding:12px 16px}.trow.thead{background:none;border:0;font-size:20px;letter-spacing:.08em;color:var(--gold);padding-top:0;padding-bottom:0}\n.title2{font-family:'DejaVu Serif',serif;font-size:56px;line-height:1.25;font-weight:700}\n.kf{position:absolute;left:0;top:0;transform-origin:0 0}\n.gap{text-align:center;font-size:20px;white-space:nowrap}\n.date3.ret{border:4px solid var(--gold);padding:14px;color:var(--gold)}\n.p6,.p4,.p5,.p7,.p3{}\nbody.fin #stage{background:#000}
'''
JS = '''
const ELS=[...document.querySelectorAll('.el')],CNS=[...document.querySelectorAll('.cn')],KFS=[...document.querySelectorAll('.kf')],PUL=[...document.querySelectorAll('.pulse')];
KFS.forEach(k=>{k._k=JSON.parse(k.dataset.k)});
const cl=x=>Math.max(0,Math.min(1,x));
window.TOTAL=%.2f;
window.seek=function(t){
  for(const e of ELS){const a=+e.dataset.a,b=+e.dataset.b,f=+e.dataset.f;const i=cl((t-a)/f);
    e.style.opacity=i*cl((b-t)/f);
    if(e.classList.contains('trait')){e.style.transform=`scaleX(${cl((t-a)/1.0)})`;}
    else if(e.classList.contains('card')||e.classList.contains('piece')) e.style.transform=`translateY(${(1-i)*14}px)`;}
  for(const k of KFS){const K=k._k;let i=0;while(i<K.length-1&&t>=K[i+1][0])i++;
    const A=K[i],B=K[Math.min(i+1,K.length-1)];const u=B[0]>A[0]?cl((t-A[0])/(B[0]-A[0])):0;
    const g=(r,j,d)=>{const x=r[j]===undefined?d:r[j];return x};
    const L=(j,d)=>g(A,j,d)+(g(B,j,d)-g(A,j,d))*u;
    const s=L(3,1);k.style.transform=`translate(${L(1,0)}px,${L(2,0)}px) scale(${s},${A[5]===undefined&&B[5]===undefined?s:L(5,s)})`;k.style.opacity=L(4,1);}
  for(const p of PUL){p.style.opacity=.35+.4*Math.abs(Math.sin(t*4.5));}
  for(const c of CNS){const a=+c.dataset.ca,b=+c.dataset.cb,to=+c.dataset.to;c.textContent=Math.round(to*cl((t-a)/(b-a)));}
  document.body.classList.toggle('fin',t>=%.2f);
};
seek(0);
''' % (TOTAL, SQ[16][0] - 0.3)
html = f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Où est l'acte ?</title><style>{CSS}</style></head><body><div id="stage">\n' + '\n'.join(EL) + f'\n</div><script>{JS}</script></body></html>'
open(os.path.join(here, 'motion.html'), 'w', encoding='utf-8').write(html)
json.dump({'total': TOTAL, 'sequences': {str(k_): v for k_, v in SQ.items()}, 'cues': cues}, open(os.path.join(out, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
print('durée totale', round(TOTAL, 1), 's ; séquences', {k_: (round(a_, 1), round(b_, 1)) for k_, (a_, b_) in SQ.items()})

