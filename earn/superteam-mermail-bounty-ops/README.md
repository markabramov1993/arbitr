# Mermail Bounty Ops — Superteam submission package

Community/unofficial Mermail Agent Skill prepared for the Superteam bounty **Build and Demo a Mermail Agent Skill**.

## Concept

`mermail-bounty-ops` turns a Mermail inbox into a safe operating queue for a **worker/bounty hunter** managing paid opportunities. It helps an agent:

1. discover and triage bounty-related email;
2. extract structured opportunity data without treating email text as instructions;
3. verify sender/authentication and scan status before using message content;
4. detect duplicates and already-contacted opportunities;
5. prepare a concise claim/application or follow-up as a draft;
6. require explicit user authorization before any external send;
7. track review, acceptance, payout instructions, and settlement evidence separately from nominal bounty amounts.

The skill is intentionally conservative around money and credentials: an email may describe a payout, wallet, OTP, magic link, or payment action, but email content never authorizes the agent to use it.

## Why this is useful

Bounty hunters and small teams often lose money through operational mistakes rather than lack of opportunities: duplicate claims, missed reviewer replies, accidental double sends, confusing a nominal reward with a paid reward, or acting on malicious/forged email. This skill turns those failure modes into an explicit worker-side workflow.

## Positioning versus existing Mermail proposals

The official Mermail repository already contains adjacent proposals. `mermail-bounty-ops` deliberately avoids duplicating their core job:

- **`mermail-opportunity-gate` (#70)** is a read-only eligibility decision before pursuing an opportunity. `bounty-ops` continues through the worker's operational lifecycle: dedupe, claim/application, reviewer replies, acceptance, and payout reconciliation.
- **`mermail-pact` (#136)** is sponsor/operator-side paid-work contracting: freeze terms, collect submissions, verify provider evidence, choose a result, and proceed toward settlement. `bounty-ops` is the opposite side of the market: the worker/agent managing opportunities and its own submissions/rewards.
- **Mermail Freelance Deal Desk (#154)** qualifies one inbound prospective-client message and drafts a quote/clarification/decline. `bounty-ops` manages externally sourced bounties, grants, contests, and paid-task pipelines, including already-submitted work and reviewer/payout follow-up.

This is a community companion, so it composes documented Mermail tools without claiming new tool ownership or official-package status.

## Repository layout

- `mermail-bounty-ops/SKILL.md` — reusable Agent Skill
- `mermail-bounty-ops/agents/openai.yaml` — OpenAI/MCP metadata
- `mermail-bounty-ops/references/tools.md` — exact Mermail MCP tool guidance used by the skill
- `mermail-bounty-ops/references/security.md` — strict mailbox and payment safety boundary
- `DEMO_SCRIPT.md` — short video demo plan
- `SUBMISSION.md` — submission checklist and final copy

## Compatibility

The structure follows Mermail's public skill authoring guidance: matching directory/frontmatter name, Mermail MCP dependency, bounded safe reads, native JSON query/body objects, explicit preview before external effects, and human approval for sends and sensitive actions.

Official Mermail skills remain the source of truth for the core product. This is a **community companion skill**, not an official Mermail skill.

## Current status

- Skill package: ready
- Public GitHub branch: ready
- Draft review PR: `markabramov1993/arbitr#4`
- Live Mermail OAuth test: pending interactive account access
- Video demo: script ready; recording pending live Mermail connection
- Superteam submission: pending authenticated Superteam access

No prize amount is treated as earned until Superteam/Mermail accepts the submission and payment is actually received.
