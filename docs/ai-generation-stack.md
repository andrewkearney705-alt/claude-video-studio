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

## How other people wire these together (researched Oct 30 2026)
Three patterns:
1. **Claude as director over MCP connectors (most relevant).** Higgsfield has an official MCP: claude.ai Settings > Connectors > Add custom connector > `https://mcp.higgsfield.ai/mcp` (Claude Code: `claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp`). Needs a paid Higgsfield plan; every MCP generation spends credits (unlimited plans don't apply via MCP); exposes image/video gen, Kling 3 Motion Control, Soul characters, upscaling, voiceover/voice clone/dubbing, credit balance. ElevenLabs has a hosted connector in the Claude directory (the directory listing is focused on its voice agents) plus an open-source MCP (TTS, voice clone, transcription). fal.ai MCP (`https://mcp.fal.ai/mcp`, pay per run, 1,000+ models incl. Kling) is the vendor-neutral option.
   Example (ceos3c): transcript → Claude writes a shot plan (line → noun → visual, shared style suffix, "no people, no hands, no readable text") → quotes credit cost → 32 stills as a contact sheet for approval → image-to-video on Seedance 2.5 (4 s, 1080p, batches ≤ 5) → rejects/re-runs bad clips → clips land in the project folder → assembled. Quoted 712 credits, actual 840 (re-runs). Clips took 3-8 min each. Rule: one prompt = one shot ("then" makes the model draw panels).
2. **Claude + browser automation of the web app.** AKCodez/higgsfield-claude-skills: 19 Claude Code skills; Playwright drives Higgsfield's UI (Soul character → Seedance video, 9:16), asks before clicking Generate. Uses web-plan pricing but breaks when the UI changes.
3. **No-code chains.** n8n / Segmind / Creatomate flows: prompt → LLM writes JSON script → Kling video + ElevenLabs voice in parallel → merge (Segmind's Kling+ElevenLabs UGC flow ≈ $4.32, ~7 min per video). Good for volume, generic results.
Human-made benchmark: PJ Accetturo's Kalshi NBA Finals ad: script with ChatGPT/Gemini → Gemini turns each shot into a Veo 3 prompt (5 at a time, more and quality slips) → 300-400 generations for 15 usable clips → edited by hand. 3 days, ~$2,000.
Common lessons: approve stills before paying for video; budget 20-30% over the quote for re-runs; keep a shared style suffix + reference images for consistency; put a human approval gate before generation spend and before posting; generated clips land straight in the project folder so the edit step picks them up.
Comment-keyword CTAs ("comment PROMPTS") are run with ManyChat-style comment-to-DM automation on Instagram.
