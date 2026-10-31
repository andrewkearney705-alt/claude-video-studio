# Editing rules (numbers, not vibes)

Hard rules every edit follows, written as numbers Claude can check. Started 2026-10-31 from Mino Lee's (@minolee.mp4, Content Academy) "15 AI editing rules" PDF, then adapted to Andrew's approved styles. Where Mino's taste and Andrew's clash, Andrew's wins and the clash is noted.

**How this file grows:** after every edit Andrew watches it like a viewer, names exactly what's off ("captions 10% smaller", not "make it better"), and says "save that as a rule". Claude adds the rule here with a number in it, and the date.

## 1. Cutting (adopted)
- **Zero dead space.** "Dead" = more than 11 dB under Andrew's speaking level, including breaths and trailing words. Every join ≤ 20 ms of dead audio. `scripts/qa_check.py audio` must report 0 dead runs before render.
- **Tone sets the gap.** Tag each EDL line with `"tone"`:
  - `normal` → 0 frames, straight into the next line
  - `serious` → 6 frames (0.2 s) of held air so it lands
  - `joke` → cut mid-word; the cut is the punchline
- **Tight, not choppy.** 1-3 frame J-cuts (next line's audio starts just before its picture). Keep up to 60 ms of each word's natural fade. Never leave a sliver of a cut word (sounds like a stutter).
- **Cut words, not just air.** Drop repeats, tangents, extra detail, double sign-offs, stumbles. Best take of every line; it must sound like one take.

## 2. Captions (partly adopted)
- 2-3 words per chunk. **Never end a chunk on a weak word** (a, an, the, to, of, my, and, but, or, in, on, for, with, is). `qa_check.py captions` flags them.
- No emojis, boxes, outlines, highlights or bouncy animation. Hard cut on the spoken word.
- **Not adopted:** Mino's big centred 52 px TikTok Sans. Andrew's signature stays: small Space Mono caps + soft shadow, with one display-font keyword (style bible rules 3-4).

## 3. Placement (adopted, re-measured for Instagram)
Instagram is the home platform, so the safe zone is Instagram's (starting values from Hopper's 2026 Reels guide; confirm against a screenshot of a posted reel and update):
- Top 0-270 px (14%): nothing readable.
- Bottom 1250-1920 px (35%): no cards or key text (caption/UI area). Running captions sit above 1250.
- Sides: 65 px margin. Button column: x ≥ 940 from y ≥ 1150.
- `qa_check.py safezone GFX_DIR` checks every graphics frame before composite.
- **Never cover the face.** Cards go in the band above the head. If Andrew leans in, the card gets smaller, not lower. One card at a time. No punch-in while a card is up.

## 4. Visuals and proof (adopted)
- **Show the real thing.** Name an app, article, person or result → show the real logo, screenshot or UI. No emojis anywhere.
- **Real receipts only.** Never invent a number, payment, follower count or review. No receipt → keep the line on Andrew's face. Label time spans ("4 days, Oct 15-19").
- **Money in full:** "$11,500 MRR", never "11.5k". Non-money counts stay as spoken ("10k views").
- **Literal B-roll** from Andrew's own footage first (the content vault, his drives), stock last. Starts on the first word. A spoken list = one clip per item, ≥ 0.9 s each. Darken B-roll to ~72% under captions.
- **Files as files:** show folders as a grid of real thumbnails with short labels, not word chips.

## 5. Motion (Andrew overrides Mino)
- Mino: cards appear full-size on their word, no pop/slide/fade; they leave on the next jump cut. **Use this on talking-head stretches** (founder one-take, build-in-public).
- Andrew's approved styles keep their motion on full-frame scenes: A card slam + collage fan, B scan line, C set reveal, serif write-on with 40-60 ms blur->sharp stagger.
- Punch-ins: most cuts stay at 1.0; ~1.25x only on the lines that matter, face re-centred. Never while a card is up.

## 6. Sound (keep Andrew's chain)
- Mino's flat rule (voice +6 dB, music 25% in a quiet intro, 10% once drums or lyrics hit) is a useful sanity check, but `mix.sh` sidechain ducking + -14 LUFS stays the method.
- Adopted: when using a real track instead of the generated piano bed, **start it where it gets good**, not at 0:00.

## Prompts that work (give Claude numbers)
- "Cut the dead space and retakes. Best take of each line. Zero gaps; serious lines get 6 frames."
- "Captions 2-3 words, never end on a weak word."
- "When I name an app or article, show the real one. No emojis."
- "B-roll from my drive; when I list things, one clip per item, 0.9 s minimum."
- "Review my hook against hooks that performed in my niche first, then edit." (needs a hook-research source; see `reel-research.md`)
