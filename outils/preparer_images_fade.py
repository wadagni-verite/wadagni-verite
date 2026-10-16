#!/usr/bin/env python3
"""Recadrages et surlignages (cadre doré) des pièces utilisées par le film « Où est l'acte ? » (page /avocat-fade/).
Usage : python3 -I outils/preparer_images_fade.py   (nécessite ImageMagick) ; écrit video/fade/img/*.png
Chaque image provient d'une pièce publiée sur le site ; les fractions (x0, y0, x1, y1) sont relatives à la page entière."""
import os, subprocess, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'video', 'fade', 'img'); os.makedirs(OUT, exist_ok=True)
P = 'pieces/procedures-benin/'
RI = 'pieces/reglement-interieur-harmonise-uemoa-2023.pdf'
L65 = 'pieces/loi-1965-06-organisation-du-barreau-dahomey-extrait-art-18-50.pdf'
# nom : (pdf, page (0 = première), recadrage, surlignages)
SPEC = {
 'j8c':  ('pieces/jugement-2014-p8-dispositif.pdf', 0, (0.05, 0.30, 1.0, 0.62), [(0.36, 0.455, 0.98, 0.515)]),
 'j5c':  ('pieces/jugement-2014-p5-lecture-pv.pdf', 0, (0.30, 0.55, 1.0, 0.97), [(0.335, 0.825, 0.985, 0.935)]),
 'j4c':  ('pieces/jugement-2014-p4-p5-vente-lot-488.pdf', 0, (0.30, 0.30, 1.0, 0.62), [(0.35, 0.365, 0.985, 0.48)]),
 'j1c':  ('pieces/jugement-2014-p1-parties.pdf', 0, (0.0, 0.40, 1.0, 0.80), [(0.05, 0.44, 0.34, 0.495), (0.33, 0.655, 0.985, 0.72)]),
 'pvc1c': ('pieces/pv-compulsion-parcelle-b-lot-488-2017-12.pdf', 0, (0.04, 0.50, 0.80, 0.72), [(0.06, 0.585, 0.76, 0.665)]),
 'pvc2c': ('pieces/pv-compulsion-parcelle-b-lot-488-2017-12.pdf', 1, (0.12, 0.30, 0.80, 0.80), [(0.16, 0.625, 0.75, 0.665)]),
 'gang': ('pieces/lettre-notaire-gangnito-a-me-fade-2007-09-19.pdf', 0, (0.0, 0.0, 1.0, 0.65), [(0.26, 0.34, 0.90, 0.395), (0.04, 0.515, 0.19, 0.58)]),
 'sig':  (P + 'plainte-fade-piece-2-signification-jugement-2015-03-09.pdf', 0, (0.05, 0.45, 1.0, 0.97), [(0.10, 0.52, 0.97, 0.585), (0.10, 0.86, 0.97, 0.93)]),
 'conv': (P + 'observations-brigade-criminelle-cour-constitutionnelle-2025-allege.pdf', 18, (0.0, 0.35, 0.70, 0.90), [(0.02, 0.43, 0.66, 0.545), (0.0, 0.72, 0.66, 0.84)]),
 'rel':  (P + 'relance-convocation-brigade-criminelle-2025-03-25.pdf', 0, (0.0, 0.40, 1.0, 0.75), [(0.08, 0.525, 0.90, 0.625)]),
 'bat':  (P + 'lettre-batonnier-procureur-general-2025-03-17.pdf', 0, (0.0, 0.38, 1.0, 0.72), [(0.07, 0.47, 0.95, 0.555), (0.07, 0.56, 0.95, 0.65)]),
 'pd':   (P + 'plainte-deontologique-fade-2023-04-02.pdf', 0, (0.05, 0.20, 1.0, 0.60), [(0.09, 0.36, 0.97, 0.485)]),
 'l65a': (L65, 3, (0.05, 0.15, 1.0, 0.32), [(0.14, 0.195, 0.98, 0.26)]),
 'l65b': (L65, 3, (0.05, 0.36, 1.0, 0.66), [(0.15, 0.385, 0.98, 0.535), (0.15, 0.54, 0.98, 0.645)]),
 'ri12': (RI, 11, (0.15, 0.43, 1.0, 0.75), [(0.22, 0.608, 0.90, 0.680)]),
 'ri13': (RI, 12, (0.15, 0.20, 1.0, 0.46), [(0.27, 0.328, 0.97, 0.397)]),
 'cd1':  (P + 'citation-directe-diffamation-heritiers-2013-06.pdf', 0, (0.0, 0.0, 1.0, 0.50), [(0.10, 0.255, 0.94, 0.315)]),
 'cd5':  (P + 'citation-directe-diffamation-heritiers-2013-06.pdf', 4, (0.05, 0.05, 1.0, 0.35), [(0.16, 0.15, 0.96, 0.24)]),
}
DPI = 130
for nom, (pdf, page, (cx0, cy0, cx1, cy1), hls) in SPEC.items():
    p = pymupdf.open(os.path.join(ROOT, pdf))[page]
    tmp = os.path.join(OUT, '_' + nom + '.png'); p.get_pixmap(dpi=DPI).save(tmp)
    W, H = [int(v) for v in subprocess.check_output(['identify', '-format', '%w %h', tmp], text=True).split()]
    cmd = ['convert', tmp, '-fill', 'rgba(212,175,55,0.30)', '-stroke', '#d4af37', '-strokewidth', '4']
    for x0, y0, x1, y1 in hls: cmd += ['-draw', f'roundrectangle {int(W*x0)},{int(H*y0)} {int(W*x1)},{int(H*y1)} 8,8']
    cmd += ['-crop', f'{int(W*(cx1-cx0))}x{int(H*(cy1-cy0))}+{int(W*cx0)}+{int(H*0)+0}', '+repage']
    # le recadrage vertical se règle par un second passage (convert -crop accepte x et y)
    cmd[-2] = f'{int(W*(cx1-cx0))}x{int(H*(cy1-cy0))}+{int(W*cx0)}+{int(H*cy0)}'
    cmd += [os.path.join(OUT, nom + '.png')]
    subprocess.run(cmd, check=True); os.remove(tmp)
    print(nom, 'ok')
