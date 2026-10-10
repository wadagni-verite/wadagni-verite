# -*- coding: utf-8 -*-
# « La Mécanique de Verrouillage » — spécification des scènes (texte, pièces, animations)
import math, json, datetime
from lib import *
N='le notaire Félix BALLEY'
SC=[]
def S(sid,tag,bg,cues,build,minlen=0,pre=None):
    SC.append(dict(id=sid,tag=tag,bg=bg,cues=cues,build=build,minlen=minlen,pre=pre))
def mech_row(T,k,lockt,x0=840,y=64,ro=26):
    """rangée des 4 pignons : verrouillés (rouge), actif (or, tourne), à venir (pâle)"""
    out=''
    for i in range(4):
        cx=x0+i*92
        if i<k: out+=gear(cx,y,ro,T['s']+.2,dir=1 if i%2==0 else -1,speed=0,fill=RED,stroke=GOLD,hole='#0A1F44')
        elif i==k: out+=gear(cx,y,ro,T['s']+.2,dir=1 if i%2==0 else -1,speed=70,fill='#26427a',stroke=GOLD,lock=lockt,hole='#0A1F44',phase=15*(i%2))
        else: out+=gear(cx,y,ro,T['s']+.2,dir=1,speed=0,fill='none',stroke='#6f7fa3',hole='#0A1F44',o=.45)
    return svg(out)
def title_gear(T,k,label,year):
    return (svg(gear(112,140,52,T['s']+.1,dir=1,speed=45,fill='#26427a',stroke=GOLD,hole='#0A1F44',lock=T['ce'][-1]-.2))
            +E(f'<span class="gold">Pignon {k}</span> — {label}<br><span class="md ivc" style="font-weight:400">{year}</span>',T['s']+.2,185,100,700,None,'fade',.6,'serif lg'))

# ====================== PROLOGUE ======================
def pro1(T):
    c=T['c'];ce=T['ce']
    seal=(f'<g class="el" data-t="{c[0]+.2:.2f}" data-fn="kf" data-kf=\'{json.dumps([[c[0]+.2,640,250,1],[ce[0]-1.4,640,250,1],[ce[0]-.2,170,150,.42]])}\'>'
          +seal_g(105)+'</g>')
    b=svg(seal)
    b+=pic('cert-deces-mandat.jpg','Certificat d\'acquit de droit, 20 octobre 2016 (P6)',ce[0]-.8,210,300,860)
    b+=E('Date de décès : <span class="red">10 juin 2016.</span>',c[1],0,470,1280,None,'fade',.8,'xl serif center')
    return b
S('pro1','Prologue — L\'acte qui devait tout prouver','bg-iv',
  [("Le 20 octobre 2016, un certificat d'acquit de droit est délivré pour la succession de Jean Florentin Féliho.",None),
   ("Il indique, pour la date de décès : le 10 juin 2016.",None)],pro1)

def pro2(T):
    c=T['c'];T['fx'].append(('heart',T['s']+.15))
    b=E('Date réelle : <span class="ivc">3 décembre 2010.</span>',c[0],0,200,1280,None,'fade',.9,'xl serif center ivc')
    b+=E('<span class="gold">5 ans et 6 mois</span> d\'écart',c[0]+2.6,0,320,1280,None,'fade',.9,'lg serif center ivc')
    b+=E('Erreur de plume, <span class="gold">ou mécanique ?</span>',c[1],0,450,1280,None,'fade',.9,'lg serif center ivc')
    return b
S('pro2',None,'bg-black',
  [("La date réelle est le 3 décembre 2010. Cinq ans et six mois d'écart.",None),
   ("Erreur de plume, ou mécanique ? Les pièces répondent.",None)],pro2)

# ====================== ACTE 1 ======================
def a11(T):
    c=T['c']
    b=paper('Statut du notariat · loi n° 2002-015 du 30 décembre 2002','',
            '<div style="height:420px"></div>',c[0],60,92,780,None,'',  'pop',.9)
    rows=[('seal','Art. 1er','chargé « d\'assurer la date de ces actes et contrats, d\'en conserver le dépôt »','loi 2002-015, p. 2'),
          ('hand','Art. 33','serment : « Je jure de remplir mes fonctions avec exactitude et probité »','loi 2002-015, p. 7'),
          ('scales','Art. 47','responsabilité disciplinaire et pénale pour les fautes commises dans son ministère','loi 2002-015, p. 8')]
    for i,(ic,art,txt,src) in enumerate(rows):
        y=148+i*128
        b+=E(f'<div style="display:flex;gap:18px;align-items:center;border-left:7px solid {GOLD};padding:6px 0 6px 16px;background:rgba(201,162,39,.12)">{icon(ic,58)}<div><div class="serif" style="font-size:26px;font-weight:700">{art}</div><div class="qt" style="font-size:20px;line-height:1.25">{txt}</div><div class="cap">{src}</div></div></div>',c[1+i],86,y,730,None,'l',.6)
    b+=E(f'<div class="paper gold center" style="padding:24px"><div style="display:flex;justify-content:center">{icon("lock",90,RED)}</div><div class="serif lg" style="margin-top:8px">Obligation de<br><span class="red">vérification renforcée</span></div></div>',c[4],880,170,340,None,'pop',.7)
    return b
S('a11','Acte 1 — L\'officier public et l\'intention','bg-iv',
  [(f"{N[0].upper()+N[1:]} est officier public. Le statut du notariat, loi n° 2002-015 du 30 décembre 2002, lui impose des obligations précises.",None),
   ("Article 1er : il est chargé d'assurer la date des actes et d'en conserver le dépôt.","Article premier : il est chargé d'assurer la date des actes et d'en conserver le dépôt."),
   ("Article 33 : il a juré de remplir ses fonctions avec exactitude et probité.",None),
   ("Article 47 : il est responsable, disciplinairement et pénalement, des fautes commises dans son ministère.",None),
   ("Cette qualité fonde une obligation de vérification renforcée.",None)],a11)

def a12(T):
    c=T['c'];b=''
    cols=[('Déclaration de décès · CNHU-HKM','P1','3 décembre 2010','Jean Florentin FÉLIHO, décédé à Cotonou',''),
          ('PV de lecture du testament · audience du 24 avril 2012','P2','3 décembre 2010','« décédé à Cotonou le 03 décembre 2010 »',''),
          ('Jugement n° 114/14 · 31 octobre 2014','P5','3 décembre 2010','« décédé le 03 décembre 2010 à Cotonou »',''),
          ('Certificat d\'acquit de droit · 20 octobre 2016','P6','10 juin 2016','« décédé à Cotonou le dix juin deux mil seize »','red')]
    for i,(ti,p,dt,nt,cl) in enumerate(cols):
        t=c[i]+(.25 if i<3 else .9)
        b+=paper(ti,p,f'<div class="date {"red" if cl else ""}" style="font-size:30px">{dt}</div><div class="qt" style="font-size:19px;margin-top:8px">{nt}</div>',t,60+i*300,100,272,248,cl,'r' if i==3 else 'fade',.7,None,'r' if cl else '')
    b+=svg(wave(1128-9,224,170,c[3]+.9))
    b+=E('Trois sources indépendantes. <span class="stone">Une seule date.</span><br><span class="red">Une seule contredit les autres.</span>',c[4],60,400,1160,None,'fade',.8,'lg serif center')
    return b
S('a12','Acte 1 — La connaissance objective','bg-iv',
  [("Quatre pièces. La déclaration de décès, P1 : décès le 3 décembre 2010.",None),
   ("Le procès-verbal de lecture du testament, P2, audience du 24 avril 2012 : décédé à Cotonou le 3 décembre 2010.",None),
   ("Le jugement n° 114/14, P5, du 31 octobre 2014 : décédé le 3 décembre 2010.",None),
   ("Le certificat d'acquit de droit, P6, daté du 20 octobre 2016 : décès le 10 juin 2016.",None),
   ("Trois sources indépendantes. Une seule date. Une seule contredit les autres.",None)],a12)

def a13(T):
    c=T['c'];ce=T['ce'];x0=90;W=1100;M=68.23
    X=lambda m: x0+W*m/M
    b=''
    b+=E('<span class="serif" style="font-size:24px"><b>Date réelle du décès</b> : 3 décembre 2010</span>',c[0],90,100,700,None,'fade',.6)
    ln=lambda y,col: f'<rect x="{x0}" y="{y}" width="{W}" height="26" fill="#e3dccb" rx="3"/>'
    s=f'<g class="el" data-t="{c[0]:.2f}" data-a="none"><rect x="{x0}" y="170" width="{W}" height="26" fill="#e3dccb" rx="3"/><rect x="{x0}" y="330" width="{W}" height="26" fill="#e3dccb" rx="3"/></g>'
    s+=f'<rect class="el" data-t="{c[0]+.5:.2f}" data-fn="grow" data-w="{X(6)-x0:.1f}" data-dur=".9" x="{x0}" y="170" width="0.01" height="26" fill="#2e8b57" rx="3"/>'
    s+=f'<rect class="el" data-t="{c[1]+.6:.2f}" data-fn="grow" data-w="{W-(X(6)-x0):.1f}" data-dur="3" x="{X(6):.1f}" y="170" width="0.01" height="26" fill="{RED}" rx="3"/>'
    s+=f'<rect class="el" data-t="{c[2]+.6:.2f}" data-fn="grow" data-w="{W-(X(66.23)-x0):.1f}" data-dur="1" x="{X(66.23):.1f}" y="330" width="0.01" height="26" fill="#2e8b57" rx="3"/>'
    b+=svg(s)
    b+=E('<span class="sm"><b>3 juin 2011</b><br>fin du délai de 6 mois</span>',c[1]+.2,X(6)-10,205,230,None,'fade',.5)
    b+=E('<span class="sm" style="text-align:right;display:block"><b>10 août 2016</b> · enregistrement<br><span class="red"><b>5 ans et 2 mois de retard</b></span></span>',c[1]+3.2,x0+W-420,205,420,None,'fade',.6)
    b+=E('<span class="sm" style="display:block"><b>Délai légal : 6 mois</b> (CGI, art. 438)</span>',c[0]+.6,90,138,500,None,'fade',.5)
    b+=E('<span class="serif" style="font-size:24px"><b>Date portée au certificat</b> : 10 juin 2016</span>',c[2],90,290,700,None,'fade',.6)
    b+=E('<span class="sm" style="text-align:right;display:block"><b>2 mois</b> : <span style="color:#2e8b57"><b>dans le délai</b></span></span>',c[2]+1.4,x0+W-420,365,420,None,'fade',.6)
    b+=E('La fausse date ne corrige pas une simple erreur :<br><span class="red">elle fait disparaître le retard.</span>',c[3],60,430,980,None,'fade',.8,'lg serif')
    b+=svg(seal_svg(1160,490,52,c[4],crack_t=c[4]+.5))
    return b
S('a13','Acte 1 — L\'effet juridique de la fausse date','bg-iv',
  [("L'article 438 du Code général des impôts impose de déclarer la succession dans les six mois du décès, lorsque le décès survient au Bénin.",None),
   ("Avec la vraie date, le 3 décembre 2010, le délai expirait le 3 juin 2011. La déclaration est enregistrée le 10 août 2016 : cinq ans et deux mois de retard.",None),
   ("Avec la date du certificat, le 10 juin 2016, la déclaration paraît faite dans les deux mois. Le retard disparaît.",None),
   ("La fausse date ne corrige pas une simple erreur : elle fait disparaître le retard.",None),
   (f"Pour comprendre, il faut remonter le fil des positions successives de {N}.",None)],a13)

# ====================== ACTE 2 ======================
LAB=[('Mandataire','2016'),('Tiers non partie','2023'),('Décision de justice','2024'),('Exécution partielle','2025')]
def a20(T):
    c=T['c'];b=''
    g=''
    xs=[412,564,716,868]
    for i,x in enumerate(xs):
        g+=gear(x,285,82,c[0]+.2+i*.25,dir=1 if i%2==0 else -1,speed=22,fill='#1c3d7a',stroke=GOLD,hole='#0A1F44',phase=15*(i%2))
    b+=svg(g)
    for i,x in enumerate(xs):
        b+=E(f'<div class="serif center" style="font-size:22px;line-height:1.2"><span class="gold" style="font-size:30px">{i+1}</span><br>{LAB[i][0]}<br><span class="cap" style="font-size:19px">{LAB[i][1]}</span></div>',c[1]+.4+i*.9,x-72,390,144,None,'fade',.6)
    b+=E('Chaque pignon enclenche le suivant.<br><span class="gold">Chacun bloque le précédent.</span>',c[1]+4.5,60,500,1160,None,'fade',.8,'lg serif center')
    return b
S('a20','Acte 2 — L\'engrenage des contradictions','bg-navy',
  [("Quatre positions successives. Chacune écarte le contrôle qui aurait dû vérifier la précédente.",None),
   ("Voici le mécanisme : un pignon par position, chaque pignon enclenche le suivant.",None)],a20)

def a21(T):
    c=T['c'];ce=T['ce'];T['fx'].append(('click',ce[-1]-.2))
    b=mech_row(T,0,ce[-1]-.2)+title_gear(T,1,'Mandataire','2016')
    b+=pic('cert-deces-mandat.jpg','Certificat d\'acquit de droit, 20 octobre 2016 (P6)',c[0]+.3,60,230,740)
    b+=paper('Mandat donné ?','',f'<div class="lg red" style="font-size:44px">Aucun</div><div class="sm" style="margin-top:6px">Gilles FÉLIHO n\'a jamais donné mandat<br>et n\'a jamais consenti à cette mention.</div>',c[1]+.2,850,230,370,None,'red','pop',.6)
    b+=pic('art61.jpg','Statut du notariat, art. 61 : procurations annexées ou déposées au rang des minutes',c[2]+.3,60,350,740)
    b+=E('<div style="border:3px dashed #9aa6bf;border-radius:8px;padding:12px 16px;color:#b8c2d6" class="serif"><div style="font-size:24px;letter-spacing:.1em">PROCURATION</div><div class="sm">aucune signature · aucune date · aucun dépôt</div></div>',c[2]+1.2,850,402,370,None,'fade',.6)
    b+=pic('mise-preuve.jpg','Mise en demeure du 28 mai 2025 (P15) — preuve écrite du mandat demandée',c[3]+.3,60,470,740)
    b+=E('<span class="red" style="font-weight:700">Aucune réponse.</span>',c[3]+1.2,850,520,370,None,'pop',.5,'lg serif')
    return b
S('a21','Acte 2 — Pignon 1','bg-navy',
  [("Pignon 1 : mandataire, en 2016. Le certificat d'acquit de droit, P6, indique : agissant en qualité de mandataire et au nom des héritiers suivants, dont Gilles Sixte Féliho.","Pignon un : mandataire, en 2016. Le certificat d'acquit de droit, P6, indique : agissant en qualité de mandataire et au nom des héritiers suivants, dont Gilles Sixte Féliho."),
   (f"Gilles Féliho n'a jamais donné mandat au notaire Félix BALLEY et n'a jamais consenti à cette mention.",None),
   ("L'article 61 du statut exige que les procurations soient annexées à l'acte ou déposées au rang des minutes. Aucune procuration n'est produite.",None),
   ("Le 28 mai 2025, P15, la preuve écrite du mandat est demandée à l'administration. Aucune réponse.",None)],a21)

def a22(T):
    c=T['c'];ce=T['ce'];T['fx'].append(('click',ce[-1]-.2))
    b=mech_row(T,1,ce[-1]-.2)+title_gear(T,2,'Tiers non partie','2023')
    b+=paper('Certificat d\'acquit · 2016','P6','<div class="serif" style="margin:0 -6px"><img src="../avocat/img/cert-deces-mandat.jpg" style="width:100%"></div><div class="sm" style="margin-top:10px">Gilles FÉLIHO : <b>représenté</b> par un mandataire</div>',c[0]+.4,60,250,540,None,'', 'l',.7)
    b+=paper('Lettre du notaire Félix BALLEY · 7 sept. 2023','P9','<div style="margin:0 -6px"><img src="../avocat/img/balley-lettre.jpg" style="width:100%"></div><div class="sm" style="margin-top:10px">Gilles FÉLIHO : <b>étranger</b> aux actes — « il n\'est pas partie »</div>',c[0]+.9,680,250,540,None,'','r',.7)
    b+=svg(wave(640,330,150,c[2]+.2)+padlock(640,330,1.6,c[2]+1.0))
    b+=E('S\'il est représenté, il est <span class="gold">partie à l\'acte</span>.<br>S\'il n\'est pas partie, <span class="gold">le mandat n\'existe pas</span>.',c[2]+.6,60,470,1160,None,'fade',.8,'lg serif center ivc')
    return b
S('a22','Acte 2 — Pignon 2','bg-navy',
  [(f"Pignon 2 : tiers non partie, en 2023. Le 7 septembre, P9, {N} écrit que les demandes portent sur la délivrance d'actes auxquels Gilles Féliho n'est pas partie.","Pignon deux : tiers non partie, en 2023. Le 7 septembre, P9, "+N+" écrit que les demandes portent sur la délivrance d'actes auxquels Gilles Féliho n'est pas partie."),
   ("Or le certificat de 2016, P6, présente Gilles Féliho comme représenté par un mandataire.",None),
   ("S'il est représenté, il est partie à l'acte. S'il n'est pas partie, le mandat n'existe pas.",None),
   ("Le certificat et la lettre ne peuvent pas être vrais ensemble.",None)],a22)

def a23(T):
    c=T['c'];ce=T['ce'];T['fx'].append(('click',ce[-1]-.2))
    b=mech_row(T,2,ce[-1]-.2)+title_gear(T,3,'Décision de justice exécutoire','2024')
    b+=pic('apdp-decision.jpg','PV de séance de l\'APDP, 19 juin 2024, p. 3/3 (P10)',c[0]+.3,60,235,700)
    ph='<div style="height:12px;background:#d9d2c0;margin:10px 0;filter:blur(2.5px);border-radius:3px"></div>'*3
    b+=paper('Décision de justice ?','',ph+'<div class="sm stone" style="margin-top:6px">sans numéro · sans juridiction · sans dispositif</div>',c[0]+1.5,830,235,390,None,'')
    b+=E('<div class="ivc" style="line-height:1.4;font-size:22px"><b class="gold">1.</b> Quelle décision ?<br><b class="gold">2.</b> Que dit son dispositif ?<br><b class="gold">3.</b> Désigne-t-elle le notaire Félix BALLEY ?</div>',c[1]+.3,830,420,390,None,'fade',.6)
    b+=paper('Jugement n° 114/14 · 31 octobre 2014','P5','<div class="qt" style="font-size:21px">« Constate » · déclare la demande irrecevable.<br><span class="red"><b>Aucun ordre adressé à un notaire.</b></span> Le notaire Félix BALLEY n\'y figure pas.</div>',c[2]+.3,60,400,700,None,'')
    b+=E('Invoquer une décision <span class="gold">ne vaut pas produire un titre.</span>',c[3]+.2,60,525,740,None,'fade',.7,'serif ivc','font-size:30px;font-weight:700')
    return b
S('a23','Acte 2 — Pignon 3','bg-navy',
  [(f"Pignon 3 : décision de justice exécutoire, en 2024. Devant l'APDP, le 19 juin, P10, {N} déclare que son action fait suite à une décision de justice devenue exécutoire.","Pignon trois : décision de justice exécutoire, en 2024. Devant l'A P D P, le 19 juin, P10, "+N+" déclare que son action fait suite à une décision de justice devenue exécutoire."),
   (f"Quelle décision ? Que dit son dispositif ? Désigne-t-elle {N} ? Aucune réponse n'est produite.",None),
   (f"Le jugement de 2014, P5, ne mentionne pas {N} et ne lui ordonne rien : il constate et déclare irrecevable.",None),
   ("Invoquer une décision ne vaut pas produire un titre.",None)],a23)

def a24(T):
    c=T['c'];ce=T['ce'];T['fx'].append(('click',ce[-1]-.2))
    b=mech_row(T,3,ce[-1]-.2)+title_gear(T,4,'Exécution partielle','2025')
    b+=pic('pv-execution.jpg','PV d\'audition du 19 mars 2025, Brigade criminelle, p. 5/5 (P11)',c[0]+.3,60,235,700)
    b+=pic('pv-dossier.jpg','PV d\'audition du 19 mars 2025, p. 2/5 (P11) : « sauf lui »',c[1]+.3,60,380,700)
    b+=paper('Code des personnes et de la famille','',f'<div class="sm"><b>Art. 940</b> : exécuteur nommé par le testateur<br><span class="red"><b>Aucune désignation produite</b></span></div><div class="sm" style="margin-top:10px"><b>Art. 941</b> : saisine limitée aux <b>meubles</b>, un an et un jour</div>',c[2]+.3,810,235,410,None,'')
    b+=E('<div class="serif md ivc"><span class="gold">Décès : 2010</span><br><span class="gold">Enregistrement de la déclaration : 2016</span><br><b>Plus de 5 ans et demi après le décès</b></div>',c[3]+.3,810,430,410,None,'fade',.6)
    return b
S('a24','Acte 2 — Pignon 4','bg-navy',
  [(f"Pignon 4 : exécution partielle, en 2025. Le 19 mars, devant la Brigade criminelle, P11, {N} déclare : « dont j'ai été saisi d'une exécution partielle ».","Pignon quatre : exécution partielle, en 2025. Le 19 mars, devant la Brigade criminelle, P11, "+N+" déclare : dont j'ai été saisi d'une exécution partielle."),
   ("Il ajoute : « Le dossier m'a été transmis par l'ensemble de la succession sauf lui ».",None),
   (f"Le Code des personnes et de la famille ne connaît qu'un exécuteur désigné par le testateur : article 940. Aucune désignation du notaire Félix BALLEY n'est produite.",None),
   ("Même un exécuteur n'a qu'une saisine limitée aux meubles, un an et un jour : article 941. Ici, la déclaration date de plus de cinq ans et demi après le décès.",None)],a24)

DOCS=[('Procuration','doc',230,160),('Acte dont il serait partie','doc',1050,160),('Décision de justice','scales',230,420),('Désignation d\'exécuteur','doc',1050,420)]
def a25(T):
    c=T['c'];ce=T['ce'];b=''
    r=''
    for i in range(4): r+=gear(900+i*53,64,20,T['s']+.2,speed=0,fill=RED,stroke=GOLD,hole='#0A1F44')
    b+=svg(r)
    b+=svg(f'<circle class="el" data-t="{c[0]:.2f}" cx="640" cy="310" r="120" fill="none" stroke="{GOLD}" stroke-width="3" stroke-dasharray="10 8"/>')
    for i,(lab,ic,x,y) in enumerate(DOCS):
        b+=E(f'<div class="paper center" style="padding:10px"><div style="display:flex;justify-content:center">{icon(ic,46)}</div><div class="sm" style="margin-top:4px">{lab}</div></div>',c[0]+.3+i*.2,x-100,y-45,200,None,'pop',.5)
    D=ce[1]-c[1]
    kf=[[c[0],595,265]]
    for i,(lab,ic,x,y) in enumerate(DOCS):
        arr=c[1]+(i+.55)*D/4
        px=x+(90 if x<640 else -90)-45;py=y+(10 if y>300 else -10)-45
        kf+=[[arr-.9,595,265],[arr,px,py],[arr+.4,px,py],[arr+1.0,595,265]]
        b+=E(f'<div style="width:204px;height:98px;background:{RED};border-radius:6px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-family:Liberation Serif,serif;font-size:24px;border:2px solid #7d1f14">FERMÉ</div>',arr+.1,x-102,y-48,204,98,'d',.35)
        T['fx'].append(('thud',arr+.2))
    kfs=json.dumps(kf)
    b+=f'<div class="el" data-t="{c[0]:.2f}" data-fn="kfd" data-kf=\'{kfs}\' style="left:0;top:0;width:90px;height:90px">{icon("person",90,"#F5F0E8")}</div>\n'
    b+=E('Chaque position <span class="gold">écarte le contrôle</span><br>qui devait vérifier la précédente.',c[2],60,500,1160,None,'fade',.8,'lg serif center ivc')
    return b
S('a25','Acte 2 — La boucle de verrouillage','bg-navy',
  [("Les quatre positions s'enchaînent en un cercle fermé.",None),
   ("Mandataire, mais aucune procuration. Tiers non partie, mais le certificat le dit représenté. Décision de justice, mais jamais produite. Exécution partielle, mais aucune désignation.",None),
   ("Chacune écarte le contrôle qui devait vérifier la précédente.",None)],a25)

def a26(T):
    c=T['c'];ce=T['ce'];b=''
    b+=pic('balley-lettre.jpg','Lettre du 7 septembre 2023 (P9) : confidentialité, absence d\'ordonnance judiciaire',c[0]+.3,60,130,740)
    b+=pic('art82.jpg','Statut du notariat, art. 82 : l\'ordonnance ne vise pas les intéressés en nom direct, héritiers ou ayants droit',c[1]+.3,60,290,740)
    b+=paper('Gilles FÉLIHO','','<div class="lg gold" style="font-size:38px">Héritier</div><div class="sm" style="margin-top:6px">Pas d\'ordonnance requise (art. 82)</div>',c[2]+.2,850,130,370,None,'gold','pop',.6)
    b+=E(f'<div style="display:flex;justify-content:center">{icon("person",96,"#F5F0E8")}</div>',c[2]+.3,1010,330,100,None,'fade',.5)
    kf=json.dumps([[c[2]+.6,820,380],[c[2]+2.2,950,380],[c[2]+2.8,950,380],[c[2]+3.6,810,380]])
    b+=f'<div class="el" data-t="{c[2]+.6:.2f}" data-fn="kfd" data-kf=\'{kf}\' style="left:0;top:0;width:60px;height:60px">{icon("key",60,GOLD)}</div>\n'
    b+=E('Le refus de communication se rattache<br>à la question du <span class="gold">prétendu mandat</span>.',c[2]+1.0,60,500,1160,None,'fade',.8,'lg serif center ivc')
    return b
S('a26','Acte 2 — Le refus d\'accès','bg-navy',
  [(f"Le refus d'accès s'inscrit dans le même mécanisme. Le 7 septembre 2023, P9, {N} invoque la confidentialité et l'absence d'ordonnance judiciaire.",None),
   ("Or l'article 82 du statut ne requiert une ordonnance que pour les personnes autres que les intéressés en nom direct, les héritiers ou les ayants droit.",None),
   ("Gilles Féliho est héritier. Le refus de communication se rattache à la question du prétendu mandat.",None)],a26)

# ====================== ACTE 3 ======================
def a31(T):
    c=T['c'];b=''
    tx,ty=500,360
    papers=[('Déclaration de décès · CNHU-HKM','P1',60,110),('PV de lecture du testament','P2',370,110),('Jugement n° 114/14','P5',680,110)]
    ln=''
    for i,(ti,p,x,y) in enumerate(papers):
        b+=paper(ti,p,'<div class="date" style="font-size:30px">3 décembre 2010</div>',c[0]+.3+i*.7,x,y,280,None,'','fade',.6)
        ln+=f'<line class="el" data-t="{c[1]+.3+i*.5:.2f}" data-fn="crack" data-len="400" data-dur=".8" x1="{x+140}" y1="{y+112}" x2="{tx}" y2="{ty}" stroke="{NAVY}" stroke-width="3"/>'
    ln+=f'<circle class="el" data-t="{c[1]+.2:.2f}" cx="{tx}" cy="{ty}" r="14" fill="{NAVY}"/>'
    b+=svg(ln)
    b+=E('<span class="serif" style="font-size:26px"><b>3 décembre 2010</b></span>',c[1]+.2,tx-120,ty+22,240,None,'fade',.5,'center')
    b+=paper('Certificat d\'acquit de droit · 20 oct. 2016','P6','<div class="date red" style="font-size:30px">10 juin 2016</div>',c[2]+.3,900,230,320,None,'red','r',.7,None,'r')
    b+=svg(wave(900,290,170,c[2]+1.0)+f'<line class="el" data-t="{c[2]+.9:.2f}" data-fn="crack" data-len="420" data-dur=".8" x1="900" y1="300" x2="{tx}" y2="{ty}" stroke="{RED}" stroke-width="4" stroke-dasharray="10 8"/>')
    b+=E('Ces pièces étaient accessibles avant l\'inscription.<br><span class="red">Il ne s\'agit pas de supposer une intention,</span> mais de constater que la vérification était possible.',c[3],60,455,1160,None,'fade',.8,'md serif center')
    return b
S('a31','Acte 3 — La preuve de l\'intention','bg-iv',
  [("Avant l'inscription au répertoire du 10 août 2016, trois pièces fixaient le décès au 3 décembre 2010 : P1, P2 et P5.",None),
   ("La déclaration de décès, le procès-verbal de lecture du testament, le jugement : trois actes publics ou judiciaires.",None),
   ("La date du 10 juin 2016 apparaît dans un acte postérieur à ces trois pièces.",None),
   ("Ces pièces étaient accessibles avant l'inscription. Il ne s'agit pas de supposer une intention, mais de constater que la vérification était possible.",None)],a31)

def a32(T):
    c=T['c'];b=''
    b+=paper('Avec la date portée au certificat · P6','',f'<div class="date">10 juin 2016</div><div class="lg" style="color:#2e8b57;margin-top:6px">2 mois</div><div class="sm">dans le délai de 6 mois (art. 438)</div>',c[0]+.3,60,100,560,None,'')
    b+=paper('Avec la date réelle · P1, P2, P5','',f'<div class="date">3 décembre 2010</div><div class="lg red" style="margin-top:6px">5 ans et 2 mois</div><div class="sm">de retard</div>',c[1]+.3,660,100,560,None,'red','fade',.6,None,'r')
    b+=pic('dgi-sollicite.jpg','Courrier DGI du 6 janvier 2025, p. 2 (P7) : certificat « sollicité par l\'Étude »',c[2]+.3,60,370,560)
    b+=pic('dgi-1428.jpg','Courrier DGI, p. 2 (P7) : déclaration enregistrée au répertoire de l\'Étude, n° 1428',c[2]+1.5,660,370,560)
    b+=E('D\'où vient la date du 10 juin 2016 ? <span class="red">Mesure n° 4.</span>',c[3],60,520,1160,None,'fade',.7,'lg serif center')
    return b
S('a32','Acte 3 — L\'utilité de la fausse date','bg-iv',
  [("La fausse date a un effet juridique immédiat : elle place la déclaration dans le délai de six mois de l'article 438.",None),
   ("Avec la vraie date, le retard est de cinq ans et deux mois.",None),
   (f"Selon la DGI, P7, le certificat a été sollicité par l'Étude du notaire Félix BALLEY, et la déclaration enregistrée dans le répertoire de l'Étude sous le numéro 1428.",None),
   ("D'où vient la date du 10 juin 2016 ? C'est l'objet de la mesure numéro 4.",None)],a32)

def a33(T):
    c=T['c'];b=''
    d0=datetime.date(2023,7,1);W=1100;span=(datetime.date(2025,6,15)-d0).days
    X=lambda y,m,d: 90+W*(datetime.date(y,m,d)-d0).days/span
    ay=300
    b+=svg(f'<line class="el" data-t="{c[0]+.2:.2f}" x1="90" y1="{ay}" x2="1190" y2="{ay}" stroke="{NAVY}" stroke-width="4"/>')
    for yy,lab in [(2024,'2024'),(2025,'2025')]:
        x=X(yy,1,1)
        b+=svg(f'<line class="el" data-t="{c[0]+.4:.2f}" x1="{x:.1f}" y1="{ay-12}" x2="{x:.1f}" y2="{ay+12}" stroke="{NAVY}" stroke-width="3"/>')
        b+=E(f'<span class="cap" style="font-size:17px"><b>{lab}</b></span>',c[0]+.4,x+4,ay-30,60,None,'fade',.4)
    b+=E('<span class="red serif" style="font-size:24px"><b>Contestations</b> de Gilles Féliho</span>',c[0]+.6,60,84,600,None,'fade',.5)
    b+=E('<span class="navy serif" style="font-size:24px"><b>Réponses</b> et auditions</span>',c[0]+.8,60,470,600,None,'fade',.5)
    cont=[((2023,8,4),'4 août 2023<br>Sommation de compulsion · P8',c[1]+.2,140,'l'),
          ((2023,10,2),'2 oct. 2023<br>Plainte devant l\'APDP',c[1]+1.6,206,'l'),
          ((2024,9,5),'5 sept. 2024<br>Sommation interpellative',c[1]+3.0,206,'c'),
          ((2025,5,28),'28 mai 2025<br>Mise en demeure · P15',c[1]+4.4,206,'r')]
    rep=[((2023,9,7),'7 sept. 2023<br>Lettre du notaire Félix BALLEY · P9',c[2]+.2,396,'l'),
         ((2023,12,27),'27 déc. 2023<br>Réponse à l\'APDP',c[2]+1.8,336,'l'),
         ((2024,6,19),'19 juin 2024<br>Audience APDP · P10',c[2]+3.2,396,'c'),
         ((2025,1,6),'6 janv. 2025<br>Observations DGI · P7',c[3]+.2,336,'c'),
         ((2025,3,19),'19 mars 2025<br>Audition Brigade criminelle · P11',c[3]+2.4,396,'r')]
    sv=''
    for lst,col in [(cont,RED),(rep,NAVY)]:
        for (dt,lab,t,ly,al) in lst:
            x=X(*dt);up=ly<ay
            ye=ly+46 if up else ly
            sv+=f'<line class="el" data-t="{t:.2f}" x1="{x:.1f}" y1="{ay}" x2="{x:.1f}" y2="{ye}" stroke="{col}" stroke-width="2"/><circle class="el" data-t="{t:.2f}" cx="{x:.1f}" cy="{ay}" r="9" fill="{col}"/>'
            w=275
            left={'l':x-4,'c':x-w/2,'r':x-w+4}[al]
            b+=E(f'<span class="sm" style="color:{col};display:block;line-height:1.25;{"text-align:right;" if al=="r" else ""}">{lab}</span>',t,left,ly,w,None,'fade',.5)
    b+=svg(sv)
    b+=E('Dans les pièces du dossier, <span class="red">aucune rectification</span> de la date du 10 juin 2016 n\'est produite.',c[4],60,512,1160,None,'fade',.8,'serif center','font-size:30px;font-weight:700')
    return b
S('a33','Acte 3 — Contestations et réponses','bg-iv',
  [("Voyons ce qui s'est passé depuis 2023. D'un côté, les contestations de Gilles Féliho. De l'autre, les réponses et les auditions.",None),
   ("Contestations : le 4 août 2023, sommation de compulsion, P8. Le 2 octobre 2023, plainte devant l'APDP. Le 5 septembre 2024, sommation interpellative. Le 28 mai 2025, mise en demeure, P15.",None),
   (f"Réponses : le 7 septembre 2023, lettre du notaire Félix BALLEY, P9. Le 27 décembre 2023, réponse à l'APDP. Le 19 juin 2024, audience devant l'APDP, P10.",None),
   ("Le 6 janvier 2025, observations de la DGI, P7 : le certificat est authentique. Le 19 mars 2025, audition devant la Brigade criminelle, P11.",None),
   ("Dans les pièces du dossier, aucune rectification de la date du 10 juin 2016 n'est produite.",None)],a33)

def a34(T):
    c=T['c'];b=''
    rows=[('145','Faux commis par un officier public dans une écriture publique','P6'),
          ('146','Constater comme vrais des faits faux, ou comme avérés des faits qui ne l\'étaient pas','P6, P7'),
          ('148','Usage de l\'acte faux','P7, P11'),
          ('153-154','Certificat inexact · document obtenu par fausse qualité (numérotation à vérifier)','P6, P8')]
    ts=[c[1]+.3,c[1]+1.4,c[2]+.3,c[2]+1.4]
    ln=''
    for i,(a,tx,p) in enumerate(rows):
        y=88+i*74
        b+=E(f'<div class="paper" style="display:flex;gap:16px;align-items:center;padding:10px 16px"><div class="serif" style="font-size:30px;font-weight:700;min-width:120px">Art. {a}</div><div class="sm" style="flex:1">{tx}</div><span class="bd r">À vérifier</span></div>',ts[i],60,y,860,None,'l',.6)
        b+=E(f'<span class="bd">{p}</span>',ts[i]+.5,1010,y+22,180,None,'fade',.5,'serif')
        ln+=f'<line class="el" data-t="{ts[i]+.4:.2f}" data-fn="crack" data-len="120" data-dur=".6" x1="920" y1="{y+30}" x2="1000" y2="{y+30}" stroke="{GOLD}" stroke-width="3"/>'
    b+=svg(ln)
    b+=paper('Ce que la loi exige','','<div class="sm">Altération frauduleuse de la vérité · écrit protégé · préjudice possible</div><div class="lg red" style="margin-top:6px;font-size:32px">L\'intention doit être établie.</div><div class="sm">C\'est l\'objet de l\'enquête sollicitée.</div>',c[3]+.3,60,402,860,None,'red','pop',.6)
    return b
S('a34','Acte 3 — La qualification pénale','bg-iv',
  [("Les textes qui suivent sont à vérifier sur le texte officiel de l'ancien code pénal, dit code Bouvenet, applicable en 2016.",None),
   ("L'article 145 vise le faux commis par un officier public dans une écriture publique. L'article 146 vise le fait de constater comme vrais des faits faux.",None),
   ("L'article 148 vise l'usage de l'acte faux. Les articles 153 et 154, pour le certificat inexact et la fausse qualité, ont une numérotation à vérifier.",None),
   ("Le faux suppose une altération frauduleuse de la vérité, un écrit protégé et un préjudice possible. L'intention doit être établie : c'est l'objet de l'enquête sollicitée.",None)],a34)

# ====================== ACTE 4 ======================
def a40(T):
    c=T['c'];b=''
    b+=svg(wave(640,290,420,c[0]+1.0,'#F5F0E8')+seal_svg(640,290,110,c[0],crack_t=c[0]+.3,ring='#8793ad'))
    b+=E('<span class="gold">10</span> mesures d\'instruction',c[0]+.6,0,450,1280,None,'fade',.9,'xl serif center ivc')
    b+=E('précises · vérifiables · contradictoires',c[1],0,520,1280,None,'fade',.8,'md serif center ivc')
    return b
S('a40','Acte 4 — Dix mesures d\'instruction','bg-navy',
  [("Face à ce verrouillage documentaire, dix mesures d'instruction sont sollicitées.",None),
   ("Elles sont précises, vérifiables et contradictoires.",None)],a40)

MES=[('bank','DGI : dossier de mutation intégral','Déclarations, annexes, bordereaux, courriers et annotations internes détenus par la DGI.','P6, P7',"Mesure 1 — DGI : l'intégralité du dossier de mutation, avec déclarations, annexes, bordereaux, courriers et annotations internes.","Mesure un : D G I : l'intégralité du dossier de mutation, avec déclarations, annexes, bordereaux, courriers et annotations internes."),
     ('doc','Procuration : original ou constat d\'absence','L\'original de la procuration, ou la constatation officielle de son absence dans les minutes et annexes.','P6, P8, P9, P15',"Mesure 2 — Procuration : son original, ou la constatation officielle de son absence dans les minutes et annexes.","Mesure deux : procuration : son original, ou la constatation officielle de son absence dans les minutes et annexes."),
     ('glass','Expertise des écritures et signatures','Comparer écritures, signatures, dates et mentions : certificat, déclaration, répertoire, pièces transmises à la DGI.','P6, P7',"Mesure 3 — Expertise : comparer écritures, signatures, dates et mentions du certificat, de la déclaration et du répertoire.","Mesure trois : expertise : comparer écritures, signatures, dates et mentions du certificat, de la déclaration et du répertoire."),
     ('finger','Traçabilité : source de la date','Identifier la personne qui a fourni la date du 10 juin 2016.','P6, P7, P11',"Mesure 4 — Traçabilité : identifier la personne qui a fourni la date du 10 juin 2016.","Mesure quatre : traçabilité : identifier la personne qui a fourni la date du 10 juin 2016."),
     ('mic','Auditions : personnel de l\'Étude','Auditionner le personnel de l\'Étude qui a préparé ou transmis la déclaration.','P11',"Mesure 5 — Auditions : le personnel de l'Étude qui a préparé ou transmis la déclaration.","Mesure cinq : auditions : le personnel de l'Étude qui a préparé ou transmis la déclaration."),
     ('mail','Échanges électroniques','Rechercher les échanges électroniques entre l\'Étude, les héritiers et la DGI.','P8, P9',"Mesure 6 — Échanges électroniques : entre l'Étude, les héritiers et la DGI.","Mesure six : échanges électroniques : entre l'Étude, les héritiers et la D G I."),
     ('scales','Accès au jugement de 2014','Vérifier si le notaire Félix BALLEY a eu accès au jugement de 2014, au vu de ses propres déclarations.','P5, P11',"Mesure 7 — Accès au jugement de 2014 : vérifier, au vu de ses propres déclarations, si le notaire Félix BALLEY y a eu accès.","Mesure sept : accès au jugement de 2014 : vérifier, au vu de ses propres déclarations, si le notaire Félix BALLEY y a eu accès."),
     ('chart','Actifs : notes d\'évaluation','Produire toute note interne d\'évaluation ou fiche de collecte des biens.','P5, P6',"Mesure 8 — Actifs : toute note interne d'évaluation ou fiche de collecte des biens.","Mesure huit : actifs : toute note interne d'évaluation ou fiche de collecte des biens."),
     ('clock','Confrontation chronologique','Confronter les contestations de Gilles Féliho et les réponses du notaire Félix BALLEY.','P8, P9, P10, P15',"Mesure 9 — Confrontation : la chronologie des contestations de Gilles Féliho et des réponses du notaire Félix BALLEY.","Mesure neuf : confrontation : la chronologie des contestations de Gilles Féliho et des réponses du notaire Félix BALLEY."),
     ('bank','Expertise immobilière indépendante','Lot 240 : déclaré 65 millions de francs CFA, loyer de la banque AIB de 60 millions en 2011. Titre foncier d\'Agla n° 2222.','P4, P5, P6',"Mesure 10 — Expertise immobilière indépendante : lot 240 (loyer AIB de 60 millions en 2011) et titre foncier d'Agla n° 2222.","Mesure dix : expertise immobilière indépendante : lot 240, loyer de la banque A I B de 60 millions en 2011, et titre foncier d'Agla numéro 2222.")]
def a41(T):
    c=T['c'];ce=T['ce'];b=''
    for i,(ic,short,det,pcs,sub,vo) in enumerate(MES):
        y=96+i*47
        b+=E(f'<div style="display:flex;gap:12px;align-items:center;font-family:Liberation Serif,serif;font-size:21px"><span style="display:inline-block;width:30px;height:30px;border-radius:50%;border:2px solid {GOLD};text-align:center;line-height:26px;font-size:17px;color:{GOLD};font-weight:700">{i+1}</span><span class="ivc">{short}</span></div>',T['s']+.3+i*.12,60,y,470,None,'fade',.4,'','',None,'data-o="0.45"')
    for i,(ic,short,det,pcs,sub,vo) in enumerate(MES):
        y=96+i*47
        xe=c[i+1] if i+1<len(c) else None
        b+=E(f'<div style="background:rgba(201,162,39,.25);border-left:6px solid {GOLD};height:42px;border-radius:4px"></div>',c[i]+.1,50,y-5,490,42,'none',.3,'','',xe)
        panel=(f'<div class="paper" style="padding:22px 26px;height:430px"><div style="display:flex;justify-content:space-between;align-items:center"><span class="bd g" style="font-size:20px">Mesure {i+1}</span><span>{"".join(badge(p.strip()) for p in pcs.split(","))}</span></div>'
               f'<div style="display:flex;justify-content:center;margin:26px 0 12px">{icon(ic,96)}</div>'
               f'<div class="serif lg center" style="font-size:32px">{short}</div><div class="md center" style="margin-top:14px;font-size:24px">{det}</div></div>')
        b+=E(panel,c[i]+.2,590,96,630,None,'fade',.5,'','',xe)
    return b
S('a41','Acte 4 — Les mesures sollicitées','bg-navy',[(m[4],m[5]) for m in MES],a41)

def a42(T):
    c=T['c'];ce=T['ce'];b='';s0=T['s']
    xs=[412,564,716,868]
    g=''
    for i,x in enumerate(xs):
        g+=gear(x,300,82,s0+.1,dir=1 if i%2==0 else -1,speed=18,fill=RED,stroke=GOLD,hole='#0A1F44',phase=15*(i%2),lock=s0+3.3,lockfill=GOLD,dx=(-200 if x<640 else 200)*(1.0 if abs(x-640)>100 else .5),dxt=s0+3.3)
    b+=svg(g)
    sq=''
    for i in range(10):
        x0=70+(i%2)*40;y0=100+i*47
        tx=560+i*12;ty=470+(0 if i<6 else (-14 if i%2 else 14))
        kf=json.dumps([[s0+.3,x0,y0],[s0+.5+i*.1,x0,y0],[s0+2.0+i*.03,tx,ty]])
        sq+=f'<rect class="el" data-t="{s0+.3:.2f}" data-fn="kfd" data-kf=\'{kf}\' x="0" y="0" width="16" height="16" fill="{GOLD}" data-x="{s0+2.5:.2f}" transform="translate({x0} {y0})"/>'
    b+=svg(sq)
    b+=f'<div class="el" data-t="{s0+2.4:.2f}" data-fn="kfd" data-kf=\'{json.dumps([[s0+2.4,590,430],[s0+3.3,590,255]])}\' style="left:0;top:0;width:100px;height:100px">{icon("key",100,GOLD)}</div>\n'
    b+=E('<span class="gold">Dix mesures.</span> Une seule finalité :<br>établir la vérité.',c[0]+.1,60,470,1160,None,'fade',.9,'xl serif center ivc')
    T['fx'].append(('click',s0+3.2));T['fx'].append(('unlock',s0+3.5))
    return b
S('a42','Acte 4 — La clé','bg-navy',[("Dix mesures. Une seule finalité : établir la vérité.",None)],a42,minlen=9,pre=4.0)

# ====================== ÉPILOGUE ======================
def e1(T):
    c=T['c'];ce=T['ce'];b=''
    b+=svg(seal_svg(640,190,90,c[0],crack_t=c[0]+1.5,ring=GOLD))
    for i in range(7):
        b+=E(icon('person',70,'#4A4A4A'),c[0]+1.0+i*.3,150+i*140,330,80,None,'fade',.6)
    texts=['La foi publique est la condition<br>de la confiance dans les actes.','Une enquête contradictoire.<br><span class="red">Les pièces-mères. L\'audition des personnes concernées.</span>','Que la justice détermine l\'origine,<br>l\'étendue et la responsabilité des faits.']
    for k,tx in enumerate(texts):
        xe=c[k+2] if k+2<len(c) else None
        b+=E(tx,c[k+1]+.2,60,430,1160,None,'fade',.8,'lg serif center',"",xe)
    return b
S('e1','Épilogue — La foi publique','bg-iv',
  [("La mécanique documentaire exposée — date de décès inexacte, mandat non prouvé, écart de valeurs non expliqué — est transposable à d'autres successions.",None),
   ("La foi publique n'est pas un ornement. C'est la condition de la confiance dans les actes.",None),
   ("Cette démonstration ne sollicite pas une sanction immédiate. Elle demande une enquête contradictoire, fondée sur la production des pièces-mères et l'audition des personnes concernées.",None),
   ("Que la justice détermine l'origine, l'étendue et la responsabilité des faits exposés.",None)],e1)

def e2(T):
    c=T['c'];b=''
    b+=E('Gilles Sixte FÉLIHO, <span class="gold">requérant</span>',c[0]+.3,0,170,1280,None,'fade',.9,'lg serif center ivc')
    b+=E('Me ATOUN Codjo Narcisse<br><span class="md" style="font-weight:400">Avocat au Barreau du Bénin</span>',c[0]+1.6,0,260,1280,None,'fade',.9,'lg serif center ivc')
    b+=E('Cotonou, le 9 octobre 2026',c[0]+3.0,0,390,1280,None,'fade',.9,'md serif center ivc')
    b+=E('wadagni2026-verite.com',c[0]+4.2,0,470,1280,None,'fade',.9,'md center gold')
    return b
S('e2',None,'bg-navy',[("Gilles Sixte Féliho, requérant. Maître Atoun Codjo Narcisse, avocat au barreau du Bénin. Cotonou, le 9 octobre 2026.",None)],e2,minlen=8)
