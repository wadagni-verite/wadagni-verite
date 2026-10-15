#!/usr/bin/env python3
"""Pièces du volet APDP : occulte (rectangles noirs, contenu supprimé) les coordonnées personnelles du plaignant (adresse, téléphone, courriel)
et du notaire (téléphones, courriels, boîte postale). Les coordonnées de l'institution (APDP) restent visibles sur les documents.
Usage : python3 -I outils/occulter_pieces_apdp.py   (lit archives-privees/ et /root/.claude/uploads)"""
import os, re, glob, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = '/root/.claude/uploads/9ba4e719-706f-5bc5-9e72-04dc219ffae1/'
A = os.path.join(ROOT, 'archives-privees') + '/'
OUT = ROOT + '/pieces/procedures-benin/'
NOTICE = "Coordonnées personnelles occultées (adresses, téléphones, courriels). Contenu inchangé par ailleurs."
PAT_LIGNE = re.compile(r'EIFFEL|CR[ÉE]TEIL|94000|0675637073|\+33|T[ée]l\.? ?[:+]|Cadi?[eèé]?[jh]ous|\b797\b', re.I)
PHRASES = ["60, rue Gustave EIFFEL", "94000 CRÉTEIL", "feliho@me.com", "feliho@me.co", "0675637073", "067563707", "+33 6 75 63 70 73",
           "02 BP 797 Cadjehoun à Cotonou - 96 36 36 76/95 85 71 22 - 21 32 15 84 Emails : felixballey@yahoo.fr etudefelixballey@outlook.fr",
           "felixballey@yahoo.fr", "etudefelixballey@outlook.fr"]

class P: mots = []

def lignes_ocr(p):
    L = {}
    P.mots = []
    for dpi in (200, 150, 300):
        tp = p.get_textpage_ocr(language='fra', dpi=dpi, full=True)
        for x0, y0, x1, y1, w, b, l, _ in p.get_text('words', textpage=tp):
            if ('@' in w or re.search(r'icloud|f[eé]li[l]?ho@|yahoo|vahoo|hotmail|outlook', w, re.I)) and not re.search(r'ap[dg]?[pdo]|apapb|spdp|contact@|gcontact|n\.issa|issa@', w, re.I):
                P.mots.append(pymupdf.Rect(x0 - 2, y0 - 1.5, x1 + 2, y1 + 1.5))
            if dpi != 200: continue
            k = (b, l); r = L.setdefault(k, [x0, y0, x1, y1, []])
            r[0] = min(r[0], x0); r[1] = min(r[1], y0); r[2] = max(r[2], x1); r[3] = max(r[3], y1); r[4].append(w)
    return [(pymupdf.Rect(r[0] - 2, r[1] - 1.5, r[2] + 2, r[3] + 1.5), ' '.join(r[4])) for r in L.values()]

def occulter(p):
    n = 0
    texte = len(p.get_text().strip()) >= 80
    rects = []
    for ph in PHRASES: rects += p.search_for(ph)
    L = lignes_ocr(p)   # OCR aussi sur les pages à couche texte : les en-têtes de courriels sont des images
    tw = [pymupdf.Rect(w[:4]) for w in p.get_text('words') if w[4].strip()]
    EXCL = re.compile(r'ap[dg]?[pdo]|apapb|spdp|contact@|gcontact|n\.issa|issa@', re.I)
    for w in p.get_text('words'):   # adresses de la couche texte
        if '@' in w[4] and not EXCL.search(w[4]): rects.append(pymupdf.Rect(w[:4]) + (-2, -1.5, 2, 1.5))
    # mots OCR : sur une page à couche texte, seulement ceux qui tombent hors du texte (images : en-têtes de courriels)
    rects += [r for r in P.mots if not texte or not any((r & t).get_area() > 0.25 * t.get_area() for t in tw)]
    if not texte:
        rects += [r for r, t in L if PAT_LIGNE.search(t) and 'apdp' not in t.lower()]
    for r in rects: p.add_redact_annot(pymupdf.Rect(r), fill=(0, 0, 0))
    if rects: p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    return len(rects)

def faire(src, dst, titre, pages=None):
    d = pymupdf.open(src)
    if pages: d.select([i - 1 for i in pages])
    n = sum(occulter(p) for p in d)
    d.set_metadata({'title': titre, 'author': 'Éthique Juridique 2.0 Internationale', 'subject': NOTICE})
    try: d.rewrite_images(dpi_threshold=220, dpi_target=200, quality=82)
    except Exception as e: print('  (images non recompressées)', e)
    d.save(OUT + dst, garbage=4, deflate=True); print(f'-> {dst} : {n} zone(s)')

PL = glob.glob(A + 'Plaintes consol*.pdf')[0]; CO = glob.glob(A + 'Communiqu*.pdf')[0]; AU = glob.glob(A + 'Audience*.pdf')[0]
faire(PL, 'apdp-plainte-notaire-balley-2023-10-02.pdf', "Plainte à l'APDP contre le notaire Félix A. Balley (2 octobre 2023, reçue le 3 octobre 2023) et ses pièces", pages=range(1, 11))
faire(PL, 'apdp-accuse-reception-2023-12-14.pdf', "APDP : accusé de réception n° 2023-1793 du 14 décembre 2023 et accusé de réception du courriel du 2 octobre 2023", pages=[11, 12])
# en-tête du courriel (image) : adresse du plaignant, zone fixe
_d = pymupdf.open(OUT + 'apdp-accuse-reception-2023-12-14.pdf'); _p = _d[1]; _f = 72 / 90
_p.add_redact_annot(pymupdf.Rect(216 * _f, 103 * _f, 362 * _f, 124 * _f), fill=(0, 0, 0))
_p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
_d.saveIncr() if False else _d.save(OUT + '_t.pdf', garbage=4, deflate=True); _d.close(); os.replace(OUT + '_t.pdf', OUT + 'apdp-accuse-reception-2023-12-14.pdf')
faire(U + 'ef234254-PV_du_19-06-24_FELIHO_vs_BALLEY.pdf', 'apdp-pv-audience-2024-06-19.pdf', "APDP : procès-verbal de séance contentieuse du 19 juin 2024")
faire(U + 'e3b1dda8-PV_du_24-07-24-_FELIHO_vs_BALLEY.pdf', 'apdp-pv-audience-2024-07-24.pdf', "APDP : procès-verbal de séance contentieuse du 24 juillet 2024")
faire(U + '4d31715b-PV_du_28-08-24-_FELIHO_vs_BALLEY.pdf', 'apdp-pv-audience-2024-08-28.pdf', "APDP : procès-verbal de séance contentieuse du 28 août 2024")
faire(U + '70bfc008-Invitation_M._FELIHO-_Octobre.pdf', 'apdp-invitation-session-2024-10-10.pdf', "APDP : invitation à la session contentieuse du 23 octobre 2024 (lettre du 10 octobre 2024)")
faire(CO, 'apdp-invitation-session-2024-12-05.pdf', "APDP : invitation à la session contentieuse du 19 décembre 2024 (lettre n° 2024-3691 du 5 décembre 2024)", pages=[2])
faire(AU, 'apdp-observations-2024-10-21.pdf', "Observations et prétentions du plaignant du 21 octobre 2024 (APDP, session du 23 octobre 2024)")
faire(CO, 'apdp-echange-communique-2024-12.pdf', "APDP : échange de courriels des 6 au 16 décembre 2024 sur le communiqué de presse du plaignant")
