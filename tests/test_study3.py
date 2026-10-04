"""Study 3 rules: correct weights and no look-ahead (synthetic data)."""
import numpy as np
import pandas as pd
import pytest

import study3 as S
from config import Config
from data import build_panels, load_raw
from synthetic import write_synthetic


def test_trend_cash_and_fallback_weights():
    idx = pd.period_range("2000-01", periods=4, freq="M")
    p = pd.DataFrame({"EQ": [True, False, False, np.nan], "UST10": [True, True, False, True],
                      "GOLD": [False, True, False, True]}, index=idx).astype(object)
    a = S.w_trend_cash(p)
    np.testing.assert_allclose(a.values, [[1/3, 1/3, 0, 1/3], [0, 1/3, 1/3, 1/3], [0, 0, 0, 1], [1/3, 1/3, 1/3, 0]])
    b = S.w_trend_redistribute(p)
    np.testing.assert_allclose(b.values, [[.5, .5, 0, 0], [0, .5, .5, 0], [0, 0, 0, 1], [1/3, 1/3, 1/3, 0]])


def test_vol_rule_matches_study2_formula():
    idx = pd.period_range("2000-01", periods=2, freq="M")
    rvt = pd.DataFrame({"rv": [1.0, 4.0], "target": [1.0, 1.0]}, index=idx)
    w = S.w_vol(rvt, idx)
    np.testing.assert_allclose(w["EQ"].values, [1/3, 1/12])
    np.testing.assert_allclose(w.sum(axis=1).values, 1.0)
    assert (w["CASH"] == 0).all()


@pytest.mark.parametrize("variant", ["primary", "R1", "R2"])
def test_no_lookahead(tmp_path, variant):
    raw_dir = tmp_path / "raw"
    write_synthetic(raw_dir)
    raw = load_raw(raw_dir, 12, use_gold_override=False)
    base = build_panels(raw)["returns"].loc["1972-01":]
    eq_m, eq_d = base["MKT"] * 0.9, raw["ff3_d"]["Mkt-RF"] * 0.9
    cfg = Config()
    cfg.cost_bps = {**cfg.cost_bps, "CASH": 0.0}
    T = pd.Period("2012-03", "M")
    _, _, W0, _ = S.build(eq_m, eq_d, base, "1991-07", cfg, variant)
    rng = np.random.default_rng(1)
    b2 = base.copy()
    b2.loc[b2.index >= T] += rng.normal(0, 0.1, b2.loc[b2.index >= T].shape)
    m2 = eq_m.copy(); m2.loc[m2.index >= T] += 0.2
    d2 = eq_d.copy(); d2.loc[d2.index >= T.start_time] *= 5
    _, _, W1, _ = S.build(m2, d2, b2, "1991-07", cfg, variant)
    for k in W0:
        pd.testing.assert_frame_equal(W0[k].loc[:T], W1[k].loc[:T], check_exact=True)
    assert any(not np.allclose(W0[k].loc[T + 1:].values, W1[k].loc[T + 1:].values) for k in W0)
