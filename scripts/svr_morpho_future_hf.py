#!/usr/bin/env python3
"""Read-only Morpho future-HF estimator driven by a pending SVR price move.

This is a prefilter, not an execution engine. It uses Morpho's public GraphQL
API and treats highly correlated wrappers as one price family so a common
ETH/USD or BTC/USD move is not incorrectly applied to only one side of a
same-family market.
"""
from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass
from typing import Iterable

MORPHO_GRAPHQL = "https://api.morpho.org/graphql"
BASE_CHAIN_ID = 8453

# Deliberately conservative families. A wrapper can have basis risk versus its
# underlying; this module only removes the common USD beta. Exact eligibility
# still belongs to a stateful fork using the market oracle.
FAMILIES: dict[str, set[str]] = {
    "ETH": {"ETH", "WETH", "WSTETH", "STETH", "WEETH", "EETH", "CBETH", "RETH", "EZETH", "RSETH", "OSETH"},
    "BTC": {"BTC", "WBTC", "CBBTC", "LBTC", "TBTC", "EBTC"},
    "SOL": {"SOL", "JITOSOL", "MSOL", "BSOL"},
    "LTC": {"LTC", "CBLTC"},
    "ZEC": {"ZEC", "CBZEC"},
    "USD": {"USD", "USDC", "USDT", "DAI", "USDS", "USDE", "SUSDE", "CRVUSD", "FRAX", "LUSD", "YOUSD"},
}


def asset_family(symbol: str | None) -> str:
    s = (symbol or "").upper().replace(".", "").replace("-", "")
    for family, members in FAMILIES.items():
        if s in members:
            return family
    return s


def _gql(query: str) -> dict:
    req = urllib.request.Request(
        MORPHO_GRAPHQL,
        data=json.dumps({"query": query}).encode(),
        headers={"content-type": "application/json", "user-agent": "profit-engine-svr-morpho"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.loads(r.read())
    if out.get("errors"):
        raise RuntimeError(out["errors"])
    return out["data"]


@dataclass(frozen=True)
class FutureHF:
    market_id: str
    user: str
    loan_symbol: str
    collateral_symbol: str
    current_hf: float
    future_hf: float
    debt_usd: float
    collateral_usd: float
    lltv: float
    feed_family: str
    move_ratio: float

    @property
    def crosses_liquidation(self) -> bool:
        return self.current_hf > 1.0 and self.future_hf <= 1.0

    def as_dict(self) -> dict:
        return {
            "market": self.market_id,
            "user": self.user,
            "loan": self.loan_symbol,
            "collateral": self.collateral_symbol,
            "current_hf": self.current_hf,
            "future_hf": self.future_hf,
            "debt_usd": self.debt_usd,
            "collateral_usd": self.collateral_usd,
            "lltv": self.lltv,
            "feed_family": self.feed_family,
            "move_ratio": self.move_ratio,
            "crosses_liquidation": self.crosses_liquidation,
        }


def _market_list(limit: int = 100) -> list[dict]:
    q = f'''query {{ markets(first: {int(limit)}, orderBy: SupplyAssetsUsd, orderDirection: Desc, where: {{ chainId_in: [{BASE_CHAIN_ID}], listed: true }}) {{ items {{ marketId lltv loanAsset {{ address symbol decimals }} collateralAsset {{ address symbol decimals }} oracle {{ address }} irmAddress state {{ borrowAssetsUsd }} }} }} }}'''
    return _gql(q)["markets"]["items"]


def _positions(market_id: str, limit: int = 80) -> list[dict]:
    q = f'''query {{ marketPositions(first: {int(limit)}, orderBy: BorrowShares, orderDirection: Desc, where: {{ marketUniqueKey_in: ["{market_id}"] }}) {{ items {{ user {{ address }} state {{ borrowAssetsUsd collateralUsd borrowShares collateral }} }} }} }}'''
    return _gql(q)["marketPositions"]["items"]


def scan(feed_family: str, move_ratio: float, *, market_limit: int = 100, positions_per_market: int = 80, future_hf_max: float = 1.01) -> list[FutureHF]:
    """Estimate post-SVR health factors for markets exposed to one price family.

    `move_ratio` is pending_price/current_price. The common beta is applied to
    both sides when both are in the same family, which makes it cancel rather
    than manufacturing a fake liquidation signal.
    """
    ff = feed_family.upper()
    rows: list[FutureHF] = []

    for m in _market_list(market_limit):
        loan_symbol = (m.get("loanAsset") or {}).get("symbol") or ""
        coll_symbol = (m.get("collateralAsset") or {}).get("symbol") or ""
        loan_family = asset_family(loan_symbol)
        coll_family = asset_family(coll_symbol)

        affects_loan = loan_family == ff
        affects_coll = coll_family == ff
        if not affects_loan and not affects_coll:
            continue

        lltv = int(m["lltv"]) / 1e18
        for p in _positions(m["marketId"], positions_per_market):
            state = p.get("state") or {}
            debt = float(state.get("borrowAssetsUsd") or 0)
            coll = float(state.get("collateralUsd") or 0)
            if debt <= 0 or coll <= 0:
                continue

            current_hf = coll * lltv / debt
            future_coll = coll * (move_ratio if affects_coll else 1.0)
            future_debt = debt * (move_ratio if affects_loan else 1.0)
            future_hf = future_coll * lltv / future_debt

            if future_hf <= future_hf_max:
                rows.append(FutureHF(
                    market_id=m["marketId"],
                    user=(p.get("user") or {}).get("address") or "",
                    loan_symbol=loan_symbol,
                    collateral_symbol=coll_symbol,
                    current_hf=current_hf,
                    future_hf=future_hf,
                    debt_usd=debt,
                    collateral_usd=coll,
                    lltv=lltv,
                    feed_family=ff,
                    move_ratio=move_ratio,
                ))

    rows.sort(key=lambda x: (x.future_hf, -x.debt_usd))
    return rows


def family_from_feed_name(feed_name: str | None) -> str:
    left = (feed_name or "").split("/")[0].strip().upper()
    return asset_family(left)


def analyze_signal(feed_name: str, current_price: float, pending_price: float) -> list[dict]:
    if current_price <= 0 or pending_price <= 0:
        return []
    family = family_from_feed_name(feed_name)
    if not family:
        return []
    ratio = pending_price / current_price
    return [x.as_dict() for x in scan(family, ratio)]


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--feed", required=True, help="e.g. ETH / USD")
    ap.add_argument("--current", type=float, required=True)
    ap.add_argument("--pending", type=float, required=True)
    args = ap.parse_args()
    print(json.dumps(analyze_signal(args.feed, args.current, args.pending), indent=2))
