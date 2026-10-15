# -*- coding: utf-8 -*-
"""Film « La voie indiquée, déjà empruntée » : la plainte avec constitution de partie civile du 29 septembre 2025 et la lettre du ministre de la Justice Yvon Détchénou du 14 janvier 2026.
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
   ("La voie indiquée, déjà empruntée.", "La voie indiquée, déjà empruntée."),
   ("Le 14 janvier 2026, le ministre de la Justice, Yvon Détchénou, invite à agir par citation directe ou constitution de partie civile. Cette voie a été empruntée 107 jours plus tôt.",
    "Le quatorze janvier deux mille vingt-six, le ministre de la Justice, Yvon Détchénou, invite à agir par citation directe ou constitution de partie civile. Cette voie a été empruntée cent sept jours plus tôt.")]),
 2: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.4, s=[
   ("Le 3 juillet 2025, le parquet spécial de la CRIET classe la plainte sans suite.", "Le trois juillet deux mille vingt-cinq, le parquet spécial de la Criet classe la plainte sans suite."),
   ("Le 26 septembre, le plaignant en prend connaissance.", "Le vingt-six septembre, le plaignant en prend connaissance."),
   ("Le 29 septembre 2025, trois jours plus tard, il dépose une plainte avec constitution de partie civile.", "Le vingt-neuf septembre deux mille vingt-cinq, trois jours plus tard, il dépose une plainte avec constitution de partie civile."),
   ("Le 14 janvier 2026, le ministre de la Justice, Yvon Détchénou, invite à agir par citation directe ou constitution de partie civile.", "Le quatorze janvier deux mille vingt-six, le ministre de la Justice, Yvon Détchénou, invite à agir par citation directe ou constitution de partie civile.")]),
 3: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.4, s=[
   ("La plainte est adressée au Doyen des juges d'instruction du tribunal de première instance de Cotonou.", "La plainte est adressée au Doyen des juges d'instruction du tribunal de première instance de Cotonou."),
   ("La page déposée porte le cachet du tribunal.", "La page déposée porte le cachet du tribunal."),
   ("Le même jour, le Trésor public délivre un récépissé : nature, plainte ; montant, 3 000 francs CFA ; poste, tribunal de première instance de première classe de Cotonou.",
    "Le même jour, le Trésor public délivre un récépissé : nature, plainte ; montant, trois mille francs CFA ; poste, tribunal de première instance de première classe de Cotonou."),
   ("Date du récépissé : le 29 septembre 2025.", "Date du récépissé : le vingt-neuf septembre deux mille vingt-cinq.")]),
 4: dict(speed=1.12, gap=0.35, lead=0.9, tail=1.4, s=[
   ("Pourquoi la constitution de partie civile ? L'article 85 du Code de procédure pénale, tel que cité dans la plainte : l'instruction préparatoire est obligatoire en matière de crime.",
    "Pourquoi la constitution de partie civile ? L'article quatre-vingt-cinq du Code de procédure pénale, tel que cité dans la plainte : l'instruction préparatoire est obligatoire en matière de crime."),
   ("Le faux en écriture publique, visé par l'article 303 du Code pénal, est puni de la réclusion criminelle à perpétuité : c'est un crime.",
    "Le faux en écriture publique, visé par l'article trois cent trois du Code pénal, est puni de la réclusion criminelle à perpétuité : c'est un crime."),
   ("L'information judiciaire est donc la voie. La citation directe n'est pas ouverte.", "L'information judiciaire est donc la voie. La citation directe n'est pas ouverte."),
   ("La plainte avec constitution de partie civile provoque cette information judiciaire lorsque le parquet classe.", "La plainte avec constitution de partie civile provoque cette information judiciaire lorsque le parquet classe.")]),
 5: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.4, s=[
   ("Elle vise X, quatre cohéritiers, Maître Victorien Olatundji Fade, et toutes autres personnes que l'instruction révélerait.", "Elle vise X, quatre cohéritiers, Maître Victorien Olatundji Fade, et toutes autres personnes que l'instruction révélerait."),
   ("Faux en écriture publique, usage de faux en écriture publique et recel.", "Faux en écriture publique, usage de faux en écriture publique et recel."),
   ("Elle demande de saisir sans délai un juge d'instruction, d'ouvrir une information judiciaire, et d'ordonner tous les actes utiles, dont l'audition des personnes mises en cause.",
    "Elle demande de saisir sans délai un juge d'instruction, d'ouvrir une information judiciaire, et d'ordonner tous les actes utiles, dont l'audition des personnes mises en cause."),
   ("Elle s'engage à consigner la somme demandée, et élit domicile chez Maître Narcisse Atoun pour les notifications.", "Elle s'engage à consigner la somme demandée, et élit domicile chez Maître Narcisse Atoun pour les notifications.")]),
 6: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.4, s=[
   ("La plainte reproche à l'enquête préliminaire d'avoir ignoré le procès-verbal de compulsion du 19 décembre 2017.", "La plainte reproche à l'enquête préliminaire d'avoir ignoré le procès-verbal de compulsion du dix-neuf décembre deux mille dix-sept."),
   ("De ne pas avoir entendu le juge signataire du jugement, ni l'avocat.", "De ne pas avoir entendu le juge signataire du jugement, ni l'avocat."),
   ("D'avoir mené des auditions sans en informer le plaignant.", "D'avoir mené des auditions sans en informer le plaignant."),
   ("Et de s'être concentrée sur le notaire, que la plainte du 17 août 2023 ne visait pas comme auteur.", "Et de s'être concentrée sur le notaire, que la plainte du dix-sept août deux mille vingt-trois ne visait pas comme auteur.")]),
 7: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.4, s=[
   ("Dix pièces sont jointes.", "Dix pièces sont jointes."),
   ("Le jugement, sa signification, le procès-verbal de compulsion, la décision de classement.", "Le jugement, sa signification, le procès-verbal de compulsion, la décision de classement."),
   ("Le certificat d'appel du 17 novembre 2014, qui atteste que le jugement est frappé d'appel.", "Le certificat d'appel du dix-sept novembre deux mille quatorze, qui atteste que le jugement est frappé d'appel."),
   ("La lettre du notaire Gangnito, du 19 septembre 2007.", "La lettre du notaire Gangnito, du dix-neuf septembre deux mille sept.")]),
 8: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.4, s=[
   ("88 jours, du classement au dépôt de la plainte.", "Quatre-vingt-huit jours, du classement au dépôt de la plainte."),
   ("107 jours, du dépôt de la plainte à la lettre du ministre Yvon Détchénou.", "Cent sept jours, du dépôt de la plainte à la lettre du ministre Yvon Détchénou."),
   ("381 jours, du 29 septembre 2025 au 15 octobre 2026, date de ce film : aucune suite connue.", "Trois cent quatre-vingt-un jours, du vingt-neuf septembre deux mille vingt-cinq au quinze octobre deux mille vingt-six, date de ce film : aucune suite connue.")]),
 9: dict(speed=1.14, gap=0.3, lead=0.9, tail=1.8, s=[
   ("Quatre questions pour le Doyen des juges d'instruction de Cotonou. Les réponses seront publiées.", "Quatre questions pour le Doyen des juges d'instruction de Cotonou. Les réponses seront publiées.")]),
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
for sq in (3, 4, 6, 8):                       # souffles secs, un par grand contraste
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

el("Aucune infraction n'est imputée aux personnes citées : ce film présente une plainte et des pièces publiées. Les qualifications pénales relèvent des juridictions compétentes. Droit de réponse ouvert.", 0, TOTAL, 0.6, 'bandeau')

# --- 1 : ouverture
a, b = Q(1)
text("LA VOIE INDIQUÉE,<br>DÉJÀ EMPRUNTÉE", 160, 280, 1600, a + 0.6, b, 'title', 1.0)
text("La plainte avec constitution de partie civile du 29 septembre 2025", 160, 640, 1600, a + 2.4, b, 'subtitle', 1.0)

# --- 2 : la chronologie
a, b = Q(2)
trait(a + 0.2, b, 250)
CH = [(3, 'JUILLET', 2025, 'Classement sans suite (CRIET)'), (26, 'SEPT.', 2025, 'Le plaignant en prend connaissance'), (29, 'SEPT.', 2025, 'Dépôt de la plainte avec constitution de partie civile'), (14, 'JANV.', 2026, 'Lettre du ministre Yvon Détchénou')]
for i, (dd, mm, yy, lb) in enumerate(CH):
    card(dd, mm, yy, 150 + i * 440, 320, W(2, i)[0] - 0.2, b, 'sm', lb)
for i, nj in enumerate(("85 jours", "3 jours", "107 jours")):
    text(f"<span class='ocre'>{nj}</span>", 400 + i * 440, 380, 190, W(2, i + 1)[0] - 0.2, b, 'ctext small gap')
text("Depuis le dépôt : <span class='ocre'>aucune suite connue.</span>", 160, 700, 1600, W(2, 3)[1] + 0.2, b, 'bigtext')

# --- 3 : le dépôt et le récépissé
a, b = Q(3)
heads(a + 0.2, b, 'LE DÉPÔT', 'LE RÉCÉPISSÉ DU TRÉSOR PUBLIC')
pic('pc-objet.png', 80, 140, 840, a + 0.4, b, "Plainte avec constitution de partie civile, p. 1 : destinataire, objet (coordonnées du plaignant occultées)", find=("Madame, Monsieur le Doyen des Juges d'Instruction", "Plainte avec Constitution de Partie Civile"), cls='p3')
pic('pc-cachet.png', 80, 470, 560, W(3, 1)[0] - 0.3, b, "Même page : cachet du tribunal de première instance de Cotonou, mention manuscrite non datée", hl=((38, 4, 52, 70),), cls='p3')
pic('recepisse.png', 1000, 140, 840, W(3, 2)[0] - 0.3, b, "Récépissé n° 25036294-026G, Direction générale du Trésor : « PLAINTE », 3 000 FCFA, en espèces", find=("TRIBUNAL DE PREMIERE INSTANCE DE 1ERE CLASSE DE COTONOU", "PLAINTE"), cls='p3')
text("29 SEPTEMBRE 2025<br><small>récépissé : nature « PLAINTE » · 3 000 FCFA</small>", 1000, 640, 840, W(3, 3)[0] - 0.3, b, 'date3 ret')

# --- 4 : l'article 85 et le crime
a, b = Q(4)
heads(a + 0.2, b, 'CE QUE CITE LA PLAINTE', 'CE QUI EN DÉCOULE')
pic('pc-art85.png', 80, 140, 840, W(4, 0)[0] - 0.3, b, "Plainte, p. 11 : article 85 du Code de procédure pénale, tel que cité ; article 90", find=("l'instruction préparatoire est obligatoire en matière de crime",), cls='p4')
text("<b>Art. 303 du Code pénal</b> : réclusion criminelle à perpétuité", 1000, 150, 840, W(4, 1)[0] - 0.3, b, 'quote')
text("<b>Faux en écriture publique = un crime</b>", 1000, 290, 840, W(4, 1)[0] + 1.2, b, 'quote')
text("<b>Crime : instruction préparatoire obligatoire</b>", 1000, 410, 840, W(4, 2)[0] - 0.3, b, 'quote')
text("<b>Citation directe : non ouverte</b>", 1000, 530, 840, W(4, 2)[0] + 1.6, b, 'quote ocrebox')
text("<b>Constitution de partie civile (art. 90 et 91) : la voie ouverte</b><br><span class='cap2'>Elle provoque l'information judiciaire lorsque le parquet classe.</span>", 1000, 670, 840, W(4, 3)[0] - 0.3, b, 'quote')

# --- 5 : ce que demande la plainte
a, b = Q(5)
heads(a + 0.2, b, 'LES DEMANDES AU DOYEN', 'LA PLAINTE EN BREF')
pic('pc-demandes.png', 80, 140, 840, a + 0.4, b, "Plainte, p. 11 : « Demandes au Doyen des Juges d'Instruction »", find=("Saisir sans délai un Juge d'Instruction de cette affaire", "Ordonner tous les actes d'instruction utiles à la manifestation de la vérité"), cls='p5')
text("<b>Mis en cause</b> : X · Albin Féliho · Lise Féliho · Florentin-Lin Féliho · Nina Féliho · Me Victorien Olatundji Fade · toutes autres personnes que l'instruction révélerait", 1000, 140, 840, W(5, 0)[0] - 0.3, b, 'quote')
text("<b>Qualifications</b> : faux en écriture publique (crime, art. 303) · usage de faux (délit, art. 305) · recel", 1000, 400, 840, W(5, 1)[0] - 0.3, b, 'quote')
text("<b>Consignation</b> (art. 91) · <b>élection de domicile</b> chez Me Narcisse Atoun (art. 94)", 1000, 620, 840, W(5, 3)[0] - 0.3, b, 'quote')

# --- 6 : ce que la plainte reproche à l'enquête préliminaire
a, b = Q(6)
text("CE QUE LA PLAINTE REPROCHE À L'ENQUÊTE PRÉLIMINAIRE", 80, 62, 1760, a + 0.2, b, 'colhead wide')
RP = ["« l'ignorance du procès-verbal de compulsion d'huissier de justice du 19 décembre 2017, une preuve matérielle essentielle et à charge »",
      "« L'enquête n'a pas entendu les protagonistes essentiels, notamment les deux principaux : le juge ayant signé le jugement […] et l'avocat »",
      "« les officiers de police judiciaire ont procédé à l'audition de, notamment Albin et Honorine FELIHO, sans jamais en informer le plaignant »",
      "« Il se focalise, de manière erronée et disproportionnée, sur le notaire BALLEY »"]
for i, q in enumerate(RP):
    text(f'<span class="num">{"①②③④"[i]}</span> {q}', 160, 150 + i * 200, 1600, W(6, i)[0] - 0.3, b, 'quote')
text("Plainte avec constitution de partie civile, pp. 9 à 11 — les termes sont ceux de la plainte", 160, 960, 1600, W(6, 3)[0], b, 'cap2')

# --- 7 : le bordereau
a, b = Q(7)
heads(a + 0.2, b, 'LE BORDEREAU DES PIÈCES JOINTES', 'DES PIÈCES PUBLIÉES SUR LE SITE')
pic('pc-bordereau.png', 80, 140, 640, a + 0.4, b, "Plainte, p. 12 : bordereau des dix pièces jointes", find=("Copie du Jugement", "Certificat d'appel en date du 17 novembre 2014", "Lettre de transmission du 19 septembre 2007"), cls='p7')
text("<b>Pièce n° 2</b> · le jugement du 31 octobre 2014<br><b>Pièce n° 3</b> · sa signification, 9 mars 2015<br><b>Pièce n° 4</b> · le procès-verbal de compulsion, 19 décembre 2017", 800, 150, 1040, W(7, 1)[0] - 0.3, b, 'quote')
text("<b>Pièce n° 5</b> · la décision de classement du 3 juillet 2025, reçue le 26 septembre", 800, 420, 1040, W(7, 1)[0] + 1.5, b, 'quote')
text("<b>Pièce n° 9</b> · le certificat d'appel du 17 novembre 2014", 800, 550, 1040, W(7, 2)[0] - 0.3, b, 'quote')
text("<b>Pièce n° 10</b> · la lettre du notaire Gangnito à Me Fade, 19 septembre 2007", 800, 680, 1040, W(7, 3)[0] - 0.3, b, 'quote')

# --- 8 : les durées
a, b = Q(8)
counter(88, 'JOURS', 40, 330, W(8, 0)[0] - 0.2, b, W(8, 0)[0], W(8, 0)[0] + 1.4, w=600, size=130, sub="du 3 juillet au 29 septembre 2025 : du classement au dépôt de la plainte")
counter(107, 'JOURS', 660, 330, W(8, 1)[0] - 0.2, b, W(8, 1)[0], W(8, 1)[0] + 1.6, w=600, size=130, sub="du 29 septembre 2025 au 14 janvier 2026 : du dépôt à la lettre du ministre")
counter(381, 'JOURS', 1280, 330, W(8, 2)[0] - 0.2, b, W(8, 2)[0], W(8, 2)[0] + 2.6, w=600, size=130, sub="du 29 septembre 2025 au 15 octobre 2026 (date de ce film) : aucune suite connue")

# --- 9 : questions
a, b = Q(9)
QS = ["Quelle suite a été donnée à la plainte avec constitution de partie civile reçue le 29 septembre 2025 ?",
      "Une consignation a-t-elle été fixée, comme la plainte le demande et comme le prévoit l'article 91 ?",
      "Un juge d'instruction a-t-il été saisi ? À défaut, quelle durée est raisonnable pour saisir un juge d'instruction dans une affaire criminelle ?",
      "Où les notifications adressées au domicile élu chez Me Atoun doivent-elles parvenir, et en existe-t-il ?"]
for i, q in enumerate(QS):
    text(q, 160, 120 + i * 200, 1600, a + 0.6 + i * 1.4, b - 0.5, 'quest')

# --- carton final
a, b = SQ[15]
text('wadagni2026-verite.com', 0, 300, 1920, a + 0.6, b, 'url', 0.8)
text('Les pièces reproduites dans ce film sont publiées sur le site, avec leurs empreintes numériques.', 0, 400, 1920, a + 1.6, b, 'finsmall', 0.8)
text("Les extraits reproduits sont des copies partielles ; les coordonnées personnelles sont occultées. Le récépissé du Trésor public porte la nature « PLAINTE » et le montant de 3 000 FCFA : il n'est pas présenté comme la consignation, que la plainte demande au Doyen d'ordonner. "
     "La page déposée porte une mention manuscrite non datée, non interprétée. Les références et les articles sont ceux que cite la plainte.", 160, 560, 1600, a + 2.6, b, 'precis', 0.8)

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
html = f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>La voie indiquée, déjà empruntée</title><style>{CSS}</style></head><body><div id="stage">\n' + '\n'.join(EL) + f'\n</div><script>{JS}</script></body></html>'
open(os.path.join(here, 'motion.html'), 'w', encoding='utf-8').write(html)
json.dump({'total': TOTAL, 'sequences': {str(k_): v for k_, v in SQ.items()}, 'cues': cues}, open(os.path.join(out, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
print('durée totale', round(TOTAL, 1), 's ; séquences', {k_: (round(a_, 1), round(b_, 1)) for k_, (a_, b_) in SQ.items()})
