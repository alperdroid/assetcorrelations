"""Allocation rules and a walk-forward backtest (long-only, fully invested, no cash).

Strategies
----------
Benchmarks (fixed weights, monthly rebalanced):
  60/40            60% US market, 40% 10y Treasury
  Static 1/3       1/3 market, 1/3 Treasury, 1/3 gold
Controls (same machinery, NO regime information) - isolate the value of the regime map:
  Uncond. ERC      equal risk contribution across sectors + Treasury + gold, full-history covariance
  Uncond. Tilt     Uncond. ERC tilted by full-history risk-adjusted returns
Regime strategies (real-time regime label):
  Regime ERC       ERC with covariance conditional on the current regime (shrunk to unconditional)
  Regime Tilt      Regime ERC tilted by regime-conditional risk-adjusted returns
Upper bound:
  Oracle Tilt      Regime Tilt using the true regime of the month being traded (perfect nowcast)

Regime value          = Regime Tilt - Uncond. Tilt
Cost of detection lag = Oracle Tilt - Regime Tilt
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.covariance import LedoitWolf


# --------------------------------------------------------------------------- building blocks
def erc_weights(cov: np.ndarray) -> np.ndarray:
    """Equal-risk-contribution weights via the log-barrier formulation (Spinu 2013)."""
    n = cov.shape[0]
    f = lambda x: 0.5 * x @ cov @ x - np.log(x).sum() / n
    g = lambda x: cov @ x - 1.0 / (n * x)
    x0 = 1.0 / np.sqrt(np.diag(cov))
    x0 /= x0.sum()
    res = minimize(f, x0, jac=g, method="L-BFGS-B", bounds=[(1e-12, None)] * n)
    w = res.x / res.x.sum()
    return w


def cap_weights(w: np.ndarray, cap: float) -> np.ndarray:
    w = w / w.sum()
    for _ in range(100):
        over = w > cap + 1e-12
        if not over.any():
            break
        excess = (w[over] - cap).sum()
        w[over] = cap
        free = ~over & (w < cap)
        if not free.any():
            break
        w[free] += excess * w[free] / w[free].sum()
    return w / w.sum()


def lw_cov(x: np.ndarray) -> np.ndarray:
    return LedoitWolf().fit(x).covariance_


def estimate(R: pd.DataFrame, rf: pd.Series, labels: pd.Series | None, current: str | None, cfg):
    """Shrunk covariance and risk-adjusted score, optionally conditional on a regime.

    R      : asset returns for months s+1 (training sample)
    labels : regime label known when the position for that month was set (aligned to R)
    """
    X = R.values
    ex = R.sub(rf, axis=0)
    cov_all = lw_cov(X)
    mu_all = ex.mean().values
    if labels is None or current is None:
        return cov_all, mu_all, 0
    mask = (labels == current).values
    n_r = int(mask.sum())
    if n_r < cfg.min_regime_obs:
        return cov_all, mu_all, n_r
    a_c = n_r / (n_r + cfg.cov_shrink_k)
    a_m = n_r / (n_r + cfg.mean_shrink_k)
    cov = a_c * lw_cov(X[mask]) + (1 - a_c) * cov_all
    mu = a_m * ex.values[mask].mean(axis=0) + (1 - a_m) * mu_all
    return cov, mu, n_r


def tilt(w_base: np.ndarray, cov: np.ndarray, mu: np.ndarray, cfg) -> np.ndarray:
    vol = np.sqrt(np.diag(cov))
    score = mu / vol
    sd = score.std()
    z = (score - score.mean()) / sd if sd > 0 else np.zeros_like(score)
    mult = np.clip(np.exp(cfg.tilt_strength * z), *cfg.tilt_clip)
    return cap_weights(w_base * mult, cfg.max_weight)


# --------------------------------------------------------------------------- backtest
def _cost_vector(assets: list[str], cfg) -> np.ndarray:
    return np.array([cfg.cost_bps.get(a, cfg.cost_bps["equity"]) / 1e4 for a in assets])


def run_backtest(returns: pd.DataFrame, regimes: pd.DataFrame, industries: list[str], cfg):
    assets = industries + ["UST10", "GOLD"]
    rets = returns.loc[cfg.sample_start:]
    R, rf, mkt = rets[assets], rets["RF"], rets["MKT"]
    # Label known at decision month s, aligned to the return month s+1
    lab_rt = regimes["regime"].shift(1).reindex(R.index)
    lab_or = regimes["regime_oracle"].shift(1).reindex(R.index)

    months = R.loc[cfg.oos_start:].index
    costs = _cost_vector(assets, cfg)
    names = ["60/40", "Static 1/3", "Uncond. ERC", "Uncond. Tilt", "Regime ERC", "Regime Tilt", "Oracle Tilt"]
    weights = {k: [] for k in names}
    port = {k: [] for k in names}
    turnover = {k: [] for k in names}
    prev = {k: None for k in names}

    for t in months:
        hist = R.loc[: t - 1]                                  # returns known before month t
        rf_h = rf.loc[hist.index]
        decision = t - 1                                       # month whose end we decide at
        cur_rt = regimes["regime"].get(decision)
        cur_or = regimes["regime_oracle"].get(decision)

        cov_u, mu_u, _ = estimate(hist, rf_h, None, None, cfg)
        w_uerc = erc_weights(cov_u)
        cov_r, mu_r, _ = estimate(hist, rf_h, lab_rt.loc[hist.index], cur_rt, cfg)
        w_rerc = erc_weights(cov_r)
        cov_o, mu_o, _ = estimate(hist, rf_h, lab_or.loc[hist.index], cur_or, cfg)
        w_oerc = erc_weights(cov_o)

        target = {
            "Uncond. ERC": w_uerc,
            "Uncond. Tilt": tilt(w_uerc, cov_u, mu_u, cfg),
            "Regime ERC": w_rerc,
            "Regime Tilt": tilt(w_rerc, cov_r, mu_r, cfg),
            "Oracle Tilt": tilt(w_oerc, cov_o, mu_o, cfg),
        }
        r_t = R.loc[t].values
        for k in names:
            if k in ("60/40", "Static 1/3"):
                continue
            w = target[k]
            to, cost = _trade(prev[k], w, costs)
            gross = float(w @ r_t)
            port[k].append(gross - cost)
            turnover[k].append(to)
            weights[k].append(pd.Series(w, index=assets, name=t))
            prev[k] = _drift(w, r_t)

        # fixed-weight benchmarks (market, Treasury, gold)
        bench_r = np.array([mkt.loc[t], R.loc[t, "UST10"], R.loc[t, "GOLD"]])
        bench_c = np.array([cfg.cost_bps["equity"], cfg.cost_bps["UST10"], cfg.cost_bps["GOLD"]]) / 1e4
        for k, w in (("60/40", np.array([0.6, 0.4, 0.0])), ("Static 1/3", np.full(3, 1 / 3))):
            to, cost = _trade(prev[k], w, bench_c)
            port[k].append(float(w @ bench_r) - cost)
            turnover[k].append(to)
            weights[k].append(pd.Series(w, index=["MKT", "UST10", "GOLD"], name=t))
            prev[k] = _drift(w, bench_r)

    port_df = pd.DataFrame(port, index=months)
    to_df = pd.DataFrame(turnover, index=months)
    w_dfs = {k: pd.DataFrame(v) for k, v in weights.items()}
    return port_df, to_df, w_dfs


def _trade(prev_w, w, costs):
    if prev_w is None:
        return 0.0, 0.0                                       # initial build not charged
    d = np.abs(w - prev_w)
    return float(d.sum() / 2), float(d @ costs)


def _drift(w, r):
    v = w * (1 + r)
    return v / v.sum()
