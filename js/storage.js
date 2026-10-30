/**
 * Travel Ticket Booking System - Storage Manager
 * Centralized LocalStorage API handling data persistence, seat status,
 * cancellations, payments, and admin statistics.
 */

const Storage = {
  KEYS: {
    USERS: "tb_users",
    CURRENT_USER: "tb_currentUser",
    ADMIN: "tb_admin",
    ADMIN_SESSION: "tb_adminSession",
    TRANSPORTS: "tb_transports",
    BOOKINGS: "tb_bookings",
    PAYMENTS: "tb_payments",
    FEEDBACK: "tb_feedback",
    REVIEWS: "tb_reviews"
  },

  // Initialize storage with seed data if not already present
  init() {
    if (typeof SEED_DATA === "undefined") {
      console.error("SEED_DATA not loaded. Ensure data.js is included before storage.js");
      return;
    }

    if (!localStorage.getItem(this.KEYS.TRANSPORTS)) {
      localStorage.setItem(this.KEYS.TRANSPORTS, JSON.stringify(SEED_DATA.transports));
    }

    if (!localStorage.getItem(this.KEYS.ADMIN)) {
      localStorage.setItem(this.KEYS.ADMIN, JSON.stringify(SEED_DATA.admin));
    }

    if (!localStorage.getItem(this.KEYS.USERS)) {
      localStorage.setItem(this.KEYS.USERS, JSON.stringify(SEED_DATA.initialUsers));
    }

    if (!localStorage.getItem(this.KEYS.BOOKINGS)) {
      localStorage.setItem(this.KEYS.BOOKINGS, JSON.stringify(SEED_DATA.initialBookings));
    }

    if (!localStorage.getItem(this.KEYS.PAYMENTS)) {
      localStorage.setItem(this.KEYS.PAYMENTS, JSON.stringify(SEED_DATA.initialPayments));
    }

    if (!localStorage.getItem(this.KEYS.REVIEWS)) {
      localStorage.setItem(this.KEYS.REVIEWS, JSON.stringify(SEED_DATA.customerReviews));
    }

    if (!localStorage.getItem(this.KEYS.FEEDBACK)) {
      localStorage.setItem(this.KEYS.FEEDBACK, JSON.stringify([]));
    }
  },

  // --- Users ---
  getUsers() {
    try {
      return JSON.parse(localStorage.getItem(this.KEYS.USERS)) || [];
    } catch {
      return [];
    }
  },

  getUserByEmail(email) {
    if (!email) return null;
    const users = this.getUsers();
    return users.find(u => u.email.toLowerCase() === email.trim().toLowerCase()) || null;
  },

  getUserById(id) {
    const users = this.getUsers();
    return users.find(u => u.id === id) || null;
  },

  addUser(user) {
    const users = this.getUsers();
    users.push(user);
    localStorage.setItem(this.KEYS.USERS, JSON.stringify(users));
    return user;
  },

  deleteUser(userId) {
    const users = this.getUsers().filter(u => u.id !== userId);
    localStorage.setItem(this.KEYS.USERS, JSON.stringify(users));
  },

  // --- User Session ---
  getCurrentUser() {
    try {
      return JSON.parse(localStorage.getItem(this.KEYS.CURRENT_USER)) || null;
    } catch {
      return null;
    }
  },

  setCurrentUser(user, remember = true) {
    if (remember) {
      localStorage.setItem(this.KEYS.CURRENT_USER, JSON.stringify(user));
    } else {
      sessionStorage.setItem(this.KEYS.CURRENT_USER, JSON.stringify(user));
    }
  },

  clearCurrentUser() {
    localStorage.removeItem(this.KEYS.CURRENT_USER);
    sessionStorage.removeItem(this.KEYS.CURRENT_USER);
  },

  // --- Admin Session ---
  getAdmin() {
    try {
      return JSON.parse(localStorage.getItem(this.KEYS.ADMIN)) || SEED_DATA.admin;
    } catch {
      return SEED_DATA.admin;
    }
  },

  getAdminSession() {
    try {
      return JSON.parse(localStorage.getItem(this.KEYS.ADMIN_SESSION)) || 
             JSON.parse(sessionStorage.getItem(this.KEYS.ADMIN_SESSION)) || null;
    } catch {
      return null;
    }
  },

  setAdminSession(adminData, remember = true) {
    if (remember) {
      localStorage.setItem(this.KEYS.ADMIN_SESSION, JSON.stringify(adminData));
    } else {
      sessionStorage.setItem(this.KEYS.ADMIN_SESSION, JSON.stringify(adminData));
    }
  },

  clearAdminSession() {
    localStorage.removeItem(this.KEYS.ADMIN_SESSION);
    sessionStorage.removeItem(this.KEYS.ADMIN_SESSION);
  },

  // --- Transports ---
  getTransports() {
    try {
      return JSON.parse(localStorage.getItem(this.KEYS.TRANSPORTS)) || [];
    } catch {
      return [];
    }
  },

  getTransportById(id) {
    const list = this.getTransports();
    return list.find(t => t.id === id) || null;
  },

  addTransport(transport) {
    const list = this.getTransports();
    list.unshift(transport);
    localStorage.setItem(this.KEYS.TRANSPORTS, JSON.stringify(list));
    return transport;
  },

  updateTransport(id, updatedData) {
    const list = this.getTransports();
    const index = list.findIndex(t => t.id === id);
    if (index !== -1) {
      list[index] = { ...list[index], ...updatedData };
      localStorage.setItem(this.KEYS.TRANSPORTS, JSON.stringify(list));
      return list[index];
    }
    return null;
  },

  deleteTransport(id) {
    const list = this.getTransports().filter(t => t.id !== id);
    localStorage.setItem(this.KEYS.TRANSPORTS, JSON.stringify(list));
  },

  // --- Bookings ---
  getBookings() {
    try {
      return JSON.parse(localStorage.getItem(this.KEYS.BOOKINGS)) || [];
    } catch {
      return [];
    }
  },

  getBookingById(id) {
    const bookings = this.getBookings();
    return bookings.find(b => b.id === id) || null;
  },

  getUserBookings(userId, userEmail) {
    const bookings = this.getBookings();
    return bookings.filter(b => 
      (userId && b.userId === userId) || 
      (userEmail && b.userEmail && b.userEmail.toLowerCase() === userEmail.toLowerCase())
    );
  },

  addBooking(booking) {
    const bookings = this.getBookings();
    bookings.unshift(booking);
    localStorage.setItem(this.KEYS.BOOKINGS, JSON.stringify(bookings));
    return booking;
  },

  updateBookingStatus(bookingId, status) {
    const bookings = this.getBookings();
    const target = bookings.find(b => b.id === bookingId);
    if (target) {
      target.bookingStatus = status;
      if (status === "Cancelled") {
        target.cancelledAt = new Date().toISOString();
      }
      localStorage.setItem(this.KEYS.BOOKINGS, JSON.stringify(bookings));
      return target;
    }
    return null;
  },

  cancelBooking(bookingId) {
    return this.updateBookingStatus(bookingId, "Cancelled");
  },

  // --- Seat Availability Tracker ---
  // Calculates currently occupied seats for a given transport & date (excluding cancelled tickets)
  getBookedSeats(transportId, journeyDate) {
    if (!transportId || !journeyDate) return [];
    const bookings = this.getBookings();
    const activeBookings = bookings.filter(b => 
      b.transportId === transportId &&
      b.journeyDate === journeyDate &&
      b.bookingStatus !== "Cancelled"
    );

    const occupiedSeats = [];
    activeBookings.forEach(b => {
      if (Array.isArray(b.seats)) {
        occupiedSeats.push(...b.seats);
      }
    });

    return occupiedSeats;
  },

  // Available seats count for a specific date
  getAvailableSeatsCount(transportId, journeyDate) {
    const transport = this.getTransportById(transportId);
    if (!transport) return 0;
    const bookedSeats = this.getBookedSeats(transportId, journeyDate);
    return Math.max(0, (transport.totalSeats || 30) - bookedSeats.length);
  },

  // --- Payments ---
  getPayments() {
    try {
      return JSON.parse(localStorage.getItem(this.KEYS.PAYMENTS)) || [];
    } catch {
      return [];
    }
  },

  addPayment(payment) {
    const payments = this.getPayments();
    payments.unshift(payment);
    localStorage.setItem(this.KEYS.PAYMENTS, JSON.stringify(payments));
    return payment;
  },

  // --- Feedback & Reviews ---
  getFeedback() {
    try {
      return JSON.parse(localStorage.getItem(this.KEYS.FEEDBACK)) || [];
    } catch {
      return [];
    }
  },

  addFeedback(item) {
    const feedback = this.getFeedback();
    feedback.unshift(item);
    localStorage.setItem(this.KEYS.FEEDBACK, JSON.stringify(feedback));
    return item;
  },

  getReviews() {
    try {
      return JSON.parse(localStorage.getItem(this.KEYS.REVIEWS)) || [];
    } catch {
      return [];
    }
  },

  addReview(item) {
    const reviews = this.getReviews();
    reviews.unshift(item);
    localStorage.setItem(this.KEYS.REVIEWS, JSON.stringify(reviews));
    return item;
  },

  // --- Admin Analytics & Statistics ---
  getStats() {
    const users = this.getUsers();
    const transports = this.getTransports();
    const bookings = this.getBookings();
    const payments = this.getPayments();

    const totalBuses = transports.filter(t => t.type === "bus").length;
    const totalTrains = transports.filter(t => t.type === "train").length;

    const confirmedBookings = bookings.filter(b => b.bookingStatus === "Confirmed");
    const cancelledBookings = bookings.filter(b => b.bookingStatus === "Cancelled");

    // Total revenue from confirmed bookings
    const totalRevenue = confirmedBookings.reduce((sum, b) => sum + (Number(b.finalAmount) || 0), 0);

    return {
      totalUsers: users.length,
      totalTransports: transports.length,
      totalBuses,
      totalTrains,
      totalBookings: bookings.length,
      confirmedCount: confirmedBookings.length,
      cancelledCount: cancelledBookings.length,
      totalRevenue,
      recentBookings: bookings.slice(0, 6),
      recentPayments: payments.slice(0, 6)
    };
  }
};

// Auto-run init on load
Storage.init();
