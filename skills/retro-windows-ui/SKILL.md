---
name: retro-windows-ui
description: Design, implement, retrofit, and review faithful retro Windows desktop and web interfaces, including Windows Classic 95/98/2000, XP Luna blue/olive/silver, and Windows 7 Aero/Basic; use for retro OS mockups, window managers, taskbars, Start-like launchers, dialogs, controls, icons, pixel logos, wordmarks, boot/loading/welcome screens, themes, CSS tokens, accessibility, or UI authenticity audits.
---

# Retro Windows UI

Build an era-specific interface that remains usable, accessible, and self-contained. Recreate visual grammar, not merely a teal desktop or a nostalgic screenshot.

## Select and load only what applies

1. Identify exactly one target era from the request or existing design evidence:
   - **Windows Classic**: [references/classic.md](references/classic.md), including 95, 98, and 2000 variants.
   - **Windows XP Luna**: [references/xp-luna.md](references/xp-luna.md), including blue, olive, and silver.
   - **Windows 7**: [references/windows-7.md](references/windows-7.md), including Aero and Basic.
2. If the era is genuinely ambiguous, ask for a selection; do not combine candidates as a compromise.
3. Read only the selected era reference. Do not load the other era guides for comparison.
4. For any interactive work, also read [references/behavior-accessibility.md](references/behavior-accessibility.md).
5. For a startup, boot, welcome, or loading screen, also read [references/boot-loading.md](references/boot-loading.md). These screens are opt-in unless the brief explicitly requests a startup recreation; when requested, reproduce the target's real loading/welcome sequence from sourced assets.
6. For logos, wordmarks, project marks, or a pixel icon family, also read [references/logo-and-wordmark.md](references/logo-and-wordmark.md).
7. For customization, design tokens, theme switching, or generated CSS, also read [references/token-schema.md](references/token-schema.md).
8. For a portfolio, résumé, project explorer, domain/role profiles, or a full desktop shell, also read [references/portfolio-patterns.md](references/portfolio-patterns.md).
9. When the brief requires authentic Microsoft media, read [references/asset-sourcing.md](references/asset-sourcing.md). The public runtime ships original stand-ins; authentic files must come from the user's local reference and stay out of the public skill package.
10. Treat [references/sources.md](references/sources.md) as bibliography, not routine implementation context; consult it only for a provenance or citation audit requested by the user.

## Work compactly

1. **Inspect first.** Identify the framework, component boundaries, current assets, input methods, and existing design tokens. Preserve product functionality and information architecture.
2. **Lock the brief.** Record era, variant/color scheme, viewport, required states, and fidelity target. Say explicitly whether this is an exact Microsoft-style recreation or an original era-inspired system. For a recreation, use the user's supplied reference sites as asset and composition sources.
3. **Map semantics before styling.** Inventory windows, captions, menus, controls, taskbar/launcher items, dialogs, selection, focus, and status feedback. Use native HTML controls where possible.
4. **Build foundations.** Apply the selected guide's font stack, semantic palette, spacing rhythm, control metrics, borders, and icon treatment. Keep era values in theme variables rather than component literals.
5. **Compose the shell.** Implement window geometry and active/inactive hierarchy before adding the taskbar, launcher, or wallpaper. Keep app content visually quieter than chrome.
6. **Implement behavior.** Cover default, hover, active/pressed, focus, selected, disabled, checked, expanded, and error states as applicable. Add keyboard operation, focus return, and reduced-motion/transparency behavior.
7. **Inspect the render.** Compare a rendered screen at the target viewport against the selected guide. Inspect both shell and dense app content, active and inactive states, keyboard focus, and text scaling.
8. **Audit and report.** Check era purity, asset licensing, offline operation, contrast, keyboard paths, and responsive behavior. State what was visually inspected; if rendering was unavailable, explicitly state that limitation and name the unverified checks.

Prefer a small set of complete, consistent surfaces over many ornamental features. Retrofit existing components in place rather than replacing the application architecture merely to obtain a look.

## Preserve the invariants

- **Never mix eras.** Do not combine Classic bevels, Luna capsule chrome, and Aero glass. Choose one era and carry its grammar through every surface and state.
- **Do not modernize by default.** Avoid unsolicited rounded cards, pill buttons, floating navigation, glassmorphism, large soft shadows, gradient meshes, emoji icons, icon-only unfamiliar controls, or modern dashboard spacing.
- **Recreate the requested target faithfully.** When the user asks for an exact Microsoft-style interface, match the reference: wallpaper, logo lockups, boot and welcome screens, icon art, Start button and menu proportions, taskbar/titlebar metrics, typography, wording, and control states. Do not substitute a generic "inspired by" theme for the requested clone.
- **Source the authentic assets.** Prefer the user's supplied reference implementations, then official or community asset packs. Save assets locally, record their source URL and rights in CREDITS, and label the result an unofficial fan recreation. Microsoft artwork remains Microsoft's; do not present the build as official or redistribute it commercially without permission. The public skill runtime cannot bundle Microsoft binaries; that is a redistribution constraint, not permission to lower fidelity. Use the bundled original asset families or import the user's local authentic assets.
- **Do not use caution as an excuse for lower fidelity.** If an asset's provenance is unclear, say so and use the assets the user supplied rather than replacing the requested look with a generic approximation. For a public build, use the complete original shell set and state the tradeoff explicitly.
- **Keep runtime local.** Do not add remote fonts, CDN CSS/scripts, hotlinked images, analytics, or network-required runtime dependencies. Use installed-font stacks and relative local assets.
- **Never autoplay sound.** Require explicit opt-in and a user gesture; provide a persistent mute/volume control and visible equivalent feedback.
- **Do not add unrequested framing effects.** Omit CRT curvature, scanlines, glitch, VHS noise, boot/BIOS sequences, fake POST messages, and shutdown theater unless explicitly requested. These are not era UI requirements. When a boot or loading screen is requested, follow [references/boot-loading.md](references/boot-loading.md): keep it short, skippable, honest, and accessible; never present simulated diagnostics as real system state.
- **Do not sacrifice usability for fidelity.** Preserve visible focus, keyboard access, readable scaling, sufficient contrast, reduced-motion support, and meaningful labels.
- **Do not invent official precision.** Label reconstruction metrics and sampled colors as practical approximations unless the selected reference identifies an authoritative source.
- **Be honest about the simulation.** A Start-like launcher, desktop, or taskbar is portfolio navigation, not a real OS. Give simulated shell actions honest accessible names (for example, "Turn Off Computer" may restart the portfolio) and disclose the fan-recreation status in credits.

## Implement with restraint

- Start at a 96-DPI logical-pixel baseline, then test scaling rather than assuming physical pixels.
- Separate semantic intent from raw values: use surface, text, border, selection, caption, focus, and state tokens.
- Use real text instead of text baked into images. Keep icons decorative unless they carry an otherwise unavailable action.
- Make bevel direction and light source consistent. Use shadows to establish window hierarchy, not to decorate every control.
- Keep hover discoverable but never make hover the only way to reveal essential actions.
- Let content determine window size within usable minimums; do not shrink targets or clip labels to force a screenshot metric.
- For an exact Microsoft recreation, use the authentic flag, shell icons, and Start button art from the supplied reference assets and credit them. For an original era-inspired build, use original or credited artwork and keep Microsoft flags and extracted shell art out. In both modes, use one grid, light source, outline, and simplified small variant per family.
- Preserve the host application's responsive behavior. At narrow sizes, reflow launcher and window content rather than introducing an unrelated mobile UI skin.

## Use bundled resources

Resolve every path relative to this `SKILL.md`, not the user's repository root. Run scripts through Python and use `--help` before reading substantial script source:

```bash
python scripts/catalog.py themes
python scripts/catalog.py show xp-luna-blue --json
python scripts/catalog.py assets --kind audio
python scripts/validate_assets.py
```

The scripts need only Python's standard library and work from any current directory. Keep generated files within the user's requested project scope.

For a user-supplied authentic reference, copy artwork into the project (never into the installed skill runtime), skip font files, and record provenance:

```bash
python scripts/import_reference_assets.py --source /path/to/local/reference --target /path/to/project/assets/reference --label "win32.run reference, accessed 2026-10-29"
```

The importer does not download anything and refuses to write inside this skill's `assets/` directory. Read its generated `IMPORTED-CREDITS.txt` and keep the build's rights status explicit.

- Start offline examples from [assets/starter/index.html](assets/starter/index.html).
- Use [assets/desktop/index.html](assets/desktop/index.html) for a default Windows desktop mockup: desktop icons, My Computer, My Documents, Read Me, Recycle Bin, Start, quick launch, taskbar, modeless windows, and a responsive mobile stack.
- Inspect startup screens in [assets/boot/index.html](assets/boot/index.html); they are original, skippable, reduced-motion safe, and not Microsoft boot media.
- Inspect all themes and states in [assets/gallery/index.html](assets/gallery/index.html).
- Select tokens from [assets/tokens/themes.css](assets/tokens/themes.css) or the matching JSON pack. Each theme also resolves a wallpaper, start mark, brand mark, 30-icon shell family, and window glyphs.
- Check [assets/manifest.json](assets/manifest.json) and [assets/LICENSE.txt](assets/LICENSE.txt) before copying assets. The runtime has no Microsoft binaries; for authentic media, follow [references/asset-sourcing.md](references/asset-sourcing.md).

Reference assets with relative paths, never remote URLs. If no suitable asset exists, use CSS geometry, text, or an original simple icon instead of fetching proprietary material.

## Review before delivery

- Confirm one era and one variant throughout, including menus, dialogs, focus, disabled states, and icons.
- Confirm all interactive controls work with keyboard and pointer and expose programmatic names and states.
- Confirm active/inactive windows, modal focus, minimize/restore, and launcher dismissal where those features exist.
- Confirm 200% text scaling, reduced motion, reduced transparency, and offline loading as applicable.
- Confirm no remote dependencies, autoplay audio, or unrequested effects were introduced. For a requested clone, inspect the supplied reference and the rendered result side by side: wallpaper, boot/welcome, Start, taskbar, titlebar, icon scale, fonts, and spacing.
- Confirm the CREDITS file records the source and rights status of every wallpaper, logo, icon set, boot image, font file, and sound.
- For a portfolio, confirm the default role and availability are broad (not tied to one specialty or country), switching a domain profile updates the About lens, project filter, and skills together, and the visitor can return to All projects.
- Report changed files, the selected guide, rendered inspection performed, and any explicit verification limitation.
