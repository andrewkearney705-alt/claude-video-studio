# Claude Video Studio — Andrew's short-form editing kit (part 1)

Everything Claude learned and built while editing the first test video, packaged so any future Claude session can do it again.

## How you make a video
1. **Write it with Claude.** Ask for a script in one of the five formats (see `docs/formats/`): AI news explainer, podcast clip, founder one-take, build-in-public series, cinematic montage reveal.
2. **Record it.** Use the Take One teleprompter (`templates/take-one-teleprompter.html`, also hosted on your Netlify site). Read each line 2-3 times. Phone vertical, 4K, any frame rate. Face a window if you can.
3. **Hand it over.** Upload the clip (or point Claude to it on your Mac) and say which format and style: A light desk, B dark editorial, C set reveal, or split-screen.
4. **Claude edits end to end** with this kit: transcript → best takes → HDR fix + grade → denoise + music + effects → animation scenes → final + no-music version.
5. **You review**, give notes, Claude revises. Post (you approve every post).

## What's inside
- `RUNBOOK.md`: the exact step-by-step Claude follows.
- `scripts/`: transcription, cutting with HDR tone-mapping, person masks, the grade (`look.py`), denoise, music + SFX, mixing, graphics rendering, final composite.
- `templates/`: the full-frame animation scenes, the 3D set-reveal intro, the teleprompter.
- `docs/`: style bible (70+ reels analysed), look-and-sound guide (McKinnon / D'Avella / Johnny Harris), pipeline, the five formats, and how to study a creator's reels frame by frame.
- `examples/test-video/`: the edit decisions and timings from the first video.

Models and fonts aren't included (too big); `setup.sh` downloads them in a minute.
