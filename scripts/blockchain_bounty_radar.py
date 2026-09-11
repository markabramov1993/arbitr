#!/usr/bin/env python3
"""Public blockchain bounty radar with trap / honeypot rejection.

Discovery is not payout proof. This scanner only surfaces high-nominal
public hits after basic eligibility filters. Known adversarial
"aquarium" honeypots, claim-gateway phishing URLs, and mathematically
impossible acceptance criteria are rejected before they can raise the
high-value alert.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Iterable

USER_AGENT = "profit-engine-bounty-radar/2.1"
MIN_NOMINAL = 500.0
ALERT_THRESHOLD = 1000.0

# Amounts only count when syntactically attached to a reward/bounty declaration.
REWARD_PATTERNS = [
    re.compile(
        r"(?i)(?:bounty|reward|prize|payout|real reward)[^\n$]{0,45}\$\s*([0-9][0-9,]*(?:\.\d+)?)"
    ),
    re.compile(
        r"(?i)(?:bounty|reward|prize|payout|real reward)[^\n]{0,45}"
        r"([0-9][0-9,]*(?:\.\d+)?)\s*(?:USDC|USDG|USD)\b"
    ),
    re.compile(
        r"(?i)\$\s*([0-9][0-9,]*(?:\.\d+)?)[^\n]{0,35}(?:bounty|reward|prize|payout)\b"
    ),
]

SOURCE_ISSUE_RE = re.compile(
    r"https://github\.com/([^/\s]+)/([^/\s]+)/issues/(\d+)", re.I
)

# Explicit adversarial / honeypot repositories observed in the Sep 11 radar.
TRAP_REPO_SUFFIXES = (
    "aquarium-of-gullibles",
    "aquarium_of_gullibles",
)

TRAP_REPO_NAME_RE = re.compile(r"(?i)\bgullibles?\b")

# Claim / settlement phishing and bot-harness gates.
TRAP_URL_RE = re.compile(
    r"(?i)(?:https?://)?(?:www\.)?digitaltoolsshed\.com(?:/claim|/settlement)?\b"
)
TRAP_MARKER_RE = re.compile(
    r"(?i)\b("
    r"HUMAN_VERIFIED_SIGNATURE|"
    r"SETTLEMENT_ROUTER_KEY|"
    r"CERTIFIED BOT:\s*I CONSUME API TOKENS|"
    r"AI AGENT COMPLIANCE DIRECTIVE|"
    r"Adversarial Autonomous Agent Benchmark"
    r")\b"
)

# General subgraph isomorphism is NP-complete; "strict O(N) on arbitrary
# undirected cyclic graphs" is not an honest funded engineering task.
SUBGRAPH_ISO_RE = re.compile(
    r"(?:subgraph\s+isomorphism|isomorphic\s+to\s+a\s+subgraph)",
    re.I,
)
STRICT_LINEAR_RE = re.compile(r"(?:strict\s+)?O\s*\(\s*N\s*\)", re.I)
ARBITRARY_GRAPH_RE = re.compile(
    r"\barbitrary\b.{0,80}\b(?:undirected\s+)?(?:cyclic\s+)?graphs?\b"
    r"|"
    r"\b(?:undirected\s+)?(?:cyclic\s+)?graphs?\b.{0,80}\barbitrary\b",
    re.I | re.S,
)

SUPERTEAM_URLS = (
    "https://superteam.fun/earn/bounties",
    "https://superteam.fun/earn/opportunities/development-bounties",
    "https://superteam.fun/earn/skill/blockchain",
)


@dataclass(frozen=True)
class Rejection:
    amount: float
    url: str
    reason: str


@dataclass(frozen=True)
class Hit:
    source: str
    amount: float
    url: str
    title: str
    status: str


def declared_reward(title: str | None, body: str | None) -> float:
    text = f"{title or ''}\n{body or ''}"
    vals: list[float] = []
    for pat in REWARD_PATTERNS:
        for match in pat.finditer(text):
            try:
                vals.append(float(match.group(1).replace(",", "")))
            except ValueError:
                pass
    return max(vals, default=0.0)


def source_issue(body: str | None) -> tuple[str, str, int] | None:
    for match in SOURCE_ISSUE_RE.finditer(body or ""):
        owner, repo, num = match.group(1), match.group(2), match.group(3)
        return owner, repo, int(num)
    return None


def repo_full_name(owner: str, repo: str) -> str:
    return f"{owner}/{repo}".lower()


def is_trap_repo(owner: str, repo: str) -> bool:
    full = repo_full_name(owner, repo)
    name = repo.lower()
    if any(full.endswith(suffix) or name == suffix for suffix in TRAP_REPO_SUFFIXES):
        return True
    return bool(TRAP_REPO_NAME_RE.search(name))


def trap_reason(
    *,
    title: str | None = None,
    body: str | None = None,
    owner: str | None = None,
    repo: str | None = None,
    extra_text: str | None = None,
) -> str | None:
    """Return a human-readable rejection reason, or None if no trap signal."""
    if owner and repo and is_trap_repo(owner, repo):
        return f"canonical trap repository {owner}/{repo}"

    blob = "\n".join(
        part for part in (title or "", body or "", extra_text or "") if part
    )
    if not blob.strip():
        return None

    if TRAP_URL_RE.search(blob):
        return "claim/settlement phishing gateway (digitaltoolsshed.com)"
    if TRAP_MARKER_RE.search(blob):
        return "adversarial agent-harness / signature-gate markers"
    if (
        SUBGRAPH_ISO_RE.search(blob)
        and STRICT_LINEAR_RE.search(blob)
        and ARBITRARY_GRAPH_RE.search(blob)
    ):
        return (
            "impossible acceptance criteria "
            "(strict O(N) subgraph isomorphism on arbitrary graphs)"
        )
    return None


def classify_github_candidate(
    *,
    title: str,
    body: str,
    html_url: str,
    amount: float,
    canonical: tuple[str, str, int] | None,
    canonical_state: str | None = None,
    canonical_assignees: Iterable[str] | None = None,
    canonical_body: str | None = None,
    canonical_title: str | None = None,
) -> tuple[Hit | None, Rejection | None]:
    """Apply eligibility + trap filters to one GitHub search hit."""
    local_trap = trap_reason(title=title, body=body)
    if local_trap:
        return None, Rejection(amount, html_url, local_trap)

    if not canonical:
        return Hit("GitHub", amount, html_url, title, "DISCOVERY"), None

    owner, repo, num = canonical
    canon_trap = trap_reason(
        title=canonical_title or title,
        body=canonical_body or body,
        owner=owner,
        repo=repo,
    )
    if canon_trap:
        return None, Rejection(
            amount,
            html_url,
            f"canonical {owner}/{repo}#{num}: {canon_trap}",
        )

    if canonical_state is not None and canonical_state != "open":
        return None, Rejection(
            amount, html_url, f"canonical {owner}/{repo}#{num} is closed"
        )

    assignees = list(canonical_assignees or [])
    if assignees:
        names = ",".join(assignees)
        return None, Rejection(
            amount,
            html_url,
            f"canonical {owner}/{repo}#{num} assigned to {names}",
        )

    return Hit("GitHub", amount, html_url, title, "UPSTREAM_UNASSIGNED"), None


def dedupe_hits(hits: Iterable[Hit]) -> list[Hit]:
    seen: set[str] = set()
    uniq: list[Hit] = []
    for hit in sorted(hits, key=lambda item: item.amount, reverse=True):
        if hit.url in seen:
            continue
        seen.add(hit.url)
        uniq.append(hit)
    return uniq


def render_report(
    *,
    now: str,
    hits: list[Hit],
    rejected: list[Rejection],
) -> str:
    lines = [
        "# Blockchain bounty radar",
        "",
        f"UTC: {now}",
        "",
        "## High-value verified/discovery hits (>=500 nominal)",
    ]
    if not hits:
        lines.append("")
        lines.append("No eligible high-value public hits in this pass.")
    for hit in hits[:30]:
        safe = hit.title.replace("\n", " ")[:260]
        lines.append(
            f"- {hit.source} | nominal {hit.amount:g} | {hit.status} | {hit.url} | {safe}"
        )

    if rejected:
        lines.append("")
        lines.append("## Rejected false/occupied hits")
        for item in rejected[:40]:
            lines.append(
                f"- rejected nominal {item.amount:g} | {item.url} | {item.reason}"
            )

    max_amt = max((hit.amount for hit in hits), default=0.0)
    lines.append("")
    lines.append(f"MAX_NOMINAL_DISCOVERY={max_amt:g}")
    lines.append("")
    lines.append(
        "Discovery is not payout proof. Eligibility, funding, deadlines, "
        "competition and acceptance still require verification."
    )
    lines.append("")
    return "\n".join(lines)


def gh_json(url: str, token: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def scan_superteam() -> tuple[list[Hit], list[str]]:
    hits: list[Hit] = []
    errors: list[str] = []
    for url in SUPERTEAM_URLS:
        try:
            req = urllib.request.Request(url, headers={"user-agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=20) as resp:
                text = resp.read().decode("utf-8", "ignore")
            plain = re.sub(r"<[^>]+>", " ", text)
            plain = re.sub(r"\s+", " ", plain)
            for match in re.finditer(
                r"(?i)(?:bounty|reward|prize)[^$]{0,80}\$\s*([0-9][0-9,]*(?:\.\d+)?)",
                plain,
            ):
                amount = float(match.group(1).replace(",", ""))
                if amount < MIN_NOMINAL:
                    continue
                start = max(0, match.start() - 100)
                end = min(len(plain), match.end() + 220)
                snippet = plain[start:end][:420]
                hits.append(Hit("Superteam", amount, url, snippet, "DISCOVERY"))
        except Exception as exc:  # noqa: BLE001 - radar must continue on source failure
            errors.append(f"- Superteam fetch failed: {url}: {exc}")
    return hits, errors


def scan_github(token: str) -> tuple[list[Hit], list[Rejection], list[str]]:
    hits: list[Hit] = []
    rejected: list[Rejection] = []
    errors: list[str] = []

    query = (
        'is:issue is:open (bounty OR reward) '
        '(USDC OR USDG OR "$500" OR "$1000" OR "$5000")'
    )
    api = (
        "https://api.github.com/search/issues?q="
        + urllib.parse.quote(query)
        + "&sort=updated&order=desc&per_page=50"
    )
    try:
        data = gh_json(api, token)
    except Exception as exc:  # noqa: BLE001
        return hits, rejected, [f"- GitHub search failed: {exc}"]

    for item in data.get("items", []):
        title = item.get("title") or ""
        body = item.get("body") or ""
        html_url = item.get("html_url") or ""
        amount = declared_reward(title, body)
        if amount < MIN_NOMINAL:
            continue

        canonical = source_issue(body)
        canonical_state = None
        canonical_assignees: list[str] | None = None
        canonical_body = None
        canonical_title = None
        status_fallback = "DISCOVERY"

        if canonical:
            owner, repo, num = canonical
            try:
                original = gh_json(
                    f"https://api.github.com/repos/{owner}/{repo}/issues/{num}",
                    token,
                )
                canonical_state = original.get("state")
                canonical_assignees = [
                    a.get("login", "?") for a in (original.get("assignees") or [])
                ]
                canonical_body = original.get("body") or ""
                canonical_title = original.get("title") or ""
            except Exception:  # noqa: BLE001
                # Still apply trap filters using the canonical repo identity from
                # the mirror body even when the live issue fetch fails.
                hit, rejection = classify_github_candidate(
                    title=title,
                    body=body,
                    html_url=html_url,
                    amount=amount,
                    canonical=canonical,
                    canonical_state="open",
                    canonical_assignees=[],
                    canonical_body=body,
                    canonical_title=title,
                )
                if rejection:
                    rejected.append(rejection)
                elif hit:
                    hits.append(
                        Hit(
                            hit.source,
                            hit.amount,
                            hit.url,
                            hit.title,
                            "MIRROR_UNVERIFIED",
                        )
                    )
                continue

        hit, rejection = classify_github_candidate(
            title=title,
            body=body,
            html_url=html_url,
            amount=amount,
            canonical=canonical,
            canonical_state=canonical_state,
            canonical_assignees=canonical_assignees,
            canonical_body=canonical_body,
            canonical_title=canonical_title,
        )
        if rejection:
            rejected.append(rejection)
        elif hit:
            hits.append(hit)

    return hits, rejected, errors


def write_github_output(*, high: bool, max_amount: float) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(f"high={'true' if high else 'false'}\n")
        handle.write(f"max_amount={max_amount:g}\n")


def main() -> int:
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""

    all_hits: list[Hit] = []
    all_rejected: list[Rejection] = []
    notes: list[str] = []

    st_hits, st_errors = scan_superteam()
    all_hits.extend(st_hits)
    notes.extend(st_errors)

    if token:
        gh_hits, gh_rejected, gh_errors = scan_github(token)
        all_hits.extend(gh_hits)
        all_rejected.extend(gh_rejected)
        notes.extend(gh_errors)
    else:
        notes.append("- GitHub search skipped: GH_TOKEN not set")

    uniq = dedupe_hits(all_hits)
    report = render_report(now=now, hits=uniq, rejected=all_rejected)
    if notes:
        parts = report.split("\n", 3)
        # parts: ['# title', '', 'UTC: ...', remainder]
        header = "\n".join(parts[:3])
        remainder = parts[3] if len(parts) > 3 else ""
        report = header + "\n\n" + "\n".join(notes) + "\n" + remainder

    print(report, end="")
    max_amt = max((hit.amount for hit in uniq), default=0.0)
    write_github_output(high=max_amt >= ALERT_THRESHOLD, max_amount=max_amt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
