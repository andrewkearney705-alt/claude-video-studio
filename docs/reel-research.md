# How Claude studies a creator's videos (frame by frame)

Use the built-in browser (Andrew is logged into Instagram there). Instagram's API rate-limits fast (429), so navigate to each reel page instead and read the `<video>` element directly.

## Rules learned the hard way
- The browser pane is usually hidden: `requestAnimationFrame` never fires and `img.decode()` can hang. Use `setTimeout` loops.
- Instagram reels often report `duration` as Infinity (streamed). If so, use the playback sampler; if duration is finite, use the seek sampler (more reliable).
- Keep each call under ~40 s (tool timeout); split long reels into several calls.
- Helpers vanish on every navigation: redefine them after `navigate`.
- After running a sampler, take a screenshot: the contact sheet is drawn as a fixed overlay `#__cs` at the top-left.
- YouTube: wait out ads first (`.ad-showing`, click `.ytp-skip-ad-button`). Video element: `#movie_player video`.

## Seek sampler (finite duration: most reels on second load, all YouTube)
```js
window.__seek = async (times, cols=5) => {
  const v=[...document.querySelectorAll('video')].sort((a,b)=>b.getBoundingClientRect().height-a.getBoundingClientRect().height)[0];
  v.muted=true; v.pause();
  const W=200, H=Math.round(W*v.videoHeight/v.videoWidth);
  const c=document.createElement('canvas'); c.width=W*cols; c.height=H*Math.ceil(times.length/cols);
  const x=c.getContext('2d'); x.font='bold 16px monospace'; x.fillStyle='#0f0';
  for(let i=0;i<times.length;i++){
    await new Promise(r=>{const f=()=>{v.removeEventListener('seeked',f);r()}; v.addEventListener('seeked',f); v.currentTime=times[i]; setTimeout(r,3000)});
    await new Promise(r=>setTimeout(r,120));
    x.drawImage(v,(i%cols)*W,Math.floor(i/cols)*H,W,H); x.fillText(times[i].toFixed(2),(i%cols)*W+4,Math.floor(i/cols)*H+16);
  }
  document.getElementById('__cs')?.remove();
  const img=document.createElement('img'); img.id='__cs'; img.src=c.toDataURL('image/jpeg',0.88);
  img.style.cssText='position:fixed;left:0;top:0;width:800px;z-index:999999;background:#000';
  document.body.appendChild(img); return 'dur '+v.duration;
};
await __seek(Array.from({length:30},(_,i)=>i*0.2));   // first 6 s at 5 fps: how the hook is built
```

## Playback sampler (streamed reels, duration = Infinity)
```js
window.__ig2 = async (step=2, cols=4, maxN=20, start=0, rate=2) => {
  const v=[...document.querySelectorAll('video')].sort((a,b)=>b.getBoundingClientRect().height-a.getBoundingClientRect().height)[0];
  v.muted=true; v.currentTime=start; v.playbackRate=rate; try{await v.play()}catch(e){}
  await new Promise(r=>setTimeout(r,800));
  const W=200,H=Math.round(W*v.videoHeight/v.videoWidth), c=document.createElement('canvas'); c.width=W*cols; c.height=H*Math.ceil(maxN/cols);
  const x=c.getContext('2d'); x.font='bold 16px monospace'; x.fillStyle='#0f0';
  let i=0,next=start+0.3,last=-1,t0=Date.now();
  while(i<maxN&&Date.now()-t0<38000){const t=v.currentTime; if(t<last-1)break; last=t;
    if(t>=next){x.drawImage(v,(i%cols)*W,Math.floor(i/cols)*H,W,H); x.fillText(t.toFixed(1),(i%cols)*W+4,Math.floor(i/cols)*H+16); i++; next+=step}
    await new Promise(r=>setTimeout(r,40))}
  v.pause(); document.getElementById('__cs')?.remove();
  const img=document.createElement('img'); img.id='__cs'; img.src=c.toDataURL('image/jpeg',0.85);
  img.style.cssText='position:fixed;left:0;top:0;width:800px;z-index:999999;background:#000'; document.body.appendChild(img);
  return 'frames '+i+' last '+last.toFixed(1);
};
```

## Grade stats (add to any sampler)
Per frame: luminance 2nd/50th/98th percentile (black level, exposure, highlight roll-off), mean saturation (max-min)/max, mean R,G,B (warmth). Sample every 16th pixel with `getImageData`. Compare with the targets in `look-and-sound.md`.

## What to write down for every reel
1. Hook: first frame, first cut time, what text appears and how it animates in.
2. Layout per section: full frame / split / animation scene; how often it changes.
3. Type: fonts (serif vs mono vs sans), size, case, position, colour, how each animates.
4. Pacing: cuts per minute, median shot length, pauses over 0.15 s.
5. Look: blacks, saturation, skin warmth, room vs subject brightness.
6. Sound: music bed, SFX per minute and which kinds, ducking.
7. Payoff + CTA, and the reel's views/likes/comments for context.
Then turn the patterns into rules and a recipe; save them in `docs/` and the matching format file.

## Reference reels already studied (Oct 2026)
- rpn "Life with Claude" DdmBks7tKga: serif title letter write-on over full-frame footage, ghost UI menu words, small serif subtitles.
- rpn "I've joined…" DdUFrgxOcOx: full-frame A-roll (cool window + warm practicals) alternating with light-desk card slams / collage / floating windows, big number counter over A-roll, tiny mono captions.
- kaye.creatives Dem0m2cPIAg: set-reveal intro (walls fall, crane back into a stadium).
- 70+ reels from rpn, greglav, DOAC and rising creators: see `style-bible.md`.
- kaye.creatives DduIcDJI3vP: 4:3 split news explainer (face left, one-phrase card right every 1.5-2 s), heavy condensed caps + italic serif word, AI-generated self inserts. 21.4K likes.
- kallawaymarketing Dd8vo8IxamX: creator teardown of Nate Gaffney with Claude + Sandcastles; 3 named patterns, section chips, proof graphics, "Comment NATE". 1,397 likes, 526 comments. See `formats/creator-teardown.md`.
