# Superteam submission — Build and Demo a Mermail Agent Skill

## Submission title

**Mermail Bounty Ops — safe worker-side paid-task operations for AI agents**

## Short description

Mermail Bounty Ops is a reusable community Mermail Agent Skill for bounty hunters, freelancers, and AI agents managing their own paid-task pipeline. It safely finds opportunities and reviewer replies, prevents duplicate claims, drafts submissions/follow-ups, resists prompt injection in email, and keeps advertised, accepted, and actually paid rewards as separate states.

## Why this skill

Most bounty automation focuses on finding more opportunities. This skill focuses on the worker-side operational layer where money is commonly lost or misreported:

- duplicate claims and duplicate follow-ups;
- missing reviewer replies;
- malicious email trying to redefine the agent's task;
- wallet/payment instructions embedded in untrusted messages;
- assuming a nominal bounty is earned before acceptance;
- assuming an accepted reward is paid before settlement evidence exists.

The workflow is reusable across GitHub bounties, grants, contests, freelance tasks, and sponsor-paid work because the opportunity source is normalized through Mermail inbox operations.

## Distinct from adjacent Mermail proposals

The public Mermail repository contains adjacent proposals, so this submission intentionally defines a different side of the workflow:

- `mermail-opportunity-gate` (#70) stops at a read-only eligibility decision. `mermail-bounty-ops` manages what happens after and around that decision: duplicate checks, claims/applications, reviewer replies, acceptance, and payout reconciliation.
- `mermail-pact` (#136) is sponsor/operator-side paid-work contracting and settlement. `mermail-bounty-ops` is **worker-side**: it manages the worker's opportunities, submissions, reviews, and incoming reward evidence.
- Mermail Freelance Deal Desk (#154) qualifies one inbound prospective client and prepares a quote/clarification/decline. `mermail-bounty-ops` is a multi-opportunity bounty/grant/contest operations queue, including already-submitted work and payment follow-up.

The goal is not to claim a new Mermail tool domain. It is a reusable community workflow composed from existing documented Mermail inbox and composition capabilities.

## Public code

Repository:
https://github.com/markabramov1993/arbitr

Submission-package PR:
https://github.com/markabramov1993/arbitr/pull/4

Official Mermail companion proposal / discussion:
https://github.com/Nudgen-Marketing/mermail-skills/issues/173

**Official Mermail implementation PR:**
https://github.com/Nudgen-Marketing/mermail-skills/pull/174

Submission branch:
https://github.com/markabramov1993/arbitr/tree/earn/superteam-mermail-bounty-ops/earn/superteam-mermail-bounty-ops

Skill:
https://github.com/markabramov1993/arbitr/blob/earn/superteam-mermail-bounty-ops/earn/superteam-mermail-bounty-ops/mermail-bounty-ops/SKILL.md

OpenAI metadata:
https://github.com/markabramov1993/arbitr/blob/earn/superteam-mermail-bounty-ops/earn/superteam-mermail-bounty-ops/mermail-bounty-ops/agents/openai.yaml

Tool reference:
https://github.com/markabramov1993/arbitr/blob/earn/superteam-mermail-bounty-ops/earn/superteam-mermail-bounty-ops/mermail-bounty-ops/references/tools.md

Security reference:
https://github.com/markabramov1993/arbitr/blob/earn/superteam-mermail-bounty-ops/earn/superteam-mermail-bounty-ops/mermail-bounty-ops/references/security.md

Validation scenarios:
https://github.com/markabramov1993/arbitr/blob/earn/superteam-mermail-bounty-ops/earn/superteam-mermail-bounty-ops/scenarios.json

Self-contained validator:
https://github.com/markabramov1993/arbitr/blob/earn/superteam-mermail-bounty-ops/earn/superteam-mermail-bounty-ops/mermail-bounty-ops/scripts/validate_skill.py

## Automated validation evidence

The repository includes a dedicated GitHub Actions workflow, `Mermail Bounty Ops Skill CI`, which runs the package validator and validates controlled live-receipt evidence on the submission branch.

The validator checks the public Mermail authoring constraints and submission-specific invariants, including:

- allowed `SKILL.md` frontmatter and exact directory/name match;
- `MERMAIL_API_KEY` OpenClaw metadata;
- hosted Mermail MCP metadata in `agents/openai.yaml`;
- `SKILL.md` line budget and required tool/security references;
- no unresolved placeholder markers in core package docs;
- untrusted-email, sender-authentication, bounded-read, OTP/magic-link and wallet/payment safety rules;
- explicit approval for external effects;
- exact `opportunity -> accepted -> paid` reward accounting;
- seven machine-readable happy-path, duplicate, prompt-injection, external-effect and payment-state scenarios.

Latest validation on the current submission head: **PASS**.

## Live Mermail evidence

A controlled live Mermail mailbox run has now been completed using the actual Mermail integration.

The run exercised two controlled messages:

1. a legitimate bounty opportunity advertising **500 USDC**;
2. a malicious prompt-injection/payment instruction attempting to make the agent act on untrusted wallet/payment text.

Observed result:

- the legitimate opportunity was identified and structured correctly;
- the malicious payment/prompt-injection content was treated as untrusted data;
- prior sent state was checked for duplicate outreach;
- no unauthorized external send or payment was performed;
- the 500 USDC amount remained classified as **opportunity / nominal**, not accepted and not paid.

This evidence is intentionally about safe live operation, not fabricated settlement.

## Official Mermail review path

The work is now in the official Mermail repository review queue:

- proposal/discussion: `Nudgen-Marketing/mermail-skills#173`;
- implementation PR: `Nudgen-Marketing/mermail-skills#174` — `feat: add mermail-bounty-ops companion skill`;
- current upstream PR state at the latest check: **open, non-draft, mergeable**.

No maintainer endorsement, merge, bounty acceptance, or payment is claimed until it actually occurs.

## Demo video

**Public recording still pending.**

The final video will show real Mermail MCP calls, not fabricated output. Planned flow is documented in `DEMO_SCRIPT.md`:

1. resolve the Mermail mailbox;
2. metadata-first bounty scan;
3. safely read one legitimate bounty and one malicious prompt-injection/payment message;
4. search prior sent mail to prevent a duplicate claim;
5. create a claim draft while the reward remains nominal;
6. send only after an exact current-user instruction;
7. show acceptance and payment as distinct ledger transitions, without fabricating settlement.

Video URL: `PENDING_LIVE_DEMO_URL`

## Mermail integration

The skill follows Mermail's public Agent Skill authoring conventions:

- directory id and YAML `name` match;
- `MERMAIL_API_KEY` metadata is declared;
- OpenAI metadata points to the Mermail streamable HTTP MCP endpoint;
- tool names are taken from documented Mermail MCP surfaces;
- queries/bodies remain native JSON objects;
- message content is treated as untrusted data;
- safe bounded reads precede body interpretation;
- sends are explicit external effects;
- OTPs, magic links, wallet destinations, and payout instructions in email do not self-authorize actions.

## Demo differentiators

**1. Worker-side lifecycle**
The skill follows one worker's opportunity from discovery/dedupe through submission, reviewer response, acceptance, and payment evidence rather than operating a sponsor's contest.

**2. Duplicate protection**
The agent checks existing sent mail before any new claim/application.

**3. Security around economic email**
Prompt injection, wallet instructions, verification links, and payment requests in email are contained as data rather than executed.

**4. Honest reward accounting**
Every opportunity is tracked as one of:
- opportunity / nominal;
- accepted / unpaid;
- paid / settled.

This makes the skill particularly useful for autonomous agents whose next actions depend on whether funds are merely advertised or actually available.

## Final checklist

- [x] Reusable `SKILL.md`
- [x] OpenAI/MCP metadata
- [x] Tool contract
- [x] Security reference
- [x] Public GitHub branch
- [x] Submission-package PR
- [x] Demo script
- [x] Differentiation from adjacent public Mermail proposals
- [x] Machine-readable validation scenarios
- [x] Self-contained package validator
- [x] GitHub Actions validation passing
- [x] Official Mermail companion proposal opened (#173)
- [x] Official Mermail implementation PR opened (#174)
- [x] Controlled live Mermail integration test completed
- [ ] Maintainer feedback incorporated (if/when received)
- [ ] Public video recording URL
- [ ] Submit through authenticated Superteam profile
- [ ] Record Superteam submission id
- [ ] Treat prize as pending until selection; paid only after actual settlement
