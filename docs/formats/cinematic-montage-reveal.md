---
name: cinematic-montage-reveal
description: Use when Andrew wants a short cinematic piece - a fast motivational montage, a before/after transformation reveal, or a film-style essay (Greg's montage, Roberto's studio reveal and short films).
---

# Cinematic Montage & Reveal

The shortest, most visual format in the set, and some of the biggest numbers: Roberto's 13-second studio reveal hit **13.6M views**, his film essay "The Great Online Game" 5.3M. Greg's montage (the reel Andrew picked) is the same family.

## Measured fingerprint
| | Montage (Greg) | Reveal (rpn) | Film essay (rpn) |
|---|---|---|---|
| Length | 15–25s | 10–20s | 45–100s |
| Cuts per minute | ~60 | 65–75 | ~34 |
| Median shot | 0.8s | 0.8–1.0s | 1.0–1.2s |
| Voice | voice-over, no pauses | none or 1 line | voice-over |
| Measured reels | DfE2ar6BNt4 (104K) | DdX1ExRts3I (13.6M), DebCNPBsSc9 (655K) | C9sN8PKJ240 (5.3M), DdmBks7tKga (4.1M) |

## Variant 1 — Motivational montage (Greg)
- One spoken line split across 15–20 shots, **1–2 words per shot** on screen in bold white with a soft shadow ("Shoot" / "f*cking stars" / "land on").
- Shots: training, working on a laptop, driving, walking through a beautiful space, the product. Each shot 0.5–1.2s, cut on the music beat.
- Open on a jarring frame (Greg uses an inverted-color flash) to stop the scroll.

## Variant 2 — Transformation reveal (Roberto)
- Same camera angle, before vs after. Roberto's 655K version uses a hands-forming-a-frame transition and "Before"/"After" labels; the 13.6M version is a walk-through of an empty warehouse becoming a finished studio, ending on a payoff detail (signed jerseys on the wall).
- One short top caption sets the stakes ("No regrets... welcome to RPN HQ").
- 10–20s total. Music does everything.

## Variant 3 — Film essay (Roberto)
- Treat it as a short film: poster-style title card ("THE GREAT ONLINE GAME — a short by..."), archival and stock-free imagery with huge single-word overlays ("SOCIAL" / "MEDIA"), close-ups of you in a cap, small yellow subtitle words, warm film grade, ends on black.
- Letterboxed 16:9 or 3:2 inside the vertical frame works here.

## Shot list for Andrew
- 20–40 short clips of you in motion across 4–6 locations (gym, desk, car, city, product, nature). Shoot 4K 60fps so Claude can slow moments down.
- For a reveal: lock the camera in exactly the same spot for the before and after.

## Edit recipe
- Build the music first; mark beats; cut every shot on a beat.
- Speed ramps into and out of the hero shot.
- Color: high-contrast film look, crushed blacks, warm highlights.
- Text: 1–2 words, bold sans, centered; one serif title card for essays.
- SFX: whooshes on transitions, a sub-drop on the reveal.

## Look & feel spec (from the frame-by-frame review; full detail in style-bible.md)
- **Greg montage:** open on 2–3 colour-inverted frames that snap to normal on the first beat; 1–2 words per shot in bold sans at ~85% opacity (image shows through), mid-frame, position can shift between shots; whip-blur transitions; 0.5–1.2s shots; voice-over line chopped across shots.
- **Roberto reveal:** one quoted line of small white text over the empty "before" ("'Bro let's get the warehouse'"); match-cut on the same camera angle to the finished space; then 6–8 hero shots of details, ~1s each; no talking; text disappears after the reveal.
- **Roberto film essay:** word-slam open (one huge extended-sans word per face, 0.5s each: "SOCIAL / MEDIA / IS"), drop to a black frame with a tiny gold italic serif subtitle ("dead."), then quiet narration with tiny gold italic subtitles over found footage and warm portraits.

## Examples
- instagram.com/reel/DdX1ExRts3I (rpn studio reveal, 13.6M)
- instagram.com/reel/DebCNPBsSc9 (rpn before/after, 655K)
- instagram.com/reel/C9sN8PKJ240 (rpn film essay, 5.3M)
- instagram.com/reel/DfE2ar6BNt4 (greglav montage)

## Production
Follow `pipeline.md` in this folder (section 9 has the effects recipes) and match `style-bible.md`. For beat-synced cuts, get beat times with librosa (`pip install librosa --break-system-packages`, then `librosa.beat.beat_track`).


## Look, sound and animation upgrades
Read `look-and-sound.md` before grading, mixing or designing animation scenes: HDR tone-mapping, subject/background grade, DPDFNet denoise + voice EQ, organic SFX, full-frame animation scenes (light desk, title write-on, dark editorial, window reveal) and the 3D set-reveal intro.
