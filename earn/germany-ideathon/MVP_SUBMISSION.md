# Superteam Germany — Build your MVP submission draft

Listing: Road to Colosseum Hackathon: Build your MVP  
Region: Germany  
Prize pool: 8,000 USDG  
Winner announcement: 2026-10-09

## Project
ProofRoute — Verifiable DeFi Execution for Autonomous Agents

## One-line pitch
Agents can find opportunities. ProofRoute makes them prove the trade before capital moves.

## Live Solana/Jupiter evidence

A read-only Jupiter quote was fetched and validated in CI on 2026-09-20:
- 0.1 SOL -> USDC
- quoted output: 10.825722 USDC
- context slot: 448719060
- route steps: 1
- canonical evidence hash: `3d6e1249ca9d42d98d0945e1b53a0c94163550d69ab4c0f8ec02fa6871b9da96`
- run: https://github.com/markabramov1993/arbitr/actions/runs/35508130762

No wallet or transaction was used. Full snapshot: `earn/germany-ideathon/mvp/JUPITER_EVIDENCE.md`.

## Current MVP evidence
- Runnable policy engine: earn/germany-ideathon/mvp/proofroute.py
- 8 deterministic invariant tests: earn/germany-ideathon/mvp/test_proofroute.py
- End-to-end two-agent demo: earn/germany-ideathon/mvp/demo.py
- Browser dashboard: earn/germany-ideathon/mvp/dashboard/index.html
- Solana/Anchor program state-machine skeleton: earn/germany-ideathon/mvp/anchor/programs/proofroute/src/lib.rs
- GitHub Actions validation: ProofRoute MVP Validate
- Review PR: markabramov1993/arbitr#9

## Demo story
1. Agent A proposes a bounded USDC route.
2. Two independent verifiers reproduce the evidence and agree within 25 bps.
3. Policy authorizes the intent only after quorum.
4. Agent B proposes a route whose reproduced output is below the user's minimum.
5. Agent B is rejected before capital authorization.
6. Agent A settles inside max-input/min-output bounds.
7. ProofRoute records expected-vs-realized data in an execution receipt.

## Safety boundary
The current demo never moves user funds. The next value-moving phase is a bounded Jupiter adapter after the Anchor state machine is compile-clean and reviewed.

## Remaining before native submission
- replace development Anchor program id with generated devnet program id;
- deploy the program to Solana devnet;
- feed the live Jupiter evidence snapshot into the verifier/intent flow and add bounded devnet execution;
- record a short demo video;
- submit the Superteam form once authenticated browser access is restored.

No prize is counted as earned before official judging and payment.
