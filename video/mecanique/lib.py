# -*- coding: utf-8 -*-
"""Bibliothèque de composants pour « La Mécanique de Verrouillage » (16:9, 1280x720).
Chaque élément animé porte data-t (instant absolu d'apparition) ; seek(t) est pur et déterministe."""
import math, re, json
IV='#F5F0E8'; NAVY='#0A1F44'; STONE='#4A4A4A'; RED='#C0392B'; GOLD='#C9A227'; PAPER='#FBF7EE'

CSS='''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>La Mécanique de Verrouillage — wadagni2026-verite.com</title>
<style>
:root{--iv:#F5F0E8;--navy:#0A1F44;--stone:#4A4A4A;--red:#C0392B;--gold:#C9A227;--paper:#FBF7EE}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1280px;height:720px;overflow:hidden;background:#050d1f;font-family:'Liberation Sans','DejaVu Sans',sans-serif}
#stage{position:relative;width:1280px;height:720px;overflow:hidden}
.scene{position:absolute;inset:0;opacity:0}
.bg-iv{background:radial-gradient(ellipse at 30% 15%,#FBF8F0 0%,#F5F0E8 55%,#E9E1D0 100%);color:var(--navy)}
.bg-navy{background:radial-gradient(ellipse at 30% 20%,#14346f 0%,#0A1F44 50%,#050d1f 100%);color:#F5F0E8}
.bg-black{background:#03070f;color:#F5F0E8}
.el{position:absolute;opacity:0}
svg.el,g.el,path.el,circle.el,rect.el,line.el,polygon.el,text.el{position:static}
.svgl{position:absolute;left:0;top:0;width:1280px;height:720px;pointer-events:none}
.tag{position:absolute;left:60px;top:22px;font-family:'Liberation Serif','DejaVu Serif',serif;font-size:22px;letter-spacing:.14em;text-transform:uppercase}
.bg-iv .tag{color:#7a6a3a}.bg-navy .tag,.bg-black .tag{color:var(--gold)}
.serif{font-family:'Liberation Serif','DejaVu Serif',serif}
.paper{background:var(--paper);border:1px solid #CDBF9F;box-shadow:0 8px 22px rgba(10,31,68,.28);color:var(--navy);font-family:'Liberation Serif','DejaVu Serif',serif;padding:14px 18px}
.paper.red{border:3px solid var(--red);color:var(--navy)}
.paper.gold{border:3px solid var(--gold);color:var(--navy)}
.ph{font-family:'Liberation Sans','DejaVu Sans',sans-serif;font-size:15px;letter-spacing:.06em;text-transform:uppercase;color:var(--stone);display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:8px}
.bd{display:inline-block;background:var(--navy);color:#F5F0E8;font-family:'Liberation Sans','DejaVu Sans',sans-serif;font-weight:700;font-size:16px;letter-spacing:.04em;padding:2px 9px;border-radius:4px;white-space:nowrap}
.bd.r{background:var(--red)}.bd.g{background:var(--gold);color:var(--navy)}
.date{font-size:38px;font-weight:700;line-height:1.1}
.qt{font-style:italic;font-size:23px;line-height:1.38}
.xl{font-size:50px;font-weight:700;line-height:1.2}
.lg{font-size:36px;font-weight:700;line-height:1.25}
.md{font-size:26px;line-height:1.35}
.sm{font-size:19px;line-height:1.35}
.red{color:var(--red)}.gold{color:var(--gold)}.stone{color:var(--stone)}.navy{color:var(--navy)}.ivc{color:#F5F0E8}
.center{text-align:center}
.pic{background:#fff;border:2px solid #CDBF9F;box-shadow:0 6px 16px rgba(0,0,0,.3);overflow:hidden}
.pic img{display:block;width:100%}
.cap{font-family:'Liberation Sans','DejaVu Sans',sans-serif;font-size:15px;color:var(--stone)}
.bg-navy .cap,.bg-black .cap{color:#b8c2d6}
#sub{position:absolute;left:70px;right:70px;bottom:24px;text-align:center;font-family:'Liberation Sans','DejaVu Sans',sans-serif;font-size:26px;line-height:1.3;color:#fff;background:rgba(5,13,31,.82);padding:10px 20px;border-radius:10px;opacity:0}
#bar{position:absolute;left:0;bottom:0;height:5px;background:var(--gold)}
</style></head><body><div id="stage">
'''

JS='''
const ease=x=>1-Math.pow(1-x,3), clamp=x=>Math.max(0,Math.min(1,x)), lerp=(a,b,p)=>a+(b-a)*p;
const scenes=[...document.querySelectorAll('.scene')], sub=document.getElementById('sub'), bar=document.getElementById('bar');
const FN={
 spin(el,t,d){const t0=+d.t,dir=+d.dir,sp=+d.speed,stop=d.stop?+d.stop:1e9;let cx=+d.cx,cy=+d.cy;
   if(d.dx){cx+=(+d.dx)*ease(clamp((t-(+d.dxt))/1.6))}
   const a=dir*sp*(Math.min(Math.max(t,t0),stop)-t0)+(+d.phase||0);
   el.setAttribute('transform',`translate(${cx} ${cy}) rotate(${a})`);
   if(d.lock&&t>=+d.lock){const p=el.querySelector('path');if(p){p.setAttribute('fill',d.lockfill||'#C0392B')}}},
 wave(el,t,d){const t0=+d.t,R=+d.R,n=+d.n||3;[...el.children].forEach((c,i)=>{const ph=(t-t0-i*.28)/1.3;
   if(ph>0&&ph<1){c.setAttribute('r',lerp(8,R,ease(ph)));c.setAttribute('opacity',(1-ph)*.9)}else c.setAttribute('opacity',0)})},
 grow(el,t,d){const p=clamp((t-(+d.t))/(+d.dur||1));el.setAttribute('width',Math.max(0.01,(+d.w)*ease(p)))},
 crack(el,t,d){const L=+d.len,p=clamp((t-(+d.t))/(+d.dur||1.2));el.setAttribute('stroke-dasharray',L);el.setAttribute('stroke-dashoffset',L*(1-p))},
 kf(el,t,d){const k=JSON.parse(d.kf);let x=k[0][1],y=k[0][2],s=k[0][3]===undefined?1:k[0][3];
   for(let i=0;i<k.length-1;i++){const a=k[i],b=k[i+1];if(t>=a[0]&&t<=b[0]){const p=ease((t-a[0])/(b[0]-a[0]||1));x=lerp(a[1],b[1],p);y=lerp(a[2],b[2],p);s=lerp(a[3]===undefined?1:a[3],b[3]===undefined?1:b[3],p);break}
     if(t>b[0]){x=b[1];y=b[2];s=b[3]===undefined?1:b[3]}}
   el.setAttribute('transform',`translate(${x} ${y}) scale(${s})`)},
 kfd(el,t,d){const k=JSON.parse(d.kf);let x=k[0][1],y=k[0][2];
   for(let i=0;i<k.length-1;i++){const a=k[i],b=k[i+1];if(t>=a[0]&&t<=b[0]){const p=ease((t-a[0])/(b[0]-a[0]||1));x=lerp(a[1],b[1],p);y=lerp(a[2],b[2],p);break}if(t>b[0]){x=b[1];y=b[2]}}
   el.style.transform=`translate(${x}px,${y}px)`},
 count(el,t,d){const p=ease(clamp((t-(+d.t))/(+d.dur||1.5)));el.textContent=Math.round(lerp(+d.from,+d.to,p))+(d.suffix||'')}
};
function apply(el,t){
  const d=el.dataset,t0=+d.t,du=+(d.d||.6),a=d.a||'fade',x=d.x?+d.x:1e9;
  let p=ease(clamp((t-t0)/du)); if(t>=x) p=Math.min(p,1-ease(clamp((t-x)/.4)));
  const svg=el instanceof SVGElement;
  if(!d.fn||d.fn==='spin'||d.fn==='kf'||d.fn==='kfd'||d.fn==='count'||d.fn==='wave'||d.fn==='grow'||d.fn==='crack'){ el.style.opacity=(t<t0)?0:(d.o?Math.min(+d.o,p):p); }
  if(!svg&&!d.fn){ let tr=''; if(a==='fade')tr=`translateY(${(1-p)*18}px)`; else if(a==='pop')tr=`scale(${.82+.18*p})`; else if(a==='l')tr=`translateX(${-(1-p)*90}px)`; else if(a==='r')tr=`translateX(${(1-p)*90}px)`; else if(a==='d')tr=`translateY(${-(1-p)*40}px)`; el.style.transform=tr; }
  if(d.fn&&FN[d.fn]) FN[d.fn](el,t,d);
}
function seek(t){
  scenes.forEach(s=>{
    const a=+s.dataset.s,b=+s.dataset.e,inside=t>=a&&t<b;
    s.style.opacity=inside?Math.min(clamp((t-a)/.45),clamp((b-t)/.45)):0;
    if(!inside) return;
    s.querySelectorAll('[data-t]').forEach(e=>apply(e,t));
  });
  const c=CUES.find(c=>t>=c[0]&&t<c[1]+0.3);
  sub.textContent=c?c[2]:''; sub.style.opacity=c?1:0;
  bar.style.width=(t/DUR*1280)+'px';
}
window.seek=seek; window.CUES=CUES; window.DUR=DUR; seek(0);
'''

# ---------- éléments ----------
def E(inner,t,x=0,y=0,w=None,h=None,a='fade',d=.6,cls='',style='',xe=None,attrs=''):
    s=f'left:{x}px;top:{y}px;'+(f'width:{w}px;' if w else '')+(f'height:{h}px;' if h else '')+style
    xx=f' data-x="{xe:.2f}"' if xe else ''
    return f'<div class="el {cls}" data-t="{t:.2f}" data-a="{a}" data-d="{d}"{xx} style="{s}" {attrs}>{inner}</div>\n'

def badge(p,cls=''): return f'<span class="bd {cls}">{p}</span>'

def paper(title,piece,body,t,x,y,w,h=None,cls='',a='fade',d=.6,xe=None,pcls=''):
    head=f'<div class="ph"><span>{title}</span>{badge(piece,pcls) if piece else ""}</div>'
    return E(head+body,t,x,y,w,h,a,d,'paper '+cls,'',xe)

def pic(src,cap,t,x,y,w,a='fade',xe=None):
    return E(f'<div class="pic"><img src="../avocat/img/{src}"></div><div class="cap" style="margin-top:6px">{cap}</div>',t,x,y,w,None,a,.6,'',"",xe)

def gear_path(ro,ri,n):
    pts=[]
    for i in range(n):
        a0=2*math.pi*i/n; w=2*math.pi/n
        for ang,r in [(a0-w*.28,ri),(a0-w*.16,ro),(a0+w*.16,ro),(a0+w*.28,ri)]:
            pts.append((r*math.cos(ang),r*math.sin(ang)))
    return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+' Z'

def gear(cx,cy,ro,t,dir=1,speed=40,n=12,fill=NAVY,stroke=GOLD,stop=None,lock=None,phase=0,hole='#F5F0E8',cls='',o=1,ri=None,lockfill=RED,dx=None,dxt=None):
    ri=ri or ro*.86
    st=f' data-stop="{stop:.2f}"' if stop else ''
    lk=(f' data-lock="{lock:.2f}" data-lockfill="{lockfill}"' if lock else '')+(f' data-dx="{dx}" data-dxt="{dxt:.2f}"' if dx else '')
    return (f'<g class="el" data-t="{t:.2f}" data-fn="spin" data-cx="{cx}" data-cy="{cy}" data-dir="{dir}" data-speed="{speed}" data-phase="{phase}"{st}{lk} data-o="{o}">'
            f'<path d="{gear_path(ro,ri,n)}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<circle r="{ro*.55:.1f}" fill="none" stroke="{stroke}" stroke-width="2" opacity=".8"/>'
            f'<circle r="{ro*.18:.1f}" fill="{hole}" stroke="{stroke}" stroke-width="2"/></g>\n')

def svg(inner): return f'<svg class="svgl" viewBox="0 0 1280 720">{inner}</svg>\n'

def wave(cx,cy,R,t,color=RED):
    return (f'<g class="el" data-t="{t:.2f}" data-fn="wave" data-R="{R}">'+''.join(f'<circle cx="{cx}" cy="{cy}" r="8" fill="none" stroke="{color}" stroke-width="4" opacity="0"/>' for _ in range(3))+'</g>\n')

# icônes 48x48 (trait)
ICONS={
 'scales':'<path d="M24 8V40M12 40H36M9 14H39M9 14L3 28H15ZM39 14L33 28H45Z"/>',
 'seal':'<circle cx="24" cy="22" r="15"/><circle cx="24" cy="22" r="9"/><path d="M16 35L12 46L21 42L24 46M32 35L36 46L27 42"/>',
 'hand':'<rect x="13" y="22" width="22" height="20" rx="6"/><rect x="14" y="8" width="5" height="18" rx="2.5"/><rect x="20.5" y="5" width="5" height="21" rx="2.5"/><rect x="27" y="7" width="5" height="19" rx="2.5"/><path d="M13 30L7 22"/>',
 'lock':'<rect x="11" y="22" width="26" height="20" rx="3"/><path d="M16 22V16A8 8 0 0 1 32 16V22"/><circle cx="24" cy="32" r="3"/>',
 'bank':'<path d="M6 18L24 6L42 18ZM10 20V36M19 20V36M29 20V36M38 20V36M5 40H43"/>',
 'doc':'<rect x="10" y="5" width="28" height="38" rx="2"/><path d="M16 14H32M16 21H32M16 28H26"/><circle cx="32" cy="35" r="5"/>',
 'glass':'<circle cx="20" cy="20" r="12"/><path d="M29 29L42 42"/>',
 'finger':'<path d="M10 30C10 16 17 8 24 8S38 16 38 30M16 34C16 22 19 14 24 14S32 22 32 34M22 40C21 32 21 22 24 20C27 22 27 32 26 40"/>',
 'mic':'<rect x="17" y="6" width="14" height="22" rx="7"/><path d="M10 24A14 14 0 0 0 38 24M24 38V44M17 44H31"/>',
 'mail':'<rect x="6" y="11" width="36" height="26" rx="2"/><path d="M6 12L24 28L42 12"/>',
 'scale2':'<path d="M24 8V40M12 40H36M9 14H39M9 14L3 28H15ZM39 14L33 28H45Z"/>',
 'clock':'<circle cx="24" cy="24" r="17"/><path d="M24 13V25L32 30"/>',
 'chart':'<path d="M7 41H43M12 41V28M20 41V20M28 41V30M36 41V12"/>',
 'key':'<circle cx="14" cy="24" r="8"/><path d="M22 24H44M36 24V31M42 24V30"/>',
 'person':'<circle cx="24" cy="14" r="8"/><path d="M8 44C8 30 16 26 24 26S40 30 40 44Z"/>',
}
def icon(name,size=44,color=NAVY,sw=3):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'

def seal_svg(cx,cy,r,t,crack_t=None,ring=GOLD,fill='none',cls=''):
    ticks=''.join(f'<line x1="{(r*.86)*math.cos(i*math.pi/12):.1f}" y1="{(r*.86)*math.sin(i*math.pi/12):.1f}" x2="{(r*.97)*math.cos(i*math.pi/12):.1f}" y2="{(r*.97)*math.sin(i*math.pi/12):.1f}" stroke="{ring}" stroke-width="3"/>' for i in range(24))
    scal=f'<g transform="scale({r/60:.3f})" stroke="{ring}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M0 -34V32M-18 32H18M-34 -24H34M-34 -24L-46 4H-22ZM34 -24L22 4H46Z"/></g>'
    out=(f'<g class="el" data-t="{t:.2f}" transform="translate({cx} {cy})"><circle r="{r}" fill="{fill}" stroke="{ring}" stroke-width="7"/>'
         f'<circle r="{r*.82:.1f}" fill="none" stroke="{ring}" stroke-width="2"/>{ticks}{scal}</g>\n')
    if crack_t:
        pts=[(cx+r*.1,cy-r*1.0),(cx-r*.05,cy-r*.55),(cx+r*.2,cy-r*.2),(cx-r*.1,cy+r*.15),(cx+r*.15,cy+r*.5),(cx,cy+r*1.0)]
        d='M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)
        L=sum(math.hypot(pts[i+1][0]-pts[i][0],pts[i+1][1]-pts[i][1]) for i in range(len(pts)-1))
        out+=f'<path class="el" data-t="{crack_t:.2f}" data-fn="crack" data-len="{L:.0f}" data-dur="1.6" d="{d}" fill="none" stroke="{RED}" stroke-width="5" stroke-linecap="round"/>\n'
    return out

def padlock(cx,cy,s,t,color=RED):
    return (f'<g class="el" data-t="{t:.2f}"><g transform="translate({cx-24*s} {cy-24*s}) scale({s})" fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round">{ICONS["lock"]}</g></g>\n')

def scene(sid,tag,bg,T,body):
    return (f'<div class="scene {bg}" id="{sid}" data-s="{T["s"]:.2f}" data-e="{T["e"]:.2f}">\n'
            +(f'<div class="tag">{tag}</div>\n' if tag else '')+body+'</div>\n\n')

# ---------- voix : conversion du texte affiché en texte lu ----------
from num2words import num2words
def voice(t):
    v=t
    for a,b in [('BALLEY','Balley'),('FÉLIHO','Féliho'),('FELIHO','Féliho'),('DMD','D M D'),('DGI','D G I'),('CGI','C G I'),('APDP','A P D P'),('CNHU-HKM','C N H U H K M'),('CNHU','C N H U'),('ATOUN','Atoun'),('ICHOLA','Ichola'),('ADJAGBA','Adjagba'),('CPF','C P F')]:
        v=v.replace(a,b)
    v=re.sub(r'\bMe\b','Maître',v)
    v=re.sub(r'\b\d{1,3}(?: \d{3})+\b',lambda m:num2words(int(m.group(0).replace(' ','')),lang='fr'),v)
    v=re.sub(r'(\d+) ?%',lambda m:num2words(int(m.group(1)),lang='fr')+' pour cent',v)
    v=v.replace('1er','premier').replace('Évenemenciel','évènementiel').replace('AIB','A I B').replace('FCFA','francs CFA')
    v=re.sub(r'\bP(\d{1,2})\b',lambda m:'pièce '+num2words(int(m.group(1)),lang='fr'),v)
    v=re.sub(r'n° (\d+)/(\d+)',lambda m:'numéro '+num2words(int(m.group(1)),lang='fr')+' barre '+num2words(int(m.group(2)),lang='fr'),v)
    v=re.sub(r'\bn° (\d+)',lambda m:'numéro '+num2words(int(m.group(1)),lang='fr'),v)
    v=re.sub(r'\bArt\. ','article ',v); v=re.sub(r'\bart\. ','article ',v)
    def num(m):
        n=int(m.group(0))
        if 1900<=n<=2100: return m.group(0)
        if n>=100: return num2words(n,lang='fr')
        return m.group(0)
    v=re.sub(r'(?<![\d/])\d{3,4}(?![\d/])',num,v)
    v=re.sub(r'(\d+)\s?FCFA',lambda m:m.group(1)+' francs CFA',v)
    v=v.replace('«','').replace('»','').replace('<b>','').replace('</b>','')
    return v

def seal_g(r,ring=GOLD):
    ticks=''.join(f'<line x1="{(r*.86)*math.cos(i*math.pi/12):.1f}" y1="{(r*.86)*math.sin(i*math.pi/12):.1f}" x2="{(r*.97)*math.cos(i*math.pi/12):.1f}" y2="{(r*.97)*math.sin(i*math.pi/12):.1f}" stroke="{ring}" stroke-width="3"/>' for i in range(24))
    scal=f'<g transform="scale({r/60:.3f})" stroke="{ring}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M0 -34V32M-18 32H18M-34 -24H34M-34 -24L-46 4H-22ZM34 -24L22 4H46Z"/></g>'
    return f'<circle r="{r}" fill="none" stroke="{ring}" stroke-width="7"/><circle r="{r*.82:.1f}" fill="none" stroke="{ring}" stroke-width="2"/>{ticks}{scal}'
