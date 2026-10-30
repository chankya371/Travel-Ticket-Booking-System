/**
 * Travel Ticket Booking System - Authentication Manager (auth.js)
 * User login, registration, password validation, session control.
 */

const Auth = {
  // Register a new user
  register(name, email, phone, password, confirmPassword) {
    if (!name || !email || !phone || !password) {
      return { success: false, message: "Please fill in all required fields." };
    }

    // Name validation
    if (name.trim().length < 3) {
      return { success: false, message: "Name must be at least 3 characters long." };
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.trim())) {
      return { success: false, message: "Please enter a valid email address." };
    }

    // Phone validation (10 digits)
    const phoneClean = phone.replace(/[^0-9]/g, "");
    if (phoneClean.length !== 10) {
      return { success: false, message: "Please enter a valid 10-digit mobile number." };
    }

    // Password validation
    if (password.length < 6) {
      return { success: false, message: "Password must be at least 6 characters long." };
    }

    if (password !== confirmPassword) {
      return { success: false, message: "Passwords do not match." };
    }

    // Check existing email
    const existingUser = Storage.getUserByEmail(email);
    if (existingUser) {
      return { success: false, message: "An account with this email already exists. Please log in." };
    }

    // Create user record
    const newUser = {
      id: "USR-" + Math.floor(100 + Math.random() * 900),
      name: name.trim(),
      email: email.trim().toLowerCase(),
      phone: phoneClean,
      password: password,
      createdAt: new Date().toISOString().split("T")[0]
    };

    Storage.addUser(newUser);
    Storage.setCurrentUser(newUser, true);

    return { success: true, user: newUser, message: "Registration successful! Welcome aboard." };
  },

  // User Login
  login(email, password, remember = true) {
    if (!email || !password) {
      return { success: false, message: "Please enter your email and password." };
    }

    // Check if user is trying admin login
    const admin = Storage.getAdmin();
    if (email.trim().toLowerCase() === admin.email.toLowerCase() && password === admin.password) {
      Storage.setAdminSession(admin, remember);
      return { success: true, isAdmin: true, message: "Welcome back, Administrator!" };
    }

    const user = Storage.getUserByEmail(email);
    if (!user) {
      return { success: false, message: "No account found with this email. Please register." };
    }

    if (user.password !== password) {
      return { success: false, message: "Incorrect password. Please try again." };
    }

    Storage.setCurrentUser(user, remember);
    return { success: true, user: user, message: `Welcome back, ${user.name}!` };
  },

  // Logout current user
  logout() {
    Storage.clearCurrentUser();
    window.location.href = "login.html";
  },

  // Check if user is logged in
  isAuthenticated() {
    return Storage.getCurrentUser() !== null;
  },

  // Current active user
  getUser() {
    return Storage.getCurrentUser();
  },

  // Require login - redirect if not logged in
  requireAuth(redirectUrl = "login.html") {
    if (!this.isAuthenticated()) {
      window.location.href = redirectUrl;
      return false;
    }
    return true;
  },

  // Simulated forgot password reset
  resetPassword(email) {
    if (!email) return { success: false, message: "Please enter your email address." };
    const user = Storage.getUserByEmail(email);
    if (!user) {
      return { success: false, message: "We could not find an account with that email." };
    }
    return { 
      success: true, 
      message: `Password reset instructions have been simulated & sent to ${email}. For demo, your password is: ${user.password}` 
    };
  }
};
