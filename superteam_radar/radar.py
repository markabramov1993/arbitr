"""Core radar scan logic: fetch, filter, and report."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

from .client import SuperteamClient
from .models import RadarReport, SuperteamListing

logger = logging.getLogger(__name__)


class SuperteamRadar:
    """Orchestrates the full radar scan cycle."""

    def __init__(
        self,
        client: Optional[SuperteamClient] = None,
        min_reward: float = 0.0,
    ) -> None:
        self.client = client or SuperteamClient()
        self.min_reward = min_reward

    async def scan(self) -> RadarReport:
        """Run a full radar scan and return the report."""
        utc_now = datetime.now(timezone.utc)
        logger.info("Starting Superteam agent radar scan at %s", utc_now.isoformat())

        listings = await self.client.fetch_listings(
            status="OPEN",
            agent_access="AGENT_ALLOWED",
        )

        # Filter by minimum reward if configured
        if self.min_reward > 0:
            listings = [l for l in listings if l.reward_detected >= self.min_reward]

        report = RadarReport(
            utc_timestamp=utc_now,
            listings=listings,
        )

        logger.info(
            "Scan complete: %d total, %d eligible, max reward %.2f %s",
            len(listings),
            len(report.eligible_listings),
            report.max_agent_reward_detected,
            "USDC",
        )
        return report

    async def scan_and_report(self) -> str:
        """Run scan and return the markdown report string."""
        report = await self.scan()
        return report.to_markdown()
