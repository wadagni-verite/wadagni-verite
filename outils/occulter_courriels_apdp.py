#!/usr/bin/env python3
"""Courriels échangés avec l'APDP en 2024 (captures d'écran) : occulte le téléphone et le courriel du plaignant ainsi que les
téléphones personnels des agents (rectangles noirs, contenu supprimé), puis assemble un PDF de 6 pages dans l'ordre chronologique.
Les coordonnées générales de l'institution restent visibles.
Usage : python3 -I outils/occulter_courriels_apdp.py <dossier des captures IMG_57xx.jpeg>   (nécessite tesseract-ocr, tesseract-ocr-fra)
Écrit : pieces/procedures-benin/apdp-courriels-2024.pdf  et video/apdp/img/mail-*.jpg (images du film, déjà occultées)"""
import sys, os, re, subprocess, tempfile, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1]
# (fichier, date, nom de l'image du film), ordre chronologique
ORDRE = [('IMG_5782.jpeg', '24 mai 2024', 'mail-24-05'), ('IMG_5778.jpeg', '23 juillet 2024', 'mail-23-07'), ('IMG_5783.jpeg', '24 juillet 2024', 'mail-24-07-attente'),
         ('IMG_5779.jpeg', '24 juillet 2024', 'mail-24-07-lien'), ('IMG_5781.jpeg', '24 juillet 2024', 'mail-24-07-acces'), ('IMG_5780.jpeg', '23 octobre 2024', 'mail-23-10')]
PERSO = re.compile(r'0675637073|0675|@me\.com|feliho@|^\+?229$|^9[67]$|^86$|^13$|^89$|^42$|^10$|^28$', re.I)

def mots(img):
    tsv = subprocess.run(['tesseract', img, 'stdout', '-l', 'fra', '--psm', '11', 'tsv'], capture_output=True, text=True).stdout.splitlines()[1:]
    out = []
    for l in tsv:
        c = l.split('\t')
        if len(c) == 12 and c[11].strip(): out.append((int(c[6]), int(c[7]), int(c[8]), int(c[9]), c[11].strip(), (c[2], c[3], c[4])))
    return out

# zones ajoutées à la main (px de la capture d'origine) : numéro mobile de l'agent signataire non repéré par l'OCR
MANUEL = {'IMG_5779.jpeg': [(522, 1530, 150, 32)]}

def zones(img):
    ws = mots(img); z = list(MANUEL.get(os.path.basename(img), []))
    for x, y, w, h, t, k in ws:
        if re.search(r'0675637073|@me\.com|feliho@me|icloud', t, re.I): z.append((x, y, w, h))
    # lignes de signature des agents : « Tel : +229 .. .. .. .. » (numéros mobiles personnels), repérées par mot « Tel » suivi de « +229 »
    for i, (x, y, w, h, t, k) in enumerate(ws):
        if re.fullmatch(r'Tel\.?:?', t, re.I):
            ligne = [m for m in ws if m[5] == k and m[0] >= x]
            if any(re.search(r'\+?229', m[4]) for m in ligne):
                x1 = max(m[0] + m[2] for m in ligne); z.append((x + w + 4, y, x1 - x - w + 4, h))
    return z

def main():
    doc = pymupdf.open()
    tmp = tempfile.mkdtemp()
    for f, date, nom in ORDRE:
        src = os.path.join(SRC, f)
        cmd = ['convert', src]
        for x, y, w, h in zones(src):
            cmd += ['-fill', 'black', '-draw', f'rectangle {x - 6},{y - 4} {x + w + 6},{y + h + 4}']
        cmd += ['-resize', '1400x', '-quality', '82', os.path.join(tmp, nom + '.jpg')]
        subprocess.run(cmd, check=True)
        out = os.path.join(ROOT, 'video', 'apdp', 'img', nom + '.jpg')
        subprocess.run(['cp', os.path.join(tmp, nom + '.jpg'), out], check=True)
        w, h = [int(v) for v in subprocess.check_output(['identify', '-format', '%w %h', out], text=True).split()]
        p = doc.new_page(width=595, height=595 * h / w)
        p.insert_image(p.rect, filename=out)
    doc.set_metadata({'title': "Courriels échangés avec l'APDP en 2024 (captures d'écran)", 'author': 'Éthique Juridique 2.0 Internationale',
                      'subject': 'Coordonnées personnelles occultées (téléphones, courriels). Contenu inchangé par ailleurs.'})
    doc.save(os.path.join(ROOT, 'pieces', 'procedures-benin', 'apdp-courriels-2024.pdf'), garbage=4, deflate=True)
    print('ok', len(doc), 'pages')

main()
