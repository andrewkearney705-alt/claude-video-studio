# Learnings log

Every Claude chat that edits a video or studies a creator adds a dated entry here (newest first), then folds anything durable into the right doc (`docs/look-and-sound.md`, `docs/style-bible.md`, `docs/ai-generation-stack.md`, `docs/formats/*`, `RUNBOOK.md`) or script. Keep entries short: what happened, what we learned, what changed.

## 2026-10-31 — Mino Lee's 15 AI editing rules (Content Academy PDF)
- Mino Lee (@minolee.mp4) edits with Claude and turns every note he gives into a numbered rule ("save that as a rule"). The loop matters more than the rules: watch as a viewer, name exactly what's off with a number, save it.
- Adopted: zero dead space (11 dB under speaking level, joins ≤ 20 ms), tone-based gaps (normal 0 / serious 6 frames / joke mid-word), 1-3 frame J-cuts, 2-3 word captions never ending on a weak word, safe zone + never cover the face, real receipts only, money in full, literal B-roll from own footage.
- Not adopted: his big centred captions and no-motion cards on full-frame scenes (Andrew's approved styles A/B/C keep their motion); his flat music levels (mix.sh ducking stays).
- New: `docs/editing-rules.md`, `scripts/qa_check.py` (audio dead space, caption chunks, Instagram safe zone), EDL `tone` field, feedback loop in RUNBOOK. Safe-zone numbers re-measured for Instagram, not TikTok.
- Business note: his funnel is free rules PDF -> free masterclass -> Claude captions skill as the reward. Same shape could work for this kit.

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
