# -*- coding: utf-8 -*-
"""Film « Décision rendue, décision non reçue » (script v2 du 14 octobre 2026).
Usage : python3 build.py <dossier_modèles_kokoro> <dossier_sortie>
  1. génère la voix (Kokoro ff_siwis) phrase par phrase et en déduit la chronologie ;
  2. écrit motion.html (rendu image par image par render.js) et timeline.json ;
  3. écrit la bande son (voix + fond 55 Hz, souffles, bruitages discrets) : sortie/audio.wav ;
  4. écrit les sous-titres film.fr.srt et film.fr.vtt.
Chaque date, chaque extrait renvoie à une pièce publiée sur le site (voir la page du film).
"""
import sys, os, re, json, math, hashlib
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

models, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
SR = 24000

# ---------------------------------------------------------------- texte : (sous-titre affiché, texte lu)
SEQ = [
 dict(n=1, speed=1.1, gap=0.4, lead=1.4, tail=0.9, sents=[
   ("Ce film n'expose pas de conclusions. Il aligne des dates, telles qu'elles figurent dans les pièces produites.",
    "Ce film n'expose pas de conclusions. Il aligne des dates, telles qu'elles figurent dans les pièces produites.")]),
 dict(n=2, speed=1.12, gap=0.35, lead=0.8, tail=0.8, sents=[
   ("Le 11 septembre 2023, le procureur spécial près la CRIET saisit la Brigade criminelle.",
    "Le onze septembre deux mille vingt-trois, le procureur spécial près la Criet saisit la Brigade criminelle."),
   ("Le 4 octobre, l'enquête est ouverte sur la plainte de Gilles Sixte Féliho, contre X.",
    "Le quatre octobre, l'enquête est ouverte sur la plainte de Gilles Sixte Féliho, contre X."),
   ("Deux officiers ministériels y sont nommés : le notaire Félix Balley et l'avocat Victorien Fade.",
    "Deux officiers ministériels y sont nommés : le notaire Félix Balley et l'avocat Victorien Fade."),
   ("Le 17 novembre 2023, l'enquêteur informe le mandataire du plaignant qu'il doit en informer le bâtonnier, par le biais du procureur général.",
    "Le dix-sept novembre deux mille vingt-trois, l'enquêteur informe le mandataire du plaignant qu'il doit en informer le bâtonnier, par le biais du procureur général.")]),
 dict(n=3, speed=1.12, gap=0.4, lead=0.8, tail=3.0, sents=[
   ("Le 3 avril 2024, le chef de la Brigade criminelle retire le dossier à son enquêteur et le met en instance, en l'annotant.",
    "Le trois avril deux mille vingt-quatre, le chef de la Brigade criminelle retire le dossier à son enquêteur et le met en instance, en l'annotant."),
   ("Il décède le 27 octobre 2024.", "Il décède le vingt-sept octobre deux mille vingt-quatre."),
   ("Le dossier n'est retrouvé qu'en mars 2025, après la notification de la Cour constitutionnelle du 6 mars.",
    "Le dossier n'est retrouvé qu'en mars deux mille vingt-cinq, après la notification de la Cour constitutionnelle du six mars.")]),
 dict(n=4, speed=1.12, gap=0.3, lead=0.7, tail=2.2, sents=[
   ("Le 11 mars 2025, la réquisition au service domanial.", "Le onze mars deux mille vingt-cinq, la réquisition au service domanial."),
   ("Le 12, les convocations et l'ordre de mission.", "Le douze, les convocations et l'ordre de mission."),
   ("Le 14, le procureur général transmet au bâtonnier la convocation de l'avocat.", "Le quatorze, le procureur général transmet au bâtonnier la convocation de l'avocat."),
   ("Le 17, le cabinet du bâtonnier répond.", "Le dix-sept, le cabinet du bâtonnier répond."),
   ("Le 19, l'audition : l'avocat ne comparaît pas ; le notaire est entendu.", "Le dix-neuf, l'audition : l'avocat ne comparaît pas ; le notaire est entendu."),
   ("Le 27, la correspondance du bâtonnier est transmise à la Brigade criminelle.", "Le vingt-sept, la correspondance du bâtonnier est transmise à la Brigade criminelle.")]),
 dict(n=5, speed=1.05, gap=0.6, lead=1.3, tail=2.2, sents=[
   ("Le 3 juillet 2025, à Cotonou, le procureur spécial près la CRIET classe la procédure sans suite.",
    "Le trois juillet deux mille vingt-cinq, à Cotonou, le procureur spécial près la Criet classe la procédure sans suite."),
   ("Motif : il n'a pas estimé opportun d'engager des poursuites.", "Motif : il n'a pas estimé opportun d'engager des poursuites."),
   ("La décision est adressée à Gilles Sixte Féliho.", "La décision est adressée à Gilles Sixte Féliho.")]),
 dict(n=6, speed=0.98, gap=0.9, lead=0.9, tail=4.0, sents=[
   ("Le plaignant reçoit cette décision le 26 septembre 2025.", "Le plaignant reçoit cette décision le vingt-six septembre deux mille vingt-cinq."),
   ("Quatre-vingt-cinq jours après qu'elle a été rendue.", "Quatre-vingt-cinq jours après qu'elle a été rendue."),
   ("La veille, son mandataire l'avait appris en se renseignant à la Brigade criminelle.", "La veille, son mandataire l'avait appris en se renseignant à la Brigade criminelle."),
   ("Douze jours après le classement, le 15 juillet 2025, une audience s'était tenue devant la Cour constitutionnelle.",
    "Douze jours après le classement, le quinze juillet deux mille vingt-cinq, une audience s'était tenue devant la Cour constitutionnelle.")]),
 dict(n=7, speed=1.1, gap=0.5, lead=0.9, tail=1.6, sents=[
   ("Les dates sont établies. Leurs causes ne le sont pas.", "Les dates sont établies. Leurs causes ne le sont pas."),
   ("Cinq questions seront adressées par écrit aux autorités compétentes. Leurs réponses seront publiées.",
    "Cinq questions seront adressées par écrit aux autorités compétentes. Leurs réponses seront publiées.")]),
]

k = Kokoro(os.path.join(models, 'kokoro.onnx'), os.path.join(models, 'voices.bin'))
t = 0.0
cues = []            # (début, fin, sous-titre)
voice_clips = []     # (début, tableau)
T = {}               # (séquence, phrase) -> (début, fin) ; séquence -> (début, fin)
SEQT = {}
for sq in SEQ:
    s0 = t
    c = s0 + sq['lead']
    for i, (sub, voice) in enumerate(sq['sents']):
        ck = os.path.join(out, 'cache', hashlib.md5(f"{voice}|{sq['speed']}".encode()).hexdigest() + '.npy')
        if os.path.exists(ck): x, sr = np.load(ck), SR
        else:
            x, sr = k.create(voice, voice='ff_siwis', speed=sq['speed'], lang='fr-fr'); os.makedirs(os.path.dirname(ck), exist_ok=True); np.save(ck, x)
        assert sr == SR
        d = len(x) / SR
        T[(sq['n'], i)] = (c, c + d)
        voice_clips.append((c, x.astype(np.float32)))
        cues.append((c, c + d, sub))
        c += d + sq['gap']
    end = c - sq['gap'] + sq['tail']
    SEQT[sq['n']] = (s0, end)
    t = end
FINAL = 6.0      # carton final et précisions
TOTAL = t + FINAL
SEQT[8] = (t, TOTAL)

def ts(a, f='srt'):
    h = int(a // 3600); m = int(a % 3600 // 60); s = a % 60
    sep = ',' if f == 'srt' else '.'
    return f"{h:02d}:{m:02d}:{int(s):02d}{sep}{int(round((s - int(s)) * 1000)):03d}"
open(os.path.join(out, 'film.fr.srt'), 'w', encoding='utf-8').write(
    '\n'.join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{s}\n" for i, (a, b, s) in enumerate(cues)))
open(os.path.join(out, 'film.fr.vtt'), 'w', encoding='utf-8').write(
    'WEBVTT\n\n' + '\n'.join(f"{i+1}\n{ts(a,'vtt')} --> {ts(b,'vtt')}\n{s}\n" for i, (a, b, s) in enumerate(cues)))

# ---------------------------------------------------------------- bande son
n = int((TOTAL + 1) * SR)
voice = np.zeros(n, dtype=np.float32)
for a, x in voice_clips:
    i = int(a * SR); voice[i:i + len(x)] += x
voice *= 0.9 / max(1e-6, np.abs(voice).max())
tt = np.arange(n) / SR
# fond : une note tenue à 55 Hz (−26 dB), de 0:00 à la fin de la séquence 5 ; elle s'éteint pendant la séquence 3, reprend en séquence 4
drone = (10 ** (-26 / 20)) * np.sin(2 * np.pi * 55 * tt).astype(np.float32)
env = np.ones(n, dtype=np.float32)
s3a, s3b = SEQT[3]; s4a, s4b = SEQT[4]; s5a, s5b = SEQT[5]
def ramp(a, b, v0, v1):
    i0, i1 = int(a * SR), int(b * SR); env[i0:i1] = np.linspace(v0, v1, i1 - i0)
ramp(s3a + 3, T[(3, 2)][0] + 2, 1.0, 0.12)          # le fond s'éteint progressivement
env[int((T[(3, 2)][0] + 2) * SR):int(s4a * SR)] = 0.12
ramp(s4a, s4a + 2.0, 0.12, 1.0)                       # bourdonnement sourd en séquence 4
env[int(s5a * SR):] = 0.0                              # arrêt net à la séquence 5 ; silence jusqu'à la fin
env[:int(2 * SR)] *= np.linspace(0, 1, int(2 * SR))
fond = drone * env
rng = np.random.default_rng(7)
def burst(at, dur, amp, lo=300, hi=3000):
    m = int(dur * SR); x = rng.standard_normal(m).astype(np.float32)
    spec = np.fft.rfft(x); f = np.fft.rfftfreq(m, 1 / SR); spec[(f < lo) | (f > hi)] = 0
    x = np.fft.irfft(spec, m).astype(np.float32); x /= max(1e-6, np.abs(x).max())
    x *= np.hanning(m).astype(np.float32) ** 0.5 * amp
    i = int(at * SR); sfx[i:i + m] += x[:max(0, min(m, n - i))]
sfx = np.zeros(n, dtype=np.float32)
for at in (SEQT[2][0] + 0.1, SEQT[4][0] + 0.1):       # souffles secs, −18 dB
    burst(at, 0.45, 10 ** (-18 / 20), 400, 2500)
burst(s5a + 0.05, 0.4, 10 ** (-16 / 20), 500, 3000)   # « un seul souffle sec »
for key in ((2, 0), (2, 1), (2, 3), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5)):   # papier / tampon, discrets
    burst(T[key][0], 0.12, 10 ** (-32 / 20), 1200, 5000)
mix = fond + sfx + voice
mix /= max(1.0, np.abs(mix).max() / 0.95)
sf.write(os.path.join(out, 'audio.wav'), mix, SR)


# ---------------------------------------------------------------- image : éléments positionnés dans le temps
import datetime as dt
EL = []
def el(html, a, b=None, fade=0.5, cls='', style=''):
    b = TOTAL if b is None else b
    EL.append(f'<div class="el {cls}" data-a="{a:.2f}" data-b="{b:.2f}" data-f="{fade}" style="{style}">{html}</div>')
def card(day, mon, yr, x, y, a, b=None, cls=''):
    el(f'<div class="dd">{day}</div><div class="mm">{mon}</div><div class="yy">{yr}</div>', a, b, 0.4, 'card ' + cls, f'left:{x}px;top:{y}px')
def pic(img, x, y, w, a, b=None, cap='', h=None, hl=(), cls=''):
    boxh = f'height:{h}px;' if h else ''
    marks = ''.join(f'<div class="hl" style="left:{l}%;top:{tp}%;width:{wd}%;height:{ht}%"></div>' for l, tp, wd, ht in hl)
    el(f'<div class="pic" style="width:{w}px;{boxh}"><img src="img/{img}">{marks}</div>' + (f'<div class="cap">{cap}</div>' if cap else ''),
       a, b, 0.5, 'piece ' + cls, f'left:{x}px;top:{y}px;width:{w}px')
def counter(num, unit, x, y, a, b, c0, c1, size=200, w=900):
    el(f'<span class="cn" data-ca="{c0:.2f}" data-cb="{c1:.2f}" data-to="{num}">0</span><span class="cu">{unit}</span>', a, b, 0.6, 'counter', f'left:{x}px;top:{y}px;width:{w}px;font-size:{size}px')
def X(m, d, y):   # frise : 1er janvier 2023 -> 31 décembre 2025, de x = 120 à x = 1800
    return 120 + (dt.date(y, m, d) - dt.date(2023, 1, 1)).days * (1680 / 1095)
FY = 210
def dot(m, d, y, a, b=None, cls=''):
    el('', a, b, 0.3, 'fdot ' + cls, f'left:{X(m,d,y)-9:.0f}px;top:{FY-9}px')
def frise(a, b, op=1.0):
    ticks = ''.join(f'<div class="ftick" style="left:{X(1,1,yr):.0f}px;top:{FY-16}px"></div><div class="fyear" style="left:{X(1,1,yr)+10:.0f}px;top:{FY+14}px">{yr}</div>' for yr in (2023, 2024, 2025))
    ticks += f'<div class="ftick" style="left:1800px;top:{FY-16}px"></div>'
    el(f'<div class="frl grow" data-ga="{a:.2f}" data-gb="{a+2.4:.2f}" style="left:120px;top:{FY}px;width:1680px"></div>{ticks}', a, b, 0.8, '', f'opacity:{op}')

SQ = {n: SEQT[n] for n in range(1, 9)}
s1, s2, s3, s4, s5, s6, s7, fin = (SQ[i] for i in range(1, 9))

# bandeau permanent
el('Aucune condamnation n\'est intervenue à ce jour. Les qualifications pénales relèvent des juridictions compétentes. Des contestations sont pendantes devant la Cour constitutionnelle du Bénin.',
   0, TOTAL, 0.6, 'bandeau')

# --- séquence 1 : le cadre
frise(s1[0] + 0.3, s5[0] + 0.15)
el('Décision rendue,<br>décision non reçue', s1[0] + 0.8, s1[1], 1.0, 'title', 'left:160px;top:380px')
el('La chronologie établie par les pièces', s1[0] + 2.6, s1[1], 1.0, 'subtitle', 'left:160px;top:660px')

# --- séquence 2 : 2023, la saisine
c = [T[(2, i)] for i in range(4)]
card(11, 'SEPT.', 2023, 120, 290, c[0][0] - 0.2, s2[1]); dot(9, 11, 2023, c[0][0] - 0.2, s2[1])
card(4, 'OCT.', 2023, 380, 290, c[1][0] - 0.2, s2[1]); dot(10, 4, 2023, c[1][0] - 0.2, s2[1])
card(17, 'NOV.', 2023, 640, 290, c[3][0] - 0.2, s2[1]); dot(11, 17, 2023, c[3][0] - 0.2, s2[1])
pic('p18-top.png', 960, 290, 860, c[0][0], c[1][0] + 0.1, 'Référence du soit-transmis du 11 septembre 2023 : n° 2239-2023/MJL/CRIET/PS/SA (citée dans la lettre de la Brigade criminelle du 11 mars 2025)', hl=((0, 80, 100, 10),), cls='p2')
pic('p3-oct.png', 960, 290, 860, c[1][0], c[3][0] + 0.1, 'Réponse n° 269/2025 de la Brigade criminelle, p. 2 : saisine du 4 octobre 2023', hl=((0, 6, 100, 50),), cls='p2')
pic('p3-nov.png', 960, 290, 860, c[3][0], s2[1], 'Réponse n° 269/2025, p. 2 : « il est tenu d\'informer le bâtonnier […] par le biais du Procureur Général »', hl=((0, 52, 100, 45),), cls='p2')

# --- séquence 3 : la mise en instance
d = [T[(3, i)] for i in range(3)]
card(3, 'AVR.', 2024, 120, 290, d[0][0] - 0.2, s3[1]); dot(4, 3, 2024, d[0][0] - 0.2, s3[1])
card(27, 'OCT.', 2024, 380, 290, d[1][0] - 0.2, s3[1]); dot(10, 27, 2024, d[1][0] - 0.2, s3[1])
card(6, 'MARS', 2025, 640, 290, d[2][0] - 0.2, s3[1]); dot(3, 6, 2025, d[2][0] - 0.2, s3[1])
pic('p4-instance.png', 960, 290, 860, d[0][0], d[2][0] + 0.1, 'Réponse n° 269/2025, p. 3 : « en mettant le dossier en instance tel qu\'il a inscrit là-dessus » ; décès à Abidjan le 27 octobre 2024', hl=((0, 20, 100, 38),), cls='p3')
pic('p4-notif.png', 960, 290, 860, d[2][0], s3[1], 'Réponse n° 269/2025, p. 3 : « À la suite de la notification […] du 06 mars 2025, la fouille des documents […] a permis de retrouver le soit transmis »', hl=((0, 8, 70, 30),), cls='p3')
el(f'<div class="seg grow" data-ga="{d[2][0]:.2f}" data-gb="{s3[1]-1.0:.2f}" style="left:{X(4,3,2024):.0f}px;top:{FY-5}px;width:{X(3,6,2025)-X(4,3,2024):.0f}px"></div>', d[2][0] - 0.1, s3[1], 0.4)
counter(11, 'MOIS', 120, 560, d[2][0], s3[1], d[2][0] + 0.2, s3[1] - 0.8)

# --- séquence 4 : mars 2025
e = [T[(4, i)] for i in range(6)]
labels = [(11, 'MARS'), (12, 'MARS'), (14, 'MARS'), (17, 'MARS'), (19, 'MARS'), (27, 'MARS')]
for i, (dd, mm) in enumerate(labels):
    card(dd, mm, 2025, 120 + i * 285, 270, e[i][0] - 0.2, e[5][1] + 0.3, 'sm')
    dot(3, dd, 2025, e[i][0] - 0.2, e[5][1] + 0.3)
B4 = e[5][1] + 0.3
pic('p19-conv.png', 710, 440, 500, e[1][0], B4, 'Convocation de Me Fade pour le 19 mars 2025, 9 h (datée du 12 mars)', h=440, cls='p4', hl=((0, 60, 100, 18),))
pic('p25-lettre.png', 160, 440, 500, e[3][0], B4, 'Lettre du Bâtonnier du 17 mars 2025 (cachet d\'arrivée au Parquet Général : 19/03/25)', h=440, cls='p4', hl=((0, 80, 100, 10),))
pic('p24-pg.png', 1260, 440, 500, e[5][0], B4, 'Correspondance du Procureur Général du 27 mars 2025 (n° 0535-2025/MJL/CAC/PG-CA-COT/SA)', h=440, cls='p4')
counter(8, 'JOURS', 360, 400, B4, s4[1], B4 + 0.1, B4 + 2.2)
el('du cachet d\'arrivée de la lettre au Parquet Général (19 mars)<br>à sa transmission à la Brigade criminelle (27 mars)', B4 + 0.8, s4[1], 0.6, 'ctext', 'left:360px;top:690px;width:1200px')

# --- séquence 5 : le classement
f = [T[(5, i)] for i in range(3)]
card(3, 'JUILLET', 2025, 150, 150, s5[0] + 0.25, s5[1], 'big')
pic('classement.png', 1090, 50, 625, f[0][0] + 0.2, s5[1], '', hl=((17, 50.4, 69, 6.4),), cls='p5')
el('<div class="conn"></div>', f[0][0] + 0.4, s5[1], 0.6, '', 'left:570px;top:330px;width:520px')
el('Le 3 juillet 2025,<br>la procédure est<br>classée sans suite.', f[0][0] + 0.3, s5[1], 0.8, 'bigtext', 'left:150px;top:640px;width:880px')

# --- séquence 6 : la non-communication
g = [T[(6, i)] for i in range(4)]
LX0, LX1 = 400, 1540     # extrémités du pointillé (85 jours)
def DX(day): return LX0 + (LX1 - LX0) * day / 85
card(3, 'JUILLET', 2025, 120, 300, s6[0] + 0.2, s6[1], 'sm2')
card(26, 'SEPT.', 2025, 1570, 300, g[0][0] - 0.2, s6[1], 'sm2')
el(f'<div class="dotl grow" data-ga="{g[1][0]:.2f}" data-gb="{g[1][1]+1.0:.2f}" style="left:{LX0}px;top:410px;width:{LX1-LX0}px"></div>', g[1][0] - 0.2, s6[1], 0.3)
el('<div class="fdot"></div>', s6[0] + 0.2, s6[1], 0.3, '', f'left:{LX0-9}px;top:401px')
el('<div class="fdot"></div>', g[0][0], s6[1], 0.3, '', f'left:{LX1-9}px;top:401px')
counter(85, 'JOURS', 330, 520, g[1][0] - 0.1, s6[1], g[1][0] + 0.3, g[1][1] + 1.0, w=1200)
card(15, 'JUILLET 2025', 'audience', int(DX(12)) - 150, 225, g[3][0] - 0.2, s6[1], 'aud')
el('', g[3][0] - 0.2, s6[1], 0.3, 'fdot', f'left:{DX(12)-9:.0f}px;top:401px')
el('<img src="img/recu.png">', g[0][0], s6[1], 0.6, 'recu', 'left:1280px;top:520px;width:520px')
el('mention portée par le plaignant sur sa copie', g[0][0] + 0.2, s6[1], 0.6, 'ctext small', 'left:1280px;top:630px;width:520px')
el('25 septembre 2025 : le mandataire du plaignant apprend le classement à la Brigade criminelle', g[2][0], s6[1], 0.6, 'ctext small', 'left:330px;top:800px;width:1250px')

# --- séquence 7 : les questions
frise(s7[0] - 0.01, s7[1], 0.12)
Q = ["Pourquoi le dossier a-t-il été mis en instance ?",
     "Pourquoi sa redécouverte a-t-elle suivi une convocation de la Cour constitutionnelle, et non une diligence interne ?",
     "Pourquoi la décision du 3 juillet 2025 n'a-t-elle été reçue que le 26 septembre 2025 ?",
     "À quelle date cette décision a-t-elle été transmise à la Cour constitutionnelle ?",
     "Sur quels éléments le procureur spécial a-t-il estimé ne pas devoir engager de poursuites ?"]
for i, q in enumerate(Q):
    el(q, s7[0] + 0.8 + i * 2.1, s7[1] - 0.6, 0.8, 'quest', f'left:160px;top:{300 + i * 140}px;width:1560px')

# --- carton final
el('wadagni2026-verite.com', fin[0] + 0.6, TOTAL, 0.8, 'url', 'left:0;top:300px;width:1920px')
el('Le dossier complet, les pièces et leurs empreintes numériques sont publiés.', fin[0] + 1.6, TOTAL, 0.8, 'finsmall', 'left:0;top:400px;width:1920px')
el('La lettre du 17 mars 2025 porte la mention « … A. HOUNKPATIN » sous la signature « Le Bâtonnier » ; elle est publiée intégralement sur le site.<br>'
   'La mention « Reçu le 26 septembre 2025 » est portée par le plaignant sur sa copie de l\'avis de classement.<br>'
   'Les extraits reproduits sont des copies partielles ; les pièces intégrales sont publiées sur le site.', fin[0] + 2.6, TOTAL, 0.8, 'precis', 'left:160px;top:560px;width:1600px')

CSS = '''
:root{--navy:#0a1f44;--gold:#d4af37;--ink:#f8fafc;--mute:#94a3b8}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:#050d1f;font-family:'DejaVu Sans',sans-serif;color:var(--ink)}
#stage{position:relative;width:1920px;height:1080px;background:radial-gradient(ellipse at 30% 20%,#12306b 0%,#0a1f44 45%,#050d1f 100%)}
.el{position:absolute;opacity:0}
.title{font-family:'DejaVu Serif',serif;font-size:104px;line-height:1.15;font-weight:700}
.subtitle{font-family:'DejaVu Serif',serif;font-size:48px;color:var(--gold);font-style:italic}
.frl{position:absolute;height:4px;background:#c7d2fe;transform-origin:left}
.ftick{position:absolute;width:3px;height:32px;background:#c7d2fe}
.fyear{position:absolute;font-size:30px;color:var(--mute)}
.fdot{width:18px;height:18px;border-radius:50%;background:var(--gold);box-shadow:0 0 14px rgba(212,175,55,.7)}
.card{width:230px;text-align:center;background:rgba(255,255,255,.07);border:3px solid var(--gold);border-radius:16px;padding:14px 8px}
.card .dd{font-size:92px;font-weight:800;line-height:1.0}
.card .mm{font-size:36px;letter-spacing:.08em;color:var(--gold);margin-top:6px}
.card .yy{font-size:34px;color:var(--mute);margin-top:4px}
.card.sm{width:250px;padding:8px}
.card.sm .dd{font-size:62px}.card.sm .mm{font-size:28px;margin-top:0}.card.sm .yy{font-size:26px}
.card.sm2{width:230px}
.card.aud{width:300px;padding:8px 6px}.card.aud .dd{font-size:56px}.card.aud .mm{font-size:26px}.card.aud .yy{font-size:30px;color:#fff;text-transform:uppercase;letter-spacing:.06em}
.card.big{width:420px;padding:30px 10px}.card.big .dd{font-size:190px}.card.big .mm{font-size:64px}.card.big .yy{font-size:60px}
.pic{position:relative;background:#fff;border:4px solid var(--gold);border-radius:6px;overflow:hidden;box-shadow:0 14px 40px rgba(0,0,0,.6)}
.pic img{display:block;width:100%}
.hl{position:absolute;background:rgba(212,175,55,.35);border:2px solid rgba(212,175,55,.9)}
.cap{font-size:22px;line-height:1.3;color:var(--mute);margin-top:10px}
.counter{font-family:'DejaVu Sans',sans-serif;font-weight:800;color:var(--gold);text-align:center;white-space:nowrap}
.counter .cu{font-size:60px;margin-left:24px;color:#fff;font-weight:600;letter-spacing:.06em}
.ctext{font-size:30px;line-height:1.4;color:#e2e8f0;text-align:center}.ctext.small{font-size:24px;color:var(--mute)}
.seg{position:absolute;height:12px;background:var(--gold);transform-origin:left;border-radius:6px}
.dotl{position:absolute;height:0;border-top:5px dotted #c7d2fe;transform-origin:left}
.bigtext{font-family:'DejaVu Serif',serif;font-size:54px;line-height:1.25;font-weight:700}
.conn{height:3px;background:var(--gold)}
.recu img{display:block;width:100%;background:#fff;border:3px solid #ef4444;border-radius:6px}
.quest{font-family:'DejaVu Serif',serif;font-size:46px;line-height:1.25}
.url{font-size:64px;text-align:center;font-family:'DejaVu Serif',serif;color:#fff}
.finsmall{font-size:30px;text-align:center;color:var(--mute)}
.precis{font-size:27px;line-height:1.6;color:#cbd5e1}
.bandeau{left:0;bottom:0;width:1920px;height:88px;background:rgba(0,0,0,.7);color:#fff;font-size:26px;line-height:1.3;padding:12px 60px;z-index:50}
body.fin #stage{background:#000}
'''
JS = '''
const ELS=[...document.querySelectorAll('.el')],CNS=[...document.querySelectorAll('.cn')],GR=[...document.querySelectorAll('.grow')];
const cl=x=>Math.max(0,Math.min(1,x));
window.TOTAL=%.2f;
window.seek=function(t){
  for(const e of ELS){const a=+e.dataset.a,b=+e.dataset.b,f=+e.dataset.f;const i=cl((t-a)/f);
    e.style.opacity=i*cl((b-t)/f);
    if(e.classList.contains('card')||e.classList.contains('piece')) e.style.transform=`translateY(${(1-i)*16}px)`;}
  for(const c of CNS){const a=+c.dataset.ca,b=+c.dataset.cb,to=+c.dataset.to;c.textContent=Math.round(to*cl((t-a)/(b-a)));}
  for(const g of GR){const a=+g.dataset.ga,b=+g.dataset.gb;g.style.transform=`scaleX(${cl((t-a)/(b-a))})`;}
  document.body.classList.toggle('fin',t>=%.2f);
};
seek(0);
''' % (TOTAL, SQ[8][0] - 0.3)
html = f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Décision rendue, décision non reçue</title><style>{CSS}</style></head><body><div id="stage">\n' + '\n'.join(EL) + f'\n</div><script>{JS}</script></body></html>'
open(os.path.join(here, 'motion.html'), 'w', encoding='utf-8').write(html)
json.dump({'total': TOTAL, 'sequences': {str(k): v for k, v in SEQT.items()}, 'cues': cues}, open(os.path.join(out, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
print('durée totale', round(TOTAL, 1), 's ; séquences', {k: (round(a, 1), round(b, 1)) for k, (a, b) in SEQT.items()})
