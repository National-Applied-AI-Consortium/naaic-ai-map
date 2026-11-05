#!/usr/bin/env python3
"""IPEDS refresh: downloads the NCES IPEDS Institutional Characteristics
(HD<year>) file and writes a community-college lookup (unitid -> name, city, state, lat, lon).
Public domain (U.S. Dept. of Education, NCES). No AI calls.
Usage: python3 scripts/refresh_ipeds.py [--year 2024]
Outputs: data/raw/HD<year>.zip, data/raw/ipeds_cc.json (2-year / associate-dominant institutions)
"""
import argparse, csv, io, json, sys, urllib.request, zipfile, datetime, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
# Carnegie 2021 Basic: 1-14 = Associate's colleges / special-focus two-year; 23 = Bacc/Assoc mixed
CC_CARNEGIE = set(range(1, 15)) | {23}

def carnegie_basic(r):
    try: return int(r.get("C21BASIC") or -9)
    except ValueError: return -9

def fetch(name):
    url = f"https://nces.ed.gov/ipeds/datacenter/data/{name}.zip"
    dest = RAW / f"{name}.zip"
    if not dest.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "naaic-refresh/1.0"})
        dest.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    return url, dest

def csv_rows(z, name):
    """Rows of one CSV inside an IPEDS zip, with upper-case column names and stripped values."""
    for r in csv.DictReader(io.TextIOWrapper(z.open(name), encoding="latin-1")):
        yield {k.strip().lstrip("\ufeff").lstrip("ï»¿").upper(): (v or "").strip() for k, v in r.items()}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--year", type=int, default=2024)
    a = ap.parse_args(); RAW.mkdir(parents=True, exist_ok=True)
    for y in (a.year, a.year - 1):
        try: url, dest = fetch(f"HD{y}"); break
        except Exception as e: print(f"HD{y} failed: {e}", file=sys.stderr)
    else: sys.exit("IPEDS download failed")
    z = zipfile.ZipFile(dest); name = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
    out = []
    for r in csv_rows(z, name):
        carn = carnegie_basic(r)
        level2 = r.get("ICLEVEL") == "2"
        if not (level2 or carn in CC_CARNEGIE): continue
        if r.get("CYACTIVE") not in ("1", ""): continue
        try: lat, lon = float(r["LATITUDE"]), float(r["LONGITUD"])
        except (KeyError, ValueError): continue
        out.append({"unitid": r["UNITID"], "name": r["INSTNM"], "alias": r.get("IALIAS", ""),
                    "city": r["CITY"], "state": r["STABBR"], "lat": lat, "lon": lon,
                    "web": r.get("WEBADDR", ""), "carnegie2021": carn, "iclevel": r.get("ICLEVEL"),
                    "control": r.get("CONTROL"), "source_url": url,
                    "as_of": datetime.date.today().isoformat()})
    (RAW / "ipeds_cc.json").write_text(json.dumps(out, indent=0))
    print(f"IPEDS {name}: {len(out)} 2-year/associate-dominant institutions -> data/raw/ipeds_cc.json")

if __name__ == "__main__": main()
