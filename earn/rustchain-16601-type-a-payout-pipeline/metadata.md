# Publishing Metadata

## Primary title
**From Bounty to Balance: How RustChain RTC Payouts Actually Settle**

## Alternate titles
1. **Paid ≠ Settled: Inside the RustChain Bounty Payout Pipeline**
2. **How a 40 RTC Bounty Becomes a Real Wallet Receipt**

## Description

A source-backed walkthrough of the RustChain bounty payout lifecycle: contribution, eligibility verification, idempotent payout creation, the pending confirmation phase, and the final wallet receipt.

The video uses current public RustChain / rustchain-bounties source plus a real read-only wallet-history example from the contributor's own public CI evidence. No private keys, token-price claims, or live fund movement are shown.

Sources:
- https://github.com/Scottcjn/rustchain-bounties
- https://github.com/Scottcjn/Rustchain
- https://github.com/markabramov1993/arbitr

## Tags
RustChain, RTC, open source bounties, bounty payout, autonomous agents, agent economy, wallet accounting, GitHub Actions, developer rewards

## Chapters
- 00:00 Work is not money yet
- Verification before payout
- Queued is not settled
- Wallet receipt evidence
- Why agents need explicit money states
- Do not count the bounty — count the receipt

## Thumbnail direction
Dark technical flow:
`BOUNTY → VERIFIED → PENDING → SETTLED`
with a large **PAID ≠ SETTLED** headline.

No price chart, profit promise, exchange-rate claim, or third-party logo is required.
