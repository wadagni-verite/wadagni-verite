# -*- coding: utf-8 -*-
"""Film « Sept séances, aucune décision » : la plainte du 3 octobre 2023 à l'Autorité de Protection des Données Personnelles (APDP, Bénin) contre le notaire Félix Balley.
Usage : python3 build.py <dossier_modèles_kokoro> <dossier_sortie>   (voix Kokoro ff_siwis ; cache des phrases dans <sortie>/cache)
Écrit : motion.html (rendu par render.js), <sortie>/audio.wav, film.fr.srt, film.fr.vtt, timeline.json.
Chaque image provient d'une pièce publiée sur le site (pieces/procedures-benin/apdp-*.pdf) ; les recadrages sont dans img/.
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
 1: Z(1.14, 1.6, 1.4,
      ("Le 3 octobre 2023, une plainte parvient à l'Autorité de Protection des Données Personnelles, à Cotonou.", "Le trois octobre deux mille vingt-trois, une plainte parvient à l'Autorité de Protection des Données Personnelles, à Cotonou."),
      ("Elle vise un notaire, Maître Félix Balley.", "Elle vise un notaire, Maître Félix Balley."),
      ("L'Autorité est présidée par Luciano Hounkponou.", "L'Autorité est présidée par Luciano Hounkponou."),
      ("Trois ans plus tard, aucune décision n'a été notifiée au plaignant.", "Trois ans plus tard, aucune décision n'a été notifiée au plaignant.")),
 2: Z(1.14, 0.9, 1.6,
      ("Le plaignant, Gilles Féliho, découvre un certificat d'acquit de droit daté du 20 octobre 2016.", "Le plaignant, Gilles Féliho, découvre un certificat d'acquit de droit daté du vingt octobre deux mille seize."),
      ("Le notaire y agit « en qualité de mandataire et au nom des héritiers », dont lui.", "Le notaire y agit « en qualité de mandataire et au nom des héritiers », dont lui."),
      ("Il ne connaît pas ce notaire. Il ne lui a jamais donné de mandat.", "Il ne connaît pas ce notaire. Il ne lui a jamais donné de mandat."),
      ("Un huissier signifie un procès-verbal de compulsion le 4 août 2023. Le notaire refuse, le 7 septembre, de lui communiquer les traitements opérés sur ses données.", "Un huissier signifie un procès-verbal de compulsion le quatre août deux mille vingt-trois. Le notaire refuse, le sept septembre, de lui communiquer les traitements opérés sur ses données.")),
 3: Z(1.14, 0.9, 1.6,
      ("La plainte invoque le droit d'accès, article 437 du Code du numérique.", "La plainte invoque le droit d'accès, article quatre cent trente-sept du Code du numérique."),
      ("Elle demande une mise en demeure sous huit jours, des sanctions, la suppression des données sur le certificat, et leur publication.", "Elle demande une mise en demeure sous huit jours, des sanctions, la suppression des données sur le certificat, et leur publication."),
      ("Et l'information du Procureur de la République, article 483, point 9.", "Et l'information du Procureur de la République, article quatre cent quatre-vingt-trois, point neuf."),
      ("Le plaignant cite lui-même l'article 448 : être tenu informé du suivi.", "Le plaignant cite lui-même l'article quatre cent quarante-huit : être tenu informé du suivi.")),
 4: Z(1.12, 0.9, 1.8,
      ("Que dit la loi ? Article 448 : l'Autorité informe l'auteur de la réclamation de l'état d'avancement et de l'issue de sa réclamation.", "Que dit la loi ? Article quatre cent quarante-huit : l'Autorité informe l'auteur de la réclamation de l'état d'avancement et de l'issue de sa réclamation."),
      ("Article 449 : quatre-vingt-dix jours.", "Article quatre cent quarante-neuf : quatre-vingt-dix jours."),
      ("Quatre-vingt-dix jours après le 3 octobre 2023 : le 1er janvier 2024.", "Quatre-vingt-dix jours après le trois octobre deux mille vingt-trois : le premier janvier deux mille vingt-quatre.")),
 5: Z(1.14, 0.9, 1.6,
      ("Le 14 décembre 2023, soixante-douze jours après la plainte, l'Autorité accuse réception.", "Le quatorze décembre deux mille vingt-trois, soixante-douze jours après la plainte, l'Autorité accuse réception."),
      ("« Une suite vous sera donnée incessamment. »", "« Une suite vous sera donnée incessamment. »"),
      ("Le même jour, elle met le notaire en demeure de produire, sous huit jours, les autorisations et consentements.", "Le même jour, elle met le notaire en demeure de produire, sous huit jours, les autorisations et consentements."),
      ("Il répond le 27 décembre, en invoquant les devoirs de son office.", "Il répond le vingt-sept décembre, en invoquant les devoirs de son office.")),
 6: Z(1.14, 0.9, 1.6,
      ("Le 21 mai 2024, l'Autorité invite le plaignant à une séance le 28 mai, à 18 heures.", "Le vingt et un mai deux mille vingt-quatre, l'Autorité invite le plaignant à une séance le vingt-huit mai, à dix-huit heures."),
      ("Le 24 mai, il pose trois questions : comment assister à distance, s'il doit produire un mémoire, et si les échanges sont contradictoires, car il a cru comprendre que le notaire a fourni des pièces dont il n'a pas connaissance.", "Le vingt-quatre mai, il pose trois questions : comment assister à distance, s'il doit produire un mémoire, et si les échanges sont contradictoires, car il a cru comprendre que le notaire a fourni des pièces dont il n'a pas connaissance."),
      ("Le 19 juin 2024, deux cent soixante jours après la plainte : séance contentieuse.", "Le dix-neuf juin deux mille vingt-quatre, deux cent soixante jours après la plainte : séance contentieuse."),
      ("La séance est présidée par Claude Dieu Donné Montcho, en présence du président Luciano Hounkponou et du rapporteur Amouda Abou Seydou.", "La séance est présidée par Claude Dieu Donné Montcho, en présence du président Luciano Hounkponou et du rapporteur Amouda Abou Seydou."),
      ("Le notaire est assisté de son avocat. Le plaignant est absent.", "Le notaire est assisté de son avocat. Le plaignant est absent."),
      ("Son avocat s'excuse, au nom de son client, de l'ignorance de l'obligation légale de mise en conformité.", "Son avocat s'excuse, au nom de son client, de l'ignorance de l'obligation légale de mise en conformité."),
      ("Délibéré au 24 juillet, pour audition du plaignant.", "Délibéré au vingt-quatre juillet, pour audition du plaignant.")),
 7: Z(1.14, 0.9, 1.6,
      ("Le 23 juillet, le rapporteur écrit au plaignant : pour obtenir le rapport d'instruction notifié au défendeur, il doit formuler sa demande en séance plénière.", "Le vingt-trois juillet, le rapporteur écrit au plaignant : pour obtenir le rapport d'instruction notifié au défendeur, il doit formuler sa demande en séance plénière."),
      ("Le 24 juillet, le plaignant écrit : « J'attends le lien de participation annoncé ». L'Autorité envoie le lien. Réponse : « Je n'ai pas accès ».", "Le vingt-quatre juillet, le plaignant écrit : « J'attends le lien de participation annoncé ». L'Autorité envoie le lien. Réponse : « Je n'ai pas accès »."),
      ("Le procès-verbal le mentionne ensuite « participant en ligne ».", "Le procès-verbal le mentionne ensuite « participant en ligne »."),
      ("Le 28 août, le procès-verbal consigne que la plénière ne peut faire suite à sa demande de mise à disposition du rapport d'instruction adressé au notaire.", "Le vingt-huit août, le procès-verbal consigne que la plénière ne peut faire suite à sa demande de mise à disposition du rapport d'instruction adressé au notaire.")),
 8: Z(1.14, 0.9, 1.6,
      ("Le 25 septembre : nouvelle séance. Le délibéré est rabattu pour envoyer les procès-verbaux au plaignant, « afin de garantir le principe du contradictoire ».", "Le vingt-cinq septembre : nouvelle séance. Le délibéré est rabattu pour envoyer les procès-verbaux au plaignant, « afin de garantir le principe du contradictoire »."),
      ("Le dossier est renvoyé au 23 octobre.", "Le dossier est renvoyé au vingt-trois octobre."),
      ("La lettre d'invitation du 10 octobre, signée du rapporteur, vise l'article 457.", "La lettre d'invitation du dix octobre, signée du rapporteur, vise l'article quatre cent cinquante-sept.")),
 8.5: Z(1.14, 0.9, 2.2,
      ("Le contradictoire est garanti : article 454 pour les sanctions, article 457 pour le rapport d'instruction.", "Le contradictoire est garanti : article quatre cent cinquante-quatre pour les sanctions, article quatre cent cinquante-sept pour le rapport d'instruction."),
      ("Pourtant, le 24 mai, le plaignant doit demander si les échanges sont contradictoires.", "Pourtant, le vingt-quatre mai, le plaignant doit demander si les échanges sont contradictoires."),
      ("Le 23 juillet, on lui répond de formuler sa demande de rapport en séance. Le 24 juillet : « Je n'ai pas accès ».", "Le vingt-trois juillet, on lui répond de formuler sa demande de rapport en séance. Le vingt-quatre juillet : « Je n'ai pas accès »."),
      ("Le 28 août, la plénière ne peut faire suite à sa demande. Le rapport, lui, a été notifié au notaire.", "Le vingt-huit août, la plénière ne peut faire suite à sa demande. Le rapport, lui, a été notifié au notaire."),
      ("Le 25 septembre, le délibéré est rabattu « afin de garantir le principe du contradictoire ».", "Le vingt-cinq septembre, le délibéré est rabattu « afin de garantir le principe du contradictoire »."),
      ("124 jours après sa première question. 98 jours après la séance du 19 juin, il accuse réception des procès-verbaux.", "Cent vingt-quatre jours après sa première question. Quatre-vingt-dix-huit jours après la séance du dix-neuf juin, il accuse réception des procès-verbaux."),
      ("Le plaignant a dû batailler pour obtenir ce que la loi garantit.", "Le plaignant a dû batailler pour obtenir ce que la loi garantit.")),
 10.5: Z(1.14, 0.9, 2.2,
      ("L'Autorité est chargée de protéger : l'article 483 lui demande de s'assurer qu'aucune menace ne pèse sur les libertés publiques et la vie privée.", "L'Autorité est chargée de protéger : l'article quatre cent quatre-vingt-trois lui demande de s'assurer qu'aucune menace ne pèse sur les libertés publiques et la vie privée."),
      ("Vendredi 13 décembre 2024, 10 heures 18 : le plaignant l'informe, par courtoisie, de son communiqué.", "Vendredi treize décembre deux mille vingt-quatre, dix heures dix-huit : le plaignant l'informe, par courtoisie, de son communiqué."),
      ("Lundi 16 décembre, 7 heures 58 : « Vous répondrez de vos actes en temps opportun. »", "Lundi seize décembre, sept heures cinquante-huit : « Vous répondrez de vos actes en temps opportun. »"),
      ("Deux jours, vingt et une heures, quarante minutes pour brandir la menace.", "Deux jours, vingt et une heures, quarante minutes pour brandir la menace."),
      ("440 jours sans décision contre le notaire. Aucune mention de l'information du Procureur, que la loi demande sans délai.", "Quatre cent quarante jours sans décision contre le notaire. Aucune mention de l'information du Procureur, que la loi demande sans délai."),
      ("Une institution chargée de protéger, qui menace.", "Une institution chargée de protéger, qui menace.")),
 9: Z(1.14, 0.9, 1.6,
      ("Le 21 octobre, le plaignant dépose ses observations.", "Le vingt et un octobre, le plaignant dépose ses observations."),
      ("Il relève trois versions du notaire : un mandat, le 20 octobre 2016 ; « pas partie aux actes », le 7 septembre 2023 ; une décision de justice exécutoire, le 19 juin 2024.", "Il relève trois versions du notaire : un mandat, le vingt octobre deux mille seize ; « pas partie aux actes », le sept septembre deux mille vingt-trois ; une décision de justice exécutoire, le dix-neuf juin deux mille vingt-quatre."),
      ("Il demande des sanctions, la suppression de ses données sous astreinte de cinquante mille francs CFA par jour, la publication, et l'information du Procureur.", "Il demande des sanctions, la suppression de ses données sous astreinte de cinquante mille francs CFA par jour, la publication, et l'information du Procureur.")),
 10: Z(1.14, 0.9, 1.8,
      ("Séance du 23 octobre. Séance du 27 novembre : le dossier est renvoyé au 19 décembre.", "Séance du vingt-trois octobre. Séance du vingt-sept novembre : le dossier est renvoyé au dix-neuf décembre."),
      ("Le 13 décembre, par courtoisie, le plaignant informe l'Autorité du communiqué de presse qu'il entend publier.", "Le treize décembre, par courtoisie, le plaignant informe l'Autorité du communiqué de presse qu'il entend publier."),
      ("Le 16 décembre, l'Autorité répond : dossier « mis en délibéré pour le 19 décembre prochain ». « Vous répondrez de vos actes en temps opportun. »", "Le seize décembre, l'Autorité répond : dossier « mis en délibéré pour le dix-neuf décembre prochain ». « Vous répondrez de vos actes en temps opportun. »"),
      ("Réponse du plaignant : « Mes deux boussoles sont : la loi et la vérité. »", "Réponse du plaignant : « Mes deux boussoles sont : la loi et la vérité. »")),
 11: Z(1.14, 0.9, 1.8,
      ("Sept séances : les 19 juin, 24 juillet, 28 août, 25 septembre, 23 octobre, 27 novembre et 19 décembre 2024.", "Sept séances : les dix-neuf juin, vingt-quatre juillet, vingt-huit août, vingt-cinq septembre, vingt-trois octobre, vingt-sept novembre et dix-neuf décembre deux mille vingt-quatre."),
      ("Le 19 décembre 2024, le dossier est mis en délibéré.", "Le dix-neuf décembre deux mille vingt-quatre, le dossier est mis en délibéré."),
      ("Depuis : rien.", "Depuis : rien.")),
 12: Z(1.14, 0.9, 1.6,
      ("443 jours entre la plainte et la dernière séance.", "Quatre cent quarante-trois jours entre la plainte et la dernière séance."),
      ("665 jours depuis cette séance.", "Six cent soixante-cinq jours depuis cette séance."),
      ("1 108 jours depuis la plainte.", "Mille cent huit jours depuis la plainte.")),
 13: Z(1.14, 0.9, 2.0,
      ("Depuis le 19 décembre 2024, le calendrier avance.", "Depuis le dix-neuf décembre deux mille vingt-quatre, le calendrier avance."),
      ("Aucune décision. Aucune notification.", "Aucune décision. Aucune notification."),
      ("Rien depuis décembre 2024.", "Rien depuis décembre deux mille vingt-quatre.")),
 14: Z(1.14, 0.9, 2.0,
      ("Une décision a-t-elle été prise à l'issue du délibéré du 19 décembre 2024 ?", "Une décision a-t-elle été prise à l'issue du délibéré du dix-neuf décembre deux mille vingt-quatre ?"),
      ("Le plaignant en sera-t-il informé, comme l'article 448 le prévoit ?", "Le plaignant en sera-t-il informé, comme l'article quatre cent quarante-huit le prévoit ?"),
      ("Le Procureur de la République a-t-il été informé, article 483, point 9 ?", "Le Procureur de la République a-t-il été informé, article quatre cent quatre-vingt-trois, point neuf ?"),
      ("La demande de suppression des données sur le certificat a-t-elle été examinée ?", "La demande de suppression des données sur le certificat a-t-elle été examinée ?"),
      ("Pourquoi deux jours pour menacer, et 440 jours sans décision ?", "Pourquoi deux jours pour menacer, et quatre cent quarante jours sans décision ?"), gap=0.5),
 15: Z(1.12, 0.9, 2.0,
      ("Une plainte, sept séances, un délibéré. Aucune décision connue du plaignant.", "Une plainte, sept séances, un délibéré. Aucune décision connue du plaignant."),
      ("Ce ne sont pas des opinions : ce sont des procès-verbaux et des lettres.", "Ce ne sont pas des opinions : ce sont des procès-verbaux et des lettres.")),
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


# ------------------------------------------------------------------ bande son : voix + note à 55 Hz + tic-tac / battements
n_ = int((TOTAL + 1) * SR)
voice = np.zeros(n_, dtype=np.float32)
for a, x in clips:
    i = int(a * SR); voice[i:i + len(x)] += x
voice *= 0.9 / max(1e-6, np.abs(voice).max())
tt = np.arange(n_) / SR
env = np.zeros(n_, dtype=np.float32)
def seg(a, b, v):
    env[int(a * SR):int(b * SR)] = v
seg(0, SEQT[11][1], 1.0)                      # note tenue jusqu'à la fin des sept séances
env[:int(2 * SR)] *= np.linspace(0, 1, int(2 * SR))
fond = (10 ** (-26 / 20)) * np.sin(2 * np.pi * 55 * tt).astype(np.float32) * env
rng = np.random.default_rng(11)
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
for sq in (4, 6, 8.5, 9, 10.5, 12):                      # souffles secs
    burst(SEQT[sq][0] + 0.1, 0.4, 10 ** (-18 / 20), 400, 2500)
thud(SEQT[1][0] + 1.0, 0.4, 120, 0.35)         # tampon : réception de la plainte
for i in range(7):                             # une séance, un coup
    thud(T[(11, 0)][0] + 0.2 + i * 1.15, 0.4, 100, 0.3)
for i in range(4):                             # les demandes du plaignant, une à une
    thud(T[(8.5, 1 + i)][0] + 0.1, 0.4, 100, 0.3)
thud(T[(10.5, 1)][0] + 0.2, 0.4, 110, 0.35); thud(T[(10.5, 2)][0] + 0.2, 0.5, 90, 0.5)   # vendredi, lundi
_tt = T[(10.5, 3)][0]
while _tt < T[(10.5, 3)][0] + 2.0:             # chronomètre
    tick(_tt, 0.3); _tt += 0.12
_tt = T[(4, 2)][0] + 0.2; _iv = 0.5            # le délai de quatre-vingt-dix jours qui s'écoule
while _tt < T[(4, 2)][1] + 1.0:
    tick(_tt); _tt += _iv; _iv *= 1.06
_tt = SEQT[13][0] + 1.0; _iv = 0.55            # tic-tac de plus en plus lent
while _tt < SEQT[13][1] - 0.5:
    tick(_tt); _tt += _iv; _iv *= 1.12
heart(T[(13, 2)][1] + 0.3)                     # un battement de cœur
heart(SEQT[15][1] - 2.2, 0.5)                  # un dernier battement
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

el("Ce film présente des pièces publiées sur le site : procès-verbaux, lettres et courriels de l'Autorité de Protection des Données Personnelles. Droit de réponse ouvert à l'Autorité et aux personnes citées.", 0, TOTAL, 0.6, 'bandeau')

# --- 1 : la plainte arrive
a, b = Q(1); W1 = [W(1, i) for i in range(4)]
text("PLAINTE À L'AUTORITÉ DE PROTECTION DES DONNÉES PERSONNELLES", 80, 62, 1760, a + 0.3, b, 'colhead wide')
pic('plainte-p1.png', 80, 140, 840, a + 0.4, b, "Plainte du 2 octobre 2023, p. 1 (coordonnées occultées)", h=780, cls='p1')
card(3, 'OCT.', 2023, 1000, 160, W1[0][0] - 0.2, b, 'big', 'reçue le 3 octobre 2023')
text("Autorité de Protection des Données Personnelles<br>Cotonou", 1450, 190, 400, W1[0][0] + 0.2, b, 'ctext')
text("Plainte contre le notaire <b>Félix A. Balley</b>", 1000, 640, 840, W1[1][0] - 0.2, b, 'quote')
text("Président de l'Autorité : <b>Luciano Hounkponou</b>", 1000, 740, 840, W1[2][0] - 0.2, b, 'quote')
text("Trois ans plus tard :<br><span class='ocre'>aucune décision notifiée au plaignant.</span>", 1000, 850, 840, W1[3][0] - 0.2, b, 'bigtext')

# --- 2 : ce que décrit la plainte
a, b = Q(2); W2 = [W(2, i) for i in range(4)]
heads(a + 0.2, b, 'LA PLAINTE · 2 OCTOBRE 2023', 'LES DATES')
pic('plainte-faits.png', 80, 140, 840, a + 0.4, b, "Plainte, p. 1 : le certificat, le mandat, la compulsion, le refus", find=("Maître Félix A. BALLEY, agit en qualité de mandataire", "Ne connaissant pas ce Maître Félix A. BALLEY et ne lui ayant en conséquence jamais donné de mandat", "a refusé de me communiquer les informations"), cls='p2')
text("<b>Jamais de mandat donné</b> à ce notaire", 80, 640, 840, W2[2][0] - 0.2, b, 'quote ocrebox')
for i, (tx, ta) in enumerate([("<b>20 octobre 2016</b> · certificat d'acquit de droit", W2[0][0]), ("<b>24 mai 2018</b> · le plaignant en prend connaissance", W2[0][0] + 3.2),
                              ("« agit en qualité de mandataire et au nom des héritiers » : le plaignant y figure", W2[1][0]), ("<b>4 août 2023</b> · procès-verbal de compulsion signifié", W2[3][0]),
                              ("<b>7 septembre 2023</b> · refus de communiquer", W2[3][0] + 4.8)]):
    text(tx, 1000, 150 + i * 135, 840, ta - 0.2, b, 'nm')

# --- 3 : les demandes
a, b = Q(3); W3 = [W(3, i) for i in range(4)]
heads(a + 0.2, b, 'CE QUE DEMANDE LA PLAINTE', 'LES ARTICLES INVOQUÉS')
pic('plainte-demandes.png', 80, 140, 840, a + 0.4, b, "Plainte, p. 2 : suppression, publication, information du Procureur, suivi (adresse électronique occultée)", find=("assortir vos sanctions d'une injonction à la suppression", "rendues publiques par publication", "informer sans délai Monsieur le Procureur de la République", "L'Autorité informe l'auteur de la réclamation de l'état d'avancement"), cls='p3')
for i, (tx, ta) in enumerate([("<b>Art. 437</b> · droit d'accès", W3[0][0]), ("<b>Mise en demeure sous 8 jours</b> · sanctions (art. 452, 454)", W3[1][0]),
                              ("<b>Art. 456</b> · suppression des données sur le certificat", W3[1][0] + 3.0), ("<b>Art. 459</b> · publication des sanctions", W3[1][0] + 5.6),
                              ("<b>Art. 483, point 9</b> · information du Procureur de la République", W3[2][0]), ("<b>Art. 448</b> · tenir le plaignant informé du suivi", W3[3][0])]):
    text(tx, 1000, 150 + i * 120, 840, ta - 0.2, b, 'nm')

# --- 4 : l'horloge de la loi
a, b = Q(4); W4 = [W(4, i) for i in range(3)]
heads(a + 0.2, b, 'CODE DU NUMÉRIQUE · LIVRE V', 'L\'HORLOGE')
pic('loi-448-449.png', 80, 140, 840, a + 0.4, b, "Code du numérique (loi n° 2017-20 modifiée), articles 448 et 449", find=("L'Autorité informe l'auteur de la réclamation de l'état d'avancement et de l'issue", "dans un délai de quatre vingt dix (90) jours"), cls='p4')
counter(90, 'JOURS', 1000, 150, W4[1][0] - 0.2, b, W4[1][0], W4[1][0] + 1.4, w=840, size=170, sub="article 449 : délai pour que l'Autorité informe l'auteur de la réclamation")
card(3, 'OCT.', 2023, 1000, 560, W4[2][0] - 0.2, b, '', 'plainte reçue')
text("+ 90 jours", 1260, 620, 300, W4[2][0] + 0.6, b, 'bigtext ocre')
card(1, 'JANV.', 2024, 1590, 560, W4[2][0] + 1.4, b, '', 'échéance')
tick_t = W4[2][0] + 1.4

# --- 5 : l'accusé de réception
a, b = Q(5); W5 = [W(5, i) for i in range(4)]
heads(a + 0.2, b, 'ACCUSÉ DE RÉCEPTION · 14 DÉCEMBRE 2023', 'CE QUI EST ÉCRIT')
pic('ar1.png', 80, 140, 840, a + 0.4, b, "APDP, lettre n° 2023-1793 du 14 décembre 2023 (coordonnées occultées)", h=730, cls='p5')
counter(72, 'JOURS', 1000, 140, W5[0][0] - 0.2, b, W5[0][0] + 0.4, W5[0][0] + 1.8, w=840, size=150, sub="du 3 octobre au 14 décembre 2023")
text("« <b>une suite vous sera donnée incessamment</b> »", 1000, 470, 840, W5[1][0] - 0.2, b, 'quote')
text("Le même jour : <b>mise en demeure du notaire</b>, huit jours, pour produire les autorisations et consentements", 1000, 620, 840, W5[2][0] - 0.2, b, 'quote')
text("<b>27 décembre</b> : réponse du notaire, « les devoirs que la loi met à sa charge en raison de son office »", 1000, 800, 840, W5[3][0] - 0.2, b, 'quote')

# --- 6 : mai, puis 19 juin 2024
a, b = Q(6); W6 = [W(6, i) for i in range(7)]
heads(a + 0.2, b, 'MAI · JUIN 2024', 'DU COURRIEL AU PROCÈS-VERBAL')
pic('mail-24-05.jpg', 80, 140, 840, a + 0.4, W6[2][0] - 0.3, "Courriel du plaignant à l'APDP, 24 mai 2024 (coordonnées occultées)", h=730, cls='p6')
pic('pv-06-19-p1.png', 80, 140, 840, W6[2][0] - 0.3, W6[5][0] - 0.3, "APDP, procès-verbal de séance du 19 juin 2024, p. 1", h=730, cls='p6')
pic('pv-06-19-p3.png', 80, 140, 840, W6[5][0] - 0.3, b, "APDP, procès-verbal de séance du 19 juin 2024, p. 3", h=730, cls='p6')
card(21, 'MAI', 2024, 1000, 160, W6[0][0] - 0.2, W6[1][0] - 0.3, 'big', 'invitation : séance du 28 mai, 18 h')
card(24, 'MAI', 2024, 1000, 160, W6[1][0] - 0.2, W6[2][0] - 0.3, 'big', 'trois questions')
for i, tx in enumerate(["Comment assister <b>à distance</b> ?", "Dois-je produire <b>un mémoire</b> ?", "Les échanges sont-ils <b>contradictoires</b> ?"]):
    text(tx, 1000, 560 + i * 110, 840, W6[1][0] + 1.5 + i * 3.0, W6[2][0] - 0.3, 'nm')
counter(260, 'JOURS', 1000, 140, W6[2][0] - 0.2, b, W6[2][0] + 0.4, W6[2][0] + 2.2, w=840, size=150, sub="du 3 octobre 2023 au 19 juin 2024 : de la plainte à la séance")
text("Présidence : <b>Claude Dieu Donné Montcho</b><br>Bureau : <b>Luciano Hounkponou</b>, président · <b>Amouda Abou Seydou</b>, rapporteur", 1000, 470, 840, W6[3][0] - 0.2, b, 'quote')
text("Le notaire : <b>assisté de son avocat</b><br>Le plaignant : <b>absent</b>", 1000, 650, 840, W6[4][0] - 0.2, W6[5][0] - 0.3, 'quote')
text("Son avocat « s'est excusé au nom de son client quant à l'ignorance de l'obligation légale de mise en conformité »", 1000, 640, 840, W6[5][0] - 0.2, b, 'quote ocrebox')
text("<b>Délibéré : 24 juillet 2024</b>", 1000, 830, 840, W6[6][0] - 0.2, b, 'bigtext')

# --- 7 : les courriels de juillet, le rapport d'instruction
a, b = Q(7); W7 = [W(7, i) for i in range(4)]
heads(a + 0.2, b, 'JUILLET · AOÛT 2024', 'LA DEMANDE DU RAPPORT D\'INSTRUCTION')
d1 = W7[1][1] - W7[1][0]; t1 = W7[1][0]
PH = [('mail-23-07.jpg', "Courriel de l'APDP, 23 juillet 2024", 23, 'JUIL.', "Le rapporteur : « formuler expressément votre demande en session plénière »", a + 0.4, W7[1][0] - 0.3),
      ('mail-24-07-attente.jpg', "Courriel du plaignant, 24 juillet 2024 (coordonnées occultées)", 24, 'JUIL.', "Le plaignant : « J'attends le lien de participation annoncé »", W7[1][0] - 0.3, t1 + d1 * 0.38),
      ('mail-24-07-lien.jpg', "Courriel de l'APDP, 24 juillet 2024 (coordonnées de l'agent occultées)", 24, 'JUIL.', "L'Autorité : le lien de la séance", t1 + d1 * 0.38, t1 + d1 * 0.62),
      ('mail-24-07-acces.jpg', "Réponse du plaignant, 24 juillet 2024 (coordonnées occultées)", 24, 'JUIL.', "Le plaignant : « Je n'ai pas accès »", t1 + d1 * 0.62, W7[2][0] - 0.3)]
for im, cap, dd, mm, lb, ta, tb in PH:
    pic(im, 80, 140, 840, ta, tb, cap, h=730, cls='p7')
    card(dd, mm, 2024, 1000, 160, ta + 0.2, tb, 'big')
    text(lb, 1450, 200, 400, ta + 0.6, tb, 'ctext')
pic('pv-07-24-p1.png', 80, 140, 840, W7[2][0] - 0.3, W7[3][0] - 0.3, "APDP, procès-verbal de séance du 24 juillet 2024, p. 1", h=730, cls='p7')
pic('pv-08-28-c.png', 80, 140, 840, W7[3][0] - 0.3, b, "APDP, procès-verbal de séance du 28 août 2024, p. 2", h=730, cls='p7')
for dd, mm, lb, ta, tb in [(24, 'JUIL.', "Procès-verbal : le plaignant est « Participant en ligne »", W7[2][0], W7[3][0] - 0.3), (28, 'AOÛT', "Procès-verbal : la Plénière « ne peut faire suite » à sa demande du rapport d'instruction adressé au notaire", W7[3][0], b)]:
    card(dd, mm, 2024, 1000, 160, ta - 0.2, tb, 'big')
    text(lb, 1450, 200, 400, ta + 0.2, tb, 'ctext')

# --- 8 : 25 septembre → 23 octobre
a, b = Q(8); W8 = [W(8, i) for i in range(3)]
heads(a + 0.2, b, 'LA LETTRE D\'INVITATION DU 10 OCTOBRE 2024', 'LE CONTRADICTOIRE')
pic('inv-oct.png', 80, 140, 840, a + 0.4, b, "APDP, lettre d'invitation du 10 octobre 2024 (coordonnées du plaignant occultées)", h=730, cls='p8')
card(25, 'SEPT.', 2024, 1000, 160, W8[0][0] - 0.2, b, '', 'séance')
arrow(W8[1][0] - 0.2, b, 1255, 210)
card(23, 'OCT.', 2024, 1360, 160, W8[1][0] - 0.2, b, '', 'renvoi')
text("« le délibéré du dossier a été rabattu pour envoi des procès-verbaux des sessions précédentes au plaignant <b>afin de garantir le principe du contradictoire</b> »", 1000, 470, 840, W8[0][0] + 2.0, b, 'quote')
text("Lettre du <b>10 octobre 2024</b>, signée du rapporteur <b>Amouda Abou Seydou</b> · article 457 du Code du numérique", 1000, 740, 840, W8[2][0] - 0.2, b, 'quote')

# --- 8.5 : le contradictoire arraché
a, b = Q(8.5); W85 = [W(8.5, i) for i in range(7)]
heads(a + 0.2, b, 'CE QUE LA LOI GARANTIT', 'CE QUE LE PLAIGNANT A DÛ OBTENIR')
text("<b>Art. 454</b> · sanctions prononcées « dans le respect du principe du contradictoire »", 80, 150, 840, W85[0][0] - 0.2, b, 'quote')
text("<b>Art. 457</b> · le rapport est notifié au responsable du traitement, qui peut faire des observations et assister aux séances", 80, 330, 840, W85[0][0] + 3.2, b, 'quote')
for i, (tx, ta, cls) in enumerate([("<b>24 mai</b> · il demande si les échanges sont contradictoires", W85[1][0], 'nm'), ("<b>23 juillet</b> · réponse : formuler sa demande de rapport en séance<br><b>24 juillet</b> · « Je n'ai pas accès »", W85[2][0], 'nm'),
                                    ("<b>28 août</b> · la plénière « ne peut faire suite » à sa demande ; le rapport a été notifié au notaire", W85[3][0], 'nm'),
                                    ("<b>25 septembre</b> · délibéré rabattu « afin de garantir le principe du contradictoire »", W85[4][0], 'nm ocrebox')]):
    text(tx, 1000, 150 + i * 165, 840, ta - 0.2, b, cls)
counter(124, 'JOURS', 80, 560, W85[5][0] - 0.2, b, W85[5][0], W85[5][0] + 1.6, w=840, size=120, sub="du 24 mai au 25 septembre 2024 : de la première question au délibéré rabattu")
text("<b>98 jours</b> après la séance du 19 juin : le plaignant accuse réception des procès-verbaux", 80, 800, 840, W85[5][0] + 2.2, b, 'nm')
text("Il a fallu <span class='ocre'>batailler</span> pour obtenir<br>ce que la loi garantit.", 1000, 830, 840, W85[6][0] - 0.2, b, 'bigtext')

# --- 10.5 : protéger ou menacer
a, b = Q(10.5); W105 = [W(10.5, i) for i in range(6)]
heads(a + 0.2, b, 'CE QUE LA LOI CONFIE À L\'AUTORITÉ', 'CE QU\'ELLE A FAIT')
text("<b>Art. 483</b> · l'Autorité « s'assure que les technologies […] ne comportent pas de menace au regard des libertés publiques et de la vie privée »", 80, 150, 840, W105[0][0] - 0.2, b, 'quote')
card(13, 'DÉC.', 2024, 1000, 150, W105[1][0] - 0.2, b, 'sm', 'vendredi · 10 h 18')
arrow(W105[2][0] - 0.2, b, 1265, 200)
card(16, 'DÉC.', 2024, 1340, 150, W105[2][0] - 0.2, b, 'sm', 'lundi · 7 h 58')
text("« l'APDP se réserve le droit d'agir convenablement et <b>vous répondrez de vos actes</b> en temps opportun »", 1000, 440, 840, W105[2][0] + 1.0, b, 'quote ocrebox')
for i, (num, un) in enumerate([(2, 'J'), (21, 'H'), (40, 'MIN')]):
    counter(num, un, 1000 + i * 290, 640, W105[3][0] - 0.2, b, W105[3][0] + i * 0.5, W105[3][0] + 1.4 + i * 0.5, w=280, size=90)
text("pour brandir la menace", 1000, 770, 840, W105[3][0] + 2.0, b, 'ctext')
counter(440, 'JOURS', 80, 430, W105[4][0] - 0.2, b, W105[4][0], W105[4][0] + 2.4, w=840, size=130, sub="sans décision contre le notaire : du 3 octobre 2023 au 16 décembre 2024")
text("Information du Procureur « sans délai » : <b>aucune mention</b>", 80, 720, 840, W105[4][0] + 3.0, b, 'nm ocrebox')
text("Protéger ?<br><span class='ocre'>Menacer.</span>", 1000, 830, 840, W105[5][0] - 0.2, b, 'bigtext')

# --- 9 : les observations du 21 octobre
a, b = Q(9); W9 = [W(9, i) for i in range(3)]
heads(a + 0.2, b, 'OBSERVATIONS · 21 OCTOBRE 2024', 'TROIS VERSIONS DU NOTAIRE')
pic('obs-p1-c.png', 80, 140, 840, a + 0.4, W9[2][0] - 0.3, "Observations et prétentions du plaignant, p. 1 (coordonnées occultées)", h=730, cls='p9')
pic('obs-p2-c.png', 80, 140, 840, W9[2][0] - 0.3, b, "Observations et prétentions du plaignant, p. 2", h=730, cls='p9')
for i, tx in enumerate(["<b>20 octobre 2016</b> · un mandat auprès de la direction des domaines", "<b>7 septembre 2023</b> · « pas partie aux actes » de son répertoire", "<b>19 juin 2024</b> · une décision de justice devenue exécutoire"]):
    text(tx, 1000, 150 + i * 130, 840, W9[1][0] + i * 5.0, W9[2][0] - 0.3, 'nm')
text("<b>Demandes</b> : sanctions · suppression des données sous astreinte de <b>50 000 FCFA par jour</b> · publication · information du Procureur", 1000, 200, 840, W9[2][0] - 0.2, b, 'quote')

# --- 10 : novembre, décembre
a, b = Q(10); W10 = [W(10, i) for i in range(4)]
heads(a + 0.2, b, 'OCTOBRE · DÉCEMBRE 2024', 'L\'ÉCHANGE DU 13 AU 16 DÉCEMBRE')
pic('echange-p1.png', 80, 140, 840, a + 0.4, W10[3][0] - 0.3, "Courriels du 16 et du 13 décembre 2024 (adresses occultées)", h=730, cls='p10')
pic('echange-p6.png', 80, 140, 840, W10[3][0] - 0.3, b, "Courriel du plaignant, 13 décembre 2024 (extrait)", h=730, cls='p10')
for i, (dd, mm) in enumerate([(23, 'OCT.'), (27, 'NOV.'), (19, 'DÉC.')]):
    card(dd, mm, 2024, 1000 + i * 290, 150, W10[0][0] + i * 1.2 - 0.2, b, 'sm', ('séance', 'séance', 'renvoi')[i])
text("<b>13 décembre</b> · le plaignant informe l'Autorité, par courtoisie, du communiqué de presse qu'il entend publier", 1000, 440, 840, W10[1][0] - 0.2, b, 'quote')
text("<b>16 décembre</b> · l'Autorité : « mis en délibéré pour le 19 décembre prochain » ; « Vous répondrez de vos actes en temps opportun. »", 1000, 610, 840, W10[2][0] - 0.2, b, 'quote')
text("Le plaignant : « Mes deux boussoles sont : <b>la loi et la vérité</b>. »", 1000, 830, 840, W10[3][0] - 0.2, b, 'quote ocretext')

# --- 11 : sept séances
a, b = Q(11); W11 = [W(11, i) for i in range(3)]
text("SEPT SÉANCES · 2024", 80, 62, 1760, a + 0.2, b, 'colhead wide')
SD = [(19, 'JUIN'), (24, 'JUIL.'), (28, 'AOÛT'), (25, 'SEPT.'), (23, 'OCT.'), (27, 'NOV.'), (19, 'DÉC.')]
for i, (dd, mm) in enumerate(SD):
    card(dd, mm, 2024, 80 + i * 252, 190, W11[0][0] + 0.2 + i * 1.15, b, '', '')
text("<b>19 décembre 2024</b> · le dossier est mis en délibéré", 160, 560, 1600, W11[1][0] - 0.2, b, 'quote ocretext')
text("Depuis : <span class='ocre'>rien.</span>", 160, 760, 1600, W11[2][0] - 0.2, b, 'title2')

# --- 12 : les durées
a, b = Q(12); W12 = [W(12, i) for i in range(3)]
counter(443, 'JOURS', 80, 200, W12[0][0] - 0.2, b, W12[0][0], W12[0][0] + 1.6, w=860, size=150, sub="du 3 octobre 2023 au 19 décembre 2024 : de la plainte à la dernière séance")
counter(665, 'JOURS', 1000, 200, W12[1][0] - 0.2, b, W12[1][0], W12[1][0] + 1.6, w=860, size=150, sub="du 19 décembre 2024 au 15 octobre 2026 : depuis la dernière séance")
counter(1108, 'JOURS', 460, 560, W12[2][0] - 0.2, b, W12[2][0], W12[2][0] + 2.2, w=1000, size=190, sub="du 3 octobre 2023 au 15 octobre 2026 : depuis la plainte")

# --- 13 : l'attente
a, b = Q(13); W13 = [W(13, i) for i in range(3)]
text("DEPUIS LE 19 DÉCEMBRE 2024", 80, 62, 840, a + 0.2, b, 'colhead')
CALS = ''.join(f'<div style="height:90px;line-height:90px;font:700 44px DejaVu Serif;color:{"#d4af37" if i in (0, 13, 22) else "#e2e8f0"};text-align:center;border-bottom:1px solid #334155">{m}</div>' for i, m in enumerate(CAL))
el(kf(CALS, [[a, 0, 0, 1], [W13[0][0] + 0.8, 0, 0, 1], [W13[2][1] + 0.5, 0, -(90 * len(CAL) - 640), 1]], 'width:700px'), a + 0.3, b, 0.6, '', 'left:120px;top:140px;width:700px;height:640px;overflow:hidden;border:4px solid var(--gold);border-radius:8px;background:#0b1630')
FOLDC = ('<div style="width:320px;height:230px;background:#cfc3a1;border:3px solid #9d8f66;border-radius:6px;position:relative;box-shadow:0 10px 30px rgba(0,0,0,.55);margin:90px 0 0 100px">'
         '<div style="position:absolute;left:-3px;top:-26px;width:110px;height:26px;background:#cfc3a1;border:3px solid #9d8f66;border-bottom:0;border-radius:6px 6px 0 0"></div></div>')
el(FOLDC, a + 0.3, b, 0.8, '', 'left:1000px;top:200px;width:520px;height:420px')
el(kf(DUST, [[a, 0, 0, 1, 0], [W13[1][0], 0, 0, 1, .25], [W13[2][0], 0, 0, 1, .9]], ''), a + 0.3, b, 0.2, '', 'left:1000px;top:200px;width:520px;height:420px')
text("Aucune décision<br>Aucune notification<br><span class='cap2'>reçue par le plaignant</span>", 1000, 650, 840, W13[1][0] - 0.2, b, 'quote ocrebox')
counter(665, 'JOURS', 80, 830, W13[2][0] - 0.2, b, W13[0][0], W13[2][1], w=840, size=100, sub="du 19 décembre 2024 au 15 octobre 2026")

# --- 14 : les questions
a, b = Q(14); W14 = [W(14, i) for i in range(5)]
card(19, 'DÉC.', 2024, 1100, 220, a + 0.3, b, 'big', 'mis en délibéré')
el('<div class="pulse" style="position:absolute;left:1085px;top:205px;width:450px;height:420px;border:6px solid #c0392b;border-radius:18px"></div>', a + 0.5, b, 0.4, '', 'left:0;top:0;width:1920px;height:1080px')
QS = ["Une décision a-t-elle été prise à l'issue du délibéré du 19 décembre 2024 ?", "Le plaignant en sera-t-il informé, comme l'article 448 le prévoit ?",
      "Le Procureur de la République a-t-il été informé, article 483, point 9 ?", "La demande de suppression des données sur le certificat a-t-elle été examinée ?", "Pourquoi deux jours pour menacer, et 440 jours sans décision ?"]
for i, q in enumerate(QS):
    text(q, 80, 330, 900, W14[i][0] - 0.2, (W14[i + 1][0] - 0.3) if i < 4 else b, 'quest')

# --- 15 : la conclusion
a, b = Q(15); W15 = [W(15, i) for i in range(2)]
for i, (im, lb) in enumerate([('pv-06-19-p1.png', 'procès-verbal'), ('inv-oct.png', 'lettre'), ('echange-p1.png', 'courriel')]):
    pic(im, 1000 + i * 290, 150, 260, W15[0][0] + i * 0.8, b, lb, h=370, cls='p15')
text("Une plainte.<br>Sept séances.<br>Un délibéré.", 80, 200, 840, W15[0][0] - 0.2, b, 'title2')
text("<span class='ocre'>Aucune décision connue du plaignant.</span>", 80, 560, 840, W15[0][0] + 3.0, b, 'bigtext')
text("Ce ne sont pas des opinions : ce sont des procès-verbaux et des lettres.", 1000, 600, 840, W15[1][0] - 0.2, b, 'quote ocretext')
text("Gilles Féliho — plaignant", 1000, 780, 840, W15[1][0] + 1.6, b, 'ctext')

# --- carton final
a, b = SQ[16]
text('wadagni2026-verite.com', 0, 300, 1920, a + 0.6, b, 'url', 0.8)
text('Les pièces reproduites dans ce film sont publiées sur le site, avec leurs empreintes numériques.', 0, 400, 1920, a + 1.6, b, 'finsmall', 0.8)
text("Les extraits reproduits sont des copies partielles ; les coordonnées personnelles sont occultées. "
     "Les références et les articles sont ceux qui figurent dans les pièces et dans le Code du numérique. Le calendrier, le dossier et la poussière sont des illustrations.", 160, 560, 1600, a + 2.6, b, 'precis', 0.8)

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
html = f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Sept séances, aucune décision</title><style>{CSS}</style></head><body><div id="stage">\n' + '\n'.join(EL) + f'\n</div><script>{JS}</script></body></html>'
open(os.path.join(here, 'motion.html'), 'w', encoding='utf-8').write(html)
json.dump({'total': TOTAL, 'sequences': {str(k_): v for k_, v in SQ.items()}, 'cues': cues}, open(os.path.join(out, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
print('durée totale', round(TOTAL, 1), 's ; séquences', {k_: (round(a_, 1), round(b_, 1)) for k_, (a_, b_) in SQ.items()})

