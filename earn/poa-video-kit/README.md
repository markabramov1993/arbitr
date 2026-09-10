# #16601 Type B — Proof of Antiquity YouTube script + storyboard kit

Publication-ready Type B package submitted for `Scottcjn/rustchain-bounties#16601`.

## One-line pitch

A ~4-minute evidence-backed explainer showing how RustChain's Proof of Antiquity combines one-CPU/one-vote identity, six hardware-fingerprint checks, a reproduced Azure VM anti-emulation failure, and current antiquity reward weights without claiming that spoofing is impossible.

## Package checklist

- `script.md` — full ~4-minute narration.
- `storyboard.md` — exact shot-by-shot capture directions.
- `assembly.md` — timed edit map from narration to visuals.
- `metadata.md` — title, two alternates, description, tags, chapters.
- `SOURCES.md` — factual claims pinned to RustChain main commit `e805b5ff18f515a7f315807b75b39ed1c5eca972`, plus the reproduced GitHub Actions evidence run.
- `thumbnail.png` — primary original 1280×720 PNG.
- `thumbnail-alt-1.png` — alternate original 1280×720 PNG.
- `thumbnail-alt-2.png` — alternate original 1280×720 PNG.

The three thumbnail assets are generated from original typography/geometry only; no third-party imagery is embedded. The generation workflow verifies PNG format and exact 1280×720 dimensions.

## Final accuracy pass — 2026-09-10

The package was re-audited against current RustChain main. The current README/whitepaper values used in the package are:

- PowerPC G4: `2.5x`
- Apple Silicon M1: `1.2x`
- Modern x86_64: `0.8x`

Older secondary documents in the upstream repository still contain historical `1.0x` modern-x86 examples; this package deliberately uses the current README/whitepaper figure and documents the drift in `SOURCES.md`.

## Evidence

Reproduced VM dry-run used by the script/storyboard:
https://github.com/markabramov1993/arbitr/actions/runs/33838143501

Thumbnail build/validation workflow:
https://github.com/markabramov1993/arbitr/actions/runs/34475821963

## Authorship / publication permission

Author credit: `markabramov1993` / Oleg Leads. AI assistance was used under operator authorization and the factual claims were independently rechecked against the cited public source revision.

By this submission, Elyan Labs may publish this submitted package on official channels with permanent attribution to `markabramov1993`. The author retains authorship; unrelated repository content is not included in this permission.

RTC wallet: `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`

Status: submitted by the documented email fallback on 2026-09-04. No acceptance or payout is asserted until maintainer confirmation.
