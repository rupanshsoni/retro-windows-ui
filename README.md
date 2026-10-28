# retro-windows-ui

![Windows XP desktop with authentic Bliss wallpaper, the desktop icon column, and the Settings window under soft scanlines](docs/media/showcase/xp.webp)

A portable Agent Skill for designing, building, retrofitting, and reviewing retro Windows interfaces. It combines era-specific design guidance with complete original offline asset families, semantic tokens, a default Windows desktop mockup, startup-screen examples, an interactive gallery, and opt-in UI sound effects. It follows the open Agent Skills standard, so the same folder runs in Claude Code, Codex, Antigravity, OpenCode, Pi, DeepSeek Harness, and Qoder.

The installable skill is original and offline. The showcase stills in this README come from a separate reference build that uses the portfolio's user-supplied Microsoft artwork; that media is documentation only and is not included in the package.

## Themes

- **Windows Classic** — Windows 95/98/2000 visual grammar, hard bevels, dense desktop controls.
- **XP Luna** — blue, olive, and silver variants with shared Luna geometry.
- **Windows 7** — Aero glass and an opaque Basic treatment.

Each theme is a complete kit, not a color swap:

- 30 original shell icons: computer, documents, folders, recycle bin, network, internet, email, search, settings, control panel, help, run, programs, briefcase, pictures, music, volume, mute, power, log off, user, task manager, AI, code, design, info, and warnings.
- An original 1600×1000 wallpaper, texture, start mark, brand mark, and every window caption glyph.
- Six startup-screen examples: Classic, XP loading and Welcome, and Windows 7; all are skippable and reduced-motion safe.
- A complete [default Windows desktop mockup](skills/retro-windows-ui/assets/desktop/index.html) with desktop icons, My Computer, My Documents, Read Me, Recycle Bin, Start, quick launch, taskbar, modeless windows, and responsive behavior.

## What the runtime does and does not include

The public runtime **does not** bundle Microsoft fonts, logos, extracted shell icons, wallpapers, boot screens, or system sounds. Microsoft-owned media cannot be redistributed in this public CC0 package. That is a rights constraint, not a lower-fidelity design choice: every era still ships the complete geometry, icon family, wallpaper, startup sequence, and behavior needed to build the interface.

The runtime also ships no portfolio template. Its full-shell example is the neutral [default Windows desktop mockup](skills/retro-windows-ui/assets/desktop/index.html); portfolio information architecture is covered as guidance in [references/portfolio-patterns.md](skills/retro-windows-ui/references/portfolio-patterns.md).

For an exact fan recreation, [references/asset-sourcing.md](skills/retro-windows-ui/references/asset-sourcing.md) documents how to import authentic assets from a user-supplied local reference, keep them out of the public package, and record the source and rights. The installable skill remains original and shippable.

## Authentic fidelity showcase

The bundled neutral [desktop mockup](skills/retro-windows-ui/assets/desktop/index.html) remains the complete shell example that ships with the skill. The stills below come from the separate reference build used for this project's portfolio, which swaps in authentic Microsoft themes and wallpapers from the portfolio. They document the target fidelity; no Microsoft media is packaged.

The hero keeps the XP desktop icon column visible. The six-era comparison captures hide desktop icons so the themes stay neutral; soft scanlines are applied throughout.

| Windows 95 · 1995 | Windows 98 · 1998 |
| :---: | :---: |
| [![Windows 95 desktop with authentic wallpaper and Settings window](docs/media/showcase/win95.webp)](docs/media/showcase/win95.webp) | [![Windows 98 desktop with authentic wallpaper and Settings window](docs/media/showcase/win98.webp)](docs/media/showcase/win98.webp) |
| **Windows 2000 · 2000** | **Windows Me · 2000** |
| [![Windows 2000 desktop with authentic wallpaper and Settings window](docs/media/showcase/win2000.webp)](docs/media/showcase/win2000.webp) | [![Windows Me desktop with authentic wallpaper and Settings window](docs/media/showcase/winme.webp)](docs/media/showcase/winme.webp) |
| **Windows XP · 2001** | **Windows 7 · 2009** |
| [![Windows XP desktop with authentic Bliss wallpaper and Settings window](docs/media/showcase/xp-neutral.webp)](docs/media/showcase/xp-neutral.webp) | [![Windows 7 desktop with authentic wallpaper and Settings window](docs/media/showcase/win7.webp)](docs/media/showcase/win7.webp) |

The skill keeps these eras distinct. Its installable runtime does not bundle Microsoft fonts, logos, extracted icons, wallpapers, or system sounds, and it is not affiliated with or endorsed by Microsoft.

## Repository layout

```text
skills/retro-windows-ui/   Portable runtime skill
  SKILL.md                 Trigger, workflow, and resource routing
  references/              Era, behavior, accessibility, portfolio, and sourcing guidance
  assets/                  Tokens, 269 original assets, starter, desktop mockup, boot, gallery
  scripts/                 Offline catalog, reference importer, and asset validation
evals/                     Agent behavior evaluation scenarios
tests/                     Deterministic repository tests
tools/                     Asset generation, packaging, and browser QA
docs/media/                Documentation-only showcase stills and harness icons
```

## Use the skill

The skill follows the open [Agent Skills](https://agentskills.io/specification) layout, so the same `retro-windows-ui/` folder runs unchanged in every harness below.

<p align="center">
  <img src="docs/media/harnesses/claude-code.svg" width="48" height="48" alt="Claude Code">
  <img src="docs/media/harnesses/codex.svg" width="48" height="48" alt="Codex">
  <img src="docs/media/harnesses/antigravity.svg" width="48" height="48" alt="Antigravity">
  <img src="docs/media/harnesses/opencode.svg" width="48" height="48" alt="OpenCode">
  <img src="docs/media/harnesses/pi.svg" width="48" height="48" alt="Pi">
  <img src="docs/media/harnesses/deepseek-harness.svg" width="48" height="48" alt="DeepSeek Harness">
  <img src="docs/media/harnesses/qoder.svg" width="48" height="48" alt="Qoder">
</p>

| Harness | Project install | Personal install |
| --- | --- | --- |
| [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/` | `~/.claude/skills/` |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `.agents/skills/` | `~/.agents/skills/` |
| [Antigravity](https://antigravity.google/docs/skills/) | `.agents/skills/` | `~/.gemini/config/skills/` |
| [OpenCode](https://opencode.ai/docs/skills/) | `.opencode/skills/` | `~/.config/opencode/skills/` |
| [Pi](https://pi.dev/docs/latest/skills) | `.pi/skills/` | `~/.pi/agent/skills/` |
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) | `.dsh/skills/` or `.agents/skills/` | `~/.dsh/skills/` or `~/.agents/skills/` |
| [Qoder](https://docs.qoder.com/extensions/skills) | `.qoder/skills/` | `~/.qoder/skills/` |

Other Agent Skills-compatible harnesses can load the same folder from their own skills root. Codex, Antigravity, OpenCode, Pi, and DeepSeek Harness also read a project `.agents/skills/` root, so one copy there can serve all five.

Clone once and copy the whole `retro-windows-ui` folder into the destination:

```bash
git clone --depth 1 https://github.com/rupanshsoni/retro-windows-ui.git
mkdir -p ~/.claude/skills
cp -R retro-windows-ui/skills/retro-windows-ui ~/.claude/skills/
```

Start a new session after copying if your harness only scans for skills at launch. In Qoder, run `/skills reload` and verify with `/skills list`; in Pi, run `/reload`. Invoke with `/retro-windows-ui` in Claude Code, Antigravity, and Qoder, `/skill:retro-windows-ui` in Pi, `$retro-windows-ui` in Codex, or simply describe the task and let OpenCode or DeepSeek Harness select the skill. For example:

> Build an accessible XP Luna file-transfer dialog with progress, cancel, and error states.

The runtime is offline and framework-free. Open `skills/retro-windows-ui/assets/starter/index.html`, `assets/desktop/index.html`, `assets/boot/index.html`, or `assets/gallery/index.html` directly, or serve the assets directory with any static server.

Suggested prompts that exercise the complete kit:

> Build a default XP Luna desktop mockup with My Computer, a Notepad window, desktop icons, Start menu, taskbar, and a theme switcher. Use only original or user-supplied assets.

> Recreate the Windows 7 startup screen using the skill's boot example as the timing reference, then hand off to a skippable desktop with a Start orb and taskbar.

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

The complete shell set is generated deterministically by `tools/build_assets.py`: 30 icons per theme, nine wallpapers including Classic 95/98/2000 alternates, six start/brand marks, six decoration sets, semantic tokens, and four synthesized cues. No Microsoft binary is bundled.

For a user-supplied authentic reference, copy artwork into a project without touching the public runtime and record its provenance:

```bash
python skills/retro-windows-ui/scripts/import_reference_assets.py \
  --source /path/to/local/reference \
  --target /path/to/project/assets/reference \
  --label "win32.run reference, accessed 2026-10-29"
```

The importer never downloads anything, skips font files, refuses symlinks, and refuses to write inside the installed skill runtime. It writes an `IMPORTED-CREDITS.txt` with SHA-256 hashes and a rights warning; see [asset-sourcing.md](skills/retro-windows-ui/references/asset-sourcing.md).

Sound is muted until explicit user opt-in. Every cue has visible feedback, and mute/volume controls persist when storage is available. CRT, boot, and similar nostalgia effects are not part of the authentic default interface.

## License

Repository code and documentation are MIT licensed. Original bundled assets are CC0-1.0; see `skills/retro-windows-ui/assets/LICENSE.txt`. README showcase stills contain Microsoft-derived reference artwork and are documentation only; they are not part of the installable skill or the CC0 asset license. Harness compatibility icons are adapted from [LobeHub Icons](https://github.com/lobehub/lobe-icons) under MIT; see [attribution](docs/media/harnesses/ATTRIBUTION.md). They remain trademarks of their respective owners, are documentation only, and are excluded from the packaged skill. Historical source documents remain linked references under their respective terms.
