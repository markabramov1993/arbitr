## Summary

Adds regression coverage for Lilly-Protocol/lily-contracts #321: protocol and payments initialization must reject an authenticated admin that differs from the address pinned by `__constructor`.

## Coverage

- Registers each contract with `pinned_admin`.
- Calls `initialize` using a distinct authenticated `other_admin` under the repository's `test_env()` (`mock_all_auths`).
- Verifies `try_initialize` returns typed contract error #3 (`Unauthorized`).
- Verifies `is_initialized()` remains false after the rejected attempt.
- Adds explicit `#[should_panic = "Error(Contract, #3)"]` coverage for the generated client panic path.
- Existing positive initialization tests remain unchanged.

## Scope

Tests only; no runtime behavior changes.

Closes #321.
