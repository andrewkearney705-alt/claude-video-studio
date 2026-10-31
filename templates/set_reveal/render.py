"""Render the 3D set-reveal intro (Three.js in headless Chromium, frame by frame).
usage: python3 render.py PROJECT_DIR SECONDS [test frame numbers...]
reads PROJECT_DIR/reveal/plate.jpg, reveal/person/*.png, thumbs.json (images for the revealed world); writes reveal/frames/*.png
Edit intro.html to change the world that gets revealed, wall timing (T1) and the camera move (T2, crane distance)."""
import json, os, sys, subprocess, time
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); P=os.path.abspath(sys.argv[1]); FPS=json.load(open(P+'/edl_f.json'))['fps']
NF=int(round(float(sys.argv[2])*FPS)); only=[int(x) for x in sys.argv[3:]]
ROOT=os.path.abspath(os.path.join(HERE,'..','..'))       # toolkit root is served; project must be inside it (projects/<name>)
rel=lambda p: '/'+os.path.relpath(p,ROOT)
th=json.load(open(P+'/thumbs.json')) if os.path.exists(P+'/thumbs.json') else []
th=[rel(os.path.join(P,x)) if not x.startswith('/') else rel(x) for x in th]
html=open(HERE+'/intro.html').read().replace('__NF__',str(NF)).replace('__THUMBS__',json.dumps(th))
html=html.replace("load('plate.jpg')",f"load('{rel(P)}/reveal/plate.jpg')").replace("load('andrew/'",f"load('{rel(P)}/reveal/person/'")
open(HERE+'/_built.html','w').write(html)
srv=subprocess.Popen(['python3','-m','http.server','8765','--directory',ROOT],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
os.makedirs(P+'/reveal/frames',exist_ok=True)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=b.new_page(viewport={'width':1080,'height':1920}); pg.on('pageerror',lambda e:print('ERR',e))
        pg.goto('http://localhost:8765'+rel(HERE)+'/_built.html'); pg.wait_for_function('window.ready!==undefined',timeout=120000); pg.evaluate('window.ready')
        for i in (only or range(NF)):
            pg.evaluate(f'render({i/FPS},{i})'); pg.locator('canvas').screenshot(path=f'{P}/reveal/frames/{i:05d}.png')
        b.close()
finally: srv.terminate()
print('rendered',len(only or range(NF)),'frames')
