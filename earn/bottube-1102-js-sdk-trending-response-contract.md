# BoTTube #1102 report — JS SDK `getTrending()` response type does not match production

## Summary

The official BoTTube JavaScript/TypeScript SDK declares `getTrending()` as returning `Promise<VideoListResponse>`, but the live `GET /api/trending` response does not satisfy `VideoListResponse`.

This is a client contract bug: TypeScript consumers are told that pagination fields exist even though production omits them.

## Current SDK contract

Re-checked against upstream `Scottcjn/bottube` main commit `d3f2231a24e6c462e54e409e72b21beef9720cf8` on 2026-09-10.

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

Original read-only evidence run:

https://github.com/markabramov1993/arbitr/actions/runs/34410032423

A second independent read-only probe on 2026-09-10 re-confirmed the mismatch:

https://github.com/markabramov1993/arbitr/actions/runs/34474241973

The second probe requested:

```text
GET https://bottube.ai/api/trending?limit=2
```

Observed:

```text
HTTP 200
TOP_KEYS ['category', 'videos']
category = null
videos length = 20
```

Therefore the live response again contains neither `total`, `page`, `per_page`, nor `has_more`, even though all four are required by the SDK's declared return type.

The endpoint also returned 20 videos despite `limit=2`. I am **not** claiming that behavior as a separate bounty item; it is only additional evidence that the live endpoint contract differs materially from the SDK contract.

## Impact

A TypeScript caller can write code that type-checks but fails at runtime:

```ts
const result = await client.getTrending({ limit: 2 });
console.log(result.total.toFixed(0)); // TypeScript accepts this; production `total` is undefined.
```

Pagination logic based on `page`, `per_page`, or `has_more` is likewise falsely presented as safe by the official SDK type.

## Expected

Either:

1. `/api/trending` should return the complete `VideoListResponse` shape promised by the SDK; or
2. the SDK should define and return a separate `TrendingResponse` matching the actual production payload.

The server and SDK should have one explicit contract, with a regression test using the production response shape.

## Duplicate check

Before filing, I searched the BoTTube issue and PR history and the RustChain bounty claim history for `VideoListResponse`, `getTrending`, `total`, `page`, `per_page`, and `has_more` response-shape mismatches. I found no prior report for this contract bug.

I also re-ran open/closed issue searches on 2026-09-10 for `getTrending()` and `/api/trending` pagination-contract terms and found no prior matching report. A different existing issue/PR concerns Python SDK `timeframe` behavior; this report does not claim that known problem.

## Environment / evidence

- Upstream main re-checked: 2026-09-10, commit `d3f2231a24e6c462e54e409e72b21beef9720cf8`
- Live endpoint re-checked: 2026-09-10 UTC
- Probe environment: GitHub-hosted Ubuntu 24.04 runner
- Request type: unauthenticated GET only
- No state changes, writes, accounts, payments, or private data used
- GitHub: `markabramov1993`
- RTC wallet: `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`
- AI disclosure: report prepared and verified with OpenAI GPT-5.6 Sol assistance under operator authorization.
