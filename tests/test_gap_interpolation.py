"""Internal macro gaps (October 2025 CPI/UNRATE) are interpolated without look-ahead."""
import numpy as np
import pandas as pd
import pytest

from data import fill_internal_gaps
from regimes import build_regimes, unpublished_interp_months


def test_fill_internal_gaps_log_linear_and_inside_only():
    idx = pd.period_range("2025-08", periods=5, freq="M")
    s = pd.Series([100.0, 110.0, np.nan, 121.0, np.nan], index=idx)
    f, gaps = fill_internal_gaps(s, log_scale=True)
    assert f.iloc[2] == pytest.approx(np.sqrt(110.0 * 121.0), rel=1e-12)   # geometric midpoint
    assert np.isnan(f.iloc[-1])                           # ragged edge is not filled
    assert gaps == [(idx[2], idx[3])]


def test_unpublished_months_for_oct_2025():
    oct25, nov25 = pd.Period("2025-10", "M"), pd.Period("2025-11", "M")
    bad = unpublished_interp_months({"CPI": [(oct25, nov25)], "UNRATE": [(oct25, nov25)]})
    assert bad == [nov25]                                 # only decision month 2025-11
    # a two-month gap in a lag-1 series blocks two decision months
    bad2 = unpublished_interp_months({"CPI": [(oct25, pd.Period("2025-12", "M")), (nov25, pd.Period("2025-12", "M"))]})
    assert bad2 == [nov25, pd.Period("2025-12", "M")]


def test_interpolated_label_is_real_time(panels):
    """Knock out CPI and UNRATE for one month, interpolate, and check the label:
    unchanged before the gap is used, blank at the one decision month where the interpolation would
    need next month's (unpublished) value, and from then on independent of later data."""
    macro, daily = panels["macro"], panels["daily"]
    m_gap = pd.Period("2015-10", "M")
    gapped = macro.copy()
    gapped.loc[m_gap, ["CPI", "UNRATE"]] = np.nan
    filled = gapped.copy()
    interp = {}
    for col, log_scale in (("CPI", True), ("UNRATE", False)):
        filled[col], interp[col] = fill_internal_gaps(gapped[col], log_scale)
    base = build_regimes(macro, daily)
    r = build_regimes(filled, daily, interpolated=interp)
    cols = ["growth_score", "infl_score", "regime"]
    pd.testing.assert_frame_equal(base.loc[:m_gap, cols], r.loc[:m_gap, cols])
    assert r.loc[m_gap + 1, "regime"] is None and np.isnan(r.loc[m_gap + 1, "infl_score"])
    assert r.loc[m_gap + 2:, "regime"].notna().loc[: m_gap + 30].all()
    # the label at m_gap+2 must not depend on CPI/UNRATE of m_gap+2 onward (published later)
    later = filled.copy()
    later.loc[later.index >= m_gap + 2, ["CPI", "UNRATE"]] *= 1.3
    r2 = build_regimes(later, daily, interpolated=interp)
    pd.testing.assert_frame_equal(r.loc[: m_gap + 2, cols], r2.loc[: m_gap + 2, cols])
