# FLASH bounty status — audited 2026-09-06

## Capital truth
- Confirmed USD/stablecoin bounty cash: **$0**.
- RTC: live wallet probe refreshed on Sep 6; use the resulting RustChain balance/history as the only authority for confirmed RTC.
- Bounty face values, prize pools, closed fallback work and simulated PnL are not capital.

## Mermail / Superteam — submitted
- Advertised prize pool: **500 USDC**.
- Superteam entry was submitted and previously verified by the UI showing `Edit Submission`; one credit was consumed.
- Official PR: https://github.com/Nudgen-Marketing/mermail-skills/pull/174 — open, mergeable, no maintainer review yet.
- Demo video: https://x.com/LeadsOleg/status/2096249643604570579
- Tagged X post: https://x.com/LeadsOleg/status/2096354167971271154
- Controlled Mermail run completed successfully; malicious prompt-injection/payment instructions were rejected and reward state stayed opportunity-only.
- Accounting: **PIPELINE**, not receivable/confirmed.

## RustChain — closest explicit pay-on-acceptance queue
- Official #16601 is open and states review within 7 days; accepted packages are paid.
- Type C RIP-302 package and Type C Beacon-liveness package were submitted by email on Sep 4 and re-audited Sep 6 against the current source and bounty requirements.
- RTC wallet: `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`.
- External GitHub App comments currently return 403, so the existing email submissions remain the valid submission records; do not duplicate-email during the stated review window.

## Mova #91 — live but competitive
- Nominal bounty: **$90**.
- PR #257: open, mergeable.
- Sep 6 audit found the original branch did not actually pin the short event symbols expected by the JS indexer.
- Branch corrected to explicit Soroban fixed topics: `pay`, `create_order`, `dispatch`, `refund`; PR now has 2 commits / 2 changed files.
- Competing PR #343 exists with overlapping/broader work. Keep this as PIPELINE, not near-certain payment.

## Lilly batch — archived, not active money
The nine Lilly issues formerly totaling **$635 nominal** are now all closed upstream as completed, with no evidence that our fallback branches/emails were accepted. Preserve the work historically, but remove the $635 from active expected income unless Lilly/GrantFox explicitly replies with acceptance/payment.

## ProofRoute
- Germany Ideathon package and pitch are prepared.
- A Germany grant application draft requests 5,000 USDG against project milestones.
- These are future platform submissions; grant funds, if awarded, are restricted ProofRoute project funding and are not FLASH trading seed capital.

## Current order
1. Verify live RTC balance/history.
2. Push already-submitted RustChain work through review without spam or duplicate claims.
3. Monitor/respond to Mova #257 and Mermail #174.
4. Native-submit ProofRoute when authenticated browser access returns.
5. Add new funded tasks only when they improve expected payout time/quality.
