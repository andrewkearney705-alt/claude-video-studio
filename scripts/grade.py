"""Apply look.py to the whole cut. usage: python3 grade.py PROJECT_DIR [FPS] -> graded.mov"""
import subprocess, numpy as np, cv2, sys, json
from look import grade, P as LOOK
import os
P=sys.argv[1]; FPS=str(json.load(open(P+'/edl_f.json'))['fps'])
W,H=1080,1920
M=np.load(P+'/masks.npy')
# per-project look overrides (e.g. daylight car: lighter, less cool room) in PROJECT_DIR/look.json
LP=dict(LOOK); LP.update(json.load(open(P+'/look.json')) if os.path.exists(P+'/look.json') else {})
dec=subprocess.Popen(['ffmpeg','-v','error','-i',P+'/cut_sdr.mov','-f','rawvideo','-pix_fmt','rgb48le','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb48le','-s',f'{W}x{H}','-r',FPS,'-i','-','-c:v','prores_ks','-profile:v','3','-pix_fmt','yuv444p10le',P+'/graded.mov'],stdin=subprocess.PIPE)
i=0
while True:
    b=dec.stdout.read(W*H*6)
    if len(b)<W*H*6: break
    rgb=np.frombuffer(b,np.uint16).reshape(H,W,3).astype(np.float32)/65535
    m=cv2.resize(M[min(i,len(M)-1)].astype(np.float32)/255,(W,H),interpolation=cv2.INTER_CUBIC)
    g=cv2.cvtColor((rgb*255).astype(np.uint8),cv2.COLOR_RGB2GRAY)
    m=cv2.ximgproc.guidedFilter(g,(np.clip(m,0,1)*255).astype(np.uint8),6,40).astype(np.float32)/255
    enc.stdin.write((grade(rgb,m,LP)*65535).astype(np.uint16).tobytes()); i+=1
    if i%100==0: print(i,flush=True)
enc.stdin.close(); enc.wait(); print('graded',i)
