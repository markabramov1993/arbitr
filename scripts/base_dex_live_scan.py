#!/usr/bin/env python3
"""Read-only Base DEX cross-venue spot-edge scanner.

Algorithm:
1. Discover USDC pools on Uniswap V3 and Aerodrome Slipstream V3.
2. Read slot0 prices + onchain pool fee configuration.
3. Rank only cross-venue edges after known swap fees.
4. Hand positive edges to a separate Foundry local-fork executor which performs
   the real two-swap route and measures final USDC.

The scanner itself does no signing, transaction submission, or public-chain
state mutation. Final admission is based on fork execution, not spot math.
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass

RPCS = [
    "https://base-mainnet.g.alchemy.com/public",
    "https://mainnet.base.org",
]

UNI_FACTORY = "0x33128a8fC17869897dcE68Ed026d694621f6FDfD"
# Aerodrome newest CLFactory (Slipstream V3 / Gauge V3 generation).
AERO_FACTORY = "0xf8f2eB4940CFE7d13603DDDD87f123820Fc061Ef"

TOKENS = {
    "USDC": ("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", 6),
    "WETH": ("0x4200000000000000000000000000000000000006", 18),
    "cbBTC": ("0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf", 8),
    "cbXRP": ("0xcb585250f852C6c6bf90434AB21A00f02833a4af", 6),
}
UNI_FEES = (100, 500, 3000, 10000)
FALLBACK_AERO_SPACINGS = (1, 10, 50, 100, 200)


def _run_cast(address: str, sig: str, *args: object) -> str:
    err = ""
    for rpc in RPCS:
        try:
            p = subprocess.run(
                ["cast", "call", address, sig, *map(str, args), "--rpc-url", rpc],
                capture_output=True,
                text=True,
                timeout=12,
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
    _, usdc_dec = TOKENS["USDC"]
    token0 = _first_addr(_run_cast(pool, "token0()(address)")).lower()
    sqrt_price_x96 = _first_int(
        _run_cast(pool, "slot0()(uint160,int24,uint16,uint16,uint16,bool)")
    )
    if sqrt_price_x96 <= 0:
        raise ValueError("zero sqrt price")
    raw_token1_per_token0 = (sqrt_price_x96 * sqrt_price_x96) / (2**192)
    if raw_token1_per_token0 <= 0:
        raise ValueError("invalid raw price")
    if token0 == asset.lower():
        price = raw_token1_per_token0 * (10**asset_dec) / (10**usdc_dec)
    else:
        price = (1.0 / raw_token1_per_token0) * (10**asset_dec) / (10**usdc_dec)
    # Obvious uninitialized/dust-price guard. The real fork executor remains final gate.
    if not (1e-8 < price < 1e9):
        raise ValueError(f"implausible spot price {price}")
    return price


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
            pools.append(VenuePool("uni", fee, pool, _pool_price(pool, asset_sym), fee / 1_000_000))
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
                # Conservative fallback. A route with unknown fee is not promoted cheaply.
                fee_fraction = 0.003
            pools.append(VenuePool("aero", spacing, pool, _pool_price(pool, asset_sym), fee_fraction))
        except Exception:
            continue
    return pools


def main() -> int:
    aero_spacings = _aero_spacings()
    print(json.dumps({"kind": "meta", "aero_spacings": aero_spacings}, separators=(",", ":")))

    edges = []
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

        unis = [v for v in venues if v.venue == "uni"]
        aeros = [v for v in venues if v.venue == "aero"]
        for uni in unis:
            for aero in aeros:
                low, high = (uni, aero) if uni.price_usdc_per_asset < aero.price_usdc_per_asset else (aero, uni)
                spread = high.price_usdc_per_asset / low.price_usdc_per_asset - 1
                fee_sum = low.fee_fraction + high.fee_fraction
                edge_bps = (spread - fee_sum) * 10_000
                row = {
                    "kind": "spot_edge",
                    "asset": asset_sym,
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
                edges.append(row)
                print(json.dumps(row, separators=(",", ":")))

    edges.sort(key=lambda x: x["spot_edge_bps_before_slippage_gas"], reverse=True)
    positive = [x for x in edges if x["spot_edge_bps_before_slippage_gas"] > 0]
    print(json.dumps({
        "kind": "summary",
        "spot_edges": len(edges),
        "positive_spot_edges": len(positive),
        "best_spot": positive[0] if positive else (edges[0] if edges else None),
        "final_gate": "fresh_fork_real_swaps",
    }, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
