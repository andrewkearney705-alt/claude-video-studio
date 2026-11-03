#!/usr/bin/env bash
# One-time setup in a fresh Claude workspace (or any Linux/Mac with python3, ffmpeg, node).
# Everything downloads from PyPI, npm or GitHub releases (HuggingFace is often blocked in Claude's sandbox).
set -e
cd "$(dirname "$0")"
pip install --break-system-packages -q onnxruntime sherpa-onnx opencv-contrib-python-headless scipy numpy pillow playwright 2>/dev/null || \
pip install -q onnxruntime sherpa-onnx opencv-contrib-python-headless scipy numpy pillow playwright
mkdir -p models fonts
cd models
# person segmentation (for the subject/background grade and cut-outs)
[ -f human.onnx ] || curl -sSL -o human.onnx https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx
# full-band 48 kHz speech denoiser
[ -f dpdfnet2_48khz_hr.onnx ] || curl -sSL -O https://github.com/k2-fsa/sherpa-onnx/releases/download/speech-enhancement-models/dpdfnet2_48khz_hr.onnx
# voice activity detection (transcribe.py splits on pauses with it)
[ -f silero_vad.onnx ] || curl -sSL -O https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx
# English speech-to-text with word timestamps
if [ ! -d sherpa-onnx-zipformer-en-2023-06-26 ]; then
  curl -sSL -o zf.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-zipformer-en-2023-06-26.tar.bz2
  tar xjf zf.tar.bz2 && rm zf.tar.bz2
fi
cd ../fonts
for f in space-mono instrument-serif inter unbounded bebas-neue great-vibes jetbrains-mono; do
  [ -d fontsource-$f ] || { npm pack -s @fontsource/$f >/dev/null && mkdir -p fontsource-$f && tar xzf fontsource-$f-*.tgz -C fontsource-$f --strip-components=1 && rm fontsource-$f-*.tgz; }
done
cd ../templates/set_reveal && [ -d node_modules/three ] || npm install -s three@0.169.0
echo "setup done"
