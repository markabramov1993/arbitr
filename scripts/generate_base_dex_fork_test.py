#!/usr/bin/env python3
"""Generate a Foundry test for the best positive Base DEX quote.

Input: JSONL emitted by base_dex_live_scan.py.
Output: a Solidity test that executes the exact two swaps on a fresh Base fork.
This is local-fork validation only; it never signs or broadcasts a transaction.
"""
from __future__ import annotations

import json
import pathlib
import sys

UNI_ROUTER = "0x2626664c2603336E57B271c5C0b26F421741e481"
# Router observed executing current Aerodrome concentrated-liquidity swaps on Base.
AERO_ROUTER = "0x698Cb2b6dd822994581fEa6eA4Fc755d1363A92F"
USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
TOKENS = {
    "WETH": "0x4200000000000000000000000000000000000006",
    "cbBTC": "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
    "cbXRP": "0xcb585250f852C6c6bf90434AB21A00f02833a4af",
}


def load_best(path: pathlib.Path):
    candidates = []
    for line in path.read_text().splitlines():
        try:
            row = json.loads(line)
        except Exception:
            continue
        if row.get("kind") == "exact_route" and float(row.get("gross_usdc", 0)) > 0:
            candidates.append(row)
    candidates.sort(key=lambda r: float(r.get("gross_usdc", 0)), reverse=True)
    return candidates[0] if candidates else None


def swap_code(venue: str, tier: int, token_in: str, token_out: str, amount_expr: str, out_var: str) -> str:
    if venue == "uni":
        return f'''
        IERC20Dex({token_in}).approve(UNI_ROUTER, {amount_expr});
        uint256 {out_var} = IUniRouterDex(UNI_ROUTER).exactInputSingle(
            IUniRouterDex.ExactInputSingleParams({{
                tokenIn: {token_in}, tokenOut: {token_out}, fee: {tier},
                recipient: address(this), amountIn: {amount_expr}, amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            }})
        );'''
    if venue == "aero":
        return f'''
        IERC20Dex({token_in}).approve(AERO_ROUTER, {amount_expr});
        uint256 {out_var} = IAeroRouterDex(AERO_ROUTER).exactInputSingle(
            IAeroRouterDex.ExactInputSingleParams({{
                tokenIn: {token_in}, tokenOut: {token_out}, tickSpacing: {tier},
                recipient: address(this), deadline: block.timestamp,
                amountIn: {amount_expr}, amountOutMinimum: 0, sqrtPriceLimitX96: 0
            }})
        );'''
    raise ValueError(f"unsupported venue: {venue}")


def render(best) -> str:
    if not best:
        return '''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import "forge-std/Test.sol";
contract GeneratedBaseDexArbTest is Test {
    function testNoPositiveQuote() external { emit log_string("NO_POSITIVE_QUOTE"); }
}
'''

    asset_sym = best["asset"]
    asset = TOKENS[asset_sym]
    amount_in = int(best["amount_in_raw"])
    buy_venue = best["buy_venue"]
    sell_venue = best["sell_venue"]
    buy_tier = int(best["buy_tier"])
    sell_tier = int(best["sell_tier"])
    qgross_raw = int(best["final_raw"]) - amount_in

    first = swap_code(buy_venue, buy_tier, "USDC", "ASSET", "amountIn", "assetOut")
    second = swap_code(sell_venue, sell_tier, "ASSET", "USDC", "assetOut", "finalUsdc")

    return f'''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import "forge-std/Test.sol";

interface IERC20Dex {{ function approve(address,uint256) external returns(bool); function balanceOf(address) external view returns(uint256); }}
interface IUniRouterDex {{
    struct ExactInputSingleParams {{ address tokenIn; address tokenOut; uint24 fee; address recipient; uint256 amountIn; uint256 amountOutMinimum; uint160 sqrtPriceLimitX96; }}
    function exactInputSingle(ExactInputSingleParams calldata params) external payable returns(uint256 amountOut);
}}
interface IAeroRouterDex {{
    struct ExactInputSingleParams {{ address tokenIn; address tokenOut; int24 tickSpacing; address recipient; uint256 deadline; uint256 amountIn; uint256 amountOutMinimum; uint160 sqrtPriceLimitX96; }}
    function exactInputSingle(ExactInputSingleParams calldata params) external payable returns(uint256 amountOut);
}}

contract GeneratedBaseDexArbTest is Test {{
    address constant USDC = {USDC};
    address constant ASSET = {asset};
    address constant UNI_ROUTER = {UNI_ROUTER};
    address constant AERO_ROUTER = {AERO_ROUTER};

    function testBestPositiveQuoteOnLatestFork() external {{
        vm.createSelectFork("https://base-mainnet.g.alchemy.com/public");
        uint256 amountIn = {amount_in};
        deal(USDC, address(this), amountIn);
        uint256 start = IERC20Dex(USDC).balanceOf(address(this));
        {first}
        {second}
        uint256 finish = IERC20Dex(USDC).balanceOf(address(this));
        emit log_named_string("ASSET", "{asset_sym}");
        emit log_named_string("BUY_VENUE", "{buy_venue}");
        emit log_named_uint("BUY_TIER", {buy_tier});
        emit log_named_string("SELL_VENUE", "{sell_venue}");
        emit log_named_uint("SELL_TIER", {sell_tier});
        emit log_named_uint("START_USDC_RAW", start);
        emit log_named_uint("ASSET_OUT_RAW", assetOut);
        emit log_named_uint("FINAL_USDC_RAW", finalUsdc);
        emit log_named_int("FORK_GROSS_PNL_USDC_RAW", int256(finish) - int256(start));
        emit log_named_int("QUOTE_GROSS_PNL_USDC_RAW", {qgross_raw});
        require(finish > start, "quote did not survive fork execution");
    }}
}}
'''


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: generate_base_dex_fork_test.py <scan.jsonl> <output.sol>", file=sys.stderr)
        return 2
    inp = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2])
    best = load_best(inp)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(best))
    pathlib.Path("dex-candidate.json").write_text(json.dumps(best, indent=2) if best else "null\n")
    print("GENERATOR_HAS_CANDIDATE=" + ("true" if best else "false"))
    if best:
        print("GENERATOR_BEST=" + json.dumps(best, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
