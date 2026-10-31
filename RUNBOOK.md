# RUNBOOK — how Claude edits one of Andrew's videos with this toolkit

Read this top to bottom before touching footage. Then read `docs/look-and-sound.md`, `docs/style-bible.md` and the format file in `docs/formats/` that fits the video.

## 0. Setup (fresh workspace)
```
bash setup.sh            # pip + models (GitHub releases) + fonts (npm) + three.js
mkdir -p projects/<name> && cd projects/<name>
```
Projects must live inside `projects/` (the 3D intro is served from the toolkit root).

## 1. Intake
- Probe: `ffprobe -v error -show_entries stream=width,height,r_frame_rate,color_transfer -of compact SOURCE`
  iPhone = usually 4K HLG HDR, 24 or 30 fps. `cut.py` detects and tone-maps HDR automatically.
- `python3 ../../scripts/transcribe.py SOURCE .` → `words.json` (word timestamps). The speech model misspells names
  (Barberto Nixon, Claud). Fix spellings against Andrew's script by hand before building captions.

## 2. Edit decisions → `edl.json`
Pick the best take of each line, drop flubs and dead air (target 0 pauses over 0.15 s for explainers).
`[{"label":"L1","src_in":3.44,"src_out":6.52}, ...]` in source seconds. Then:
`python3 ../../scripts/cut.py SOURCE .` → `cut_sdr.mov`, `edl_f.json` (frame-accurate), `words_cut.json` (words on the new timeline).
Correct `words_cut.json` spellings / punctuation; this drives captions, graphics timing and SFX timing.

## 3. Look
```
python3 ../../scripts/masks.py .      # person mask per frame (slow on 2 CPUs: ~3 s/frame; run in background)
python3 ../../scripts/grade.py .      # look.py on every frame → graded.mov
```
Tune `scripts/look.py` P values on 3 test frames first if the lighting differs a lot from the test video
(white-walled apartment, overhead light). Check skin RGB (aim R-G ≈ 35-45, G-B ≈ 12-20) and wall brightness.

## 4. Sound
```
python3 ../../scripts/denoise.py .        # DPDFNet 48 kHz → den48.wav
# write sound.json: bpm, busy sections (where drums play), breath (dip before the payoff), sfx events per style
python3 ../../scripts/sound.py . A        # voice.wav, music.wav, sfx_A.wav
bash ../../scripts/mix.sh . A 1           # → mix_A.wav at -14 LUFS (and `0` for the no-music version)
```
SFX names: whoosh(d,lo,hi) thump(g) paper(g) tick(f,g) key(g) swell(d) boom() shimmer() pop(). Times are seconds or a spoken word
("ROBERTO", "CUTS@10.5"). Keep them quiet and organic (gains 0.05-0.22). Claude cannot hear: verify with loudness + spectrum numbers.

## 5. Graphics
- Copy `templates/gfx_fullframe_example.html` to the project and rewrite the scene functions for this script. Reusable parts:
  captions (`capHTML`), letter write-on (`writeOn`), typed text, card slam + collage fan (scene1 A), thumbnail grid + scan line (scene1 B),
  creator card + cut timeline (`track`), app window → video reveal with a hole (scene3), CTA pill. Scene windows are `S1/S2/S3`.
- `render(t)` must be deterministic. Return a hole rect `[x,y,w,h,r]` when footage should show inside a window.
- Test 6-12 frames, composite over a graded frame, look at them, fix, then render all:
  `python3 ../../scripts/render_gfx.py gfx.html . A gfxA [t1 t2 ...]`
- Put any images the scenes need in the project (`thumbs/`, `thumbs.json`, `p_*.jpg`).

## 6. Optional: set-reveal intro (walls fall, crane back)
```
python3 ../../templates/set_reveal/prep.py . 3.08      # seconds of the intro shot
python3 ../../templates/set_reveal/render.py . 3.08 0 40 70   # test frames first, then without frame numbers
```
Edit `templates/set_reveal/intro.html` for the world that gets revealed (it should mean something for the topic), T1 (walls go) and T2 (end of camera move).
Add sfx: low whoosh at T1, two thumps when walls land, an airy swell that cuts dead on the next hard cut.

## 7. Composite and deliver
`zoom.json` = punch-ins on jump cuts: `[[start,end,zoom_from,zoom_to], ...]`.
```
python3 ../../scripts/composite.py . gfxA mix_A.wav out_A.mp4 [reveal/frames]
ffmpeg -i out_A.mp4 -i mix_A_nomusic.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest out_A_nomusic.mp4
```
Build a 12-frame contact sheet of the final and look at it before sending. Deliver the main version + no-music version.

## Measured targets to check against
Explainer: 25-45 cuts/min, median shot 1-2.5 s, first cut < 1 s, 0 pauses > 0.15 s, -14 LUFS, TP ≤ -1.5 dB.
