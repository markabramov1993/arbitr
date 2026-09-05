# FLASH bounty / seed-capital ledger — 2026-09-05

Purpose: generate small, real external rewards first; only cleared/received funds become seed capital for FLASH. A bounty amount is **not** counted as cash until acceptance and payment are confirmed.

## Fresh work completed 2026-09-05

| Opportunity | Nominal reward | Work state | Submission state |
|---|---:|---|---|
| Lilly-Protocol/lily-contracts #324 — ARCHITECTURE.md storage/function sync | $80 | Complete; patch + PR notes in `earn/lily-contracts-324/` | Emailed to Lily + GrantFox; upstream GitHub writes blocked by integration 403 |
| Lilly-Protocol/lily-contracts #323 — ERRORS.md current error/raise-site sync | $90 | Complete; patch + PR notes in `earn/lily-contracts-323/` | Emailed to Lily + GrantFox; upstream GitHub writes blocked by integration 403 |
| Lilly-Protocol/lily-contracts #321 — pinned-admin negative tests | $90 | Complete patch + PR notes in `earn/lily-contracts-321/` | Emailed to Lily + GrantFox; upstream GitHub writes blocked by integration 403 |
| Lilly-Protocol/agentlily-runtime #253 — ISO-safe property-test dates | $50 | Commit `1d68f61...` on fork branch `fix/issue-253-safe-property-dates` | Upstream PR creation returned 403; updated submission sent by email |

Fresh nominal pipeline added today: **$310**. Cleared cash added today: **$0 until acceptance/payment confirmation**.

## Existing cash-bounty pipeline recovered from 2026-09-04 work

- Mova Labs `mova-store` #91 — **$90**. Upstream PR #257 is open, mergeable, not merged. Current external failing status is Vercel authorization for the project team, not a code-review rejection.
- Mova Labs `mova-store` #53 — **$45**. Patch/follow-up already sent to Mova Labs.
- Claude Builders bounty #1 — **$50**. CHANGELOG task completed; `/opire try` path was blocked by GitHub integration permissions; fallback sent by email.
- Lilly Protocol `agentlily-runtime` #253 — **$50**. Now promoted from standalone fallback to an actual fork branch/commit (see fresh table).
- Movalabs #60 — **$50** fallback/application sent to GrantFox.
- Expensify help-wanted pipeline — target items around **$250**, contributor-access request sent; not counted as claimed money.
- Security/responsible disclosure leads: Moorcheh/Memanto #1852 and 42project staging-access request. No reward counted until scope/acceptance is confirmed.

## RustChain / RTC pipeline recovered

Known submitted RTC claims include:

- #16601 Type C — 15 RTC
- #16601 Type D add-on — 8 RTC
- #16601 Type B — 15 RTC
- #16497 long-form tutorial submissions — 33 RTC + 33 RTC
- #293 audio/music/SFX submissions — 7 + 7 + 14 + 7 RTC
- #13953 — 5 RTC
- #398 architecture assessment — 10 RTC
- #13949 badge claim — value not counted here
- #3418 Tier A / Beacon Atlas proof-of-commerce claim — value pending/unknown
- private #2819 integrity finding — reward pending/unknown

Known RTC amount with explicit numeric rewards in recovered mail: **154 RTC nominal**, before acceptance.

## Superteam / verified-platform track

- ProofRoute / Germany Ideathon package was emailed to Superteam Germany on 2026-09-04.
- Current Superteam public listings recovered by radar/web include live USDC/USDG opportunities such as ZNS Solana Creator Challenge (500 USDC), Steve Agent Arena (500 USDC), Terminal 3 trusted-agent docs (290 USDC), Manual QA Tester — Sana.run (50–250 USDC), and other current content/dev bounties.
- Priority: use Superteam as a verified payout platform, but authenticated signup/submission currently requires the interactive browser connection. Opera Browser Connector is installed but not currently connected to ChatGPT.

## Current blockers

1. GitHub App can write to the user's repos/forks but gets `403 Resource not accessible by integration` on several upstream issue/PR writes.
2. Opera Browser Connector reports browser not connected; Remote Desktop Commander has no connected device. This blocks authenticated web registrations/forms that cannot be completed through Gmail/GitHub.
3. Do not treat scraped/mirrored issue amounts as payout proof. Prefer platform-backed bounties, maintainer-confirmed rewards, or merged/accepted work.

## Operating rules

1. No duplicate claims/submissions.
2. Prefer small tasks with clear acceptance criteria and low competition.
3. Verify comments/PRs before starting so already-claimed items are skipped.
4. Keep every deliverable public/reviewable in a user-controlled repo when upstream writes are blocked.
5. Follow up through the already-authorized Gmail account, but avoid repeated spam when a prior follow-up is still unanswered.
6. Record reward as `pending` until maintainer/platform acceptance; record as `cleared` only after actual payment confirmation.
7. Cleared funds are the only funds eligible to move into FLASH execution capital.
