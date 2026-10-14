#!/usr/bin/env python3
"""Masque (rectangles noirs, contenu sous-jacent supprimé) des coordonnées encore lisibles sur des pages scannées publiées :
adresses de particuliers, téléphones et courriels. Les en-têtes d'institutions sont conservés.
Usage : python3 -I outils/masquer_coordonnees_images.py   (idempotent ; à lancer avant outils/ocr_pieces.py si les fichiers sont régénérés)
"""
import os, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAC = 'pieces/procedures-benin/observations-brigade-criminelle-cour-constitutionnelle-2025-allege.pdf'
PVC = 'pieces/pv-compulsion-parcelle-b-lot-488-2017-12.pdf'
JUG = 'jugement-succession-feliho-2014.pdf'

MASQUES = {
    # Jugement n° 114/14/3e CH-EP, page 1 : adresses des héritiers demandeurs
    (JUG, 1): [(292, 332, 380, 350), (497, 345, 552, 363), (215, 359, 472, 382), (480, 376, 556, 394),
               (487, 409, 560, 428), (512, 440, 556, 458), (216, 466, 533, 485)],
    # Réponse de la Brigade criminelle, page 8 : signification du jugement (adresses des héritiers et de l'expéditeur, téléphones et courriels)
    (BAC, 8): [
        (68, 276, 356, 296),     # adresse de Mme Nina Féliho
        (448, 290, 508, 310), (68, 322, 94, 340),     # carré de Mme Lise Féliho
        (470, 338, 510, 358), (68, 374, 108, 392),    # carré de M. Albin Féliho
        (84, 412, 380, 440),     # adresse de M. Florentin-Lin Féliho
        (357, 462, 525, 484), (68, 484, 480, 504),    # téléphones et courriel du cabinet de l'avocat
        (483, 578, 522, 598), (68, 612, 232, 637), (226, 608, 391, 629),    # téléphones et courriel de l'étude de l'huissier
        (146, 672, 446, 700),    # adresse de M. Gilles Féliho
    ],
    # Procès-verbal de compulsion, page 1 : téléphones et courriels
    (PVC, 1): [(133, 170, 163, 179), (78, 205.5, 326, 218), (78, 454, 268, 465)],
}

for (f, n), rects in MASQUES.items():
    path = os.path.join(ROOT, f)
    d = pymupdf.open(path)
    p = d[n - 1]
    for r in rects:
        p.add_redact_annot(pymupdf.Rect(r), fill=(0, 0, 0))
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    d.save(path + '.tmp', garbage=4, deflate=True)
    os.replace(path + '.tmp', path)
    print(f"{os.path.basename(f)} p.{n} : {len(rects)} zone(s) masquée(s)")
