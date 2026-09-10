# FLASH bounty / seed-capital ledger — audited 2026-09-10

Purpose: obtain **real external rewards first**. Only money/tokens actually received become FLASH seed capital. Face value, prize pools, sent emails, open PRs, bids and simulated PnL are never counted as cash.

## Headline
- **Confirmed USD/stablecoin bounty cash: $0**
- **Confirmed RTC: 5.0 RTC**
- **Confirmed DeFi profit: $0**
- RTC wallet: `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`
- **Live RustChain probe 2026-09-10 12:14 UTC:** HTTP 200 balance = `5.0 RTC`; history count = `1`.
- Confirmed tx: `b5034bc573d119c8b74c0b9773afa88c`, inbound 5 RTC from `founder_community`.
- This is the **first real external reward received** by FLASH bounty operations.

## 1. First paid bounty — BoTTube/RustChain #1102 — 5 RTC
- Report: official JS/TS SDK `health()` type was `{status, timestamp}` while the live `/health` payload is `{ok, service, version, uptime_s, videos, agents, humans}`.
- Public report: `earn/bottube-1102-js-sdk-health-contract.md`.
- Sophia Elya accepted it as a **functional bug** for **5 RTC**.
- Idempotency key: `markabramov1993-1102-sdk-health-type`.
- Public #1102 receipt names `@markabramov1993` as accepted.
- 24h hold elapsed and live wallet history proves settlement.
- **State: CONFIRMED / PAID.**

## 2. Second/final #1102 item — mobile false-success login — requested 5 RTC
- Fresh source audit found `mobile-app/src/api/client.ts::login(agentName, apiKey)` fetches the public `/api/agents/<name>` profile with `includeAuth=false`, then persists whatever API-key string was supplied.
- `mobile-app/src/hooks/useAuth.ts` immediately sets `isAuthenticated=true` from that public-profile success.
- `/api/agents/<name>` is explicitly documented as public/no-auth; later authenticated calls such as `getMe()` expose the invalid key.
- This is a client-side false-success authentication state, **not** a server authorization bypass.
- Strong open/closed duplicate searches found no issue describing this exact path.
- Public report: `earn/bottube-1102-mobile-login-does-not-validate-api-key.md`.
- Submitted once by documented 403 email fallback on 2026-09-10 as the **second and final** item under `cap: 2`.
- Requested classification: functional bug, 5 RTC, subject to maintainer verification.
- **State: PIPELINE.**

## 3. Other short payout requests

### RustChain #13949 — README badge — 2 RTC
- Existing real repo: `markabramov1993/arbitr`.
- RustChain badge verified in README.
- Canonical claim already exists; no public receipt yet. Do not send another duplicate.
- **State: PIPELINE.**

### Contributor Registry #1575 — canonical 3–5 RTC ambiguity
- `markabramov1993` remains absent from the registry at 2026-09-10 check.
- Direct issue creation is blocked by external GitHub App permissions (`403`).
- Registration was sent through documented fallback; an additional Sep 10 fallback already exists, so **send nothing further** until maintainer response.
- Registry/template says 5 RTC while bounty title has shown a lower amount; maintainer chooses canonical current rate.
- **State: PIPELINE.**

### RustChain #1579 — contextual Elyan Labs mention — 3 RTC
- Existing `arbitr` repo predates the bounty and contains original work.
- README has a contextual Elyan Labs section in commit `c43c34329ae8076d60a720ca8a65472cf6f063dc`.
- Claim already sent through documented fallback; no public receipt yet.
- **State: PIPELINE.**

### RustChain #100 — Discovery Mode — 2 RTC
- First-discovery claim for `Scottcjn/beacon-skill` already sent after checking prior claim history.
- **State: PIPELINE.**

### RustChain #16497 — two draft-acceptance tranches — 13 + 13 RTC
- Two long-form tutorials originally submitted Sep 4, before the Sep 8 Live-URL rule change.
- Beacon tutorial copy/paste bug corrected before follow-up (`600401ec7d1eaa0c56a1b2bc6de508c28f98a787`).
- Follow-up requests only the **13 RTC draft-acceptance tranche per article**; a Sep 10 reconciliation note explicitly says it is not a new/duplicate claim.
- No inbound acceptance yet. Do not send more follow-ups now.
- **State: PIPELINE.**

## 4. Mermail / Superteam — submitted competition
- Advertised prize pool: **500 USDC total**.
- Superteam sent `Submission Received!` on 2026-09-09.
- Official PR `Nudgen-Marketing/mermail-skills#174` is **open, mergeable, not merged** at 2026-09-10 check.
- No maintainer acceptance/payment evidence.
- **State: PIPELINE, not RECEIVABLE.**

## 5. Mova Labs #91 — archived / no longer counted
- Issue #91 was completed through upstream work that is not our PR.
- Our PR #257 remains open but is currently non-mergeable and has no maintainer acceptance/payment.
- Do not spend more time here unless maintainer explicitly revives/payably requests the contribution.
- **State: ARCHIVED / CLOSED ELSEWHERE.**

## 6. Occupied / archived lanes
- RustChain #16601 Type C: earlier accepted Type C submission makes our historical packages low probability. **OCCUPIED.**
- Lilly batch formerly $635 nominal: all nine relevant issues closed elsewhere without acceptance of our work. **ARCHIVED.**
- Mova #53/#60, Claude Builders #1 and similar older fallback submissions remain unconfirmed and low priority.

## 7. RTC conversion / FLASH gate
- RustChain current source exposes `/wallet/swap-info` for a Base-network wRTC/USDC route and identifies an Aerodrome pool, but source configuration/reference pricing is **not proof of current executable liquidity**.
- 5 RTC is confirmed seed capital, but no conversion or live trade is authorized merely by its existence.
- Before any conversion/execution: verify live swap endpoint, bridge mechanics, pool reserves/quote, gas requirement, slippage and whether the exact amount is economically usable.

## 8. Operating rules
1. Search canonical issue state, maintainer history, linked PRs and SENT mail before every claim/bid.
2. No duplicate claims or duplicate follow-up emails.
3. Prefer funded, open, unoccupied, explicit payout paths.
4. `CONFIRMED` requires actual receipt; `RECEIVABLE` requires explicit acceptance; everything else stays PIPELINE/PREPARED/ARCHIVED.
5. Re-run RTC balance/history after any acceptance/payment signal.
6. No live FLASH trading until asset usability/conversion, current-state strategy economics and failure bounds are independently verified.
