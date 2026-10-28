# Windows XP Luna

Use this guide for Windows XP interfaces in blue, olive, or silver. Keep one color scheme throughout. The 2001 Microsoft visual guidelines are a pre-release source; verify against shipped-XP evidence when exact fidelity matters and label web values as reconstruction baselines.

## 1. Visual intent

Combine warm gray working surfaces with rounded, glossy blue, olive-green, or silver chrome. Luna retains dense desktop productivity layouts; it is not a modern rounded-card system.

- Use rounded caption and control geometry selectively, with crisp borders and small highlights.
- Keep fields, lists, menus, and document areas rectangular and opaque.
- Establish hierarchy through active captions, taskbar buttons, focus, and pressed states rather than large shadows.
- Blue, olive, and silver change palette tokens, not control anatomy or spacing.
- Do not introduce Classic hard bevels, Aero blur, Fluent acrylic, floating pills, or oversized headings.

## 2. Typography

Use installed fonts only:

```css
font-family: Tahoma, "MS Sans Serif", Arial, sans-serif;
```

- Use **8 pt Tahoma** for ordinary UI, approximately 11 CSS px at 96 DPI. The Microsoft guide also permits 9 and 11 pt in appropriate contexts.
- Use **Trebuchet MS Bold 10 pt** as the documented caption treatment when available; Tahoma bold is a practical local fallback. Do not redistribute either font.
- Keep labels sentence case. Use regular weight for body text and bold sparingly for captions, default actions, or selected shell labels.
- Allow fallback fonts and 200% text to increase control height. Never shrink labels to preserve a screenshot metric.

## 3. Palette and material

The guide's color tables are samples, not complete gradient specifications. Treat these as practical starting roles:

| Role | Practical baseline |
|---|---|
| Window/dialog surface | `#ece9d8` |
| Field/menu surface | `#ffffff` |
| Primary text | `#101010` |
| Input border | `#7f9db9` |
| Menu highlight | `#316ac5` with white text |
| Disabled text | Muted warm gray; keep discernible |
| Blue active caption | Deep blue-to-light blue vertical treatment |
| Olive active caption | Muted leaf/olive treatment, not neon green |
| Silver active caption | Light silver/lavender treatment with dark navy text |

Use the bundled theme packs for complete role assignments. Preserve dark caption text across the entire Silver gradient; do not reuse the blue theme's dark gradient stop.

Aero-like `backdrop-filter`, glass panels, neon glows, and blurred shadows are out of era. Luna gloss comes from compact gradients and crisp highlight edges.

## 4. Metrics and spacing

| Element | Practical 96-DPI baseline |
|---|---|
| Standard command button | 75 × 23 px / 50 × 14 dialog units |
| Textbox/combo height | 23 px |
| Dialog margin | 7–11 px consistently |
| Related controls | 5–7 px gap |
| Unrelated groups | 11 px gap |
| Label-to-control | About 5 px |
| Caption | 28 px including Luna frame |
| Taskbar | 30 px (34 px only as an intentional touch scaling) |
| Start button | 100 × 30 px |
| Start menu | 390 × 500 px |
| Desktop icon | 32 × 32 px, 8 pt label |
| Toolbar icon | 16 or 24 px according to context |
| Shell icon | 16, 24, 32, or 48 px |

Expand containers for localization, zoom, and fallback fonts. Avoid laying out every surface on a modern 24/32 px card grid.

## 5. Controls and states

- **Buttons:** rounded rectangle, subtle vertical face gradient, crisp colored border, and small hover highlight. Pressed state darkens/insets without moving the layout box. Show keyboard focus independently of hover.
- **Default button:** emphasize one safe default with a stronger edge; Enter activates it only in the documented dialog context.
- **Fields:** opaque white, square corners, inset border, visible caret/focus. Disabled and read-only are distinct states.
- **Checkbox/radio:** small Luna glyph with label hit area, persistent check/dot, and visible focus around the control/label group.
- **Menus:** white surface, compact items, full-row blue highlight with white text. Keep separators, accelerators, and submenu arrows aligned.
- **Tabs:** connected tab/page geometry; selected tab joins its panel rather than floating as a modern pill.
- **Progress:** period-appropriate segmented or glossy bar plus text/value. Do not make animation the only indication.
- **Scrollbar:** compact Luna track and thumb with separate hover/pressed/disabled states; do not substitute an overlay scrollbar.

Load [behavior-accessibility.md](behavior-accessibility.md) for complete state and keyboard matrices.

## 6. Window and taskbar grammar

1. Use a rounded top caption with application icon/title at left and minimize, maximize/restore, and close at right.
2. Differentiate active/inactive captions without dimming the whole window. Keep content legible.
3. Place optional menubar, toolbar, content, and status bar in compact horizontal bands.
4. Attach the taskbar to one screen edge, normally bottom. Use the color-scheme taskbar gradient, launcher at the start edge, grouped application buttons, and notification area.
5. For a faithful recreation, use the two-column XP Start menu: a 70 px blue identity header with user picture and name; a white left column of pinned applications; a light-blue right column of places and shortcuts; an "All Programs" flyout; and a 38 px blue footer with Log Off and Turn Off Computer actions. Map those session actions to real portfolio behavior (reload/restart) and label them honestly for assistive technology.
6. Use the authentic XP Start button sprite (100 × 30), the 30 px taskbar gradient, and the blue taskbar button states. Keep the notification area with volume and clock at the right.
7. Group related taskbar buttons when appropriate, but provide an accessible label and keyboard route to every window.
8. Window fades, sliding desktops, and elaborate startup sequences are not required unless the brief asks for a startup recreation. When it does, follow [boot-loading.md](boot-loading.md) and use the real XP black loading and blue Welcome stages with sourced art.

## 7. Icons and imagery

For an exact XP recreation, use the authentic icon family and wallpaper from the reference build; do not draw substitutes:

- Use the real 32 × 32 desktop icons and 16 × 16 titlebar/taskbar variants from the win32.run or WinXP reference sets: My Computer, My Documents, folder, Recycle Bin, Internet Explorer, Control Panel, Help, email, WordPad, volume, power, logoff, and so on.
- Use the Bliss wallpaper unless the brief names another XP wallpaper; source the image locally and record it in CREDITS.
- Keep the 8 pt white desktop labels with a dark 1 px shadow.
- If an app has no matching XP icon, choose the closest authentic shell icon or draw a 48/32/16 family that matches the XP material, light source, and perspective.
- For project logos, read [logo-and-wordmark.md](logo-and-wordmark.md): use one grid, light source, outline, and a true small variant. Pixelated marks must be built on an integer grid, not a smoothed vector shrunk to 16 px.
- Microsoft flags, shell icons, Bliss, files, and theme art remain Microsoft's. Use them for the requested local fan recreation, record provenance, and do not claim official status.

## 8. Motion and sound

- Keep ordinary feedback immediate; where animation is useful, use roughly 80–220 ms rather than theatrical transitions.
- Avoid unrequested boot/login delays, CRT effects, bouncing icons, and window fade-in/out as a generic XP signature.
- A startup/welcome screen is a separate, opt-in deliverable. When asked for one, follow [boot-loading.md](boot-loading.md): a blue Luna-style welcome surface, original mark, honest short status, a visible Skip control, and a remembered "show on startup" choice. Do not fake a login or hardware diagnostics.
- Keep sound off until explicit opt-in. Use the bundled original short cues only with visible equivalents, persistent mute, and volume control.

## 9. Review checklist

- Exactly one of blue, olive, or silver is active across caption, launcher, selection, focus, and controls.
- Command buttons, fields, menus, tabs, scrollbars, and taskbar buttons share Luna anatomy.
- Active/inactive windows, default/cancel, disabled, focus, checked, pressed, and error states are rendered and operable.
- Silver caption/selection contrast passes across the complete gradient.
- The interface works with local fonts, keyboard only, 200% text, reduced motion, and muted audio.
- Inspect a real render. Compare against [sources.md](sources.md) rather than treating community CSS or memory as an official specification.
