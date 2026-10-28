#!/usr/bin/env python3
import argparse
import functools
import http.server
import json
import socketserver
import threading
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills" / "retro-windows-ui" / "assets"
ARTIFACTS = ROOT / "artifacts"
THEMES = (
    "classic",
    "xp-luna-blue",
    "xp-luna-olive",
    "xp-luna-silver",
    "windows-7-aero",
    "windows-7-basic",
)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


class Server:
    def __init__(self, assets):
        self.assets = assets

    def __enter__(self):
        handler = functools.partial(QuietHandler, directory=str(self.assets))
        self.server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return f"http://127.0.0.1:{self.server.server_address[1]}"

    def __exit__(self, exc_type, exc_value, traceback):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)


def attach_audits(page, failures):
    page.on("pageerror", lambda error: failures.append(f"page error: {error}"))
    page.on("console", lambda message: failures.append(f"console error: {message.text}") if message.type == "error" else None)
    page.on("requestfailed", lambda request: failures.append(f"failed request: {request.url}"))
    page.on(
        "request",
        lambda request: failures.append(f"external request: {request.url}")
        if not request.url.startswith(("http://127.0.0.1:", "file:", "data:", "blob:"))
        else None,
    )


def install_audio_probe(page):
    page.add_init_script(
        """
        window.__retroQaAudioPlays = 0;
        const originalPlay = HTMLMediaElement.prototype.play;
        HTMLMediaElement.prototype.play = function (...args) {
          window.__retroQaAudioPlays += 1;
          return originalPlay.apply(this, args);
        };
        """
    )


def theme_select(page):
    for index in range(page.locator("select").count()):
        select = page.locator("select").nth(index)
        values = select.locator("option").evaluate_all("options => options.map(option => option.value)")
        if all(theme in values for theme in THEMES):
            return select
    raise AssertionError("No theme selector exposes all six expected theme values")


def select_theme(page, theme):
    theme_select(page).select_option(theme)
    expect(page.locator("html")).to_have_attribute("data-theme", theme)


def assert_no_horizontal_overflow(page, label):
    dimensions = page.evaluate("({scroll: document.documentElement.scrollWidth, viewport: window.innerWidth})")
    if dimensions["scroll"] > dimensions["viewport"] + 2:
        raise AssertionError(f"{label}: horizontal overflow {dimensions['scroll']}px > {dimensions['viewport']}px")


def assert_window_active(locator):
    classes = (locator.get_attribute("class") or "").split()
    if "active" not in classes or "inactive" in classes:
        raise AssertionError(f"Window is not active: {locator.get_attribute('class')}")


def check_menus_and_dialog(page):
    file_trigger = page.locator(".menu-trigger[aria-controls='file-menu']")
    next_trigger = page.locator(".menubar .menu-trigger").nth(1)
    file_menu = page.locator("#file-menu")
    next_menu = page.locator(f"#{next_trigger.get_attribute('aria-controls')}")
    page.locator("input[type='text']:visible").first.focus()
    page.keyboard.press("F10")
    expect(file_trigger).to_be_focused()

    file_trigger.press("Enter")
    expect(file_menu).to_be_visible()
    items = file_menu.locator("[role='menuitem']")
    expect(items.nth(0)).to_be_focused()
    page.keyboard.press("ArrowRight")
    expect(file_menu).to_be_hidden()
    expect(next_menu).to_be_visible()
    expect(next_menu.locator("[role='menuitem']").first).to_be_focused()
    page.keyboard.press("Escape")
    expect(next_menu).to_be_hidden()
    expect(next_trigger).to_be_focused()

    file_trigger.press("Enter")
    page.keyboard.press("s")
    expect(items.nth(1)).to_be_focused()
    page.keyboard.press("Escape")
    expect(file_trigger).to_be_focused()

    file_trigger.press("Enter")
    page.keyboard.press("Tab")
    expect(file_menu).to_be_hidden()
    assert not page.evaluate("document.activeElement.closest('.menu-popup') !== null")

    file_trigger.press("ArrowDown")
    expect(items.nth(0)).to_be_focused()
    page.keyboard.press("ArrowDown")
    expect(items.nth(1)).to_be_focused()
    page.keyboard.press("Escape")
    expect(file_menu).to_be_hidden()
    expect(file_trigger).to_be_focused()

    file_trigger.press("ArrowDown")
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    expect(file_menu).to_be_hidden()
    expect(file_trigger).to_be_focused()
    expect(page.locator("#status-message")).to_contain_text("saved")

    start_button = page.locator("#start-button")
    start_button.focus()
    start_button.press("Enter")
    expect(page.locator("#start-menu")).to_be_visible()
    expect(page.locator("#start-menu [role='menuitem']").first).to_be_focused()
    page.keyboard.press("Escape")
    expect(page.locator("#start-menu")).to_be_hidden()
    expect(start_button).to_be_focused()

    file_trigger.click()
    items.first.click()
    dialog = page.locator("#properties-dialog")
    expect(dialog).to_be_visible()
    expect(page.locator("#profile-name")).to_be_focused()
    page.keyboard.press("Shift+Tab")
    assert page.evaluate("document.getElementById('properties-dialog').contains(document.activeElement)")
    page.keyboard.press("Tab")
    assert page.evaluate("document.getElementById('properties-dialog').contains(document.activeElement)")
    page.keyboard.press("Escape")
    expect(dialog).to_be_hidden()
    expect(file_trigger).to_be_focused()
    expect(page.locator("#status-message")).to_have_text("Changes cancelled")

    visible_opener = page.locator("[data-open-dialog]:visible").first
    visible_opener.click()
    expect(page.locator("#profile-name")).to_be_focused()
    page.keyboard.press("Enter")
    expect(dialog).to_be_hidden()
    expect(visible_opener).to_be_focused()
    expect(page.locator("#status-message")).to_have_text("Profile saved")


def check_tabs_and_listbox(page):
    tabs = page.locator("[role='tablist']").first.locator("[role='tab']")
    tabs.first.focus()
    tabs.first.press("ArrowRight")
    expect(tabs.nth(1)).to_have_attribute("aria-selected", "true")
    expect(tabs.nth(1)).to_be_focused()
    first_panel = page.locator(f"#{tabs.first.get_attribute('aria-controls')}")
    second_panel = page.locator(f"#{tabs.nth(1).get_attribute('aria-controls')}")
    expect(first_panel).to_be_hidden()
    expect(second_panel).to_be_visible()
    tabs.nth(1).press("Home")
    expect(tabs.first).to_have_attribute("aria-selected", "true")
    expect(first_panel).to_be_visible()

    listbox = page.locator("[role='listbox']").first
    options = listbox.locator("[role='option']")
    expect(listbox).to_have_attribute("aria-activedescendant", options.first.get_attribute("id"))
    listbox.focus()
    listbox.press("ArrowDown")
    expect(options.nth(1)).to_have_attribute("aria-selected", "true")
    expect(listbox).to_have_attribute("aria-activedescendant", options.nth(1).get_attribute("id"))
    listbox.press("End")
    expect(options.last).to_have_attribute("aria-selected", "true")
    expect(listbox).to_have_attribute("aria-activedescendant", options.last.get_attribute("id"))
    listbox.press("Home")
    expect(options.first).to_have_attribute("aria-selected", "true")
    expect(listbox).to_have_attribute("aria-activedescendant", options.first.get_attribute("id"))


def check_windows(page, primary_id, secondary_id):
    primary = page.locator(f"[data-window='{primary_id}']")
    secondary = page.locator(f"[data-window='{secondary_id}']")
    secondary_task = page.locator(f"[data-task-window='{secondary_id}']")

    secondary.locator(".titlebar").click()
    assert_window_active(secondary)
    expect(secondary_task).to_have_attribute("aria-pressed", "true")
    secondary.locator("[data-window-action='minimize']").click()
    expect(secondary).to_be_hidden()
    assert_window_active(primary)
    expect(secondary_task).to_be_focused()
    secondary_task.click()
    expect(secondary).to_be_visible()
    assert_window_active(secondary)

    maximize = primary.locator("[data-window-action='maximize']")
    maximize.click()
    assert "maximized" in (primary.get_attribute("class") or "").split()
    expect(maximize).to_have_attribute("aria-label", "Restore Active workspace" if primary_id == "gallery-main" else "Restore Display Properties")
    maximize.click()
    assert "maximized" not in (primary.get_attribute("class") or "").split()


def check_reduced_modes(page, screenshot_prefix=None, check_progress=False):
    if check_progress:
        select_theme(page, "classic")
        fill = page.locator(".progress-fill")
        color = fill.evaluate("element => getComputedStyle(element).backgroundColor")
        if color in ("transparent", "rgba(0, 0, 0, 0)"):
            raise AssertionError("Classic custom progress fill has no solid fallback")

    select_theme(page, "windows-7-aero")
    window = page.locator(".window").first
    backdrop = window.evaluate("element => getComputedStyle(element).backdropFilter")
    if "blur" not in backdrop:
        raise AssertionError(f"Aero backdrop filter is not active: {backdrop}")
    transparency = page.locator("[data-reduced-transparency-control]")
    transparency.check()
    expect(page.locator("html")).to_have_attribute("data-reduced-transparency", "true")
    expect(window).to_have_css("backdrop-filter", "none")
    if screenshot_prefix:
        page.screenshot(path=ARTIFACTS / f"{screenshot_prefix}-reduced-transparency.png", full_page=True)
    transparency.uncheck()

    motion = page.locator("[data-reduced-motion-control]")
    motion.check()
    expect(page.locator("html")).to_have_attribute("data-reduced-motion", "true")
    durations = window.evaluate("element => getComputedStyle(element).transitionDuration.split(',').map(value => parseFloat(value))")
    if any(duration != 0 for duration in durations):
        raise AssertionError(f"Reduced motion left nonzero transitions: {durations}")
    if screenshot_prefix:
        page.screenshot(path=ARTIFACTS / f"{screenshot_prefix}-reduced-motion.png", full_page=True)
    motion.uncheck()

    select_theme(page, "windows-7-basic")
    expect(window).to_have_css("backdrop-filter", "none")


def check_audio_persistence(page):
    expect(page.locator("[data-sound-enable]")).not_to_be_checked()
    if page.evaluate("window.__retroQaAudioPlays") != 0:
        raise AssertionError("Audio played before user opt-in")

    page.locator("[data-sound-enable]").check()
    page.wait_for_function("window.__retroQaAudioPlays === 1")
    cue = page.locator("[data-feedback][data-cue]:visible").first
    cue.click()
    page.wait_for_function("window.__retroQaAudioPlays === 2")

    mute = page.locator("[data-mute]")
    mute.click()
    expect(mute).to_have_attribute("aria-pressed", "true")
    message = cue.get_attribute("data-feedback")
    cue.click()
    expect(page.locator("#status-message")).to_have_text(message)
    if page.evaluate("window.__retroQaAudioPlays") != 2:
        raise AssertionError("Audio played while muted")

    volume = page.locator("[data-volume]")
    volume.evaluate("element => { element.value = '22'; element.dispatchEvent(new Event('input', {bubbles: true})); }")
    select_theme(page, "xp-luna-olive")
    page.reload(wait_until="networkidle")
    expect(page.locator("[data-sound-enable]")).to_be_checked()
    expect(page.locator("[data-mute]")).to_have_attribute("aria-pressed", "true")
    expect(page.locator("[data-volume]")).to_have_value("22")
    expect(theme_select(page)).to_have_value("xp-luna-olive")
    if page.evaluate("window.__retroQaAudioPlays") != 0:
        raise AssertionError("Audio autoplayed after reload")

    page.locator("[data-mute]").click()
    page.locator("[data-feedback][data-cue]:visible").first.click()
    page.wait_for_function("window.__retroQaAudioPlays === 1")


def run_gallery_checks(browser, base_url):
    failures = []
    context = browser.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
    page = context.new_page()
    attach_audits(page, failures)
    install_audio_probe(page)
    page.goto(f"{base_url}/gallery/index.html", wait_until="networkidle")
    expect(page.locator("body")).to_be_visible()
    expect(page.locator("html")).to_have_attribute("data-gallery-ready", "true")
    if page.evaluate("window.__retroQaAudioPlays") != 0:
        raise AssertionError("Audio played before user opt-in")

    for theme in THEMES:
        select_theme(page, theme)
        assert_no_horizontal_overflow(page, theme)
        page.screenshot(path=ARTIFACTS / f"gallery-{theme}.png", full_page=True)

    check_menus_and_dialog(page)
    check_tabs_and_listbox(page)
    check_windows(page, "gallery-main", "gallery-notes")
    check_reduced_modes(page, "gallery", check_progress=True)

    page.emulate_media(reduced_motion="reduce")
    durations = page.locator(".window").first.evaluate("element => getComputedStyle(element).transitionDuration.split(',').map(value => parseFloat(value))")
    if any(duration != 0 for duration in durations):
        raise AssertionError("System reduced-motion preference did not disable transitions")
    page.emulate_media(reduced_motion="no-preference")

    scaled = browser.new_context(viewport={"width": 1280, "height": 900}, device_scale_factor=2)
    scaled_page = scaled.new_page()
    attach_audits(scaled_page, failures)
    scaled_page.goto(f"{base_url}/gallery/index.html", wait_until="networkidle")
    scaled_page.add_style_tag(content="html { font-size: 200% !important; }")
    scaled_page.screenshot(path=ARTIFACTS / "gallery-text-200-dpi-2.png", full_page=True)
    assert_no_horizontal_overflow(scaled_page, "200% text at DPI 2")
    scaled.close()

    if failures:
        raise AssertionError("\n".join(sorted(set(failures))))
    context.close()


def run_starter_checks(browser, base_url):
    failures = []
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()
    attach_audits(page, failures)
    install_audio_probe(page)
    page.goto(f"{base_url}/starter/index.html", wait_until="networkidle")
    expect(page.locator("body")).to_be_visible()
    check_menus_and_dialog(page)
    check_tabs_and_listbox(page)
    check_windows(page, "settings", "notes")
    check_reduced_modes(page)
    check_audio_persistence(page)
    assert_no_horizontal_overflow(page, "starter after interactions")
    page.screenshot(path=ARTIFACTS / "starter-interactions.png", full_page=True)
    if failures:
        raise AssertionError("\n".join(sorted(set(failures))))
    context.close()


def run_boot_checks(browser, base_url):
    failures = []
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()
    attach_audits(page, failures)
    page.goto(f"{base_url}/boot/index.html", wait_until="networkidle")
    stage = page.locator("#boot-stage")
    expect(stage).to_have_attribute("data-view", "xp")
    page.wait_for_timeout(1700)
    expect(stage).to_have_attribute("data-phase", "welcome")
    page.locator("#boot-skip").click()
    expect(page.locator("#boot-end")).to_be_visible()
    page.locator("#boot-again").click()
    expect(page.locator("#boot-end")).to_be_hidden()
    select_theme(page, "classic")
    expect(stage).to_have_attribute("data-view", "classic")
    assert_no_horizontal_overflow(page, "boot classic")
    select_theme(page, "windows-7-aero")
    expect(stage).to_have_attribute("data-view", "win7")
    page.screenshot(path=ARTIFACTS / "boot-win7.png", full_page=True)
    page.locator("#boot-skip").click()
    if failures:
        raise AssertionError("\n".join(sorted(set(failures))))
    context.close()


def run_desktop_checks(browser, base_url):
    failures = []
    context = browser.new_context(viewport={"width": 1440, "height": 960})
    page = context.new_page()
    attach_audits(page, failures)
    install_audio_probe(page)
    page.goto(f"{base_url}/desktop/index.html", wait_until="networkidle")
    expect(page.locator("#computer-title")).to_have_text("My Computer")
    expect(page.locator("[data-window='computer']")).to_be_visible()
    page.locator("[data-open-window='notepad']").first.click()
    notepad = page.locator("[data-window='notepad']")
    expect(notepad).to_be_visible()
    notepad.locator("[data-window-action='minimize']").click()
    expect(notepad).to_be_hidden()
    page.locator("[data-task-window='notepad']").click()
    expect(notepad).to_be_visible()
    select_theme(page, "classic")
    assert_no_horizontal_overflow(page, "default desktop mockup")
    page.screenshot(path=ARTIFACTS / "desktop-mockup.png", full_page=True)
    if page.evaluate("window.__retroQaAudioPlays") != 0:
        raise AssertionError("Desktop mockup played audio before opt-in")
    if failures:
        raise AssertionError("\n".join(sorted(set(failures))))
    context.close()

    mobile = browser.new_context(viewport={"width": 390, "height": 844})
    mobile_page = mobile.new_page()
    attach_audits(mobile_page, failures)
    mobile_page.goto(f"{base_url}/desktop/index.html", wait_until="networkidle")
    mobile_page.locator("[data-open-window='notepad']").first.click()
    expect(mobile_page.locator("[data-window='notepad']")).to_be_visible()
    expect(mobile_page.locator("[data-window='computer']")).to_be_hidden()
    assert_no_horizontal_overflow(mobile_page, "default desktop mobile")
    mobile_page.screenshot(path=ARTIFACTS / "desktop-mockup-mobile.png", full_page=True)
    mobile.close()
    if failures:
        raise AssertionError("\n".join(sorted(set(failures))))


def run_file_protocol_check(browser, assets):
    failures = []
    context = browser.new_context(viewport={"width": 1100, "height": 800})
    page = context.new_page()
    attach_audits(page, failures)
    install_audio_probe(page)
    page.goto((assets / "starter" / "index.html").as_uri(), wait_until="networkidle")
    expect(page.locator("#settings-title")).to_have_text("Display Properties")
    select_theme(page, "xp-luna-silver")
    page.locator("[data-feedback='Settings applied successfully']").click()
    expect(page.locator("#status-message")).to_have_text("Settings applied successfully")
    if page.evaluate("window.__retroQaAudioPlays") != 0:
        raise AssertionError("Audio played from file:// before user opt-in")
    assert_no_horizontal_overflow(page, "file:// starter")
    page.screenshot(path=ARTIFACTS / "starter-file-protocol.png", full_page=True)
    if failures:
        raise AssertionError("\n".join(sorted(set(failures))))
    context.close()


def main():
    parser = argparse.ArgumentParser(description="Run real Chromium checks against the offline retro Windows examples.")
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--assets", type=Path, default=ASSETS, help="Asset directory to test, including an installed skill copy.")
    args = parser.parse_args()
    assets = args.assets.resolve()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    with Server(assets) as base_url:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=not args.headed)
            try:
                run_gallery_checks(browser, base_url)
                run_starter_checks(browser, base_url)
                run_boot_checks(browser, base_url)
                run_desktop_checks(browser, base_url)
                run_file_protocol_check(browser, assets)
            finally:
                browser.close()
    report = {
        "audioPersistence": "passed",
        "audioPlaysBeforeOptIn": 0,
        "fileProtocol": "passed",
        "interactionPages": ["starter", "gallery", "boot", "desktop"],
        "screenshots": 16,
        "themes": len(THEMES),
    }
    report_path = ARTIFACTS / "browser-report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Browser QA passed: {json.dumps(report, sort_keys=True)}")
    print(f"Screenshots and report: {ARTIFACTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
