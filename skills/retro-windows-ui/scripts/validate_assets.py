#!/usr/bin/env python3
import argparse
import array
import hashlib
import json
import math
import re
import sys
import wave
from pathlib import Path, PurePosixPath

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS = SKILL_DIR / "assets"
TOKENS = ASSETS / "tokens"
HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?$")
REMOTE_RESOURCE = re.compile(
    r"<(?:script|img|audio|video|source|iframe|embed)\b[^>]*\bsrc\s*=\s*[\"']https?://|"
    r"<link\b[^>]*\bhref\s*=\s*[\"']https?://|url\(\s*[\"']?https?://|@import\s+[\"']https?://",
    re.I | re.S,
)
LOCAL_RESOURCE = re.compile(r"(?:src|href)\s*=\s*[\"']([^\"']+)[\"']|url\(\s*[\"']?([^\"')]+)", re.I)


class Validation:
    def __init__(self):
        self.errors = []
        self.checks = 0

    def check(self, condition, message):
        self.checks += 1
        if not condition:
            self.errors.append(message)

    def fail(self, message):
        self.errors.append(message)


def load_json(path, validation):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        validation.fail(f"Cannot read {path.relative_to(SKILL_DIR)}: {error}")
        return None


def schema_type_matches(value, expected):
    types = expected if isinstance(expected, list) else [expected]
    mapping = {
        "object": dict,
        "array": list,
        "string": str,
        "boolean": bool,
        "null": type(None),
    }
    for name in types:
        if name == "number" and isinstance(value, (int, float)) and not isinstance(value, bool):
            return True
        if name == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return True
        if name in mapping and isinstance(value, mapping[name]):
            return True
    return False


def resolve_schema(schema, root):
    reference = schema.get("$ref")
    if not reference or not reference.startswith("#/"):
        return schema
    target = root
    for part in reference[2:].split("/"):
        target = target[part.replace("~1", "/").replace("~0", "~")]
    return target


def validate_schema(value, schema, root, path, validation):
    schema = resolve_schema(schema, root)
    if "type" in schema:
        validation.check(schema_type_matches(value, schema["type"]), f"{path}: expected {schema['type']}")
        if not schema_type_matches(value, schema["type"]):
            return
    if "const" in schema:
        validation.check(value == schema["const"], f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema:
        validation.check(value in schema["enum"], f"{path}: value is not in enum")
    if "minLength" in schema and isinstance(value, str):
        validation.check(len(value) >= schema["minLength"], f"{path}: string is too short")
    if "minProperties" in schema and isinstance(value, dict):
        validation.check(len(value) >= schema["minProperties"], f"{path}: too few properties")
    if "pattern" in schema and isinstance(value, str):
        validation.check(re.search(schema["pattern"], value) is not None, f"{path}: invalid string format")
    if "minimum" in schema and isinstance(value, (int, float)):
        validation.check(value >= schema["minimum"], f"{path}: below minimum")
    if "maximum" in schema and isinstance(value, (int, float)):
        validation.check(value <= schema["maximum"], f"{path}: above maximum")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            validation.check(key in value, f"{path}: missing required key '{key}'")
        for key, child_schema in schema.get("properties", {}).items():
            if key in value:
                validate_schema(value[key], child_schema, root, f"{path}.{key}", validation)
    if isinstance(value, list) and "items" in schema:
        for index, item in enumerate(value):
            validate_schema(item, schema["items"], root, f"{path}[{index}]", validation)


def color_luminance(color):
    values = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in values]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(first, second):
    light, dark = sorted((color_luminance(first), color_luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def check_contrast_pairs(value, validation, path="theme"):
    if isinstance(value, dict):
        foreground = value.get("foreground", value.get("fg"))
        background = value.get("background", value.get("bg"))
        if isinstance(foreground, str) and isinstance(background, str) and HEX_COLOR.match(foreground) and HEX_COLOR.match(background):
            minimum = float(value.get("minimumRatio", value.get("minimum", value.get("min", value.get("ratio", 4.5)))))
            ratio = contrast_ratio(foreground, background)
            validation.check(ratio + 1e-9 >= minimum, f"{path}: contrast {ratio:.2f}:1 is below {minimum}:1")
        for key, child in value.items():
            check_contrast_pairs(child, validation, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            check_contrast_pairs(child, validation, f"{path}[{index}]")


def validate_tokens(validation):
    schema = load_json(TOKENS / "schema.json", validation)
    if schema is None:
        return
    paths = sorted(path for path in TOKENS.glob("*.json") if path.name != "schema.json")
    validation.check(len(paths) == 6, f"Expected 6 theme packs, found {len(paths)}")
    for path in paths:
        data = load_json(path, validation)
        if data is not None:
            validate_schema(data, schema, schema, path.stem, validation)
            check_contrast_pairs(data, validation, path.stem)


def validate_wav(path, validation):
    try:
        with wave.open(str(path), "rb") as audio:
            channels = audio.getnchannels()
            rate = audio.getframerate()
            width = audio.getsampwidth()
            frames = audio.getnframes()
            raw = audio.readframes(frames)
        duration = frames / rate if rate else 0
        validation.check(width == 2, f"{path.name}: expected PCM16")
        validation.check(rate == 44100, f"{path.name}: expected 44100 Hz")
        validation.check(channels in (1, 2), f"{path.name}: expected mono or stereo")
        validation.check(0.03 <= duration <= 2.0, f"{path.name}: duration {duration:.3f}s is outside UI-cue range")
        samples = array.array("h")
        samples.frombytes(raw)
        if sys.byteorder != "little":
            samples.byteswap()
        peak = max((abs(sample) for sample in samples), default=0)
        validation.check(0 < peak < 32767, f"{path.name}: silent or clipped audio")
        validation.check(all(math.isfinite(sample) for sample in samples), f"{path.name}: invalid samples")
    except (OSError, wave.Error) as error:
        validation.fail(f"{path.name}: invalid WAV: {error}")


def manifest_records(manifest):
    return manifest.get("assets", manifest) if isinstance(manifest, dict) else manifest


def validate_manifest(validation):
    manifest = load_json(ASSETS / "manifest.json", validation)
    if manifest is None:
        return
    records = manifest_records(manifest)
    if not isinstance(records, list):
        validation.fail("manifest.json does not contain an assets list")
        return
    seen = set()
    for record in records:
        relative_text = record.get("path", "")
        pure = PurePosixPath(relative_text)
        validation.check(bool(relative_text) and not pure.is_absolute() and ".." not in pure.parts, f"Invalid manifest path: {relative_text}")
        if not relative_text or pure.is_absolute() or ".." in pure.parts:
            continue
        validation.check(relative_text not in seen, f"Duplicate manifest path: {relative_text}")
        seen.add(relative_text)
        path = ASSETS.joinpath(*pure.parts)
        validation.check(path.is_file(), f"Missing manifest asset: {relative_text}")
        if not path.is_file():
            continue
        validation.check(bool(record.get("license")), f"Missing license: {relative_text}")
        validation.check(bool(record.get("source") or record.get("author") or record.get("provenance")), f"Missing provenance: {relative_text}")
        expected_hash = record.get("sha256", "")
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        validation.check(expected_hash == actual_hash, f"SHA256 mismatch: {relative_text}")
        size = record.get("bytes", record.get("sizeBytes", record.get("size")))
        if size is not None:
            validation.check(size == path.stat().st_size, f"Byte-size mismatch: {relative_text}")
    actual = {path.relative_to(ASSETS).as_posix() for path in ASSETS.rglob("*") if path.is_file() and path.name != "manifest.json"}
    for relative in sorted(actual - seen):
        validation.fail(f"Asset missing from manifest: {relative}")
    for relative in sorted(seen - actual):
        validation.fail(f"Manifest entry is not a shippable asset: {relative}")


def validate_resources(validation):
    for path in sorted(ASSETS.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix == ".wav":
            validate_wav(path, validation)
        if path.suffix not in {".html", ".css", ".js", ".svg"}:
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ASSETS).as_posix()
        validation.check(REMOTE_RESOURCE.search(text) is None, f"Remote runtime resource: {relative}")
        if path.suffix == ".js":
            continue
        for match in LOCAL_RESOURCE.finditer(text):
            target = (match.group(1) or match.group(2) or "").strip()
            if not target or target.startswith(("#", "data:", "mailto:", "http://", "https://")):
                continue
            if target.startswith("/"):
                validation.fail(f"Root-relative resource breaks file:// use: {relative}: {target}")
                continue
            target_path = (path.parent / target.split("#", 1)[0].split("?", 1)[0]).resolve()
            validation.check(target_path.exists(), f"Broken local resource: {relative}: {target}")


def main():
    parser = argparse.ArgumentParser(description="Validate retro-windows-ui tokens, local resources, manifest, and WAV assets.")
    args = parser.parse_args()
    validation = Validation()
    validate_tokens(validation)
    validate_manifest(validation)
    validate_resources(validation)
    if validation.errors:
        print(f"Validation failed with {len(validation.errors)} error(s):", file=sys.stderr)
        for error in validation.errors[:50]:
            print(f"- {error}", file=sys.stderr)
        if len(validation.errors) > 50:
            print(f"- ... {len(validation.errors) - 50} more", file=sys.stderr)
        return 1
    print(f"Validated {validation.checks} checks: themes, contrast, manifest, resources, and audio are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
