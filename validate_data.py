"""Validate the raw inputs and write results/data_validation.md plus charts in results/data_checks/.

    python validate_data.py            # uses cached files in data/raw (downloads anything missing)

Checks
------
1. Coverage: date range, observation count, missing values and internal gaps for every series.
2. Known annual returns: 10y Treasury 2022 (about -15% to -17%) and 2008 (about +20%),
   US market 2008 (about -36% to -37%). Plus range checks on every series.
3. Ken French parsing: the parsed block must be 'Average Value Weighted Returns -- Monthly'.
   Verified three ways: (a) exact match with that block and not the equal-weighted block,
   (b) compounded monthly returns reproduce the file's own value-weighted ANNUAL block,
   (c) a market-cap-weighted average of the parsed industries (weights from the file's
   'Number of Firms' x 'Average Firm Size' blocks) reproduces the Fama-French market return.
4. One chart per input series in results/data_checks/ for visual inspection.
A source that cannot be downloaded is reported as unavailable; nothing is filled in.
"""
from __future__ import annotations

import io
import re
import zipfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import data as D

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"
CHK = OUT / "data_checks"

INK, INK2, GRID, BLUE = "#0b0b0b", "#52514e", "#e6e5e0", "#2a78d6"

# (series, year, low, high, what the user / literature expects)
KNOWN = [
    ("UST10", 2022, -0.17, -0.15, "10y Treasury total return about -15% to -17%"),
    ("UST10", 2008, 0.18, 0.22, "10y Treasury total return about +20%"),
    ("MKT", 2008, -0.37, -0.36, "US market (Fama-French Mkt-RF + RF) about -36% to -37%"),
]
TOL = 0.02  # outside the band by less than this -> CHECK; more -> IMPLAUSIBLE

RANGES = {  # plausible bounds for levels / monthly returns
    "DGS10 (%)": (0.3, 16.5), "CPI": (20, 400), "PHILLY": (-80, 80), "UNRATE": (2.0, 15.5),
    "GOLD price": (30, 10000),
}


# --------------------------------------------------------------------------- loading
def kf_blocks(text: str) -> dict[str, pd.DataFrame]:
    """All data blocks of a Ken French CSV, keyed by their title line."""
    blocks, title, header, rows = {}, "first block", None, []

    def flush():
        if header and rows:
            df = pd.DataFrame(rows, columns=["date"] + header)
            idx = df.pop("date")
            out = df.astype(float).replace([-99.99, -999.0], np.nan)
            out.index = idx
            blocks.setdefault(title, out)

    for line in text.splitlines():
        parts = [p.strip() for p in line.split(",")]
        while parts and parts[-1] == "":
            parts.pop()
        if not parts:
            continue
        if len(parts) == 1 and not re.fullmatch(r"\d+", parts[0]):
            flush()
            title, header, rows = parts[0], None, []
        elif parts[0] == "" and len(parts) > 1:
            flush()
            header, rows = parts[1:], []
        elif header and re.fullmatch(r"\d{4}|\d{6}|\d{8}", parts[0]):
            rows.append(parts[: len(header) + 1])
    flush()
    return blocks


def kf_text(fn: str) -> str:
    content = D._fetch(D.KF_BASE + fn, RAW / fn, False)
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        name = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
        return z.read(name).decode("latin-1")


def load_all():
    RAW.mkdir(parents=True, exist_ok=True)
    got, errors, texts = {}, {}, {}
    for key, fn in D.KF_FILES.items():
        try:
            texts[key] = kf_text(fn)
            got[key] = D.parse_kf_csv(texts[key])
        except Exception as e:  # noqa: BLE001
            errors[f"Ken French {fn}"] = repr(e)
    for name, sid in D.FRED_SERIES.items():
        try:
            got[name] = D.parse_fred_csv(D._fetch(D.FRED_URL.format(sid), RAW / f"fred_{sid}.csv", False))
        except Exception as e:  # noqa: BLE001
            errors[f"FRED {sid}"] = f"{type(e).__name__}: {str(e)[:160]}"
    try:
        got["GOLD_WB"] = D.parse_gold_csv(D._fetch(D.GOLD_URL, RAW / "gold_monthly.csv", False))
    except Exception as e:  # noqa: BLE001
        errors["World Bank gold (datahub mirror)"] = repr(e)
    ov = ROOT / "data" / "gold_override.csv"
    if ov.exists():
        got["GOLD_EOM"] = D.parse_gold_csv(ov.read_bytes())
    return got, errors, texts


# --------------------------------------------------------------------------- helpers
def coverage(name: str, s: pd.Series | pd.DataFrame, freq: str) -> dict:
    df = s.to_frame() if isinstance(s, pd.Series) else s
    idx = df.index
    if freq == "M":
        pidx = idx if isinstance(idx, pd.PeriodIndex) else pd.DatetimeIndex(idx).to_period("M")
        full = pd.period_range(pidx.min(), pidx.max(), freq="M")
        gaps = full.difference(pidx)
        gap_txt = ", ".join(str(g) for g in gaps[:12]) + (" ..." if len(gaps) > 12 else "")
        n_gap = len(gaps)
    else:
        d = pd.DatetimeIndex(idx)
        diffs = pd.Series(d[1:] - d[:-1], index=d[1:])
        long = diffs[diffs > pd.Timedelta(days=5)]
        n_gap = len(long)
        gap_txt = ", ".join(f"{(a - b).date()}..{a.date()}" for a, b in zip(long.index[:6], long.values[:6]))
    return {"series": name, "freq": "monthly" if freq == "M" else "daily",
            "start": str(idx.min())[:10], "end": str(idx.max())[:10], "obs": len(df),
            "missing values": int(df.isna().sum().sum()),
            "missing months / gaps>5d": n_gap, "gap detail": gap_txt}


def annual(r: pd.Series) -> pd.Series:
    return (1 + r).groupby(r.index.year).prod() - 1


def verdict(v, lo, hi):
    if pd.isna(v):
        return "NOT AVAILABLE"
    if lo <= v <= hi:
        return "OK"
    return "CHECK (close)" if (lo - TOL) <= v <= (hi + TOL) else "IMPLAUSIBLE"


def md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join("" if (isinstance(v, float) and np.isnan(v)) else str(v)
                                       for v in row.values) + " |")
    return "\n".join(lines)


def pct(v, d=1):
    return "n/a" if pd.isna(v) else f"{v * 100:+.{d}f}%"


# --------------------------------------------------------------------------- charts
def _style(ax, title, ylabel=""):
    ax.set_title(title, loc="left", fontsize=11, color=INK)
    ax.set_ylabel(ylabel, color=INK2, fontsize=9)
    ax.grid(color=GRID, lw=0.6)
    ax.tick_params(colors=INK2, labelsize=8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(GRID)


def _x(idx):
    return idx.to_timestamp() if isinstance(idx, pd.PeriodIndex) else idx


def plot_line(s: pd.Series, title, ylabel, fn, log=False, zero=False):
    fig, ax = plt.subplots(figsize=(11, 3.6))
    ax.plot(_x(s.index), s.values, color=BLUE, lw=1.0)
    if log:
        ax.set_yscale("log")
    if zero:
        ax.axhline(0, color=INK2, lw=0.6)
    _style(ax, title, ylabel)
    fig.tight_layout()
    fig.savefig(CHK / fn, dpi=110)
    plt.close(fig)


def plot_small_multiples(df: pd.DataFrame, title, fn, ncol=4):
    """Cumulative growth of $1 (log scale) for each column, one panel each (no colour legend)."""
    n = df.shape[1]
    nrow = int(np.ceil(n / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(3.2 * ncol, 2.2 * nrow), sharex=True, sharey=True)
    wealth = (1 + df.fillna(0)).cumprod()
    for ax, c in zip(axes.flat, df.columns):
        ax.plot(_x(wealth.index), wealth[c].values, color=BLUE, lw=0.9)
        ax.set_yscale("log")
        _style(ax, c)
    for ax in list(axes.flat)[n:]:
        ax.axis("off")
    fig.suptitle(title, x=0.01, ha="left", fontsize=12, color=INK)
    fig.tight_layout()
    fig.savefig(CHK / fn, dpi=110)
    plt.close(fig)


# --------------------------------------------------------------------------- main
def main():
    CHK.mkdir(parents=True, exist_ok=True)
    got, errors, texts = load_all()
    md = ["# Data validation", "",
          f"Generated by `validate_data.py` from the files in `data/raw/` "
          f"(run date {pd.Timestamp.today().date()}).", ""]

    # ---- derived series
    derived = {}
    if "ff3_m" in got:
        derived["MKT"] = got["ff3_m"]["Mkt-RF"] + got["ff3_m"]["RF"]
        derived["RF"] = got["ff3_m"]["RF"]
    if "DGS10" in got:
        y_d = got["DGS10"] / 100
        y_m = y_d.groupby(y_d.index.to_period("M")).last()
        y_m = y_m.reindex(pd.period_range(y_m.index.min(), y_m.index.max(), freq="M")).ffill()
        derived["UST10"] = D.bond_returns_from_yields(y_m, 1 / 12).dropna()

    # ---- 1. availability
    md += ["## 1. Download status", ""]
    if errors:
        md += ["**Some sources could not be downloaded. They are NOT filled in or substituted.**", ""]
        md += [f"- {k}: `{v}`" for k, v in errors.items()]
    else:
        md += ["All sources downloaded."]
    md += [""]

    # ---- 2. coverage
    rows = []
    for key in ("ind12", "ind17", "ff3_m"):
        if key in got:
            rows.append(coverage(f"Ken French {key}", got[key], "M"))
    if "ff3_d" in got:
        rows.append(coverage("Ken French ff3_d (daily)", got["ff3_d"], "D"))
    for k in ("DGS10",):
        if k in got:
            rows.append(coverage(f"FRED {D.FRED_SERIES[k]} (daily)", got[k], "D"))
    for k in ("CPI", "PHILLY", "UNRATE"):
        if k in got:
            rows.append(coverage(f"FRED {D.FRED_SERIES[k]}", got[k], "M"))
    if "GOLD_WB" in got:
        rows.append(coverage("Gold, World Bank monthly average", got["GOLD_WB"], "M"))
    if "GOLD_EOM" in got:
        rows.append(coverage("Gold, month-end override", got["GOLD_EOM"], "M"))
    md += ["## 2. Coverage, observations and missing values", "",
           "Missing values = NaN / '.' entries inside the file (FRED '.' rows are dropped on parse and "
           "therefore show up as missing months or gaps). Daily gaps > 5 calendar days are listed.", "",
           md_table(pd.DataFrame(rows)), ""]
    if "FRED DGS10" not in errors:
        raw_fred = {}
        for k, sid in D.FRED_SERIES.items():
            f = RAW / f"fred_{sid}.csv"
            if f.exists():
                df = pd.read_csv(f)
                raw_fred[sid] = int((df.iloc[:, 1].astype(str).str.strip() == ".").sum())
        if raw_fred:
            md += ["FRED rows marked '.' (no value) in the raw files: "
                   + ", ".join(f"{k}: {v}" for k, v in raw_fred.items()), ""]

    # ---- 3. known annual returns
    md += ["## 3. Known annual returns", "",
           f"Verdict: OK = inside the expected band; CHECK = within {TOL:.0%} of the band; "
           "IMPLAUSIBLE = further out; NOT AVAILABLE = source could not be downloaded.", ""]
    krows = []
    for ser, yr, lo, hi, note in KNOWN:
        v = annual(derived[ser].loc[str(yr)]).iloc[0] if ser in derived and str(yr) in derived[ser].index.astype(str).str[:4] else np.nan
        krows.append({"series": ser, "year": yr, "computed": pct(v), "expected": f"{lo:.0%} to {hi:.0%}",
                      "verdict": verdict(v, lo, hi), "note": note})
    md += [md_table(pd.DataFrame(krows)), ""]
    if "UST10" in derived:
        a = annual(derived["UST10"])
        md += ["Selected 10y Treasury annual total returns (Swinkels par-bond method, month-end DGS10): "
               + ", ".join(f"{y}: {pct(a.get(y))}" for y in (1994, 1999, 2008, 2009, 2013, 2020, 2021, 2022, 2023, 2024, 2025)
                           if y in a.index), ""]
    if "MKT" in derived:
        a = annual(derived["MKT"])
        md += ["Selected US market annual returns: "
               + ", ".join(f"{y}: {pct(a.get(y))}" for y in (1974, 1987, 2001, 2002, 2008, 2020, 2022, 2025) if y in a.index), ""]
    if "GOLD_WB" in got:
        g = got["GOLD_WB"].loc["1971":].pct_change().dropna()
        a = annual(g)
        md += ["Gold (World Bank monthly average) annual returns: "
               + ", ".join(f"{y}: {pct(a.get(y))}" for y in (1974, 1980, 2008, 2013, 2022, 2024, 2025) if y in a.index),
               "", "Note: annual returns from monthly averages compare December average to December average, "
               "not year-end to year-end, so they differ from published calendar-year gold returns.", ""]

    # ---- 4. range / outlier checks
    flags = []
    def rng(label, s, lo, hi):
        bad = s[(s < lo) | (s > hi)].dropna()
        flags.append({"series": label, "min": f"{s.min():.4g}", "max": f"{s.max():.4g}",
                      "plausible range": f"{lo} to {hi}", "outside": len(bad),
                      "examples": ", ".join(f"{str(i)[:10]}={v:.4g}" for i, v in bad.head(5).items())})
    if "DGS10" in got:
        rng("DGS10 (%)", got["DGS10"], *RANGES["DGS10 (%)"])
    for k in ("CPI", "PHILLY", "UNRATE"):
        if k in got:
            rng(k, got[k].loc["1960":], *RANGES[k])
    if "GOLD_WB" in got:
        rng("GOLD price", got["GOLD_WB"].loc["1960":], *RANGES["GOLD price"])
    mret = {}
    for k in ("ind12", "ind17"):
        if k in got:
            for c in got[k].columns:
                mret[f"{k}:{c}"] = got[k][c].loc["1972":]
    for k in ("MKT", "UST10"):
        if k in derived:
            mret[k] = derived[k].loc["1972":]
    if "GOLD_WB" in got:
        mret["GOLD (WB avg)"] = got["GOLD_WB"].loc["1971":].pct_change().loc["1972":]
    if "GOLD_EOM" in got:
        mret["GOLD (month-end)"] = got["GOLD_EOM"].pct_change().loc["1972":]
    for k, s in mret.items():
        bad = s[s.abs() > 0.35].dropna()
        if len(bad):
            flags.append({"series": f"{k} monthly return", "min": f"{s.min():.3f}", "max": f"{s.max():.3f}",
                          "plausible range": "|r| <= 35%", "outside": len(bad),
                          "examples": ", ".join(f"{i}={v:+.1%}" for i, v in bad.head(5).items())})
    md += ["## 4. Range and outlier checks (1960/1972 onward)", "",
           md_table(pd.DataFrame(flags)) if flags else "No series available.", "",
           "Monthly returns are listed only when some month exceeds |35%|; extreme months are not "
           "necessarily errors (for example Durbl in 2020, gold in 1980) but should be inspected on the charts.", ""]

    # ---- 5. Ken French value-weighted check
    md += ["## 5. Ken French: value-weighted monthly block?", ""]
    for key in ("ind12", "ind17"):
        if key not in texts:
            continue
        b = kf_blocks(texts[key])
        parsed = got[key] * 100
        parsed.index = parsed.index.strftime("%Y%m")
        vw_t = [t for t in b if "value weighted returns" in t.lower() and "monthly" in t.lower()]
        ew_t = [t for t in b if "equal weighted returns" in t.lower() and "monthly" in t.lower()]
        vwa_t = [t for t in b if "value weighted returns" in t.lower() and "annual" in t.lower()]
        nf_t = [t for t in b if "number of firms" in t.lower()]
        sz_t = [t for t in b if "average firm size" in t.lower()]
        res = [f"**{key}** - blocks found: " + "; ".join(f"'{t}'" for t in b), ""]
        vw, ew = b[vw_t[0]], b[ew_t[0]]
        same_vw = parsed.shape == vw.shape and np.allclose(parsed.values, vw.values, equal_nan=True, atol=1e-9)
        diff_ew = float(np.nanmax(np.abs(parsed.values - ew.reindex(parsed.index).values)))
        res += [f"- (a) Parsed data equal to '{vw_t[0]}': **{same_vw}**. "
                f"Largest absolute difference from '{ew_t[0]}': {diff_ew:.2f} pp (so not the EW block).",
                f"- First rows of the parsed block (percent): "
                + "; ".join(f"{i}: {parsed.columns[0]}={parsed.iloc[j, 0]:.2f}, {parsed.columns[-1]}={parsed.iloc[j, -1]:.2f}"
                            for j, i in enumerate(parsed.index[:2])) + "."]
        if vwa_t:
            ann_file = b[vwa_t[0]]
            comp = ((1 + got[key]).groupby(got[key].index.year).prod() - 1) * 100
            comp.index = comp.index.astype(str)
            common = comp.index.intersection(ann_file.index)
            common = [y for y in common if (got[key].index.year == int(y)).sum() == 12]
            err = (comp.loc[common] - ann_file.loc[common]).abs()
            ew_ann = b.get([t for t in b if "equal weighted returns" in t.lower() and "annual" in t.lower()][0])
            err_ew = (comp.loc[common] - ew_ann.loc[common]).abs()
            res += [f"- (b) Compounded parsed monthly returns vs the file's '{vwa_t[0]}' block, {len(common)} years: "
                    f"median abs diff {err.stack().median():.3f} pp, max {err.stack().max():.3f} pp "
                    f"(vs the EW annual block: median {err_ew.stack().median():.2f} pp). "
                    f"Example 2008: " + ", ".join(f"{c} {comp.loc['2008', c]:.1f}% vs file {ann_file.loc['2008', c]:.1f}%"
                                                  for c in list(comp.columns)[:3]) + "."]
        if nf_t and sz_t and "MKT" in derived:
            capw = b[nf_t[0]] * b[sz_t[0]]
            mkt = derived["MKT"].copy() * 100
            mkt.index = mkt.index.strftime("%Y%m")
            out = []
            for lab, ret in (("value-weighted (parsed)", parsed), ("equal-weighted block", ew.reindex(parsed.index))):
                for lag_lab, w in (("same-month caps", capw), ("prior-month caps", capw.shift(1))):
                    w = w.reindex(ret.index)
                    rec = (ret * w).sum(axis=1) / w.where(ret.notna()).sum(axis=1)
                    cmp = pd.concat([rec, mkt], axis=1, keys=["rec", "mkt"]).loc["197201":].dropna()
                    te = (cmp["rec"] - cmp["mkt"])
                    out.append(f"{lab}, {lag_lab}: corr {cmp['rec'].corr(cmp['mkt']):.4f}, "
                               f"mean abs diff {te.abs().mean():.3f} pp/month")
            res += ["- (c) Cap-weighted average of industries vs Fama-French market return, 1972 onward: "
                    + "; ".join(out) + ". Value-weighted should track the market almost exactly; "
                    "equal-weighted should not."]
        md += res + [""]

    # ---- 6. gold source comparison
    md += ["## 6. Gold series", ""]
    if "GOLD_EOM" in got and "GOLD_WB" in got:
        a = got["GOLD_WB"].pct_change().loc["1972":]
        e = got["GOLD_EOM"].pct_change().loc["1972":]
        j = pd.concat([a, e], axis=1, keys=["avg", "eom"]).dropna()
        ac = lambda x: x.autocorr(1)
        md += [f"World Bank monthly-average vs month-end override, {j.index[0]} to {j.index[-1]}: "
               f"ann. vol {j['avg'].std() * np.sqrt(12):.1%} vs {j['eom'].std() * np.sqrt(12):.1%}; "
               f"first-order autocorrelation {ac(j['avg']):.2f} vs {ac(j['eom']):.2f}; "
               f"correlation {j['avg'].corr(j['eom']):.2f}. Averaging lowers volatility and induces "
               "positive autocorrelation (Working 1960).", ""]
    elif "GOLD_WB" in got:
        a = got["GOLD_WB"].pct_change().loc["1972":]
        md += [f"Only the World Bank monthly-AVERAGE series is available (no data/gold_override.csv). "
               f"Ann. vol 1972 onward {a.std() * np.sqrt(12):.1%}, first-order autocorrelation "
               f"{a.autocorr(1):.2f}. Positive autocorrelation is the expected artefact of averaging.", ""]

    # ---- 7. charts
    charts = []
    for key in ("ind12", "ind17"):
        if key in got:
            plot_small_multiples(got[key].loc["1972":], f"Ken French {key[3:]} industries (VW): growth of $1 since 1972, log",
                                 f"kf_{key}.png")
            charts.append(f"kf_{key}.png")
    if "MKT" in derived:
        plot_line((1 + derived["MKT"].loc["1972":]).cumprod(), "US market (Mkt-RF + RF): growth of $1 since 1972", "log", "mkt.png", log=True)
        plot_line(derived["RF"].loc["1972":] * 1200, "1-month T-bill (Fama-French RF), annualised", "% p.a.", "rf.png")
        charts += ["mkt.png", "rf.png"]
    if "ff3_d" in got:
        d = got["ff3_d"]["Mkt-RF"] + got["ff3_d"]["RF"]
        plot_line(d.loc["1972":], "US market daily return", "return", "mkt_daily.png", zero=True)
        charts.append("mkt_daily.png")
    if "DGS10" in got:
        plot_line(got["DGS10"].loc["1962":], "FRED DGS10: 10y Treasury yield (daily)", "%", "dgs10.png")
        plot_line((1 + derived["UST10"].loc["1972":]).cumprod(), "10y Treasury total return index (from DGS10)", "log",
                  "ust10.png", log=True)
        charts += ["dgs10.png", "ust10.png"]
    if "CPI" in got:
        plot_line(got["CPI"].pct_change(12).loc["1960":] * 100, "FRED CPIAUCNS: CPI YoY", "%", "cpi_yoy.png", zero=True)
        charts.append("cpi_yoy.png")
    if "PHILLY" in got:
        plot_line(got["PHILLY"], "FRED GACDFSA066MSFRBPHI: Philly Fed current activity", "diffusion index", "philly.png", zero=True)
        charts.append("philly.png")
    if "UNRATE" in got:
        plot_line(got["UNRATE"].loc["1960":], "FRED UNRATE: unemployment rate", "%", "unrate.png")
        charts.append("unrate.png")
    if "GOLD_WB" in got:
        plot_line(got["GOLD_WB"].loc["1968":], "Gold, World Bank monthly average (USD/oz)", "log", "gold_wb.png", log=True)
        plot_line(got["GOLD_WB"].pct_change().loc["1972":], "Gold monthly return (World Bank average)", "return", "gold_wb_ret.png", zero=True)
        charts += ["gold_wb.png", "gold_wb_ret.png"]
    if "GOLD_EOM" in got:
        plot_line(got["GOLD_EOM"], "Gold, month-end override (USD/oz)", "log", "gold_eom.png", log=True)
        charts.append("gold_eom.png")
    md += ["## 7. Charts (results/data_checks/)", "", ", ".join(f"`{c}`" for c in charts), ""]

    (OUT / "data_validation.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
