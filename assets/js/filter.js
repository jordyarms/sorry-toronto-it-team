document.addEventListener("DOMContentLoaded", function () {
  const filterButtons = document.querySelectorAll(".filter-btn");
  const cards = document.querySelectorAll(".community-card");
  const allButton = document.querySelector('.filter-btn[data-filter="all"]');
  const modeToggle = document.getElementById("filter-mode-toggle");

  let isAndMode = false; // false = OR mode, true = AND mode

  // Update mode toggle text and apply filtering
  function updateMode() {
    if (modeToggle) {
      modeToggle.textContent = isAndMode ? "Mode: ALL (AND)" : "Mode: ANY (OR)";
      modeToggle.setAttribute(
        "aria-label",
        isAndMode ? "Switch to ANY mode" : "Switch to ALL mode"
      );
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
        const hasMatchingTag = isAndMode
          ? activeFilters.every((filter) => tags.includes(filter)) // AND logic
          : activeFilters.some((filter) => tags.includes(filter)); // OR logic
        card.style.display = hasMatchingTag ? "block" : "none";
      });
    }
  }

  // Mode toggle functionality
  if (modeToggle) {
    modeToggle.addEventListener("click", () => {
      isAndMode = !isAndMode;
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
