import pytest
from math import inf, nan

from bounty_radar.core import InvalidHit, build_report, parse_hits


def record(**overrides):
    value = {"sponsor": "Superteam", "nominal": 10000, "status": "DISCOVERY", "url": "https://superteam.fun/earn/bounties"}
    value.update(overrides)
    return value


def test_filters_threshold_and_sorts_descending():
    report = build_report([
        record(nominal=500, url="https://x.example/500"),
        record(nominal=999, url="https://x.example/999"),
        record(nominal=499, url="https://x.example/499"),
    ])
    assert [hit.nominal for hit in report.hits] == [999, 500]
    assert report.max_nominal == 999


def test_duplicate_url_keeps_highest_nominal():
    hits = parse_hits([record(nominal=500), record(nominal=1200, sponsor="Other")])
    assert len(hits) == 1
    assert hits[0].nominal == 1200


def test_defaults_status_and_currency():
    hit = parse_hits([{ "sponsor": "X", "nominal": 1, "url": "https://x.example/b" }])[0]
    assert (hit.status, hit.currency) == ("DISCOVERY", "USD")


@pytest.mark.parametrize("bad", [
    {"sponsor": "X", "nominal": -1, "url": "https://x.example"},
    {"sponsor": "X", "nominal": 1, "url": "ftp://x.example"},
    {"sponsor": "X", "nominal": 1, "status": "PAID", "url": "https://x.example"},
    {"sponsor": "X", "nominal": 1},
])
def test_rejects_unsafe_or_incomplete_records(bad):
    with pytest.raises(InvalidHit):
        parse_hits([bad])


def test_empty_report_is_safe():
    report = build_report([], 500)
    assert report.hits == ()
    assert report.max_nominal == 0
    assert report.discovery_only is False


def test_verified_hit_is_not_marked_discovery_only():
    report = build_report([record(status="VERIFIED")])
    assert report.discovery_only is False


def test_negative_threshold_rejected():
    with pytest.raises(ValueError):
        build_report([], -1)


@pytest.mark.parametrize("nominal", [nan, inf, -inf])
def test_non_finite_nominal_rejected(nominal):
    with pytest.raises(InvalidHit):
        parse_hits([record(nominal=nominal)])


@pytest.mark.parametrize("threshold", [nan, inf, -inf])
def test_non_finite_threshold_rejected(threshold):
    with pytest.raises(ValueError):
        build_report([], threshold)


def test_normalizes_outer_whitespace_and_case():
    hit = parse_hits([record(sponsor="  Sponsor  ", status=" discovery ",
                             currency=" usd ", url=" https://x.example/path ")])[0]
    assert (hit.sponsor, hit.status, hit.currency, hit.url) == (
        "Sponsor", "DISCOVERY", "USD", "https://x.example/path"
    )


def test_blank_sponsor_and_currency_rejected():
    with pytest.raises(InvalidHit):
        parse_hits([record(sponsor="   ")])
    with pytest.raises(InvalidHit):
        parse_hits([record(currency="   ")])
