# Motion playbook: how Claude makes motion graphics for Andrew

Status: **reference + tooling**. Learned 2026-11-01 from the Prompt Motion library (233 Claude-made motion films with their prompts, full copy in `prompt-motion-catalog.json`) and HeyGen's HyperFrames motion skills. Nothing here overrides a house rule in `style-bible.md`; it is how to *build* the graphics those rules ask for.

## 1. What the library tells us (233 films, Sept-Oct 2026)
- **Most prompts are one line.** Median prompt is ~150 characters; 90 were marked one-shot. The single most-copied prompt (40 films): "make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are". Short prompts get showreels, not story. They look impressive and say nothing, so we don't use them for Andrew's reels.
- **The best ones read like a creative brief.** The 12 strongest entries share one shape: `inputs → direction → structure → build → gotchas → start`. That shape is our brief template (section 3).
- **Almost everything is landscape.** 149 of 233 are 1920x1080; only 19 are vertical. Vertical motion for Reels is still open ground, a chance to stand out.
- **Themes:** Product UI (102), kinetic type (96), music-timed (49), particles (43), shapes (42), charts (33), diagrams (31), characters (27), photos (23), phone mockups (22).
- **Stacks:** where stated, Remotion (12), plain HTML (10), HyperFrames (9), Three.js (5). All work the same way: Claude writes a page where every pixel is a function of time, and a headless browser renders it frame by frame. Our `scripts/render_gfx.py` already works this way (`render(t)`), so no new tool is needed.
- **What creators ban:** particle bursts, glows, crossfades, stock-looking assets, gradients on UI, neon/purple "AI" looks, text and frames hugging the corners, dead time. These are the tells that something was AI-made.

## 2. Motion rules worth borrowing (plain language)
1. **Pure function of time.** Every frame is computed from `t` alone: no CSS transitions, timers or random numbers without a seed. That is why a render is identical every time.
2. **Exit decides entry.** How one scene leaves sets how the next arrives: same direction, same speed, and cut while both are still moving. A thing that shrinks away should not be answered by a thing growing in (it reads as a bump).
3. **One main direction per video.** Pick it (default: left) and use it for every ordinary transition. Save up, zoom-in and zoom-out for moments that mean something (a reveal, an arrival).
4. **Carry the eye across cuts.** Hand a real object across the cut (a cursor mid-move, a card that docks into the next layout, a word that flies into its slot). Never a plain crossfade.
5. **Cause, then effect, same frame.** Click → squash → spring → land → reveal. A reaction starts on the frame of its cause, not "shortly after".
6. **No idle wobble.** No breathing, floating or pulsing to fill time. If a scene has nothing left to do, it's too long or needs more story.
7. **A beat of stillness before the payoff:** 0.3-0.75 s pause between the action and the result.
8. **Timing:** single entries ≤ 0.8 s, exits ~75% of entries, total stagger ≤ 0.5 s. No bounce or elastic easing; a small overshoot is fine. Similar elements share one easing.
9. **Two or three transition types per video**, repeated. Variety reads as noise.
10. **Music is the clock.** Find the beat grid in the track first; land every change on a beat; place each sound effect on its visual hit.
11. **Loops:** last frame identical to the first (cursor position and speed included).

## 3. The brief Claude writes before any motion scene
```
<inputs>   What only Andrew can give: the words, the real screens/photos, the song, the brand colours.
<direction> The look in one paragraph + a "Banned:" list (from section 1 plus Andrew's own no-gos).
<structure> Beat-by-beat: what happens on each beat or spoken word, with times.
<build>    Size (1080x1920 for Reels), render(t) rules, springs, motion blur setting, sound placement.
<gotchas>  Known traps for this kind of scene (section 5).
<start>    Render one still per beat first; fix anything cramped or off-grid before the full render.
```
Andrew's look to plug into `direction`: modern corporate meets cozy: wood tones, earthy neutrals, one green, a pop of blue or a blue gradient used once. One UI font plus one display font per video (style-bible keyword promotion).

## 4. Rendering in this kit
- `python3 scripts/render_gfx.py TEMPLATE.html PROJECT STYLE OUT` as before.
- **New:** `GFX_SUBFRAMES=8` adds real motion blur (8 moments per frame averaged, 180° shutter by default; `GFX_SHUTTER` changes it). Use it for anything fast: whips, flying cards, morphs. Costs ~8x render time, so test stills without it. Tested 2026-11-01: a box at 3,000 px/s gets a 50 px soft streak instead of a hard edge.
- Fewer than ~6 subframes leaves ghost copies on fast moves; use 8, or slow the move.
- HyperFrames (HeyGen, open source) is the most complete off-the-shelf version of this: GSAP timelines, a preview app, a block registry and the motion skills summarised above. Optional install: `npx skills add heygen-com/hyperframes`. Worth trying for a long explainer; not needed for overlays and cards, which `render_gfx.py` already does.

## 5. Gotchas collected from the library
- Measure text only after fonts load; a long name won't fit where a short one did, so scale the whole lockup.
- Text that swaps inside a morphing shape needs its own enter/exit timing (or mask) or letters overlap.
- No `will-change` on anything the camera scales (text goes blurry). No opacity or filter on a 3D (`preserve-3d`) element; fade its wrapper.
- A colour flood must overscale past all four corners and take ~0.3 s, or half the screen changes in one frame and reads as a glitch.
- Fading phones/cards to transparent shows what's behind; fade to the background colour first.
- A white card on a white page disappears: give it a 1px hairline and a faint shadow.
- A 0.05 s fade reads as a pop; a highlight box behind a word looks like a text selection.
- Keep overlays clear of real screen recordings' own cursors and HUDs.
- Only music and SFX licensed for commercial use.

## 6. Entries worth opening first (in the catalog JSON, by slug)
- `twoclipping-5cba86` Shape morphing through UI states: best example of the full brief format; one shape, beat-locked, cursor-driven.
- `gizakdag-cf4ae6` Overthinking motion study (vertical): an abstract concept as motion, the closest match to Andrew's thought-leadership talks.
- `x4b47x-9cc84f` Shadow theatre "what makes a place feel like home" (vertical, code-made audio): story-led motion, fits the apartment/home content.
- `lexnlin-038035` Engraving-style ad (vertical): how to brief "study a reference, borrow the timing, change the design".
- `kloss-xyz-15182a` Chaotic Claude POV (vertical, Python + ffmpeg): high-energy edit with sound design from code.
