#!/usr/bin/env python3
"""Post-process SVR monitor JSONL into relative-price Morpho risk signals."""
from __future__ import annotations

import argparse
import json

from svr_morpho_future_hf import analyze_signal


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--max-signals", type=int, default=12)
    args = ap.parse_args()

    seen: set[tuple[str, int, int]] = set()
    signals = []
    with open(args.path, "r", encoding="utf-8") as fh:
        for line in fh:
            try:
                row = json.loads(line)
            except Exception:
                continue
            summary = row.get("summary") or {}
            if not summary.get("is_base_svr"):
                continue
            feed = summary.get("feed")
            current = summary.get("current_price")
            pending = summary.get("pending_price")
            if not feed or not current or not pending:
                continue
            key = (str(feed), int(float(current) * 1e8), int(float(pending) * 1e8))
            if key in seen:
                continue
            seen.add(key)
            signals.append((feed, float(current), float(pending), summary))

    total_future = 0
    total_cross = 0
    for feed, current, pending, summary in signals[: args.max_signals]:
        move_bps = (pending / current - 1.0) * 10000.0
        print("SVR_SIGNAL", json.dumps({
            "auction_id": summary.get("auction_id"),
            "feed": feed,
            "current_price": current,
            "pending_price": pending,
            "move_bps": move_bps,
        }, separators=(",", ":")))
        try:
            rows = analyze_signal(feed, current, pending)
        except Exception as exc:
            print("MORPHO_ANALYSIS_ERROR", json.dumps({"feed": feed, "error": str(exc)[:200]}))
            continue
        total_future += len(rows)
        for r in rows[:20]:
            if r.get("crosses_liquidation"):
                total_cross += 1
                print("FUTURE_LIQUIDATION_CROSS", json.dumps(r, separators=(",", ":")))
            else:
                print("FUTURE_NEAR_LIQUIDATION", json.dumps(r, separators=(",", ":")))

    print("FUTURE_HF_SUMMARY", json.dumps({
        "distinct_svr_signals": min(len(signals), args.max_signals),
        "future_near_liquidations": total_future,
        "crosses_liquidation": total_cross,
    }, separators=(",", ":")))


if __name__ == "__main__":
    main()
