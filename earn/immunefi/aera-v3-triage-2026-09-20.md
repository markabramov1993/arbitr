# Aera V3 Immunefi triage — 2026-09-20

Status: **read-only review; no reportable vulnerability confirmed yet**

Program facts checked against Immunefi on 2026-09-20:
- max reward: $500,000
- smart-contract Medium: $2,000
- smart-contract High: $10,000
- PoC required
- scope includes Base and freshly-added Arbitrum/Optimism V3 assets

Evidence:
- upstream snapshot: aera-finance/aera-contracts-public
- workflow run: https://github.com/markabramov1993/arbitr/actions/runs/35511273213
- build: success with Solidity 0.8.34
- Slither: completed far enough to emit detector evidence; detector findings make its step non-zero
- analyzer evidence artifact retained by GitHub Actions

## Triage

### arbitrary-send-erc20 — MultiDepositorVault.enter
Slither flags `token.safeTransferFrom(sender, address(this), tokenAmount)`.

Current disposition: **likely false positive / expected authority flow**.

Reason:
- `enter` is protected by `onlyProvisioner`.
- user synchronous entry from Provisioner passes `msg.sender` as `sender`.
- request-solving path passes `address(this)` after the Provisioner has custody/approval.
- no public path was found that lets an arbitrary caller choose another wallet as `sender` while also satisfying `onlyProvisioner`.

Do not submit without a path that lets an unauthorized caller control the provisioner call.

### incorrect-equality — ProvisionerV2.getSyncRedeemEpochState
Flagged check:
`epochTimestamp == _syncRedeemEpochTimestamp`.

Current disposition: **expected epoch identity comparison**.

It selects whether the stored redeemed amount belongs to the current PFC anchor epoch. No fund-loss/freeze impact demonstrated.

### uninitialized-local
Flagged:
- `BaseVault._executeSubmit(...).ctx`
- `ProvisionerV2._solveRequestsVault(...).depositsExist`
- `ProvisionerV2._solveRequestsVault(...).solverTip`
- `CallbackHandler._storeCallbackApprovals(...).i`

Current disposition: **Solidity zero-initialization / deliberate reuse; no impact shown**.
- booleans and uints intentionally begin at zero/false.
- BaseVault overwrites the operation context fields before non-static authorization use; static branch does not perform that merkle-root check.
- CallbackHandler deliberately starts `i` at zero unless the empty-existing-list branch sets it to one.

### unused-return — EnumerableMap set/remove
Flagged guardian and whitelist map mutations.

Current disposition: **idempotent mutation semantics; no security impact shown**.
Ignoring whether an entry previously existed does not by itself create unauthorized access or fund movement.

## Next security work
Prioritize manual/invariant review of the in-scope V3 money paths rather than reporting raw detector output:
1. ProvisionerV2 deposit/redeem request accounting and sync-redeem caps.
2. PriceAndFeeCalculatorV2 price-age / fee / epoch transitions.
3. MultiDepositorVault mint/burn accounting around callbacks/hooks.
4. BaseVault callback approval cleanup and guardian/whitelist transitions.
5. TransferBlacklistHook behavior during mint/burn/transfer edge cases.

Only escalate to Immunefi after a reproducible impact-aligned PoC exists. No live contracts are to be attacked or modified.
