"""Study 5: features use only information known at the end of month t; targets are aligned to t+1..."""
import numpy as np
import pandas as pd
import pytest

import study5 as S
from config import Config
from data import build_panels, load_raw
from regimes import build_regimes
from synthetic import write_synthetic


def _build(raw_dir, shock_from=None):
    raw = load_raw(raw_dir, 12, use_gold_override=False)
    if shock_from is not None:
        T = pd.Period(shock_from, "M")
        ff = raw["ff3_d"].copy(); ff.loc[ff.index >= T.start_time] *= -2.0; raw["ff3_d"] = ff
        d = raw["DGS10"].copy(); d.loc[d.index >= T.start_time] += 1.5; raw["DGS10"] = d
        for k in ("ind12", "ff3_m"):
            m = raw[k].copy(); m.loc[m.index >= T] += 0.05; raw[k] = m
        g = raw["GOLD"].copy(); g.loc[g.index >= T] *= 1.3; raw["GOLD"] = g
        for k in ("CPI", "UNRATE", "PHILLY"):
            s = raw[k].copy(); s.loc[s.index >= T.start_time] *= 1.2; raw[k] = s
    p = build_panels(raw)
    cfg = Config()
    rg = build_regimes(p["macro"], p["daily"], cfg.corr_window_days, cfg.zscore_min_periods, 1, p["interpolated"])
    idx = pd.period_range("1960-01", "2026-12", freq="M")
    baa = pd.Series(np.linspace(5, 7, len(idx)), index=idx)
    aaa = pd.Series(np.linspace(4, 6, len(idx)), index=idx)
    if shock_from is not None:
        baa.loc[baa.index >= pd.Period(shock_from, "M")] += 2
    return S.build_dataset(p, raw, rg, baa, aaa)


@pytest.fixture(scope="module")
def synth(tmp_path_factory):
    d = tmp_path_factory.mktemp("s5") / "raw"
    write_synthetic(d)
    return d


def test_features_ignore_everything_from_month_T_on(synth):
    F0, *_ = _build(synth)
    T = pd.Period("2015-06", "M")
    F1, *_ = _build(synth, "2015-06")
    pd.testing.assert_frame_equal(F0.loc[:T - 1], F1.loc[:T - 1], check_exact=False, rtol=1e-12, atol=1e-12)
    assert not np.allclose(F0.loc[T + 1:T + 24].values, F1.loc[T + 1:T + 24].values, equal_nan=True)


def test_target_alignment(synth):
    F, Y, R, aux, *_ = _build(synth)
    t = pd.Period("2010-03", "M")
    assert Y.loc[t, "ret1_MKT"] == pytest.approx(R.loc[t + 1, "MKT"] - R.loc[t + 1, "RF"])
    g = np.prod(1 + R.loc[t + 1:t + 12, "UST10"]) - np.prod(1 + R.loc[t + 1:t + 12, "RF"])
    assert Y.loc[t, "ret12_UST10"] == pytest.approx(g)
    assert Y.loc[t, "lrv_mkt"] == pytest.approx(aux.loc[t + 1, "lrv_m"])
    assert Y.loc[t, "sbc3"] == pytest.approx(aux.loc[t + 3, "c3"])
    assert Y.loc[t, "regime_next"] == aux.loc[t + 1, "lab"]


def test_clark_west_and_dm_sanity():
    rng = np.random.default_rng(0)
    y = rng.normal(0, 1, 500)
    bench = np.zeros(500)
    good = y * 0.5
    assert S.clark_west(y, bench, good, 0)[1] < 0.01
    assert S.r2_os(y, bench, good) > 0
    t, p = S.diebold_mariano(y, bench, bench + 1e-9, 1)
    assert p > 0.5
