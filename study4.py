"""Study 4: H4a (trend + cash) vs cash-matched and volatility-matched static portfolios.
Specification: PREREGISTRATION_STUDY4.md. Robustness / decomposition on data seen in Study 3.

    python study4.py     # -> results_study4/
"""
from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import brentq

from config import Config
from data import build_panels, load_raw
from significance import bootstrap_diff
from study2 import BOOT, holm, md, simulate, stats_table
from study3 import INTL_START, REGIONS, US_START, build, kf_region

ROOT = Path(__file__).resolve().parent
PRIMARY = "Developed ex US"


def cash_mix(c: float, index) -> pd.DataFrame:
    s = (1 - c) / 3
    return pd.DataFrame([[s, s, s, c]] * len(index), index=index, columns=["EQ", "UST10", "GOLD", "CASH"])


def run_universe(eq_m, eq_d, base, start, cfg):
    port, turn, W, rets = build(eq_m, eq_d, base, start, cfg)
    h4a = port["H4a"]
    c1 = float(W["H4a"]["CASH"].mean())
    p1, _ = simulate(cash_mix(c1, port.index), rets, cfg)
    target_vol = h4a.std()
    f = lambda c: simulate(cash_mix(c, port.index), rets, cfg)[0].std() - target_vol
    c2 = brentq(f, 0.0, 0.99, xtol=1e-6)
    p2, _ = simulate(cash_mix(c2, port.index), rets, cfg)
    out = pd.DataFrame({"H4a Trend + cash": h4a, "C1 cash-matched static": p1, "C2 vol-matched static": p2,
                        "Static 1/3": port["Static 1/3"]})
    return out, c1, c2


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg = Config()
    cfg.cost_bps = {**cfg.cost_bps, "CASH": 0.0}
    raw_dir = ROOT / "data" / "raw"
    out = ROOT / "results_study4"
    out.mkdir(exist_ok=True)
    raw = load_raw(raw_dir, 12, use_gold_override=False)
    base = build_panels(raw)["returns"].loc[cfg.sample_start:]
    rf = base["RF"]
    unis = {n: (*kf_region(raw_dir, s), INTL_START) for n, s in REGIONS.items()}
    unis["US (1973-, seen)"] = (base["MKT"], raw["ff3_d"]["Mkt-RF"] + raw["ff3_d"]["RF"], US_START)

    pct = ["CAGR", "Vol", "MaxDD", "Worst month", "CVaR 5% (monthly)"]
    rep = ["# Study 4 results: is trend + cash (H4a) timing, or just holding cash?", "",
           "Specification: `PREREGISTRATION_STUDY4.md`. Robustness / decomposition on data already seen in "
           "Study 3; not confirmatory. After costs.", ""]
    rows, tests_all, eps = [], [], {}
    for name, (eq_m, eq_d, start) in unis.items():
        p, c1, c2 = run_universe(eq_m, eq_d, base, start, cfg)
        p.to_csv(out / f"returns_{name.split(' (')[0].replace(' ', '_')}.csv")
        st = stats_table(p, rf)
        rows.append((name, c1, c2, st))
        r = rf.reindex(p.index).values
        for ctrl in ("C1 cash-matched static", "C2 vol-matched static"):
            for stat in ("maxdd", "sharpe"):
                res = bootstrap_diff(p["H4a Trend + cash"].values, p[ctrl].values, r, stat, **BOOT)
                tests_all.append({"universe": name, "control": ctrl,
                                  "statistic": "MaxDD" if stat == "maxdd" else "Sharpe", **res})
        for en, (a, b) in cfg.episodes.items():
            sub = p.loc[a:b]
            if len(sub) and sub.index[0] == pd.Period(a, "M"):
                eps[(name, en)] = (1 + sub).prod() - 1
    T = pd.DataFrame(tests_all)
    prim = T[(T.universe == PRIMARY) & (T.control == "C1 cash-matched static")].reset_index(drop=True)
    prim = prim.join(holm(prim["p_value"]))
    prim.to_csv(out / "tests_primary_holm.csv", index=False)
    T.to_csv(out / "tests_all.csv", index=False)
    md_ = prim.set_index("statistic")["diff"]
    supported = (md_["MaxDD"] > 0 and md_["Sharpe"] > 0 and prim["holm_reject_5pct"].any())
    rep += [f"## Verdict (primary: {PRIMARY}, H4a vs C1, Holm over 2 tests)", "",
            f"- **H6**: {'SUPPORTED' if supported else 'not supported'}", ""]
    show = prim.copy()
    show["diff"] = [f"{d * 100:+.1f}pp" if s == "MaxDD" else f"{d:+.2f}" for d, s in zip(prim["diff"], prim.statistic)]
    show["95% CI"] = [f"[{lo * 100:+.1f}, {hi * 100:+.1f}]pp" if s == "MaxDD" else f"[{lo:+.2f}, {hi:+.2f}]"
                      for lo, hi, s in zip(prim.ci_low, prim.ci_high, prim.statistic)]
    rep += [md(show.set_index("statistic")[["diff", "95% CI", "p_value", "holm_adj_p", "holm_reject_5pct"]]), ""]
    for name, c1, c2, st in rows:
        rep += [f"## {name}: C1 cash = {c1:.1%}, C2 cash = {c2:.1%}", "", md(st.drop(columns="Months"), pct=pct), ""]
    allshow = T.copy()
    allshow["diff"] = [f"{d * 100:+.1f}pp" if s == "MaxDD" else f"{d:+.2f}" for d, s in zip(T["diff"], T.statistic)]
    rep += ["## All comparisons (H4a minus control; not Holm-corrected; MaxDD > 0 = H4a shallower)", "",
            md(allshow.set_index("universe")[["control", "statistic", "diff", "p_value"]]), ""]
    cols = {}
    for (u, en), ser in eps.items():
        for strat in ("H4a Trend + cash", "C1 cash-matched static"):
            cols.setdefault(f"{u.split(' (')[0]}: {strat.split(' ')[0]}", {})[en] = ser[strat]
    ep = pd.DataFrame(cols).reindex(list(cfg.episodes)).dropna(how="all")
    ep.to_csv(out / "episodes.csv")
    rep += ["## Stress episodes, H4a vs C1 (cumulative return)", "", md(ep, pct=list(ep.columns)), ""]
    (out / "report.md").write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
