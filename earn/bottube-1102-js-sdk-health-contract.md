# BoTTube #1102 functional bug report — JavaScript SDK `/health` response type is incompatible with the live API

Date verified: **2026-09-08**

Bounty route: `Scottcjn/rustchain-bounties#1102`

Reporter: `markabramov1993`

RTC wallet: `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`

## Summary

The official BoTTube JavaScript/TypeScript SDK declares `BoTTubeClient.health()` as returning:

```ts
Promise<{ status: string; timestamp: number }>
```

but the live `https://bottube.ai/health` endpoint returns a different object shape:

```json
{
  "agents": 1429,
  "humans": 144,
  "ok": true,
  "service": "bottube",
  "uptime_s": 83659,
  "version": "1.2.0",
  "videos": 3378
}
```

Neither `status` nor `timestamp` exists in the live response. TypeScript callers therefore compile successfully when reading `result.status` or `result.timestamp`, but those values are `undefined` at runtime.

## Live reproduction

A read-only GitHub Actions smoke run queried the documented public endpoint on 2026-09-08:

- Workflow: `BoTTube Docs Smoke`
- Run: https://github.com/markabramov1993/arbitr/actions/runs/34266991492
- HTTP status: `200`
- Content-Type: `application/json`
- Actual payload contained `ok`, `service`, `version`, `uptime_s`, `videos`, `agents`, `humans`.

No authentication, writes, fuzzing, or destructive requests were used.

## Source evidence

Current upstream file:

`Scottcjn/bottube/js-sdk/src/client.ts`

contains:

```ts
/** Check API health. */
async health(): Promise<{ status: string; timestamp: number }> {
  return this.request<{ status: string; timestamp: number }>('GET', '/health');
}
```

The current web API docs also document `/health` as a public health endpoint, while the live server payload is the object shown above.

## Impact

This is a runtime contract bug for TypeScript consumers. For example:

```ts
const health = await client.health();
console.log(health.status.toUpperCase());
```

is accepted by TypeScript because the SDK promises `status: string`, but fails at runtime because `health.status` is actually `undefined`.

The same applies to `timestamp`.

## Expected

The SDK return type should match the live server contract, ideally through a named exported type such as:

```ts
export interface HealthResponse {
  ok: boolean;
  service: string;
  version: string;
  uptime_s: number;
  videos: number;
  agents: number;
  humans: number;
}
```

and:

```ts
async health(): Promise<HealthResponse> {
  return this.request<HealthResponse>('GET', '/health');
}
```

A focused SDK test should mock the current live payload and assert the public return shape.

## Actual

The SDK advertises two fields that the server does not return and omits every field that the server does return.

## Duplicate check

Before filing, searches were run over current `Scottcjn/bottube` issues and PRs for combinations of `health`, `timestamp`, `status`, `js-sdk`, and `TypeScript`. No existing report or PR for this response-contract mismatch was found.

## Environment

- Live API: `https://bottube.ai/health`
- Verification runner: GitHub-hosted Ubuntu 24.04
- Upstream source: `Scottcjn/bottube` main
- Client affected: official `js-sdk/src/client.ts`

## Disclosure

This report was produced with AI assistance under operator authorization. All claimed live results were independently executed through the linked read-only CI run; no acceptance or payment is asserted until the maintainer verifies the finding.
