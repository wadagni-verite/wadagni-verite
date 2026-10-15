# -*- coding: utf-8 -*-
"""Film « Faits précis demandés, faits précis fournis » : la lettre du 14 janvier 2026 du ministre de la Justice Yvon Détchénou et les pièces.
Usage : python3 build.py <dossier_modèles_kokoro> <dossier_sortie>   (voix Kokoro ff_siwis ; cache des phrases dans <sortie>/cache)
Écrit : motion.html (rendu par render.js), <sortie>/audio.wav, film.fr.srt, film.fr.vtt, timeline.json.
Chaque image provient d'une pièce publiée sur le site ; les recadrages sont dans img/.
"""
import sys, os, json, hashlib, datetime as dt
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

models, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
SR = 24000
MIN = "le ministre de la Justice Yvon Détchénou"

# ------------------------------------------------------------------ texte : (sous-titre, texte lu) par séquence
SEQ = {
 1: dict(speed=1.14, gap=0.3, lead=1.4, tail=1.2, s=[
   ("Faits précis demandés. Faits précis fournis.", "Faits précis demandés. Faits précis fournis."),
   ("Le 14 janvier 2026, le ministre de la Justice, Yvon Détchénou, écrit : « aucun fait précis allégué ». Ce film remet les dates et les pièces dans l'ordre.",
    "Le quatorze janvier deux mille vingt-six, le ministre de la Justice, Yvon Détchénou, écrit : aucun fait précis allégué. Ce film remet les dates et les pièces dans l'ordre.")]),
 2: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.4, s=[
   ("Le 3 juillet 2025, le parquet spécial de la CRIET classe la plainte sans suite.", "Le trois juillet deux mille vingt-cinq, le parquet spécial de la Criet classe la plainte sans suite."),
   ("Le 25 novembre 2025, la demande de réouverture de l'enquête arrive au parquet spécial.", "Le vingt-cinq novembre deux mille vingt-cinq, la demande de réouverture de l'enquête arrive au parquet spécial."),
   ("Le 5 janvier 2026, l'avocat du plaignant écrit au ministre de la Justice, Yvon Détchénou.", "Le cinq janvier deux mille vingt-six, l'avocat du plaignant écrit au ministre de la Justice, Yvon Détchénou."),
   ("Le 14 janvier, le ministre Yvon Détchénou répond.", "Le quatorze janvier, le ministre Yvon Détchénou répond."),
   ("Le 6 février, le plaignant lui écrit à son tour.", "Le six février, le plaignant lui écrit à son tour.")]),
 3: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.2, s=[
   ("Sur la demande de réouverture, deux dates. Le 24 septembre 2025 : la date portée par la lettre.", "Sur la demande de réouverture, deux dates. Le vingt-quatre septembre deux mille vingt-cinq : la date portée par la lettre."),
   ("Le 25 novembre 2025 : la date d'arrivée, portée par le cachet du parquet spécial.", "Le vingt-cinq novembre deux mille vingt-cinq : la date d'arrivée, portée par le cachet du parquet spécial."),
   ("La date retenue est celle de la réception : le 25 novembre 2025.", "La date retenue est celle de la réception : le vingt-cinq novembre deux mille vingt-cinq.")]),
 4: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.4, s=[
   ("Le 14 janvier 2026, le ministre de la Justice Yvon Détchénou répond à l'avocat du plaignant par une lettre de trois phrases.",
    "Le quatorze janvier deux mille vingt-six, le ministre de la Justice Yvon Détchénou répond à l'avocat du plaignant par une lettre de trois phrases."),
   ("Première phrase : « J'accuse bonne réception de votre demande ».", "Première phrase : j'accuse bonne réception de votre demande."),
   ("Deuxième phrase : « Je vous invite en l'état d'un classement sans suite à agir par citation directe ou constitution de partie civile ».",
    "Deuxième phrase : je vous invite, en l'état d'un classement sans suite, à agir par citation directe ou constitution de partie civile."),
   ("Troisième phrase : « votre présente lettre n'est appuyée d'aucun fait précis allégué ».", "Troisième phrase : votre présente lettre n'est appuyée d'aucun fait précis allégué.")]),
 5: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.4, s=[
   ("La lettre de l'avocat, du 5 janvier 2026, renvoie à la demande déposée le 25 novembre 2025 auprès du Procureur spécial.",
    "La lettre de l'avocat, du cinq janvier deux mille vingt-six, renvoie à la demande déposée le vingt-cinq novembre deux mille vingt-cinq auprès du Procureur spécial."),
   ("Cette demande, de cinq pages, vise la plainte du 17 août 2023 et le classement du 3 juillet 2025. Elle formule quatre demandes.",
    "Cette demande, de cinq pages, vise la plainte du dix-sept août deux mille vingt-trois et le classement du trois juillet deux mille vingt-cinq. Elle formule quatre demandes."),
   ("La lettre adressée au ministre ne mentionne aucune pièce jointe.", "La lettre adressée au ministre ne mentionne aucune pièce jointe.")]),
 6: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.4, s=[
   ("Le 6 février 2026, le plaignant, Gilles Féliho, répond au ministre de la Justice Yvon Détchénou.", "Le six février deux mille vingt-six, le plaignant, Gilles Féliho, répond au ministre de la Justice Yvon Détchénou."),
   ("Il écrit qu'il porte à sa connaissance « les faits précis » réclamés dans sa correspondance du 14 janvier.", "Il écrit qu'il porte à sa connaissance les faits précis réclamés dans sa correspondance du quatorze janvier."),
   ("Un tableau : cinq documents, leurs dates, le fait matériel contradictoire, la personne concernée.", "Un tableau : cinq documents, leurs dates, le fait matériel contradictoire, la personne concernée."),
   ("Un magistrat, un huissier de justice, un notaire, un avocat. Sept pièces jointes.", "Un magistrat, un huissier de justice, un notaire, un avocat. Sept pièces jointes.")]),
 7: dict(speed=1.12, gap=0.35, lead=0.9, tail=1.4, s=[
   ("Le fait nouveau : la lettre du notaire Denise Ehouzou Gangnito, du 19 septembre 2007.", "Le fait nouveau : la lettre du notaire Denise Ehouzou Gangnito, du dix-neuf septembre deux mille sept."),
   ("Elle est adressée à Maître Victorien Olatundji Fade, « mandataire » de Gilles Féliho, à la suite de l'adjudication de constructions sur la parcelle B du lot 923, à Gbégamey.",
    "Elle est adressée à Maître Victorien Olatundji Fade, mandataire de Gilles Féliho, à la suite de l'adjudication de constructions sur la parcelle B du lot neuf cent vingt-trois, à Gbégamey."),
   ("Cette lettre ne concerne pas le testament.", "Cette lettre ne concerne pas le testamant."),
   ("Selon la lettre du 6 février, Maître Fade apparaît ensuite comme avocat des cohéritiers, dans l'instance qui produit le jugement de 2014, puis dans la signification du jugement en France.",
    "Selon la lettre du six février, Maître Fade apparaît ensuite comme avocat des cohéritiers, dans l'instance qui produit le jugement de deux mille quatorze, puis dans la signification du jugement en France."),
   ("Le plaignant écrit : « triple conflit d'intérêts non déclaré ».", "Le plaignant écrit : triple conflit d'intérêts non déclaré.")]),
 8: dict(speed=1.12, gap=0.4, lead=0.9, tail=1.4, s=[
   ("Le ministre invite à agir par citation directe ou constitution de partie civile.", "Le ministre invite à agir par citation directe ou constitution de partie civile."),
   ("L'article 303 du Code pénal, cité dans la plainte, punit le faux en écriture publique de la réclusion criminelle à perpétuité.",
    "L'article trois cent trois du Code pénal, cité dans la plainte, punit le faux en écriture publique de la réclusion criminelle à perpétuité."),
   ("Pour une infraction de nature criminelle, la citation directe n'est pas ouverte.", "Pour une infraction de nature criminelle, la citation directe n'est pas ouverte."),
   ("Reste la plainte avec constitution de partie civile, qui fera l'objet d'une prochaine page.", "Reste la plainte avec constitution de partie civile, qui fera l'objet d'une prochaine page.")]),
 9: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.4, s=[
   ("Neuf jours, du 5 au 14 janvier 2026 : de la lettre de l'avocat à la réponse du ministre Yvon Détchénou.", "Neuf jours, du cinq au quatorze janvier deux mille vingt-six : de la lettre de l'avocat à la réponse du ministre Yvon Détchénou."),
   ("Vingt-trois jours, du 14 janvier au 6 février : de cette réponse à la lettre du plaignant, qui fournit les faits précis.", "Vingt-trois jours, du quatorze janvier au six février : de cette réponse à la lettre du plaignant, qui fournit les faits précis."),
   ("Deux cent cinquante et un jours, du 6 février au 15 octobre 2026, date de ce film : aucune réponse du ministre Yvon Détchénou.",
    "Deux cent cinquante et un jours, du six février au quinze octobre deux mille vingt-six, date de ce film : aucune réponse du ministre Yvon Détchénou.")]),
 10: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.8, s=[
   ("Quatre questions pour le ministre de la Justice, Yvon Détchénou. Les réponses seront publiées.", "Quatre questions pour le ministre de la Justice, Yvon Détchénou. Les réponses seront publiées.")]),
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
for sq in (4, 6, 8, 9):                       # souffles secs, un par grand contraste
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

el("Aucune infraction n'est imputée au ministre de la Justice : ce film met en regard une lettre et des pièces publiées. Les personnes citées peuvent exercer leur droit de réponse.", 0, TOTAL, 0.6, 'bandeau')

# --- 1 : ouverture
a, b = Q(1)
text("FAITS PRÉCIS<br>DEMANDÉS, FOURNIS", 160, 280, 1600, a + 0.6, b, 'title', 1.0)
text("Le ministre de la Justice Yvon Détchénou — sa lettre du 14 janvier 2026", 160, 640, 1600, a + 2.4, b, 'subtitle', 1.0)

# --- 2 : la chronologie
a, b = Q(2)
trait(a + 0.2, b, 250)
CH = [(3, 'JUILLET', 2025, 'Classement sans suite (CRIET)'), (25, 'NOV.', 2025, 'Demande de réouverture reçue'), (5, 'JANV.', 2026, "Lettre de l'avocat au ministre"),
      (14, 'JANV.', 2026, 'Réponse du ministre Yvon Détchénou'), (6, 'FÉV.', 2026, 'Lettre du plaignant')]
for i, (dd, mm, yy, lb) in enumerate(CH):
    card(dd, mm, yy, 90 + i * 360, 320, W(2, i)[0] - 0.2, b, 'sm', lb)
for i, nj in enumerate((145, 41, 9, 23)):   # durées entre deux actes consécutifs
    text(f"<span class='ocre'>{nj} jours</span>", 340 + i * 360, 380, 110, W(2, i + 1)[0] - 0.2, b, 'ctext small gap')
text("Depuis : <span class='ocre'>aucune réponse du ministre.</span>", 160, 700, 1600, W(2, 4)[1] + 0.2, b, 'bigtext')

# --- 3 : deux dates sur la demande de réouverture
a, b = Q(3)
pic('c-stamp.png', 80, 150, 1000, a + 0.3, b, "Demande de réouverture au Procureur spécial près la CRIET : date de la lettre et cachet « COURRIER ARRIVÉ »", hl=((13.5, 8, 26.5, 34),), find=("Le Mesnil, le 24 Septembre 2025",), cls='p3')
pic('c-plainte.png', 80, 560, 1000, W(3, 2)[0] - 0.3, b, "Même lettre, p. 1 : la plainte du 17 août 2023", find=("plainte de mon client du 17 août 2023",), cls='p3')
text("24 SEPTEMBRE 2025<br><small>date portée par la lettre</small>", 1150, 150, 700, W(3, 0)[0] - 0.3, b, 'date3')
text("25 NOVEMBRE 2025<br><small>date d'arrivée : cachet du parquet spécial</small>", 1150, 330, 700, W(3, 1)[0] - 0.3, b, 'date3')
text("DATE RETENUE<br>25 NOVEMBRE 2025", 1150, 560, 700, W(3, 2)[0] - 0.3, b, 'date3 ret')

# --- 4 : la réponse du 14 janvier
a, b = Q(4)
heads(a + 0.2, b, 'LA LETTRE DU 14 JANVIER 2026', 'CE QU\'ELLE DIT')
pic('m-reponse.png', 80, 130, 800, W(4, 0)[0] - 0.3, b, "Lettre n° 0049/MJL/SP-C du 14 janvier 2026, signée Yvon Détchénou, à Me Samba Sidibé", find=("J'accuse bonne réception de votre demande", "agir par citation directe ou constitution de partie civile", "aucun fait précis allégué"), cls='p4')
qs = ["« J'accuse bonne réception de votre demande citée en objet. »",
      "« Je vous invite en l'état d'un classement sans suite à agir par citation directe ou constitution de partie civile pour la défense de vos intérêts. »",
      "« Pour le reste, votre présente lettre n'est appuyée d'aucun fait précis allégué à l'appui des éléments concrets de nature à en motiver la prise en considération à mon niveau administratif. »"]
for i, q in enumerate(qs):
    text(f'<span class="num">{"①②③"[i]}</span> {q}', 960, (150, 290, 510)[i], 880, W(4, i + 1)[0] - 0.3, b, 'quote')

# --- 5 : ce que la lettre du 5 janvier renvoie
a, b = Q(5)
heads(a + 0.2, b, 'LA LETTRE DE L\'AVOCAT, 5 JANVIER 2026', 'LA DEMANDE DU 25 NOVEMBRE 2025')
pic('j-top.png', 80, 130, 840, W(5, 0)[0] - 0.3, b, "Lettre de Me Samba Sidibé au ministre de la Justice, 5 janvier 2026, p. 1", find=("Le 25 novembre 2025, j'ai saisi le Procureur Spécial près la CRIET",), cls='p5')
pic('c-plainte.png', 960, 130, 880, W(5, 1)[0] - 0.3, b, "Demande du 25 novembre 2025, p. 1 : la plainte du 17 août 2023 ; classement du 3 juillet 2025", find=("plainte de mon client du 17 août 2023",), cls='p5')
pic('c-demandes.png', 960, 330, 880, W(5, 1)[0] + 1.2, b, "Même demande, p. 4 : « Demandes précises et motivées », au nombre de quatre", h=560, cls='p5')
text("Lettre du 5 janvier 2026 au ministre : <span class='ocre'>aucune pièce jointe mentionnée.</span>", 80, 700, 840, W(5, 2)[0] - 0.3, b, 'quote ocrebox')

# --- 6 : la lettre du 6 février et son tableau
a, b = Q(6)
text('LA LETTRE DU 6 FÉVRIER 2026', 80, 62, 760, a + 0.2, b, 'colhead'); text('SON TABLEAU DE « FAITS PRÉCIS »', 880, 62, 980, a + 0.2, b, 'colhead')
pic('f-intro.png', 80, 130, 760, W(6, 0)[0] - 0.3, b, "Lettre de Gilles Féliho au ministre de la Justice, 6 février 2026, p. 1 (adresse et courriel occultés)", find=("les “faits précis” réclamés dans votre correspondance du 14 janvier",), cls='p6')
ROWS = [("Jugement n° 114/14/3ᵉ CH-EP<br>31 oct. 2014", "Constate la parcelle B lot 488 léguée, dont le légataire a disposé. Contradiction : parcelle inexistante ; absence d'acte de disposition.", "Magistrat signataire du jugement"),
        ("Procès-verbal de compulsion<br>19 déc. 2017", "Même parcelle « inexistante » : le jugement constate des faits matériellement inexacts.", "Huissier de justice"),
        ("Certificat d'acquit de droit<br>20 oct. 2016", "Décès au 10 juin 2016 ; l'acte de décès indique le 3 déc. 2010 : six ans d'écart.", "Notaire Félix A. Balley"),
        ("Même certificat", "Mandat de Gilles Féliho au notaire : « inexistant », selon le plaignant.", "Notaire Balley"),
        ("Lettre du notaire Gangnito<br>19 sept. 2007", "Fait nouveau : triple conflit d'intérêts non déclaré de l'avocat Fade.", "Avocat Fade")]
text("<span>DOCUMENT ET DATE</span><span>FAIT MATÉRIEL CONTRADICTOIRE</span><span>ACTEUR CONCERNÉ</span>", 880, 130, 980, W(6, 2)[0] - 0.3, b, 'trow thead', 0.4)
for i, (c1, c2, c3) in enumerate(ROWS):
    text(f"<span>{c1}</span><span>{c2}</span><span>{c3}</span>", 880, 190 + i * 150, 980, W(6, 2)[0] + 0.6 + i * 1.1, b, 'trow', 0.5)

# --- 7 : le fait nouveau : la lettre du notaire de 2007
a, b = Q(7)
heads(a + 0.2, b, 'LA LETTRE DU NOTAIRE (2007)', 'SELON LA LETTRE DU 6 FÉVRIER')
pic('g-tete.png', 80, 150, 840, W(7, 0)[0] - 0.3, b, "Lettre de Me Denise Ehouzou Gangnito, notaire, du 19 septembre 2007", cls='p7')
pic('g-dest.png', 80, 300, 420, W(7, 1)[0] - 0.3, b, "Destinataire : Maître Victorien Fade, avocat à la Cour", cls='p7')
pic('g-corps.png', 80, 480, 840, W(7, 1)[0] + 0.4, b, "Même lettre : « Suite à l'adjudication […] sur la parcelle « B » du lot 923 […] au profit de Monsieur Gilles Sixte FELIHO, dont vous êtes le mandataire »", hl=((3, 38, 94, 38),), cls='p7')
text("<b>Cette lettre ne concerne pas le testament.</b>", 1000, 150, 840, W(7, 2)[0] - 0.3, b, 'quote')
for i, tx in enumerate(["<b>2007</b> — mandataire de Gilles Féliho (lettre du notaire)", "<b>2014</b> — avocat des cohéritiers dans l'instance (jugement n° 114/14, p. 1)", "<b>2015</b> — avocat des cohéritiers dans la signification du jugement en France (selon la lettre du 6 février)"]):
    text(tx, 1000, 290 + i * 130, 840, W(7, 3)[0] + i * 1.3, b, 'nm')
text("« Triple conflit d'intérêts non déclaré »<br><span class='cap2'>Lettre du plaignant du 6 février 2026</span>", 1000, 700, 840, W(7, 4)[0] - 0.3, b, 'quote')

# --- 8 : la voie indiquée
a, b = Q(8)
text("<b>Ministre de la Justice Yvon Détchénou, 14 janvier 2026</b><br>« agir par citation directe ou constitution de partie civile »", 160, 110, 1600, W(8, 0)[0] - 0.3, b, 'quote wide')
text("<b>Code pénal, art. 303</b> (cité dans la plainte) : le faux en écriture publique est puni de la réclusion criminelle à perpétuité", 160, 300, 1600, W(8, 1)[0] - 0.3, b, 'quote wide')
text("<b>Infraction de nature criminelle : la citation directe n'est pas ouverte.</b>", 160, 490, 1600, W(8, 2)[0] - 0.3, b, 'quote wide')
text("<b>Reste : la plainte avec constitution de partie civile</b><br><span class='cap2'>Objet d'une prochaine page.</span>", 160, 710, 1600, W(8, 3)[0] - 0.3, b, 'quote wide ocrebox')

# --- 9 : les durées
a, b = Q(9)
counter(9, 'JOURS', 40, 330, W(9, 0)[0] - 0.2, b, W(9, 0)[0], W(9, 0)[0] + 1.2, w=600, size=130, sub="du 5 au 14 janvier 2026 : de la lettre de l'avocat à la réponse du ministre")
counter(23, 'JOURS', 660, 330, W(9, 1)[0] - 0.2, b, W(9, 1)[0], W(9, 1)[0] + 1.4, w=600, size=130, sub="du 14 janvier au 6 février 2026 : de la réponse à la lettre du plaignant")
counter(251, 'JOURS', 1280, 330, W(9, 2)[0] - 0.2, b, W(9, 2)[0], W(9, 2)[0] + 2.4, w=600, size=130, sub="du 6 février au 15 octobre 2026 (date de ce film) : aucune réponse")

# --- 10 : questions
a, b = Q(10)
QS = ["Quels faits précis supplémentaires le ministre de la Justice Yvon Détchénou attendait-il, que la lettre du 6 février 2026 ne lui fournit pas ?",
      "La lettre du 6 février 2026 a-t-elle reçu une suite ?",
      "Quelle voie le ministre Yvon Détchénou indique-t-il pour un faux en écriture publique, infraction criminelle, alors que la citation directe n'est pas ouverte ?",
      "Quelle suite a été donnée à la demande de réouverture d'enquête reçue le 25 novembre 2025 ?"]
for i, q in enumerate(QS):
    text(q, 160, 120 + i * 200, 1600, a + 0.6 + i * 1.4, b - 0.5, 'quest')

# --- carton final
a, b = SQ[15]
text('wadagni2026-verite.com', 0, 300, 1920, a + 0.6, b, 'url', 0.8)
text('Les pièces reproduites dans ce film sont publiées sur le site, avec leurs empreintes numériques.', 0, 400, 1920, a + 1.6, b, 'finsmall', 0.8)
text("Les extraits reproduits sont des copies partielles ; les coordonnées personnelles sont occultées. La lettre de réouverture porte la date du 24 septembre 2025 et le cachet d'arrivée du 25 novembre 2025 : la date retenue est celle de la réception. "
     "La lettre du ministre est adressée à l'avocat du plaignant. "
     "Le tableau du 6 février 2026 est celui de la lettre du plaignant : il expose les allégations de celui-ci.", 160, 560, 1600, a + 2.6, b, 'precis', 0.8)

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
.ocretext{color:#d4af37}\n.vide2{border:4px dashed rgba(199,210,254,.6);color:#e2e8f0;font-size:30px;text-align:center;padding:22px;line-height:1.4}.vide2 b{color:#d4af37}
.bigtext{font-family:'DejaVu Serif',serif;font-size:42px;line-height:1.3;font-weight:700}
.quest{font-family:'DejaVu Serif',serif;font-size:40px;line-height:1.25}
.url{font-size:64px;text-align:center;font-family:'DejaVu Serif',serif;color:#fff}.finsmall{font-size:30px;text-align:center;color:var(--mute)}
.precis{font-size:24px;line-height:1.6;color:#cbd5e1}
.bandeau{left:0;bottom:0;width:1920px;height:88px;background:rgba(0,0,0,.7);color:#fff;font-size:26px;line-height:1.3;padding:12px 60px;z-index:50}
.trow{min-height:128px;align-items:start;display:grid;grid-template-columns:250px 1fr 230px;gap:18px;font-size:24px;line-height:1.3;background:rgba(255,255,255,.07);border-left:6px solid var(--gold);padding:12px 16px}.trow.thead{background:none;border:0;font-size:20px;letter-spacing:.08em;color:var(--gold);padding-top:0;padding-bottom:0}\n.gap{text-align:center;font-size:20px;white-space:nowrap}\n.date3.ret{border:4px solid var(--gold);padding:14px;color:var(--gold)}\n.p6,.p4,.p5,.p7,.p3{}\nbody.fin #stage{background:#000}
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
html = f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Faits précis demandés, faits précis fournis</title><style>{CSS}</style></head><body><div id="stage">\n' + '\n'.join(EL) + f'\n</div><script>{JS}</script></body></html>'
open(os.path.join(here, 'motion.html'), 'w', encoding='utf-8').write(html)
json.dump({'total': TOTAL, 'sequences': {str(k_): v for k_, v in SQ.items()}, 'cues': cues}, open(os.path.join(out, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
print('durée totale', round(TOTAL, 1), 's ; séquences', {k_: (round(a_, 1), round(b_, 1)) for k_, (a_, b_) in SQ.items()})
