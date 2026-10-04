import numpy as np
import pandas as pd

import study4 as S


def test_cash_mix_weights():
    idx = pd.period_range("2000-01", periods=3, freq="M")
    w = S.cash_mix(0.4, idx)
    np.testing.assert_allclose(w.iloc[0].values, [0.2, 0.2, 0.2, 0.4])
    np.testing.assert_allclose(w.sum(axis=1).values, 1.0)
