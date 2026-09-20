# RustChain #16471 finding — docstring cron can go green after discovery API failure

Verified against Scottcjn/rustchain-bounties main commit
13f87382b2d67685ef6ab8aee2dcef6fe2058f90 on 2026-09-20.

Scope: .github/workflows/docstring-gate.yml

## Finding

The scheduled Docstring Bounty Gate suppresses both discovery-query failures:

    held=$(gh api -X GET search/issues ... 2>/dev/null || true)
    fresh=$(gh api -X GET search/issues ... 2>/dev/null || true)

If GitHub Search returns a transport error, auth error, secondary-rate-limit error,
5xx, or another non-zero exit, the failing command is converted to success and
the corresponding variable becomes empty.

The later accounting only counts issues returned by those variables:

    attempted=0
    adjudicated=0
    failed=0
    for i in $(printf '%s\n%s\n' "$held" "$fresh" | sort -un); do
        ...
    done

    echo "attempted ${attempted} claim(s): adjudicated ${adjudicated}, failed ${failed}"

    if [ "$failed" -gt 0 ]; then
        exit 1
    fi

With both discovery reads unavailable, the loop performs zero iterations,
failed remains zero, and the scheduled job exits 0. The workflow is green even
though it did not discover or adjudicate any awaiting-merge/recent docstring
claims.

This is distinct from defects already reported in scripts/docstring_gate.py.
The gate script can fail closed once it is actually invoked; this finding is in
the workflow layer before ISSUE_NUMBER is ever selected.

## Deterministic reproduction of the shell control flow

The GitHub API does not need to be disturbed. Replace each gh search with a
command that exits non-zero:

    set -uo pipefail
    held=$(false 2>/dev/null || true)
    fresh=$(false 2>/dev/null || true)

    attempted=0
    adjudicated=0
    failed=0

    for i in $(printf '%s\n%s\n' "$held" "$fresh" | sort -un); do
        [ -z "$i" ] && continue
        attempted=$((attempted+1))
    done

    echo "attempted ${attempted} claim(s): adjudicated ${adjudicated}, failed ${failed}"

    if [ "$failed" -gt 0 ]; then
        exit 1
    fi

    echo "exit=0"

Observed result by shell semantics:

    attempted 0 claim(s): adjudicated 0, failed 0
    exit=0

That is indistinguishable from a genuinely empty queue in Actions.

## Impact

A scheduled sweep can report success while all held/fresh claims remain
unprocessed. Because the schedule is the mechanism that revisits
awaiting-merge claims after their PR later lands, this can delay payouts and
hide a discovery outage behind a green run. There is no error annotation and
no count saying discovery itself failed.

Even if a later 3-hour sweep succeeds, the failed run is still a silent-success
event: the effect expected from that run (authoritative queue enumeration and
adjudication) never happened.

## Suggested fix

Do not suppress authoritative discovery failures.

One safe shape:

    if ! held=$(gh api ... --jq '.items[].number'); then
        echo "::error::failed to enumerate awaiting-merge docstring claims"
        exit 1
    fi

    if ! fresh=$(gh api ... --jq '.items[].number'); then
        echo "::error::failed to enumerate fresh docstring claims"
        exit 1
    fi

If partial progress is desired, record discovery_ok flags separately and still
fail the job when either authoritative query failed.

Add a workflow-level regression test or extract the enumeration into a tested
script where a non-zero gh exit must produce a non-zero gate exit.

## Duplicate check

Before submission I searched the public bounty tracker for:
- "docstring-gate.yml" silent
- "Docstring Bounty Gate" scheduled
- "gh api" awaiting-merge docstring
- "2>/dev/null || true" docstring

I found #16471 itself, #16662 (failed payable label writes in docstring_gate.py),
#16711 (weekly-cap repeated comment spam), and unrelated findings, but no report
of this scheduled-discovery fail-open path.

No production endpoint, payout API, secret, or fund movement was used.
