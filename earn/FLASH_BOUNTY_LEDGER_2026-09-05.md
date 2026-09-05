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

- Advertised pool: **500 USDC** on Superteam Earn; prize structure currently shown as 250 USDC first, 100 second, 50 third, plus two 50 USDC bonuses.
- Deadline shown by Mermail/Superteam: **2026-09-23**; winner announcement shown as **2026-10-01**.
- Concept built: `mermail-bounty-ops`, a community/unofficial **worker-side** Mermail companion skill for safe bounty/freelance inbox operations.
- Internal public working branch/package remains in `markabramov1993/arbitr` with validator/demo/submission materials.
- Official fork created: `markabramov1993/mermail-skills`.
- Official upstream PR created: **`Nudgen-Marketing/mermail-skills#174`** — open, non-draft, mergeable; head `7fbaac48a223584bb847dac67419c336a10a3c79`; 7 changed files, +587/-0.
- Official companion proposal: `Nudgen-Marketing/mermail-skills#173`; linked to PR #174. No maintainer reply yet at the latest check.
- Upstream workflow runs currently show `action_required` / no jobs for the external-contributor PR; this is not evidence of a code failure.
- Validation: **PASS**. `SKILL.md` is 173/500 lines; 7 machine-readable scenarios; authoring/MCP/safety/dedup/reward-state invariants checked.
- Live Mermail test: **completed** on an authenticated mailbox. The agent identified the legitimate 500 USDC opportunity, rejected a controlled malicious prompt-injection/payment message, found no duplicate sent claim, and performed no external send/payment.
- Live reward-state result: **opportunity = yes; accepted = no evidence; paid = no evidence**.
- Demo video produced from the real Mermail run: approximately **2:04**, English narration, H.264/AAC. Local final file was verified before publishing.
- Public X media/demo post: `https://x.com/LeadsOleg/status/2096249643604570579` (verified through X oEmbed to contain media).
- Public tagged X post: `https://x.com/LeadsOleg/status/2096354167971271154` tagging `@Mermailapp` and linking PR #174.
- **Superteam submission filed successfully.** One credit was consumed and the listing changed from `Submit Now` to `Edit Submission`; submission count increased to 61 during verification.
- Saved Superteam submission fields verified through Edit Submission:
  - public PR: `https://github.com/Nudgen-Marketing/mermail-skills/pull/174`
  - Tweet Link: `https://x.com/LeadsOleg/status/2096354167971271154`
  - video demonstration: `https://x.com/LeadsOleg/status/2096249643604570579`
- Submission can still be edited until the deadline. A cleanup/improvement pass should replace any placeholder text in `Anything Else` with the concise skill description and AI-client information when browser access is stable.
- Accounting rule: the 500 USDC is an **opportunity / prize pool only**. Do **not** add it to accepted, earned, paid, or FLASH capital until corresponding evidence exists.

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
- Current exact-listing audits on 2026-09-05:
  - Mermail Agent Skill — 500 USDC: **submission filed**; official PR #174 + live Mermail demo + public X evidence now exist.
  - Terminal 3 trusted-agent docs — 290 USDC: real/global but already high competition and requires SSO + DID + API-key quickstart; lower priority.
  - ZNS Solana Creator Challenge — 500 USDC: requires launching a token plus organic volume/holder activity; skipped because it is not a zero-capital seed path and activity must not be fabricated.
  - Steve Agent Arena — 500 USDC: requires live Solana agent activity; candidate only without artificial trading/activity.
  - Superteam Canada Solana dashboard — 1,000 USDG: Canada-only; skipped rather than bypassing regional eligibility.
  - Manic Bug Bounty — 1,000 USDC: explicitly requires deposits and real-money trading; skipped rather than risking seed capital for testing.
- Priority: platform-backed opportunities with reproducible deliverables, global/user-eligible rules, no artificial activity, and no requirement to risk user funds.

## Other verified-source filters

- Tenstorrent has a real bounty program, but current `label:bounty no:assignee` search returned no free items. The surfaced $5,000 issue #55502 is assigned and its maintainer explicitly asked others not to request assignment; skipped.
- warpSpeed OPEN is a real paid bounty platform with published payment/review/KYC terms, but its $750 Email Threads API already has multiple claims and active submissions. Platform terms also prohibit automated claiming/submission; skipped.
- Claude Builders / Opire #2-#5 are real-formatted bounty issues but currently have very high competition; skipped rather than joining a crowded race.
- False-positive radar amounts are discarded when the number is not a reward.

## Current blockers / watch items

1. Mermail submission is **already filed**, so browser access is no longer a blocker to having a valid entry; browser stability only affects optional polishing/edits.
2. Remote Desktop / Opera connectivity became intermittent late in the session. Do not infer that the submission or authenticated accounts were lost.
3. Upstream Mermail PR #174 awaits maintainer review and permission to run external-contributor workflows.
4. No new human acceptance/payment email from Lily, GrantFox, Mova, Superteam, or Mermail was found at the latest Gmail check.
5. Do not treat scraped/mirrored issue amounts as payout proof. Prefer platform-backed bounties, maintainer-confirmed rewards, or merged/accepted work.

## Operating rules

1. No duplicate claims/submissions.
2. Prefer small tasks with clear acceptance criteria and low competition.
3. Verify comments/PRs before starting so already-claimed items are skipped.
4. Keep every deliverable public/reviewable in a user-controlled repo when upstream writes are blocked.
5. Follow up through the already-authorized Gmail account, but avoid repeated spam when a prior follow-up is still unanswered.
6. Record reward as `pending` until maintainer/platform acceptance; record as `cleared` only after actual payment confirmation.
7. Cleared funds are the only funds eligible to move into FLASH execution capital.
