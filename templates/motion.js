// motion.js: animation-principle helpers for the gfx templates (frame-rendered, so everything is a pure function of t).
// Why: linear or plain ease-out moves are the main reason AI-made motion graphics "feel AI". Real motion designers use
// anticipation, overshoot and settle, staggered follow-through and motion blur. Paste into a template or <script src>.
// All helpers take t in seconds and return a number; combine them in inline styles.
//
//   const p = M.spring(t, 2.0)                      // 0 -> 1 with a natural overshoot, settles in ~0.5 s
//   el.style.transform = `translateY(${(1-p)*60}px) scale(${M.pop(t,2.0)})`
//   el.style.filter = `blur(${M.blurFromSpeed(t, 2.0, M.spring, 60)}px)`  // motion blur only while it moves fast
//   letters.map((c,i) => M.spring(t, M.stagger(2.0, i, 0.03)))         // follow-through across letters
(function (root) {
  const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const pr = (t, a, b) => cl((t - a) / (b - a));
  // Easing curves. Never use linear for anything that moves on screen.
  const ease = {
    out: u => 1 - Math.pow(1 - u, 3),                                   // arrivals
    in: u => u * u * u,                                                  // exits, things falling away
    inOut: u => (u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2), // camera moves, pans
    expoOut: u => (u >= 1 ? 1 : 1 - Math.pow(2, -10 * u)),             // snappy UI (Apple-like)
    backOut: (u, s = 1.6) => 1 + (s + 1) * Math.pow(u - 1, 3) + s * Math.pow(u - 1, 2), // small overshoot
  };
  // Damped spring from 0 to 1 starting at t0. stiffness/damping in the usual (k, c) sense, mass 1.
  // Defaults give ~5% overshoot and settle in ~0.5 s (tested). damping >= 2*sqrt(k) means no overshoot.
  function spring(t, t0, k = 170, c = 18) {
    const s = t - t0; if (s <= 0) return 0;
    const w0 = Math.sqrt(k), z = c / (2 * w0);
    if (z < 1) { const wd = w0 * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w0 * s) * (Math.cos(wd * s) + (z * w0 / wd) * Math.sin(wd * s)); }
    return 1 - Math.exp(-w0 * s) * (1 + w0 * s);
  }
  // Anticipation: a small move the opposite way before the main move (wind-up), then a spring.
  // Returns progress that dips to -amt during [t0, t0+wind] and springs to 1 after.
  function anticipate(t, t0, wind = 0.12, amt = 0.08, k = 170, c = 18) {
    if (t < t0) return 0;
    if (t < t0 + wind) return -amt * Math.sin(Math.PI / 2 * (t - t0) / wind);
    return -amt + (1 + amt) * spring(t, t0 + wind, k, c);
  }
  // Scale "pop": grows from 85%, overshoots to ~102.5% and settles to 100% (tested). Use for cards, chips, logos landing.
  const pop = (t, t0, from = 0.85) => from + (1 - from) * spring(t, t0, 260, 16);
  // Stagger: start time for item i (letters, list rows, grid tiles). Use 20-60 ms per item.
  const stagger = (t0, i, step = 0.04) => t0 + i * step;
  // Follow-through for a group: later items start later AND settle softer, so the group trails like cloth.
  const follow = (t, t0, i, step = 0.035) => spring(t, t0 + i * step, 170, 18 + i * 0.6);
  // Motion blur: blur in px proportional to on-screen speed (dist px per unit progress). 0 while slow or still.
  function blurFromSpeed(t, t0, fn, dist, k = 0.012) {
    const d = 1 / 120, v = Math.abs(fn(t + d, t0) - fn(t - d, t0)) / (2 * d) * dist; // px per second
    return Math.min(24, Math.max(0, v * k - 1));
  }
  // Hold: keep something still for a beat before it leaves (easy to forget; motion needs rest to read).
  const hold = (t, inAt, outAt, fnIn = spring, fnOut = (tt, t0) => ease.in(pr(tt, t0, t0 + 0.35))) =>
    t < outAt ? fnIn(t, inAt) : 1 - fnOut(t, outAt);
  const api = { cl, pr, ease, spring, anticipate, pop, stagger, follow, blurFromSpeed, hold };
  if (typeof module !== 'undefined') module.exports = api; else root.M = api;
})(this);
