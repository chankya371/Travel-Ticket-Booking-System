/**
 * Travel Ticket Booking System - Main Application Controller (main.js)
 * Global navbar user state, toast system, city swapper, modals, utilities.
 */

// Toast notification helper
function showToast(message, type = "info", duration = 3500) {
  let container = document.getElementById("toastContainer");
  if (!container) {
    container = document.createElement("div");
    container.id = "toastContainer";
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const icons = {
    success: "✓",
    error: "✕",
    warning: "⚠",
    info: "ℹ"
  };

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${icons[type] || "ℹ"}</span>
    <span class="toast-msg">${message}</span>
    <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Modal management
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("active");
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove("active");
  }
}

// Global initialization
document.addEventListener("DOMContentLoaded", () => {
  // 1. Initialize user state in navbar
  initNavbar();

  // 2. Setup mobile hamburger menu
  initMobileNav();

  // 3. Setup city swap button if on search / home page
  initCitySwap();

  // 4. Setup date input default to today/tomorrow
  initDateInputs();

  // 5. Populate city datalists if present
  initCityDataLists();

  // 6. Close modals on backdrop click
  document.querySelectorAll(".modal-backdrop").forEach(backdrop => {
    backdrop.addEventListener("click", (e) => {
      if (e.target === backdrop) {
        backdrop.classList.remove("active");
      }
    });
  });
});

// Navbar User State
function initNavbar() {
  const userActionsContainer = document.getElementById("navUserActions");
  if (!userActionsContainer) return;

  const currentUser = Auth.getUser();

  if (currentUser) {
    const initials = currentUser.name.split(" ").map(n => n[0]).join("").toUpperCase().substring(0, 2);
    userActionsContainer.innerHTML = `
      <div class="nav-user-dropdown" id="navUserDropdown">
        <button class="user-profile-btn" id="userMenuToggleBtn">
          <div class="user-avatar-circle">${initials}</div>
          <span>${currentUser.name.split(" ")[0]}</span>
          <span style="font-size: 0.7rem; color: #94a3b8;">▼</span>
        </button>
        <div class="user-menu-dropdown" id="userMenuDropdown">
          <div class="user-menu-header">
            <div class="name">${currentUser.name}</div>
            <div class="email">${currentUser.email}</div>
          </div>
          <a href="my-bookings.html" class="user-menu-item">
            <span>🎫</span> My Bookings
          </a>
          <a href="about.html" class="user-menu-item">
            <span>ℹ️</span> About Us
          </a>
          <a href="contact.html" class="user-menu-item">
            <span>💬</span> Help & Support
          </a>
          <div class="user-menu-divider"></div>
          <div class="user-menu-item" style="color: #ef4444;" onclick="Auth.logout()">
            <span>🚪</span> Logout
          </div>
        </div>
      </div>
    `;

    // Dropdown toggle
    const toggleBtn = document.getElementById("userMenuToggleBtn");
    const menuDropdown = document.getElementById("userMenuDropdown");
    if (toggleBtn && menuDropdown) {
      toggleBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        menuDropdown.classList.toggle("active");
      });
      document.addEventListener("click", () => {
        menuDropdown.classList.remove("active");
      });
    }
  } else {
    userActionsContainer.innerHTML = `
      <a href="login.html" class="btn btn-outline btn-sm">Login</a>
      <a href="register.html" class="btn btn-primary btn-sm">Register</a>
    `;
  }
}

// Mobile Nav Toggle
function initMobileNav() {
  const hamburgerBtn = document.getElementById("hamburgerBtn");
  const mobileNav = document.getElementById("mobileNav");
  if (hamburgerBtn && mobileNav) {
    hamburgerBtn.addEventListener("click", () => {
      mobileNav.classList.toggle("open");
    });
  }
}

// City Swapper
function initCitySwap() {
  const swapBtn = document.getElementById("swapCitiesBtn");
  const sourceInput = document.getElementById("sourceInput");
  const destInput = document.getElementById("destInput");

  if (swapBtn && sourceInput && destInput) {
    swapBtn.addEventListener("click", (e) => {
      e.preventDefault();
      const temp = sourceInput.value;
      sourceInput.value = destInput.value;
      destInput.value = temp;
      swapBtn.style.transform = "rotate(180deg)";
      setTimeout(() => {
        swapBtn.style.transform = "rotate(0deg)";
      }, 300);
    });
  }
}

// Date Inputs Defaulting
function initDateInputs() {
  const dateInputs = document.querySelectorAll("input[type='date']");
  const today = new Date().toISOString().split("T")[0];

  dateInputs.forEach(input => {
    input.min = today;
    if (!input.value) {
      // Default to tomorrow
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      input.value = tomorrow.toISOString().split("T")[0];
    }
  });
}

// City Datalists
function initCityDataLists() {
  const dataList = document.getElementById("indianCitiesList");
  if (dataList && typeof SEED_DATA !== "undefined" && SEED_DATA.cities) {
    dataList.innerHTML = SEED_DATA.cities
      .map(city => `<option value="${city}">`)
      .join("");
  }
}
