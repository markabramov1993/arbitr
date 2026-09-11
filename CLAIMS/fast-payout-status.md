# Fast payout status — audited 2026-09-10

## Confirmed
- USD/stablecoin bounty cash actually received: **$0**.
- RTC wallet `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`: **5.0 RTC CONFIRMED**.
- Live Sep 10 22:48 CEST probe: `/wallet/balance` returned `amount_rtc: 5.0`; wallet history contains one incoming transfer from `founder_community`.
- Confirmed tx: `b5034bc573d119c8b74c0b9773afa88c`.
- Source bounty: BoTTube/RustChain #1102 — JS SDK `health()` return-type mismatch; accepted as a functional bug for 5 RTC.

## Fastest current payout asks
1. **#315 Human Funnel Stage 1 — 30 RTC requested:** fresh original asset pack completed and submitted once by the documented email fallback on Sep 10. Public deliverable: `earn/rustchain-315-human-funnel/ASSET_PACK.md`; separate rights declaration included. It contains 10 CTA hooks, 3 original 8–15s vertical-video templates, and 5 original static visual/meme concepts. Current title rate is 30 RTC; prior maintainer rulings on the same issue confirm 30 RTC despite stale 45 RTC body text. **SUBMITTED / awaiting verification; not accepted yet.**
2. **#398 Harden the Chain Step 2 — 15 RTC requested:** Mock Signature Mode known-fix reproduction completed and submitted Sep 10. Public write-up: `bounties/rustchain-security-step2/MOCK_SIGNATURE_MODE.md`. Reproducible CI cloned RustChain head `883c18ad50778657ed386d55b2284220ebff7707`, verified fail-closed flags + WSGI guard, and upstream `node/tests/test_mock_signature_guard.py` passed **3/3 in 1.06s**. Run: `https://github.com/markabramov1993/arbitr/actions/runs/34531744614`. The Sep 4 Step 1 assessment was referenced for continuity, not duplicated. **SUBMITTED / awaiting verification; not accepted yet.**
3. **#1102 second/final item — 5 RTC requested:** mobile login does not validate the API key. Submitted Sep 10; no acceptance reply yet. Contributor cap is now full, so no additional #1102 claims.
4. **#13949 — 2 RTC:** README badge claim already sent; no duplicate.
5. **#1575 — 3–5 RTC canonical amount:** contributor-registry registration sent through the documented 403 email fallback; no reply yet.
6. **#1579 — 3 RTC:** contextual Elyan Labs mention in the pre-existing `arbitr` README; claim already sent; no reply yet.
7. **#100 — 2 RTC:** first Discovery Mode claim already sent; no reply yet.
8. **#16497 — 26 RTC requested as draft-acceptance tranches:** two Sep 4 articles, 13 RTC each; correction/reconciliation already sent.
9. **#16601 Type B — 15 RTC:** Proof-of-Antiquity YouTube script/storyboard package submitted Sep 4 and re-audited Sep 10.
10. **#16601 Type D — +8 RTC conditional:** syndication add-on submitted Sep 4; depends on acceptance of the backing article. Type C lane is occupied and is not forecast.

## Duplicate / evidence controls
- #315: Gmail SENT search across the prior year found no earlier #315 / Human Funnel Stage 1 submission; public thread confirms recent 30 RTC email-fallback acceptances.
- #398: Gmail search found only the Sep 4 Step 1 submission before the new Step 2 mail. Step 2 is a new quest stage, not a duplicate. Public #398 requirements explicitly pay 15 RTC for reproducing one known BuilderFred fix and do not require finding a new vulnerability.
- #1102: correction already sent to keep mobile-login as second/final item and withdraw the earlier `getTrending()` payout request.

## Platform-backed judged lane
- **Mermail / Superteam — 500 USDC prize pool:** Superteam sent `Submission Received!` on Sep 9. Existing submission and PR #174 remain the only entry; no duplicate submission. Prize pool is PIPELINE, not receivable.

## Archived / skipped
- **aquarium-of-gullibles / bounty-plaza#1336+#1334 ($1,250+$850 nominal):** verified honeypot on 2026-09-11 (impossible O(N) isomorphism claim, missing source paths, digitaltoolsshed claim gate). Rejected by radar filters; not receivable. Evidence: `earn/aquarium-gullibles-radar-rejection.md`.
- **Mova #91:** archived after upstream resolution elsewhere; no acceptance/payment for our PR.
- **Lilly former $635 nominal batch:** archived; issues closed elsewhere with no acceptance evidence.
- #1102 further findings may still be technically valid but cannot be claimed under our already-full cap.
- #16471 silent-success audit remains attractive but is heavily mined; many apparent current defects are already on the public confirmed-finding list, so do not re-report known findings.
- Avoid capital-risking bounties, fabricated activity, region-ineligible work, occupied slots and stale scraped amounts.

## FLASH gate
The 5 native RTC is real received capital but is not yet directly usable for a FLASH trade. Verify a legitimate user-accessible RTC conversion/bridge route, liquidity, gas and slippage before moving it.
