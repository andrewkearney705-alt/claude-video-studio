"""Sound for a cut: voice assembly, music bed, SFX.
usage: python3 sound.py PROJECT_DIR STYLE
reads  edl_f.json, words_cut.json, src48.wav, den48.wav (+ den_gain.txt)
       sound.json (optional): {"bpm":90, "busy":[[4.3,13.0],[14.5,16.4]], "breath":13.75,
                               "sfx":[["whoosh", 4.03, 0.16], ["paper","ROBERTO",0.22], ...]}
           sfx times can be seconds or a spoken WORD (first match; "WORD@12" = first match after 12 s)
writes voice.wav, music.wav, sfx_STYLE.wav
"""
import numpy as np, json, wave, sys, os
from scipy.signal import butter, sosfilt, fftconvolve
P = sys.argv[1]; STYLE = sys.argv[2] if len(sys.argv) > 2 else 'A'; os.chdir(P)
SR = 48000; rng = np.random.default_rng(7)
E = json.load(open('edl_f.json')); Wd = json.load(open('words_cut.json')); FPS = E['fps']
CFG = json.load(open('sound.json')) if os.path.exists('sound.json') else {}
def wt(w, a=0):
    w = w.strip('.,…"!?').upper(); return next(x['t'] for x in Wd if x['w'].strip('.,…"!?').upper() == w and x['t'] >= a)
DUR = E['frames'] / FPS; N = int((DUR + 0.8) * SR); t = np.arange(N) / SR
def rd(p):
    w = wave.open(p); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return a.reshape(-1, w.getnchannels()).mean(1) if w.getnchannels() > 1 else a
def wr(p, x):
    x = np.clip(x, -1, 1); ch = 1 if x.ndim == 1 else 2; w = wave.open(p, 'w'); w.setnchannels(ch); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x.T.reshape(-1) if ch == 2 else x).__mul__(32767).astype(np.int16).tobytes()); w.close()
def filt(x, f, kind, o=2): return sosfilt(butter(o, f, btype=kind, fs=SR, output='sos'), x)
lp = lambda x, f, o=2: filt(x, f, 'low', o); hp = lambda x, f, o=2: filt(x, f, 'high', o)
bp = lambda x, a, b, o=2: filt(x, [a, b], 'band', o)

# ---------------- voice: denoised take + a little of the real room, frame-accurate joins ----------------
den = rd('den48.wav'); g = float(open('den_gain.txt').read()) if os.path.exists('den_gain.txt') else 4
orig = rd('src48.wav') * g
src = den + 0.05 * orig[:len(den)]
voice = np.zeros(N); X = int(0.02 * SR)
for s in E['segs']:
    a = int(s['f_in'] / FPS * SR); n = int(s['n'] / FPS * SR)
    seg = src[max(0, a - X // 2): a + n + X // 2].copy()
    fi = np.sin(np.linspace(0, np.pi / 2, X)) ** 2; seg[:X] *= fi; seg[-X:] *= fi[::-1]
    o = int(s['out_f'] / FPS * SR) - X // 2; o0 = max(0, o)
    voice[o0:o0 + len(seg) - (o0 - o)] += seg[o0 - o:][:N - o0]
wr('voice.wav', voice)

# ---------------- reverb ----------------
def make_ir(sec, decay, lpf):
    n = int(sec * SR); tt = np.arange(n) / SR
    L = lp(rng.standard_normal(n), lpf) * np.exp(-tt * decay); R = lp(rng.standard_normal(n), lpf) * np.exp(-tt * decay)
    L[:int(.015 * SR)] = 0; R[:int(.021 * SR)] = 0
    return np.stack([L, R]) / np.sqrt(np.sum(L ** 2))
IR_HALL = make_ir(2.8, 2.4, 5000); IR_ROOM = make_ir(0.9, 7, 7000)
def verb(x, ir, mix):
    wet = np.stack([fftconvolve(x, ir[0])[:len(x)], fftconvolve(x, ir[1])[:len(x)]])
    return np.stack([x, x]) * (1 - mix) + wet * mix

# ---------------- music: warm felt-piano bed with an arc ----------------
bpm = CFG.get('bpm', 90); beat = 60 / bpm; bar = beat * 4; mf = lambda m: 440 * 2 ** ((m - 69) / 12)
prog = [[41, 53, 57, 60, 64, 67], [45, 52, 55, 60, 64, 67], [38, 50, 53, 57, 60, 64], [46, 53, 57, 58, 62, 65]]  # Fmaj9 Am7 Dm9 Bbmaj7
def felt(f, n, vel):
    tt = np.arange(n) / SR
    env = (1 - np.exp(-tt / 0.006)) * (0.65 * np.exp(-tt * 1.6) + 0.35 * np.exp(-tt * 0.45))
    x = np.zeros(n)
    for k, a in ((1, 1), (2, .38), (3, .16), (4, .07), (5, .03)):
        fk = f * k * (1 + 0.0004 * k * k)
        x += a * np.sin(2 * np.pi * fk * tt + rng.random() * 6) * np.exp(-tt * (0.6 + 0.7 * k))
    ham = lp(rng.standard_normal(n), 1800) * np.exp(-tt * 90) * 0.15
    return (x * env + ham) * vel
pno = np.zeros(N); pad = np.zeros(N); sub = np.zeros(N); kick = np.zeros(N); shk = np.zeros(N)
def put(buf, x, at):
    s = int(at * SR)
    if s >= N: return
    e = min(N, s + len(x)); buf[s:e] += x[:e - s]
for bi in range(int(DUR / bar) + 2):
    ch = prog[bi % 4]; s0 = bi * bar
    # piano: rolled chord on 1, two upper notes on the "and" of 2 and on 4
    for j, m in enumerate(ch[1:]): put(pno, felt(mf(m), int(3.2 * SR), 0.10 - j * 0.008), s0 + j * 0.022 + rng.random() * 0.006)
    put(pno, felt(mf(ch[4] + 12), int(2 * SR), 0.035), s0 + beat * 1.5)
    put(pno, felt(mf(ch[5]), int(2 * SR), 0.03), s0 + beat * 3)
    # pad: detuned saws, heavily low-passed
    n = int((bar + 0.6) * SR); tt = np.arange(n) / SR; p = np.zeros(n)
    for m in ch[1:4]:
        for d in (-0.08, 0.0, 0.09):
            ph = (mf(m) * (1 + d / 100) * tt + rng.random()) % 1; p += 2 * ph - 1
    p = lp(lp(p, 900), 1200) * np.minimum(1, tt / 0.5) * np.minimum(1, np.maximum(0, (n / SR - tt) / 0.6))
    put(pad, p * 0.012, s0)
    # sub on root
    n = int(bar * SR); tt = np.arange(n) / SR
    put(sub, np.sin(2 * np.pi * mf(ch[0] - 12) * tt) * np.minimum(1, tt / 0.05) * np.exp(-tt * 0.5) * 0.16, s0)
# drums: soft kick + shaker, only in the busy middle sections
def kk():
    n = int(0.45 * SR); tt = np.arange(n) / SR; f = 48 + 70 * np.exp(-tt * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) + lp(rng.standard_normal(n), 3000) * np.exp(-tt * 300) * 0.2
def sh():
    n = int(0.09 * SR); tt = np.arange(n) / SR; return bp(rng.standard_normal(n), 6000, 12000) * np.exp(-tt * 45)
sections = [tuple(x) for x in CFG.get('busy', [(DUR * 0.2, DUR * 0.85)])]
b = 0.0
while b < DUR:
    if any(a <= b < e for a, e in sections):
        if round(b / beat) % 2 == 0: put(kick, kk() * 0.33, b)
        put(shk, sh() * (0.05 if round(b / beat * 2) % 2 else 0.028), b)
        put(shk, sh() * 0.022, b + beat / 2)
    b += beat / 1 if False else beat
    # shaker 8ths handled above
# breath at "once": everything but pad dips 13.0-14.5
arc = np.ones(N)
if CFG.get('breath'): arc *= 1 - 0.55 * np.clip(1 - np.abs(t - CFG['breath']) / 0.9, 0, 1)
mus = (pno * 1.0 + pad + sub) * arc + kick + shk
mus = hp(mus, 32)
mus = np.tanh(mus * 1.8) / 1.8                        # tape-ish saturation
mus = lp(mus, 7500)
mus *= np.minimum(1, t / 0.4) * np.clip((DUR + 0.6 - t) / 1.2, 0, 1)
musS = verb(mus, IR_HALL, 0.22)
# gentle stereo width on pad via short Haas offset
d = int(0.011 * SR); padS = np.zeros_like(pad); padS[d:] = pad[:-d]; musS[1] += (padS - pad) * arc * 0.5
wr('music.wav', musS.T)

# ---------------- SFX library (soft, organic) ----------------
def whoosh(d=0.5, lo=200, hi=4000):
    n = int(d * SR); x = rng.standard_normal(n); u = np.linspace(0, 1, n); out = np.zeros(n); K = 16
    for i in range(K):
        f = lo * (hi / lo) ** (i / K); sl = slice(i * n // K, (i + 1) * n // K); out[sl] = bp(x, f * .7, min(f * 1.5, 20000))[sl]
    return lp(out, 6000) * np.sin(np.pi * u) ** 2.5
def thump(g=1.0):
    n = int(0.5 * SR); tt = np.arange(n) / SR; f = 70 + 60 * np.exp(-tt * 30)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 12) + lp(rng.standard_normal(n), 1200) * np.exp(-tt * 60) * .4) * g
def paper(g=1.0):  # card landing on a table
    n = int(0.12 * SR); tt = np.arange(n) / SR
    return (bp(rng.standard_normal(n), 900, 5000) * np.exp(-tt * 70) + np.sin(2 * np.pi * (140 + 40 * rng.random()) * tt) * np.exp(-tt * 50) * .6) * g
def tick(f=2600, g=1.0):
    n = int(0.035 * SR); tt = np.arange(n) / SR; return (np.sin(2 * np.pi * f * tt) * .6 + bp(rng.standard_normal(n), 3000, 9000) * .5) * np.exp(-tt * 160) * g
def key(g=1.0):
    n = int(0.06 * SR); tt = np.arange(n) / SR
    return (bp(rng.standard_normal(n), 1500, 7000) * np.exp(-tt * 120) + np.sin(2 * np.pi * (300 + 80 * rng.random()) * tt) * np.exp(-tt * 90) * .3) * g
def swell(d=0.45):
    n = int(d * SR); u = np.linspace(0, 1, n); x = bp(rng.standard_normal(n), 300, 6000)
    return x * u ** 3 * (u < 0.98)
def boom():
    n = int(2.4 * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * 42 * tt) * np.exp(-tt * 2.2) * (1 - np.exp(-tt / .01)) + lp(rng.standard_normal(n), 400) * np.exp(-tt * 6) * .25
def shimmer():
    n = int(1.6 * SR); tt = np.arange(n) / SR; x = np.zeros(n)
    for f in (1760, 2637, 3520): x += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 3.5)
    return x * (1 - np.exp(-tt / .03)) * .2
def pop():
    n = int(0.12 * SR); tt = np.arange(n) / SR; f = 500 + 900 * np.exp(-tt * 60)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 40)

LIB = dict(whoosh=whoosh, thump=thump, paper=paper, tick=tick, key=key, swell=swell, boom=boom, shimmer=shimmer, pop=pop)
def when(x):
    if isinstance(x, (int, float)): return float(x)
    w, _, a = str(x).partition('@'); return wt(w.upper(), float(a or 0))
def build(events):
    fx = np.zeros(N)
    for ev in events:
        name, at, g = ev[0], when(ev[1]), ev[2]; args = ev[3] if len(ev) > 3 else []
        x = LIB[name](*args); s0 = int(at * SR)
        if 0 <= s0 < N: e = min(N, s0 + len(x)); fx[s0:e] += x[:e - s0] * g
    return verb(fx, IR_ROOM, 0.18)
ev = CFG.get('sfx_' + STYLE, CFG.get('sfx', []))
wr(f'sfx_{STYLE}.wav', build(ev).T)
print('sound done', round(DUR, 2), 's,', len(ev), 'sfx events')
