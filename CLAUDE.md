# claude-video-studio: instructions for any Claude session

This is Andrew Kearney's private short-form video kit: how he likes reels scripted, shot, edited and graded. Read `README.md` first, then `RUNBOOK.md` before editing footage.

## How this repo learns
Read `CURATION.md`. In short:
- The **Kit Curator** (a nightly scheduled task) owns the rule docs and keeps them tidy.
- If you learned something in your chat (Andrew's feedback, a fix, a creator breakdown, a tool change), **drop a signal** instead of rewriting rule docs yourself: add a doc to the Brand OS `kitsignals` collection (ArtifactData, url https://claude.ai/artifact/JJuNiBCQvnjtEfcgK6ZsAz), shaped `{source, kind, title, body, evidence, createdAt, status:"new"}`. If the database isn't reachable, add a markdown file to `inbox/` in this repo and push.
- You **may** edit rule docs directly when Andrew explicitly adopted a rule in your chat or you fixed a script on real footage. Then still add a `LEARNINGS.md` entry, run `python3 scripts/curate_check.py`, and push.
- Strategies Andrew collects (Kallaway, Mino Lee, kaye, etc.) are **reference**, not house rules, unless he adopts them.

## Never commit
Footage, renders, voice, models, fonts, keys, personal details, or anything naming his employer (say "a Fortune 500 insurer").

## Pushing
`git pull --rebase` before you push. Plain commit messages. If a push is refused, put the change in a `kitsignals` doc so the Curator applies it; don't hand Andrew zip files.
