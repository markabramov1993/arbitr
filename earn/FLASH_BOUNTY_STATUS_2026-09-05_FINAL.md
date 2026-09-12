# FLASH bounty status — audited 2026-09-12

## Capital truth
- Confirmed USD/stablecoin bounty cash: **$0**.
- Confirmed spendable RTC: **5.0 RTC** in `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`.
- Paid but still under RustChain 24-hour hold: **121 RTC** across 9 inbound transfers.
- Current live probe (2026-09-12 13:19 UTC): balance HTTP 200 / `amount_rtc: 5.0`; history HTTP 200 / 10 transactions.
- If all pending transfers clear normally, spendable total should become **126 RTC** after approximately 16:20 CEST on Sep 12.
- Bounty face values, prize pools and simulated PnL remain separate from capital.

## 121 RTC adjudicated batch — PAID / HOLD
Sophia Elya confirmed all nine Sep 9–11 awards were paid to the wallet with a 24-hour hold. The wallet independently shows matching pending transfers:

- 30 RTC — #315 Stage 1 asset pack.
- 15 RTC — #398 Step 2 Mock Signature Mode reproduction.
- 15 RTC — #16601 Type C Shorts kit.
- 13 RTC — #16497 tutorial 1 draft tranche.
- 13 RTC — #16497 tutorial 2 draft tranche.
- 10 RTC — #398 Step 1 security assessment.
- 10 RTC — #13954 Proof-of-Antiquity infographic.
- 10 RTC — #13224 identity-churn critique.
- 5 RTC — #1102 mobile-login false-success (second/final item under contributor cap).

Do not mark these 121 RTC as spendable until a post-hold wallet probe confirms settlement.

## Already confirmed before this batch
- #1102 JS SDK `health()` return-type mismatch: **5 RTC CONFIRMED / PAID**.
- Confirmed tx: `b5034bc573d119c8b74c0b9773afa88c`.

## #16497 remaining upside — publication package READY
Each accepted tutorial still has a further **20 RTC** tranche available after an allowlisted off-platform Live-URL (dev.to, Hashnode, Medium, or Substack) remains live for seven days.

Potential remaining #16497 value: **40 RTC**.

Publication-ready versions are now committed:
- `earn/offplatform/rustchain-miner-dryrun-publication.md`
- `earn/offplatform/beacon-liveness-publication.md`

They are not claimed as live publications yet. Browser/account access is required to publish them on an allowlisted host; after publication, record each Live-URL and wait the full seven-day verifier window before claiming the remaining 20+20 RTC.

## #398 Step 3 private security research
A private report was sent about missing banned-account enforcement in wRTC bridge authentication. A second routing audit found the originally cited `wrtc_bridge.py` path is legacy/unregistered and the currently registered Solana/Base bridge blueprints are globally disabled by HTTP-410 compliance guards.

A corrective addendum was immediately sent to Sophia: **no current production exploitability is asserted**. The registered bridge auth helpers still omit the `is_banned` predicate, so this is at most a latent authorization defect if those bridges are re-enabled. Do not count the 75 RTC Step 3 reward unless maintainers independently accept a valid previously unknown finding.

## Mermail / Superteam
- Prize pool: **500 USDC**.
- Submission is filed.
- Official PR #174 remains open and mergeable; latest check shows no maintainer conversation comments.
- Accounting: **PIPELINE**, not receivable/confirmed.

## Other existing queue — no duplicate follow-up
- #1575 Contributor Registry — fallback already sent.
- #1579 contextual Elyan Labs README mention — fallback already sent.
- #13949 README badge — prior claim already sent.
- #100 Discovery Mode — prior claim already sent.

## Archived / lower probability
- Mova #91: no acceptance/payment and competing upstream resolution.
- Lilly batch: closed upstream with no acceptance evidence for our fallback work.

## Device / browser
- Remote Desktop Commander device is currently offline; auth token remains valid.
- Opera Browser Connector is currently disconnected.
- Therefore off-platform publication cannot be completed autonomously until one of those interactive surfaces reconnects.

## Current order
1. Re-check RTC wallet after ~16:20 CEST Sep 12; if pending transfers settle, update CONFIRMED RTC from 5 to 126.
2. Publish the two ready #16497 articles on allowlisted off-platform hosts as soon as authenticated browser access is available; then start the seven-day clocks for 40 RTC.
3. Await #398 Step 3 adjudication on the corrected factual record; do not overstate the latent bridge issue.
4. Monitor Mermail/Superteam judging without duplicate outreach.
5. Continue only funded, open, non-duplicate zero-capital tasks.
6. Do not use native RTC for FLASH until a verified conversion/use path and transaction economics are established.
