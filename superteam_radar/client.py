"""Async HTTP client for the Superteam API."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Optional

import aiohttp

from .models import SuperteamListing
from .parser import parse_listings

logger = logging.getLogger(__name__)

SUPERTEAM_API_BASE = "https://api.superteam.fun"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0


class SuperteamClient:
    """Async client for fetching Superteam listings."""

    def __init__(
        self,
        base_url: str = SUPERTEAM_API_BASE,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
        api_key: Optional[str] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.api_key = api_key

    def _headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "User-Agent": "superteam-agent-radar/1.0",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def _get(self, session: aiohttp.ClientSession, path: str) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        last_exc: Optional[Exception] = None

        for attempt in range(1, self.max_retries + 1):
            try:
                async with session.get(
                    url,
                    headers=self._headers(),
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as resp:
                    if resp.status == 429:
                        retry_after = int(resp.headers.get("Retry-After", "5"))
                        logger.warning(
                            "Rate limited (429). Retrying in %ds (attempt %d/%d)",
                            retry_after, attempt, self.max_retries,
                        )
                        await asyncio.sleep(retry_after)
                        continue
                    resp.raise_for_status()
                    return await resp.json()
            except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
                last_exc = exc
                wait = RETRY_BACKOFF * attempt
                logger.warning(
                    "Request failed (attempt %d/%d): %s. Retrying in %.1fs",
                    attempt, self.max_retries, exc, wait,
                )
                await asyncio.sleep(wait)

        raise ConnectionError(
            f"Failed to fetch {url} after {self.max_retries} attempts"
        ) from last_exc

    async def fetch_listings(
        self,
        status: str = "OPEN",
        agent_access: str = "AGENT_ALLOWED",
        page: int = 1,
        per_page: int = 50,
    ) -> list[SuperteamListing]:
        """Fetch eligible listings from the Superteam API."""
        params = {
            "status": status,
            "agentAccess": agent_access,
            "page": page,
            "perPage": per_page,
        }
        query = "&".join(f"{k}={v}" for k, v in params.items())
        path = f"/v1/listings?{query}"

        async with aiohttp.ClientSession() as session:
            data = await self._get(session, path)

        # The API may return {"data": [...]} or a bare list
        items = data.get("data", data) if isinstance(data, dict) else data
        if not isinstance(items, list):
            logger.error("Unexpected API response shape: %s", type(data))
            return []

        listings = parse_listings(items)
        logger.info("Fetched %d listings (page %d)", len(listings), page)
        return listings

    async def fetch_listing_detail(self, listing_id: str) -> dict[str, Any]:
        """Fetch full detail for a single listing."""
        path = f"/v1/listings/{listing_id}"
        async with aiohttp.ClientSession() as session:
            return await self._get(session, path)
