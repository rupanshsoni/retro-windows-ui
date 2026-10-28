import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "retro-windows-ui"


def run_script(script, *arguments, cwd):
    return subprocess.run(
        [sys.executable, str(script), *arguments],
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )


class PortabilityTests(unittest.TestCase):
    def test_catalog_from_unrelated_working_directory(self):
        with tempfile.TemporaryDirectory(prefix="retro catalog ") as temporary:
            result = run_script(SKILL / "scripts" / "catalog.py", "themes", "--json", cwd=temporary)
            self.assertEqual(result.returncode, 0, result.stderr)
            themes = json.loads(result.stdout)
            self.assertEqual(len(themes), 6)
            self.assertEqual({item["id"] for item in themes}, {
                "classic", "xp-luna-blue", "xp-luna-olive", "xp-luna-silver",
                "windows-7-aero", "windows-7-basic"
            })

    def test_catalog_aliases_resolve_deterministically(self):
        for alias, expected in (("Luna", "xp-luna-blue"), ("Aero", "windows-7-aero"), ("Windows Classic", "classic")):
            with self.subTest(alias=alias):
                result = run_script(SKILL / "scripts" / "catalog.py", "path", alias, cwd=ROOT)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(result.stdout.strip().endswith(f"{expected}.json"))

    def test_copied_project_installation_is_self_contained(self):
        with tempfile.TemporaryDirectory(prefix="retro install ") as temporary:
            destination = Path(temporary) / ".qoder" / "skills" / "retro-windows-ui"
            shutil.copytree(SKILL, destination)
            result = run_script(destination / "scripts" / "catalog.py", "themes", "--json", cwd=temporary)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(json.loads(result.stdout)), 6)
            validation = run_script(destination / "scripts" / "validate_assets.py", cwd=temporary)
            self.assertEqual(validation.returncode, 0, validation.stderr)


if __name__ == "__main__":
    unittest.main()
