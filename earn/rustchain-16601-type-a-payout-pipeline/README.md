# From Verified Bounty to Settled RTC — Type A Production Kit

Submission target: Scottcjn/rustchain-bounties #16601, **Package Type A — YouTube full production kit (40 RTC)**.

## Concept

A source-backed 4–5 minute explainer of the RustChain bounty payout lifecycle:
**work → verification → payout request → pending hold → settled wallet history**.

This is a new underlying topic, distinct from this contributor's earlier Type B Proof-of-Antiquity package, Type C shorts, and Type D syndication add-on.

## Package contents

- `script.md` — full sectioned narration
- `voiceover_text/` — narration source per section
- `voiceover/` — generated WAV sections + engine note
- `visuals/` — original generated 1920×1080 diagrams/cards
- `assembly.md` — generated timestamp/edit map from actual WAV durations
- `thumbnail.png` + 2 alternates — 1280×720
- `metadata.md` — titles, description, tags, chapters
- `SOURCES.md` — claim-by-claim source map
- `VERIFY.md` — reproducible package checks
- `generate_assets.py` — deterministic asset generator
- `visual_specs.json` — visual source spec

All visual assets are generated from text/shapes in this repository. No third-party stock footage or music is used.

## Validation

The asset workflow installs eSpeak NG + Pillow, generates all audio/visual files, validates image dimensions and WAV readability, then commits the generated package back to this branch.

No payout is asserted until Elyan Labs accepts the package.
