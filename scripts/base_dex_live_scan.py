#!/usr/bin/env python3
"""Read-only Base DEX cross-venue scanner.

Staged algorithm:
1. Discover USDC pools on Uniswap V3 and the newest Aerodrome Slipstream CL factory.
2. Compare slot0 spot prices and known pool fees to shortlist cross-venue edges.
3. Exact-quote only the best edges at several sizes.
4. Emit JSONL. A separate local-fork validator executes the best positive route.

No private key, signing, transaction submission, or public-chain state mutation.
"""
from __future__ import annotations

import json
import subprocess
import time
from dataclasses import dataclass

RPCS = [
    "https://base-mainnet.g.alchemy.com/public",
    "https://mainnet.base.org",
]

UNI_FACTORY = "0x33128a8fC17869897dcE68Ed026d694621f6FDfD"
UNI_QUOTER = "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a"
AERO_FACTORY = "0xf8f2eB4940CFE7d13603DDDD87f123820Fc061Ef"
AERO_QUOTER = "0x514c8B5f54112481E28028F1166Bd78501089259"

TOKENS = {
    "USDC": ("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", 6),
    "WETH": ("0x4200000000000000000000000000000000000006", 18),
    "cbBTC": ("0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf", 8),
    "cbXRP": ("0xcb585250f852C6c6bf90434AB21A00f02833a4af", 6),
}
UNI_FEES = (100, 500, 3000, 10000)
FALLBACK_AERO_SPACINGS = (1, 10, 50, 100, 200)
SIZES_USDC = (100.0, 500.0, 1_000.0, 2_500.0, 5_000.0, 10_000.0, 25_000.0)


def _run_cast(address: str, sig: str, *args: object) -> str:
    err = ""
    for rpc in RPCS:
        try:
            p = subprocess.run(
                ["cast", "call", address, sig, *map(str, args), "--rpc-url", rpc],
                capture_output=True,
                text=True,
                timeout=15,
            )
        except Exception as exc:
            err = str(exc)
            continue
        if p.returncode == 0:
            return p.stdout.strip()
        err = (p.stderr or p.stdout).strip()
    raise RuntimeError(err or "cast call failed")


def _first_int(text: str) -> int:
    return int(text.split()[0], 0)


def _first_addr(text: str) -> str:
    return text.split()[0]


def _aero_spacings() -> list[int]:
    try:
        raw = _run_cast(AERO_FACTORY, "tickSpacings()(int24[])")
        cleaned = raw.replace("[", " ").replace("]", " ").replace(",", " ")
        vals = []
        for token in cleaned.split():
            try:
                vals.append(int(token, 0))
            except ValueError:
                pass
        vals = sorted(set(v for v in vals if v > 0))
        if vals:
            return vals
    except Exception:
        pass
    return list(FALLBACK_AERO_SPACINGS)


@dataclass(frozen=True)
class VenuePool:
    venue: str
    tier: int
    pool: str
    price_usdc_per_asset: float
    fee_fraction: float


def _pool_price(pool: str, asset_sym: str) -> float:
    asset, asset_dec = TOKENS[asset_sym]
    usdc, usdc_dec = TOKENS["USDC"]
    token0 = _first_addr(_run_cast(pool, "token0()(address)")).lower()
    sqrt_price_x96 = _first_int(
        _run_cast(pool, "slot0()(uint160,int24,uint16,uint16,uint16,bool)")
    )
    if sqrt_price_x96 <= 0:
        raise ValueError("zero sqrt price")
    raw_token1_per_token0 = (sqrt_price_x96 * sqrt_price_x96) / (2**192)
    if token0 == asset.lower():
        return raw_token1_per_token0 * (10**asset_dec) / (10**usdc_dec)
    return (1.0 / raw_token1_per_token0) * (10**asset_dec) / (10**usdc_dec)


def _discover(asset_sym: str, aero_spacings: list[int]) -> list[VenuePool]:
    asset, _ = TOKENS[asset_sym]
    usdc, _ = TOKENS["USDC"]
    pools: list[VenuePool] = []

    for fee in UNI_FEES:
        try:
            pool = _first_addr(
                _run_cast(UNI_FACTORY, "getPool(address,address,uint24)(address)", asset, usdc, fee)
            )
            if int(pool, 16) == 0:
                continue
            pools.append(
                VenuePool("uni", fee, pool, _pool_price(pool, asset_sym), fee / 1_000_000)
            )
        except Exception:
            continue

    for spacing in aero_spacings:
        try:
            pool = _first_addr(
                _run_cast(AERO_FACTORY, "getPool(address,address,int24)(address)", asset, usdc, spacing)
            )
            if int(pool, 16) == 0:
                continue
            try:
                fee_raw = _first_int(_run_cast(AERO_FACTORY, "getSwapFee(address)(uint24)", pool))
                fee_fraction = fee_raw / 1_000_000
            except Exception:
                # Conservative fallback rather than pretending an unknown fee is zero.
                fee_fraction = 0.003
            pools.append(
                VenuePool("aero", spacing, pool, _pool_price(pool, asset_sym), fee_fraction)
            )
        except Exception:
            continue

    return pools


def _quote(venue: str, tier: int, token_in: str, token_out: str, amount: int) -> int:
    if venue == "uni":
        return _first_int(
            _run_cast(
                UNI_QUOTER,
                "quoteExactInputSingle((address,address,uint256,uint24,uint160))(uint256,uint160,uint32,uint256)",
                f"({token_in},{token_out},{amount},{tier},0)",
            )
        )
    if venue == "aero":
        return _first_int(
            _run_cast(
                AERO_QUOTER,
                "quoteExactInputSingle(address,address,int24,uint256,uint160)(uint256)",
                token_in,
                token_out,
                tier,
                amount,
                0,
            )
        )
    raise ValueError(f"unknown venue {venue}")


def _exact_route(asset_sym: str, low: VenuePool, high: VenuePool, amount_usdc: float):
    usdc, usdc_dec = TOKENS["USDC"]
    asset, asset_dec = TOKENS[asset_sym]
    amount_in = int(round(amount_usdc * (10**usdc_dec)))
    try:
        mid_out = _quote(low.venue, low.tier, usdc, asset, amount_in)
        if mid_out <= 0:
            return None
        final_out = _quote(high.venue, high.tier, asset, usdc, mid_out)
        if final_out <= 0:
            return None
    except Exception as exc:
        return {"kind": "quote_error", "pair": f"{asset_sym}/USDC", "amount_in": amount_usdc, "error": str(exc)[:180]}

    gross_raw = final_out - amount_in
    return {
        "kind": "exact_route",
        "pair": f"{asset_sym}/USDC",
        "asset": asset_sym,
        "amount_in_usdc": amount_usdc,
        "amount_in_raw": amount_in,
        "buy_venue": low.venue,
        "buy_tier": low.tier,
        "buy_pool": low.pool,
        "asset_out": mid_out / (10**asset_dec),
        "asset_out_raw": mid_out,
        "sell_venue": high.venue,
        "sell_tier": high.tier,
        "sell_pool": high.pool,
        "final_usdc": final_out / (10**usdc_dec),
        "final_raw": final_out,
        "gross_usdc": gross_raw / (10**usdc_dec),
        "gross_bps": (gross_raw / amount_in) * 10_000,
    }


def main() -> int:
    aero_spacings = _aero_spacings()
    print(json.dumps({"kind": "meta", "aero_spacings": aero_spacings}, separators=(",", ":")))

    exact_results = []
    spot_edges = []
    for asset_sym in ("WETH", "cbBTC", "cbXRP"):
        venues = _discover(asset_sym, aero_spacings)
        for v in venues:
            print(json.dumps({
                "kind": "pool",
                "pair": f"{asset_sym}/USDC",
                "venue": v.venue,
                "tier": v.tier,
                "pool": v.pool,
                "price_usdc_per_asset": v.price_usdc_per_asset,
                "fee_bps": v.fee_fraction * 10_000,
            }, separators=(",", ":")))

        for uni in [v for v in venues if v.venue == "uni"]:
            for aero in [v for v in venues if v.venue == "aero"]:
                low, high = (uni, aero) if uni.price_usdc_per_asset < aero.price_usdc_per_asset else (aero, uni)
                spread = high.price_usdc_per_asset / low.price_usdc_per_asset - 1
                fee_sum = low.fee_fraction + high.fee_fraction
                edge_bps = (spread - fee_sum) * 10_000
                spot = {
                    "kind": "spot_edge",
                    "pair": f"{asset_sym}/USDC",
                    "buy_venue": low.venue,
                    "buy_tier": low.tier,
                    "buy_pool": low.pool,
                    "sell_venue": high.venue,
                    "sell_tier": high.tier,
                    "sell_pool": high.pool,
                    "spread_bps": spread * 10_000,
                    "fees_bps": fee_sum * 10_000,
                    "spot_edge_bps_before_slippage_gas": edge_bps,
                }
                spot_edges.append((edge_bps, asset_sym, low, high, spot))
                print(json.dumps(spot, separators=(",", ":")))

    # Only exact-quote the strongest cross-venue edges. Negative spot edges can still
    # hide tiny quote differences, so keep a modest -10 bps admission window.
    spot_edges.sort(key=lambda x: x[0], reverse=True)
    selected = spot_edges[:8]
    for edge_bps, asset_sym, low, high, _ in selected:
        if edge_bps < -10:
            continue
        for size in SIZES_USDC:
            result = _exact_route(asset_sym, low, high, size)
            if result:
                print(json.dumps(result, separators=(",", ":")))
                if result.get("kind") == "exact_route":
                    exact_results.append(result)
            time.sleep(0.015)

    exact_results.sort(key=lambda x: x["gross_usdc"], reverse=True)
    profitable = [x for x in exact_results if x["gross_usdc"] > 0]
    best = profitable[0] if profitable else (exact_results[0] if exact_results else None)
    summary = {
        "kind": "summary",
        "spot_edges": len(spot_edges),
        "exact_routes": len(exact_results),
        "profitable_before_gas": len(profitable),
        "best": best,
    }
    print(json.dumps(summary, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
