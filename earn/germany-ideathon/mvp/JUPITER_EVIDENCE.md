# ProofRoute — live Jupiter quote evidence

Captured by GitHub Actions on **2026-09-20T11:32:42Z**.

Workflow:
- ProofRoute Jupiter Live Quote
- run: https://github.com/markabramov1993/arbitr/actions/runs/35508130762
- commit: `705ba2072f95bac2ada2f668d52b6540e1662aab`

This is a **read-only quote snapshot**. No wallet, signature, transaction construction, swap, token transfer, or capital movement was performed.

## Route snapshot

- source: `https://api.jup.ag/swap/v1/quote`
- input mint: wrapped SOL `So11111111111111111111111111111111111111112`
- output mint: USDC `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- input amount: `100000000` lamports = 0.1 SOL
- quoted output: `10825722` USDC base units = 10.825722 USDC
- minimum output threshold at 50 bps: `10771594`
- slippage setting: 50 bps
- price impact returned by quote: `0`
- context slot: `448719060`
- route plan steps: `1`
- canonical evidence SHA-256: `3d6e1249ca9d42d98d0945e1b53a0c94163550d69ab4c0f8ec02fa6871b9da96`

The CI validation independently asserted:
- output amount > 0
- evidence hash is 64 hex chars
- at least one route-plan step exists

Result: **Live Jupiter evidence: PASS**.

## Why this matters for ProofRoute

This closes one gap between the deterministic policy demo and a real Solana data source: ProofRoute can now bind a live Jupiter quote to a canonical evidence hash that verifiers can reproduce.

The next step is still **not** to trade. It is to:
1. store the quote snapshot/evidence hash in the intent flow;
2. reproduce the quote/simulation independently;
3. deploy the policy state machine to devnet;
4. only then add a bounded value-moving adapter.
