#!/usr/bin/env python3
"""Read-only live Base triangular-arbitrage scanner.

Searches exact same-block quotes for two USDC-funded triangular cycles:
USDC -> WETH -> cbBTC -> USDC and the reverse token order.  Each leg chooses
the best executable quote across Uniswap V3 and Aerodrome Slipstream quoters.
No transaction is signed or broadcast.
"""
from __future__ import annotations

import json
import os
import urllib.request

RPCS = ["https://mainnet.base.org", "https://base-mainnet.g.alchemy.com/public"]
UNI_QUOTER = "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a"
AERO_V3 = "0xCd2A7D98e82D6107eac1828ce8DeAA6acB65b555"
AERO_LEGACY = "0x0A5aA5D3a4d28014f967Bf0f29EAA3FF9807D5c6"
AAVE_POOL = "0xA238Dd80C259a72e81d7e4664a9801593F98d1c5"
TOKENS = {
    "USDC": ("833589fcd6edb6e08f4c7c32d4f71b54bda02913", 6),
    "WETH": ("4200000000000000000000000000000000000006", 18),
    "cbBTC": ("cbb7c0000ab88b473b1f5afd9ef808440eed33bf", 8),
}
UNI_FEES = [100, 500, 3000]
AERO_SPACINGS = [1, 10, 50]
SIZES = [25, 50, 100, 250, 500, 1000, 2500, 5000]

# selectors are supplied by the workflow via `cast sig`
UNI_SEL = os.environ["UNI_SEL"].removeprefix("0x")
AERO_SEL = os.environ["AERO_SEL"].removeprefix("0x")
FLASH_SEL = os.environ["FLASH_SEL"]


def u(x: int) -> str:
    return (x & ((1 << 256) - 1)).to_bytes(32, "big").hex()


def a(x: str) -> str:
    return "0" * 24 + x.lower().removeprefix("0x")


def static_tuple(sel: str, tin: str, tout: str, amount: int, tier: int) -> str:
    return "0x" + sel + a(tin) + a(tout) + u(amount) + u(tier) + u(0)


def post(url: str, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"content-type": "application/json", "user-agent": "flash-profit-engine-v07"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def rpc(reqs):
    last = None
    for url in RPCS:
        try:
            out = post(url, reqs)
            if not isinstance(out, list):
                raise RuntimeError(out)
            return {str(x["id"]): x for x in out}, url
        except Exception as e:
            last = e
    raise RuntimeError(last)


def words(raw: str):
    h = raw.removeprefix("0x")
    return [int(h[i : i + 64], 16) for i in range(0, len(h), 64) if len(h[i : i + 64]) == 64]


def best_quote(token_in: str, token_out: str, amount: int):
    ia = TOKENS[token_in][0]
    oa = TOKENS[token_out][0]
    reqs = []
    meta = {}
    n = 0
    for fee in UNI_FEES:
        rid = str(n); n += 1
        meta[rid] = ("uni", fee, UNI_QUOTER)
        reqs.append({"jsonrpc": "2.0", "id": rid, "method": "eth_call", "params": [{"to": UNI_QUOTER, "data": static_tuple(UNI_SEL, ia, oa, amount, fee)}, "latest"]})
    for qname, qaddr in (("aero_v3", AERO_V3), ("aero_legacy", AERO_LEGACY)):
        for sp in AERO_SPACINGS:
            rid = str(n); n += 1
            meta[rid] = (qname, sp, qaddr)
            reqs.append({"jsonrpc": "2.0", "id": rid, "method": "eth_call", "params": [{"to": qaddr, "data": static_tuple(AERO_SEL, ia, oa, amount, sp)}, "latest"]})
    raw, used_rpc = rpc(reqs)
    best = None
    for rid, (venue, tier, _addr) in meta.items():
        x = raw.get(rid)
        if not x or "error" in x or not x.get("result"):
            continue
        w = words(x["result"])
        if len(w) < 4 or w[0] <= 0:
            continue
        row = {"venue": venue, "tier": tier, "out": w[0], "gas": w[3], "rpc": used_rpc}
        if best is None or row["out"] > best["out"]:
            best = row
    return best


def scalar_rpc(method: str, params):
    req = [{"jsonrpc": "2.0", "id": "0", "method": method, "params": params}]
    x, used = rpc(req)
    return x["0"]["result"], used


def flash_bps():
    raw, _ = scalar_rpc("eth_call", [{"to": AAVE_POOL, "data": FLASH_SEL}, "latest"])
    return int(raw, 16)


def gas_price():
    raw, _ = scalar_rpc("eth_gasPrice", [])
    return int(raw, 16)


def block_number():
    raw, _ = scalar_rpc("eth_blockNumber", [])
    return int(raw, 16)


def cycle(size: float, path: tuple[str, str, str, str]):
    amount = int(size * 10 ** TOKENS[path[0]][1])
    legs = []
    for tin, tout in zip(path, path[1:]):
        q = best_quote(tin, tout, amount)
        if not q:
            return None
        q = dict(q)
        q.update({"token_in": tin, "token_out": tout, "amount_in": amount})
        legs.append(q)
        amount = q["out"]
    out_h = amount / 10 ** TOKENS[path[-1]][1]
    return {"size_usdc": size, "path": "->".join(path), "output_usdc": out_h, "gross_usd": out_h - size, "legs": legs}


def main():
    block = block_number()
    gp = gas_price()
    fb = flash_bps()
    # Live WETH mark for gas conversion.
    ethq = best_quote("WETH", "USDC", 10**18)
    eth_usd = ethq["out"] / 1e6 if ethq else 2500.0
    print(json.dumps({"kind": "meta", "block": block, "gas_price_wei": gp, "flash_bps": fb, "eth_usd": eth_usd}, separators=(",", ":")))

    paths = (("USDC", "WETH", "cbBTC", "USDC"), ("USDC", "cbBTC", "WETH", "USDC"))
    rows = []
    for size in SIZES:
        for path in paths:
            try:
                r = cycle(size, path)
                if not r:
                    print(json.dumps({"kind": "unavailable", "size_usdc": size, "path": "->".join(path)}, separators=(",", ":")))
                    continue
                gas_units = sum(int(x["gas"]) for x in r["legs"]) + 220_000
                gas_usd = gas_units * gp / 1e18 * eth_usd + 0.12
                flash_fee = size * fb / 10_000
                r["flash_fee_usd"] = flash_fee
                r["gas_plus_l1_reserve_usd"] = gas_usd
                r["estimated_net_usd"] = r["gross_usd"] - flash_fee - gas_usd
                rows.append(r)
                print(json.dumps({"kind": "route", **r}, separators=(",", ":")))
            except Exception as e:
                print(json.dumps({"kind": "error", "size_usdc": size, "path": "->".join(path), "error": str(e)[:220]}, separators=(",", ":")))

    rows.sort(key=lambda x: x["estimated_net_usd"], reverse=True)
    positives = [r for r in rows if r["estimated_net_usd"] > 0]
    print(json.dumps({"kind": "summary", "routes_tested": len(rows), "net_positive": len(positives), "best": rows[0] if rows else None}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
