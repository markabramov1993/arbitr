# Git Changelog Generator

A dependency-free Python tool that generates a structured `CHANGELOG.md` from git history.

It reads commits **after the latest git tag**, categorizes them into `Added`, `Fixed`, `Changed`, and `Removed`, then writes a Keep-a-Changelog-style Markdown file.

## Install and run

1. Copy `changelog.py` into any git repository.
2. Run `python3 changelog.py`.
3. Commit the generated `CHANGELOG.md`.

Optional flags:

```bash
python3 changelog.py --title v1.4.0 --output CHANGELOG.md
python3 changelog.py --repo /path/to/repo --output /tmp/CHANGELOG.md
```

## Categorization

Conventional Commit prefixes are recognized first:

- `feat:` → Added
- `fix:` → Fixed
- `refactor:`, `docs:`, `test:`, `ci:`, `chore:` → Changed
- `remove:`, `delete:`, `deprecate:` → Removed

Free-form commit subjects are classified with conservative keyword matching. Unknown subjects go to `Changed` rather than being silently dropped.

## Edge cases

- If the repository has no tags, history is read from `HEAD` back to the repository start.
- Empty ranges produce a valid changelog with an explicit no-commits message.
- Commit short SHAs are included for traceability.
- The script never modifies git history or creates tags.

## Test

```bash
python3 -m unittest -v test_changelog.py
```

The tests create temporary real git repositories, including tagged and untagged histories, so no network access is required.

## Real-repository proof

`SAMPLE_CHANGELOG.md` is generated from the public `markabramov1993/arbitr` repository. A GitHub Actions proof workflow also runs the unit tests and regenerates a sample changelog from that real repository on every relevant change.
