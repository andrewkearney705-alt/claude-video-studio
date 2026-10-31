"""Build the cut from an edit decision list, at the source frame rate, tone-mapping iPhone HDR.
usage: python3 cut.py SOURCE.mov PROJECT_DIR
needs PROJECT_DIR/edl.json : [{"label":"L1","src_in":3.44,"src_out":6.52,"keep":"I just taught Claude..."}, ...]
       PROJECT_DIR/words.json (from transcribe.py) and a 'display' list is optional
writes cut_sdr.mov (ProRes 4444-ish, 1080x1920), edl_f.json (frame-accurate), words_cut.json (word times on the new timeline)"""
import sys, json, subprocess, os
SRC, P = sys.argv[1], sys.argv[2]
probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate,color_transfer,width,height',
                                   '-of', 'json', SRC], capture_output=True, text=True).stdout)['streams'][0]
a, b = probe['r_frame_rate'].split('/'); F = round(int(a) / int(b))
hdr = probe.get('color_transfer') in ('arib-std-b67', 'smpte2084')
print('fps', F, 'HDR' if hdr else 'SDR', probe['width'], 'x', probe['height'])
TM = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100:w=1080:h=1920:f=spline36,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv444p10le") if hdr else \
     "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv444p10le"
if hdr and probe.get('color_transfer') == 'smpte2084': TM = TM.replace('tin=arib-std-b67', 'tin=smpte2084')
edl = json.load(open(f'{P}/edl.json')); segs = []; o = 0; L = []
os.makedirs(f'{P}/segs', exist_ok=True)
for i, s in enumerate(edl):
    fi = round(s['src_in'] * F); n = round((s['src_out'] - s['src_in']) * F)
    segs.append(dict(label=s['label'], f_in=fi, n=n, out_f=o, src_in=s['src_in'], src_out=s['src_out'])); o += n
    f = f'{P}/segs/seg{i:02d}.mov'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{fi / F:.4f}', '-i', SRC, '-frames:v', str(n), '-an', '-vf', TM, '-c:v', 'prores_ks', '-profile:v', '3', f], check=True)
    L.append(f"file 'segs/seg{i:02d}.mov'")
open(f'{P}/segs.txt', 'w').write('\n'.join(L))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-i', f'{P}/segs.txt', '-c', 'copy', f'{P}/cut_sdr.mov'], check=True, cwd=None)
json.dump(dict(fps=F, frames=o, segs=segs), open(f'{P}/edl_f.json', 'w'), indent=1)
words = json.load(open(f'{P}/words.json')); out = []
for w in words:
    for s in segs:
        if s['src_in'] - 1e-3 <= w['t0'] < s['src_out']:
            out.append(dict(w=w['w'].upper(), t=round((s['out_f'] + (w['t0'] - s['src_in']) * F) / F, 3))); break
json.dump(out, open(f'{P}/words_cut.json', 'w'))
print('frames', o, 'duration', round(o / F, 2), 's;', len(out), 'words kept')
