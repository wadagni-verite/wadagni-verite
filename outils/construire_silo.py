#!/usr/bin/env python3
"""Génère le silo /batonnier-hounkpatin/ (10 pages HTML) à partir de outils/silo/02-pages-du-silo-contenu.md.

Usage : python3 -I outils/construire_silo.py
À relancer après l'ajout d'une pièce dans pieces/ (la page « Sources et pièces vérifiables » recalcule
les empreintes SHA-256 des fichiers réellement en ligne) ou après une modification du contenu.
Les corrections apportées au texte d'origine sont listées dans CORRECTIONS, avec leur motif.
"""
import re, os, sys, json, hashlib, html, markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'outils', 'silo', '02-pages-du-silo-contenu.md')
SRC10 = os.path.join(ROOT, 'outils', 'silo', '10-cas-pratique-contenu.md')   # volet pédagogique (page 10)
CAS = '/batonnier-hounkpatin/cas-pratique-plainte-deontologique/'
OUT = os.path.join(ROOT, 'batonnier-hounkpatin')
SITE = 'https://wadagni2026-verite.com'
DATE = '2026-10-14'
HUB = '/batonnier-hounkpatin/'
ANCRE_HUB = 'Bâtonnier Angelo Hounkpatin — le dossier des pièces'
CONTACT = 'contact@eji2.org'

# ---------------------------------------------------------------- corrections (texte d'origine -> texte publié)
LNT21 = 'https://lanouvelletribune.info/2021/12/barreau-au-benin-me-angelo-hounkpatin-succede-dans-un-an-au-batonnier-me-prospere-ahounou/'
BWTV = 'https://beninwebtv.bj/benin-ordre-des-avocats-me-angelo-hounkpatin-designe-nouveau-batonnier/'
LNT26 = 'https://lanouvelletribune.info/2026/01/ordre-des-avocats-du-benin-me-zachari-baba-body-prend-les-renes-du-barreau/'
CORRECTIONS = [
    # (ancien, nouveau, nombre d'occurrences attendu, motif)
    ('Hungbo Klopca', 'Hungbo Kploca', 1, "graphie du jugement : HUNGBO KPLOCA"),
    ('Me Joss Arthur Ménou', 'Me Joss Arthur Medenou', 1, "graphie du jugement : Joss Arthur MEDENOU"),
    ("Aucune réponse n'est connue du plaignant à ce jour — soit quatorze mois puis vingt-cinq mois après le dépôt.",
     "Aucune réponse n'est connue du plaignant à ce jour : la relance est intervenue quatorze mois après le dépôt, la requête devant la Cour constitutionnelle vingt-cinq mois après, et quarante-deux mois se sont écoulés au 14 octobre 2026.",
     1, "calcul des délais : 2 avr. 2023 -> 14 oct. 2026 = 42 mois"),
    ('quarante-quatre mois après le dépôt de la plainte', 'quarante-deux mois après le dépôt de la plainte', 1, "calcul : 42 mois et non 44"),
    ("| 19 mars 2025 | Convocation de Me Fade par la Brigade criminelle ; non-comparution | Lettre de relance de la Brigade criminelle |\n"
     "| 17 mars 2025 | Lettre du cabinet du Bâtonnier au Procureur Général, réf. `0082/COA/BAT/AAH/2024/mp` | Transmise à la Brigade criminelle |",
     "| 17 mars 2025 | Lettre du cabinet du Bâtonnier au Procureur Général, réf. `0082/COA/BAT/AAH/2024/mp` | Transmise à la Brigade criminelle |\n"
     "| 19 mars 2025 | Convocation de Me Fade par la Brigade criminelle ; non-comparution | Lettre de relance de la Brigade criminelle |",
     1, "ordre chronologique"),
    ("la première mention écrite, dans une correspondance institutionnelle, de la lettre du cabinet du bâtonnier",
     "une mention écrite, dans une correspondance institutionnelle, de la lettre du cabinet du bâtonnier", 1,
     "« première » non vérifiable"),
    ("Elle a été adressée par courriel, puis réitérée par lettre recommandée avec accusé de réception.",
     "Elle a été adressée par courriel, puis réitérée par lettre recommandée avec accusé de réception. Un avis de réception postal, revêtu du cachet de l'Ordre des avocats du Bénin et d'un cachet postal de Cotonou daté du 20 octobre 2023, figure en page 3 du [dossier complet](/pieces/procedures-benin/plainte-deontologique-fade-dossier-complet-relance-2024-06-20.pdf) ; le texte de la plainte y figure aux pages 6 à 9.",
     1, "mode d'envoi confirmé par le plaignant et par l'avis de réception du dossier complet : mention conservée"),
    ("Le point doit être vérifié et discuté sur le texte de la décision elle-même.",
     "Le texte de la décision est publié sur le site de la Cour : [DCC 25-024](https://courconstitutionnelle.bj/fr/decisions/DCC25-024). Ce que la décision dit : saisie d'une requête relative au refus du Bâtonnier de commettre d'office des avocats à des accusés devant la CRIET, la Cour s'est saisie d'office, a rappelé l'article 7 de la Charte africaine (dont le droit d'être jugé dans un délai raisonnable) et a dit que le Bâtonnier de l'Ordre des avocats du Bénin avait violé cet article (article 3 du dispositif). Elle a aussi retenu que la suspension de la participation des avocats aux sessions criminelles portait atteinte au fonctionnement du service public de la justice.",
     1, "décision confirmée par le requérant : texte d'origine conservé, lien ajouté"),
    ("Elle s'appuie sur la décision **DCC 25-024 du 30 janvier 2025** de la Cour constitutionnelle du Bénin,",
     "Elle s'appuie sur la décision [**DCC 25-024 du 30 janvier 2025**](https://courconstitutionnelle.bj/fr/decisions/DCC25-024) de la Cour constitutionnelle du Bénin,",
     1, "lien vers le texte de la décision"),
    ("### Les trois faits de ce dossier\n",
     "### Qui est visé par ce volet ?\n\nCe volet concerne le traitement, par le Bâtonnier en exercice, **Me Angelo Hounkpatin**, de la plainte déontologique déposée contre Me Victorien Olatundji Fade. Me Fade est le mis en cause dans la plainte initiale ; Me Angelo Hounkpatin est le destinataire de cette plainte, et l'autorité dont l'absence de réponse est constatée par les pièces.\n\n### Les trois faits de ce dossier\n",
     1, "précision demandée : l'affaire dans l'affaire"),
    ("*Empreintes relevées le 14 octobre 2026 sur les fichiers reçus à cette date. Elles attestent de l'identité des fichiers publiés, non de la véracité de leur contenu.*",
     "*Les empreintes du tableau sont celles des fichiers publiés. Lorsque des coordonnées personnelles ont été occultées (rectangles noirs, contenu sous-jacent supprimé), l'empreinte de l'original non occulté est indiquée ci-dessous : son détenteur peut ainsi vérifier qu'il s'agit du même document. Elles attestent de l'identité des fichiers, non de la véracité de leur contenu.*",
     1, "empreintes des fichiers réellement publiés"),
    ("hormis l'occultation de données personnelles de tiers sans lien avec le débat.", "hormis l'occultation de coordonnées personnelles (adresses, téléphones, courriels), signalée sur cette page.", 1, "politique d'occultation du site"),
    ("Il a été élu le 18 décembre 2021, est entré en fonction le 5 janvier 2023 pour un mandat de trois ans. Selon des sources publiques, un nouveau bâtonnier a été installé le 26 janvier 2026 — information à confirmer auprès de l'Ordre des avocats du Bénin. Le dossier porte sur des actes accomplis pendant son mandat.",
     f"Non. Me Angelo Hounkpatin a été désigné le 18 décembre 2021 ([La Nouvelle Tribune]({LNT21})) et investi le 5 janvier 2023 ([Benin Web TV]({BWTV})). Son successeur, Me Zachari Baba Body, a été installé le 26 janvier 2026 ([La Nouvelle Tribune]({LNT26})). Le dossier porte sur des actes accomplis pendant son mandat.",
     1, "vérifié par recherche : sources publiques citées ; orthographe « Zachari » de la presse"),
    ("### Ce que la lettre énonce\n",
     "### Qui a signé la lettre ?\n\nLa signature n'est pas lisible sur la copie disponible : la lettre porte la mention « Le Bâtonnier » sans nom. Une autre pièce du dossier, la Déclaration de l'Ordre des avocats du Bénin du 20 août 2024 (pages 1 et 2 du [dossier complet](/pieces/procedures-benin/plainte-deontologique-fade-dossier-complet-relance-2024-06-20.pdf)), est signée « Le Bâtonnier — Angelo Aimé HOUNKPATIN » et revêtue du cachet de l'Ordre. Me Angelo Hounkpatin exerçait donc la fonction à cette date, comme le 17 mars 2025 (investi le 5 janvier 2023, successeur installé le 26 janvier 2026).\n\n### Ce que la lettre énonce\n",
     1, "identité du signataire établie par une pièce du dossier"),
    ('reponse@eji2.org', CONTACT, None, "adresse de contact existante du site (à remplacer si un alias reponse@ est créé)"),
    ("Le courriel seul ne constitue pas une preuve de date fiable ; le recommandé seul est lent.",
     "Le courriel seul est plus facile à contester ; le recommandé seul est plus lent.", 1, "formulation moins absolue"),
    ('| 31 oct. 2014 | Jugement n° 114/14/3ᵉ CH-EP, tribunal de 1ʳᵉ classe de Cotonou | Pièce n° 1 |',
     '| 31 oct. 2014 | Jugement n° 114/14/3ᵉ CH-EP, tribunal de 1ʳᵉ classe de Cotonou | Annexe n° 1 de la plainte |', 1, "évite la confusion avec la numérotation de la page des pièces"),
    ('| 9 mars 2015 | Signification du jugement à Créteil | Pièce n° 2 |',
     '| 9 mars 2015 | Signification du jugement à Créteil | Annexe n° 2 de la plainte |', 1, "idem"),
    ('| 19 déc. 2017 | Procès-verbal de compulsion (Mairie de Cotonou, IGN) | Pièce n° 3 |',
     '| 19 déc. 2017 | Procès-verbal de compulsion (Mairie de Cotonou, IGN) | Annexe n° 3 de la plainte |', 1, "idem"),
]

# ---------------------------------------------------------------- pièces publiées (page « sources »)
DOSSIER = 'pieces/procedures-benin/plainte-deontologique-fade-dossier-complet-relance-2024-06-20.pdf'
# titre, date, pages, fichier publié (ou None), empreinte de l'original non occulté (relevé du 14/10/2026), coordonnées occultées ?, renvoi
PIECES = [
    ('Plainte déontologique au Bâtonnier', '2 avr. 2023', 4, 'pieces/procedures-benin/plainte-deontologique-fade-2023-04-02.pdf', '6ef960b8e48371d945f137c84db652bbc6056475590785342f96d6fabaacb872', True, None),
    ('Relance au Bâtonnier', '20 juin 2024', 1, 'pieces/procedures-benin/relance-batonnier-2024-06-20.pdf', 'b28f60453ce57dbd33ce5401aeb9f40a5064be0aceca6d4002989e36aefc8aea', True, None),
    ('Requête devant la Cour constitutionnelle', '28 mai 2025', 3, 'pieces/procedures-benin/requete-cour-constitutionnelle-2025-05-28.pdf', 'ea75eddae5ab8a2a25918d8a407780f854f35758ed4efb87575379e4ed01d7d1', True, None),
    ('Notification de convocation n° 3081/CC/GEC', '5 août 2025', 1, 'pieces/procedures-benin/convocation-cour-constitutionnelle-recours-1471-331-2025-08-05.pdf', 'ff7ea59bdfa7de4f56449652ca4869fac6e4928a9a8e9b064ded6d69c40ff7cf', True, None),
    ('Réponse n° 269/2025 de la Brigade criminelle et annexes (version allégée)', '29 avr. 2025', 30, 'pieces/procedures-benin/observations-brigade-criminelle-cour-constitutionnelle-2025-allege.pdf', '1e3685fba3d692f8a6b4da201a57cd526bb0d86d84a2494d23b69d1e7857a3d6', True, None),
    ('Procès-verbal d\u2019audition n° 2 (pages 1, 2/5 et 5/5)', '19 mars 2025', 3, 'pieces/bac-pv-audition-2-2025-03-19.pdf', 'd3590116e5ad9de9e87f2accdf55426224571efac2ec668b87e969ae3a83f478', True, None),
    ('Jugement n° 114/14/3ᵉ CH-EP', '31 oct. 2014', 8, 'jugement-succession-feliho-2014.pdf', '81f38a3b6459bfe09335ec8b49a0330d5c4d4fc8daca750ad25dd2ea077c5d06', True, None),
    ('Signification du jugement', '9 mars 2015', 3, 'pieces/procedures-benin/plainte-fade-piece-2-signification-jugement-2015-03-09.pdf', '5946ebe64458bd2939af16ebc7ff8d4e08759f1b787a8e0e928b9f761d5fe978', True, None),
    ('Procès-verbal de compulsion', '19 déc. 2017', 3, 'pieces/pv-compulsion-parcelle-b-lot-488-2017-12.pdf', 'be038ee0706cfc627722ff667748bf334f0246996848b4af8d9b4552da21d3dd', True, None),
    ('Dossier complet (correspondances et plainte)', '2023–2025', 13, DOSSIER, '4b9eb7bcb4bc0ab914bc8c0119b15b45dba7b11a677dcededee7677e81ad6d40', True, None),
]

# ---------------------------------------------------------------- outils
def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def ko(path):
    n = os.path.getsize(path)
    return f"{n/1048576:.1f} Mo" if n >= 1048576 else f"{round(n/1024)} Ko"

def strip_md(t):
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
    t = re.sub(r'[*`]', '', t)
    return re.sub(r'\s+', ' ', t).strip()

def parse_pages(text):
    for old, new, n, why in CORRECTIONS:
        c = text.count(old)
        if n is not None and c != n:
            sys.exit(f"Correction introuvable ({c} occurrence(s), {n} attendue(s)) : {old[:70]}…")
        if n is None and c == 0:
            sys.exit(f"Correction introuvable : {old[:70]}")
        text = text.replace(old, new)
    parts = re.split(r'\n## PAGE (\d+) — [^\n]*\n', text)
    pages = []
    for i in range(1, len(parts), 2):
        num = int(parts[i]); body = parts[i + 1]
        body = body.split('\n---\n')[0] if False else re.split(r'\n---\s*(?:\n|$)', body)[0]
        meta = {}
        for key, rx in (('url', r'\*\*URL :\*\* `([^`]+)`'), ('title', r'\*\*Title :\*\* ([^\n]+)'),
                        ('desc', r'\*\*Meta description :\*\* ([^\n]+)'), ('h1', r'\*\*H1 :\*\* ([^\n]+)'),
                        ('bal', r'\*\*Balisage :\*\* ([^\n]+)')):
            m = re.search(rx, body); meta[key] = m.group(1).strip()
        content = body.split('**Balisage :**', 1)[1].split('\n', 1)[1]
        content = re.sub(r'\n\*\*Maillage sortant :\*\*[^\n]*\n', '\n', content)
        content = re.sub(r'^\s*\n', '', content)
        t, d = SEO.get(meta['url'], (None, None))
        if t: meta['title'] = t
        if d: meta['desc'] = d
        pages.append(dict(num=num, **meta, md=content))
    return pages

# titres (<= 60 car.) et descriptions (<= 155 car.) raccourcis par rapport au texte d'origine
SEO = {
    '/batonnier-hounkpatin/': ("Angelo Hounkpatin, bâtonnier : le dossier des pièces", "Plainte déontologique du 2 avril 2023 sans réponse connue, lettre du Bâtonnier du 17 mars 2025, recours devant la Cour constitutionnelle : les pièces."),
    '/batonnier-hounkpatin/plainte-deontologique-fade-2023/': ("Plainte déontologique du 2 avril 2023 : pièce par pièce", None),
    '/batonnier-hounkpatin/lettre-batonnier-procureur-general-17-mars-2025/': (None, "Analyse de la lettre du cabinet du Bâtonnier au Procureur Général du 17 mars 2025 : ce qu'elle énonce, ce que les pièces permettent de vérifier."),
    '/batonnier-hounkpatin/brigade-criminelle-reponse-29-avril-2025/': (None, "La lettre n° 269/2025 de la Brigade criminelle du 29 avril 2025 et ses neuf pièces jointes : chronologie, audition de Me Balley, points en suspens."),
    '/batonnier-hounkpatin/article-7-1-d-cadhp-delai-raisonnable/': ("Article 7-1 d) CADHP : délai raisonnable en déontologie", None),
    '/batonnier-hounkpatin/questions-frequentes/': ("Questions fréquentes — dossier Bâtonnier Angelo Hounkpatin", None),
    '/batonnier-hounkpatin/sources-et-pieces-verifiables/': ("Sources et pièces vérifiables — Angelo Hounkpatin", None),
    '/batonnier-hounkpatin/recours-contre-le-batonnier-benin-mode-emploi/': ("Plainte contre un avocat au Bénin : mode d'emploi", None),
    '/batonnier-hounkpatin/cas-pratique-plainte-deontologique/': (None, "Cas pratique de déontologie : délai raisonnable, devoir de réponse d'un ordre, preuve de l'envoi, voies de recours. Sept questions, pistes, grille."),
}

def sources_table():
    rows = ['| Pièce | Date | Pages | Fichier | Empreinte SHA-256 du fichier publié |', '|---|---|---|---|---|']
    origines = []
    for titre, date, pages, rel, orig, occ, renvoi in PIECES:
        p = os.path.join(ROOT, rel) if rel else None
        if p and os.path.exists(p):
            h = sha256(p)
            fich = f"[PDF — {ko(p)}](/{rel})" + (" · coordonnées occultées" if occ else "")
            rows.append(f"| {titre} | {date} | {pages} | {fich} | `{h}` |")
            if occ:
                origines.append((titre, orig))
        elif renvoi:
            rows.append(f"| {titre} | {date} | {pages} | [{renvoi[1]}](/{DOSSIER}) | voir le dossier complet |")
        else:
            rows.append(f"| {titre} | {date} | {pages} | en cours de versement | — |")
    out = '\n'.join(rows)
    if origines:
        out += '\n\n**Empreintes des originaux non occultés** (fichiers reçus le 14 octobre 2026), pour vérification par leur détenteur :\n\n'
        out += '\n'.join(f"- {t} : `{h}`" for t, h in origines)
        out += ("\n\nLa réponse de la Brigade criminelle (30 pages) est publiée en **version allégée** : les images des pages sont ré-encodées à 120 ppi pour un téléchargement rapide, "
                "sans changement du contenu ni de la mise en page. L'empreinte de la colonne de droite est celle du fichier allégé ; celle de l'original est donnée dans la liste ci-dessus.")
    return out

# ---------------------------------------------------------------- gabarit HTML
BANDEAU = ("<b>Cadre.</b> Ce dossier présente des pièces. Les qualifications pénales évoquées relèvent des juridictions compétentes. "
           "Aucune condamnation n'est intervenue à ce jour à l'encontre des personnes mises en cause. "
           "Les personnes citées peuvent demander l'exercice de leur droit de réponse.")
DROIT = (f"<b>Droit de réponse.</b> Toute personne nommée dans cette page peut demander la publication d'une réponse. "
         f"Écrire à <a href=\"mailto:{CONTACT}\">{CONTACT}</a> en précisant la page et le passage concernés. La réponse est publiée dans les "
         f"<b>72 heures</b>, sans modification, avec la mention de sa date. Les demandes de rectification portant sur une erreur matérielle sont traitées sous <b>48 heures</b>. "
         f"<a href=\"{HUB}droit-de-reponse-et-mises-au-point/\">Procédure complète</a>.")

def head(p, canonical, og):
    t = html.escape(p['title']); d = html.escape(p['desc'])
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Wadagni 2026 Vérité — EJI 2.0">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{og}">
<link rel="icon" type="image/png" href="/logo-eji-carre.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/batonnier-hounkpatin/assets/silo.css">
'''

def slug_of(url):
    return url.strip('/').split('/')[-1] or 'index'

def jsonld(p, pages, canonical, og, html_body):
    org = {"@type": "Organization", "@id": SITE + "/#editeur", "name": "Éthique Juridique 2.0 Internationale", "url": "https://eji2.org/",
           "identifier": "RNA W941020107",
           "address": {"@type": "PostalAddress", "streetAddress": "11 quai A. France", "postalCode": "75007", "addressLocality": "Paris", "addressCountry": "FR"}}
    art = {"@type": "Article", "@id": canonical + "#article", "headline": p['h1'][:110], "description": p['desc'],
           "datePublished": DATE, "dateModified": DATE, "inLanguage": "fr", "mainEntityOfPage": canonical, "image": og,
           "author": {"@id": SITE + "/#editeur"}, "publisher": {"@id": SITE + "/#editeur"}, "isAccessibleForFree": True}
    graph = []
    n = p['num']
    if n == 0:
        graph.append(org)
        graph.append({"@type": "Organization", "name": "Ordre des avocats du Bénin", "url": "https://barreaudubenin.bj/",
                      "address": {"@type": "PostalAddress", "streetAddress": "Maison de l'Avocat, Palais de Justice de Cotonou, 01 BP 2694", "addressLocality": "Cotonou", "addressCountry": "BJ"}})
        art["about"] = [{"@type": "Person", "name": "Angelo Hounkpatin", "jobTitle": "Avocat, ancien bâtonnier de l'Ordre des avocats du Bénin"}]
    elif n == 1:
        art["mentions"] = [{"@type": "Person", "name": "Victorien Olatundji Fade", "jobTitle": "Avocat près la Cour d'appel de Cotonou"},
                           {"@type": "Person", "name": "Gilles Sixte Féliho"}]
    graph.append(art)
    if n == 10:
        graph.append({"@type": "LearningResource", "@id": canonical + "#cas-pratique", "name": p['h1'], "description": p['desc'], "inLanguage": "fr",
                      "learningResourceType": "Cas pratique", "educationalUse": "Exercice", "educationalLevel": "Enseignement supérieur (droit, déontologie des professions juridiques)",
                      "teaches": ["Délai raisonnable (article 7-1 d de la Charte africaine)", "Devoir d'information d'un ordre professionnel", "Preuve de l'envoi et de la réception",
                                  "Faute déontologique et infraction pénale", "Voies de recours"],
                      "isAccessibleForFree": True, "creator": {"@id": SITE + "/#editeur"}, "datePublished": DATE,
                      "encoding": {"@type": "MediaObject", "contentUrl": SITE + CAS + "cas-pratique-plainte-deontologique.pdf", "encodingFormat": "application/pdf"}})
    if n == 6:
        steps = re.findall(r'^### (Étape \d+ — [^\n]+)\n\n(.+?)(?=\n### |\Z)', p['md'], re.M | re.S)
        graph.append({"@type": "HowTo", "name": "Comment saisir le Bâtonnier de l'Ordre des avocats du Bénin puis la Cour constitutionnelle",
                      "inLanguage": "fr",
                      "step": [{"@type": "HowToStep", "position": i + 1, "name": s[0].split('—', 1)[1].strip(), "text": strip_md(s[1])[:500]} for i, s in enumerate(steps)]})
    if n == 7:
        dist = []
        for titre, date, pages_, rel, att, occ, renvoi in PIECES:
            fp = os.path.join(ROOT, rel) if rel else None
            if fp and os.path.exists(fp):
                dist.append({"@type": "MediaObject", "name": titre, "contentUrl": f"{SITE}/{rel}", "encodingFormat": "application/pdf", "sha256": sha256(fp)})
        graph.append({"@type": "Dataset", "name": "Pièces du dossier Bâtonnier Hounkpatin — références et empreintes SHA-256",
                      "description": p['desc'], "inLanguage": "fr", "creator": {"@id": SITE + "/#editeur"}, "license": None, "distribution": dist})
        graph[-1].pop('license')
    if n == 9:
        qa = re.findall(r'^\*\*([^\n]+\?)\*\*\n(.+?)(?=\n\n\*\*|\n\n###|\Z)', p['md'], re.M | re.S)
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": strip_md(q), "acceptedAnswer": {"@type": "Answer", "text": strip_md(a)}} for q, a in qa]})
    crumbs = [("Accueil", SITE + "/"), ("Dossier Bâtonnier", SITE + HUB)]
    if n != 0:
        crumbs.append((p['h1'], canonical))
    graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": c[0], "item": c[1]} for i, c in enumerate(crumbs)]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)

EXERCICE = (0, 5, 6, 9)   # pages qui renvoient vers le cas pratique

def render(p, pages):
    url = p['url']; canonical = SITE + url
    slug = slug_of(url) if p['num'] else 'dossier'
    og = f"{SITE}{HUB}og/{slug}.jpg"
    md = p['md']
    if p['num'] == 7:
        md = re.sub(r'\| Pièce \| Date \| Pages \| Empreinte SHA-256 \|.*?(?=\n\n\*Les empreintes du tableau)', lambda m: sources_table(), md, flags=re.S)
    md = md.replace('### Chapô\n\n', '')
    if p['num'] in EXERCICE:
        md = md.rstrip() + f"\n\n**Pour s'exercer.** [Cas pratique : le traitement d'une plainte déontologique par un ordre d'avocats]({CAS}) — sept questions, pistes de réponse et grille de correction, en version PDF.\n"
    md = md.replace('<details class="correspondance">', '<details class="correspondance" markdown="1">')
    md = re.sub(r'^### ', '## ', md, flags=re.M)
    exts = ['tables', 'sane_lists', 'md_in_html'] + (['nl2br'] if p['num'] == 10 else [])
    body = markdown.markdown(md, extensions=exts)
    body = body.replace('<table>', '<div class="tw"><table>').replace('</table>', '</table></div>')
    crumbs = f'<nav class="fil" aria-label="Fil d\'Ariane"><a href="/">Accueil</a> › <a href="{HUB}">Dossier Bâtonnier</a>' + ('' if p['num'] == 0 else f' › <span>{html.escape(p["h1"])}</span>') + '</nav>'
    retour = '' if p['num'] == 0 else f'<p class="retour">← <a href="{HUB}">{ANCRE_HUB}</a></p>'
    page = head(p, canonical, og)
    page += f'<script type="application/ld+json">\n{jsonld(p, pages, canonical, og, body)}\n</script>\n</head>\n<body>\n'
    page += f'<div class="cadre">{BANDEAU}</div>\n'
    page += f'<header class="h"><div class="wrap"><a class="site" href="/">Wadagni 2026 Vérité · Éthique Juridique 2.0</a><span class="kick">Dossier institutionnel</span><h1>{html.escape(p["h1"])}</h1></div></header>\n'
    page += f'<main class="wrap">\n{crumbs}\n<article>\n{body}\n</article>\n{retour}\n<aside class="droit">{DROIT}</aside>\n</main>\n'
    page += (f'<footer class="wrap">© 2026 Gilles FÉLIHO — Éthique Juridique 2.0 Internationale · <a href="/mentions-legales.html">Mentions légales</a> · '
             f'<a href="{HUB}droit-de-reponse-et-mises-au-point/">Droit de réponse</a> · <a href="/">Accueil</a></footer>\n</body>\n</html>\n')
    return page, slug

def main():
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    text = open(SRC, encoding='utf-8').read() + '\n' + open(SRC10, encoding='utf-8').read()
    pages = parse_pages(text)
    assert len(pages) == 11, len(pages)
    liste = []
    for p in pages:
        out, slug = render(p, pages)
        d = OUT if p['num'] == 0 else os.path.join(OUT, slug)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)
        liste.append((p['url'], p['title'], p['desc'], slug, p['h1']))
        print(f"{len(p['title']):3d} {len(p['desc']):3d}  {p['url']}")
    json.dump(liste, open(os.path.join(ROOT, 'outils', 'silo', 'pages.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
