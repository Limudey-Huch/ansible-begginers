// Live Aircraft Radar — polls /api/aircraft and draws a classic radar scope.
// Center/range match the poller's default bounding box (see poller.py) — change
// both together if you point the radar at a different city.
const CENTER_LAT = 59.5;
const CENTER_LON = 18.0;
const MAX_RANGE_KM = 150;
const POLL_MS = 5000;
const SWEEP_PERIOD_MS = 4000;

const canvas = document.getElementById("radar");
const ctx = canvas.getContext("2d");
const W = canvas.width, H = canvas.height, CX = W / 2, CY = H / 2, R = W / 2 - 10;
const infoPanel = document.getElementById("info");
const countEl = document.getElementById("count");

let aircraft = [];
let blipPositions = []; // [{x, y, plane}] — recomputed every draw, used for click hit-testing

function toRad(d) { return d * Math.PI / 180; }

// Haversine distance (km) + initial bearing (degrees) from center to a point.
function distanceAndBearing(lat, lon) {
  const R_EARTH = 6371;
  const dLat = toRad(lat - CENTER_LAT);
  const dLon = toRad(lon - CENTER_LON);
  const a = Math.sin(dLat / 2) ** 2 +
            Math.cos(toRad(CENTER_LAT)) * Math.cos(toRad(lat)) * Math.sin(dLon / 2) ** 2;
  const dist = R_EARTH * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  const y = Math.sin(dLon) * Math.cos(toRad(lat));
  const x = Math.cos(toRad(CENTER_LAT)) * Math.sin(toRad(lat)) -
            Math.sin(toRad(CENTER_LAT)) * Math.cos(toRad(lat)) * Math.cos(dLon);
  const bearing = (Math.atan2(y, x) * 180 / Math.PI + 360) % 360;

  return { dist, bearing };
}

function drawScope(sweepAngle) {
  ctx.clearRect(0, 0, W, H);

  // Range rings
  ctx.strokeStyle = "rgba(57, 255, 106, 0.25)";
  ctx.fillStyle = "rgba(57, 255, 106, 0.6)";
  ctx.font = "10px monospace";
  for (let i = 1; i <= 3; i++) {
    const r = (R / 3) * i;
    ctx.beginPath();
    ctx.arc(CX, CY, r, 0, Math.PI * 2);
    ctx.stroke();
    ctx.fillText(Math.round((MAX_RANGE_KM / 3) * i) + " km", CX + 4, CY - r + 10);
  }
  // Crosshair
  ctx.beginPath();
  ctx.moveTo(CX, CY - R); ctx.lineTo(CX, CY + R);
  ctx.moveTo(CX - R, CY); ctx.lineTo(CX + R, CY);
  ctx.stroke();

  // Rotating sweep
  const sweepRad = toRad(sweepAngle);
  const grad = ctx.createLinearGradient(
    CX, CY, CX + R * Math.sin(sweepRad), CY - R * Math.cos(sweepRad)
  );
  grad.addColorStop(0, "rgba(57, 255, 106, 0.5)");
  grad.addColorStop(1, "rgba(57, 255, 106, 0)");
  ctx.strokeStyle = grad;
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(CX, CY);
  ctx.lineTo(CX + R * Math.sin(sweepRad), CY - R * Math.cos(sweepRad));
  ctx.stroke();
  ctx.lineWidth = 1;

  // Blips
  blipPositions = [];
  for (const plane of aircraft) {
    if (plane.lat == null || plane.lon == null) continue;
    const { dist, bearing } = distanceAndBearing(plane.lat, plane.lon);
    if (dist > MAX_RANGE_KM) continue; // out of range — doesn't get drawn (= "disappeared")
    const r = (dist / MAX_RANGE_KM) * R;
    const rad = toRad(bearing);
    const x = CX + r * Math.sin(rad);
    const y = CY - r * Math.cos(rad);

    ctx.fillStyle = "#39ff6a";
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillText(plane.callsign || plane.icao24, x + 6, y - 6);

    blipPositions.push({ x, y, plane });
  }

  countEl.textContent = aircraft.length ? `(${aircraft.length} tracked)` : "";
}

async function refreshData() {
  try {
    const resp = await fetch("/api/aircraft");
    aircraft = await resp.json();
  } catch (e) {
    console.error("Failed to fetch /api/aircraft", e);
  }
}

canvas.addEventListener("click", (ev) => {
  const rect = canvas.getBoundingClientRect();
  const clickX = ev.clientX - rect.left;
  const clickY = ev.clientY - rect.top;

  let closest = null, closestDist = 12; // px hit-test radius
  for (const b of blipPositions) {
    const d = Math.hypot(b.x - clickX, b.y - clickY);
    if (d < closestDist) { closest = b.plane; closestDist = d; }
  }

  if (closest) {
    infoPanel.innerHTML = `
      <div><b>Callsign:</b> ${closest.callsign || "(unknown)"}</div>
      <div><b>ICAO24:</b> ${closest.icao24}</div>
      <div><b>Altitude:</b> ${closest.baro_altitude != null ? Math.round(closest.baro_altitude) + " m" : "?"}</div>
      <div><b>Speed:</b> ${closest.velocity != null ? Math.round(closest.velocity * 3.6) + " km/h" : "?"}</div>
      <div><b>Heading:</b> ${closest.true_track != null ? Math.round(closest.true_track) + "°" : "?"}</div>
    `;
    infoPanel.classList.remove("hidden");
  } else {
    infoPanel.classList.add("hidden");
  }
});

function animate(ts) {
  const sweepAngle = (ts / SWEEP_PERIOD_MS * 360) % 360;
  drawScope(sweepAngle);
  requestAnimationFrame(animate);
}

refreshData();
setInterval(refreshData, POLL_MS);
requestAnimationFrame(animate);
