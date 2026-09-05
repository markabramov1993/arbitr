# Protocol Error Reference

`ProtocolError` is the shared typed error enum defined in `crates/lily-common/src/lib.rs`. Its numeric discriminants are part of the contract interface and currently run from 1 through 10. Signature failures from `Address::require_auth()` are host `Auth` errors; role failures checked with `require_caller` are typed `ProtocolError::Unauthorized` errors.

## Error table

| Code | Variant | Description | Current raise sites / examples |
|---|---|---|---|
| 1 | `AlreadyInitialized` | `initialize` was called after the contract's `Initialized` flag was set. | `identity::initialize`, `payments::initialize`, `protocol::initialize`, `wallet::initialize` |
| 2 | `NotInitialized` | An entrypoint guarded by `ensure_initialized` was called before initialization. | `ensure_initialized` helpers in `identity`, `payments`, `protocol`, and `wallet` |
| 3 | `Unauthorized` | A caller does not match the principal/role required by contract state. This is distinct from a missing/invalid signature, which is a host `Auth` error. | `lily_common::require_caller`; `payments::settle_intent` when `caller != stored admin`; deployment-pinned initial-admin checks where `require_initial_admin` is used |
| 4 | `InvalidInput` | Caller-provided data violates an input/state invariant. | `require_non_empty` / `require_non_whitespace`; inactive identity profile update; non-positive wallet limits; invalid payment amount or payer/payee relation; disabled-binding checks |
| 5 | `FeeBpsTooHigh` | A fee exceeds `MAX_BPS` (`10_000`, or 100%). | `require_valid_bps` from protocol/payments fee configuration paths |
| 6 | `AlreadyExists` | Creation would overwrite a unique record. | `identity::register` when `Profile(agent)` already exists |
| 7 | `MissingRecord` | A required record or prerequisite state is absent. | `identity::get_profile_internal`; `payments::get_intent_internal`; `wallet::get_binding_internal`; `protocol::accept_admin` with no pending admin; `wallet::rebind_wallet` with no existing binding; payments wallet/config lookups that explicitly map absence to this error |
| 8 | `PaymentAlreadyFinalized` | A payment transition was requested for an intent that is not `Pending`. | `payments::settle_intent`, `payments::cancel_intent` |
| 9 | `WalletAlreadyBound` | `bind_wallet` was called for an agent that already has any binding record. | `wallet::bind_wallet` |
| 10 | `ReentrantCall` | A `NonReentrantGuard` key is already held when another acquisition is attempted. | `lily_common::NonReentrantGuard::acquire`; guards used by `payments::settle_intent` and `payments::cancel_intent` |

## Authorization errors: typed role failure vs host signature failure

Lily has two authorization failure shapes and integrators should not conflate them:

1. **Wrong principal / role** — `require_caller(env, caller, expected)` raises typed `ProtocolError::Unauthorized` (`Error(Contract, #3)`). `payments::settle_intent` uses this check before signature verification so a non-admin `caller` receives the stable typed role error.
2. **Missing or invalid signature** — `require_auth_or_error` delegates to `Address::require_auth()`. Soroban reports this as a host-level `Auth` failure rather than `ProtocolError::Unauthorized`.

This matches the mapping documented in `CONTRIBUTING.md`: role mismatch is typed `Unauthorized`; cryptographic authorization failure remains a host error.

## Per-contract details

### `identity`

- `AlreadyInitialized` — `initialize` called after initialization.
- `NotInitialized` — entrypoints that call `ensure_initialized` before the registry has been initialized.
- `AlreadyExists` — `register` called for an `agent` that already has a `Profile` entry.
- `InvalidInput` — empty/invalid profile input or `update_profile` on an inactive profile.
- `MissingRecord` — operations that call `get_profile_internal` for an unregistered agent, including `update_profile`, `deactivate`, `reactivate`, and `get_profile`.
- `get_profile_opt` is intentionally optional: a missing profile is returned as `None`, not raised as `MissingRecord`.

### `payments`

- `AlreadyInitialized` — `initialize` called after initialization.
- `NotInitialized` — entrypoints protected by `ensure_initialized` before initialization.
- `Unauthorized` — `settle_intent` calls `require_caller` and raises code 3 when its `caller` is not the stored admin. Initial-admin pin validation also uses typed `Unauthorized` where the pinned-admin guard is applied.
- `InvalidInput` — invalid payment amount, invalid payer/payee relation, or empty storage-bound strings through shared validators.
- `FeeBpsTooHigh` — fee configuration paths using `require_valid_bps` with `fee_bps > MAX_BPS`.
- `MissingRecord` — `settle_intent`, `cancel_intent`, or `get_intent` when `get_intent_internal` cannot find the requested intent; explicit required-config lookups may also map absence to this code.
- `PaymentAlreadyFinalized` — `settle_intent` or `cancel_intent` when status is already `Settled` or `Cancelled`.
- `ReentrantCall` — the shared `NonReentrantGuard` used by `settle_intent` and `cancel_intent` rejects a second acquisition of the same guard key.
- `get_intent_opt` is intentionally optional and returns `None` for a missing intent.

### `protocol`

- `AlreadyInitialized` — `initialize` called after initialization.
- `NotInitialized` — initialized-only views/mutations guarded by `ensure_initialized`.
- `Unauthorized` — initial admin does not match the deployment-pinned `PinnedAdmin` where `require_initial_admin` is enforced.
- `FeeBpsTooHigh` — `initialize` or `set_fee_bps` with `fee_bps > MAX_BPS`.
- `MissingRecord` — `accept_admin` when no `PendingAdmin` exists.

### `wallet`

- `AlreadyInitialized` — `initialize` called after initialization.
- `NotInitialized` — entrypoints protected by `ensure_initialized` before initialization.
- `InvalidInput` — non-positive `spend_limit` or an operation requiring an enabled binding when that binding is disabled.
- `WalletAlreadyBound` — `bind_wallet` when *any* `Binding(agent)` record already exists. Disabled bindings are not silently overwritten; use `rebind_wallet` for an explicit replacement.
- `MissingRecord` — `rebind_wallet` when there is no existing binding, and operations using `get_binding_internal` (`update_spend_limit`, `set_enabled`, `admin_deactivate`, `get_binding`) when the binding is absent.
- `get_binding_opt` is intentionally optional and returns `None` for a missing binding.

## Reentrancy guard semantics

`NonReentrantGuard::acquire` stores a per-transition instance flag and raises `ProtocolError::ReentrantCall` (`Error(Contract, #10)`) when that flag is already present. Dropping the guard clears the flag, including during panic unwind. Payments currently hold distinct guard keys across the mutation windows of settlement and cancellation.

On Soroban hosts that reject direct cross-contract re-entry before user code runs, the host may surface its own context error first. The typed guard remains the contract-level defense-in-depth error for guard reacquisition paths that reach contract code.

## Notes

- `MAX_BPS` is `10_000` and represents 100% in basis points.
- `require_non_empty` and `require_non_whitespace` map invalid strings to `InvalidInput`.
- `ProtocolError` numeric codes are stable interface identifiers; consumers should match the typed code rather than panic text.
- Optional getters (`get_profile_opt`, `get_binding_opt`, `get_intent_opt`) return `Option` and do not convert normal absence into `MissingRecord`.
