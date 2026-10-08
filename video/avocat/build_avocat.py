# -*- coding: utf-8 -*-
import re,json,sys,html
sys.path.insert(0,'.')
import importlib, spec_avocat as sp
from num2words import num2words
OUT='motion.html'
CSS='''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Le notaire Félix BALLEY face à ses obligations — wadagni2026-verite.com</title>
<style>
:root{--navy:#0a1f44;--blue:#1e3a8a;--gold:#d4af37;--red:#ef4444;--green:#10b981;--ink:#f8fafc;--mute:#94a3b8}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1280px;height:720px;overflow:hidden;background:#050d1f;font-family:'DejaVu Sans','Inter',sans-serif;color:var(--ink)}
#stage{position:relative;width:1280px;height:720px;background:radial-gradient(ellipse at 30% 20%,#12306b 0%,#0a1f44 45%,#050d1f 100%)}
.scene{position:absolute;inset:0;opacity:0}
.el{opacity:0}
.gold{color:var(--gold)}.red{color:var(--red)}.green{color:var(--green)}.mute{color:var(--mute)}
.tag{position:absolute;left:60px;top:26px;width:1160px;font-size:21px;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}
.cols{position:absolute;left:60px;right:60px;top:78px;display:flex;gap:30px;align-items:flex-start}
.col{flex:1;display:flex;flex-direction:column;gap:12px;min-width:0}
.card{font-size:24px;line-height:1.35;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);border-radius:14px;padding:16px 22px}
.big{font-size:42px;font-weight:800;line-height:1.25}
.pic{background:#fff;border-radius:6px;box-shadow:0 12px 36px rgba(0,0,0,.55);overflow:hidden;border:3px solid var(--gold)}
.pic img{display:block;width:100%}
.cap{font-size:17px;color:var(--mute);margin-top:-6px}
#sub{position:absolute;left:70px;right:70px;bottom:26px;text-align:center;font-size:26px;line-height:1.3;background:rgba(0,0,0,.66);padding:10px 20px;border-radius:10px;opacity:0}
#bar{position:absolute;left:0;bottom:0;height:5px;background:var(--gold)}
</style></head><body><div id="stage">
'''
def split_sub(t,mx=150):
    sents=re.split(r'(?<=[.!?])\s+',t)
    parts=[];cur=''
    for s_ in sents:
        if len(s_)>mx:
            sub=re.split(r'(?<=[,:;])\s+',s_); 
            for x in sub:
                if cur and len(cur)+1+len(x)>mx: parts.append(cur); cur=x
                else: cur=(cur+' '+x).strip()
            continue
        if cur and len(cur)+1+len(s_)>mx: parts.append(cur); cur=s_
        else: cur=(cur+' '+s_).strip()
    if cur: parts.append(cur)
    return parts
def voice(t):
    v=t
    for a,b in [('BALLEY','Balley'),('FÉLIHO','Féliho'),('FELIHO','Féliho'),('FADE','Fade'),('DMD','D M D'),('DGI','D G I'),('CGI','C G I'),('APDP','A P D P'),('OPJ','O P J'),('CNHU','C N H U'),('BAC','B A C'),('CPF','C P F')]:
        v=v.replace(a,b)
    v=re.sub(r'\bMe\b','Maître',v)
    v=re.sub(r'n° (\d+)/(\d+)',lambda m:'numéro '+num2words(int(m.group(1)),lang='fr')+' barre '+num2words(int(m.group(2)),lang='fr'),v)
    v=re.sub(r'\bn° (\d+)',lambda m:'numéro '+m.group(1),v)
    def num(m):
        n=int(m.group(0))
        if 1900<=n<=2100: return m.group(0)
        if n>=100: return num2words(n,lang='fr')
        return m.group(0)
    v=re.sub(r'(?<![\d/])\d{3,4}(?![\d/])',num,v)
    v=v.replace('«','').replace('»','')
    return v
def est(t): return len(t)/12.5+0.9
import subprocess,math
IMGD='/home/user/wadagni-verite/video/avocat/img/'
_dims={}
def dims(f):
    if f not in _dims:
        w,h=subprocess.check_output(['identify','-format','%w %h',IMGD+f],text=True).split(); _dims[f]=(int(w),int(h))
    return _dims[f]
COLW=585
def plain(h): return re.sub(r'<[^>]+>',' ',h)
def height(kind,content):
    if kind=='pic':
        f,cap=content; w,h=dims(f); return int(COLW*h/w)+6+(26 if cap else 0)+12
    txt=plain(content); br=content.count('<br')
    if kind=='big': 
        lines=sum(max(1,math.ceil(len(x)/24)) for x in re.split(r'<br\s*/?>',content.replace("<span class='gold'>","").replace("</span>","")))
        return 54*lines+12
    lines=sum(max(1,math.ceil(len(plain(x))/37)) for x in re.split(r'<br\s*/?>',content))
    return 33*lines+34+12
B='';CUES=[];t=0.5
LIM=470
pages=[]
for sc in sp.SCENES:
    cur=None
    for c in sc['cues']:
        parts=split_sub(c['sub'])
        rowparts=[]
        for k,p in enumerate(parts):
            rowparts.append((p,c['items'] if k==0 else []))
        # hauteurs ajoutées par ce cue
        add={'L':0,'R':0}
        for (col,kind,content) in c['items']: add[col]+=height(kind,content)
        if cur is None or cur['h']['L']+add['L']>LIM or cur['h']['R']+add['R']>LIM:
            cur=dict(tag=sc['tag']+('' if cur is None else ' (suite)'),style=sc.get('style',''),rows=[],h={'L':0,'R':0}); pages.append(cur)
        cur['h']['L']+=add['L']; cur['h']['R']+=add['R']
        cur['rows']+=rowparts
for pg in pages:
    s_start=t
    cue_rows=[]
    for (p,items) in pg['rows']:
        v=voice(p)
        cue_rows.append((t,t+est(v),p,v if v!=p else None,items)); t+=est(v)+0.4
    s_end=t+0.6
    cols={'L':[],'R':[]}
    for (a_,b_,p,v,items) in cue_rows:
        CUES.append((a_,b_,p,v))
        for (col,kind,content) in items:
            d=round(a_-s_start+0.2,1)
            if kind=='pic':
                f,cap=content
                h=f'<div class="el pic" data-in="{d}"><img src="img/{f}"></div>'+(f'<div class="el cap" data-in="{d}">{cap}</div>' if cap else '')
            else:
                h=f'<div class="el {kind}" data-in="{d}">{content}</div>'
            cols[col].append(h)
    inner=f'<div class="col">{"".join(cols["L"])}</div>'+(f'<div class="col">{"".join(cols["R"])}</div>' if cols['R'] else '')
    st=f' style="{pg["style"]}"' if pg['style'] else ''
    B+=f'<div class="scene" data-s="{round(s_start-0.3,1)}" data-e="{round(s_end,1)}"{st}>\n <div class="tag el" data-in="0.1">{pg["tag"]}</div>\n <div class="cols">{inner}</div>\n</div>\n\n'
DUR=round(t+1,1)
js='<div id="sub"></div><div id="bar"></div>\n</div>\n<script>\nconst DUR=%s;\n// CUES = [début, fin, sous-titre, (texte lu si différent)]\nconst CUES=[\n'%DUR
L=[]
for a,b,p,v in CUES:
    assert '"' not in p and '\\' not in p,p
    L.append(f'[{round(a,1)},{round(b,1)},"{p}"'+(f',"{v}"' if v else '')+']')
js+=',\n'.join(L)+'\n];\n'
tail=open('/home/user/wadagni-verite/video/balley/motion.html',encoding='utf-8').read()
tail=tail[tail.index('const ease='):]
open(OUT,'w',encoding='utf-8').write(CSS+B+js+tail)
print('pages',len(pages),'cues',len(CUES),'durée est.',DUR)
# audit nommage
bad=[]
for a,b,p,v in CUES:
    for m in re.finditer(r'\bnotaires?\b',p):
        nxt=p[m.end():m.end()+14]; prv=p[max(0,m.start()-8):m.start()]
        if 'Félix' in nxt or 'Maître' in nxt or 'Chambre nationale des' in p[max(0,m.start()-24):m.start()+8]: continue
        bad.append((p[max(0,m.start()-30):m.end()+30]))
print('mentions « notaire » sans nom :',len(bad)); [print('  -',x) for x in bad]

# fenêtres de scènes contiguës (sans chevauchement) pour build_voix.py
import re as _re
_s=open('motion.html',encoding='utf-8').read()
_st=[a for a,b in _re.findall(r'data-s="([\d.]+)" data-e="([\d.]+)"',_s)];_i=[0]
def _f(m):
    k=_i[0];_i[0]+=1
    return f'data-s="{m.group(1)}" data-e="{_st[k+1] if k+1<len(_st) else m.group(2)}"'
open('motion.html','w',encoding='utf-8').write(_re.sub(r'data-s="([\d.]+)" data-e="([\d.]+)"',_f,_s))
