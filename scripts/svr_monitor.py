#!/usr/bin/env python3
"""Read-only Chainlink SVR / Atlas auction monitor.

No private key, no SolverOperation, no bid submission. It only subscribes to the
public solver userOperations JSON-RPC subscription and records raw notifications.
"""
import argparse
import asyncio
import json
import time

import websockets

WS_URL = "wss://svr-bid-endpoint.chain.link/ws/solver"
BASE_CHAIN_ID = 8453
BASE_ATLAS = "0x583dcfef0d240dc80753f0f0b26513fee27d9b77"
BASE_CONTROL = "0xa5e1a36938769cbd5a26f5e19d8fcb379f597c83"


def _to_int(v):
    if isinstance(v, int):
        return v
    if isinstance(v, str):
        try:
            return int(v, 0)
        except ValueError:
            return None
    if isinstance(v, dict):
        for k in ("value", "hex", "chain_id", "chainId"):
            if k in v:
                x = _to_int(v[k])
                if x is not None:
                    return x
    return None


def _first(d, *keys):
    if not isinstance(d, dict):
        return None
    for k in keys:
        if k in d:
            return d[k]
    return None


def summarize(result):
    if not isinstance(result, dict):
        return {"kind": type(result).__name__}
    partial = _first(result, "partial_user_operation", "partialUserOperation") or {}
    chain_raw = _first(partial, "chain_id", "chainId")
    chain_id = _to_int(chain_raw)
    control = str(_first(partial, "control") or "").lower()
    atlas = str(_first(partial, "to") or "").lower()
    hints = _first(partial, "hints")
    auction = _first(result, "auction_id", "auctionId")
    return {
        "auction_id": auction,
        "chain_id": chain_id,
        "control": control,
        "atlas": atlas,
        "is_base": chain_id == BASE_CHAIN_ID,
        "is_base_svr": chain_id == BASE_CHAIN_ID and control == BASE_CONTROL and atlas == BASE_ATLAS,
        "partial_keys": sorted(partial.keys()) if isinstance(partial, dict) else [],
        "has_hints": hints is not None,
        "hints_type": type(hints).__name__ if hints is not None else None,
    }


async def run(seconds: int, out_path: str):
    deadline = time.monotonic() + seconds
    count = base = base_svr = 0
    with open(out_path, "w", encoding="utf-8") as f:
        async with websockets.connect(
            WS_URL,
            open_timeout=15,
            ping_interval=20,
            ping_timeout=20,
            max_size=8 * 1024 * 1024,
        ) as ws:
            req = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "solver_subscribe",
                "params": ["userOperations"],
            }
            await ws.send(json.dumps(req))
            ack = await asyncio.wait_for(ws.recv(), timeout=15)
            ack_obj = json.loads(ack)
            print("SUBSCRIBE_ACK", json.dumps(ack_obj, separators=(",", ":")))
            f.write(json.dumps({"type": "subscribe_ack", "data": ack_obj}) + "\n")
            f.flush()

            while time.monotonic() < deadline:
                timeout = min(15.0, max(0.1, deadline - time.monotonic()))
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
                except asyncio.TimeoutError:
                    continue
                now = time.time()
                try:
                    msg = json.loads(raw)
                except Exception:
                    f.write(json.dumps({"ts": now, "type": "non_json", "raw": str(raw)[:10000]}) + "\n")
                    continue
                params = msg.get("params") if isinstance(msg, dict) else None
                result = params.get("result") if isinstance(params, dict) else None
                if result is None and isinstance(msg, dict):
                    result = msg.get("result")
                s = summarize(result)
                count += 1
                base += int(bool(s.get("is_base")))
                base_svr += int(bool(s.get("is_base_svr")))
                row = {"ts": now, "summary": s, "raw": msg}
                f.write(json.dumps(row, separators=(",", ":")) + "\n")
                f.flush()
                print("AUCTION", json.dumps(s, separators=(",", ":")))

    summary = {"seconds": seconds, "notifications": count, "base": base, "base_svr": base_svr}
    print("MONITOR_SUMMARY", json.dumps(summary, separators=(",", ":")))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=int, default=180)
    ap.add_argument("--out", default="svr-auctions.jsonl")
    args = ap.parse_args()
    asyncio.run(run(args.seconds, args.out))


if __name__ == "__main__":
    main()
