# Sources / Claim Map

All technical claims are mapped to public source or reproducible evidence.

## Claim: payout automation requires verified eligibility

Source:
https://github.com/Scottcjn/rustchain-bounties/blob/main/scripts/bounty_payout.py

The current script builds a candidate set, verifies `bounty-eligible` / trusted eligibility evidence, resolves the payout destination, and skips claims already carrying the auto-pay confirmation marker.

## Claim: payout writes use stable idempotency keys

Source:
https://github.com/Scottcjn/rustchain-bounties/blob/main/scripts/bounty_payout.py

The review/docstring payout branches derive stable idempotency keys from the claim number.

## Claim: a successful transfer request can still be pending rather than settled

Source:
https://github.com/Scottcjn/rustchain-bounties/blob/main/scripts/bounty_payout.py

The script inspects `resp["phase"]`. When the phase is `pending`, the public issue text is deliberately described as **queued** and says the balance moves when the confirmation clears.

## Claim: RustChain API documents a pending transfer response with a 24-hour confirmation window

Source:
https://github.com/Scottcjn/Rustchain/blob/main/RustChain_API.postman_collection.json

The collection includes a `200 - Transfer pending` example with:
- `phase: pending`
- `pending_id`
- `tx_hash`
- `confirms_in_hours: 24.0`

## Claim: the payout pipeline has had silent-success failures

Source bounty:
https://github.com/Scottcjn/rustchain-bounties/issues/16471

The maintainer-authored issue documents multiple prior cases where automation reported success while the intended payout/label/confirmation effect did not happen.

## Claim: this contributor wallet showed 126.1 RTC and 11 settled inbound transfers on Sep 20, 2026

Public reproducible evidence:
https://github.com/markabramov1993/arbitr/actions/runs/35507570860

The workflow queried:
`https://rustchain.org/wallet/balance?miner_id=RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`

Observed:
- HTTP 200
- `amount_rtc: 126.1`
- history HTTP 200
- `HISTORY_COUNT=11`
- all eleven records are `transfer_in` from `founder_community`

The video uses this only as an accounting example. It does not imply an exchange rate or external liquidity.

## Excluded claims

This package intentionally does not claim:
- that RTC has a guaranteed external market value;
- that native RTC can currently be converted to USDC;
- that every advertised bounty will be accepted;
- that a pending transfer is spendable;
- guaranteed income, profit, or investment return.
