#!/usr/bin/env python3
"""Prépare les pièces du dossier « ministre de la Justice » : occulte (rectangles noirs, contenu supprimé) les coordonnées personnelles
et, sur les papiers à en-tête de l'avocat, son nom d'en-tête et son bloc d'adresse (téléphones, courriel, site). Les titres et diplômes
et le corps des lettres restent visibles. Usage : python3 -I outils/occulter_pieces_ministre.py   (lit /root/.claude/uploads et images/)"""
import os, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = '/root/.claude/uploads/9ba4e719-706f-5bc5-9e72-04dc219ffae1/'
IMG = '/tmp/claude-0/-home-user-wadagni-verite/9ba4e719-706f-5bc5-9e72-04dc219ffae1/images/'
OUT = ROOT + '/pieces/procedures-benin/'
META = lambda t: {'title': t, 'author': 'Éthique Juridique 2.0 Internationale', 'subject': "Coordonnées personnelles occultées. Contenu inchangé par ailleurs."}

def finir(d, dst, titre):
    d.set_metadata(META(titre))
    try: d.rewrite_images(dpi_threshold=220, dpi_target=200, quality=82)
    except Exception as e: print('  (images non recompressées)', e)
    d.save(dst, garbage=4, deflate=True); print('->', os.path.basename(dst))

def rects(p, rs):
    for r in rs: p.add_redact_annot(pymupdf.Rect(r), fill=(0, 0, 0))
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)

NOM = (44, 42, 172, 64)          # nom en en-tête (haut gauche)
def pied(y0, y1, x0=125, x1=470): return (x0, y0, x1, y1)

# 1. demande de réouverture au Procureur spécial : page 1 = copie reçue (cachet d'arrivée du 25-11-25), pages 2 à 5 = fichier d'origine
src = pymupdf.open(U + '8a2a8afc-Lettre_PS_CRIET_2.pdf')
d = pymupdf.open()
pg = d.new_page(width=595.28, height=841.89)
pg.insert_image(pg.rect, filename=IMG + '29.jpg')
d.insert_pdf(src, from_page=1, to_page=4)
import json
R1 = json.load(open(os.path.join(ROOT, 'outils', 'ministre_rects.json')))
for i, p in enumerate(d): rects(p, R1['ps'][i])
finir(d, OUT + 'demande-reouverture-procureur-special-criet-2025-11-25.pdf', "Demande de réouverture d'enquête préliminaire au Procureur spécial près la CRIET (lettre datée du 24 septembre 2025, courrier arrivé le 25 novembre 2025)")

# 2. lettre au ministre du 5 janvier 2026
d = pymupdf.open(U + '5c987214-BRW3C0AF3BD70FF_003878.pdf')
for i, p in enumerate(d): rects(p, R1['min'][i])
finir(d, OUT + 'lettre-conseil-ministre-justice-2026-01-05.pdf', "Lettre au ministre de la Justice du 5 janvier 2026")

# 3. réponse du ministre (aucune occultation : acte public)
d = pymupdf.open(U + '41593e06-L0049_14012026_Cotonou_SIDIBE_Samba_.pdf')
d.set_metadata({'title': "Réponse du ministre de la Justice et de la Législation n° 0049/MJL/SP-C du 14 janvier 2026", 'author': 'Éthique Juridique 2.0 Internationale'})
d.save(OUT + 'reponse-ministre-justice-2026-01-14.pdf', garbage=4, deflate=True); print('-> reponse-ministre-justice-2026-01-14.pdf')

# 4. lettre du 6 février 2026 (PDF texte : recherche des lignes d'adresse)
d = pymupdf.open(U + '13638598-Lettre_MLJ_B_nin.pdf')
p = d[0]
rects(p, [r for t in ("60, rue Gustave EIFFEL", "94000 CRÉTEIL", "E-mail : feliho@me.com") for r in p.search_for(t)])
finir(d, OUT + 'lettre-ministre-justice-faits-precis-2026-02-06.pdf', "Lettre au ministre de la Justice du 6 février 2026 : faits précis")

# 5. attestation d'appel du 17 novembre 2014 (photo -> PDF)
d = pymupdf.open(); img = pymupdf.open(IMG + '31.jpg'); r = img[0].rect
pg = d.new_page(width=595.28, height=595.28 * r.height / r.width); pg.insert_image(pg.rect, filename=IMG + '31.jpg')
d.set_metadata({'title': "Attestation d'appel du 17 novembre 2014 (appel n° 015/2014/3ème EP/GTC contre le jugement n° 114/14)", 'author': 'Éthique Juridique 2.0 Internationale'})
d.save(OUT + 'attestation-appel-jugement-114-14-2014-11-17.pdf', garbage=4, deflate=True); print('-> attestation-appel...')
