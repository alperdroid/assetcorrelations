import numpy as np
import pandas as pd
import pytest

from data import bond_returns_from_yields, build_panels, par_bond_price
from significance import bootstrap_diff, max_drawdown, stationary_bootstrap_indices


@pytest.mark.parametrize("y", [0.005, 0.03, 0.0725, 0.15])
def test_constant_yield_monthly_return_is_y_over_12(y):
    idx = pd.period_range("2000-01", periods=24, freq="M")
    r = bond_returns_from_yields(pd.Series(y, index=idx), 1.0 / 12.0).dropna()
    np.testing.assert_allclose(r.values, y / 12.0, rtol=0, atol=1e-14)


def test_constant_yield_daily_return_is_y_times_dt():
    idx = pd.bdate_range("2020-01-01", periods=300)
    y = pd.Series(0.04, index=idx)
    dt = pd.Series(idx, index=idx).diff().dt.days / 365.25
    r = bond_returns_from_yields(y, dt).dropna()
    np.testing.assert_allclose(r.values, 0.04 * dt.dropna().values, rtol=0, atol=1e-14)


def test_par_bond_prices_at_par_and_rate_rise_loses():
    assert par_bond_price(0.05, 0.05, 10.0) == pytest.approx(1.0, abs=1e-14)
    idx = pd.period_range("2000-01", periods=2, freq="M")
    r = bond_returns_from_yields(pd.Series([0.04, 0.05], index=idx), 1 / 12).iloc[-1]
    assert -0.085 < r < -0.07                                    # ~ -duration (8.1) * 1pp + carry


def test_panel_ust10_constant_yield(panels):
    """End-to-end through build_panels: a flat DGS10 gives UST10 = y/12 every month."""
    from synthetic import write_synthetic  # noqa: F401  (panels fixture already built raw data)
    raw = {"ind_key": "ind12"}
    idx_m = pd.period_range("1990-01", "1995-12", freq="M")
    raw["ind12"] = pd.DataFrame(0.01, index=idx_m, columns=panels["industries"])
    raw["ff3_m"] = pd.DataFrame({"Mkt-RF": 0.005, "SMB": 0.0, "HML": 0.0, "RF": 0.003}, index=idx_m)
    d = pd.bdate_range("1989-12-01", "1995-12-31")
    raw["ff3_d"] = pd.DataFrame({"Mkt-RF": 0.0, "SMB": 0.0, "HML": 0.0, "RF": 0.0001}, index=d)
    raw["DGS10"] = pd.Series(6.0, index=d)
    for k in ("CPI", "PHILLY", "UNRATE"):
        raw[k] = pd.Series(1.0, index=idx_m.to_timestamp())
    raw["GOLD"] = pd.Series(np.linspace(400, 500, len(idx_m)), index=idx_m)
    p = build_panels(raw)
    np.testing.assert_allclose(p["returns"]["UST10"].values, 0.06 / 12, atol=1e-14)


def test_bootstrap_indices_and_determinism():
    rng = np.random.default_rng(3)
    idx = stationary_bootstrap_indices(100, 50, 12.0, rng)
    assert idx.shape == (50, 100) and idx.min() >= 0 and idx.max() < 100
    # mean block length roughly 12
    breaks = (np.diff(idx, axis=1) != 1) & ~((idx[:, :-1] == 99) & (idx[:, 1:] == 0))
    assert 8 < 100 / (1 + breaks.sum(axis=1).mean()) < 18
    a, b = np.random.default_rng(0).normal(0.01, 0.04, (2, 240))
    rf = np.zeros(240)
    r1 = bootstrap_diff(a, b, rf, "sharpe", n_boot=500)
    r2 = bootstrap_diff(a, b, rf, "sharpe", n_boot=500)
    assert r1 == r2


def test_bootstrap_identical_series_not_significant_and_shift_is():
    x = np.random.default_rng(0).normal(0.005, 0.04, 360)
    rf = np.zeros(360)
    same = bootstrap_diff(x, x, rf, "sharpe", n_boot=500)
    assert same["diff"] == 0 and same["p_value"] == 1.0
    better = bootstrap_diff(x + 0.01, x, rf, "sharpe", n_boot=500)
    assert better["p_value"] < 0.01 and better["ci_low"] > 0


def test_max_drawdown():
    assert max_drawdown(np.array([0.1, -0.5, 0.2])) == pytest.approx(-0.5)


def test_avg_price_returns_are_ratios_of_monthly_average_levels():
    from data import avg_price_returns
    idx = pd.bdate_range("2020-01-01", "2020-03-31")
    r = pd.Series(0.001, index=idx)
    out = avg_price_returns(r)
    level = (1 + r).cumprod()
    avg = level.groupby(level.index.to_period("M")).mean()
    np.testing.assert_allclose(out.values, (avg / avg.shift(1) - 1).dropna().values, rtol=1e-14)
    assert list(out.index.astype(str)) == ["2020-02", "2020-03"]
    # an incomplete trailing month is dropped
    assert avg_price_returns(r.loc[:"2020-03-10"]).index[-1] == pd.Period("2020-02", "M")
