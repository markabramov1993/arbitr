# ProofRoute MVP

Agents can find opportunities. ProofRoute makes them prove the trade before capital moves.

This directory is the runnable MVP for the Superteam Germany Road to Colosseum Hackathon: Build your MVP track.

## Implemented now

- bounded execution intents: max_input, min_output and expiry slot
- canonical evidence hashing
- independent verifier attestations
- duplicate-verifier protection
- quorum and verifier-disagreement policy
- duplicate opportunity fingerprinting
- settlement bounds
- expected-vs-realized execution receipts
- a two-agent demo where one candidate is rejected before capital authorization

The reference implementation is dependency-free Python so the invariants can be tested in CI before they are mapped onto Anchor accounts.

## Run

    cd earn/germany-ideathon/mvp
    python -m unittest -v
    python demo.py

Expected result: 8 tests pass. The demo authorizes one verified intent, creates a deterministic receipt, and rejects a competing route whose reproduced output violates policy.

## Solana mapping

Next implementation maps the same invariants onto:
- IntentAccount
- VerificationAccount
- ExecutionReceipt

The first execution adapter will use one bounded Jupiter route. Exact quote/simulation evidence is hashed, independently reproduced, and settlement is allowed only after quorum and policy pass.

No private key or live user capital is required for this reference demo.
