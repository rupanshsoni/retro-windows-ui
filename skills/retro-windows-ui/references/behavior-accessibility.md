# Behavior and accessibility

Apply these requirements to every era. Visual fidelity never excuses an inert control, invisible focus, keyboard trap, or motion that ignores user preferences.

## 1. Establish the interaction model

- Prefer native `button`, `input`, `select`, `textarea`, `a`, and dialog semantics. Add ARIA only when native semantics cannot express the desktop pattern.
- Expose an accessible name, role, value, and state. Use `aria-expanded`, `aria-selected`, `aria-checked`, `aria-current`, `aria-disabled`, and `aria-modal` only where they match actual behavior.
- Do not apply `role="application"` to an entire web page. A desktop visual shell is still application content, not a reason to override assistive-technology navigation.
- Keep DOM order aligned with reading and focus order. Position windows visually without creating an unpredictable keyboard sequence.
- Use a visible text label for unfamiliar actions. An icon-only caption button needs an accessible name and a discoverable tooltip.
- Make pointer targets at least 24 by 24 CSS px where feasible. Preserve smaller visual glyphs by extending the hit area without changing era geometry.
- Never require double-click, right-click, hover, drag, sound, or color perception as the sole path to an action.

## 2. Testable control-state matrix

Implement only states supported by a control, but do not omit focus or disabled treatment because the era reference lacks a sample. Verify each row with pointer and keyboard, not CSS inspection alone.

| Control | Rest/default | Hover | Pressed/active | Keyboard focus | Selected/checked/expanded | Disabled |
|---|---|---|---|---|---|---|
| Push button | Era face, border, legible label; one dialog default may have an emphasized edge | Subtle era highlight; no layout shift | Depressed bevel or era press fill; label stays put or shifts only per era guide | Visible focus indicator inside/outside border; Enter and Space activate | Toggle button remains pressed and exposes `aria-pressed`; ordinary buttons do not fake selection | No activation; muted era treatment; keep label discernible |
| Checkbox/radio | Box/diamond and label; state not conveyed by color alone | Highlight without changing glyph size | Press feedback on pointer down; commit on release | Focus ring around box/label group; Space toggles checkbox or selects radio | Persistent check/dot plus programmatic state | Glyph and label muted; no state change; current value remains visible |
| Text input | Opaque field, inset era border, readable value | No required movement or border jump | Caret and normal editing | Strong focus edge plus caret; text remains visible | Selection uses theme selection pair and does not erase focus | Distinct field/label treatment; no editing; avoid placeholder-only values |
| Select/dropdown | Closed value and clear drop affordance | Hover on button/list option | Open or press state matches era | Closed: arrows change or navigate per platform pattern; open: focus follows active option | Check/highlight current option; `aria-expanded` tracks popup | Closed and noninteractive; value remains readable |
| Menu item | Full label, accelerator/shortcut where applicable | Highlight entire item row | Activate once on click/release | Highlight entire row; arrows move; focus indicator remains visible | Checked items retain check plus highlight; submenu exposes expanded state | Skip during arrow navigation; muted label; do not activate |
| Tab | One connected tab set and panel | Subtle highlight | Selected tab connects visually to panel | Arrow keys move tabs; activation model is consistent | `aria-selected=true`, visible selected surface, only its panel active | Unavailable tab is not focusable/activatable; label remains readable |
| List/tree item | Text/icon, indentation and expander where needed | Row highlight | Selection on click; avoid double-click-only actions | Row focus distinct from selection; arrows navigate | Selection uses tested colors; expansion also changes glyph and `aria-expanded` | Disabled branch cannot activate; expanded content stays understandable |
| Slider | Track, thumb, label and current value | Thumb/track highlight | Drag with pointer capture; no value jump on release | Arrows adjust; Page Up/Down larger steps; Home/End bounds | Value exposed programmatically; thumb position matches value | No drag/keyboard change; value still readable |
| Window caption | Active/inactive hierarchy per selected era | Only interactive controls respond | Caption buttons show press state | Caption actions keyboard reachable through a menu or equivalent controls | Active window has one unambiguous treatment | Disabled caption action is muted and unavailable |
| Taskbar/launcher item | Window/program name and icon; stable ordering | Era hover highlight | Pressed/open state and click action | Focus indicator; Enter/Space activates | Current/active item distinct from merely focused item | Unavailable item cannot activate; text remains legible |
| Link | Underline plus meaningful text | Pointer and era hover treatment | Activation feedback without navigation duplication | Visible focus; Enter activates | Current location uses `aria-current` where relevant | Prefer no disabled links; use disabled button semantics for unavailable actions |

### State test protocol

1. Tab to the control; confirm a visible indicator before activation.
2. Activate with the control's documented keys; verify exactly one state change.
3. Repeat with pointer down, move off, and release; ensure no accidental activation when cancelled.
4. Compare hover, focus, selected, and pressed states; ensure each is distinguishable and no border changes cause layout shift.
5. Disable the control while focused; move focus predictably to the nearest useful control rather than losing it to the document body.
6. Enable forced-colors/high-contrast mode; ensure system colors or explicit borders preserve the control outline, focus, check, and selection.

## 3. Keyboard menus and launchers

Use menubar behavior for a horizontal application menu and menu behavior for a Start-like launcher's menu surface. A launcher that is a simple dialog of links may use ordinary Tab navigation instead; do not emulate menu keys inconsistently.

| Input | Required behavior |
|---|---|
| `F10` or `Alt` | Focus the menubar when one exists; preserve the prior focus location for cancellation |
| `Alt+<accelerator>` | Activate the advertised access key unless the host platform reserves it; do not suppress browser/assistive-technology shortcuts globally |
| Left/Right on menubar | Move between top-level menus; when a submenu is open, move to the adjacent menu and open it |
| Down on menubar | Open the selected menu and focus its first enabled item |
| Up/Down in menu | Move through enabled items, wrapping when conventional; never stop on separators or disabled items |
| Right on submenu parent | Open submenu and focus its first enabled item |
| Left in submenu | Close current submenu and return focus to its parent item |
| `Home`/`End` | Move to first/last enabled menu item |
| Printable characters | Use typeahead within the current menu; do not trigger global shortcuts while typing in a field |
| `Enter`/`Space` | Activate focused item; close the menu after a command, not after opening a submenu |
| `Escape` | Close one submenu level; if at the root, close the menu and return focus to its trigger |
| `Tab` | Close a menu and continue normal document navigation; do not cycle through dozens of menu items with Tab |
| Click/tap outside | Dismiss the transient menu and return focus if dismissal leaves focus inside hidden content |

For a Start-like launcher, place initial focus on its first meaningful item or search field according to the selected design. On close, return focus to the launcher button. Keep the trigger's expanded state synchronized. A taskbar remains outside the launcher; closing the launcher must not minimize the active window.

## 4. Dialogs and focus containment

### Modal dialogs

1. Store the invoking element and the previously focused element.
2. Move focus to the first logical field, or to the dialog heading/container when content must be read first. Do not automatically focus a destructive action.
3. Mark background content inert and noninteractive. Trap Tab and Shift+Tab within the modal while leaving browser and assistive-technology commands available.
4. Let Enter activate the default action only when focus is not in a multiline field or on another button. Let Escape cancel when cancellation is safe and supported.
5. On close, remove inert state before restoring focus to the invoker. If it no longer exists, focus the nearest logical surviving control and announce the context change if needed.

### Modeless dialogs and desktop windows

- Do not trap focus. Allow normal movement among windows and application controls.
- Bring a focused or explicitly activated window to the front and update active styling together; do not create visual and keyboard disagreement about which window is active.
- Give each window an accessible name from its visible caption. Associate its content with that caption.
- Offer keyboard alternatives to drag/resize. If moving/resizing is implemented, provide documented arrow-key adjustment and usable size limits.
- Keep at least part of every window reachable at small viewports; do not allow off-screen captions with no recovery mechanism.

## 5. Active and inactive windows

- Maintain exactly one active window in a desktop shell, except while no window is open.
- Active state affects caption, taskbar item, and input destination together. Inactive windows remain readable and may expose available actions.
- Clicking an inactive window's control may both activate the window and perform the control action only when that behavior is predictable; avoid swallowing the first click without explanation.
- Do not use opacity on the entire inactive window: it harms text contrast. Change caption/chrome tokens instead.
- Keep focused-element styling visible when a window becomes inactive, but distinguish window-level active state from control-level focus.
- Restore prior focus when returning to a window. If focus was in a closed dialog, use its surviving invoker within that window.

## 6. Taskbar minimize, restore, and window lifecycle

| Action | Visual result | Focus/semantic result |
|---|---|---|
| Minimize active window | Remove window from layout or hide it accessibly; taskbar item remains | Choose the next visible window and focus its prior element; if none, focus its taskbar item or desktop landmark |
| Minimize inactive window | Hide that window without unnecessarily changing other window geometry | Do not leave focus inside hidden content; restore active-window focus if needed |
| Restore from taskbar | Show window at its previous size/position, constrained to current viewport | Make it active and restore its prior focused control |
| Activate an already visible taskbar item | Bring its window forward without duplicating it | Focus prior control; update active caption and taskbar state |
| Minimize via active taskbar item | If supported, toggle consistently | Apply minimize behavior above |
| Close window | Remove window and taskbar item; clean up menus/dialogs owned by it | Focus the next logical window/taskbar item, never a removed node |
| Maximize | Fill the defined work area, not the taskbar | Keep focus and accessible name; expose restore action and state |
| Restore size | Return to previous usable bounds | Keep focus; ensure caption controls remain on-screen |

Use `hidden`, `inert`, or equivalent accessibility hiding for minimized content; merely moving it off-screen or setting transparency leaves ghost tab stops. Announce important lifecycle changes through visible labels and, sparingly, a polite live region.

## 7. Text, zoom, and contrast

- Test at 200% text size and 200% browser zoom, plus 400% zoom at a narrow viewport where applicable. Permit reflow; avoid clipping, overlapping captions, inaccessible controls, and two-dimensional page scrolling except for genuinely tabular or desktop-canvas content.
- Use relative units for type and container sizing. Logical-pixel borders and icon dimensions may remain fixed when needed for fidelity.
- Allow captions and button labels to wrap or enlarge their containers. Ellipsize only secondary window titles when a full accessible name/tooltip remains available.
- Maintain WCAG contrast of at least 4.5:1 for normal text and 3:1 for large text. Target 3:1 for control boundaries, icons required to understand state, and focus indicators against adjacent colors.
- Test actual token pairs, including inactive captions, selection, menu highlight, taskbar text, input text, and text over glass. Disabled text is exempt from WCAG contrast minimums but should remain discernible.
- Never encode errors, selection, required fields, or active state by color alone; add text, shape, glyph, border, or pattern.
- Preserve meaningful outlines in forced-colors mode. Do not globally disable outlines or force backgrounds that hide system focus colors.

## 8. Motion and transparency

- Honor `prefers-reduced-motion: reduce` by removing nonessential translation, zoom, pulsing, animated gradients, and taskbar/window slide effects. Use immediate state changes or a short opacity change when comprehension benefits.
- Keep essential progress indication available without motion: provide text/value and a determinate state, not only an animated stripe.
- Pause or stop nonessential repeating animation; provide a control for any motion lasting more than five seconds.
- Honor reduced-transparency platform settings where exposed and provide an application setting when glass is central. Replace translucent/blurred surfaces with opaque theme surfaces, not lower-contrast approximations.
- Test transparency against the lightest and darkest permitted wallpaper/content. Text must have a stable backing surface if contrast cannot be guaranteed.
- Do not use flashing content. Avoid more than three flashes per second and avoid high-contrast full-screen flashes entirely.

## 9. Opt-in persistent audio controls

- Default audio to off. Never play startup, navigation, error, hover, or background sound automatically.
- Require an explicit, labelled opt-in action and a user gesture before creating or resuming audio playback.
- Keep a persistent mute/unmute control available wherever sound can occur. Offer volume when more than minimal feedback is used; remember the user's choice only with appropriate consent/storage behavior.
- Stop or mute audio when the controlling surface closes, and handle page visibility changes without surprising playback.
- Pair every meaningful sound with simultaneous visible feedback: status text, icon/state change, dialog, or live-region announcement where appropriate.
- Do not make sound the only error, success, notification, or progress signal. Do not play sound on mere focus or every hover.
- Use licensed local files, short durations, conservative levels, and no remote media dependency. Captions are required for speech; a visual description is required for meaningful non-speech audio.

## 10. Minimum verification pass

1. Complete all primary tasks with keyboard only; record focus entry, order, containment, cancellation, and return.
2. Inspect default, hover, pressed, focused, selected, disabled, and error states in the rendered interface.
3. Open/close every menu and dialog; test Escape, outside click, and invoker removal where relevant.
4. Minimize, restore, maximize, and close windows; verify no hidden focus or orphaned taskbar items.
5. Increase text/zoom and test long labels, validation messages, and empty/error/loading content.
6. Measure foreground/background and non-text contrast pairs, including glass fallbacks and inactive states.
7. Test reduced motion, reduced transparency, and forced colors independently.
8. Verify audio starts muted, remains controllable, and always has visible equivalents.
9. If any step could not be exercised in a rendered environment, state the exact limitation rather than claiming a complete accessibility pass.
