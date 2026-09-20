# Anchor program skeleton

This program maps the runnable ProofRoute MVP invariants onto Solana accounts.

Implemented instructions:
- create_intent
- attest_intent
- authorize_intent with two distinct verifier accounts and a 25 bps disagreement bound
- settle_intent

Accounts:
- IntentAccount
- VerificationAccount
- ExecutionReceipt

The program is compile-checked in CI. The program ID is the standard Anchor development placeholder and is NOT a deployed ProofRoute address. Before devnet deployment it must be replaced with a generated keypair/program id.

This skeleton does not custody tokens yet. The bounded Jupiter CPI/transaction adapter is the next phase; keeping custody out of this commit makes the policy state machine reviewable before value movement is introduced.
