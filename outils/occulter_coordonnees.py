"""Occulte (rectangles noirs, contenu sous-jacent supprimé) les coordonnées personnelles dans les PDF publiés.
Usage : python3 -I outils/occulter_coordonnees.py   (lit les fichiers d'origine, écrit dans pieces/)
Les pièces occultées sont signalées comme telles sur la page « Sources et pièces vérifiables », avec l'empreinte
SHA-256 de l'original non occulté pour que le détenteur de l'original puisse vérifier.
"""
import os, sys, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = '/root/.claude/uploads/9ba4e719-706f-5bc5-9e72-04dc219ffae1/'

def appliquer(src, dst, par_page_rects, par_page_textes, notice):
    d = pymupdf.open(src)
    n = 0
    for i, p in enumerate(d, 1):
        rects = list(par_page_rects.get(i, []))
        for t in par_page_textes.get(i, []):
            rects += p.search_for(t)
        for r in rects:
            p.add_redact_annot(pymupdf.Rect(r), fill=(0, 0, 0)); n += 1
        if rects:
            p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    d.set_metadata({**d.metadata, "subject": notice, "title": os.path.basename(dst)})
    try:
        d.rewrite_images(dpi_threshold=220, dpi_target=200, quality=82)
    except Exception as e:
        print('  (images non recompressées :', e, ')')
    d.save(dst, garbage=4, deflate=True)
    print(f"{os.path.basename(dst)} : {n} zone(s) occultée(s)")

NOTICE = "Coordonnées personnelles occultées (adresse, téléphone, courriel). Contenu inchangé par ailleurs."

# Dossier complet (13 p.) : en-têtes de lettres (p. 5, 6, 10), signature de courriel (p. 4), avis de réception (p. 3)
EN_TETE = (55, 67, 200, 118)   # adresse, code postal, téléphone, courriel du plaignant (lignes 2 à 5 de l'en-tête)
appliquer(U + 'cef8d167-Plainte_contre_FADE.pdf', ROOT + '/pieces/dossier-correspondances-plainte-2023-2025.pdf',
          {3: [(338, 150, 792 * 0.72, 176), (338, 220, 554, 251)],
           4: [(170, 63, 290, 79), (410, 388, 525, 414), (410, 438, 525, 480)],
           5: [EN_TETE], 6: [EN_TETE], 10: [EN_TETE]}, {}, NOTICE)

# PV d'audition n° 2 (pages 1, 2/5, 5/5) : numéro de téléphone du témoin (page 1)
appliquer(U + 'f8dbdbab-Audition_BALLEY.pdf', ROOT + '/pieces/bac-pv-audition-2-2025-03-19.pdf',
          {1: [(445, 630, 556, 657)]}, {}, NOTICE)
