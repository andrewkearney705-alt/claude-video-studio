"""Render an HTML motion-graphics template to transparent PNG frames (deterministic render(t)).
usage: python3 render_gfx.py TEMPLATE.html PROJECT_DIR STYLE OUT_DIR [t1 t2 ... for test frames]
template placeholders: __TIMELINE__ (words + dur), __THUMBS__ (list of image paths, optional thumbs.json in PROJECT_DIR)
motion blur (optional): GFX_SUBFRAMES=8 renders 8 moments per frame and averages them (fast moves look filmed, not stepped).
  GFX_SHUTTER=0.5 is the share of a frame the shutter is open (0.5 = film's 180-degree shutter). Default off (1 subframe)."""
import json,sys,os,io
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
SUB=int(os.environ.get('GFX_SUBFRAMES','1')); SHUTTER=float(os.environ.get('GFX_SHUTTER','0.5'))
TPL,P,style,out=sys.argv[1:5]; os.makedirs(out,exist_ok=True)
E=json.load(open(P+'/edl_f.json')); F=E['fps']; n=E['frames']
tl=dict(dur=n/F, words=json.load(open(P+'/words_cut.json')))
thumbs=json.dumps(['file://'+os.path.abspath(os.path.join(P,x)) for x in json.load(open(P+'/thumbs.json'))]) if os.path.exists(P+'/thumbs.json') else '[]'
built=os.path.join(os.path.dirname(os.path.abspath(TPL)),'_built.html')
open(built,'w').write(open(TPL).read().replace('__TIMELINE__',json.dumps(tl)).replace('__THUMBS__',thumbs).replace('__PROJECT__','file://'+os.path.abspath(P)))
times=[float(x) for x in sys.argv[5:]] or [i/F for i in range(n)]
holes={}
with sync_playwright() as p:
    b=p.chromium.launch(args=["--allow-file-access-from-files","--disable-web-security"]); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file://'+built+'?s='+style); pg.evaluate('window.ready'); pg.wait_for_timeout(500)
    for t in times:
        nm=f'{out}/{round(t*F):05d}.png' if len(sys.argv)<=5 else f'{out}/t{t:05.2f}.png'
        if SUB<=1:
            hl=pg.evaluate(f'render({t})'); pg.evaluate('Promise.all([...document.images].map(i=>i.decode().catch(()=>0)))')
            pg.screenshot(path=nm,omit_background=True)
        else:
            # motion blur: render SUB moments inside the frame's shutter and average them (premultiplied alpha)
            acc=None
            for k in range(SUB):
                ts=t+(k/SUB-0.5)*SHUTTER/F
                hl=pg.evaluate(f'render({max(0.0,ts)})'); pg.evaluate('Promise.all([...document.images].map(i=>i.decode().catch(()=>0)))')
                a=np.asarray(Image.open(io.BytesIO(pg.screenshot(omit_background=True))).convert('RGBA'),dtype=np.float32)
                a[...,:3]*=a[...,3:]/255.0; acc=a if acc is None else acc+a
            acc/=SUB; al=acc[...,3:]; acc[...,:3]=np.where(al>0,acc[...,:3]*255.0/np.maximum(al,1e-3),0)
            Image.fromarray(np.clip(acc,0,255).astype(np.uint8),'RGBA').save(nm)
        if hl: holes[round(t*F)]=hl
    b.close()
if len(sys.argv)<=5: json.dump(holes,open(f'{out}/holes.json','w'))
print('done',len(times),'frames;',len(holes),'window-hole frames')
