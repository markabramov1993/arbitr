# ProofRoute — Ideathon Pitch

## 1 — The problem
Autonomous agents can find trades, liquidations and treasury actions, but capital providers still have to trust a black-box claim that an action is executable and worthwhile.

A quote can be stale. A route can revert. Fees can erase the spread. Two agents can report the same opportunity.

**Discovery is not proof.**

## 2 — The product
**ProofRoute is a Solana-native pre-trade verification and post-trade receipt layer for autonomous agents.**

An agent proposes an execution intent. Independent verifiers reproduce it. Capital moves only if the intent satisfies policy. Solana records what actually settled.

Three objects:
- Intent
- Verification quorum
- Execution receipt

## 3 — Why now
AI agents are becoming capable of initiating economic actions, but safe capital authorization has not caught up.

The emerging agent economy needs a standard way to answer:

> “Why should this agent be allowed to touch capital for this specific action, right now?”

## 4 — Why Solana
- atomic settlement
- low-cost, high-frequency receipts
- slot-bounded expiry
- permissionless verifier competition
- composable treasury policies
- public performance history for agents

A centralized quote service cannot provide neutral shared settlement and portable execution reputation without becoming the trusted intermediary.

## 5 — Target users
Initial users:
- Solana agent developers
- DAO/protocol treasuries
- searchers and liquidators
- trading automation teams
- wallets/capital providers

Initial wedge: builders already using simulations, route quotes, slippage limits and automated execution.

## 6 — Hackathon MVP
Five capabilities only:
1. create a bounded intent
2. attest or reject it independently
3. enforce expiry + max-input/min-output
4. execute one real Solana route
5. record expected-vs-realized execution receipt

Demo: two agents submit competing intents; one fails verification, one passes; capital is released only to the verified intent.

## 7 — Why it is different
Aggregators find routes. RPCs simulate. Bots execute. Solver networks match intent to execution.

**ProofRoute focuses on capital authorization from reproducible evidence.**

It sits between discovery and execution rather than replacing either side.

## 8 — Business model
- success-based settlement fee
- verifier-marketplace fee for stronger quorum
- treasury policy/analytics SaaS

Public low-value intents can remain permissionless/free to drive integrations.

## 9 — Evidence already de-risked
The public `markabramov1993/arbitr` work already demonstrates the core failure mode:
- live opportunity discovery
- cost-aware filtering
- stateful execution validation
- false-positive rejection when an API says “liquidatable” but protocol execution rejects the call
- separation of candidate / executable / realized states

ProofRoute turns that lesson into a Solana-native protocol primitive.

## 10 — Team & next step
Germany-based solo builder: `markabramov1993`.

The MVP scope is deliberately narrow enough for a hackathon. Highest-leverage next addition after validation: Solana/Anchor engineering or frontend product design support.

**Success metric:** percentage of proposed agent actions rejected before capital movement that would otherwise revert or violate minimum-net policy.

### Closing
**Agents can find opportunities. ProofRoute makes them prove the trade before capital moves.**
