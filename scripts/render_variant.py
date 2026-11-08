"""Render one variant: graphics (front + back), sound, mix, composite, no-music version.
usage: runvar.py VARIANT_DIR pops.json [--test t1 t2 ...]
pops.json: {"capY":1300,"capSize":58,"wmY":1180,"popY":250,"zoomCenter":"0.5,0.4","musicDb":-10,"bpm":72,
            "pops":[{"on":"WORST","dur":2.2,"y":250,"items":[{"text":"The worst","f":"sans","size":150,"on":"WORST"},{"text":"advice","f":"it","size":170,"on":"ADVICE","color":"#A9C4A6"}]}]}"""
import json, sys, os, subprocess
K = '' + os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + ''
V = os.path.abspath(sys.argv[1]); C = json.load(open(sys.argv[2])); TEST = sys.argv[4:] if len(sys.argv) > 3 and sys.argv[3] == '--test' else None
E = json.load(open(f'{V}/edl_f.json')); F = E['fps']; dur = E['frames'] / F
W = json.load(open(f'{V}/words_cut.json'))
def wt(word, after=0.0):
    word = word.lower()
    for w in W:
        if w['w'].strip('.,?!').lower() == word and w['t'] >= after - 1e-3: return w['t']
    raise SystemExit(f'word not found: {word} after {after}')
pops = []; last = 0.0
for p in C['pops']:
    t0 = wt(p['on'], p.get('after', last)); last = t0
    items = []
    for it in p['items']:
        ti = wt(it['on'], t0) if it.get('on') else t0
        items.append({k: v for k, v in it.items() if k != 'on'} | {'t': round(ti, 3)})
    t1 = min(dur, t0 + p.get('dur', 2.2)) if 'until' not in p else wt(p['until'], t0)
    pops.append(dict(t0=round(t0 - 0.02, 3), t1=round(t1, 3), layer=p.get('layer', 'back'), y=p.get('y', C.get('popY', 250)), items=items))
# no two pops overlap
for a, b in zip(pops, pops[1:]):
    if a['t1'] > b['t0']: a['t1'] = b['t0']
cfg = dict(capY=C['capY'], capSize=C['capSize'], bigScale=C.get('bigScale', 1.5), wm=None, wmY=C['wmY'], pops=pops, maxW=C.get('maxW', 820))
json.dump(cfg, open(f'{V}/gfx_cfg.json', 'w'), indent=1)
tpl = open(f'{K}/templates/gfx_brandv2.html').read().replace('__CFG__', json.dumps(cfg))
name = 'gfx_v_' + os.path.basename(V) + '.html'
open(f'{K}/templates/{name}', 'w').write(tpl)
def gfx(style, out, times=None):
    subprocess.run(['python3', f'{K}/scripts/render_gfx.py', f'{K}/templates/{name}', V, style, out] + (times or []), check=True)
if TEST:
    gfx('front', f'{V}/test_front', TEST); gfx('back', f'{V}/test_back', TEST); print('test frames done'); sys.exit()
gfx('front', f'{V}/gfx_front'); gfx('back', f'{V}/gfx_back')
# sound: bed only, no SFX hits (founder one-take recipe); breath before the last line
lastseg = E['segs'][-1]['out_f'] / F
snd = dict(bpm=C.get('bpm', 72), busy=[], breath=round(max(0.5, lastseg - 0.25), 2), sfx=[])
json.dump(snd, open(f'{V}/sound.json', 'w'))
subprocess.run(['python3', f'{K}/scripts/sound.py', V, 'A'], check=True)
env = dict(os.environ, MUSIC_DB=str(C.get('musicDb', -10)))
subprocess.run(['bash', f'{K}/scripts/mix.sh', V, 'A', '1'], check=True, env=env)
subprocess.run(['bash', f'{K}/scripts/mix.sh', V, 'A', '0'], check=True, env=env)
# punch-ins: alternate 1.0 / 1.07 across jump cuts so joins read as camera moves
zoom = []; z = False
for s in E['segs']:
    a, b = s['out_f'] / F, (s['out_f'] + s['n']) / F
    if z: zoom.append([a, b, 1.07, 1.07])
    z = not z
json.dump(zoom, open(f'{V}/zoom.json', 'w'))
env = dict(os.environ, X264_PRESET='veryfast', GFX_BACK=f'{V}/gfx_back', ZOOM_CENTER=C.get('zoomCenter', '0.5,0.42'))
out = f'{V}/final.mp4'
subprocess.run(['python3', f'{K}/scripts/composite.py', V, f'{V}/gfx_front', f'{V}/mix_A.wav', out], check=True, env=env)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-i', f'{V}/mix_A_nomusic.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', f'{V}/final_nomusic.mp4'], check=True)
print('DONE', out)
