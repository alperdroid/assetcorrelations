"""Stationary block bootstrap (Politis & Romano 1994) for strategy comparisons.

Paired resampling: the same block indices are applied to both strategies and the T-bill rate,
so cross-strategy dependence and serial dependence (within blocks) are preserved.

Two-sided p-values use the centred bootstrap distribution (Ledoit & Wolf 2008 style):
    p = P*( |d* - d_hat| >= |d_hat| )
which approximates the null H0: d = 0. Confidence intervals are percentile intervals of d*.

Caveat: max drawdown is path dependent. Resampled blocks break long drawdowns apart, so the
bootstrap distribution of max drawdown is only a rough guide; interpret those p-values cautiously.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

COMPARISONS = (("Regime Tilt", "Uncond. Tilt"), ("Regime Tilt", "60/40"))


def stationary_bootstrap_indices(n: int, n_boot: int, block: float, rng: np.random.Generator) -> np.ndarray:
    """(n_boot, n) index matrix; block lengths are geometric with mean `block`, wrapping around."""
    p = 1.0 / block
    idx = np.empty((n_boot, n), dtype=np.int64)
    idx[:, 0] = rng.integers(0, n, n_boot)
    new_block = rng.random((n_boot, n)) < p
    starts = rng.integers(0, n, (n_boot, n))
    for t in range(1, n):
        idx[:, t] = np.where(new_block[:, t], starts[:, t], (idx[:, t - 1] + 1) % n)
    return idx


def sharpe(r: np.ndarray, rf: np.ndarray) -> np.ndarray:
    """Annualised Sharpe along the last axis; same definition as analysis.perf_stats."""
    return (r - rf).mean(axis=-1) / r.std(axis=-1, ddof=1) * np.sqrt(12)


def max_drawdown(r: np.ndarray) -> np.ndarray:
    w = np.cumprod(1 + r, axis=-1)
    return (w / np.maximum.accumulate(w, axis=-1) - 1).min(axis=-1)


def bootstrap_diff(a: np.ndarray, b: np.ndarray, rf: np.ndarray, stat: str, n_boot: int = 5000,
                   block: float = 12.0, seed: int = 20260101, alpha: float = 0.05) -> dict:
    rng = np.random.default_rng(seed)
    idx = stationary_bootstrap_indices(len(a), n_boot, block, rng)
    if stat == "sharpe":
        f = lambda x, i: sharpe(x[i], rf[i])
    elif stat == "maxdd":
        f = lambda x, i: max_drawdown(x[i])
    else:
        raise ValueError(stat)
    full = np.arange(len(a))
    d_hat = float(f(a, full) - f(b, full))
    d_star = f(a, idx) - f(b, idx)
    p = float(np.mean(np.abs(d_star - d_hat) >= abs(d_hat)))
    lo, hi = np.quantile(d_star, [alpha / 2, 1 - alpha / 2])
    return {"diff": d_hat, "ci_low": float(lo), "ci_high": float(hi), "p_value": p,
            "boot_mean": float(d_star.mean()), "boot_sd": float(d_star.std(ddof=1))}


def significance_table(port: pd.DataFrame, rf: pd.Series, n_boot: int = 5000, block: float = 12.0,
                       seed: int = 20260101) -> pd.DataFrame:
    rf = rf.reindex(port.index).values
    rows = []
    for a, b in COMPARISONS:
        for stat, label in (("sharpe", "Sharpe ratio"), ("maxdd", "Max drawdown")):
            res = bootstrap_diff(port[a].values, port[b].values, rf, stat, n_boot, block, seed)
            rows.append({"strategy": a, "versus": b, "statistic": label,
                         "value_strategy": _stat(port[a].values, rf, stat),
                         "value_versus": _stat(port[b].values, rf, stat), **res,
                         "n_months": len(port), "n_boot": n_boot, "mean_block": block, "seed": seed})
    return pd.DataFrame(rows)


def _stat(r, rf, stat):
    return float(sharpe(r, rf) if stat == "sharpe" else max_drawdown(r))
