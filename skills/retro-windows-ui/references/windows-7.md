# Windows 7 Aero and Basic

Use this guide for Windows 7-era desktop interfaces. Choose **Aero** or **Basic** before styling. Both share typography, layout, controls, and shell behavior; Aero adds composited transparency and richer glass highlights. Vista is historical context, not the same theme.

## 1. Visual intent

- Use light working surfaces, compact blue selection, precise control borders, and subtle gloss.
- Aero glass is a composited material that blends with content behind the window. CSS transparency/backdrop blur is only an approximation.
- Basic uses opaque caption/frame surfaces and no blur dependency. It is not merely Aero with reduced opacity.
- Keep app content quieter than window chrome. Avoid Luna's warm beige surfaces and green/blue capsule taskbar, Classic hard bevels, and modern Fluent acrylic/cards.

## 2. Typography

Use installed fonts only:

```css
font-family: "Segoe UI", Tahoma, Arial, sans-serif;
```

- Use **9 pt Segoe UI** for ordinary Vista/7 application UI, approximately 12 CSS px at 96 DPI.
- Microsoft guidance uses 12 pt Segoe UI `#003399` for main instructions when that pattern is present; ordinary labels remain 9 pt.
- Use regular weight for most text. Bold is for emphasis, not every caption or button.
- Use sentence case, meaningful labels, and direct instructions. Permit localization and text scaling to expand layouts.

## 3. Layout and control metrics

Microsoft layout guidance supplies these 96-DPI baselines:

| Element | Baseline |
|---|---:|
| Command button | 75 × 23 px |
| Textbox/combo height | 23 px |
| Checkbox/radio height | 17 px |
| Static text height | 13 px |
| Slider | 24 px |
| Dialog margin | 11 px |
| Label-to-control gap | 5 px |
| Related-control gap | 7 px |
| Unrelated-control gap | 11 px |
| Dependent-control indent | 18 px |

Use these as logical pixels, not mandatory physical bitmap dimensions. Test at 96/120/144 DPI equivalents, browser zoom, and 200% text. Support usable narrow layouts rather than clipping to an 800×600 screenshot.

## 4. Aero material

- Restrict glass to window frames and intentional shell surfaces. Keep text and editable fields on stable opaque backing where necessary.
- Use compact inset highlights, a subtle border, restrained glow, and shadows for window hierarchy.
- Test text and meaningful boundaries against the lightest and darkest content behind glass. Do not assume one backdrop.
- Provide a reduced-transparency mode that uses `surface.windowSolid` and opaque frame/menu tokens. Remove blur rather than leaving low-contrast translucent layers.
- Respect reduced motion. Most feedback can be immediate or 100–300 ms; frequent operations should be shorter.

## 5. Basic material

- Use opaque `#f0f0f0`-family working surfaces and solid blue/gray captions.
- Retain Windows 7 control radii, typography, spacing, focus, and shell behavior. Do not fall back to XP Luna or Classic bevels.
- Use compact gradients and borders without `backdrop-filter` or transparency-dependent layering.
- Ensure Basic is a complete theme, not a degraded error state.

## 6. Controls and states

- **Buttons:** 23 px baseline height, light face, 3 px practical radius, crisp border, subtle hover glow, and clear pressed state. One dialog default may have a stronger edge.
- **Fields:** white opaque surface, compact border, visible focus/caret, separate disabled and read-only treatment.
- **Checkbox/radio:** persistent glyph plus label, 17 px baseline row, keyboard focus around the group.
- **Selection:** light blue surface with dark text in lists and menus; maintain contrast and a separate focus indicator.
- **Tabs:** selected tab connects to its page. Arrow keys navigate; avoid detached modern pill tabs.
- **Progress:** Windows 7-style blue/green fill plus numeric/text state. Pause animation under reduced motion without hiding progress.
- **Links:** use meaningful underlined text; documented normal link blue is `#0066CC`, with hover treatment that preserves contrast.

See [behavior-accessibility.md](behavior-accessibility.md) for the full state and keyboard matrix.

## 7. Window grammar

1. Use a caption with application icon/title and minimize, maximize/restore, close controls. Keep caption actions keyboard reachable.
2. Change active/inactive caption and frame tokens without applying opacity to the whole window.
3. Keep menubar/toolbar/content/status regions compact and aligned to the 5/7/11 px rhythm.
4. Center owned dialogs relative to their owner where practical. Preserve window size/position and constrain restored windows to the current viewport.
5. Use modal focus containment only for modal dialogs; modeless windows retain normal keyboard navigation.
6. Do not force activation or sound to request attention. Use a visible taskbar/caption state and a non-audio cue.

## 8. Taskbar and shell grammar

- Use a bottom-attached, approximately 40 px taskbar at baseline, with pinned/open items, active state, notification area, and show-desktop affordance only when functional.
- Windows 7 taskbar items may represent pinned applications even when closed. Distinguish pinned, open, active, attention, and progress states programmatically and visually.
- Thumbnail previews, Jump Lists, thumbnail toolbars, overlays, and taskbar progress are optional shell features, not decorations to fake.
- Jump Lists must not be the only route to functionality. Thumbnail toolbars contain at most seven commands in the Microsoft guidance.
- Use temporary 16 × 16 lower-right overlay indicators without animation when implementing overlays.
- A Start-like launcher should expose real application destinations and return focus to its trigger on close.

## 9. Icons and sound

- Vista/7 application icon guidance includes 16, 32, 48, and 256 px sizes. Create simplified small variants rather than scaling one detailed render.
- Use upper/front-left lighting and more realistic but restrained gradients than XP. For an exact Windows 7 recreation, use the supplied reference build's wallpapers, shell icons, boot art, and logo lockups; record the source and Microsoft rights in CREDITS. For an original era-inspired build, keep original artwork.
- For project marks and wordmarks, read [logo-and-wordmark.md](logo-and-wordmark.md). Keep the family's light source and provide a true 16/32 px variant.
- Use supplemental, pleasant, nonverbal sound only after opt-in. Microsoft guidance favors cues generally under one second and no more than two consecutive repetitions; the bundled cues are shorter originals, not Windows recordings.
- Pair every cue with visible status and persistent mute/volume controls.
- A startup screen is opt-in. When requested, follow [boot-loading.md](boot-loading.md): a quiet black "Starting Windows" stage with an original four-color-style mark and "Starting Windows" text, then an immediate transition. Do not reuse XP or Classic loading grammar.

## 10. Review checklist

- Aero and Basic share Windows 7 anatomy but have intentionally different materials.
- Glass is limited, legible, and replaced by coherent opaque surfaces under reduced transparency.
- Command buttons, fields, tabs, menus, selection, focus, disabled, active/inactive, and error states are complete.
- Taskbar/window behavior works with keyboard and pointer and does not imply fake OS functionality.
- Inspect real renders at normal/high DPI, 200% text, reduced motion, and reduced transparency. State any unverified behavior.
- Consult [sources.md](sources.md) for official versus community values; do not present 7.css approximations as official Aero tokens.
