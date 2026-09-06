# FLASH bounty / seed-capital ledger — audited 2026-09-06

Purpose: obtain **real external rewards first**. Only money/tokens actually received become FLASH seed capital. Face value, prize pools, sent emails, open PRs, bids and simulated PnL are never counted as cash.

## Headline
- **Confirmed USD/stablecoin bounty cash: $0**
- **Confirmed RTC: 0.0 RTC**
- **Confirmed DeFi profit: $0**
- RTC wallet: `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`
- Sep 6 live probe: balance HTTP 200 / `amount_rtc: 0.0`; history HTTP 200 / **0 transactions**.
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

## 2. Linden Lab / Second Life — USD 750 Phase 0 bid

- Official source: `secondlife/viewer#4390` — **RFP: Replace Autobuild with Modern Dependency Management System**.
- Source issue is open, unassigned, `help wanted`, and carries the repository's `💰 Reward` label.
- Maintainer explicitly states the contract is open for proposals/bids in USD.
- Current Viewer source was inspected before bidding; active Autobuild coupling and the existing optional Conan path were verified.
- Public proposal: `earn/secondlife-autobuild-rfp/PHASE0_PROPOSAL.md`, commit `80361e1fc5c32b259bb712c6c39d3e9d01945b3a`.
- Official issue bid posted successfully Sep 6 as comment **5560819778**.
- Bid: **USD 750 fixed** for a bounded Phase 0: dependency/coupling inventory, Conan 2 `llcommon` PoC, Windows/macOS CI evidence, Linux smoke where applicable, measurements, Conan-vs-vcpkg analysis, TPV override design, and staged migration/risk plan.
- Payment proposed on Phase 0 acceptance; no upfront payment requested.
- **State: BID / PIPELINE. USD 750 is not RECEIVABLE until Linden Lab accepts the proposal/contract.**

## 3. Mermail / Superteam — submitted competition
- Advertised prize pool: **500 USDC total**.
- Superteam entry was submitted; prior UI verification showed `Edit Submission` and one credit consumed.
- Official PR: `Nudgen-Marketing/mermail-skills#174` — latest Sep 6 check: open, no maintainer feedback.
- Companion proposal: `Nudgen-Marketing/mermail-skills#173` — no maintainer reply at latest check.
- Controlled live Mermail run completed safely; no fabricated send/payment/settlement.
- **State: PIPELINE, not RECEIVABLE.**

## 4. Mova Labs #91 — live $90 path, competitive
- Issue #91 nominal bounty: **$90**.
- PR #257 remains open/mergeable at latest Sep 6 check.
- Audit fixed a substantive flaw by explicitly pinning Soroban fixed event topics:
  - `PaymentReceived` -> `pay`
  - `OrderCreated` -> `create_order`
  - `OrderShipped` -> `dispatch`
  - `OrderRefunded` -> `refund`
- Competing PR #343 covers overlapping/broader work.
- Material update email already sent; no duplicate follow-up until new review/state change.
- **State: PIPELINE.**

## 5. Downgraded / occupied
### RustChain #16601 Type C
- Our two Sep 4 Type C packages remain technically valid historical submissions.
- Thread history shows an earlier Type C email package was already accepted for the round.
- Therefore this is **OCCUPIED / low probability**, not the main first-payout forecast.

## 6. Archived from active expected income
### Lilly batch — formerly $635 nominal
All nine relevant Lilly issues are closed upstream as completed with no acceptance evidence for our fallback work:
- lily-contracts #321, #323, #324;
- agentlily-runtime #241, #242, #243, #247, #248, #253.

Preserve the work historically, but do not carry $635 as active pending money unless Lily/GrantFox explicitly accepts it.

## 7. Other older paths
- Mova #53 — $45 nominal; no acceptance evidence.
- Mova #60 — $50 nominal; no acceptance evidence.
- Claude Builders #1 — $50 nominal; no acceptance evidence.
- RustChain #2271 miner dry-run was already submitted Sep 3; **do not duplicate**.
- Historical RTC claims remain PIPELINE unless individually accepted and then received.

## 8. External-source audit notes
- Ubiquity/DevPool source issues with real `Price: USD` labels were verified, but attractive current tasks checked were assigned or collaborator/core-only; no speculative work started.
- Opire's old public watcher snapshot is stale (Apr 15) and contains deleted/404 upstream issues; snapshots are not treated as current funding evidence.
- Current Opire `💰 Reward` issues were source-audited; most visible candidates are stale, contested, mirrors/tests, assigned, or require human/device-specific proof. No unsupported claim was submitted.
- Algora current board did not surface a strong open target worth diverting from the active queue.

## 9. ProofRoute / Germany opportunities
Prepared project assets remain available for native Germany-eligible submissions when authenticated browser access returns. Any awarded grant is restricted ProofRoute project funding and is not automatically FLASH trading seed capital.

## 10. Operating rules
1. Search the canonical inventory, issue state/comments and SENT mail before every new claim.
2. No duplicate claims or duplicate follow-up emails.
3. Prefer funded, open, unoccupied, explicit payout paths.
4. `CONFIRMED` requires actual receipt; `RECEIVABLE` requires explicit acceptance; bids and submissions remain PIPELINE.
5. Re-run RTC live balance/history after any acceptance/payment signal.
6. No live FLASH execution before confirmed seed capital and deterministic current-state cost-aware validation.
