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


