# PROFIT ENGINE — Capital Ledger

Updated: **2026-09-06 live audit**

This ledger separates money actually received from receivables, submitted pipeline, prepared work and simulated trading PnL.

## 1. Confirmed capital

| Bucket | Confirmed amount | Evidence |
|---|---:|---|
| Cash / stablecoin bounty payouts | **$0** | No accepted payment/transfer recovered |
| RTC | **0.0 RTC** | Sep 6 RustChain live probe returned `amount_rtc: 0.0` and wallet history count `0` for `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d` |
| DeFi execution profit | **$0** | No settled live FLASH execution |

**CONFIRMED seed capital = $0 + 0.0 RTC.**

Bounty labels, prize pools, sent emails, open PRs, fork results and simulated PnL are not capital.

## 2. Closest submitted payout requests

| Opportunity | Face value | State |
|---|---:|---|
| RustChain #13949 — README badge | 2 RTC | PIPELINE — clean claim emailed Sep 6; repo and no-prior-claim state verified |
| RustChain #1575 — Contributor Registry | 3–5 RTC canonical-rate ambiguity | PIPELINE — no existing registry entry; direct issue write 403; complete registration emailed via documented fallback |
| RustChain #1579 — contextual Elyan Labs README mention | 3 RTC | PIPELINE — real pre-existing `arbitr` repo updated; claim emailed Sep 6 |
| RustChain #100 — first Discovery Mode claim | 2 RTC | PIPELINE — Beacon Skill discovery claim emailed Sep 6 after duplicate check |
| RustChain #16497 — two article draft-acceptance tranches | 13 + 13 RTC | PIPELINE — two Sep 4 submissions; material Sep 6 follow-up asks only for draft acceptance; no reply yet |
| Mova Store #91 / PR #257 | $90 | PIPELINE — open/mergeable; explicit Soroban topic fix added; competing PR #343 exists |
| Mermail / Superteam | 500 USDC total prize pool | PIPELINE — entry submitted; PR #174 open; judged competition, not a receivable |

## 3. Downgraded / archived

- **RustChain #16601 Type C packages:** technically valid historical submissions, but thread evidence shows an earlier Type C email package was already accepted for the round. Treat our Type C lane as **OCCUPIED / low probability**, not a primary payout forecast.
- **Lilly batch — formerly $635 nominal:** all nine relevant upstream issues are closed as completed with no acceptance evidence for our fallback work. **ARCHIVED** unless a maintainer explicitly reopens/accepts it.
- Stale mirrored bounty values, assigned work and duplicate winner slots are not pipeline.

## 4. Capital ladder

1. **BOOTSTRAP** — zero-capital, funded external work only.
2. **CONFIRM RECEIPT** — independently verify the first token/cash arrival.
3. **GAS RESERVE** — ring-fence confirmed crypto/stablecoin for execution costs.
4. **LIVE MICRO-EXECUTION** — only after deterministic current-state simulation with fees, gas and slippage.
5. **FLASH-LIQUIDITY EXECUTION** — only when exact execution remains net-positive under conservative assumptions.
6. **SCALE FROM REALIZED PROFIT** — never from bounty face value or paper PnL.

## 5. Accounting states

- **CONFIRMED** — money/token actually received or settled on-chain.
- **RECEIVABLE** — explicitly accepted/merged and payment is due, but not received.
- **PIPELINE** — submitted/open, not accepted.
- **PREPARED** — deliverable/application ready but not yet natively submitted.
- **FORK** — transaction succeeded only in simulation/fork.
- **PAPER** — calculated opportunity, not executed.
- **ARCHIVED / REJECTED / OCCUPIED** — no longer a current expected payout path.

## 6. Execution safety gate

No live FLASH transaction until confirmed capital exists and the exact current-state route has deterministic simulation, conservative gas/fees/slippage, bounded failure loss and positive net outcome. No private key/seed phrase in repo/CI; no fabricated users, wash volume, duplicate identities or prohibited activity.
