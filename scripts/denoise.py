"""Studio-clean voice: DPDFNet 48 kHz denoise.  usage: python3 denoise.py PROJECT_DIR  (reads src48.wav, writes den48.wav)"""
import sys, os, wave, numpy as np, sherpa_onnx as so
P=sys.argv[1]; MD=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','models')
w=wave.open(f'{P}/src48.wav'); x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
g=0.5/max(np.abs(x).max(),1e-4)            # normalise input peak to -6 dB
cfg=so.OfflineSpeechDenoiserModelConfig(dpdfnet=so.OfflineSpeechDenoiserDpdfNetModelConfig(model=f'{MD}/dpdfnet2_48khz_hr.onnx'),num_threads=os.cpu_count() or 2)
y=np.array(so.OfflineSpeechDenoiser(so.OfflineSpeechDenoiserConfig(model=cfg))(x*g,48000).samples)
o=wave.open(f'{P}/den48.wav','w'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(48000); o.writeframes((np.clip(y,-1,1)*32767).astype(np.int16).tobytes()); o.close()
open(f'{P}/den_gain.txt','w').write(str(g)); print('denoised, input gain',round(g,2))
