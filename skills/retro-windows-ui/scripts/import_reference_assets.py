#!/usr/bin/env python3
"""Copy user-supplied reference artwork into a project-local asset folder.

This script never downloads anything and never writes into the installed skill
runtime. Point it at a reference directory the user cloned or downloaded, and
it copies only raster/vector artwork and audio into the project. Font files are
skipped: use installed era fonts instead of redistributing Microsoft fonts.

Microsoft artwork remains Microsoft's. The generated credits file records the
source label, each copied path, its SHA-256, and the rights warning so the
project can keep an honest provenance trail.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_ASSETS = SKILL_DIR / "assets"
ALLOWED_SUFFIXES = {
    ".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".ico",
    ".wav", ".mp3", ".ogg", ".flac", ".m4a",
}
SKIPPED_SUFFIXES = {".ttf", ".otf", ".woff", ".woff2", ".eot"}
MAX_FILE_BYTES = 80 * 1024 * 1024


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def collect(source: Path, target: Path):
    copied = []
    skipped = []
    for path in sorted(source.rglob("*"), key=lambda item: item.as_posix()):
        if not path.is_file() or path.is_symlink():
            continue
        suffix = path.suffix.lower()
        if path.name.startswith("."):
            continue
        if suffix in SKIPPED_SUFFIXES:
            skipped.append((path, "font files are not redistributed; use installed fonts"))
            continue
        if suffix not in ALLOWED_SUFFIXES:
            skipped.append((path, "unsupported file type"))
            continue
        if path.stat().st_size > MAX_FILE_BYTES:
            skipped.append((path, "larger than 80 MiB"))
            continue
        relative = path.relative_to(source)
        destination = (target / relative).resolve()
        if not inside(destination, target):
            skipped.append((path, "path escapes target"))
            continue
        copied.append((path, destination, digest(path)))
    return copied, skipped


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="local folder containing user-supplied reference assets")
    parser.add_argument("--target", type=Path, required=True, help="project-local folder to receive the assets")
    parser.add_argument("--label", default="user-supplied local reference", help="human-readable source label for the credits file")
    parser.add_argument("--dry-run", action="store_true", help="list what would be copied without writing")
    args = parser.parse_args()

    source = args.source.resolve()
    target = args.target.resolve()
    if not source.is_dir():
        print(f"Source is not a directory: {source}", file=sys.stderr)
        return 1
    if inside(target, SKILL_ASSETS) or target == SKILL_ASSETS:
        print("Refusing to copy authentic media into the public skill runtime. Choose a project-local folder instead.", file=sys.stderr)
        return 1

    copied, skipped = collect(source, target)
    print(f"Source: {source}")
    print(f"Target: {target}")
    print(f"Copy: {len(copied)} file(s); skip: {len(skipped)} file(s)")
    for path, destination, sha in copied:
        print(f"  {'[dry-run] ' if args.dry_run else ''}{path.relative_to(source)} -> {destination} ({sha[:12]}…)")
    for path, reason in skipped:
        print(f"  skip {path.relative_to(source)}: {reason}")

    if args.dry_run:
        return 0
    if not copied:
        print("Nothing to copy.")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    lines = [
        "Imported reference assets",
        "========================",
        f"Source label: {args.label}",
        f"Source path: {source}",
        "",
        "These files are user-supplied reference assets. Microsoft artwork, fonts,",
        "wallpapers, icons, boot screens, and sounds remain the property of their",
        "respective owners. This import does not grant a license to redistribute",
        "them. Label the build an unofficial fan recreation and keep this record",
        "with the project. Do not commit this folder to a public repository unless",
        "you have the rights to redistribute every file.",
        "",
        "Files:",
    ]
    for path, destination, sha in copied:
        relative = destination.relative_to(target).as_posix()
        lines.append(f"- {relative}  sha256={sha}")
    (target / "IMPORTED-CREDITS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    for path, destination, _ in copied:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    print(f"Wrote {target / 'IMPORTED-CREDITS.txt'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
