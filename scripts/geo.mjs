// Build-time only: projects college points (lon, lat) into the map's Albers USA coordinates and
// also returns the state outlines. Base map: us-atlas (ISC license), derived from U.S. Census Bureau
// cartographic boundary files (public domain).
// Usage: echo '[{"id":"225423","lon":-95.4,"lat":29.7}]' | node scripts/geo.mjs
// Needs `npm install` (or `npm ci`) in the repo root first.
import fs from "fs";
import { createRequire } from "module";
const require = createRequire(new URL("../package.json", import.meta.url));
const topo = require("topojson-client");
const d3 = require("d3-geo");
const us = JSON.parse(fs.readFileSync(require.resolve("us-atlas/states-albers-10m.json")));
const pts = JSON.parse(fs.readFileSync(0, "utf8"));
const path = d3.geoPath();
const proj = d3.geoAlbersUsa().scale(1300).translate([487.5, 305]);
const rnd = s => s.replace(/(\d+\.\d)\d+/g, "$1");
const states = topo.feature(us, us.objects.states).features.map(f => {
  const b = path.bounds(f);
  return { name: f.properties.name, d: rnd(path(f)), bbox: b.flat().map(v => +v.toFixed(1)), c: path.centroid(f).map(v => +v.toFixed(1)) };
});
const out = {
  states,
  border: rnd(path(topo.mesh(us, us.objects.states, (a, b) => a !== b))),
  points: pts.map(p => { const xy = proj([p.lon, p.lat]); return { id: p.id, xy: xy ? xy.map(v => +v.toFixed(1)) : null }; }),
};
process.stdout.write(JSON.stringify(out));
