# -*- coding: utf-8 -*-
"""Film « L'enquête contre elle-même » : l'instruction du commissaire principal Sabi Fulbert Konto, acte par acte.
Usage : python3 build.py <dossier_modèles_kokoro> <dossier_sortie>   (voix Kokoro ff_siwis ; cache des phrases dans <sortie>/cache)
Écrit : motion.html (rendu par render.js), <sortie>/audio.wav, film.fr.srt, film.fr.vtt, timeline.json.
Chaque citation provient d'une pièce publiée sur le site ; les recadrages sont dans img/.
"""
import sys, os, json, hashlib, datetime as dt
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

models, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
SR = 24000
KONTO = "le commissaire principal Sabi Fulbert Konto"

# ------------------------------------------------------------------ texte : (sous-titre, texte lu) par séquence
SEQ = {
 1: dict(speed=1.14, gap=0.3, lead=1.4, tail=1.2, s=[
   ("Un dossier. Une Brigade criminelle. Un commissaire principal : Sabi Fulbert Konto.", "Un dossier. Une Brigade criminelle. Un commissaire principal : Sabi Fulbert Konto."),
   ("Des actes, des écrits. Les actes sont datés. Les écrits sont signés. Ce film les met en regard.", "Des actes, des écrits. Les actes sont datés. Les écrits sont signés. Ce film les met en regard.")]),
 3: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.4, s=[
   ("Le 29 avril 2025, le commissaire principal Sabi Fulbert Konto écrit à la Cour constitutionnelle du Bénin. Quatre phrases.",
    "Le vingt-neuf avril deux mille vingt-cinq, le commissaire principal Sabi Fulbert Konto écrit à la Cour constitutionnelle du Bénin. Quatre phrases."),
   ("Voyons ce que le dossier dit de chacune.", "Voyons ce que le dossier dit de chacune.")]),
 4: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.0, s=[
   ("Le 3 avril 2024, l'huissier de justice consigne la réponse du commissaire de la Brigade criminelle : « Ils seront convoqués diligemment dans les tous prochains jours pour que ce dossier soit bouclé. »",
    "Le trois avril deux mille vingt-quatre, l'huissier de justice consigne la réponse du commissaire de la Brigade criminelle : ils seront convoqués diligemment dans les tous prochains jours pour que ce dossier soit bouclé."),
   ("Le 29 avril 2025, le commissaire principal Konto écrit qu'au regard de cette sommation, le chef d'alors a dessaisi l'enquêteur et mis le dossier en instance, pour s'en occuper lui-même.",
    "Le vingt-neuf avril deux mille vingt-cinq, le commissaire principal Konto écrit qu'au regard de cette sommation, le chef d'alors a dessaisi l'enquêteur et mis le dossier en instance, pour s'en occuper lui-même."),
   ("Une sommation d'huissier, acte régulier, est devenue un « comportement ».", "Une sommation d'huissier, acte régulier, est devenue un comportement."),
   ("Le chef d'alors est décédé le 27 octobre 2024. Le dossier n'est retrouvé qu'après la notification de la Cour constitutionnelle, le 6 mars 2025.",
    "Le chef d'alors est décédé le vingt-sept octobre deux mille vingt-quatre. Le dossier n'est retrouvé qu'après la notification de la Cour constitutionnelle, le six mars deux mille vingt-cinq."),
   ("Onze mois sans acte produit. Puis six jours, de la notification de la Cour aux convocations du 12 mars.",
    "Onze mois sans acte produit. Puis six jours, de la notification de la Cour aux convocations du douze mars.")]),
 5: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.0, s=[
   ("Le 12 mars 2025, le commissaire principal Konto réquisitionne le registre foncier, aux fins de compulsion de la parcelle B du lot 488.",
    "Le douze mars deux mille vingt-cinq, le commissaire principal Konto réquisitionne le registre foncier, aux fins de compulsion de la parcelle B du lot quatre cent quatre-vingt-huit."),
   ("Le 29 avril, le mémoire qu'il signe écrit que le plaignant est « supposé détenir » les documents de cette parcelle.",
    "Le vingt-neuf avril, le mémoire qu'il signe écrit que le plaignant est supposé détenir les documents de cette parcelle."),
   ("Le même service requiert le registre du domaine, et suppose que le plaignant détient les titres.", "Le même service requiert le registre du domaine, et suppose que le plaignant détient les titres."),
   ("La mairie répond le 27 mars en joignant une page de répertoire : la couverture du registre, déjà décrite dans le procès-verbal de 2017. Elle ne mentionne aucune parcelle.",
    "La mairie répond le vingt-sept mars en joignant une page de répertoire : la couverture du registre, déjà décrite dans le procès-verbal de deux mille dix-sept. Elle ne mentionne aucune parcelle.")]),
 6: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.0, s=[
   ("La plainte déposée le 21 août 2023 porte sur un faux en écriture publique, dans un jugement.",
    "La plainte déposée le vingt et un août deux mille vingt-trois porte sur un faux en écriture publique, dans un jugement."),
   ("Le mémoire du commissaire principal Konto écrit : « Dans ladite plainte, Gilles Sixte conteste le testament. »",
    "Le mémoire du commissaire principal Konto écrit : dans ladite plainte, Gilles Sixte conteste le testament."),
   ("Toute la suite du raisonnement part de cette seconde lecture.", "Toute la suite du raisonnement part de cette seconde lecture.")]),
 7: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.0, s=[
   ("Le notaire, Maître Félix Awé Balley, est entendu le 19 mars 2025. Le procès-verbal est intitulé : audition de témoin.",
    "Le notaire, Maître Félix Awé Balley, est entendu le dix-neuf mars deux mille vingt-cinq. Le procès-verbal est intitulé : audition de témoin."),
   ("Son en-tête le range parmi les personnes soupçonnées.", "Son en-tête le range parmi les personnes soupçonnées."),
   ("Le mémoire du commissaire principal Konto écrit que la plainte vise Maître Balley.", "Le mémoire du commissaire principal Konto écrit que la plainte vise Maître Balley."),
   ("La sommation du 3 avril 2024, qui désigne les personnes à convoquer, ne le nomme pas.", "La sommation du trois avril deux mille vingt-quatre, qui désigne les personnes à convoquer, ne le nomme pas.")]),
 8: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.0, s=[
   ("La sommation désignait six personnes. Deux convocations sont produites, datées du 12 mars 2025, au nom du commissaire principal Konto.",
    "La sommation désignait six personnes. Deux convocations sont produites, datées du douze mars deux mille vingt-cinq, au nom du commissaire principal Konto."),
   ("L'une pour Maître Victorien Olatundji Fade. L'autre pour Maître Félix Awé Balley, qui n'est pas dans la liste.",
    "L'une pour Maître Victorien Olatundji Fade. L'autre pour Maître Félix Awé Balley, qui n'est pas dans la liste."),
   ("Aucune convocation n'est produite pour les quatre autres personnes, dont la magistrate qui a signé le jugement.",
    "Aucune convocation n'est produite pour les quatre autres personnes, dont la magistrate qui a signé le jugement."),
   ("Le 25 mars, le commissaire principal Konto écrit que Maître Fade a été convoqué pour le 19 mars et ne s'est pas présenté.",
    "Le vingt-cinq mars, le commissaire principal Konto écrit que Maître Fade a été convoqué pour le dix-neuf mars et ne s'est pas présenté.")]),
 9: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.2, s=[
   ("Le jugement du 31 octobre 2014 constate que Gilles Féliho a même déjà disposé de l'immeuble, et qu'il a exécuté les dispositions testamentaires de manière volontaire.",
    "Le jugement du trente et un octobre deux mille quatorze constate que Gilles Féliho a même déjà disposé de l'immeuble, et qu'il a exécuté les dispositions testamentaires de manière volontaire."),
   ("Or un testament ne prend effet qu'au décès de son auteur. Le décès est du 3 décembre 2010.",
    "Or un testament ne prend effet qu'au décès de son auteur. Le décès est du trois décembre deux mille dix."),
   ("Un testament daté de juillet 2009 ne peut constater aucun acte postérieur à la mort de son auteur.",
    "Un testament daté de juillet deux mille neuf ne peut constater aucun acte postérieur à la mort de son auteur."),
   ("Le mémoire du commissaire principal Konto écrit : « à la lecture du testament, son père a déclaré lui avoir acheté la parcelle ».",
    "Le mémoire du commissaire principal Konto écrit : à la lecture du testament, son père a déclaré lui avoir acheté la parcelle."),
   ("Un achat n'est pas un legs. Une acquisition n'est pas une disposition. Et le testament ne figure pas parmi les pièces jointes au mémoire.",
    "Un achat n'est pas un legs. Une acquisition n'est pas une disposition. Et le testament ne figure pas parmi les pièces jointes au mémoire."),
   ("Le jugement ne cite ni date, ni acte de disposition. Le mémoire non plus.", "Le jugement ne cite ni date, ni acte de disposition. Le mémoire non plus.")]),
 10: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.2, s=[
   ("Le mémoire écrit que ce jugement, ayant autorité de la chose jugée, est non assorti de recours.", "Le mémoire écrit que ce jugement, ayant autorité de la chose jugée, est non assorti de recours."),
   ("Le jugement dit : en premier ressort. Exécution provisoire. Délai d'appel : un mois.", "Le jugement dit : en premier ressort. Exécution provisoire. Délai d'appel : un mois."),
   ("La Brigade criminelle tranche ainsi une question de droit civil, qui n'est pas la sienne.", "La Brigade criminelle tranche ainsi une question de droit civil, qui n'est pas la sienne."),
   ("Devant la Cour constitutionnelle, le plaignant dénonce une usurpation des prérogatives judiciaires, sans aucune garantie procédurale.",
    "Devant la Cour constitutionnelle, le plaignant dénonce une usurpation des prérogatives judiciaires, sans aucune garantie procédurale.")]),
 11: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.0, s=[
   ("Interrogé sur les obstacles que poserait le plaignant, le notaire répond : « son objectif principal est de faire échec à l'exécution des dispositions du testament ».",
    "Interrogé sur les obstacles que poserait le plaignant, le notaire répond : son objectif principal est de faire échec à l'exécution des dispositions du testament."),
   ("Le mémoire du commissaire principal Konto rapporte cette déclaration. Aucun acte d'enquête n'est cité à son appui.",
    "Le mémoire du commissaire principal Konto rapporte cette déclaration. Aucun acte d'enquête n'est cité à son appui.")]),
 12: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.4, s=[
   ("En 2017, un huissier consigne que la mairie de Cotonou indique, pour la parcelle B du lot 488, une superficie : néant.",
    "En deux mille dix-sept, un huissier consigne que la mairie de Cotonou indique, pour la parcelle B du lot quatre cent quatre-vingt-huit, une superficie : néant."),
   ("Et que l'Institut géographique national ne dispose d'aucun document afférent.", "Et que l'Institut géographique national ne dispose d'aucun document afférent."),
   ("Ce procès-verbal ne figure pas dans le mémoire du commissaire principal Konto.", "Ce procès-verbal ne figure pas dans le mémoire du commissaire principal Konto.")]),
 13: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.2, s=[
   ("Cinq cent soixante-trois jours entre la plainte et la notification de la Cour constitutionnelle.", "Cinq cent soixante-trois jours entre la plainte et la notification de la Cour constitutionnelle."),
   ("Cinquante-quatre jours, de cette notification au mémoire du commissaire principal Konto.", "Cinquante-quatre jours, de cette notification au mémoire du commissaire principal Konto."),
   ("Le 3 juillet 2025, le parquet de la CRIET classe sans suite : « je n'ai pas estimé opportun d'engager des poursuites ».",
    "Le trois juillet deux mille vingt-cinq, le parquet de la Criet classe sans suite : je n'ai pas estimé opportun d'engager des poursuites."),
   ("Douze jours plus tard, le 15 juillet, la Cour constitutionnelle tient audience.", "Douze jours plus tard, le quinze juillet, la Cour constitutionnelle tient audience.")]),
 14: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.8, s=[
   ("Six questions pour le commissaire principal Sabi Fulbert Konto. Les réponses seront publiées.", "Six questions pour le commissaire principal Sabi Fulbert Konto. Les réponses seront publiées.")]),
}

k = Kokoro(os.path.join(models, 'kokoro.onnx'), os.path.join(models, 'voices.bin'))
t = 0.0
cues, clips, T, SEQT = [], [], {}, {}
for n in sorted(SEQ):
    q = SEQ[n]; s0 = t; c = s0 + q['lead']
    for i, (sub, voice) in enumerate(q['s']):
        ck = os.path.join(out, 'cache', hashlib.md5(f"{voice}|{q['speed']}".encode()).hexdigest() + '.npy')
        if os.path.exists(ck): x = np.load(ck)
        else:
            x, sr = k.create(voice, voice='ff_siwis', speed=q['speed'], lang='fr-fr'); assert sr == SR
            os.makedirs(os.path.dirname(ck), exist_ok=True); np.save(ck, x)
        d = len(x) / SR
        T[(n, i)] = (c, c + d); clips.append((c, x.astype(np.float32))); cues.append((c, c + d, sub)); c += d + q['gap']
    end = c - q['gap'] + q['tail']; SEQT[n] = (s0, end); t = end
FINAL = 6.0
TOTAL = t + FINAL; SEQT[15] = (t, TOTAL)

def ts(a, f='srt'):
    h = int(a // 3600); m = int(a % 3600 // 60); s = a % 60; sep = ',' if f == 'srt' else '.'
    return f"{h:02d}:{m:02d}:{int(s):02d}{sep}{int(round((s - int(s)) * 1000)):03d}"
open(os.path.join(out, 'film.fr.srt'), 'w', encoding='utf-8').write('\n'.join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{s}\n" for i, (a, b, s) in enumerate(cues)))
open(os.path.join(out, 'film.fr.vtt'), 'w', encoding='utf-8').write('WEBVTT\n\n' + '\n'.join(f"{i+1}\n{ts(a,'vtt')} --> {ts(b,'vtt')}\n{s}\n" for i, (a, b, s) in enumerate(cues)))

# ------------------------------------------------------------------ bande son : voix + note à 55 Hz (éteinte pendant les contrastes) + souffles
n_ = int((TOTAL + 1) * SR)
voice = np.zeros(n_, dtype=np.float32)
for a, x in clips:
    i = int(a * SR); voice[i:i + len(x)] += x
voice *= 0.9 / max(1e-6, np.abs(voice).max())
tt = np.arange(n_) / SR
env = np.zeros(n_, dtype=np.float32)
def seg(a, b, v):
    env[int(a * SR):int(b * SR)] = v
seg(0, SEQT[3][1], 1.0)                       # note tenue jusqu'à la fin de la séquence 3
env[:int(2 * SR)] *= np.linspace(0, 1, int(2 * SR))
fond = (10 ** (-26 / 20)) * np.sin(2 * np.pi * 55 * tt).astype(np.float32) * env   # silence pendant les contrastes (4 à 14)
rng = np.random.default_rng(11)
sfx = np.zeros(n_, dtype=np.float32)
def burst(at, dur, amp, lo, hi):
    m = int(dur * SR); x = rng.standard_normal(m).astype(np.float32)
    sp = np.fft.rfft(x); f = np.fft.rfftfreq(m, 1 / SR); sp[(f < lo) | (f > hi)] = 0
    x = np.fft.irfft(sp, m).astype(np.float32); x /= max(1e-6, np.abs(x).max()); x *= np.hanning(m).astype(np.float32) ** 0.5 * amp
    i = int(at * SR); sfx[i:i + m] += x[:max(0, min(m, n_ - i))]
for sq in (3, 4, 9, 12):                       # souffles secs, un par grand contraste
    burst(SEQT[sq][0] + 0.1, 0.4, 10 ** (-18 / 20), 400, 2500)
for key in ():   # papier / tampon, discrets
    burst(T[key][0], 0.12, 10 ** (-32 / 20), 1200, 5000)
mix = fond + sfx + voice
mix /= max(1.0, np.abs(mix).max() / 0.95)
sf.write(os.path.join(out, 'audio.wav'), mix, SR)

# ------------------------------------------------------------------ image
import subprocess, re, difflib, unicodedata
_OCR = {}
def _norm(w): return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', w.lower()).encode('ascii', 'ignore').decode())
def _words(img):
    if img not in _OCR:
        p = os.path.join(here, 'img', img)
        tsv = subprocess.run(['tesseract', p, 'stdout', '-l', 'fra', '--psm', '6', 'tsv'], capture_output=True, text=True).stdout.splitlines()[1:]
        W_ = []
        for l in tsv:
            c = l.split('\t')
            if len(c) == 12 and c[11].strip() and _norm(c[11]):
                W_.append((int(c[6]), int(c[7]), int(c[8]), int(c[9]), _norm(c[11]), (c[2], c[3], c[4])))
        _OCR[img] = W_
    return _OCR[img]
def hlfind(img, phrase):
    """rectangles (%) des lignes qui portent la phrase, repérées par OCR (fenêtre de mots la plus proche)."""
    ws = _words(img); toks = [_norm(t) for t in phrase.split() if _norm(t)]
    best, bi = 0, None
    for i in range(0, max(1, len(ws) - len(toks) + 1)):
        sc = sum(difflib.SequenceMatcher(None, ws[i + j][4], t).ratio() for j, t in enumerate(toks) if i + j < len(ws)) / len(toks)
        if sc > best: best, bi = sc, i
    if best < 0.62: print('  ! phrase non repérée', img, phrase, round(best, 2)); return []
    win = ws[bi:bi + len(toks)]
    W0, H0 = [int(x) for x in subprocess.check_output(['identify', '-format', '%w %h', os.path.join(here, 'img', img)], text=True).split()]
    lines = {}
    for (x, y, w, h, t, key) in win: lines.setdefault(key, []).append((x, y, w, h))
    out_ = []
    for key, bs in lines.items():
        x0 = min(b[0] for b in bs); y0 = min(b[1] for b in bs); x1 = max(b[0] + b[2] for b in bs); y1 = max(b[1] + b[3] for b in bs)
        out_.append((max(0, (x0 - 8) / W0 * 100), max(0, (y0 - 6) / H0 * 100), min(100, (x1 - x0 + 16) / W0 * 100), (y1 - y0 + 12) / H0 * 100))
    return out_
EL = []
def el(html, a, b=None, fade=0.5, cls='', style=''):
    b = TOTAL if b is None else b
    EL.append(f'<div class="el {cls}" data-a="{a:.2f}" data-b="{b:.2f}" data-f="{fade}" style="{style}">{html}</div>')
def card(day, mon, yr, x, y, a, b=None, cls='', label=''):
    el(f'<div class="dd">{day}</div><div class="mm">{mon}</div><div class="yy">{yr}</div>' + (f'<div class="lb">{label}</div>' if label else ''), a, b, 0.4, 'card ' + cls, f'left:{x}px;top:{y}px')
def pic(img, x, y, w, a, b, cap='', h=None, hl=(), cls='', find=()):
    hl = list(hl) + [r for ph in find for r in hlfind(img, ph)]
    boxh = f'max-height:{h}px;' if h else ''
    marks = ''.join(f'<div class="hl" style="left:{l}%;top:{tp}%;width:{wd}%;height:{ht}%"></div>' for l, tp, wd, ht in hl)
    el(f'<div class="pic" style="{boxh}"><img src="img/{img}">{marks}</div>' + (f'<div class="cap">{cap}</div>' if cap else ''), a, b, 0.5, 'piece ' + cls, f'left:{x}px;top:{y}px;width:{w}px')
def text(html, x, y, w, a, b, cls='', fade=0.6): el(html, a, b, fade, cls, f'left:{x}px;top:{y}px;width:{w}px')
def counter(num, unit, x, y, a, b, c0, c1, w=700, size=170, sub=''):
    el(f'<span class="cn" data-ca="{c0:.2f}" data-cb="{c1:.2f}" data-to="{num}">0</span><span class="cu">{unit}</span>' + (f'<div class="csub">{sub}</div>' if sub else ''), a, b, 0.6, 'counter', f'left:{x}px;top:{y}px;width:{w}px;font-size:{size}px')
def heads(a, b, l='CE QUI A ÉTÉ FAIT', r='CE QUI A ÉTÉ ÉCRIT'):
    text(l, 80, 62, 840, a, b, 'colhead'); text(r, 1000, 62, 840, a, b, 'colhead')
    el('', a, b, 0.5, 'vbar', 'left:959px;top:56px;height:880px')
def trait(a, b, y): el('', a, b, 0.2, 'trait grow', f'left:80px;top:{y}px;width:1760px;--ga:{a:.2f};--gb:{a+1.0:.2f}')
def bar(a, b): el('', a, b, 0.3, 'nada')
SQ = {n: SEQT[n] for n in SEQT}
def S(n): return SQ[n]
def W(n, i): return T[(n, i)]
def Q(n): return SQ[n][0], SQ[n][1]

el("Aucune condamnation n'est intervenue à ce jour. Les qualifications pénales relèvent des juridictions compétentes. Des contestations sont pendantes devant la Cour constitutionnelle du Bénin.", 0, TOTAL, 0.6, 'bandeau')

# --- 1 : ouverture
a, b = Q(1)
text("L'ENQUÊTE<br>CONTRE ELLE-MÊME", 160, 300, 1500, a + 0.6, b, 'title', 1.0)
text("L'instruction du commissaire principal Sabi Fulbert Konto, acte par acte", 160, 600, 1500, a + 2.4, b, 'subtitle', 1.0)

# --- 3 : les écrits
a, b = Q(3)
heads(a + 0.2, b)
qs = ["« Dans ladite plainte, Gilles Sixte conteste le testament laissé par son feu père »",
      "« à la lecture du testament […] son père a déclaré : lui avoir acheté la parcelle sise au lot 488 »",
      "« il est supposé détenir les documents relatifs à ladite parcelle »",
      "« Cette décision de justice ayant autorité de la chose jugée est non assorti de recours »"]
for i, q in enumerate(qs):
    text(f'<span class="num">{"①②③④"[i]}</span> {q}', 1000, 150 + i * 180, 840, a + 1.0 + i * 0.5, b, 'quote')
pic('m4-konto.png', 130, 330, 600, W(3, 0)[0] + 2.0, b, "Mémoire n° 268/2025 du 29 avril 2025 : signature de Sabi Fulbert Konto", cls='p3')

# --- 4 : « il dit / il fait le contraire »
a, b = Q(4)
heads(a + 0.2, b)
pic('s3-reponse.png', 80, 150, 840, W(4, 0)[0] - 0.3, W(4, 3)[0] - 0.2, "Sommation interpellative du 3 avril 2024 (acte d'huissier) : réponse consignée du commissaire de la Brigade criminelle", hl=((0, 60, 100, 40),), cls='p4')
pic('m3-instance.png', 1000, 150, 840, W(4, 1)[0] - 0.3, W(4, 3)[0] - 0.2, "Mémoire du 29 avril 2025, p. 3 — signé Sabi Fulbert Konto", find=("Au regard de ce comportement de l'huissier", "dessaisir le chargé de l'enquête en mettant le dossier en instance"), cls='p4')
pic('m3-deces.png', 1000, 420, 840, W(4, 3)[0] - 0.1, W(4, 4)[0] - 0.2, "Mémoire du 29 avril 2025, p. 3 : décès du chef d'alors ; notification de la Cour du 6 mars 2025", hl=((0, 14, 100, 16),), find=("06 mars 2025",), cls='p4')
counter(11, 'MOIS', 80, 330, W(4, 4)[0] - 0.2, b, W(4, 4)[0], W(4, 4)[0] + 2.0, w=800, size=190, sub="du 3 avril 2024 au 6 mars 2025")
counter(6, 'JOURS', 1000, 330, W(4, 4)[0] + 2.2, b, W(4, 4)[0] + 2.4, W(4, 4)[0] + 3.6, w=840, size=190, sub="de la notification de la Cour (6 mars) aux convocations du 12 mars")

# --- 5 : la réquisition contre « supposé détenir »
a, b = Q(5)
heads(a + 0.2, b)
pic('q-requisition.png', 80, 150, 840, W(5, 0)[0] - 0.3, W(5, 3)[0] - 0.2, "Réquisition n° 60/2025, procédure n° 134/2025 : Sabi Fulbert Konto, commissaire principal, assisté de Boni C. Maurice", h=730, find=("Bien vouloir mettre le registre foncier à la disposition des enquêteurs aux fins de compulsion de la parcelle B du lot 488",), cls='p5')
pic('m4-detenir.png', 1000, 150, 840, W(5, 1)[0] - 0.3, W(5, 3)[0] - 0.2, "Mémoire du 29 avril 2025, p. 4 — signé Sabi Fulbert Konto", find=("supposé détenir les documents relatifs à ladite parcelle",), cls='p5')
trait(W(5, 2)[0], W(5, 3)[0] - 0.2, 590)
pic('q-repertoire.png', 80, 150, 520, W(5, 3)[0] - 0.1, b, "Page jointe à la lettre de la mairie du 27 mars 2025 : couverture du registre « Cotonou 475 à 675, n° 216 », décrite dans le procès-verbal de 2017", h=720, cls='p5')
text("Mairie de Cotonou, 27 mars 2025 :<br>« je vous informe que la copie du répertoire est jointe à ladite réquisition »", 1000, 300, 840, W(5, 3)[0] - 0.1, b, 'quote')

# --- 6 : l'objet de la plainte
a, b = Q(6)
heads(a + 0.2, b)
pic('s1-plainte.png', 80, 200, 840, W(6, 0)[0] - 0.3, b, "Sommation du 3 avril 2024 : la plainte du 21 août 2023, « relativement au jugement n°114/14/3ème CH-EP du 31 octobre 2014 »", find=("faux et usage de faux en écriture publique, relativement au jugement",), cls='p6')
pic('m2-plainte.png', 1000, 200, 840, W(6, 1)[0] - 0.3, b, "Mémoire du 29 avril 2025, p. 2 — signé Sabi Fulbert Konto", find=("Gilles Sixte conteste le testament",), cls='p6')
trait(W(6, 2)[0], b, 640)

# --- 7 : le notaire, témoin, soupçonné, visé
a, b = Q(7)
text("MAÎTRE FÉLIX AWÉ BALLEY", 80, 62, 1760, a + 0.2, b, 'colhead wide')
pic('pa-title.png', 80, 150, 560, W(7, 0)[0] - 0.3, b, "Procès-verbal n° 2 du 19 mars 2025 : « audition de témoin »", cls='p7')
pic('pa-susp.png', 680, 150, 560, W(7, 1)[0] - 0.3, b, "Même procès-verbal, en-tête : « Personne soupçonnée »", find=("BALLEY A. Félix",), cls='p7')
pic('m2-balley.png', 1280, 150, 560, W(7, 2)[0] - 0.3, b, "Mémoire du 29 avril 2025, p. 2 : « Gilles Sixte FELIHO porte plainte contre Maître FADE O. Victorien […] Maître BALLEY »", find=("porte plainte contre Maître FADE", "BALLEY Félix Awé Notaire"), cls='p7')
text("<b>Sommation du 3 avril 2024 — personnes à convoquer :</b><br>FADE Victorien Olatundji · Lise FELIHO · Albin FELIHO · Florentin-Lin FELIHO · Nina FELIHO · HUNGBO Olivia Aubierge épouse KPLOCA<br><span class='ocre'>BALLEY : absent de la liste</span>", 80, 640, 1760, W(7, 3)[0] - 0.2, b, 'quote wide')

# --- 8 : six personnes demandées, deux convocations
a, b = Q(8)
heads(a + 0.2, b, 'CE QUI A ÉTÉ DEMANDÉ', 'CE QUI A ÉTÉ FAIT')
names = ["FADE Victorien Olatundji, avocat", "Lise FELIHO", "Albin FELIHO", "Florentin-Lin FELIHO", "Nina FELIHO", "HUNGBO Olivia Aubierge épouse KPLOCA, magistrate"]
for i, nm in enumerate(names):
    text(f'{i+1}. {nm}', 80, 170 + i * 80, 840, W(8, 0)[0] + i * 0.25, b, 'nm' + (' off' if i > 0 else ''))
text("Sommation du 3 avril 2024 : « les convocations au nom des mis en cause suivants et toute autre personne que l'enquête révélera »", 80, 700, 840, W(8, 0)[0] + 1.6, b, 'ctext small')
pic('q-conv141.png', 1000, 150, 400, W(8, 1)[0] - 0.3, b, "Convocation n° 141 du 12 mars 2025 : Maître Fade", h=380, cls='p8')
pic('q-conv142.png', 1440, 150, 400, W(8, 1)[0] + 0.6, b, "Convocation n° 142 : Maître Balley", h=380, cls='p8')
pic('q-relance.png', 1000, 560, 840, W(8, 3)[0] - 0.3, b, "Relance de convocation du 25 mars 2025 : signée Sabi Fulbert Konto", h=390, find=("il a été convoqué pour le mercredi 19 mars 2025 mais il ne s'est pas présenté",), cls='p8')

# --- 9 : le jugement, le testament, la disposition « constatée »
a, b = Q(9)
text("JUILLET 2009<br><small>testament</small>", 80, 120, 520, W(9, 1)[0] - 0.3, b, 'date3')
text("3 DÉCEMBRE 2010<br><small>décès</small>", 700, 120, 520, W(9, 1)[0] + 0.4, b, 'date3')
text("?<br><small>disposition « constatée » : ni date, ni acte</small>", 1300, 120, 540, W(9, 1)[0] + 1.0, b, 'date3 vide')
el('', W(9, 1)[0] - 0.3, b, 0.5, 'frl2', 'left:80px;top:300px;width:1760px')
pic('jg5.png', 80, 360, 840, W(9, 0)[0] - 0.3, W(9, 3)[0] - 0.2, "Jugement n° 114/14/3ème CH-EP, p. 5 : « Que Gilles Sixte FELIHO a même déjà disposé de cet immeuble »", find=("a même déjà disposé de cet immeuble",), cls='p9')
pic('jg8a.png', 1000, 360, 840, W(9, 0)[0] + 3.0, W(9, 3)[0] - 0.2, "Même jugement, dispositif : « Constate que Gilles Sixte FELIHO a exécuté les dispositions testamentaires de manière volontaire »", find=("Constate que Gilles Sixte FELIHO a exécuté les dispositions testamentaires de manière volontaire",), cls='p9')
pic('m3-achete.png', 1000, 360, 840, W(9, 3)[0] - 0.3, b, "Mémoire du 29 avril 2025, p. 3 — signé Sabi Fulbert Konto", find=("lui avoir acheté la parcelle sise au lot 488",), cls='p9')
text("Un achat n'est pas un legs.<br>Une acquisition n'est pas une disposition.<br>Le testament n'est pas dans les pièces.", 80, 660, 840, W(9, 4)[0] - 0.2, b, 'bigtext')

# --- 10 : « non assorti de recours » et l'usurpation
a, b = Q(10)
heads(a + 0.2, b, 'CE QUE DIT LE JUGEMENT', 'CE QU\'ÉCRIT LE MÉMOIRE')
pic('jg8a.png', 80, 150, 840, W(10, 1)[0] - 0.3, b, "Jugement du 31 octobre 2014, dispositif : « en premier ressort »", find=("en premier ressort",), cls='p10')
pic('jg8b.png', 80, 600, 840, W(10, 1)[0] + 0.6, b, "Même dispositif : « Ordonne l'exécution provisoire » ; « Délai d'appel : 01 mois »", find=("Ordonne l'exécution provisoire", "Délai d'appel : 01 mois"), cls='p10')
pic('m4-chose.png', 1000, 150, 840, W(10, 0)[0] - 0.3, b, "Mémoire du 29 avril 2025, p. 4 — signé Sabi Fulbert Konto", find=("autorité de la chose jugée est non assorti de recours",), cls='p10')
text("« Une usurpation des prérogatives judiciaires, sans aucune garantie procédurale »<br><span class='cap2'>Réplique du plaignant à la Cour constitutionnelle, 2 juin 2025</span>", 1000, 640, 840, W(10, 3)[0] - 0.3, b, 'quote ocrebox')

# --- 11 : l'intention prêtée
a, b = Q(11)
heads(a + 0.2, b, 'CE QUE DIT LE TÉMOIN', 'CE QU\'ÉCRIT LE MÉMOIRE')
pic('pa-objectif.png', 80, 200, 840, W(11, 0)[0] - 0.3, b, "Procès-verbal d'audition de témoin n° 2 du 19 mars 2025, p. 2", find=("son objectif principal est de faire échec à l'exécution des dispositions du testament",), cls='p11')
pic('m3-balley.png', 1000, 200, 840, W(11, 1)[0] - 0.3, b, "Mémoire du 29 avril 2025, p. 3 — signé Sabi Fulbert Konto", find=("l'objectif principal de Gilles Sixte FELIHO est de faire échec à l'exécution des dispositions",), cls='p11')

# --- 12 : le procès-verbal de 2017
a, b = Q(12)
heads(a + 0.2, b, 'CE QUI EXISTE AU DOSSIER', 'CE QUI N\'Y FIGURE PAS')
pic('pc2c.png', 80, 150, 840, W(12, 0)[0] - 0.3, b, "Procès-verbal de compulsion du 19 décembre 2017, p. 2 — Mairie de Cotonou : « SUPERFICIE : néant »", hl=((14, 24, 36, 11),), cls='p12')
pic('pc3c.png', 80, 580, 840, W(12, 1)[0] - 0.3, b, "Même procès-verbal, p. 3 — IGN : « L'IGN ne dispose d'aucun document afférent à la parcelle B »", hl=((8, 44, 86, 38),), cls='p12')
el('<div class="vide">non mentionné dans le mémoire du 29 avril 2025</div>', W(12, 2)[0] - 0.3, b, 0.6, '', 'left:1000px;top:260px;width:840px;height:480px')

# --- 13 : les durées et le classement
a, b = Q(13)
counter(563, 'JOURS', 80, 150, W(13, 0)[0] - 0.2, W(13, 2)[0] - 0.2, W(13, 0)[0], W(13, 0)[0] + 2.2, w=840, size=170, sub="de la plainte (21 août 2023) à la notification de la Cour (6 mars 2025)")
counter(54, 'JOURS', 1000, 150, W(13, 1)[0] - 0.2, W(13, 2)[0] - 0.2, W(13, 1)[0], W(13, 1)[0] + 1.6, w=840, size=170, sub="de cette notification au mémoire du 29 avril 2025")
pic('classement.png', 1200, 60, 560, W(13, 2)[0] - 0.3, b, '', hl=((17, 50.4, 69, 6.4),), cls='p13')
card(3, 'JUILLET', 2025, 160, 220, W(13, 2)[0] - 0.2, b, 'big')
counter(12, 'JOURS', 160, 640, W(13, 3)[0] - 0.2, b, W(13, 3)[0], W(13, 3)[0] + 1.6, w=900, size=150, sub="du classement à l'audience du 15 juillet 2025")

# --- 14 : questions
a, b = Q(14)
QS = ["Pourquoi une sommation d'huissier est-elle devenue un « comportement » justifiant le retrait du dossier ?",
      "Pourquoi les premières convocations produites datent-elles du 12 mars 2025, six jours après la notification de la Cour ?",
      "Sur quelle pièce le jugement constate-t-il une disposition postérieure au décès ?",
      "Sur quelle pièce le mémoire fonde-t-il que le plaignant est « supposé détenir » les titres, alors que le testament n'est pas produit ?",
      "Pourquoi les autres personnes désignées par la sommation n'ont-elles pas été convoquées ?",
      "Pourquoi le procès-verbal de compulsion de 2017 n'est-il pas discuté ?"]
for i, q in enumerate(QS):
    text(q, 160, 90 + i * 140, 1600, a + 0.6 + i * 1.3, b - 0.5, 'quest')

# --- carton final
a, b = SQ[15]
text('wadagni2026-verite.com', 0, 300, 1920, a + 0.6, b, 'url', 0.8)
text('Les pièces reproduites dans ce film sont publiées dans leur intégralité sur le site, avec leurs empreintes numériques.', 0, 400, 1920, a + 1.6, b, 'finsmall', 0.8)
text("Les extraits reproduits sont des copies partielles. Les annotations rouges des originaux ont été effacées des recadrages ; les coordonnées personnelles sont occultées.<br>"
     "Le chef de la Brigade criminelle d'avril 2024 est désigné par la lettre du 29 avril 2025 comme « le Chef d'alors », sans être nommé. Le testament est daté du 16 juillet 2009 dans le procès-verbal de compulsion et du 19 juillet 2009 dans le jugement.", 160, 560, 1600, a + 2.6, b, 'precis', 0.8)

CSS = '''
:root{--navy:#0a1f44;--gold:#d4af37;--ink:#f8fafc;--mute:#94a3b8}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:#050d1f;font-family:'DejaVu Sans',sans-serif;color:var(--ink)}
#stage{position:relative;width:1920px;height:1080px;background:radial-gradient(ellipse at 30% 20%,#12306b 0%,#0a1f44 45%,#050d1f 100%)}
.el{position:absolute;opacity:0}
.title{font-family:'DejaVu Serif',serif;font-size:100px;line-height:1.15;font-weight:700}
.subtitle{font-family:'DejaVu Serif',serif;font-size:44px;color:var(--gold);font-style:italic}
.colhead{font-size:30px;letter-spacing:.1em;color:var(--gold);text-transform:uppercase}.colhead.wide{text-align:center}
.vbar{width:2px;background:rgba(199,210,254,.5)}
.attente{font-size:90px;color:var(--mute);text-align:center}
.card{width:230px;text-align:center;background:rgba(255,255,255,.07);border:3px solid var(--gold);border-radius:16px;padding:12px 8px}
.card .dd{font-size:72px;font-weight:800;line-height:1.0}.card .mm{font-size:30px;letter-spacing:.08em;color:var(--gold);margin-top:4px}.card .yy{font-size:28px;color:var(--mute)}.card .lb{font-size:22px;color:#e2e8f0;margin-top:8px;line-height:1.2}
.card.sm{width:250px}
.card.big{width:420px;padding:30px 10px}.card.big .dd{font-size:180px}.card.big .mm{font-size:60px}.card.big .yy{font-size:56px}
.pic{position:relative;background:#fff;border:4px solid var(--gold);border-radius:6px;overflow:hidden;box-shadow:0 14px 40px rgba(0,0,0,.6)}
.pic img{display:block;width:100%}
.hl{position:absolute;background:rgba(212,175,55,.35);border:2px solid rgba(212,175,55,.9)}
.cap{font-size:21px;line-height:1.3;color:var(--mute);margin-top:10px}.cap2{font-size:22px;color:var(--mute)}
.counter{font-weight:800;color:var(--gold);text-align:center;white-space:nowrap}
.counter .cu{font-size:56px;margin-left:20px;color:#fff;font-weight:600;letter-spacing:.06em}
.csub{font-size:26px;color:#cbd5e1;font-weight:400;white-space:normal;margin-top:6px}
.quote{font-family:'DejaVu Serif',serif;font-size:34px;line-height:1.3;background:rgba(255,255,255,.07);border-left:6px solid var(--gold);padding:14px 22px}
.quote.wide{font-size:30px}
.num{color:var(--gold);font-weight:700}
.ocre{color:var(--gold)}
.ocrebox{border-left-color:#ef4444}
.ctext{font-size:28px;line-height:1.4;color:#e2e8f0}.ctext.small{font-size:24px;color:var(--mute)}
.nm{font-size:34px;font-family:'DejaVu Serif',serif;padding:8px 14px;background:rgba(255,255,255,.07);border-left:6px solid var(--gold)}
.trait{position:absolute;height:4px;background:var(--gold);transform-origin:left}
.grow{transform-origin:left}
.vide{border:4px dashed rgba(199,210,254,.6);color:var(--mute);font-size:38px;display:flex;align-items:center;justify-content:center;text-align:center;padding:30px}
.date3{font-family:'DejaVu Serif',serif;font-size:44px;font-weight:700;text-align:center;line-height:1.2}.date3 small{font-size:24px;font-weight:400;color:var(--mute);font-family:'DejaVu Sans'}
.date3.vide{border:4px dashed rgba(199,210,254,.6);padding:10px;font-size:90px;color:var(--gold)}.date3.vide small{color:#cbd5e1}
.frl2{height:3px;background:#c7d2fe}
.bigtext{font-family:'DejaVu Serif',serif;font-size:42px;line-height:1.3;font-weight:700}
.quest{font-family:'DejaVu Serif',serif;font-size:40px;line-height:1.25}
.url{font-size:64px;text-align:center;font-family:'DejaVu Serif',serif;color:#fff}.finsmall{font-size:30px;text-align:center;color:var(--mute)}
.precis{font-size:24px;line-height:1.6;color:#cbd5e1}
.bandeau{left:0;bottom:0;width:1920px;height:88px;background:rgba(0,0,0,.7);color:#fff;font-size:26px;line-height:1.3;padding:12px 60px;z-index:50}
body.fin #stage{background:#000}
'''
JS = '''
const ELS=[...document.querySelectorAll('.el')],CNS=[...document.querySelectorAll('.cn')];
const cl=x=>Math.max(0,Math.min(1,x));
window.TOTAL=%.2f;
window.seek=function(t){
  for(const e of ELS){const a=+e.dataset.a,b=+e.dataset.b,f=+e.dataset.f;const i=cl((t-a)/f);
    e.style.opacity=i*cl((b-t)/f);
    if(e.classList.contains('trait')){e.style.transform=`scaleX(${cl((t-a)/1.0)})`;}
    else if(e.classList.contains('card')||e.classList.contains('piece')) e.style.transform=`translateY(${(1-i)*14}px)`;}
  for(const c of CNS){const a=+c.dataset.ca,b=+c.dataset.cb,to=+c.dataset.to;c.textContent=Math.round(to*cl((t-a)/(b-a)));}
  document.body.classList.toggle('fin',t>=%.2f);
};
seek(0);
''' % (TOTAL, SQ[15][0] - 0.3)
html = f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>L\'enquête contre elle-même</title><style>{CSS}</style></head><body><div id="stage">\n' + '\n'.join(EL) + f'\n</div><script>{JS}</script></body></html>'
open(os.path.join(here, 'motion.html'), 'w', encoding='utf-8').write(html)
json.dump({'total': TOTAL, 'sequences': {str(k_): v for k_, v in SQ.items()}, 'cues': cues}, open(os.path.join(out, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
print('durée totale', round(TOTAL, 1), 's ; séquences', {k_: (round(a_, 1), round(b_, 1)) for k_, (a_, b_) in SQ.items()})
