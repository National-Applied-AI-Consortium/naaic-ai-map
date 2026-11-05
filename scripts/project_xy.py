#!/usr/bin/env python3
"""Look up colleges in the IPEDS directory file and give their map position (xy) for data/naaic-map.json.

Needs: `python3 scripts/refresh_ipeds.py` (downloads data/raw/HD<year>.zip) and `npm ci` (for scripts/geo.mjs).
Usage: python3 scripts/project_xy.py 225423 184180 ...
Prints one JSON object per college: id, name, city, state, lat, lon, xy, geo_source.
"""
import csv, io, json, pathlib, subprocess, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"


def ipeds_rows(unitids):
    zips = sorted(RAW.glob("HD*.zip"))
    if not zips:
        raise SystemExit("no data/raw/HD<year>.zip; run python3 scripts/refresh_ipeds.py first")
    z = zipfile.ZipFile(zips[-1])
    name = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
    out = {}
    for r in csv.DictReader(io.TextIOWrapper(z.open(name), encoding="latin-1")):
        r = {k.strip().lstrip("\ufeff").lstrip("ï»¿").upper(): (v or "").strip() for k, v in r.items()}
        if r["UNITID"] in unitids:
            out[r["UNITID"]] = dict(id=r["UNITID"], name=r["INSTNM"], city=r["CITY"], state=r["STABBR"],
                                    lat=float(r["LATITUDE"]), lon=float(r["LONGITUD"]),
                                    geo_source=f"https://nces.ed.gov/ipeds/datacenter/data/{zips[-1].name}")
    return out


def main():
    ids = sys.argv[1:]
    if not ids:
        raise SystemExit(__doc__)
    rows = ipeds_rows(set(ids))
    missing = [u for u in ids if u not in rows]
    if missing:
        print("not found in IPEDS:", " ".join(missing), file=sys.stderr)
    pts = [{"id": u, "lon": r["lon"], "lat": r["lat"]} for u, r in rows.items()]
    res = subprocess.run(["node", str(ROOT / "scripts" / "geo.mjs")], input=json.dumps(pts),
                         capture_output=True, text=True, check=True)
    xy = {p["id"]: p["xy"] for p in json.loads(res.stdout)["points"]}
    for u in ids:
        if u in rows:
            print(json.dumps(dict(rows[u], xy=xy.get(u)), ensure_ascii=False))


if __name__ == "__main__":
    main()
