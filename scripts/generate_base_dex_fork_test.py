#!/usr/bin/env python3
"""Generate a real-swap Foundry search from positive Base DEX spot edges.

The generated test:
- creates a fresh latest Base fork for every route/size attempt;
- funds only the local fork test contract with USDC via Foundry deal();
- executes the actual Uniswap V3 / Aerodrome Slipstream V3 router calls;
- measures final USDC and emits only fork-surviving positive routes.

No mainnet key, signature or transaction broadcast is involved.
"""
from __future__ import annotations

import json
import pathlib
import sys

UNI_ROUTER = "0x2626664c2603336E57B271c5C0b26F421741e481"
AERO_ROUTER = "0x698Cb2b6dd822994581fEa6eA4Fc755d1363A92F"
USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
TOKENS = {
    "WETH": "0x4200000000000000000000000000000000000006",
    "cbBTC": "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
    "cbXRP": "0xcb585250f852C6c6bf90434AB21A00f02833a4af",
}
SIZES = (100, 500, 1_000, 2_500, 5_000, 10_000)
MAX_EDGES = 4


def load_edges(path: pathlib.Path):
    rows = []
    for line in path.read_text().splitlines():
        try:
            row = json.loads(line)
        except Exception:
            continue
        if row.get("kind") != "spot_edge":
            continue
        asset = row.get("asset") or str(row.get("pair", "")).split("/")[0]
        if asset not in TOKENS:
            continue
        edge = float(row.get("spot_edge_bps_before_slippage_gas", -1e99))
        if edge <= 0:
            continue
        if row.get("buy_venue") == row.get("sell_venue"):
            continue
        row = dict(row)
        row["asset"] = asset
        rows.append(row)
    rows.sort(key=lambda r: float(r["spot_edge_bps_before_slippage_gas"]), reverse=True)

    # Deduplicate exact venue/tier direction.
    out = []
    seen = set()
    for r in rows:
        key = (r["asset"], r["buy_venue"], int(r["buy_tier"]), r["sell_venue"], int(r["sell_tier"]))
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
        if len(out) >= MAX_EDGES:
            break
    return out


def addr(x: str) -> str:
    return f"address(uint160({int(x, 16)}))"


def render(edges) -> str:
    candidate_lines = []
    for i, r in enumerate(edges):
        candidate_lines.append(
            "cs[{i}] = Candidate({asset},{buy_uni},{buy_tier},{sell_uni},{sell_tier},{spot});".format(
                i=i,
                asset=addr(TOKENS[r["asset"]]),
                buy_uni="true" if r["buy_venue"] == "uni" else "false",
                buy_tier=int(r["buy_tier"]),
                sell_uni="true" if r["sell_venue"] == "uni" else "false",
                sell_tier=int(r["sell_tier"]),
                spot=max(0, int(round(float(r["spot_edge_bps_before_slippage_gas"]) * 1_000_000))),
            )
        )
    size_values = ",".join(str(x * 1_000_000) for x in SIZES)

    return f'''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import "forge-std/Test.sol";

interface IERC20Dex {{
    function approve(address,uint256) external returns(bool);
    function balanceOf(address) external view returns(uint256);
}}
interface IUniRouterDex {{
    struct ExactInputSingleParams {{
        address tokenIn; address tokenOut; uint24 fee; address recipient;
        uint256 amountIn; uint256 amountOutMinimum; uint160 sqrtPriceLimitX96;
    }}
    function exactInputSingle(ExactInputSingleParams calldata params) external payable returns(uint256 amountOut);
}}
interface IAeroRouterDex {{
    struct ExactInputSingleParams {{
        address tokenIn; address tokenOut; int24 tickSpacing; address recipient;
        uint256 deadline; uint256 amountIn; uint256 amountOutMinimum; uint160 sqrtPriceLimitX96;
    }}
    function exactInputSingle(ExactInputSingleParams calldata params) external payable returns(uint256 amountOut);
}}

contract GeneratedBaseDexArbTest is Test {{
    address constant USDC = {USDC};
    address constant UNI_ROUTER = {UNI_ROUTER};
    address constant AERO_ROUTER = {AERO_ROUTER};
    string constant RPC = "https://base-mainnet.g.alchemy.com/public";

    struct Candidate {{
        address asset;
        bool buyUni;
        int24 buyTier;
        bool sellUni;
        int24 sellTier;
        uint256 spotEdgeBpsE6;
    }}

    function candidates() internal pure returns (Candidate[] memory cs) {{
        cs = new Candidate[]({len(edges)});
        {' '.join(candidate_lines)}
    }}

    function sizes() internal pure returns (uint256[] memory xs) {{
        uint256[{len(SIZES)}] memory fixedSizes = [{size_values}];
        xs = new uint256[]({len(SIZES)});
        for (uint256 i; i < fixedSizes.length; i++) xs[i] = fixedSizes[i];
    }}

    function testSearchPositiveSpotEdgesOnFreshFork() external {{
        Candidate[] memory cs = candidates();
        uint256[] memory xs = sizes();
        uint256 positives;
        emit log_named_uint("EDGE_COUNT", cs.length);
        emit log_named_uint("SIZE_COUNT", xs.length);
        for (uint256 i; i < cs.length; i++) {{
            for (uint256 j; j < xs.length; j++) {{
                if (_attempt(cs[i], i, xs[j])) positives++;
            }}
        }}
        emit log_named_uint("FORK_PROFITABLE_COUNT", positives);
    }}

    function _attempt(Candidate memory c, uint256 idx, uint256 amountIn) internal returns (bool) {{
        vm.createSelectFork(RPC);
        deal(USDC, address(this), amountIn);
        uint256 start = IERC20Dex(USDC).balanceOf(address(this));

        (bool ok1, uint256 assetOut) = _swap(c.buyUni, c.buyTier, USDC, c.asset, amountIn);
        if (!ok1 || assetOut == 0) return false;
        (bool ok2, uint256 finalUsdc) = _swap(c.sellUni, c.sellTier, c.asset, USDC, assetOut);
        if (!ok2) return false;

        int256 pnl = int256(finalUsdc) - int256(start);
        if (pnl > 0) {{
            emit log_named_uint("POSITIVE_ROUTE", 1);
            emit log_named_uint("ROUTE_INDEX", idx);
            emit log_named_address("ASSET", c.asset);
            emit log_named_uint("AMOUNT_IN_USDC_RAW", amountIn);
            emit log_named_uint("BUY_IS_UNI", c.buyUni ? 1 : 0);
            emit log_named_int("BUY_TIER", int256(c.buyTier));
            emit log_named_uint("SELL_IS_UNI", c.sellUni ? 1 : 0);
            emit log_named_int("SELL_TIER", int256(c.sellTier));
            emit log_named_uint("ASSET_OUT_RAW", assetOut);
            emit log_named_uint("FINAL_USDC_RAW", finalUsdc);
            emit log_named_int("FORK_GROSS_PNL_USDC_RAW", pnl);
            emit log_named_uint("SPOT_EDGE_BPS_E6", c.spotEdgeBpsE6);
            return true;
        }}
        return false;
    }}

    function _swap(bool isUni, int24 tier, address tokenIn, address tokenOut, uint256 amountIn)
        internal returns (bool ok, uint256 amountOut)
    {{
        if (isUni) {{
            IERC20Dex(tokenIn).approve(UNI_ROUTER, amountIn);
            try IUniRouterDex(UNI_ROUTER).exactInputSingle(
                IUniRouterDex.ExactInputSingleParams({{
                    tokenIn: tokenIn, tokenOut: tokenOut, fee: uint24(uint256(int256(tier))),
                    recipient: address(this), amountIn: amountIn, amountOutMinimum: 0,
                    sqrtPriceLimitX96: 0
                }})
            ) returns (uint256 out) {{ return (true, out); }} catch {{ return (false, 0); }}
        }}

        IERC20Dex(tokenIn).approve(AERO_ROUTER, amountIn);
        try IAeroRouterDex(AERO_ROUTER).exactInputSingle(
            IAeroRouterDex.ExactInputSingleParams({{
                tokenIn: tokenIn, tokenOut: tokenOut, tickSpacing: tier,
                recipient: address(this), deadline: block.timestamp,
                amountIn: amountIn, amountOutMinimum: 0, sqrtPriceLimitX96: 0
            }})
        ) returns (uint256 out) {{ return (true, out); }} catch {{ return (false, 0); }}
    }}
}}
'''


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: generate_base_dex_fork_test.py <scan.jsonl> <output.sol>", file=sys.stderr)
        return 2
    inp = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2])
    edges = load_edges(inp)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(edges))
    pathlib.Path("dex-candidate.json").write_text(json.dumps(edges, indent=2) + "\n")
    print(f"GENERATOR_EDGE_COUNT={len(edges)}")
    for edge in edges:
        print("GENERATOR_EDGE=" + json.dumps(edge, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
