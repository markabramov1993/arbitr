# PROFIT ENGINE — Capital Ledger

Updated: 2026-09-04

This ledger deliberately separates real money from bounty face value and simulated PnL.

## 1. Confirmed capital

| Bucket | Confirmed amount | Evidence rule |
|---|---:|---|
| Cash / stablecoin bounty payouts | $0 confirmed | Count only after an actual transfer, platform payout, or independently verifiable wallet receipt |
| RTC | UNKNOWN live balance | Count only after wallet balance/history is read successfully for the configured miner ID |
| DeFi execution profit | $0 confirmed | Count only settled on-chain net profit after loan fees, DEX fees, gas, slippage and relay/builder costs |

**CONFIRMED_USD_EQUIVALENT = $0 + verified RTC value (currently unknown)**

Historical forks, oracle-valued liquidations, paper arbitrage and bounty sticker prices are NOT capital.

## 2. Active external earning pipeline

| Opportunity | Face value | State | Count as cash? |
|---|---:|---|---|
| Mova Store #91 / PR #257 | $90 | Formal upstream PR open; mergeable; waiting for maintainer review/CI authorization | NO |
| Mova Store #53 | $45 | Patch + formatting verified in fork; upstream PR creation blocked by integration; competitor has announced work | NO |
| RustChain / RTC claims | mixed RTC | Multiple submissions sent; live wallet receipt not yet verified | NO |
| Superteam agent-eligible radar | variable | Open listings tracked; submission/winner status required | NO |
| Other bounty submissions | variable | Pending replies/acceptance | NO |

## 3. Capital ladder

1. **BOOTSTRAP** — use zero-cost GitHub Actions, public RPC, forks and external bounties.
2. **GAS RESERVE** — first confirmed crypto/stablecoin receipts are ring-fenced for execution costs.
3. **CONTRACT RESERVE** — fund deployment/verification only after the gas reserve exists.
4. **LIVE MICRO-EXECUTION** — start with the cheapest chain/route and tiny controlled notional.
5. **FLASH-LIQUIDITY EXECUTION** — flash loans only when the exact transaction is reproducibly profitable on a current fork and remains positive under conservative cost assumptions.
6. **SCALE** — increase route coverage and execution frequency only from realized profit, not from paper PnL.

## 4. Main on-chain tracks

### A. Liquidations
- Morpho/Base position scan
- borrower health / LLTV boundary detection
- fork execution
- collateral-sale quote
- flash-liquidity sourcing where useful
- atomic repayment

### B. DEX arbitrage
- same-chain multi-DEX quote graph
- exact-input and exact-output simulation
- route-size optimization
- flash liquidity only when it improves net outcome
- private submission path where economically justified

### C. Chainlink SVR / oracle-linked opportunities
- readonly state/event monitoring
- opportunity reconstruction
- fork-only execution until invariants and economics are proven

### D. Protocol incentives / public rewards
- Superteam / GitHub / ecosystem bounties
- testnets / public incentive programs where legitimate and sybil-safe
- grants and agent work
- no fabricated activity, wash volume, fake users or duplicate identities

## 5. Mainnet activation gates

A candidate may move from paper/fork to a live transaction only when all of the following are true:

- current-state quote is available;
- transaction succeeds on a recent fork or equivalent deterministic simulation;
- flash-loan premium is included if used;
- every DEX/protocol fee is included;
- gas is estimated using a conservative current price;
- slippage / price impact is included;
- expected net profit remains positive after a safety buffer;
- revert/failure loss is bounded by the gas reserve;
- no private key or seed phrase is stored in this repository or CI logs;
- strategy does not depend on deceptive, manipulative, or prohibited activity.

## 6. Accounting states

Use exactly these labels in reports:

- **CONFIRMED** — money/token actually received or settled on-chain.
- **RECEIVABLE** — accepted/merged and payment is contractually or explicitly due, but not received yet.
- **PIPELINE** — submitted/open bounty or PR, not accepted yet.
- **FORK** — transaction succeeded only in simulation/fork.
- **PAPER** — calculated opportunity, not executed.
- **REJECTED / OCCUPIED** — competitor won/claimed it or opportunity is no longer actionable.

The project headline must always report CONFIRMED separately from every other state.
