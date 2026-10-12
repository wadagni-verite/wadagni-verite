# -*- coding: utf-8 -*-
"""Génère le cas pratique : page du site (noms réels), page de correspondance, et les deux versions imprimables (PDF via render)."""
import re, html, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REAL={'A':'Félix BALLEY','B':'Irène ADJAGBA ICHOLA','C':'Lazare CRINOT','R':'Gilles Féliho','X':'Albin Féliho','Y':'Lise Féliho','V':'office notarial de Vincennes'}
ANON={'A':'A','B':'B','C':'C','R':'R','X':'X','Y':'Y','V':'office notarial français'}
def sub(t,m): return re.sub(r'<([ABCRXYV])>',lambda k:m[k.group(1)],t)

TITRE_REAL="La succession Féliho : cas pratique de droit notarial et successoral (Bénin)"
TITRE_ANON="Une succession au Bénin : cas pratique de droit notarial et successoral"
NOTE=("Ce cas pratique est fondé sur des pièces publiées et sur un dossier dont l'issue n'est pas connue. Il est proposé à des fins pédagogiques. "
      "Les étudiants sont invités à former leur propre opinion à partir des seules pièces visées.")

FAITS=[
("16 juillet 2009","Un avocat rédige un testament olographe de dix feuilles (acte de dépôt, P16)."),
("3 décembre 2010","Il décède à Cotonou. L'extrait d'acte de décès est établi le 6 décembre 2010 (P1, P18)."),
("Février 2011","Entre cohéritiers, trois versions circulent sur l'origine du testament : aucun notaire ne le détiendrait ; la mère le détiendrait ; il aurait été trouvé dans les affaires du défunt (annexes de la lettre du 5 mai 2012)."),
("24 avril 2012","Le tribunal de Cotonou lit le testament, le paraphe et ordonne son retour « au Notaire pour être déposé au rang de ses minutes », celui du notaire <B> (procès-verbal de lecture, P2)."),
("25 avril et 8 mai 2012","Selon l'étude du notaire <B>, l'original lui est retourné le 25 avril, puis repris le 8 mai par deux héritiers, décharges manuscrites à l'appui (P3)."),
("30 août 2012","La cour d'appel de Cotonou nomme le notaire <C> administrateur provisoire de la succession, à la demande de l'héritier <R> (P21, P4)."),
("28 novembre 2013","Un héritier, <X>, agit « au nom et pour le compte de ses cohéritiers, à l'exception de » l'héritier <R>. Il fait mettre au rang des minutes du notaire <C> « l'original du testament », « malencontreusement certifié conforme » par le notaire <B>. La couverture du dossier porte « copie conforme » (P16). Le 30 décembre 2013, le même notaire reçoit un acte de notoriété qui énumère les cinq enfants du défunt comme héritiers (P17, P18)."),
("10 août et 20 octobre 2016","Une déclaration de succession est enregistrée au répertoire de l'Étude du notaire <A> ; le certificat d'acquit de droit du 20 octobre 2016 porte la date de décès « dix juin deux mil seize » et mentionne que le notaire <A> agit « en qualité de mandataire et au nom des héritiers », dont l'héritier <R> (P6, P7)."),
("19 mars - 24 mai 2018","Un <V> demande des informations à l'Étude du notaire <A>, qui accuse réception, puis est relancé en avril. Le 24 mai, l'<V> transmet à l'héritier <R> un fichier de trente pages : certificat, acte de dépôt, acte de notoriété (P20, P8)."),
("7 septembre 2023","Saisi de demandes de communication d'actes, le notaire <A> répond que les demandes portent sur des actes « auxquels il n'est pas partie » et invoque la confidentialité et l'absence d'ordonnance (P9)."),
]

QUESTIONS=[
("Le dessaisissement d'une minute",
 "Un notaire peut-il se dessaisir d'une minute ? À quelles conditions ? Que devient l'acte si ces conditions ne sont pas respectées ?",
 "Statut du notariat (loi n° 2002-015), art. 81 et 75.",
 "L'article 81 interdit au notaire de se dessaisir d'une minute « sauf dans les cas prévus par la loi ou en vertu d'un jugement » ; avant de s'en dessaisir, il dresse une copie dont la conformité est mentionnée par le président du tribunal de première instance, substituée à la minute. L'article 75 attache la nullité aux actes faits en contravention à l'article 81, s'ils ne sont pas revêtus de la signature de toutes les parties. À examiner : l'original du testament était-il une minute de l'étude du notaire <B> ? Une décision autorise-t-elle la reprise du 8 mai 2012 ? Une copie visée par le président du tribunal existe-t-elle ? Le procès-verbal du 24 avril 2012 vaut-il autorisation de dessaisissement, ou ordre de retour ?"),
("« Certifié conforme » et original",
 "Un acte « certifié conforme » par un notaire vaut-il original ? Qui peut mentionner la conformité d'une copie remplaçant une minute ? Que dire d'un acte qui qualifie « d'original » un exemplaire « certifié conforme » ?",
 "Statut du notariat, art. 81 ; acte de dépôt (P16), rapport de l'administrateur provisoire (P22).",
 "Une copie, même certifiée conforme, reste une copie. Dans le régime de l'article 81, la mention de conformité relève du président du tribunal, non du notaire. L'étudiant relèvera la formule de l'acte (« l'original… malencontreusement certifié conforme ») et la mention « copie conforme » de la couverture, puis envisagera les hypothèses : un original portant par erreur une mention, ou une copie qualifiée à tort d'original. Quelles preuves permettraient de trancher (examen de l'exemplaire annexé, minute, répertoire) ?"),
("Le mandat et la procuration",
 "Une mention « agissant en qualité de mandataire et au nom des héritiers » suppose-t-elle un mandat ? Comment est-il prouvé ? Quel est le rôle de l'acte de notoriété ?",
 "Statut du notariat, art. 61 ; Code des personnes et de la famille ; acte de notoriété (P17).",
 "L'article 61 impose d'annexer les procurations à l'acte ou de les déposer au rang des minutes, avec mention dans l'acte. L'acte de notoriété établit la qualité et la vocation héréditaires des personnes qui se présentent comme héritiers ; il n'établit pas le pouvoir de représenter l'un d'eux. L'étudiant examinera : une procuration est-elle produite ? Que dit l'acte du 28 novembre 2013 sur la représentation de l'héritier <R> ? La mention du certificat de 2016 peut-elle s'appuyer sur un document antérieur ?"),
("La communication des actes",
 "À qui un notaire peut-il refuser la délivrance d'actes ? Une ordonnance est-elle toujours nécessaire ? La confidentialité peut-elle être opposée à un héritier ?",
 "Statut du notariat, art. 82 ; lettre du 7 septembre 2023 (P9).",
 "L'article 82 ne requiert l'ordonnance du président du tribunal que pour les personnes autres que les intéressés en nom direct, les héritiers ou les ayants droit. L'étudiant vérifiera la qualité de l'héritier <R> (acte de notoriété, P17), puis la cohérence entre le refus (« tiers non partie ») et la mention du certificat qui le dit représenté."),
("L'acte de notoriété",
 "Que prouve un acte de notoriété après décès ? Quelle foi lui accorder ? Quelles mentions de cet acte peut-on rapprocher des autres pièces ?",
 "Acte de notoriété (P17) ; acte de dépôt (P16) ; certificat d'acquit de droit (P6).",
 "L'acte constate des déclarations de témoins sur la qualité d'héritier, la date de décès et la dévolution. Il fixe le décès au 3 décembre 2010 ; il mentionne un titre foncier 729 pour le lot 240, là où le certificat porte 739. L'étudiant distinguera ce que l'acte établit (qualité d'héritier, composition de la succession selon les déclarants) de ce qu'il n'établit pas (représentation, évaluation des biens)."),
("La date de décès et le délai de déclaration",
 "Quelle est la date de décès ? Quels documents la fixent ? Quel est le délai de déclaration de la succession et quelle différence fait la date portée au certificat ?",
 "Code général des impôts, art. 438 (délai de six mois, décès survenu au Bénin) ; P1, P2, P5, P16, P17, P18 ; P6 et P7.",
 "Six pièces fixent le décès au 3 décembre 2010 ; le certificat porte le 10 juin 2016. Avec la première date, le délai de six mois expire le 3 juin 2011 et la déclaration enregistrée le 10 août 2016 est en retard de cinq ans et deux mois ; avec la seconde, la déclaration paraît faite dans le délai. L'étudiant déterminera qui a pu fournir la date, quelles pièces étaient disponibles au moment de l'inscription, et si l'écart relève d'une erreur matérielle ou d'une autre cause, en s'en tenant aux pièces."),
("Responsabilités",
 "Quelles conséquences, pour le notaire, d'une mention de qualité non établie ? À quelles responsabilités s'expose-t-il, et comment une personne concernée peut-elle obtenir réparation ?",
 "Statut du notariat, art. 33 et 47 ; Code civil, art. 1382 (à vérifier) ; ancien code pénal applicable en 2016 (articles à vérifier) ; loi n° 64-35, art. 509 (à vérifier).",
 "L'article 47 du statut prévoit la responsabilité disciplinaire et pénale du notaire pour les fautes commises dans son ministère. L'étudiant articulera : la voie disciplinaire, la voie civile (faute, préjudice, lien de causalité), la voie pénale (faux, qui suppose une altération de la vérité, un écrit protégé, un préjudice et l'élément intentionnel) et les conséquences fiscales éventuelles pour les héritiers. Il appréciera quels éléments de preuve sont nécessaires pour chacune, et lesquels manquent à ce stade."),
]

PIEGES=[
("Un acte certifié conforme vaut-il original ?","Que signifie exactement la mention « certifié conforme », et qui peut l'apposer ?"),
("Un acte de notoriété vaut-il mandat ?","Que prouve-t-il, et que ne prouve-t-il pas ?"),
("L'absence d'une pièce prouve-t-elle son inexistence ?","Quelle différence entre « non produite à ce stade » et « inexistante » ?"),
("Une décision qui destine un dépôt à un notaire permet-elle un autre dépôt ?","Quelle autorité peut modifier la destination fixée ?"),
]
BAREME=[("Connaissance des textes",8,"Identification des articles applicables et de leur portée (statut du notariat, CPF, CGI) ; exactitude des citations."),
        ("Application aux pièces",8,"Rapprochement précis des textes et des pièces (P1 à P22), distinction entre ce que les pièces établissent et ce qu'elles n'établissent pas."),
        ("Esprit critique et objection",4,"Hypothèses alternatives, objections raisonnables, identification des pièces manquantes.")]
TEXTES=[("Statut du notariat, loi n° 2002-015 du 30 décembre 2002","art. 1, 33, 37, 47, 51 à 57, 61, 75, 76, 77, 81, 82","pieces/loi-2002-015-statut-du-notariat.pdf"),
        ("Code des personnes et de la famille, loi n° 2002-07","art. 13, 813, 881","https://wadagni2026-verite.com/"),
        ("Code général des impôts","art. 438 (délai de déclaration des successions)",None),
        ("Cour suprême du Bénin, 29 novembre 2019, arrêt n° 49/CJ-CM","obligation d'information du notaire",None)]

CSS="""
:root{--navy:#0a1f44;--blue:#1e3a8a;--gold:#d4af37;--red:#b91c1c;--gray:#6b7280;--paper:#fbf7ee;--line:#d9dde7}
*{box-sizing:border-box}body{font-family:'Inter','Liberation Sans',Arial,sans-serif;color:#1f2937;line-height:1.6;margin:0;background:#fff}
.wrap{max-width:900px;margin:0 auto;padding:0 22px}
header.h{background:linear-gradient(135deg,var(--navy),var(--blue));color:#fff;padding:40px 0 34px}
header.h a{color:rgba(255,255,255,.8);text-decoration:none;font-size:.95rem}
h1{font-family:'Merriweather','Liberation Serif',Georgia,serif;font-size:2rem;line-height:1.25;margin:16px 0 8px}
.kick{display:inline-block;background:var(--gold);color:var(--navy);font-weight:700;font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;padding:5px 12px;border-radius:4px}
h2{font-family:'Merriweather','Liberation Serif',Georgia,serif;color:var(--navy);font-size:1.45rem;border-bottom:3px solid var(--gold);display:inline-block;margin:40px 0 14px}
h3{color:var(--navy);font-size:1.1rem;margin:22px 0 6px}
.note{border-left:5px solid var(--gold);background:var(--paper);padding:12px 16px;border-radius:0 8px 8px 0;margin:18px 0;font-size:.95rem}
table{width:100%;border-collapse:collapse;font-size:.93rem;margin:10px 0}td,th{padding:9px 11px;border-top:1px solid var(--line);vertical-align:top;text-align:left}
th{background:var(--navy);color:#fff;font-size:.8rem;letter-spacing:.05em;text-transform:uppercase;border-top:0}
td.d{font-weight:700;color:var(--navy);width:21%}
.q{border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:18px 0;background:#fff}
.q .n{font-size:.78rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--red)}
.q .qq{font-weight:600;margin:4px 0 8px}.q .tx{font-size:.88rem;color:var(--gray)}
details{margin-top:8px}summary{cursor:pointer;color:var(--blue);font-weight:600}details p{margin:8px 0 0;font-size:.95rem}
ul{padding-left:22px}.pg li{margin:8px 0}
footer{border-top:1px solid var(--line);margin:50px 0 0;padding:20px 0;color:var(--gray);font-size:.88rem;text-align:center}
@media print{header.h{padding:18px 0}.q{break-inside:avoid}details{display:block}details>summary{display:none}details>p{display:block}h2{break-after:avoid}}
"""

def body(m, anon, print_mode=False):
    S=lambda t: html.escape(sub(t,m),quote=False)
    o=[]
    o.append(f'<div class="note"><b>Note.</b> {S(NOTE)}</div>')
    if anon:
        o.append('<div class="note"><b>Version anonymisée.</b> Les noms des personnes sont remplacés par des lettres (notaires A, B, C ; héritiers R, X, Y). Les dates et les numéros de pièces (P1 à P22) sont conservés : les pièces citées sont, elles, des documents authentiques.</div>')
    o.append('<h2>1. Les faits</h2><table><tr><th>Date</th><th>Fait</th></tr>'+''.join(f'<tr><td class="d">{S(d)}</td><td>{S(t)}</td></tr>' for d,t in FAITS)+'</table>')
    o.append('<h2>2. Les questions</h2><p>Chaque question est assortie des textes applicables et d\'une piste de réponse. La piste de réponse indique la règle et les éléments à examiner ; elle ne conclut pas à la place de l\'étudiant.</p>')
    for i,(t,q,tx,rep) in enumerate(QUESTIONS,1):
        o.append(f'<div class="q"><div class="n">Question {i} · {S(t)}</div><div class="qq">{S(q)}</div><div class="tx">Textes et pièces : {S(tx)}</div><details><summary>Piste de réponse</summary><p>{S(rep)}</p></details></div>')
    o.append('<h2>3. Pièges pédagogiques (sous forme de questions)</h2><ul class="pg">'+''.join(f'<li><b>{S(a)}</b> {S(b)}</li>' for a,b in PIEGES)+'</ul>')
    o.append('<h2>4. Grille de correction (20 points)</h2><table><tr><th>Compétence</th><th>Points</th><th>Critère</th></tr>'+''.join(f'<tr><td><b>{a}</b></td><td>{p}</td><td>{S(c)}</td></tr>' for a,p,c in BAREME)+'</table>')
    o.append('<h2>5. Pour aller plus loin</h2><ul>'
        '<li>Les 22 pièces du bordereau, téléchargeables : <a href="https://wadagni2026-verite.com/#bordereau">wadagni2026-verite.com/#bordereau</a></li>'
        '<li>Analyse « Où était le testament ? Chronologie et incohérences » : <a href="https://wadagni2026-verite.com/analyse-localisation-testament-par-date.html">analyse-localisation-testament-par-date.html</a></li>'
        '<li>Vidéo « La Mécanique de Verrouillage » (19 min 06) : <a href="https://wadagni2026-verite.com/#video-mecanique">wadagni2026-verite.com/#video-mecanique</a></li>'
        '</ul><h3>Textes de référence</h3><ul>'+''.join(f'<li><b>{a}</b> : {b}</li>' for a,b,_ in TEXTES)+'</ul>')
    return '\n'.join(o)

def page(title,m,anon,standalone_site):
    pass
    head=f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{CSS}</style></head><body>'
    back='<a href="index.html#documents">← Retour aux documents</a><br>' if standalone_site else ''
    hdr='<header class="h"><div class="wrap">'+back+'<span class="kick">Cas pratique · droit notarial et successoral</span><h1>'+html.escape(title)+'</h1></div></header>'
    return head+hdr+'<main class="wrap">'+body(m,anon)+'</main><footer class="wrap">'+('© 2026 Gilles FÉLIHO - Éthique Juridique 2.0 Internationale' if not anon else 'Cas pratique pédagogique · wadagni2026-verite.com')+(' · <a href="mentions-legales.html">Mentions légales</a>' if standalone_site else '')+'</footer></body></html>'

os.makedirs(os.path.join(ROOT,'outils','cas-pratique'),exist_ok=True)
site=page(TITRE_REAL,REAL,False,True)
# métadonnées de la page du site
URL="https://wadagni2026-verite.com/cas-pratique-succession-feliho.html"
IMG="https://wadagni2026-verite.com/synthese-parcours-testament.png"
DESC="Cas pratique de droit notarial et successoral (Bénin) fondé sur des pièces publiées : dix faits datés, sept questions, pistes de réponse neutres, grille de correction, versions PDF avec noms réels ou anonymisée."
import json
ld={"@context":"https://schema.org","@graph":[
 {"@type":"LearningResource","name":TITRE_REAL,"description":DESC,"inLanguage":"fr","url":URL,"image":IMG,
  "learningResourceType":"Cas pratique","educationalLevel":"Master (droit notarial, droit des successions)",
  "audience":{"@type":"EducationalAudience","educationalRole":"student"},"teaches":["Droit notarial","Droit des successions","Statut du notariat (Bénin)"],
  "datePublished":"2026-10-12","dateModified":"2026-10-12","isAccessibleForFree":True,
  "author":{"@type":"Person","name":"Gilles Féliho"},"publisher":{"@type":"Organization","name":"Wadagni 2026 Vérité","url":"https://wadagni2026-verite.com/"},
  "encoding":[{"@type":"MediaObject","name":"Version avec noms réels (PDF)","encodingFormat":"application/pdf","contentUrl":"https://wadagni2026-verite.com/cas-pratique-succession-feliho-noms-reels.pdf"},
              {"@type":"MediaObject","name":"Version anonymisée (PDF)","encodingFormat":"application/pdf","contentUrl":"https://wadagni2026-verite.com/cas-pratique-succession-anonymisee.pdf"}]},
 {"@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"Accueil","item":"https://wadagni2026-verite.com/"},
  {"@type":"ListItem","position":2,"name":"Les documents","item":"https://wadagni2026-verite.com/#documents"},
  {"@type":"ListItem","position":3,"name":"Cas pratique : la succession Féliho","item":URL}]}]}
def esc(a): return html.escape(a,quote=True)
meta=('<meta name="description" content="'+esc(DESC)+'"><meta name="robots" content="index, follow, max-image-preview:large">'
 '<link rel="canonical" href="'+URL+'">'
 '<meta property="og:type" content="article"><meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="Wadagni 2026 Vérité">'
 '<meta property="og:title" content="'+esc(TITRE_REAL)+'"><meta property="og:description" content="'+esc(DESC)+'"><meta property="og:url" content="'+URL+'"><meta property="og:image" content="'+IMG+'">'
 '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="'+esc(TITRE_REAL)+'"><meta name="twitter:description" content="'+esc(DESC)+'"><meta name="twitter:image" content="'+IMG+'">'
 '<meta property="article:published_time" content="2026-10-12">'
 '<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>')
site=site.replace('</title>','</title>'+meta,1)
dl='<div class="note"><b>Télécharger :</b> <a href="cas-pratique-succession-feliho-noms-reels.pdf" download>version avec les noms réels (PDF)</a> · <a href="cas-pratique-succession-anonymisee.pdf" download>version anonymisée (PDF)</a> · <a href="cas-pratique-correspondance.html">table de correspondance des noms</a></div>'
img='<figure style="margin:18px 0"><img src="synthese-parcours-testament.png" alt="Synthèse en une page du parcours du testament : chronologie des positions de l\'original, trois récits de février 2011, original et copie certifiée conforme, base légale exigée et produite pour chaque déplacement" style="max-width:100%;height:auto;border:1px solid #d9dde7;border-radius:10px" loading="lazy" width="1561" height="1260"><figcaption style="font-size:.88rem;color:#6b7280">Synthèse du parcours du testament (P1 à P22). <a href="analyse-localisation-testament-par-date.html">Lire l\'analyse complète</a></figcaption></figure>'
site=site.replace('<main class="wrap">','<main class="wrap">'+dl+img,1)
open(os.path.join(ROOT,'cas-pratique-succession-feliho.html'),'w',encoding='utf-8').write(site)
open(os.path.join(ROOT,'outils','cas-pratique','pdf-reel.html'),'w',encoding='utf-8').write(page(TITRE_REAL,REAL,False,False).replace('<details>','<details open>'))
open(os.path.join(ROOT,'outils','cas-pratique','pdf-anonymise.html'),'w',encoding='utf-8').write(page(TITRE_ANON,ANON,True,False).replace('<details>','<details open>'))
corr=f'''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cas pratique : table de correspondance des noms</title><meta name="robots" content="noindex"><style>{CSS}</style></head><body><header class="h"><div class="wrap"><a href="cas-pratique-succession-feliho.html">← Retour au cas pratique</a><br><span class="kick">Cas pratique</span><h1>Table de correspondance des noms</h1></div></header><main class="wrap"><div class="note">Cette page permet à l'enseignant qui utilise la version anonymisée de retrouver les personnes citées. Elle ne figure pas dans le PDF anonymisé.</div><table><tr><th>Lettre</th><th>Personne</th></tr><tr><td>Notaire A</td><td>Maître Félix BALLEY (Étude BALLEY)</td></tr><tr><td>Notaire B</td><td>Maître Irène ADJAGBA ICHOLA</td></tr><tr><td>Notaire C</td><td>Maître Lazare CRINOT</td></tr><tr><td>Héritier R</td><td>Gilles Féliho (requérant)</td></tr><tr><td>Héritier X</td><td>Albin Féliho</td></tr><tr><td>Héritière Y</td><td>Lise Féliho</td></tr><tr><td>Office notarial français</td><td>Office notarial de Vincennes</td></tr></table></main><footer class="wrap">© 2026 Gilles FÉLIHO</footer></body></html>'''
open(os.path.join(ROOT,'cas-pratique-correspondance.html'),'w',encoding='utf-8').write(corr)
print('ok')
