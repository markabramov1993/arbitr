"""Normalize and rank bounty discovery data without treating discovery as proof."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from math import isfinite
from typing import Any, Iterable, Mapping
from urllib.parse import urlparse


class InvalidHit(ValueError):
    """Raised when a source record cannot be safely normalized."""


@dataclass(frozen=True, slots=True)
class BountyHit:
    sponsor: str
    nominal: float
    status: str
    url: str
    evidence: str = ""
    currency: str = "USD"

    def __post_init__(self) -> None:
        if not self.sponsor.strip():
            raise InvalidHit("sponsor must not be empty")
        if not isfinite(self.nominal) or self.nominal < 0:
            raise InvalidHit("nominal must be a finite, non-negative number")
        if self.status not in {"DISCOVERY", "VERIFIED"}:
            raise InvalidHit("status must be DISCOVERY or VERIFIED")
        parsed = urlparse(self.url.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise InvalidHit("url must be an absolute HTTP(S) URL")
        if not self.currency.strip():
            raise InvalidHit("currency must not be empty")

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class DiscoveryReport:
    generated_at: str
    minimum_nominal: float
    max_nominal: float
    hits: tuple[BountyHit, ...]

    @property
    def discovery_only(self) -> bool:
        return bool(self.hits) and all(hit.status == "DISCOVERY" for hit in self.hits)

    def as_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "minimum_nominal": self.minimum_nominal,
            "max_nominal": self.max_nominal,
            "discovery_only": self.discovery_only,
            "hits": [hit.as_dict() for hit in self.hits],
        }


def parse_hits(records: Iterable[Mapping[str, Any]]) -> tuple[BountyHit, ...]:
    """Normalize mappings and remove duplicate URLs, keeping the highest value."""
    best: dict[str, BountyHit] = {}
    for record in records:
        try:
            hit = BountyHit(
                sponsor=str(record["sponsor"]).strip(),
                nominal=float(record["nominal"]),
                status=str(record.get("status", "DISCOVERY")).strip().upper(),
                url=str(record["url"]).strip(),
                evidence=str(record.get("evidence", "")),
                currency=str(record.get("currency", "USD")).strip().upper(),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise InvalidHit(f"invalid bounty record: {exc}") from exc
        previous = best.get(hit.url)
        if previous is None or hit.nominal > previous.nominal:
            best[hit.url] = hit
    return tuple(sorted(best.values(), key=lambda item: (-item.nominal, item.sponsor.lower(), item.url)))


def build_report(records: Iterable[Mapping[str, Any]], minimum_nominal: float = 500) -> DiscoveryReport:
    """Return high-value hits. Values are nominal claims, not payout verification."""
    if not isfinite(minimum_nominal) or minimum_nominal < 0:
        raise ValueError("minimum_nominal must be a finite, non-negative number")
    hits = tuple(hit for hit in parse_hits(records) if hit.nominal >= minimum_nominal)
    max_nominal = max((hit.nominal for hit in hits), default=0.0)
    return DiscoveryReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
        minimum_nominal=minimum_nominal,
        max_nominal=max_nominal,
        hits=hits,
    )
