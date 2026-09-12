# PROFIT ENGINE — Capital Ledger

Updated: **2026-09-12 live audit**

This ledger separates money actually received from receivables, pending settlement, open bounty pipeline and simulated trading PnL.

## 1. Confirmed capital

| Bucket | Confirmed amount | Evidence |
|---|---:|---|
| Cash / stablecoin bounty payouts | **$0** | No fiat/stablecoin payout received yet |
| RTC spendable/settled | **5.0 RTC** | Live RustChain probe on 2026-09-12 13:19 UTC returned `amount_rtc: 5.0`; confirmed transfer `b5034bc573d119c8b74c0b9773afa88c` |
| DeFi execution profit | **$0** | No settled live FLASH execution |

**CONFIRMED seed capital right now = 5.0 RTC + $0 fiat/stablecoin.**

## 2. Paid but still in RustChain 24-hour hold

Sophia Elya adjudicated the Sep 9–11 batch and explicitly reported **121 RTC paid** to `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`, subject to the network's 24-hour hold.

The 2026-09-12 13:19 UTC live probe independently shows **nine pending inbound transfers totaling 121 RTC** from `founder_community`; current spendable balance is still 5 RTC.

| Source | RTC | Current state |
|---|---:|---|
| #315 Stage 1 asset pack | 30 | PAID / pending hold |
| #398 Step 2 Mock Signature Mode reproduction | 15 | PAID / pending hold |
| #16601 Type C Shorts kit | 15 | PAID / pending hold |
| #16497 tutorial 1 draft tranche | 13 | PAID / pending hold |
| #16497 tutorial 2 draft tranche | 13 | PAID / pending hold |
| #398 Step 1 security assessment | 10 | PAID / pending hold |
| #13954 Proof-of-Antiquity infographic | 10 | PAID / pending hold |
| #13224 identity-churn critique | 10 | PAID / pending hold |
| #1102 mobile login false-success | 5 | PAID / pending hold |

**Pending settlement total = 121 RTC.** If all nine holds clear normally, spendable RTC should become **126 RTC**. Do not count the 121 as confirmed spendable capital until the wallet balance/history changes from `pending`.

The pending transfers were created around 2026-09-11 16:18–16:20 CEST, so the 24-hour hold should expire around 2026-09-12 16:18–16:20 CEST. Re-query after that window.

## 3. Remaining active payout paths

| Opportunity | Face value | State |
|---|---:|---|
| #16497 tutorial 1 live-publication tranche | 20 RTC | AVAILABLE after allowlisted off-platform article stays live 7 days |
| #16497 tutorial 2 live-publication tranche | 20 RTC | AVAILABLE after allowlisted off-platform article stays live 7 days |
| #1575 Contributor Registry | 3–5 RTC rate ambiguity | PIPELINE — email fallback already sent; do not duplicate |
| #1579 contextual Elyan Labs README mention | 3 RTC | PIPELINE — email fallback already sent |
| #13949 README badge | 2 RTC | PIPELINE — prior claim already sent |
| #100 Discovery Mode | 2 RTC | PIPELINE — prior claim already sent |
| Mermail / Superteam | 500 USDC prize pool | PIPELINE — submitted; PR #174 open/mergeable |

The #1102 contributor cap is exhausted: the first 5 RTC item is confirmed and the second 5 RTC item is in the 121 RTC paid batch. Do not submit additional #1102 claims unless maintainers explicitly reopen capacity.

## 4. Downgraded / archived

- **Mova Store #91 / $90:** issue completed via other upstream work; our PR #257 has no acceptance/payment. ARCHIVED unless maintainer explicitly revives it.
- **Lilly batch formerly $635 nominal:** closed elsewhere with no acceptance evidence. ARCHIVED.
- Stale mirrored bounty values and occupied/assigned tasks are not pipeline.

## 5. Capital usability / conversion gate

Native RTC is not automatically liquid EVM capital. RustChain documentation has bridge/swap surfaces, but a verified user-controlled conversion path, liquidity quote, gas requirement and slippage economics are still required before treating RTC as usable FLASH trading capital.

The 5 spendable RTC remains ring-fenced. The 121 pending RTC remains non-spendable until the hold clears.

## 6. Capital ladder

1. **BOOTSTRAP — ACHIEVED:** first external reward settled: 5 RTC.
2. **PAYOUT ACCUMULATION — ACTIVE:** 121 RTC paid and in network hold.
3. **CONFIRM RELEASE:** verify wallet reaches 126 RTC and pending records settle.
4. **CONVERSION CHECK:** verify an actual user-accessible bridge/swap route and total economics.
5. **LIVE MICRO-EXECUTION:** only after deterministic current-state simulation with fees, gas and slippage.
6. **FLASH-LIQUIDITY EXECUTION:** only when exact execution remains net-positive under conservative assumptions.
7. **SCALE FROM REALIZED PROFIT:** never from bounty face value or paper PnL.

## 7. Accounting states

- **CONFIRMED** — money/token actually spendable/received or settled on-chain.
- **PAID / HOLD** — maintainer sent it and wallet history shows a pending transfer, but it is not spendable yet.
- **RECEIVABLE** — explicitly accepted and payment is due, but no transfer is visible yet.
- **PIPELINE** — submitted/open, not accepted.
- **PREPARED** — deliverable ready but not submitted.
- **FORK** — transaction succeeded only in simulation/fork.
- **PAPER** — calculated opportunity, not executed.
- **ARCHIVED / REJECTED / OCCUPIED** — no longer a current expected payout path.

## 8. Execution safety gate

Confirmed capital exists, but native RTC requires a verified conversion/use path before it can fund FLASH execution. No private key/seed phrase in repo/CI; no fabricated users, wash volume, duplicate identities or prohibited activity. Every live transaction requires independently verified asset usability, current-state economics and bounded failure loss.
