# Portfolio patterns

Use these patterns when the requested product is a portfolio, résumé, or project showcase rather than a single dialog. The selected era guide still controls every visual detail.

## 1. Treat the shell as navigation

A desktop shell is a navigation metaphor, not an operating-system simulation. Give it:

- a wallpaper and desktop icon column;
- one window frame per app;
- a taskbar with Start, open-window buttons, and a clock/tray;
- optional startup/welcome screens that are skippable and replayable.

Keep the real content in the DOM. A user must be able to reach About, Projects, Skills, Contact, and Résumé with the shell hidden or broken.

## 2. Information architecture

| App | Purpose | Essential states |
|---|---|---|
| About | Identity, availability, selected work, focus areas | default, profile-selected |
| Projects | Filterable index plus a detail preview | all, filtered, empty, selected |
| Skills | Grouped toolkit, optionally profile-specific | default, profile-selected |
| Contact | Direct links, no form | copy success/failure if copy exists |
| Résumé | Print/PDF-friendly technical summary | screen, print |
| Read Me | Honest description of the simulation and controls | default |
| Settings | Theme, sound, startup, display effects | saved, reset |

Do not force users through the boot terminal or Start menu to reach the content.

## 3. Domain profiles

A profile is a **lens over the same person**, not a separate identity or a fabricated second résumé. It lets a visitor see the same work through a selected specialization.

Recommended data model:

```js
const profiles = {
  ai: {
    label: "AI/ML",
    role: "AI/ML Engineer",
    tagline: "Retrieval, vision-language, and evaluation systems.",
    projectIds: ["atlas", "lumen", "evalbench"],
    focus: [{ title: "Retrieval", text: "Hybrid search and reranking." }],
    skillGroups: [{ title: "Retrieval & RAG", items: ["FAISS", "RRF"] }]
  }
};
```

Rules:

- Give every profile the same underlying facts, contact details, and availability.
- Filter **projects and skills** together; never show a project that contradicts the selected profile.
- Show a visible label such as “Viewing the AI/ML profile” and preserve a way back to **All**.
- Use icons to identify profiles only when they carry a text label as well.
- Keep the default profile broad enough to represent the whole portfolio. Do not bake a single specialty into the page title, meta description, Start menu, résumé, or availability line.
- Avoid proficiency bars and invented metrics. Let projects and outcomes show depth.
- When the visitor changes profile, update the About lens, Projects filter, Skills groups, status bar copy, and any profile-aware résumé summary.

These patterns are guidance for a portfolio you build; the bundled examples stay as neutral Windows mockups.

## 4. Project explorer

- Use a list or table for scanning and a persistent preview pane for context.
- Provide category/profile filters as real buttons with `aria-pressed`.
- Offer `All` plus one filter per profile; changing the profile should not strand an invisible project.
- Selecting a row updates the preview; double-click/Enter opens the detail view.
- Keep empty and filtered states explicit: “No projects match this profile.”
- Detail pages should include summary, measured facts, what was built, stack, media, and a back path. Do not put the only copy of essential content in images.
- Do not require drag, hover, or double-click for essential actions; always provide a button.

## 5. Window and taskbar behavior

- Modeless windows: opening a second window must not trap focus.
- One active window at a time, with visible active/inactive titlebar chrome.
- Caption buttons: minimize, maximize where useful, restore, close. Label each with the window name.
- The taskbar reflects every open window and restores minimized ones.
- Start closes on outside click and Escape; return focus to the Start button.
- On narrow screens, reflow windows to full-width panels and avoid a horizontal scrollbar. A single-window mobile stack is acceptable.
- Persist only preferences (theme, sound, startup), never transient open-window state.

## 6. Résumé and print

- Keep a dedicated print stylesheet; print only the résumé, not the desktop.
- Include name, role (broad or profile-neutral), email, GitHub, LinkedIn, location, summary, skills, experience, selected projects, and achievements.
- Use real headings and lists, not positioned text.
- Test `Ctrl+P` at A4 and confirm links remain readable.
- If profiles change the résumé, state which profile is active in the print heading.

## 7. Startup and theme switching

- Startup is optional; keep a visible Skip control and a preference to disable it.
- Never autoplay audio. If startup sound is requested, require a gesture and provide a mute control.
- Remember the selected era, but do not replay the full boot sequence on every route change.
- Theme changes must reach icons, wallpapers, Start marks, boot screens, taskbar, and custom-drawn app scenes — not just buttons and titlebars.
- Honor reduced motion and forced colors in the startup, CRT, and theme layers.
- Provide a boot-theme preview page; do not claim the site is an actual OS.

## 8. Asset checklist for a portfolio

- 30-icon shell family (computer, documents, folders, recycle bin, network, internet, email, search, settings, control panel, help, run, programs, briefcase, pictures, music, volume, mute, power, log off, user, task manager, AI, code, design, info, warning).
- Wallpaper and wallpaper fallback color at 1600×1000 and mobile crop.
- Start mark, brand mark, and site favicon.
- Window decorations at 16×16 plus hover/pressed states.
- One icon family per era; do not mix eras.
- Original or user-supplied boot art, with rights recorded.

The runtime ships these as original CC0 vectors. If a project needs authentic Microsoft artwork, follow [asset-sourcing.md](asset-sourcing.md): import it from the user's local reference and record the rights. Never hotlink it.
