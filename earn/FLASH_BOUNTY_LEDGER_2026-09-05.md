# FLASH bounty / seed-capital ledger — audited 2026-09-06

Purpose: obtain **real external rewards first**. Only money/tokens actually received become FLASH seed capital. Face value, prize pools, emails, open PRs and simulated PnL are never counted as cash.

## Headline
- **Confirmed USD/stablecoin bounty cash: $0**
- **Confirmed DeFi profit: $0**
- **RTC:** live balance/history probe refreshed Sep 6; use RustChain wallet data as the only authority for confirmed RTC.
- RTC wallet: `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`

## 1. Closest explicit pay-on-acceptance path — RustChain

### #16601 Distribution Packages
Official issue states `paid: true`, review within 7 days, and accepted packages are paid.

Existing Sep 4 submissions re-audited Sep 6:
1. **Type C — RIP-302 Agent Economy Shorts kit — 15 RTC**
   - `bounties/rip302-agent-economy-shorts-kit/`
   - ≤60s timed script, 9:16 storyboard, metadata and SOURCES.
   - Key claims independently rechecked against current `Scottcjn/Rustchain/rip302_agent_economy.py` (5% fee, escrow, lifecycle, settlement, reputation).
2. **Type C — Beacon Liveness Shorts kit — 15 RTC**
   - `earn/shorts/beacon-liveness/`
   - 60s script, 9:16 storyboard, metadata and SOURCES.
   - Commands/Atlas heartbeat/signed bounty metadata rechecked against current `Scottcjn/beacon-skill`.

Both were submitted through the issue's allowed **email** route. A Sep 6 attempt to add public queue comments failed with GitHub App `403`; do not resend duplicate email during the stated 7-day review window. When authenticated browser write access returns, add comments explicitly identifying them as the same existing submissions, not duplicate reward claims.

Other historical RTC claims remain **PIPELINE** until each is individually accepted/paid. Do not infer the wallet balance from their nominal totals.

## 2. Mermail / Superteam — submitted competition

- Listing: Build and Demo a Mermail Agent Skill.
- Advertised prize pool: **500 USDC**.
- Superteam entry was submitted; prior UI verification showed `Edit Submission` and one credit consumed.
- Official PR: `Nudgen-Marketing/mermail-skills#174`.
- PR state Sep 6: open, mergeable, no maintainer reviews/comments.
- Controlled Mermail live run completed: legitimate opportunity identified, malicious prompt-injection/payment instruction rejected, duplicate check performed, no unauthorized send/payment, state remained opportunity-only.
- Demo video: `https://x.com/LeadsOleg/status/2096249643604570579`
- Tagged post: `https://x.com/LeadsOleg/status/2096354167971271154`
- Upstream fork workflows currently show `action_required` with no validation jobs, consistent with maintainer approval being required for external-fork Actions rather than a demonstrated code failure.

Accounting: **PIPELINE**, not receivable or confirmed.

## 3. Mova Labs #91 — live $90 path, now competitive

- Issue #91 remains open: **$90**.
- Our upstream PR #257 remains open and mergeable.
- Sep 6 audit found an important flaw in the original submission: comparing emitted events to `.to_xdr()` of the same event structs did not prove that the first topic matched the JS indexer's short symbols.
- Current Soroban behavior defaults a contractevent fixed topic to the struct name in snake_case, while Mova's JS decoder expects `pay`.
- Our fork branch was corrected to pin explicit topics:
  - `PaymentReceived` -> `pay`
  - `OrderCreated` -> `create_order`
  - `OrderShipped` -> `dispatch`
  - `OrderRefunded` -> `refund`
- PR #257 now has 2 commits / 2 changed files and remains mergeable.
- Competing PR #343 exists and covers overlapping/broader work, so payout probability is lower than previously assumed.
- Upstream PR-body mutation still returns GitHub integration `403`; update/explain through browser when available.

Accounting: **PIPELINE**.

## 4. Lilly work — archived from active expected income

The nine tasks previously summarized as **$635 nominal** are now all closed upstream as `completed`:
- lily-contracts #321, #323, #324;
- agentlily-runtime #241, #242, #243, #247, #248, #253.

Our branches/patches/email fallbacks remain useful historical work, but there is **no evidence they were accepted for payment**. Do not carry $635 as active pending money. Re-open only if Lilly/GrantFox explicitly replies with acceptance/payment or requests the work.

Accounting: **ARCHIVED / no acceptance evidence**.

## 5. Other older bounty paths

- Mova #53 — $45 nominal; patch/follow-up sent, no acceptance evidence.
- Mova #60 — $50 nominal; fallback sent, no acceptance evidence.
- Claude Builders #1 — $50 nominal; fallback sent, no acceptance evidence.
- Expensify help-wanted access request — no accepted assignment/payout evidence.
- Security leads — no reward counted without explicit scope/acceptance.

These remain lower priority than already-submitted RustChain, Mova #91 and Mermail.

## 6. ProofRoute / Germany opportunities

Prepared in `earn/germany-ideathon/`:
- `README.md`
- `PITCH.md`
- `GRANT_APPLICATION.md`

Germany Ideathon and suitable Germany grant forms should be submitted natively when authenticated browser access returns. Any awarded grant is **restricted ProofRoute project funding**, not free FLASH trading capital.

## 7. Operating rules

1. No duplicate claims/submissions.
2. Verify issue state, competition and funding before new work.
3. Prefer explicit pay-on-acceptance / platform-backed opportunities.
4. Do not follow up inside a published review SLA unless there is a material change or maintainer request.
5. `CONFIRMED` requires an actual receipt; `RECEIVABLE` requires explicit acceptance; everything else stays `PIPELINE`, `PREPARED` or `ARCHIVED`.
6. No live trading until confirmed seed capital exists and the exact route passes current deterministic cost-aware validation.
