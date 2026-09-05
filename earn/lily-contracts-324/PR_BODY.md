## Summary

Addresses Lilly-Protocol/lily-contracts issue #324 by syncing `docs/ARCHITECTURE.md` with the current per-contract `DataKey` layouts and public `#[contractimpl]` entrypoints.

## Changes

- Adds `PinnedAdmin` to all four storage-key tables.
- Adds protocol `PendingAdmin` and `SchemaVersion`.
- Adds wallet `SchemaVersion`.
- Adds payments `SchemaVersion`, `Wallet`, and `PayerIntents(Address)`.
- Adds missing public functions including protocol `accept_admin`, identity `reactivate`, wallet `rebind_wallet` and `admin_deactivate`, and payments admin setters/transfer.
- Adds read-only function lists so every public contract function is represented.
- Corrects the blanket TTL claim: `is_initialized` views and `protocol::get_pending_admin` do not call `bump_instance`; constructors also do not use the normal bump path.

## Scope

Documentation only. No contract behavior or storage code is changed.

Closes #324.
