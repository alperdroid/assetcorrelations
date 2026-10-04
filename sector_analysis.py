"""Sector deep dive (descriptive; no new strategy is tested). Writes results/sector_deepdive.md
and charts in results/sector_charts/.

    python sector_analysis.py

A. Sector risk profile by era: return, vol, Sharpe, max drawdown, beta, downside capture,
   correlation with Treasuries and gold (1972-89 vs 1990-latest).
B. Sector-bond correlation by decade: did bonds stop hedging every sector, or only some?
C. Stress episodes: which sectors protected, and how consistently.
D. Regime map at sector level: within-regime Sharpe ranking of the 12 sectors, 1972-89 vs 1990-latest.
E. Attribution of Study 1's Regime Tilt vs Uncond. Tilt: sector bets vs Treasury/gold bets.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import Config
from data import build_panels, load_raw
from regimes import REGIME_ORDER

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
CH = OUT / "sector_charts"
ERAS = {"1972-1989": ("1972-01", "1989-12"), "1990-latest": ("1990-01", None)}
DECADES = {"1972-79": ("1972", "1979"), "1980s": ("1980", "1989"), "1990s": ("1990", "1999"),
           "2000s": ("2000", "2009"), "2010s": ("2010", "2019"), "2020-26": ("2020", "2026")}
INK2, GRID = "#52514e", "#e6e5e0"


def md(df, pct=(), dec=2):
    d = df.copy()
    for c in d.columns:
        if c in pct:
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v * 100:.1f}%")
        elif pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:.{dec}f}")
    cols = [str(d.index.name or "")] + list(map(str, d.columns))
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join([str(i)] + [str(v) for v in r]) + " |" for i, r in zip(d.index, d.values)]
    return "\n".join(out)


def maxdd(r):
    w = (1 + r).cumprod()
    return (w / w.cummax() - 1).min()


def profile(R, inds):
    rows = {}
    down = R["MKT"] < 0
    for a in inds + ["MKT", "UST10", "GOLD"]:
        r = R[a]
        rows[a] = {"CAGR": (1 + r).prod() ** (12 / len(r)) - 1, "Vol": r.std() * np.sqrt(12),
                   "Sharpe": (r - R["RF"]).mean() / r.std() * np.sqrt(12), "MaxDD": maxdd(r),
                   "Beta": r.cov(R["MKT"]) / R["MKT"].var(),
                   "Down capture": r[down].mean() / R.loc[down, "MKT"].mean(),
                   "Corr UST10": r.corr(R["UST10"]), "Corr GOLD": r.corr(R["GOLD"])}
    return pd.DataFrame(rows).T


def style(ax, title):
    ax.set_title(title, loc="left", fontsize=9)
    ax.grid(color=GRID, lw=0.6)
    ax.tick_params(labelsize=7, colors=INK2)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)


def main():
    CH.mkdir(parents=True, exist_ok=True)
    cfg = Config()
    p = build_panels(load_raw(ROOT / "data" / "raw", 12))
    R = p["returns"].loc[cfg.sample_start:]
    inds = p["industries"]
    rep = ["# Sector deep dive", "",
           f"Descriptive analysis of the 12 Ken French value-weighted industries, {R.index[0]} to {R.index[-1]}, "
           "monthly, month-end returns (gold: World Bank monthly average). No strategy is tested here. "
           "GICS analogues: NoDur ≈ staples, Durbl ≈ autos/durables, Manuf ≈ industrials, Enrgy ≈ energy, "
           "Chems ≈ materials, BusEq ≈ tech, Telcm ≈ communication, Utils ≈ utilities, Shops ≈ retail, "
           "Hlth ≈ health care, Money ≈ financials.", ""]

    # ---- A. profile by era
    rep += ["## A. Sector risk profile by era", "",
            "Down capture = average return in months the US market fell, divided by the market's average in those "
            "months (1.00 = falls as much as the market; lower = more defensive).", ""]
    prof = {}
    for era, (a, b) in ERAS.items():
        prof[era] = profile(R.loc[a:b], inds)
        prof[era].to_csv(OUT / f"sector_profile_{era}.csv")
    cmp = pd.DataFrame({
        "Sharpe 72-89": prof["1972-1989"]["Sharpe"], "Sharpe 90-": prof["1990-latest"]["Sharpe"],
        "MaxDD 72-89": prof["1972-1989"]["MaxDD"], "MaxDD 90-": prof["1990-latest"]["MaxDD"],
        "Beta 72-89": prof["1972-1989"]["Beta"], "Beta 90-": prof["1990-latest"]["Beta"],
        "DownCap 72-89": prof["1972-1989"]["Down capture"], "DownCap 90-": prof["1990-latest"]["Down capture"],
        "Corr UST 72-89": prof["1972-1989"]["Corr UST10"], "Corr UST 90-": prof["1990-latest"]["Corr UST10"],
        "Corr Gold 72-89": prof["1972-1989"]["Corr GOLD"], "Corr Gold 90-": prof["1990-latest"]["Corr GOLD"],
    })
    rep += [md(cmp, pct=["MaxDD 72-89", "MaxDD 90-"]), ""]
    dc = cmp.loc[inds]
    rk = lambda s: s.rank().astype(int)
    rep += [f"Most defensive sectors by down capture: 1972-89 {', '.join(dc['DownCap 72-89'].nsmallest(3).index)}; "
            f"1990-latest {', '.join(dc['DownCap 90-'].nsmallest(3).index)}. "
            f"Rank correlation of sector down capture across eras: {dc['DownCap 72-89'].corr(dc['DownCap 90-'], method='spearman'):.2f}; "
            f"of sector beta: {dc['Beta 72-89'].corr(dc['Beta 90-'], method='spearman'):.2f}; "
            f"of sector Sharpe: {dc['Sharpe 72-89'].corr(dc['Sharpe 90-'], method='spearman'):.2f}.", ""]

    # ---- B. sector-bond correlation by decade
    cb = pd.DataFrame({dname: {a: R.loc[a0:b0, a].corr(R.loc[a0:b0, "UST10"]) for a in inds + ["MKT"]}
                       for dname, (a0, b0) in DECADES.items()})
    cg = pd.DataFrame({dname: {a: R.loc[a0:b0, a].corr(R.loc[a0:b0, "GOLD"]) for a in inds + ["MKT"]}
                       for dname, (a0, b0) in DECADES.items()})
    cb.to_csv(OUT / "sector_corr_ust10_by_decade.csv")
    cg.to_csv(OUT / "sector_corr_gold_by_decade.csv")
    rep += ["## B. Do bonds still hedge sectors? Correlation with the 10y Treasury by decade", "",
            "Monthly-return correlation within each decade. Negative = the Treasury hedged that sector.", "",
            md(cb), "",
            "Correlation with gold by decade:", "", md(cg), ""]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    v = 0.8
    im = ax.imshow(cb.values, cmap="RdBu_r", vmin=-v, vmax=v, aspect="auto")
    ax.set_xticks(range(cb.shape[1]), cb.columns, fontsize=8)
    ax.set_yticks(range(cb.shape[0]), cb.index, fontsize=8)
    for i in range(cb.shape[0]):
        for j in range(cb.shape[1]):
            ax.text(j, i, f"{cb.values[i, j]:+.2f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, label="correlation with 10y Treasury")
    ax.set_title("Sector correlation with the 10y Treasury, by decade (red = bonds did not hedge)", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(CH / "sector_bond_corr_by_decade.png", dpi=130)
    plt.close(fig)

    # ---- C. stress episodes
    ep = {}
    for name, (a, b) in cfg.episodes.items():
        sub = R.loc[a:b]
        if len(sub) and sub.index[0] == pd.Period(a, "M"):
            ep[name] = (1 + sub[inds + ["MKT", "UST10", "GOLD"]]).prod() - 1
    ep = pd.DataFrame(ep).T
    ep.to_csv(OUT / "sector_episodes.csv")
    secrank = ep[inds].rank(axis=1, ascending=False)
    top3 = (secrank <= 3).sum().sort_values(ascending=False)
    bot3 = (secrank >= len(inds) - 2).sum().sort_values(ascending=False)
    best = ep[inds].idxmax(axis=1)
    worst = ep[inds].idxmin(axis=1)
    rel = ep[inds].sub(ep["MKT"], axis=0)
    beat = (rel > 0).sum().sort_values(ascending=False)
    rep += ["## C. Stress episodes: which sectors protected?", "",
            md(ep, pct=list(ep.columns)), "",
            "Best and worst sector in each episode:", "",
            md(pd.DataFrame({"best sector": best, "best": ep[inds].max(axis=1), "worst sector": worst,
                             "worst": ep[inds].min(axis=1), "market": ep["MKT"],
                             "10y Treasury": ep["UST10"], "gold": ep["GOLD"]}),
               pct=["best", "worst", "market", "10y Treasury", "gold"]), "",
            f"Episodes (of {len(ep)}) in which each sector beat the market: "
            + ", ".join(f"{k} {v}" for k, v in beat.items()) + ".", "",
            "Times in the top 3 sectors: " + ", ".join(f"{k} {v}" for k, v in top3.items()) + ".  ",
            "Times in the bottom 3 sectors: " + ", ".join(f"{k} {v}" for k, v in bot3.items()) + ".", ""]
    n_any = int((ep[inds].max(axis=1) > 0).sum())
    hedge_cnt = {"10y Treasury": int((ep["UST10"] > 0).sum()), "gold": int((ep["GOLD"] > 0).sum()),
                 "best sector": n_any}
    rep += [f"Episodes with a positive return: 10y Treasury {hedge_cnt['10y Treasury']}, gold {hedge_cnt['gold']}, "
            f"best sector {hedge_cnt['best sector']} of {len(ep)} (the best sector is only known after the fact).", ""]
    fig, ax = plt.subplots(figsize=(12, 5.2))
    show = ep[inds + ["MKT", "UST10", "GOLD"]] * 100
    v = np.nanmax(np.abs(show.values))
    im = ax.imshow(show.values, cmap="RdBu", vmin=-v, vmax=v, aspect="auto")
    ax.set_xticks(range(show.shape[1]), show.columns, fontsize=8, rotation=30, ha="right")
    ax.set_yticks(range(show.shape[0]), show.index, fontsize=8)
    for i in range(show.shape[0]):
        for j in range(show.shape[1]):
            ax.text(j, i, f"{show.values[i, j]:.0f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, label="cumulative return, %")
    ax.set_title("Stress episodes: cumulative return by sector, market, Treasury and gold", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(CH / "sector_episodes_heatmap.png", dpi=130)
    plt.close(fig)

    # ---- D. sector-only regime map stability
    regimes = pd.read_csv(ROOT / "results_main" / "regimes.csv", index_col=0)
    regimes.index = pd.PeriodIndex(regimes.index, freq="M")
    lab = regimes["regime"].shift(1).reindex(R.index)
    rows, tab = [], {}
    for reg in REGIME_ORDER:
        s = {}
        for era, (a, b) in ERAS.items():
            sub = R.loc[a:b][lab.loc[a:b] == reg]
            s[era] = ((sub[inds].sub(sub["RF"], axis=0)).mean() / sub[inds].std() * np.sqrt(12))
            tab[(reg.split(" (")[0], era)] = s[era]
        rows.append({"regime": reg.split(" (")[0], "rank corr (sectors only)": s["1972-1989"].corr(s["1990-latest"], method="spearman"),
                     "top 3 sectors 1972-89": ", ".join(s["1972-1989"].nlargest(3).index),
                     "top 3 sectors 1990-": ", ".join(s["1990-latest"].nlargest(3).index),
                     "bottom 3 sectors 1972-89": ", ".join(s["1972-1989"].nsmallest(3).index),
                     "bottom 3 sectors 1990-": ", ".join(s["1990-latest"].nsmallest(3).index)})
    stab = pd.DataFrame(rows).set_index("regime")
    stab.to_csv(OUT / "sector_regime_stability.csv")
    pd.DataFrame(tab).to_csv(OUT / "sector_regime_sharpe_by_era.csv")
    rep += ["## D. Sector-level regime map: does the same sector win in the same regime in both eras?", "",
            "Spearman rank correlation of the 12 sectors' Sharpe ratios within each real-time regime, 1972-89 vs "
            "1990-latest (Treasuries and gold excluded).", "", md(stab), ""]

    # ---- E. attribution of Study 1 Regime Tilt vs Uncond. Tilt
    w_rt = pd.read_csv(ROOT / "results_main" / "weights_Regime_Tilt.csv", index_col=0)
    w_ut = pd.read_csv(ROOT / "results_main" / "weights_Uncond_Tilt.csv", index_col=0)
    for w in (w_rt, w_ut):
        w.index = pd.PeriodIndex(w.index, freq="M")
    idx = w_rt.index
    dw = (w_rt - w_ut)
    contrib = dw * R.loc[idx, dw.columns]
    sec_c = contrib[inds].sum(axis=1)
    def_c = contrib[["UST10", "GOLD"]].sum(axis=1)
    # split sector contribution into allocation (total equity weight) and selection (mix within equities)
    eq_rt, eq_ut = w_rt[inds].sum(axis=1), w_ut[inds].sum(axis=1)
    eqret_rt = (w_rt[inds] * R.loc[idx, inds]).sum(axis=1) / eq_rt
    eqret_ut = (w_ut[inds] * R.loc[idx, inds]).sum(axis=1) / eq_ut
    alloc = (eq_rt - eq_ut) * eqret_ut
    select = eq_rt * (eqret_rt - eqret_ut)
    att = pd.DataFrame({"sector selection": select, "equity sleeve size": alloc,
                        "Treasury + gold holdings": def_c, "total (gross, before costs)": sec_c + def_c})
    assert np.allclose(att[["sector selection", "equity sleeve size", "Treasury + gold holdings"]].sum(axis=1),
                       att["total (gross, before costs)"])
    per = {"1990-latest": (None, None), "1990s": ("1990", "1999"), "2000s": ("2000", "2009"),
           "2010s": ("2010", "2019"), "2020-26": ("2020", "2026"), "2008 GFC (2007-11..2009-02)": ("2007-11", "2009-02"),
           "2022 (Jan-Oct)": ("2022-01", "2022-10")}
    at = pd.DataFrame({k: att.loc[a:b].mean() * 12 * 100 for k, (a, b) in per.items()}).T
    from significance import stationary_bootstrap_indices
    bidx = stationary_bootstrap_indices(len(att), 5000, 12.0, np.random.default_rng(20260101))
    sig = {}
    for c in att.columns:
        x = att[c].values
        m = x.mean() * 1200
        bm = x[bidx].mean(axis=1) * 1200
        sig[c] = {"mean (pp/yr)": m, "95% CI low": np.quantile(bm, 0.025), "95% CI high": np.quantile(bm, 0.975),
                  "p (two-sided)": float(np.mean(np.abs(bm - m) >= abs(m)))}
    sig = pd.DataFrame(sig).T
    sig.to_csv(OUT / "sector_attribution_bootstrap.csv")
    at.to_csv(OUT / "sector_attribution_regime_tilt.csv")
    gross_gap = (contrib.sum(axis=1)).mean() * 12 * 100
    avgw = pd.DataFrame({reg.split(" (")[0]: w_rt.loc[lab.reindex(idx) == reg, inds].mean() for reg in REGIME_ORDER})
    avgw["Uncond. Tilt (all months)"] = w_ut[inds].mean()
    avgw.loc["Total equity"] = avgw.sum()
    avgw.loc["UST10"] = [w_rt.loc[lab.reindex(idx) == reg, "UST10"].mean() for reg in REGIME_ORDER] + [w_ut["UST10"].mean()]
    avgw.loc["GOLD"] = [w_rt.loc[lab.reindex(idx) == reg, "GOLD"].mean() for reg in REGIME_ORDER] + [w_ut["GOLD"].mean()]
    rep += ["## E. Study 1 attribution: did Regime Tilt's sector bets add value?", "",
            "Regime Tilt minus Uncond. Tilt, monthly return gap split additively into: sector selection (mix within the "
            "equity sleeve), equity sleeve size (more or less equity, valued at the control's sector mix), and the "
            "Treasury + gold holdings (difference in UST10 and GOLD weights times their returns). "
            "Annualised arithmetic means in percentage points, gross of costs, using target weights at the start of "
            "each month (within-month drift ignored).", "",
            md(at), "",
            "Is any component distinguishable from zero? Stationary block bootstrap of the 1990-latest mean "
            "(mean block 12, 5,000 resamples, seed 20260101; descriptive, not a pre-registered test):", "",
            md(sig), "",
            "Average Regime Tilt weights by real-time regime (out-of-sample 1990-latest):", "",
            md(avgw, pct=list(avgw.columns)), ""]
    (OUT / "sector_deepdive.md").write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
