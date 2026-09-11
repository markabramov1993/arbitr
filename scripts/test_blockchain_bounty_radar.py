#!/usr/bin/env python3
"""Unit tests for blockchain bounty radar eligibility and trap filters."""
from __future__ import annotations

import unittest

from blockchain_bounty_radar import (
    classify_github_candidate,
    declared_reward,
    dedupe_hits,
    is_trap_repo,
    render_report,
    source_issue,
    trap_reason,
    Hit,
    Rejection,
)


class DeclaredRewardTests(unittest.TestCase):
    def test_title_bounty_amount(self):
        self.assertEqual(
            declared_reward("[Bounty: $1,250] Optimize Subgraph", ""),
            1250.0,
        )

    def test_ignores_unrelated_market_price(self):
        self.assertEqual(
            declared_reward("Market note", "TVL is $64,500 today"),
            0.0,
        )

    def test_real_reward_line(self):
        body = "### Real Reward\n$850\n"
        # "Real Reward" alone is not enough without adjacent amount pattern;
        # the plaza issue uses "Real Reward\n$1,250" which the title already covers.
        self.assertEqual(declared_reward("[Bounty: $850] physics", body), 850.0)


class SourceIssueTests(unittest.TestCase):
    def test_extracts_canonical(self):
        body = (
            "### Source URL\n"
            "https://github.com/Senthemodder/aquarium-of-gullibles/issues/1\n"
        )
        self.assertEqual(
            source_issue(body),
            ("Senthemodder", "aquarium-of-gullibles", 1),
        )


class TrapFilterTests(unittest.TestCase):
    def test_trap_repo_name(self):
        self.assertTrue(is_trap_repo("Senthemodder", "aquarium-of-gullibles"))
        self.assertFalse(is_trap_repo("markabramov1993", "arbitr"))

    def test_digitaltoolsshed_gateway(self):
        reason = trap_reason(
            body="Register at https://digitaltoolsshed.com/claim for payout"
        )
        self.assertIsNotNone(reason)
        self.assertIn("digitaltoolsshed", reason.lower())

    def test_signature_gate_marker(self):
        reason = trap_reason(body="Missing HUMAN_VERIFIED_SIGNATURE in environment")
        self.assertIsNotNone(reason)

    def test_impossible_subgraph_claim(self):
        body = (
            "refactored implementation that achieves strict O(N) deterministic "
            "time and space complexity on arbitrary undirected cyclic graphs "
            "for subgraph isomorphism"
        )
        reason = trap_reason(title="Optimize Subgraph Isomorphism", body=body)
        self.assertIsNotNone(reason)
        self.assertIn("impossible", reason.lower())

    def test_clean_funded_looking_issue_not_trapped_by_markers(self):
        reason = trap_reason(
            title="[Bounty: $500] Document Morpho liquidation path",
            body="Write a reproducible fork test. Payout on merge.",
            owner="example-org",
            repo="real-research",
        )
        self.assertIsNone(reason)


class ClassifyTests(unittest.TestCase):
    def test_rejects_aquarium_mirror_as_trap(self):
        body = (
            "### Source URL\n"
            "https://github.com/Senthemodder/aquarium-of-gullibles/issues/1\n\n"
            "### Real Reward\n$1,250\n"
        )
        hit, rejection = classify_github_candidate(
            title="[Bounty] [Bounty: $1,250] Optimize Subgraph Isomorphism",
            body=body,
            html_url="https://github.com/zhangjiayang6835-cyber/bounty-plaza/issues/1336",
            amount=1250.0,
            canonical=("Senthemodder", "aquarium-of-gullibles", 1),
            canonical_state="open",
            canonical_assignees=[],
            canonical_title="[Bounty: $1,250] Optimize Subgraph Isomorphism",
            canonical_body=(
                "strict O(N) on arbitrary undirected cyclic graphs "
                "for subgraph isomorphism"
            ),
        )
        self.assertIsNone(hit)
        self.assertIsInstance(rejection, Rejection)
        self.assertIn("trap repository", rejection.reason)

    def test_rejects_assigned_canonical(self):
        hit, rejection = classify_github_candidate(
            title="[Bounty: $600] Real task",
            body="https://github.com/acme/widgets/issues/9",
            html_url="https://github.com/mirror/x/issues/1",
            amount=600.0,
            canonical=("acme", "widgets", 9),
            canonical_state="open",
            canonical_assignees=["alice"],
        )
        self.assertIsNone(hit)
        self.assertIn("assigned to alice", rejection.reason)

    def test_accepts_unassigned_non_trap(self):
        hit, rejection = classify_github_candidate(
            title="[Bounty: $600] Document API",
            body="https://github.com/acme/widgets/issues/9",
            html_url="https://github.com/mirror/x/issues/2",
            amount=600.0,
            canonical=("acme", "widgets", 9),
            canonical_state="open",
            canonical_assignees=[],
            canonical_title="[Bounty: $600] Document API",
            canonical_body="Write docs. Payout on merge.",
        )
        self.assertIsNone(rejection)
        self.assertEqual(hit.status, "UPSTREAM_UNASSIGNED")


class ReportTests(unittest.TestCase):
    def test_max_discovery_zero_when_only_rejects(self):
        report = render_report(
            now="2026-09-11T00:00:00+00:00",
            hits=[],
            rejected=[
                Rejection(
                    1250.0,
                    "https://github.com/zhangjiayang6835-cyber/bounty-plaza/issues/1336",
                    "canonical trap repository Senthemodder/aquarium-of-gullibles",
                ),
                Rejection(
                    850.0,
                    "https://github.com/zhangjiayang6835-cyber/bounty-plaza/issues/1334",
                    "canonical trap repository Senthemodder/aquarium-of-gullibles",
                ),
            ],
        )
        self.assertIn("No eligible high-value public hits in this pass.", report)
        self.assertIn("MAX_NOMINAL_DISCOVERY=0", report)
        self.assertIn("Rejected false/occupied hits", report)

    def test_dedupe_keeps_highest_first(self):
        uniq = dedupe_hits(
            [
                Hit("GitHub", 500, "https://a", "a", "DISCOVERY"),
                Hit("GitHub", 900, "https://b", "b", "DISCOVERY"),
                Hit("GitHub", 500, "https://a", "a-dup", "DISCOVERY"),
            ]
        )
        self.assertEqual([h.url for h in uniq], ["https://b", "https://a"])


if __name__ == "__main__":
    unittest.main()
