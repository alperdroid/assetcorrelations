"""Download, cache and parse the free data sources, then build monthly/daily panels.

Sources
-------
- Kenneth French Data Library: industry portfolios (value-weighted) and market factor + T-bill.
- FRED: DGS10 (daily 10y yield), CPIAUCNS (CPI, not seasonally adjusted -> never revised),
  GACDFSA066MSFRBPHI (Philadelphia Fed manufacturing activity), UNRATE.
- Gold: World Bank "Pink Sheet" monthly gold price via the datahub/GitHub mirror.
  NOTE: these are monthly AVERAGE prices, which smooth returns. For the final paper, place an
  end-of-month series (e.g. World Gold Council, free registration) in data/gold_override.csv
  with columns date,price and it will be used automatically.
"""
from __future__ import annotations

import io
import logging
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)

KF_BASE = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
KF_FILES = {
    "ind12": "12_Industry_Portfolios_CSV.zip",
    "ind17": "17_Industry_Portfolios_CSV.zip",
    "ff3_m": "F-F_Research_Data_Factors_CSV.zip",
    "ff3_d": "F-F_Research_Data_Factors_daily_CSV.zip",
}
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
FRED_SERIES = {"DGS10": "DGS10", "CPI": "CPIAUCNS", "PHILLY": "GACDFSA066MSFRBPHI", "UNRATE": "UNRATE"}
GOLD_URL = "https://raw.githubusercontent.com/datasets/gold-prices/main/data/monthly.csv"


# --------------------------------------------------------------------------- download
def _fetch(url: str, path: Path, refresh: bool) -> bytes:
    if path.exists() and not refresh:
        return path.read_bytes()
    import requests  # imported lazily so offline/synthetic runs don't need it
    log.info("Downloading %s", url)
    r = requests.get(url, timeout=120, headers={"User-Agent": "Mozilla/5.0 (regime-study)"})
    r.raise_for_status()
    path.write_bytes(r.content)
    return r.content


# --------------------------------------------------------------------------- parsers
def _is_num(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def parse_kf_csv(text: str) -> pd.DataFrame:
    """Parse the FIRST data block of a Ken French CSV.

    For industry files this is 'Average Value Weighted Returns -- Monthly'; for factor files it is
    the monthly (or daily) factor table. Returns decimals (French reports percent).
    """
    header, rows = None, []
    for line in text.splitlines():
        parts = [p.strip() for p in line.split(",")]
        while parts and parts[-1] == "":
            parts.pop()
        if header is None:
            if len(parts) > 1 and parts[0] == "" and not any(_is_num(p) for p in parts[1:]):
                header = parts[1:]
            continue
        if parts and re.fullmatch(r"\d{6}|\d{8}", parts[0]):
            rows.append(parts[: len(header) + 1])
        elif rows:
            break
    if header is None or not rows:
        raise ValueError("Could not find a data block in Ken French file")
    df = pd.DataFrame(rows, columns=["date"] + header)
    daily = len(df["date"].iloc[0]) == 8
    idx = pd.to_datetime(df["date"], format="%Y%m%d") if daily else pd.PeriodIndex(df["date"], freq="M")
    out = df.drop(columns="date").astype(float)
    out.index = idx
    out = out.replace([-99.99, -999.0], np.nan) / 100.0
    out.columns = [c.strip() for c in out.columns]
    return out


def _read_kf_zip(content: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        name = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
        text = z.read(name).decode("latin-1")
    return parse_kf_csv(text)


def parse_fred_csv(content: bytes) -> pd.Series:
    df = pd.read_csv(io.BytesIO(content), na_values=["."])
    s = pd.Series(pd.to_numeric(df.iloc[:, 1], errors="coerce").values,
                  index=pd.to_datetime(df.iloc[:, 0]), name=df.columns[1])
    return s.dropna()


def parse_gold_csv(content: bytes) -> pd.Series:
    df = pd.read_csv(io.BytesIO(content))
    df.columns = [c.lower() for c in df.columns]
    s = pd.Series(df["price"].astype(float).values,
                  index=pd.DatetimeIndex(pd.to_datetime(df["date"].astype(str))).to_period("M"), name="GOLD")
    return s.groupby(level=0).last()


# --------------------------------------------------------------------------- bonds
def par_bond_price(c, y, n):
    """Price (per 1 face) of a semiannual-coupon bond with annual coupon c, yield y, n years left."""
    c, y, n = np.asarray(c, float), np.asarray(y, float), np.asarray(n, float)
    h, m = y / 2.0, 2.0 * n
    disc = (1.0 + h) ** (-m)
    with np.errstate(divide="ignore", invalid="ignore"):
        annuity = np.where(np.abs(h) < 1e-12, m, (1.0 - disc) / h)
    return c / 2.0 * annuity + disc


def bond_returns_from_yields(y: pd.Series, dt: pd.Series | float, maturity: float = 10.0) -> pd.Series:
    """Constant-maturity total returns from yields (Swinkels 2019 method).

    Buy a par bond at last period's yield, hold for dt years, reprice at today's yield with
    maturity - dt remaining, and add coupon accrual.
    """
    y_prev = y.shift(1)
    price = par_bond_price(y_prev, y, maturity - np.asarray(dt))
    return pd.Series(price - 1.0 + y_prev.values * np.asarray(dt), index=y.index)


# --------------------------------------------------------------------------- panel
def _to_monthly_period(s: pd.Series, how: str = "last") -> pd.Series:
    g = s.groupby(s.index.to_period("M"))
    return g.last() if how == "last" else g.mean()


def load_raw(raw_dir: Path, industries: int = 12, refresh: bool = False, use_gold_override: bool = True) -> dict:
    raw_dir.mkdir(parents=True, exist_ok=True)
    ind_key = f"ind{industries}"
    raw = {}
    for key in (ind_key, "ff3_m", "ff3_d"):
        fn = KF_FILES[key]
        raw[key] = _read_kf_zip(_fetch(KF_BASE + fn, raw_dir / fn, refresh))
    for name, sid in FRED_SERIES.items():
        raw[name] = parse_fred_csv(_fetch(FRED_URL.format(sid), raw_dir / f"fred_{sid}.csv", refresh))
    override = raw_dir.parent / "gold_override.csv"
    if use_gold_override and override.exists():
        log.info("Using end-of-month gold override: %s", override)
        raw["GOLD"] = parse_gold_csv(override.read_bytes())
        raw["gold_source"] = "override (end-of-month)"
    else:
        raw["GOLD"] = parse_gold_csv(_fetch(GOLD_URL, raw_dir / "gold_monthly.csv", refresh))
        raw["gold_source"] = "World Bank monthly average (datahub mirror)"
    raw["ind_key"] = ind_key
    return raw


def build_panels(raw: dict) -> dict:
    """Return dict with monthly returns, daily returns and monthly macro data (PeriodIndex)."""
    ind = raw[raw["ind_key"]]
    ff_m, ff_d = raw["ff3_m"], raw["ff3_d"]

    # Treasury returns from daily DGS10
    y_d = raw["DGS10"] / 100.0
    dt_d = pd.Series(y_d.index, index=y_d.index).diff().dt.days / 365.25
    bond_d = bond_returns_from_yields(y_d, dt_d).dropna()
    y_m = _to_monthly_period(y_d)
    y_m = y_m.reindex(pd.period_range(y_m.index.min(), y_m.index.max(), freq="M")).ffill()
    bond_m = bond_returns_from_yields(y_m, 1.0 / 12.0)

    gold_m = raw["GOLD"]
    gold_m = gold_m.reindex(pd.period_range(gold_m.index.min(), gold_m.index.max(), freq="M")).ffill()

    rets = ind.copy()
    rets["MKT"] = ff_m["Mkt-RF"] + ff_m["RF"]
    rets["RF"] = ff_m["RF"]
    rets["UST10"] = bond_m
    rets["GOLD"] = gold_m.pct_change()
    rets = rets.dropna()

    daily = pd.DataFrame({"MKT": ff_d["Mkt-RF"] + ff_d["RF"], "UST10": bond_d}).dropna()

    macro = pd.DataFrame({
        "CPI": _to_monthly_period(raw["CPI"]),
        "PHILLY": _to_monthly_period(raw["PHILLY"]),
        "UNRATE": _to_monthly_period(raw["UNRATE"]),
        "Y10": y_m,
    })
    macro = macro.reindex(pd.period_range(macro.index.min(), macro.index.max(), freq="M"))
    return {"returns": rets, "daily": daily, "macro": macro,
            "industries": list(ind.columns), "gold_source": raw.get("gold_source", "")}
