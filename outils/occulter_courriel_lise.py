#!/usr/bin/env python3
"""Occulte, dans le courriel de 2007 entre Gilles et Lise Féliho, les adresses électroniques, le nom d'usage de la correspondante,
l'adresse IP et l'identifiant de compte bancaire. Usage : python3 -I outils/occulter_courriel_lise.py <original.pdf> <sortie.pdf>"""
import sys, pymupdf
src, dst = sys.argv[1], sys.argv[2]
d = pymupdf.open(src)
R = {1: [(118, 109, 445, 121),   # Received : adresse IP
         (128, 137, 272, 150),   # From : adresse
         (146, 166, 242, 178),   # To : nom et adresse
         (112, 180, 304, 192),   # In-Reply-To
         (146, 208, 346, 221),   # boundary
         (318, 4, 594, 19),      # URL de la messagerie
         (440, 516, 512, 531),   # compte bancaire
         (90, 577, 218, 592)],   # « lise … a écrit »
     2: [(88, 232, 246, 253), (90, 440, 228, 453), (306, 12, 585, 31)]}
for pg, rs in R.items():
    p = d[pg - 1]
    for r in rs: p.add_redact_annot(pymupdf.Rect(r), fill=(0, 0, 0))
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
d.set_metadata({'title': 'Courriel de Gilles Féliho à Lise Féliho, 7 août 2007 (échange des 6 et 7 août 2007)', 'author': 'Éthique Juridique 2.0 Internationale',
                'subject': 'Adresses électroniques, adresse IP et coordonnées bancaires occultées. Contenu inchangé par ailleurs.'})
try: d.rewrite_images(dpi_threshold=220, dpi_target=200, quality=82)
except Exception as e: print('(images non recompressées)', e)
d.save(dst, garbage=4, deflate=True)
