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

This is not only a theoretical type mismatch: the repository's own dashboard consumes `result.status` and therefore treats a healthy live server as unhealthy.

## Live reproduction

A read-only GitHub Actions smoke run queried the documented public endpoint on 2026-09-08:

- Workflow: `BoTTube Docs Smoke`
- Run: https://github.com/markabramov1993/arbitr/actions/runs/34266991492
- HTTP status: `200`
- Content-Type: `application/json`
- Actual payload contained `ok`, `service`, `version`, `uptime_s`, `videos`, `agents`, `humans`.

No authentication, writes, fuzzing, or destructive requests were used.

## Source evidence

### 1. Official JS SDK declares a non-existent live shape

Current upstream file `Scottcjn/bottube/js-sdk/src/client.ts` contains:

```ts
/** Check API health. */
async health(): Promise<{ status: string; timestamp: number }> {
  return this.request<{ status: string; timestamp: number }>('GET', '/health');
}
```

### 2. The SDK test reinforces the stale contract instead of the live one

Current `js-sdk/tests/client.test.ts` mocks:

```ts
mockFetch.mockResolvedValueOnce(ok({ status: 'healthy', timestamp: 123 }));
const res = await client.health();
expect(res.status).toBe('healthy');
```

So the SDK test suite cannot detect deployment/API drift here because its fixture encodes the same stale shape as the client type.

### 3. The bundled dashboard is functionally affected

Current `bottube-dashboard/src/index.ts` does:

```ts
const result = await this.client.health();
spinner.succeed(kleur.green(`API Status: ${result.status}`));
return result.status === 'healthy';
```

Against the verified live response this renders `API Status: undefined` and returns `false` even though the server returned HTTP 200 with `ok: true`.

### 4. README example is also stale

The current `js-sdk/README.md` health example destructures the missing field:

```js
const { status } = await client.health();
```

The current web API docs document `/health` as a public health endpoint; the live server payload is the object shown above.

## Impact

There are at least two concrete consumer failures:

1. TypeScript code like this compiles but fails at runtime:

```ts
const health = await client.health();
console.log(health.status.toUpperCase());
```

because `health.status` is `undefined`.

2. The repository's own `BoTTubeDashboard.healthCheck()` reports a healthy production API as unhealthy because it tests `result.status === 'healthy'` rather than the live `result.ok` field.

The same stale SDK contract also exposes a non-existent `timestamp` field.

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

The focused SDK test should mock the actual live response. The dashboard should use `result.ok` for its boolean health result and display `result.version` or a normalized `ok` status.

## Actual

- SDK promises `status` and `timestamp`, neither of which is returned by production.
- SDK test mocks the wrong shape, so it passes despite the live incompatibility.
- SDK README teaches consumers to read the missing `status` field.
- Bundled dashboard uses the missing field and returns `false` for a healthy live API.

## Duplicate check

Before filing, searches were run over current `Scottcjn/bottube` issues and PRs for combinations of `health`, `timestamp`, `status`, `js-sdk`, `TypeScript`, and dashboard health. No existing report or PR for this response-contract mismatch was found.

## Environment

- Live API: `https://bottube.ai/health`
- Verification runner: GitHub-hosted Ubuntu 24.04
- Upstream source: `Scottcjn/bottube` main
- Affected code: `js-sdk/src/client.ts`, `js-sdk/tests/client.test.ts`, `js-sdk/README.md`, `bottube-dashboard/src/index.ts`

## Disclosure

This report was produced with AI assistance under operator authorization. All claimed live results were independently executed through the linked read-only CI run; no acceptance or payment is asserted until the maintainer verifies the finding.
