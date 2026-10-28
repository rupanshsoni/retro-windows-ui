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
ICON_NAMES = ("folder", "document", "search", "settings", "info", "warning")
DECORATION_NAMES = ("minimize", "maximize", "restore", "close")
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


def icon_defs(theme_id: str) -> str:
    gold, pale, paper, accent, ink = icon_palette(theme_id)
    prefix = theme_id
    soft = ".18" if theme_id == "windows-7-aero" else ".10"
    return f'''<defs>
  <linearGradient id="{prefix}-gold" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{pale}"/><stop offset="1" stop-color="{gold}"/></linearGradient>
  <linearGradient id="{prefix}-paper" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#ffffff"/><stop offset="1" stop-color="{paper}"/></linearGradient>
  <filter id="{prefix}-soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="1" stdDeviation=".6" flood-color="{ink}" flood-opacity="{soft}"/></filter>
</defs>'''


def icon_shapes(theme_id: str, name: str) -> str:
    gold, pale, paper, accent, ink = icon_palette(theme_id)
    rounded = theme_id != "classic"
    rx = "2" if rounded else "0"
    stroke = "1.25" if theme_id == "classic" else "1"
    filt = "" if theme_id == "classic" else f' filter="url(#{theme_id}-soft)"'
    if name == "folder":
        return f'''<g{filt} stroke="{ink}" stroke-width="{stroke}" stroke-linejoin="round">
<path d="M2 6h7l2-3h8a2 2 0 0 1 2 2v4H2Z" fill="url(#{theme_id}-gold)" rx="{rx}"/>
<path d="M2 8h20l-2 12H4Z" fill="url(#{theme_id}-gold)"/>
<path d="M5 10h14" stroke="{pale}"/>
</g>'''
    if name == "document":
        return f'''<g{filt} stroke="{ink}" stroke-width="{stroke}" stroke-linejoin="round">
<path d="M5 2h10l4 4v16H5Z" fill="url(#{theme_id}-paper)" rx="{rx}"/>
<path d="M15 2v5h4" fill="{pale}"/>
<path d="M8 11h8M8 14h8M8 17h6" stroke="{accent}"/>
</g>'''
    if name == "search":
        return f'''<g{filt} fill="none" stroke="{ink}" stroke-width="2" stroke-linecap="round">
<circle cx="10" cy="10" r="6" fill="{paper}" stroke="{accent}"/>
<path d="m14.5 14.5 6 6" stroke="{ink}" stroke-width="3"/>
<path d="M7 7a4 4 0 0 1 4-2" stroke="#fff" stroke-width="1"/>
</g>'''
    if name == "settings":
        teeth = " ".join(f'<path d="M12 2v3" transform="rotate({a} 12 12)"/>' for a in range(0, 360, 45))
        return f'''<g{filt} stroke="{ink}" stroke-width="2.4" stroke-linecap="square">
{teeth}
<circle cx="12" cy="12" r="7" fill="{accent}"/>
<circle cx="12" cy="12" r="3" fill="{paper}" stroke-width="1"/>
</g>'''
    if name == "info":
        return f'''<g{filt} stroke="{ink}" stroke-width="{stroke}">
<circle cx="12" cy="12" r="9" fill="{accent}"/>
<circle cx="12" cy="7" r="1.3" fill="#fff" stroke="none"/>
<path d="M12 11v6" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>
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
<div class="texture" style="background-image:url('textures/{theme_id}.svg')"><span>Original subtle texture</span></div>
</section>''')
    audio = "".join(f'''<tr><th scope="row">{name}.wav</th><td><audio controls preload="none" src="audio/{name}.wav">Audio cue: {name}.wav</audio></td><td>Original deterministic PCM16 synthesis; CC0-1.0; no Windows audio sampled or imitated.</td></tr>''' for name in ("activate", "notify", "complete", "error"))
    html = f'''<!doctype html>
<html lang="en" data-theme="classic">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Retro Windows UI — Asset Contact Sheet</title>
<link rel="stylesheet" href="tokens/themes.css">
<style>
*{{box-sizing:border-box}}body{{margin:0;padding:24px;background:#e7e7e7;color:#171717;font:14px/1.45 Tahoma,'Segoe UI',sans-serif}}header,section,table{{max-width:1180px;margin:auto}}h1{{margin:0 0 6px}}a{{color:#0645ad}}.theme-card{{padding:18px;margin:20px 0;background:var(--rw-surface-window);border:2px solid var(--rw-border-default);border-radius:var(--rw-radius-window);box-shadow:var(--rw-shadow-window);backdrop-filter:var(--rw-backdrop-filter)}}.theme-card h2{{font:var(--rw-title-weight) var(--rw-title-size)/1.2 var(--rw-font-ui);margin:0}}.theme-card p{{margin:3px 0 14px;color:var(--rw-text-secondary)}}.icons{{display:flex;flex-wrap:wrap;gap:10px}}figure{{margin:0;width:68px;text-align:center}}figure img{{display:block;margin:auto;image-rendering:auto}}figcaption{{font-size:11px;margin-top:4px}}.decorations{{display:flex;gap:8px;padding:10px 0}}.decorations img{{background:var(--rw-titlebar-active-background);padding:2px;border-radius:2px}}.texture{{height:58px;border:1px solid var(--rw-border-default);display:flex;align-items:end;padding:6px;background-size:96px}}.texture span{{background:#fff;color:#111;padding:2px 5px}}table{{width:100%;border-collapse:collapse;background:#fff;margin-top:20px}}th,td{{padding:10px;border:1px solid #aaa;text-align:left;vertical-align:middle}}th{{width:130px}}audio{{max-width:100%;height:32px}}footer{{max-width:1180px;margin:22px auto}}@media(max-width:600px){{body{{padding:12px}}td{{display:block}}th{{display:block;width:auto}}audio{{width:100%}}}}
</style></head>
<body><header><h1>Retro Windows UI asset contact sheet</h1><p>Six original theme families, locally rendered vectors, textures, and opt-in audio. No remote resources.</p><nav><a href="starter/index.html">Starter example</a> · <a href="gallery/index.html">Interactive gallery</a> · <a href="manifest.json">Manifest</a> · <a href="LICENSE.txt">CC0 and independence notice</a></nav></header>
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
The starter and gallery are original hand-authored offline examples. Consult
manifest.json for per-file provenance, media metadata, byte sizes, and SHA256.
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
    generated = not path.startswith(("starter/", "gallery/"))
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
    elif parts[0] == "textures":
        theme_id = Path(path).stem
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
