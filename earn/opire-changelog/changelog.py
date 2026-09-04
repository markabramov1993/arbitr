#!/usr/bin/env python3
"""Generate a Keep-a-Changelog style CHANGELOG from git history."""
from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

CATEGORIES = ("Added", "Fixed", "Changed", "Removed")
CONVENTIONAL = {
    "feat": "Added", "add": "Added", "new": "Added",
    "fix": "Fixed", "bugfix": "Fixed", "hotfix": "Fixed",
    "refactor": "Changed", "perf": "Changed", "docs": "Changed",
    "test": "Changed", "build": "Changed", "ci": "Changed",
    "chore": "Changed", "style": "Changed", "change": "Changed",
    "remove": "Removed", "delete": "Removed", "deprecate": "Removed",
}

@dataclass(frozen=True)
class Commit:
    sha: str
    subject: str


def git(*args: str, cwd: Path | None = None, allow_fail: bool = False) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=cwd, text=True, capture_output=True, check=False
    )
    if proc.returncode and not allow_fail:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def latest_tag(cwd: Path | None = None) -> str | None:
    tag = git("describe", "--tags", "--abbrev=0", cwd=cwd, allow_fail=True)
    return tag or None


def commits_since(tag: str | None, cwd: Path | None = None) -> list[Commit]:
    rev = f"{tag}..HEAD" if tag else "HEAD"
    raw = git("log", rev, "--pretty=format:%h%x09%s", cwd=cwd)
    commits: list[Commit] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        sha, subject = line.split("\t", 1)
        commits.append(Commit(sha=sha, subject=subject.strip()))
    return commits


def category_for(subject: str) -> str:
    lowered = subject.lower().strip()
    conventional = re.match(r"^([a-z]+)(?:\([^)]*\))?!?:\s+", lowered)
    if conventional:
        return CONVENTIONAL.get(conventional.group(1), "Changed")
    for prefix, category in CONVENTIONAL.items():
        if lowered.startswith(prefix + " ") or lowered.startswith(prefix + ":"):
            return category
    if any(word in lowered for word in ("remove", "delete", "drop ", "deprecated")):
        return "Removed"
    if any(word in lowered for word in ("fix", "bug", "repair", "correct", "resolve")):
        return "Fixed"
    if any(word in lowered for word in ("add", "introduce", "create", "implement", "support")):
        return "Added"
    return "Changed"


def clean_subject(subject: str) -> str:
    cleaned = re.sub(r"^[a-z]+(?:\([^)]*\))?!?:\s*", "", subject, flags=re.I)
    return cleaned[:1].upper() + cleaned[1:] if cleaned else subject


def render(commits: list[Commit], tag: str | None, title: str) -> str:
    groups: dict[str, list[Commit]] = {name: [] for name in CATEGORIES}
    for commit in commits:
        groups[category_for(commit.subject)].append(commit)
    date = dt.date.today().isoformat()
    lines = ["# Changelog", "", "All notable changes to this project are documented here.", ""]
    lines += [f"## [{title}] - {date}", ""]
    if not commits:
        lines += ["No commits found since the latest tag.", ""]
    else:
        for category in CATEGORIES:
            if not groups[category]:
                continue
            lines += [f"### {category}", ""]
            for commit in groups[category]:
                lines.append(f"- {clean_subject(commit.subject)} (`{commit.sha}`)")
            lines.append("")
    baseline = tag or "repository start (no tags found)"
    lines += [f"_Generated from commits after `{baseline}`._", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="CHANGELOG.md", help="Output file path")
    parser.add_argument("--title", default="Unreleased", help="Release heading")
    parser.add_argument("--repo", default=".", help="Path to git repository")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    if not (repo / ".git").exists():
        parser.error(f"not a git repository: {repo}")
    tag = latest_tag(repo)
    commits = commits_since(tag, repo)
    output = Path(args.output)
    output.write_text(render(commits, tag, args.title), encoding="utf-8")
    print(f"Generated {output} from {len(commits)} commit(s); baseline={tag or 'none'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
