"""Collect every run folder into results/robustness_summary.md (one table, all runs, nothing dropped).

    python summarize_runs.py                       # default run list below
    python summarize_runs.py results_main results_x --out results/robustness_summary.md
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
RUNS = {
    "results_main": "Main (default settings)",
    "results_gold_avg": "World Bank average gold",
    "results_ind17": "17 industries",
    "results_confirm2": "Regime confirmation 2 months",
    "results_oos2000": "OOS start 2000-01",
    "results_start1982": "Sample 1982-, OOS 2000-01",
    "results_costx2": "Transaction costs x2",
    "results_gap_asis": "Oct-2025 gap not interpolated",
    "results_all_avg": "All assets on monthly-average prices",
}
STRATS = ["Regime Tilt", "Uncond. Tilt", "Regime ERC", "Uncond. ERC", "Oracle Tilt", "60/40", "Static 1/3"]


def load(run: Path):
    s = pd.read_csv(run / "oos_summary.csv", index_col=0)
    h = pd.read_csv(run / "headline.csv", index_col=0)["value"]
    sig = pd.read_csv(run / "significance.csv") if (run / "significance.csv").exists() else None
    return s, h, sig


def main():
    p = argparse.ArgumentParser()
    p.add_argument("runs", nargs="*")
    p.add_argument("--out", default="results/robustness_summary.md")
    args = p.parse_args()
    runs = {r: RUNS.get(r, r) for r in (args.runs or RUNS)}

    head_rows, long_rows, sig_rows, missing = [], [], [], []
    for r, label in runs.items():
        path = ROOT / r
        if not (path / "oos_summary.csv").exists():
            missing.append(r)
            continue
        s, h, sig = load(path)
        rt, ut = s.loc["Regime Tilt"], s.loc["Uncond. Tilt"]
        head_rows.append({
            "run": label, "folder": r, "OOS": f"{h['oos_start']} to {h['sample_end']}",
            "gold": "avg" if "average" in str(h["gold_source"]) else "month-end",
            "RT Sharpe": f"{rt['Sharpe']:.2f}", "UT Sharpe": f"{ut['Sharpe']:.2f}",
            "60/40 Sharpe": f"{s.loc['60/40', 'Sharpe']:.2f}",
            "RT MaxDD": f"{rt['MaxDD']:.1%}", "UT MaxDD": f"{ut['MaxDD']:.1%}",
            "60/40 MaxDD": f"{s.loc['60/40', 'MaxDD']:.1%}",
            "RT CAGR": f"{rt['CAGR']:.2%}", "UT CAGR": f"{ut['CAGR']:.2%}",
            "Value of regime map": f"{float(h['regime_value_ann']):+.2%}",
            "Cost of detection lag": f"{float(h['detection_cost_ann']):+.2%}",
        })
        for k in STRATS:
            if k in s.index:
                long_rows.append({"run": label, "strategy": k, "Sharpe": f"{s.loc[k, 'Sharpe']:.2f}",
                                  "MaxDD": f"{s.loc[k, 'MaxDD']:.1%}", "CAGR": f"{s.loc[k, 'CAGR']:.2%}",
                                  "Vol": f"{s.loc[k, 'Vol']:.1%}",
                                  "Turnover/m": f"{s.loc[k, 'Avg monthly turnover']:.1%}"})
        if sig is not None:
            for _, x in sig.iterrows():
                fmt = (lambda v: f"{v:+.2f}") if x["statistic"] == "Sharpe ratio" else (lambda v: f"{v:+.1%}")
                sig_rows.append({"run": label, "test": f"{x['strategy']} - {x['versus']}: {x['statistic']}",
                                 "diff": fmt(x["diff"]), "95% CI": f"[{fmt(x['ci_low'])}, {fmt(x['ci_high'])}]",
                                 "p-value": f"{x['p_value']:.3f}"})

    md = ["# Robustness summary: all runs", "",
          "RT = Regime Tilt (main strategy), UT = Uncond. Tilt (same machinery, no regime information). "
          "Value of the regime map = CAGR(RT) - CAGR(UT); cost of detection lag = CAGR(Oracle Tilt) - CAGR(RT). "
          "All figures are out-of-sample, after transaction costs. Every run is reported, favourable or not.", ""]
    if missing:
        md += [f"Runs not found (not run or failed): {', '.join(missing)}", ""]
    md += ["## Headline", "", _md(pd.DataFrame(head_rows)), "",
           "## All strategies, all runs", "", _md(pd.DataFrame(long_rows)), ""]
    if sig_rows:
        md += ["## Block-bootstrap tests (stationary bootstrap, mean block 12 months, 5,000 resamples)", "",
               "Max-drawdown difference > 0 means Regime Tilt's drawdown was shallower.", "",
               _md(pd.DataFrame(sig_rows)), ""]
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


def _md(df: pd.DataFrame) -> str:
    if df.empty:
        return "(none)"
    lines = ["| " + " | ".join(df.columns) + " |", "|" + "---|" * len(df.columns)]
    lines += ["| " + " | ".join(str(v) for v in row) + " |" for row in df.values]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
