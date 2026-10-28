# retro-windows-ui

A portable Agent Skill for designing, building, retrofitting, and reviewing retro Windows interfaces. It combines era-specific design guidance with original offline assets, semantic tokens, an interactive gallery, and opt-in UI sound effects.

## Themes

- **Windows Classic** — Windows 95/98/2000 visual grammar, hard bevels, dense desktop controls.
- **XP Luna** — blue, olive, and silver variants with shared Luna geometry.
- **Windows 7** — Aero glass and an opaque Basic treatment.

The skill keeps these eras distinct. It does not bundle Microsoft fonts, logos, extracted icons, wallpapers, or system sounds, and it is not affiliated with or endorsed by Microsoft.

## Repository layout

```text
skills/retro-windows-ui/   Portable runtime skill
  SKILL.md                 Trigger, workflow, and resource routing
  references/              Era, behavior, accessibility, and source guidance
  assets/                  Tokens, original SVG/WAV media, starter, and gallery
  scripts/                 Offline catalog and asset validation
evals/                     Agent behavior evaluation scenarios
tests/                     Deterministic repository tests
tools/                     Asset generation, packaging, and browser QA
```

## Use the skill

Install the unchanged `skills/retro-windows-ui` directory in the desired agent skills folder:

- Qoder project: `.qoder/skills/retro-windows-ui/`
- Qoder user: `~/.qoder/skills/retro-windows-ui/`
- Claude Code project: `.claude/skills/retro-windows-ui/`
- Claude Code user: `~/.claude/skills/retro-windows-ui/`

In Qoder, run `/skills reload`, verify with `/skills list`, and invoke `/retro-windows-ui` or ask naturally, for example:

> Build an accessible XP Luna file-transfer dialog with progress, cancel, and error states.

The runtime is offline and framework-free. Open `skills/retro-windows-ui/assets/starter/index.html` or `assets/gallery/index.html` directly, or serve the assets directory with any static server.

## Catalog and validation

Run from any working directory, substituting the path to the installed skill:

```bash
python skills/retro-windows-ui/scripts/catalog.py themes
python skills/retro-windows-ui/scripts/catalog.py show xp-luna-blue --json
python skills/retro-windows-ui/scripts/catalog.py assets --kind audio
python skills/retro-windows-ui/scripts/validate_assets.py
```

Scripts resolve their own resources relative to `SKILL.md`; they do not depend on the caller's working directory or network access.

## Build and package

Python 3.10 or later is sufficient for generation, validation, tests, and packaging:

```bash
python tools/build_assets.py
python tools/build_assets.py --check
python -m unittest discover -s tests -v
python tools/package_skill.py
```

The release is written to `dist/retro-windows-ui.skill`. It is a deterministic ZIP archive with one top-level `retro-windows-ui/` directory and no development tests, evals, caches, or installation copies.

## Browser QA

Create a development environment and install the pinned browser dependency:

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
.venv/Scripts/python -m playwright install chromium
.venv/Scripts/python tools/browser_qa.py
```

On POSIX shells, use `.venv/bin/python`. Screenshots and results are written to the ignored `artifacts/` directory. Browser QA checks all themes, keyboard interactions, reduced modes, local resources, and opt-in audio behavior.

## Asset and sound policy

All bundled visual and audio assets are original and covered by `assets/LICENSE.txt`. `assets/manifest.json` records provenance, licensing, dimensions or audio metadata, byte size, and SHA-256. Unknown-provenance material is not shippable.

Sound is muted until explicit user opt-in. Every cue has visible feedback, and mute/volume controls persist when storage is available. CRT, boot, and similar nostalgia effects are not part of the authentic default interface.

## License

Repository code and documentation are MIT licensed. Original bundled assets are CC0-1.0; see `skills/retro-windows-ui/assets/LICENSE.txt`. Historical source documents remain linked references under their respective terms.
