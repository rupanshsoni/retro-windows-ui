# Authentic asset sourcing

## 1. Why the bundled runtime uses originals

The public skill is a CC0-1.0 package. It cannot redistribute Microsoft-owned fonts, logos, extracted shell icons, wallpapers, boot screens, or system sounds. That is a **redistribution-rights** constraint, not a fidelity preference and not a fear of looking too close.

The bundled runtime therefore ships:

- a complete original 30-icon shell family for every theme;
- original wallpapers, start marks, textures, window glyphs, and startup screens;
- installed-font stacks rather than font files.

Those assets are enough to build a complete portfolio with authentic **era grammar**. They are not Microsoft's artwork and must not be described as official.

## 2. Three fidelity levels

| Level | What it uses | Where it is appropriate |
|---|---|---|
| Original | Bundled CC0 assets only | Public skills, open-source examples, commercial work that must be clean |
| Hybrid | Bundled geometry plus user-supplied brand/project artwork | Most portfolios; strongest default |
| Authentic recreation | User-supplied Microsoft-derived wallpaper, icons, logo, boot art, and sounds | Private fan projects or builds with permission; the portfolio in this workspace is this level |

For a documented Microsoft recreation, the skill instructions still require full fidelity: do not redraw the flag, do not approximate the Start button, and do not substitute an "inspired" wallpaper. Use the user's supplied reference assets exactly. Label the result an unofficial fan recreation and keep the rights record.

## 3. Where authentic references live

The user's reference implementations are the first source:

| Reference | Useful material |
|---|---|
| [win32.run](https://win32.run/) / `ducbao414/win32.run` | XP boot images, Start button, shell icons, wallpapers, window chrome |
| [WinXP](https://winxp.vercel.app/) / `ShizukuIchi/winXP` | XP icons, boot stages, UI sprites, fonts fallback |
| [98.js](https://98.js.org/) / `1j01/98` | 98 shell icons, wallpapers, boot/welcome grammar |
| [XP.css](https://github.com/botoxparty/XP.css) | XP control and window measurements; CSS reference |
| [Win7 Simu](https://win7simu.visnalize.com/) | Windows 7 boot, orb, taskbar, Aero behavior |
| [PCjs Windows 95](https://www.pcjs.org/blog/2015/09/21/) | 95 boot/splash sequencing and first-run behavior |
| [win98.si](https://win98.si/) | Consentful startup gate and welcome window |
| [Windows 92](https://windows92.com/) | Stylized BIOS/POST theater |

These projects' source licenses do **not** grant rights to Microsoft artwork, fonts, wallpapers, or sounds. Use their code as composition/measurement reference; treat the Microsoft media as Microsoft's.

## 4. Import workflow for a user-supplied project

1. Ask the user for the reference clone or a local asset folder. Do not fetch or hotlink at runtime.
2. Create a project-local `assets/` folder. Never write authentic binaries into the installed public skill runtime.
3. Copy only the files the project actually uses. Prefer the smallest complete set; avoid shipping an entire OS image.
4. Record for each file: the source repository/URL, the source path, the commit or access date, the license of the wrapper project, and a rights note saying the underlying artwork remains Microsoft's.
5. Update `CREDITS.txt` and the project's Read Me. Name the build an unofficial fan recreation and state that it is not affiliated with Microsoft.
6. Use installed fonts. Do not copy `tahoma.ttf`, `trebuchet.ms`, `segoeui.ttf`, or other Microsoft font files into the project.
7. Verify every asset path at 320 px, 1024 px, 200% text, forced colors, and reduced motion.
8. If the project is public, re-check distribution rights before pushing. When in doubt, keep the authentic assets local and ship the original set.

The bundled importer performs steps 2–5 for a curated local folder:

```bash
python scripts/import_reference_assets.py \
  --source /path/to/local/reference \
  --target /path/to/project/assets/reference \
  --label "win32.run reference, accessed 2026-10-29"
```

It copies only common image/audio formats, refuses symlinks, caps individual files at 80 MiB, skips font files, refuses to write inside the public skill runtime, and writes an `IMPORTED-CREDITS.txt` with SHA-256 hashes and the rights warning. It never downloads anything.

Example layout:

```text
assets/
  xp/
    boot/loading.jpg
    boot/ms-logo.jpg
    brand/logo-horizontal.png
    icons/MyComputer.png
    icons/RecycleBin.png
    wallpapers/Bliss.jpg
    ui/start-button.png
  win7/
    boot/starting-flag.png
    icons/start-orb.png
    wallpapers/harmony.jpg
  audio/
    startup-xp.mp3
  CREDITS.txt
```

## 5. Source-to-role map

| Runtime role | Authentic source | Bundled fallback |
|---|---|---|
| Wallpaper | Reference build's `wallpapers/` | `assets/wallpapers/{theme}.svg` |
| Shell icons | Reference build's `icons/` (16/32/48 px variants) | `assets/icons/{theme}/` |
| Start button / orb | Reference build's Start sprite | `assets/brand/{theme}-start.svg` |
| Brand/boot mark | Reference build's boot logo | `assets/brand/{theme}-mark.svg` |
| Window buttons | Reference build's caption sprites | `assets/decorations/{theme}/` |
| Boot stages | Reference build's boot images | `assets/boot/` |
| System sounds | User's licensed/owned audio | Original `assets/audio/*.wav` cues |
| Fonts | Installed stack only | No font files |

## 6. Public repository rule

Do not put Microsoft binaries in a public skill repository, including "just the icons" or "just the wallpaper". A public repo redistributes them. If the user asks for a public authentic clone, explain the rights issue, keep the original asset set as the shippable default, and let the user supply their own local media at build time.

## 7. Fidelity review

For an authentic recreation, inspect the rendered result side by side with the reference at the same viewport:

- wallpaper crop, brightness, and desktop icon shadow;
- boot logo size/position, loader pitch, copyright band, and stage timing;
- Start button proportions and menu header height;
- titlebar height, caption button spacing, inactive titlebar color;
- icon scale at 16/32/48 px and taskbar/titlebar variants;
- menu selection, focus, disabled, pressed, and checked states;
- taskbar height, clock/tray alignment, quick-launch spacing;
- typography: installed era font, size, weight, and antialiasing;
- sound: opt-in only, with visible feedback and mute/volume persistence.

Record what was inspected. If you cannot render the target browser, say so rather than claiming visual verification.
