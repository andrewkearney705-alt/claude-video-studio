# Learnings log

Every Claude chat that edits a video or studies a creator adds a dated entry here (newest first), then folds anything durable into the right doc (`docs/look-and-sound.md`, `docs/style-bible.md`, `docs/ai-generation-stack.md`, `docs/formats/*`, `RUNBOOK.md`) or script. Keep entries short: what happened, what we learned, what changed.

## 2026-10-30 — Part 1 (first test video, v1 → v3)
- v1 "a bit much"; v2 more refined; v3 approved direction: full-frame alternation, styles A light desk / B dark editorial / C set reveal.
- Root cause of the bad grade: iPhone HLG HDR never tone-mapped. Fixed in `cut.py`; subject/background grade in `look.py`.
- Sound: DPDFNet 48 kHz denoise, EQ toward natural speech curve, felt-piano bed, organic SFX, -14 LUFS.
- Studied: McKinnon / D'Avella / Johnny Harris (grade), rpn reels DdmBks7tKga + DdUFrgxOcOx, kaye.creatives (set reveal + collage explainer), higgsfield.ai one-camera multi-angle reel.
- Tool stack decided: Higgsfield Plus (connector) + ElevenLabs Creator; ~8-20 AI-shot videos/month on ~$81.
