# Learnings log

Every Claude chat that edits a video or studies a creator adds a dated entry here (newest first), then folds anything durable into the right doc (`docs/look-and-sound.md`, `docs/style-bible.md`, `docs/ai-generation-stack.md`, `docs/formats/*`, `RUNBOOK.md`) or script. Keep entries short: what happened, what we learned, what changed.

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
