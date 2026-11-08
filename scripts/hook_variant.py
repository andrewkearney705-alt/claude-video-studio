"""Build a hook variant project from a superset project (hooks + body cut, masked and graded once).
usage: mkvar.py SUPERSET_DIR VARIANT_DIR spec.json
spec: {"labels":["H_A","B1",...], "fix":{"A EYE":"AI",...}, "hide":["LIKE","UM"], "keys":{"WORD@sec":"#97A9FF"}, "breaks":[...]}"""
import json, sys, os, subprocess, shutil, numpy as np
S, V, spec = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
os.makedirs(V, exist_ok=True)
E = json.load(open(f'{S}/edl_f.json')); F = E['fps']; Wc = json.load(open(f'{S}/words_cut.json'))
segs = []; o = 0; ranges = []
for lab in spec['labels']:
    for s in E['segs']:
        if s['label'] == lab:
            segs.append(dict(s, out_f=o, sup_f=s['out_f'])); ranges.append((s['out_f'], s['n'])); o += s['n']
json.dump(dict(fps=F, frames=o, segs=segs), open(f'{V}/edl_f.json', 'w'), indent=1)
# words onto the variant timeline
words = []
SW = json.load(open(f'{S}/words.json'))
for k, s in enumerate(segs):
    a = s['f_in'] / F; b = (s['f_in'] + s['n']) / F
    for w in SW:
        if a - 1e-3 <= w['t0'] < b - 0.02:
            words.append(dict(w=w['w'].upper(), t=round(s['out_f'] / F + (w['t0'] - a), 3), seg=k))
# spelling fixes: multiword merges first
fix = {k.upper(): v for k, v in spec.get('fix', {}).items()}
out = []; i = 0
while i < len(words):
    done = False
    for n in (3, 2):
        key = ' '.join(x['w'] for x in words[i:i + n])
        if key in fix: out.append(dict(words[i], w=fix[key])); i += n; done = True; break
    if done: continue
    w = words[i]; out.append(dict(w, w=fix.get(w['w'], w['w']))); i += 1
hide = set(x.upper() for x in spec.get('hide', []))
out = [w for w in out if w['w'].upper() not in hide]
# sentence case: lowercase, capitalise first word of each sentence (a segment that starts a new label) and I / AI
starts = set(); prev = None
for k, s in enumerate(segs):
    if s['label'] != prev: starts.add(k)
    prev = s['label']
first_seen = set()
for w in out:
    t = w['w']
    if t.isupper() and t not in ('I', 'AI', "I'M", "I'VE", "I'D", "I'LL"): t = t.lower()
    t = t.replace("I'M", "I'm").replace("I'VE", "I've").replace("I'LL", "I'll").replace("I'D", "I'd")
    if w['seg'] in starts and w['seg'] not in first_seen: t = t[:1].upper() + t[1:]; first_seen.add(w['seg'])
    w['w'] = t
# caption chunks: 1-4 words, break at segment starts, at ~18 chars, never end on a weak word
weak = {'the', 'to', 'a', 'an', 'and', 'of', 'your', 'my', 'in', 'into', 'that', 'for', 'at', 'with', 'or', 'but', 'so', 'is'}
for kk in spec.get('emph', []):
    word, _, after = kk.partition('@'); after = float(after or 0)
    for w in out:
        if w['w'].strip('.,').lower() == word.lower() and w['t'] >= after: w['b'] = 1; break
g = 0; cur = []
def flush():
    global g, cur
    if cur: g += 1
    cur = []
for w in out:
    newsent = bool(cur) and cur[-1]['seg'] != w['seg']
    chars = sum(len(x['w']) + 1 for x in cur)
    if cur and (newsent or len(cur) >= 4 or chars + len(w['w']) > 18) and cur[-1]['w'].lower() not in weak: flush()
    elif cur and len(cur) >= 5: flush()
    if w.get('b') and cur and cur[-1]['w'].lower() not in weak: flush()
    w['g'] = g; cur.append(w)
    if w.get('b'): flush()
for kk, col in spec.get('keys', {}).items():
    word, _, after = kk.partition('@'); after = float(after or 0)
    for w in out:
        if w['w'].strip('.,').lower() == word.lower() and w['t'] >= after: w['k'] = col; break
json.dump([{k: w[k] for k in w if k != 'seg'} for w in out], open(f'{V}/words_cut.json', 'w'))
# picture + masks
L = []
os.makedirs(f'{V}/vs', exist_ok=True)
for k, (f0, n) in enumerate(ranges):
    p = f'{V}/vs/v{k:02d}.mov'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{f0 / F:.5f}', '-i', f'{S}/graded.mov', '-frames:v', str(n), '-c', 'copy', p], check=True)
    L.append(f"file 'vs/v{k:02d}.mov'")
open(f'{V}/vs.txt', 'w').write('\n'.join(L))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{V}/vs.txt', '-c', 'copy', f'{V}/graded.mov'], check=True)
M = np.load(f'{S}/masks.npy', mmap_mode='r')
np.save(f'{V}/masks.npy', np.concatenate([M[f0:f0 + n] for f0, n in ranges]))
for f in ('src48.wav', 'den48.wav', 'den_gain.txt'):
    if os.path.exists(f'{S}/{f}'): shutil.copy(f'{S}/{f}', f'{V}/{f}')
nf = int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', f'{V}/graded.mov'], capture_output=True, text=True).stdout.strip() or 0)
print(V, 'frames', o, 'video frames', nf, 'dur', round(o / F, 2), 'words', len(out), 'chunks', g + 1)
