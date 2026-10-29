<h1 align="center">retro-windows-ui</h1>

<p align="center">
  <strong>Faithful retro Windows interfaces, packaged as a portable Agent Skill.</strong><br>
  Windows Classic, XP Luna, and Windows 7 — complete original assets, semantic tokens, and accessible behavior.
</p>

![Windows desktops cycling through XP, 95, 98, 2000, Me, and 7 with each era's Start menu open and default icons](docs/media/showcase/eras.gif)

<p align="center">
  <img src="docs/media/harnesses/claude-code.svg" width="44" height="44" alt="Claude Code">
  <img src="docs/media/harnesses/codex.svg" width="44" height="44" alt="Codex">
  <img src="docs/media/harnesses/antigravity.svg" width="44" height="44" alt="Antigravity">
  <img src="docs/media/harnesses/opencode.svg" width="44" height="44" alt="OpenCode">
  <img src="docs/media/harnesses/pi.svg" width="44" height="44" alt="Pi">
  <img src="docs/media/harnesses/deepseek-harness.svg" width="44" height="44" alt="DeepSeek Harness">
  <img src="docs/media/harnesses/qoder.svg" width="44" height="44" alt="Qoder">
</p>

<p align="center">
  <sub><strong>Works with</strong> Claude Code · Codex · Antigravity · OpenCode · Pi · DeepSeek Harness · Qoder</sub>
</p>

<p align="center">
  <img src="docs/media/badges/classic.svg" height="27" alt="Windows Classic 95, 98, and 2000">
  <img src="docs/media/badges/xp.svg" height="27" alt="XP Luna blue, olive, and silver">
  <img src="docs/media/badges/win7.svg" height="27" alt="Windows 7 Aero and Basic"><br>
  <img src="docs/media/badges/offline.svg" height="27" alt="Offline and framework-free">
  <img src="docs/media/badges/cc0.svg" height="27" alt="Packaged assets under CC0">
  <img src="docs/media/badges/a11y.svg" height="27" alt="Accessible and keyboard-ready">
</p>

<p align="center">
  <sub><a href="#install">Install</a> · <a href="#themes">Themes</a> · <a href="#demo">Demo</a> · <a href="#authentic-fidelity-showcase">Showcase</a> · <a href="#develop-and-validate">Develop</a> · <a href="#license">License</a></sub>
</p>

A portable Agent Skill for designing, building, retrofitting, and reviewing retro Windows interfaces. It combines era-specific design guidance with complete original offline asset families, semantic tokens, a default Windows desktop mockup, startup-screen examples, an interactive gallery, and opt-in UI sound effects.

## Install

The skill follows the open [Agent Skills](https://agentskills.io/specification) layout, so the same `retro-windows-ui/` folder runs unchanged in every harness below.

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

## Themes

Three complete kits, not color swaps:

- <img src="docs/media/badges/swatch-classic.svg" width="16" height="16" align="middle" alt=""> **Windows Classic** — Windows 95/98/2000 visual grammar, hard bevels, dense desktop controls.
- <img src="docs/media/badges/swatch-xp.svg" width="16" height="16" align="middle" alt=""> **XP Luna** — blue, olive, and silver variants with shared Luna geometry.
- <img src="docs/media/badges/swatch-win7.svg" width="16" height="16" align="middle" alt=""> **Windows 7** — Aero glass and an opaque Basic treatment.

Every era includes:

- 30 original shell icons: computer, documents, folders, recycle bin, network, internet, email, search, settings, control panel, help, run, programs, briefcase, pictures, music, volume, mute, power, log off, user, task manager, AI, code, design, info, and warnings.
- An original 1600×1000 wallpaper, texture, start mark, brand mark, and every window caption glyph.
- Six startup-screen examples: Classic, XP loading and Welcome, and Windows 7; all are skippable and reduced-motion safe.
- A complete [default Windows desktop mockup](skills/retro-windows-ui/assets/desktop/index.html) with desktop icons, My Computer, My Documents, Read Me, Recycle Bin, Start, quick launch, taskbar, modeless windows, and responsive behavior.

## Authentic fidelity showcase

The reference stills, animated hero, and Start menu capture come from a docs-only build that uses the portfolio's user-supplied Microsoft artwork; no Microsoft media is packaged. The runtime examples below use only the original bundled assets.

The hero opens each era's official Start menu over the default desktop icons with stronger CRT treatment. The static comparisons hide desktop icons and use lighter scanlines for legibility.

### Demo

<p align="center">
  <a href="docs/media/showcase/demo.mp4">
    <img src="docs/media/showcase/demo-poster.webp" width="960" alt="38-second demo showing a real XP Luna desktop, a copy dialog with progress and error states, three eras of the same markup, the shell icon set, and offline accessibility checks">
  </a>
  <br>
  <sub><a href="docs/media/showcase/demo.mp4">▶ Watch the 38-second demo</a> · real skill pages, not mockups · original chiptune score · 720p MP4</sub>
</p>

| Windows 95 · 1995 | Windows 98 · 1998 |
| :---: | :---: |
| [![Windows 95 desktop with authentic wallpaper and Settings window](docs/media/showcase/win95.webp)](docs/media/showcase/win95.webp) | [![Windows 98 desktop with authentic wallpaper and Settings window](docs/media/showcase/win98.webp)](docs/media/showcase/win98.webp) |
| **Windows 2000 · 2000** | **Windows Me · 2000** |
| [![Windows 2000 desktop with authentic wallpaper and Settings window](docs/media/showcase/win2000.webp)](docs/media/showcase/win2000.webp) | [![Windows Me desktop with authentic wallpaper and Settings window](docs/media/showcase/winme.webp)](docs/media/showcase/winme.webp) |
| **Windows XP · 2001** | **Windows 7 · 2009** |
| [![Windows XP desktop with authentic Bliss wallpaper and Settings window](docs/media/showcase/xp-neutral.webp)](docs/media/showcase/xp-neutral.webp) | [![Windows 7 desktop with authentic wallpaper and Settings window](docs/media/showcase/win7.webp)](docs/media/showcase/win7.webp) |

<p align="center">
  <a href="docs/media/showcase/start-xp.webp"><img src="docs/media/showcase/start-xp.webp" width="470" alt="Windows XP desktop with the official Start menu open showing default programs, places, and the taskbar"></a>
</p>

<p align="center"><sub>XP Luna Start menu with the official two-column layout, default programs and places, and the taskbar.</sub></p>

### Runtime examples

Captured from the packaged `desktop`, `boot`, and `gallery` pages using only original assets.

| Desktop + Start menu | Startup screen | Component gallery |
| :---: | :---: | :---: |
| <a href="docs/media/showcase/runtime-desktop.webp"><img src="docs/media/showcase/runtime-desktop.webp" width="288" alt="Packaged XP desktop with original icons and the Start menu open"></a> | <a href="docs/media/showcase/runtime-startup.webp"><img src="docs/media/showcase/runtime-startup.webp" width="288" alt="Packaged Windows 7 startup screen with an original loader"></a> | <a href="docs/media/showcase/runtime-gallery.webp"><img src="docs/media/showcase/runtime-gallery.webp" width="288" alt="Packaged component gallery showing buttons, fields, and selection states in Windows Classic"></a> |

## Runtime scope

The runtime ships no portfolio template. Its full-shell example is the neutral [default Windows desktop mockup](skills/retro-windows-ui/assets/desktop/index.html); portfolio information architecture is covered as guidance in [references/portfolio-patterns.md](skills/retro-windows-ui/references/portfolio-patterns.md).

For an exact fan recreation, [references/asset-sourcing.md](skills/retro-windows-ui/references/asset-sourcing.md) documents how to import authentic assets from a user-supplied local reference, keep them out of the public package, and record the source and rights. The installable skill remains original and offline; full media terms are in [License](#license).

## Repository layout

The runtime is one self-contained folder; the rest of the repo supports development, testing, and documentation.

```text
skills/retro-windows-ui/   Portable runtime skill
  SKILL.md                 Trigger, workflow, and resource routing
  references/              Era, behavior, accessibility, portfolio, and sourcing guidance
  assets/                  Tokens, 269 original assets, starter, desktop mockup, boot, gallery
  scripts/                 Offline catalog, reference importer, and asset validation
evals/                     Agent behavior evaluation scenarios
tests/                     Deterministic repository tests
tools/                     Asset generation, packaging, and browser QA
docs/media/                Documentation-only stills, harness icons, color badges, and the demo
```

## Develop and validate

Python 3.10 or later is sufficient for generation, validation, tests, and packaging.

### Catalog

Run from any working directory, substituting the path to the installed skill:

```bash
python skills/retro-windows-ui/scripts/catalog.py themes
python skills/retro-windows-ui/scripts/catalog.py show xp-luna-blue --json
python skills/retro-windows-ui/scripts/catalog.py assets --kind audio
python skills/retro-windows-ui/scripts/validate_assets.py
```

Scripts resolve their own resources relative to `SKILL.md`; they do not depend on the caller's working directory or network access.

### Build and package

```bash
python tools/build_assets.py
python tools/build_assets.py --check
python -m unittest discover -s tests -v
python tools/package_skill.py
```

The release is written to `dist/retro-windows-ui.skill`. It is a deterministic ZIP archive with one top-level `retro-windows-ui/` directory and no development tests, evals, caches, or installation copies.

### Browser QA

Create a development environment and install the pinned browser dependency:

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
.venv/Scripts/python -m playwright install chromium
.venv/Scripts/python tools/browser_qa.py
```

On POSIX shells, use `.venv/bin/python`. Screenshots and results are written to the ignored `artifacts/` directory. Browser QA checks all themes, keyboard interactions, reduced modes, local resources, and opt-in audio behavior.

## Asset and sound policy

**Bundled assets.** All bundled visual and audio assets are original and covered by `assets/LICENSE.txt`. `assets/manifest.json` records provenance, licensing, dimensions or audio metadata, byte size, and SHA-256. Unknown-provenance material is not shippable.

**Generated shell set.** `tools/build_assets.py` deterministically produces 30 icons per theme, nine wallpapers including Classic 95/98/2000 alternates, six start/brand marks, six decoration sets, semantic tokens, and four synthesized cues.

**Reference imports.** For a user-supplied authentic reference, copy artwork into a project without touching the public runtime and record its provenance:

```bash
python skills/retro-windows-ui/scripts/import_reference_assets.py \
  --source /path/to/local/reference \
  --target /path/to/project/assets/reference \
  --label "win32.run reference, accessed 2026-10-29"
```

The importer never downloads anything, skips font files, refuses symlinks, and refuses to write inside the installed skill runtime. It writes an `IMPORTED-CREDITS.txt` with SHA-256 hashes and a rights warning; see [asset-sourcing.md](skills/retro-windows-ui/references/asset-sourcing.md).

**Sound.** Sound is muted until explicit user opt-in. Every cue has visible feedback, and mute/volume controls persist when storage is available. CRT, boot, and similar nostalgia effects are not part of the authentic default interface.

## License

- **Code and documentation:** MIT.
- **Original bundled runtime assets:** CC0-1.0; see `skills/retro-windows-ui/assets/LICENSE.txt`.
- **Runtime example screenshots:** original bundled assets, CC0-1.0, documentation only.
- **Reference showcase stills, animated hero, Start menu capture, demo poster, and demo video:** Microsoft-derived reference artwork, documentation only; not part of the installable skill or the CC0 asset license. The package bundles no Microsoft fonts, icons, wallpapers, boot screens, or system sounds.
- **Demo soundtrack and sound design:** original chiptune score and cues, documentation only; not part of the packaged skill.
- **Harness icons:** adapted from [LobeHub Icons](https://github.com/lobehub/lobe-icons) under MIT; see [attribution](docs/media/harnesses/ATTRIBUTION.md). They remain trademarks of their respective owners, are documentation only, and are excluded from the packaged skill.
- **Historical sources:** linked references under their respective terms.

---

<p align="center"><sub>Unofficial fan recreation. Not affiliated with or endorsed by Microsoft.</sub></p>
