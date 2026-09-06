# PROFIT ENGINE — Capital Ledger

Updated: **2026-09-06 audit**

This ledger separates money actually received from receivables, open bounty pipeline and simulated trading PnL.

## 1. Confirmed capital

| Bucket | Confirmed amount | Evidence rule |
|---|---:|---|
| Cash / stablecoin bounty payouts | **$0 confirmed** | Actual transfer, platform payout, or independently verifiable receipt only |
| RTC | **LIVE PROBE REQUIRED** | RustChain wallet balance/history for `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d` only |
| DeFi execution profit | **$0 confirmed** | Settled on-chain net profit after all costs only |

Bounty labels, prize pools, emails sent, merged-looking simulations and fork PnL are not capital.

## 2. Active external earning pipeline

| Opportunity | Face value | State | Capital? |
|---|---:|---|---|
| RustChain #16601 — two distinct Type C packages | 15 RTC + 15 RTC | Submitted by allowed email route Sep 4; audited valid Sep 6; official review SLA 7 days | PIPELINE |
| Mova Store #91 / PR #257 | $90 | Open/mergeable; Sep 6 branch corrected to explicit Soroban event-topic symbols; competing PR #343 exists | PIPELINE |
| Mermail / Superteam | 500 USDC prize pool | Superteam entry submitted; upstream PR #174 open/mergeable; judged competition | PIPELINE |
| Other RTC claims | mixed RTC | Submitted; acceptance/payment evidence not yet recovered | PIPELINE |
| ProofRoute Germany opportunities | 3,000 USDG Ideathon pool / grant request 5,000 USDG | Prepared; native platform submission pending browser access | NOT YET SUBMITTED / restricted if grant |

## 3. Removed from active expected income

- **Lilly batch — formerly $635 nominal:** all nine relevant upstream issues are now closed as completed with no acceptance evidence for our fallback work. Historical work only unless maintainers explicitly revive/accept it.
- Stale mirrored bounty values and occupied/assigned tasks are not pipeline.

## 4. Capital ladder

1. **BOOTSTRAP** — zero-cost bounties, grants, public CI/RPC and reproducible work.
2. **CONFIRM RECEIPT** — verify cash/stablecoin/token arrival independently.
3. **GAS RESERVE** — ring-fence first confirmed crypto/stablecoin funds for execution costs.
4. **LIVE MICRO-EXECUTION** — only tiny controlled notional after deterministic simulation and full cost model.
5. **FLASH-LIQUIDITY EXECUTION** — only when current-state execution remains positive under conservative fees/slippage/gas.
6. **SCALE FROM REALIZED PROFIT** — never from bounty face value or paper PnL.

## 5. Accounting states

- **CONFIRMED** — money/token actually received or settled on-chain.
- **RECEIVABLE** — explicitly accepted/merged and payment is due, but not received.
- **PIPELINE** — submitted/open, not accepted.
- **PREPARED** — deliverable/application ready but not yet natively submitted.
- **FORK** — transaction succeeded only in simulation/fork.
- **PAPER** — calculated opportunity, not executed.
- **ARCHIVED / REJECTED / OCCUPIED** — no longer a current expected payout path.

The headline must always show CONFIRMED separately from every other state.

## 6. Execution safety gates

No live FLASH transaction until there is confirmed capital and the exact current-state route has deterministic simulation, conservative gas/fees/slippage, bounded failure loss, and positive net outcome. No private key/seed phrase in repo/CI; no fabricated users, wash volume, duplicate identities or prohibited activity.
