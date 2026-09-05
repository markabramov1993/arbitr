## Summary

Addresses Lilly-Protocol/lily-contracts issue #323 by bringing `docs/ERRORS.md` in line with the current shared error enum, typed authorization model, wallet binding semantics, and reentrancy guard.

## Changes

- Documents `ReentrantCall = 10` and its `NonReentrantGuard::acquire` raise path.
- Documents typed `Unauthorized = 3` separately from host-level signature/Auth failures.
- Corrects `WalletAlreadyBound`: any existing binding blocks `bind_wallet`, not only enabled bindings.
- Expands current `MissingRecord` raise sites, including `protocol::accept_admin`, `wallet::rebind_wallet`, and internal required-record getters.
- Explicitly records that optional getters return `None` on normal absence rather than raising `MissingRecord`, matching the current code.
- Updates per-contract notes and keeps the auth terminology consistent with `CONTRIBUTING.md`.

## Scope

Documentation only. No runtime contract behavior is changed.

Closes #323.
