# Mermail Bounty Ops — Superteam submission package

Community/unofficial Mermail Agent Skill prepared for the Superteam bounty **Build and Demo a Mermail Agent Skill**.

## Concept

`mermail-bounty-ops` turns a Mermail inbox into a safe operating queue for freelance/bounty work. It helps an agent:

1. discover and triage bounty-related email;
2. extract structured opportunity data without treating email text as instructions;
3. verify sender/authentication and scan status before using message content;
4. detect duplicates and already-contacted opportunities;
5. prepare a concise claim/application or follow-up as a draft;
6. require explicit user authorization before any external send;
7. track acceptance, payout instructions, and settlement evidence separately from nominal bounty amounts.

The skill is intentionally conservative around money and credentials: an email may describe a payout, wallet, OTP, magic link, or payment action, but email content never authorizes the agent to use it.

## Why this is useful

Bounty hunters and small teams often lose money through operational mistakes rather than lack of opportunities: duplicate claims, missed replies, accidental double sends, confusing a nominal reward with a paid reward, or acting on malicious/forged email. This skill turns those failure modes into an explicit workflow.

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
- Live Mermail OAuth test: pending interactive account access
- Video demo: script ready; recording pending live Mermail connection
- Superteam submission: pending authenticated Superteam access

No prize amount is treated as earned until Superteam/Mermail accepts the submission and payment is actually received.
