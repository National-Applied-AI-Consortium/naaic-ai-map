#!/usr/bin/env python3
"""Check that every source link in data/naaic-map.json still answers. Changes nothing.

Usage: python3 scripts/check_links.py [--out data/candidates/link_check.json]
Some college sites block scripted requests; treat a 403 as "open it in a browser", not as dead.
"""
import argparse, json, pathlib, urllib.request, concurrent.futures as cf

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def urls(D):
    seen = {}
    for c in D["inst"]:
        for p in c["programs"]:
            seen.setdefault(p["source_url"], f"program {c['id']} {p['name']}")
    for g in D["grants"]:
        seen.setdefault(g["source_url"], f"grant {g['id']}")
    for l in D["lines"]:
        for it in l["items"]:
            seen.setdefault(it["source_url"], f"line {l['a']}-{l['b']}")
    for e in D["featured"]:
        seen.setdefault(e["source_url"], f"featured {e['outlet']}")
    return seen


def probe(u):
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return f"error: {type(e).__name__}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "data" / "candidates" / "link_check.json"))
    a = ap.parse_args()
    D = json.loads((ROOT / "data" / "naaic-map.json").read_text(encoding="utf-8"))
    todo = urls(D)
    with cf.ThreadPoolExecutor(8) as ex:
        res = dict(zip(todo, ex.map(probe, todo)))
    out = [{"url": u, "used_by": todo[u], "status": s} for u, s in res.items()]
    bad = [o for o in out if not (isinstance(o["status"], int) and o["status"] < 400)]
    p = pathlib.Path(a.out); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    for o in bad:
        print(o["status"], o["url"], "(" + o["used_by"] + ")")
    print(f"{len(out)} links checked, {len(bad)} need a look; full results in {p}")


if __name__ == "__main__":
    main()
