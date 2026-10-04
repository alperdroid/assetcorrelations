"""Study 5: forecasting horse race (returns, risk, regimes). Spec: PREREGISTRATION_STUDY5.md.

    python study5.py            # -> results_study5/  (takes a while: ~37 annual refits x many models)
    python study5.py --quick    # smoke run: 3 refits, fewer trees (for testing only)
"""
from __future__ import annotations

import argparse
import json
import logging
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sps
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import ElasticNet, LinearRegression
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from config import Config
from data import build_panels, load_raw, parse_fred_csv
from regimes import build_regimes
from significance import bootstrap_diff
from study2 import BOOT, holm, md, simulate, stats_table

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent
log = logging.getLogger("study5")
ASSETS = ["MKT", "UST10", "GOLD"]
FIRST_TRAIN, FIRST_OOS = pd.Period("1973-01", "M"), pd.Period("1989-12", "M")
REG = ["G", "R", "S", "D"]
SHORT = {"Goldilocks (G+ I-)": "G", "Reflation (G+ I+)": "R", "Stagflation (G- I+)": "S",
         "Disinflationary slowdown (G- I-)": "D"}


# --------------------------------------------------------------------------- data
def monthly_rv(daily: pd.Series) -> pd.Series:
    return (daily ** 2).groupby(daily.index.to_period("M")).sum()


def build_dataset(panels, raw, regimes, baa, aaa):
    """Features at decision month t (info known at end of t) and targets after t."""
    R = panels["returns"]
    idx = pd.period_range(R.index[0], R.index[-1], freq="M")
    R = R.reindex(idx)
    mac = panels["macro"].reindex(idx)
    rg = regimes.reindex(idx)
    d_mkt = (raw["ff3_d"]["Mkt-RF"] + raw["ff3_d"]["RF"])
    d_ust = panels["daily"]["UST10"]
    rv_m, rv_u = monthly_rv(d_mkt).reindex(idx), monthly_rv(d_ust).reindex(idx)
    lrv_m, lrv_u = np.log(rv_m), np.log(rv_u)
    F = pd.DataFrame(index=idx)
    F["y10"] = mac["Y10"]
    F["term"] = mac["Y10"] - R["RF"] * 12
    F["credit"] = ((baa - aaa) / 100).reindex(idx)
    F["cpi_yoy"] = rg["cpi_yoy"]
    F["infl"] = rg["infl_score"]
    F["growth"] = rg["growth_score"]
    F["d_unrate"] = mac["UNRATE"].diff(3).shift(1)
    F["philly"] = mac["PHILLY"]
    for a in ASSETS:
        F[f"mom1_{a}"] = R[a]
        F[f"mom12_{a}"] = (1 + R[a]).rolling(12).apply(np.prod, raw=True) - 1
    F["lrv_mkt"], F["lrv_ust"] = lrv_m, lrv_u
    F["lrv_mkt3"] = lrv_m.rolling(3).mean()
    F["sbc"] = rg["sb_corr"]
    F["gvol"] = R["GOLD"].rolling(12).std()
    lab = rg["regime"].map(lambda x: SHORT.get(x, None) if isinstance(x, str) else None)
    for r in ("R", "S", "D"):
        F[f"reg_{r}"] = (lab == r).astype(float)
    # forward-fill features for months where a real-time value is missing (e.g. decision 2025-11):
    # carrying the last known value is what an investor would have had (logged as an implementation detail)
    F = F.ffill()

    Y = pd.DataFrame(index=idx)
    for a in ASSETS:
        ex = R[a] - R["RF"]
        Y[f"ret1_{a}"] = ex.shift(-1)
        g = (1 + R[a]).rolling(12).apply(np.prod, raw=True)
        gf = (1 + R["RF"]).rolling(12).apply(np.prod, raw=True)
        Y[f"ret12_{a}"] = (g - gf).shift(-12)
    Y["lrv_mkt"] = lrv_m.shift(-1)
    Y["lrv_ust"] = lrv_u.shift(-1)
    both = pd.DataFrame({"m": d_mkt, "u": d_ust}).dropna()
    per = both.index.to_period("M")
    corr3 = {}
    months = sorted(set(per))
    for i in range(len(months) - 2):
        win = both[(per >= months[i]) & (per <= months[i + 2])]
        corr3[months[i + 2]] = win["m"].corr(win["u"])                # 3-month corr ending at month
    c3 = pd.Series(corr3).reindex(idx)
    Y["sbc3"] = c3.shift(-3)
    c1 = both.groupby(per).apply(lambda w: w["m"].corr(w["u"])).reindex(idx)
    both12 = {}
    for i in range(len(months) - 11):
        win = both[(per >= months[i]) & (per <= months[i + 11])]
        both12[months[i + 11]] = win["m"].corr(win["u"])
    c12 = pd.Series(both12).reindex(idx)
    Y["regime_next"] = lab.shift(-1)
    aux = pd.DataFrame({"lab": lab, "c3": c3, "c1": c1, "c12": c12, "lrv_m": lrv_m, "lrv_u": lrv_u, "RF": R["RF"]})
    return F, Y, R, aux, d_mkt, d_ust


HORIZON = {"ret1_MKT": 1, "ret1_UST10": 1, "ret1_GOLD": 1, "ret12_MKT": 12, "ret12_UST10": 12, "ret12_GOLD": 12,
           "lrv_mkt": 1, "lrv_ust": 1, "sbc3": 3, "regime_next": 1}
RET_T = [k for k in HORIZON if k.startswith("ret")]
RISK_T = ["lrv_mkt", "lrv_ust", "sbc3"]


# --------------------------------------------------------------------------- models
def m_enet():
    grid = {"elasticnet__alpha": [1e-4, 1e-3, 1e-2, 1e-1, 1], "elasticnet__l1_ratio": [0.2, 0.5, 0.8]}
    return GridSearchCV(make_pipeline(StandardScaler(), ElasticNet(max_iter=20000)), grid,
                        cv=TimeSeriesSplit(5), scoring="neg_mean_squared_error")


def m_rf(n):
    return RandomForestRegressor(n_estimators=n, max_depth=4, min_samples_leaf=24, max_features=0.5,
                                 random_state=0, n_jobs=-1)


def m_gbm():
    return HistGradientBoostingRegressor(learning_rate=0.03, max_depth=2, max_iter=200, l2_regularization=1.0,
                                         min_samples_leaf=24, random_state=0)


class MLPEnsemble:
    def __init__(self, seeds=5):
        self.seeds = seeds

    def fit(self, X, y):
        self.xs, self.mu, self.sd = StandardScaler().fit(X), y.mean(), y.std() or 1.0
        Xs = self.xs.transform(X)
        self.ms = [MLPRegressor(hidden_layer_sizes=(32, 16), alpha=1e-3, early_stopping=True, max_iter=2000, random_state=s)
                   .fit(Xs, (y - self.mu) / self.sd) for s in range(self.seeds)]
        return self

    def predict(self, X):
        Xs = self.xs.transform(X)
        return np.mean([m.predict(Xs) for m in self.ms], axis=0) * self.sd + self.mu


def stage1(n):
    return RandomForestClassifier(n_estimators=n, max_depth=4, min_samples_leaf=12, random_state=0, n_jobs=-1)


def proba4(clf, X):
    p = clf.predict_proba(X)
    out = np.zeros((len(X), 4))
    for j, c in enumerate(clf.classes_):
        out[:, REG.index(c)] = p[:, j]
    return out


def oof_proba(X, y, n):
    """Out-of-fold stage-1 probabilities inside a training window (earliest block: its class frequencies)."""
    out = np.zeros((len(X), 4))
    tss = TimeSeriesSplit(5)
    first_test = len(X)
    for tr, te in tss.split(X):
        first_test = min(first_test, te[0])
        c = stage1(n).fit(X[tr], y[tr])
        out[te] = proba4(c, X[te])
    freq = pd.Series(y[:first_test]).value_counts(normalize=True)
    out[:first_test] = [freq.get(r, 0.0) for r in REG]
    return out


# --------------------------------------------------------------------------- walk-forward
def walk_forward(F, Y, aux, d_mkt, d_ust, quick=False):
    n_trees = 100 if quick else 500
    last_dec = F.index[-1]
    refits = [p for p in pd.period_range(FIRST_OOS, last_dec, freq="M") if p.month == 12]
    if quick:
        refits = refits[:3]
    feat_cols = list(F.columns)
    preds = {t: {} for t in HORIZON}                      # target -> model -> Series over decision months
    garch_par = {}
    for T in refits:
        block = [p for p in pd.period_range(T, min(T + 11, last_dec), freq="M")]
        Xb = F.loc[block, feat_cols].values
        log.info("refit %s (%d decision months)", T, len(block))
        # stage-1 regime classifier (shared)
        ok1 = (F.index >= FIRST_TRAIN) & (F.index <= T - 1) & Y["regime_next"].notna() & F.notna().all(axis=1)
        X1, y1 = F.loc[ok1, feat_cols].values, Y.loc[ok1, "regime_next"].values
        clf = stage1(n_trees).fit(X1, y1)
        oof = pd.DataFrame(oof_proba(X1, y1, n_trees), index=F.index[ok1], columns=REG)
        pb = proba4(clf, Xb)
        for i, p in enumerate(block):
            preds["regime_next"].setdefault("stage1", {})[p] = pb[i]
            preds["regime_next"].setdefault("persist", {})[p] = aux.loc[p, "lab"]
        for tgt in RET_T + RISK_T:
            h = HORIZON[tgt]
            ok = (F.index >= FIRST_TRAIN) & (F.index <= T - h) & Y[tgt].notna() & F.notna().all(axis=1)
            X, y = F.loc[ok, feat_cols].values, Y.loc[ok, tgt].values
            res = {}
            res["enet"] = m_enet().fit(X, y).predict(Xb)
            res["rf"] = m_rf(n_trees).fit(X, y).predict(Xb)
            res["gbm"] = m_gbm().fit(X, y).predict(Xb)
            res["mlp"] = MLPEnsemble(2 if quick else 5).fit(X, y).predict(Xb)
            res["ensemble"] = np.mean([res[k] for k in ("enet", "rf", "gbm", "mlp")], axis=0)
            if tgt in RET_T:
                res["hist_mean"] = np.full(len(block), y.mean())
                okp = oof.index.intersection(F.index[ok])
                X2 = np.hstack([F.loc[okp, feat_cols].values, oof.loc[okp].values])
                y2 = Y.loc[okp, tgt].values
                res["regime_rf"] = m_rf(n_trees).fit(X2, y2).predict(np.hstack([Xb, pb]))
                if tgt == "ret12_UST10":
                    res["yield_anchor"] = (F.loc[block, "y10"] - aux.loc[block, "RF"] * 12).values
            else:
                own = {"lrv_mkt": "lrv_m", "lrv_ust": "lrv_u", "sbc3": None}[tgt]
                if own:
                    s = aux[own]
                    H = pd.DataFrame({"h1": s, "h3": s.rolling(3).mean(), "h12": s.rolling(12).mean()})
                    res["rw"] = s.loc[block].values
                else:
                    H = pd.DataFrame({"h1": aux["c1"], "h3": aux["c3"], "h12": aux["c12"]})
                    res["rw"] = aux.loc[block, "c3"].values
                okh = ok & H.notna().all(axis=1).values
                lr = LinearRegression().fit(H.loc[okh].values, Y.loc[okh, tgt].values)
                res["har"] = lr.predict(H.loc[block].ffill().values)
                if own:
                    res["garch"] = garch_block(d_mkt if tgt == "lrv_mkt" else d_ust, T, block, garch_par, tgt, quick)
            for k, v in res.items():
                for i, p in enumerate(block):
                    preds[tgt].setdefault(k, {})[p] = v[i]
    out = {}
    for tgt, d in preds.items():
        if tgt == "regime_next":
            out[tgt] = d
        else:
            out[tgt] = pd.DataFrame({k: pd.Series(v) for k, v in d.items()})
    return out


def garch_block(daily, T, block, cache, tgt, quick):
    from arch import arch_model
    r = daily.dropna() * 100
    r = r[r.index >= pd.Timestamp("1963-01-01")]
    fit_data = r[r.index.to_period("M") <= T]
    am = arch_model(fit_data, mean="Constant", vol="GARCH", p=1, q=1, dist="t")
    res = am.fit(disp="off")
    out = []
    for p in block:
        d = r[r.index.to_period("M") <= p]
        if quick:
            d = d.iloc[-5000:]
        fr = arch_model(d, mean="Constant", vol="GARCH", p=1, q=1, dist="t").fix(res.params)
        v = fr.forecast(horizon=21, reindex=False).variance.values[-1].sum() / 1e4
        out.append(np.log(v))
    return np.array(out)


# --------------------------------------------------------------------------- tests
def nw_se(x, lags):
    x = np.asarray(x) - np.mean(x)
    n = len(x)
    g0 = x @ x / n
    s = g0
    for l in range(1, lags + 1):
        s += 2 * (1 - l / (lags + 1)) * (x[l:] @ x[:-l] / n)
    return np.sqrt(max(s, 1e-30) / n)


def clark_west(y, bench, model, lags):
    f = (y - bench) ** 2 - ((y - model) ** 2 - (bench - model) ** 2)
    t = f.mean() / nw_se(f, lags)
    return float(t), float(1 - sps.norm.cdf(t))


def diebold_mariano(y, bench, model, lags):
    d = (y - bench) ** 2 - (y - model) ** 2
    t = d.mean() / nw_se(d, lags)
    return float(t), float(2 * (1 - sps.norm.cdf(abs(t))))


def r2_os(y, bench, model):
    return float(1 - np.sum((y - model) ** 2) / np.sum((y - bench) ** 2))


def score(preds, Y):
    rows = []
    for tgt in RET_T:
        P = preds[tgt]
        ok = P.index.intersection(Y.index[Y[tgt].notna()])
        y, b = Y.loc[ok, tgt].values, P.loc[ok, "hist_mean"].values
        lags = 12 if tgt.startswith("ret12") else 0
        for m in ["enet", "rf", "gbm", "mlp", "regime_rf", "ensemble"] + (["yield_anchor"] if "yield_anchor" in P else []):
            t, p = clark_west(y, b, P.loc[ok, m].values, max(lags, 1) if lags else 0)
            rows.append({"family": "R", "target": tgt, "model": m, "r2_os": r2_os(y, b, P.loc[ok, m].values),
                         "stat": t, "p_value": p, "n": len(ok), "benchmark": "historical mean"})
    for tgt in RISK_T:
        P = preds[tgt]
        ok = P.index.intersection(Y.index[Y[tgt].notna()])
        ok = [p for p in ok if not np.isnan(P.loc[p, "rw"])]
        y, b = Y.loc[ok, tgt].values, P.loc[ok, "rw"].values
        lags = 3 if tgt == "sbc3" else 1
        for m in ["har"] + (["garch"] if "garch" in P else []) + ["enet", "rf", "gbm", "mlp", "ensemble"]:
            t, p = diebold_mariano(y, b, P.loc[ok, m].values, lags)
            rows.append({"family": "K", "target": tgt, "model": m, "r2_os": r2_os(y, b, P.loc[ok, m].values),
                         "stat": t, "p_value": p, "n": len(ok), "benchmark": "random walk"})
    df = pd.DataFrame(rows)
    out = []
    for fam, g in df.groupby("family"):
        out.append(g.join(holm(g["p_value"])))
    return pd.concat(out)


def head_to_head(preds, Y):
    rows = []
    for tgt in RET_T:
        P = preds[tgt]
        ok = P.index.intersection(Y.index[Y[tgt].notna()])
        y = Y.loc[ok, tgt].values
        lags = 12 if tgt.startswith("ret12") else 1
        t, p = diebold_mariano(y, P.loc[ok, "rf"].values, P.loc[ok, "regime_rf"].values, lags)
        rows.append({"target": tgt, "r2_regimeRF_vs_RF": r2_os(y, P.loc[ok, "rf"].values, P.loc[ok, "regime_rf"].values),
                     "dm_stat": t, "p_value": p})
    df = pd.DataFrame(rows)
    return df.join(holm(df["p_value"]))


def regime_score(preds, Y):
    st, pe = preds["regime_next"]["stage1"], preds["regime_next"]["persist"]
    rows = []
    for p, prob in st.items():
        y = Y.loc[p, "regime_next"] if p in Y.index else None
        if not isinstance(y, str) or not isinstance(pe.get(p), str):
            continue
        rows.append({"p": p, "y": y, "hat": REG[int(np.argmax(prob))], "persist": pe[p], "py": prob[REG.index(y)]})
    d = pd.DataFrame(rows)
    acc_m, acc_p = (d.hat == d.y).mean(), (d.persist == d.y).mean()
    b = ((d.hat == d.y) & (d.persist != d.y)).sum()
    c = ((d.hat != d.y) & (d.persist == d.y)).sum()
    p_mc = float(sps.binomtest(int(b), int(b + c), 0.5).pvalue) if b + c > 0 else 1.0
    # persistence log loss: empirical transition probabilities from labels known before each month
    lab = Y["regime_next"].shift(1)
    ll_p = []
    for _, r in d.iterrows():
        hist = pd.DataFrame({"a": lab.loc[:r.p], "b": Y["regime_next"].loc[:r.p - 1]}).dropna()
        sub = hist[hist.a == r.persist]
        pr = ((sub.b == r.y).sum() + 1) / (len(sub) + 4)
        ll_p.append(-np.log(pr))
    return {"months": len(d), "accuracy_stage1": acc_m, "accuracy_persist": acc_p,
            "logloss_stage1": float(-np.log(np.clip(d.py, 1e-6, 1)).mean()), "logloss_persist": float(np.mean(ll_p)),
            "mcnemar_b_stage1_only_right": int(b), "mcnemar_c_persist_only_right": int(c), "mcnemar_p": p_mc}


# --------------------------------------------------------------------------- economic tests
def economic(preds, R, cfg):
    idx = pd.period_range(FIRST_OOS + 1, R.index[-1], freq="M")          # return months
    dec = [p - 1 for p in idx]
    rets = R.loc[idx, ASSETS + ["RF"]].rename(columns={"RF": "CASH"})
    vol36 = R[ASSETS].rolling(36).std()
    E = {}
    # E1: return tilt with ML-ensemble 1-month forecasts
    fc = pd.DataFrame({a: preds[f"ret1_{a}"]["ensemble"] for a in ASSETS})
    rows = []
    for d in dec:
        s = fc.loc[d] / vol36.loc[d]
        z = (s - s.mean()) / s.std() if s.std() > 0 else s * 0
        w = (1 / 3) * np.clip(np.exp(0.5 * z), 0.25, 3)
        rows.append(list(w / w.sum()) + [0.0])
    W1 = pd.DataFrame(rows, index=idx, columns=ASSETS + ["CASH"])
    core = pd.DataFrame([[1 / 3, 1 / 3, 1 / 3, 0.0]] * len(idx), index=idx, columns=ASSETS + ["CASH"])
    E["E1 return tilt"], _ = simulate(W1, rets, cfg)
    E["Core 1/3"], _ = simulate(core, rets, cfg)
    # E2: risk scaling with risk-ensemble variance forecasts
    vm, vu = np.exp(preds["lrv_mkt"]["ensemble"]), np.exp(preds["lrv_ust"]["ensemble"])
    gvol = R["GOLD"].rolling(12).std()
    corr36 = R[ASSETS].rolling(36).corr()
    fcv, a_list, hist = [], [], []
    for d in dec:
        sd = np.array([np.sqrt(vm.loc[d]), np.sqrt(vu.loc[d]), gvol.loc[d]])
        C = corr36.loc[d].loc[ASSETS, ASSETS].values
        w = np.full(3, 1 / 3)
        v = float(np.sqrt(w @ (np.outer(sd, sd) * C) @ w))
        target = np.median(hist) if hist else v
        a = min(1.0, target / v)
        hist.append(v)
        a_list.append(a)
        fcv.append(v)
    a_s = pd.Series(a_list, index=idx)
    W2 = pd.DataFrame({k: a_s / 3 for k in ASSETS}).assign(CASH=1 - a_s)
    E["E2 risk scaling"], _ = simulate(W2, rets, cfg)
    cbar = float((1 - a_s).mean())
    W2c = pd.DataFrame([[(1 - cbar) / 3] * 3 + [cbar]] * len(idx), index=idx, columns=ASSETS + ["CASH"])
    E[f"Core + {cbar:.0%} cash (static control)"], _ = simulate(W2c, rets, cfg)
    port = pd.DataFrame(E)
    rf = R.loc[idx, "RF"].values
    tests = []
    for a, b in (("E1 return tilt", "Core 1/3"), ("E2 risk scaling", port.columns[-1])):
        for stt in ("sharpe", "maxdd"):
            r = bootstrap_diff(port[a].values, port[b].values, rf, stt, **BOOT)
            tests.append({"test": a, "control": b, "statistic": "Sharpe" if stt == "sharpe" else "MaxDD", **r})
    T = pd.DataFrame(tests)
    return port, T.join(holm(T["p_value"])), cbar


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--out", default="results_study5")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    cfg = Config()
    cfg.cost_bps = {**cfg.cost_bps, "CASH": 0.0}
    raw_dir = ROOT / "data" / "raw"
    raw = load_raw(raw_dir, 12)
    panels = build_panels(raw)
    regimes = build_regimes(panels["macro"], panels["daily"], cfg.corr_window_days, cfg.zscore_min_periods, 1,
                            panels["interpolated"])
    baa = parse_fred_csv((raw_dir / "fred_BAA.csv").read_bytes())
    aaa = parse_fred_csv((raw_dir / "fred_AAA.csv").read_bytes())
    baa.index, aaa.index = baa.index.to_period("M"), aaa.index.to_period("M")
    F, Y, R, aux, d_mkt, d_ust = build_dataset(panels, raw, regimes, baa, aaa)
    out = ROOT / args.out
    out.mkdir(exist_ok=True)
    preds = walk_forward(F, Y, aux, d_mkt, d_ust, args.quick)
    for t, P in preds.items():
        if t != "regime_next":
            P.to_csv(out / f"pred_{t}.csv")
    sc = score(preds, Y)
    sc.to_csv(out / "scores.csv", index=False)
    h2h = head_to_head(preds, Y)
    h2h.to_csv(out / "head_to_head_regimeRF_vs_RF.csv", index=False)
    rs = regime_score(preds, Y)
    (out / "regime_classifier.json").write_text(json.dumps(rs, indent=2))
    port, et, cbar = economic(preds, R, cfg)
    port.to_csv(out / "economic_returns.csv")
    et.to_csv(out / "economic_tests.csv", index=False)
    est = stats_table(port, R["RF"])

    # current forecasts (latest decision month) for the site
    last = F.index[-1]
    cur = {"decision_month": str(last)}
    for t, P in preds.items():
        if t == "regime_next":
            cur["regime_probs"] = dict(zip(REG, map(float, P["stage1"][last]))) if last in P["stage1"] else None
        elif last in P.index:
            cur[t] = {k: float(v) for k, v in P.loc[last].items() if pd.notna(v)}
    cur["y10"] = float(F.loc[last, "y10"])
    cur["rf_annual"] = float(aux.loc[last, "RF"] * 12)
    (out / "current_forecasts.json").write_text(json.dumps(cur, indent=2))

    def fam_table(f):
        d = sc[sc.family == f].copy()
        d["r2_os"] = d["r2_os"].map(lambda v: f"{v * 100:+.2f}%")
        return md(d.set_index("target")[["model", "r2_os", "stat", "p_value", "holm_adj_p", "holm_reject_5pct", "n"]])
    rep = ["# Study 5 results: forecasting horse race", "",
           "Specification: `PREREGISTRATION_STUDY5.md`. Out-of-sample decision months 1989-12 onward, annual refits, "
           "expanding window. R² OS > 0 = better than the benchmark.", "",
           "## Family R: return forecasts vs historical mean (Clark-West, one-sided; Holm over the family)", "",
           fam_table("R"), "",
           "## Family K: risk forecasts vs random walk (Diebold-Mariano, two-sided; Holm over the family)", "",
           fam_table("K"), "",
           "## Regime-enhanced RF vs plain RF (Diebold-Mariano, two-sided; Holm over 6)", "",
           md(h2h.set_index("target")), "",
           "## Stage-1 regime classifier vs 'regime persists'", "",
           md(pd.DataFrame([rs]).T.rename(columns={0: "value"})), "",
           f"## Economic tests (Holm over 4); E2 static control holds {cbar:.1%} cash", "",
           md(et.set_index("test")[["control", "statistic", "diff", "ci_low", "ci_high", "p_value", "holm_adj_p", "holm_reject_5pct"]]), "",
           md(est, pct=["CAGR", "Vol", "MaxDD", "Worst month", "CVaR 5% (monthly)"]), "",
           "## Current forecasts (latest decision month)", "", "```json", json.dumps(cur, indent=2), "```"]
    (out / "report.md").write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
