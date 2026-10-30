# TravelEase - Travel Ticket Booking System

A modern, responsive, and complete travel ticket booking web application inspired by **MakeMyTrip** and **RedBus**, built purely using **HTML5, CSS3, and Vanilla JavaScript** with **LocalStorage** persistence.

---

## 🌟 Key Highlights & Features

- **Pure Frontend Architecture:** No Node.js, React, Java, PHP, or external backend server required. Runs directly in any web browser by opening `index.html`.
- **Modern UI & Aesthetic:** Built with a design system featuring the Google Plus Jakarta Sans typography, vibrant RedBus/MakeMyTrip inspired palettes, glassmorphism headers, responsive mobile drawer menus, and micro-interactions.
- **Visual Seat Selection:** Interactive vehicle chassis with driver cabin, sleeper berths/chair car rows, color-coded seat states:
  - 🟢 **Green:** Available
  - 🔵 **Blue:** Selected
  - ⚪ **Grey:** Booked / Occupied
- **Realistic Indian Routes:** Delhi, Chandigarh, Shimla, Bilaspur, Manali, Mumbai, Pune, Jaipur, Agra, Dehradun.
- **Dynamic Pricing & Coupons:**
  - `TRAVEL50`: 10% Discount
  - `FIRSTBOOK`: Flat ₹150 Discount
- **Simulated Payment Gateway:** Multi-tab checkout with simulated UPI (QR Code & VPA), Credit/Debit Card, and Pay-at-Boarding with processing animations and unique Booking ID generation.
- **E-Ticket & Boarding Pass:** Perforated tear-line boarding pass design with SVG QR code, passenger manifest, route timeline, and 1-click **Print / Download PDF** support.
- **Seat Restoration on Cancellation:** Cancelling a ticket in *My Bookings* immediately frees up the seats back into the availability pool for that route and date.
- **Full Admin Portal:** Dedicated management suite with statistics KPI cards, HTML5 Canvas revenue charts, Transport Fleet CRUD, Booking Management, User Profiles, Payment Ledgers, and **Export to CSV**.

---

## 🔐 Credentials & Demo Accounts

### Administrator Portal
- **URL:** [admin/login.html](admin/login.html)
- **Email:** `admin@gmail.com`
- **Password:** `admin123`

### Demo User Accounts
- **User 1:** `rahul@gmail.com` / `password123`
- **User 2:** `pooja@gmail.com` / `password123`
- **User 3:** `amit@gmail.com` / `password123`
*(Or register any new account on [register.html](register.html))*

---

## 📂 Project Directory Structure

```
Travel Ticket Booking System/
├── index.html                  # Homepage (Search widget, popular routes, reviews)
├── login.html                  # User authentication with demo quick-fill
├── register.html               # User registration with validation
├── search.html                 # Search results with live multi-facet filters
├── seat-selection.html         # Interactive visual seat map & real-time calculation
├── booking.html                # Passenger details form & simulated payment
├── my-bookings.html            # User booking history & cancellation
├── ticket.html                 # Boarding pass with QR code & print/PDF download
├── about.html                  # About Us, mission & company milestones
├── contact.html                # Help & support form with interactive FAQ
│
├── admin/
│   ├── login.html              # Admin login
│   ├── dashboard.html          # Analytics, KPI metrics & Canvas revenue chart
│   ├── manage-transport.html   # Fleet CRUD (Buses & Trains)
│   ├── manage-bookings.html    # All bookings search, filter & cancellation
│   ├── manage-users.html       # Registered user accounts list
│   ├── payments.html           # Transaction ledger
│   └── reports.html            # Financial analytics & CSV export
│
├── css/
│   ├── style.css               # Core design system & responsive navigation
│   ├── auth.css                # Authentication screens
│   ├── booking.css             # Search, seat selection & checkout
│   ├── ticket.css              # Boarding pass & print media rules
│   └── admin.css               # Admin dashboard, tables & charts
│
└── js/
    ├── data.js                 # Realistic Indian routes & transport seed data
    ├── storage.js              # LocalStorage manager with seat tracking
    ├── auth.js                 # Session & registration management
    ├── main.js                 # Global toasts, city swapper & modals
    ├── search.js               # Search query parser & filter sidebar
    ├── seats.js                # Seat selection & live fare calculation
    ├── booking.js              # Checkout, promo codes & payment simulation
    ├── ticket.js               # E-ticket rendering & print triggers
    └── admin.js                # Admin controller, charts & CSV exporter
```

---

## 🚀 How to Run the Project

1. Simply double-click **`index.html`** or right-click and open it in Google Chrome, Microsoft Edge, Mozilla Firefox, or any modern web browser.
2. No installation (`npm install`), build step, or web server is required!

---

## 🧪 Recommended Demonstration Flow

1. **Homepage & Search:** Open `index.html`. Choose "Delhi" to "Shimla", select tomorrow's date, and click **Search Tickets**.
2. **Filters & Sorting:** On `search.html`, use the price slider and vehicle type filters (Bus / Train). Click **View Seats** on any option.
3. **Seat Selection:** On `seat-selection.html`, click on available green seats. Watch the seat chips and total fare update dynamically. Click **Continue to Booking**.
4. **Checkout & Payment:** On `booking.html`, enter passenger names, enter coupon code `TRAVEL50` to receive a discount, select your preferred simulated payment mode, and click **Pay & Confirm Booking**.
5. **E-Ticket:** View your generated boarding pass on `ticket.html`. Test the **Print Ticket** and **Download PDF** buttons.
6. **Booking History & Cancellation:** Go to `my-bookings.html`. View your reservation. Click **Cancel Ticket** to test the cancellation dialog. Notice how the booking status changes to Cancelled and the seats are instantly restored.
7. **Admin Portal:** Visit `admin/login.html` and sign in with `admin@gmail.com` / `admin123`. Check the dashboard stats and revenue chart, add or edit a bus route in `manage-transport.html`, and export reports to CSV in `reports.html`.
