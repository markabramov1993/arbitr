#!/usr/bin/env python3
"""Targeted live Base DEX round-trip scanner.

The fast spot scanner first showed the current cbBTC/USDC cross-venue edge on
Uniswap V3 -> Aerodrome Slipstream V3. This script then asks the real quoters
for executable amounts. It is read-only: no transaction is signed or sent.
"""
from __future__ import annotations

import json
import subprocess
import time

RPCS = ["https://mainnet.base.org", "https://base-mainnet.g.alchemy.com/public"]
UNI_QUOTER = "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a"
# Aerodrome Slipstream V3 deployment paired with the newest Base CLFactory.
AERO_MIXED_QUOTER_V3 = "0xCd2A7D98e82D6107eac1828ce8DeAA6acB65b555"
# Keep the published legacy MixedQuoter as a fallback for older Slipstream pools.
AERO_MIXED_QUOTER_LEGACY = "0x0A5aA5D3a4d28014f967Bf0f29EAA3FF9807D5c6"
AERO_FACTORY_V3 = "0xf8f2eB4940CFE7d13603DDDD87f123820Fc061Ef"

TOKENS = {
    "USDC": ("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", 6),
    "WETH": ("0x4200000000000000000000000000000000000006", 18),
    "cbBTC": ("0xcbb7C0000ab88B473b1f5aFd9ef808440eed33bF", 8),
    "cbXRP": ("0xcb585250f852C6c6bf90434AB21A00f02833a4af", 6),
}

# The live spot shortlist currently points to these low-fee pools. Keeping the
# candidate set narrow makes the exact-quote pass fast enough to react to edges.
CB_BTC_UNI_FEES = [100]
CB_BTC_AERO_SPACINGS = [1, 50]
SIZES_USDC = [25.0, 50.0, 100.0, 250.0, 500.0, 1000.0, 2500.0, 5000.0]


def call(args):
    err = ""
    for rpc in RPCS:
        try:
            p = subprocess.run(
                ["cast", "call", *args, "--rpc-url", rpc],
                capture_output=True,
                text=True,
                timeout=20,
            )
        except subprocess.TimeoutExpired:
            err = f"timeout via {rpc}"
            continue
        if p.returncode == 0:
            return p.stdout.strip()
        err = (p.stderr or p.stdout).strip()
    raise RuntimeError(err)


def first_int(s):
    return int(s.split()[0], 0)


def discover_aero_spacings():
    try:
        raw = call([AERO_FACTORY_V3, "tickSpacings()(int24[])"])
        values = []
        for token in raw.replace("[", " ").replace("]", " ").replace(",", " ").split():
            try:
                values.append(int(token, 0))
            except ValueError:
                pass
        return sorted(set(values))
    except Exception:
        return []


def uni_quote(token_in, token_out, amount, fees):
    best = None
    for fee in fees:
        try:
            out = first_int(call([
                UNI_QUOTER,
                "quoteExactInputSingle((address,address,uint256,uint24,uint160))(uint256,uint160,uint32,uint256)",
                f"({token_in},{token_out},{amount},{fee},0)",
            ]))
            if out > 0 and (best is None or out > best[0]):
                best = (out, fee, "uniswap-quoter-v2")
        except Exception:
            pass
    return best


def aero_quote(token_in, token_out, amount, spacings):
    best = None
    for quoter_name, quoter in (
        ("aerodrome-mixed-quoter-v3", AERO_MIXED_QUOTER_V3),
        ("aerodrome-mixed-quoter-legacy", AERO_MIXED_QUOTER_LEGACY),
    ):
        for spacing in spacings:
            try:
                out = first_int(call([
                    quoter,
                    "quoteExactInputSingleV3((address,address,uint256,int24,uint160))(uint256,uint160,uint32,uint256)",
                    f"({token_in},{token_out},{amount},{spacing},0)",
                ]))
                if out > 0 and (best is None or out > best[0]):
                    best = (out, spacing, quoter_name)
            except Exception:
                pass
            time.sleep(0.01)
    return best


def route(amount_human, buy_venue, sell_venue):
    start_sym = "USDC"
    mid_sym = "cbBTC"
    start_addr, start_dec = TOKENS[start_sym]
    mid_addr, mid_dec = TOKENS[mid_sym]
    amount = int(amount_human * 10**start_dec)

    if buy_venue == "uni":
        q1 = uni_quote(start_addr, mid_addr, amount, CB_BTC_UNI_FEES)
    else:
        q1 = aero_quote(start_addr, mid_addr, amount, CB_BTC_AERO_SPACINGS)
    if not q1:
        return None
    mid_out, tier1, quoter1 = q1

    if sell_venue == "uni":
        q2 = uni_quote(mid_addr, start_addr, mid_out, CB_BTC_UNI_FEES)
    else:
        q2 = aero_quote(mid_addr, start_addr, mid_out, CB_BTC_AERO_SPACINGS)
    if not q2:
        return None
    final_out, tier2, quoter2 = q2

    pnl_raw = final_out - amount
    return {
        "start": start_sym,
        "mid": mid_sym,
        "amount_in": amount_human,
        "buy_venue": buy_venue,
        "buy_tier": tier1,
        "buy_quoter": quoter1,
        "mid_out": mid_out / 10**mid_dec,
        "sell_venue": sell_venue,
        "sell_tier": tier2,
        "sell_quoter": quoter2,
        "amount_out": final_out / 10**start_dec,
        "gross_pnl": pnl_raw / 10**start_dec,
        "gross_bps": pnl_raw / amount * 10000,
    }


def main():
    print(json.dumps({
        "kind": "meta",
        "aero_factory_v3": AERO_FACTORY_V3,
        "aero_factory_v3_spacings": discover_aero_spacings(),
        "aero_quoter_v3": AERO_MIXED_QUOTER_V3,
        "aero_quoter_legacy": AERO_MIXED_QUOTER_LEGACY,
        "target_pair": "cbBTC/USDC",
        "target_uni_fees": CB_BTC_UNI_FEES,
        "target_aero_spacings": CB_BTC_AERO_SPACINGS,
    }, separators=(",", ":")))

    results = []
    for amount in SIZES_USDC:
        for a, b in (("uni", "aero"), ("aero", "uni")):
            try:
                r = route(amount, a, b)
                if r:
                    results.append(r)
                    print(json.dumps({"kind": "route", **r}, separators=(",", ":")))
                else:
                    print(json.dumps({
                        "kind": "route_unavailable",
                        "amount": amount,
                        "route": f"{a}->{b}",
                    }, separators=(",", ":")))
            except Exception as e:
                print(json.dumps({
                    "kind": "route_error",
                    "amount": amount,
                    "route": f"{a}->{b}",
                    "error": str(e)[:180],
                }, separators=(",", ":")))

    results.sort(key=lambda x: x["gross_pnl"], reverse=True)
    profitable = [x for x in results if x["gross_pnl"] > 0]
    print(json.dumps({
        "kind": "summary",
        "routes_tested": len(results),
        "profitable_before_gas": len(profitable),
        "best": results[0] if results else None,
    }, separators=(",", ":")))
    return 0 if results else 2


if __name__ == "__main__":
    raise SystemExit(main())
