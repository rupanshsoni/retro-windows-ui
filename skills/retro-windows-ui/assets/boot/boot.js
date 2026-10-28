(() => {
  "use strict";

  const root = document.documentElement;
  const stage = document.getElementById("boot-stage");
  const themeSelect = document.getElementById("boot-theme");
  const endPanel = document.getElementById("boot-end");
  const status = document.getElementById("boot-status");
  const views = {
    classic: document.querySelector(".boot-view--classic"),
    xp: document.querySelector(".boot-view--xp"),
    win7: document.querySelector(".boot-view--seven")
  };
  const marks = {
    bar: document.getElementById("bar-mark"),
    classic: document.getElementById("classic-mark"),
    xp: document.getElementById("xp-mark"),
    welcome: document.getElementById("welcome-mark"),
    seven: document.getElementById("seven-mark")
  };
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let timers = [];
  let currentTheme = themeSelect.value;

  function clearTimers() {
    timers.forEach(timer => window.clearTimeout(timer));
    timers = [];
  }

  function later(callback, delay) {
    timers.push(window.setTimeout(callback, delay));
  }

  function viewFor(theme) {
    if (theme === "classic") return "classic";
    if (theme.startsWith("xp-")) return "xp";
    return "win7";
  }

  function setStatus(message) {
    if (status) status.textContent = message;
  }

  function showEnd() {
    clearTimers();
    if (!endPanel) return;
    endPanel.hidden = false;
    stage.dataset.phase = "done";
    setStatus("Startup sequence complete. Choose Play again or open the default desktop mockup.");
  }

  function start() {
    clearTimers();
    endPanel.hidden = true;
    root.dataset.theme = currentTheme;
    const view = viewFor(currentTheme);
    stage.dataset.view = view;
    stage.dataset.phase = "loading";
    const suffix = currentTheme;
    marks.bar.src = `../brand/${suffix}-start.svg`;
    marks.classic.src = `../brand/${suffix}-mark.svg`;
    marks.xp.src = `../brand/${suffix}-mark.svg`;
    marks.welcome.src = `../brand/${suffix}-start.svg`;
    marks.seven.src = `../brand/${suffix}-mark.svg`;

    Object.keys(views).forEach(key => {
      views[key].setAttribute("aria-hidden", key === view ? "false" : "true");
    });
    const welcome = views.xp.querySelector(".xp-welcome");
    welcome.setAttribute("aria-hidden", "true");
    setStatus(view === "xp" ? "Loading stage. The welcome stage follows." : view === "win7" ? "Starting your desktop." : "Starting desktop.");

    if (view === "xp") {
      later(() => {
        stage.dataset.phase = "welcome";
        welcome.setAttribute("aria-hidden", "false");
        setStatus("Welcome stage. Entering the demo desktop in a moment.");
      }, reducedMotion ? 450 : 1500);
      later(showEnd, reducedMotion ? 1300 : 3200);
    } else {
      later(showEnd, reducedMotion ? 900 : 3000);
    }
  }

  themeSelect.addEventListener("change", () => {
    currentTheme = themeSelect.value;
    try { localStorage.setItem("retro-windows-ui:boot-theme", currentTheme); } catch { /* Storage is optional. */ }
    start();
  });

  document.getElementById("boot-replay").addEventListener("click", start);
  document.getElementById("boot-skip").addEventListener("click", showEnd);
  document.getElementById("boot-again").addEventListener("click", start);
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") showEnd();
  });

  try {
    const saved = localStorage.getItem("retro-windows-ui:boot-theme");
    if (saved && [...themeSelect.options].some(option => option.value === saved)) {
      currentTheme = saved;
      themeSelect.value = saved;
    }
  } catch { /* Storage is optional. */ }

  start();
})();
