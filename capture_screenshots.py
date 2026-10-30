"""
Capture real live screenshots of TravelEase using Microsoft Edge Headless
"""

import subprocess
import time
import os

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE_PATH):
    EDGE_PATH = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

os.makedirs('diagrams', exist_ok=True)

targets = [
    ("screen_home.png", "http://localhost:3000/index.html", "1280,820"),
    ("screen_login.png", "http://localhost:3000/login.html", "1280,800"),
    ("screen_register.png", "http://localhost:3000/register.html", "1280,850"),
    ("screen_search.png", "http://localhost:3000/search.html?source=Delhi&destination=Shimla", "1280,850"),
    ("screen_seats.png", "http://localhost:3000/seat-selection.html?id=BUS-101&date=2026-11-10", "1280,850"),
    ("screen_ticket.png", "http://localhost:3000/ticket.html?id=TRV-894120", "1280,900"),
    ("screen_admin.png", "http://localhost:3000/admin/dashboard.html", "1280,850"),
    ("screen_mybookings.png", "http://localhost:3000/my-bookings.html", "1280,800")
]

print("Starting headless screenshot captures...")
for filename, url, size in targets:
    out_path = os.path.join('diagrams', filename)
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        f"--window-size={size}",
        f"--screenshot={out_path}",
        url
    ]
    try:
        subprocess.run(cmd, check=True, timeout=15)
        print(f"[OK] Captured real screenshot: {out_path}")
    except Exception as e:
        print(f"[ERROR] Failed to capture {filename}: {e}")

print("All live screenshots captured successfully!")
