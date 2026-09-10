# BoTTube: Coinbase wallet endpoint accepts non-hex EVM addresses

Target: `Scottcjn/bottube` current `main`

Verified upstream commit: `d3f2231a24e6c462e54e409e72b21beef9720cf8`

## Summary

`POST /api/agents/me/coinbase-wallet` validates a manually linked address using only `startswith("0x")` and `len(...) == 42`. It never verifies that the remaining 40 characters are hexadecimal.

As a result, an authenticated agent can persist an impossible EVM address such as `0xZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ`, and the API reports success.

## Local reproduction

The reproduction uses Flask's test client and a temporary SQLite database. It does not touch production state, real wallets, or real funds.

Control input:

```json
{"coinbase_address":"0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
```

Observed: HTTP `200`.

Invalid non-hex input:

```json
{"coinbase_address":"0xZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"}
```

Observed against the same upstream revision:

```text
NONHEX_STATUS= 200
NONHEX_JSON= {'agent': 'probe-agent', 'coinbase_address': '0xZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ', 'method': 'manual_link', 'ok': True}
PERSISTED_ADDRESS= 0xZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
BUG_REPRODUCED=true
```

Public CI reproduction:
https://github.com/markabramov1993/arbitr/actions/runs/34454374710

Evidence artifact:
https://github.com/markabramov1993/arbitr/actions/runs/34454374710/artifacts/10142830799

## Expected behavior

A manually linked Coinbase/Base wallet should be accepted only if it is a syntactically valid 20-byte EVM address (`0x` followed by exactly 40 hexadecimal characters). Invalid input should return HTTP 400 and must not replace the stored wallet field.

## Actual behavior

Any string of length 42 beginning with `0x` is accepted and stored.

## Impact

Payment-adjacent data integrity. An account can be left configured with an unusable wallet while the API reports a successful manual link. Downstream wallet/payout/payment consumers that trust this stored field can fail later instead of rejecting the configuration at the write boundary.

This report does **not** claim theft or successful transfer to an invalid address; the proven impact is acceptance and persistence of an invalid payout/wallet configuration.

## Root cause

Current logic in `bottube_x402.py`:

```python
if not (manual_address.startswith("0x") and len(manual_address) == 42):
    return _jsonify({"error": "Invalid Ethereum address format"}), 400
```

This is a length/prefix check rather than Ethereum address syntax validation.

## Suggested fix

Use a strict full match such as `0x[0-9a-fA-F]{40}` or a standard Ethereum-address parser. If checksum enforcement is desired, apply it after syntactic validation. Add a regression test covering a 42-character non-hex string.

## Duplicate check

Searches covered `coinbase-wallet`, `coinbase_address`, `non-hex`, `Ethereum address`, and matching PRs. Existing issue `Scottcjn/bottube#1230` covers malformed JSON and non-string values that crash the endpoint; it does not cover a string of the correct length containing non-hex characters. `#2210` covers x402 facilitator/pricing/auth-header issues, not address syntax validation.

AI assistance was used for source inspection, duplicate checking, and regression-test construction. The reproduction itself ran against the actual upstream code in GitHub Actions.
