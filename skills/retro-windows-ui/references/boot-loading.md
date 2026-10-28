# Boot, welcome, and loading screens

Use this guide only when the user explicitly asks for a startup, boot, welcome, or loading sequence. It is an optional presentation layer, not a requirement of any era.

## 1. Boundary and consent

- A requested Windows startup recreation should reproduce the chosen Microsoft startup grammar, not a generic logo fade. For Windows XP that means the black Windows XP loading stage and/or the blue Welcome stage, with the authentic logo lockup and segmented loader from the reference assets.
- Do not add BIOS/POST diagnostics, memory tests, driver logs, or activation prompts unless the brief explicitly asks for them. An XP loading screen is enough; a BIOS gate is a separate recreation.
- The screen is still a fan recreation. Label it in the credits; do not claim to be Microsoft or an actual OS boot.
- Keep real content in the DOM; do not delay it behind a network request or font load. For a requested startup recreation, a short fixed timer is acceptable because it is skippable and the desktop is already rendered underneath.
- Provide a visible **Skip** control from the first frame. Do not trap focus, require a key press, or hide the skip route behind a pointer-only gesture.
- Remember the user's choice. Offer "Show this screen next time" in the screen or a setting, and default to showing the launch screen at most once per session for a portfolio.
- Keep the sequence brief: about 2–3 seconds for a two-phase XP boot/welcome introduction (roughly 1.5 s black loading followed by 0.7–1 s Welcome). Do not replay it on every route change.
- Do not autoplay sound as part of the sequence. If a startup cue is explicitly requested, it is opt-in, licensed, short, and paired with visible feedback.
- Honor `prefers-reduced-motion: reduce`: remove translation, zoom, pulsing, and animated fills. A static welcome screen may remain, or the screen may be skipped immediately.
- Honor forced-colors/high-contrast: keep the mark, title, status, and Skip control visible with system colors. Do not rely on the blue gradient alone to communicate the phase.

## 2. Composition anatomy

A restrained reconstruction needs only these layers:

1. **Stage** — a full-viewport surface that matches the selected era; no app content behind it is required.
2. **Mark** — one original logo or wordmark, centered or left-aligned according to the era. Provide a simplified pixel variant for small sizes.
3. **Title/status** — short, honest text such as "Welcome", "Starting the desk", or "Opening portfolio". Do not fake system status.
4. **Progress** — an indeterminate segmented animation or an honest determinate fill. Never show a percentage that is unrelated to real work.
5. **Skip** — a normal button with a visible label, usable by keyboard and screen reader.
6. **Optional preference** — a checkbox such as "Show this on startup", with a real persisted setting.
7. **Exit** — a brief fade or immediate cut; remove the overlay from the accessibility tree and move focus to the first meaningful heading/control.

Keep the mark and text above the fold at 320 × 568 and at 200% text. Do not create a login field, password box, user tile, or fake account menu unless it maps to a real product feature.

## 3. Era-specific patterns

### Classic 95/98/2000

- A black or DOS-like phase may show a compact logo and a single line such as `Starting Windows 98...` with a block cursor. Keep the type monospace and the palette monochrome.
- A logo splash may use a large pixel mark, a thin horizontal rule, and a marquee-like line at the bottom. Do not include fake hardware inventories by default.
- A "welcome back" window can use the Classic raised frame, a bitmap-like mark, a small menu on the left, and a "show this screen every time" checkbox. This is a good pattern for a desktop-like portfolio because it is clearly a product window rather than a fake OS boot.
- Use a 32 × 32 or 48 × 48 pixel mark; avoid anti-aliased vector logos on a Classic splash.

### XP Luna

- Use the two authentic XP stages when a full startup is requested:
  1. **Black loading stage:** an entirely black viewport, the Microsoft Windows XP logo lockup centered at roughly 400 px wide (571 × 349 source), the thin blue segmented loader about 150 × 20 px with a 2 px light-gray rounded border, "Copyright © Microsoft Corporation" bottom-left, and the Microsoft wordmark bottom-right. Use the reference assets rather than drawing the flag.
  2. **Blue Welcome stage:** #5a7edc base, a 70 px #00309c top bar with the Windows XP horizontal logo, a 2 px orange/blue divider, a large white italic "Welcome" in Trebuchet MS (≈42 px), and a 70 px footer. Cross-fade or cut after about one second.
- Source the authentic art from the supplied win32.run reference: `static/images/xp_loading_logo.jpg`, `static/images/xp_loading_mslogo.jpg`, `static/images/xp_logo_horizontal.png`. Record the source and Microsoft rights in CREDITS.
- Preserve readable text and a visible Skip route. The XP boot has no native Skip; add a small underlined "Skip intro" in the bottom band or use a clearly discoverable Escape shortcut without making it look like a Windows system control.
- Do not invent a login password, user picker, "Loading personal settings" log, or activation prompt unless the portfolio has real accounts. A single-user auto-logon recreation can go straight from Welcome to the desktop.

### Windows 7 Aero/Basic

- The authentic startup impression is a black stage with a small centered four-color orb/mark and "Starting Windows" below it, followed by a calm login/welcome surface.
- Keep glow soft and typography Segoe UI; do not turn it into a neon loading page or add a spinner that belongs to a modern app.
- Do not reuse the XP blue gradient or Classic bevel frame. The era's loading grammar is its own.

## 4. Community references

These are comparison targets for composition, timing, and interaction. Their source code and licenses do not grant rights to Microsoft logos, fonts, wallpapers, icons, or sounds.

| Reference | Observed behavior | Useful lesson |
|---|---|---|
| [win32.run](https://win32.run/) | Award BIOS-style text and boot-device menu; selecting "Start Windows Normally" leads to a blue XP "Welcome" phase, then the desktop. | A boot phase can be theater, but it must be skippable and clearly a simulation. |
| [WinXP in React](https://winxp.vercel.app/) | Opens directly into an Explorer window on a blue XP desktop; green Start surface, beige folder lists, blue captions. | A recreation can skip the boot entirely and still feel authentic. Loader is not required. |
| [98.js.org](https://98.js.org/) | Opens directly on a cloud wallpaper with teal desktop labels and a Classic taskbar. | Preserve the desktop grammar; do not add a loader just because the era had one. |
| [win98.si](https://win98.si/) | Teal landing page with a raised window, ASCII pixel logo, "WELCOME BACK TO THE 2000s", and a "Start Windows 98" button; boot text and a welcome window follow. | A consentful "start" button and a "show this screen every time" checkbox make the intro optional and replayable. |
| [Win7 Simu](https://win7simu.visnalize.com/) | Black "Starting Windows" stage with a centered four-color mark, then a login surface and desktop. | Match the era's own mark scale, spacing, and quiet motion; do not over-animate. |
| [PCjs Windows 95](https://www.pcjs.org/blog/2015/09/21/) | Emulated hardware boot and first-run Windows 95 splash. | Real emulators earn long boot sequences because they are actually booting; a portfolio does not. |
| [Windows 92](https://windows92.com/) | Monochrome "W92 BIOS" text with memory test and a "Press any key or click to start" gate. | If using a fake BIOS, keep it obviously stylized and never present it as real diagnostics. |

## 5. Mark on the loading screen

- For an explicit XP recreation, use the authentic Microsoft Windows XP logo lockup, Microsoft wordmark, and Start button art from the user's reference sources. Do not redraw or approximate the flag.
- For an original era-inspired product, use an original mark and record it. A four-pane composition may evoke the GUI language, but must not be presented as Microsoft's mark.
- A pixelated project logo may be used when the owner supplied it. Follow the logo method in [logo-and-wordmark.md](logo-and-wordmark.md).
- Record the source URL and rights status in the project credits. Keep the mark readable at 32, 64, and 96 px; use integer scaling and `image-rendering: pixelated` for bitmap marks. Do not blur a 16 px mark to fill a 120 px stage.

## 6. Implementation checklist

- Put the overlay in the initial HTML so it appears on first paint and load the authentic logo/boot images locally.
- For XP, reproduce the measured stages: black loading (≈1.5 s), then blue Welcome (≈0.7–1 s), then desktop. Use a CSS cross-fade and a single timer; skippable at any point.
- Hide it in the no-JS path: the static fallback must not be blocked by the overlay. Prefer `<noscript>` CSS that sets `display: none`.
- Read a persisted "skip startup" preference with a tiny synchronous script in the head so the overlay is not flashed when disabled.
- Use a fixed, full-viewport layer above the shell; do not use a modal `<dialog>` for a non-interactive splash. Keep the Skip control and checkbox as normal buttons/inputs.
- Pause or remove decorative animation under reduced motion. Do not use flashing or more than three flashes per second.
- Expose the phase as `role="status"` or a labelled region; do not announce every progress tick.
- On exit, set `hidden`, remove animation, and move focus to the first meaningful heading or control. If the user activated Skip, return focus to the skipped-to content, not a removed button.
- Hide the overlay in print and forced-colors fallback as appropriate.
- Test at 320 × 568, 1024 × 768, 200% text, reduced motion, forced colors, keyboard-only, and with JavaScript disabled.
- Do not add runtime network requests, remote fonts, analytics, or a CDN dependency for the splash. Vendor the reference assets locally.
- Compare the rendered startup to the supplied reference screenshot at the same viewport; check logo size/position, loader pitch, bar heights, copyright, and Microsoft mark placement.
