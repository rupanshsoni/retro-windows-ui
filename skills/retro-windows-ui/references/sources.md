# Sources and evidence quality

Use this bibliography for provenance audits, not as routine implementation context. Sources were reviewed on 2026-10-28. Historical names and documents belong to their respective owners. For a user-requested fan recreation, reference media may be copied into the user's local project with provenance; do not redistribute it commercially.

## User-supplied starting points

| Source | Evidence class | What it informs |
|---|---|---|
| [MitchIvin XP](https://mitchivin.com/) and [repository](https://github.com/mitchivin/MitchIvin-XP) | Community implementation | Browser windowing, applications, session restoration, nostalgic presentation, and integration test ideas. Not an authoritative visual specification. |
| [Microsoft Windows XP Visual Guidelines, 2001](http://interface.free.fr/Archives/GUI_Xp.pdf) | Microsoft pre-release guide | Tahoma UI, Trebuchet caption treatment, 75×23 px command buttons, sample colors, icon sizes/lighting, Start/taskbar behavior, and theme-aware fallback. Its in-development disclaimer means shipped XP wins where they differ. |
| [Show HN: I recreated Windows XP as my portfolio](https://news.ycombinator.com/item?id=45154609) | Community discussion | Review hypotheses for capitalization, balloons, scrollbars, gradients, taskbar behavior, boot/login skipping, and era mismatches. Commenter corrections are not Microsoft documentation. |

## Microsoft guidance

- [Win32 UX guidelines](https://learn.microsoft.com/en-us/windows/win32/uxguide/guidelines): hub for historical Windows desktop guidance.
- [Fonts](https://learn.microsoft.com/en-us/windows/win32/uxguide/vis-fonts): `MS Shell Dlg` mappings, XP/2000 Tahoma, Vista/7 9 pt Segoe UI, main-instruction and link roles.
- [Layout](https://learn.microsoft.com/en-us/windows/win32/uxguide/vis-layout): Windows 7-era control measurements, 11 px dialog margins, 5/7/11 px spacing, scaling and localization.
- [Window Management](https://learn.microsoft.com/en-us/windows/win32/uxguide/win-window-mgt): ownership, placement, activation, Z-order, persistence, and restoration.
- [Taskbar](https://learn.microsoft.com/en-us/windows/win32/uxguide/winenv-taskbar): Windows 7 pinning, Jump Lists, thumbnails, overlays, progress, and attention behavior.
- [XP shell visual styles](https://learn.microsoft.com/en-us/archive/msdn-magazine/2001/november/new-graphical-interface-enhance-your-programs-with-new-windows-xp-shell-features): themed non-client/control drawing, hot states, and alpha transparency.
- [Aero Glass and DWM](https://learn.microsoft.com/en-us/archive/msdn-magazine/2007/april/aero-glass-create-special-effects-with-the-desktop-window-manager): composited glass, actual desktop blending, user-controlled color/opacity, and Basic fallback.
- [Graphic Elements](https://learn.microsoft.com/en-us/windows/win32/uxguide/vis-graphic): limited strategic glass, contrast across gradients/backdrops, and restrained shadows.
- [Animations and Transitions](https://learn.microsoft.com/en-us/windows/win32/uxguide/vis-animations): responsive feedback, restrained durations, and system animation preferences.
- [Icons](https://learn.microsoft.com/en-us/windows/win32/uxguide/vis-icons): Vista/7 sizes, small-icon simplification, perspective, and lighting.
- [Sound](https://learn.microsoft.com/en-us/windows/win32/uxguide/vis-sound): supplemental meaningful cues, restrained repetition/duration, and PCM WAV guidance.
- [Color](https://learn.microsoft.com/en-us/windows/win32/uxguide/vis-color) and [Accessibility](https://learn.microsoft.com/en-us/windows/win32/uxguide/inter-accessibility): semantic system colors, high contrast, keyboard/programmatic access, and non-color cues.
- [Font redistribution FAQ](https://learn.microsoft.com/en-us/typography/fonts/font-faq): local CSS font-name references versus restrictions on copying/converting/hosting Windows font files.
- [Use of Microsoft Copyrighted Content](https://www.microsoft.com/en-us/legal/intellectualproperty/copyright/permissions): permission framework; do not infer that OS media is freely redistributable.
- [The Windows Interface Guidelines for Software Design, 1995](https://www.ics.uci.edu/~kobsa/courses/ICS104/course-notes/Microsoft_WindowsGuidelines.pdf): Classic interaction/design principles; preliminary historical source, not a source for invented exact web metrics.

## Community implementation comparisons

- [98.css](https://github.com/jdan/98.css) and [documentation](https://jdan.github.io/98.css/): semantic HTML/CSS and Classic bevel constructions.
- [XP.css](https://github.com/botoxparty/XP.css) and [documentation](https://botoxparty.github.io/XP.css/): MIT-licensed Luna components and authentic-looking window control sprites, gradients, and metrics.
- [7.css](https://github.com/khang-nd/7.css) and [documentation](https://khang-nd.github.io/7.css/): practical Windows 7/Aero web approximations.

These are comparison targets, not official specifications. For a requested fidelity recreation, code and assets may be copied into the user's project with source/provenance records; MIT code licenses do not establish rights to Microsoft-derived imagery or fonts. The skill itself does not vendor third-party files.

## Boot, welcome, and loading references

Reviewed 2026-10-28 for composition, layout, and asset sourcing. For a user-requested Windows recreation, the supplied source repositories can provide boot images, wallpaper, Start button art, icons, and control sprites. Those Microsoft-derived assets remain Microsoft's; copy them locally only for the user's fan project and record the source and rights note in CREDITS.

- [win32.run](https://win32.run/): BIOS-style text, boot-device menu, and a blue XP "Welcome" phase before the desktop; useful for skippable simulation patterns, not for fake hardware claims.
- [WinXP in React](https://winxp.vercel.app/): direct-to-desktop XP Explorer recreation; demonstrates that a loader is optional.
- [98.js.org](https://98.js.org/): direct-to-desktop Classic shell; useful for desktop grammar without a boot sequence.
- [win98.si](https://win98.si/): raised landing window, ASCII pixel mark, explicit "Start Windows 98" button, and a replayable welcome window with "show this screen every time".
- [Win7 Simu](https://win7simu.visnalize.com/): black "Starting Windows" stage followed by a login surface; useful for era-specific loading tone.
- [PCjs Windows 95](https://www.pcjs.org/blog/2015/09/21/): genuine emulated boot; illustrates why a real emulator can justify a long boot and a portfolio cannot.
- [Windows 92](https://windows92.com/): monochrome fake-BIOS gate with a "press any key" start; useful for stylized theater, not to be presented as real diagnostics.
- [ShizukuIchi/winXP](https://github.com/ShizukuIchi/winXP): MIT-licensed React recreation with Microsoft-derived icons and sounds; useful for layout, interaction, and asset comparison. Attribute the repository and Microsoft rights.
- [ducbao414/win32.run](https://github.com/ducbao414/win32.run): MIT-licensed XP recreation with the complete asset set used for this portfolio — Bliss, XP boot logo, Microsoft logo, Start button sprite, shell icons, wallpapers, and audio. Source URL and Microsoft rights belong in CREDITS. This is the primary asset reference for a full XP clone.
- [XP.css](https://github.com/botoxparty/XP.css): MIT-licensed CSS framework with authentic Luna close/minimize/maximize/restore button SVGs, gradients, and control metrics.

See [boot-loading.md](boot-loading.md) for the implementation rules derived from these references.

## Accessibility and safer assets

- [WCAG text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) and [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html): modern web quality floor alongside period behavior.
- [Selawik](https://learn.microsoft.com/en-us/typography/font-list/selawik): Microsoft's open Segoe UI alternative when a redistributable fallback is actually needed; not a pixel-perfect replacement.
- [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds): example of explicitly licensed third-party UI audio. This repository instead ships original synthesized cues with per-asset provenance.

## Skill structure references

- [Agent Skills specification](https://agentskills.io/specification): portable anatomy and progressive disclosure.
- [Anthropic skills](https://github.com/anthropics/skills): concise entry points, selective resources, black-box scripts, and iterative evaluation.
- [Superpowers writing-skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md) and [porting guidance](https://github.com/obra/superpowers/blob/main/docs/porting-to-a-new-harness.md): trigger-focused descriptions, portable skill content, and behavior evaluation.
- [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) and [Impeccable](https://github.com/pbakaus/impeccable): searchable catalogs, portable path tests, and rendered-output quality gates.

## Confidence rules

1. Label exact Microsoft-documented values with their era and source.
2. Label community CSS values and reconstruction metrics as practical approximations.
3. Treat memories and HN comments as hypotheses until verified against evidence.
4. Do not claim pixel-perfect fidelity when local font rasterization or composited glass differs.
5. For an exact Microsoft-style recreation requested by the user, use the authentic sourced assets, record provenance and Microsoft rights, and label the result an unofficial fan project. For an original era-inspired build, keep the artwork independent of Microsoft logos and recognizable startup compositions. Never claim official status or infer redistribution permission from an MIT code license.
