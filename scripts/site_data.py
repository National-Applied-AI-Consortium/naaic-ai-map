#!/usr/bin/env python3
"""Move the map data between data/naaic-map.json and the copy embedded in site/index.html, and check the site.

The live page is one self-contained file. Its data lives on a single line that starts with `const D={`.
data/naaic-map.json is the readable copy of that same object.

Usage (from the repo root):
  python3 scripts/site_data.py extract   # site/index.html -> data/naaic-map.json
  python3 scripts/site_data.py growth    # recompute the yearly counts in data/naaic-map.json from growth_progs
  python3 scripts/site_data.py ipeds     # data/ipeds_cip110102_by_year.csv -> the ipeds rows in data/naaic-map.json
  python3 scripts/site_data.py embed     # data/naaic-map.json -> site/index.html
  python3 scripts/site_data.py check     # validate data and site; non-zero exit on any problem
"""
import csv, datetime, json, pathlib, re, sys, xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "site" / "index.html"
DATA = ROOT / "data" / "naaic-map.json"
IPEDS = ROOT / "data" / "ipeds_cip110102_by_year.csv"
PREFIX = "const D="


def _split(html):
    lines = html.split("\n")
    hits = [i for i, s in enumerate(lines) if s.startswith(PREFIX + "{")]
    if len(hits) != 1:
        raise SystemExit(f"expected exactly one line starting with {PREFIX}{{ in {INDEX}, found {len(hits)}")
    i = hits[0]
    s = lines[i]
    if not s.endswith(";"):
        raise SystemExit("embedded data line does not end with ';'")
    return lines, i, s[len(PREFIX):-1]


def compact(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)


def read_embedded():
    _, _, raw = _split(INDEX.read_text(encoding="utf-8"))
    obj = json.loads(raw)
    assert compact(obj) == raw, "embedded data is not in the canonical compact form"
    return obj


def extract():
    obj = read_embedded()
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {DATA.relative_to(ROOT)}")


def embed():
    obj = json.loads(DATA.read_text(encoding="utf-8"))
    html = INDEX.read_text(encoding="utf-8")
    lines, i, _ = _split(html)
    lines[i] = PREFIX + compact(obj) + ";"
    INDEX.write_text("\n".join(lines), encoding="utf-8")
    print(f"updated {INDEX.relative_to(ROOT)}")


def growth_counts(D):
    """Yearly cumulative program counts for the growth table (United States and Texas). A program counts from its
    first-offered year onward; programs that started before the first table year count from that year."""
    y0 = min(g["year"] for g in D["growth"])
    out = {}
    for g in D["growth"]:
        y = g["year"]
        rows = [p for p in D["growth_progs"] if max(p["fy"], y0) <= y]
        out[y] = (len(rows), sum(1 for p in rows if p["state"] == "TX"))
    return out


def unknown_count(D):
    """Program rows on the map with no sourced launch year, shown as a note under the growth table."""
    dated = {(p["unitid"], p["name"]) for p in D["growth_progs"]}
    return sum(1 for c in D["inst"] if c["kind"] == "prog" for p in c["programs"] if (c["id"], p["name"]) not in dated)


def growth():
    D = json.loads(DATA.read_text(encoding="utf-8"))
    for g in D["growth"]:
        g["us"], g["tx"] = growth_counts(D)[g["year"]]
        g["unknown"] = str(unknown_count(D))
    D["growth_unknown_us"] = str(unknown_count(D))
    DATA.write_text(json.dumps(D, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("growth counts:", {g["year"]: g["us"] for g in D["growth"]})


def need(rec, where):
    """Problems with the source link and date that every published item must have."""
    problems = []
    if not re.match(r"^https?://", str(rec.get("source_url") or "")):
        problems.append(f"{where}: missing or non-http source_url")
    if not rec.get("as_of"):
        problems.append(f"{where}: missing as_of")
    return problems


def launch_problems(p, where):
    """Problems with a program's status. The map lists launched programs only; announced, approved or upcoming
    ones wait in NEEDS-VERIFICATION.md."""
    if re.fullmatch(r"offered( \(.+\))?", str(p.get("status") or "")):
        return []
    return [f"{where}: status {p.get('status')!r} is not launched (move it to NEEDS-VERIFICATION.md)"]


def valid_date(d):
    """True for a date the page can show: YYYY-MM-DD or YYYY-MM."""
    fmt = {10: "%Y-%m-%d", 7: "%Y-%m"}.get(len(str(d)))
    try:
        return bool(fmt and datetime.datetime.strptime(str(d), fmt))
    except ValueError:
        return False


def featured_problems(entries):
    """Problems in the "As featured in" entries. The section shows whatever is here, so an entry must be complete."""
    problems = []
    for e in entries:
        where = f"featured {e.get('outlet')!r}"
        problems += need(e, where)
        if not valid_date(e.get("date")):
            problems.append(f"{where}: date must be YYYY-MM-DD or YYYY-MM")
        if not re.match(r"^data:image/[\w.+-]+[;,].", str(e.get("logo") or "")):
            problems.append(f"{where}: logo must be embedded as a data:image/ URI")
        for k in ("outlet", "excerpt"):
            if not e.get(k):
                problems.append(f"{where}: missing {k}")
    return problems


def ipeds_rows():
    """The growth table's IPEDS rows, as scripts/refresh_ipeds_cip.py rebuilt them."""
    with IPEDS.open(encoding="utf-8", newline="") as f:
        return [{"year": int(r["award_year_end"]), "award_year": r["award_year"], "release": r["release"],
                 "completers": int(r["total_completers"]), "source_url": r["source_url"], "as_of": r["as_of"]}
                for r in csv.DictReader(f)]


def ipeds():
    D = json.loads(DATA.read_text(encoding="utf-8"))
    D["ipeds"] = ipeds_rows()
    DATA.write_text(json.dumps(D, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("ipeds completers:", {r["year"]: r["completers"] for r in D["ipeds"]})


def check():
    problems = []
    D = read_embedded()
    if DATA.exists() and json.loads(DATA.read_text(encoding="utf-8")) != D:
        problems.append("data/naaic-map.json differs from the data embedded in site/index.html (run extract or embed)")

    ids = set()
    for c in D["inst"]:
        ids.add(c["id"])
        if c["kind"] not in ("prog", "ep", "grant"):
            problems.append(f"inst {c['id']}: unknown kind {c['kind']!r}")
        if c["kind"] == "prog" and not c["programs"]:
            problems.append(f"inst {c['id']}: on the map (kind prog) but has no programs")
        if not c.get("xy"):
            problems.append(f"inst {c['id']}: no map position (xy)")
        for p in c["programs"]:
            where = f"program {c['id']} {p.get('name')!r}"
            problems += need(p, where) + launch_problems(p, where)
    for g in D["grants"]:
        problems += need(g, f"grant {g.get('id')}")
    for l in D["lines"]:
        if l["a"] not in ids or l["b"] not in ids:
            problems.append(f"line {l['a']}-{l['b']}: endpoint not in inst")
        for it in l["items"]:
            problems += need(it, f"line {l['a']}-{l['b']}")
    problems += featured_problems(D["featured"])
    for p in D["growth_progs"] + D["hcc"]:
        if p.get("conf") != "high":
            problems.append(f"growth row {p.get('unitid')} {p.get('name')!r}: confidence {p.get('conf')!r} (only 'high' rows are published)")

    gc = growth_counts(D)
    for g in D["growth"]:
        if (g["us"], g["tx"]) != gc[g["year"]]:
            problems.append(f"growth {g['year']}: stored {g['us']}/{g['tx']} but growth_progs gives {gc[g['year']][0]}/{gc[g['year']][1]} (run growth)")

    if D["growth_unknown_us"] != str(unknown_count(D)):
        problems.append(f"growth_unknown_us: stored {D['growth_unknown_us']} but the data gives {unknown_count(D)} (run growth)")

    for r in D["ipeds"]:
        problems += need(r, f"ipeds {r.get('year')}")
    if D["ipeds"] != ipeds_rows():
        problems.append(f"ipeds: the embedded rows differ from {IPEDS.relative_to(ROOT)} (run ipeds)")

    html = INDEX.read_text(encoding="utf-8")
    if "Content-Security-Policy" not in html or "default-src 'none'" not in html:
        problems.append("index.html: strict Content-Security-Policy meta tag missing")
    for f in [INDEX, ROOT / "site" / "news" / "index.html"]:
        h = f.read_text(encoding="utf-8")
        if re.search(r"<script[^>]+\bsrc=[\"']https?://", h) or re.search(r"<link[^>]+rel=[\"']stylesheet[\"'][^>]+href=[\"']https?://", h):
            problems.append(f"{f.relative_to(ROOT)}: loads a third-party script or stylesheet")
    try:
        ET.parse(ROOT / "site" / "feed.xml")
    except ET.ParseError as e:
        problems.append(f"feed.xml: not well-formed XML ({e})")

    on_map = sum(1 for c in D["inst"] if c["kind"] == "prog")
    n_prog = sum(len(c["programs"]) for c in D["inst"] if c["kind"] == "prog")
    print(f"updated {D['updated']}: {on_map} colleges on the map, {n_prog} programs, "
          f"{len(D['inst'])} institutions in total, {len(D['grants'])} grants, {len(D['lines'])} partnership lines, {len(D['featured'])} featured")
    for p in problems:
        print("PROBLEM:", p)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "extract": extract()
    elif cmd == "growth": growth()
    elif cmd == "ipeds": ipeds()
    elif cmd == "embed": embed()
    elif cmd == "check": sys.exit(check())
    else: raise SystemExit(__doc__)
