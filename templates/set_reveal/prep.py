"""Prepare the set-reveal intro: clean plate (person removed) + person cut-out frames.
usage: python3 prep.py PROJECT_DIR SECONDS   (SECONDS = length of the intro shot on the cut timeline)
writes PROJECT_DIR/reveal/plate.jpg and PROJECT_DIR/reveal/person/00000.png ..."""
import subprocess, numpy as np, cv2, os, sys, json
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,'..','..','scripts')); from look import grade
P=sys.argv[1]; FPS=json.load(open(P+'/edl_f.json'))['fps']; NF=int(round(float(sys.argv[2])*FPS))
W,H=1080,1920; M=np.load(P+'/masks.npy'); R=P+'/reveal'; os.makedirs(R+'/person',exist_ok=True)
def full_mask(i,ref):
    m=cv2.resize(M[i].astype(np.float32)/255,(W,H),interpolation=cv2.INTER_CUBIC)
    g=cv2.cvtColor((ref*255).astype(np.uint8),cv2.COLOR_RGB2GRAY)
    return cv2.ximgproc.guidedFilter(g,(np.clip(m,0,1)*255).astype(np.uint8),6,40).astype(np.float32)/255
# clean plate from first frame
dec=subprocess.Popen(['ffmpeg','-v','error','-i',P+'/cut_sdr.mov','-frames:v','1','-f','rawvideo','-pix_fmt','rgb48le','-'],stdout=subprocess.PIPE)
rgb=np.frombuffer(dec.stdout.read(W*H*6),np.uint16).reshape(H,W,3).astype(np.float32)/65535
# union of masks over the intro, so moving hands never leave a hole
U=np.max(M[:NF],axis=0); U=cv2.dilate((U>40).astype(np.uint8)*255,np.ones((25,25),np.uint8))
small=cv2.resize((rgb*255).astype(np.uint8),(540,960),interpolation=cv2.INTER_AREA)
inp=cv2.inpaint(small,U,12,cv2.INPAINT_TELEA)
inp=cv2.GaussianBlur(inp,(0,0),2)
big=cv2.resize(inp,(W,H),interpolation=cv2.INTER_CUBIC).astype(np.float32)/255
Uf=cv2.GaussianBlur(cv2.resize(U,(W,H)).astype(np.float32)/255,(0,0),6)[...,None]
plate=rgb*(1-Uf)+big*Uf
pg=grade(plate,np.zeros((H,W),np.float32))
cv2.imwrite(R+'/plate.jpg',cv2.cvtColor((pg*255).astype(np.uint8),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,95])
# andrew RGBA from graded + mask
dg=subprocess.Popen(['ffmpeg','-v','error','-i',P+'/graded.mov','-frames:v',str(NF),'-f','rawvideo','-pix_fmt','rgb48le','-'],stdout=subprocess.PIPE)
ds=subprocess.Popen(['ffmpeg','-v','error','-i',P+'/cut_sdr.mov','-frames:v',str(NF),'-f','rawvideo','-pix_fmt','rgb48le','-'],stdout=subprocess.PIPE)
for i in range(NF):
    g=np.frombuffer(dg.stdout.read(W*H*6),np.uint16).reshape(H,W,3).astype(np.float32)/65535
    s=np.frombuffer(ds.stdout.read(W*H*6),np.uint16).reshape(H,W,3).astype(np.float32)/65535
    m=full_mask(i,s); m=np.clip((m-0.08)/0.84,0,1)
    out=np.dstack([cv2.cvtColor((g*255).astype(np.uint8),cv2.COLOR_RGB2BGR),(m*255).astype(np.uint8)])
    cv2.imwrite(f'{R}/person/{i:05d}.png',out)
print('prep ok')
