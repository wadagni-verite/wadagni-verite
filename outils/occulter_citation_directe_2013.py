#!/usr/bin/env python3
"""Citation directe en diffamation des 4 et 7 juin 2013 (héritiers assistés de Me Victorien Fade) : occulte l'adresse du plaignant (cité) et les
téléphones, télécopie et courriels des parties et de l'officier ministériel (rectangles noirs, contenu supprimé).
Usage : python3 -I outils/occulter_citation_directe_2013.py   (lit archives-privees/Citation directe BAH.pdf ; nécessite tesseract-ocr-fra)
Écrit : pieces/procedures-benin/citation-directe-diffamation-heritiers-2013-06.pdf"""
import os, re, glob, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = glob.glob(os.path.join(ROOT, 'archives-privees', 'Citation directe BAH*.pdf'))[0]
OUT = os.path.join(ROOT, 'pieces', 'procedures-benin', 'citation-directe-diffamation-heritiers-2013-06.pdf')
PAT = re.compile(r'T[ée]l\b|Cell\b|/fax|@|yahoo')   # lignes de coordonnées (sensible à la casse : « tel le cabinet » n'est pas une coordonnée)
d = pymupdf.open(SRC); n = 0
for p in d:
    tp = p.get_textpage_ocr(language='fra', dpi=200, full=True)
    L = {}
    for x0, y0, x1, y1, w, b, l, _ in p.get_text('words', textpage=tp):
        r = L.setdefault((b, l), [x0, y0, x1, y1, []])
        r[0] = min(r[0], x0); r[1] = min(r[1], y0); r[2] = max(r[2], x1); r[3] = max(r[3], y1); r[4].append(w)
    rects = []
    for r in L.values():
        t = ' '.join(r[4])
        if PAT.search(t): rects.append(pymupdf.Rect(r[0] - 2, r[1] - 1.5, r[2] + 2, r[3] + 1.5))
    if p.number == 0:   # adresse du plaignant (« 60 rue G. / Eiffel 94000 CRETEIL ») : la reconnaissance de texte échoue sur ce scan, zones relevées à la main (points)
        rects += [pymupdf.Rect(498, 671, 563, 698), pymupdf.Rect(86, 699, 222, 724)]
    for r in rects: p.add_redact_annot(r, fill=(0, 0, 0))
    if rects: p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    n += len(rects); print('page', p.number + 1, len(rects), 'zone(s)')
d.set_metadata({'title': 'Citation directe en diffamation (4 et 7 juin 2013) : héritiers assistés de Me Victorien Fade contre le directeur de publication de La Nation et Gilles Féliho',
                'author': 'Éthique Juridique 2.0 Internationale', 'subject': 'Coordonnées personnelles occultées (adresse, téléphones, courriels). Contenu inchangé par ailleurs.'})
try: d.rewrite_images(dpi_threshold=220, dpi_target=200, quality=82)
except Exception as e: print('(images non recompressées)', e)
d.save(OUT, garbage=4, deflate=True); print('ok', n, 'zone(s) ->', OUT)
