# PROFIT ENGINE v0.7 — FLASH research/execution pipeline

Branch: `profit-engine-v07`

This branch is the controlled Base/EVM research branch for the FLASH / Profit Engine project. Its job is to turn live market state into reproducible fork evidence before any real-money execution is considered.

## Core pipeline

`SEARCH → READ STATE → DECODE → QUOTE/SIMULATE → OPTIMIZE SIZE → COSTS/NET → FORK/BACKTEST → PAPER RANK`

**Public mainnet signing/broadcasting is OFF by default.** Fork/paper results are not counted as earned cash.

## What is actually present in this branch

### Solidity
- `contracts/AtomicRouteHarness.sol` — local atomic route validation harness.
- `contracts/MorphoSelfFundedLiquidator.sol` — Morpho liquidation research executor.
- `contracts/MorphoSelfFundedLiquidatorV2.sol` — second iteration of the Morpho liquidation research executor.

### Live/research scripts
- `scripts/base_dex_arb_scan.py` — Base DEX arbitrage scan.
- `scripts/base_dex_spread_quick.py` — quick spread screen.
- `scripts/cbbtc_focused_quote.py` — focused cbBTC quoting research.
- `scripts/perp_funding_scan.py` — basis/funding scan.
- `scripts/svr_monitor.py` — read-only SVR monitoring.
- `scripts/svr_live_edge.py` — SVR live-edge research.
- `scripts/svr_aave_preliq_live.py` — Aave pre-liquidation live research.
- `scripts/svr_morpho_opportunity.py` — Morpho/SVR opportunity research.

### Build/test
- Foundry project via `foundry.toml`.
- Tests live under `test/`.
- GitHub Actions under `.github/workflows/` provide remote CI/research workers.

## Verified project-level results

The wider Profit Engine project has already demonstrated the following classes of checks:
- successful Solidity/Foundry CI after enabling optimizer + `via_ir` where required;
- public Base RPC health/failover path in CI;
- Morpho live candidate discovery followed by stateful fork validation;
- historical liquidation reconstruction and DEX exit analysis;
- read-only Chainlink SVR / Atlas research;
- DEX route scanning and atomic fork validation.

These are research/validation results, **not realized profit**.

## Current execution policy

A candidate is eligible for real-money execution only after all of the following are true:
1. live state and quotes are fresh;
2. the complete route executes atomically on a fresh fork;
3. flash-loan premium, gas, Base L1 data fee, DEX fees and conservative slippage are included;
4. net profit remains positive after all costs;
5. the same route survives repeated validation immediately before signing;
6. private keys/secrets are never written to the repository or workflow logs.

Until then the system stays read-only/fork-only.

## Documentation note

The master project archive previously referenced a `FlashArbExecutor.sol`. That file is **not present in this branch snapshot**, so this README deliberately does not claim it is available here. The branch inventory above reflects the repository state, not an older release manifest.

## Capital bootstrap

The intended bootstrap path remains:
- €0: public RPC + GitHub Actions + local/fork simulation;
- first external bounty/payment or other verified funding;
- reserve a small amount for gas/RPC;
- only then enable tightly controlled capital deployment.

See `START_CAPITAL.md` for the branch bootstrap notes.
