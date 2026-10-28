(() => {
  "use strict";

  document.addEventListener("focusin", event => {
    if (event.target.matches("button, input, select, textarea, [tabindex]")) event.target.classList.add("is-focused");
  });
  document.addEventListener("focusout", event => {
    if (!event.target.hasAttribute("data-state")) event.target.classList.remove("is-focused");
  });
  document.querySelectorAll("[data-show-error]").forEach(button => {
    button.addEventListener("click", () => {
      const message = document.getElementById("dynamic-error");
      if (!message) return;
      message.hidden = !message.hidden;
      button.setAttribute("aria-expanded", String(!message.hidden));
      document.getElementById("error-input")?.setAttribute("aria-invalid", String(!message.hidden));
    });
  });
  document.documentElement.dataset.galleryReady = "true";
})();
