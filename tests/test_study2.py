"""Study 2 rules use only information available at the end of month t-1."""
import numpy as np
import pandas as pd
import pytest

import study2 as S
from config import Config
from data import build_panels, load_raw
from synthetic import write_synthetic


@pytest.fixture(scope="module")
def setup(tmp_path_factory):
    raw_dir = tmp_path_factory.mktemp("s2") / "raw"
    write_synthetic(raw_dir)
    raw = load_raw(raw_dir, 12, use_gold_override=False)
    return raw, build_panels(raw)


def test_trend_window_months():
    idx = pd.period_range("2000-01", periods=40, freq="M")
    r = pd.DataFrame({"A": 0.0}, index=idx)
    rf = pd.Series(0.0, index=idx)
    r.loc["2001-06", "A"] = 0.5                       # one big month
    p0 = S.trailing_excess_pass(r, rf + 1e-6, 12, 0)
    assert p0.loc["2001-06", "A"] == False            # not yet known at decision for 2001-06
    assert p0.loc["2001-07", "A"] == True and p0.loc["2002-06", "A"] == True
    assert p0.loc["2002-07", "A"] == False            # dropped out of t-12..t-1
    p1 = S.trailing_excess_pass(r, rf + 1e-6, 12, 1)
    assert p1.loc["2001-07", "A"] == False and p1.loc["2001-08", "A"] == True   # skip-month


def test_trend_weights_redistribute_and_fallback():
    idx = pd.period_range("2000-01", periods=3, freq="M")
    p = pd.DataFrame({"MKT": [True, False, False], "UST10": [True, True, False], "GOLD": [False, True, False]},
                     index=idx).astype(object)
    w = S.w_trend(p, ["MKT", "UST10", "GOLD"])
    np.testing.assert_allclose(w.iloc[0].values, [0.5, 0.5, 0.0])
    np.testing.assert_allclose(w.iloc[1].values, [0.0, 0.5, 0.5])
    np.testing.assert_allclose(w.iloc[2].values, [0.0, 1.0, 0.0])


@pytest.mark.parametrize("variant", ["primary", "R1", "R2", "R4"])
def test_weights_ignore_data_from_month_t_onward(setup, variant):
    raw, panels = setup
    cfg = Config()
    T = pd.Period("2010-06", "M")
    _, _, W0 = S.build_all(panels, raw, cfg, variant)
    # shock monthly returns from T on, and daily data from the first day of T on
    p2 = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in panels.items()}
    r = p2["returns"]
    r.loc[r.index >= T] += np.random.default_rng(0).normal(0, 0.1, r.loc[r.index >= T].shape)
    d = p2["daily"]
    d.loc[d.index >= T.start_time] *= -3.0
    raw2 = dict(raw)
    ff = raw["ff3_d"].copy()
    ff.loc[ff.index >= T.start_time] *= -3.0
    raw2["ff3_d"] = ff
    _, _, W1 = S.build_all(p2, raw2, cfg, variant)
    for k in W0:
        pd.testing.assert_frame_equal(W0[k].loc[:T], W1[k].loc[:T], check_exact=True)
    changed = any(not np.allclose(W0[k].loc[T + 1:].values, W1[k].loc[T + 1:].values) for k in W0)
    assert changed                                    # power: later weights do react


def test_holm():
    p = pd.Series([0.01, 0.04, 0.03, 0.5])
    h = S.holm(p)
    assert h.loc[0, "holm_reject_5pct"] and not h.loc[2, "holm_reject_5pct"] and not h.loc[1, "holm_reject_5pct"]
    assert h.loc[0, "holm_adj_p"] == pytest.approx(0.04) and h.loc[2, "holm_adj_p"] == pytest.approx(0.09)
