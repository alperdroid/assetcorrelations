"""Study 3: trend with a cash fallback (H4a/H4b) and an international confirmation of
volatility-managed equity (H5). Specification: PREREGISTRATION_STUDY3.md.

    python study3.py            # -> results_study3/

Primary family: Developed ex US, return months 1991-07 to 2026-08, Holm over 6 tests.
Weights for return month t use only information available at the end of month t-1.
"""
from __future__ import annotations

import io
import logging
import zipfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import Config
from data import KF_BASE, _fetch, build_panels, load_raw, parse_kf_csv
from significance import bootstrap_diff
from study2 import BOOT, holm, md, simulate, stats_table, trailing_excess_pass

ROOT = Path(__file__).resolve().parent
ASSETS = ["EQ", "UST10", "GOLD", "CASH"]
REGIONS = {"Developed ex US": "Developed_ex_US", "Europe": "Europe", "Japan": "Japan",
           "Asia Pacific ex Japan": "Asia_Pacific_ex_Japan"}
PRIMARY_REGION = "Developed ex US"
INTL_START, US_START = "1991-07", "1973-01"
HYPS = {"H4a Trend + cash (Faber)": "H4a", "H4b Trend redistribute, cash fallback": "H4b",
        "H5 Vol-managed equity": "H5"}


# --------------------------------------------------------------------------- data
def kf_region(raw_dir: Path, stem: str) -> tuple[pd.Series, pd.Series]:
    out = []
    for suf in ("_3_Factors_CSV.zip", "_3_Factors_Daily_CSV.zip"):
        fn = stem + suf
        with zipfile.ZipFile(io.BytesIO(_fetch(KF_BASE + fn, raw_dir / fn, False))) as z:
            df = parse_kf_csv(z.read(z.namelist()[0]).decode("latin-1"))
        out.append(df["Mkt-RF"] + df["RF"])
    return out[0], out[1]


def realized_variance(daily: pd.Series, minp: int = 12) -> pd.DataFrame:
    rv = (daily ** 2).groupby(daily.index.to_period("M")).sum()
    return pd.DataFrame({"rv": rv, "target": rv.expanding(minp).mean()}).shift(1)   # value at t uses t-1


# --------------------------------------------------------------------------- rules (columns = ASSETS)
def _frame(rows, index):
    return pd.DataFrame(rows, index=index, columns=ASSETS)


def w_static(index):
    return _frame([[1 / 3, 1 / 3, 1 / 3, 0.0]] * len(index), index)


def w_trend_cash(passes: pd.DataFrame) -> pd.DataFrame:
    """H4a: each passing sleeve keeps 1/3; each failing sleeve goes to CASH."""
    rows = []
    for _, p in passes[["EQ", "UST10", "GOLD"]].iterrows():
        if p.isna().any():
            rows.append([1 / 3, 1 / 3, 1 / 3, 0.0])
            continue
        ok = p.values.astype(bool)
        w = np.where(ok, 1 / 3, 0.0)
        rows.append(list(w) + [1 - w.sum()])
    return _frame(rows, passes.index)


def w_trend_redistribute(passes: pd.DataFrame) -> pd.DataFrame:
    """H4b: Study 2 H2a, but 100% CASH when no sleeve passes."""
    rows = []
    for _, p in passes[["EQ", "UST10", "GOLD"]].iterrows():
        if p.isna().any():
            rows.append([1 / 3, 1 / 3, 1 / 3, 0.0])
            continue
        ok = p.values.astype(bool)
        if not ok.any():
            rows.append([0.0, 0.0, 0.0, 1.0])
        else:
            w = np.where(ok, 1 / 3 + (1 / 3) * (~ok).sum() / ok.sum(), 0.0)
            rows.append(list(w) + [0.0])
    return _frame(rows, passes.index)


def w_vol(rvt: pd.DataFrame, index, cap: float | None = 2 / 3) -> pd.DataFrame:
    x = rvt.reindex(index)
    w = ((1 / 3) * x["target"] / x["rv"]).clip(0, 1.0 if cap is None else cap).fillna(1 / 3)
    rest = (1 - w) / 2
    return pd.DataFrame({"EQ": w, "UST10": rest, "GOLD": rest, "CASH": 0.0}, index=index)


def build(eq_m, eq_d, base, start, cfg, variant="primary"):
    rets = pd.DataFrame({"EQ": eq_m, "UST10": base["UST10"], "GOLD": base["GOLD"], "CASH": base["RF"],
                         "RF": base["RF"]}).dropna()
    idx = rets.loc[start:].index
    skip = 1 if variant == "R1" else 0
    passes = trailing_excess_pass(rets[["EQ", "UST10", "GOLD"]], rets["RF"], 12, skip).reindex(idx)
    rvt = realized_variance(eq_d)
    W = {"Static 1/3": w_static(idx), "H4a": w_trend_cash(passes), "H4b": w_trend_redistribute(passes),
         "H5": w_vol(rvt, idx, None if variant == "R2" else 2 / 3)}
    port, turn = {}, {}
    for k, w in W.items():
        port[k], turn[k] = simulate(w, rets, cfg)
    return pd.DataFrame(port), pd.DataFrame(turn), W, rets


def test_family(port, rf, hyps, stats=("sharpe", "maxdd")):
    r = rf.reindex(port.index).values
    rows = []
    for h in hyps:
        for st in stats:
            res = bootstrap_diff(port[h].values, port["Static 1/3"].values, r, st, **BOOT)
            rows.append({"test": f"{h} {'Sharpe' if st == 'sharpe' else 'MaxDD'}", "hyp": h,
                         "statistic": "Sharpe" if st == "sharpe" else "MaxDD", **res})
    return pd.DataFrame(rows)


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg = Config()
    cfg.cost_bps = {**cfg.cost_bps, "CASH": 0.0}
    cfg2 = Config()
    cfg2.cost_bps = {**{k: 2 * v for k, v in cfg.cost_bps.items()}, "CASH": 0.0}
    raw_dir = ROOT / "data" / "raw"
    out = ROOT / "results_study3"
    out.mkdir(exist_ok=True)
    raw = load_raw(raw_dir, 12, use_gold_override=False)
    base = build_panels(raw)["returns"].loc[cfg.sample_start:]
    us_d = raw["ff3_d"]["Mkt-RF"] + raw["ff3_d"]["RF"]

    universes = {name: (*kf_region(raw_dir, stem), INTL_START) for name, stem in REGIONS.items()}
    universes["US (seen, exploratory)"] = (base["MKT"], us_d, US_START)

    results, report = {}, ["# Study 3 results", "",
                           "Specification: `PREREGISTRATION_STUDY3.md` (committed before any code or international "
                           "return was examined). After costs. Gold = World Bank monthly average. "
                           "H4 may hold cash (T-bills); H5 and the control may not.", ""]
    pct = ["CAGR", "Vol", "MaxDD", "Worst month", "CVaR 5% (monthly)", "Turnover/m", "Avg cash"]
    for name, (eq_m, eq_d, start) in universes.items():
        port, turn, W, rets = build(eq_m, eq_d, base, start, cfg)
        results[name] = (port, turn, W, rets)
        port.to_csv(out / f"returns_{name.split(' (')[0].replace(' ', '_')}.csv")
        for k, w in W.items():
            w.to_csv(out / f"weights_{name.split(' (')[0].replace(' ', '_')}_{k.replace('/', '-').replace(' ', '_')}.csv")

    # ---- primary family
    pport = results[PRIMARY_REGION][0]
    rf = base["RF"]
    prim = test_family(pport, rf, list(HYPS.values()))
    prim = prim.join(holm(prim["p_value"]))
    prim.to_csv(out / "tests_primary_holm.csv", index=False)
    verdict = {}
    for h in HYPS.values():
        s = prim[(prim.hyp == h) & (prim.statistic == "Sharpe")].iloc[0]
        d = prim[(prim.hyp == h) & (prim.statistic == "MaxDD")].iloc[0]
        verdict[h] = "SUPPORTED" if (s.holm_reject_5pct and s["diff"] > 0 and d["diff"] >= 0) else "not supported"

    # ---- secondary family (other regions, Sharpe only)
    sec = []
    for name in ["Europe", "Japan", "Asia Pacific ex Japan"]:
        t = test_family(results[name][0], rf, list(HYPS.values()), ("sharpe",))
        t.insert(0, "region", name)
        sec.append(t)
    sec = pd.concat(sec, ignore_index=True)
    sec = sec.join(holm(sec["p_value"]))
    sec.to_csv(out / "tests_secondary_holm.csv", index=False)

    # ---- US exploratory incl. sub-periods
    usp = results["US (seen, exploratory)"][0]
    us_tests = pd.concat({lab: test_family(usp.loc[a:b], rf, list(HYPS.values()))
                          for lab, (a, b) in {"1973-latest": ("1973-01", None), "1973-1989": ("1973-01", "1989-12"),
                                              "1990-latest": ("1990-01", None)}.items()}, names=["period"])
    us_tests.to_csv(out / "tests_us_exploratory.csv")

    def tshow(t):
        d = t.copy()
        d["diff"] = [f"{v:+.2f}" if s == "Sharpe" else f"{v * 100:+.1f}pp" for v, s in zip(t["diff"], t.statistic)]
        d["95% CI"] = [f"[{lo:+.2f}, {hi:+.2f}]" if s == "Sharpe" else f"[{lo * 100:+.1f}, {hi * 100:+.1f}]pp"
                       for lo, hi, s in zip(t.ci_low, t.ci_high, t.statistic)]
        keep = [c for c in ["region", "test", "diff", "95% CI", "p_value", "holm_adj_p", "holm_reject_5pct"] if c in d]
        return d[keep].set_index(keep[0])

    names = {"Static 1/3": "Static 1/3 (control)", "H4a": "H4a Trend + cash", "H4b": "H4b Trend, cash fallback",
             "H5": "H5 Vol-managed equity"}
    report += ["## Verdicts: primary family (Developed ex US, Holm over 6 tests)", "",
               "\n".join(f"- **{k}**: {verdict[v]}" for k, v in HYPS.items()), "",
               "Supported = Sharpe difference vs Static 1/3 survives Holm at 5% with a positive sign AND "
               "the max drawdown is no worse.", "", md(tshow(prim)), ""]
    for name, (port, turn, W, rets) in results.items():
        st = stats_table(port, rf, turn)
        st["Avg cash"] = pd.Series({k: W[k]["CASH"].mean() for k in W})
        st.index = [names[i] for i in st.index]
        st.to_csv(out / f"summary_{name.split(' (')[0].replace(' ', '_')}.csv")
        report += [f"## Performance: {name}, {port.index[0]} to {port.index[-1]}", "", md(st, pct=pct), ""]
    report += ["## Secondary family: other regions, Sharpe difference vs Static 1/3 (Holm over 9)", "",
               md(tshow(sec)), "", "## US exploratory (data already seen in Study 2; no confirmatory claim)", "",
               md(tshow(us_tests.reset_index().assign(test=lambda d: d["period"] + ": " + d["test"])
                        .drop(columns="period"))), ""]

    # ---- robustness
    rob = []
    for vlab, v, c in (("Primary", "primary", cfg), ("R1 trend 12-1", "R1", cfg), ("R2 H5 uncapped", "R2", cfg),
                       ("R3 costs x2", "primary", cfg2)):
        for name, (eq_m, eq_d, start) in universes.items():
            p, _, _, _ = build(eq_m, eq_d, base, start, c, v)
            st = stats_table(p, rf)
            for h in HYPS.values():
                rob.append({"variant": vlab, "universe": name, "strategy": names[h],
                            "Sharpe": st.loc[h, "Sharpe"], "control Sharpe": st.loc["Static 1/3", "Sharpe"],
                            "MaxDD": f"{st.loc[h, 'MaxDD'] * 100:.1f}%",
                            "control MaxDD": f"{st.loc['Static 1/3', 'MaxDD'] * 100:.1f}%"})
    rob = pd.DataFrame(rob)
    rob.to_csv(out / "robustness.csv", index=False)
    report += ["## Robustness variants (all reported)", "", md(rob.set_index("variant")), ""]

    # ---- episodes
    for name, (port, *_ ) in results.items():
        ep = {}
        for en, (a, b) in cfg.episodes.items():
            sub = port.loc[a:b]
            if len(sub) and sub.index[0] == pd.Period(a, "M"):
                ep[en] = (1 + sub).prod() - 1
        if ep:
            e = pd.DataFrame(ep).T.rename(columns=names)
            e.to_csv(out / f"episodes_{name.split(' (')[0].replace(' ', '_')}.csv")
            report += [f"## Stress episodes: {name}", "", md(e, pct=list(e.columns)), ""]

    plot(results, out / "study3_performance.png", names)
    report += ["Chart: study3_performance.png"]
    (out / "report.md").write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))


def plot(results, path, names):
    colors = {"Static 1/3": "#2a78d6", "H4a": "#eb6834", "H4b": "#1baf7a", "H5": "#e87ba4"}
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharex="col")
    for col, uni in enumerate([PRIMARY_REGION, "US (seen, exploratory)"]):
        port = results[uni][0]
        x = port.index.to_timestamp()
        for k, c in colors.items():
            w = (1 + port[k]).cumprod()
            axes[0, col].plot(x, w, color=c, lw=1.8 if k != "Static 1/3" else 1.2, label=names[k])
            axes[1, col].plot(x, w / w.cummax() - 1, color=c, lw=1.2)
        axes[0, col].set_yscale("log")
        axes[0, col].set_title(f"{uni}: growth of $1 (log)", loc="left", fontsize=10)
        axes[1, col].set_title("Drawdown", loc="left", fontsize=10)
        for ax in axes[:, col]:
            ax.grid(color="#e6e5e0", lw=0.6)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
    axes[0, 0].legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()
