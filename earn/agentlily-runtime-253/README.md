# AgentLily Runtime bounty #253 — ready patch

Target: `Lilly-Protocol/agentlily-runtime#253` — **$50**.

## Root cause

The repository uses fast-check `^4.9.0`. In fast-check v4, `fc.date()` may generate `Invalid Date` by default. Mapping such a value through `Date.prototype.toISOString()` throws `RangeError: Invalid time value` before the property can exercise `InMemoryMemoryStore`.

## Fix

```ts
const recordedAtArb = fc
  .date({ noInvalidDate: true })
  .map((d) => d.toISOString());
```

This follows fast-check's documented v4 migration behavior and retains the full valid JavaScript Date domain. It does not impose an arbitrary year restriction.

## Scope

- Test-only change.
- Keeps all three property tests at `numRuns: 50`.
- No runtime/API behavior changes.

The adjacent `.patch` file is ready to apply directly to current `main`.

GitHub claimant: `markabramov1993`.
