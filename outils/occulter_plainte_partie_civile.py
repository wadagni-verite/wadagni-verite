#!/usr/bin/env python3
"""Pièces du volet « plainte avec constitution de partie civile » : occulte les coordonnées personnelles (adresse, téléphone, courriel, naissances,
domiciles des personnes mises en cause, coordonnées du cabinet du conseil béninois) ; le récépissé du Trésor est publié tel quel.
Usage : python3 -I outils/occulter_plainte_partie_civile.py   (lit /root/.claude/uploads et images/)"""
import os, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = '/root/.claude/uploads/9ba4e719-706f-5bc5-9e72-04dc219ffae1/'
IMG = '/tmp/claude-0/-home-user-wadagni-verite/9ba4e719-706f-5bc5-9e72-04dc219ffae1/images/'
OUT = ROOT + '/pieces/procedures-benin/'
NOTICE = "Coordonnées personnelles occultées (adresses, téléphones, courriels, dates et lieux de naissance). Contenu inchangé par ailleurs."

def red(p, rects):
    for r in rects: p.add_redact_annot(pymupdf.Rect(r), fill=(0, 0, 0))
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)

def finir(d, dst, titre, notice=NOTICE):
    d.set_metadata({'title': titre, 'author': 'Éthique Juridique 2.0 Internationale', 'subject': notice})
    try: d.rewrite_images(dpi_threshold=220, dpi_target=200, quality=82)
    except Exception as e: print('  (images non recompressées)', e)
    d.save(dst, garbage=4, deflate=True); print('->', os.path.basename(dst))

d = pymupdf.open(U + 'bb00889f-Plainte_PartieCivile_DoyenJI_Cotonou_P.pdf')
red(d[0], [(60, 30, 160, 88)])                                   # p. 1 (photographie de la page déposée, cachet du tribunal) : coordonnées du plaignant
red(d[1], [(55, 71, 190, 143)])                                  # p. 2 : coordonnées du plaignant
red(d[3], [(55, 194, 520, 234), (55, 246, 520, 286), (55, 298, 520, 326), (55, 337, 520, 365)] +
          [r for t in ("60 rue Gustave EIFFEL", "94000 CRÉTEIL (FRANCE)") for r in d[3].search_for(t)])   # p. 4 : naissances et domiciles des personnes mises en cause
p = d[13]
r2 = [r for t in ("né le 12 janvier 1966 à Cotonou", "60 rue Gustave EIFFEL", "94000 CRÉTEIL (France)") for r in p.search_for(t)]
x0 = p.search_for("carré 3099/AGLA")[0].x0
red(p, r2 + [(x0 - 1, 321, 545, 336), (55, 335, 545, 352)])                           # p. 14 : naissance et adresse du plaignant ; coordonnées du cabinet du conseil (le nom reste visible)
finir(d, OUT + 'plainte-partie-civile-doyen-juges-instruction-cotonou-2025-09-29.pdf', "Plainte avec constitution de partie civile au Doyen des juges d'instruction de Cotonou, 29 septembre 2025 (12 pages, bordereau, élection de domicile)")

d = pymupdf.open(); r = pymupdf.open(IMG + '36.jpg')[0].rect
pg = d.new_page(width=595.28, height=595.28 * 1080 / 810); pg.insert_image(pg.rect, filename=IMG + '36.jpg')
finir(d, OUT + 'recepisse-tresor-plainte-3000-fcfa-2025-09-29.pdf', "Récépissé n° 25036294-026G de la Direction générale du Trésor : « PLAINTE », 3 000 FCFA, 29 septembre 2025", "Photographie du récépissé original. Contenu inchangé.")
