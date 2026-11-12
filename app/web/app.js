// CampusRoute web client. No frameworks, no innerHTML with data:
// everything from the API is inserted with textContent.
"use strict";

const $ = (id) => document.getElementById(id);
const SVG = "http://www.w3.org/2000/svg";
let campus = { places: [], edges: [] };

async function api(path, params = {}) {
  const url = new URL(path, window.location.origin);
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== "") url.searchParams.set(k, v);
  }
  const res = await fetch(url);
  const body = await res.json();
  if (!res.ok) throw new Error(body.error || res.statusText);
  return body;
}

function el(tag, text, cls) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (cls) node.className = cls;
  return node;
}

function svg(tag, attrs) {
  const node = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  return node;
}

function drawMap(routePath = []) {
  const map = $("map");
  map.replaceChildren();
  const byId = Object.fromEntries(campus.places.map((p) => [p.id, p]));
  const onRoute = new Set();
  for (let i = 0; i + 1 < routePath.length; i++) {
    onRoute.add([routePath[i], routePath[i + 1]].sort().join("|"));
  }
  for (const e of campus.edges) {
    const a = byId[e.a], b = byId[e.b];
    const key = [e.a, e.b].sort().join("|");
    const cls = ["edge", e.stairs ? "stairs" : "", e.covered ? "covered" : "", onRoute.has(key) ? "route" : ""].join(" ");
    map.append(svg("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, class: cls }));
  }
  for (const p of campus.places) {
    const g = svg("g", { class: "place " + p.kind + (routePath.includes(p.id) ? " on" : "") });
    g.append(svg("circle", { cx: p.x, cy: p.y, r: p.kind === "junction" ? 5 : 11 }));
    if (p.kind !== "junction") {
      const label = svg("text", { x: p.x, y: p.y - 16, "text-anchor": "middle" });
      label.textContent = p.name;
      g.append(label);
    }
    map.append(g);
  }
}

async function findRoute(event) {
  if (event) event.preventDefault();
  const steps = $("route-steps");
  steps.replaceChildren();
  try {
    const r = await api("/api/route", {
      from: $("from").value, to: $("to").value,
      avoid_stairs: $("avoid-stairs").checked ? "1" : "",
    });
    $("route-summary").textContent =
      `${r.names[0]} → ${r.names[r.names.length - 1]}: ${r.meters} m, about ${r.minutes} min` +
      (r.has_stairs ? " (includes stairs)" : "");
    for (const s of r.steps) steps.append(el("li", s));
    drawMap(r.path);
  } catch (err) {
    $("route-summary").textContent = "⚠ " + err.message;
    drawMap();
  }
}

let searchTimer;
function onSearch() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(async () => {
    const list = $("results");
    list.replaceChildren();
    const q = $("q").value.trim();
    if (!q) return;
    const { results } = await api("/api/search", { q });
    if (!results.length) list.append(el("li", "No matches", "muted"));
    for (const hit of results) {
      const li = el("li");
      const btn = el("button", hit.label, "link");
      btn.type = "button";
      btn.addEventListener("click", () => { $("to").value = hit.id; findRoute(); });
      li.append(btn);
      list.append(li);
    }
  }, 200);
}

async function refreshNow() {
  const now = $("now").value;
  const box = $("next");
  box.replaceChildren();
  const n = await api("/api/next-class", { now });
  if (n.current) box.append(el("p", "Now: " + n.current));
  if (n.next) {
    box.append(el("p", `Next: ${n.next.session} — in ${n.next.in_minutes} min`, "summary"));
    if (n.next.place) {
      const btn = el("button", "Route me there", "link");
      btn.type = "button";
      btn.addEventListener("click", () => { $("to").value = n.next.place; findRoute(); });
      box.append(btn);
    }
  }
  const crowd = $("crowd");
  crowd.replaceChildren();
  const { levels } = await api("/api/crowd", { now });
  const names = Object.fromEntries(campus.places.map((p) => [p.id, p.name]));
  const entries = Object.entries(levels);
  if (!entries.length) crowd.append(el("li", "No recent reports", "muted"));
  for (const [id, level] of entries) crowd.append(el("li", `${names[id]}: ${level}`, "crowd " + level));
}

async function init() {
  campus = await api("/api/places");
  const list = $("place-list");
  for (const p of campus.places) {
    if (p.kind === "junction") continue;
    const option = document.createElement("option");
    option.value = p.name;
    list.append(option);
  }
  drawMap();
  $("route-form").addEventListener("submit", findRoute);
  $("q").addEventListener("input", onSearch);
  $("now").addEventListener("change", refreshNow);
  await findRoute();
  await refreshNow();
}

init().catch((err) => { $("route-summary").textContent = "⚠ Could not reach the API: " + err.message; });
