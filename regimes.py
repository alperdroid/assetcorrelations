"""Real-time macro regime signals.

Timing convention: a label indexed by month t uses only information published by the END of
month t, and is used to set weights for returns in month t+1.

Publication lags (US):
  - Philly Fed manufacturing survey for month t: released ~3rd Thursday of month t  -> lag 0
  - CPI for month t: released mid-month t+1                                           -> lag 1
  - Unemployment rate for month t: released first Friday of month t+1                 -> lag 1
  - Daily stock-bond correlation: known at the close of the last trading day of t     -> lag 0
CPI is used NOT seasonally adjusted (CPIAUCNS) because it is never revised, so the inflation
signal is a true real-time series. Unemployment and the Philly index have minor seasonal
revisions; ALFRED vintages can be swapped in as a robustness check.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

REGIME_NAMES = {
    (True, False): "Goldilocks (G+ I-)",
    (True, True): "Reflation (G+ I+)",
    (False, True): "Stagflation (G- I+)",
    (False, False): "Disinflationary slowdown (G- I-)",
}
REGIME_ORDER = list(REGIME_NAMES.values())


def _z_expanding(x: pd.Series, minp: int) -> pd.Series:
    """Scale by expanding std (past data only); before warm-up, use the sign only."""
    sd = x.expanding(minp).std()
    z = x / sd
    return z.fillna(np.sign(x))


def macro_scores(macro: pd.DataFrame, lags: dict, minp: int = 24) -> pd.DataFrame:
    cpi_yoy = macro["CPI"].pct_change(12)
    infl = (cpi_yoy.rolling(3).mean() - cpi_yoy.rolling(12).mean()).shift(lags["cpi"])

    ph = macro["PHILLY"]
    g1 = (ph.rolling(3).mean() - ph.rolling(12).mean()).shift(lags["philly"])
    ur = macro["UNRATE"]
    g2 = -(ur.rolling(3).mean() - ur.rolling(12).mean()).shift(lags["unrate"])
    growth = 0.5 * _z_expanding(g1, minp) + 0.5 * _z_expanding(g2, minp)

    out = pd.DataFrame({"growth_score": growth, "infl_score": infl,
                        "cpi_yoy": cpi_yoy.shift(lags["cpi"])})
    ok = out[["growth_score", "infl_score"]].notna().all(axis=1)
    out["regime"] = None
    out.loc[ok, "regime"] = [
        REGIME_NAMES[(g > 0, i > 0)] for g, i in zip(out.loc[ok, "growth_score"], out.loc[ok, "infl_score"])
    ]
    return out


def stock_bond_corr(daily: pd.DataFrame, window: int = 63) -> pd.Series:
    c = daily["MKT"].rolling(window).corr(daily["UST10"])
    return c.groupby(c.index.to_period("M")).last().rename("sb_corr")


def confirm_switches(labels: pd.Series, k: int) -> pd.Series:
    """Only switch to a new regime after it has been signalled k months in a row (reduces whipsaw)."""
    if k <= 1:
        return labels
    out, cur, streak, cand = [], None, 0, None
    for v in labels:
        if v is None or (isinstance(v, float) and np.isnan(v)):
            out.append(cur)
            continue
        if cur is None:
            cur = v
        elif v != cur:
            streak = streak + 1 if v == cand else 1
            cand = v
            if streak >= k:
                cur, streak, cand = v, 0, None
        else:
            streak, cand = 0, None
        out.append(cur)
    return pd.Series(out, index=labels.index)


def build_regimes(macro: pd.DataFrame, daily: pd.DataFrame, window: int = 63, minp: int = 24,
                  confirm: int = 1) -> pd.DataFrame:
    """Real-time labels (for trading) and oracle labels (perfect nowcast of next month)."""
    rt = macro_scores(macro, {"cpi": 1, "unrate": 1, "philly": 0}, minp)
    rt["regime_raw"] = rt["regime"]
    rt["regime"] = confirm_switches(rt["regime"], confirm)
    nowcast = macro_scores(macro, {"cpi": 0, "unrate": 0, "philly": 0}, minp)
    sb = stock_bond_corr(daily, window)

    out = rt.copy()
    # Oracle label at decision month t = the true regime of the month being traded (t+1).
    out["regime_oracle"] = nowcast["regime"].shift(-1)
    out["sb_corr"] = sb.reindex(out.index)
    out["sb_regime"] = np.where(out["sb_corr"] > 0, "positive", np.where(out["sb_corr"] <= 0, "negative", None))
    return out
