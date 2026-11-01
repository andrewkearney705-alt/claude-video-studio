---
name: product-demo-film
description: Use when Andrew wants a polished, no-talking "watch it build" reel: a real screen recording of Claude (or another tool) doing one big thing, cut like a product launch film, ending on a cinematic payoff.
---

# Product demo film ("one prompt, watch it build")

Added Nov 1 2026 at Andrew's request ("add this kind of video style to our toolkit as something I can create"). An opt-in format, not a default.
Reference: higgsfield.ai DZcy41GithZ, a 43 s launch film for Claude + Higgsfield MCP. ~717K likes, 11.4K comments, 1.6K reposts; its original audio page shows ~2.1M plays and 62 reels reusing the sound. That is roughly 7x the account's recent median (~300K views over its last 12 reels), though the reel is older than that sample and is a brand launch ad with paid reach possible, so treat the multiple as rough.

## Measured fingerprint
| | Reference | Notes |
|---|---|---|
| Length | 43 s | |
| Frame | 16:9 film (1916x1078) placed in the vertical reel | reads as "a film", not a phone video |
| Voice | none | the caption carries the words; music + SFX do the rest |
| Mix | loud and continuous, ~-17 dB RMS, peaks ~-7 dB | one music bed throughout |
| Sound events | ~21 onsets, mostly 13-30 s, on cursor clicks, toggles and card arrivals | |
| Big beat | biggest hit at 27 s, a ~1 s drop-out at 29 s, the payoff title slams at 30.5 s | breath before the reveal |
| Payoff share | last 30% of runtime is the finished output | |

## Beat sheet
1. **0-1.9 s brand lockup**: soft pastel gradient, a few organic elements drifting in (butterflies), "Tool A × Tool B" lockup; blur-dissolve to white.
2. **2-7 s the ask**: clean chat window, the prompt types itself, extreme punch-in on the cursor hitting send (the model name huge in frame).
3. **8-17 s the thinking**: a checklist animates line by line, option cards appear, a second macro punch-in on the next confirm, one toggle switching on (the integration).
4. **18-29 s the making**: asset grids fill in (characters, scenes, UI), each group landing with a tick; a status line ("All set… building…") and the drop-out.
5. **30-41 s the payoff**: hard cut to the finished thing full frame and cinematic (title card slam, then 10 s of the result itself).
6. **42 s end card**: "Now available on …" logos on white.
Caption: one-line hook ("X + Y is insane"), two sentences on what it does, comment-keyword CTA for the setup guide.

## Why it likely worked (moderate confidence)
- Result-first promise in the first line, proof shown rather than claimed: the whole pipeline is visible.
- Every interaction is real UI, magnified: punch-ins land on real clicks, so it feels like watching the tool, not an ad mock-up.
- No talking means no translation needed; it travels across languages and works muted.
- The payoff is a different medium (cinematic game footage) from the setup (white UI), so the contrast lands.
- Comment-keyword CTA on something useful to the viewer's own work (see `knowledge/patterns.md`, Emerging).

## Andrew's version
- Subject: his own real builds, shot from his screen (Open Loops panel, a brand-system run, the empty-wall redesign going from photos to a 3D model to the real build). The payoff should be real-world when possible: the built wall, the edited reel, the finished tool in use.
- Look: keep the brand lockup and white UI clean, but swap pastel butterflies for his palette (wood, earthy green, one blue gradient) and his clay accent on clicks. His cinematography is the payoff edge: end on real camera footage, graded (look B).
- Motion: `templates/motion.js` springs for every card and chip, `anticipate` on the punch-ins, `blurFromSpeed` on the fast zooms. Real screen recordings only, never drawn mock UI.
- Sound: one music bed, real recorded SFX (`ui-tick` on clicks, `soft-impact` on card groups, `riser` into the drop-out, silence for ~1 s, `low-boom` on the payoff title). Read `look-and-sound.md` §3c.
- Optional: his voice for one line at the payoff only ("I didn't touch a single setting"), to keep it personal.

## Shot list
- Screen recording of the full run at 60 fps, high resolution, cursor visible, notifications off. Record the real app (screen recorder or OBS driven by Claude).
- Camera footage of the finished thing (or him using it) for the payoff, 5-10 s.
- One clean prompt written in advance so the typing reads well.
