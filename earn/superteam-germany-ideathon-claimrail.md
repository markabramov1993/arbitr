# ClaimRail

> **On-chain claim locks and escrow for human + AI bounty work.**

## Tagline

Stop five builders from unknowingly solving the same paid task. ClaimRail gives public bounties a neutral, time-limited claim lock, USDC escrow, proof-of-submission trail, and automatic release when a claim expires.

## Why this matters

Open-source and agent bounty markets have a coordination problem. A task can look completely unclaimed in the issue tracker while several contributors are already working on it in forks or private branches. The result is duplicated engineering effort, last-minute races, sponsor review overload, and frustrated contributors who finish valid work that can no longer be paid.

The problem becomes larger as autonomous coding agents enter these markets. Agents can discover and start work faster than humans, but today there is no shared, platform-neutral state that answers four simple questions:

1. Is this bounty actually available right now?
2. Who has the active right to attempt it, and until when?
3. Is the reward really escrowed?
4. What submission was made against that claim?

ClaimRail turns those answers into public state rather than platform-specific comments and screenshots.

## Why blockchain is necessary

A normal database can track claims, but it cannot provide a neutral coordination and payment layer across GitHub, Superteam, Algora, agent marketplaces, independent sponsors, and autonomous agents without making one company the trusted custodian.

ClaimRail uses Solana for the parts that benefit from shared, programmable ownership:

- **USDC escrow:** sponsors lock the advertised reward before contributors spend time.
- **Claim lock:** a contributor or agent obtains a short exclusive attempt window recorded on-chain.
- **Refundable bond:** optional small bond discourages spam claims without becoming a paywall; successful submission or clean expiry returns it according to the task policy.
- **Automatic expiry:** stale claims become available again without waiting for a maintainer.
- **Submission commitment:** a Git commit/PR/content hash is attached to the claim, creating a tamper-evident chronology.
- **Portable reputation:** completed, expired, abandoned, and disputed claims form a platform-independent work history.
- **Programmable settlement:** sponsor approval, multisig approval, or later oracle/attestation modules can release the escrow.

Solana is a strong fit because the product may need a large number of low-value state transitions—claim, heartbeat, submit, release, expire—where low fees and fast finality matter.

## User flow

### Sponsor

1. Creates a bounty and deposits the reward in USDC.
2. Selects claim duration, optional bond, review window, and max concurrent claim slots.
3. Links the external work item (GitHub issue, Superteam listing, spec URL, etc.).

### Builder or agent

1. Sees `AVAILABLE` rather than guessing from comments.
2. Creates a claim for a fixed period.
3. Works against the external repository/task.
4. Submits a PR URL plus commit/content hash before expiry.
5. Receives the bond back when the submission is valid under the bounty policy.

### Resolution

- Sponsor accepts → escrow pays the claimant.
- Claim expires with no submission → lock is released automatically.
- Sponsor needs more review time → review state is visible while new claims follow the configured policy.
- Disputed work → funds remain escrowed while the configured resolver/multisig decides.

## MVP for the Colosseum Hackathon

### On-chain Anchor program

Accounts / instructions:

- `Bounty`
  - sponsor
  - reward mint + amount
  - external task hash / URI
  - claim duration
  - review duration
  - max concurrent claims
  - state
- `Claim`
  - bounty
  - claimant
  - claimed_at
  - expires_at
  - submission_hash
  - submission_uri
  - state
- instructions
  - `create_bounty`
  - `fund_bounty`
  - `claim`
  - `submit`
  - `accept`
  - `release_expired_claim`
  - `cancel_before_claim`
  - `resolve_dispute`

### Web app

- Searchable bounty board
- `AVAILABLE / CLAIMED / SUBMITTED / PAID / EXPIRED` status
- Wallet connection
- USDC funding and claim actions
- Countdown until claim expiry
- GitHub issue + PR linking
- Public claim history

### GitHub integration

A lightweight GitHub App / Action can:

- display the current ClaimRail state in an issue/PR;
- verify that the submitted commit belongs to the linked repository;
- post the PR URL and commit hash back to ClaimRail;
- release a claim if the contributor explicitly abandons it.

## First target market

Start with high-churn OSS and AI-agent bounty programs, where duplicate work is already a visible problem:

- funded GitHub issues;
- autonomous coding-agent work queues;
- hackathon micro-bounties;
- protocol contributor programs;
- independent maintainers that want escrow without building a payment backend.

The protocol does not need every platform to migrate. A sponsor can create a ClaimRail bounty that points to any public URL, and a browser/GitHub integration can expose the on-chain claim state beside the original task.

## Business model

Initial model: **0% fee while bootstrapping liquidity and integrations**.

Later options:

- small fee on successfully paid bounties;
- sponsor SaaS for private repositories, analytics, policy templates, and reviewer automation;
- API tier for agent fleets that need high-volume discovery/claim/settlement;
- optional arbitration fee only when a dispute is opened.

The base claim/escrow state remains portable and publicly verifiable.

## Why now

AI coding agents dramatically reduce the time needed to discover and attempt tasks. That makes coordination—not raw coding speed—the bottleneck. Existing issue comments such as “/attempt” are useful social signals but are not universal, escrowed, atomic, or portable across platforms.

ClaimRail is infrastructure for a world where both people and software agents compete for paid work in real time.

## Hackathon build plan

### Week 1
- Anchor program + USDC escrow
- deterministic bounty/claim PDAs
- claim expiry + release
- unit/property tests

### Week 2
- web dashboard
- GitHub issue/PR linking
- submission commitments
- devnet deployment

### Week 3
- GitHub Action/App prototype
- agent API (`discover → claim → submit → status`)
- demo with multiple agents racing for one task
- security review + documentation + pitch demo

## Demo scenario

1. Sponsor funds a 100 USDC GitHub bounty.
2. Two autonomous agents discover it simultaneously.
3. Agent A atomically obtains the single claim slot.
4. Agent B immediately sees `CLAIMED until 14:32 UTC` and does not waste compute.
5. Agent A opens a PR and commits its PR URL + head SHA to the claim.
6. Sponsor accepts the work.
7. 100 USDC is released from escrow and the completed claim becomes part of Agent A's portable reputation.

Then repeat with Agent A abandoning the task: the claim expires and Agent B can claim it without a maintainer manually clearing a comment.

## Long-term vision

ClaimRail becomes a neutral settlement rail for autonomous work markets: discovery can happen anywhere, execution can happen by any person or agent, while availability, escrow, claim priority, submission provenance, and payout have one composable source of truth.

The same primitive can later support milestone work, reviewer markets, security bounties, dataset labeling, agent-to-agent subcontracting, and machine-priced tasks.
