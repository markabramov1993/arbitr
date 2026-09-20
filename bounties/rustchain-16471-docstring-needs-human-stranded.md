# RustChain #16471 finding — needs-human docstring claims are excluded from the scheduled retry sweep

Verified against Scottcjn/rustchain-bounties main commit
13f87382b2d67685ef6ab8aee2dcef6fe2058f90 on 2026-09-20.

Scope: .github/workflows/docstring-gate.yml and scripts/docstring_gate.py

## Finding

The docstring gate script itself does not treat needs-human as a terminal state, so
a needs-human claim can be re-evaluated if scripts/docstring_gate.py is invoked
again.

But the scheduled safety-net workflow explicitly excludes those claims from its
fresh query:

    fresh=$(gh api -X GET search/issues \
      -f q="repo:${GH_REPO} is:issue is:open -label:bounty-eligible -label:awaiting-merge -label:needs-human docstring" \
      -f per_page=60 --jq '.items[].number' 2>/dev/null || true)

The other scheduled source only selects label:awaiting-merge.

Therefore a docstring claim that is put into needs-human is not selected by
either scheduled query. Unless a human edits/reopens the issue or manually
dispatches the workflow for that exact issue, later gate fixes or transient
condition recovery never reach it.

This recreates the historical stranded-claim pattern that
pr_review_gate_backfill.py was added to fix for review claims, but the
docstring scheduled sweep still has the exclusion.

## Concrete path

1. A valid docstring claim is opened.
2. At adjudication time, a transient/ambiguous condition causes
   scripts/docstring_gate.py to apply needs-human and return normally.
3. The transient condition later clears, or gate logic is fixed.
4. Every 3-hour scheduled run executes.
5. The held query ignores the claim because it lacks awaiting-merge.
6. The fresh query ignores it because of -label:needs-human.
7. The schedule stays green while the claim is never reconsidered.

The expected effect of the scheduled safety net — revisiting unresolved claims
after conditions change — does not happen for this class of unresolved claim.

## Impact

A claim can become permanently stranded in needs-human despite the repository
having a periodic backfill specifically to prevent missed adjudications.
Contributors then require manual intervention even after the original blocker
is gone.

This is not the same as the already reported weekly-cap comment spam (#16711)
or payable-label write failure (#16662). It is a queue-selection gap in the
scheduled workflow.

## Suggested fix

Add needs-human claims as an explicit retry lane, for example:

    human=$(gh api -X GET search/issues \
      -f q="repo:${GH_REPO} is:issue is:open label:needs-human docstring" \
      -f per_page=60 --jq '.items[].number')

Then union human with held/fresh and invoke the gate in retry mode, or remove the
-label:needs-human exclusion if the script is already safe/idempotent for
re-evaluation.

To avoid notification spam, the gate can stay quiet when the verdict remains
needs-human and only comment if the outcome improves.

Add a regression test where a claim starts needs-human, the mocked ambiguity is
removed, and the scheduled selector must feed that issue back into the gate.

## Duplicate check

Public searches for:
- needs-human docstring scheduled
- docstring stranded needs-human
- fresh -label:needs-human

returned #16471 itself and no issue describing this retry-selection gap.

No production state, payment endpoint, key, or wallet operation was used.
