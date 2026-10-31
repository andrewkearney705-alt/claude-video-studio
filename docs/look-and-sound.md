# Look, sound and full-frame animation (v3 learnings)

Learned from Andrew's feedback on v1/v2, from studying Peter McKinnon, Matt D'Avella and Johnny Harris on YouTube, and from three reels Andrew pointed to (rpn "Life with Claude" DdmBks7tKga, rpn "I've joined…" DdUFrgxOcOx, kaye.creatives set reveal Dem0m2cPIAg).

## 1. Color: start from correct pixels
- iPhone footage is usually **HDR (HLG, bt2020, 10-bit)**. Check with `ffprobe ... color_transfer`. If it says `arib-std-b67`, tone-map first or everything looks flat and washed out:
  `zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv`
- Cut segments one at a time from the 4K original (`-ss` per segment), never 14 trims in one filter graph (runs out of memory).
- Keep the source frame rate (iPhone cinematic = 24fps). Re-time word timestamps to the 24fps cut.

## 2. Color: the talking-head look (what the references have in common)
| Measured | McKinnon | D'Avella | Johnny Harris | Target for Andrew |
|---|---|---|---|---|
| Blacks (2nd pct, 0-255) | 4-12, crushed | 10-18, lifted | 1, crushed | ~8-10 |
| Saturation | varies 0.2-0.6 | 0.17-0.30, restrained | 0.5 warm | ~0.3 |
| Skin | warm | warm-neutral | very warm tungsten | warm-neutral, no magenta |
| Room vs subject | room darker | room darker, window key | room very dark, practical lamps | room ~0.75 stop under, cooler |

The single biggest move: **subject brighter than the room.** In a white-walled apartment, fake it:
1. Person mask per frame: `u2net_human_seg.onnx` (rembg GitHub release) through onnxruntime at 320px, refined with `cv2.ximgproc.guidedFilter` (radius 6) at full res, temporal smoothing 0.6/0.4. Raise mask to power ~1.8 before blending so there is no halo.
2. Background: -0.75 stop, saturation x0.6, tint toward cool grey (R .95, G .99, B 1.045).
3. Subject: -0.05 stop, sat x0.9, pull iPhone magenta out of skin (R x0.945, B x0.96).
4. Soft "key" gaussian centred on the face, vignette, top-down falloff (ceilings get darker, like real light).
5. Filmic curve: contrast 1.10 around 0.40, soft shoulder above 0.75, black 0.03, white 0.965. Teal shadows / warm highlights split tone, final sat 0.95. Light grain.
Code: `look.py` + `grade_all.py` in the v3 edit folder.

## 3. Sound
- iPhone voice in an empty room: low level, noise floor only ~20 dB under speech, dull above 1 kHz.
- **Denoise with DPDFNet 48 kHz** (`dpdfnet2_48khz_hr.onnx`, sherpa-onnx GitHub release `speech-enhancement-models`) via `sherpa_onnx.OfflineSpeechDenoiser`. It took the floor from -39 to -110 dB. Then blend 5% of the original back so pauses aren't dead silence.
- EQ toward a natural speech curve (check with Welch spectrum by octave). His voice fundamental sits at 95-125 Hz; keep it (warmth), cut below 95 Hz.
  Chain: `highpass 95 x2, lowshelf 130 -5, eq 200 -2, eq 700 -2, eq 3k +4, eq 6.2k +2, deesser, comp -24dB 3:1 fast, comp -14dB 2:1 slow, limiter`.
- Music: soft felt piano + low-passed pad + sub, kick/shaker only in the busy middle sections, a "breath" (duck) right before the payoff line, tape saturation + 7.5 kHz low-pass, hall reverb. Bed sits ~12 dB under voice and sidechain-ducks a few dB more.
- SFX must be organic and quiet: card/paper landings, soft UI ticks, key clicks for typing, short airy whooshes on scene cuts, one low boom on the payoff word. No bright chimes.
- Master: two-pass linear loudnorm, -14 LUFS, true peak -1.5 dBFS. Always export a no-music version too.

## 4. Full-frame animation scenes (instead of split-screen)
Roberto alternates **full-frame A-roll** with **full-frame animation scenes**; the split screen is one option, not the default.
- **Light desk (rpn "joined" reel):** off-white canvas with a soft vignette. Photo/tweet cards slam into the centre one after another, faster and faster (card lands at 115% → 100% in 3 frames, ±4° rotation, real drop shadow), then the stack fans into a collage around one small centred word. Tiny white mono captions. Hard cuts in and out.
- **Title write-on (rpn "Life with Claude"):** big serif title over the live shot, each letter blur → sharp and rising 18px with 40-60ms stagger. Ghost UI words drift at 20% opacity at the side.
- **Dark editorial:** near-black with a faint 90px grid; a 10x7 grid of thumbnails populates, a big serif counter counts up, then an accent scan line sweeps rows and greys out the "analysed" tiles.
- **Window reveal:** an app window types the prompt, ticks off steps, then its content becomes the actual video and the window grows to full frame — "the video you're watching now." The footage is composited into the hole in Python, so it scales with the window.

## 5. Set reveal (kaye.creatives intro)
What happens: 0-1.9s locked-off cosy room, words pop in near the head (sans + italic serif emphasis). At ~1.9s the walls fall away from the subject, hinged at the floor (back wall tips backward, sides drop outward). The camera does one continuous crane back + up (2.0-5.6s) until the set is a small platform in the middle of a night stadium. The topic is then painted huge on the ground.
How Claude builds it (Three.js rendered frame by frame in Playwright, SwiftShader WebGL):
1. Clean plate: inpaint the subject out of frame 1 (union of masks over the intro, dilated), grade it with the background grade.
2. Subject card: graded frames with the person mask as alpha, on a plane just in front of the wall.
3. The room plate is split into left / centre / right panels hinged at the frame bottom; panels topple back with an ease-in (gravity) and drop off the edge.
4. Camera starts at the exact original framing (card fills frame), then cranes back ~12 units and up ~5.6, tilting down.
5. The revealed world should mean something for the topic (for the editing video: an arena of screens playing the reels studied, light beams, glossy floor, the key line painted on the floor).
6. Sound: low whoosh as walls go, two low thuds when they land, an airy arena swell that cuts dead on the next hard cut.
Code: `v3/c/intro.html`, `prep_c.py`, `render_c.py`.
