# FLASH bounty / seed-capital ledger — audited 2026-09-13

Purpose: obtain **real external rewards first**. Only money/tokens actually received become FLASH seed capital. Face value, prize pools, sent emails, open PRs and simulated PnL are never counted as cash.

## Headline

- **Confirmed USD/stablecoin bounty cash: $0**
- **Confirmed RTC: 126.0 RTC**
- **Confirmed DeFi profit: $0**
- RTC wallet: `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`
- Fresh live probe: GitHub Actions run `34759583859`, job `103729901214`, commit `acc86954404409f777d5111406f9edc7059a0551`, completed successfully on 2026-09-13.
- Live RustChain response: `amount_rtc = 126.0`, history count `10`.

This **126 RTC is cleared/received capital**. It is not a bounty face value or pending reward.

## 1. Confirmed receipts

### Original 5 RTC

- Source: BoTTube/RustChain #1102 JS SDK `health()` contract mismatch.
- Tx: `b5034bc573d119c8b74c0b9773afa88c`
- Amount: **5 RTC**
- State: **CONFIRMED / PAID**.

### September 11 adjudication — 121 RTC, now settled

Sophia Elya confirmed all Sept 9–11 submissions below as paid with a 24-hour hold. The hold has elapsed and the wallet now independently reports the funds.

| Work | Amount | Wallet-history tx | State |
|---|---:|---|---|
| #315 Human Funnel Stage 1 asset pack | 30 RTC | `9bffbd87c18a1e6de798173cafd04dd6` | CONFIRMED |
| #398 Step 2 — Mock Signature Mode reproduction + CI | 15 RTC | `a7c4d95baf408665f316143810fdf647` | CONFIRMED |
| #16601 Type C Shorts kit | 15 RTC | `f1ae62e6bdaf98bd9509db05d50e32c7` | CONFIRMED |
| #16497 Tutorial 1 — miner dry-run, draft tranche | 13 RTC | `a002133631334223d5399dff2970c84f` | CONFIRMED |
| #16497 Tutorial 2 — Beacon liveness, draft tranche | 13 RTC | `44c64730923966fbf28732f77ae11591` | CONFIRMED |
| #398 Step 1 security assessment | 10 RTC | `f1adea86bf1ea35c1cfe95c63ef766cc` | CONFIRMED |
| #13954 Proof-of-Antiquity infographic | 10 RTC | `0d19ee39eac9371780afaa79aa5bd140` | CONFIRMED |
| #13224 RIP-0301 identity-churn critique | 10 RTC | `569ec2ed091baa3b076202b20489fdd1` | CONFIRMED |
| #1102 mobile login false-success | 5 RTC | `5357aa747f2db68d1d22612b2310a540` | CONFIRMED |

Subtotal: **121 RTC**. Together with the original 5 RTC: **126 RTC confirmed**.

## 2. Highest-value receivable path — #16497 +40 RTC

Two already accepted long-form tutorials each have an additional **20 RTC live-publication tranche**.

Requirements confirmed by maintainer:
- publish each tutorial on an allowlisted off-platform host: Dev.to, Hashnode, Medium or Substack;
- keep each Live-URL publicly accessible under the claimant/byline for seven days;
- GitHub does not count as the article home.

Remaining upside: **40 RTC**.

Current blocker: authenticated browser/desktop connector is offline, so native publication has not been completed. Do not fabricate a Live-URL or claim the second tranche early.

State: **ACCEPTED WORK / CONDITIONAL SECOND TRANCHE, not yet receivable until publication + seven days**.

## 3. Fresh submissions awaiting adjudication

- #2784 RustChain miner dry-run hardware report — submitted once by documented email fallback on 2026-09-13. **PIPELINE**.
- #12442 RustChain vs Helium / DePIN comparison — submitted once 2026-09-12. **PIPELINE**.
- #12444 Proof of Antiquity vs Proof of Storage comparison — submitted once 2026-09-12. **PIPELINE**.
- #16601 historical Type B (15 RTC) + Type D (+8 RTC) — one reconciliation email sent 2026-09-12; not a new duplicate claim. **PIPELINE / maintainer reconciliation**.

Do not resend or chase these while normal review is pending.

## 4. Mermail / Superteam

- Build and Demo a Mermail Agent Skill.
- Advertised prize pool: **500 USDC total**.
- Superteam entry submitted; prior UI verification showed `Edit Submission` and one credit consumed.
- Official PR: `Nudgen-Marketing/mermail-skills#174`.
- Demo video: `https://x.com/LeadsOleg/status/2096249643604570579`.
- Tagged post: `https://x.com/LeadsOleg/status/2096354167971271154`.
- No sponsor winner/payment evidence yet.

State: **PIPELINE, not RECEIVABLE/CONFIRMED**.

## 5. RTC -> wRTC/USDC conversion status

A withdrawal/bridge clarification was sent to Sophia on 2026-09-12 after the 121 RTC adjudication. No reply has arrived yet.

Current official RustChain docs state:
- native RTC -> wRTC/Solana is **operator-assisted/admin-authenticated**, not public self-service;
- `/api/bridge/initiate` for RustChain-origin deposits requires an operator `X-Admin-Key` and configured `RC_ADMIN_KEY`;
- minimum documented bridge amount defaults to 1 RTC;
- public routing may intentionally not expose the management route.

Therefore:
- **No bridge has been initiated.**
- **No wRTC or USDC has been received.**
- Do not send RTC to any address copied from another user's bridge request.
- Do not expose any private key/seed phrase.
- Wait for the official operator procedure or an authenticated official portal before moving the 126 RTC.

## 6. Archived / occupied work

- Lilly batch formerly $635 nominal: all relevant upstream issues closed elsewhere without acceptance of our fallback work. **ARCHIVED**.
- Mova #91: issue resolved through competing upstream work; our PR is no longer a high-probability payout path. **ARCHIVED / OCCUPIED**.
- #1102 contributor cap is exhausted for `markabramov1993`. **DO NOT SUBMIT MORE**.
- #13224 is one claim per contributor and already paid. **DO NOT SUBMIT MORE**.

## 7. FLASH activation rule

126 RTC is real seed capital, but it is not automatically usable as trading capital on EVM/Solana.

Before any live FLASH transaction:
1. obtain the official RTC -> wRTC/USDC custody/bridge procedure;
2. verify exact bridge destination and fees/minimums;
3. verify current executable wRTC liquidity/quote, gas and slippage;
4. start with a small test tranche if the official operator supports it;
5. reconcile the resulting bridge/chain receipt before any larger movement;
6. only then evaluate current arbitrage/liquidation execution economics.

## 8. Operating rules

1. No duplicate claims/submissions or duplicate follow-up emails.
2. Check issue state, comments, competing PRs, caps and funding before new work.
3. Prefer explicit pay-on-acceptance, low-capital, globally eligible work.
4. `CONFIRMED` requires a real receipt; `RECEIVABLE` requires explicit acceptance and a due payment; all else stays PIPELINE/PREPARED/ARCHIVED.
5. Re-run the wallet balance/history after every acceptance/payment signal.
6. Never risk the confirmed seed capital merely to qualify for another bounty.
7. Never fabricate social activity, transactions, users, publication URLs or settlement evidence.
