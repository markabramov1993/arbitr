# FLASH bounty / seed-capital ledger — audited 2026-09-07

Purpose: obtain **real external rewards first**. Only money/tokens actually received become FLASH seed capital. Face value, prize pools, sent emails, open PRs, bids and simulated PnL are never counted as cash.

## Headline
- **Confirmed USD/stablecoin bounty cash: $0**
- **Confirmed RTC: 0.0 RTC**
- **Confirmed DeFi profit: $0**
- RTC wallet: `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`
- Sep 7 payout/reply audit: no authoritative acceptance/payment evidence found for the active USD/stablecoin paths.
- Canonical Elyan duplicate-prevention inventory: `earn/ELYAN_SUBMISSION_INVENTORY_2026-09-06.md`.

## 1. Shortest current payout requests

### RustChain #13949 — README badge — 2 RTC
- Existing real repo: `markabramov1993/arbitr`.
- RustChain badge verified in README.
- Canonical first claim was emailed **Sep 4**.
- A duplicate Sep 6 email was discovered during SENT-mail reconciliation; an administrative dedupe notice explicitly instructs Elyan Labs to treat this as **ONE claim only**.
- **State: PIPELINE.**

### Contributor Registry #1575 — canonical 3–5 RTC ambiguity
- `markabramov1993` absent from `Scottcjn/contributors/CONTRIBUTORS.yml` when checked.
- Direct issue creation returned `403 Resource not accessible by integration`.
- Complete registration emailed Sep 6 and requested filing on our behalf.
- Issue title and current registry/template disagree on 3 vs 5 RTC, so do not select the higher number ourselves.
- **State: PIPELINE.**

### RustChain #1579 — contextual Elyan Labs mention — 3 RTC
- Existing `arbitr` repo predates the bounty and contains real original work.
- README received a dedicated contextual Elyan Labs tooling section in commit `c43c34329ae8076d60a720ca8a65472cf6f063dc`.
- Claim emailed Sep 6 through documented fallback after duplicate check.
- **State: PIPELINE; pool availability still requires maintainer acceptance.**

### RustChain #100 — Discovery Mode — 2 RTC
- First-discovery claim for `Scottcjn/beacon-skill` emailed Sep 6 after checking the canonical inventory, SENT mail and public claim history.
- Submission explains actual inspected use: persistent agent identity, Atlas liveness and signed envelopes.
- Includes RTC wallet and AI disclosure; requests maintainer filing because external GitHub write access is 403.
- **State: PIPELINE.**

### RustChain #16497 — two draft-acceptance tranches — 13 + 13 RTC
- Two long-form tutorials originally submitted Sep 4.
- Sep 6 audit found and fixed a real broken dual-stdin shell/Python example in the Beacon tutorial; fix commit `600401ec7d1eaa0c56a1b2bc6de508c28f98a787`.
- One material follow-up asks for review only of the **13 RTC draft-acceptance tranche per article** under the pre-Sep-8 submission state.
- The later 20+20 publication tranches are not claimed/receivable without qualifying Live-URLs and persistence checks.
- **State: PIPELINE.**

## 2. Mermail / Superteam — submitted competition
- Advertised prize pool: **500 USDC total**.
- Superteam entry was submitted; prior UI verification showed `Edit Submission` and one credit consumed.
- Official PR: `Nudgen-Marketing/mermail-skills#174` — Sep 7 check: **open, mergeable, no comments/reviewer feedback**.
- Companion proposal: `Nudgen-Marketing/mermail-skills#173` — Sep 7 check: open; its only comment is our own PR update, not maintainer acceptance.
- Controlled live Mermail run completed safely; no fabricated send/payment/settlement.
- **State: PIPELINE, not RECEIVABLE.**

## 3. Mova Labs #91 — live $90 path, competitive
- Issue #91 nominal bounty: **$90**.
- PR #257 remains open/mergeable at Sep 7 check.
- Sep 7 PR discussion audit: only the pre-existing Vercel bot authorization notice; **0 maintainer reviews**.
- Audit fixed a substantive flaw by explicitly pinning Soroban fixed event topics:
  - `PaymentReceived` -> `pay`
  - `OrderCreated` -> `create_order`
  - `OrderShipped` -> `dispatch`
  - `OrderRefunded` -> `refund`
- Competing PR #343 covers overlapping/broader work, so probability is reduced.
- Material update email already sent; no duplicate follow-up until new review/state change.
- **State: PIPELINE / COMPETITIVE.**

## 4. Downgraded / occupied

### Linden Lab / Second Life #4390 — our USD 750 Phase 0 bid
- Our proposal was posted Sep 6 as issue comment `5560819778`; nominal bid was **USD 750 fixed**.
- Sep 7 full comment-history audit found a decisive earlier maintainer decision that the open-issue surface alone hid:
  - contributor `@RyeMutt` had already published the vcpkg migration proposal/PoC;
  - on **2025-10-14**, RFP author/maintainer `bennettgoble` replied: **“Thanks @RyeMutt, your write up and proof of concept looks promising. Let's move forward with this proposal.”**
- Therefore the issue being `open`, unassigned, `help wanted`, and `💰 Reward` is **not sufficient evidence that the contract remains genuinely available**.
- Do not count our USD 750 bid as a live expected payout unless Linden Lab explicitly reopens procurement and invites our proposal.
- **State: OCCUPIED / STALE RFP SIGNAL.**

### RustChain #16601 Type C
- Our two Sep 4 Type C packages remain technically valid historical submissions.
- Thread history shows an earlier Type C email package was already accepted for the round.
- Therefore this is **OCCUPIED / low probability**, not the main first-payout forecast.

## 5. Archived from active expected income
### Lilly batch — formerly $635 nominal
All nine relevant Lilly issues are closed upstream as completed with no acceptance evidence for our fallback work:
- lily-contracts #321, #323, #324;
- agentlily-runtime #241, #242, #243, #247, #248, #253.

Preserve the work historically, but do not carry $635 as active pending money unless Lily/GrantFox explicitly accepts it.

## 6. Other older paths
- Mova #53 — $45 nominal; no acceptance evidence.
- Mova #60 — $50 nominal; no acceptance evidence.
- Claude Builders #1 — $50 nominal; no acceptance evidence.
- RustChain #2271 miner dry-run was already submitted Sep 3; **do not duplicate**.
- Historical RTC claims remain PIPELINE unless individually accepted and then received.

## 7. External-source audit notes
- Ubiquity/DevPool source issues with real `Price: USD` labels were verified, but attractive current tasks checked were assigned or collaborator/core-only; no speculative work started.
- Opire's old public watcher snapshot is stale and contains deleted/404 upstream issues; snapshots are not treated as current funding evidence.
- Current Opire `💰 Reward` issues were source-audited; most visible candidates are stale, contested, mirrors/tests, assigned, or require human/device-specific proof. No unsupported claim was submitted.
- Algora boards can retain “open” bounty entries after the canonical GitHub task is closed or otherwise no longer actionable; canonical issue + discussion history must be checked before work starts.
- Sep 7 high-value blockchain radar completed successfully with `MAX_NOMINAL_DISCOVERY=0` after false-positive filtering.

## 8. Security-contest lane
- ENS Immunefi audit competition is being treated as research/PoC work only until a distinct in-scope issue is reproduced locally and checked against known issues.
- Current ENS API-worker triage so far found no reportable issue: JWT/SIWE path validates domain/URI/signature; notification channel ownership checks bind operations to authenticated `user_id`; testnet wallet faucet behavior is not counted as a financial exploit.
- Intuition/0x/Origin static-analysis output is never counted as bounty evidence without a concrete local PoC and scope/known-issue check.

## 9. ProofRoute / Germany opportunities
Prepared project assets remain available for native Germany-eligible submissions when authenticated browser access returns. Any awarded grant is restricted ProofRoute project funding and is not automatically FLASH trading seed capital.

## 10. Operating rules
1. Search the canonical inventory, canonical issue state, **full maintainer discussion history**, linked PRs and SENT mail before every new claim/bid.
2. No duplicate claims or duplicate follow-up emails.
3. Prefer funded, open, unoccupied, explicit payout paths.
4. An open issue/reward label alone is not enough; prior maintainer selection/award makes a lane occupied unless explicitly reopened.
5. `CONFIRMED` requires actual receipt; `RECEIVABLE` requires explicit acceptance; bids and submissions remain PIPELINE.
6. Re-run RTC live balance/history after any acceptance/payment signal.
7. No live FLASH execution before confirmed seed capital and deterministic current-state cost-aware validation.
