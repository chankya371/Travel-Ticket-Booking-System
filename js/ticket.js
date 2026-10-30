/**
 * Travel Ticket Booking System - E-Ticket Controller (ticket.js)
 * Boarding pass renderer, SVG QR generator, print & download PDF actions.
 */

document.addEventListener("DOMContentLoaded", () => {
  initTicketPage();
});

function initTicketPage() {
  const params = new URLSearchParams(window.location.search);
  const bookingId = params.get("id");

  if (!bookingId) {
    showTicketError("No Booking ID provided in URL.");
    return;
  }

  const booking = Storage.getBookingById(bookingId);
  if (!booking) {
    showTicketError(`Booking with ID "${bookingId}" could not be found.`);
    return;
  }

  renderTicketData(booking);
  setupTicketActions(booking);
}

function showTicketError(msg) {
  const wrapper = document.getElementById("ticketContainer");
  if (wrapper) {
    wrapper.innerHTML = `
      <div class="empty-state" style="margin: 2rem auto; max-width: 600px;">
        <div class="empty-state-icon">⚠️</div>
        <h3>Ticket Not Found</h3>
        <p>${msg}</p>
        <div style="display: flex; gap: 12px; justify-content: center;">
          <a href="index.html" class="btn btn-outline">Go to Home</a>
          <a href="my-bookings.html" class="btn btn-primary">My Bookings</a>
        </div>
      </div>
    `;
  }
}

function renderTicketData(b) {
  // Booking ID & Header
  const idElem = document.getElementById("ticketBookingId");
  const transportNameElem = document.getElementById("ticketTransportName");
  const categoryElem = document.getElementById("ticketCategory");

  if (idElem) idElem.textContent = b.id;
  if (transportNameElem) transportNameElem.textContent = b.transportName;
  if (categoryElem) categoryElem.textContent = b.category || b.transportType.toUpperCase();

  // Route & Timings
  const srcElem = document.getElementById("ticketSourceCity");
  const dstElem = document.getElementById("ticketDestCity");
  const depTimeElem = document.getElementById("ticketDepTime");
  const arrTimeElem = document.getElementById("ticketArrTime");
  const depDateElem = document.getElementById("ticketDepDate");
  const durationElem = document.getElementById("ticketDuration");

  const formattedDate = new Date(b.journeyDate + "T00:00:00").toLocaleDateString("en-IN", {
    weekday: "short", day: "numeric", month: "short", year: "numeric"
  });

  if (srcElem) srcElem.textContent = b.source;
  if (dstElem) dstElem.textContent = b.destination;
  if (depTimeElem) depTimeElem.textContent = b.departureTime;
  if (arrTimeElem) arrTimeElem.textContent = b.arrivalTime;
  if (depDateElem) depDateElem.textContent = formattedDate;
  if (durationElem) durationElem.textContent = b.duration || "Direct";

  // Passenger Manifest Table
  const manifestBody = document.getElementById("ticketPassengersBody");
  if (manifestBody && Array.isArray(b.passengers)) {
    manifestBody.innerHTML = b.passengers.map(p => `
      <tr>
        <td><span class="manifest-seat-badge">${p.seat}</span></td>
        <td style="font-weight: 700;">${p.name}</td>
        <td>${p.age} yrs</td>
        <td>${p.gender}</td>
      </tr>
    `).join("");
  }

  // Status Badge
  const statusElem = document.getElementById("ticketStatusBadge");
  if (statusElem) {
    statusElem.textContent = b.bookingStatus;
    statusElem.className = b.bookingStatus === "Confirmed" 
      ? "ticket-status-pill confirmed" 
      : "ticket-status-pill cancelled";
  }

  // Fare Details
  const baseFareElem = document.getElementById("ticketBaseFare");
  const taxElem = document.getElementById("ticketTax");
  const discountElem = document.getElementById("ticketDiscount");
  const finalAmountElem = document.getElementById("ticketFinalAmount");
  const paymentMethodElem = document.getElementById("ticketPaymentMethod");

  if (baseFareElem) baseFareElem.textContent = `₹${b.totalFare}`;
  if (taxElem) taxElem.textContent = `₹${b.tax || 0}`;
  if (discountElem) discountElem.textContent = `-₹${b.discount || 0}`;
  if (finalAmountElem) finalAmountElem.textContent = `₹${b.finalAmount}`;
  if (paymentMethodElem) paymentMethodElem.textContent = b.paymentMethod;

  // Render QR Code SVG
  renderQrCodeSvg(b.id);
}

// Generate an SVG QR code graphic representation
function renderQrCodeSvg(bookingId) {
  const qrFrame = document.getElementById("ticketQrFrame");
  if (!qrFrame) return;

  qrFrame.innerHTML = `
    <svg viewBox="0 0 100 100" fill="currentColor">
      <!-- Outer Framing Marks -->
      <rect x="5" y="5" width="26" height="26" fill="#0f172a" rx="4"/>
      <rect x="9" y="9" width="18" height="18" fill="#ffffff" rx="2"/>
      <rect x="13" y="13" width="10" height="10" fill="#0f172a" rx="1"/>

      <rect x="69" y="5" width="26" height="26" fill="#0f172a" rx="4"/>
      <rect x="73" y="9" width="18" height="18" fill="#ffffff" rx="2"/>
      <rect x="77" y="13" width="10" height="10" fill="#0f172a" rx="1"/>

      <rect x="5" y="69" width="26" height="26" fill="#0f172a" rx="4"/>
      <rect x="9" y="73" width="18" height="18" fill="#ffffff" rx="2"/>
      <rect x="13" y="77" width="10" height="10" fill="#0f172a" rx="1"/>

      <!-- Matrix Patterns -->
      <rect x="36" y="8" width="6" height="6" fill="#0f172a"/>
      <rect x="48" y="12" width="12" height="6" fill="#0f172a"/>
      <rect x="36" y="24" width="8" height="6" fill="#0f172a"/>
      <rect x="52" y="24" width="6" height="6" fill="#0f172a"/>

      <rect x="10" y="38" width="6" height="12" fill="#0f172a"/>
      <rect x="22" y="44" width="8" height="6" fill="#0f172a"/>
      <rect x="36" y="36" width="28" height="28" fill="#e52b50" rx="4"/>
      <rect x="42" y="42" width="16" height="16" fill="#ffffff" rx="2"/>
      <rect x="46" y="46" width="8" height="8" fill="#0077ed" rx="1"/>

      <rect x="72" y="38" width="8" height="6" fill="#0f172a"/>
      <rect x="86" y="44" width="6" height="12" fill="#0f172a"/>
      <rect x="68" y="52" width="10" height="8" fill="#0f172a"/>

      <rect x="38" y="70" width="10" height="6" fill="#0f172a"/>
      <rect x="54" y="68" width="6" height="12" fill="#0f172a"/>
      <rect x="44" y="82" width="16" height="6" fill="#0f172a"/>
      <rect x="68" y="76" width="24" height="6" fill="#0f172a"/>
      <rect x="74" y="88" width="18" height="6" fill="#0f172a"/>
    </svg>
  `;
}

function setupTicketActions(booking) {
  const printBtn = document.getElementById("printTicketBtn");
  const downloadBtn = document.getElementById("downloadTicketBtn");

  if (printBtn) {
    printBtn.addEventListener("click", () => {
      window.print();
    });
  }

  if (downloadBtn) {
    downloadBtn.addEventListener("click", () => {
      showToast("Opening Print to PDF dialog...", "info");
      setTimeout(() => {
        window.print();
      }, 500);
    });
  }
}
