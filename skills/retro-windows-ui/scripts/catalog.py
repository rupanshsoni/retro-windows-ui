#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS = SKILL_DIR / "assets"
TOKENS = ASSETS / "tokens"


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot read {path}: {error}") from error


def theme_identity(path, data=None):
    data = data if data is not None else read_json(path)
    identity = data.get("identity", data.get("theme", data))
    return {
        "id": identity.get("id", path.stem),
        "name": identity.get("name", identity.get("label", path.stem)),
        "era": identity.get("era", "unknown"),
        "variant": identity.get("variant", path.stem),
        "tokens": str(path),
    }


def themes():
    return [theme_identity(path) for path in sorted(TOKENS.glob("*.json")) if path.name != "schema.json"]


def find_theme(query):
    normalized = query.casefold().replace("_", "-").replace(" ", "-").strip()
    aliases = {
        "xp": "xp-luna-blue",
        "luna": "xp-luna-blue",
        "xp-blue": "xp-luna-blue",
        "olive": "xp-luna-olive",
        "silver": "xp-luna-silver",
        "aero": "windows-7-aero",
        "basic": "windows-7-basic",
        "windows-classic": "classic",
        "95": "classic",
        "98": "classic",
        "2000": "classic",
    }
    normalized = aliases.get(normalized, normalized)
    matches = [item for item in themes() if item["id"].casefold() == normalized]
    if not matches:
        matches = [item for item in themes() if normalized in item["id"].casefold() or normalized in item["name"].casefold()]
    if len(matches) != 1:
        choices = ", ".join(item["id"] for item in themes())
        raise ValueError(f"Unknown or ambiguous theme '{query}'. Choose: {choices}")
    return matches[0]


def asset_records():
    manifest = read_json(ASSETS / "manifest.json")
    records = manifest.get("assets", manifest) if isinstance(manifest, dict) else manifest
    if not isinstance(records, list):
        raise ValueError("Asset manifest must contain an assets list")
    return records


def emit(data, as_json):
    if as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))
        return
    if isinstance(data, list):
        if not data:
            print("No matching entries")
            return
        for item in data:
            if "tokens" in item:
                print(f"{item['id']}: {item['name']} [{item['era']}/{item['variant']}]\n  {item['tokens']}")
            else:
                print(f"{item.get('path', '(unknown)')} [{item.get('kind', 'asset')}; {item.get('license', 'unspecified')}]")
        return
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
        return
    print(data)


def main():
    parser = argparse.ArgumentParser(description="Query retro Windows themes and cleared bundled assets.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (("eras", "List supported eras"), ("themes", "List available themes"), ("assets", "List manifest-cleared assets")):
        sub = subparsers.add_parser(name, help=help_text)
        sub.add_argument("--json", action="store_true")
        if name == "assets":
            sub.add_argument("--era")
            sub.add_argument("--kind")

    show = subparsers.add_parser("show", help="Inspect one theme's complete token pack")
    show.add_argument("theme")
    show.add_argument("--json", action="store_true")

    path_parser = subparsers.add_parser("path", help="Print one theme's token file path")
    path_parser.add_argument("theme")

    args = parser.parse_args()
    try:
        if args.command == "eras":
            eras = sorted({item["era"] for item in themes()})
            emit(eras if args.json else "\n".join(eras), args.json)
        elif args.command == "themes":
            emit(themes(), args.json)
        elif args.command == "show":
            identity = find_theme(args.theme)
            token_path = Path(identity["tokens"])
            data = read_json(token_path)
            emit(data if args.json else identity, args.json)
        elif args.command == "path":
            print(find_theme(args.theme)["tokens"])
        elif args.command == "assets":
            records = asset_records()
            if args.era:
                records = [item for item in records if str(item.get("era", "")).casefold() == args.era.casefold()]
            if args.kind:
                records = [item for item in records if args.kind.casefold() in str(item.get("kind", "")).casefold()]
            emit(records, args.json)
        return 0
    except ValueError as error:
        print(f"Catalog error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
