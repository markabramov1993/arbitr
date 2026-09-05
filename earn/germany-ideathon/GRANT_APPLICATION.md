# ProofRoute — Solana Foundation Germany Grant Application

## Project
**ProofRoute — Verifiable DeFi Execution for Autonomous Agents**

**One-line pitch:** Agents can find opportunities. ProofRoute makes them prove the trade before capital moves.

**Builder:** `markabramov1993`  
**Region:** Germany  
**Category:** Solana infrastructure / agent infrastructure / DeFi safety

## What are you building?

ProofRoute is a Solana-native intent, verification and execution-receipt layer for autonomous agents and capital providers.

An agent proposes a bounded economic action with max input, min output, evidence hash and expiry slot. Independent verifier agents reproduce the candidate action. Capital is released only when the result satisfies a user-controlled policy. The final execution creates an on-chain receipt that records expected versus realized outcome.

The protocol separates three states that are often dangerously conflated in agent systems:

1. **Intent** — what an agent claims it can do.
2. **Verification** — what independent agents can reproduce before capital movement.
3. **Execution receipt** — what Solana actually settled.

## Problem

Autonomous agents can already discover liquidations, route swaps, propose treasury rebalances and generate transaction plans. Discovery output is not reliable enough to authorize capital automatically:

- quotes become stale;
- routes revert;
- fees erase expected profit;
- multiple agents report the same opportunity;
- one agent's simulation is not an independent trust signal;
- a successful simulation still needs hard execution bounds.

ProofRoute is designed as a neutral safety and coordination layer between agent discovery and capital execution.

## Why Solana?

ProofRoute benefits directly from Solana's execution model:

- slot-bounded validity for expiring intents;
- atomic settlement for funding + execution + receipt creation;
- low-cost high-frequency verification/receipt records;
- composability with wallets, treasuries, DEXs and lending protocols;
- permissionless verifier participation;
- public, portable agent execution history.

A centralized quote service can simulate an action, but it cannot provide neutral shared settlement and portable multi-agent execution reputation without becoming the trusted intermediary.

## Current proof of work

The public `markabramov1993/arbitr` repository already contains practical work around the failure mode ProofRoute addresses:

- live opportunity discovery;
- cost-aware filtering;
- stateful execution validation;
- liquidation candidate screening;
- rejection of false positives when an API reports an opportunity but protocol execution rejects it;
- explicit separation of candidate, executable and realized states.

Public concept document:
`https://github.com/markabramov1993/arbitr/blob/main/earn/germany-ideathon/README.md`

Concise pitch:
`https://github.com/markabramov1993/arbitr/blob/main/earn/germany-ideathon/PITCH.md`

## Grant request

**Requested amount: 5,000 USDG**

The amount is sized around a narrow, shippable MVP rather than a full protocol launch.

### Proposed use of funds

| Workstream | Budget | Deliverable |
|---|---:|---|
| Solana/Anchor program engineering | 2,000 USDG | Intent, verification, expiry and receipt lifecycle on devnet/test environment |
| Reference verifier + execution adapter | 1,250 USDG | Deterministic evidence hashing and one real Solana execution route |
| Frontend/dashboard | 750 USDG | Live intents, verifier agreement and expected-vs-realized view |
| Testing / RPC / infra / monitoring | 500 USDG | Reproducible test suite, hosted indexer/demo environment |
| Documentation, demo and external builder feedback | 500 USDG | Public integration docs, demo video and initial builder interviews |

Grant funds will be used for the ProofRoute project and its stated build costs; they are not treated as unrestricted trading capital.

## Milestones

### M1 — Public protocol specification
- Anchor account schema
- intent lifecycle/state machine
- deterministic intent fingerprint
- verification evidence format
- expiry and policy rules

### M2 — Working on-chain MVP
- `create_intent`
- `attest_intent`
- `fund_intent`
- `settle_intent`
- `expire_intent`
- tests for unauthorized funding/settlement and stale intents

### M3 — Reference verifier
- reads candidate intent
- reproduces quote/simulation
- rejects stale or below-policy candidates
- writes verifier attestation

### M4 — Real execution adapter
- one bounded Solana route, initially a rebalance/swap path
- hard max-input/min-output protection
- execution receipt with actual output and settled slot

### M5 — Public demo
- two competing candidate intents
- one rejected by verification
- one approved
- capital reaches only the approved path
- expected-vs-realized receipt visible in dashboard

## 6-week execution plan

**Week 1:** protocol spec, Anchor scaffold, account/instruction tests  
**Week 2:** verifier evidence format + intent fingerprinting  
**Week 3:** reference verifier and quote adapter  
**Week 4:** bounded execution + receipt settlement  
**Week 5:** dashboard, telemetry, failure/replay tests  
**Week 6:** external builder test, docs, demo, deployment cleanup

## Success criteria

The MVP is successful if it proves all of the following:

1. an agent can submit an intent without receiving unrestricted capital;
2. a second agent can independently verify or reject it;
3. an expired or below-policy intent cannot be funded;
4. a valid intent can settle through one real Solana route;
5. expected and realized results are recorded separately;
6. another builder can reproduce the flow from public documentation.

Primary product metric:

> Percentage of agent-proposed actions rejected before capital movement that would otherwise revert or fall below the user's minimum-net policy.

## Target users

- Solana agent developers
- DAO/protocol treasuries
- automated searchers/liquidators
- wallets and capital providers
- teams building agent-to-agent commerce

The initial wedge is developers already dealing with transaction simulation, quotes, slippage and execution failures rather than a broad consumer launch.

## Business path

Potential revenue after MVP validation:

- small success-based settlement fee;
- paid verifier quorum / specialist verifier marketplace;
- treasury policy and analytics SaaS.

The protocol can retain a free public/developer tier to encourage integrations.

## Team

`markabramov1993` — Germany-based solo builder for the current phase, covering product architecture, automation/backend, protocol design and public documentation.

The scope is deliberately limited to one execution route and one clear verification lifecycle. If the MVP validates demand, the highest-leverage additional role is a Solana/Anchor engineer or frontend product designer.

## Why this grant now?

The ideathon phase has already produced the architecture and concrete protocol schema. The next risk is implementation, not ideation. A Germany grant would directly convert the current public proof of work into a working Solana MVP with an independently reproducible demo.
