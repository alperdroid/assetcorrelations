"""Run the full study: data -> regimes -> descriptive analysis -> walk-forward backtest -> report.

    python run_study.py                 # download real data (cached in data/raw), write results/
    python run_study.py --refresh       # force re-download
    python run_study.py --industries 17 # Ken French 17-industry set instead of 12
    python run_study.py --synthetic     # offline smoke test on fake data (results meaningless)
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd

import analysis as A
from config import Config
from data import build_panels, load_raw
from portfolio import run_backtest
from regimes import build_regimes

ROOT = Path(__file__).resolve().parent


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--synthetic", action="store_true")
    p.add_argument("--industries", type=int, default=12, choices=[12, 17])
    p.add_argument("--oos-start", default=None)
    p.add_argument("--confirm", type=int, default=None, help="months a new regime must persist")
    p.add_argument("--sample-start", default=None, help="first return month, e.g. 1982-01")
    p.add_argument("--cost-mult", type=float, default=1.0, help="multiply all transaction costs")
    p.add_argument("--gold-avg", action="store_true",
                   help="ignore data/gold_override.csv and use World Bank monthly-average gold")
    p.add_argument("--no-interp", action="store_true",
                   help="do not interpolate internal macro gaps (e.g. Oct 2025 CPI/UNRATE)")
    p.add_argument("--avg-prices", action="store_true",
                   help="robustness: build ALL asset returns from monthly-average prices (like the gold series)")
    p.add_argument("--bootstrap", type=int, default=5000, help="block-bootstrap resamples (0 = skip)")
    p.add_argument("--out", default="results")
    args = p.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    cfg = Config(industries=args.industries)
    if args.oos_start:
        cfg.oos_start = args.oos_start
    if args.confirm:
        cfg.confirm_months = args.confirm
    if args.sample_start:
        cfg.sample_start = args.sample_start
    if args.cost_mult != 1.0:
        cfg.cost_bps = {k: v * args.cost_mult for k, v in cfg.cost_bps.items()}

    if args.synthetic:
        from synthetic import write_synthetic
        raw_dir = ROOT / "data_synthetic" / "raw"
        write_synthetic(raw_dir)
        cfg.industries = 12
        label = "SYNTHETIC TEST DATA - results are meaningless"
    else:
        raw_dir = ROOT / "data" / "raw"
        label = "free public data (Ken French, FRED, World Bank/WGC gold)"

    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)

    raw = load_raw(raw_dir, cfg.industries, refresh=args.refresh and not args.synthetic,
                   use_gold_override=not args.gold_avg, avg_prices=args.avg_prices)
    panels = build_panels(raw, interpolate_gaps=not args.no_interp, avg_prices=args.avg_prices)
    rets, inds = panels["returns"], panels["industries"]
    rets = rets.loc[cfg.sample_start:]
    logging.info("Return panel %s to %s, %d assets", rets.index[0], rets.index[-1], len(inds) + 2)

    regimes = build_regimes(panels["macro"], panels["daily"], cfg.corr_window_days,
                            cfg.zscore_min_periods, cfg.confirm_months, panels["interpolated"])
    regimes.to_csv(out / "regimes.csv")
    assets = inds + ["UST10", "GOLD", "MKT"]

    # ---- descriptive: the regime map
    freq = A.regime_frequency(regimes.loc[: rets.index[-1]], cfg.sample_start)
    freq.to_csv(out / "regime_frequency.csv")
    stats = A.regime_asset_stats(rets, regimes, assets)
    stats.to_csv(out / "regime_asset_stats.csv", index=False)
    stab, stab_detail = A.regime_stability(rets, regimes, assets)
    stab.to_csv(out / "regime_stability.csv", index=False)
    stab_detail.to_csv(out / "regime_stability_detail.csv", index=False)
    sb_by_regime = (regimes.loc[cfg.sample_start:].groupby("regime")["sb_corr"].describe())
    sb_by_regime.to_csv(out / "stock_bond_corr_by_regime.csv")
    ep_assets = A.episode_returns(rets[assets], cfg.episodes)
    ep_assets.to_csv(out / "episodes_assets.csv")

    A.plot_regimes(regimes.loc[: rets.index[-1]], cfg.sample_start, out / "regimes.png")
    A.plot_regime_heatmap(stats, out / "regime_sharpe_heatmap.png")

    # ---- walk-forward backtest
    logging.info("Running walk-forward backtest from %s ...", cfg.oos_start)
    port, turnover, weights = run_backtest(rets, regimes, inds, cfg)
    port.to_csv(out / "oos_returns.csv")
    for k, w in weights.items():
        w.to_csv(out / f"weights_{k.replace('/', '-').replace(' ', '_').replace('.', '')}.csv")

    rf = rets["RF"]
    summary = A.summary_table(port, rf, turnover)
    summary.to_csv(out / "oos_summary.csv")
    ep_strat = A.episode_returns(port, {k: v for k, v in cfg.episodes.items()
                                        if pd.Period(v[0], "M") >= pd.Period(cfg.oos_start, "M")})
    ep_strat.to_csv(out / "episodes_strategies.csv")

    robust = pd.DataFrame({s: A.summary_table(port.loc[s:], rf)["Sharpe"] for s in cfg.robustness_starts
                           if pd.Period(s, "M") >= port.index[0]})
    robust.columns = [f"from {c}" for c in robust.columns]
    robust.to_csv(out / "robustness_sharpe.csv")

    ann = lambda s: (1 + s).prod() ** (12 / len(s)) - 1
    regime_value = ann(port["Regime Tilt"]) - ann(port["Uncond. Tilt"])
    detection_cost = ann(port["Oracle Tilt"]) - ann(port["Regime Tilt"])

    pd.DataFrame({
        "value": {"regime_value_ann": regime_value, "detection_cost_ann": detection_cost,
                  "sample_start": str(rets.index[0]), "sample_end": str(rets.index[-1]),
                  "oos_start": cfg.oos_start, "industries": cfg.industries,
                  "confirm_months": cfg.confirm_months, "cost_bps": str(cfg.cost_bps),
                  "gold_source": panels["gold_source"],
                  "price_basis": "monthly averages (all assets)" if args.avg_prices else "month-end (gold: average)",
                  "interpolated": "; ".join(f"{k}: {', '.join(str(m) for m, _ in v)}"
                                            for k, v in panels["interpolated"].items()) or "none"}}).to_csv(out / "headline.csv")
    rf.loc[port.index].to_csv(out / "rf.csv")

    if args.bootstrap > 0:
        from significance import significance_table
        sig = significance_table(port, rf.loc[port.index], n_boot=args.bootstrap)
        sig.to_csv(out / "significance.csv", index=False)

    A.plot_wealth(port, out / "oos_performance.png")
    A.plot_weights(_group_weights(weights["Regime Tilt"], inds), regimes, out / "weights_regime_tilt.png",
                   "Regime Tilt: weights over time")

    A.write_report(out / "summary.md", {
        "data_label": label + f"; regime confirmation = {cfg.confirm_months} month(s)"
                      + ("; ALL asset returns from monthly-average prices" if args.avg_prices else ""), "sample": f"{rets.index[0]} to {rets.index[-1]}", "oos": cfg.oos_start,
        "gold_source": panels["gold_source"], "freq": freq, "summary": summary,
        "regime_value": regime_value, "detection_cost": detection_cost,
        "episodes_strat": ep_strat, "episodes_assets": ep_assets, "stability": stab, "robust": robust,
    })
    logging.info("Done. Results in %s", out)


def _group_weights(w: pd.DataFrame, inds: list[str]) -> pd.DataFrame:
    """Keep sector detail but order columns: Treasury, gold, then sectors."""
    return w[["UST10", "GOLD"] + inds]


if __name__ == "__main__":
    main()
