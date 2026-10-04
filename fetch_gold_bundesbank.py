"""Build data/gold_override.csv (month-end gold, USD/oz) from the Bundesbank SDMX REST API.

    python fetch_gold_bundesbank.py              # discover, choose, download, save
    python fetch_gold_bundesbank.py --list       # only list the candidate series
    python fetch_gold_bundesbank.py --key D.XAU.USD.EA.xx.yyy   # force a specific series key

Dataflow BBEX3, key structure FREQ.CURRENCY.PARTNER_CURRENCY.SERIES_TYPE.RATE_TYPE.SUFFIX.
Gold = CURRENCY XAU, PARTNER USD, SERIES_TYPE EA. The exact series is DISCOVERED by querying the
API (wildcard key, detail=nodata); nothing is hard-coded.

Choice rule (fixed in advance):
  1. Prefer a DAILY series (FREQ = D). Month-end value = last available daily price in the month.
  2. Otherwise a MONTHLY series whose title says end-of-month. Never a monthly average.
  3. If more than one series qualifies and the titles do not single out a London USD price,
     stop and list them; rerun with --key.
The chosen key, its title, the exact URL and the retrieval date are written to
data/gold_override_source.json (and must be copied into DEVIATIONS.md).
"""
from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent
BASE = "https://api.statistiken.bundesbank.de/rest/data/BBEX3/"
XML = "application/vnd.sdmx.genericdata+xml;version=2.1"
HEAD = {"Accept": XML}


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _values(elem, container: str) -> dict:
    """Generic SDMX-ML: <container><Value id=.. value=../></container>."""
    out = {}
    for c in elem.iter():
        if _local(c.tag) == container:
            for v in c:
                if _local(v.tag) == "Value":
                    out[v.get("id")] = v.get("value")
    return out


def parse_series(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    out = []
    for s in root.iter():
        if _local(s.tag) != "Series":
            continue
        key = _values(s, "SeriesKey")
        attrs = _values(s, "Attributes")
        if not key:  # structure-specific format: dimensions/attributes are XML attributes
            key = {k: v for k, v in s.attrib.items()}
            attrs = {}
        obs = []
        for o in s:
            if _local(o.tag) != "Obs":
                continue
            per = val = None
            for c in o:
                if _local(c.tag) == "ObsDimension":
                    per = c.get("value")
                elif _local(c.tag) == "ObsValue":
                    val = c.get("value")
            if per is None:
                per, val = o.get("TIME_PERIOD"), o.get("OBS_VALUE")
            if per is not None and val not in (None, "", "NaN"):
                obs.append((per, float(val)))
        out.append({"key": key, "attrs": attrs, "obs": obs})
    return out


def key_string(key: dict) -> str:
    return ".".join(key.values())


def title(s: dict) -> str:
    a = s["attrs"]
    for k in ("BBK_TITLE_ENG", "TITLE_ENG", "BBK_TITLE", "TITLE", "TITLE_COMPL"):
        if a.get(k):
            return a[k]
    return " | ".join(f"{k}={v}" for k, v in a.items())[:300]


def discover() -> tuple[list[dict], str]:
    url = BASE + ".XAU.USD.EA..?detail=nodata"
    r = requests.get(url, headers=HEAD, timeout=120)
    if r.status_code == 404:  # the API answers 404 when no series matches the key
        return [], url
    r.raise_for_status()
    return parse_series(r.content), url


def choose(series: list[dict]) -> dict | None:
    def freq(s):
        return list(s["key"].values())[0]
    daily = [s for s in series if freq(s) == "D"]
    if len(daily) == 1:
        return daily[0]
    if len(daily) > 1:
        lon = [s for s in daily if "london" in title(s).lower() and "usd" in title(s).lower().replace("us dollar", "usd")]
        return lon[0] if len(lon) == 1 else None
    monthly = [s for s in series if freq(s) == "M"]
    eom = [s for s in monthly
           if any(w in title(s).lower() for w in ("end of month", "end-of-month", "month-end", "monatsende"))
           and not any(w in title(s).lower() for w in ("average", "durchschnitt", "mean"))]
    return eom[0] if len(eom) == 1 else None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--list", action="store_true")
    p.add_argument("--key", default=None)
    args = p.parse_args()

    try:
        series, disc_url = discover()
    except Exception as e:  # noqa: BLE001
        sys.exit(f"Bundesbank API not reachable or query failed: {e}\n"
                 "Continue with the World Bank monthly-average series (no override written).")
    print(f"Discovery query: {disc_url}\nFound {len(series)} series:")
    if not series and not args.key:
        sys.exit("No BBEX3 series matches CURRENCY=XAU, PARTNER=USD, SERIES_TYPE=EA. "
                 "Continue with the World Bank monthly-average series (no override written).")
    for s in series:
        print(f"  {key_string(s['key']):35s}  {title(s)}")
    if args.list:
        return

    if args.key:
        chosen_key = args.key
    else:
        ch = choose(series)
        if ch is None:
            sys.exit("No unique daily (or end-of-month) gold series; rerun with --key <series key>.")
        chosen_key = key_string(ch["key"])
    if chosen_key.split(".")[0] not in ("D", "M"):
        sys.exit(f"Unexpected frequency in {chosen_key}")
    meta = next((s for s in series if key_string(s["key"]) == chosen_key), None)
    ttl = title(meta) if meta else "(not in discovery list)"
    if chosen_key.startswith("M") and any(w in ttl.lower() for w in ("average", "durchschnitt")):
        sys.exit(f"Refusing monthly-average series {chosen_key}: {ttl}")

    data_url = BASE + chosen_key
    r = requests.get(data_url, headers=HEAD, timeout=300)
    r.raise_for_status()
    got = parse_series(r.content)
    if len(got) != 1 or not got[0]["obs"]:
        sys.exit(f"Unexpected response for {chosen_key}: {len(got)} series")
    s = pd.Series(dict(got[0]["obs"])).sort_index()
    s.index = pd.to_datetime(s.index)
    s = s[s > 0]
    # month-end = last available observation in each calendar month
    last = s.groupby(s.index.to_period("M")).tail(1)
    out = pd.DataFrame({"date": last.index.strftime("%Y-%m-%d"), "price": last.values})
    # drop the current, incomplete month
    if pd.Period(out["date"].iloc[-1], "M") >= pd.Period(date.today(), "M"):
        out = out.iloc[:-1]
    dest = ROOT / "data" / "gold_override.csv"
    out.to_csv(dest, index=False)
    info = {"series_key": f"BBEX3.{chosen_key}", "title": ttl, "data_url": data_url,
            "discovery_url": disc_url, "retrieved": str(date.today()),
            "frequency": "daily -> last obs per month" if chosen_key.startswith("D") else "monthly end-of-month",
            "first": out["date"].iloc[0], "last": out["date"].iloc[-1], "months": len(out)}
    (ROOT / "data" / "gold_override_source.json").write_text(json.dumps(info, indent=2))
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
