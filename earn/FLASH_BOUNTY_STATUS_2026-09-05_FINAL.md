# FLASH bounty status — audited 2026-09-10

## Capital truth
- Confirmed USD/stablecoin bounty cash: **$0**.
- Confirmed RTC: **5.0 RTC** in `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`.
- Sep 10 22:48 CEST live RustChain probe: balance HTTP 200 / `amount_rtc: 5.0`; history HTTP 200 / **1 transaction**.
- Confirmed tx: `b5034bc573d119c8b74c0b9773afa88c`, **5 RTC inbound from `founder_community`**.
- This is settled/received external reward capital. Bounty face values, prize pools, emails and simulated PnL are not capital.

## First paid bounty — #1102
- Finding: official BoTTube JS/TS SDK typed `health()` as `{status, timestamp}` while live `/health` returns `{ok, service, version, uptime_s, videos, agents, humans}`.
- Sophia Elya independently confirmed the source/live mismatch and accepted it as a **functional bug**.
- Amount: **5 RTC**.
- Idempotency key: `markabramov1993-1102-sdk-health-type`.
- Live wallet history proves settlement.
- **Accounting: CONFIRMED / PAID.**

## #1102 second/final item — duplicate-cap correction
Two different reports had accidentally been sent as a “second” item under the two-item contributor cap:
1. Sep 9 — JS SDK `getTrending()` response-contract mismatch.
2. Sep 10 — official mobile client login stores an API key and reports authenticated state after querying a public agent endpoint without validating that key.

A correction email was sent on Sep 10: **keep the mobile-login report as the second/final #1102 item and withdraw/disregard the earlier `getTrending()` report for payout purposes.** Do not send any more #1102 claims for this contributor unless the maintainer explicitly reopens capacity.

Current state of mobile-login report: **SUBMITTED / awaiting verification**, requested functional tier **5 RTC**. No acceptance/payment claimed yet.

## Mermail / Superteam — submitted
- Advertised prize pool: **500 USDC total**.
- Superteam sent `Submission Received!` on 2026-09-09 for `Build and Demo a Mermail Agent Skill`.
- Official PR #174 remains the review artifact.
- Accounting: **PIPELINE**, not receivable/confirmed.

## Other payout requests already in queue
- **#13949 — 2 RTC:** badge claim already sent; do not duplicate.
- **#1575 — registration reward:** already submitted; await canonical maintainer rate/acceptance.
- **#1579 — 3 RTC:** contextual Elyan Labs mention claim already sent.
- **#100 — 2 RTC:** Discovery Mode claim already sent.
- **#16497 — two tutorial acceptance tranches:** follow-up already sent; do not spam inside review window.

## Archived / lower probability
- Mova #91: closed elsewhere; our PR has no acceptance/payment evidence.
- RustChain #16601 Type C lane: earlier Type C slot was already accepted for another submission; our old Type C packages are low probability.
- Lilly batch: closed upstream with no acceptance evidence for our fallback work.

## Device / browser
- Remote Desktop Commander check on Sep 10 22:49 CEST: `DESKTOP-87DF3OM` is **offline** (last seen Sep 9 21:39 UTC; auth token still valid).
- Do not depend on local browser/desktop automation until the device reconnects.

## Current order
1. Treat the settled **5 RTC** as confirmed capital, separate from USD/stablecoin cash.
2. Wait for verification of the mobile-login #1102 report; no more #1102 submissions under the cap.
3. Watch #13949 / #1575 / #1579 / #100 / #16497 for acceptance or payout without duplicate follow-ups.
4. Monitor Mermail/Superteam judging and upstream PR #174.
5. Add only funded, open, unoccupied, zero-capital work after GitHub + SENT-mail duplicate checks.
