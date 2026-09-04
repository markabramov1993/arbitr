# ProofRoute — Verifiable DeFi Execution for Autonomous Agents

**Tagline:** Agents can find opportunities. ProofRoute makes them prove the trade before capital moves.

Submission concept for the Superteam Germany Road to Colosseum Ideathon.

## 1. Problem

Autonomous agents can already search markets, read protocols, generate strategies and propose transactions. The hard part is deciding which proposed action deserves capital.

Today a user or treasury typically sees a black-box claim such as:

- “this liquidation is profitable”
- “this route has positive arbitrage”
- “this rebalance will save money”

But an API quote can be stale, a route can revert, fees can erase the spread, and multiple agents can report the same opportunity. This makes autonomous capital allocation hard to trust.

**The missing primitive is a verifiable execution receipt before capital is committed.**

## 2. Product

ProofRoute is a Solana-native marketplace and settlement layer for **verified execution intents**.

An agent submits an intent describing:

1. the action it wants to execute,
2. the expected inputs and outputs,
3. the maximum capital required,
4. the minimum acceptable net result,
5. a simulation/fork-equivalent evidence hash,
6. an expiry slot.

Independent verifier agents reproduce the simulation and attest to the result. Capital providers can fund only intents that meet their policy. The final transaction executes atomically on Solana; settlement records what actually happened.

The system therefore creates three durable objects:

- **Intent** — what the agent proposes.
- **Verification quorum** — what independent agents reproduced.
- **Execution receipt** — what the chain actually settled.

## 3. Why Solana is necessary

This is not “blockchain for the sake of blockchain.” ProofRoute needs a shared execution layer because the core product is coordination between mutually untrusted agents and capital providers.

Solana gives the product:

- **Atomic settlement:** capital transfer, protocol action and payout can settle in one transaction when the route supports it.
- **Slot-bounded validity:** intents expire against chain state instead of relying on a centralized server timestamp.
- **Permissionless verification:** independent agents can verify and compete without being approved by one operator.
- **Auditable reputation:** successful, reverted and expired execution receipts become public performance history.
- **Composable treasury rules:** DAOs, bots and wallets can fund the same standardized intent format.
- **Low-cost high-frequency receipts:** recording many small verification and execution events is economically plausible.

A centralized service could provide quotes, but it could not provide neutral shared settlement and portable agent reputation without becoming the trusted counterparty.

## 4. Initial use cases

### A. Liquidation execution
An agent detects an unhealthy lending position. It submits the repay amount, collateral expected, exit route and minimum net value. Verifiers reproduce the state. A capital provider funds only if the verified net remains above threshold.

### B. DEX route / arbitrage execution
Agents compete to submit profitable routes. ProofRoute deduplicates equivalent opportunities and ranks them by verified net outcome rather than claimed spread.

### C. Treasury rebalancing
A DAO treasury can publish a policy such as “convert up to 50k USDC into SOL only if expected all-in slippage is <20 bps.” Agents compete to provide verified execution intents.

### D. Agent-to-agent paid research
One agent can pay another only when its proposed action passes verification, turning market research into a machine-native marketplace.

## 5. MVP for the Colosseum Hackathon

### On-chain program

Accounts:

- `IntentAccount`
  - proposer
  - input_mint / output_mint
  - max_input
  - min_output
  - expiry_slot
  - evidence_hash
  - status
- `VerificationAccount`
  - intent
  - verifier
  - reproduced_output
  - evidence_hash
- `ExecutionReceipt`
  - intent
  - executor
  - actual_input
  - actual_output
  - fee_paid
  - settled_slot

Instructions:

- `create_intent`
- `attest_intent`
- `fund_intent`
- `settle_intent`
- `expire_intent`

### Off-chain agent

A reference agent will:

1. monitor a small set of Solana DEX/lending markets,
2. create candidate intents,
3. quote routes using public RPC/protocol interfaces,
4. reject stale or negative-net candidates,
5. submit evidence hashes,
6. monitor verification quorum and settlement.

### Dashboard

A simple dashboard shows:

- live intents,
- verification agreement/disagreement,
- expiry slots,
- realized vs expected output,
- per-agent success/revert/expiry rates,
- cumulative value routed through verified intents.

## 6. Differentiation

Most agent trading systems optimize **discovery and execution**. ProofRoute focuses on the missing layer between them: **capital authorization based on reproducible evidence**.

It is closer to a clearinghouse for autonomous agents than another trading bot.

The product does not promise profit and does not require one proprietary strategy. Any agent can propose a strategy; ProofRoute standardizes how that strategy earns the right to touch capital.

## 7. Business model

Three potential revenue streams:

1. **Settlement fee:** small bps fee only on successfully settled intents.
2. **Verifier marketplace fee:** capital providers pay for higher verification quorum or specialist verifier sets.
3. **Treasury policy SaaS:** teams pay for policy templates, analytics and private strategy metadata while settlement remains on-chain.

A free developer tier can keep public intents and low-value settlement permissionless.

## 8. Go-to-market

Start with developers already operating Solana agents and searchers.

Initial integration targets:

- Solana agent frameworks and MCP tools,
- DEX aggregators and trading agents,
- lending / liquidation bots,
- DAO treasury automation,
- agent hackathon teams that need a safe capital-control primitive.

The wedge is simple: **“Show me the receipt before I fund your agent.”**

## 9. Safety and risk controls

ProofRoute deliberately separates *proposed* profit from *realized* settlement.

Rules for the reference implementation:

- no opportunity is counted as realized before an on-chain receipt exists,
- expired evidence cannot authorize new capital,
- each intent includes hard max-input and min-output bounds,
- verifier disagreement is visible rather than averaged away,
- duplicate opportunity fingerprints are deduplicated,
- no private keys are stored in the public indexer,
- treasury funding policy remains user-controlled.

## 10. What is already de-risked

The concept is based on practical execution research already performed in the public `markabramov1993/arbitr` repository:

- live opportunity discovery,
- cost-aware ranking,
- stateful fork validation on EVM chains,
- liquidation candidate filtering,
- false-positive rejection when an API says a position is liquidatable but the protocol rejects the actual call,
- separation of candidate, executable and realized stages.

The hackathon work is to translate those lessons into a **Solana-native standardized intent + verification + receipt protocol**, not to port an EVM bot.

## 11. Hackathon build plan

**Phase 1 — Protocol schema**
Anchor program, intent lifecycle, expiry and receipt accounts.

**Phase 2 — Verifier**
Reference verifier agent, deterministic evidence hashing and quorum rules.

**Phase 3 — Execution adapter**
One real Solana route (for example a Jupiter-routed rebalance) with strict input/output bounds.

**Phase 4 — Dashboard and telemetry**
Expected-vs-realized analysis, agent scorecards and replayable evidence.

**Phase 5 — Demo**
Two competing agents submit intents; one fails verification, one passes; capital is released only to the verified intent and an execution receipt is created on Solana.

## 12. Success metric

The first meaningful metric is not TVL or token price.

It is:

> **Percentage of agent-proposed actions rejected before capital movement that would otherwise have reverted or fallen below the user’s minimum-net policy.**

If ProofRoute can reduce bad autonomous executions while preserving permissionless competition between agents, it becomes useful infrastructure for the agent economy.

---

**Project:** ProofRoute  
**Category:** Solana / Agent Infrastructure / DeFi  
**Country:** Germany  
**Builder:** markabramov1993  
**Repository:** https://github.com/markabramov1993/arbitr  
**Status:** Ideathon concept; MVP intended for the upcoming Colosseum Hackathon.
