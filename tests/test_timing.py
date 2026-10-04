"""No-look-ahead tests.

Convention (regimes.py): the label indexed by decision month t uses information published by the
end of month t and sets the weights for returns in month t+1.

  * CPI and unemployment for month t are published in month t+1 -> label at t uses them up to t-1.
  * The Philly Fed survey for month t is published in month t   -> label at t uses it up to t.
  * Weights applied to returns of month t use returns up to t-1 only.
  * The oracle label is the only place future information enters, and only Oracle Tilt uses it.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from portfolio import run_backtest
from regimes import REGIME_ORDER, build_regimes

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ["1995-06", "2008-09", "2022-03"]
NON_ORACLE = ["60/40", "Static 1/3", "Uncond. ERC", "Uncond. Tilt", "Regime ERC", "Regime Tilt"]


def _regimes(macro, daily, confirm=1):
    return build_regimes(macro, daily, 63, 24, confirm)


def _bump(macro, col, months, factor):
    m = macro.copy()
    m.loc[months, col] = m.loc[months, col] * factor
    return m


def _same_rt(a, b, upto):
    cols = ["growth_score", "infl_score", "regime"]
    pd.testing.assert_frame_equal(a.loc[:upto, cols], b.loc[:upto, cols])


# --------------------------------------------------------------------------- regime labels
@pytest.mark.parametrize("t", DECISIONS)
@pytest.mark.parametrize("confirm", [1, 2])
def test_label_ignores_cpi_unrate_from_t_and_philly_from_t_plus_1(panels, t, confirm):
    macro, daily = panels["macro"], panels["daily"]
    base = _regimes(macro, daily, confirm)
    T = pd.Period(t, "M")
    m = _bump(macro, "CPI", macro.index >= T, 1.30)                 # CPI of month t and later
    m = _bump(m, "UNRATE", m.index >= T, 1.80)                      # unemployment of t and later
    m = _bump(m, "PHILLY", m.index >= T + 1, -3.0)                  # Philly of t+1 and later
    _same_rt(base, _regimes(m, daily, confirm), T)


@pytest.mark.parametrize("t", DECISIONS)
def test_label_uses_cpi_and_unrate_at_t_minus_1(panels, t):
    macro, daily = panels["macro"], panels["daily"]
    T = pd.Period(t, "M")
    base = _regimes(macro, daily)
    cpi = _regimes(_bump(macro, "CPI", macro.index == T - 1, 1.10), daily)
    assert cpi.loc[T, "infl_score"] != pytest.approx(base.loc[T, "infl_score"])
    _same_rt(base, cpi, T - 1)                                      # not visible one month earlier
    ur = _regimes(_bump(macro, "UNRATE", macro.index == T - 1, 1.50), daily)
    assert ur.loc[T, "growth_score"] != pytest.approx(base.loc[T, "growth_score"])
    _same_rt(base, ur, T - 1)


@pytest.mark.parametrize("t", DECISIONS)
def test_label_uses_philly_at_t(panels, t):
    macro, daily = panels["macro"], panels["daily"]
    T = pd.Period(t, "M")
    base = _regimes(macro, daily)
    m = macro.copy()
    m.loc[T, "PHILLY"] = m.loc[T, "PHILLY"] + 40.0
    ph = _regimes(m, daily)
    assert ph.loc[T, "growth_score"] != pytest.approx(base.loc[T, "growth_score"])
    _same_rt(base, ph, T - 1)


# --------------------------------------------------------------------------- weights
def _bt(rets, regimes, panels, cfg):
    return run_backtest(rets.loc[cfg.sample_start:], regimes, panels["industries"], cfg)


def test_weights_for_month_t_use_returns_up_to_t_minus_1(panels, cfg):
    rets = panels["returns"]
    regimes = _regimes(panels["macro"], panels["daily"])
    T = pd.Period("2025-01", "M")
    p0, _, w0 = _bt(rets, regimes, panels, cfg)
    shocked = rets.copy()
    rng = np.random.default_rng(0)
    fut = shocked.index >= T
    shocked.loc[fut] = shocked.loc[fut] + rng.normal(0, 0.10, shocked.loc[fut].shape)
    p1, _, w1 = _bt(shocked, regimes, panels, cfg)
    for k in w0:
        pd.testing.assert_frame_equal(w0[k].loc[:T], w1[k].loc[:T], check_exact=True)
    pd.testing.assert_frame_equal(p0.loc[: T - 1], p1.loc[: T - 1], check_exact=False, rtol=0, atol=1e-15)
    # power check: the shock does move later weights of the estimated strategies
    assert not np.allclose(w0["Regime Tilt"].loc[T + 1:].values, w1["Regime Tilt"].loc[T + 1:].values)


def test_weights_for_month_t_use_label_from_t_minus_1_only(panels, cfg):
    rets = panels["returns"]
    regimes = _regimes(panels["macro"], panels["daily"])
    T = pd.Period("2025-01", "M")
    _, _, w0 = _bt(rets, regimes, panels, cfg)

    # Changing the label of decision month t must not move the weights for returns in t ...
    r1 = regimes.copy()
    r1.loc[T, "regime"] = next(r for r in REGIME_ORDER if r != regimes.loc[T, "regime"])
    _, _, w1 = _bt(rets, r1, panels, cfg)
    for k in w0:
        pd.testing.assert_frame_equal(w0[k].loc[:T], w1[k].loc[:T], check_exact=True)

    # ... but changing the label of decision month t-1 must (and only for regime strategies).
    r2 = regimes.copy()
    counts = regimes["regime"].shift(1).loc[cfg.sample_start: T - 1].value_counts()
    alt = next(r for r in counts.index if r != regimes.loc[T - 1, "regime"] and counts[r] >= cfg.min_regime_obs)
    r2.loc[T - 1, "regime"] = alt
    _, _, w2 = _bt(rets, r2, panels, cfg)
    assert not np.allclose(w0["Regime Tilt"].loc[T].values, w2["Regime Tilt"].loc[T].values)
    for k in ("Uncond. ERC", "Uncond. Tilt", "Oracle Tilt", "60/40", "Static 1/3"):
        pd.testing.assert_series_equal(w0[k].loc[T], w2[k].loc[T], check_exact=True)


# --------------------------------------------------------------------------- oracle
def test_future_macro_data_only_reaches_oracle(panels, cfg):
    """Perturb all macro data from month T on: only Oracle Tilt may change for returns in T."""
    macro, daily, rets = panels["macro"], panels["daily"], panels["returns"]
    T = pd.Period("2025-01", "M")
    base = _regimes(macro, daily)
    # Push month T's true regime to a quadrant different from the baseline oracle label.
    target = next(r for r in REGIME_ORDER if r != base.loc[T - 1, "regime_oracle"])
    g_up, i_up = target.startswith(("Goldilocks", "Reflation")), target.startswith(("Reflation", "Stagflation"))
    m = macro.copy()
    fut = m.index >= T
    m.loc[fut, "CPI"] *= 1.05 if i_up else 0.95
    m.loc[fut, "PHILLY"] = 60.0 if g_up else -60.0
    m.loc[fut, "UNRATE"] = m.loc[fut, "UNRATE"] - 2.0 if g_up else m.loc[fut, "UNRATE"] + 2.0
    pert = _regimes(m, daily)
    assert pert.loc[T - 1, "regime_oracle"] == target                 # oracle sees month T
    _same_rt(base, pert, T - 1)                                       # real-time label does not

    _, _, w0 = _bt(rets, base, panels, cfg)
    _, _, w1 = _bt(rets, pert, panels, cfg)
    for k in NON_ORACLE:
        pd.testing.assert_frame_equal(w0[k].loc[:T], w1[k].loc[:T], check_exact=True)
    assert not np.allclose(w0["Oracle Tilt"].loc[T].values, w1["Oracle Tilt"].loc[T].values)


def test_scrambled_oracle_changes_nothing_but_oracle(panels, cfg):
    rets = panels["returns"]
    regimes = _regimes(panels["macro"], panels["daily"])
    scr = regimes.copy()
    scr["regime_oracle"] = np.random.default_rng(1).permutation(scr["regime_oracle"].values)
    p0, _, _ = _bt(rets, regimes, panels, cfg)
    p1, _, _ = _bt(rets, scr, panels, cfg)
    pd.testing.assert_frame_equal(p0[NON_ORACLE], p1[NON_ORACLE], check_exact=False, rtol=0, atol=1e-15)
    assert not np.allclose(p0["Oracle Tilt"].values, p1["Oracle Tilt"].values)


def test_oracle_referenced_only_in_allowed_places():
    """Static check: the oracle label appears only in its definition (regimes.py), the Oracle Tilt
    strategy (portfolio.py) and the real-time-vs-oracle agreement diagnostic (analysis.py); the
    Oracle Tilt return is used only for the 'cost of detection lag' upper-bound comparison."""
    hits = {p.name for p in ROOT.glob("*.py") if "regime_oracle" in p.read_text()}
    assert hits == {"regimes.py", "portfolio.py", "analysis.py"}
    src = (ROOT / "portfolio.py").read_text()
    oracle_vars = ("lab_or", "cur_or", "cov_o", "mu_o", "w_oerc")
    uses = [ln.strip() for ln in src.splitlines() if any(v in ln for v in oracle_vars)]
    for ln in uses:
        assert ln.startswith(("lab_or =", "cur_or =", "cov_o, mu_o", "w_oerc =", '"Oracle Tilt"')), ln
    ana = (ROOT / "analysis.py").read_text()
    assert ana.count("regime_oracle") == 1 and "agree = (r[\"regime\"] == r[\"regime_oracle\"])" in ana
    run = (ROOT / "run_study.py").read_text()
    assert [ln.strip() for ln in run.splitlines() if 'port["Oracle Tilt"]' in ln] == [
        'detection_cost = ann(port["Oracle Tilt"]) - ann(port["Regime Tilt"])']
