"""Pre-render checks for docs/editing-rules.md. Prints PASS/FAIL lines; exit code 1 on any FAIL.
usage:
  python3 qa_check.py audio PROJECT_DIR [voice.wav]   dead space: runs > 20 ms more than 11 dB under speaking level
  python3 qa_check.py captions PROJECT_DIR            2-3 word chunks, never ending on a weak word -> captions.json
  python3 qa_check.py safezone GFX_DIR                Instagram safe zone on every graphics frame (transparent PNGs)
audio reads PROJECT_DIR/edl_f.json and, if present, PROJECT_DIR/edl.json "tone" per line
(normal = 0 gap, serious = up to 6 frames held at the end of the line, joke = 0)."""
import sys, os, json, glob, wave
import numpy as np

DEAD_DB, MAX_DEAD_MS, WIN_MS = 11.0, 20, 10
WEAK = set('a an the to of my and but or in on for with is at as so your our its'.split())
# Instagram Reels, 1080x1920 (Hopper 2026 guide; confirm on a posted reel and update)
ZONES = {'top': (0, 0, 1080, 270), 'bottom': (0, 1250, 1080, 1920), 'left': (0, 0, 65, 1920),
         'right': (1015, 0, 1080, 1920), 'buttons': (940, 1150, 1080, 1920)}
FULLFRAME = 0.6   # frames more than 60% covered are full-frame scenes: check those by eye on the contact sheet


def read_wav(path):
    w = wave.open(path)
    n, ch, sw, sr = w.getnframes(), w.getnchannels(), w.getsampwidth(), w.getframerate()
    raw = w.readframes(n)
    dt = {2: np.int16, 4: np.int32}[sw]
    x = np.frombuffer(raw, dt).astype(np.float32).reshape(-1, ch).mean(1) / np.iinfo(dt).max
    return x, sr


def audio(P, wav=None):
    x, sr = read_wav(wav or os.path.join(P, 'voice.wav'))
    hop = int(sr * WIN_MS / 1000)
    frames = x[:len(x) // hop * hop].reshape(-1, hop)
    db = 20 * np.log10(np.sqrt((frames ** 2).mean(1)) + 1e-9)
    speak = np.percentile(db[db > db.max() - 40], 75)        # typical speaking level
    dead = db < speak - DEAD_DB
    E = json.load(open(os.path.join(P, 'edl_f.json'))); F = E['fps']
    tones = {}
    if os.path.exists(os.path.join(P, 'edl.json')):
        tones = {s['label']: s.get('tone', 'normal') for s in json.load(open(os.path.join(P, 'edl.json')))}
    allow = []   # (start_s, end_s) where a held pause is allowed: last 6 frames + 20 ms of serious lines
    for s in E['segs']:
        if tones.get(s['label']) == 'serious':
            end = (s['out_f'] + s['n']) / F
            allow.append((end - 6 / F - 0.03, end + 0.03))
    joins = [s['out_f'] / F for s in E['segs'][1:]]
    runs, i = [], 0
    edges = np.flatnonzero(np.diff(np.r_[0, dead.astype(int), 0]))
    for a, b in zip(edges[::2], edges[1::2]):
        t0, t1 = a * WIN_MS / 1000, b * WIN_MS / 1000
        if (t1 - t0) * 1000 <= MAX_DEAD_MS or t0 < 0.05 or t1 > len(db) * WIN_MS / 1000 - 0.05:
            continue
        if any(lo <= t0 and t1 <= hi for lo, hi in allow):
            continue
        near = min(joins, key=lambda j: abs(j - (t0 + t1) / 2)) if joins else None
        where = f'at join {near:.2f}s' if near is not None and t0 - 0.05 <= near <= t1 + 0.05 else 'inside a line'
        runs.append((t0, t1, where))
    print(f'speaking level {speak:.1f} dBFS, dead threshold {speak - DEAD_DB:.1f} dBFS')
    for t0, t1, where in runs:
        print(f'  dead {t0:6.2f}-{t1:6.2f}s ({(t1 - t0) * 1000:.0f} ms, {round((t1 - t0) * F)} frames) {where}')
    print(('FAIL' if runs else 'PASS'), f'audio: {len(runs)} dead runs over {MAX_DEAD_MS} ms')
    return not runs


def captions(P):
    words = json.load(open(os.path.join(P, 'words_cut.json')))
    chunks, cur = [], []
    for k, w in enumerate(words):
        cur.append(w)
        nxt = words[k + 1]['w'] if k + 1 < len(words) else None
        end_word = w['w'].strip('.,!?;:"\'').lower()
        sentence_end = w['w'].rstrip()[-1:] in '.!?'
        if nxt is None or sentence_end or (len(cur) >= 2 and end_word not in WEAK) or len(cur) == 3:
            chunks.append(cur); cur = []
    bad = [c for c in chunks if c[-1]['w'].strip('.,!?;:"\'').lower() in WEAK and len(chunks) > 1]
    long = [c for c in chunks if len(c) > 3]
    out = [dict(t=round(c[0]['t'], 3), text=' '.join(w['w'] for w in c)) for c in chunks]
    json.dump(out, open(os.path.join(P, 'captions.json'), 'w'), indent=0)
    for c in bad:
        print(f'  weak ending at {c[0]["t"]:.2f}s: "{" ".join(w["w"] for w in c)}"')
    ok = not bad and not long
    print(('PASS' if ok else 'FAIL'), f'captions: {len(chunks)} chunks, {len(bad)} weak endings -> captions.json')
    return ok


def safezone(G):
    from PIL import Image
    files = sorted(glob.glob(os.path.join(G, '*.png')))
    hits, full = {}, 0
    for f in files:
        a = np.asarray(Image.open(f).convert('RGBA'))[:, :, 3]
        if a.shape != (1920, 1080):
            print(f'  {os.path.basename(f)} is {a.shape[1]}x{a.shape[0]}, expected 1080x1920'); continue
        if (a > 16).mean() > FULLFRAME:
            full += 1; continue
        for name, (x0, y0, x1, y1) in ZONES.items():
            if (a[y0:y1, x0:x1] > 64).sum() > 200:
                hits.setdefault(name, []).append(os.path.basename(f))
    for name, fs in hits.items():
        print(f'  {name}: {len(fs)} frames, first {fs[0]}, last {fs[-1]}')
    print(('FAIL' if hits else 'PASS'), f'safezone: {len(files)} frames, {full} full-frame scenes skipped (check on contact sheet)')
    return not hits


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    fn = {'audio': audio, 'captions': captions, 'safezone': safezone}.get(mode)
    if not fn:
        print(__doc__); sys.exit(2)
    sys.exit(0 if fn(*sys.argv[2:]) else 1)
