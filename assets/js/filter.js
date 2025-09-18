document.addEventListener("DOMContentLoaded", function () {
  const filterButtons = document.querySelectorAll(".filter-btn");
  const cards = document.querySelectorAll(".community-card");
  const allButton = document.querySelector('.filter-btn[data-filter="all"]');
  const modeToggle = document.getElementById("filter-mode-toggle");

  let filterMode = "OR"; // 'OR', 'AND', or 'NOT'
  const modes = ["OR", "AND", "NOT"];

  // Update mode toggle text and apply filtering
  function updateMode() {
    if (modeToggle) {
      const modeText = {
        OR: "CURRENT MODE: OR (ANY OF)",
        AND: "CURRENT MODE: AND (ALL OF)",
        NOT: "CURRENT MODE: NOT (NONE OF)",
      };

      const nextMode = modes[(modes.indexOf(filterMode) + 1) % modes.length];
      const ariaText = {
        OR: "Switch to ALL mode",
        AND: "Switch to NONE mode",
        NOT: "Switch to ANY mode",
      };

      modeToggle.textContent = modeText[filterMode];
      modeToggle.setAttribute("aria-label", ariaText[filterMode]);
    }
    applyFilters();
  }

  // Apply current filters based on mode
  function applyFilters() {
    const activeFilters = Array.from(
      document.querySelectorAll(".filter-btn.active")
    )
      .map((btn) => btn.dataset.filter)
      .filter((filter) => filter !== "all");

    if (activeFilters.length === 0) {
      cards.forEach((card) => (card.style.display = "block"));
    } else {
      cards.forEach((card) => {
        const tags = card.dataset.tags.split(" ");
        let shouldShow = false;

        switch (filterMode) {
          case "OR":
            // Show if card has ANY of the selected tags
            shouldShow = activeFilters.some((filter) => tags.includes(filter));
            break;
          case "AND":
            // Show if card has ALL of the selected tags
            shouldShow = activeFilters.every((filter) => tags.includes(filter));
            break;
          case "NOT":
            // Show if card has NONE of the selected tags
            shouldShow = !activeFilters.some((filter) => tags.includes(filter));
            break;
        }

        card.style.display = shouldShow ? "block" : "none";
      });
    }
  }

  // Mode toggle functionality
  if (modeToggle) {
    modeToggle.addEventListener("click", () => {
      const currentIndex = modes.indexOf(filterMode);
      filterMode = modes[(currentIndex + 1) % modes.length];
      updateMode();
    });
  }

  // Filter button functionality
  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.filter;

      if (filter === "all") {
        // Clear all other selections and show all cards
        filterButtons.forEach((btn) => btn.classList.remove("active"));
        button.classList.add("active");
        cards.forEach((card) => (card.style.display = "block"));
      } else {
        // Remove "All" selection if a specific filter is clicked
        allButton.classList.remove("active");

        // Toggle the clicked button
        button.classList.toggle("active");

        // Get all currently active filters
        const activeFilters = Array.from(
          document.querySelectorAll(".filter-btn.active")
        )
          .map((btn) => btn.dataset.filter)
          .filter((filter) => filter !== "all");

        // If no filters are active, show all cards
        if (activeFilters.length === 0) {
          allButton.classList.add("active");
          cards.forEach((card) => (card.style.display = "block"));
        } else {
          applyFilters();
        }
      }
    });
  });

  // Initialize mode display
  updateMode();
});
