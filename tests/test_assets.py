import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "retro-windows-ui"
ASSETS = SKILL / "assets"


class AssetTests(unittest.TestCase):
    def test_generated_assets_are_current(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "build_assets.py"), "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_asset_validator(self):
        result = subprocess.run(
            [sys.executable, str(SKILL / "scripts" / "validate_assets.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_manifest_has_provenance_and_integrity_fields(self):
        manifest = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
        records = manifest.get("assets", manifest) if isinstance(manifest, dict) else manifest
        self.assertGreater(len(records), 10)
        for record in records:
            with self.subTest(asset=record.get("path")):
                self.assertIn("path", record)
                self.assertIn("license", record)
                self.assertTrue(record.get("source") or record.get("author") or record.get("provenance"))
                self.assertRegex(record.get("sha256", ""), r"^[0-9a-f]{64}$")
                self.assertTrue((ASSETS / record["path"]).is_file())

    def test_runtime_examples_have_no_remote_resources(self):
        for folder in (ASSETS / "starter", ASSETS / "gallery"):
            for path in folder.iterdir():
                if path.suffix not in {".html", ".css", ".js"}:
                    continue
                text = path.read_text(encoding="utf-8")
                self.assertNotRegex(text, r"(?:src|href)=[\"']https?://")
                self.assertNotRegex(text, r"url\(\s*[\"']?https?://")
                self.assertNotIn("TODO:", text)


if __name__ == "__main__":
    unittest.main()
