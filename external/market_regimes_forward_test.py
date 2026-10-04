"""Exploratory forward test of the regime labels saved in alperdroid/market-regimes.

    python external/market_regimes_forward_test.py /path/to/market-regimes/market_regimes

Question: does the regime label known at the close of day t (VIX rule, walk-forward HMM with
causal filtered states, GMM, ensemble) predict what SPY does over the NEXT 21 trading days
(t+1 .. t+21)? Non-overlapping 21-day windows, so the observations are independent.
Not pre-registered: exploratory triangulation of another repository's saved, out-of-sample labels.
Writes results/external_market_regimes_forward_test.md.
"""
from __future__ import annotations

import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
MR = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/alperdroid/market-regimes/market_regimes")
NAMES = {0: "Calm", 1: "Transitional", 2: "Crisis"}


def r2(y, X):
    X = np.column_stack([np.ones(len(y)), X])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    return 1 - e @ e / ((y - y.mean()) @ (y - y.mean()))


def main():
    d = pickle.load(open(MR / "results" / "data_cache.pkl", "rb"))
    spy = d["prices"]["SPY"]
    rf = d["rf"] / 100 / 252                                # ^IRX annualised % -> daily
    r = np.log(spy).diff()
    ex = r - rf
    lab = pd.read_csv(MR / "results" / "regime_labels.csv", index_col=0, parse_dates=True)
    df = pd.DataFrame({"ex": ex, "r": r, "vix": d["vix"]}).join(lab).dropna(subset=["HMM", "GMM"])
    idx = df.index
    pos = np.arange(0, len(idx) - 21, 21)                    # non-overlapping decision days
    rows = []
    for p in pos:
        if p < 21:
            continue
        t = idx[p]
        fwd = df["r"].iloc[p + 1:p + 22]
        rows.append({"t": t, "fwd_ret": float(df["ex"].iloc[p + 1:p + 22].sum()) * 12,          # annualised
                     "fwd_vol": float(fwd.std() * np.sqrt(252)),
                     "past_vol": float(df["r"].iloc[p - 20:p + 1].std() * np.sqrt(252)),
                     "vix": float(df["vix"].iloc[p]),
                     **{k: int(df[k].iloc[p]) for k in ("VIX", "HMM", "GMM", "Ensemble") if pd.notna(df[k].iloc[p])}})
    S = pd.DataFrame(rows).set_index("t")
    out = ["# Forward test of market-regimes labels (exploratory)", "",
           f"SPY, {S.index[0].date()} to {S.index[-1].date()}, {len(S)} non-overlapping 21-trading-day windows. "
           "Label = the classifier's out-of-sample label at the close of day t; outcome = the next 21 trading days. "
           "Returns are SPY excess log returns, annualised (x12); volatility is annualised daily volatility.", ""]
    tab = []
    for k in ("VIX", "HMM", "GMM", "Ensemble"):
        if k not in S:
            continue
        g = S.dropna(subset=[k]).groupby(k)
        for code, sub in g:
            tab.append({"classifier": k, "regime today": NAMES[code], "windows": len(sub),
                        "next-month return (ann.)": f"{sub.fwd_ret.mean():+.1%}",
                        "t-stat": f"{sub.fwd_ret.mean() / (sub.fwd_ret.std() / np.sqrt(len(sub))):+.2f}" if len(sub) > 2 else "",
                        "next-month vol (ann.)": f"{sub.fwd_vol.mean():.1%}"})
    out += ["## Next-month SPY outcome by today's regime label", "", pd.DataFrame(tab).to_markdown(index=False), ""]
    tests = []
    for k in ("VIX", "HMM", "GMM", "Ensemble"):
        sub = S.dropna(subset=[k])
        D = pd.get_dummies(sub[k].astype(int), drop_first=True).astype(float).values
        f_ret = stats.f_oneway(*[g.fwd_ret.values for _, g in sub.groupby(k)])
        tests.append({"classifier": k, "R² next-month return": f"{r2(sub.fwd_ret.values, D):.3f}",
                      "ANOVA p (returns)": f"{f_ret.pvalue:.2f}",
                      "R² next-month vol": f"{r2(sub.fwd_vol.values, D):.3f}",
                      "R² vol: past 21-day vol only": f"{r2(sub.fwd_vol.values, sub.past_vol.values):.3f}",
                      "R² vol: past vol + label": f"{r2(sub.fwd_vol.values, np.column_stack([sub.past_vol.values, D])):.3f}"})
    out += ["## How much does today's label explain? (in-sample R² across windows)", "",
            pd.DataFrame(tests).to_markdown(index=False), "",
            "Reading: a label 'forecasts' returns only if returns differ by regime beyond noise (ANOVA p); "
            "it adds risk information only if 'past vol + label' clearly beats 'past vol only'.", ""]
    pers = []
    for k in ("HMM", "GMM", "VIX"):
        s = S[k].dropna().astype(int)
        pers.append({"classifier": k, "same label 21 days later": f"{(s.values[1:] == s.values[:-1]).mean():.0%}"})
    out += ["## Persistence", "", pd.DataFrame(pers).to_markdown(index=False), ""]
    (ROOT / "results" / "external_market_regimes_forward_test.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
