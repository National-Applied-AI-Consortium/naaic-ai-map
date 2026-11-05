#!/usr/bin/env python3
"""NSF Award Search pull: AI-related awards to community colleges.
Usage: python3 scripts/refresh_grants_nsf.py [--since 2024-01-01]
Writes: data/raw/nsf_<date>.json (PI/PO personal fields stripped)
        data/candidates/nsf_grants_auto.json  auto-matched: unique IPEDS 2-yr match + AI term in title
        data/candidates/nsf_partnerships_auto.json  NSF collaborative awards linking >=2 matched colleges
        data/candidates/nsf_candidates.json  needs a closer look (fuzzy match / AI only in abstract)
"""
import argparse, datetime, re, time, urllib.parse, sys
from common import *
API = "https://api.nsf.gov/services/v1/awards.json"
FIELDS = "id,title,awardeeName,awardeeCity,awardeeStateCode,date,startDate,expDate,estimatedTotalAmt,fundsObligatedAmt,fundProgramName,program,abstractText,transType"
QUERIES = [
    {"keyword": '"artificial intelligence"', "fundProgramName": "ADVANCED TECHNOLOGICAL EDUCATION"},
    {"keyword": '"machine learning"', "fundProgramName": "ADVANCED TECHNOLOGICAL EDUCATION"},
    {"keyword": "artificial intelligence", "awardeeName": "College"},
    {"keyword": "artificial intelligence", "awardeeName": "Technical"},
]

def pull(q, since):
    out, off = [], 1
    while True:
        p = dict(q, dateStart=since.strftime("%m/%d/%Y"), rpp=25, offset=off, printFields=FIELDS)
        r = http_json(API + "?" + urllib.parse.urlencode(p))["response"]
        aw = r.get("award", []); out += aw
        if len(aw) < 25 or off > 2000: return out
        off += 25; time.sleep(0.3)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--since", default="2024-01-01")
    since = datetime.date.fromisoformat(ap.parse_args().since)
    _, idx = load_ipeds(); seen = {}
    for q in QUERIES:
        try:
            for a in pull(q, since): seen[a["id"]] = {k: v for k, v in a.items() if k not in PERSONAL}
            print("NSF query ok:", q, file=sys.stderr)
        except Exception as e: print("NSF query FAILED:", q, e, file=sys.stderr)
    dump(RAW / f"nsf_{TODAY}.json", list(seen.values()))
    grants, cands = [], []
    for a in seen.values():
        m = match(idx, a.get("awardeeName", ""), a.get("awardeeStateCode", ""))
        mm, dd, yy = a["date"].split("/"); date = f"{yy}-{mm}-{dd}"
        if date < since.isoformat(): continue
        url = f"https://www.nsf.gov/awardsearch/showAward?AWD_ID={a['id']}"
        rec = {"id": f"nsf-{a['id']}", "unitid": m["unitid"] if m else None,
               "recipient": a.get("awardeeName"), "state": a.get("awardeeStateCode"),
               "amount": int(float(a.get("estimatedTotalAmt") or a.get("fundsObligatedAmt") or 0)),
               "amount_note": "NSF estimated total award amount", "funder": "NSF",
               "program": a.get("fundProgramName") or "", "award_date": date,
               "title": a.get("title", ""), "purpose": a.get("title", ""),
               "source_url": url, "as_of": TODAY, "origin": "nsf_api"}
        ai_title = bool(AI_TITLE.search(a.get("title", "")))
        ai_any = ai_title or bool(AI_ANY.search(a.get("abstractText", "")))
        nm = a.get("awardeeName", "")
        cc_like = re.search(r"community|technical|junior|county college|state college", nm, re.I) and not re.search(r"universit", nm, re.I)
        if m and ai_title: grants.append(rec)
        elif (m and ai_any) or (cc_like and ai_any):
            rec["review_reason"] = ("AI only in abstract" if m else "no unique IPEDS 2-yr match")
            cands.append(rec)
    # collaborative awards -> partnerships (same normalized title, >=2 matched colleges)
    groups = {}
    for g in grants:  # only AI-titled, IPEDS-matched awards
        t = re.sub(r"^collaborative research:\s*", "", g["title"], flags=re.I).strip().lower()
        if g["title"].lower().startswith("collaborative"): groups.setdefault(t, []).append(g)
    parts = []
    for t, gs in groups.items():
        ids = sorted({g["unitid"] for g in gs})
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                parts.append({"id": f"nsfcollab-{ids[i]}-{ids[j]}", "a_unitid": ids[i], "b_unitid": ids[j],
                    "type": "NSF collaborative award", "title": gs[0]["title"],
                    "source_url": next(g["source_url"] for g in gs if g["unitid"] == ids[i]),
                    "source_url_b": next(g["source_url"] for g in gs if g["unitid"] == ids[j]),
                    "as_of": TODAY, "origin": "nsf_api"})
    dump(CAND / "nsf_grants_auto.json", sorted(grants, key=lambda g: g["award_date"], reverse=True))
    dump(CAND / "nsf_partnerships_auto.json", parts)
    dump(CAND / "nsf_candidates.json", cands)
    print(f"NSF: {len(seen)} awards pulled; {len(grants)} auto-accepted; {len(cands)} candidates; {len(parts)} collaborative partnerships")

if __name__ == "__main__": main()
