#!/usr/bin/env python3
"""Read-only perpetual funding differential scanner.

Normalizes each venue's predicted funding by its settlement interval before
comparison. No keys, orders, balances or signatures. Output is projected gross
funding carry only; trading fees, basis moves, slippage and changing rates are
not subtracted here.
"""
from __future__ import annotations
import json
import urllib.request

URL = "https://api.hyperliquid.xyz/info"
MIN_HL_DAY_VOLUME_USD = 5_000_000.0
MIN_HL_OI_USD = 5_000_000.0


def post(payload: dict):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(URL, data=body, headers={"content-type":"application/json","user-agent":"profit-engine-research/0.8"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read())


def f(x):
    try: return float(x)
    except Exception: return None


def main():
    meta, ctxs = post({"type":"metaAndAssetCtxs"})
    current = {}
    for u,c in zip(meta.get("universe",[]),ctxs):
        coin=u.get("name")
        funding=f(c.get("funding")); mark=f(c.get("markPx")); oracle=f(c.get("oraclePx")); oi=f(c.get("openInterest")); vol=f(c.get("dayNtlVlm"))
        basis=((mark/oracle)-1)*10000 if mark and oracle else None
        oi_usd=(oi*mark) if oi is not None and mark is not None else None
        current[coin]={
            "coin":coin,
            "hl_funding_hourly":funding,
            "mark":mark,
            "oracle":oracle,
            "mark_oracle_basis_bps":basis,
            "hl_open_interest_units":oi,
            "hl_open_interest_usd_approx":oi_usd,
            "hl_day_volume_usd":vol,
        }

    predicted=post({"type":"predictedFundings"})
    carries=[]
    venue_points=0
    if isinstance(predicted,list):
        for item in predicted:
            if not (isinstance(item,list) and len(item)>=2 and isinstance(item[1],list)):
                continue
            coin=str(item[0])
            venues=[]
            for ent in item[1]:
                if not (isinstance(ent,list) and len(ent)>=2):
                    continue
                venue=str(ent[0]); val=ent[1]
                if isinstance(val,dict):
                    rate=f(val.get("fundingRate") or val.get("funding") or val.get("rate"))
                    interval=f(val.get("fundingIntervalHours")) or 1.0
                    next_ms=val.get("nextFundingTime")
                else:
                    rate=f(val); interval=1.0; next_ms=None
                if rate is None or interval <= 0:
                    continue
                hourly=rate/interval
                venues.append({
                    "venue":venue,
                    "funding_rate_per_settlement":rate,
                    "interval_hours":interval,
                    "funding_hourly_normalized":hourly,
                    "next_funding_time_ms":next_ms,
                })
                venue_points += 1
            if len(venues) < 2:
                continue
            # Positive funding: longs pay shorts. Negative funding: shorts pay longs.
            # Delta-neutral funding carry therefore longs the lowest hourly rate and
            # shorts the highest hourly rate.
            long_leg=min(venues,key=lambda x:x["funding_hourly_normalized"])
            short_leg=max(venues,key=lambda x:x["funding_hourly_normalized"])
            edge=short_leg["funding_hourly_normalized"]-long_leg["funding_hourly_normalized"]
            if edge <= 0:
                continue
            ctx=current.get(coin,{})
            vol=ctx.get("hl_day_volume_usd")
            oi_usd=ctx.get("hl_open_interest_usd_approx")
            practical=bool(vol is not None and oi_usd is not None and vol>=MIN_HL_DAY_VOLUME_USD and oi_usd>=MIN_HL_OI_USD)
            carries.append({
                "coin":coin,
                "long_venue":long_leg["venue"],
                "long_hourly_rate":long_leg["funding_hourly_normalized"],
                "long_interval_hours":long_leg["interval_hours"],
                "long_next_funding_ms":long_leg["next_funding_time_ms"],
                "short_venue":short_leg["venue"],
                "short_hourly_rate":short_leg["funding_hourly_normalized"],
                "short_interval_hours":short_leg["interval_hours"],
                "short_next_funding_ms":short_leg["next_funding_time_ms"],
                "gross_edge_hourly":edge,
                "gross_edge_bps_per_hour":edge*10000,
                "gross_usd_per_hour_at_1000_notional":edge*1000,
                "gross_usd_per_hour_at_10000_notional":edge*10000,
                "hl_day_volume_usd":vol,
                "hl_open_interest_usd_approx":oi_usd,
                "hl_mark_oracle_basis_bps":ctx.get("mark_oracle_basis_bps"),
                "practical_liquidity_filter":practical,
            })

    carries.sort(key=lambda x:x["gross_edge_hourly"],reverse=True)
    practical=[x for x in carries if x["practical_liquidity_filter"]]
    for r in practical[:30]:
        print(json.dumps({"kind":"practical_carry",**r},separators=(",",":")))
    print(json.dumps({
        "kind":"summary",
        "hl_markets":len(current),
        "venue_points":venue_points,
        "carry_pairs":len(carries),
        "practical_pairs":len(practical),
        "best_practical":practical[0] if practical else None,
        "best_any":carries[0] if carries else None,
        "warning":"projected gross funding only; rates can change before settlement and execution costs/basis risk are excluded"
    },separators=(",",":")))

if __name__=="__main__": main()
