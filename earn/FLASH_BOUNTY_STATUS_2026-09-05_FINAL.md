# FLASH bounty status — audited 2026-09-06

## Capital truth
- Confirmed USD/stablecoin bounty cash: **$0**.
- Confirmed RTC: **0.0 RTC** in `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`.
- Sep 6 live RustChain probe: balance HTTP 200 / `amount_rtc: 0.0`; history HTTP 200 / **0 transactions**.
- Bounty face values, prize pools, emails, closed fallback work and simulated PnL are not capital.

## Closest current payout requests
- **#13949 — 2 RTC:** badge claim emailed Sep 6 after verifying the real `arbitr` README and no prior `markabramov1993` claim.
- **#16497 — 13 RTC + 13 RTC draft-acceptance:** two long-form tutorials were filed Sep 4. A Sep 6 follow-up requests only the draft-acceptance tranche under the pre-Sep-8 state. The Beacon tutorial was corrected before follow-up to remove a broken dual-stdin redirection example.
- **#1579 — 3 RTC:** contextual RustChain mention added to the existing `arbitr` README in commit `c43c34329ae8076d60a720ca8a65472cf6f063dc`; claim emailed through the documented 403 fallback.
- **#1575 Contributor Registry — 3/5 RTC depending canonical rate:** no existing registry/issue match; direct registration issue creation returned 403, so the complete registration was emailed with a request to file it on our behalf. No amount is counted until accepted.

## Mermail / Superteam — submitted
- Advertised prize pool: **500 USDC**.
- Superteam entry submitted; prior UI showed `Edit Submission` and one credit consumed.
- Official PR #174: open, mergeable, no maintainer review/comments.
- Controlled live Mermail run passed the intended safety behavior.
- Accounting: **PIPELINE**, not receivable/confirmed.

## Mova #91 — live but competitive
- Nominal bounty: **$90**.
- PR #257 open and mergeable.
- Sep 6 audit corrected a real weakness: the branch now explicitly pins Soroban fixed event topics `pay`, `create_order`, `dispatch`, `refund` instead of relying on struct-name defaults.
- Competing PR #343 exists with overlapping/broader work.
- Accounting: **PIPELINE**.

## RustChain #16601 — downgrade Type C expectation
- Our two Sep 4 Type C packages remain valid historical submissions.
- Thread history shows an earlier email Type C was already accepted for the round, so this lane is **occupied / low-probability** and should not be used as the main first-payout forecast.

## Lilly — archived
All nine Lilly issues formerly summarized as **$635 nominal** are closed upstream as completed with no acceptance evidence for our fallback work. They are not active expected income.

## ProofRoute
- Germany Ideathon README/PITCH and grant application are prepared.
- Native submission remains browser-dependent.
- Any grant award is restricted ProofRoute project funding, not FLASH trading seed capital.

## Current order
1. Monitor wallet + email for #13949 / #16497 / #1579 / #1575 acceptance or payout.
2. Respond immediately to real maintainer questions; do not spam duplicate claims.
3. Monitor Mova #257 and Mermail #174.
4. Native-submit ProofRoute when authenticated browser access returns.
5. Add only new funded, unoccupied, zero-capital tasks with a better expected payout path.
