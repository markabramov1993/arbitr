#!/usr/bin/env python3
"""Live read-only Base DEX round-trip scanner.

Compares Uniswap V3 QuoterV2 with the current Aerodrome Slipstream Quoter across
common fee/tick-spacing tiers. It does not sign or submit transactions.
"""
from __future__ import annotations

import json
import subprocess
import time

RPCS = ["https://base-mainnet.g.alchemy.com/public", "https://mainnet.base.org"]
UNI_QUOTER = "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a"
AERO_QUOTER = "0x514c8B5f54112481E28028F1166Bd78501089259"
TOKENS = {
    "USDC": ("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", 6),
    "WETH": ("0x4200000000000000000000000000000000000006", 18),
    "cbBTC": ("0xcbb7C0000ab88B473b1f5aFd9ef808440eed33bF", 8),
    "cbXRP": ("0xcb585250f852C6c6bf90434AB21A00f02833a4af", 6),
}
UNI_FEES = [100, 500, 3000, 10000]
AERO_SPACINGS = [1, 10, 50, 100, 200, 500, 1000]


def call(args):
    err = ""
    for rpc in RPCS:
        p = subprocess.run(["cast", "call", *args, "--rpc-url", rpc], capture_output=True, text=True, timeout=25)
        if p.returncode == 0:
            return p.stdout.strip()
        err = (p.stderr or p.stdout).strip()
    raise RuntimeError(err)


def first_int(s):
    return int(s.split()[0], 0)


def uni_quote(token_in, token_out, amount):
    best = None
    for fee in UNI_FEES:
        try:
            out = first_int(call([
                UNI_QUOTER,
                "quoteExactInputSingle((address,address,uint256,uint24,uint160))(uint256,uint160,uint32,uint256)",
                f"({token_in},{token_out},{amount},{fee},0)",
            ]))
            if out > 0 and (best is None or out > best[0]):
                best = (out, fee)
        except Exception:
            pass
        time.sleep(0.02)
    return best


def aero_quote(token_in, token_out, amount):
    best = None
    for spacing in AERO_SPACINGS:
        try:
            out = first_int(call([
                AERO_QUOTER,
                "quoteExactInputSingle(address,address,int24,uint256,uint160)(uint256)",
                token_in, token_out, str(spacing), str(amount), "0",
            ]))
            if out > 0 and (best is None or out > best[0]):
                best = (out, spacing)
        except Exception:
            pass
        time.sleep(0.02)
    return best


def route(start_sym, mid_sym, amount_human, buy_venue, sell_venue):
    start_addr, start_dec = TOKENS[start_sym]
    mid_addr, mid_dec = TOKENS[mid_sym]
    amount = int(amount_human * 10**start_dec)
    q1 = uni_quote(start_addr, mid_addr, amount) if buy_venue == "uni" else aero_quote(start_addr, mid_addr, amount)
    if not q1:
        return None
    mid_out, tier1 = q1
    q2 = uni_quote(mid_addr, start_addr, mid_out) if sell_venue == "uni" else aero_quote(mid_addr, start_addr, mid_out)
    if not q2:
        return None
    final_out, tier2 = q2
    pnl_raw = final_out - amount
    return {
        "start": start_sym,
        "mid": mid_sym,
        "amount_in": amount_human,
        "buy_venue": buy_venue,
        "buy_tier": tier1,
        "mid_out": mid_out / 10**mid_dec,
        "sell_venue": sell_venue,
        "sell_tier": tier2,
        "amount_out": final_out / 10**start_dec,
        "gross_pnl": pnl_raw / 10**start_dec,
        "gross_bps": pnl_raw / amount * 10000,
    }


def main():
    results = []
    for mid in ("WETH", "cbBTC", "cbXRP"):
        for amount in (100.0, 1000.0, 10000.0, 50000.0):
            for a, b in (("uni", "aero"), ("aero", "uni")):
                try:
                    r = route("USDC", mid, amount, a, b)
                    if r:
                        results.append(r)
                        print(json.dumps({"kind":"route", **r}, separators=(",", ":")))
                except Exception as e:
                    print(json.dumps({"kind":"route_error","mid":mid,"amount":amount,"route":f"{a}->{b}","error":str(e)[:180]}, separators=(",", ":")))
    results.sort(key=lambda x: x["gross_pnl"], reverse=True)
    profitable = [x for x in results if x["gross_pnl"] > 0]
    print(json.dumps({
        "kind":"summary",
        "routes_tested": len(results),
        "profitable_before_gas": len(profitable),
        "best": results[0] if results else None,
    }, separators=(",", ":")))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
