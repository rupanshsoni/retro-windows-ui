# Logos, wordmarks, and pixel marks

Use this guide when an interface needs a product mark, project logo, wordmark, or icon family. It supplements the selected era guide; the era still controls chrome, spacing, and typography.

## 1. Fidelity, sourcing, and rights

- For an explicit Microsoft-style recreation, use the authentic Windows flag, boot logo, Start button, shell icons, wallpapers, and brand lockups. Do not redraw them from memory or substitute an "inspired" four-pane shape. Source them from the user's reference implementations or an official archive, save them locally, and record the source URL and rights status in CREDITS.
- Prefer the supplied reference sites and their repositories first: win32.run (`ducbao414/win32.run`), WinXP (`ShizukuIchi/winXP`), 98.js (`1j01/98`), and XP.css (`botoxparty/XP.css`). These provide ready-to-use XP icons, Start button art, boot images, captions, and control sprites.
- Microsoft artwork remains Microsoft's. Label the result an unofficial fan recreation, do not present it as an official Microsoft product, and do not redistribute it commercially without permission. The user's local portfolio can carry the requested assets; record the risk rather than diluting the visual target.
- Project logos may be used when the project owner supplied them. Record the source in the project credits.
- A wordmark set in an installed font is not a font redistribution; embedding or shipping a font file is a separate licensing decision.
- Use the project owner's mark for the portfolio identity, but do not use a third-party project's logo as the portfolio's own brand.

## 2. One visual grammar

Before drawing, lock:

- **Grid:** 16 × 16 for Classic and compact UI; 32 × 32 for XP shell marks; 48 × 48 for XP detail/desktop; 16/32/48/256 for Vista/7 application icons.
- **Light source:** upper-left, every mark in the family. Do not mix top-light and bottom-light marks.
- **Palette:** one brand ink, one shadow tone, one highlight, and a neutral outline. Keep the same palette across sizes.
- **Perspective:** either straight-on or the same isometric angle. Do not alternate between flat and perspective symbols.
- **Outline:** a 1 px dark outline for pixel marks; a crisp 1 px vector edge for larger marks. The outline must survive the desktop background.
- **Silhouette:** the object must be recognizable at its smallest size before detail is added.

A family may contain project marks with different colors. They still share the grid, light source, border weight, and corner/slot geometry.

## 3. Pixel logo method

Use this when turning an existing, licensed brand mark into a period-appropriate pixel icon.

1. Start from the highest-resolution original. Crop to a square around the recognizable mark, not the full lockup with small text.
2. Remove transparent or flat background cleanly. Do not erase parts of the mark to force a silhouette.
3. Reduce to the target grid with an integer-friendly size (12, 16, 24, 28, or 32 px). Use nearest-neighbor for the final pixel pass; use a high-quality resample only before quantization.
4. Limit the palette to roughly 8–16 colors sampled from the original. Keep the brand's dominant hue; do not shift it to a modern neon or gradient.
5. Add a 1 px dark outline or a light rim only if the mark needs separation from the chosen tile. Use the same treatment for every mark in the family.
6. Build a **small variant** separately: remove interior detail, thicken the key stroke, and keep only the silhouette. Do not simply scale the 48 px drawing to 16 px.
7. Export PNG (or an SVG made of integer-aligned rectangles) and display with `image-rendering: pixelated` when scaling. Test at 1×, 2×, and 200% zoom.
8. Inspect the mark on the lightest and darkest surfaces used by the interface. If contrast fails, change the tile or add a stable backing plate; do not recolor the mark arbitrarily.

## 4. Authentic XP shell icon families

- Prefer the real XP icon art from a reference build: 32 × 32 desktop icons, 48 × 48 detail icons, 16 × 16 taskbar/titlebar icons, and the Start button sprite. The win32.run set includes My Computer, My Documents, folders, Recycle Bin, Internet Explorer, Control Panel, Help, email, WordPad, volume, power, and logoff.
- Use the source art at its native aspect ratio. Scale down with a high-quality resampler for 32/24/16 px display; never blur a 100 px icon through a CSS filter to fake a small variant.
- Keep XP's light source and material treatment consistent: glossy blue/green/orange, soft highlights, no added drop shadows beyond the desktop label shadow.
- For an original icon family, a 48 × 48 tile with a compact rounded square, 1 px dark border, narrow inner highlight, and restrained gradient still works. Keep one perspective and radius across the family.
- Provide a 16 × 16 or 24 × 24 variant for lists, titlebars, and taskbar buttons. Do not put unreadable wordmarks inside 16 px icons.
- The XP Start button is a 100 × 30 sprite containing the flag and "start" wordmark. Use it as a single image; do not rebuild it from text and a generic flag.

## 5. Wordmarks

Era-appropriate stacks, using installed fonts only:

```css
/* XP */
font-family: "Trebuchet MS", Tahoma, sans-serif;
font-weight: 700;

/* Classic */
font-family: Tahoma, "MS Sans Serif", Arial, sans-serif;
font-weight: 700;

/* Windows 7 */
font-family: "Segoe UI", Tahoma, Arial, sans-serif;
font-weight: 600;
```

- Keep product names and menu labels in sentence case unless the brand's wordmark is intentionally all caps.
- Do not apply large tracking, gradient text, drop shadows, or glow to UI wordmarks. Use type, weight, and an optional small mark.
- Do not use a modern geometric sans display face for a period wordmark unless the brief explicitly allows a modern/retro mashup.
- Keep wordmarks out of the primary content heading hierarchy unless they are the actual page title.
- At 200% text, let the wordmark wrap or disappear in favor of the accessible name; never let it clip the titlebar or taskbar.

## 6. Dark/light and era surfaces

- XP desktop icons sit on a saturated blue gradient. Test the mark against `#0a246a`, `#245edb`, and the light end of the desktop gradient.
- Classic icons sit on teal or gray. Pixel marks need a dark outline or a light backing pixel to survive both.
- Windows 7 icons sit on light Aero or wallpaper. Keep the outline and detail readable at 16 px on light backgrounds.
- Do not add a permanent white tile behind every mark unless the era's icon style calls for it. For app windows, a normal opaque content surface is enough.
- On a requested fidelity clone, use the original XP boot and welcome backgrounds, logo lockups, and wallpaper. Keep the copy readable and credit the source. A fan recreation may look official, but must not claim to be official.

## 7. Review checklist

- The mark is the authentic requested Microsoft art or an explicitly licensed substitute; credit, source URL, and rights status are recorded.
- One grid, light source, outline weight, and palette logic across the family.
- A simplified small variant exists for 16/24 px; no blurred downscaling.
- The mark reads at 16 px, 32 px, 48 px, 200% text, and on both light and dark surfaces.
- The wordmark uses an installed era font and remains legible at 200% text.
- For a fidelity build, the supplied Microsoft-style flag, shell icon, wallpaper, and boot art are present and documented; for an original build, none are bundled.
- Decorative marks are hidden from assistive technology; meaningful marks have text alternatives.
