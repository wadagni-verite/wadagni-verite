# -*- coding: utf-8 -*-
"""Film « Où est l'acte ? » : le jugement du 31 octobre 2014, la parcelle B du lot 488, Me Victorien Olatundji Fade et le silence de l'Ordre.
Usage : python3 build.py <dossier_modèles_kokoro> <dossier_sortie>   (voix Kokoro ff_siwis ; cache des phrases dans <sortie>/cache)
Écrit : motion.html (rendu par render.js), <sortie>/audio.wav, film.fr.srt, film.fr.vtt, timeline.json.
Chaque image provient d'une pièce publiée sur le site (pieces/, pieces/procedures-benin/) ; les recadrages sont dans img/.
"""
import sys, os, json, hashlib, datetime as dt
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

models, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
SR = 24000

def Z(sp, lead, tail, *s, gap=0.3): return {'speed': sp, 'gap': gap, 'lead': lead, 'tail': tail, 's': list(s)}
# ------------------------------------------------------------------ texte : (sous-titre, texte lu) par séquence
SEQ = {
 1: Z(1.14, 1.6, 1.6,
      ("Le 31 octobre 2014, le tribunal de Cotonou constate que Gilles Féliho a exécuté volontairement le testament.", "Le trente et un octobre deux mille quatorze, le tribunal de Cotonou constate que Gilles Féliho a exécuté volontairement le testament."),
      ("La raison : il aurait « même déjà disposé » de la parcelle bâtie du lot 488.", "La raison : il aurait « même déjà disposé » de la parcelle bâtie du lot quatre cent quatre-vingt-huit."),
      ("Disposé par quel acte ? Le jugement n'en cite aucun.", "Disposé par quel acte ? Le jugement n'en cite aucun.")),
 2: Z(1.14, 0.9, 1.8,
      ("Le 19 décembre 2017, à la demande de Gilles Féliho, un huissier compulse les registres.", "Le dix-neuf décembre deux mille dix-sept, à la demande de Gilles Féliho, un huissier compulse les registres."),
      ("Mairie de Cotonou : superficie « néant ». Institut géographique national : aucun document.", "Mairie de Cotonou : superficie « néant ». Institut géographique national : aucun document."),
      ("Gilles Féliho l'avait dit : soit quelqu'un a vendu à sa place, soit la parcelle n'existe pas. Les registres répondent : néant.", "Gilles Féliho l'avait dit : soit quelqu'un a vendu à sa place, soit la parcelle n'existe pas. Les registres répondent : néant.")),
 3: Z(1.14, 0.9, 1.8,
      ("Qui a invoqué cette vente ? Les héritiers, dans leurs conclusions.", "Qui a invoqué cette vente ? Les héritiers, dans leurs conclusions."),
      ("Ils sont assistés de Maître Victorien Olatundji Fade, avocat à la Cour.", "Ils sont assistés de Maître Victorien Fade, avocat à la Cour."),
      ("Leurs conclusions écrivent : « en vendant la parcelle bâtie du lot 488, quartier Godomey ».", "Leurs conclusions écrivent : « en vendant la parcelle bâtie du lot quatre cent quatre-vingt-huit, quartier Godomey »."),
      ("Le jugement écrit : quartier Gbégamey. Deux quartiers pour une seule parcelle.", "Le jugement écrit : quartier Gbégamey. Deux quartiers pour une seule parcelle.")),
 4: Z(1.12, 0.9, 2.0,
      ("Dans une procédure où l'avocat est obligatoire, seuls les avocats des parties déposent les pièces.", "Dans une procédure où l'avocat est obligatoire, seuls les avocats des parties déposent les pièces."),
      ("Et ces pièces sont débattues contradictoirement, rappelle le plaignant.", "Et ces pièces sont débattues contradictoirement, rappelle le plaignant."),
      ("Si un acte de disposition existe, il est donc entre les mains de Maître Fade.", "Si un acte de disposition existe, il est donc entre les mains de Maître Fade."),
      ("Qu'il le montre : une date, un officier, un acquéreur.", "Qu'il le montre : une date, un officier, un acquéreur."),
      ("Près de douze ans après le jugement, aucun acte n'a été montré au plaignant.", "Près de douze ans après le jugement, aucun acte n'a été montré au plaignant.")),
 5: Z(1.14, 0.9, 2.0,
      ("Le 19 septembre 2007, le notaire écrit à Maître Fade, « mandataire » de Gilles Féliho.", "Le dix-neuf septembre deux mille sept, le notaire écrit à Maître Fade, « mandataire » de Gilles Féliho."),
      ("Août 2007 : sa sœur écrit que Maître Fade « fera l'affaire », « maîtrisant le dossier pour l'avoir suivi à son début ».", "Août deux mille sept : sa sœur écrit que Maître Fade « fera l'affaire », « maîtrisant le dossier pour l'avoir suivi à son début »."),
      ("Juin 2013 : Maître Fade assiste trois héritiers qui citent Gilles Féliho comme « complice » de diffamation.", "Juin deux mille treize : Maître Fade assiste trois héritiers qui citent Gilles Féliho comme « complice » de diffamation."),
      ("2014 : il assiste les héritiers contre lui dans l'affaire du testament. Mars 2015 : il fait signifier le jugement.", "Deux mille quatorze : il assiste les héritiers contre lui dans l'affaire du testament. Mars deux mille quinze : il fait signifier le jugement."),
      ("Le mandataire d'hier, l'adversaire d'aujourd'hui.", "Le mandataire d'hier, l'adversaire d'aujourd'hui.")),
 6: Z(1.14, 0.9, 1.8,
      ("La règle que la profession s'est donnée en mai 2023 : pas d'affaire d'un nouveau client si la connaissance des affaires de l'ancien client le favoriserait.", "La règle que la profession s'est donnée en mai deux mille vingt-trois : pas d'affaire d'un nouveau client si la connaissance des affaires de l'ancien client le favoriserait."),
      ("En cas de conflit d'intérêts, l'avocat ne peut être le conseil ou le défenseur de plus d'un client dans une même affaire.", "En cas de conflit d'intérêts, l'avocat ne peut être le conseil ou le défenseur de plus d'un client dans une même affaire."),
      ("Le 2 avril 2023, le plaignant dépose une plainte déontologique devant le Bâtonnier.", "Le deux avril deux mille vingt-trois, le plaignant dépose une plainte déontologique devant le Bâtonnier."),
      ("Complicité de faux en écriture publique. Usage de faux en écriture publique.", "Complicité de faux en écriture publique. Usage de faux en écriture publique.")),
 7: Z(1.14, 0.9, 1.8,
      ("Le 12 mars 2025, la Brigade criminelle convoque Maître Fade pour le 19 mars, à 9 heures.", "Le douze mars deux mille vingt-cinq, la Brigade criminelle convoque Maître Fade pour le dix-neuf mars, à neuf heures."),
      ("La convocation rappelle l'article 56 du Code de procédure pénale : les personnes convoquées sont tenues de comparaître, sous peine d'y être contraintes par la force publique.", "La convocation rappelle l'article cinquante-six du Code de procédure pénale : les personnes convoquées sont tenues de comparaître, sous peine d'y être contraintes par la force publique."),
      ("Le 17 mars, le Bâtonnier invoque sa « prérogative de consultation » auprès du procureur général.", "Le dix-sept mars, le Bâtonnier invoque sa « prérogative de consultation » auprès du procureur général."),
      ("Le 19 mars, Maître Fade « ne s'est pas présenté ». Le notaire, lui, est entendu de 9 h 14 à 10 h 52.", "Le dix-neuf mars, Maître Fade « ne s'est pas présenté ». Le notaire, lui, est entendu de neuf heures quatorze à dix heures cinquante-deux."),
      ("Une convocation oblige. Une invitation, non.", "Une convocation oblige. Une invitation, non.")),
 8: Z(1.14, 0.9, 1.8,
      ("2 avril 2023 : plainte déontologique. 20 juin 2024 : relance. Aucune décision connue.", "Deux avril deux mille vingt-trois : plainte déontologique. Vingt juin deux mille vingt-quatre : relance. Aucune décision connue."),
      ("Loi sur le barreau, article 30 : sans décision du conseil de discipline dans les trois mois, le procureur général peut saisir directement la Cour d'appel.", "Loi sur le barreau, article trente : sans décision du conseil de discipline dans les trois mois, le procureur général peut saisir directement la Cour d'appel."),
      ("Le 14 mars 2025, le procureur général écrit au Bâtonnier. Le 17 mars : « la cause est déjà en instruction ».", "Le quatorze mars deux mille vingt-cinq, le procureur général écrit au Bâtonnier. Le dix-sept mars : « la cause est déjà en instruction »."),
      ("1 293 jours depuis la plainte. 581 jours depuis la lettre du procureur général.", "Mille deux cent quatre-vingt-treize jours depuis la plainte. Cinq cent quatre-vingt-un jours depuis la lettre du procureur général."),
      ("Le pouvoir de saisir la Cour d'appel existe. Qui l'exerce ?", "Le pouvoir de saisir la Cour d'appel existe. Qui l'exerce ?")),
 9: Z(1.14, 0.9, 2.0,
      ("À Maître Fade : où est l'acte de disposition ? Quelle date, quel officier, quel acquéreur ?", "À Maître Fade : où est l'acte de disposition ? Quelle date, quel officier, quel acquéreur ?"),
      ("À Maître Fade : pourquoi ne pas vous être présenté à la convocation de la Brigade criminelle ?", "À Maître Fade : pourquoi ne pas vous être présenté à la convocation de la Brigade criminelle ?"),
      ("Au Bâtonnier : où est la décision sur la plainte de 2023 ?", "Au Bâtonnier : où est la décision sur la plainte de deux mille vingt-trois ?"),
      ("Au procureur général : pourquoi ne pas saisir la Cour d'appel ?", "Au procureur général : pourquoi ne pas saisir la Cour d'appel ?"), gap=0.5),
 10: Z(1.12, 0.9, 2.2,
      ("Une seule pièce suffit.", "Une seule pièce suffit."),
      ("Si l'acte existe, qu'il le montre.", "Si l'acte existe, qu'il le montre."),
      ("Tant qu'il ne le montre pas, le constat du jugement repose sur un acte que personne n'a vu.", "Tant qu'il ne le montre pas, le constat du jugement repose sur un acte que personne n'a vu.")),
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
TOTAL = t + FINAL; SEQT[16] = (t, TOTAL)

def ts(a, f='srt'):
    h = int(a // 3600); m = int(a % 3600 // 60); s = a % 60; sep = ',' if f == 'srt' else '.'
    return f"{h:02d}:{m:02d}:{int(s):02d}{sep}{int(round((s - int(s)) * 1000)):03d}"
open(os.path.join(out, 'film.fr.srt'), 'w', encoding='utf-8').write('\n'.join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{s}\n" for i, (a, b, s) in enumerate(cues)))
open(os.path.join(out, 'film.fr.vtt'), 'w', encoding='utf-8').write('WEBVTT\n\n' + '\n'.join(f"{i+1}\n{ts(a,'vtt')} --> {ts(b,'vtt')}\n{s}\n" for i, (a, b, s) in enumerate(cues)))


# ------------------------------------------------------------------ bande son : voix + note à 55 Hz + tampons, tic-tac, battements
n_ = int((TOTAL + 1) * SR)
voice = np.zeros(n_, dtype=np.float32)
for a, x in clips:
    i = int(a * SR); voice[i:i + len(x)] += x
voice *= 0.9 / max(1e-6, np.abs(voice).max())
tt = np.arange(n_) / SR
env = np.zeros(n_, dtype=np.float32)
def seg(a, b, v):
    env[int(a * SR):int(b * SR)] = v
seg(0, SEQT[8][1], 1.0)
env[:int(2 * SR)] *= np.linspace(0, 1, int(2 * SR))
fond = (10 ** (-26 / 20)) * np.sin(2 * np.pi * 55 * tt).astype(np.float32) * env
rng = np.random.default_rng(13)
sfx = np.zeros(n_, dtype=np.float32)
def burst(at, dur, amp, lo, hi):
    m = int(dur * SR); x = rng.standard_normal(m).astype(np.float32)
    sp = np.fft.rfft(x); f = np.fft.rfftfreq(m, 1 / SR); sp[(f < lo) | (f > hi)] = 0
    x = np.fft.irfft(sp, m).astype(np.float32); x /= max(1e-6, np.abs(x).max()); x *= np.hanning(m).astype(np.float32) ** 0.5 * amp
    i = int(at * SR); sfx[i:i + m] += x[:max(0, min(m, n_ - i))]
def thud(at, dur=0.5, f0=95, amp=0.5):
    m = int(dur * SR); x = np.arange(m) / SR
    fr = f0 * np.exp(-x * 5); ph = 2 * np.pi * np.cumsum(fr) / SR
    y = np.sin(ph) * np.exp(-x * 9)
    nz = rng.standard_normal(m).astype(np.float32); sp = np.fft.rfft(nz); f = np.fft.rfftfreq(m, 1 / SR); sp[f > 900] = 0
    y = y + 0.5 * np.fft.irfft(sp, m) * np.exp(-x * 14) / max(1e-6, np.abs(np.fft.irfft(sp, m)).max())
    i = int(at * SR); y = (y * amp).astype(np.float32); sfx[i:i + m] += y[:max(0, min(m, n_ - i))]
def tick(at, amp=0.25):
    m = int(0.02 * SR); x = np.arange(m) / SR
    y = (np.sin(2 * np.pi * 2300 * x) * np.exp(-x * 220) * amp).astype(np.float32)
    i = int(at * SR); sfx[i:i + m] += y[:max(0, min(m, n_ - i))]
def heart(at, amp=0.55):
    thud(at, 0.35, 62, amp); thud(at + 0.34, 0.35, 55, amp * 0.8)
for sq in (2, 4, 6, 8):
    burst(SEQT[sq][0] + 0.1, 0.4, 10 ** (-18 / 20), 400, 2500)
thud(SEQT[1][0] + 1.0, 0.4, 120, 0.35)           # tampon : le jugement
thud(T[(1, 2)][0] + 0.2, 0.7, 80, 0.7)           # « quel acte ? »
thud(T[(2, 1)][0] + 0.2, 0.5, 100, 0.5)          # « néant »
for i, tm in enumerate((T[(5, 0)][0], T[(5, 2)][0], T[(5, 3)][0])):
    thud(tm + 0.1, 0.4, 105, 0.35)
thud(T[(7, 1)][0] + 0.2, 0.7, 70, 0.7)           # force publique
_tt = T[(4, 4)][0]; _iv = 0.4                    # le compteur de jours, de plus en plus lent
while _tt < T[(4, 4)][1] + 2.5:
    tick(_tt, 0.28); _tt += _iv; _iv *= 1.07
_tt = T[(8, 3)][0]; _iv = 0.3
while _tt < T[(8, 3)][1] + 1.5:
    tick(_tt, 0.28); _tt += _iv; _iv *= 1.04
heart(T[(9, 3)][1] + 0.3)
heart(SEQT[10][1] - 2.2, 0.5)
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

import json as _json
def kf(inner, keys, style='', cls=''):
    return f"<div class=\"kf {cls}\" data-k='{_json.dumps(keys)}' style=\"{style}\">{inner}</div>"
SIL = ('<svg width="260" height="560" viewBox="0 0 260 560"><circle cx="130" cy="70" r="52" fill="#94a3b8"/>'
       '<path d="M40 560 L52 220 Q58 150 130 150 Q202 150 208 220 L220 560 Z" fill="#94a3b8"/>'
       '<rect x="168" y="300" width="14" height="150" rx="7" fill="#7b8ba3" transform="rotate(-62 175 305)"/></svg>')
FOLD = ('<div style="width:190px;height:140px;background:#e8dcc0;border:3px solid #b9a77a;border-radius:6px;position:relative;box-shadow:0 8px 24px rgba(0,0,0,.5)">'
        '<div style="position:absolute;left:-3px;top:-22px;width:80px;height:22px;background:#e8dcc0;border:3px solid #b9a77a;border-bottom:0;border-radius:6px 6px 0 0"></div>'
        '<div style="position:absolute;left:18px;top:48px;border:4px solid #c0392b;color:#c0392b;font:800 30px DejaVu Sans;letter-spacing:.08em;padding:2px 10px;transform:rotate(-8deg)">PLAINTE</div></div>')
import random as _r
_r.seed(5)
DUST = '<svg width="520" height="420" viewBox="0 0 520 420">' + ''.join(
    f'<circle cx="{_r.randint(10,510)}" cy="{_r.randint(30,410)}" r="{_r.choice([1.5,2,2.5,3,4])}" fill="#d6c9a8" opacity="{_r.choice([.35,.5,.65,.8])}"/>' for _ in range(160)) + '</svg>'

CAL = ["DÉCEMBRE 2024", "JANVIER 2025", "FÉVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOÛT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DÉCEMBRE", "JANVIER 2026", "FÉVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOÛT", "SEPTEMBRE", "OCTOBRE 2026"]
def mail(date, sujet, corps, x, y, w, a, b, de="Autorité de Protection des Données Personnelles"):
    el(f'<div class="mail"><div class="mh">{de}<span>{date}</span></div><div class="ms">{sujet}</div>{corps}</div>', a, b, 0.5, 'piece', f'left:{x}px;top:{y}px;width:{w}px')
def arrow(a, b, x, y): text("→", x, y, 80, a, b, 'bigtext ocre')

def arrow(a, b, x, y): text("→", x, y, 80, a, b, 'bigtext ocre')
def qcard(src, date, html, x, y, w, a, b):   # citation typée d'une pièce (courriel), avec sa source
    el(f'<div class="mail"><div class="mh">{src}<span>{date}</span></div>{html}</div>', a, b, 0.5, 'piece', f'left:{x}px;top:{y}px;width:{w}px')

el("Ce film présente des pièces publiées sur le site : jugement, procès-verbal, convocations, lettres, plainte déontologique. Aucune infraction n'est imputée par ce film ; les qualifications relèvent des juridictions. Droit de réponse ouvert à Me Fade, à l'Ordre et au parquet général.", 0, TOTAL, 0.6, 'bandeau')

# --- 1 : le constat sans acte
a, b = Q(1); W1 = [W(1, i) for i in range(3)]
text("31 OCTOBRE 2014 · LE JUGEMENT N° 114/14", 80, 62, 1760, a + 0.3, b, 'colhead wide')
pic('j8c.png', 80, 140, 840, a + 0.4, W1[1][0] - 0.3, "Jugement n° 114/14/3ᵉ CH-EP du 31 octobre 2014, dispositif", h=640, cls='f1')
pic('j5c.png', 80, 140, 840, W1[1][0] - 0.3, b, "Jugement, p. 5 : « a même déjà disposé de cet immeuble »", h=640, cls='f1')
text("« Constate que Gilles Sixte Féliho <b>a exécuté les dispositions testamentaires de manière volontaire</b> »", 1000, 150, 840, W1[0][0] - 0.2, b, 'quote')
text("« Que Gilles Sixte Féliho <b>a même déjà disposé de cet immeuble</b> » : la parcelle bâtie du lot 488", 1000, 330, 840, W1[1][0] - 0.2, b, 'quote')
text("<div class='pulse qa'>QUEL ACTE ?</div>", 1000, 520, 840, W1[2][0] - 0.2, b, '')
text("Le jugement n'en cite aucun.", 1000, 740, 840, W1[2][0] + 1.6, b, 'nm ocrebox')

# --- 2 : l'huissier, les registres
a, b = Q(2); W2 = [W(2, i) for i in range(3)]
heads(a + 0.2, b, 'PROCÈS-VERBAL DE COMPULSION', 'CE QUE RÉPONDENT LES REGISTRES')
pic('pvc1c.png', 80, 140, 840, a + 0.4, W2[1][0] - 0.3, "Procès-verbal de compulsion du 19 décembre 2017, p. 1", h=640, cls='f2')
pic('pvc2c.png', 80, 140, 840, W2[1][0] - 0.3, b, "Procès-verbal de compulsion, p. 2 : mairie de Cotonou, « superficie : néant »", h=640, cls='f2')
card(19, 'DÉC.', 2017, 1000, 150, W2[0][0] - 0.2, b, 'big', 'compulsion')
text("« Qu'en réalité, il n'a <b>jamais aliéné</b> à quelque titre que ce soit ladite parcelle »", 1450, 170, 420, W2[0][0] + 0.8, b, 'ctext')
text("Mairie de Cotonou · superficie : <b>néant</b>", 1000, 560, 840, W2[1][0] - 0.2, b, 'nm')
text("Institut géographique national · <b>aucun document</b>", 1000, 660, 840, W2[1][0] + 2.4, b, 'nm')
text("Soit quelqu'un a vendu à sa place.<br>Soit la parcelle n'existe pas.", 1000, 790, 840, W2[2][0] + 1.0, b, 'bigtext')

# --- 3 : qui a invoqué la vente
a, b = Q(3); W3 = [W(3, i) for i in range(4)]
heads(a + 0.2, b, 'LES PARTIES ET LEUR AVOCAT', 'QUI A ALLÉGUÉ LA VENTE ?')
pic('j1c.png', 80, 140, 840, a + 0.4, W3[2][0] - 0.3, "Jugement, p. 1 : « tous assistés de Maître Victorien Olatoundji Fade »", h=640, cls='f3')
pic('j4c.png', 80, 140, 840, W3[2][0] - 0.3, b, "Jugement, p. 4 : les conclusions des héritiers", h=640, cls='f3')
text("<b>Les héritiers</b>, dans leurs conclusions", 1000, 150, 840, W3[0][0] - 0.2, b, 'quote')
text("<b>Assistés de Me Victorien Olatundji Fade</b>, avocat à la Cour", 1000, 270, 840, W3[1][0] - 0.2, b, 'quote ocrebox')
text("Conclusions des héritiers : quartier <b>Godomey</b>", 1000, 440, 840, W3[2][0] - 0.2, b, 'nm')
text("Jugement : quartier <b>Gbégamey</b>", 1000, 540, 840, W3[3][0] - 0.2, b, 'nm')
text("Procès-verbal de 2017 : lotissement de <b>Gbégamey</b>", 1000, 640, 840, W3[3][0] + 1.4, b, 'nm')
text("Deux quartiers pour une seule parcelle.", 1000, 780, 840, W3[3][0] + 3.0, b, 'bigtext')

# --- 4 : l'acte, s'il existe
a, b = Q(4); W4 = [W(4, i) for i in range(5)]
text("L'ACTE DE DISPOSITION", 80, 62, 840, a + 0.2, b, 'colhead'); text("QUI PEUT LE PRODUIRE ?", 1000, 62, 840, a + 0.2, b, 'colhead')
el('', a, b, 0.5, 'vbar', 'left:959px;top:56px;height:880px')
FR = ('<div style="width:840px;height:760px;border:5px dashed rgba(199,210,254,.5);border-radius:14px;padding:30px 36px;font:700 34px DejaVu Serif;color:#e2e8f0;line-height:1.3">'
      'ACTE DE DISPOSITION<br><span style="font-size:26px;color:#94a3b8;font-weight:400">de la parcelle B du lot 488, après le décès du 3 décembre 2010</span></div>')
el(FR, a + 0.3, b, 0.6, '', 'left:80px;top:140px;width:840px;height:760px')
for i, (lb, ta) in enumerate([("DATE", W4[3][0] - 0.2), ("OFFICIER", W4[3][0] + 0.9), ("ACQUÉREUR", W4[3][0] + 1.8)]):
    text(f"<span style='color:#94a3b8;font-size:30px'>{lb}</span> <span class='qa' style='font-size:90px'>?</span>", 120, 330 + i * 170, 760, ta, b, '')
text("Avocat obligatoire : <b>seuls les avocats des parties déposent les pièces</b>", 1000, 150, 840, W4[0][0] - 0.2, b, 'quote')
text("Ces pièces sont <b>débattues contradictoirement</b>", 1000, 300, 840, W4[1][0] - 0.2, b, 'quote')
text("Si l'acte existe, <b>il est entre les mains de Me Fade</b>", 1000, 430, 840, W4[2][0] - 0.2, b, 'quote ocrebox')
text("Qu'il le montre.", 1000, 590, 840, W4[3][0] - 0.2, b, 'bigtext')
counter(4368, 'JOURS', 1000, 690, W4[4][0] - 0.2, b, W4[4][0], W4[4][0] + 3.2, w=840, size=120, sub="du 31 octobre 2014 au 16 octobre 2026 : aucun acte montré au plaignant")

# --- 5 : mandataire, puis adversaire
a, b = Q(5); W5 = [W(5, i) for i in range(5)]
heads(a + 0.2, b, 'LES PIÈCES', 'DE MANDATAIRE À ADVERSAIRE')
pic('gang.png', 80, 140, 840, a + 0.4, W5[1][0] - 0.3, "Lettre du notaire Gangnito à Me Fade, 19 septembre 2007", h=640, cls='f5')
qcard("Courriels de Lise Féliho, août 2007", "« a/s ta maison »", "<p>« je voulais confier ça à FADE et tu as refusé »</p><p>« maîtrisant le dossier pour l'avoir suivi à son début, il fera l'affaire »</p>", 80, 160, 840, W5[1][0] - 0.3, W5[2][0] - 0.3)
pic('cd1.png', 80, 140, 840, W5[2][0] - 0.3, W5[2][1] + 3.0, "Citation directe, 4 et 7 juin 2013 : héritiers « assistés de Maître Victorien Olatoundji Fade »", h=640, cls='f5')
pic('cd5.png', 80, 140, 840, W5[2][1] + 3.0, W5[3][0] - 0.3, "Citation directe, p. 5 : Gilles Féliho « complice du délit de diffamation »", h=640, cls='f5')
pic('j1c.png', 80, 140, 840, W5[3][0] - 0.3, W5[3][0] + 4.2, "Jugement du 31 octobre 2014 : « tous assistés de Maître Victorien Olatoundji Fade »", h=640, cls='f5')
pic('sig.png', 80, 140, 840, W5[3][0] + 4.2, b, "Signification du jugement, 9 mars 2015 : « tous assistés de Maître Victorien O. Fade »", h=640, cls='f5')
card(19, 'SEPT.', 2007, 1000, 150, W5[0][0] - 0.2, b, 'sm', 'mandataire')
card(4, 'JUIN', 2013, 1290, 150, W5[2][0] - 0.2, b, 'sm', 'citation directe')
card(31, 'OCT.', 2014, 1000, 430, W5[3][0] - 0.2, b, 'sm', 'jugement')
card(9, 'MARS', 2015, 1290, 430, W5[3][0] + 3.6, b, 'sm', 'signification')
text("Le mandataire d'hier,<br><span class='ocre'>l'adversaire d'aujourd'hui.</span>", 1000, 740, 840, W5[4][0] - 0.2, b, 'bigtext')

# --- 6 : la règle
a, b = Q(6); W6 = [W(6, i) for i in range(4)]
heads(a + 0.2, b, 'LA RÈGLE ÉCRITE', 'LA PLAINTE DÉONTOLOGIQUE')
pic('ri12.png', 80, 140, 840, a + 0.4, W6[2][0] - 0.3, "Règlement intérieur harmonisé des barreaux de l'espace UEMOA (5 mai 2023), art. 24.1", h=640, cls='f6')
pic('pd.png', 80, 140, 840, W6[2][0] - 0.3, b, "Plainte déontologique au Bâtonnier, 2 avril 2023, p. 1 (coordonnées occultées)", h=640, cls='f6')
text("« […] ne peut accepter l'affaire d'un nouveau client […] lorsque la connaissance par l'avocat des affaires de <b>l'ancien client favoriserait le nouveau client</b> »", 1000, 150, 840, W6[0][0] - 0.2, b, 'quote')
text("« ne peut être ni le conseil ni le représentant ou le défenseur <b>de plus d'un client dans une même affaire</b> »", 1000, 400, 840, W6[1][0] - 0.2, b, 'quote')
card(2, 'AVR.', 2023, 1000, 150, W6[2][0] - 0.2, b, 'sm', 'plainte déontologique')
text("<b>Complicité</b> de faux en écriture publique<br><b>Usage</b> de faux en écriture publique<br><span class='cap2'>articles 303 à 305 et 22 du Code pénal, tels que cités dans la plainte</span>", 1000, 430, 840, W6[3][0] - 0.2, b, 'quote ocrebox')

# --- 7 : la convocation qu'on ne peut pas ignorer
a, b = Q(7); W7 = [W(7, i) for i in range(5)]
heads(a + 0.2, b, 'CONVOQUÉ, NON PRÉSENTÉ', 'CE QUE DISENT LES PIÈCES')
pic('conv.png', 80, 140, 840, a + 0.4, W7[2][0] - 0.3, "Brigade criminelle, convocation n° 141/DGPR/DPJ/BC/2025", h=640, cls='f7')
pic('bat.png', 80, 140, 840, W7[2][0] - 0.3, W7[3][0] - 0.3, "Le Bâtonnier au procureur général, 17 mars 2025", h=640, cls='f7')
pic('rel.png', 80, 140, 840, W7[3][0] - 0.3, b, "Brigade criminelle, 25 mars 2025 : « il ne s'est pas présenté »", h=640, cls='f7')
card(12, 'MARS', 2025, 1000, 150, W7[0][0] - 0.2, b, 'sm', 'convocation')
arrow(W7[0][0] + 1.0, b, 1265, 190); card(19, 'MARS', 2025, 1340, 150, W7[0][0] + 1.0, b, 'sm', 'comparution')
text("<b>Art. 56 du Code de procédure pénale</b> : « les personnes convoquées sont tenues de comparaître […] elles peuvent y être contraintes par la force publique »", 1000, 430, 840, W7[1][0] - 0.2, b, 'quote ocrebox')
text("17 mars · le Bâtonnier : « prérogative de consultation »", 1000, 650, 840, W7[2][0] - 0.2, b, 'nm')
text("19 mars · « il ne s'est pas présenté »<br>Le notaire est entendu de 9 h 14 à 10 h 52", 1000, 750, 840, W7[3][0] - 0.2, b, 'nm')
text("Une convocation <span class='ocre'>oblige</span>.<br>Une invitation, non.", 1000, 870, 840, W7[4][0] - 0.2, b, 'bigtext')

# --- 8 : l'Ordre et le procureur général
a, b = Q(8); W8 = [W(8, i) for i in range(5)]
heads(a + 0.2, b, 'LA LOI SUR LE BARREAU (1965)', 'CE QUI S\'EST PASSÉ')
pic('l65b.png', 80, 140, 840, W8[1][0] - 0.3, b, "Loi sur le barreau (avril 1965), art. 30 : plaintes transmises, délais de trois mois, saisine directe de la Cour d'appel", h=640, cls='f8')
card(2, 'AVR.', 2023, 80, 160, a + 0.4, W8[1][0] - 0.3, 'big', 'plainte déontologique')
text("20 juin 2024 · relance au Bâtonnier<br><b>aucune décision connue</b>", 560, 220, 360, W8[0][0] + 1.6, W8[1][0] - 0.3, 'ctext')
text("Art. 30 : <b>trois mois</b> sans décision du conseil de discipline → le procureur général <b>peut saisir directement la Cour d'appel</b>", 1000, 150, 840, W8[1][0] - 0.2, b, 'quote')
text("14 mars 2025 · le procureur général écrit au Bâtonnier<br>17 mars · « la cause est déjà en instruction »", 1000, 400, 840, W8[2][0] - 0.2, b, 'nm')
counter(1293, 'JOURS', 1000, 520, W8[3][0] - 0.2, b, W8[3][0], W8[3][0] + 2.4, w=840, size=100, sub="depuis la plainte déontologique du 2 avril 2023")
counter(581, 'JOURS', 1000, 700, W8[3][0] + 1.6, b, W8[3][0] + 2.0, W8[3][0] + 4.0, w=840, size=100, sub="depuis la lettre du procureur général du 14 mars 2025")
text("Le pouvoir existe.<br><span class='ocre'>Qui l'exerce ?</span>", 1000, 890, 840, W8[4][0] - 0.2, b, 'bigtext')

# --- 9 : les questions
a, b = Q(9); W9 = [W(9, i) for i in range(4)]
QS = [("À ME FADE", "Où est <b>l'acte de disposition</b> ? Quelle date, quel officier, quel acquéreur ?"),
      ("À ME FADE", "Pourquoi ne pas vous être présenté <b>à la convocation</b> de la Brigade criminelle ?"),
      ("AU BÂTONNIER", "Où est <b>la décision</b> sur la plainte du 2 avril 2023 ?"),
      ("AU PROCUREUR GÉNÉRAL", "Pourquoi ne pas <b>saisir la Cour d'appel</b> ?")]
for i, (who, q) in enumerate(QS):
    text(f"<span class='colhead'>{who}</span><br><span class='bigq'>{q}</span>", 160, 150 + i * 200, 1600, W9[i][0] - 0.2, b, 'quest')

# --- 10 : conclusion
a, b = Q(10); W10 = [W(10, i) for i in range(3)]
text("Une seule pièce suffit.", 80, 260, 1760, W10[0][0] - 0.2, b, 'title2')
text("<span class='ocre'>Si l'acte existe, qu'il le montre.</span>", 80, 440, 1760, W10[1][0] - 0.2, b, 'title2')
text("Tant qu'il ne le montre pas, le constat du jugement repose<br>sur un acte que personne n'a vu.", 80, 640, 1760, W10[2][0] - 0.2, b, 'quote ocretext')
text("Gilles Sixte Féliho — plaignant", 80, 840, 1760, W10[2][0] + 2.0, b, 'ctext')

# --- carton final
a, b = SQ[16]
text('wadagni2026-verite.com', 0, 300, 1920, a + 0.6, b, 'url', 0.8)
text('Les pièces reproduites dans ce film sont publiées sur le site, avec leurs empreintes numériques.', 0, 400, 1920, a + 1.6, b, 'finsmall', 0.8)
text("Les extraits reproduits sont des copies partielles ; les coordonnées personnelles sont occultées. Les articles sont ceux qui figurent dans les pièces, dans la loi d'avril 1965 sur le barreau et dans le règlement intérieur harmonisé des barreaux de l'UEMOA (5 mai 2023, postérieur aux faits de 2007 à 2015). "
     "Le règlement intérieur du Barreau du Bénin n'est pas publié ici. Le dossier, l'acte de disposition et les points d'interrogation sont des illustrations.", 160, 560, 1600, a + 2.6, b, 'precis', 0.8)

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
.mail{background:#fff;color:#111;border:4px solid var(--gold);border-radius:6px;padding:20px 26px;font-size:23px;line-height:1.4;box-shadow:0 14px 40px rgba(0,0,0,.6)}.mail .mh{font-weight:700;font-size:22px;display:flex;justify-content:space-between;border-bottom:1px solid #ccc;padding-bottom:8px;margin-bottom:10px}.mail .mh span{font-weight:400;color:#666}.mail .ms{font-size:34px;font-weight:800;margin:10px 0 14px}.mail p{margin:0 0 12px}.mail .rep{background:#eef2ff;border-left:5px solid #4f46e5;padding:10px 14px;margin-top:10px}
.qa{font:800 130px DejaVu Serif,serif;color:#ef4444;letter-spacing:.04em}.bigq{font-family:'DejaVu Serif',serif;font-size:44px;line-height:1.3}
.bigtext{font-family:'DejaVu Serif',serif;font-size:42px;line-height:1.3;font-weight:700}
.quest{font-family:'DejaVu Serif',serif;font-size:40px;line-height:1.25}
.url{font-size:64px;text-align:center;font-family:'DejaVu Serif',serif;color:#fff}.finsmall{font-size:30px;text-align:center;color:var(--mute)}
.precis{font-size:24px;line-height:1.6;color:#cbd5e1}
.bandeau{left:0;bottom:0;width:1920px;height:88px;background:rgba(0,0,0,.7);color:#fff;font-size:26px;line-height:1.3;padding:12px 60px;z-index:50}
.trow{min-height:128px;align-items:start;display:grid;grid-template-columns:250px 1fr 230px;gap:18px;font-size:24px;line-height:1.3;background:rgba(255,255,255,.07);border-left:6px solid var(--gold);padding:12px 16px}.trow.thead{background:none;border:0;font-size:20px;letter-spacing:.08em;color:var(--gold);padding-top:0;padding-bottom:0}\n.title2{font-family:'DejaVu Serif',serif;font-size:56px;line-height:1.25;font-weight:700}\n.kf{position:absolute;left:0;top:0;transform-origin:0 0}\n.gap{text-align:center;font-size:20px;white-space:nowrap}\n.date3.ret{border:4px solid var(--gold);padding:14px;color:var(--gold)}\n.p6,.p4,.p5,.p7,.p3{}\nbody.fin #stage{background:#000}
'''
JS = '''
const ELS=[...document.querySelectorAll('.el')],CNS=[...document.querySelectorAll('.cn')],KFS=[...document.querySelectorAll('.kf')],PUL=[...document.querySelectorAll('.pulse')];
KFS.forEach(k=>{k._k=JSON.parse(k.dataset.k)});
const cl=x=>Math.max(0,Math.min(1,x));
window.TOTAL=%.2f;
window.seek=function(t){
  for(const e of ELS){const a=+e.dataset.a,b=+e.dataset.b,f=+e.dataset.f;const i=cl((t-a)/f);
    e.style.opacity=i*cl((b-t)/f);
    if(e.classList.contains('trait')){e.style.transform=`scaleX(${cl((t-a)/1.0)})`;}
    else if(e.classList.contains('card')||e.classList.contains('piece')) e.style.transform=`translateY(${(1-i)*14}px)`;}
  for(const k of KFS){const K=k._k;let i=0;while(i<K.length-1&&t>=K[i+1][0])i++;
    const A=K[i],B=K[Math.min(i+1,K.length-1)];const u=B[0]>A[0]?cl((t-A[0])/(B[0]-A[0])):0;
    const g=(r,j,d)=>{const x=r[j]===undefined?d:r[j];return x};
    const L=(j,d)=>g(A,j,d)+(g(B,j,d)-g(A,j,d))*u;
    const s=L(3,1);k.style.transform=`translate(${L(1,0)}px,${L(2,0)}px) scale(${s},${A[5]===undefined&&B[5]===undefined?s:L(5,s)})`;k.style.opacity=L(4,1);}
  for(const p of PUL){p.style.opacity=.35+.4*Math.abs(Math.sin(t*4.5));}
  for(const c of CNS){const a=+c.dataset.ca,b=+c.dataset.cb,to=+c.dataset.to;c.textContent=Math.round(to*cl((t-a)/(b-a)));}
  document.body.classList.toggle('fin',t>=%.2f);
};
seek(0);
''' % (TOTAL, SQ[16][0] - 0.3)
html = f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Où est l&#39;acte ?</title><style>{CSS}</style></head><body><div id="stage">\n' + '\n'.join(EL) + f'\n</div><script>{JS}</script></body></html>'
open(os.path.join(here, 'motion.html'), 'w', encoding='utf-8').write(html)
json.dump({'total': TOTAL, 'sequences': {str(k_): v for k_, v in SQ.items()}, 'cues': cues}, open(os.path.join(out, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
print('durée totale', round(TOTAL, 1), 's ; séquences', {k_: (round(a_, 1), round(b_, 1)) for k_, (a_, b_) in SQ.items()})

