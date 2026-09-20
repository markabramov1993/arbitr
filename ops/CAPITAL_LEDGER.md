# PROFIT ENGINE — Capital Ledger

Updated: **2026-09-20 live audit**

This ledger separates money actually received from receivables, open bounty pipeline and simulated trading PnL.

## 1. Confirmed capital

| Bucket | Confirmed amount | Evidence |
|---|---:|---|
| Cash / stablecoin bounty payouts | **$0** | No fiat/stablecoin payout received |
| RTC settled in RustChain wallet | **126.1 RTC** | Live wallet probe 2026-09-20: `amount_rtc: 126.1`, HTTP 200, 11 settled inbound transfers |
| DeFi execution profit | **$0** | No settled live FLASH execution |

**Important:** 126.1 RTC is real settled RustChain balance, but it is **not usable FLASH seed capital** while RustChain has no supported RTC→wRTC/Solana/USDC off-ramp. Maintainer email on Sep 14 explicitly says the off-ramp is paused/not supported.

## 2. Reconciled payout history

Live wallet history on Sep 20 returned 11 settled inbound transfers totaling **126.1 RTC**:

- 30 RTC — #315 Stage 1 asset pack
- 15 RTC — #398 Step 2 Mock Signature Mode reproduction
- 15 RTC — #16601 Type C Shorts kit
- 13 RTC — #16497 tutorial 1 draft tranche
- 13 RTC — #16497 tutorial 2 corrected draft tranche
- 10 RTC — #398 Step 1 security assessment
- 10 RTC — #13954 Proof-of-Antiquity infographic
- 10 RTC — #13224 identity-churn critique
- 5 RTC — #1102 mobile-login false-success
- 5 RTC — #1102 JS SDK health() return-type mismatch
- 0.1 RTC — #16863 contributor feedback, confirmed Sep 19

The earlier 24-hour holds have cleared. These RTC are no longer pending.

## 3. Highest-confidence remaining payout

### #16497 off-platform publication — 40 RTC
Both accepted tutorials have a further **20 RTC each** once an allowlisted off-platform Live-URL has remained live for seven days.

Accepted publication surfaces from maintainer correspondence: dev.to, Hashnode, Medium, Substack. Current bounty rules also allow an own blog on an own domain.

Publication-ready source files:
- `earn/offplatform/rustchain-miner-dryrun-publication.md`
- `earn/offplatform/beacon-liveness-publication.md`

Interactive publishing is currently blocked because the Remote Desktop device is offline and Opera Browser Connector is disconnected. Do not claim the 40 RTC until real Live-URLs exist and survive the verifier window.

## 4. Platform-backed USDG lane

### Superteam Germany — Road to Colosseum: Build your MVP
- **8,000 USDG total prize pool**
- Germany-only; user is eligible
- 10 prize places (2,000 / 1,500 / 1,100 / 800 / 650 / 500 / 450 / 400 / 350 / 250 USDG)
- Only **2 submissions** on the current listing crawl
- Winner announcement scheduled for **2026-10-09**
- ProofRoute is the primary candidate to turn into an actual Solana MVP.

This is a judged prize competition: **PIPELINE/PREPARED**, never confirmed capital until selected and paid.

### Mermail / Superteam
- 500 USDC prize pool
- Submission already filed
- Upstream PR #174 remains the code-review surface
- No prize acceptance/payment evidence yet

## 5. RustChain research lane
- #16471 payout-pipeline audit remains eligible only for genuinely new silent-success defects.
- Known duplicates must not be resubmitted.
- #1102 cap is exhausted for this contributor.
- #1575 and #1579 were already submitted through fallback; no duplicates.
- #16253 is actively claimed by another contributor; skipped.

## 6. Archived / lower probability
- Mova #91: no acceptance/payment; competing/overlapping upstream work.
- Lilly former $635 nominal batch: closed upstream without our acceptance evidence.
- Stale/occupied/scraped bounty values are not pipeline.

## 7. Capital ladder

1. **BOOTSTRAP — ACHIEVED:** 126.1 RTC has actually settled.
2. **OFF-RAMP GATE — BLOCKED:** maintainer states no supported RTC conversion path.
3. **USD/STABLECOIN SEED — $0:** only external stablecoin/fiat receipts count for FLASH trading.
4. **PAYOUT EXPANSION — ACTIVE:** pursue #16497 40 RTC, Superteam Germany 8,000 USDG pool, and new funded work.
5. **LIVE MICRO-EXECUTION:** only after usable seed exists and exact route passes deterministic current-state simulation.
6. **FLASH-LIQUIDITY EXECUTION:** only when exact execution remains net-positive after all costs.
7. **SCALE FROM REALIZED PROFIT:** never from bounty face value or paper PnL.

## 8. Accounting states

- **CONFIRMED** — actually received/settled.
- **RECEIVABLE** — explicitly accepted and payment due, not yet received.
- **PIPELINE** — submitted/open, not accepted.
- **PREPARED** — deliverable ready but not natively submitted.
- **FORK** — transaction succeeded only in simulation/fork.
- **PAPER** — calculated opportunity, not executed.
- **ARCHIVED / REJECTED / OCCUPIED** — no longer a current expected payout path.

## 9. Execution safety gate

Do not move RTC based on unsupported bridge claims, public comments, copied addresses, or unofficial swap routes. No private key/seed phrase in repo/CI. FLASH stays at **$0 usable seed** until a supported, independently verifiable liquid asset receipt exists.
