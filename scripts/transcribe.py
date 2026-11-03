"""Word-level transcript of a clip.
usage: python3 transcribe.py SOURCE.mov PROJECT_DIR
writes PROJECT_DIR/src48.wav (48k mono, for the mix) and PROJECT_DIR/words.json  [{w, t0, t1}]

Splits the audio on speech pauses with Silero VAD (models/silero_vad.onnx) and decodes each speech
segment on its own. Fixed 20 s chunks dropped most words of any chunk that started mid-sentence
(car-video test, Nov 2026); VAD segments fix that. Falls back to 20 s chunks if the VAD model is missing."""
import sys, os, json, subprocess, wave, numpy as np, sherpa_onnx as so
SRC, P = sys.argv[1], sys.argv[2]; os.makedirs(P, exist_ok=True)
MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')
M = os.path.join(MD, 'sherpa-onnx-zipformer-en-2023-06-26')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-vn', '-ac', '1', '-ar', '48000', f'{P}/src48.wav'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-vn', '-ac', '1', '-ar', '16000', f'{P}/voice16.wav'], check=True)
rec = so.OfflineRecognizer.from_transducer(encoder=f'{M}/encoder-epoch-99-avg-1.onnx', decoder=f'{M}/decoder-epoch-99-avg-1.onnx',
                                           joiner=f'{M}/joiner-epoch-99-avg-1.onnx', tokens=f'{M}/tokens.txt', num_threads=2,
                                           decoding_method='modified_beam_search')
w = wave.open(f'{P}/voice16.wav'); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
SR = 16000

def segments():
    vm = os.path.join(MD, 'silero_vad.onnx')
    if not os.path.exists(vm):
        print('WARNING: no silero_vad.onnx, using fixed 20 s chunks (drops words)'); return [(o, min(o + 20 * SR, len(x))) for o in range(0, len(x), 20 * SR)]
    cfg = so.VadModelConfig(); cfg.silero_vad.model = vm; cfg.silero_vad.min_silence_duration = 0.25
    cfg.silero_vad.min_speech_duration = 0.2; cfg.silero_vad.max_speech_duration = 15; cfg.silero_vad.threshold = 0.4; cfg.sample_rate = SR
    vad = so.VoiceActivityDetector(cfg, buffer_size_in_seconds=600); out = []
    win = cfg.silero_vad.window_size
    for i in range(0, len(x), win):
        vad.accept_waveform(x[i:i + win])
        while not vad.empty(): out.append((vad.front.start, vad.front.start + len(vad.front.samples))); vad.pop()
    vad.flush()
    while not vad.empty(): out.append((vad.front.start, vad.front.start + len(vad.front.samples))); vad.pop()
    pad = int(0.15 * SR)  # a little context either side helps the first/last word
    return [(max(0, a - pad), min(len(x), b + pad)) for a, b in out]

words = []
for a, b in segments():
    s = rec.create_stream(); s.accept_waveform(SR, x[a:b]); rec.decode_stream(s)
    r = s.result; cur = None
    for tok, ts in zip(r.tokens, r.timestamps):
        t = ts + a / SR
        if tok.startswith(('▁', ' ')) or cur is None:
            if cur: words.append(cur)
            cur = dict(w=tok.replace('▁', '').strip(), t0=round(t, 3), t1=round(t + 0.12, 3))
        else:
            cur['w'] += tok; cur['t1'] = round(t + 0.12, 3)
    if cur: words.append(cur)
words = [w for w in words if w['w']]
words.sort(key=lambda w: w['t0'])
for i in range(len(words) - 1): words[i]['t1'] = min(max(words[i]['t1'], words[i]['t0'] + 0.05), words[i + 1]['t0'])
json.dump(words, open(f'{P}/words.json', 'w'), indent=0)
print(len(words), 'words ->', f'{P}/words.json'); print(' '.join(f"{w['t0']:.2f}:{w['w']}" for w in words))
