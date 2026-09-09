# BoTTube #1102 report — JS SDK `getTrending()` response type does not match production

## Summary

The official BoTTube JavaScript/TypeScript SDK declares `getTrending()` as returning `Promise<VideoListResponse>`, but the live `GET /api/trending` response does not satisfy `VideoListResponse`.

This is a client contract bug: TypeScript consumers are told that pagination fields exist even though production omits them.

## Current SDK contract

In `js-sdk/src/client.ts`, `getTrending()` returns:

```ts
async getTrending(options: TrendingOptions = {}): Promise<VideoListResponse> {
  const params = new URLSearchParams();
  if (options.limit) params.append('limit', String(options.limit));
  if (options.timeframe) params.append('timeframe', options.timeframe);
  const qs = params.toString();
  return this.request<VideoListResponse>('GET', `/api/trending${qs ? '?' + qs : ''}`);
}
```

In `js-sdk/src/types.ts`, `VideoListResponse` requires:

```ts
export interface VideoListResponse {
  videos: Video[];
  total: number;
  page: number;
  per_page: number;
  has_more: boolean;
}
```

## Production reproduction

A read-only GitHub Actions probe requested:

```text
GET https://bottube.ai/api/trending?limit=3
```

Evidence run:

https://github.com/markabramov1993/arbitr/actions/runs/34410032423

Observed:

```text
STATUS=200
TOP_LEVEL_KEYS=["category", "videos"]
HAS_TOTAL=False
HAS_PAGE=False
HAS_PER_PAGE=False
HAS_HAS_MORE=False
VIDEO_COUNT=20
```

So the live response is not a `VideoListResponse`. All four pagination fields declared as required are absent.

The same probe also shows the endpoint returned 20 videos even though `limit=3` was requested. I am not treating that as a separate bounty finding here; it is supporting evidence that the live endpoint contract differs from the JS SDK contract.

## Impact

A TypeScript caller can write code that type-checks but fails at runtime:

```ts
const result = await client.getTrending({ limit: 3 });
console.log(result.total.toFixed(0)); // TypeScript accepts this; production `total` is undefined.
```

Likewise, pagination logic based on `page`, `per_page`, or `has_more` is falsely presented as safe by the official SDK type.

## Expected

Either:

1. `/api/trending` should return the complete `VideoListResponse` shape promised by the SDK; or
2. the SDK should define and return a separate `TrendingResponse` matching the actual production payload.

The server and SDK should have one explicit contract, with a regression test using the production response shape.

## Duplicate check

Before filing, I searched the BoTTube issue and PR history and the RustChain bounty claim history for `VideoListResponse`, `getTrending`, `total`, `page`, `per_page`, and `has_more` response-shape mismatches. I found no prior report for this contract bug.

I did find PR #2218, which documents a different known problem: an ignored Python SDK `timeframe` argument. I deliberately did **not** claim that issue because it is already known. This report is specifically about the JavaScript SDK's declared response shape versus the live JSON shape.

## Environment / evidence

- Live endpoint checked: 2026-09-09 UTC
- Probe environment: GitHub-hosted Ubuntu 24.04 runner
- Request type: unauthenticated GET only
- No state changes, writes, accounts, payments, or private data used
- GitHub: `markabramov1993`
- RTC wallet: `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`
- AI disclosure: report prepared and verified with OpenAI GPT-5.6 Sol assistance under operator authorization.
