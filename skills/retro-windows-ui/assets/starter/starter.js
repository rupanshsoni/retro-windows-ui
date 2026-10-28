(() => {
  "use strict";

  const root = document.documentElement;
  const storage = {
    get(key) {
      try { return localStorage.getItem(`retro-windows-ui:${key}`); } catch { return null; }
    },
    set(key, value) {
      try { localStorage.setItem(`retro-windows-ui:${key}`, String(value)); } catch { /* Storage is optional. */ }
    }
  };
  const validThemes = new Set(["classic", "xp-luna-blue", "xp-luna-olive", "xp-luna-silver", "windows-7-aero", "windows-7-basic"]);
  let soundEnabled = storage.get("sound-enabled") === "true";
  let muted = storage.get("muted") === "true";
  let volume = Number(storage.get("volume") || 35) / 100;
  let dialogInvoker = null;
  let dialogResult = null;
  const menuTypeahead = new WeakMap();

  function status(message) {
    const target = document.getElementById("status-message");
    if (target) target.textContent = message;
  }

  function updateAudioControls() {
    const enabled = document.querySelector("[data-sound-enable]");
    const mute = document.querySelector("[data-mute]");
    const tray = document.getElementById("tray-status");
    if (enabled) enabled.checked = soundEnabled;
    if (mute) {
      mute.setAttribute("aria-pressed", String(muted));
      mute.textContent = muted ? "Unmute" : "Mute";
    }
    if (tray) tray.textContent = soundEnabled ? (muted ? "Sound muted" : "Sound on") : "Sound off";
  }

  function playCue(cue) {
    if (!cue || !soundEnabled || muted || document.hidden) return;
    const audio = new Audio(`../audio/${cue}.wav`);
    audio.volume = Math.max(0, Math.min(1, volume));
    audio.play().catch(() => status("Audio unavailable; visual feedback remains active"));
  }

  function feedback(message, cue) {
    status(message);
    playCue(cue);
  }

  function applyTheme(theme, announce = false) {
    if (!validThemes.has(theme)) return;
    root.dataset.theme = theme;
    document.querySelectorAll("[data-theme-select]").forEach(select => { select.value = theme; });
    document.querySelectorAll("img[data-icon]").forEach(icon => {
      icon.src = `../icons/${theme}/${icon.dataset.icon}.svg`;
    });
    storage.set("theme", theme);
    if (announce) {
      const select = document.querySelector("[data-theme-select]");
      const label = select?.selectedOptions[0]?.textContent || theme;
      feedback(`${label} applied`, "activate");
    }
  }

  function closeMenus(except) {
    document.querySelectorAll(".menu-trigger[aria-expanded='true'], #start-button[aria-expanded='true']").forEach(trigger => {
      if (trigger === except) return;
      trigger.setAttribute("aria-expanded", "false");
      const menu = document.getElementById(trigger.getAttribute("aria-controls"));
      if (menu) menu.hidden = true;
    });
  }

  function openMenu(trigger) {
    closeMenus(trigger);
    const menu = document.getElementById(trigger.getAttribute("aria-controls"));
    if (!menu) return;
    trigger.setAttribute("aria-expanded", "true");
    menu.hidden = false;
  }

  function closeMenu(trigger, restoreFocus = false) {
    const menu = document.getElementById(trigger.getAttribute("aria-controls"));
    trigger.setAttribute("aria-expanded", "false");
    if (menu) menu.hidden = true;
    if (restoreFocus) trigger.focus();
  }

  function menuItems(menu) {
    return [...menu.querySelectorAll("[role='menuitem']:not(:disabled)")].filter(item => !item.hidden);
  }

  function menuTriggerFor(menu) {
    return document.querySelector(`[aria-controls="${menu.id}"]`);
  }

  function activateWindow(window) {
    if (!window || window.hidden) return;
    document.querySelectorAll("[data-window]").forEach(item => {
      const active = item === window;
      item.classList.toggle("active", active);
      item.classList.toggle("inactive", !active);
    });
    document.querySelectorAll("[data-task-window]").forEach(button => {
      button.setAttribute("aria-pressed", String(button.dataset.taskWindow === window.dataset.window && !button.hidden));
    });
  }

  function windowAction(button) {
    const window = button.closest("[data-window]");
    if (!window) return;
    const id = window.dataset.window;
    const task = document.querySelector(`[data-task-window="${id}"]`);
    const action = button.dataset.windowAction;
    if (action === "maximize") {
      window.classList.toggle("maximized");
      button.setAttribute("aria-label", `${window.classList.contains("maximized") ? "Restore" : "Maximize"} ${window.querySelector(".window-title")?.textContent || "window"}`);
      activateWindow(window);
      return;
    }
    if (action === "minimize" || action === "close") {
      window.hidden = true;
      if (action === "close" && task) task.hidden = true;
      const next = [...document.querySelectorAll("[data-window]")].find(item => !item.hidden);
      if (next) activateWindow(next);
      if (task && !task.hidden) task.focus();
      else document.getElementById("start-button")?.focus();
      status(`${window.querySelector(".window-title")?.textContent || "Window"} ${action === "close" ? "closed" : "minimized"}`);
      closeMenus();
    }
  }

  document.querySelectorAll("[data-theme-select]").forEach(select => {
    select.addEventListener("change", () => applyTheme(select.value, true));
  });

  document.querySelectorAll("[data-window]").forEach(window => {
    window.addEventListener("pointerdown", () => activateWindow(window));
  });
  document.querySelectorAll("[data-window-action]").forEach(button => {
    button.addEventListener("click", () => windowAction(button));
  });
  document.querySelectorAll("[data-task-window]").forEach(button => {
    button.addEventListener("click", () => {
      const window = document.querySelector(`[data-window="${button.dataset.taskWindow}"]`);
      if (!window) return;
      window.hidden = false;
      activateWindow(window);
      window.querySelector("button, input, select, [tabindex='0']")?.focus();
      status(`${window.querySelector(".window-title")?.textContent || "Window"} restored`);
    });
  });

  document.querySelectorAll(".menu-trigger, #start-button").forEach(trigger => {
    trigger.addEventListener("click", event => {
      event.stopPropagation();
      if (trigger.getAttribute("aria-expanded") === "true") closeMenu(trigger);
      else openMenu(trigger);
    });
    trigger.addEventListener("keydown", event => {
      if (event.key === "ArrowDown" || event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openMenu(trigger);
        const menu = document.getElementById(trigger.getAttribute("aria-controls"));
        menuItems(menu)[0]?.focus();
      } else if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
        const triggers = [...document.querySelectorAll(".menubar .menu-trigger")];
        const index = triggers.indexOf(trigger);
        if (index >= 0) {
          event.preventDefault();
          const direction = event.key === "ArrowRight" ? 1 : -1;
          triggers[(index + direction + triggers.length) % triggers.length].focus();
        }
      }
    });
  });

  document.addEventListener("keydown", event => {
    if (event.key !== "F10" && event.key !== "Alt") return;
    if (event.key === "Alt" && (event.ctrlKey || event.shiftKey || event.metaKey)) return;
    const triggers = [...document.querySelectorAll(".menubar .menu-trigger")];
    if (!triggers.length) return;
    event.preventDefault();
    triggers[0].focus();
  });

  document.querySelectorAll(".menu-popup").forEach(menu => {
    menu.addEventListener("keydown", event => {
      const items = menuItems(menu);
      const index = items.indexOf(document.activeElement);
      const trigger = menuTriggerFor(menu);
      if (["ArrowDown", "ArrowUp", "Home", "End"].includes(event.key)) {
        event.preventDefault();
        let next = index;
        if (event.key === "Home") next = 0;
        else if (event.key === "End") next = items.length - 1;
        else next = (index + (event.key === "ArrowDown" ? 1 : -1) + items.length) % items.length;
        items[next]?.focus();
      } else if (["ArrowLeft", "ArrowRight"].includes(event.key)) {
        const triggers = [...document.querySelectorAll(".menubar .menu-trigger")];
        const triggerIndex = triggers.indexOf(trigger);
        if (triggerIndex < 0) return;
        event.preventDefault();
        const direction = event.key === "ArrowRight" ? 1 : -1;
        const nextTrigger = triggers[(triggerIndex + direction + triggers.length) % triggers.length];
        openMenu(nextTrigger);
        const nextMenu = document.getElementById(nextTrigger.getAttribute("aria-controls"));
        menuItems(nextMenu)[0]?.focus();
      } else if (event.key === "Escape") {
        event.preventDefault();
        if (trigger) closeMenu(trigger, true);
      } else if (event.key === "Tab") {
        closeMenu(trigger);
        trigger?.focus();
      } else if (event.key.length === 1 && !event.ctrlKey && !event.metaKey && !event.altKey) {
        const state = menuTypeahead.get(menu) || { text: "", timer: 0 };
        clearTimeout(state.timer);
        state.text += event.key.toLowerCase();
        const start = index >= 0 ? index + 1 : 0;
        const ordered = [...items.slice(start), ...items.slice(0, start)];
        const match = ordered.find(item => item.textContent.trim().replace(/\s+/g, " ").toLowerCase().startsWith(state.text));
        state.timer = setTimeout(() => { state.text = ""; }, 600);
        menuTypeahead.set(menu, state);
        if (!match) return;
        event.preventDefault();
        match.focus();
      }
    });
    menu.addEventListener("click", event => {
      const item = event.target.closest("[role='menuitem']:not(:disabled)");
      if (!item) return;
      const preserveFocus = item.hasAttribute("data-open-dialog") || item.hasAttribute("data-window-action");
      closeMenus();
      if (!preserveFocus) document.querySelector(`[aria-controls="${menu.id}"]`)?.focus();
    });
  });
  document.addEventListener("click", event => {
    if (!event.target.closest(".menu-popup") && !event.target.closest(".menu-trigger") && !event.target.closest("#start-button")) closeMenus();
  });

  document.querySelectorAll("[role='tablist']").forEach(list => {
    const tabs = [...list.querySelectorAll("[role='tab']")];
    function selectTab(tab) {
      tabs.forEach(item => {
        const selected = item === tab;
        item.setAttribute("aria-selected", String(selected));
        item.tabIndex = selected ? 0 : -1;
        const panel = document.getElementById(item.getAttribute("aria-controls"));
        if (panel) panel.hidden = !selected;
      });
    }
    tabs.forEach((tab, index) => {
      tab.addEventListener("click", () => selectTab(tab));
      tab.addEventListener("keydown", event => {
        if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
        event.preventDefault();
        let next = index;
        if (event.key === "Home") next = 0;
        else if (event.key === "End") next = tabs.length - 1;
        else next = (index + (event.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
        selectTab(tabs[next]);
        tabs[next].focus();
      });
    });
  });

  document.querySelectorAll("[role='listbox']").forEach((list, listIndex) => {
    const options = [...list.querySelectorAll("[role='option']")];
    const prefix = list.id || `retro-listbox-${listIndex + 1}`;
    options.forEach((option, optionIndex) => {
      if (!option.id) option.id = `${prefix}-option-${optionIndex + 1}`;
    });
    function selectOption(option) {
      if (!option) return;
      options.forEach(item => item.setAttribute("aria-selected", String(item === option)));
      list.setAttribute("aria-activedescendant", option.id);
    }
    options.forEach(option => option.addEventListener("click", () => {
      selectOption(option);
      list.focus();
    }));
    list.addEventListener("keydown", event => {
      if (!["ArrowDown", "ArrowUp", "Home", "End"].includes(event.key)) return;
      event.preventDefault();
      let index = options.findIndex(option => option.getAttribute("aria-selected") === "true");
      if (event.key === "Home") index = 0;
      else if (event.key === "End") index = options.length - 1;
      else index = Math.max(0, Math.min(options.length - 1, index + (event.key === "ArrowDown" ? 1 : -1)));
      selectOption(options[index]);
      options[index].scrollIntoView({ block: "nearest" });
    });
    selectOption(options.find(option => option.getAttribute("aria-selected") === "true") || options[0]);
  });

  const dialog = document.getElementById("properties-dialog");
  dialog?.addEventListener("keydown", event => {
    if (event.key !== "Tab") return;
    const focusable = [...dialog.querySelectorAll("button:not(:disabled), input:not(:disabled), select:not(:disabled), textarea:not(:disabled), [tabindex]:not([tabindex='-1'])")]
      .filter(element => element.getClientRects().length > 0);
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && (document.activeElement === first || document.activeElement === dialog)) {
      event.preventDefault();
      last?.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first?.focus();
    }
  });
  document.querySelectorAll("[data-open-dialog]").forEach(button => {
    button.addEventListener("click", () => {
      if (!dialog) return;
      closeMenus();
      const parentMenu = button.closest(".menu-popup");
      dialogInvoker = parentMenu ? document.querySelector(`[aria-controls="${parentMenu.id}"]`) : button;
      dialogResult = null;
      dialog.showModal();
      dialog.querySelector("input")?.focus();
    });
  });
  dialog?.querySelectorAll("[data-dialog-result]").forEach(button => {
    button.addEventListener("click", () => { dialogResult = button; });
  });
  dialog?.addEventListener("close", () => {
    feedback(dialogResult?.dataset.dialogResult || "Changes cancelled", dialogResult?.dataset.cue);
    dialogInvoker?.focus();
  });

  document.querySelectorAll("[data-feedback]").forEach(button => {
    button.addEventListener("click", () => feedback(button.dataset.feedback, button.dataset.cue));
  });
  document.querySelectorAll("[data-progress]").forEach(button => {
    button.addEventListener("click", () => {
      const progress = document.getElementById("transfer-progress");
      const output = document.getElementById("progress-output");
      if (!progress) return;
      progress.value = Math.min(100, progress.value + 12);
      if (output) output.value = `${progress.value}%`;
      feedback(progress.value === 100 ? "Transfer complete" : `Transfer progress ${progress.value}%`, progress.value === 100 ? "complete" : "activate");
    });
  });
  document.querySelectorAll("input[type='range'][data-output]").forEach(input => {
    const update = () => {
      const output = document.getElementById(input.dataset.output);
      if (output) output.value = `${input.value}${input.dataset.suffix || ""}`;
    };
    input.addEventListener("input", update);
    update();
  });

  document.querySelector("[data-sound-enable]")?.addEventListener("change", event => {
    soundEnabled = event.target.checked;
    storage.set("sound-enabled", soundEnabled);
    updateAudioControls();
    feedback(soundEnabled ? "Sound enabled" : "Sound disabled", soundEnabled ? "activate" : null);
  });
  document.querySelector("[data-mute]")?.addEventListener("click", () => {
    muted = !muted;
    storage.set("muted", muted);
    updateAudioControls();
    status(muted ? "Sound muted" : "Sound unmuted");
  });
  document.querySelector("[data-volume]")?.addEventListener("input", event => {
    volume = Number(event.target.value) / 100;
    storage.set("volume", event.target.value);
  });
  document.querySelector("[data-reduced-transparency-control]")?.addEventListener("change", event => {
    root.dataset.reducedTransparency = String(event.target.checked);
    status(event.target.checked ? "Opaque surfaces enabled" : "Theme transparency restored");
  });
  document.querySelector("[data-reduced-motion-control]")?.addEventListener("change", event => {
    root.dataset.reducedMotion = String(event.target.checked);
    status(event.target.checked ? "Reduced motion enabled" : "Theme motion restored");
  });

  const savedTheme = storage.get("theme");
  applyTheme(validThemes.has(savedTheme) ? savedTheme : root.dataset.theme);
  const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");
  const motionControl = document.querySelector("[data-reduced-motion-control]");
  if (motionControl) {
    motionControl.checked = motionPreference.matches;
    root.dataset.reducedMotion = String(motionPreference.matches);
  }
  const volumeControl = document.querySelector("[data-volume]");
  if (volumeControl) volumeControl.value = String(Math.round(volume * 100));
  updateAudioControls();
})();
