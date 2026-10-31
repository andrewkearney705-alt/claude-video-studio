# AI generation stack + the kaye.creatives playbook (studied Oct 30 2026)

## Who: kaye.creatives (Kareema Yertargyn)
Musician + CS engineer, 1.1M followers in ~6 months from zero, top reels 28M / 12.7M / 10.2M views, partners with Higgsfield (#higgsfieldcreator). Posts almost daily. Nearly every caption ends "Comment WORD for prompts / guide", which drives huge comment counts (her set-reveal reel: 25K likes, 10K comments) and feeds an auto-DM.

## Her four content lanes
1. **Collage explainer (the one Andrew loves, DfAu-coo2xr, Microduck):** 4:3 frame. Light-grey dot-grid "paper" canvas. Her talking head is a small framed card that grows. Words stack one at a time in small bold black sans at the left; one word in small caps elsewhere ("ADMITTED"). Brand logos pop in as tilted sticker icons, cut-out heads of the people mentioned pop around her, a pixel-art robot icon. Then a hard cut to an AI-generated cinematic scene (Jensen on stage with robots) with big mono type-on ("4 DUCKS"). Back to her real A-roll in a warm cosy room (practical lamps, piano, posters) with huge yellow condensed numbers with drop shadow ("$399", "$4,000,000"); the product composited into real places (duck on a NYC street, by a yellow cab); "Isn't that FASCINATING?" on black with hand-drawn sparkles; editorial cards with yellow highlighter text ("Its most important feature is actually how it learns") on the dot grid; tilted screenshots and screen recordings with drop shadows; split screen (B-roll top, her bottom, captions on the seam); glitchy rainbow display type for the closing question ("Who wins the RACE?"). Cuts every 1-1.5 s, never the same treatment twice in a row.
2. **Spec commercials for brands** ("Day 4 of making commercials until a brand pays me", Oakley Meta 65K likes, Ballon d'Or 94K likes): fully AI-generated ads made in Higgsfield (Seedance / Kling / Soul), brand tagged, tutorial on YouTube.
3. **Film/trend recreations** (Coraline 87K, Blade Runner, Ghostbusters): recognisable worlds rebuilt with AI.
4. **Real footage + AI worlds:** set reveal (walls fall into a stadium), herself composited into generated scenes.

## Her "secret sauce" workflow (from her own captions + the workflow reel De-Jc_lIC70)
1. Don't invent from scratch: find trends/formats already working.
2. Rebuild them with your own character + motion: generate a consistent character image (Higgsfield Soul / Soul ID or Nano Banana), then motion-transfer the trend clip onto it (on screen: a dark app with a lime Generate button, consistent with Higgsfield; a person in a dance trend becomes a frog-headed character).
3. Ship fast, daily, with a comment-keyword CTA; the full tutorial lives on YouTube (long-form funnel); brand deals follow.
She also ran a "Claude Motion with Opus 5.5 vs a human motion designer" video, so Claude-made motion graphics are already part of this scene.

## Tool stack and what each is for (prices from 3rd-party summaries, Oct 2026: verify before buying)
| Job | Tool | Cost | How Claude drives it |
|---|---|---|---|
| Generated shots (B-roll, product in a scene, spec ads, AI worlds) | **Higgsfield** (one sub = Seedance 2/2.5, Kling 3, Veo 3.1, Sora 2, Nano Banana, Soul) | Plus $59/mo (1,200 credits, all models); Starter $19 excludes Seedance 2 / Veo | Pay-as-you-go API at cloud.higgsfield.ai (`pip install higgsfield-client`, HF_API_KEY/SECRET), Higgsfield MCP, or Claude drives the web app in the built-in browser |
| Your voice for pickups, fixes, VO | **ElevenLabs** voice clone | Instant clone from Starter ~$6/mo; Professional clone needs Creator ~$22/mo | API (api.elevenlabs.io) |
| A talking avatar of you (low-effort videos) | **HeyGen** Digital Twin / Avatar V | Creator ~$29/mo; API ~$0.05/s | API |
| Motion graphics, captions, layouts, grade, sound, assembly | **Claude + this kit** | already have | local |
Rule: Claude is the director/editor; generators make individual shots; Claude writes prompts, keeps characters consistent, cuts, grades, mixes and animates.

## What has to be switched on for Claude to call them
- Claude's workspace blocks these hosts by default (tested: api.elevenlabs.io, cloud.higgsfield.ai, api.heygen.com all refused). Andrew adds them under claude.ai Settings > Capabilities (allowed domains), then gives API keys via a secrets file he creates (Claude never types passwords).
- Or: Claude drives the Higgsfield/ElevenLabs web apps in the built-in browser where he's signed in (he logs in himself).
- Label AI-generated content (Instagram's "AI content" tag); never put words in real people's mouths; brand ads are spec work, clearly marked.

## Recreating her collage explainer in the kit
New template scene types to build: dot-grid canvas, growing talking-head card (use the person mask for a cut-out version), stacked left words, logo/head stickers popping with 1-frame overshoot, yellow condensed number slams (Bebas/Anton + drop shadow), highlighter-text cards, tilted screenshot cards, black "question" card with hand-drawn sparkles, glitch rainbow display type. 4:3 or 9:16 both work (she posts 4:3).
