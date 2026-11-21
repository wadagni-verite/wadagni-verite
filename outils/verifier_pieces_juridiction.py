"""Signale les occultations vectorielles (aplats noirs opaques) dans des PDF destinés à une juridiction.
Règle : on ne floute, ne noircit et n'occulte jamais une pièce de procédure (voir .claude/skills/pieces-juridiction).
Limite : une occultation incorporée à l'image n'est pas détectée ; contrôler aussi le rendu à l'œil.
Usage : python3 -I outils/verifier_pieces_juridiction.py fichier1.pdf [fichier2.pdf ...]"""
import sys, pymupdf

def aplats_noirs(path):
    res = []
    for i, p in enumerate(pymupdf.open(path)):
        for d in p.get_drawings():
            f = d.get("fill")
            op = d.get("fill_opacity")
            op = 1.0 if op is None else op
            r = d["rect"]
            if f and sum(f[:3]) < 0.15 and op > 0.5 and r.width > 20 and r.height > 8:
                res.append((i + 1, tuple(round(v) for v in r)))
    return res

if __name__ == "__main__":
    ko = 0
    for f in sys.argv[1:]:
        a = aplats_noirs(f)
        if a:
            ko += 1
            print(f"OCCULTATION ? {f} : {len(a)} aplat(s) noir(s) opaque(s), pages/rect {a[:6]}")
        else:
            print(f"ok {f}")
    sys.exit(1 if ko else 0)
