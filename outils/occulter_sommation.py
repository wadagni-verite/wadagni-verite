#!/usr/bin/env python3
"""Occulte (rectangles noirs, contenu supprimé) les adresses de particuliers, téléphones et courriels de la sommation interpellative
du 3 avril 2024 (scan de 3 pages) avant publication. Les lignes sont repérées par OCR ; les noms sont conservés.
Usage : python3 -I outils/occulter_sommation.py <sommation.pdf d'origine> pieces/procedures-benin/sommation-interpellative-2024-04-03.pdf
"""
import sys, pymupdf
src, dst = sys.argv[1], sys.argv[2]
d = pymupdf.open(src)
# (page, y0, y1, mot de début, mot de fin) : mot de début/fin = fragment de mot de la ligne ; None = début/fin de ligne
CIBLES = [
    (1, 345, 360, '60,', None), (1, 362, 376, None, 'France,'),
    (1, 440, 456, None, None), (1, 457, 473, 'Email', '60,'),
    (2, 729, 749, 'demeurant', None), (2, 746, 763, None, None),
    (3, 48, 66, 'demeurant', None), (3, 60, 84, None, None), (3, 82, 99, None, None),
    (3, 109, 130, 'demeurant', None), (3, 124, 147, None, None), (3, 146, 163, None, None),
    (3, 173, 194, 'à26', None), (3, 197, 211, None, None),
    (3, 226, 243, 'demeurant', None), (3, 244, 260, None, None),
    (3, 290, 309, None, None), (3, 308, 323, None, None),
]
n = 0
for pg, y0, y1, a, b in CIBLES:
    p = d[pg - 1]
    tp = p.get_textpage_ocr(language='fra', dpi=300, full=True)
    ws = [w for w in p.get_text('words', textpage=tp) if (w[1] + w[3]) / 2 > y0 and (w[1] + w[3]) / 2 < y1]
    if not ws:
        print('  ! ligne introuvable', pg, y0); continue
    ws.sort(key=lambda w: w[0])
    i0 = next((i for i, w in enumerate(ws) if a and a in w[4]), 0)
    i1 = next((i for i in range(len(ws) - 1, -1, -1) if b and b in ws[i][4]), len(ws) - 1)
    r = pymupdf.Rect(ws[i0][0] - 2, min(w[1] for w in ws) - 2, ws[i1][2] + 3, max(w[3] for w in ws) + 2)
    p.add_redact_annot(r, fill=(0, 0, 0)); n += 1
for p in d:
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
d.set_metadata({'title': 'Sommation interpellative n° 048/2024-RY du 3 avril 2024', 'author': 'Éthique Juridique 2.0 Internationale',
                'subject': 'Coordonnées personnelles occultées (adresses, téléphones, courriel). Contenu inchangé par ailleurs.'})
try: d.rewrite_images(dpi_threshold=220, dpi_target=200, quality=82)
except Exception as e: print('  (images non recompressées :', e, ')')
d.save(dst, garbage=4, deflate=True)
print(n, 'zone(s) occultée(s) ->', dst)
