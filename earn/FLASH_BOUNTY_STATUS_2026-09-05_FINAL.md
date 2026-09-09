# FLASH bounty status — audited 2026-09-09

## Capital truth
- Confirmed USD/stablecoin bounty cash: **$0**.
- Confirmed RTC: **5.0 RTC** in `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`.
- Sep 9 live RustChain probe: balance HTTP 200 / `amount_rtc: 5.0`; history HTTP 200 / **1 transaction**.
- Confirmed tx: `b5034bc573d119c8b74c0b9773afa88c`, 5 RTC inbound from `founder_community`.
- This is the first real external reward received by the project.
- Bounty face values, prize pools, emails, closed fallback work and simulated PnL are not capital.

## First paid bounty — #1102
- Finding: official BoTTube JS/TS SDK typed `health()` as `{status, timestamp}` while live `/health` returns `{ok, service, version, uptime_s, videos, agents, humans}`.
- Sophia independently confirmed the live endpoint and source contract mismatch.
- Accepted as a **functional bug**, amount **5 RTC**.
- Idempotency key: `markabramov1993-1102-sdk-health-type`.
- Public receipt was filed on `Scottcjn/rustchain-bounties#1102` naming `@markabramov1993`.
- Live wallet history now proves settlement.
- **Accounting: CONFIRMED / PAID.**

## Closest current payout requests
- **#13949 — 2 RTC:** canonical badge claim already sent through the documented fallback; do not duplicate.
- **#1575 — 3–5 RTC canonical rate:** registration sent; maintainer must choose the canonical current amount.
- **#1579 — 3 RTC:** contextual Elyan Labs tooling section added to existing `arbitr`; claim sent.
- **#100 — 2 RTC:** first Discovery Mode claim for Beacon Skill sent after duplicate checks.
- **#16497 — 13 + 13 RTC draft acceptance:** two Sep 4 tutorials; follow-up requests only the draft-acceptance tranche for each.

## Mermail / Superteam — submitted
- Advertised prize pool: **500 USDC total**.
- Superteam sent a fresh `Submission Received!` confirmation on 2026-09-09 for `Build and Demo a Mermail Agent Skill`.
- Official PR #174 remains open and mergeable; no maintainer comments/reviews at latest check.
- Companion issue #173 has no maintainer response beyond our own implementation link.
- Accounting: **PIPELINE**, not receivable/confirmed.

## Mova #91 — archived
- Nominal bounty was **$90**.
- Issue #91 was closed as completed by maintainer on 2026-09-08 through upstream work that is not our commit/PR.
- Our PR #257 remains open but has no acceptance/payment evidence and is no longer worth rebasing unless the maintainer explicitly requests or separately values our event-prefix work.
- Accounting: **ARCHIVED / CLOSED ELSEWHERE**.

## RustChain #16601 — occupied / downgraded
- Our two Sep 4 Type C packages remain useful historical work.
- Thread history shows an earlier Type C email submission was already accepted for the round.
- Accounting: **OCCUPIED / low probability**.

## Lilly — archived
All nine Lilly issues formerly summarized as **$635 nominal** are closed upstream as completed with no acceptance evidence for our fallback work. They are not active expected income.

## Device / browser
- Remote Desktop Commander now lists `DESKTOP-87DF3OM` as **online**, so the registration blocker is materially improved.
- However, current ping/process attempts time out; do not assume live GUI control until the device actually answers a command.

## Current order
1. Preserve the first 5 RTC as confirmed capital; do not confuse it with USD/stablecoin cash.
2. Watch/respond to #13949 / #1575 / #1579 / #100 / #16497 without duplicate submissions.
3. Monitor Mermail #174 and Superteam judging.
4. Stop spending time on Mova #91 unless a maintainer explicitly reopens the path.
5. Add only funded, open, unoccupied, zero-capital work after GitHub + SENT-mail duplicate checks.
