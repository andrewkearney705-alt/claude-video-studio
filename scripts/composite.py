"""Final picture: graded footage + punch-ins + graphics layer + window-hole inserts + grain, muxed with the mix.
usage: python3 composite.py PROJECT_DIR GFX_DIR MIX.wav OUT.mp4 [INTRO_FRAMES_DIR]
PROJECT_DIR/zoom.json (optional): [[start,end,zoom_from,zoom_to], ...] seconds on the cut timeline"""
import sys, json, subprocess, numpy as np, cv2, os
P=sys.argv[1]; GD=sys.argv[2]; AUD=sys.argv[3]; OUT=sys.argv[4]; INTRO=sys.argv[5] if len(sys.argv)>5 else None
W,H=1080,1920; F=json.load(open(P+'/edl_f.json'))['fps']
ZP=json.load(open(P+'/zoom.json')) if os.path.exists(P+'/zoom.json') else []
holes={int(k):v for k,v in (json.load(open(f'{GD}/holes.json')) if os.path.exists(f'{GD}/holes.json') else {}).items()}
def Z(t):
    for a,b,z0,z1 in ZP:
        if a<=t<b: return z0+(z1-z0)*(t-a)/(b-a)
    return 1.0
ZC=[float(v) for v in os.environ.get('ZOOM_CENTER','0.52,0.46').split(',')]  # punch-in centre (face position), e.g. ZOOM_CENTER=0.5,0.55
def zoom(img,z,cx=ZC[0],cy=ZC[1]):
    if z<=1.0001: return img
    w,h=W/z,H/z; x0=np.clip(cx*W-w/2,0,W-w); y0=np.clip(cy*H-h/2,0,H-h)
    M=np.float32([[z,0,-x0*z],[0,z,-y0*z]]); return cv2.warpAffine(img,M,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
def rmask(w,h,r):
    m=np.zeros((h,w),np.float32); r=int(r)
    cv2.rectangle(m,(r,0),(w-r,h),1,-1); cv2.rectangle(m,(0,r),(w,h-r),1,-1)
    for cx,cy in ((r,r),(w-r-1,r),(r,h-r-1),(w-r-1,h-r-1)): cv2.circle(m,(cx,cy),r,1,-1,lineType=cv2.LINE_AA)
    return m
rng=np.random.default_rng(1)
# optional text-behind-subject layer: GFX_BACK=<dir of PNGs>; the person (masks.npy) is laid back over it
BACK=os.environ.get('GFX_BACK'); MK=np.load(P+'/masks.npy',mmap_mode='r') if BACK else None
dec=subprocess.Popen(['ffmpeg','-v','error','-i',P+'/graded.mov','-f','rawvideo','-pix_fmt','rgb48le','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb48le','-s',f'{W}x{H}','-r',str(F),'-i','-','-i',AUD,
   '-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
   '-c:a','aac','-b:a','256k','-shortest','-movflags','+faststart',OUT],stdin=subprocess.PIPE)
i=0
while True:
    b=dec.stdout.read(W*H*6)
    if len(b)<W*H*6: break
    t=i/F
    fr=np.frombuffer(b,np.uint16).reshape(H,W,3).astype(np.float32)/65535
    if INTRO and os.path.exists(f'{INTRO}/{i:05d}.png'):
        fr=cv2.cvtColor(cv2.imread(f'{INTRO}/{i:05d}.png'),cv2.COLOR_BGR2RGB).astype(np.float32)/255
    else:
        if BACK and os.path.exists(f'{BACK}/{i:05d}.png'):
            gb=cv2.imread(f'{BACK}/{i:05d}.png',cv2.IMREAD_UNCHANGED).astype(np.float32)/255
            if gb[...,3].max()>0:
                m=cv2.resize(MK[min(i,len(MK)-1)].astype(np.float32)/255,(W,H),interpolation=cv2.INTER_CUBIC)
                gy=cv2.cvtColor((np.clip(fr,0,1)*255).astype(np.uint8),cv2.COLOR_RGB2GRAY)
                m=cv2.ximgproc.guidedFilter(gy,(np.clip(m,0,1)*255).astype(np.uint8),4,30).astype(np.float32)/255
                m=np.clip((m-0.3)/0.5,0,1)[...,None]
                ab=gb[...,3:4]; cb=cv2.cvtColor(gb[...,:3],cv2.COLOR_BGR2RGB)
                fr=(fr*(1-ab)+cb*ab)*(1-m)+fr*m
        fr=zoom(fr,Z(t))
    g=cv2.imread(f'{GD}/{i:05d}.png',cv2.IMREAD_UNCHANGED)
    g=g.astype(np.float32)/255
    if g.shape[2]==3: g=np.dstack([g,np.ones((H,W),np.float32)])
    col=cv2.cvtColor(g[...,:3],cv2.COLOR_BGR2RGB); a=g[...,3:4]
    if i in holes:
        x,y,w,h,r=holes[i]; x,y,w,h=int(round(x)),int(round(y)),int(round(w)),int(round(h))
        x0,y0=max(0,x),max(0,y); x1,y1=min(W,x+w),min(H,y+h)
        s=max(w/W,h/H); ins=cv2.resize(fr,(int(W*s+1),int(H*s+1)),interpolation=cv2.INTER_AREA)
        ox=(ins.shape[1]-w)//2; oy=(ins.shape[0]-h)//2; ins=ins[oy:oy+h,ox:ox+w]
        base=np.zeros_like(fr); mk=rmask(w,h,max(r,1))[...,None]
        base[y0:y1,x0:x1]=(ins*mk)[y0-y:y1-y,x0-x:x1-x]
        fr=base
    o=fr*(1-a)+col*a
    n=rng.standard_normal((H//2,W//2)).astype(np.float32); n=cv2.resize(n,(W,H),interpolation=cv2.INTER_LINEAR)*0.010
    o=np.clip(o+n[...,None],0,1)
    enc.stdin.write((o*65535).astype(np.uint16).tobytes()); i+=1
enc.stdin.close(); enc.wait(); print('done',i,OUT)
