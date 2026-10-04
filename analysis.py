"""Tables, charts and the markdown summary."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from regimes import REGIME_ORDER

REGIME_COLORS = dict(zip(REGIME_ORDER, ["#cfe8cf", "#fde3b0", "#f4b6b6", "#c9d9f2"]))


# --------------------------------------------------------------------------- metrics
def perf_stats(r: pd.Series, rf: pd.Series) -> dict:
    r = r.dropna()
    rf = rf.reindex(r.index)
    wealth = (1 + r).cumprod()
    years = len(r) / 12
    cagr = wealth.iloc[-1] ** (1 / years) - 1
    vol = r.std() * np.sqrt(12)
    ex = r - rf
    sharpe = ex.mean() / r.std() * np.sqrt(12) if r.std() > 0 else np.nan
    dd = wealth / wealth.cummax() - 1
    mdd = dd.min()
    var5 = r.quantile(0.05)
    cvar5 = r[r <= var5].mean()
    return {"CAGR": cagr, "Vol": vol, "Sharpe": sharpe, "MaxDD": mdd,
            "Calmar": cagr / abs(mdd) if mdd < 0 else np.nan,
            "Worst month": r.min(), "CVaR 5% (monthly)": cvar5, "Months": len(r)}


def summary_table(port: pd.DataFrame, rf: pd.Series, turnover: pd.DataFrame | None = None) -> pd.DataFrame:
    tab = pd.DataFrame({k: perf_stats(port[k], rf) for k in port.columns}).T
    tab["Months"] = tab["Months"].astype(int)
    if turnover is not None:
        tab["Avg monthly turnover"] = turnover.mean()
    return tab


def episode_returns(df: pd.DataFrame, episodes: dict) -> pd.DataFrame:
    out = {}
    for name, (a, b) in episodes.items():
        sub = df.loc[a:b]
        if len(sub) == 0 or sub.index[0] > pd.Period(a, "M") or sub.index[-1] < pd.Period(b, "M"):
            continue
        out[name] = (1 + sub).prod() - 1
    return pd.DataFrame(out).T


# --------------------------------------------------------------------------- regime analysis
def regime_asset_stats(rets: pd.DataFrame, regimes: pd.DataFrame, assets: list[str]) -> pd.DataFrame:
    """Per-asset, per-regime stats, pairing the real-time label at s with returns in s+1."""
    lab = regimes["regime"].shift(1).reindex(rets.index)
    rows = []
    for reg in REGIME_ORDER:
        sub = rets[lab == reg]
        if len(sub) < 6:
            continue
        ex = sub[assets].sub(sub["RF"], axis=0)
        for a in assets:
            rows.append({
                "regime": reg, "asset": a, "months": len(sub),
                "ann_excess_return": ex[a].mean() * 12,
                "ann_vol": sub[a].std() * np.sqrt(12),
                "sharpe": ex[a].mean() / sub[a].std() * np.sqrt(12),
                "corr_with_market": sub[a].corr(sub["MKT"]),
                "corr_with_ust10": sub[a].corr(sub["UST10"]),
                "downside_corr_market": sub.loc[sub["MKT"] < 0, a].corr(sub.loc[sub["MKT"] < 0, "MKT"]),
                "hit_rate": (ex[a] > 0).mean(),
            })
    return pd.DataFrame(rows)


def regime_stability(rets, regimes, assets, split="1989-12"):
    """Do assets rank the same way within each regime before and after the split?"""
    a = regime_asset_stats(rets.loc[:split], regimes, assets)
    b = regime_asset_stats(rets.loc[pd.Period(split, "M") + 1:], regimes, assets)
    rows = []
    for reg in REGIME_ORDER:
        sa = a[a.regime == reg].set_index("asset")["sharpe"]
        sb = b[b.regime == reg].set_index("asset")["sharpe"]
        common = sa.index.intersection(sb.index)
        if len(common) < 3:
            continue
        rows.append({"regime": reg, "months_pre": int(a[a.regime == reg]["months"].iloc[0]),
                     "months_post": int(b[b.regime == reg]["months"].iloc[0]),
                     "rank_corr_sharpe": sa[common].rank().corr(sb[common].rank())})
    detail = a.merge(b, on=["regime", "asset"], suffixes=("_pre", "_post"))[
        ["regime", "asset", "sharpe_pre", "sharpe_post", "corr_with_market_pre", "corr_with_market_post"]]
    return pd.DataFrame(rows), detail


def regime_frequency(regimes: pd.DataFrame, start: str) -> pd.DataFrame:
    r = regimes.loc[start:]
    freq = r["regime"].value_counts().reindex(REGIME_ORDER).rename("months").to_frame()
    switches = (r["regime"] != r["regime"].shift()).sum() - 1
    freq["share"] = freq["months"] / freq["months"].sum()
    freq.attrs["switches"] = int(switches)
    agree = (r["regime"] == r["regime_oracle"]).mean()
    freq.attrs["realtime_vs_oracle_agreement"] = float(agree)
    return freq


# --------------------------------------------------------------------------- charts
def _shade(ax, labels: pd.Series):
    labels = labels.dropna()
    if labels.empty:
        return
    start, cur = labels.index[0], labels.iloc[0]
    for p, v in list(labels.items())[1:] + [(labels.index[-1] + 1, None)]:
        if v != cur:
            ax.axvspan(start.to_timestamp(), p.to_timestamp(), color=REGIME_COLORS.get(cur, "#eee"), lw=0)
            start, cur = p, v


def plot_regimes(regimes, start, path):
    r = regimes.loc[start:]
    fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    for ax in axes:
        _shade(ax, r["regime"])
    x = r.index.to_timestamp()
    axes[0].plot(x, r["cpi_yoy"] * 100, color="k", lw=1)
    axes[0].set_ylabel("CPI YoY %")
    axes[1].plot(x, r["growth_score"], color="k", lw=1)
    axes[1].axhline(0, color="grey", lw=0.5)
    axes[1].set_ylabel("Growth score")
    axes[2].plot(x, r["sb_corr"], color="k", lw=1)
    axes[2].axhline(0, color="grey", lw=0.5)
    axes[2].set_ylabel("Stock-bond corr (63d)")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in REGIME_COLORS.values()]
    axes[0].legend(handles, REGIME_COLORS.keys(), loc="upper right", fontsize=8, ncol=2)
    axes[0].set_title("Real-time macro regimes")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_wealth(port, path):
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
    x = port.index.to_timestamp()
    for k in port.columns:
        w = (1 + port[k]).cumprod()
        a1.plot(x, w, label=k, lw=1.6 if "Regime" in k else 1)
        a2.plot(x, w / w.cummax() - 1, lw=1.6 if "Regime" in k else 1)
    a1.set_yscale("log")
    a1.set_ylabel("Growth of $1 (log)")
    a1.legend(fontsize=8, ncol=4)
    a2.set_ylabel("Drawdown")
    a1.set_title("Out-of-sample performance")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_weights(w: pd.DataFrame, regimes, path, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    x = w.index.to_timestamp()
    ax.stackplot(x, w.T.values, labels=w.columns, alpha=0.9)
    ax.set_ylim(0, 1)
    ax.set_title(title)
    ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_regime_heatmap(stats: pd.DataFrame, path):
    piv = stats.pivot(index="asset", columns="regime", values="sharpe")[
        [r for r in REGIME_ORDER if r in stats.regime.unique()]]
    fig, ax = plt.subplots(figsize=(10, 0.45 * len(piv) + 1.5))
    v = np.nanmax(np.abs(piv.values))
    im = ax.imshow(piv.values, cmap="RdYlGn", vmin=-v, vmax=v, aspect="auto")
    ax.set_xticks(range(piv.shape[1]), piv.columns, rotation=20, ha="right", fontsize=8)
    ax.set_yticks(range(piv.shape[0]), piv.index, fontsize=8)
    for i in range(piv.shape[0]):
        for j in range(piv.shape[1]):
            ax.text(j, i, f"{piv.values[i, j]:.2f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, label="Sharpe ratio (annualized)")
    ax.set_title("Sharpe ratio by real-time regime, full sample")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


# --------------------------------------------------------------------------- report
def _md(df: pd.DataFrame, pct_cols=(), fmt="{:.2f}") -> str:
    d = df.copy()
    for c in d.columns:
        if c in pct_cols:
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v * 100:.1f}%")
        elif pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else fmt.format(v))
    cols = [str(d.index.name or "")] + [str(c) for c in d.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for idx, row in d.iterrows():
        lines.append("| " + " | ".join([str(idx)] + [str(v) for v in row.values]) + " |")
    return "\n".join(lines)


def write_report(path: Path, ctx: dict):
    pct = ["CAGR", "Vol", "MaxDD", "Worst month", "CVaR 5% (monthly)", "Avg monthly turnover"]
    s = [
        "# Regime-aware bonds / gold / equity-sector allocation: results",
        "",
        f"Data run: {ctx['data_label']}. Return sample {ctx['sample']}; out-of-sample from {ctx['oos']}.",
        f"Gold price source: {ctx['gold_source']}.",
        "",
        "## 1. Regime frequency (real-time labels)",
        _md(ctx["freq"], pct_cols=["share"]),
        "",
        f"Regime switches: {ctx['freq'].attrs['switches']}. "
        f"Real-time label equals oracle label in {ctx['freq'].attrs['realtime_vs_oracle_agreement']:.0%} of months.",
        "",
        "## 2. Out-of-sample performance",
        _md(ctx["summary"], pct_cols=pct),
        "",
        f"Value of the regime map (Regime Tilt minus Uncond. Tilt), annualized: {ctx['regime_value']:+.2%}.  ",
        f"Cost of detection lag (Oracle Tilt minus Regime Tilt), annualized: {ctx['detection_cost']:+.2%}.",
        "",
        "## 3. Stress episodes (strategies, cumulative return)",
        _md(ctx["episodes_strat"], pct_cols=list(ctx["episodes_strat"].columns)),
        "",
        "## 4. Stress episodes (individual assets, cumulative return)",
        _md(ctx["episodes_assets"], pct_cols=list(ctx["episodes_assets"].columns)),
        "",
        "## 5. Stability of the regime map (1972-1989 vs 1990-latest)",
        "Spearman rank correlation of asset Sharpe ratios within each regime. Values near 1 mean the "
        "same assets win in that regime in both eras; values near 0 mean the map is not stable.",
        "",
        _md(ctx["stability"].set_index("regime")),
        "",
        "## 6. Sub-period robustness (Sharpe ratio by out-of-sample start)",
        _md(ctx["robust"]),
        "",
        "Charts: regimes.png, regime_sharpe_heatmap.png, oos_performance.png, weights_regime_tilt.png.",
        "Full tables: CSV files in this folder.",
    ]
    path.write_text("\n".join(s), encoding="utf-8")
