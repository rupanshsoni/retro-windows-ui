import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "retro-windows-ui"
SKILL_MD = SKILL / "SKILL.md"


class SkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL_MD.read_text(encoding="utf-8")
        cls.lines = cls.text.splitlines()

    def test_frontmatter_and_name(self):
        self.assertEqual(self.lines[0], "---")
        end = self.lines.index("---", 1)
        fields = {}
        for line in self.lines[1:end]:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
        self.assertEqual(fields.get("name"), "retro-windows-ui")
        self.assertRegex(fields.get("name", ""), r"^[a-z0-9-]+$")
        description = fields.get("description", "")
        self.assertTrue(description)
        self.assertLessEqual(len(description), 1024)
        self.assertNotIn("<", description)
        self.assertNotIn(">", description)

    def test_entrypoint_is_concise_and_has_no_todos(self):
        self.assertLess(len(self.lines), 500)
        for path in SKILL.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".py", ".json", ".html", ".css", ".js", ".svg"}:
                self.assertNotIn("TODO:", path.read_text(encoding="utf-8"), str(path))

    def test_local_markdown_links_resolve(self):
        pattern = re.compile(r"\[[^]]*\]\(([^)]+)\)")
        for markdown in SKILL.rglob("*.md"):
            text = markdown.read_text(encoding="utf-8")
            for target in pattern.findall(text):
                target = target.split("#", 1)[0].strip()
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                resolved = (markdown.parent / target).resolve()
                self.assertTrue(resolved.exists(), f"Broken link in {markdown}: {target}")

    def test_runtime_has_no_absolute_workspace_paths(self):
        for path in SKILL.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".py", ".json", ".html", ".css", ".js", ".svg"}:
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("D:\\PROJECT_LARP", text, str(path))
                self.assertNotIn("D:/PROJECT_LARP", text, str(path))
                self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", text, str(path))


if __name__ == "__main__":
    unittest.main()
