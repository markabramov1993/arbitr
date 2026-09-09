# PROFIT ENGINE — Capital Ledger

Updated: **2026-09-09 live audit**

This ledger separates money actually received from receivables, submitted pipeline, prepared work and simulated trading PnL.

## 1. Confirmed capital

| Bucket | Confirmed amount | Evidence |
|---|---:|---|
| Cash / stablecoin bounty payouts | **$0** | No fiat/stablecoin payout received yet |
| RTC | **5.0 RTC** | Live RustChain probe on 2026-09-09 returned `amount_rtc: 5.0`; wallet history contains one `transfer_in` from `founder_community`, tx `b5034bc573d119c8b74c0b9773afa88c` |
| DeFi execution profit | **$0** | No settled live FLASH execution |

**CONFIRMED seed capital = 5.0 RTC + $0 fiat/stablecoin.**

The 5 RTC is the first independently verified external reward received by this project. It came from BoTTube/RustChain bounty #1102 for the JS SDK `health()` return-type mismatch. Sophia accepted it as a functional bug for 5 RTC with idempotency key `markabramov1993-1102-sdk-health-type`; public receipt exists on #1102. The subsequent live wallet check proves settlement.

Bounty labels, prize pools, sent emails, open PRs, fork results and simulated PnL are not capital.

## 2. Active submitted payout requests

| Opportunity | Face value | State |
|---|---:|---|
| BoTTube/RustChain #1102 — JS SDK `health()` type mismatch | 5 RTC | **CONFIRMED / PAID** — tx `b5034bc573d119c8b74c0b9773afa88c` |
| RustChain #13949 — README badge | 2 RTC | PIPELINE — canonical email fallback claim already sent; no duplicate |
| RustChain #1575 — Contributor Registry | 3–5 RTC canonical-rate ambiguity | PIPELINE — registration emailed through documented 403 fallback; maintainer chooses canonical amount |
| RustChain #1579 — contextual Elyan Labs README mention | 3 RTC | PIPELINE — real pre-existing `arbitr` repo updated; claim already sent |
| RustChain #100 — first Discovery Mode claim | 2 RTC | PIPELINE — Beacon Skill discovery claim already sent |
| RustChain #16497 — two article draft-acceptance tranches | 13 + 13 RTC | PIPELINE — two Sep 4 submissions; one material follow-up asks only for draft acceptance |
| Mermail / Superteam | 500 USDC total prize pool | PIPELINE — Superteam email confirms submission received on Sep 9; upstream PR #174 remains open and mergeable with no maintainer comments |

## 3. Downgraded / archived

- **Mova Store #91 / $90:** issue was closed as completed by maintainer on 2026-09-08 via upstream work that is not our PR. Our PR #257 remains open but no acceptance/payment exists. **ARCHIVED / CLOSED ELSEWHERE** unless maintainer explicitly revives or separately pays our work.
- **RustChain #16601 Type C packages:** technically valid historical submissions, but thread evidence shows an earlier Type C email package was already accepted. **OCCUPIED / low probability**.
- **Lilly batch — formerly $635 nominal:** all nine relevant upstream issues are closed as completed with no acceptance evidence for our fallback work. **ARCHIVED**.
- Stale mirrored bounty values, assigned work and duplicate winner slots are not pipeline.

## 4. Capital ladder

1. **BOOTSTRAP — ACHIEVED:** first external reward settled: 5 RTC.
2. **RING-FENCE:** keep confirmed RTC separate from nominal bounty values.
3. **GAS/CONVERSION CHECK:** do not assume RTC is directly usable as EVM/Solana gas or liquid trading capital; only deploy where conversion/liquidity and costs are independently verified.
4. **LIVE MICRO-EXECUTION:** only after deterministic current-state simulation with fees, gas and slippage.
5. **FLASH-LIQUIDITY EXECUTION:** only when exact execution remains net-positive under conservative assumptions.
6. **SCALE FROM REALIZED PROFIT:** never from bounty face value or paper PnL.

## 5. Accounting states

- **CONFIRMED** — money/token actually received or settled on-chain.
- **RECEIVABLE** — explicitly accepted/merged and payment is due, but not received.
- **PIPELINE** — submitted/open, not accepted.
- **PREPARED** — deliverable/application ready but not yet natively submitted.
- **FORK** — transaction succeeded only in simulation/fork.
- **PAPER** — calculated opportunity, not executed.
- **ARCHIVED / REJECTED / OCCUPIED** — no longer a current expected payout path.

## 6. Execution safety gate

Confirmed capital now exists, but **5 RTC alone does not authorize a live FLASH trade**. Before any live execution, verify that the asset can be safely converted/used for gas, quantify conversion cost/liquidity, and re-run the exact strategy against current chain state with conservative fees/slippage and bounded failure loss. No private key/seed phrase in repo/CI; no fabricated users, wash volume, duplicate identities or prohibited activity.
