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

