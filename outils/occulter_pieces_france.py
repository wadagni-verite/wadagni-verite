#!/usr/bin/env python3
"""Occulte (rectangles noirs, contenu supprimé) les coordonnées personnelles de deux pièces françaises avant publication :
  1. arrêt de la Cour d'appel de Paris du 15 février 2017 (RG 15/15518) : dates de naissance et adresses des parties (page 1),
     adresses des immeubles de France (page 3) ; les noms, les lieux de naissance étant masqués avec les dates ;
  2. procès-verbal de plainte du CSP de Créteil du 18 décembre 2015 : état civil, adresse et téléphone du plaignant (page 1).
Les noms des parties, des avocats et des magistrats sont conservés.
Usage : python3 -I outils/occulter_pieces_france.py <arret_original.pdf> <arret_occulte.pdf> <pv_original.pdf> <pv_occulte.pdf>
"""
import sys, pymupdf
arret_src, arret_dst, pv_src, pv_dst = sys.argv[1:5]

# --- 1. arrêt de la Cour d'appel de Paris
d = pymupdf.open(arret_src)
P1 = [(336, 348, 327), (348, 360, 404),            # Mme Honorine Bah : naissance, adresse
      (394, 406, 337), (406, 416, 286), (417, 426, 231),   # M. Florentin-Lin Féliho
      (451, 463, 349), (463, 474, 409),            # M. Albin Féliho
      (509, 520, 336), (521, 532, 409),            # Mme Lise Féliho
      (566, 578, 345), (578, 587, 204), (590, 598, 262),   # Mme Nina Féliho
      (681, 692, 330), (693, 702, 218), (704, 713, 198)]   # M. Gilles Féliho
for y0, y1, x1 in P1:
    d[0].add_redact_annot(pymupdf.Rect(116, y0 - 0.5, x1 + 4, y1 + 0.5), fill=(0, 0, 0))
n = len(P1)
p3 = d[2]
tp = p3.get_textpage_ocr(language='fra', dpi=300, full=True)
words = p3.get_text('words', textpage=tp)
for motif in (['11', 'rue', 'Rossini'], ['58', 'allée', 'du', 'Cèdre']):
    for i in range(len(words) - len(motif) + 1):
        if all(m in words[i + k][4] for k, m in enumerate(motif)):
            for w in words[i:i + len(motif)]:   # un rectangle par mot : le motif peut chevaucher deux lignes
                p3.add_redact_annot(pymupdf.Rect(w[0] - 2, w[1] - 0.5, w[2] + 2, w[3] + 0.5), fill=(0, 0, 0)); n += 1
for p in d:
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
d.set_metadata({'title': "Arrêt de la Cour d'appel de Paris du 15 février 2017 (RG 15/15518)", 'author': 'Éthique Juridique 2.0 Internationale',
                'subject': 'Dates de naissance et adresses de particuliers occultées. Contenu inchangé par ailleurs.'})
try: d.rewrite_images(dpi_threshold=220, dpi_target=200, quality=82)
except Exception as e: print('  (images non recompressées :', e, ')')
d.save(arret_dst, garbage=4, deflate=True)
print(n, 'zone(s) occultée(s) ->', arret_dst)

# --- 2. procès-verbal de plainte, CSP de Créteil
d = pymupdf.open(pv_src)
k = 72 / 130   # coordonnées relevées sur un rendu à 130 ppp
d[0].add_redact_annot(pymupdf.Rect(305 * k, 788 * k, 995 * k, 939 * k), fill=(0, 0, 0))   # naissance, domicile, téléphone (lignes déjà barrées au feutre sur l'original)
for p in d:
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
d.set_metadata({'title': 'Procès-verbal de plainte, CSP de Créteil, 18 décembre 2015 (P.V. n° 2015/011797)', 'author': 'Éthique Juridique 2.0 Internationale',
                'subject': 'État civil, adresse et téléphone du plaignant occultés. Contenu inchangé par ailleurs.'})
try: d.rewrite_images(dpi_threshold=220, dpi_target=200, quality=82)
except Exception as e: print('  (images non recompressées :', e, ')')
d.save(pv_dst, garbage=4, deflate=True)
print('1 zone occultée ->', pv_dst)
