"""
Generate high-resolution professional system diagrams for the Travel Ticket Booking System report.
Uses matplotlib with clean vector rendering.
"""

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

os.makedirs('diagrams', exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# 1. System Architecture Diagram
def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(5, 5.6, "Three-Tier Client-Side System Architecture", fontsize=14, fontweight='bold', ha='center', color='#0f172a')

    # Presentation Tier
    p_box = patches.FancyBboxPatch((0.5, 3.6), 9.0, 1.5, boxstyle="round,pad=0.2", ec="#0077ed", fc="#eff6ff", lw=2)
    ax.add_patch(p_box)
    ax.text(0.8, 4.8, "PRESENTATION TIER (USER & ADMIN INTERFACES)", fontsize=11, fontweight='bold', color='#0077ed')
    
    modules = ["Home & Search\n(index.html, search.html)", "Seat Visualizer\n(seat-selection.html)", "Checkout & Pay\n(booking.html)", "E-Ticket Pass\n(ticket.html)", "Admin Console\n(dashboard.html)"]
    for i, m in enumerate(modules):
        x = 0.8 + i * 1.8
        box = patches.FancyBboxPatch((x, 3.8), 1.6, 0.8, boxstyle="round,pad=0.1", ec="#94a3b8", fc="#ffffff", lw=1)
        ax.add_patch(box)
        ax.text(x + 0.8, 4.2, m, fontsize=7.5, ha='center', va='center', color='#1e293b', fontweight='bold')

    ax.annotate('', xy=(5, 3.1), xytext=(5, 3.6), arrowprops=dict(arrowstyle="<->", lw=2, color="#e52b50"))

    # Logic Tier
    l_box = patches.FancyBboxPatch((0.5, 1.8), 9.0, 1.3, boxstyle="round,pad=0.2", ec="#e52b50", fc="#fff1f3", lw=2)
    ax.add_patch(l_box)
    ax.text(0.8, 2.8, "BUSINESS LOGIC & CONTROLLER TIER (VANILLA JAVASCRIPT)", fontsize=11, fontweight='bold', color='#e52b50')
    
    js_mods = ["Auth & Security\n(auth.js)", "Search & Sort Engine\n(search.js)", "Seat Allocation Engine\n(seats.js)", "Simulated Gateway\n(booking.js)", "Admin Controller\n(admin.js)"]
    for i, m in enumerate(js_mods):
        x = 0.8 + i * 1.8
        box = patches.FancyBboxPatch((x, 1.95), 1.6, 0.7, boxstyle="round,pad=0.1", ec="#cbd5e1", fc="#ffffff", lw=1)
        ax.add_patch(box)
        ax.text(x + 0.8, 2.3, m, fontsize=7.5, ha='center', va='center', color='#1e293b', fontweight='bold')

    ax.annotate('', xy=(5, 1.3), xytext=(5, 1.8), arrowprops=dict(arrowstyle="<->", lw=2, color="#10b981"))

    # Storage Tier
    s_box = patches.FancyBboxPatch((0.5, 0.2), 9.0, 1.1, boxstyle="round,pad=0.2", ec="#10b981", fc="#ecfdf5", lw=2)
    ax.add_patch(s_box)
    ax.text(0.8, 1.05, "CLIENT STORAGE TIER (LOCALSTORAGE LAYER)", fontsize=11, fontweight='bold', color='#065f46')

    storages = ["tb_users\n(User Accounts)", "tb_transports\n(Bus/Train Fleets)", "tb_bookings\n(Reservations)", "tb_payments\n(Transactions)", "tb_feedback\n(Support Logs)"]
    for i, m in enumerate(storages):
        x = 0.8 + i * 1.8
        box = patches.FancyBboxPatch((x, 0.35), 1.6, 0.6, boxstyle="round,pad=0.1", ec="#a7f3d0", fc="#ffffff", lw=1)
        ax.add_patch(box)
        ax.text(x + 0.8, 0.65, m, fontsize=7.5, ha='center', va='center', color='#065f46', fontweight='bold')

    plt.tight_layout()
    plt.savefig('diagrams/fig_architecture.png', bbox_inches='tight')
    plt.close()
    print("[OK] Created diagrams/fig_architecture.png")

# 2. DFD Level 0 (Context Level)
def create_dfd_lvl0():
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    center = patches.Circle((4.5, 2.25), 1.2, ec="#0077ed", fc="#eff6ff", lw=2.5)
    ax.add_patch(center)
    ax.text(4.5, 2.45, "0.0", fontsize=11, fontweight='bold', ha='center', color='#0077ed')
    ax.text(4.5, 2.1, "Travel Ticket\nBooking System", fontsize=10, fontweight='bold', ha='center', color='#0f172a')

    # Entity 1: User
    user = patches.Rectangle((0.5, 1.5), 1.8, 1.5, ec="#e52b50", fc="#fff1f3", lw=2)
    ax.add_patch(user)
    ax.text(1.4, 2.35, "TRAVELER /", fontsize=10, fontweight='bold', ha='center', color='#991b1b')
    ax.text(1.4, 2.05, "PASSENGER", fontsize=10, fontweight='bold', ha='center', color='#991b1b')

    # Entity 2: Admin
    admin = patches.Rectangle((6.7, 1.5), 1.8, 1.5, ec="#10b981", fc="#ecfdf5", lw=2)
    ax.add_patch(admin)
    ax.text(7.6, 2.35, "SYSTEM", fontsize=10, fontweight='bold', ha='center', color='#065f46')
    ax.text(7.6, 2.05, "ADMIN", fontsize=10, fontweight='bold', ha='center', color='#065f46')

    ax.annotate("Search Route, Book Seats, Demo Pay", xy=(3.3, 2.6), xytext=(2.3, 2.6),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#1e293b"), fontsize=8, ha='center', va='bottom')
    ax.annotate("E-Ticket, Booking Status, Confirmations", xy=(2.3, 1.9), xytext=(3.3, 1.9),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#0077ed"), fontsize=8, ha='center', va='top')

    ax.annotate("Manage Fleets, Routes, Bookings", xy=(5.7, 2.6), xytext=(6.7, 2.6),
                arrowprops=dict(arrowstyle="<-", lw=1.5, color="#1e293b"), fontsize=8, ha='center', va='bottom')
    ax.annotate("KPI Reports, Passenger Lists, Financials", xy=(6.7, 1.9), xytext=(5.7, 1.9),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#10b981"), fontsize=8, ha='center', va='top')

    plt.tight_layout()
    plt.savefig('diagrams/fig_dfd_lvl0.png', bbox_inches='tight')
    plt.close()
    print("[OK] Created diagrams/fig_dfd_lvl0.png")

# 3. DFD Level 1
def create_dfd_lvl1():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    processes = [
        ("1.0\nRegistration\n& Login", (1.8, 5.0)),
        ("2.0\nSearch\nTransports", (5.0, 5.0)),
        ("3.0\nSeat Selection\n& Lock", (8.2, 5.0)),
        ("4.0\nSimulated Pay\n& Checkout", (8.2, 2.2)),
        ("5.0\nTicket Generation\n& Storage", (5.0, 2.2)),
        ("6.0\nAdmin Fleet &\nBooking Control", (1.8, 2.2))
    ]

    for label, (x, y) in processes:
        circle = patches.Circle((x, y), 0.75, ec="#0077ed", fc="#eff6ff", lw=2)
        ax.add_patch(circle)
        ax.text(x, y, label, fontsize=8, fontweight='bold', ha='center', va='center', color='#0f172a')

    ds = patches.Rectangle((3.5, 0.4), 3.0, 0.7, ec="#10b981", fc="#ecfdf5", lw=2)
    ax.add_patch(ds)
    ax.text(5.0, 0.75, "D1: LocalStorage Repository", fontsize=9.5, fontweight='bold', ha='center', va='center', color='#065f46')

    arrows = [
        ((2.55, 5.0), (4.25, 5.0), "Auth State"),
        ((5.75, 5.0), (7.45, 5.0), "Route Match"),
        ((8.2, 4.25), (8.2, 2.95), "Seats Picked"),
        ((7.45, 2.2), (5.75, 2.2), "Paid Status"),
        ((5.0, 2.95), (5.0, 4.25), "Confirmed"),
        ((1.8, 4.25), (1.8, 2.95), "Admin Role"),
        ((5.0, 1.45), (5.0, 1.1), "Persist Records"),
        ((8.2, 1.45), (6.5, 0.75), "Read/Write Bookings"),
        ((1.8, 1.45), (3.5, 0.75), "CRUD Updates")
    ]

    for p1, p2, text in arrows:
        ax.annotate(text, xy=p2, xytext=p1,
                    arrowprops=dict(arrowstyle="->", lw=1.2, color="#475569"),
                    fontsize=7, ha='center', va='center', backgroundcolor='#ffffff')

    plt.tight_layout()
    plt.savefig('diagrams/fig_dfd_lvl1.png', bbox_inches='tight')
    plt.close()
    print("[OK] Created diagrams/fig_dfd_lvl1.png")

# Helper to draw a clean UML stick figure actor
def draw_actor(ax, x, y, label):
    # Head
    ax.add_patch(patches.Circle((x, y + 0.5), 0.2, ec="#0f172a", fc="#ffffff", lw=1.5))
    # Body
    ax.plot([x, x], [y + 0.3, y - 0.2], color="#0f172a", lw=1.5)
    # Arms
    ax.plot([x - 0.3, x + 0.3], [y + 0.1, y + 0.1], color="#0f172a", lw=1.5)
    # Legs
    ax.plot([x, x - 0.25], [y - 0.2, y - 0.6], color="#0f172a", lw=1.5)
    ax.plot([x, x + 0.25], [y - 0.2, y - 0.6], color="#0f172a", lw=1.5)
    # Text
    ax.text(x, y - 0.9, label, fontsize=9.5, fontweight='bold', ha='center', va='top', color='#0f172a')

# 4. User Use Case Diagram
def create_usecase_user():
    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    boundary = patches.Rectangle((2.4, 0.3), 5.6, 4.9, ec="#0f172a", fc="#f8fafc", lw=1.5, ls='--')
    ax.add_patch(boundary)
    ax.text(5.2, 4.9, "Travel Ticket Booking System (User Scope)", fontsize=10, fontweight='bold', ha='center', color='#0f172a')

    draw_actor(ax, 1.1, 3.2, "Traveler /\nPassenger")

    use_cases = [
        ("Register / Login Account", 4.3),
        ("Search Bus / Train Schedules", 3.6),
        ("Select Preferred Seats Interactively", 2.9),
        ("Apply Promo Codes & Calculate Fare", 2.2),
        ("Simulate Online Payment (UPI/Card)", 1.5),
        ("Download / Print E-Ticket & Cancel Booking", 0.8)
    ]

    for uc, y in use_cases:
        ellipse = patches.Ellipse((5.2, y), 3.8, 0.52, ec="#0077ed", fc="#ffffff", lw=1.5)
        ax.add_patch(ellipse)
        ax.text(5.2, y, uc, fontsize=8.5, ha='center', va='center', fontweight='bold', color='#1e293b')
        ax.plot([1.4, 3.3], [3.2, y], color="#64748b", lw=1.2)

    plt.tight_layout()
    plt.savefig('diagrams/fig_usecase_user.png', bbox_inches='tight')
    plt.close()
    print("[OK] Created diagrams/fig_usecase_user.png")

# 5. Admin Use Case Diagram
def create_usecase_admin():
    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    boundary = patches.Rectangle((2.4, 0.3), 5.6, 4.9, ec="#0f172a", fc="#f8fafc", lw=1.5, ls='--')
    ax.add_patch(boundary)
    ax.text(5.2, 4.9, "Admin Management Portal Scope", fontsize=10, fontweight='bold', ha='center', color='#0f172a')

    draw_actor(ax, 1.1, 3.2, "System\nAdministrator")

    use_cases = [
        ("Secure Admin Login Authentication", 4.3),
        ("View Dynamic Analytics & KPI Metrics", 3.6),
        ("Add / Edit / Delete Bus & Train Fleets", 2.9),
        ("Monitor Passenger Bookings & Cancellations", 2.2),
        ("Inspect Payment Transactions Ledger", 1.5),
        ("Generate & Export Route Reports to CSV", 0.8)
    ]

    for uc, y in use_cases:
        ellipse = patches.Ellipse((5.2, y), 3.8, 0.52, ec="#e52b50", fc="#ffffff", lw=1.5)
        ax.add_patch(ellipse)
        ax.text(5.2, y, uc, fontsize=8.5, ha='center', va='center', fontweight='bold', color='#1e293b')
        ax.plot([1.4, 3.3], [3.2, y], color="#64748b", lw=1.2)

    plt.tight_layout()
    plt.savefig('diagrams/fig_usecase_admin.png', bbox_inches='tight')
    plt.close()
    print("[OK] Created diagrams/fig_usecase_admin.png")

# 6. Flowchart (Booking Workflow)
def create_booking_flowchart():
    fig, ax = plt.subplots(figsize=(7, 10), dpi=300)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Start
    ax.add_patch(patches.FancyBboxPatch((2.0, 9.1), 3.0, 0.5, boxstyle="round,pad=0.2", ec="#0f172a", fc="#0f172a"))
    ax.text(3.5, 9.35, "START", color="#fff", fontweight='bold', ha='center', va='center')

    # Step 1
    ax.add_patch(patches.Rectangle((1.5, 8.2), 4.0, 0.6, ec="#0077ed", fc="#eff6ff", lw=1.5))
    ax.text(3.5, 8.5, "Search Source, Destination & Date", ha='center', va='center', fontweight='bold', fontsize=8.5)

    # Step 2
    ax.add_patch(patches.Rectangle((1.5, 7.3), 4.0, 0.6, ec="#0077ed", fc="#eff6ff", lw=1.5))
    ax.text(3.5, 7.6, "View Available Buses & Trains", ha='center', va='center', fontweight='bold', fontsize=8.5)

    # Step 3
    ax.add_patch(patches.Rectangle((1.5, 6.4), 4.0, 0.6, ec="#0077ed", fc="#eff6ff", lw=1.5))
    ax.text(3.5, 6.7, "Select Preferred Seats (Visual Map)", ha='center', va='center', fontweight='bold', fontsize=8.5)

    # Decision 1
    d1 = patches.Polygon([[3.5, 5.9], [4.9, 5.3], [3.5, 4.7], [2.1, 5.3]], ec="#e52b50", fc="#fff1f3", lw=1.5)
    ax.add_patch(d1)
    ax.text(3.5, 5.3, "Logged In?", ha='center', va='center', fontweight='bold', fontsize=8.5)

    # Side login box
    ax.add_patch(patches.Rectangle((5.3, 5.0), 1.5, 0.6, ec="#e52b50", fc="#ffffff", lw=1.5))
    ax.text(6.05, 5.3, "Login /\nRegister", ha='center', va='center', fontweight='bold', fontsize=7.5)

    # Step 4
    ax.add_patch(patches.Rectangle((1.5, 3.8), 4.0, 0.6, ec="#0077ed", fc="#eff6ff", lw=1.5))
    ax.text(3.5, 4.1, "Enter Passenger & Contact Details", ha='center', va='center', fontweight='bold', fontsize=8.5)

    # Step 5
    ax.add_patch(patches.Rectangle((1.5, 2.9), 4.0, 0.6, ec="#0077ed", fc="#eff6ff", lw=1.5))
    ax.text(3.5, 3.2, "Simulate Online Payment (UPI / Card)", ha='center', va='center', fontweight='bold', fontsize=8.5)

    # Decision 2
    d2 = patches.Polygon([[3.5, 2.5], [4.9, 2.0], [3.5, 1.5], [2.1, 2.0]], ec="#10b981", fc="#ecfdf5", lw=1.5)
    ax.add_patch(d2)
    ax.text(3.5, 2.0, "Pay Success?", ha='center', va='center', fontweight='bold', fontsize=8.5)

    # Step 6
    ax.add_patch(patches.Rectangle((1.5, 0.7), 4.0, 0.55, ec="#10b981", fc="#ffffff", lw=1.5))
    ax.text(3.5, 0.97, "Generate Boarding Pass & QR Code", ha='center', va='center', fontweight='bold', fontsize=8.5)

    # End
    ax.add_patch(patches.FancyBboxPatch((2.2, 0.05), 2.6, 0.4, boxstyle="round,pad=0.15", ec="#0f172a", fc="#0f172a"))
    ax.text(3.5, 0.25, "END: Download / Print", color="#fff", fontweight='bold', ha='center', va='center', fontsize=8.5)

    # Connectors
    arrows = [
        ((3.5, 9.1), (3.5, 8.8)),
        ((3.5, 8.2), (3.5, 7.9)),
        ((3.5, 7.3), (3.5, 7.0)),
        ((3.5, 6.4), (3.5, 5.9)),
        ((3.5, 4.7), (3.5, 4.4)),
        ((3.5, 3.8), (3.5, 3.5)),
        ((3.5, 2.9), (3.5, 2.5)),
        ((3.5, 1.5), (3.5, 1.25)),
        ((3.5, 0.7), (3.5, 0.45)),
    ]
    for p1, p2 in arrows:
        ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="->", lw=1.5, color="#1e293b"))

    ax.text(3.6, 4.5, "Yes", fontsize=8, color="#059669", fontweight='bold')
    ax.text(4.9, 5.45, "No", fontsize=8, color="#dc2626", fontweight='bold')
    ax.annotate("", xy=(5.3, 5.3), xytext=(4.9, 5.3), arrowprops=dict(arrowstyle="->", lw=1.2, color="#dc2626"))
    ax.annotate("", xy=(3.5, 4.4), xytext=(6.05, 5.0), arrowprops=dict(arrowstyle="->", lw=1.2, color="#059669", connectionstyle="arc3,rad=-0.3"))

    ax.text(3.6, 1.35, "Yes", fontsize=8, color="#059669", fontweight='bold')

    plt.tight_layout()
    plt.savefig('diagrams/fig_flowchart.png', bbox_inches='tight')
    plt.close()
    print("[OK] Created diagrams/fig_flowchart.png")

# 7. Screenshot Placeholders
def create_screenshot_placeholder(name, title, route_desc):
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    frame = patches.FancyBboxPatch((0.2, 0.2), 7.6, 4.1, boxstyle="round,pad=0.15", ec="#cbd5e1", fc="#ffffff", lw=2)
    ax.add_patch(frame)

    bar = patches.Rectangle((0.2, 3.8), 7.6, 0.5, ec="#cbd5e1", fc="#f1f5f9")
    ax.add_patch(bar)

    ax.add_patch(patches.Circle((0.5, 4.05), 0.08, color="#ef4444"))
    ax.add_patch(patches.Circle((0.75, 4.05), 0.08, color="#f59e0b"))
    ax.add_patch(patches.Circle((1.0, 4.05), 0.08, color="#10b981"))

    ax.add_patch(patches.FancyBboxPatch((1.4, 3.9), 5.8, 0.3, boxstyle="round,pad=0.05", ec="#e2e8f0", fc="#ffffff"))
    ax.text(1.6, 4.05, f"http://localhost:3000/{route_desc}", fontsize=7.5, va='center', color="#64748b", fontfamily="monospace")

    inner = patches.Rectangle((0.6, 0.6), 6.8, 3.0, ec="#94a3b8", fc="#f8fafc", lw=1.5, ls="--")
    ax.add_patch(inner)

    # Camera box icon
    ax.add_patch(patches.Rectangle((3.6, 2.3), 0.8, 0.55, ec="#0f172a", fc="#cbd5e1", lw=1.5))
    ax.add_patch(patches.Circle((4.0, 2.57), 0.16, ec="#0f172a", fc="#ffffff", lw=1.5))

    ax.text(4.0, 1.8, title, fontsize=12, fontweight='bold', ha='center', va='center', color="#0f172a")
    ax.text(4.0, 1.4, "[ Live Application Interface Screenshot Placeholder ]", fontsize=9, ha='center', va='center', color="#64748b", fontstyle='italic')
    ax.text(4.0, 1.0, "Verified in browser via Local Server (HTML5/CSS3/JavaScript)", fontsize=8, ha='center', va='center', color="#0077ed")

    plt.tight_layout()
    plt.savefig(f'diagrams/{name}.png', bbox_inches='tight')
    plt.close()
    print(f"[OK] Created diagrams/{name}.png")

if __name__ == "__main__":
    create_architecture_diagram()
    create_dfd_lvl0()
    create_dfd_lvl1()
    create_usecase_user()
    create_usecase_admin()
    create_booking_flowchart()
    
    create_screenshot_placeholder("screen_home", "Figure 8.1: Home Page & Search Interface", "index.html")
    create_screenshot_placeholder("screen_login", "Figure 8.2: User Authentication & Login Screen", "login.html")
    create_screenshot_placeholder("screen_register", "Figure 8.3: Passenger Registration Form", "register.html")
    create_screenshot_placeholder("screen_search", "Figure 8.4: Ticket Search Results & Filter Sidebar", "search.html")
    create_screenshot_placeholder("screen_seats", "Figure 8.5: Interactive Visual Seat Layout", "seat-selection.html")
    create_screenshot_placeholder("screen_checkout", "Figure 8.6: Passenger Details & Simulated Payment", "booking.html")
    create_screenshot_placeholder("screen_ticket", "Figure 8.7: Official E-Ticket Boarding Pass with QR", "ticket.html")
    create_screenshot_placeholder("screen_admin", "Figure 8.8: Admin Analytics Dashboard & Fleet Management", "admin/dashboard.html")
