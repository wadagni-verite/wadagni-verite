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
