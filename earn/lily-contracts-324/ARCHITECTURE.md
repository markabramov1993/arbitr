# Architecture

This document describes the high-level storage, durability, and authorization design shared by the Lily Protocol Soroban contracts. It is intended for contributors, auditors, and integrators who need to understand where state lives, how long it lasts, and who can change it.

## Storage durability

Soroban provides two storage kinds that the contracts use deliberately:

- **Instance storage** (`env.storage().instance()`): small, frequently accessed state tied to the contract deployment. Used for global config, admin addresses, schema/lifecycle state, and deployment-pinned admin addresses. Stateful entrypoints and most initialized reads refresh its TTL; the exceptions are called out below.
- **Persistent storage** (`env.storage().persistent()`): per-entity state that must survive for the lifetime of the protocol. Used for profiles, payment intents, payer indexes, and wallet bindings.

Both kinds are keyed by typed `DataKey` enums local to each contract crate. There is no shared `DataKey` across contracts.

## TTL policy

Shared TTL constants live in `crates/lily-common/src/lib.rs`:

```rust
pub const INSTANCE_BUMP_THRESHOLD: u32 = 17_280;   // ~1 day of ledgers
pub const INSTANCE_BUMP_AMOUNT: u32 = 172_800;     // ~10 days of ledgers
```

The helper `bump_instance(env)` extends the **instance storage** TTL by `INSTANCE_BUMP_AMOUNT` whenever it is called. Stateful operations and most initialized read entrypoints call it on their happy path. The lightweight `is_initialized` view in each contract does not bump instance TTL, and `protocol::get_pending_admin` also reads without bumping. Constructors only pin deployment-time state and do not use the normal entrypoint bump path.

Persistent storage entries do not currently call `extend_ttl` explicitly. In a production deployment, long-lived per-entity records (profiles, intents, payer indexes, bindings) should be bumped explicitly or the protocol should rely on periodic keeper transactions to keep critical records alive.

## Initialization state

Each contract stores an `Initialized` flag in instance storage and rejects re-initialization with `ProtocolError::AlreadyInitialized`. Deployment also stores a `PinnedAdmin` address in instance storage through `__constructor`, which is the deployment-time anchor for the intended initial administrator.

## Authorization model

Three categories of actors appear across the contracts:

- **Admin**: Can change global config and perform privileged actions such as deactivating profiles, deactivating wallet bindings, settling payment intents, or transferring admin authority.
- **Self-authorized actor**: The agent, controller, or payer that owns or controls a specific record and signs operations that affect it.
- **Dual authorization**: Some wallet operations require both the agent and the wallet to sign.

Read-only entrypoints are listed separately for each contract below.

---

## `contracts/protocol`

Global protocol configuration.

### Storage keys

| Key | Type | Durability | Description |
|---|---|---|---|
| `Admin` | `Address` | Instance | Active protocol admin address. |
| `PendingAdmin` | `Address` | Instance | Proposed admin awaiting `accept_admin`. |
| `Treasury` | `Address` | Instance | Treasury address for fee collection. |
| `FeeBps` | `u32` | Instance | Fee in basis points. |
| `Initialized` | `bool` | Instance | One-time initialization flag. |
| `SchemaVersion` | `u32` | Instance | Current protocol contract storage/schema version. |
| `PinnedAdmin` | `Address` | Instance | Deployment-time initial admin pinned by `__constructor`. |

### Deployment / initialization

- `__constructor` (pins the intended initial admin)
- `initialize` (initial admin-authorized configuration)

### Admin functions

- `set_fee_bps`
- `set_treasury`
- `transfer_admin` (proposes a pending admin)
- `accept_admin` (pending admin accepts authority)

### Read-only functions

- `is_initialized` (does not call `bump_instance`)
- `schema_version`
- `get_config`
- `get_pending_admin` (does not call `bump_instance`)

---

## `contracts/identity`

Agent identity registry.

### Storage keys

| Key | Type | Durability | Description |
|---|---|---|---|
| `Admin` | `Address` | Instance | Registry admin address. |
| `Initialized` | `bool` | Instance | One-time initialization flag. |
| `Profile(Address)` | `AgentProfile` | Persistent | Per-agent profile record. |
| `PinnedAdmin` | `Address` | Instance | Deployment-time initial admin pinned by `__constructor`. |

### Deployment / initialization

- `__constructor`
- `initialize`

### Admin functions

- `deactivate`
- `reactivate`

### Self-authorized functions

- `register` (agent signs)
- `update_profile` (current controller signs)

### Read-only functions

- `is_initialized` (does not call `bump_instance`)
- `get_profile`
- `get_profile_opt`

---

## `contracts/wallet`

Wallet policy registry.

### Storage keys

| Key | Type | Durability | Description |
|---|---|---|---|
| `Admin` | `Address` | Instance | Wallet registry admin address. |
| `Initialized` | `bool` | Instance | One-time initialization flag. |
| `SchemaVersion` | `u32` | Instance | Current wallet contract storage/schema version. |
| `Binding(Address)` | `WalletBinding` | Persistent | Per-agent wallet binding. |
| `PinnedAdmin` | `Address` | Instance | Deployment-time initial admin pinned by `__constructor`. |

### Deployment / initialization

- `__constructor`
- `initialize`

### Admin functions

- `admin_deactivate`

### Self-authorized functions

- `update_spend_limit` (agent signs)
- `set_enabled` (agent signs)

### Dual-authorized functions

- `bind_wallet` (agent and wallet both sign)
- `rebind_wallet` (agent and replacement wallet both sign)

### Read-only functions

- `is_initialized` (does not call `bump_instance`)
- `get_binding`
- `get_binding_opt`

---

## `contracts/payments`

Payment intent and settlement.

### Storage keys

| Key | Type | Durability | Description |
|---|---|---|---|
| `Admin` | `Address` | Instance | Settlement admin address. |
| `Treasury` | `Address` | Instance | Treasury address for fee collection. |
| `FeeBps` | `u32` | Instance | Fee in basis points. |
| `NextIntentId` | `u64` | Instance | Monotonically increasing intent ID counter. |
| `Wallet` | `Address` | Instance | Wallet-policy contract used to validate payer bindings. |
| `Initialized` | `bool` | Instance | One-time initialization flag. |
| `SchemaVersion` | `u32` | Instance | Current payments contract storage/schema version. |
| `Intent(u64)` | `PaymentIntent` | Persistent | Per-intent payment record. |
| `PinnedAdmin` | `Address` | Instance | Deployment-time initial admin pinned by `__constructor`. |
| `PayerIntents(Address)` | `Vec<u64>` | Persistent | Per-payer index of payment intent IDs. |

### Deployment / initialization

- `__constructor`
- `initialize`

### Admin functions

- `settle_intent`
- `set_fee_bps`
- `set_treasury`
- `transfer_admin`

### Self-authorized functions

- `create_intent` (payer signs)
- `cancel_intent` (payer signs)

### Read-only functions

- `is_initialized` (does not call `bump_instance`)
- `schema_version`
- `get_config`
- `get_next_intent_id`
- `get_intent`
- `get_intent_opt`

---

## Shared primitives

### `crates/lily-common`

- `ProtocolError`: typed errors used across all contracts.
- `PaymentStatus`: enum used by `payments` (and potentially future settlement contracts).
- `MAX_BPS`: basis-point ceiling.
- `bump_instance`: TTL refresh helper.

### `crates/lily-test-support`

Test-only helpers; no runtime storage.

## Versioning

Where a contract stores `SchemaVersion`, that instance key records the explicit storage/schema version. Other lifecycle state remains tied to the deployed contract and wasm revision; upgrade behavior is documented separately in `docs/UPGRADABILITY.md`.
