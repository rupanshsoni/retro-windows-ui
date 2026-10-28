#!/usr/bin/env python3
"""Build and verify the original, offline retro-windows-ui assets.

Only Python's standard library is used. Output ordering and formatting are fixed;
no timestamps, random values, network resources, or platform fonts are embedded.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
import wave

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills" / "retro-windows-ui" / "assets"
THEME_IDS = (
    "classic",
    "xp-luna-blue",
    "xp-luna-olive",
    "xp-luna-silver",
    "windows-7-aero",
    "windows-7-basic",
)
ICON_NAMES = (
    "computer", "documents", "folder", "folder-open", "document", "recycle-bin",
    "recycle-bin-full", "network", "internet", "email", "search", "settings",
    "control-panel", "help", "run", "programs", "briefcase", "pictures", "music",
    "volume", "mute", "power", "logoff", "user", "task-manager", "ai", "code",
    "design", "info", "warning",
)
SHELL_ICON_NAMES = ICON_NAMES
DECORATION_NAMES = ("minimize", "maximize", "restore", "close")
WALLPAPER_NAMES = ("classic", "classic-95", "classic-98", "classic-2000", "xp-luna-blue", "xp-luna-olive", "xp-luna-silver", "windows-7-aero", "windows-7-basic")
AUTHOR = "retro-windows-ui contributors"
PROVENANCE_SVG = "Original programmatically authored vector artwork; no source artwork used."
PROVENANCE_AUDIO = "Original synthesized sine-wave composition; no sampled or prerecorded audio used."
PROVENANCE_CODE = "Original hand-authored offline HTML, CSS, and JavaScript example."
LICENSE = "CC0-1.0"


def jbytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def theme_pack(theme_id: str) -> dict:
    common = {
        "schemaVersion": "1.0.0",
        "identity": {
            "id": theme_id,
            "name": "",
            "family": "",
            "era": "",
            "variant": "default",
            "description": "",
        },
        "typography": {
            "fontFamily": "Tahoma, 'MS Sans Serif', Geneva, sans-serif",
            "fontFamilyMono": "'Courier New', Courier, monospace",
            "roles": {
                "body": {"size": "11px", "weight": 400, "lineHeight": "1.35"},
                "windowTitle": {"size": "11px", "weight": 700, "lineHeight": "1.1"},
                "menu": {"size": "11px", "weight": 400, "lineHeight": "1.25"},
                "small": {"size": "10px", "weight": 400, "lineHeight": "1.3"},
                "code": {"size": "11px", "weight": 400, "lineHeight": "1.4"},
            },
        },
        "colors": {},
        "metrics": {},
        "spacing": {"unit": "4px", "xs": "2px", "sm": "4px", "md": "8px", "lg": "12px", "xl": "16px", "xxl": "24px"},
        "radius": {},
        "gradients": {},
        "shadows": {},
        "motion": {},
        "contrastPairs": {},
        "assets": {
            "icons": f"../icons/{theme_id}/icons.svg",
            "decorations": f"../decorations/{theme_id}/decorations.svg",
            "texture": f"../textures/{theme_id}.svg",
            "wallpaper": f"../wallpapers/{theme_id}.svg",
            "startMark": f"../brand/{theme_id}-start.svg",
            "brandMark": f"../brand/{theme_id}-mark.svg",
            "bootExample": "../boot/index.html",
            "audio": {
                "activate": "../audio/activate.wav",
                "notify": "../audio/notify.wav",
                "complete": "../audio/complete.wav",
                "error": "../audio/error.wav",
            },
        },
    }
    p = common
    ident = p["identity"]
    c = p["colors"]
    p["metrics"] = {
        "controlHeight": "23px", "borderWidth": "2px", "bevelWidth": "2px",
        "titlebarHeight": "20px", "titlebarButtonSize": "16px", "taskbarHeight": "30px",
        "iconSize": "24px", "checkboxSize": "13px", "scrollbarWidth": "16px",
        "menuMinWidth": "176px", "focusOffset": "2px",
    }
    p["radius"] = {"none": "0px", "control": "0px", "window": "0px", "menu": "0px", "selection": "0px"}
    p["gradients"] = {
        "desktop": "#008080", "titleActive": "none", "titleInactive": "none",
        "button": "none", "taskbar": "none", "selection": "none", "progress": "none",
    }
    p["shadows"] = {"window": "4px 4px 0 rgb(0 0 0 / 35%)", "menu": "3px 3px 0 rgb(0 0 0 / 35%)", "focus": "none", "dialog": "6px 6px 0 rgb(0 0 0 / 40%)"}
    p["motion"] = {"durationFast": "0ms", "durationNormal": "0ms", "durationSlow": "0ms", "easing": "linear"}
    p["contrastPairs"] = {
        "body": {"foreground": "#000000", "background": "#d4d0c8", "minimumRatio": 4.5},
        "titlebar": {"foreground": "#ffffff", "background": "#000080", "minimumRatio": 4.5},
        "selection": {"foreground": "#ffffff", "background": "#000080", "minimumRatio": 4.5},
        "status": {"foreground": "#000000", "background": "#d4d0c8", "minimumRatio": 4.5},
    }

    if theme_id == "classic":
        ident.update(name="Classic", family="classic", era="Windows 95/98/2000", description="Square geometry, hard 3D bevels, flat colors, and immediate state changes.")
        c.update(
            surface={"desktop": "#008080", "window": "#d4d0c8", "windowSolid": "#d4d0c8", "control": "#d4d0c8", "input": "#ffffff", "inset": "#ffffff", "menu": "#d4d0c8", "tooltip": "#ffffe1", "overlay": "rgb(0 0 0 / 35%)"},
            text={"primary": "#000000", "secondary": "#303030", "muted": "#4c4c4c", "disabled": "#808080", "inverse": "#ffffff", "link": "#000080", "error": "#9c0006"},
            border={"default": "#404040", "light": "#ffffff", "dark": "#808080", "shadow": "#000000", "highlight": "#dfdfdf"},
            bevel={"outerLight": "#dfdfdf", "outerDark": "#0a0a0a", "innerLight": "#ffffff", "innerDark": "#808080", "pressedLight": "#808080", "pressedDark": "#ffffff"},
            selection={"background": "#000080", "text": "#ffffff", "inactiveBackground": "#808080", "inactiveText": "#ffffff"},
            focus={"color": "#000000", "ring": "1px dotted #000000", "alternate": "#ffffff"},
            titlebar={"activeBackground": "#000080", "activeBackgroundEnd": "#000080", "activeText": "#ffffff", "inactiveBackground": "#808080", "inactiveBackgroundEnd": "#808080", "inactiveText": "#d4d0c8", "button": "#d4d0c8", "buttonText": "#000000"},
            taskbar={"background": "#d4d0c8", "backgroundEnd": "#d4d0c8", "text": "#000000", "button": "#d4d0c8", "activeButton": "#ffffff", "activeText": "#000000"},
            status={"background": "#d4d0c8", "text": "#000000", "info": "#000080", "success": "#006400", "warning": "#7f6000", "error": "#9c0006"},
        )
    else:
        xp = theme_id.startswith("xp-")
        aero = theme_id == "windows-7-aero"
        basic = theme_id == "windows-7-basic"
        if xp:
            names = {
                "xp-luna-blue": ("Luna Blue", "blue", "#0058e6", "#3a93ff", "#0a246a", "#245edb", "#3f8cf3", "#eef4fb"),
                "xp-luna-olive": ("Luna Olive", "olive", "#6f8f3e", "#a9bd7d", "#253818", "#658c3b", "#9eb86d", "#f1f4e9"),
                "xp-luna-silver": ("Luna Silver", "silver", "#8d8da7", "#c7c7d4", "#182036", "#8d8da7", "#e3e3ed", "#f5f5f8"),
            }
            name, variant, title, title_end, dark, task, task_end, pale = names[theme_id]
            ident.update(name=name, family="xp-luna", era="Windows XP", variant=variant, description="Rounded Luna chrome, glossy controls, pill-like taskbar buttons, and short eased transitions.")
            title_text = "#ffffff" if variant != "silver" else "#10182c"
            task_text = "#ffffff"
            p["typography"]["roles"]["windowTitle"].update(size="12px", weight=700)
            p["metrics"].update(controlHeight="23px", borderWidth="1px", bevelWidth="1px", titlebarHeight="28px", titlebarButtonSize="21px", taskbarHeight="34px", checkboxSize="14px", focusOffset="3px")
            p["radius"].update(control="4px", window="8px", menu="3px", selection="2px")
            p["gradients"].update(
                desktop=f"linear-gradient(135deg, {dark}, {task} 55%, {pale})",
                titleActive=f"linear-gradient(180deg, {title_end} 0%, {title} 45%, {dark} 100%)",
                titleInactive="linear-gradient(180deg, #f3f3ed 0%, #c8c8bd 55%, #a8a89e 100%)",
                button="linear-gradient(180deg, #ffffff 0%, #f4f4ed 42%, #dcdcd1 100%)",
                taskbar=f"linear-gradient(180deg, {task_end} 0%, {task} 48%, {dark} 100%)",
                selection=f"linear-gradient(180deg, {title_end}, {title})",
                progress="linear-gradient(180deg, #b5ef8a, #42a52c 55%, #237a18)",
            )
            if variant == "silver":
                p["gradients"]["titleActive"] = "linear-gradient(180deg, #e3e3ed 0%, #c7c7d4 45%, #8d8da7 100%)"
            p["shadows"].update(window="3px 5px 12px rgb(0 0 0 / 42%)", menu="3px 4px 8px rgb(0 0 0 / 35%)", focus=f"0 0 0 2px {pale}", dialog="5px 8px 18px rgb(0 0 0 / 42%)")
            p["motion"].update(durationFast="80ms", durationNormal="140ms", durationSlow="220ms", easing="ease-out")
            c.update(
                surface={"desktop": task, "window": "#ece9d8", "windowSolid": "#ece9d8", "control": "#f8f8f2", "input": "#ffffff", "inset": "#ffffff", "menu": "#ffffff", "tooltip": "#ffffe1", "overlay": "rgb(0 0 0 / 32%)"},
                text={"primary": "#101010", "secondary": "#3e3e38", "muted": "#55554e", "disabled": "#8b8b80", "inverse": "#ffffff", "link": "#0645ad", "error": "#a40000"},
                border={"default": "#7f9db9" if variant == "blue" else dark, "light": "#ffffff", "dark": dark, "shadow": "#5d5d55", "highlight": pale},
                bevel={"outerLight": "#ffffff", "outerDark": dark, "innerLight": pale, "innerDark": "#b8b8aa", "pressedLight": dark, "pressedDark": "#ffffff"},
                selection={"background": title, "text": title_text, "inactiveBackground": "#c5c5ba", "inactiveText": "#3d3d38"},
                focus={"color": title if variant != "silver" else "#303b6c", "ring": f"1px dotted {dark}", "alternate": "#ffffff"},
                titlebar={"activeBackground": title, "activeBackgroundEnd": title_end, "activeText": title_text, "inactiveBackground": "#c8c8bd", "inactiveBackgroundEnd": "#f3f3ed", "inactiveText": "#5e5e58", "button": title_end if variant != "silver" else "#e8e8ef", "buttonText": title_text},
                taskbar={"background": task, "backgroundEnd": task_end, "text": task_text, "button": task_end, "activeButton": dark, "activeText": "#ffffff"},
                status={"background": "#ece9d8", "text": "#101010", "info": title, "success": "#287a1e", "warning": "#7a5200", "error": "#a40000"},
            )
            p["contrastPairs"] = {
                "body": {"foreground": "#101010", "background": "#ece9d8", "minimumRatio": 4.5},
                "titlebar": {"foreground": title_text, "background": dark if variant != "silver" else "#8d8da7", "minimumRatio": 4.5},
                "selection": {"foreground": title_text, "background": dark if variant != "silver" else "#8d8da7", "minimumRatio": 4.5},
                "status": {"foreground": "#101010", "background": "#ece9d8", "minimumRatio": 4.5},
            }
        else:
            ident.update(
                name="Windows 7 Aero" if aero else "Windows 7 Basic", family="windows-7", era="Windows 7",
                variant="aero" if aero else "basic",
                description="Translucent glass, soft highlights, and layered depth." if aero else "Opaque window chrome, flatter surfaces, and no blur or glass dependency.",
            )
            p["typography"].update(fontFamily="'Segoe UI', Tahoma, Geneva, sans-serif")
            p["typography"]["roles"]["body"].update(size="12px", lineHeight="1.4")
            p["typography"]["roles"]["windowTitle"].update(size="12px", weight=400)
            p["typography"]["roles"]["menu"].update(size="12px")
            p["metrics"].update(controlHeight="23px", borderWidth="1px", bevelWidth="1px", titlebarHeight="30px", titlebarButtonSize="28px", taskbarHeight="40px", checkboxSize="15px", scrollbarWidth="17px", focusOffset="3px")
            p["radius"].update(control="3px", window="8px" if aero else "5px", menu="4px", selection="2px")
            p["motion"].update(durationFast="100ms", durationNormal="180ms", durationSlow="280ms", easing="cubic-bezier(.2,.7,.2,1)")
            window = "rgb(239 248 252 / 82%)" if aero else "#f0f0f0"
            menu = "rgb(248 252 255 / 94%)" if aero else "#f0f0f0"
            task = "rgb(15 35 50 / 86%)" if aero else "#294c68"
            title = "rgb(220 240 250 / 66%)" if aero else "#456f96"
            title_text = "#102b40" if aero else "#ffffff"
            p["gradients"].update(
                desktop="radial-gradient(circle at 70% 20%, #4c89a9 0%, #214f70 42%, #102f4b 100%)" if aero else "linear-gradient(135deg, #527f9b, #244a68 60%, #183a56)",
                titleActive="linear-gradient(135deg, rgb(255 255 255 / 78%), rgb(174 217 237 / 42%))" if aero else "linear-gradient(180deg, #668faf, #345f86)",
                titleInactive="linear-gradient(180deg, rgb(242 246 248 / 72%), rgb(204 214 220 / 55%))" if aero else "linear-gradient(180deg, #c2cbd1, #9aa8b1)",
                button="linear-gradient(180deg, rgb(255 255 255 / 92%), rgb(218 235 244 / 76%))" if aero else "linear-gradient(180deg, #ffffff, #dcdcdc)",
                taskbar="linear-gradient(180deg, rgb(93 133 156 / 60%), rgb(7 23 35 / 90%))" if aero else "linear-gradient(180deg, #416a89, #203f58)",
                selection="linear-gradient(180deg, #dceffc, #a9d7f2)",
                progress="linear-gradient(180deg, #a9e9f5, #2ca8ca 55%, #167a9c)",
            )
            p["shadows"].update(
                window="0 12px 36px rgb(0 15 28 / 48%), 0 0 0 1px rgb(255 255 255 / 38%)" if aero else "0 5px 16px rgb(0 0 0 / 38%)",
                menu="0 6px 18px rgb(0 0 0 / 32%)", focus="0 0 5px rgb(77 177 220 / 75%)", dialog="0 16px 42px rgb(0 0 0 / 48%)",
            )
            c.update(
                surface={"desktop": "#214f70", "window": window, "windowSolid": "#eef3f5" if aero else "#f0f0f0", "control": "#f4f8fa" if aero else "#f0f0f0", "input": "#ffffff", "inset": "#ffffff", "menu": menu, "tooltip": "#ffffe1", "overlay": "rgb(3 18 30 / 42%)"},
                text={"primary": "#17232b", "secondary": "#34444e", "muted": "#4d5b63", "disabled": "#7b858a", "inverse": "#ffffff", "link": "#0645ad", "error": "#a40000"},
                border={"default": "#6f8794" if aero else "#707070", "light": "#ffffff", "dark": "#365265" if aero else "#4d4d4d", "shadow": "#243b49", "highlight": "#d9f0fa"},
                bevel={"outerLight": "#ffffff", "outerDark": "#547487" if aero else "#a0a0a0", "innerLight": "#eaf8ff", "innerDark": "#9db6c4" if aero else "#a0a0a0", "pressedLight": "#7faabd", "pressedDark": "#ffffff"},
                selection={"background": "#b7def3", "text": "#102b40", "inactiveBackground": "#d7dde0", "inactiveText": "#4b555b"},
                focus={"color": "#177da8", "ring": "1px dotted #176785", "alternate": "#ffffff"},
                titlebar={"activeBackground": title, "activeBackgroundEnd": "#a8d2e5" if aero else "#668faf", "activeText": title_text, "inactiveBackground": "#d5dde1", "inactiveBackgroundEnd": "#edf1f3", "inactiveText": "#53616a", "button": "#d7edf6" if aero else "#668faf", "buttonText": "#17394e" if aero else "#ffffff"},
                taskbar={"background": task, "backgroundEnd": "#527b93" if aero else "#416a89", "text": "#ffffff", "button": "#416a84" if aero else "#416a89", "activeButton": "#7298ad" if aero else "#668ca6", "activeText": "#ffffff"},
                status={"background": "#e5f0f5" if aero else "#f0f0f0", "text": "#17232b", "info": "#146b91", "success": "#26732d", "warning": "#795400", "error": "#a40000"},
            )
            p["contrastPairs"] = {
                "body": {"foreground": "#17232b", "background": "#eef3f5" if aero else "#f0f0f0", "minimumRatio": 4.5},
                "titlebar": {"foreground": title_text, "background": "#dceef5" if aero else "#456f96", "minimumRatio": 4.5},
                "selection": {"foreground": "#102b40", "background": "#b7def3", "minimumRatio": 4.5},
                "status": {"foreground": "#17232b", "background": "#e5f0f5" if aero else "#f0f0f0", "minimumRatio": 4.5},
            }
    return p


def schema() -> dict:
    color = {"type": "string", "minLength": 1}
    role = {
        "type": "object", "additionalProperties": False,
        "required": ["size", "weight", "lineHeight"],
        "properties": {"size": {"type": "string"}, "weight": {"type": "integer", "minimum": 100, "maximum": 900}, "lineHeight": {"type": "string"}},
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "./schema.json",
        "title": "retro-windows-ui semantic theme pack",
        "type": "object",
        "additionalProperties": False,
        "required": ["schemaVersion", "identity", "typography", "colors", "metrics", "spacing", "radius", "gradients", "shadows", "motion", "contrastPairs"],
        "properties": {
            "schemaVersion": {"const": "1.0.0"},
            "identity": {
                "type": "object", "additionalProperties": False,
                "required": ["id", "name", "family", "era", "variant", "description"],
                "properties": {"id": {"type": "string", "pattern": "^[a-z0-9-]+$"}, "name": {"type": "string"}, "family": {"enum": ["classic", "xp-luna", "windows-7"]}, "era": {"type": "string"}, "variant": {"type": "string"}, "description": {"type": "string"}},
            },
            "typography": {
                "type": "object", "additionalProperties": False, "required": ["fontFamily", "fontFamilyMono", "roles"],
                "properties": {"fontFamily": {"type": "string"}, "fontFamilyMono": {"type": "string"}, "roles": {"type": "object", "required": ["body", "windowTitle", "menu", "small", "code"], "properties": {name: role for name in ("body", "windowTitle", "menu", "small", "code")}, "additionalProperties": False}},
            },
            "colors": {
                "type": "object", "additionalProperties": False,
                "required": ["surface", "text", "border", "bevel", "selection", "focus", "titlebar", "taskbar", "status"],
                "properties": {name: {"type": "object", "minProperties": 1, "additionalProperties": color} for name in ("surface", "text", "border", "bevel", "selection", "focus", "titlebar", "taskbar", "status")},
            },
            "metrics": {"type": "object", "minProperties": 1, "additionalProperties": {"type": "string"}},
            "spacing": {"type": "object", "required": ["unit", "xs", "sm", "md", "lg", "xl", "xxl"], "additionalProperties": {"type": "string"}},
            "radius": {"type": "object", "required": ["none", "control", "window", "menu", "selection"], "additionalProperties": {"type": "string"}},
            "gradients": {"type": "object", "minProperties": 1, "additionalProperties": {"type": "string"}},
            "shadows": {"type": "object", "minProperties": 1, "additionalProperties": {"type": "string"}},
            "motion": {"type": "object", "required": ["durationFast", "durationNormal", "durationSlow", "easing"], "additionalProperties": {"type": "string"}},
            "contrastPairs": {
                "type": "object", "minProperties": 1,
                "additionalProperties": {"type": "object", "additionalProperties": False, "required": ["foreground", "background", "minimumRatio"], "properties": {"foreground": color, "background": color, "minimumRatio": {"type": "number", "minimum": 1, "maximum": 21}}},
            },
            "assets": {"type": "object", "minProperties": 1, "description": "Optional paths are relative to the theme pack file.", "additionalProperties": {"oneOf": [{"type": "string", "pattern": "^(?!https?:)"}, {"type": "object", "additionalProperties": {"type": "string", "pattern": "^(?!https?:)"}}]}},
        },
    }


def kebab(value: str) -> str:
    out = []
    for char in value:
        if char.isupper():
            out.append("-")
            out.append(char.lower())
        else:
            out.append(char)
    return "".join(out)


def themes_css(packs: dict[str, dict]) -> bytes:
    lines = [
        "/* Generated by tools/build_assets.py. Original CC0-1.0 theme values. */",
        ":root { color-scheme: light; }",
        "",
    ]
    for theme_id in THEME_IDS:
        p = packs[theme_id]
        t = p["typography"]
        lines.append(f'[data-theme="{theme_id}"] {{')
        lines.extend([
            f"  --rw-font-ui: {t['fontFamily']};",
            f"  --rw-font-mono: {t['fontFamilyMono']};",
            f"  --rw-font-size: {t['roles']['body']['size']};",
            f"  --rw-line-height: {t['roles']['body']['lineHeight']};",
            f"  --rw-title-size: {t['roles']['windowTitle']['size']};",
            f"  --rw-title-weight: {t['roles']['windowTitle']['weight']};",
            f"  --rw-small-size: {t['roles']['small']['size']};",
        ])
        for group, values in p["colors"].items():
            for key, value in values.items():
                lines.append(f"  --rw-{kebab(group)}-{kebab(key)}: {value};")
        for key, value in p["metrics"].items():
            lines.append(f"  --rw-{kebab(key)}: {value};")
        for key, value in p["spacing"].items():
            lines.append(f"  --rw-space-{kebab(key)}: {value};")
        for key, value in p["radius"].items():
            lines.append(f"  --rw-radius-{kebab(key)}: {value};")
        for key, value in p["gradients"].items():
            lines.append(f"  --rw-gradient-{kebab(key)}: {value};")
        for key, value in p["shadows"].items():
            lines.append(f"  --rw-shadow-{kebab(key)}: {value};")
        lines.extend([
            f"  --rw-motion-fast: {p['motion']['durationFast']};",
            f"  --rw-motion-normal: {p['motion']['durationNormal']};",
            f"  --rw-motion-slow: {p['motion']['durationSlow']};",
            f"  --rw-motion-easing: {p['motion']['easing']};",
            f'  --rw-texture: url("../textures/{theme_id}.svg");',
            f'  --rw-wallpaper: url("../wallpapers/{theme_id}.svg");',
            "  --rw-backdrop-filter: blur(12px) saturate(125%);" if theme_id == "windows-7-aero" else "  --rw-backdrop-filter: none;",
            "  --rw-control-style: glass;" if theme_id == "windows-7-aero" else ("  --rw-control-style: rounded;" if theme_id.startswith("xp-") or theme_id == "windows-7-basic" else "  --rw-control-style: bevel;"),
            "}",
            "",
        ])
    lines.extend([
        "/* User and OS accessibility overrides retain opaque, readable surfaces. */",
        '[data-theme][data-reduce-transparency="true"] {',
        "  --rw-surface-window: var(--rw-surface-window-solid);",
        "  --rw-surface-menu: var(--rw-surface-window-solid);",
        "  --rw-taskbar-background: #294c68;",
        "  --rw-titlebar-active-background: #456f96;",
        "  --rw-titlebar-active-text: #ffffff;",
        "  --rw-backdrop-filter: none;",
        "  --rw-texture: none;",
        "}",
        '[data-theme][data-reduce-motion="true"] {',
        "  --rw-motion-fast: 0ms; --rw-motion-normal: 0ms; --rw-motion-slow: 0ms;",
        "}",
        "@media (prefers-reduced-motion: reduce) {",
        "  [data-theme] { --rw-motion-fast: 0ms; --rw-motion-normal: 0ms; --rw-motion-slow: 0ms; }",
        "}",
        "",
    ])
    return "\n".join(lines).encode("utf-8")


def svg_document(content: str, width: int, height: int, label: str | None = None) -> bytes:
    aria = f' role="img" aria-label="{label}"' if label else ' aria-hidden="true"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"{aria}>\n{content}\n</svg>\n').encode("utf-8")


def icon_palette(theme_id: str) -> tuple[str, str, str, str, str]:
    if theme_id == "classic":
        return "#ffd867", "#fff4b0", "#ffffff", "#000080", "#000000"
    if theme_id == "xp-luna-blue":
        return "#f8ce45", "#fff2a0", "#f9fdff", "#2b72d6", "#17365e"
    if theme_id == "xp-luna-olive":
        return "#e8c955", "#fff1a5", "#fcfff7", "#6b913d", "#2f421c"
    if theme_id == "xp-luna-silver":
        return "#e6ca68", "#fff2b0", "#fdfdff", "#8585a5", "#30334b"
    if theme_id == "windows-7-aero":
        return "#f2c34e", "#fff0a1", "rgb(255 255 255 / 82%)", "#56a9cf", "#173c52"
    return "#e6b94f", "#f9dfa0", "#ffffff", "#4b86a9", "#233e50"


def icon_extra(theme_id: str) -> dict[str, str]:
    if theme_id == "classic":
        return {"screen": "#000080", "green": "#008000", "red": "#800000", "metal": "#c0c0c0", "line": "#ffffff"}
    if theme_id == "xp-luna-blue":
        return {"screen": "#2b72d6", "green": "#3f9e45", "red": "#c74631", "metal": "#d8d2c4", "line": "#ffffff"}
    if theme_id == "xp-luna-olive":
        return {"screen": "#6b913d", "green": "#3f8a35", "red": "#a8462f", "metal": "#ded8c8", "line": "#ffffff"}
    if theme_id == "xp-luna-silver":
        return {"screen": "#8585a5", "green": "#4b8a55", "red": "#a34a42", "metal": "#dedee8", "line": "#ffffff"}
    if theme_id == "windows-7-aero":
        return {"screen": "#3f9fd0", "green": "#4e9d59", "red": "#c05a4b", "metal": "#dce7ec", "line": "#ffffff"}
    return {"screen": "#4b86a9", "green": "#4e8e58", "red": "#a95146", "metal": "#d7dadd", "line": "#ffffff"}


def icon_defs(theme_id: str) -> str:
    gold, pale, paper, accent, ink = icon_palette(theme_id)
    prefix = theme_id
    extra = icon_extra(theme_id)
    soft = ".18" if theme_id == "windows-7-aero" else ".10"
    return f'''<defs>
  <linearGradient id="{prefix}-gold" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{pale}"/><stop offset="1" stop-color="{gold}"/></linearGradient>
  <linearGradient id="{prefix}-paper" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#ffffff"/><stop offset="1" stop-color="{paper}"/></linearGradient>
  <linearGradient id="{prefix}-accent" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{extra['line']}" stop-opacity=".55"/><stop offset=".45" stop-color="{accent}"/><stop offset="1" stop-color="{ink}"/></linearGradient>
  <linearGradient id="{prefix}-screen" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{extra['screen']}"/><stop offset="1" stop-color="{ink}"/></linearGradient>
  <filter id="{prefix}-soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="1" stdDeviation=".6" flood-color="{ink}" flood-opacity="{soft}"/></filter>
</defs>'''


def icon_shapes(theme_id: str, name: str) -> str:
    gold, pale, paper, accent, ink = icon_palette(theme_id)
    extra = icon_extra(theme_id)
    rounded = theme_id != "classic"
    rx = "2" if rounded else "0"
    stroke = "1.25" if theme_id == "classic" else "1"
    filt = "" if theme_id == "classic" else f' filter="url(#{theme_id}-soft)"'
    common = f'stroke="{ink}" stroke-width="{stroke}" stroke-linejoin="round"'
    if name == "computer":
        return f'''<g{filt} {common}>
<rect x="2" y="3" width="20" height="14" rx="{rx}" fill="{extra['metal']}"/>
<rect x="4" y="5" width="16" height="9" fill="url(#{theme_id}-screen)"/>
<path d="M6 7h6M6 9.5h4" stroke="{extra['line']}" opacity=".75"/>
<path d="M9 17v3M15 17v3M6.5 20h11" fill="none"/>
<circle cx="18.2" cy="6.3" r="1" fill="{extra['green']}" stroke-width=".7"/>
</g>'''
    if name == "documents":
        return f'''<g{filt} {common}>
<path d="M3 5h7l2 2h8v13H3Z" fill="url(#{theme_id}-gold)"/>
<path d="M7 3h9l3 3v12H7Z" fill="url(#{theme_id}-paper)"/>
<path d="M16 3v4h3M10 9h6M10 12h6M10 15h4" fill="none" stroke="{accent}"/>
</g>'''
    if name == "folder":
        return f'''<g{filt} stroke="{ink}" stroke-width="{stroke}" stroke-linejoin="round">
<path d="M2 6h7l2-3h8a2 2 0 0 1 2 2v4H2Z" fill="url(#{theme_id}-gold)"/>
<path d="M2 8h20l-2 12H4Z" fill="url(#{theme_id}-gold)"/>
<path d="M5 10h14" stroke="{pale}"/>
</g>'''
    if name == "folder-open":
        return f'''<g{filt} {common}>
<path d="M2 5h7l2-2h8a1 1 0 0 1 1 1v4H6L2 19Z" fill="url(#{theme_id}-gold)"/>
<path d="M6 9h16l-3 11H3Z" fill="url(#{theme_id}-paper)"/>
<path d="M8 11h12" stroke="{extra['line']}"/>
</g>'''
    if name == "document":
        return f'''<g{filt} stroke="{ink}" stroke-width="{stroke}" stroke-linejoin="round">
<path d="M5 2h10l4 4v16H5Z" fill="url(#{theme_id}-paper)"/>
<path d="M15 2v5h4" fill="{pale}"/>
<path d="M8 11h8M8 14h8M8 17h6" stroke="{accent}"/>
</g>'''
    if name in ("recycle-bin", "recycle-bin-full"):
        papers = ""
        if name == "recycle-bin-full":
            papers = f'''<path d="M7 9 9 5l2 3 2-4 2 4 2-3 1 5Z" fill="{paper}" stroke="{ink}" stroke-width=".8"/>'''
        return f'''<g{filt} {common}>
{papers}
<path d="M5 7h14l-1.4 14H6.4Z" fill="{extra['metal']}"/>
<path d="M4 7h16M9 7V4h6v3" fill="none"/>
<path d="M8.6 11h3.2l-1.6 2.2M15.4 14.5h-3.2l1.6-2.2M12 18v-2.8" fill="none" stroke="{extra['green']}" stroke-width="1.6"/>
<path d="M7 19h10" stroke="{ink}" opacity=".35"/>
</g>'''
    if name == "network":
        return f'''<g{filt} {common}>
<rect x="1.5" y="4" width="9" height="7" rx="{rx}" fill="{extra['metal']}"/>
<rect x="3" y="5.5" width="6" height="4" fill="url(#{theme_id}-screen)"/>
<rect x="13.5" y="13" width="9" height="7" rx="{rx}" fill="{extra['metal']}"/>
<rect x="15" y="14.5" width="6" height="4" fill="url(#{theme_id}-screen)"/>
<path d="M6 11v4h12v-2M6 15v3M18 15v-2" fill="none" stroke="{ink}" opacity=".7"/>
<circle cx="6" cy="15" r="1.3" fill="{gold}"/>
<circle cx="18" cy="13" r="1.3" fill="{extra['green']}"/>
</g>'''
    if name == "internet":
        return f'''<g{filt} stroke="{ink}" stroke-width="{stroke}">
<circle cx="12" cy="12" r="9" fill="url(#{theme_id}-screen)"/>
<path d="M6 7c2 1 4 0 5 1s-1 3-3 3-3-1-4-2ZM13 14c2-1 4 1 5 2s0 3-2 3-3-1-3-2Z" fill="{extra['green']}" stroke-width=".7"/>
<path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18" fill="none" stroke="{extra['line']}" opacity=".8" stroke-width=".8"/>
</g>'''
    if name == "email":
        return f'''<g{filt} {common}>
<rect x="2" y="5" width="20" height="14" rx="{rx}" fill="url(#{theme_id}-paper)"/>
<path d="m3 6 9 7 9-7M3 18l7-6M21 18l-7-6" fill="none" stroke="{accent}"/>
</g>'''
    if name == "search":
        return f'''<g{filt} fill="none" stroke="{ink}" stroke-width="2" stroke-linecap="round">
<circle cx="10" cy="10" r="6" fill="{paper}" stroke="{accent}"/>
<path d="m14.5 14.5 6 6" stroke="{ink}" stroke-width="3"/>
<path d="M7 7a4 4 0 0 1 4-2" stroke="{extra['line']}" stroke-width="1"/>
</g>'''
    if name == "settings":
        teeth = " ".join(f'<path d="M12 2v3" transform="rotate({a} 12 12)"/>' for a in range(0, 360, 45))
        return f'''<g{filt} stroke="{ink}" stroke-width="2.4" stroke-linecap="square">
{teeth}
<circle cx="12" cy="12" r="7" fill="{accent}"/>
<circle cx="12" cy="12" r="3" fill="{paper}" stroke-width="1"/>
</g>'''
    if name == "control-panel":
        return f'''<g{filt} {common}>
<rect x="3" y="4" width="18" height="16" rx="{rx}" fill="url(#{theme_id}-paper)"/>
<path d="M3 8h18" stroke="{accent}" stroke-width="2"/>
<path d="M7 12h10M7 16h10" fill="none" stroke="{ink}" opacity=".55"/>
<circle cx="10" cy="12" r="2" fill="url(#{theme_id}-gold)"/>
<circle cx="15" cy="16" r="2" fill="{extra['green']}"/>
</g>'''
    if name == "help":
        return f'''<g{filt} stroke="{ink}" stroke-width="{stroke}">
<circle cx="12" cy="12" r="9" fill="url(#{theme_id}-accent)"/>
<path d="M9 9a3 3 0 1 1 4.8 2.5c-.8.6-1.8 1.1-1.8 2.5" fill="none" stroke="{extra['line']}" stroke-width="2" stroke-linecap="round"/>
<circle cx="12" cy="18" r="1.2" fill="{extra['line']}" stroke="none"/>
</g>'''
    if name == "run":
        return f'''<g{filt} {common}>
<rect x="2" y="4" width="20" height="16" rx="{rx}" fill="url(#{theme_id}-paper)"/>
<path d="M2 4h20v4H2Z" fill="url(#{theme_id}-accent)"/>
<path d="m6 11 3 2.5L6 16M11 16h5" fill="none" stroke="{extra['green']}" stroke-width="1.8" stroke-linecap="round"/>
</g>'''
    if name == "programs":
        return f'''<g{filt} {common}>
<rect x="2" y="4" width="20" height="16" rx="{rx}" fill="url(#{theme_id}-paper)"/>
<path d="M2 4h20v4H2Z" fill="url(#{theme_id}-accent)"/>
<rect x="5" y="10" width="6" height="4" fill="{extra['green']}"/>
<rect x="13" y="10" width="6" height="4" fill="url(#{theme_id}-gold)"/>
<rect x="5" y="16" width="6" height="2.5" fill="{extra['red']}"/>
<rect x="13" y="16" width="6" height="2.5" fill="{accent}"/>
</g>'''
    if name == "briefcase":
        return f'''<g{filt} {common}>
<path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" fill="none"/>
<rect x="2" y="7" width="20" height="13" rx="{rx}" fill="url(#{theme_id}-accent)"/>
<path d="M2 12h20M10 12v2h4v-2" fill="none" stroke="{extra['line']}" opacity=".8"/>
</g>'''
    if name == "pictures":
        return f'''<g{filt} {common}>
<rect x="2" y="4" width="20" height="16" rx="{rx}" fill="url(#{theme_id}-paper)"/>
<rect x="4" y="6" width="16" height="12" fill="{extra['screen']}"/>
<circle cx="8" cy="9.5" r="1.8" fill="{gold}" stroke="none"/>
<path d="m4 16 5-5 3 3 3-3 5 5v2H4Z" fill="{extra['green']}" stroke-width=".8"/>
</g>'''
    if name == "music":
        return f'''<g{filt} {common}>
<circle cx="12" cy="12" r="9" fill="url(#{theme_id}-accent)"/>
<circle cx="12" cy="12" r="2.2" fill="{paper}" stroke-width=".8"/>
<path d="M14 6v7.5M14 6l4 1" fill="none" stroke="{extra['line']}" stroke-width="1.8" stroke-linecap="round"/>
<circle cx="12.5" cy="14.5" r="1.8" fill="{extra['line']}" stroke="none"/>
</g>'''
    if name in ("volume", "mute"):
        wave = f'''<path d="M15 9c1.5 1.5 1.5 4.5 0 6M17.5 7c2.5 2.5 2.5 7.5 0 10" fill="none" stroke="{accent}" stroke-width="1.5" stroke-linecap="round"/>''' if name == "volume" else f'''<path d="m15 9 5 6m0-6-5 6" fill="none" stroke="{extra['red']}" stroke-width="1.8" stroke-linecap="round"/>'''
        return f'''<g{filt} {common}>
<path d="M3 9h4l5-4v14l-5-4H3Z" fill="url(#{theme_id}-paper)"/>
{wave}
</g>'''
    if name == "power":
        return f'''<g{filt} fill="none" stroke="{ink}" stroke-width="1.6">
<circle cx="12" cy="13" r="7" fill="{paper}" stroke="{extra['green']}" stroke-width="2"/>
<path d="M12 5v7" stroke="{extra['green']}" stroke-width="2.2" stroke-linecap="round"/>
</g>'''
    if name == "logoff":
        return f'''<g{filt} {common}>
<path d="M4 3h9v18H4Z" fill="url(#{theme_id}-paper)"/>
<path d="M13 12h7M17 9l3 3-3 3" fill="none" stroke="{extra['green']}" stroke-width="1.8" stroke-linecap="round"/>
<circle cx="10" cy="12" r="1" fill="{ink}" stroke="none"/>
</g>'''
    if name == "user":
        return f'''<g{filt} {common}>
<circle cx="12" cy="8" r="4" fill="{extra['metal']}"/>
<path d="M4 21c.6-4.2 3.6-6 8-6s7.4 1.8 8 6Z" fill="url(#{theme_id}-accent)"/>
</g>'''
    if name == "task-manager":
        return f'''<g{filt} {common}>
<rect x="2" y="4" width="20" height="16" rx="{rx}" fill="url(#{theme_id}-paper)"/>
<path d="M2 4h20v4H2Z" fill="url(#{theme_id}-accent)"/>
<path d="M6 16V12M10 16V9M14 16v-3M18 16V7" stroke="{extra['green']}" stroke-width="2" stroke-linecap="square"/>
<path d="M5 16h14" stroke="{ink}" opacity=".4"/>
</g>'''
    if name == "ai":
        return f'''<g{filt} {common}>
<rect x="6" y="6" width="12" height="12" rx="{rx}" fill="url(#{theme_id}-accent)"/>
<rect x="9" y="9" width="6" height="6" fill="url(#{theme_id}-paper)"/>
<path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4" fill="none" stroke="{ink}" stroke-width="1.4"/>
<circle cx="12" cy="12" r="1.2" fill="{extra['green']}" stroke="none"/>
</g>'''
    if name == "code":
        return f'''<g{filt} {common}>
<rect x="2" y="4" width="20" height="16" rx="{rx}" fill="url(#{theme_id}-paper)"/>
<path d="M2 4h20v4H2Z" fill="url(#{theme_id}-accent)"/>
<path d="M9 10 6 13l3 3M15 10l3 3-3 3M13 9l-2 8" fill="none" stroke="{extra['green']}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
</g>'''
    if name == "design":
        return f'''<g{filt} {common}>
<rect x="3" y="3" width="18" height="18" rx="{rx}" fill="url(#{theme_id}-paper)"/>
<path d="m7 17 7-9 3 3-7 9H7Z" fill="url(#{theme_id}-gold)"/>
<path d="m14 8 3 3" stroke="{ink}" stroke-width="1"/>
<circle cx="17" cy="7" r="2" fill="{accent}"/>
<circle cx="7" cy="7" r="1.4" fill="{extra['green']}" stroke="none"/>
</g>'''
    if name == "info":
        return f'''<g{filt} stroke="{ink}" stroke-width="{stroke}">
<circle cx="12" cy="12" r="9" fill="{accent}"/>
<circle cx="12" cy="7" r="1.3" fill="{extra['line']}" stroke="none"/>
<path d="M12 11v6" stroke="{extra['line']}" stroke-width="2.2" stroke-linecap="round"/>
</g>'''
    if name == "warning":
        return f'''<g{filt} stroke="{ink}" stroke-width="{stroke}" stroke-linejoin="round">
<path d="M12 2 23 21H1Z" fill="url(#{theme_id}-gold)"/>
<path d="M12 8v6" stroke-width="2.2" stroke-linecap="round"/>
<circle cx="12" cy="17.5" r="1.2" fill="{ink}" stroke="none"/>
</g>'''
    raise ValueError(name)


def make_icon_assets(outputs: dict[str, bytes]) -> None:
    for theme_id in THEME_IDS:
        defs = icon_defs(theme_id)
        symbols = []
        for name in ICON_NAMES:
            content = defs + "\n" + icon_shapes(theme_id, name)
            outputs[f"icons/{theme_id}/{name}.svg"] = svg_document(content, 24, 24, f"{theme_id} {name}")
            symbols.append(f'<symbol id="{name}" viewBox="0 0 24 24">\n{icon_shapes(theme_id, name)}\n</symbol>')
        sprite = '<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true">\n' + defs + "\n" + "\n".join(symbols) + "\n</svg>\n"
        outputs[f"icons/{theme_id}/icons.svg"] = sprite.encode("utf-8")


def decoration_shapes(theme_id: str, name: str) -> str:
    classic = theme_id == "classic"
    aero = theme_id == "windows-7-aero"
    color = "#000000" if classic else ("#173c52" if aero or theme_id == "xp-luna-silver" else "#ffffff")
    outline = "" if classic else ' stroke="#ffffff" stroke-width="2.8" stroke-opacity=".55"'
    width = "1.6" if classic else "1.5"
    if name == "minimize":
        shape = '<path d="M4 11h8"/>'
    elif name == "maximize":
        shape = '<rect x="4" y="4" width="9" height="8"/>'
    elif name == "restore":
        shape = '<path d="M6 4h7v6M4 7h7v7H4Z"/>'
    elif name == "close":
        shape = '<path d="m5 5 7 7m0-7-7 7"/>'
    else:
        raise ValueError(name)
    return f'<g fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="square" stroke-linejoin="miter">{shape}</g>' + (f'<g fill="none"{outline} stroke-linecap="round">{shape}</g>' if outline else "")


def make_decoration_assets(outputs: dict[str, bytes]) -> None:
    for theme_id in THEME_IDS:
        symbols = []
        for name in DECORATION_NAMES:
            outputs[f"decorations/{theme_id}/{name}.svg"] = svg_document(decoration_shapes(theme_id, name), 16, 16, f"{theme_id} {name}")
            symbols.append(f'<symbol id="{name}" viewBox="0 0 16 16">\n{decoration_shapes(theme_id, name)}\n</symbol>')
        outputs[f"decorations/{theme_id}/decorations.svg"] = ('<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true">\n' + "\n".join(symbols) + "\n</svg>\n").encode("utf-8")


def wallpaper_svg(theme_id: str) -> bytes:
    if theme_id in ("classic", "classic-95"):
        content = '''<defs>
<pattern id="dither" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="#008080"/><path d="M0 0h1v1H0Zm2 2h1v1H2Z" fill="#ffffff" opacity=".035"/></pattern>
<radialGradient id="soft" cx="50%" cy="38%" r="65%"><stop stop-color="#0f9b9b"/><stop offset="1" stop-color="#006e6e"/></radialGradient>
</defs>
<rect width="1600" height="1000" fill="url(#soft)"/><rect width="1600" height="1000" fill="url(#dither)"/>
<path d="M0 780q400-70 800 0t800 0v220H0Z" fill="#006666" opacity=".25"/>'''
        return svg_document(content, 1600, 1000, "Original Classic teal desktop wallpaper")
    if theme_id == "classic-98":
        content = '''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#1b66b8"/><stop offset=".55" stop-color="#6ba9df"/><stop offset="1" stop-color="#c5e3f7"/></linearGradient>
<linearGradient id="field" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#4c9b46"/><stop offset="1" stop-color="#1f6529"/></linearGradient>
</defs>
<rect width="1600" height="1000" fill="url(#sky)"/>
<g fill="#ffffff" opacity=".8"><ellipse cx="260" cy="220" rx="170" ry="52"/><ellipse cx="360" cy="190" rx="110" ry="42"/><ellipse cx="1150" cy="300" rx="210" ry="58"/><ellipse cx="1290" cy="268" rx="120" ry="38"/></g>
<path d="M0 700q320-130 640-20t960-10v330H0Z" fill="url(#field)"/>
<path d="M0 790q400-90 780 10t820-20v220H0Z" fill="#1c5925" opacity=".65"/>'''
        return svg_document(content, 1600, 1000, "Original cloudy Classic desktop wallpaper")
    if theme_id == "classic-2000":
        content = '''<defs>
<linearGradient id="blue" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0a2f66"/><stop offset=".5" stop-color="#23629e"/><stop offset="1" stop-color="#7fb6cf"/></linearGradient>
<linearGradient id="wave" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ffffff" stop-opacity=".22"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
</defs>
<rect width="1600" height="1000" fill="url(#blue)"/>
<path d="M-80 780c260-240 480-260 820-60s600 170 940-80v360H-80Z" fill="#0c3c75" opacity=".55"/>
<path d="M-50 690c300-210 520-200 840 20s620 160 860-60" fill="none" stroke="url(#wave)" stroke-width="120"/>
<path d="M0 120h1600M0 220h1600" stroke="#ffffff" stroke-opacity=".04" stroke-width="2"/>'''
        return svg_document(content, 1600, 1000, "Original Windows 2000 inspired blue wallpaper")
    if theme_id.startswith("xp-"):
        pack = theme_pack(theme_id)
        task = pack["colors"]["taskbar"]["background"]
        task_end = pack["colors"]["taskbar"]["backgroundEnd"]
        if theme_id == "xp-luna-blue":
            sky_top, sky_bottom = "#2d7bd8", "#c9e9ff"
            hill_far, hill_near = "#6cae3b", "#2f6b1f"
            sun = "#fff4c2"
        elif theme_id == "xp-luna-olive":
            sky_top, sky_bottom = "#e2a949", "#f7e4b1"
            hill_far, hill_near = "#84984a", "#41541f"
            sun = "#fff1b8"
        else:
            sky_top, sky_bottom = "#9cabb9", "#e8eef3"
            hill_far, hill_near = "#8f9ca7", "#4f5e69"
            sun = "#ffffff"
        content = f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{sky_top}"/><stop offset=".62" stop-color="{sky_bottom}"/></linearGradient>
<linearGradient id="hillFar" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{hill_far}"/><stop offset="1" stop-color="{hill_near}"/></linearGradient>
<linearGradient id="haze" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{sun}" stop-opacity=".4"/><stop offset="1" stop-color="{sun}" stop-opacity="0"/></linearGradient>
<radialGradient id="sun" cx="76%" cy="18%" r="30%"><stop stop-color="{sun}" stop-opacity=".9"/><stop offset="1" stop-color="{sun}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1600" height="1000" fill="url(#sky)"/><rect width="1600" height="1000" fill="url(#sun)"/>
<g fill="#ffffff" opacity=".55"><ellipse cx="310" cy="220" rx="180" ry="48"/><ellipse cx="420" cy="192" rx="130" ry="38"/><ellipse cx="1060" cy="160" rx="160" ry="40"/></g>
<path d="M0 610c260-90 430-50 620-120 230-85 430-40 610 10 150 42 270 20 370-12v512H0Z" fill="url(#hillFar)"/>
<path d="M0 760c240-110 480-80 720-10s560 72 880-34v284H0Z" fill="{hill_near}" opacity=".75"/>
<path d="M0 680h1600v320H0Z" fill="url(#haze)"/>
<rect y="986" width="1600" height="14" fill="{task}"/><rect y="982" width="1600" height="4" fill="{task_end}" opacity=".7"/>'''
        return svg_document(content, 1600, 1000, f"Original {pack['identity']['name']} inspired wallpaper")
    if theme_id == "windows-7-aero":
        content = '''<defs>
<radialGradient id="deep" cx="52%" cy="34%" r="82%"><stop stop-color="#1d638f"/><stop offset=".48" stop-color="#0c3151"/><stop offset="1" stop-color="#041321"/></radialGradient>
<linearGradient id="aurora" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#78e3ff" stop-opacity=".55"/><stop offset=".45" stop-color="#2f9fd8" stop-opacity=".16"/><stop offset="1" stop-color="#b7ffd9" stop-opacity="0"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#68c7ee" stop-opacity=".38"/><stop offset="1" stop-color="#03101b" stop-opacity="0"/></linearGradient>
</defs>
<rect width="1600" height="1000" fill="url(#deep)"/>
<path d="M-80 610C280 380 520 470 760 420s500-190 920-40v460H-80Z" fill="url(#aurora)"/>
<path d="M-50 760c340-170 620-150 900-40s620 80 800-30v310H-50Z" fill="url(#floor)"/>
<path d="M0 690h1600" stroke="#bdeeff" stroke-opacity=".16"/>
<g fill="#d8f7ff" opacity=".55"><circle cx="220" cy="180" r="2"/><circle cx="480" cy="110" r="1.5"/><circle cx="1180" cy="140" r="2"/><circle cx="1390" cy="260" r="1.5"/><circle cx="960" cy="80" r="1"/></g>'''
        return svg_document(content, 1600, 1000, "Original Windows 7 Aero inspired aurora wallpaper")
    content = '''<defs>
<linearGradient id="deep" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#17415f"/><stop offset=".55" stop-color="#214f70"/><stop offset="1" stop-color="#0a2233"/></linearGradient>
<linearGradient id="stripe" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#ffffff" stop-opacity=".1"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
</defs>
<rect width="1600" height="1000" fill="url(#deep)"/>
<path d="M-100 900 700 300h260L160 980Z" fill="url(#stripe)"/>
<path d="M200 1000 1080 220h120L420 1000Z" fill="#ffffff" opacity=".03"/>
<rect y="900" width="1600" height="100" fill="#071c2b" opacity=".4"/>'''
    return svg_document(content, 1600, 1000, "Original Windows 7 Basic inspired wallpaper")


def make_wallpaper_assets(outputs: dict[str, bytes]) -> None:
    for name in WALLPAPER_NAMES:
        outputs[f"wallpapers/{name}.svg"] = wallpaper_svg(name)


def brand_mark(theme_id: str, size: int) -> bytes:
    gold, pale, paper, accent, ink = icon_palette(theme_id)
    classic = theme_id == "classic"
    radius = "0" if classic else "12"
    inner_radius = "0" if classic else "4"
    border = "3" if classic else "2"
    gloss = "" if classic else '<path d="M8 8h48v20c-12 8-36 8-48 0Z" fill="#ffffff" opacity=".14"/>'
    content = f'''<defs>
<linearGradient id="brand" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{accent}"/><stop offset=".55" stop-color="{ink}"/><stop offset="1" stop-color="#051018"/></linearGradient>
<linearGradient id="screen" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{paper}"/><stop offset="1" stop-color="{pale}"/></linearGradient>
</defs>
<rect x="2" y="2" width="60" height="60" rx="{radius}" fill="url(#brand)" stroke="{ink}" stroke-width="{border}"/>
{gloss}
<rect x="11" y="13" width="42" height="38" rx="{inner_radius}" fill="url(#screen)" stroke="{ink}" stroke-width="{border}"/>
<path d="M11 22h42" stroke="{ink}" stroke-width="{border}"/>
<rect x="15" y="15.5" width="5" height="4" fill="{gold}" stroke="{ink}" stroke-width="1"/>
<rect x="22" y="15.5" width="5" height="4" fill="{accent}" stroke="{ink}" stroke-width="1"/>
<path d="M17 30h22M17 36h16" stroke="{accent}" stroke-width="2.5" stroke-linecap="square"/>
<path d="m28 39 9 4-3.5 1.2L35 47l-2 .8-1.5-2.8L29 46Z" fill="{gold}" stroke="{ink}" stroke-width="1.5" stroke-linejoin="round"/>'''
    if size == 64:
        return svg_document(content, 64, 64, f"{theme_id} original window mark")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 64 64" role="img" aria-label="{theme_id} start mark">\n{content}\n</svg>\n').encode("utf-8")


def make_brand_assets(outputs: dict[str, bytes]) -> None:
    for theme_id in THEME_IDS:
        outputs[f"brand/{theme_id}-mark.svg"] = brand_mark(theme_id, 64)
        outputs[f"brand/{theme_id}-start.svg"] = brand_mark(theme_id, 24)


def make_texture_assets(outputs: dict[str, bytes]) -> None:
    for theme_id in THEME_IDS:
        if theme_id == "classic":
            content = '''<defs><pattern id="dither" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="#008080"/><path d="M0 0h1v1H0Zm2 2h1v1H2Z" fill="#ffffff" opacity=".035"/></pattern></defs>
<rect width="8" height="8" fill="url(#dither)"/>'''
            outputs[f"textures/{theme_id}.svg"] = svg_document(content, 8, 8)
        elif theme_id.startswith("xp-"):
            pack = theme_pack(theme_id)
            a = pack["colors"]["titlebar"]["activeBackground"]
            b = pack["colors"]["titlebar"]["activeBackgroundEnd"]
            content = f'''<defs><linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{a}"/><stop offset=".55" stop-color="{b}"/><stop offset="1" stop-color="{a}"/></linearGradient></defs>
<rect width="64" height="64" fill="url(#sheen)"/><path d="M0 20Q32 2 64 20V0H0Z" fill="#fff" opacity=".08"/><path d="M0 48Q32 30 64 48" fill="none" stroke="#fff" opacity=".06"/>'''
            outputs[f"textures/{theme_id}.svg"] = svg_document(content, 64, 64)
        elif theme_id == "windows-7-aero":
            content = '''<defs><linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#bce8f4" stop-opacity=".22"/><stop offset=".5" stop-color="#5ba4c3" stop-opacity=".05"/><stop offset="1" stop-color="#ffffff" stop-opacity=".16"/></linearGradient></defs>
<rect width="96" height="96" fill="url(#glass)"/><path d="M-20 70 70-20M18 108 108 18" stroke="#fff" stroke-width="12" opacity=".07"/><circle cx="75" cy="20" r="35" fill="none" stroke="#d9f7ff" opacity=".08"/>'''
            outputs[f"textures/{theme_id}.svg"] = svg_document(content, 96, 96)
        else:
            content = '''<defs><pattern id="weave" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#527f9b"/><path d="M0 1h8M1 0v8" stroke="#fff" opacity=".025"/></pattern></defs>
<rect width="8" height="8" fill="url(#weave)"/>'''
            outputs[f"textures/{theme_id}.svg"] = svg_document(content, 8, 8)


def synthesize(name: str) -> bytes:
    sample_rate = 44100
    # Short, original motifs. Each voice is normalized before the safety envelope.
    recipes = {
        "activate": (0.20, [(0.00, 0.10, 392.0), (0.07, 0.12, 587.33)]),
        "notify": (0.34, [(0.00, 0.18, 659.25), (0.13, 0.19, 880.0)]),
        "complete": (0.52, [(0.00, 0.18, 440.0), (0.12, 0.18, 554.37), (0.24, 0.25, 739.99)]),
        "error": (0.32, [(0.00, 0.22, 246.94), (0.08, 0.22, 233.08)]),
    }
    duration, voices = recipes[name]
    count = int(sample_rate * duration)
    samples = []
    for index in range(count):
        t = index / sample_rate
        value = 0.0
        for start, length, frequency in voices:
            local = t - start
            if 0 <= local < length:
                attack = min(1.0, local / 0.008)
                release = min(1.0, (length - local) / 0.035)
                env = max(0.0, min(attack, release))
                value += math.sin(2 * math.pi * frequency * local) * env
        # A subtle second harmonic gives a clean electronic timbre, not a recorded cue.
        value = math.tanh(value * 0.72) * 0.62
        edge = min(1.0, t / 0.006, (duration - t) / 0.025)
        value *= max(0.0, edge)
        samples.append(max(-32767, min(32767, round(value * 32767))))
    import io
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(struct.pack("<" + "h" * len(samples), *samples))
    return buffer.getvalue()


def audio_metadata(data: bytes) -> dict:
    import io
    with wave.open(io.BytesIO(data), "rb") as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        width = wav.getsampwidth()
        channels = wav.getnchannels()
        raw = wav.readframes(frames)
    values = struct.unpack("<" + "h" * (len(raw) // 2), raw)
    return {
        "durationSeconds": round(frames / rate, 6), "sampleRate": rate,
        "channels": channels, "bitsPerSample": width * 8, "frames": frames,
        "peakAmplitude": max(abs(value) for value in values), "clippedSamples": sum(abs(value) >= 32767 for value in values),
    }


def contact_sheet() -> bytes:
    sections = []
    for theme_id in THEME_IDS:
        pack = theme_pack(theme_id)
        icons = "".join(f'<figure><img src="icons/{theme_id}/{name}.svg" width="32" height="32" alt="{name}"><figcaption>{name}</figcaption></figure>' for name in ICON_NAMES)
        decorations = "".join(f'<img src="decorations/{theme_id}/{name}.svg" width="20" height="20" alt="{name}" title="{name}">' for name in DECORATION_NAMES)
        sections.append(f'''<section class="theme-card" data-theme="{theme_id}">
<h2>{pack['identity']['name']}</h2><p>{pack['identity']['era']} / {pack['identity']['variant']}</p>
<div class="icons">{icons}</div><div class="decorations" aria-label="Window decoration glyphs">{decorations}</div>
<div class="brands"><img src="brand/{theme_id}-mark.svg" width="48" height="48" alt="{theme_id} brand mark"><img src="brand/{theme_id}-start.svg" width="24" height="24" alt="{theme_id} start mark"><span>Brand + start marks</span></div>
<div class="previews"><div class="texture" style="background-image:url('textures/{theme_id}.svg')"><span>Original subtle texture</span></div><div class="wallpaper" style="background-image:url('wallpapers/{theme_id}.svg')"><span>Original desktop wallpaper</span></div></div>
</section>''')
    audio = "".join(f'''<tr><th scope="row">{name}.wav</th><td><audio controls preload="none" src="audio/{name}.wav">Audio cue: {name}.wav</audio></td><td>Original deterministic PCM16 synthesis; CC0-1.0; no Windows audio sampled or imitated.</td></tr>''' for name in ("activate", "notify", "complete", "error"))
    html = f'''<!doctype html>
<html lang="en" data-theme="classic">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Retro Windows UI — Asset Contact Sheet</title>
<link rel="stylesheet" href="tokens/themes.css">
<style>
*{{box-sizing:border-box}}body{{margin:0;padding:24px;background:#e7e7e7;color:#171717;font:14px/1.45 Tahoma,'Segoe UI',sans-serif}}header,section,table{{max-width:1180px;margin:auto}}h1{{margin:0 0 6px}}a{{color:#0645ad}}.theme-card{{padding:18px;margin:20px 0;background:var(--rw-surface-window);border:2px solid var(--rw-border-default);border-radius:var(--rw-radius-window);box-shadow:var(--rw-shadow-window);backdrop-filter:var(--rw-backdrop-filter)}}.theme-card h2{{font:var(--rw-title-weight) var(--rw-title-size)/1.2 var(--rw-font-ui);margin:0}}.theme-card p{{margin:3px 0 14px;color:var(--rw-text-secondary)}}.icons{{display:flex;flex-wrap:wrap;gap:10px}}figure{{margin:0;width:68px;text-align:center}}figure img{{display:block;margin:auto;image-rendering:auto}}figcaption{{font-size:11px;margin-top:4px}}.decorations{{display:flex;gap:8px;padding:10px 0}}.decorations img{{background:var(--rw-titlebar-active-background);padding:2px;border-radius:2px}}.brands{{display:flex;align-items:center;gap:8px;padding:4px 0}}.brands img{{image-rendering:auto}}.brands span{{color:var(--rw-text-secondary);font-size:11px}}.previews{{display:grid;grid-template-columns:minmax(160px,.45fr) minmax(260px,1fr);gap:10px}}.texture,.wallpaper{{height:108px;border:1px solid var(--rw-border-default);display:flex;align-items:end;padding:6px;background-position:center;background-size:cover}}.texture{{background-size:96px}}.texture span,.wallpaper span{{background:#fff;color:#111;padding:2px 5px}}table{{width:100%;border-collapse:collapse;background:#fff;margin-top:20px}}th,td{{padding:10px;border:1px solid #aaa;text-align:left;vertical-align:middle}}th{{width:130px}}audio{{max-width:100%;height:32px}}footer{{max-width:1180px;margin:22px auto}}@media(max-width:600px){{body{{padding:12px}}td{{display:block}}th{{display:block;width:auto}}audio{{width:100%}}.previews{{grid-template-columns:1fr}}}}
</style></head>
<body><header><h1>Retro Windows UI asset contact sheet</h1><p>Six original theme families, a complete shell icon set, textures, wallpapers, start marks, and opt-in audio. No remote resources.</p><nav><a href="starter/index.html">Starter example</a> · <a href="desktop/index.html">Default desktop mockup</a> · <a href="boot/index.html">Startup screens</a> · <a href="gallery/index.html">Interactive gallery</a> · <a href="manifest.json">Manifest</a> · <a href="LICENSE.txt">CC0 and independence notice</a></nav></header>
{''.join(sections)}
<section aria-labelledby="audio-title"><h2 id="audio-title">Audio cues</h2><p>Audio never autoplays. Use the controls to audition each original cue.</p><table><thead><tr><th>File</th><th>Local preview</th><th>Provenance</th></tr></thead><tbody>{audio}</tbody></table></section>
<footer>Independent, unofficial interface study. Microsoft and Windows are trademarks of their respective owners; no proprietary assets are included.</footer></body></html>
'''
    return html.encode("utf-8")


LICENSE_TEXT = """Retro Windows UI — Original Asset Dedication

Copyright status of original assets in this directory:
To the extent possible under law, the retro-windows-ui contributors have waived
all copyright and related or neighboring rights to the original SVG artwork,
WAV sound cues, token values, and generated presentation assets in this
directory under Creative Commons CC0 1.0 Universal (CC0-1.0).

You may copy, modify, distribute, and use these original assets, including for
commercial purposes, without asking permission. This dedication does not grant
rights to third-party trademarks or to fonts installed on your computer.

CC0 legal code: https://creativecommons.org/publicdomain/zero/1.0/
SPDX-License-Identifier: CC0-1.0

Independent / unofficial notice:
This is an independent, unofficial interface study. It is not affiliated with,
endorsed by, or sponsored by Microsoft. Microsoft and Windows are trademarks of
their respective owners. No Microsoft font files, logos, extracted icons,
wallpapers, traced proprietary artwork, or original Windows sounds are included.
The interface artwork and audio are original implementations. Font names refer
only to local system font stacks; no font software is distributed here.

Provenance:
SVG and WAV assets are deterministically generated by tools/build_assets.py.
The starter, default desktop mockup, boot screens, and gallery are original
hand-authored offline examples. Consult manifest.json for per-file provenance,
media metadata, byte sizes, and SHA256.
"""


def media_type(path: str) -> str:
    suffix = Path(path).suffix.lower()
    return {
        ".svg": "image/svg+xml", ".wav": "audio/wav", ".json": "application/json",
        ".css": "text/css", ".html": "text/html", ".js": "text/javascript", ".txt": "text/plain",
    }.get(suffix, "application/octet-stream")


def asset_kind(path: str) -> str:
    if path == "contact-sheet.html":
        return "contact-sheet"
    if path.startswith("icons/"):
        return "icon-sprite" if path.endswith("/icons.svg") else "icon"
    if path.startswith("decorations/"):
        return "decoration-sprite" if path.endswith("/decorations.svg") else "decoration-glyph"
    if path.startswith("textures/"):
        return "texture"
    if path.startswith("wallpapers/"):
        return "wallpaper"
    if path.startswith("brand/"):
        return "brand-mark"
    if path.startswith("boot/"):
        return "boot-example"
    if path.startswith("desktop/"):
        return "desktop-example"
    if path.startswith("audio/"):
        return "audio-cue"
    if path == "tokens/schema.json":
        return "schema"
    if path.startswith("tokens/") and path.endswith(".json"):
        return "theme-pack"
    if path.endswith(".css"):
        return "stylesheet"
    if path.endswith(".js"):
        return "script"
    if path.endswith(".html"):
        return "example"
    if path == "LICENSE.txt":
        return "license"
    return "asset"


def manifest_entry(path: str, data: bytes) -> dict:
    generated = not path.startswith(("starter/", "gallery/", "boot/", "desktop/"))
    provenance = PROVENANCE_CODE if not generated else (PROVENANCE_AUDIO if path.endswith(".wav") else PROVENANCE_SVG if path.endswith(".svg") else "Original deterministic semantic theme and presentation data.")
    entry = {
        "path": path,
        "kind": asset_kind(path),
        "mediaType": media_type(path),
        "source": "Original hand-authored example" if not generated else "tools/build_assets.py",
        "author": AUTHOR,
        "provenance": provenance,
        "license": LICENSE,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    parts = path.split("/")
    if parts[0] in ("icons", "decorations") and len(parts) > 2:
        entry["era"] = theme_pack(parts[1])["identity"]["era"]
        entry["variant"] = parts[1]
    elif parts[0] in ("textures", "wallpapers"):
        stem = Path(path).stem
        theme_id = stem if stem in THEME_IDS else (stem.split("-")[0] if stem.startswith("classic-") else "classic")
        entry["era"] = theme_pack(theme_id)["identity"]["era"]
        entry["variant"] = stem
    elif parts[0] == "brand" and len(parts) > 1:
        theme_id = Path(path).stem.rsplit("-", 1)[0]
        if theme_id in THEME_IDS:
            entry["era"] = theme_pack(theme_id)["identity"]["era"]
            entry["variant"] = theme_id
    elif path.startswith("tokens/") and path.endswith(".json") and path != "tokens/schema.json":
        theme_id = Path(path).stem
        entry["era"] = theme_pack(theme_id)["identity"]["era"]
        entry["variant"] = theme_pack(theme_id)["identity"]["variant"]
    elif path.startswith("audio/"):
        entry["era"] = "cross-era original cues"
    if path.endswith(".svg"):
        # All generated standalone artwork has an explicit integer viewBox.
        text = data.decode("utf-8")
        if 'viewBox="' in text:
            viewbox = text.split('viewBox="', 1)[1].split('"', 1)[0]
            dims = viewbox.split()
            entry["image"] = {"viewBox": viewbox, "width": int(dims[2]), "height": int(dims[3])}
        else:
            entry["image"] = {"format": "SVG symbol sprite", "symbols": ICON_NAMES if parts[0] == "icons" else DECORATION_NAMES}
    if path.endswith(".wav"):
        entry["audio"] = audio_metadata(data)
    return entry


def build_outputs() -> dict[str, bytes]:
    packs = {theme_id: theme_pack(theme_id) for theme_id in THEME_IDS}
    outputs: dict[str, bytes] = {"tokens/schema.json": jbytes(schema())}
    for theme_id in THEME_IDS:
        outputs[f"tokens/{theme_id}.json"] = jbytes(packs[theme_id])
    outputs["tokens/themes.css"] = themes_css(packs)
    make_icon_assets(outputs)
    make_decoration_assets(outputs)
    make_texture_assets(outputs)
    make_wallpaper_assets(outputs)
    make_brand_assets(outputs)
    for name in ("activate", "notify", "complete", "error"):
        outputs[f"audio/{name}.wav"] = synthesize(name)
    outputs["contact-sheet.html"] = contact_sheet()
    outputs["LICENSE.txt"] = LICENSE_TEXT.encode("utf-8")
    return outputs


def all_asset_bytes(generated: dict[str, bytes]) -> dict[str, bytes]:
    files = dict(generated)
    if ASSETS.exists():
        for path in sorted(ASSETS.rglob("*"), key=lambda p: p.as_posix()):
            if path.is_file():
                relative = path.relative_to(ASSETS).as_posix()
                if relative != "manifest.json" and relative not in files:
                    files[relative] = path.read_bytes()
    return files


def manifest_bytes(files: dict[str, bytes]) -> bytes:
    manifest = {
        "schemaVersion": "1.0.0",
        "name": "retro-windows-ui original offline assets",
        "license": LICENSE,
        "independentUnofficial": True,
        "generatedBy": "tools/build_assets.py",
        "assetCount": len(files),
        "assets": [manifest_entry(path, files[path]) for path in sorted(files)],
    }
    return jbytes(manifest)


def check(generated: dict[str, bytes]) -> int:
    files = all_asset_bytes(generated)
    expected = dict(files)
    expected["manifest.json"] = manifest_bytes(files)
    failures = []
    for relative, data in expected.items():
        path = ASSETS / Path(relative)
        if not path.is_file():
            failures.append(f"missing: {relative}")
        elif path.read_bytes() != data:
            failures.append(f"changed: {relative}")
    current = {
        path.relative_to(ASSETS).as_posix()
        for path in ASSETS.rglob("*") if path.is_file()
    } if ASSETS.exists() else set()
    for relative in sorted(current - set(expected)):
        failures.append(f"unexpected: {relative}")
    if failures:
        print("Asset check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        print("Run python tools/build_assets.py to regenerate outputs.", file=sys.stderr)
        return 1
    print(f"OK: {len(files)} assets and manifest match deterministic rebuild.")
    return 0


def write(generated: dict[str, bytes]) -> int:
    files = all_asset_bytes(generated)
    outputs = dict(files)
    outputs["manifest.json"] = manifest_bytes(files)
    for relative in sorted(outputs):
        path = ASSETS / Path(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(outputs[relative])
    print(f"Generated {len(files)} original assets plus manifest in {ASSETS}.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify current files against a deterministic in-memory rebuild")
    args = parser.parse_args()
    generated = build_outputs()
    return check(generated) if args.check else write(generated)


if __name__ == "__main__":
    raise SystemExit(main())
