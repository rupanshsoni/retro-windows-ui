#!/usr/bin/env python3
import argparse
import hashlib
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "retro-windows-ui"
SKILL_DIR = ROOT / "skills" / SKILL_NAME
EXCLUDED_PARTS = {"__pycache__", "evals", "node_modules"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def payload_files():
    if not (SKILL_DIR / "SKILL.md").is_file():
        raise ValueError(f"Missing {SKILL_DIR / 'SKILL.md'}")
    files = []
    for path in sorted(SKILL_DIR.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(SKILL_DIR)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if path.suffix in EXCLUDED_SUFFIXES or path.name == ".DS_Store":
            continue
        if path.is_symlink():
            raise ValueError(f"Symlinks are not supported: {relative}")
        files.append((path, PurePosixPath(SKILL_NAME, *relative.parts)))
    if not files:
        raise ValueError("Skill payload is empty")
    return files


def build_archive(output):
    files = payload_files()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, destination in files:
            info = zipfile.ZipInfo(str(destination), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())
    return files


def validate_archive(path):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if not names:
            raise ValueError("Archive is empty")
        for name in names:
            pure = PurePosixPath(name)
            if pure.is_absolute() or ".." in pure.parts or pure.parts[0] != SKILL_NAME:
                raise ValueError(f"Unsafe or invalid archive path: {name}")
        if f"{SKILL_NAME}/SKILL.md" not in names:
            raise ValueError("Archive does not contain SKILL.md")
        if len(names) != len(set(names)):
            raise ValueError("Archive contains duplicate paths")
    return names


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Package the retro-windows-ui skill as a deterministic .skill ZIP.")
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / f"{SKILL_NAME}.skill")
    args = parser.parse_args()
    try:
        output = args.output.resolve()
        files = build_archive(output)
        names = validate_archive(output)
        print(f"Packaged {len(files)} files: {output}")
        print(f"SHA256: {digest(output)}")
        if len(names) != len(files):
            raise ValueError("Archived file count does not match payload")
        return 0
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"Packaging failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
