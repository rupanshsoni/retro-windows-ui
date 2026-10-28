# Semantic token schema

Use the bundled JSON packs as era contracts rather than copying component-specific hex values into new code. The canonical schema is [../assets/tokens/schema.json](../assets/tokens/schema.json); generated CSS is [../assets/tokens/themes.css](../assets/tokens/themes.css).

## 1. Theme identity

Each pack contains `schemaVersion` and `identity`:

- `id`: stable hyphen-case identifier such as `xp-luna-blue`.
- `name`: human-readable variant.
- `family`: `classic`, `xp-luna`, or `windows-7`.
- `era`: historical family label.
- `variant`: `default`, `blue`, `olive`, `silver`, `aero`, or `basic`.
- `description`: concise material/behavior summary.

Select exactly one theme with `data-theme="<id>"`. Do not combine variables from different packs to make a generic retro skin.

## 2. Required roles

| Group | Responsibility |
|---|---|
| `typography` | Local font stacks and body, caption, menu, small, and code roles |
| `colors.surface` | Desktop, window, solid fallback, control, input, inset, menu, tooltip, overlay |
| `colors.text` | Primary, secondary, muted, disabled, inverse, link, error |
| `colors.border` / `colors.bevel` | Default/light/dark/shadow edges and era-specific raised/pressed treatment |
| `colors.selection` / `colors.focus` | Selected/inactive-selected surfaces and independent keyboard focus |
| `colors.titlebar` / `colors.taskbar` | Active/inactive caption and shell roles |
| `colors.status` | Text/background and info, success, warning, error cues |
| `metrics` | Control height, borders, caption/taskbar/icon/checkbox/scrollbar dimensions |
| `spacing` | Shared logical spacing rhythm |
| `radius` / `gradients` / `shadows` | Era material and geometry |
| `motion` | Fast/normal/slow durations and easing |
| `contrastPairs` | Declared foreground/background/minimum-ratio tests |
| `assets` | Optional local paths relative to the theme JSON file |

Keep raw values inside packs. Components should consume generated custom properties such as surface, text, border, selection, and motion roles.

## 3. Extending a theme

1. Choose the correct era file and duplicate its semantic structure; do not create a hybrid family.
2. Update identity and every dependent role together. A caption color change may require caption text, glyph, focus, and contrast-pair changes.
3. Preserve solid fallbacks for translucent values and non-color equivalents for status/selection.
4. Use relative local asset paths. Do not add remote font, image, script, or audio URLs.
5. Regenerate `themes.css` and the manifest with the repository asset tool rather than hand-editing generated output.
6. Run the asset validator and inspect the gallery in the modified theme.

## 4. Contrast contract

Each `contrastPairs` entry contains:

```json
{
  "foreground": "#101010",
  "background": "#ece9d8",
  "minimumRatio": 4.5
}
```

- Use 4.5:1 for normal text and 3:1 for large text.
- Target 3:1 for meaningful control boundaries, icons required to understand state, and focus indicators.
- Add pairs for custom caption, inactive caption, menu selection, taskbar, input, status, and text-over-glass roles.
- Test the least favorable gradient stop/backdrop, not only the lightest sample. Disabled text is exempt from WCAG minimums but must remain discernible.
- A passing numeric pair does not replace rendered inspection of focus, gradients, transparency, and forced colors.

## 5. Runtime use

- `themes.css` exposes variables under `data-theme`, so examples work over `file://` and static servers without fetching JSON.
- Use conventional deferred JavaScript; do not require a module loader, framework, web font, or build step in generated output.
- Keep audio muted until explicit user activation and resolve audio through local paths.
- When copying a starter into another project, preserve its relative assets or copy the required cleared files and update paths deliberately.
- Use `scripts/catalog.py` to discover theme/resource paths and `scripts/validate_assets.py` after changing bundled resources.
