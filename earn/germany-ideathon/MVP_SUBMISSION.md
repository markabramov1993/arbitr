# Superteam Germany — Build your MVP submission draft

Listing: Road to Colosseum Hackathon: Build your MVP  
Region: Germany  
Prize pool: 8,000 USDG  
Winner announcement: 2026-10-09

## Project
ProofRoute — Verifiable DeFi Execution for Autonomous Agents

## One-line pitch
Agents can find opportunities. ProofRoute makes them prove the trade before capital moves.

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
- connect one bounded Jupiter quote/simulation adapter;
- record a short demo video;
- submit the Superteam form once authenticated browser access is restored.

No prize is counted as earned before official judging and payment.
