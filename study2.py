"""Study 2: pre-registered rule-based hedging strategies (see PREREGISTRATION.md).

    python study2.py                  # primary specs + all robustness variants -> results_study2/
    python study2.py --synthetic      # offline smoke test (results meaningless)

Every rule is a fixed formula with no estimation window. Weights for return month t use only
information available at the end of month t-1.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis import perf_stats
from config import Config
from data import build_panels, load_raw
from portfolio import _drift, _trade
from regimes import stock_bond_corr
from significance import bootstrap_diff

ROOT = Path(__file__).resolve().parent
EVAL_START, EVAL_END = "1973-01", None
SUBPERIODS = {"1973-1989 (unseen)": ("1973-01", "1989-12"), "1990-latest (seen in Study 1)": ("1990-01", None)}
THREE = ["MKT", "UST10", "GOLD"]
BOOT = dict(n_boot=5000, block=12.0, seed=20260101)
PRIMARY = {  # hypothesis -> (strategy column, control column)
    "H1 bond-hedge switch": ("H1 Bond-hedge switch", "Static 1/3"),
    "H2a trend overlay (3 assets)": ("H2a Trend 3-asset", "Static 1/3"),
    "H2b trend overlay (sectors)": ("H2b Trend sectors", "EW 14 assets"),
    "H3 volatility-managed equity": ("H3 Vol-managed equity", "Static 1/3"),
}


# --------------------------------------------------------------------------- signals (index = return month t)
def trailing_excess_pass(rets: pd.DataFrame, rf: pd.Series, months: int, skip: int) -> pd.DataFrame:
    """At return month t: True if the asset's compounded return over months
    t-months-skip .. t-1-skip beats compounded T-bills over the same months
    (skip=0: t-12..t-1; skip=1: t-13..t-2). NaN where the window is incomplete."""
    gr = np.log1p(rets).rolling(months, min_periods=months).sum()
    grf = np.log1p(rf).rolling(months, min_periods=months).sum()
    ex = gr.sub(grf, axis=0).shift(1 + skip)          # value at t uses months up to t-1-skip
    out = ex > 0
    return out.where(ex.notna())


def realized_variance(daily_mkt: pd.Series) -> pd.DataFrame:
    rv = (daily_mkt ** 2).groupby(daily_mkt.index.to_period("M")).sum()
    target = rv.expanding().mean()                    # real-time: mean of RV up to and including that month
    return pd.DataFrame({"rv": rv, "target": target}).shift(1)   # value at t uses month t-1


# --------------------------------------------------------------------------- weight rules
def w_static(index, assets, weights) -> pd.DataFrame:
    return pd.DataFrame([weights] * len(index), index=index, columns=assets)


def w_bond_switch(sb_prev: pd.Series, index) -> pd.DataFrame:
    w = w_static(index, THREE, [1 / 3, 1 / 3, 1 / 3])
    pos = (sb_prev.reindex(index) > 0).values
    w.loc[pos, :] = [1 / 3, 0.0, 2 / 3]
    return w


def w_trend(passes: pd.DataFrame, assets: list[str], fallback: str = "UST10") -> pd.DataFrame:
    n = len(assets)
    base = np.full(n, 1.0 / n)
    rows = []
    for t, p in passes[assets].iterrows():
        if p.isna().any():                            # incomplete history -> control weights
            rows.append(base)
            continue
        ok = p.values.astype(bool)
        if not ok.any():
            w = np.zeros(n)
            w[assets.index(fallback)] = 1.0
        else:
            w = np.where(ok, base + base[~ok].sum() / ok.sum(), 0.0)
        rows.append(w)
    return pd.DataFrame(rows, index=passes.index, columns=assets)


def w_vol_managed(rvt: pd.DataFrame, index, cap: float | None = 2 / 3) -> pd.DataFrame:
    x = rvt.reindex(index)
    w_eq = (1 / 3) * x["target"] / x["rv"]
    w_eq = w_eq.clip(0, cap if cap is not None else 1.0).fillna(1 / 3)
    rest = (1 - w_eq) / 2
    return pd.DataFrame({"MKT": w_eq, "UST10": rest, "GOLD": rest}, index=index)


# --------------------------------------------------------------------------- backtest
def simulate(w: pd.DataFrame, rets: pd.DataFrame, cfg: Config) -> tuple[pd.Series, pd.Series]:
    costs = np.array([cfg.cost_bps.get(a, cfg.cost_bps["equity"]) for a in w.columns]) / 1e4
    prev, out, to = None, [], []
    R = rets.loc[w.index, w.columns].values
    for i, wt in enumerate(w.values):
        assert abs(wt.sum() - 1) < 1e-9 and (wt >= -1e-12).all()
        turn, cost = _trade(prev, wt, costs)
        out.append(float(wt @ R[i]) - cost)
        to.append(turn)
        prev = _drift(wt, R[i])
    return pd.Series(out, index=w.index), pd.Series(to, index=w.index)


def build_all(panels, raw, cfg, variant: str = "primary") -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    rets = panels["returns"].loc[cfg.sample_start:]
    inds = panels["industries"]
    idx = rets.loc[EVAL_START:EVAL_END].index
    rf = rets["RF"]
    sb_win = 252 if variant == "R1" else cfg.corr_window_days
    sb = stock_bond_corr(panels["daily"], sb_win)
    months, skip = (10, 0) if variant == "R3" else ((12, 1) if variant == "R2" else (12, 0))
    sec = inds + ["UST10", "GOLD"]
    trend3 = trailing_excess_pass(rets[THREE], rf, months, skip).reindex(idx)
    trend14 = trailing_excess_pass(rets[sec], rf, months, skip).reindex(idx)
    daily_mkt = raw["ff3_d"]["Mkt-RF"] + raw["ff3_d"]["RF"]
    rvt = realized_variance(daily_mkt)

    W = {
        "60/40": w_static(idx, THREE, [0.6, 0.4, 0.0]),
        "Static 1/3": w_static(idx, THREE, [1 / 3, 1 / 3, 1 / 3]),
        "EW 14 assets": w_static(idx, sec, [1 / len(sec)] * len(sec)),
        "H1 Bond-hedge switch": w_bond_switch(sb.shift(1), idx),
        "H2a Trend 3-asset": w_trend(trend3, THREE),
        "H2b Trend sectors": w_trend(trend14, sec),
        "H3 Vol-managed equity": w_vol_managed(rvt, idx, cap=None if variant == "R4" else 2 / 3),
    }
    port, turn = {}, {}
    for k, w in W.items():
        port[k], turn[k] = simulate(w, rets, cfg)
    return pd.DataFrame(port), pd.DataFrame(turn), W


# --------------------------------------------------------------------------- reporting
def stats_table(port, rf, turn=None):
    t = pd.DataFrame({k: perf_stats(port[k], rf) for k in port}).T
    if turn is not None:
        t["Turnover/m"] = turn.mean()
    return t


def holm(p: pd.Series, alpha=0.05) -> pd.Series:
    order = p.sort_values().index
    m, reject, still = len(p), {}, True
    for i, k in enumerate(order):
        still = still and p[k] <= alpha / (m - i)
        reject[k] = still
    adj = pd.Series(np.minimum(1, np.maximum.accumulate([p[k] * (m - i) for i, k in enumerate(order)])), index=order)
    return pd.DataFrame({"holm_reject_5pct": pd.Series(reject), "holm_adj_p": adj})


def tests(port, rf, window=None) -> pd.DataFrame:
    p = port.loc[slice(*window)] if window else port
    r = rf.reindex(p.index).values
    rows = []
    for h, (a, b) in PRIMARY.items():
        for stat, lab in (("sharpe", "Sharpe"), ("maxdd", "MaxDD")):
            res = bootstrap_diff(p[a].values, p[b].values, r, stat, **BOOT)
            rows.append({"hypothesis": h, "strategy": a, "control": b, "statistic": lab, **res})
    return pd.DataFrame(rows)


def md(df: pd.DataFrame, pct=(), f2=()) -> str:
    d = df.copy()
    for c in d.columns:
        if c in pct:
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v * 100:.1f}%")
        elif c in f2 or pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:.2f}")
    cols = [str(d.index.name or "")] + list(map(str, d.columns))
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join([str(i)] + [str(v) for v in r]) + " |" for i, r in zip(d.index, d.values)]
    return "\n".join(lines)


COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7"]


def plot(port, path):
    cols = ["Static 1/3", "60/40", "H1 Bond-hedge switch", "H2a Trend 3-asset", "H3 Vol-managed equity",
            "H2b Trend sectors", "EW 14 assets"]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
    x = port.index.to_timestamp()
    for c, col in zip(cols, COLORS):
        w = (1 + port[c]).cumprod()
        a1.plot(x, w, color=col, lw=2.0 if c.startswith("H") else 1.2, label=c)
        a2.plot(x, w / w.cummax() - 1, color=col, lw=1.4 if c.startswith("H") else 1.0)
    a1.set_yscale("log")
    a1.set_ylabel("Growth of $1 (log)")
    a2.set_ylabel("Drawdown")
    a1.legend(fontsize=8, ncol=4, frameon=False)
    a1.set_title("Study 2: pre-registered strategies, 1973-01 onward (after costs)", loc="left")
    for ax in (a1, a2):
        ax.grid(color="#e6e5e0", lw=0.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--out", default="results_study2")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg = Config()
    if args.synthetic:
        from synthetic import write_synthetic
        raw_dir = ROOT / "data_synthetic" / "raw"
        write_synthetic(raw_dir)
    else:
        raw_dir = ROOT / "data" / "raw"
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)

    raw = load_raw(raw_dir, 12, use_gold_override=False, avg_prices=not args.synthetic)
    panels = build_panels(raw)
    rf = panels["returns"]["RF"]

    port, turn, W = build_all(panels, raw, cfg)
    port.to_csv(out / "returns_primary.csv")
    for k, w in W.items():
        w.to_csv(out / f"weights_{k.replace('/', '-').replace(' ', '_')}.csv")
    full = stats_table(port, rf, turn)
    full.to_csv(out / "summary_full.csv")
    subs = {name: stats_table(port.loc[a:b], rf) for name, (a, b) in SUBPERIODS.items()}
    for name, t in subs.items():
        t.to_csv(out / f"summary_{name.split(' ')[0]}.csv")

    tst = tests(port, rf)
    tst = tst.join(holm(tst["p_value"]), how="left")
    tst.to_csv(out / "tests_primary_holm.csv", index=False)
    sub_tests = pd.concat({name: tests(port, rf, (a, b)) for name, (a, b) in SUBPERIODS.items()}, names=["period"])
    sub_tests.to_csv(out / "tests_subperiods.csv")

    verdict = {}
    for h, (a, b) in PRIMARY.items():
        s = tst[(tst.hypothesis == h) & (tst.statistic == "Sharpe")].iloc[0]
        d = tst[(tst.hypothesis == h) & (tst.statistic == "MaxDD")].iloc[0]
        verdict[h] = ("SUPPORTED" if (s.holm_reject_5pct and s["diff"] > 0 and d["diff"] >= 0)
                      else "not supported")

    # robustness variants
    rob_rows = []
    variants = {"R1": "H1 252-day window", "R2": "Trend 12-1 (skip month)", "R3": "Trend 10-month",
                "R4": "H3 uncapped"}
    for v, label in variants.items():
        pv, tv, _ = build_all(panels, raw, cfg, v)
        rob_rows.append((label, pv, tv))
    if not args.synthetic:
        raw_a = load_raw(raw_dir, 12, use_gold_override=False, avg_prices=True)
        pa, ta, _ = build_all(build_panels(raw_a, avg_prices=True), raw_a, cfg)
        rob_rows.append(("All assets on monthly averages", pa, ta))
    cfg2 = Config()
    cfg2.cost_bps = {k: 2 * v for k, v in cfg.cost_bps.items()}
    pc, tc, _ = build_all(panels, raw, cfg2)
    rob_rows.append(("Costs x2", pc, tc))
    rob = []
    for label, pv, tv in [("Primary", port, turn)] + rob_rows:
        st = stats_table(pv, rf, tv)
        for h, (a, b) in PRIMARY.items():
            rob.append({"variant": label, "hypothesis": h, "Sharpe": st.loc[a, "Sharpe"],
                        "control Sharpe": st.loc[b, "Sharpe"], "MaxDD": st.loc[a, "MaxDD"],
                        "control MaxDD": st.loc[b, "MaxDD"], "CAGR": st.loc[a, "CAGR"],
                        "control CAGR": st.loc[b, "CAGR"]})
    rob = pd.DataFrame(rob)
    rob.to_csv(out / "robustness.csv", index=False)

    ep = {}
    for name, (a, b) in cfg.episodes.items():
        sub = port.loc[a:b]
        if len(sub) and sub.index[0] == pd.Period(a, "M"):
            ep[name] = (1 + sub).prod() - 1
    ep = pd.DataFrame(ep).T
    ep.to_csv(out / "episodes.csv")
    plot(port, out / "study2_performance.png")

    pct = ["CAGR", "Vol", "MaxDD", "Worst month", "CVaR 5% (monthly)", "Turnover/m"]
    tshow = tst.copy()
    tshow["diff"] = [f"{d:+.2f}" if s == "Sharpe" else f"{d * 100:+.1f}pp" for d, s in zip(tshow["diff"], tshow.statistic)]
    tshow["95% CI"] = [f"[{lo:+.2f}, {hi:+.2f}]" if s == "Sharpe" else f"[{lo * 100:+.1f}, {hi * 100:+.1f}]pp"
                       for lo, hi, s in zip(tst.ci_low, tst.ci_high, tst.statistic)]
    tshow = tshow.set_index("hypothesis")[["control", "statistic", "diff", "95% CI", "p_value", "holm_adj_p", "holm_reject_5pct"]]
    st_sub = sub_tests.reset_index()
    st_sub = st_sub[st_sub.statistic == "Sharpe"].pivot(index="hypothesis", columns="period", values=["diff", "p_value"])
    st_sub.columns = [f"{a} {b}" for a, b in st_sub.columns]
    robshow = rob.copy()
    for c in ("MaxDD", "control MaxDD", "CAGR", "control CAGR"):
        robshow[c] = robshow[c].map(lambda v: f"{v * 100:.1f}%")
    rep = [
        "# Study 2 results: pre-registered rule-based hedging strategies", "",
        "Specification: `PREREGISTRATION.md` (committed before any code or run). Evaluation: return months "
        f"{port.index[0]} to {port.index[-1]}, after costs. Gold = World Bank monthly average.", "",
        "## Verdicts (Holm-corrected, 8 tests)", "",
        "\n".join(f"- **{h}**: {v}" for h, v in verdict.items()), "",
        "Rule: supported only if the Sharpe difference vs control survives Holm at 5% with a positive "
        "sign AND the max drawdown is no worse than the control.", "",
        "## Primary tests, 1973-latest", "", md(tshow), "",
        "## Performance, 1973-latest", "", md(full, pct=pct), "",
    ]
    for name, t in subs.items():
        rep += [f"## Performance, {name}", "", md(t, pct=pct), ""]
    rep += ["## Sharpe difference vs control by sub-period (bootstrap p, not Holm-corrected)", "",
            md(st_sub), "",
            "## Robustness variants (all reported)", "", md(robshow.set_index("variant")), "",
            "## Stress episodes (cumulative return)", "", md(ep, pct=list(ep.columns)), "",
            "Chart: study2_performance.png"]
    (out / "report.md").write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
