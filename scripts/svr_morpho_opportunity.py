#!/usr/bin/env python3
"""Project Morpho Blue health factors using a future Chainlink SVR median.

Read-only research scanner. It never signs or submits a transaction.
The key mapping is Chainlink proxy -> aggregator: Morpho oracles normally store
proxy feed addresses, while the SVR websocket hint names the underlying aggregator.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
import urllib.request

MORPHO_GQL = "https://api.morpho.org/graphql"
RPC = "https://base-mainnet.g.alchemy.com/public"
WAD = 10**18
ORACLE_SCALE = 10**36
LIQUIDATION_CURSOR = 0.3
MAX_LIF = 1.15


def gql(query: str, variables: dict) -> dict:
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(MORPHO_GQL, data=body, headers={"content-type": "application/json", "user-agent": "profit-engine-research/0.7"})
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.loads(r.read())
    if out.get("errors"):
        raise RuntimeError(json.dumps(out["errors"], separators=(",", ":")))
    return out["data"]


def cast_call(address: str, sig: str) -> str:
    last = ""
    for rpc in (RPC, "https://mainnet.base.org"):
        p = subprocess.run(["cast", "call", address, sig, "--rpc-url", rpc], text=True, capture_output=True, timeout=25)
        if p.returncode == 0:
            return p.stdout.strip()
        last = (p.stderr or p.stdout).strip()
    raise RuntimeError(last)


def first_int(text: str) -> int:
    return int(text.split()[0], 0)


def market_query() -> str:
    return r'''
query Markets($first: Int!, $skip: Int!, $where: MarketFilters) {
  markets(first: $first, skip: $skip, orderBy: BorrowAssetsUsd, orderDirection: Desc, where: $where) {
    items {
      marketId listed lltv irmAddress
      loanAsset { address symbol decimals }
      collateralAsset { address symbol decimals }
      oracle {
        address type
        data {
          ... on MorphoChainlinkOracleV2Data {
            baseFeedOne { address }
            baseFeedTwo { address }
            quoteFeedOne { address }
            quoteFeedTwo { address }
          }
          ... on MorphoChainlinkOracleData {
            baseFeedOne { address }
            baseFeedTwo { address }
            quoteFeedOne { address }
            quoteFeedTwo { address }
          }
        }
      }
    }
  }
}
'''


def positions_query() -> str:
    return r'''
query Positions($first: Int!, $marketIds: [String!]) {
  marketPositions(first: $first, orderBy: BorrowShares, orderDirection: Desc,
    where: { marketUniqueKey_in: $marketIds }) {
    items {
      market { marketId }
      user { address }
      state { borrowShares borrowAssets borrowAssetsUsd collateral collateralUsd }
    }
  }
}
'''


def feed_entries(oracle: dict):
    data = (oracle or {}).get("data") or {}
    for key in ("baseFeedOne", "baseFeedTwo", "quoteFeedOne", "quoteFeedTwo"):
        item = data.get(key) or {}
        addr = item.get("address")
        if addr and int(addr, 16) != 0:
            yield key, addr


def lif(lltv_wad: int) -> float:
    lltv = lltv_wad / WAD
    return min(MAX_LIF, 1.0 / (1.0 - LIQUIDATION_CURSOR * (1.0 - lltv)))


def resolve_proxy(feed: str, cache: dict[str, str | None]) -> str | None:
    k = feed.lower()
    if k in cache:
        return cache[k]
    try:
        out = cast_call(feed, "aggregator()(address)")
        resolved = out.split()[0].lower()
        if int(resolved, 16) == 0:
            resolved = None
    except Exception:
        resolved = None
    cache[k] = resolved
    # Be polite to public RPCs and avoid burst limits.
    time.sleep(0.015)
    return resolved


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--aggregator", required=True)
    ap.add_argument("--median", required=True)
    ap.add_argument("--feed-decimals", type=int, required=True)
    ap.add_argument("--max-markets", type=int, default=500)
    ap.add_argument("--max-positions", type=int, default=500)
    args = ap.parse_args()
    agg = args.aggregator.lower()
    future = int(args.median, 0)

    try:
        current = first_int(cast_call(args.aggregator, "latestAnswer()(int256)"))
        desc = cast_call(args.aggregator, "description()(string)").strip('"')
    except Exception as e:
        print(json.dumps({"error": "feed_read_failed", "detail": str(e)}))
        return 2

    markets = []
    for skip in range(0, args.max_markets, 100):
        data = gql(market_query(), {"first": min(100, args.max_markets-skip), "skip": skip, "where": {"chainId_in": [8453]}})
        batch = data["markets"]["items"]
        markets.extend(batch)
        if len(batch) < 100:
            break

    proxy_cache: dict[str, str | None] = {}
    matched = []
    matched_proxies = set()
    for m in markets:
        for slot, feed in feed_entries(m.get("oracle") or {}):
            feed_l = feed.lower()
            resolved = agg if feed_l == agg else resolve_proxy(feed, proxy_cache)
            if resolved == agg:
                m["_slot"] = slot
                m["_feed_proxy"] = feed
                matched_proxies.add(feed)
                matched.append(m)
                break

    print(json.dumps({
        "kind": "feed",
        "description": desc,
        "aggregator": args.aggregator,
        "current_raw": current,
        "future_raw": future,
        "decimals": args.feed_decimals,
        "current": current/(10**args.feed_decimals),
        "future": future/(10**args.feed_decimals),
        "delta_bps": (future/current-1)*10000 if current else None,
        "base_markets_scanned": len(markets),
        "unique_proxy_feeds_resolved": len(proxy_cache),
        "matched_markets": len(matched),
        "matched_proxy_feeds": sorted(matched_proxies),
    }, separators=(",", ":")))

    if not matched:
        return 0

    ids = [m["marketId"] for m in matched]
    byid = {m["marketId"].lower(): m for m in matched}
    try:
        data = gql(positions_query(), {"first": min(args.max_positions, 500), "marketIds": ids})
    except Exception as e:
        print(json.dumps({"error":"positions_query_failed","detail":str(e),"market_ids":ids}, separators=(",", ":")))
        return 3

    candidates = []
    seen = 0
    oracle_price_cache = {}
    for p in data["marketPositions"]["items"]:
        mid = p["market"]["marketId"].lower()
        m = byid.get(mid)
        if not m:
            continue
        st = p.get("state") or {}
        borrow = int(st.get("borrowAssets") or 0)
        coll = int(st.get("collateral") or 0)
        if borrow <= 0 or coll <= 0:
            continue
        seen += 1
        oa = m["oracle"]["address"].lower()
        try:
            if oa not in oracle_price_cache:
                oracle_price_cache[oa] = first_int(cast_call(oa, "price()(uint256)"))
            oracle_current = oracle_price_cache[oa]
        except Exception:
            continue
        slot = m["_slot"]
        ratio = (future/current) if current else 1.0
        if slot.startswith("quoteFeed"):
            ratio = 1.0 / ratio
        oracle_future = int(oracle_current * ratio)
        lltv = int(m["lltv"])
        max_borrow_now = (coll * oracle_current // ORACLE_SCALE) * lltv // WAD
        max_borrow_future = (coll * oracle_future // ORACLE_SCALE) * lltv // WAD
        hf_now = max_borrow_now / borrow
        hf_future = max_borrow_future / borrow
        if hf_future <= 1.01:
            incentive = lif(lltv)
            borrow_usd = float(st.get("borrowAssetsUsd") or 0)
            gross_usd = borrow_usd * (incentive - 1.0)
            candidates.append({
                "marketId": m["marketId"],
                "borrower": p["user"]["address"],
                "pair": f"{m['collateralAsset']['symbol']}/{m['loanAsset']['symbol']}",
                "feedProxy": m["_feed_proxy"],
                "slot": slot,
                "lltv": lltv/WAD,
                "hf_now": hf_now,
                "hf_future": hf_future,
                "crosses_liquidation": hf_now > 1.0 and hf_future <= 1.0,
                "borrowAssetsUsd": borrow_usd,
                "collateralUsd": float(st.get("collateralUsd") or 0),
                "lif": incentive,
                "gross_bonus_usd_approx": gross_usd,
                "oracle": m["oracle"]["address"],
            })

    candidates.sort(key=lambda x: (not x["crosses_liquidation"], x["hf_future"], -x["gross_bonus_usd_approx"]))
    print(json.dumps({"kind":"summary","positions_examined":seen,"candidate_count":len(candidates),"crossing_count":sum(1 for c in candidates if c["crosses_liquidation"])}, separators=(",", ":")))
    for c in candidates[:50]:
        print(json.dumps({"kind":"candidate", **c}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
