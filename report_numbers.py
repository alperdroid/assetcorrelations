"""Numbers for the investment recommendation report, on ONE common basis:
US universe, return months 1990-01 to 2026-08, after costs, gold = World Bank monthly average.

    python report_numbers.py   # -> results/report_strategies_1990.csv, results/report_portfolios_1990.csv

Strategy returns are read from the saved study outputs (nothing is re-estimated). The portfolio
options are static mixes simulated with the same cost model; the 'growth' mix is illustrative
and was not part of any pre-registered test.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from analysis import perf_stats
from config import Config
from data import build_panels, load_raw
from study2 import simulate

ROOT = Path(__file__).resolve().parent
A, B = "1990-01", "2026-08"


def load(path, cols):
    r = pd.read_csv(ROOT / path, index_col=0)
    r.index = pd.PeriodIndex(r.index, freq="M")
    return r[list(cols)].rename(columns=cols).loc[A:B]


def main():
    cfg = Config()
    cfg.cost_bps = {**cfg.cost_bps, "CASH": 0.0}
    base = build_panels(load_raw(ROOT / "data" / "raw", 12))["returns"]
    rf = base["RF"]
    s1 = load("results_main/oos_returns.csv", {"60/40": "60/40", "Static 1/3": "Static 1/3",
                                               "Regime Tilt": "S1 Regime Tilt", "Uncond. Tilt": "S1 Uncond. Tilt",
                                               "Regime ERC": "S1 Regime ERC", "Uncond. ERC": "S1 Uncond. ERC"})
    s2 = load("results_study2/returns_primary.csv", {"H1 Bond-hedge switch": "S2 H1 Bond-gold switch",
                                                      "H2a Trend 3-asset": "S2 H2a Trend, no cash",
                                                      "H2b Trend sectors": "S2 H2b Trend sectors",
                                                      "H3 Vol-managed equity": "S2 H3 Vol-managed equity"})
    s3 = load("results_study3/returns_US.csv", {"H4a": "S3 H4a Trend + cash", "H4b": "S3 H4b Trend, cash fallback"})
    strat = pd.concat([s1, s2, s3], axis=1).dropna()
    st = pd.DataFrame({k: perf_stats(strat[k], rf) for k in strat}).T
    for name, (a, b) in {"2008 GFC": ("2007-11", "2009-02"), "2022": ("2022-01", "2022-10")}.items():
        st[name] = (1 + strat.loc[a:b]).prod() - 1
    st.to_csv(ROOT / "results" / "report_strategies_1990.csv")

    rets = pd.DataFrame({"EQ": base["MKT"], "UST10": base["UST10"], "GOLD": base["GOLD"], "CASH": base["RF"]}).loc[A:B]
    mixes = {"Reference: 60/40 stocks/Treasuries": [0.6, 0.4, 0.0, 0.0],
             "Conservative: 70% core + 30% T-bills": [0.7 / 3, 0.7 / 3, 0.7 / 3, 0.3],
             "Core: 1/3 stocks, 1/3 Treasuries, 1/3 gold": [1 / 3, 1 / 3, 1 / 3, 0.0],
             "Growth (illustrative): 50/25/25": [0.5, 0.25, 0.25, 0.0]}
    port = {}
    for k, w in mixes.items():
        port[k], _ = simulate(pd.DataFrame([w] * len(rets), index=rets.index, columns=rets.columns), rets, cfg)
    port = pd.DataFrame(port)
    pt = pd.DataFrame({k: perf_stats(port[k], rf) for k in port}).T
    for name, (a, b) in {"2008 GFC": ("2007-11", "2009-02"), "2022": ("2022-01", "2022-10"),
                         "2000-02": ("2000-09", "2002-09")}.items():
        pt[name] = (1 + port.loc[a:b]).prod() - 1
    pt.to_csv(ROOT / "results" / "report_portfolios_1990.csv")
    pd.set_option("display.width", 200)
    print(st[["CAGR", "Vol", "Sharpe", "MaxDD", "2008 GFC", "2022"]].round(3).sort_values("MaxDD"))
    print(pt[["CAGR", "Vol", "Sharpe", "MaxDD", "Worst month", "2000-02", "2008 GFC", "2022"]].round(3))


if __name__ == "__main__":
    main()
