"""Supporting tables for results/findings_draft.md, computed from the main run's inputs/outputs.

    python findings_tables.py --run results_main     # writes results/findings_tables.md

Descriptive (in-sample, 1972-latest, real-time labels paired with next-month returns):
  - hedging by regime: correlation with the market, return in down-market months, Sharpe +- SE
  - hypothesis scorecard (README table) with Sharpe ranks, full sample and both eras
Out-of-sample:
  - 2022 and the 2025 tariff shock month by month: labels, returns, Regime Tilt allocation
Sharpe standard errors use the iid approximation SE = sqrt((1 + SR^2 / 2) / years) (Lo 2002);
they ignore autocorrelation and are only a rough guide to what is noise.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from config import Config
from data import build_panels, load_raw
from regimes import REGIME_ORDER

ROOT = Path(__file__).resolve().parent
HYP = {
    "Goldilocks (G+ I-)": (["BusEq", "Shops", "Durbl"], ["GOLD", "Enrgy"]),
    "Reflation (G+ I+)": (["Enrgy", "Chems", "Money"], ["UST10"]),
    "Stagflation (G- I+)": (["Enrgy", "GOLD", "NoDur"], ["UST10", "BusEq"]),
    "Disinflationary slowdown (G- I-)": (["UST10", "NoDur", "Hlth", "Utils"], ["Durbl", "Enrgy", "Money"]),
}


def md(df: pd.DataFrame, idx=True) -> str:
    d = df.reset_index() if idx else df
    lines = ["| " + " | ".join(map(str, d.columns)) + " |", "|" + "---|" * d.shape[1]]
    lines += ["| " + " | ".join("" if (isinstance(v, float) and np.isnan(v)) else str(v) for v in r) + " |"
              for r in d.values]
    return "\n".join(lines)


def short(r: str) -> str:
    return r.split(" (")[0]


def regime_stats(rets, lab, assets):
    rows = []
    for reg in REGIME_ORDER:
        sub = rets[lab == reg]
        down = sub[sub["MKT"] < 0]
        for a in assets:
            ex = sub[a] - sub["RF"]
            sr = ex.mean() / sub[a].std() * np.sqrt(12)
            yrs = len(sub) / 12
            rows.append({"regime": reg, "asset": a, "months": len(sub), "down_months": len(down),
                         "sharpe": sr, "se": np.sqrt((1 + sr ** 2 / 2) / yrs),
                         "corr_mkt": sub[a].corr(sub["MKT"]),
                         "down_mkt_ret": down[a].mean(), "mkt_down_ret": down["MKT"].mean()})
    return pd.DataFrame(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run", default="results_main")
    args = p.parse_args()
    run = ROOT / args.run
    cfg = Config()
    panels = build_panels(load_raw(ROOT / "data" / "raw", 12))
    rets = panels["returns"].loc[cfg.sample_start:]
    inds = panels["industries"]
    regimes = pd.read_csv(run / "regimes.csv", index_col=0)
    regimes.index = pd.PeriodIndex(regimes.index, freq="M")
    lab = regimes["regime"].shift(1).reindex(rets.index)
    assets = inds + ["UST10", "GOLD"]
    out = ["# Supporting tables for the findings draft", "",
           f"Inputs: {args.run}, returns {rets.index[0]} to {rets.index[-1]}. Labels are real-time labels "
           "known at the end of month t-1, paired with returns in month t.", ""]

    # ---- 1. hedging by regime (full sample, descriptive)
    st = regime_stats(rets, lab, assets + ["MKT"])
    st.to_csv(ROOT / "results" / "regime_hedging_full.csv", index=False)
    out += ["## 1. Hedging by regime, 1972-latest (descriptive, in-sample)", "",
            "Average monthly return in months when the US market fell (down-market months), "
            "with the market's own average in the last row. Higher = better hedge.", ""]
    piv = st.pivot(index="asset", columns="regime", values="down_mkt_ret")[REGIME_ORDER] * 100
    piv.columns = [f"{short(c)} (n={int(st[st.regime == c].down_months.iloc[0])})" for c in REGIME_ORDER]
    piv = piv.loc[assets + ["MKT"]]
    out += [md(piv.round(2)), ""]
    cm = st.pivot(index="asset", columns="regime", values="corr_mkt")[REGIME_ORDER].loc[assets]
    cm.columns = [short(c) for c in REGIME_ORDER]
    out += ["Correlation with the US market by regime:", "", md(cm.round(2)), ""]
    sr = st.pivot(index="asset", columns="regime", values="sharpe")[REGIME_ORDER].loc[assets + ["MKT"]]
    se = st.pivot(index="asset", columns="regime", values="se")[REGIME_ORDER].loc[assets + ["MKT"]]
    srt = sr.round(2).astype(str) + " (" + se.round(2).astype(str) + ")"
    srt.columns = [f"{short(c)} (n={int(st[st.regime == c].months.iloc[0])})" for c in REGIME_ORDER]
    out += ["Annualised Sharpe ratio by regime (approximate iid standard error in brackets):", "", md(srt), ""]

    # ---- 2. hypothesis scorecard: full sample and both eras
    rows = []
    eras = {"full": rets.index, "1972-89": rets.loc[:"1989-12"].index, "1990-latest": rets.loc["1990-01":].index}
    ranks = {}
    for era, idx in eras.items():
        s = regime_stats(rets.loc[idx], lab.loc[idx], assets)
        s["rank"] = s.groupby("regime")["sharpe"].rank(ascending=False).astype(int)
        ranks[era] = s.set_index(["regime", "asset"])
    for reg, (win, lose) in HYP.items():
        for role, names in (("expected winner", win), ("expected loser", lose)):
            for a in names:
                row = {"regime": short(reg), "asset": a, "hypothesis": role}
                for era in eras:
                    r = ranks[era].loc[(reg, a)]
                    row[f"rank {era}"] = f"{int(r['rank'])}/{len(assets)}"
                    row[f"Sharpe {era}"] = f"{r['sharpe']:.2f}"
                ok = ranks["full"].loc[(reg, a), "rank"]
                row["full-sample verdict"] = ("supported" if (role == "expected winner" and ok <= 5) or
                                              (role == "expected loser" and ok >= len(assets) - 4) else "not supported")
                rows.append(row)
    sc = pd.DataFrame(rows)
    sc.to_csv(ROOT / "results" / "hypothesis_scorecard.csv", index=False)
    out += ["## 2. Hypothesis scorecard (README table)", "",
            f"Rank of each asset's Sharpe ratio among the {len(assets)} tradable assets within the regime "
            "(1 = best). 'Supported' = expected winner in the top 5, or expected loser in the bottom 5, "
            "on the full sample. Months per regime and era are in regime_stability.csv.", "",
            md(sc, idx=False), ""]
    stab = pd.read_csv(run / "regime_stability.csv")
    out += ["Era stability (Spearman rank correlation of Sharpe ratios, 1972-89 vs 1990-latest, "
            "includes MKT):", "", md(stab.round(2), idx=False), ""]

    # ---- 3. 2022 and 2025 month by month (out-of-sample)
    port = pd.read_csv(run / "oos_returns.csv", index_col=0)
    port.index = pd.PeriodIndex(port.index, freq="M")
    w = pd.read_csv(run / "weights_Regime_Tilt.csv", index_col=0)
    w.index = pd.PeriodIndex(w.index, freq="M")
    wu = pd.read_csv(run / "weights_Uncond_Tilt.csv", index_col=0)
    wu.index = pd.PeriodIndex(wu.index, freq="M")
    for title, a, b in (("2022 inflation shock", "2021-10", "2022-12"), ("2025 tariff shock", "2024-12", "2025-06")):
        idx = port.loc[a:b].index
        t = pd.DataFrame(index=idx.astype(str))
        t["label used (t-1)"] = [short(str(lab.get(m))) for m in idx]
        t["sb corr"] = [f"{regimes['sb_corr'].get(m - 1, np.nan):.2f}" for m in idx]
        for k in ("Regime Tilt", "Uncond. Tilt", "60/40", "Static 1/3"):
            t[k] = [f"{v:+.1%}" for v in port.loc[idx, k]]
        for k in ("MKT", "UST10", "GOLD"):
            t[k] = [f"{v:+.1%}" for v in rets.loc[idx, k]]
        t["RT: UST10/GOLD/equity"] = [f"{w.loc[m, 'UST10']:.0%}/{w.loc[m, 'GOLD']:.0%}/{w.loc[m, inds].sum():.0%}" for m in idx]
        t["UT: UST10/GOLD/equity"] = [f"{wu.loc[m, 'UST10']:.0%}/{wu.loc[m, 'GOLD']:.0%}/{wu.loc[m, inds].sum():.0%}" for m in idx]
        t["RT top sectors"] = [", ".join(f"{c} {w.loc[m, c]:.0%}" for c in w.loc[m, inds].nlargest(3).index) for m in idx]
        out += [f"## 3. {title}, month by month (out-of-sample)", "", md(t), ""]
        tot = (1 + port.loc[a:b]).prod() - 1
        out += ["Cumulative over the window: " + ", ".join(f"{k} {v:+.1%}" for k, v in tot.items()), ""]

    # ---- 4. regime-conditional out-of-sample strategy returns
    oos_lab = lab.reindex(port.index)
    g = port.groupby(oos_lab.map(lambda r: short(str(r))))
    tab = (g.mean() * 12 * 100).round(1)
    tab["months"] = g.size()
    out += ["## 4. Out-of-sample strategy returns by real-time regime (annualised mean, %)", "", md(tab), ""]
    (ROOT / "results" / "findings_tables.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
