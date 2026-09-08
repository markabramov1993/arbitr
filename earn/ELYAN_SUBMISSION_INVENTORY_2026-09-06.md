# Elyan / RustChain submission inventory — canonical dedupe ledger

Updated: **2026-09-08**

Purpose: this file is the canonical duplicate-prevention register for work submitted by `markabramov1993` through GitHub or the documented `sophia.eagent@gmail.com` fallback.

## Accounting rules

- One bounty = one payout claim unless the issue explicitly permits multiple distinct items.
- A repeated email does **not** create a second claim.
- When issue title/body amounts conflict, use the **title / maintainer-confirmed rate** until a maintainer resolves the mismatch.
- `PIPELINE` means submitted but not accepted. `RECEIVABLE` requires explicit acceptance. `CONFIRMED` requires an actual wallet receipt.
- Live wallet authority as of Sep 8: `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d` = **0.0 RTC, 0 transactions**.

## Canonical unique submissions

| Bounty | Deliverable / lane | Canonical reward basis | First sent | Current state | Dedupe / acceptance note |
|---|---|---:|---|---|---|
| #100 | Discovery Mode — Beacon Skill | 2 RTC | 2026-09-06 | PIPELINE | One claim only; no maintainer reply yet |
| #1102 | BoTTube functional bug — JS SDK `health()` response contract mismatches live `/health`, breaks dashboard health check | title/body rate conflict; maintainer decides | 2026-09-08 | PIPELINE | Public report `earn/bottube-1102-js-sdk-health-contract.md`; live CI run 34266991492; direct upstream issue blocked 403; one fallback email only |
| #13949 | RustChain badge in `markabramov1993/arbitr` README | 2 RTC | 2026-09-04 | PIPELINE | **Duplicate email Sep 6 corrected by administrative dedupe notice; ONE claim only** |
| #1575 | Elyan Contributor Registry registration | 3 RTC title / 5 RTC current template | 2026-09-06 | PIPELINE | No pre-existing registry entry; maintainer must resolve canonical amount |
| #1579 | Contextual Elyan Labs tooling mention in existing `arbitr` README | 3 RTC | 2026-09-06 | PIPELINE | Commit `c43c34329ae8076d60a720ca8a65472cf6f063dc`; one claim |
| #16497 | RustChain miner dry-run long-form tutorial | 33 RTC total article tier; 13 RTC draft tranche currently requested | 2026-09-04 | PIPELINE | Sep 6 material follow-up asks only for 13 RTC draft acceptance; later publication tranche not yet eligible |
| #16497 | Beacon agent liveness + GitHub Actions long-form tutorial | 33 RTC total article tier; 13 RTC draft tranche currently requested | 2026-09-04 | PIPELINE | Copy/paste CI example fixed in `600401ec7d1eaa0c56a1b2bc6de508c28f98a787`; later publication tranche not yet eligible |
| #16601 | Type C — RIP-302 Agent Economy Shorts kit | 15 RTC | 2026-09-04 | OCCUPIED / low probability | Earlier Type C email submission by another contributor was accepted; do not follow up unless maintainer asks |
| #16601 | Type C — Beacon liveness Shorts kit | 15 RTC | 2026-09-04 | OCCUPIED / low probability | Distinct package, but same occupied Type C lane |
| #16601 | Type B — Proof-of-Antiquity YouTube script + storyboard kit | 15 RTC | 2026-09-04 | PIPELINE | Distinct package type; no acceptance evidence recovered |
| #16601 | Type D — syndication add-on for #16497 article | +8 RTC | 2026-09-04 | PIPELINE | Distinct add-on; no acceptance evidence recovered |
| #293 | Weapon SFX set | 7 RTC | 2026-09-04 | PIPELINE | Distinct per-item submission under cap |
| #293 | Background track 1 | 7 RTC | 2026-09-04 | PIPELINE | Sent in 2-track pack; distinct item |
| #293 | Background track 2 | 7 RTC | 2026-09-04 | PIPELINE | Sent in 2-track pack; distinct item |
| #293 | Announcer voice-line set | 7 RTC | 2026-09-04 | PIPELINE | Distinct per-item submission |
| #293 | Background track 3 / final capped item | 7 RTC | 2026-09-04 | PIPELINE | Fifth/final item under machine-readable cap=5 |
| #2819 | Private UTXO dual-write precision / quantization finding | Issue range 33–133 RTC; exact finding value unaccepted | 2026-09-04 | PIPELINE / PRIVATE | Do not assign a numeric receivable until severity/acceptance is explicit |
| #13953 | Azure/Microsoft GitHub-hosted VM anti-emulation self-test | 5 RTC | 2026-09-04 | PIPELINE | One environment claim; no acceptance evidence recovered |
| #398 | Security architecture assessment — Step 1 | 10 RTC | 2026-09-04 | PIPELINE | One step submission; no acceptance evidence recovered |
| #3418 | Beacon Atlas Tier A + proof of commerce | 5 RTC | 2026-09-04 | PIPELINE | One Tier A claim; no wallet receipt |
| #1109 | BoTTube first impression | 1 RTC | 2026-09-04 | PIPELINE | Already sent; **do not resubmit** |
| #1107 | BoTTube vs YouTube Shorts comparison | 3 RTC | 2026-09-04 | PIPELINE | Already sent; **do not resubmit** |
| #12442 | RustChain vs Helium / DePIN comparison | 3 RTC | 2026-09-03 | PIPELINE | Already sent; **do not resubmit** |
| #12443 | wRTC Bridge vs Cross-Chain DEX Architecture | 3 RTC | 2026-09-03 | PIPELINE | **Duplicate/follow-up emails corrected by administrative dedupe notice; ONE claim only** |
| #12444 | Proof of Antiquity vs Proof of Storage | 3 RTC | 2026-09-04 | PIPELINE | **Duplicate/follow-up emails corrected by administrative dedupe notice; ONE claim only** |
| #1112 | `/attest/submit` fuzzing report — 120 cases | **7 RTC title-authoritative** | 2026-09-04 | PIPELINE | Body later mentions 10; do not self-upgrade amount |
| #2271 | RustChain miner dry-run on Ubuntu GitHub runner | **2 RTC title-authoritative** | 2026-09-03 | PIPELINE | Already sent; body text may show a different older rate; do not resubmit |

## Administrative dedupe correction

Sent Sep 6 to `sophia.eagent@gmail.com`:

`Administrative dedupe clarification — markabramov1993 bounty submissions`

It explicitly instructs Elyan Labs to count **one claim only** for #13949, #12443 and #12444. It does **not** withdraw genuinely distinct #16497 articles or #293 per-item submissions.

## Other active non-Elyan paths

- **Mova #91 / PR #257 — ARCHIVED Sep 8** — upstream issue closed by maintainer commit `0ec1ab0ddde4cf5d880709efd423fda06f6f6862`; no acceptance/payment for our PR.
- **Mermail / Superteam — 500 USDC total prize pool** — submission filed; official PR #174 open/mergeable/no maintainer feedback at Sep 8 check.
- **Lilly batch — formerly $635 nominal** — ARCHIVED because all nine upstream tasks closed with no acceptance evidence for our fallback work.

## Mandatory pre-submit gate

Before any future Elyan/RustChain submission:

1. Search this file for the issue number.
2. Search Gmail SENT for the issue number / subject.
3. Search the public issue comments for `markabramov1993` or an on-behalf entry.
4. Confirm the issue is open, funded and the relevant winner/item slot is not occupied.
5. Only then submit once through the permitted route.

If any of steps 1–4 finds an existing claim, **stop and update the existing row instead of sending another claim**.
