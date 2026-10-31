/**
 * Travel Ticket Booking System - Booking & Payment Controller (booking.js)
 * Passenger dynamic form, coupon discounting, payment simulation, ticket creation.
 */

let checkoutData = null;
let currentTransport = null;
let discountAmount = 0;
let appliedCoupon = "";

document.addEventListener("DOMContentLoaded", () => {
  initBookingPage();
});

function initBookingPage() {
  const urlParams = new URLSearchParams(window.location.search);
  const isPreview = urlParams.get("preview") === "1" || urlParams.get("demo") === "1";
  if (isPreview) {
    if (!Auth.getUser()) {
      const demoUser = (Storage.getUsers() && Storage.getUsers()[0]) || {
        id: "USR-101",
        name: "Rahul Sharma",
        email: "rahul@gmail.com",
        phone: "9876543210"
      };
      Storage.saveCurrentUser(demoUser);
    }
    if (!Storage.getCurrentCheckout()) {
      const allTransports = Storage.getTransports() || [];
      const sampleTransport = allTransports.find(t => t.id === "BUS-101") || allTransports[0];
      if (sampleTransport) {
        Storage.saveCurrentCheckout({
          transportId: sampleTransport.id,
          transport: sampleTransport,
          date: "2026-11-10",
          seats: ["L3", "L4"],
          totalFare: (sampleTransport.fare || 950) * 2
        });
      }
    }
  }

  // Enforce authentication
  if (!Auth.isAuthenticated()) {
    showToast("Please sign in or create an account to proceed with your booking.", "warning");
    setTimeout(() => {
      window.location.href = "login.html?redirect=booking.html";
    }, 1200);
    return;
  }

  const stored = sessionStorage.getItem("tb_currentCheckout");
  if (!stored) {
    showToast("Session expired or no seats selected. Please search again.", "warning");
    setTimeout(() => { window.location.href = "search.html"; }, 1500);
    return;
  }

  checkoutData = JSON.parse(stored);
  currentTransport = Storage.getTransportById(checkoutData.transportId);

  if (!currentTransport) {
    showToast("Transport not found. Please search again.", "error");
    setTimeout(() => { window.location.href = "search.html"; }, 1500);
    return;
  }

  // Pre-fill user contact info if logged in
  prefillUserInfo();

  // Render Transport Summary Bar
  renderTransportSummary();

  // Render Dynamic Passenger Forms
  renderPassengerForms();

  // Render Initial Fare Summary
  updateFareSummary();

  // Setup Payment Tabs
  setupPaymentTabs();

  // Setup Coupon Code
  setupCoupon();

  // Setup Form Submit
  const bookingForm = document.getElementById("bookingForm");
  if (bookingForm) {
    bookingForm.addEventListener("submit", handleBookingSubmit);
  }
}

function prefillUserInfo() {
  const user = Auth.getUser();
  if (user) {
    const nameIn = document.getElementById("contactName");
    const emailIn = document.getElementById("contactEmail");
    const phoneIn = document.getElementById("contactPhone");

    if (nameIn) nameIn.value = user.name;
    if (emailIn) emailIn.value = user.email;
    if (phoneIn) phoneIn.value = user.phone || "";
  }
}

function renderTransportSummary() {
  const nameElem = document.getElementById("summaryTransportName");
  const routeElem = document.getElementById("summaryRoute");
  const dateElem = document.getElementById("summaryDate");
  const timeElem = document.getElementById("summaryTime");

  if (nameElem) nameElem.textContent = currentTransport.name;
  if (routeElem) routeElem.textContent = `${currentTransport.source} ➔ ${currentTransport.destination}`;
  if (dateElem) {
    const d = new Date(checkoutData.journeyDate + "T00:00:00");
    dateElem.textContent = d.toLocaleDateString("en-IN", { weekday: "short", day: "numeric", month: "short", year: "numeric" });
  }
  if (timeElem) timeElem.textContent = `${currentTransport.departureTime} - ${currentTransport.arrivalTime} (${currentTransport.duration})`;
}

// Generate one passenger fieldset per selected seat
function renderPassengerForms() {
  const container = document.getElementById("passengerFormsContainer");
  if (!container) return;

  const seats = checkoutData.selectedSeats || [];
  const user = Auth.getUser();

  container.innerHTML = seats.map((seat, index) => {
    const defaultName = (index === 0 && user) ? user.name : "";
    return `
      <div class="passenger-card">
        <div class="passenger-card-header">
          <span>Passenger ${index + 1}</span>
          <span class="badge badge-secondary">Seat ${seat}</span>
        </div>
        <div class="passenger-inputs-grid">
          <div class="form-group">
            <label>Full Name *</label>
            <input 
              type="text" 
              name="passenger_name_${index}" 
              class="passenger-name-input" 
              placeholder="e.g. Rahul Sharma" 
              value="${defaultName}" 
              required
            >
          </div>
          <div class="form-group">
            <label>Age *</label>
            <input 
              type="number" 
              name="passenger_age_${index}" 
              class="passenger-age-input" 
              placeholder="25" 
              min="1" 
              max="110" 
              required
            >
          </div>
          <div class="form-group">
            <label>Gender *</label>
            <select name="passenger_gender_${index}" class="passenger-gender-input" required>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

// Coupon system
function setupCoupon() {
  const applyBtn = document.getElementById("applyCouponBtn");
  const couponInput = document.getElementById("couponCodeInput");
  const couponMsg = document.getElementById("couponMessage");

  if (applyBtn && couponInput) {
    applyBtn.addEventListener("click", () => {
      const code = couponInput.value.trim().toUpperCase();
      if (!code) {
        showToast("Please enter a promo code", "warning");
        return;
      }

      if (code === "TRAVEL50") {
        // 10% discount
        discountAmount = Math.round(checkoutData.baseTotal * 0.1);
        appliedCoupon = "TRAVEL50 (10% Off)";
        if (couponMsg) {
          couponMsg.textContent = "Coupon TRAVEL50 applied! You saved 10%.";
          couponMsg.style.color = "#10b981";
        }
        showToast("Coupon TRAVEL50 applied successfully!", "success");
      } else if (code === "FIRSTBOOK") {
        // Flat ₹150 discount
        discountAmount = 150;
        appliedCoupon = "FIRSTBOOK (Flat ₹150)";
        if (couponMsg) {
          couponMsg.textContent = "Coupon FIRSTBOOK applied! ₹150 discount.";
          couponMsg.style.color = "#10b981";
        }
        showToast("Coupon FIRSTBOOK applied successfully!", "success");
      } else {
        discountAmount = 0;
        appliedCoupon = "";
        if (couponMsg) {
          couponMsg.textContent = "Invalid or expired promo code.";
          couponMsg.style.color = "#ef4444";
        }
        showToast("Invalid promo code. Try 'TRAVEL50' or 'FIRSTBOOK'", "error");
      }

      updateFareSummary();
    });
  }
}

function updateFareSummary() {
  const baseTotal = checkoutData.baseTotal;
  const tax = checkoutData.tax;
  const finalAmount = Math.max(0, baseTotal + tax - discountAmount);

  const baseElem = document.getElementById("checkoutBaseFare");
  const taxElem = document.getElementById("checkoutTax");
  const discountElem = document.getElementById("checkoutDiscount");
  const totalElem = document.getElementById("checkoutTotalAmount");
  const payBtnAmount = document.getElementById("payBtnAmount");

  if (baseElem) baseElem.textContent = `₹${baseTotal}`;
  if (taxElem) taxElem.textContent = `₹${tax}`;
  if (discountElem) discountElem.textContent = `-₹${discountAmount}`;
  if (totalElem) totalElem.textContent = `₹${finalAmount}`;
  if (payBtnAmount) payBtnAmount.textContent = `₹${finalAmount}`;
}

// Payment method tab switching
function setupPaymentTabs() {
  const tabItems = document.querySelectorAll(".payment-tab-item");
  const tabPanels = document.querySelectorAll(".payment-tab-panel");

  tabItems.forEach(item => {
    item.addEventListener("click", () => {
      tabItems.forEach(t => t.classList.remove("active"));
      tabPanels.forEach(p => p.classList.remove("active"));

      item.classList.add("active");
      const targetPanel = document.getElementById(item.dataset.target);
      if (targetPanel) targetPanel.classList.add("active");
    });
  });
}

// Process Simulated Booking
function handleBookingSubmit(e) {
  e.preventDefault();

  // Validate Contact info
  const contactName = document.getElementById("contactName")?.value.trim();
  const contactEmail = document.getElementById("contactEmail")?.value.trim();
  const contactPhone = document.getElementById("contactPhone")?.value.trim();

  if (!contactName || !contactEmail || !contactPhone) {
    showToast("Please provide primary contact name, email, and mobile number.", "error");
    return;
  }

  // Collect passengers
  const names = document.querySelectorAll(".passenger-name-input");
  const ages = document.querySelectorAll(".passenger-age-input");
  const genders = document.querySelectorAll(".passenger-gender-input");

  const passengers = [];
  for (let i = 0; i < names.length; i++) {
    const pName = names[i].value.trim();
    const pAge = parseInt(ages[i].value);
    const pGender = genders[i].value;
    const seat = checkoutData.selectedSeats[i];

    if (!pName || isNaN(pAge) || pAge <= 0) {
      showToast(`Please enter a valid name and age for Passenger ${i + 1}.`, "error");
      return;
    }

    passengers.push({
      seat: seat,
      name: pName,
      age: pAge,
      gender: pGender
    });
  }

  // Active payment method
  const activeTab = document.querySelector(".payment-tab-item.active");
  const paymentMethod = activeTab ? activeTab.dataset.method : "UPI (Demo)";

  // Open simulated payment processing modal
  openPaymentSimulationModal(() => {
    // Finalize booking
    const finalAmount = Math.max(0, checkoutData.baseTotal + checkoutData.tax - discountAmount);
    const bookingId = "TRV-" + Math.floor(100000 + Math.random() * 900000);
    const transactionId = "TXN-" + Math.floor(1000000 + Math.random() * 9000000);

    const currentUser = Auth.getUser();

    const newBooking = {
      id: bookingId,
      userId: currentUser ? currentUser.id : "GUEST",
      userName: contactName,
      userEmail: contactEmail,
      userPhone: contactPhone,
      transportId: currentTransport.id,
      transportName: currentTransport.name,
      transportType: currentTransport.type,
      category: currentTransport.category,
      source: currentTransport.source,
      destination: currentTransport.destination,
      journeyDate: checkoutData.journeyDate,
      departureTime: currentTransport.departureTime,
      arrivalTime: currentTransport.arrivalTime,
      duration: currentTransport.duration,
      seats: [...checkoutData.selectedSeats],
      passengers: passengers,
      farePerSeat: currentTransport.price,
      totalFare: checkoutData.baseTotal,
      tax: checkoutData.tax,
      discount: discountAmount,
      finalAmount: finalAmount,
      paymentMethod: paymentMethod,
      paymentStatus: "Paid",
      bookingStatus: "Confirmed",
      bookedAt: new Date().toISOString()
    };

    // Save booking to storage
    Storage.addBooking(newBooking);

    // Save payment log
    Storage.addPayment({
      transactionId: transactionId,
      bookingId: bookingId,
      userId: newBooking.userId,
      userName: contactName,
      amount: finalAmount,
      method: paymentMethod,
      status: "Successful",
      date: new Date().toLocaleString("en-IN")
    });

    // Clear checkout session
    sessionStorage.removeItem("tb_currentCheckout");

    // Redirect to E-ticket
    window.location.href = `ticket.html?id=${bookingId}`;
  });
}

function openPaymentSimulationModal(onSuccess) {
  const modal = document.getElementById("paymentModal");
  const spinnerContainer = document.getElementById("paymentModalContent");
  if (!modal || !spinnerContainer) {
    onSuccess();
    return;
  }

  modal.classList.add("active");
  spinnerContainer.innerHTML = `
    <div class="payment-processing-modal">
      <div class="payment-spinner"></div>
      <h3 style="font-size: 1.3rem; font-weight: 800; color: var(--dark); margin-bottom: 8px;">
        Processing Payment...
      </h3>
      <p style="color: var(--text-muted); font-size: 0.95rem;">
        Contacting bank gateway securely. Please do not refresh or close this page.
      </p>
    </div>
  `;

  setTimeout(() => {
    spinnerContainer.innerHTML = `
      <div class="payment-processing-modal">
        <div style="width: 64px; height: 64px; border-radius: 50%; background: #ecfdf5; color: #10b981; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; margin: 0 auto 1.25rem;">
          ✓
        </div>
        <h3 style="font-size: 1.3rem; font-weight: 800; color: #065f46; margin-bottom: 8px;">
          Payment Successful!
        </h3>
        <p style="color: var(--text-muted); font-size: 0.95rem;">
          Generating your official boarding pass...
        </p>
      </div>
    `;

    setTimeout(() => {
      modal.classList.remove("active");
      onSuccess();
    }, 1200);
  }, 1800);
}
