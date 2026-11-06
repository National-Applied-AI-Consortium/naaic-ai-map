#!/usr/bin/env node
// Tests for the credential filter. Runs the page's own script lines, the part that doesn't touch the DOM, on sample colleges.
// Run from the repo root: node scripts/test_credential_filter.mjs
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const lines = readFileSync(new URL("../site/index.html", import.meta.url), "utf8").split("\n");
const at = (prefix) => {
  const i = lines.findIndex((s) => s.startsWith(prefix));
  assert.notEqual(i, -1, `no line starts with ${prefix}`);
  return i;
};
const SCRIPT = [
  lines[at("const C=")],
  lines[at("const esc=")],
  ...lines.slice(at("const YEARS="), at("const pinned=") + 1),
  lines[at("const CRED=")],
  lines[at("const rowHTML=")],
].join("\n");

const cert = (name) => ({ name, award: "Certificate" });
const assoc = (name) => ({ name, award: "AAS/AS (associate)" });
const bach = (name) => ({ name, award: "BAS/Bachelor's" });
const college = (id, ...programs) => ({ id, kind: "prog", programs });

const SAMPLE = [
  college("certOnly", cert("Cert")),
  college("assocAndCert", assoc("Degree"), cert("Later cert")),
  college("bachAndUndatedCert", bach("BS"), cert("Undated cert")),
  college("undated", cert("No year")),
  { id: "grantOnly", kind: "grant", programs: [] },
];
const YEARS = [
  ["certOnly", "Cert", 2023],
  ["assocAndCert", "Degree", 2022],
  ["assocAndCert", "Later cert", 2024],
  ["bachAndUndatedCert", "BS", 2018],
];

function page(inst = SAMPLE, growth_progs = YEARS.map(([unitid, name, fy]) => ({ unitid, name, fy }))) {
  const D = { inst, grants: [], growth: [2020, 2021, 2022, 2023, 2024, 2025, 2026].map((year) => ({ year })), growth_progs };
  const ctx = vm.createContext({ D });
  vm.runInContext(SCRIPT, ctx);
  const run = (code) => vm.runInContext(code, ctx);
  return {
    run,
    types: () => JSON.parse(run(`JSON.stringify(credTypes().map(t=>t.k))`)),
    shown(cred, year) {
      ctx.pick = cred;
      ctx.at = year;
      return JSON.parse(run(`cred=pick;year=at;JSON.stringify(pinned().map(c=>c.id))`));
    },
    matching(cred, year, id) {
      ctx.pick = cred;
      ctx.at = year;
      ctx.id = id;
      return JSON.parse(run(`cred=pick;JSON.stringify(C[id].programs.filter(p=>credAt(C[id],p,at)).map(p=>p.name))`));
    },
  };
}

test("a college appears when any program matches, not only its highest credential", () => {
  const p = page();
  assert.deepEqual(p.shown("tc", 2026), ["certOnly", "assocAndCert", "bachAndUndatedCert", "undated"]);
  assert.deepEqual(p.shown("ta", 2026), ["assocAndCert"]);
  assert.deepEqual(p.shown("tb", 2026), ["bachAndUndatedCert"]);
});

test("the highest credential stays available for the details label while filtered", () => {
  const p = page();
  p.shown("tc", 2026);
  assert.equal(p.run(`TY(C.assocAndCert)`), "ta");
  assert.equal(p.run(`TY(C.bachAndUndatedCert)`), "tb");
  assert.equal(p.run(`TY(C.certOnly)`), "tc");
});

test("with a filter on, every shown college's dot uses the selected credential's color", () => {
  const p = page([college("assocAndBach", assoc("A"), bach("B")), college("certAndAssoc", cert("C"), assoc("D")), college("certOnly", cert("E"))]);
  const dots = (cred) => p.shown(cred, 2026).map((id) => [id, p.run(`dotCls(C.${id})`)]);
  assert.deepEqual(dots("ta"), [["assocAndBach", "dot ta"], ["certAndAssoc", "dot ta"]]);
  assert.deepEqual(dots("tc"), [["certAndAssoc", "dot tc"], ["certOnly", "dot tc"]]);
  assert.deepEqual(dots("tb"), [["assocAndBach", "dot tb"]]);
});

test("with no filter on, dots show the highest credential", () => {
  const p = page([college("assocAndBach", assoc("A"), bach("B")), college("certAndAssoc", cert("C"), assoc("D")), college("certOnly", cert("E"))]);
  p.shown("ta", 2026);
  const dots = () => p.shown(null, 2026).map((id) => p.run(`dotCls(C.${id})`));
  assert.deepEqual(dots(), ["dot tb", "dot ta", "dot tc"]);
});

test("the hover popup's color dot follows the same rule", () => {
  const p = page([college("assocAndBach", assoc("A"), bach("B"))]);
  const row = () => p.run(`rowHTML(C.assocAndBach)`);
  p.shown("ta", 2026);
  assert.match(row(), /class="cpd ta"/);
  assert.match(row(), /1 associate degree/);
  p.shown(null, 2026);
  assert.match(row(), /class="cpd tb"/);
});

test("amber marks an unconfirmed year on the matching program, in the selected color", () => {
  const { run } = page([college("c", assoc("Unsure degree"), cert("Sure cert"), bach("Unsure BS"))], [
    { unitid: "c", name: "Unsure degree", fy: 2021, conf: "medium" },
    { unitid: "c", name: "Sure cert", fy: 2021, conf: "high" },
    { unitid: "c", name: "Unsure BS", fy: 2022, method: "board_approval" },
  ]);
  assert.equal(run(`cred=null;dotCls(C.c)`), "dot tb");
  assert.equal(run(`cred="ta";dotCls(C.c)`), "dot amb ta");
  assert.equal(run(`cred="tb";dotCls(C.c)`), "dot amb tb");
  assert.equal(run(`cred="tc";dotCls(C.c)`), "dot tc");
  const alone = page([college("d", assoc("Unsure degree"))], [{ unitid: "d", name: "Unsure degree", fy: 2021, conf: "medium" }]);
  assert.equal(alone.run(`cred=null;dotCls(C.d)`), "dot amb ta");
});

test("the legend sentence names the selected color, not the highest credential", () => {
  const p = page();
  p.shown("ta", 2026);
  const text = p.run(`credLegend()`);
  assert.match(text, /with an associate degree/);
  assert.match(text, /associate degree color/);
  assert.doesNotMatch(text, /highest/i);
});

test("the year slider follows the matching program, not the college's first program", () => {
  const p = page();
  assert.deepEqual(p.shown("tc", 2023), ["certOnly"]);
  assert.deepEqual(p.shown("tc", 2024), ["certOnly", "assocAndCert"]);
  assert.deepEqual(p.shown("ta", 2022), ["assocAndCert"]);
});

test("a matching program with no sourced year counts only in the latest year", () => {
  const p = page();
  assert.ok(!p.shown("tc", 2025).includes("undated"));
  assert.ok(!p.shown("tc", 2025).includes("bachAndUndatedCert"));
  assert.ok(p.shown("tc", 2026).includes("undated"));
  assert.ok(p.shown("tb", 2025).includes("bachAndUndatedCert"));
});

test("start years before the first slider year count from that year", () => {
  assert.deepEqual(page().shown("tb", 2020), ["bachAndUndatedCert"]);
});

test("clearing the filter returns the same colleges as no filter", () => {
  const p = page();
  const full = ["certOnly", "assocAndCert", "bachAndUndatedCert", "undated"];
  p.shown("tb", 2026);
  assert.deepEqual(p.shown(null, 2026), full);
  assert.deepEqual(p.shown(null, 2023), ["certOnly", "assocAndCert", "bachAndUndatedCert"]);
  assert.deepEqual(p.shown(null, 2021), ["bachAndUndatedCert"]);
});

test("the detail view's matches are that college's matching programs at that year", () => {
  const p = page();
  assert.deepEqual(p.matching("tc", 2026, "assocAndCert"), ["Later cert"]);
  assert.deepEqual(p.matching("ta", 2026, "assocAndCert"), ["Degree"]);
  assert.deepEqual(p.matching("tc", 2023, "assocAndCert"), []);
  assert.deepEqual(p.matching("tb", 2026, "certOnly"), []);
});

test("the unconfirmed-year count follows the filter", () => {
  const p = page();
  assert.equal(p.run(`cred="tc";undatedC(C.undated)`), true);
  assert.equal(p.run(`cred="tc";undatedC(C.bachAndUndatedCert)`), true);
  assert.equal(p.run(`cred="tb";undatedC(C.bachAndUndatedCert)`), false);
  assert.equal(p.run(`cred="ta";undatedC(C.undated)`), false);
  assert.equal(p.run(`cred=null;undatedC(C.undated)`), true);
  assert.equal(p.run(`cred=null;undatedC(C.bachAndUndatedCert)`), false);
});

test("need-confirmation follows the matching program", () => {
  const { run } = page([college("c", assoc("Degree"), cert("Sure cert"))], [
    { unitid: "c", name: "Degree", fy: 2021, conf: "medium" },
    { unitid: "c", name: "Sure cert", fy: 2022, conf: "high" },
  ]);
  assert.equal(run(`cred=null;ambC(C.c)`), true);
  assert.equal(run(`cred="ta";ambC(C.c)`), true);
  assert.equal(run(`cred="tc";ambC(C.c)`), false);
});

test("the filter offers only credentials on the map, lowest first", () => {
  assert.deepEqual(page().types(), ["tc", "ta", "tb"]);
  assert.deepEqual(page([college("x", cert("Cert")), { id: "g", kind: "grant", programs: [] }]).types(), ["tc"]);
});

test("the filter picks up a new credential type from one new table row (naaic-ai-map-planning#3)", () => {
  const p = page([...SAMPLE, college("tracked", { name: "AI track", award: "AI track" })]);
  p.run(`CT.splice(2,0,{k:"tt",re:/track/i,short:"AI track",label:"AI track",a:"an",one:"AI track",many:"AI tracks"})`);
  assert.deepEqual(p.shown("tt", 2026), ["tracked"]);
  assert.equal(p.run(`TY(C.tracked)`), "tt");
  assert.deepEqual(p.types(), ["tc", "tt", "ta", "tb"]);
});
