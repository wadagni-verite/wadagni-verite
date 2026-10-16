#!/usr/bin/env python3
"""Ajoute une couche texte invisible (OCR Tesseract, français) aux PDF publiés qui sont des images pures.
Usage : python3 -I outils/ocr_pieces.py   (nécessite tesseract-ocr et tesseract-ocr-fra ; idempotent)
L'image de chaque page est conservée telle quelle ; seul un calque de texte invisible (mode de rendu 3) est ajouté.
L'OCR est appliqué aux fichiers déjà occultés : les zones noires ne produisent aucun texte.
Relancer ensuite outils/construire_silo.py (les empreintes SHA-256 des fichiers publiés changent).
"""
import os, re, sys, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIBLES = [
    'jugement-succession-feliho-2014.pdf',
    'pieces/courriel-lise-gilles-feliho-2007-08-07.pdf',
    'pieces/procedures-benin/sommation-interpellative-2024-04-03.pdf',
    'pieces/bac-pv-audition-2-2025-03-19.pdf',
    'pieces/pv-compulsion-parcelle-b-lot-488-2017-12.pdf',
    'pieces/procedures-benin/lettre-batonnier-procureur-general-2025-03-17.pdf',
    'pieces/procedures-benin/transmission-procureur-general-brigade-2025-03-27.pdf',
    'pieces/procedures-benin/relance-convocation-brigade-criminelle-2025-03-25.pdf',
    'pieces/procedures-benin/observations-brigade-criminelle-cour-constitutionnelle-2025-allege.pdf',
    'pieces/procedures-benin/plainte-fade-piece-2-signification-jugement-2015-03-09.pdf',
    'pieces/procedures-benin/demande-reouverture-procureur-special-criet-2025-11-25.pdf',
    'pieces/procedures-benin/lettre-conseil-ministre-justice-2026-01-05.pdf',
    'pieces/procedures-benin/reponse-ministre-justice-2026-01-14.pdf',
    'pieces/procedures-benin/attestation-appel-jugement-114-14-2014-11-17.pdf',
    'pieces/procedures-benin/plainte-partie-civile-doyen-juges-instruction-cotonou-2025-09-29.pdf',
    'pieces/procedures-benin/recepisse-tresor-plainte-3000-fcfa-2025-09-29.pdf',
    'pieces/procedures-benin/apdp-plainte-notaire-balley-2023-10-02.pdf',
    'pieces/procedures-benin/apdp-accuse-reception-2023-12-14.pdf',
    'pieces/procedures-benin/apdp-courriels-2024.pdf',
    'pieces/procedures-benin/apdp-pv-audience-2024-06-19.pdf',
    'pieces/procedures-benin/apdp-pv-audience-2024-07-24.pdf',
    'pieces/procedures-benin/apdp-pv-audience-2024-08-28.pdf',
    'pieces/procedures-benin/apdp-invitation-session-2024-10-10.pdf',
    'pieces/procedures-benin/apdp-invitation-session-2024-12-05.pdf',
    'pieces/procedures-benin/apdp-observations-2024-10-21.pdf',
    'pieces/procedures-benin/apdp-echange-communique-2024-12.pdf',
    'pieces/procedures-benin/citation-directe-diffamation-heritiers-2013-06.pdf',
    'pieces/reglement-interieur-harmonise-uemoa-2023.pdf',
    'pieces/loi-1965-06-organisation-du-barreau-dahomey-extrait-art-18-50.pdf',
]
# lignes écartées du calque de texte : courriels et numéros de téléphone (même d'institutions), pour qu'aucune coordonnée
# ne soit indexée par les moteurs de recherche, y compris lorsqu'elle est lisible sur l'image d'origine
COORDONNEES = re.compile(r'@|(?:\+\(?\d{2,3}\)?|\b)\d{2}[\s.\-]?\d{2}[\s.\-]\d{2}[\s.\-]\d{2}\b|\bt[ée]l\b|\be-?mail\b', re.I)
SEUIL = int(os.environ.get('SEUIL', 80))   # caractères : en dessous, la page est considérée comme une image pure

def ocr(path):
    d = pymupdf.open(path)
    n = 0
    for p in d:
        if len(p.get_text().strip()) >= SEUIL:
            continue
        tp = p.get_textpage_ocr(language='fra', dpi=300, full=True)
        mots = p.get_text('words', textpage=tp)
        lignes = {}
        for w in mots:
            lignes.setdefault((w[5], w[6]), []).append(w[4])
        ecartees = {k for k, v in lignes.items() if COORDONNEES.search(' '.join(v))}
        for x0, y0, x1, y1, mot, bloc, lig, *_ in mots:
            if (bloc, lig) in ecartees:
                continue
            h = max(y1 - y0, 4)
            p.insert_text((x0, y1 - h * 0.2), mot, fontsize=h * 0.85, render_mode=3, fontname='helv')
        n += 1
    if n:
        d.saveIncr() if False else d.save(path + '.tmp', garbage=4, deflate=True)
        os.replace(path + '.tmp', path)
    print(f"{os.path.basename(path)} : {n} page(s) océrisée(s), {len(pymupdf.open(path)[0].get_text())} car. page 1")

for c in (sys.argv[1:] or CIBLES):
    ocr(os.path.join(ROOT, c))
