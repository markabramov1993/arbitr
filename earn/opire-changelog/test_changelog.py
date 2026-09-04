import tempfile
import unittest
from pathlib import Path

import changelog


class ChangelogTests(unittest.TestCase):
    def make_repo(self) -> Path:
        root = Path(tempfile.mkdtemp())
        changelog.git("init", cwd=root)
        changelog.git("config", "user.email", "test@example.com", cwd=root)
        changelog.git("config", "user.name", "Test User", cwd=root)
        (root / "file.txt").write_text("one\n", encoding="utf-8")
        changelog.git("add", ".", cwd=root)
        changelog.git("commit", "-m", "feat: initial feature", cwd=root)
        return root

    def commit(self, repo: Path, message: str, text: str) -> None:
        (repo / "file.txt").write_text(text, encoding="utf-8")
        changelog.git("add", ".", cwd=repo)
        changelog.git("commit", "-m", message, cwd=repo)

    def test_category_mapping(self):
        self.assertEqual(changelog.category_for("feat: add API"), "Added")
        self.assertEqual(changelog.category_for("fix(parser): handle empty input"), "Fixed")
        self.assertEqual(changelog.category_for("refactor: simplify cache"), "Changed")
        self.assertEqual(changelog.category_for("remove: legacy flag"), "Removed")
        self.assertEqual(changelog.category_for("misc maintenance"), "Changed")

    def test_commits_since_latest_tag(self):
        repo = self.make_repo()
        changelog.git("tag", "v1.0.0", cwd=repo)
        self.commit(repo, "fix: repair parser", "two\n")
        self.commit(repo, "docs: refresh usage", "three\n")
        commits = changelog.commits_since(changelog.latest_tag(repo), repo)
        self.assertEqual(len(commits), 2)
        subjects = [c.subject for c in commits]
        self.assertIn("fix: repair parser", subjects)
        self.assertNotIn("feat: initial feature", subjects)

    def test_no_tag_uses_full_history(self):
        repo = self.make_repo()
        self.commit(repo, "remove: stale option", "two\n")
        self.assertIsNone(changelog.latest_tag(repo))
        commits = changelog.commits_since(None, repo)
        self.assertEqual(len(commits), 2)

    def test_render_has_required_sections(self):
        commits = [
            changelog.Commit("abc1234", "feat: add export"),
            changelog.Commit("def5678", "fix: repair crash"),
            changelog.Commit("aaa1111", "docs: update setup"),
            changelog.Commit("bbb2222", "remove: old command"),
        ]
        text = changelog.render(commits, "v1.0.0", "Unreleased")
        for heading in ("### Added", "### Fixed", "### Changed", "### Removed"):
            self.assertIn(heading, text)
        self.assertIn("`abc1234`", text)
        self.assertIn("after `v1.0.0`", text)


if __name__ == "__main__":
    unittest.main()
