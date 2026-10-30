/**
 * Travel Ticket Booking System - Search Results Controller (search.js)
 * Manages transport queries, live filters, sorting, and dynamic card generation.
 */

document.addEventListener("DOMContentLoaded", () => {
  initSearchPage();
});

let currentTransports = [];
let filteredTransports = [];
let queryParams = {};

function initSearchPage() {
  parseQueryParams();
  setupFilterListeners();
  executeSearch();
}

// 1. Extract query parameters from URL
function parseQueryParams() {
  const params = new URLSearchParams(window.location.search);
  queryParams = {
    source: (params.get("source") || "").trim(),
    destination: (params.get("destination") || "").trim(),
    date: params.get("date") || getDefaultTomorrowDate(),
    type: (params.get("type") || "all").toLowerCase(),
    passengers: parseInt(params.get("passengers")) || 1
  };

  // Populate search summary bar if elements exist
  const sourceElem = document.getElementById("summarySource");
  const destElem = document.getElementById("summaryDest");
  const dateElem = document.getElementById("summaryDate");
  const typeElem = document.getElementById("summaryType");

  if (sourceElem) sourceElem.textContent = queryParams.source || "All Sources";
  if (destElem) destElem.textContent = queryParams.destination || "All Destinations";
  if (dateElem) dateElem.textContent = formatDateDisplay(queryParams.date);
  if (typeElem) typeElem.textContent = queryParams.type === "all" ? "Buses & Trains" : queryParams.type.toUpperCase();

  // Populate top input controls if present
  const srcIn = document.getElementById("sourceInput");
  const dstIn = document.getElementById("destInput");
  const dateIn = document.getElementById("dateInput");
  if (srcIn) srcIn.value = queryParams.source;
  if (dstIn) dstIn.value = queryParams.destination;
  if (dateIn) dateIn.value = queryParams.date;
}

function getDefaultTomorrowDate() {
  const d = new Date();
  d.setDate(d.getDate() + 1);
  return d.toISOString().split("T")[0];
}

function formatDateDisplay(dateStr) {
  if (!dateStr) return "";
  const d = new Date(dateStr + "T00:00:00");
  return d.toLocaleDateString("en-IN", { weekday: "short", day: "numeric", month: "short", year: "numeric" });
}

// 2. Fetch and filter data
function executeSearch() {
  const allTransports = Storage.getTransports();

  // Primary filtering
  currentTransports = allTransports.filter(item => {
    // Source filter
    if (queryParams.source && !item.source.toLowerCase().includes(queryParams.source.toLowerCase())) {
      return false;
    }
    // Destination filter
    if (queryParams.destination && !item.destination.toLowerCase().includes(queryParams.destination.toLowerCase())) {
      return false;
    }
    // Transport type filter
    if (queryParams.type !== "all" && item.type.toLowerCase() !== queryParams.type) {
      return false;
    }
    return true;
  });

  // Calculate live available seats for each transport for the chosen date
  currentTransports = currentTransports.map(item => {
    const availableSeats = Storage.getAvailableSeatsCount(item.id, queryParams.date);
    return { ...item, availableSeats };
  });

  applySidebarFilters();
}

// 3. Setup interactive filters
function setupFilterListeners() {
  // Price slider
  const priceSlider = document.getElementById("priceSlider");
  const maxPriceLabel = document.getElementById("maxPriceLabel");
  if (priceSlider && maxPriceLabel) {
    priceSlider.addEventListener("input", (e) => {
      maxPriceLabel.textContent = `₹${e.target.value}`;
      applySidebarFilters();
    });
  }

  // Type checkboxes
  document.querySelectorAll(".type-filter-checkbox").forEach(cb => {
    cb.addEventListener("change", applySidebarFilters);
  });

  // Time slot buttons
  document.querySelectorAll(".time-slot-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      btn.classList.toggle("active");
      applySidebarFilters();
    });
  });

  // Sort select
  const sortSelect = document.getElementById("sortSelect");
  if (sortSelect) {
    sortSelect.addEventListener("change", applySidebarFilters);
  }

  // Reset filters button
  const resetBtn = document.getElementById("resetFiltersBtn");
  if (resetBtn) {
    resetBtn.addEventListener("click", resetAllFilters);
  }
}

function resetAllFilters() {
  const priceSlider = document.getElementById("priceSlider");
  const maxPriceLabel = document.getElementById("maxPriceLabel");
  if (priceSlider) {
    priceSlider.value = 2000;
    if (maxPriceLabel) maxPriceLabel.textContent = "₹2000";
  }

  document.querySelectorAll(".type-filter-checkbox").forEach(cb => cb.checked = true);
  document.querySelectorAll(".time-slot-btn").forEach(btn => btn.classList.remove("active"));
  
  const sortSelect = document.getElementById("sortSelect");
  if (sortSelect) sortSelect.value = "price-asc";

  applySidebarFilters();
}

// 4. Apply all active filters and sort
function applySidebarFilters() {
  filteredTransports = [...currentTransports];

  // 1. Price Filter
  const priceSlider = document.getElementById("priceSlider");
  if (priceSlider) {
    const maxPrice = Number(priceSlider.value);
    filteredTransports = filteredTransports.filter(t => t.price <= maxPrice);
  }

  // 2. Transport Type Checkboxes
  const busChecked = document.getElementById("filterBus")?.checked ?? true;
  const trainChecked = document.getElementById("filterTrain")?.checked ?? true;

  if (!busChecked && !trainChecked) {
    filteredTransports = [];
  } else if (!busChecked) {
    filteredTransports = filteredTransports.filter(t => t.type === "train");
  } else if (!trainChecked) {
    filteredTransports = filteredTransports.filter(t => t.type === "bus");
  }

  // 3. Departure Time Slots
  const activeTimeSlots = Array.from(document.querySelectorAll(".time-slot-btn.active"))
    .map(btn => btn.dataset.slot);

  if (activeTimeSlots.length > 0) {
    filteredTransports = filteredTransports.filter(t => {
      const hour = parseInt(t.departureTime.split(":")[0], 10);
      if (activeTimeSlots.includes("morning") && hour >= 6 && hour < 12) return true;
      if (activeTimeSlots.includes("afternoon") && hour >= 12 && hour < 18) return true;
      if (activeTimeSlots.includes("evening") && hour >= 18 && hour < 23) return true;
      if (activeTimeSlots.includes("night") && (hour >= 23 || hour < 6)) return true;
      return false;
    });
  }

  // 4. Sorting
  const sortSelect = document.getElementById("sortSelect");
  const sortVal = sortSelect ? sortSelect.value : "price-asc";

  if (sortVal === "price-asc") {
    filteredTransports.sort((a, b) => a.price - b.price);
  } else if (sortVal === "price-desc") {
    filteredTransports.sort((a, b) => b.price - a.price);
  } else if (sortVal === "rating-desc") {
    filteredTransports.sort((a, b) => (b.rating || 0) - (a.rating || 0));
  } else if (sortVal === "time-asc") {
    filteredTransports.sort((a, b) => a.departureTime.localeCompare(b.departureTime));
  }

  renderResults();
}

// 5. Render result cards
function renderResults() {
  const container = document.getElementById("searchResultsContainer");
  const countBadge = document.getElementById("resultsCountBadge");

  if (countBadge) {
    countBadge.textContent = `${filteredTransports.length} Options Available`;
  }

  if (!container) return;

  if (filteredTransports.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">🚌</div>
        <h3>No Tickets Found</h3>
        <p>No buses or trains match your current search criteria. Try modifying your search route or clearing the filters.</p>
        <button class="btn btn-primary" onclick="resetAllFilters()">Reset All Filters</button>
      </div>
    `;
    return;
  }

  container.innerHTML = filteredTransports.map(t => {
    const isBus = t.type === "bus";
    const typeBadge = isBus 
      ? `<span class="badge badge-primary">BUS</span>` 
      : `<span class="badge badge-secondary">TRAIN</span>`;

    const seatsClass = t.availableSeats < 10 ? "seats-badge low" : "seats-badge";

    const amenitiesHtml = (t.amenities || []).slice(0, 4).map(a => `
      <span class="amenity-chip">
        <span style="color: var(--secondary);">•</span> ${a}
      </span>
    `).join("");

    return `
      <div class="transport-card">
        <div class="transport-card-main">
          <!-- Info Column -->
          <div class="transport-info-col">
            <div class="transport-header-line">
              ${typeBadge}
              <h3 class="transport-name">${t.name}</h3>
            </div>
            <div class="transport-category">${t.category}</div>
            <div class="transport-rating-badge">
              ★ ${t.rating || "4.6"} <span style="font-weight: 400; opacity: 0.9;">(${t.reviewsCount || 120})</span>
            </div>
          </div>

          <!-- Schedule Timeline -->
          <div class="transport-schedule-col">
            <div class="time-point">
              <span class="time">${t.departureTime}</span>
              <span class="city">${t.source}</span>
            </div>
            <div class="journey-timeline">
              <span class="journey-duration">${t.duration}</span>
              <div class="timeline-line"></div>
            </div>
            <div class="time-point" style="text-align: right;">
              <span class="time">${t.arrivalTime}</span>
              <span class="city">${t.destination}</span>
            </div>
          </div>

          <!-- Price & Action -->
          <div class="transport-action-col">
            <div class="fare-box">
              <div class="fare-label">Starting From</div>
              <div class="fare-amount">₹${t.price}</div>
            </div>
            <div class="${seatsClass}">${t.availableSeats} seats left</div>
            <a href="seat-selection.html?id=${t.id}&date=${queryParams.date}&passengers=${queryParams.passengers}" class="btn btn-primary btn-sm btn-block">
              View Seats
            </a>
          </div>
        </div>

        <!-- Footer Strip with Amenities -->
        <div class="transport-card-footer">
          <div class="amenities-list">
            ${amenitiesHtml}
          </div>
          <div style="font-size: 0.8rem; font-weight: 600;">
            Boarding: ${t.boardingPoints ? t.boardingPoints[0] : t.source}
          </div>
        </div>
      </div>
    `;
  }).join("");
}
