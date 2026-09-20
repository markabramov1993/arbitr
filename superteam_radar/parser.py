"""Parse raw Superteam API responses into SuperteamListing objects."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from .models import AgentAccess, BountyType, ListingStatus, SuperteamListing


def _parse_agent_access(value: Any) -> AgentAccess:
    if isinstance(value, str):
        try:
            return AgentAccess(value.upper())
        except ValueError:
            pass
    return AgentAccess.UNKNOWN


def _parse_status(value: Any) -> ListingStatus:
    if isinstance(value, str):
        try:
            return ListingStatus(value.upper())
        except ValueError:
            pass
    return ListingStatus.UNKNOWN


def _parse_bounty_type(value: Any) -> BountyType:
    if isinstance(value, str):
        try:
            return BountyType(value.lower())
        except ValueError:
            pass
    return BountyType.UNKNOWN


def _parse_deadline(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        # Handle ISO 8601 with trailing Z
        cleaned = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(cleaned)
        except ValueError:
            return None
    return None


def _parse_reward(value: Any) -> float:
    if value is None:
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _parse_token(value: Any) -> str:
    if isinstance(value, str) and value:
        return value.upper()
    return "USDC"


def parse_listing(raw: dict[str, Any]) -> SuperteamListing:
    """Convert a raw API dict into a SuperteamListing.

    Handles both the Superteam API v1 shape and the internal
    normalised shape used by the radar workflow.
    """
    listing_id = str(raw.get("id", ""))
    slug = str(raw.get("slug", ""))
    title = str(raw.get("title", slug.replace("-", " ").title()))

    # agentAccess can be top-level or nested
    agent_access_raw = raw.get("agentAccess", raw.get("agent_access", "UNKNOWN"))
    agent_access = _parse_agent_access(agent_access_raw)

    status_raw = raw.get("status", "UNKNOWN")
    status = _parse_status(status_raw)

    deadline = _parse_deadline(raw.get("deadline", raw.get("endsAt")))

    # Reward can be a number, a string, or nested under reward/amount
    reward_raw = raw.get("reward_detected", raw.get("reward", raw.get("amount", 0)))
    reward_detected = _parse_reward(reward_raw)

    token = _parse_token(raw.get("token", raw.get("currency", "USDC")))

    type_raw = raw.get("type", raw.get("listingType", "bounty"))
    bounty_type = _parse_bounty_type(type_raw)

    url = str(raw.get("url", f"https://superteam.fun/listing/{slug}"))

    return SuperteamListing(
        id=listing_id,
        slug=slug,
        title=title,
        agent_access=agent_access,
        status=status,
        deadline=deadline,
        reward_detected=reward_detected,
        token=token,
        type=bounty_type,
        url=url,
        raw=raw,
    )


def parse_listings(raw_list: list[dict[str, Any]]) -> list[SuperteamListing]:
    """Parse a list of raw API dicts into SuperteamListing objects."""
    return [parse_listing(item) for item in raw_list]
