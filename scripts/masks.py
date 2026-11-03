"""Person masks for every frame.  usage: python3 masks.py PROJECT_DIR  -> masks.npy (540x960 uint8)
MASK_STEP=3 runs the model on every 3rd frame and blends between them (each frame still gets its own guided-filter edge).
Use it for locked-off talking heads on a 2-CPU box: ~3x faster, edges still follow the frame."""
import subprocess, numpy as np, cv2, onnxruntime as ort, sys, os
P=sys.argv[1]; MD=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','models')
W,H=1080,1920
so=ort.SessionOptions(); so.intra_op_num_threads=os.cpu_count() or 2
sess=ort.InferenceSession(MD+'/human.onnx',so,providers=['CPUExecutionProvider']); iname=sess.get_inputs()[0].name
MEAN=np.array([0.485,0.456,0.406],np.float32); STD=np.array([0.229,0.224,0.225],np.float32)
dec=subprocess.Popen(['ffmpeg','-v','error','-i',P+'/cut_sdr.mov','-vf','scale=540:960','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
M=[];prev=None;STEP=int(os.environ.get('MASK_STEP','1'));frames=[]
while True:
    b=dec.stdout.read(540*960*3)
    if len(b)<540*960*3: break
    frames.append(np.frombuffer(b,np.uint8).reshape(960,540,3))
def infer(rgb):
    x=cv2.resize(rgb,(320,320),interpolation=cv2.INTER_AREA).astype(np.float32)/255
    x=(x/max(x.max(),1e-6)-MEAN)/STD
    m=sess.run(None,{iname:x.transpose(2,0,1)[None]})[0][0,0]; m=(m-m.min())/(m.max()-m.min()+1e-6)
    return cv2.resize(m,(540,960),interpolation=cv2.INTER_CUBIC)
keys=list(range(0,len(frames),STEP));
if keys[-1]!=len(frames)-1: keys.append(len(frames)-1)
K={k:infer(frames[k]) for k in keys}; print('model frames',len(K),flush=True)
for i,rgb in enumerate(frames):
    a=max(k for k in keys if k<=i); b2=min(k for k in keys if k>=i); w=0 if b2==a else (i-a)/(b2-a)
    m=K[a]*(1-w)+K[b2]*w
    g=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
    m=cv2.ximgproc.guidedFilter(g,(np.clip(m,0,1)*255).astype(np.uint8),8,60).astype(np.float32)/255
    m=m if prev is None else 0.6*m+0.4*prev; prev=m
    M.append((np.clip(m,0,1)*255).astype(np.uint8))
np.save(P+'/masks.npy',np.stack(M)); print('done',len(M))
