/**
 * Travel Ticket Booking System - Seat Selection Controller (seats.js)
 * Visual seat layout, real-time seat status, multi-seat selection, fare calculation.
 */

let currentTransport = null;
let journeyDate = "";
let selectedSeats = [];
let bookedSeats = [];
const MAX_SEATS = 6;

document.addEventListener("DOMContentLoaded", () => {
  initSeatSelection();
});

function initSeatSelection() {
  const params = new URLSearchParams(window.location.search);
  const transportId = params.get("id");
  journeyDate = params.get("date") || new Date().toISOString().split("T")[0];

  if (!transportId) {
    showToast("No transport selected. Redirecting to search...", "warning");
    setTimeout(() => { window.location.href = "search.html"; }, 1500);
    return;
  }

  currentTransport = Storage.getTransportById(transportId);
  if (!currentTransport) {
    showToast("Transport not found. Redirecting to search...", "error");
    setTimeout(() => { window.location.href = "search.html"; }, 1500);
    return;
  }

  // Load booked seats for this transport & journey date
  bookedSeats = Storage.getBookedSeats(currentTransport.id, journeyDate);

  // Render header info
  renderHeaderInfo();

  // Generate visual seat layout
  renderSeatLayout();

  // Setup continue button
  const proceedBtn = document.getElementById("proceedToBookingBtn");
  if (proceedBtn) {
    proceedBtn.addEventListener("click", proceedToCheckout);
  }
}

function renderHeaderInfo() {
  const nameElem = document.getElementById("transportName");
  const catElem = document.getElementById("transportCategory");
  const routeElem = document.getElementById("transportRoute");
  const dateElem = document.getElementById("journeyDateDisplay");
  const fareElem = document.getElementById("seatBaseFare");

  if (nameElem) nameElem.textContent = currentTransport.name;
  if (catElem) catElem.textContent = currentTransport.category;
  if (routeElem) routeElem.textContent = `${currentTransport.source} ➔ ${currentTransport.destination}`;
  if (dateElem) {
    const d = new Date(journeyDate + "T00:00:00");
    dateElem.textContent = d.toLocaleDateString("en-IN", { weekday: "short", day: "numeric", month: "short", year: "numeric" });
  }
  if (fareElem) fareElem.textContent = `₹${currentTransport.price}`;
}

// Generate the visual seat layout
function renderSeatLayout() {
  const container = document.getElementById("seatDeckContainer");
  if (!container) return;

  const isBus = currentTransport.type === "bus";
  const totalSeats = currentTransport.totalSeats || (isBus ? 32 : 54);

  let html = "";

  if (isBus) {
    // Bus Layout: 2 seats left, aisle, 2 seats right (or 1 sleeper)
    const isSleeper = currentTransport.category.toLowerCase().includes("sleeper");
    const rows = Math.ceil(totalSeats / (isSleeper ? 3 : 4));

    for (let r = 1; r <= rows; r++) {
      const seatLeft1 = `L${r}A`;
      const seatLeft2 = isSleeper ? null : `L${r}B`;
      const seatRight1 = isSleeper ? `R${r}A` : `R${r}A`;
      const seatRight2 = `R${r}B`;

      html += `
        <div class="seat-row">
          <div class="seat-pair">
            ${createSeatButton(seatLeft1, isSleeper)}
            ${seatLeft2 ? createSeatButton(seatLeft2, isSleeper) : ""}
          </div>
          <div class="seat-aisle">Aisle</div>
          <div class="seat-pair">
            ${createSeatButton(seatRight1, isSleeper)}
            ${createSeatButton(seatRight2, isSleeper)}
          </div>
        </div>
      `;
    }
  } else {
    // Train Layout: 3 seats left, aisle, 2 seats right (CC Style)
    const rows = Math.ceil(totalSeats / 5);
    for (let r = 1; r <= rows; r++) {
      const s1 = `C${(r - 1) * 5 + 1}`;
      const s2 = `C${(r - 1) * 5 + 2}`;
      const s3 = `C${(r - 1) * 5 + 3}`;
      const s4 = `C${(r - 1) * 5 + 4}`;
      const s5 = `C${(r - 1) * 5 + 5}`;

      html += `
        <div class="seat-row">
          <div class="seat-pair" style="gap: 6px;">
            ${createSeatButton(s1, false)}
            ${createSeatButton(s2, false)}
            ${createSeatButton(s3, false)}
          </div>
          <div class="seat-aisle">Aisle</div>
          <div class="seat-pair" style="gap: 6px;">
            ${createSeatButton(s4, false)}
            ${createSeatButton(s5, false)}
          </div>
        </div>
      `;
    }
  }

  container.innerHTML = html;

  // Add click handlers to seats
  container.querySelectorAll(".seat-btn:not(.booked)").forEach(btn => {
    btn.addEventListener("click", () => toggleSeat(btn.dataset.seatId));
  });
}

function createSeatButton(seatId, isSleeper) {
  const isBooked = bookedSeats.includes(seatId);
  const isSelected = selectedSeats.includes(seatId);

  let classes = "seat-btn";
  if (isSleeper) classes += " sleeper";
  if (isBooked) classes += " booked";
  if (isSelected) classes += " selected";

  return `
    <button 
      type="button" 
      class="${classes}" 
      data-seat-id="${seatId}" 
      title="${isBooked ? 'Seat ' + seatId + ' is already booked' : 'Seat ' + seatId}"
      ${isBooked ? "disabled" : ""}
    >
      ${seatId}
    </button>
  `;
}

function toggleSeat(seatId) {
  const index = selectedSeats.indexOf(seatId);

  if (index > -1) {
    selectedSeats.splice(index, 1);
  } else {
    if (selectedSeats.length >= MAX_SEATS) {
      showToast(`You can select a maximum of ${MAX_SEATS} seats.`, "warning");
      return;
    }
    selectedSeats.push(seatId);
  }

  updateSeatUI();
  calculateFare();
}

function updateSeatUI() {
  // Update seat button classes
  document.querySelectorAll(".seat-btn").forEach(btn => {
    const seatId = btn.dataset.seatId;
    if (selectedSeats.includes(seatId)) {
      btn.classList.add("selected");
    } else {
      btn.classList.remove("selected");
    }
  });

  // Render chips
  const chipsContainer = document.getElementById("selectedSeatsChips");
  if (chipsContainer) {
    if (selectedSeats.length === 0) {
      chipsContainer.innerHTML = `<span style="font-size: 0.85rem; color: #94a3b8; font-style: italic;">No seats selected yet. Click on available green seats.</span>`;
    } else {
      chipsContainer.innerHTML = selectedSeats.map(seat => `
        <span class="selected-chip">
          Seat ${seat}
          <button style="background: none; border: none; cursor: pointer; color: inherit; font-size: 0.8rem; margin-left: 4px;" onclick="toggleSeat('${seat}')">✕</button>
        </span>
      `).join("");
    }
  }

  // Count display
  const countDisplay = document.getElementById("selectedSeatsCount");
  if (countDisplay) {
    countDisplay.textContent = selectedSeats.length;
  }
}

function calculateFare() {
  const count = selectedSeats.length;
  const price = currentTransport.price;
  const baseTotal = count * price;
  const tax = Math.round(baseTotal * 0.05); // 5% GST
  const grandTotal = baseTotal + tax;

  const baseFareElem = document.getElementById("summaryBaseFare");
  const taxElem = document.getElementById("summaryTax");
  const grandTotalElem = document.getElementById("summaryGrandTotal");
  const proceedBtn = document.getElementById("proceedToBookingBtn");

  if (baseFareElem) baseFareElem.textContent = `₹${baseTotal}`;
  if (taxElem) taxElem.textContent = `₹${tax}`;
  if (grandTotalElem) grandTotalElem.textContent = `₹${grandTotal}`;

  if (proceedBtn) {
    proceedBtn.disabled = count === 0;
    if (count > 0) {
      proceedBtn.textContent = `Continue to Booking (₹${grandTotal})`;
    } else {
      proceedBtn.textContent = "Select Seats to Continue";
    }
  }
}

function proceedToCheckout() {
  if (selectedSeats.length === 0) {
    showToast("Please select at least 1 seat to continue.", "warning");
    return;
  }

  const baseTotal = selectedSeats.length * currentTransport.price;
  const tax = Math.round(baseTotal * 0.05);
  const grandTotal = baseTotal + tax;

  const checkoutData = {
    transportId: currentTransport.id,
    journeyDate: journeyDate,
    selectedSeats: [...selectedSeats],
    farePerSeat: currentTransport.price,
    baseTotal: baseTotal,
    tax: tax,
    grandTotal: grandTotal
  };

  sessionStorage.setItem("tb_currentCheckout", JSON.stringify(checkoutData));

  // Enforce login before proceeding to checkout
  if (!Auth.isAuthenticated()) {
    showToast("Please sign in or create an account to proceed with booking.", "warning", 3000);
    setTimeout(() => {
      window.location.href = "login.html?redirect=booking.html";
    }, 1200);
    return;
  }

  window.location.href = "booking.html";
}
