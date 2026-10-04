"""Build site/hedge_lab.html: inject the study's monthly data into site/template.html.

    python site/build_site.py

Data: monthly returns 1972-01..latest for the US market, 12 Ken French industries, the 10y Treasury
(from DGS10), gold (World Bank monthly average) and T-bills, plus the real-time regime label known at
the end of the previous month. Strategy points for the risk map come from results/report_strategies_1990.csv.
"""
import json
import sys

import numpy as np
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from data import build_panels, load_raw  # noqa: E402

p = build_panels(load_raw(ROOT / "data" / "raw", 12))
R = p["returns"].loc["1972-01":]
inds = p["industries"]
reg = pd.read_csv(ROOT / "results_main" / "regimes.csv", index_col=0)
reg.index = pd.PeriodIndex(reg.index, freq="M")
lab = reg["regime"].shift(1).reindex(R.index)
short = {"Goldilocks (G+ I-)": "G", "Reflation (G+ I+)": "R", "Stagflation (G- I+)": "S",
         "Disinflationary slowdown (G- I-)": "D"}
cols = ["MKT", "UST10", "GOLD", "RF"] + inds
data = {
    "start": str(R.index[0]), "end": str(R.index[-1]),
    "sectors": inds,
    "series": {c: [round(float(v), 5) for v in R[c].values] for c in cols},
    "regime": "".join(short.get(x, "-") if isinstance(x, str) else "-" for x in lab.values),
}
st = pd.read_csv(ROOT / "results" / "report_strategies_1990.csv", index_col=0)
data["strategies"] = [{"name": k, "dd": round(float(r["MaxDD"]), 4), "sr": round(float(r["Sharpe"]), 3),
                       "cagr": round(float(r["CAGR"]), 4)} for k, r in st.iterrows()]

# ---- Study 5 (forecasting horse race): summary + pre-registered conditioning rules
s5 = ROOT / "results_study5"
if (s5 / "scores.csv").exists():
    sc = pd.read_csv(s5 / "scores.csv")
    cur = json.loads((s5 / "current_forecasts.json").read_text())
    rs = json.loads((s5 / "regime_classifier.json").read_text())
    h2h = pd.read_csv(s5 / "head_to_head_regimeRF_vs_RF.csv")
    econ = pd.read_csv(s5 / "economic_tests.csv")
    label = {"ret1_MKT": "US stocks, next month", "ret1_UST10": "Treasuries, next month", "ret1_GOLD": "Gold, next month",
             "ret12_MKT": "US stocks, next 12 months", "ret12_UST10": "Treasuries, next 12 months",
             "ret12_GOLD": "Gold, next 12 months", "lrv_mkt": "Stock volatility, next month",
             "lrv_ust": "Treasury volatility, next month", "sbc3": "Stock-bond correlation, next 3 months"}
    rows = []
    for tgt, g in sc.groupby("target", sort=False):
        best = g.sort_values("r2_os", ascending=False).iloc[0]
        passing = g[(g.holm_reject_5pct.astype(bool)) & (g.r2_os > 0)].sort_values("r2_os", ascending=False)
        rows.append({"target": tgt, "label": label[tgt], "family": best.family, "best": best.model,
                     "best_r2": round(float(best.r2_os), 4), "n_pass": int(len(passing)),
                     "pass_model": passing.iloc[0].model if len(passing) else None,
                     "pass_r2": round(float(passing.iloc[0].r2_os), 4) if len(passing) else None,
                     "models": {m: round(float(v), 4) for m, v in zip(g.model, g.r2_os)}})
    cond = {"vol": {}, "mean": {}, "ust_anchor": None}
    lrv_hist = {"lrv_mkt": "MKT", "lrv_ust": "UST10"}
    for r in rows:
        if r["family"] == "K" and r["target"] in lrv_hist and r["pass_model"]:
            fc = float(np.exp(cur[r["target"]][r["pass_model"]]))
            hist = pd.read_csv(s5 / f"pred_{r['target']}.csv", index_col=0)["rw"]          # realised log RV history (t)
            cond["vol"][lrv_hist[r["target"]]] = round(float(np.sqrt(fc / np.exp(hist).mean())), 4)
        if r["family"] == "R" and r["target"].startswith("ret1_") and r["pass_model"]:
            a = r["target"].split("_")[1]
            cond["mean"][a] = round(float(cur[r["target"]][r["pass_model"]]) + cur["rf_annual"] / 12, 5)
    ya = sc[(sc.model == "yield_anchor")]
    if len(ya) and bool(ya.iloc[0].holm_reject_5pct) and ya.iloc[0].r2_os > 0:
        cond["ust_anchor"] = round(cur["y10"] / 12, 5)
    data["s5"] = {"rows": rows, "regime": rs, "cond": cond, "decision": cur["decision_month"],
                  "regime_probs": cur.get("regime_probs"), "y10": cur["y10"],
                  "yield_anchor": {"r2": round(float(ya.iloc[0].r2_os), 4), "pass": bool(ya.iloc[0].holm_reject_5pct)} if len(ya) else None,
                  "h2h": [{"target": label[t], "r2": round(float(v), 4), "p": round(float(pv), 3)} for t, v, pv in zip(h2h.target, h2h.r2_regimeRF_vs_RF, h2h.p_value)],
                  "econ": [{"test": t, "stat": st, "diff": round(float(d), 4), "p": round(float(pa), 3), "pass": bool(rj)}
                           for t, st, d, pa, rj in zip(econ.test, econ.statistic, econ["diff"], econ.holm_adj_p, econ.holm_reject_5pct)]}
tpl = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
out = tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
(ROOT / "site" / "hedge_lab.html").write_text(out, encoding="utf-8")
print(f"wrote site/hedge_lab.html ({len(out) / 1024:.0f} KB), {len(R)} months {data['start']}..{data['end']}")
