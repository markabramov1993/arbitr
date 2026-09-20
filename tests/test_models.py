"""Tests for Superteam radar data models."""

from datetime import datetime, timezone

from superteam_radar.models import (
    AgentAccess,
    BountyType,
    ListingStatus,
    RadarReport,
    SuperteamListing,
)


def _make_listing(**overrides) -> SuperteamListing:
    defaults = dict(
        id="43f663e0-ef0b-40b4-89c9-b4e11375cff5",
        slug="steve-agent-arena-launch-your-agent-and-win-500-usdc",
        title="Steve Agent Arena: Launch Your Agent & Win 500 USDC",
        agent_access=AgentAccess.AGENT_ALLOWED,
        status=ListingStatus.OPEN,
        deadline=datetime(2026, 10, 1, 21, 59, 59, tzinfo=timezone.utc),
        reward_detected=500.0,
        token="USDC",
        type=BountyType.BOUNTY,
        url="https://superteam.fun/listing/steve-agent-arena",
    )
    defaults.update(overrides)
    return SuperteamListing(**defaults)


class TestSuperteamListing:
    def test_is_agent_eligible_true(self):
        listing = _make_listing()
        assert listing.is_agent_eligible is True

    def test_is_agent_eligible_false(self):
        listing = _make_listing(agent_access=AgentAccess.AGENT_FORBIDDEN)
        assert listing.is_agent_eligible is False

    def test_is_open_true(self):
        listing = _make_listing()
        assert listing.is_open is True

    def test_is_open_false(self):
        listing = _make_listing(status=ListingStatus.CLOSED)
        assert listing.is_open is False

    def test_is_eligible_requires_both(self):
        listing = _make_listing()
        assert listing.is_eligible is True

        listing_closed = _make_listing(status=ListingStatus.CLOSED)
        assert listing_closed.is_eligible is False

        listing_forbidden = _make_listing(agent_access=AgentAccess.AGENT_FORBIDDEN)
        assert listing_forbidden.is_eligible is False

    def test_to_radar_line_contains_fields(self):
        listing = _make_listing()
        line = listing.to_radar_line()
        assert "43f663e0-ef0b-40b4-89c9-b4e11375cff5" in line
        assert "AGENT_ALLOWED" in line
        assert "OPEN" in line
        assert "500.0" in line
        assert "USDC" in line
        assert "bounty" in line


class TestRadarReport:
    def test_eligible_listings_filters_correctly(self):
        eligible = _make_listing()
        closed = _make_listing(
            id="3c12a2d7-88af-40cb-add1-79546e76b8a2",
            slug="road-to-colosseum-builders-reflect-and-share",
            title="Road to Colosseum | Builders Reflect & Share",
            status=ListingStatus.CLOSED,
            reward_detected=0.0,
        )
        report = RadarReport(
            utc_timestamp=datetime(2026, 9, 20, 20, 55, 9, tzinfo=timezone.utc),
            listings=[eligible, closed],
        )
        assert len(report.eligible_listings) == 1
        assert report.eligible_listings[0].id == eligible.id

    def test_max_agent_reward_detected(self):
        l1 = _make_listing(reward_detected=500.0)
        l2 = _make_listing(
            id="3c12a2d7-88af-40cb-add1-79546e76b8a2",
            slug="road-to-colosseum-builders-reflect-and-share",
            title="Road to Colosseum | Builders Reflect & Share",
            reward_detected=0.0,
        )
        report = RadarReport(
            utc_timestamp=datetime(2026, 9, 20, 20, 55, 9, tzinfo=timezone.utc),
            listings=[l1, l2],
        )
        assert report.max_agent_reward_detected == 500.0

    def test_max_agent_reward_empty(self):
        report = RadarReport(
            utc_timestamp=datetime(2026, 9, 20, 20, 55, 9, tzinfo=timezone.utc),
            listings=[],
        )
        assert report.max_agent_reward_detected == 0.0

    def test_to_markdown_structure(self):
        l1 = _make_listing()
        l2 = _make_listing(
            id="3c12a2d7-88af-40cb-add1-79546e76b8a2",
            slug="road-to-colosseum-builders-reflect-and-share",
            title="Road to Colosseum | Builders Reflect & Share",
            reward_detected=0.0,
        )
        report = RadarReport(
            utc_timestamp=datetime(2026, 9, 20, 20, 55, 9, tzinfo=timezone.utc),
            listings=[l1, l2],
        )
        md = report.to_markdown()
        assert "# Superteam agent-eligible live radar" in md
        assert "Eligible live listings: 2" in md
        assert "Steve Agent Arena" in md
        assert "Road to Colosseum" in md
        assert "MAX_AGENT_REWARD_DETECTED=500.0" in md
