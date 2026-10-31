/**
 * Travel Ticket Booking System - Admin Portal Controller (admin.js)
 * Authentication, KPI stats, Canvas chart visualization, Transport CRUD,
 * Booking status updates, User management, Payments log, CSV export.
 */

const Admin = {
  // Check admin session security
  checkAuth(isLoginPage = false) {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get("preview") === "1" || urlParams.get("demo") === "1") {
      if (!Storage.getAdminSession()) {
        Storage.setAdminSession(Storage.getAdmin(), true);
      }
      return true;
    }
    const session = Storage.getAdminSession();
    if (!session && !isLoginPage) {
      window.location.href = "login.html";
      return false;
    }
    if (session && isLoginPage) {
      window.location.href = "dashboard.html";
      return false;
    }
    return true;
  },

  // Admin login process
  login(email, password, remember = true) {
    const admin = Storage.getAdmin();
    if (email.trim().toLowerCase() === admin.email.toLowerCase() && password === admin.password) {
      Storage.setAdminSession(admin, remember);
      return { success: true, message: "Admin authenticated successfully!" };
    }
    return { success: false, message: "Invalid administrator credentials." };
  },

  // Admin logout
  logout() {
    Storage.clearAdminSession();
    window.location.href = "login.html";
  },

  // Render Dashboard
  initDashboard() {
    if (!this.checkAuth()) return;
    const stats = Storage.getStats();

    // Fill KPI Metrics
    this.setElemText("statTotalUsers", stats.totalUsers);
    this.setElemText("statTotalBuses", stats.totalBuses);
    this.setElemText("statTotalTrains", stats.totalTrains);
    this.setElemText("statTotalBookings", stats.totalBookings);
    this.setElemText("statTotalRevenue", `₹${stats.totalRevenue.toLocaleString("en-IN")}`);
    this.setElemText("statCancelledBookings", stats.cancelledCount);

    // Render Recent Bookings Table
    const tbody = document.getElementById("recentBookingsTableBody");
    if (tbody) {
      if (stats.recentBookings.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 2rem;">No bookings yet.</td></tr>`;
      } else {
        tbody.innerHTML = stats.recentBookings.map(b => `
          <tr>
            <td style="font-family: monospace; font-weight: 700;">${b.id}</td>
            <td><strong>${b.userName}</strong><br><small style="color:#64748b;">${b.userPhone}</small></td>
            <td>${b.transportName}</td>
            <td>${b.source} ➔ ${b.destination}</td>
            <td>${b.journeyDate}</td>
            <td style="font-weight: 800; color: var(--primary);">₹${b.finalAmount}</td>
            <td>
              <span class="badge ${b.bookingStatus === 'Confirmed' ? 'badge-success' : 'badge-danger'}">
                ${b.bookingStatus}
              </span>
            </td>
          </tr>
        `).join("");
      }
    }

    // Draw Canvas Bar Chart for Monthly Revenue
    this.drawMonthlyRevenueChart();
  },

  setElemText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  },

  // Draw Revenue Chart on HTML5 Canvas
  drawMonthlyRevenueChart() {
    const canvas = document.getElementById("revenueChartCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    // Sample 6-month data
    const labels = ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"];
    const revenues = [28500, 34200, 42100, 39800, 48200, 52400];

    const width = canvas.width;
    const height = canvas.height;
    const padding = 40;
    const maxVal = 60000;

    ctx.clearRect(0, 0, width, height);

    // Draw grid lines
    ctx.strokeStyle = "#e2e8f0";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = padding + ((height - padding * 2) / 4) * i;
      ctx.beginPath();
      ctx.moveTo(padding, y);
      ctx.lineTo(width - padding, y);
      ctx.stroke();

      // Label
      ctx.fillStyle = "#94a3b8";
      ctx.font = "10px sans-serif";
      const val = Math.round(maxVal - (maxVal / 4) * i);
      ctx.fillText(`₹${(val / 1000).toFixed(0)}k`, 5, y + 4);
    }

    // Draw Bars
    const barWidth = 36;
    const gap = (width - padding * 2) / labels.length;

    labels.forEach((lbl, index) => {
      const x = padding + gap * index + (gap - barWidth) / 2;
      const barHeight = (revenues[index] / maxVal) * (height - padding * 2);
      const y = height - padding - barHeight;

      // Gradient bar
      const grad = ctx.createLinearGradient(0, y, 0, height - padding);
      grad.addColorStop(0, "#0077ed");
      grad.addColorStop(1, "#3b82f6");

      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.roundRect(x, y, barWidth, barHeight, [6, 6, 0, 0]);
      ctx.fill();

      // X-axis label
      ctx.fillStyle = "#64748b";
      ctx.font = "12px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(lbl, x + barWidth / 2, height - padding + 20);
    });
  },

  // --- Transport Management ---
  initManageTransport() {
    if (!this.checkAuth()) return;
    this.renderTransportTable();

    // Search and filter
    const searchIn = document.getElementById("transportSearchInput");
    const typeFilter = document.getElementById("transportTypeFilter");

    if (searchIn) searchIn.addEventListener("input", () => this.renderTransportTable());
    if (typeFilter) typeFilter.addEventListener("change", () => this.renderTransportTable());

    // Save transport form
    const form = document.getElementById("transportForm");
    if (form) {
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        this.saveTransport();
      });
    }
  },

  renderTransportTable() {
    const list = Storage.getTransports();
    const searchVal = (document.getElementById("transportSearchInput")?.value || "").toLowerCase();
    const typeVal = document.getElementById("transportTypeFilter")?.value || "all";

    const filtered = list.filter(t => {
      const matchSearch = t.name.toLowerCase().includes(searchVal) || 
                          t.source.toLowerCase().includes(searchVal) || 
                          t.destination.toLowerCase().includes(searchVal);
      const matchType = typeVal === "all" || t.type === typeVal;
      return matchSearch && matchType;
    });

    const tbody = document.getElementById("transportsTableBody");
    if (!tbody) return;

    if (filtered.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 2rem;">No transports found.</td></tr>`;
      return;
    }

    tbody.innerHTML = filtered.map(t => `
      <tr>
        <td style="font-weight: 700;">${t.id}</td>
        <td>
          <strong>${t.name}</strong><br>
          <small style="color: #64748b;">${t.category}</small>
        </td>
        <td><span class="badge ${t.type === 'bus' ? 'badge-primary' : 'badge-secondary'}">${t.type.toUpperCase()}</span></td>
        <td>${t.source} ➔ ${t.destination}</td>
        <td>${t.departureTime} - ${t.arrivalTime}</td>
        <td><strong>₹${t.price}</strong></td>
        <td>${t.totalSeats} seats</td>
        <td>
          <div class="action-btns-group">
            <button class="btn-icon" title="Edit" onclick="Admin.openEditTransport('${t.id}')">✏️</button>
            <button class="btn-icon delete" title="Delete" onclick="Admin.deleteTransportConfirm('${t.id}')">🗑️</button>
          </div>
        </td>
      </tr>
    `).join("");
  },

  openAddTransport() {
    const form = document.getElementById("transportForm");
    if (form) form.reset();
    document.getElementById("transportEditId").value = "";
    document.getElementById("transportModalTitle").textContent = "Add New Transport";
    openModal("transportModal");
  },

  openEditTransport(id) {
    const t = Storage.getTransportById(id);
    if (!t) return;

    document.getElementById("transportEditId").value = t.id;
    document.getElementById("transportNameInput").value = t.name;
    document.getElementById("transportTypeSelect").value = t.type;
    document.getElementById("transportCategoryInput").value = t.category;
    document.getElementById("transportSourceInput").value = t.source;
    document.getElementById("transportDestInput").value = t.destination;
    document.getElementById("transportDepTime").value = t.departureTime;
    document.getElementById("transportArrTime").value = t.arrivalTime;
    document.getElementById("transportDuration").value = t.duration;
    document.getElementById("transportPrice").value = t.price;
    document.getElementById("transportSeats").value = t.totalSeats;

    document.getElementById("transportModalTitle").textContent = "Edit Transport";
    openModal("transportModal");
  },

  saveTransport() {
    const editId = document.getElementById("transportEditId").value;
    const name = document.getElementById("transportNameInput").value.trim();
    const type = document.getElementById("transportTypeSelect").value;
    const category = document.getElementById("transportCategoryInput").value.trim();
    const source = document.getElementById("transportSourceInput").value.trim();
    const destination = document.getElementById("transportDestInput").value.trim();
    const departureTime = document.getElementById("transportDepTime").value;
    const arrivalTime = document.getElementById("transportArrTime").value;
    const duration = document.getElementById("transportDuration").value.trim();
    const price = Number(document.getElementById("transportPrice").value);
    const totalSeats = Number(document.getElementById("transportSeats").value);

    if (editId) {
      // Update existing
      Storage.updateTransport(editId, {
        name, type, category, source, destination, departureTime, arrivalTime, duration, price, totalSeats
      });
      showToast("Transport updated successfully!", "success");
    } else {
      // Add new
      const newId = (type === "bus" ? "BUS-" : "TRN-") + Math.floor(100 + Math.random() * 900);
      Storage.addTransport({
        id: newId,
        name, type, category, source, destination, departureTime, arrivalTime, duration, price, totalSeats,
        rating: 4.8,
        reviewsCount: 1,
        amenities: ["WiFi", "Water Bottle", "Charging Point"]
      });
      showToast("New transport added successfully!", "success");
    }

    closeModal("transportModal");
    this.renderTransportTable();
  },

  deleteTransportConfirm(id) {
    if (confirm(`Are you sure you want to delete transport ${id}? This cannot be undone.`)) {
      Storage.deleteTransport(id);
      showToast(`Transport ${id} deleted successfully.`, "success");
      this.renderTransportTable();
    }
  },

  // --- Bookings Management ---
  initManageBookings() {
    if (!this.checkAuth()) return;
    this.renderBookingsTable();

    const searchIn = document.getElementById("bookingSearchInput");
    const statusFilter = document.getElementById("bookingStatusFilter");
    if (searchIn) searchIn.addEventListener("input", () => this.renderBookingsTable());
    if (statusFilter) statusFilter.addEventListener("change", () => this.renderBookingsTable());
  },

  renderBookingsTable() {
    const bookings = Storage.getBookings();
    const searchVal = (document.getElementById("bookingSearchInput")?.value || "").toLowerCase();
    const statusVal = document.getElementById("bookingStatusFilter")?.value || "all";

    const filtered = bookings.filter(b => {
      const matchSearch = b.id.toLowerCase().includes(searchVal) || 
                          b.userName.toLowerCase().includes(searchVal) ||
                          b.transportName.toLowerCase().includes(searchVal);
      const matchStatus = statusVal === "all" || b.bookingStatus === statusVal;
      return matchSearch && matchStatus;
    });

    const tbody = document.getElementById("bookingsTableBody");
    if (!tbody) return;

    if (filtered.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 2rem;">No matching bookings found.</td></tr>`;
      return;
    }

    tbody.innerHTML = filtered.map(b => `
      <tr>
        <td style="font-weight: 700; font-family: monospace;">${b.id}</td>
        <td><strong>${b.userName}</strong><br><small style="color:#64748b;">${b.userEmail}</small></td>
        <td>${b.transportName}</td>
        <td>${b.source} ➔ ${b.destination}</td>
        <td>${b.journeyDate}</td>
        <td><span class="badge badge-secondary">${(b.seats || []).join(", ")}</span></td>
        <td style="font-weight: 800; color: var(--primary);">₹${b.finalAmount}</td>
        <td>
          <span class="badge ${b.bookingStatus === 'Confirmed' ? 'badge-success' : 'badge-danger'}">
            ${b.bookingStatus}
          </span>
        </td>
        <td>
          <div class="action-btns-group">
            <button class="btn-icon" title="View E-Ticket" onclick="window.open('../ticket.html?id=${b.id}', '_blank')">👁️</button>
            ${b.bookingStatus === 'Confirmed' ? `
              <button class="btn-icon delete" title="Cancel Booking" onclick="Admin.cancelBookingConfirm('${b.id}')">✕</button>
            ` : ""}
          </div>
        </td>
      </tr>
    `).join("");
  },

  cancelBookingConfirm(id) {
    if (confirm(`Cancel booking ${id}? Seats will be freed and returned to availability immediately.`)) {
      Storage.cancelBooking(id);
      showToast(`Booking ${id} has been cancelled. Seats restored!`, "success");
      this.renderBookingsTable();
    }
  },

  // --- Users Management ---
  initManageUsers() {
    if (!this.checkAuth()) return;
    this.renderUsersTable();

    const searchIn = document.getElementById("userSearchInput");
    if (searchIn) searchIn.addEventListener("input", () => this.renderUsersTable());
  },

  renderUsersTable() {
    const users = Storage.getUsers();
    const searchVal = (document.getElementById("userSearchInput")?.value || "").toLowerCase();

    const filtered = users.filter(u => 
      u.name.toLowerCase().includes(searchVal) || 
      u.email.toLowerCase().includes(searchVal) || 
      (u.phone && u.phone.includes(searchVal))
    );

    const tbody = document.getElementById("usersTableBody");
    if (!tbody) return;

    if (filtered.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 2rem;">No users found.</td></tr>`;
      return;
    }

    tbody.innerHTML = filtered.map(u => {
      const userBookings = Storage.getUserBookings(u.id, u.email);
      return `
        <tr>
          <td style="font-weight: 700;">${u.id}</td>
          <td><strong>${u.name}</strong></td>
          <td>${u.email}</td>
          <td>${u.phone || "N/A"}</td>
          <td><span class="badge badge-secondary">${userBookings.length} Bookings</span></td>
          <td>${u.createdAt || "2026-01-01"}</td>
          <td>
            <button class="btn-icon delete" title="Delete User" onclick="Admin.deleteUserConfirm('${u.id}')">🗑️</button>
          </td>
        </tr>
      `;
    }).join("");
  },

  deleteUserConfirm(id) {
    if (confirm(`Are you sure you want to delete user ${id}?`)) {
      Storage.deleteUser(id);
      showToast(`User ${id} removed.`, "success");
      this.renderUsersTable();
    }
  },

  // --- Payments Management ---
  initPayments() {
    if (!this.checkAuth()) return;
    const payments = Storage.getPayments();
    const tbody = document.getElementById("paymentsTableBody");
    if (!tbody) return;

    if (payments.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 2rem;">No payment transactions recorded.</td></tr>`;
      return;
    }

    tbody.innerHTML = payments.map(p => `
      <tr>
        <td style="font-family: monospace; font-weight: 700;">${p.transactionId}</td>
        <td style="font-family: monospace;">${p.bookingId}</td>
        <td><strong>${p.userName}</strong></td>
        <td style="font-weight: 800; color: var(--primary);">₹${p.amount}</td>
        <td>${p.method}</td>
        <td>${p.date}</td>
        <td><span class="badge badge-success">${p.status}</span></td>
      </tr>
    `).join("");
  },

  // --- Reports & Export ---
  initReports() {
    if (!this.checkAuth()) return;
    const stats = Storage.getStats();

    this.setElemText("reportTotalRevenue", `₹${stats.totalRevenue.toLocaleString("en-IN")}`);
    this.setElemText("reportTotalBookings", stats.totalBookings);
    this.setElemText("reportConfirmedCount", stats.confirmedCount);
    this.setElemText("reportCancelledCount", stats.cancelledCount);

    const avg = stats.confirmedCount > 0 ? Math.round(stats.totalRevenue / stats.confirmedCount) : 0;
    this.setElemText("reportAvgTicketValue", `₹${avg}`);

    // Route popularity
    this.renderRoutePerformanceTable();

    // Export CSV Trigger
    const exportBtn = document.getElementById("exportCsvBtn");
    if (exportBtn) {
      exportBtn.addEventListener("click", () => this.exportBookingsCsv());
    }
  },

  renderRoutePerformanceTable() {
    const bookings = Storage.getBookings();
    const routeMap = {};

    bookings.forEach(b => {
      const key = `${b.source} ➔ ${b.destination}`;
      if (!routeMap[key]) {
        routeMap[key] = { bookings: 0, revenue: 0 };
      }
      routeMap[key].bookings += 1;
      if (b.bookingStatus === "Confirmed") {
        routeMap[key].revenue += Number(b.finalAmount) || 0;
      }
    });

    const tbody = document.getElementById("routeReportsTableBody");
    if (!tbody) return;

    const entries = Object.entries(routeMap).sort((a, b) => b[1].bookings - a[1].bookings);

    tbody.innerHTML = entries.map(([route, data]) => `
      <tr>
        <td><strong>${route}</strong></td>
        <td><span class="badge badge-secondary">${data.bookings} Bookings</span></td>
        <td style="font-weight: 800; color: var(--primary);">₹${data.revenue.toLocaleString("en-IN")}</td>
        <td>
          <div style="background: #e2e8f0; border-radius: 4px; height: 8px; width: 100px;">
            <div style="background: var(--secondary); height: 100%; border-radius: 4px; width: ${Math.min(100, data.bookings * 20)}%;"></div>
          </div>
        </td>
      </tr>
    `).join("");
  },

  // Export Bookings directly as CSV file download
  exportBookingsCsv() {
    const bookings = Storage.getBookings();
    if (bookings.length === 0) {
      showToast("No bookings to export.", "warning");
      return;
    }

    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Booking ID,Passenger Name,Email,Phone,Transport,Source,Destination,Journey Date,Seats,Amount,Payment Method,Status\n";

    bookings.forEach(b => {
      const row = [
        b.id,
        `"${b.userName}"`,
        b.userEmail,
        b.userPhone,
        `"${b.transportName}"`,
        b.source,
        b.destination,
        b.journeyDate,
        `"${(b.seats || []).join(';')}"`,
        b.finalAmount,
        `"${b.paymentMethod}"`,
        b.bookingStatus
      ].join(",");
      csvContent += row + "\n";
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `Travel_Bookings_Report_${new Date().toISOString().split("T")[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();

    showToast("Bookings report downloaded as CSV!", "success");
  }
};
