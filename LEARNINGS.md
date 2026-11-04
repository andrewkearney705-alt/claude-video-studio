# Learnings log

Every Claude chat that edits a video or studies a creator adds a dated entry here (newest first), then folds anything durable into the right doc (`docs/look-and-sound.md`, `docs/style-bible.md`, `docs/ai-generation-stack.md`, `docs/formats/*`, `RUNBOOK.md`) or script. Keep entries short: what happened, what we learned, what changed.

## 2026-11-04: Brand V2 adopted (Pine, Oat & Electric)
- Andrew chose the brand in a design session: Satoshi bold sans + one Fraunces italic word + Geist Mono labels; palette Pine/Fern/Electric/Honey/Oat/Walnut on Cream (light) or Night (dark).
- Color rule: green = him, blue = the key idea once per piece (not "AI"), mono labels mark AI and tools. Replaces "one clay accent" and V1 "blue means AI".
- New `docs/knowledge/brand.md`; `my-flavor.md` and `pipeline.md` fonts updated; old "I don't code" brand line replaced with his throughline.

## 2026-11-03 — Curator: HLG number, text rule, caption house rules, pace pattern
- `look-and-sound.md` still said `npl=100` for HLG; now `npl=400` like `cut.py` (100 clipped skin).
- `founder-one-take.md`: Andrew rejected a pinned headline and series framing; Greg's pinned headline is now reference only and the kinetic key-word text is the current approach.
- `style-bible.md`: Jake's caption phrasing and safe-zone rules added as a house rule (Andrew asked to pull the best of his setup).
- `patterns.md`: "shorter, faster cut beats the long one" is Emerging (3 reels, 3 creators); the keyword-CTA line now notes the newest reels won on topic and pace, not the CTA. Six new Seen patterns.
- `RUNBOOK.md`: gzip + split for big renders. `reel-research.md`: browser-pane and handle notes.
- Not applied: `deadspace.py` and `stopmotion.py` (not in the repo, untested on footage), and the uncompressed-voice A/B (render both on the next edit and let Andrew choose by ear).

## 2026-11-02 (later) — Andrew's notes on the car-video text
- Andrew: on-screen text "not very engaging"; doesn't want a pinned headline that stays up, and doesn't want reels framed as a series (they're trial reels, tested against each other).
- Rebuilt with `templates/gfx_kinetic.html` (from liked vault positions: kaye word-by-word condensed caps + one italic serif word, rpn keyword promotion into a different display face every few seconds, gp__multimedia text behind the subject, colour carries meaning): a key word hard-cuts in on its syllable every 2-4 s (Bebas / Instrument Serif italic / Great Vibes / Unbounded 900), clay = the emotional word, lines auto-fit to 780 px, mono captions build word by word.
- `composite.py` gains `GFX_BACK=<dir>`: a layer composited under the person using masks.npy, so big words sit behind the head. Anchor the last line's glyph bottom ~1 head-height above the face (y ~700 for this framing) or the key word gets hidden.
- Awaiting Andrew's verdict on v2.

## 2026-11-02 — First car video (iPhone, daylight, parked): fixes found on real footage
- **HDR was too hot.** `cut.py` tone-mapped HLG with npl=100, which clipped skin to pink-white (Andrew: "way blown out"). Now npl=400 + mobius: skin and sky hold. Re-cut anything made before this.
- **Transcripts dropped words.** Fixed 20 s chunks lost most of any chunk that began mid-sentence. `transcribe.py` now splits on pauses with Silero VAD (`models/silero_vad.onnx`, added to `setup.sh`). Car music/handling noise is not speech: DPDFNet removes it, a quick way to tell.
- **Reframe from 4K:** `CROP="1.3,0.5,0.62" cut.py` crops before scaling (dashboard phone shots have too much roof). `composite.py` takes `ZOOM_CENTER` for punch-ins on the face.
- **Speed on 2 CPUs:** `MASK_STEP=3 masks.py` (model every 3rd frame, blended), `look.grade` uses 16-bit lookup tables (~4x faster, max diff 0.0007; `grade_ref` kept). Per-project grade overrides in `look.json` (daylight car: bg -0.45 stop, sat 0.82, near-neutral tint, magenta fix 0.015).
- `mix.sh` takes `MUSIC_DB` (used -8 for a one-take bed; -12 left the bed ~22 dB under the voice).
- New `templates/gfx_one_take.html`: pinned serif headline (strike/underline accent on a spoken word), series kicker, Space Mono phrase captions from explicit phrase lists, optional slate labels (blooper "TAKE 03") and an end line.
- Formats used: founder one-take split into a 3-part "On passion" series + a POV blooper reel (speed-ramped chaos, music hard-stops on the phone fall). Awaiting Andrew's notes.

## 2026-11-02 — Apple-style motion noted (reference)
- Added one reference line to `docs/motion/motion-playbook.md` (springs, no bounce unless flicked, glass panels, tight tracking on big type) from Andrew's Apple design skill request. Other open editing/sound signals were already in the kit from Nov 1 chat pushes.

## 2026-11-01 — Real SFX, motion principles, demo-film format, stereo bug fixed
- **Bug fixed in `sound.py`:** stereo files (music.wav, sfx_*.wav) were written de-interleaved (all left samples, then all right), so music and SFX played at double speed. Verified on a synthetic project: hits now land at the requested times in both channels. Re-render any earlier test mixes.
- **Real recorded SFX:** `sound.py` loads `SFX_DIR/<name>/*.wav` first (random take, ±3% pitch, ±1.5 dB) and only falls back to the synth with a warning. Source: withian.t DfLz2NMsgxz ("Why your Claude edits feel AI": synthesized sound, fake UI and linear motion are the tells). Andrew asked Claude to act on it.
- **Motion:** new `templates/motion.js` (spring ~5% overshoot / 0.5 s settle, anticipation, pop, stagger, follow-through, speed-based motion blur, hold), tested numerically. Rules in `look-and-sound.md` §4b.
- **New opt-in format** `formats/product-demo-film.md` from higgsfield.ai DZcy41GithZ (Andrew: add it to the toolkit). Audio decoded: one loud bed, ~21 onsets on clicks and card landings, drop-out at 29 s before the 30.5 s payoff.
- Reference only: realskytan DexJ-qWiWdY "ultimate storytelling caption" (Introduction, Struggle, Rise, Proof, Unique Mechanism, Expectations, Two-door CTA), filed to the Content Vault.

## 2026-11-01 — Motion graphics: Prompt Motion library + motion blur
- Andrew asked the editing/motion team to study everything in griffinwooldridge1's reel (DeLw2M6mx8n) on Prompt Motion, a gallery of Claude-made motion films with their prompts.
- Copied all 233 entries to `docs/motion/prompt-motion-catalog.json` (reference; prompts belong to their creators). Distilled `docs/motion/motion-playbook.md`: what the library shows, borrowed motion rules (HeyGen HyperFrames motion doctrine), the brief template, gotchas, entries to open first.
- Tooling: `render_gfx.py` gains optional motion blur (`GFX_SUBFRAMES=8`), tested on a fast-moving box. Off by default; nothing else changed.
- Also studied (signals filed): jun_yuh B-Roll Director (DfMB6cExd0Y), heystevetan OpenReply comment-to-DM (DbVq4mwz38L), rpn photos-to-3D dollhouse (DdHWQ3CJb6i).

## 2026-11-01 — Kit Curator, first run
- Brand decisions from the Brand OS folded into `knowledge/my-flavor.md`: day job is "a global insurance company" on Instagram (company topics LinkedIn-only), no banned topic categories, voice never cocky, handle settled. Same employer wording in `CLAUDE.md` and `CURATION.md`.
- Andrew's Content Vault picks added to `my-flavor.md`: 6 adopted options (dark warm set, one clay accent, desk-card alternation, serif write-on, set reveal, one-clip-many-versions) and a liked shortlist. Liked items stay opt-in; dense SFX conflicts with the calmer defaults, so nothing in `look-and-sound.md` changed.
- `knowledge/patterns.md`: 7 new Seen patterns from 5 breakdowns; comment-keyword CTA promoted to Emerging (3 reels, 3 creators).
- `reel-research.md`: Reel Scout's grid-render fix (screenshot before reading a profile's reels grid) and offline shortcode-to-date decode.
- `agents/`: first mirror of the 17 Brand OS playbooks.

## 2026-10-31 — rpn "Keiretsu" essay style added to the toolbelt (DdG9xwqNqxY)
- Andrew: "love this editing style, add to your toolbelt." Added as an opt-in format, `formats/curiosity-essay.md`; not a default.
- 83 s non-tech essay, 4:3 frame, daylight living-room set. Signature: ~1 s trailer-style title at 1.4 s (stencil accent word + kanji, B&W stock, viewfinder HUD, glitch hits), warm colour face vs near-mono B-roll (A-roll sat 0.34, B-roll 0.01-0.08), face holds 3-5 s then B-roll bursts at ~4/s, editorial collage B-roll (print pages, cut-outs, archival).
- 8.7K likes, 100 comments, 403 reposts; views and outlier score not readable (profile grid didn't load).
- Method: a 32x24 frame-difference pass at 0.25 s steps (threshold 28) gives a fast visual-change count over a whole reel in ~25 s.

## 2026-10-31 — Kit Curator set up (how the kit learns from now on)
- Added `CURATION.md` (taste rules: Adopted > Proven > Reference; quiet nights, edit in place, size caps), `CLAUDE.md` for every session, `inbox/` fallback, `agents/` playbook mirror and `scripts/curate_check.py`.
- Only the nightly Kit Curator rewrites rule docs; chats and Brand OS agents drop signals in the Brand OS `kitsignals` collection. Fixes the "push blocked, kit stops learning" problem.

## 2026-10-31 — Three reels studied (reference, nothing adopted yet)
- rhian_marie DceBlMMo3cw "6 months" (25 s, 71.3K likes, 2,930 reposts): 0-2.8 s supercut of other creators saying "6 months" (cut every ~0.5 s), one borrowed clip to 8 s, then her plain selfie pledge with one-word centre captions. Trend hook + personal pledge; reposts show people share it as their own commitment.
- cruz.juarezz DfGwbBIBtOp (27 s, 22.3K likes, 1,052 reposts, 23 comments): letterboxed widescreen strip in a vertical frame, dark warm tungsten, desk-at-night to gym, small serif subtitles, no talking to camera. Gets saves, not conversation.
- bryanbea_ DfKbiMQRmmb (47 s, new account, no proof yet): top-half graphics on grid paper (red label headlines, screenshot cards, italic serif accents, outlined "#3"), talking head bottom, ends on [FOLLOW ME]. Same family as the Kallaway/kaye split.
- Suggested combo for Andrew (not adopted): "6 months" supercut hook → his own specific pledge to camera → cinematic letterboxed montage of the real work → "follow along".

## 2026-10-31 — Sound effects in talking heads (abigaildaniellla DbJEDXOxgkC)
- Measured SFX from the decoded audio track for the first time (voice is mono, so added sounds show up in the stereo side channel). Method written up in `reel-research.md`.
- 13 hits in 33 s, all on cuts, card landings and text pops; none on plain spoken words; ~2/3 of cuts get one. Whooshes lead the picture cut by ~50 ms.
- One low boom right after the topic noun and one on the CTA keyword; music stops dead for ~1 s at the CTA, then comes back ~10 dB quieter.
- Bed never ducks; it just sits ~20 dB under the voice. Comment-keyword CTA pulled 4.1K comments on 9.6K likes.
- Changed: new §3b in `look-and-sound.md` (placement rules + how to apply in `sound.py`).

## 2026-10-31 — Mino Lee's AI editing rules (reference, not adopted)
- Studied Mino Lee's (@minolee.mp4) "15 AI editing rules" PDF. Filed in the Content Vault as one strategy among many; his numbers are an opt-in preset, not house rules.
- Andrew's direction: sources in the vault are reference. Only what Andrew explicitly adopts changes how videos are scripted or edited.
- Added `scripts/qa_check.py` as an optional measuring tool (dead air, caption chunks, safe zone).

## 2026-10-31 — Two reels studied: kaye.creatives split explainer + Kallaway creator teardown
- kaye.creatives DduIcDJI3vP (Opus 5.5 news, 21.4K likes): 4:3 face-left / card-right split, card every 1.5-2 s, AI self-inserts every 8-12 s. Added as a variant in `formats/ai-news-explainer.md`; Andrew's angle: show what you built, not the news.
- kallawaymarketing Dd8vo8IxamX (Nate Gaffney teardown via Claude + Sandcastles): 3 named patterns (Identity Labels, Series Familiarity, Demeanor Matching). Only 1,397 likes but 526 comments: teardowns are lead-gen more than reach.
- New format file `formats/creator-teardown.md`; style bible sections 7 (Kallaway) and 8 (kaye split) plus three cross-creator rules.

## 2026-10-30 — Part 1 (first test video, v1 → v3)
- v1 "a bit much"; v2 more refined; v3 approved direction: full-frame alternation, styles A light desk / B dark editorial / C set reveal.
- Root cause of the bad grade: iPhone HLG HDR never tone-mapped. Fixed in `cut.py`; subject/background grade in `look.py`.
- Sound: DPDFNet 48 kHz denoise, EQ toward natural speech curve, felt-piano bed, organic SFX, -14 LUFS.
- Studied: McKinnon / D'Avella / Johnny Harris (grade), rpn reels DdmBks7tKga + DdUFrgxOcOx, kaye.creatives (set reveal + collage explainer), higgsfield.ai one-camera multi-angle reel.
- Tool stack decided: Higgsfield Plus (connector) + ElevenLabs Creator; ~8-20 AI-shot videos/month on ~$81.
