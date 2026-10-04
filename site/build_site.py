"""Build site/hedge_lab.html: inject the study's monthly data into site/template.html.

    python site/build_site.py

Data: monthly returns 1972-01..latest for the US market, 12 Ken French industries, the 10y Treasury
(from DGS10), gold (World Bank monthly average) and T-bills, plus the real-time regime label known at
the end of the previous month. Strategy points for the risk map come from results/report_strategies_1990.csv.
"""
import json
import sys
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
tpl = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
out = tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
(ROOT / "site" / "hedge_lab.html").write_text(out, encoding="utf-8")
print(f"wrote site/hedge_lab.html ({len(out) / 1024:.0f} KB), {len(R)} months {data['start']}..{data['end']}")
