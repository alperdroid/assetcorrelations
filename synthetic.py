"""Write SYNTHETIC raw files in the same formats as the real sources (Ken French zips, FRED CSVs,
gold CSV). Used only to test the pipeline end-to-end without internet. Results are meaningless."""
from __future__ import annotations

import io
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from data import FRED_SERIES, KF_FILES

IND12 = ["NoDur", "Durbl", "Manuf", "Enrgy", "Chems", "BusEq", "Telcm", "Utils", "Shops", "Hlth", "Money", "Other"]
END = "2026-09"


def _kf_text(df: pd.DataFrame, title: str, daily=False) -> str:
    buf = io.StringIO()
    buf.write("This file was created synthetically for testing.\n\n")
    buf.write(f"  {title}\n")
    buf.write("," + ",".join(df.columns) + "\n")
    fmt = "%Y%m%d" if daily else None
    for idx, row in df.iterrows():
        d = idx.strftime(fmt) if daily else idx.strftime("%Y%m")
        buf.write(d + "," + ",".join(f"{v:8.2f}" for v in row.values) + "\n")
    buf.write("\n  Annual Factors: January-December \n," + ",".join(df.columns) + "\n")
    buf.write("1927," + ",".join("   1.00" for _ in df.columns) + "\n")
    return buf.getvalue()


def _zip(path: Path, name: str, text: str):
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(name, text)


def write_synthetic(raw_dir: Path, seed: int = 7):
    rng = np.random.default_rng(seed)
    raw_dir.mkdir(parents=True, exist_ok=True)

    m_idx = pd.period_range("1926-07", END, freq="M")
    n = len(m_idx)
    mkt = rng.normal(0.007, 0.045, n)
    betas = rng.uniform(0.6, 1.4, len(IND12))
    ind = np.outer(mkt, betas) + rng.normal(0, 0.025, (n, len(IND12)))
    rf = np.full(n, 0.003)
    ind_df = pd.DataFrame(ind * 100, index=m_idx, columns=IND12)
    _zip(raw_dir / KF_FILES["ind12"], "12_Industry_Portfolios.csv",
         _kf_text(ind_df, "Average Value Weighted Returns -- Monthly"))
    ff_m = pd.DataFrame({"Mkt-RF": (mkt - rf) * 100, "SMB": 0.0, "HML": 0.0, "RF": rf * 100}, index=m_idx)
    _zip(raw_dir / KF_FILES["ff3_m"], "F-F_Research_Data_Factors.csv", _kf_text(ff_m, ""))

    d_idx = pd.bdate_range("1962-01-02", pd.Period(END, "M").end_time.normalize())
    nd = len(d_idx)
    mkt_d = rng.normal(0.0003, 0.01, nd)
    ff_d = pd.DataFrame({"Mkt-RF": mkt_d * 100, "SMB": 0.0, "HML": 0.0, "RF": 0.01}, index=d_idx)
    _zip(raw_dir / KF_FILES["ff3_d"], "F-F_Research_Data_Factors_daily.csv", _kf_text(ff_d, "", daily=True))

    # 10y yield random walk, mean-reverting, in percent; some missing days like FRED
    y = np.empty(nd)
    y[0] = 4.0
    for i in range(1, nd):
        y[i] = max(0.3, y[i - 1] + 0.002 * (5.5 - y[i - 1]) + rng.normal(0, 0.06))
    dgs = pd.Series(y.round(2), index=d_idx).astype(object)
    dgs.iloc[rng.choice(nd, 200, replace=False)] = "."
    pd.DataFrame({"observation_date": d_idx.strftime("%Y-%m-%d"), "DGS10": dgs.values}).to_csv(
        raw_dir / f"fred_{FRED_SERIES['DGS10']}.csv", index=False)

    def monthly_fred(sid, start, values):
        idx = pd.period_range(start, END, freq="M").to_timestamp()
        pd.DataFrame({"observation_date": idx.strftime("%Y-%m-%d"), sid: values(len(idx))}).to_csv(
            raw_dir / f"fred_{sid}.csv", index=False)

    monthly_fred(FRED_SERIES["CPI"], "1947-01", lambda k: (22 * np.exp(np.cumsum(rng.normal(0.003, 0.004, k)))).round(3))
    monthly_fred(FRED_SERIES["PHILLY"], "1968-05", lambda k: (np.convolve(rng.normal(0, 15, k), np.ones(6) / 6, "same")).round(1))
    monthly_fred(FRED_SERIES["UNRATE"], "1948-01", lambda k: np.clip(5.5 + np.cumsum(rng.normal(0, 0.15, k)), 3, 11).round(1))

    g_idx = pd.period_range("1960-01", END, freq="M")
    gold = 35 * np.exp(np.cumsum(rng.normal(0.005, 0.05, len(g_idx))))
    pd.DataFrame({"Date": g_idx.strftime("%Y-%m"), "Price": gold.round(3)}).to_csv(raw_dir / "gold_monthly.csv", index=False)
