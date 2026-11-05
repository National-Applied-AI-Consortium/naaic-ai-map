"""Shared helpers for the NAAIC map refresh scripts."""
import json, re, pathlib, datetime, urllib.request
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA, RAW, CAND = ROOT / "data", ROOT / "data" / "raw", ROOT / "data" / "candidates"
TODAY = datetime.date.today().isoformat()
AI_TITLE = re.compile(r"\b(A\.?I\.?|artificial intelligence|machine learning|deep learning|generative|GenAI|LLMs?|large language model)\b", re.I)
AI_ANY = re.compile(r"artificial intelligence|machine learning|\bAI\b|generative|deep learning", re.I)
# personal fields never stored (no PI/PO names, emails, phones)
PERSONAL = {"pi","piEmail","piFirstName","piLastName","piMiddeInitial","piId","pdPIName","coPDPI","poEmail","poName","poPhone","awardeePhone"}

import unicodedata
def norm(name, loose=False):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower().replace("&", " and ")
    s = re.sub(r"\bsaint\b", "st", s); s = re.sub(r"\bmount\b", "mt", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\b(the|inc|district|system office)\b", " ", s)
    if loose: s = re.sub(r"\b(county|community|branch|office|of technology|campus)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def load_ipeds():
    p = RAW / "ipeds_cc.json"
    if not p.exists(): raise SystemExit("run scripts/refresh_ipeds.py first")
    rows = json.loads(p.read_text()); idx = {}
    for r in rows:
        keys = {norm(r["name"])} | {norm(a) for a in re.split(r"[|,]", r.get("alias") or "") if len(a.strip()) > 5}
        keys |= {"~" + norm(k, True) for k in keys}
        for k in keys: idx.setdefault((k, r["state"]), []).append(r)
    return rows, idx

def match(idx, name, state):
    for key in (norm(name), "~" + norm(name, True)):
        hits = {h["unitid"]: h for h in idx.get((key, state), [])}
        if len(hits) == 1: return next(iter(hits.values()))
    return None

def http_json(url, data=None, timeout=60):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None,
          headers={"User-Agent": "naaic-refresh/1.0", "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())

def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(obj, indent=1, ensure_ascii=False))
