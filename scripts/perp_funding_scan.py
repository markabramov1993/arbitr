#!/usr/bin/env python3
"""Read-only perpetual funding scanner.

Uses Hyperliquid public info endpoints. No keys, orders, balances or signatures.
Prints current funding/basis plus predicted funding data that Hyperliquid exposes
for multiple venues, then ranks the largest funding differentials when schema permits.
"""
from __future__ import annotations
import json
import urllib.request

URL = "https://api.hyperliquid.xyz/info"


def post(payload: dict):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(URL, data=body, headers={"content-type":"application/json","user-agent":"profit-engine-research/0.7"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read())


def f(x):
    try: return float(x)
    except Exception: return None


def main():
    meta_ctx = post({"type":"metaAndAssetCtxs"})
    meta, ctxs = meta_ctx
    rows=[]
    for u,c in zip(meta.get("universe",[]),ctxs):
        coin=u.get("name")
        funding=f(c.get("funding")); mark=f(c.get("markPx")); oracle=f(c.get("oraclePx")); oi=f(c.get("openInterest")); vol=f(c.get("dayNtlVlm"))
        basis=((mark/oracle)-1)*10000 if mark and oracle else None
        apr=funding*24*365*100 if funding is not None else None  # HL funding is hourly.
        rows.append({"coin":coin,"funding_hourly":funding,"funding_apr_pct_simple":apr,"mark":mark,"oracle":oracle,"mark_oracle_basis_bps":basis,"open_interest":oi,"day_volume_usd":vol})
    rows.sort(key=lambda r: abs(r["funding_hourly"] or 0), reverse=True)
    for r in rows[:40]:
        print(json.dumps({"kind":"hl_current",**r},separators=(",",":")))

    predicted=post({"type":"predictedFundings"})
    print(json.dumps({"kind":"predicted_schema","python_type":type(predicted).__name__,"sample":predicted[:3] if isinstance(predicted,list) else predicted},separators=(",",":")))

    # Common current response shape: [[coin, [[venue, rate], ...]], ...].
    diffs=[]
    if isinstance(predicted,list):
        for item in predicted:
            if not (isinstance(item,list) and len(item)>=2 and isinstance(item[1],list)):
                continue
            coin=item[0]
            vr=[]
            for ent in item[1]:
                if not (isinstance(ent,list) and len(ent)>=2):
                    continue
                venue=str(ent[0]); val=ent[1]
                # Some schemas wrap rate in an object.
                if isinstance(val,dict): rate=f(val.get("fundingRate") or val.get("funding") or val.get("rate"))
                else: rate=f(val)
                if rate is not None: vr.append((venue,rate))
            for i,a in enumerate(vr):
                for b in vr[i+1:]:
                    gap=abs(a[1]-b[1])
                    diffs.append({"coin":coin,"venue_a":a[0],"rate_a":a[1],"venue_b":b[0],"rate_b":b[1],"abs_rate_gap":gap})
    diffs.sort(key=lambda x:x["abs_rate_gap"],reverse=True)
    for d in diffs[:50]:
        print(json.dumps({"kind":"funding_diff",**d},separators=(",",":")))
    print(json.dumps({"kind":"summary","markets":len(rows),"venue_diffs":len(diffs),"largest_current_funding":rows[0] if rows else None,"largest_venue_diff":diffs[0] if diffs else None},separators=(",",":")))

if __name__=="__main__": main()
