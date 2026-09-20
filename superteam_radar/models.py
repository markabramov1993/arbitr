"""Data models for Superteam bounty radar."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class AgentAccess(str, Enum):
    AGENT_ALLOWED = "AGENT_ALLOWED"
    AGENT_FORBIDDEN = "AGENT_FORBIDDEN"
    UNKNOWN = "UNKNOWN"


class ListingStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    PAUSED = "PAUSED"
    UNKNOWN = "UNKNOWN"


class BountyType(str, Enum):
    BOUNTY = "bounty"
    GRANT = "grant"
    CONTEST = "contest"
    UNKNOWN = "unknown"


@dataclass
class SuperteamListing:
    """A single Superteam listing (bounty/grant/contest)."""

    id: str
    slug: str
    title: str
    agent_access: AgentAccess
    status: ListingStatus
    deadline: Optional[datetime]
    reward_detected: float
    token: str
    type: BountyType
    url: str = ""
    raw: dict = field(default_factory=dict, repr=False)

    @property
    def is_agent_eligible(self) -> bool:
        return self.agent_access == AgentAccess.AGENT_ALLOWED

    @property
    def is_open(self) -> bool:
        return self.status == ListingStatus.OPEN

    @property
    def is_eligible(self) -> bool:
        """Eligible = agent-allowed AND open."""
        return self.is_agent_eligible and self.is_open

    def to_radar_line(self) -> str:
        """Format as a single radar report line."""
        deadline_str = self.deadline.isoformat() if self.deadline else "N/A"
        return (
            f"- id: {self.id}\n"
            f"- slug: {self.slug}\n"
            f"- agentAccess: {self.agent_access.value}\n"
            f"- status: {self.status.value}\n"
            f"- deadline: {deadline_str}\n"
            f"- reward_detected: {self.reward_detected}\n"
            f"- token: {self.token}\n"
            f"- type: {self.type.value}"
        )


@dataclass
class RadarReport:
    """Aggregated radar scan result."""

    utc_timestamp: datetime
    listings: list[SuperteamListing] = field(default_factory=list)

    @property
    def eligible_listings(self) -> list[SuperteamListing]:
        return [l for l in self.listings if l.is_eligible]

    @property
    def max_agent_reward_detected(self) -> float:
        rewards = [l.reward_detected for l in self.eligible_listings]
        return max(rewards) if rewards else 0.0

    def to_markdown(self) -> str:
        """Render the full radar report as markdown."""
        lines: list[str] = []
        lines.append("# Superteam agent-eligible live radar")
        lines.append("")
        lines.append(f"UTC: {self.utc_timestamp.isoformat()}")
        lines.append("")
        lines.append(f"Eligible live listings: {len(self.eligible_listings)}")
        lines.append("")
        for listing in self.eligible_listings:
            lines.append(f"## {listing.title}")
            lines.append(listing.to_radar_line())
            lines.append("")
        lines.append(f"MAX_AGENT_REWARD_DETECTED={self.max_agent_reward_detected}")
        lines.append("")
        return "\n".join(lines)
