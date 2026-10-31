/**
 * Automated Website Screenshot Capture
 * Spins up local HTTP server on port 3055 and uses headless Chrome
 * to capture pixel-perfect screenshots of all application screens.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const PORT = 3055;
const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const OUTPUT_DIR = path.join(__dirname, 'diagrams');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

const screens = [
  { name: 'screen_home.png', url: `http://localhost:${PORT}/index.html`, size: '1280,850' },
  { name: 'screen_login.png', url: `http://localhost:${PORT}/login.html`, size: '1280,850' },
  { name: 'screen_register.png', url: `http://localhost:${PORT}/register.html`, size: '1280,850' },
  { name: 'screen_search.png', url: `http://localhost:${PORT}/search.html?source=Delhi&destination=Shimla&date=2026-11-10`, size: '1280,850' },
  { name: 'screen_seats.png', url: `http://localhost:${PORT}/seat-selection.html?id=BUS-101&date=2026-11-10&preview=1`, size: '1280,850' },
  { name: 'screen_checkout.png', url: `http://localhost:${PORT}/booking.html?preview=1`, size: '1280,850' },
  { name: 'screen_mybookings.png', url: `http://localhost:${PORT}/my-bookings.html?preview=1`, size: '1280,850' },
  { name: 'screen_ticket.png', url: `http://localhost:${PORT}/ticket.html?id=TRV-894120`, size: '1280,850' },
  { name: 'screen_admin.png', url: `http://localhost:${PORT}/admin/dashboard.html?preview=1`, size: '1280,850' }
];

const server = http.createServer((req, res) => {
  let reqPath = decodeURI(req.url.split('?')[0]);
  if (reqPath === '/' || reqPath === '') reqPath = '/index.html';

  const filePath = path.join(__dirname, reqPath);
  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end(`404 Not Found: ${reqPath}`);
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    }
  });
});

server.listen(PORT, async () => {
  console.log(`[INFO] Screenshot server running at http://localhost:${PORT}`);

  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  for (const s of screens) {
    const outPath = path.join(OUTPUT_DIR, s.name);
    console.log(`[CAPTURE] Rendering ${s.name} from ${s.url} ...`);
    try {
      const cmd = `cmd.exe /c ""${CHROME_PATH}" --headless=new --window-size=${s.size} --force-device-scale-factor=1 --hide-scrollbars --virtual-time-budget=2000 --screenshot="${outPath}" "${s.url}""`;
      execSync(cmd, { stdio: 'inherit' });
      if (fs.existsSync(outPath)) {
        const stats = fs.statSync(outPath);
        console.log(`[OK] Successfully saved ${s.name} (${stats.size} bytes)`);
      } else {
        console.warn(`[WARN] File was not created: ${outPath}`);
      }
    } catch (e) {
      console.error(`[ERROR] Failed to capture ${s.name}:`, e.message);
    }
  }

  console.log('[DONE] All screenshots processed. Closing server.');
  server.close(() => {
    process.exit(0);
  });
});
