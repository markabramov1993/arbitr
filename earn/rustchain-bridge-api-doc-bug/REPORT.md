# RustChain Bridge API documentation mismatch

## Summary

`Scottcjn/Rustchain/docs/bridge-api.md` correctly documents `POST /api/bridge/initiate` as an operator/admin-only endpoint requiring `X-Admin-Key`, but the Python integration example later in the same file calls that endpoint without the required header.

A reader copying the example cannot obtain the documented success response on a correctly configured operator node; it should follow the documented `401 unauthorized` path.

## Current-source evidence

Audited on 2026-09-13 against current public `Scottcjn/Rustchain` main.

The authentication section states that RustChain-origin deposits are operator-assisted/admin-authenticated and require:

```text
X-Admin-Key: <admin-key>
```

The endpoint section repeats:

```text
POST /api/bridge/initiate
Headers (operator/admin only):
X-Admin-Key: <admin-key>
Content-Type: application/json
```

But the Python integration example uses:

```python
response = requests.post(
    f"{BASE_URL}/api/bridge/initiate",
    json={
        "direction": "deposit",
        "source_chain": "rustchain",
        "dest_chain": "solana",
        "source_address": miner_id,
        "dest_address": dest_address,
        "amount_rtc": amount_rtc,
    },
)
```

No `X-Admin-Key` header is sent, and the function has no operator-key parameter.

Source:
https://github.com/Scottcjn/Rustchain/blob/main/docs/bridge-api.md

## Expected behavior

The example should either:

1. be an explicitly operator-only executable example that accepts/reads an admin key and sends `X-Admin-Key`; or
2. be rewritten as non-executable pseudocode so an end user cannot mistake it for a public self-service bridge call.

Any fixed example should clearly state that the operator secret must not be committed or distributed to end users.

## Actual behavior

The document's normative authentication section and its copy-paste integration example contradict each other. The example omits a header that the same document says is mandatory and therefore demonstrates a request that should fail authorization.

## Suggested correction

```python
def initiate_bridge_deposit(miner_id, dest_address, amount_rtc, admin_key):
    response = requests.post(
        f"{BASE_URL}/api/bridge/initiate",
        headers={"X-Admin-Key": admin_key},
        json={...},
        timeout=30,
    )
```

Add an adjacent warning that only the authorized bridge operator should possess `admin_key`; native RTC -> wRTC is not a public self-service operation.

## Impact

Documentation/integration bug. Copy-paste users get an authorization failure and can incorrectly conclude the bridge is broken or public-but-malfunctioning. The inconsistency is particularly confusing because the top of the same document explicitly explains the operator-assisted custody boundary.

## Safety

This finding is source/documentation based. No production bridge transaction, admin-key guess, balance mutation, or other state-changing request was made.

## Submission context

Prepared by `markabramov1993` after a GitHub App attempt to open the upstream issue returned `403 Resource not accessible by integration`. Public timestamped report is kept here for the documented email fallback route.
