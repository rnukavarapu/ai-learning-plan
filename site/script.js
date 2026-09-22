(function () {
  const STORAGE_KEY = "ai-learning-plan-lectures-v1";
  const allLectureIds = window.ALL_LECTURE_IDS || [];
  const phaseLectures = window.PHASE_LECTURES || {};

  function loadProgress() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch (e) {
      return {};
    }
  }

  function saveProgress(progress) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }

  function applyProgress(progress) {
    // Content checkboxes + lecture wrapper highlight (only present on the
    // current phase's page — harmless no-op elsewhere).
    document.querySelectorAll(".lecture-checkbox").forEach((box) => {
      const id = box.getAttribute("data-lecture");
      const done = !!progress[id];
      box.checked = done;
      const lecture = document.getElementById(id);
      if (lecture) lecture.classList.toggle("is-complete", done);
    });

    // Sidebar checkmarks (present on every page).
    document.querySelectorAll(".lecture-link").forEach((link) => {
      const id = link.getAttribute("data-lecture");
      const check = link.querySelector(".lecture-check");
      const done = !!progress[id];
      link.classList.toggle("is-complete", done);
      if (check) check.textContent = done ? "✓" : "○";
    });

    // Per-phase fraction + "complete" pill, everywhere the phase appears.
    Object.keys(phaseLectures).forEach((phaseId) => {
      const ids = phaseLectures[phaseId];
      const done = ids.filter((id) => progress[id]).length;
      const isDone = done === ids.length && ids.length > 0;
      document.querySelectorAll(`[data-fraction="${phaseId}"]`).forEach((el) => {
        el.textContent = `${done}/${ids.length}`;
      });
      const section = document.getElementById(phaseId);
      if (section) section.classList.toggle("is-complete", isDone);
      const group = document.querySelector(`[data-phase-group="${phaseId}"]`);
      if (group) group.classList.toggle("is-complete", isDone);
      const card = document.querySelector(`.phase-card[href="${phaseId}.html"]`);
      if (card) card.classList.toggle("is-complete", isDone);
    });

    // Overall progress bar (same total shown on every page).
    const doneTotal = allLectureIds.filter((id) => progress[id]).length;
    const total = allLectureIds.length || 1;
    const pct = Math.round((doneTotal / total) * 100);
    const fill = document.getElementById("progress-fill");
    const label = document.getElementById("progress-label");
    if (fill) fill.style.width = pct + "%";
    if (label) label.textContent = `${doneTotal} / ${allLectureIds.length} lectures complete`;
  }

  function initProgress() {
    const progress = loadProgress();
    applyProgress(progress);

    document.querySelectorAll(".lecture-checkbox").forEach((box) => {
      box.addEventListener("change", () => {
        const id = box.getAttribute("data-lecture");
        const current = loadProgress();
        current[id] = box.checked;
        saveProgress(current);
        applyProgress(current);
      });
    });
  }

  function initMobileMenu() {
    const toggle = document.getElementById("menu-toggle");
    const scrim = document.getElementById("sidebar-scrim");
    const sidebar = document.getElementById("sidebar");
    if (!toggle || !scrim || !sidebar) return;

    function close() {
      document.body.classList.remove("sidebar-open");
    }

    toggle.addEventListener("click", () => {
      document.body.classList.toggle("sidebar-open");
    });
    scrim.addEventListener("click", close);
    // Only real navigation (not the expand/collapse chevron) should close the drawer.
    sidebar.querySelectorAll(".lecture-link, .nav-link, .nav-phase-link").forEach((link) => {
      link.addEventListener("click", close);
    });
  }

  function initNavSearch() {
    const input = document.getElementById("nav-search");
    if (!input) return;
    const groups = Array.from(document.querySelectorAll(".sidebar > .nav-group-label"));

    input.addEventListener("input", () => {
      const q = input.value.trim().toLowerCase();
      groups.forEach((label) => {
        const list = label.nextElementSibling;
        if (!list) return;
        let visibleCount = 0;
        Array.from(list.children).forEach((li) => {
          const searchTarget = li.querySelector(".nav-link, .nav-phase-link");
          const haystack = (searchTarget && (searchTarget.getAttribute("data-search") || searchTarget.textContent) || "").toLowerCase();
          const match = !q || haystack.includes(q);
          li.style.display = match ? "" : "none";
          if (match) visibleCount++;
        });
        label.style.display = visibleCount ? "" : "none";
      });
    });
  }

  function initCollapsibleSections() {
    // Expand/collapse state is set server-side (the current page's phase
    // starts expanded); this just wires up the toggle, it doesn't decide
    // the default.
    document.querySelectorAll(".nav-chevron-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const group = btn.closest(".nav-phase-group");
        if (group) group.classList.toggle("expanded");
      });
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initProgress();
    initMobileMenu();
    initNavSearch();
    initCollapsibleSections();
  });
})();
