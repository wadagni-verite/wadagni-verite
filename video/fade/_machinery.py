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

