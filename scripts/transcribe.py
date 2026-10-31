"""Word-level transcript of a clip.
usage: python3 transcribe.py SOURCE.mov PROJECT_DIR
writes PROJECT_DIR/src48.wav (48k mono, for the mix) and PROJECT_DIR/words.json  [{w, t0, t1}]"""
import sys, os, json, subprocess, wave, numpy as np, sherpa_onnx as so
SRC, P = sys.argv[1], sys.argv[2]; os.makedirs(P, exist_ok=True)
M = os.path.join(os.path.dirname(__file__), '..', 'models', 'sherpa-onnx-zipformer-en-2023-06-26')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-vn', '-ac', '1', '-ar', '48000', f'{P}/src48.wav'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-vn', '-ac', '1', '-ar', '16000', f'{P}/voice16.wav'], check=True)
rec = so.OfflineRecognizer.from_transducer(encoder=f'{M}/encoder-epoch-99-avg-1.int8.onnx', decoder=f'{M}/decoder-epoch-99-avg-1.onnx',
                                           joiner=f'{M}/joiner-epoch-99-avg-1.int8.onnx', tokens=f'{M}/tokens.txt', num_threads=2, decoding_method='greedy_search')
w = wave.open(f'{P}/voice16.wav'); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
words = []; CH = 16000 * 20  # 20 s chunks, overlap-free (cut on quiet points is better for long clips)
for off in range(0, len(x), CH):
    s = rec.create_stream(); s.accept_waveform(16000, x[off:off + CH]); rec.decode_stream(s)
    r = s.result; cur = None
    for tok, ts in zip(r.tokens, r.timestamps):
        t = ts + off / 16000
        if tok.startswith(('▁', ' ')) or cur is None:
            if cur: words.append(cur)
            cur = dict(w=tok.replace('▁', '').strip(), t0=round(t, 3), t1=round(t + 0.12, 3))
        else:
            cur['w'] += tok; cur['t1'] = round(t + 0.12, 3)
    if cur: words.append(cur)
for i in range(len(words) - 1): words[i]['t1'] = min(words[i]['t1'], words[i + 1]['t0'])
json.dump(words, open(f'{P}/words.json', 'w'), indent=0)
print(len(words), 'words ->', f'{P}/words.json'); print(' '.join(f"{w['t0']:.2f}:{w['w']}" for w in words))
