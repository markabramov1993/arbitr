"""CLI entry point for the Superteam agent radar.

Usage:
    python -m superteam_radar [--min-reward 100] [--json]
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys

from .radar import SuperteamRadar


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Superteam agent-eligible bounty radar"
    )
    parser.add_argument(
        "--min-reward",
        type=float,
        default=0.0,
        help="Minimum reward to include (default: 0.0)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of markdown",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    radar = SuperteamRadar(min_reward=args.min_reward)

    try:
        if args.json:
            report = asyncio.run(radar.scan())
            output = {
                "utc_timestamp": report.utc_timestamp.isoformat(),
                "eligible_count": len(report.eligible_listings),
                "max_agent_reward_detected": report.max_agent_reward_detected,
                "listings": [
                    {
                        "id": l.id,
                        "slug": l.slug,
                        "title": l.title,
                        "agent_access": l.agent_access.value,
                        "status": l.status.value,
                        "deadline": l.deadline.isoformat() if l.deadline else None,
                        "reward_detected": l.reward_detected,
                        "token": l.token,
                        "type": l.type.value,
                        "url": l.url,
                    }
                    for l in report.eligible_listings
                ],
            }
            print(json.dumps(output, indent=2))
        else:
            markdown = asyncio.run(radar.scan_and_report())
            print(markdown)
    except Exception as exc:
        logging.getLogger(__name__).error("Radar scan failed: %s", exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
