# Production pipeline (shared by all five content skills)

How Claude turns Andrew's raw clips into a finished vertical video. Use in this order.

## 1. Intake
- Andrew uploads clips here, or points to a folder on his Mac (device bridge).
- Probe everything: `ffprobe -v error -show_entries stream=width,height,r_frame_rate,duration -of csv=p=0 FILE`
- Transcribe with word timestamps: `pip install faster-whisper --break-system-packages`, model `small.en`, `word_timestamps=True`. Save `transcript.json`.

## 2. Assemble the talking track
- Pick the best take per script line (Andrew reads each line 2–3 times).
- Remove dead air: `ffmpeg -i in.wav -af silencedetect=noise=-30dB:d=0.18 -f null -` then cut every gap longer than ~0.15s (target: 0 pauses over 0.15s for explainers; that is what Roberto and Ray measure at).
- Overlap the start of each line 2–4 frames into the end of the previous one so there is no breath gap.

## 3. Build the frame (1080x1920, 30fps)
- Full frame: `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920`
- Split-screen (Roberto): B-roll scaled to 1080x960 on top, talking head 1080x960 below; captions sit on the seam.
- Stacked podcast hook (DOAC): host top half, guest bottom half, question box centered on the seam.
- Letterbox (Roberto cinematic / tweet-header): 16:9 picture centered on black, header text in the top bar.
- Slow push-in on talking head: `zoompan=z='min(1+0.0008*on,1.06)':d=1:s=1080x1920:fps=30`
- Punch-in on emphasis words: hard cut to the same shot at 112–118% scale.

## 4. Captions and titles (ASS subtitles, burned in)
- One Dialogue event per word (or 2–3 words), timed from `transcript.json`.
- Pop-in: `{\fscx112\fscy112\t(0,90,\fscx100\fscy100)}`
- Burn in: `-vf "ass=captions.ass"` (libass is installed).
- Fonts (Brand V2, see `knowledge/brand.md`): Satoshi Bold for captions (sentence case, 3–4 word chunks), Satoshi Black for hooks, Fraunces Italic for the one accent word, Geist Mono for AI/tool labels; a marker/handwritten face (e.g. Permanent Marker, Caveat Brush) for Greg-style quote overlays.

## 5. Sound (full detail in look-and-sound.md)
- Denoise first with DPDFNet 48 kHz (sherpa-onnx), blend 5% original back.
- Voice chain: `highpass=f=95,highpass=f=95,lowshelf=f=130:g=-5,equalizer=f=200:t=q:w=1:g=-2,equalizer=f=700:t=q:w=1.2:g=-2,equalizer=f=3000:t=q:w=1.1:g=4,equalizer=f=6200:t=q:w=1:g=2,deesser=i=0.35:f=0.55,acompressor=threshold=-24dB:ratio=3:attack=4:release=60:knee=4:makeup=6dB,acompressor=threshold=-14dB:ratio=2:attack=25:release=250:makeup=2dB,alimiter=limit=0.89:level=false`
- Music bed under voice the whole time (none of the high performers drop to silence), ducked with `sidechaincompress`.
- SFX: whoosh/hit on cuts, tick on caption words, riser into the hook, ding on the payoff.
- Master: two-pass linear `loudnorm=I=-14:TP=-1.5:LRA=9`

## 6. Color (full detail in look-and-sound.md)
- FIRST check for iPhone HDR (`color_transfer=arib-std-b67`) and tone-map to bt709 SDR, or the grade will look flat and washed out.
- Then subject/background separation: person mask per frame, room ~0.75 stop down and cooler, skin warm-neutral with magenta pulled out, soft face key, filmic curve, light grain.

## 7. Render and deliver
- `-c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart`
- Always also export: a voice-only version (for adding trending audio in-app), the .srt, and an FCP7 XML so Andrew can open the timeline in Premiere Pro.
- Watch the full render before sending; send a rough cut early.

## 8. Measure against the benchmark
Run the same checks Claude used on 70+ reference reels (cuts per minute, median shot length, pauses over 0.15s, first-cut time) and compare with the target numbers in the skill being used. Flag anything off-target to Andrew in one line.

## 9. Effects library (plus full-frame scenes and the set reveal in look-and-sound.md) (how Claude recreates each signature move)
| Move (who) | How |
|---|---|
| Word-timed hard-cut captions (all) | One ASS Dialogue per word from Whisper timestamps; no \fad, no \t scaling |
| Mono seam captions (rpn) | ASS style: Space Mono Bold, size ~3% of height, all caps, \fsp3 letter-spacing, positioned at the split line (y=960) |
| Keyword promotion (rpn) | Same event list, but the keyword gets its own style (Instrument Serif / Great Vibes / Bebas Neue), 3–4x larger; stacked words each start on their own spoken time |
| Smear slide-in title (rpn) | ASS `\move(-300,y,540,y,0,120)` plus `\blur8` on the first 3 frames, `\blur0` after (`\t(80,120,\blur0)`); mirror for the exit |
| App-icon stickers (rpn) | PNG logos overlaid with ffmpeg `overlay=enable='gte(t,T)'`, staggered 0.1s apart; 1-frame 120% scale then 100% |
| Hand-drawn arrow (rpn, DOAC) | Pre-drawn transparent PNG arrow, hard-cut on |
| Contestant card / scoreboard (rpn) | Built as HTML, rendered to PNG with Playwright, overlaid; re-render per score update |
| Pill label (rpn) | ASS BorderStyle=3 with translucent grey BackColour, or a Pillow-rendered rounded PNG |
| CRT / glitch screen (rpn) | Track the prop screen corners once, `perspective` + `overlay` the content; add `noise=alls=40:allf=t` for static, `rgbashift` for glitch |
| Word-slam over face cuts (rpn essay) | One word per 0.4–0.5s shot, Unbounded Black, centre, hard cuts on beats |
| Pinned lowercase headline (Greg) | One ASS event lasting the whole video, Inter SemiBold, lowercase, top-centre, no box, soft shadow |
| 85% opacity words (Greg montage) | ASS primary colour alpha `&H26FFFFFF` |
| Negative flash open (Greg) | `negate` with `enable='lt(t,0.25)'` |
| Whip blur (Greg, rpn) | 2–3 frames of `gblur=sigma=40:sigmaV=0` at the cut point |
| Text behind subject (Greg) | `pip install rembg --break-system-packages`, cut the person out per frame, stack: background → text → person |
| Question box (DOAC) | Pillow-rendered white rounded rect (radius ~18px) with black Archivo Black caps, overlaid 0–4.5s on the seam |
| Show badge (DOAC) | Small PNG, top-left, whole video |
| Green money highlight (Chida) | ASS override `{\c&H76E600&}` on number tokens |
| Gold keywords (Rui Fu) | `{\c&H3CC8F0&}` (gold) on keywords in a Playfair Display headline |
| Timestamp labels (Chase) | Two-line ASS event per scene: time line + action line, small, centre |
