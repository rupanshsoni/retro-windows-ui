(() => {
  "use strict";

  const root = document.documentElement;
  const narrow = window.matchMedia("(max-width: 900px)");
  const drag = { window: null, pointerId: null, offsetX: 0, offsetY: 0 };

  function currentTheme() {
    return root.dataset.theme || "xp-luna-blue";
  }

  function openWindow(id) {
    const target = document.querySelector(`[data-window="${id}"]`);
    if (!target) return;
    if (narrow.matches) {
      document.querySelectorAll("[data-window]").forEach(window => {
        if (window !== target) {
          window.hidden = true;
          const otherTask = document.querySelector(`[data-task-window="${window.dataset.window}"]`);
          if (otherTask) otherTask.hidden = true;
        }
      });
    }
    target.hidden = false;
    const task = document.querySelector(`[data-task-window="${id}"]`);
    if (task) task.hidden = false;
    document.querySelectorAll("[data-window]").forEach(window => {
      window.classList.toggle("active", window === target);
      window.classList.toggle("inactive", window !== target);
    });
    document.querySelectorAll("[data-task-window]").forEach(button => {
      button.setAttribute("aria-pressed", String(button.dataset.taskWindow === id));
    });
    const focusTarget = target.querySelector("[data-window-focus], h2, button, a, input, select");
    if (focusTarget) focusTarget.focus({ preventScroll: true });
    const startMenu = document.getElementById("start-menu");
    if (startMenu) startMenu.hidden = true;
    document.getElementById("start-button")?.setAttribute("aria-expanded", "false");
  }

  document.addEventListener("click", event => {
    const opener = event.target.closest("[data-open-window]");
    if (opener) {
      event.preventDefault();
      openWindow(opener.dataset.openWindow);
    }
  });

  document.getElementById("theme-select").addEventListener("change", () => {
    window.setTimeout(() => {
      document.querySelectorAll("[data-brand-start]").forEach(image => {
        image.src = `../brand/${currentTheme()}-start.svg`;
      });
    }, 0);
  });

  document.querySelectorAll(".mockup-window .titlebar").forEach(titlebar => {
    titlebar.addEventListener("pointerdown", event => {
      if (event.button !== 0 || event.target.closest("button, input, select, a")) return;
      const target = titlebar.closest(".mockup-window");
      if (!target || target.classList.contains("maximized") || narrow.matches) return;
      const rect = target.getBoundingClientRect();
      drag.window = target;
      drag.pointerId = event.pointerId;
      drag.offsetX = event.clientX - rect.left;
      drag.offsetY = event.clientY - rect.top;
      target.style.left = `${rect.left}px`;
      target.style.top = `${rect.top}px`;
      target.style.right = "auto";
      titlebar.setPointerCapture(event.pointerId);
      event.preventDefault();
    });

    titlebar.addEventListener("pointermove", event => {
      if (!drag.window || drag.pointerId !== event.pointerId) return;
      const maxLeft = Math.max(0, window.innerWidth - drag.window.offsetWidth);
      const maxTop = Math.max(0, window.innerHeight - drag.window.offsetHeight - 40);
      drag.window.style.left = `${Math.min(maxLeft, Math.max(0, event.clientX - drag.offsetX))}px`;
      drag.window.style.top = `${Math.min(maxTop, Math.max(0, event.clientY - drag.offsetY))}px`;
    });

    function endDrag(event) {
      if (!drag.window || drag.pointerId !== event.pointerId) return;
      drag.window = null;
      drag.pointerId = null;
    }
    titlebar.addEventListener("pointerup", endDrag);
    titlebar.addEventListener("pointercancel", endDrag);
  });
})();
