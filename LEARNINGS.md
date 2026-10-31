# Learnings log

Every Claude chat that edits a video or studies a creator adds a dated entry here (newest first), then folds anything durable into the right doc (`docs/look-and-sound.md`, `docs/style-bible.md`, `docs/ai-generation-stack.md`, `docs/formats/*`, `RUNBOOK.md`) or script. Keep entries short: what happened, what we learned, what changed.

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
