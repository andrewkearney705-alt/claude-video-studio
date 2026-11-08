"""Free pre-test: score each cut on the hook/pacing checks short-form retention depends on. A ranking aid, not a prediction.
usage: pretest.py science1.json science2.json ..."""
import json, sys
rows = []
for f in sys.argv[1:]:
    s = json.load(open(f)); h = s['hook']; p = s['pacing']; pts = []
    def add(ok, n, why): pts.append((n if ok else 0, n, why))
    hs = h['seconds']
    pts.append((3 if hs <= 4 else 2 if hs <= 7 else 1 if hs <= 10 else 0, 3, f"hook lands in {hs:.1f}s (3 pts at 4s or less, 2 at 7s, 1 at 10s)"))
    add(h['first_word_s'] is not None and h['first_word_s'] <= 0.3, 1, f"first word at {h['first_word_s']}s")
    add(h['words_per_s'] >= 3.0, 1, f"hook pace {h['words_per_s']} words/s")
    add(h['big_text_in_first_3s'], 1, "big text in first 3s (sound-off viewers)")
    add(h['face_in_first_frame'], 1, "face in the first frame")
    add(p['median_shot_s'] <= 2.0, 1, f"median shot {p['median_shot_s']}s")
    add(p['longest_shot_s'] <= 6.0, 1, f"longest unbroken shot {p['longest_shot_s']}s")
    add(s['duration_s'] <= 45, 1, f"length {s['duration_s']}s (1 pt at 45s or less)")
    score = sum(a for a, _, _ in pts)
    rows.append(dict(post_id=s['post_id'], score=score, max=10, checks=[dict(pts=a, of=b, why=w) for a, b, w in pts]))
print(json.dumps(rows))
