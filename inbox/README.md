# inbox/

Fallback drop box for signals when the Brand OS database isn't reachable. One markdown file per signal, named `YYYY-MM-DD-short-title.md`, starting with:

```
source: <chat / agent / Andrew>
kind: feedback | adopted | evidence | reference | fix | tool
evidence: <links, numbers, or "Andrew said so">
```

followed by the signal in plain words. The Kit Curator processes these nightly (see `CURATION.md`) and deletes each file once it's handled.
