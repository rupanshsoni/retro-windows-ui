import hashlib
import importlib.util
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("package_skill", ROOT / "tools" / "package_skill.py")
package_skill = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package_skill)


class PackageTests(unittest.TestCase):
    def test_archive_is_deterministic_and_contains_only_skill(self):
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.skill"
            second = Path(temporary) / "second.skill"
            package_skill.build_archive(first)
            package_skill.build_archive(second)
            self.assertEqual(hashlib.sha256(first.read_bytes()).digest(), hashlib.sha256(second.read_bytes()).digest())
            names = package_skill.validate_archive(first)
            self.assertIn("retro-windows-ui/SKILL.md", names)
            self.assertTrue(all(PurePosixPath(name).parts[0] == "retro-windows-ui" for name in names))
            self.assertFalse(any("/tests/" in name or "/evals/" in name or "__pycache__" in name for name in names))
            with zipfile.ZipFile(first) as archive:
                self.assertTrue(all(info.date_time == (1980, 1, 1, 0, 0, 0) for info in archive.infolist()))

    def test_extracted_archive_runs_from_a_path_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix="retro archive ") as temporary:
            archive_path = Path(temporary) / "release.skill"
            package_skill.build_archive(archive_path)
            install = Path(temporary) / "installed skill"
            with zipfile.ZipFile(archive_path) as archive:
                archive.extractall(install)
            scripts = install / "retro-windows-ui" / "scripts"
            catalog = subprocess.run(
                [sys.executable, str(scripts / "catalog.py"), "themes", "--json"],
                cwd=temporary, text=True, capture_output=True, timeout=30, check=False,
            )
            self.assertEqual(catalog.returncode, 0, catalog.stderr)
            validation = subprocess.run(
                [sys.executable, str(scripts / "validate_assets.py")],
                cwd=temporary, text=True, capture_output=True, timeout=60, check=False,
            )
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)


if __name__ == "__main__":
    unittest.main()
