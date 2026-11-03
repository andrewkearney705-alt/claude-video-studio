# Look, sound and full-frame animation (v3 learnings)

Learned from Andrew's feedback on v1/v2, from studying Peter McKinnon, Matt D'Avella and Johnny Harris on YouTube, and from three reels Andrew pointed to (rpn "Life with Claude" DdmBks7tKga, rpn "I've joined…" DdUFrgxOcOx, kaye.creatives set reveal Dem0m2cPIAg).

## 1. Color: start from correct pixels
- iPhone footage is usually **HDR (HLG, bt2020, 10-bit)**. Check with `ffprobe ... color_transfer`. If it says `arib-std-b67`, tone-map first or everything looks flat and washed out:
  `zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=400,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv`
  Use `npl=400`, not 100: at 100 skin clipped to pink-white on a daylight car clip ("way blown out"). [Andrew's feedback + 5-variant frame test, Nov 2026]
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

### 3b. Where SFX go in a talking head (measured: abigaildaniellla DbJEDXOxgkC, 9.6K likes / 4.1K comments)
Measured from the decoded audio track, not by ear: her voice is mono, so every hit shows up as a jump in the stereo side channel.
- **SFX mark changes of picture, not words.** 13 hits in 33 s (~24/min). Every one sits on a hard cut, a title card landing or a word of on-screen text popping in. None sit on ordinary spoken words. Busy sections (b-roll montage, list cards) get them; plain A-roll gets none.
- **Not every cut gets one.** ~18 cuts, ~2/3 got a sound. Back-to-back cuts in a montage get one whoosh for the run, not one each.
- **Sound leads picture by 1-2 frames.** Whooshes peak ~50 ms before the cut (3.85 vs 3.90 s, 23.90 vs 24.0, 25.35 vs 25.40). Place `sfx` events 2 frames early.
- **One low boom per idea, right after the key noun.** A sub hit lands ~0.25 s after she says the topic word ("sound", 21.55 s) and again on the CTA keyword (28.45 s).
- **Silence is the loudest effect.** At the cut back to camera for the CTA (26.9 s) the music stops dead ~0.3 s later and she talks totally dry for ~1 s; then the boom hits on the keyword and a much quieter bed returns (~10 dB lower) under the ask.
- **Bed doesn't duck.** Music sat at one steady level ~20 dB under the voice the whole time, with no movement in pauses. Keeping it that low is what makes un-ducked music work; our sidechain ducking stays, but the starting level can go lower.
- Hook (0-3.5 s) has no placed hits, just the bed and voice: the hook is carried by word-by-word captions with the key words in yellow.
- Hot master: peaks at 0.0 dBFS, about -16 dB RMS. Don't copy that; -14 LUFS / -1.5 dBTP stays.
How to apply in `sound.py`: one `whoosh` per cut-run at cut time minus 0.08 s, `pop`/`tick` per text-card word, one `boom` after the topic noun and one on the CTA keyword, and a hard music stop (cut `music.wav` to zero) at the start of the CTA section.

### 3c. Real recorded SFX, not synthesized (Nov 2026)
- Viewers can hear synthesized whooshes and pops as "AI-made" (withian.t DfLz2NMsgxz; his fix: give Claude a library of real sounds and let it choose). `sound.py` now loads real recordings first: `SFX_DIR/<name>/*.wav`, a different take per hit with ±3% pitch and ±1.5 dB gain; the old synth is a fallback that prints a warning.
- Name folders by feel, not mechanism: `airy-whoosh`, `soft-impact`, `glass-pop`, `paper-land`, `ui-tick`, `key-click`, `low-boom`, `riser`. 3-6 takes each. Library lives outside git (`~/claude-video-studio-sfx`).

## 4. Full-frame animation scenes (instead of split-screen)
Roberto alternates **full-frame A-roll** with **full-frame animation scenes**; the split screen is one option, not the default.
- **Light desk (rpn "joined" reel):** off-white canvas with a soft vignette. Photo/tweet cards slam into the centre one after another, faster and faster (card lands at 115% → 100% in 3 frames, ±4° rotation, real drop shadow), then the stack fans into a collage around one small centred word. Tiny white mono captions. Hard cuts in and out.
- **Title write-on (rpn "Life with Claude"):** big serif title over the live shot, each letter blur → sharp and rising 18px with 40-60ms stagger. Ghost UI words drift at 20% opacity at the side.
- **Dark editorial:** near-black with a faint 90px grid; a 10x7 grid of thumbnails populates, a big serif counter counts up, then an accent scan line sweeps rows and greys out the "analysed" tiles.
- **Window reveal:** an app window types the prompt, ticks off steps, then its content becomes the actual video and the window grows to full frame — "the video you're watching now." The footage is composited into the hole in Python, so it scales with the window.

### 4b. Motion that doesn't feel AI-made (Nov 2026)
- Never linear for anything that moves. Arrivals spring (`templates/motion.js`: `spring`, ~5% overshoot, settles in ~0.5 s); exits ease in; camera moves ease in-out.
- Anticipation before big moves (`anticipate`), staggered follow-through for groups (`follow`, 20-60 ms per item), motion blur only while fast (`blurFromSpeed`), and a hold so each element rests long enough to read.
- Show real interfaces, not drawn mock-ups: record the actual app (screen recording, or Claude driving OBS through an MCP server) and animate punch-ins on the real cursor clicks. Generic fake UI is another tell.
- Claude executes; Andrew sets the creative direction for every animation scene.
- Deeper reference: `docs/motion/motion-playbook.md` (Prompt Motion library); frame-level motion blur in `render_gfx.py` (`GFX_SUBFRAMES=8`) pairs with `blurFromSpeed` for per-element blur.

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
