# FLASH bounty / seed-capital ledger — 2026-09-05

Purpose: generate small, real external rewards first; only cleared/received funds become seed capital for FLASH. A bounty amount is **not** counted as cash until acceptance and payment are confirmed.

## Fresh work completed 2026-09-05

| Opportunity | Nominal reward | Work state | Submission state |
|---|---:|---|---|
| Lilly-Protocol/lily-contracts #324 — ARCHITECTURE.md storage/function sync | $80 | Complete; patch + PR notes in `earn/lily-contracts-324/` | Emailed to Lily + GrantFox; upstream GitHub writes blocked by integration 403 |
| Lilly-Protocol/lily-contracts #323 — ERRORS.md current error/raise-site sync | $90 | Complete; patch + PR notes in `earn/lily-contracts-323/` | Emailed to Lily + GrantFox; upstream GitHub writes blocked by integration 403 |
| Lilly-Protocol/lily-contracts #321 — pinned-admin negative tests | $90 | Complete patch + PR notes in `earn/lily-contracts-321/` | Emailed to Lily + GrantFox; upstream GitHub writes blocked by integration 403 |
| Lilly-Protocol/agentlily-runtime #253 — ISO-safe property-test dates | $50 | Commit `1d68f61...` on fork branch `fix/issue-253-safe-property-dates` | Upstream PR creation returned 403; updated submission sent by email |
| Lilly-Protocol/agentlily-runtime #247 — runtime event catalog/docs | $45 | Commit `c490d26...` on `docs/issue-247-runtime-events` | Branch ready; combined submission sent to Lily + GrantFox |
| Lilly-Protocol/agentlily-runtime #248 — JsonFileMemoryStore/durable-memory docs | $90 | Commit `7e84941...` on `docs/issue-248-durable-memory` | Branch ready; combined submission sent to Lily + GrantFox |
| Lilly-Protocol/agentlily-runtime #243 — ToolRegistry lifecycle tests | $55 | Commit `980d8f7...` on `test/issue-243-tool-registry-lifecycle` | Branch ready; upstream GitHub write still blocked |
| Lilly-Protocol/agentlily-runtime #242 — state-store eviction/lifecycle tests | $40 | Commit `a939f5d...` on `test/issue-242-state-store-lifecycle` | Branch ready; upstream GitHub write still blocked |
| Lilly-Protocol/agentlily-runtime #241 — AgentInstanceManager FIFO eviction tests | $95 | Commit `cd2505f...` on `test/issue-241-agent-manager-eviction` | Branch ready; upstream GitHub write still blocked |

Fresh nominal pipeline added today: **$635**. Cleared cash added today: **$0 until acceptance/payment confirmation**.

## Platform-backed work in progress — not included in the $635 completed nominal total

### Superteam / Mermail — Build and Demo a Mermail Agent Skill

- Advertised pool: **500 USDC** on Superteam Earn.
- Public Mermail announcement: reusable Mermail Agent Skill + live video demo; deadline stated as **2026-09-23**.
- Concept built: `mermail-bounty-ops`, a community/unofficial Mermail companion skill for safe bounty/freelance inbox operations.
- Public branch: `earn/superteam-mermail-bounty-ops` in `markabramov1993/arbitr`.
- Draft review PR: `markabramov1993/arbitr#4`.
- Package currently contains 7 isolated files / 666 added lines: `SKILL.md`, OpenAI/MCP metadata, tool reference, security reference, README, live-demo script, and Superteam submission copy/checklist.
- Code/docs phase: **ready**.
- Live Mermail OAuth/MCP test: **blocked by disconnected interactive browser**.
- Video demo: **script ready; live recording pending**.
- Superteam submission: **not submitted yet**; authenticated profile/browser step pending.
- Accounting rule: the 500 USDC is an opportunity only. Do **not** add it to earned, accepted, or paid totals until the corresponding evidence exists.

## Existing cash-bounty pipeline recovered from 2026-09-04 work

- Mova Labs `mova-store` #91 — **$90**. Upstream PR #257 is open, mergeable, not merged. Current external failing status is Vercel authorization for the project team, not a code-review rejection. Latest check on 2026-09-05 still shows no human review.
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
- Current Superteam public listings verified on 2026-09-05 include Mermail Agent Skill (500 USDC), Terminal 3 trusted-agent docs (290 USDC), ZNS Solana Creator Challenge (500 USDC), and other current content/dev bounties.
- Treat individual listing status as dynamic and re-check before starting; previously surfaced Sana.run and some regional opportunities showed inconsistent/stale indexing and are not current priority targets without a fresh exact-listing verification.
- Priority: platform-backed opportunities with a reproducible deliverable and clear submission path.

## Current blockers

1. GitHub App can write to the user's repos/forks but gets `403 Resource not accessible by integration` on several upstream issue/PR writes.
2. Opera Browser Connector still reports: `Browser not connected. Make sure to enable Allow AI connection ... and sign in with your Opera account.` This blocks authenticated Mermail/Superteam web/OAuth steps that cannot be completed through Gmail/GitHub.
3. Remote Desktop Commander has no connected device.
4. Local/container internet is unavailable, so repository tests cannot be executed locally in this session; test-only bounty branches are written against the current source/API and remain pending maintainer/CI verification.
5. Do not treat scraped/mirrored issue amounts as payout proof. Prefer platform-backed bounties, maintainer-confirmed rewards, or merged/accepted work.

## Operating rules

1. No duplicate claims/submissions.
2. Prefer small tasks with clear acceptance criteria and low competition.
3. Verify comments/PRs before starting so already-claimed items are skipped.
4. Keep every deliverable public/reviewable in a user-controlled repo when upstream writes are blocked.
5. Follow up through the already-authorized Gmail account, but avoid repeated spam when a prior follow-up is still unanswered.
6. Record reward as `pending` until maintainer/platform acceptance; record as `cleared` only after actual payment confirmation.
7. Cleared funds are the only funds eligible to move into FLASH execution capital.
