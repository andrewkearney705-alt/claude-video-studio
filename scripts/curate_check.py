#!/usr/bin/env python3
"""Pre-push check for the kit. Run from the repo root: python3 scripts/curate_check.py
Fails (exit 1) on: oversized docs, media or model files, secret-looking strings,
merge markers, or banned employer references. Prints plain-language problems."""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAPS = {"docs/style-bible.md": 18_000}
DEFAULT_DOC_CAP = 10_000
LEARNINGS_CAP = 20_000
BLOCKED_EXT = {".mp4", ".mov", ".m4a", ".wav", ".mp3", ".aac", ".heic", ".jpg", ".jpeg", ".png",
               ".onnx", ".pt", ".pth", ".bin", ".safetensors", ".ttf", ".otf", ".zip"}
SECRET = re.compile(r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|"
                    r"xox[abp]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
BANNED = re.compile(r"\bAIG\b|Assist\+", re.I)
# Files allowed to mention the employer rule itself.
BANNED_OK = {"CURATION.md", "CLAUDE.md", "scripts/curate_check.py"}

def tracked():
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [p for p in out.splitlines() if p]

problems = []
for rel in tracked():
    p = ROOT / rel
    if not p.is_file():
        continue
    if p.suffix.lower() in BLOCKED_EXT:
        problems.append(f"{rel}: media/model/font files never go in the repo")
        continue
    if p.stat().st_size > 2_000_000:
        problems.append(f"{rel}: over 2 MB; keep big files out of git")
        continue
    try:
        text = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    if SECRET.search(text):
        problems.append(f"{rel}: contains something that looks like a key or token")
    if re.search(r"^(<{7}|>{7}|={7})( |$)", text, re.M):
        problems.append(f"{rel}: leftover merge markers")
    if rel not in BANNED_OK and BANNED.search(text):
        problems.append(f"{rel}: mentions the employer; say 'a Fortune 500 insurer'")
    if rel.endswith(".md") and (rel.startswith("docs/") or rel == "RUNBOOK.md") and not rel.startswith("docs/archive/"):
        cap = CAPS.get(rel, DEFAULT_DOC_CAP)
        if len(text.encode()) > cap:
            problems.append(f"{rel}: {len(text.encode()):,} bytes, cap {cap:,}; merge or cut lines")
    if rel == "LEARNINGS.md" and len(text.encode()) > LEARNINGS_CAP:
        problems.append("LEARNINGS.md: too long; roll entries older than 30 days into docs/archive/")

if problems:
    print("Kit check failed:")
    for x in problems:
        print(" -", x)
    sys.exit(1)
print("Kit check passed.")
