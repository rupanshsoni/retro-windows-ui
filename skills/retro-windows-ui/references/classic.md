# Windows Classic: 95, 98, and 2000

Use this guide for squared, beveled, system-colored desktop interfaces. The three releases share a grammar, but exact system metrics varied with display settings, font settings, DPI, and product updates. Treat pixel values below as practical 96-DPI reconstruction baselines, not undocumented canonical specifications.

## 1. Visual intent and variant selection

Aim for a utilitarian work surface: cool gray controls, hard rectangular geometry, black text, navy selection, and a consistent top-left light source. Depth comes from one- and two-pixel bevels, not blur or rounded elevation.

- **95 baseline:** Prefer flat teal desktop, single-color captions, simple title-bar controls, and restrained gray chrome. Use this when strict early-Classic simplicity matters.
- **98 baseline:** Permit the familiar two-color active-caption gradient, richer shell icons, and slightly more polished launcher/taskbar treatment. Keep the same bevel grammar as 95.
- **2000 baseline:** Use the more sober business-desktop balance: conservative caption treatment, muted palette, crisp controls, and minimal decorative color. A gradient may be present depending on settings; do not make it mandatory.

Choose one baseline before styling. Do not use Luna blue plastic, green Start capsules, Aero blur, translucent panels, or modern floating cards.

## 2. Semantic palette

Use system-color intent rather than scattering literal values. These sRGB samples are reconstruction defaults, not claims that every installation used identical colors.

| Intent | Practical value | Use |
|---|---|---|
| Desktop | `#008080` | Empty desktop/work area only |
| Button/control face | `#c0c0c0` | Dialogs, buttons, menus, taskbar |
| Raised light | `#dfdfdf` | Inner top/left bevel |
| Raised highlight | `#ffffff` | Outer top/left highlight |
| Raised shadow | `#808080` | Inner bottom/right bevel |
| Raised dark edge | `#000000` | Outer bottom/right edge |
| Field background | `#ffffff` | Text/list editable surfaces |
| Primary text | `#000000` | Labels and field text |
| Secondary/disabled text | `#565656` or etched `#808080` | Unavailable labels; preserve legibility |
| Active caption | `#000080` | 95 default and 98/2000 start color |
| Active caption end | `#1084d0` | Optional 98/2000 horizontal gradient |
| Inactive caption | `#808080` | Inactive window hierarchy |
| Active caption text | `#ffffff` | Active title and glyph |
| Inactive caption text | `#c0c0c0` | Verify contrast; darken if necessary |
| Selection | `#000080` | Menu/list/taskbar selection |
| Selection text | `#ffffff` | Selected label |
| Focus | `#000000` | Dotted rectangle or high-contrast outline |
| Error | `#800000` | Pair with text/icon, never color alone |

For accessible custom themes, retain semantic relationships but adjust sampled values to tested contrast pairs. Do not put body text directly on the desktop color without a backing surface.

## 3. Local fonts and typography

Use local installed fonts only:

```css
font-family: "MS Sans Serif", Tahoma, Arial, sans-serif;
```

- Start with **8 pt Tahoma** (about 11 CSS px at 96 DPI) for a cross-release reconstruction. `"MS Sans Serif"` is an era-appropriate first choice when installed; its absence must not break layout.
- Use regular weight for labels, fields, menus, and captions. Bold may identify a default button or selected shell label, but avoid modern heading hierarchies.
- Keep title bars and menus close to UI text size. Do not enlarge captions into marketing headings.
- Use normal or slightly tight line spacing, approximately 1.2–1.35, and leave enough height for fallback fonts and scaled text.
- Keep sentence case. Use ellipses on commands that request more information, access-key underlines when the platform exposes them, and keyboard shortcuts right-aligned in menus.
- Use a separately licensed bitmap font only if its redistribution license is verified. Never copy a Windows font file into the project.

## 4. Spacing and control metrics

Use a 4 px base rhythm with small optical adjustments. Metrics below are starting points; allow font scaling to change control height.

| Element | Practical baseline |
|---|---|
| Dialog outer padding | 7–11 px; use one value consistently per layout |
| Related control gap | 4–6 px |
| Unrelated group gap | 8–12 px |
| Label-to-field gap | 4–6 px horizontally or vertically |
| Standard command button | 75 × 23 px reconstruction baseline; 4–8 px between buttons |
| Small toolbar button | 22–24 px square hit area, icon centered |
| Text field | Minimum 23 px high at baseline; inset 2 px border |
| Checkbox/radio glyph | 13 px visual box; larger label hit area |
| Menu item | 20–22 px high; icon/check column about 20–24 px |
| Window outer border | 2–3 px including frame and bevel |
| Caption height | About 18–20 px plus frame; 16 px caption icon |
| Caption buttons | About 16 × 14 px visual face, grouped at right |
| Taskbar | About 28–30 px high |
| Desktop icons | 32 px image with label below, or 16 px in compact lists |

Do not shrink long labels to meet these values. Expand controls and dialogs, then verify 200% text behavior.

## 5. Borders, bevels, and shadows

Build depth with discrete edges:

- **Raised button:** white outer top/left, light-gray inner top/left, dark-gray inner bottom/right, black outer bottom/right.
- **Pressed button:** reverse the perceived light direction, simplify to an inset edge, and optionally shift the label by 1 px. Never move the component's layout box.
- **Sunken field:** dark-gray top/left with black or dark inner edge where appropriate; white/light bottom/right. Keep the interior white and rectangular.
- **Window frame:** raised outer frame around a separate caption and content region. Do not bevel every nested container.
- **Group box:** a single etched border with its label interrupting the top rule; avoid a modern card shadow.
- **Focus:** dotted 1 px rectangle inside command buttons or around labels, kept visible against selection. Supplement it when forced colors remove the dotted effect.
- **Shadow:** reserve a small hard-edged or very restrained offset shadow for menus and overlapping windows. Avoid blur-heavy shadows on buttons, fields, and every panel.

Use pseudo-elements or multiple inset shadows to create crisp bevels without images. Avoid `border-radius` except where a genuine control requires it.

## 6. Interaction states

- Resting controls use the face color; hover is subtle and may be absent for strict 95 behavior. Never rely on hover to expose essential commands.
- Pressed controls invert bevels. Toggle buttons and active taskbar items remain pressed, with a programmatic state.
- Selected list/menu items use navy with white text. Focused-but-unselected items need a separate dotted indicator.
- Disabled labels may use the era's etched technique—light offset with gray foreground—but test readability. Disabled controls do not respond to hover or keyboard activation.
- Caption controls show recognizable minimize, maximize/restore, and close geometry using original CSS or licensed icons, with accessible names.
- Validation uses text and optionally an icon; do not introduce modern toast stacks or red glowing fields.

Load [behavior-accessibility.md](behavior-accessibility.md) for keyboard, focus, state, scaling, and test requirements when implementing interactions.

## 7. Window grammar

1. Start with a rectangular raised frame and a single caption row.
2. Put an optional 16 px application icon and title at the left; group caption buttons at the right. Keep close visually separated when space permits.
3. Use the active navy caption and white title. For 98/2000, an optional left-to-right gradient may end in blue. Use gray inactive chrome without dimming the entire window.
4. Place an optional application menubar directly below the caption. Use File/Edit/View-style menus only when the product has corresponding commands.
5. Put content on the control-face surface. Use white only for fields, lists, document areas, and other content canvases.
6. Put optional status information in a bottom status bar with shallow sunken cells. Avoid turning every status cell into a button.
7. Make resize handles and borders functional if windows are resizable. Keep captions reachable at narrow viewports.

Overlap windows sparingly and establish clear z-order. A single maximized work area is more faithful than arbitrary floating cards for a productivity interface.

## 8. Taskbar and Start-like launcher grammar

- Keep the taskbar attached to one screen edge, normally the bottom. Use the same gray face and raised edge as dialog chrome.
- Put the launcher button at the left/start edge, task buttons in the center, and a sunken status/notification area at the right/end. Use a text label on the launcher button; an original flag-like mark is optional and must not imitate Microsoft's logo.
- Represent each open window with a rectangular task button, 16 px icon, and ellipsizable title. Distinguish active, inactive, focused, minimized, and attention states without animation dependence.
- Use a raised launcher menu with a narrow decorative side band only for the 95/98-style shell when desired. Keep menu items single-column with 32 px icons or a compact 16 px variant, labels, and submenu arrows.
- Include Programs-like groups, Documents-like recent items, Settings-like configuration, Find/Search, Help, Run-like command, and shutdown actions only when they map to real application functions. Do not present fake operating-system operations.
- Keep the launcher above the taskbar but below dialogs that must remain modal. Close on Escape, selection, or outside interaction and return focus to its button.

## 9. Icons and imagery

- Design original pixel icons on a 16 × 16 or 32 × 32 grid, with crisp edges, limited colors, a consistent top-left light, and a restrained dark outline.
- Prefer recognizable objects and simple metaphors over abstract modern line icons. Use the same perspective and palette within an icon family.
- Provide 1× assets at minimum; use integer scaling for pixel art. Do not apply smoothing that makes scaled pixel icons muddy.
- For a project mark or wordmark, read [logo-and-wordmark.md](logo-and-wordmark.md). Crop the licensed mark, reduce it on an integer grid, simplify it for 16 px, and record provenance.
- For an explicit faithful Classic recreation, use the Microsoft-style flags, shell icons, wallpapers, cursors, and boot art from the user-supplied reference build (for example 98.js or win98.si), copy them locally, and record the source and Microsoft rights in CREDITS. Do not claim official status; do not silently redistribute proprietary font files.
- Use text alternatives for meaningful icons and hide redundant decorative icons from accessibility APIs.

## 10. Motion and sound

- Keep interaction feedback effectively immediate. Menus may appear without animation; window operations may use a brief 50–120 ms state change if desired.
- Avoid sliding desktops, bouncing icons, pulsing taskbar buttons, and animated gradients. Honor reduced motion by removing all nonessential transitions.
- A boot/loading screen is not part of the default Classic look. When explicitly requested, follow [boot-loading.md](boot-loading.md): a short, skippable simulation with a monochrome start line, an original pixel mark, and no fake hardware diagnostics by default.
- Keep audio off by default. If explicitly requested, use short licensed local sounds with opt-in playback, persistent mute, and visible equivalents.

## 11. Do / don't

**Do**

- Use square corners, gray faces, white fields, navy selection, crisp bevels, and real text.
- Preserve system-color semantics so a custom theme can restyle all components.
- Keep density compact but labels readable and targets operable.
- Distinguish 95, 98, and 2000 mainly through caption and shell refinements.

**Don't**

- Add rounded dialogs, capsule buttons, glass, blur, neon, modern hero layouts, or oversized headings.
- Turn every surface into an independently raised card.
- Use generic flat gray rectangles with no pressed, focus, or inactive treatment.
- Claim pixel-perfect official metrics from memory or community CSS.
- Add boot screens, scanlines, CRT noise, or startup audio unless explicitly requested.

## 12. Implementation and inspection notes

- Build a small primitive set—frame, button, field, menu, list, caption, task button—then compose all surfaces from those primitives.
- Use semantic custom properties for face, light, highlight, shadow, dark edge, caption, selection, text, and focus. Avoid component-specific copies of palette literals.
- Use `box-shadow` or pseudo-elements for multiple 1 px bevel lines; verify rendering at non-integer zoom for hairline gaps.
- Keep icons and assets local and relative. No runtime network dependency is necessary for this visual style.
- Render and inspect at least a dialog, menu, active/inactive window pair, and taskbar/launcher state. Check pressed-bevel direction, focus visibility, text fallback, and 200% scaling. If rendering is unavailable, explicitly report that visual fidelity and zoom behavior remain unverified.
- See [sources.md](sources.md) for the distinction between official guidance and community approximations.
