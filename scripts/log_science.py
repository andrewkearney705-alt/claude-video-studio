"""Log the measurable 'science' of a finished variant so results can be correlated later.
usage: science.py VARIANT_DIR POST_ID -> prints JSON"""
import json, sys, subprocess, re, statistics as st, numpy as np
V, PID = sys.argv[1], sys.argv[2]
E = json.load(open(f'{V}/edl_f.json')); F = E['fps']; segs = E['segs']; dur = E['frames'] / F
W = json.load(open(f'{V}/words_cut.json')); C = json.load(open(f'{V}/gfx_cfg.json'))
Z = json.load(open(f'{V}/zoom.json'))
hook_lab = segs[0]['label']; hook_segs = [s for s in segs if s['label'] == hook_lab]
hook_end = (hook_segs[-1]['out_f'] + hook_segs[-1]['n']) / F
hook_words = [w for w in W if w['t'] < hook_end]
shots = [s['n'] / F for s in segs]
labels = []
for s in segs:
    if not labels or labels[-1][0] != s['label']: labels.append([s['label'], s['out_f'] / F])
payoff = labels[-1][1]
src_span = sum(s['src_out'] - s['src_in'] for s in segs)
M = np.load(f'{V}/masks.npy', mmap_mode='r'); idx = np.linspace(0, len(M) - 1, 40).astype(int)
subj = float(np.mean([(M[i] > 128).mean() for i in idx]))
top = []
for i in idx:
    ys = np.nonzero((M[i] > 128).any(1))[0]; top.append(ys.min() / M.shape[1] if len(ys) else None)
ld = subprocess.run(['ffmpeg', '-hide_banner', '-i', f'{V}/final.mp4', '-af', 'ebur128=peak=true:framelog=quiet', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = re.findall(r'I:\s+(-?[\d.]+) LUFS', ld); P = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', ld)
groups = {}
for w in W: groups.setdefault(w['g'], []).append(w)
emph = [dict(t=w['t'], word=w['w'], key=bool(w.get('k'))) for w in W if w.get('b') or w.get('k')]
pops = [dict(t0=p['t0'], t1=p['t1'], text=' '.join(i['text'] for i in p['items'])) for p in C['pops']]
out = dict(post_id=PID, measuredAt='2026-11-08', duration_s=round(dur, 2), length_bucket='35-50' if dur < 50 else '50+',
    hook=dict(label=hook_lab, text=' '.join(w['w'] for w in hook_words), words=len(hook_words), seconds=round(hook_end, 2),
              words_per_s=round(len(hook_words) / max(hook_end, .1), 2), first_word_s=round(W[0]['t'], 2) if W else None,
              big_text_in_first_3s=any(p['t0'] < 3 for p in pops), face_in_first_frame=bool((M[0] > 128).mean() > 0.05)),
    speech=dict(words=len(W), words_per_s=round(len(W) / dur, 2)),
    pacing=dict(cuts=len(segs) - 1, cuts_per_min=round((len(segs) - 1) / dur * 60, 1), median_shot_s=round(st.median(shots), 2),
                longest_shot_s=round(max(shots), 2), punch_ins=len(Z), sections=[dict(label=l, start_s=round(t, 2)) for l, t in labels]),
    payoff_line_s=round(payoff, 2), payoff_share_of_video=round(payoff / dur, 2),
    text=dict(caption_chunks=len(groups), avg_words_per_chunk=round(len(W) / max(len(groups), 1), 2), caption_style='Plus Jakarta Sans bold, cream, sentence case, bottom (y 1330-1400)',
              big_word_pops=pops, emphasized_caption_words=emph, key_idea_word=next((e['word'] for e in emph if e['key']), None),
              key_idea_s=next((e['t'] for e in emph if e['key']), None), name_wordmark=False),
    framing=dict(subject_share_of_frame=round(subj, 3), head_top_share=round(float(np.median([t for t in top if t is not None])), 3)),
    sound=dict(music='felt piano bed', sfx='none', breath_before_payoff=True, loudness_lufs=float(I[-1]) if I else None, true_peak_db=float(P[-1]) if P else None),
    tested_element='hook (everything after the hook is identical across variants)')
print(json.dumps(out))
