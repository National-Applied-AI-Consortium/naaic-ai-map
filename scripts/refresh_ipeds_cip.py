#!/usr/bin/env python3
"""IPEDS CIP 11.0102 rebuild: recomputes the completions shown in the growth table from the NCES completions files,
and the community college figures behind them. Public domain (U.S. Dept. of Education, NCES). No AI calls.
Usage: python3 scripts/refresh_ipeds_cip.py
Downloads to data/raw/ and reuses what is there; as_of is the date a file was downloaded, so delete
data/raw/C20*_A.zip to check NCES again.
Outputs: data/ipeds_cip110102_by_year.csv, data/ipeds_cip110102_by_award_level.csv,
data/ipeds_cip110102_community_colleges.csv
The published figure counts first majors at all institutions and all award levels. See docs/ipeds-cip-11.0102.md.
"""
import csv, datetime, zipfile
from refresh_ipeds import CC_CARNEGIE, RAW, ROOT, carnegie_basic, csv_rows, fetch

CIP = "11.0102"
YEARS = range(2019, 2025)  # the C<year> file covers the award year ending in <year>
DIRECTORY_FILE = "HD2024"  # one directory for every year: C21BASIC is not in HD2019 or HD2020, and a college stays in one group
# AWLEVEL labels from the C2024_A data dictionary. Totals (12-15) are left out so that a total row stops the run.
AWARD_LEVELS = {
    1: "Certificate of less than 1 year",
    2: "Certificate of at least 1 but less than 2 years",
    3: "Associate's degree",
    4: "Certificate of at least 2 but less than 4 years",
    5: "Bachelor's degree",
    6: "Postbaccalaureate certificate",
    7: "Master's degree",
    8: "Post-master's certificate",
    17: "Doctor's degree: research/scholarship",
    18: "Doctor's degree: professional practice",
    19: "Doctor's degree: other",
    20: "Certificate of less than 12 weeks",
    21: "Certificate of at least 12 weeks but less than 1 year",
}


def is_community_college(inst):
    """Public, and two-year or Carnegie associate-dominant, so colleges that also grant bachelor's degrees still count."""
    return inst["CONTROL"] == "1" and (inst["ICLEVEL"] == "2" or carnegie_basic(inst) in CC_CARNEGIE)


def tally(files, directory):
    revised = [n for n in files if n.lower().endswith("_rv.csv")]
    name = revised[0] if revised else next(iter(files))
    rows = [r for r in files[name] if r["CIPCODE"] == CIP]
    first = [r for r in rows if r["MAJORNUM"] == "1"]
    second = [r for r in rows if r["MAJORNUM"] == "2"]
    reporting = {r["UNITID"] for r in rows}
    cc = {u for u in reporting if is_community_college(directory[u])}
    levels = {}
    for r in first:
        level, n = int(r["AWLEVEL"]), int(r["CTOTALT"])
        if level not in AWARD_LEVELS: raise KeyError(f"unknown award level {level} for {r['UNITID']}")
        all_count, cc_count = levels.get(level, (0, 0))
        levels[level] = (all_count + n, cc_count + (n if r["UNITID"] in cc else 0))
    return {
        "release": "final (revised)" if revised else "provisional",
        "institutions_reporting": len(reporting),
        "institutions_with_completers": len({r["UNITID"] for r in first if int(r["CTOTALT"]) > 0}),
        "two_year_institutions_reporting": sum(directory[u]["ICLEVEL"] == "2" for u in reporting),
        "texas_institutions_reporting": sum(directory[u]["STABBR"] == "TX" for u in reporting),
        "total_completers": sum(int(r["CTOTALT"]) for r in first),
        "second_major_completers": sum(int(r["CTOTALT"]) for r in second),
        "community_college_institutions_reporting": len(cc),
        "community_college_institutions_with_completers": len({r["UNITID"] for r in first if r["UNITID"] in cc and int(r["CTOTALT"]) > 0}),
        "community_college_completers": sum(int(r["CTOTALT"]) for r in first if r["UNITID"] in cc),
        "levels": dict(sorted(levels.items())),
        "colleges": [(r["UNITID"], int(r["AWLEVEL"]), int(r["CTOTALT"])) for r in first if r["UNITID"] in cc],
    }


def write_csv(name, rows):
    with open(ROOT / "data" / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote data/{name} ({len(rows)} rows)")


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    directory_url, directory_zip = fetch(DIRECTORY_FILE)
    z = zipfile.ZipFile(directory_zip)
    directory = {r["UNITID"]: r for r in csv_rows(z, z.namelist()[0])}
    by_year, by_level, colleges = [], [], []
    for year in YEARS:
        ipeds_file = f"C{year}_A"
        url, dest = fetch(ipeds_file)
        z = zipfile.ZipFile(dest)
        counts = tally({n: csv_rows(z, n) for n in z.namelist()}, directory)
        award_year = f"{year - 1}-{year % 100:02d}"
        year_columns = {"ipeds_file": ipeds_file, "award_year": award_year, "award_year_end": year}
        source_columns = {"source_url": url, "as_of": datetime.date.fromtimestamp(dest.stat().st_mtime).isoformat()}
        by_year.append({**year_columns, **{k: v for k, v in counts.items() if k not in ("levels", "colleges")}, **source_columns})
        for level, (all_count, cc_count) in counts["levels"].items():
            by_level.append({**year_columns, "awlevel": level, "award_level": AWARD_LEVELS[level], "all_institutions_completers": all_count,
                             "community_college_completers": cc_count, **source_columns})
        for unitid, level, n in sorted(counts["colleges"], key=lambda c: (directory[c[0]]["INSTNM"], c[1])):
            d = directory[unitid]
            colleges.append({**year_columns, "unitid": unitid, "institution": d["INSTNM"], "state": d["STABBR"], "iclevel": d["ICLEVEL"],
                             "carnegie_2021_basic": d["C21BASIC"], "awlevel": level, "award_level": AWARD_LEVELS[level], "completers": n,
                             "directory_source_url": directory_url, **source_columns})
    write_csv("ipeds_cip110102_by_year.csv", by_year)
    write_csv("ipeds_cip110102_by_award_level.csv", by_level)
    write_csv("ipeds_cip110102_community_colleges.csv", colleges)
    for r in by_year:
        print(f"{r['award_year']} ({r['release']}): {r['total_completers']} completers, {r['community_college_completers']} at community colleges")


if __name__ == "__main__": main()
