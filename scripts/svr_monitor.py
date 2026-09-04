#!/usr/bin/env python3
"""Read-only Chainlink SVR / Atlas auction monitor.

No private key, SolverOperation, or bid submission. For Base SVR notifications
it compares the hinted pending median price with the still-active on-chain
aggregator answer, turning the stream into a measurable pre-oracle signal.
"""
import argparse
import asyncio
import json
import time
import urllib.request

import websockets

WS_URL = "wss://svr-bid-endpoint.chain.link/ws/solver"
BASE_RPC = "https://base-mainnet.g.alchemy.com/public"
BASE_CHAIN_ID = 8453
BASE_ATLAS = "0x583dcfef0d240dc80753f0f0b26513fee27d9b77"
BASE_CONTROL = "0xa5e1a36938769cbd5a26f5e19d8fcb379f597c83"
LATEST_ANSWER_SELECTOR = "0x50d25bcd"
DECIMALS_SELECTOR = "0x313ce567"

# Metadata read directly on-chain from the first live observed Base SVR feed set.
FEED_META = {
    "0xb00e68fb3754ee8cc7b5f61348a2f09d53fb2e0e": ("ZEC / USD", 18),
    "0xeb3ad4395924b76eb64b3d6ababa0b62875b1a1f": ("BTC / USD", 18),
    "0x43151d66d653ad888bf909f006a01792d5f33243": ("SOL / USD", 8),
    "0xe5ec87a39445b8d5b751b116802a53c5ae7e9df1": ("BTC / USD", 8),
    "0x05c84a58fe042275b37db038baacd15f410c7bb0": ("ETH / USD", 8),
    "0xd175aa4ed3aeccd03266c2bbbb16b0b419d005aa": ("LTC / USD", 8),
}


def _to_int(v):
    if isinstance(v, int): return v
    if isinstance(v, str):
        try: return int(v, 0)
        except ValueError: return None
    if isinstance(v, dict):
        for k in ("value", "hex", "chain_id", "chainId"):
            if k in v:
                x = _to_int(v[k])
                if x is not None: return x
    return None


def _first(d, *keys):
    if not isinstance(d, dict): return None
    for k in keys:
        if k in d: return d[k]
    return None


def _rpc_call(to, data):
    payload={"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":to,"data":data},"latest"]}
    req=urllib.request.Request(BASE_RPC,data=json.dumps(payload).encode(),headers={"content-type":"application/json","user-agent":"profit-engine-svr-monitor"})
    with urllib.request.urlopen(req,timeout=10) as r:
        out=json.loads(r.read())
    if out.get("error"): raise RuntimeError(out["error"])
    return out.get("result") or "0x"


def _decode_int256(hex_value):
    x=int(hex_value,16)
    if x >= 1 << 255: x -= 1 << 256
    return x


def _read_feed_state(aggregator):
    a=aggregator.lower()
    name,decimals=FEED_META.get(a,(a,None))
    if decimals is None:
        decimals=int(_rpc_call(aggregator,DECIMALS_SELECTOR),16)
    current=_decode_int256(_rpc_call(aggregator,LATEST_ANSWER_SELECTOR))
    return name,decimals,current


def summarize(result):
    if not isinstance(result, dict): return {"kind": type(result).__name__}
    partial = _first(result, "partial_user_operation", "partialUserOperation") or {}
    chain_id = _to_int(_first(partial, "chain_id", "chainId"))
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


async def enrich_base_svr(result, summary):
    if not summary.get("is_base_svr") or not isinstance(result,dict): return summary
    partial=_first(result,"partial_user_operation","partialUserOperation") or {}
    hints=_first(partial,"hints") or {}
    aggregator=str(hints.get("aggregator") or "")
    median_hex=hints.get("medianPrice")
    if not aggregator or not median_hex: return summary
    try:
        pending=int(median_hex,16)
        name,decimals,current=await asyncio.to_thread(_read_feed_state,aggregator)
        scale=10**decimals
        summary.update({
            "feed":name,
            "aggregator":aggregator.lower(),
            "feed_decimals":decimals,
            "current_answer_raw":current,
            "pending_median_raw":pending,
            "current_price":current/scale,
            "pending_price":pending/scale,
            "pending_move_bps":((pending-current)*10000/current) if current else None,
            "forward_data_bytes":max(0,(len(str(hints.get('forwardData') or ''))-2)//2),
            "raw_report_bytes":max(0,(len(str(hints.get('rawReport') or ''))-2)//2),
        })
    except Exception as exc:
        summary["enrichment_error"]=str(exc)[:180]
    return summary


async def run(seconds: int, out_path: str):
    deadline=time.monotonic()+seconds
    count=base=base_svr=0
    with open(out_path,"w",encoding="utf-8") as f:
        async with websockets.connect(WS_URL,open_timeout=15,ping_interval=20,ping_timeout=20,max_size=8*1024*1024) as ws:
            req={"jsonrpc":"2.0","id":1,"method":"solver_subscribe","params":["userOperations"]}
            await ws.send(json.dumps(req))
            ack_obj=json.loads(await asyncio.wait_for(ws.recv(),timeout=15))
            print("SUBSCRIBE_ACK",json.dumps(ack_obj,separators=(",",":")))
            f.write(json.dumps({"type":"subscribe_ack","data":ack_obj})+"\n"); f.flush()
            while time.monotonic()<deadline:
                timeout=min(15.0,max(0.1,deadline-time.monotonic()))
                try: raw=await asyncio.wait_for(ws.recv(),timeout=timeout)
                except asyncio.TimeoutError: continue
                now=time.time()
                try: msg=json.loads(raw)
                except Exception:
                    f.write(json.dumps({"ts":now,"type":"non_json","raw":str(raw)[:10000]})+"\n"); continue
                params=msg.get("params") if isinstance(msg,dict) else None
                result=params.get("result") if isinstance(params,dict) else None
                if result is None and isinstance(msg,dict): result=msg.get("result")
                s=summarize(result)
                s=await enrich_base_svr(result,s)
                count+=1; base+=int(bool(s.get("is_base"))); base_svr+=int(bool(s.get("is_base_svr")))
                f.write(json.dumps({"ts":now,"summary":s,"raw":msg},separators=(",",":"))+"\n"); f.flush()
                print("AUCTION",json.dumps(s,separators=(",",":")))
                if s.get("is_base_svr") and s.get("pending_move_bps") is not None:
                    print("BASE_PRICE_SIGNAL",json.dumps({k:s.get(k) for k in ("auction_id","feed","current_price","pending_price","pending_move_bps","aggregator")},separators=(",",":")))
    summary={"seconds":seconds,"notifications":count,"base":base,"base_svr":base_svr}
    print("MONITOR_SUMMARY",json.dumps(summary,separators=(",",":")))
    return summary


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seconds",type=int,default=240)
    ap.add_argument("--out",default="svr-auctions.jsonl")
    args=ap.parse_args()
    asyncio.run(run(args.seconds,args.out))


if __name__=="__main__": main()
