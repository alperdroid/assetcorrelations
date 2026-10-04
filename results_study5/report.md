# Study 5 results: forecasting horse race

Specification: `PREREGISTRATION_STUDY5.md`. Out-of-sample decision months 1989-12 onward, annual refits, expanding window. R² OS > 0 = better than the benchmark.

## Family R: return forecasts vs historical mean (Clark-West, one-sided; Holm over the family)

| target | model | r2_os | stat | p_value | holm_adj_p | holm_reject_5pct | n |
|---|---|---|---|---|---|---|---|
| ret1_MKT | enet | +0.00% | 0.71 | 0.24 | 1.00 | False | 440 |
| ret1_MKT | rf | -2.50% | -0.07 | 0.53 | 1.00 | False | 440 |
| ret1_MKT | gbm | -8.68% | 0.00 | 0.50 | 1.00 | False | 440 |
| ret1_MKT | mlp | -6.30% | -0.55 | 0.71 | 1.00 | False | 440 |
| ret1_MKT | regime_rf | -2.62% | -0.20 | 0.58 | 1.00 | False | 440 |
| ret1_MKT | ensemble | -2.49% | -0.24 | 0.60 | 1.00 | False | 440 |
| ret1_UST10 | enet | +1.05% | 1.69 | 0.05 | 1.00 | False | 440 |
| ret1_UST10 | rf | -1.46% | 0.89 | 0.19 | 1.00 | False | 440 |
| ret1_UST10 | gbm | -6.34% | 0.78 | 0.22 | 1.00 | False | 440 |
| ret1_UST10 | mlp | -7.00% | 0.52 | 0.30 | 1.00 | False | 440 |
| ret1_UST10 | regime_rf | -1.29% | 1.03 | 0.15 | 1.00 | False | 440 |
| ret1_UST10 | ensemble | -0.99% | 0.95 | 0.17 | 1.00 | False | 440 |
| ret1_GOLD | enet | +1.66% | 3.49 | 0.00 | 0.01 | True | 440 |
| ret1_GOLD | rf | +1.71% | 2.62 | 0.00 | 0.16 | False | 440 |
| ret1_GOLD | gbm | -6.63% | 1.27 | 0.10 | 1.00 | False | 440 |
| ret1_GOLD | mlp | -7.03% | 0.58 | 0.28 | 1.00 | False | 440 |
| ret1_GOLD | regime_rf | +1.40% | 2.47 | 0.01 | 0.24 | False | 440 |
| ret1_GOLD | ensemble | +0.59% | 1.73 | 0.04 | 1.00 | False | 440 |
| ret12_MKT | enet | -0.01% | -0.16 | 0.56 | 1.00 | False | 429 |
| ret12_MKT | rf | -14.08% | -1.11 | 0.87 | 1.00 | False | 429 |
| ret12_MKT | gbm | -27.72% | -0.10 | 0.54 | 1.00 | False | 429 |
| ret12_MKT | mlp | -78.86% | -2.19 | 0.99 | 1.00 | False | 429 |
| ret12_MKT | regime_rf | -15.94% | -1.32 | 0.91 | 1.00 | False | 429 |
| ret12_MKT | ensemble | -20.05% | -1.41 | 0.92 | 1.00 | False | 429 |
| ret12_UST10 | enet | +5.27% | 1.82 | 0.03 | 1.00 | False | 429 |
| ret12_UST10 | rf | -1.14% | 1.88 | 0.03 | 0.96 | False | 429 |
| ret12_UST10 | gbm | -11.01% | 1.34 | 0.09 | 1.00 | False | 429 |
| ret12_UST10 | mlp | -36.33% | 0.32 | 0.37 | 1.00 | False | 429 |
| ret12_UST10 | regime_rf | -3.51% | 1.75 | 0.04 | 1.00 | False | 429 |
| ret12_UST10 | ensemble | -1.56% | 1.44 | 0.08 | 1.00 | False | 429 |
| ret12_UST10 | yield_anchor | +6.30% | 1.96 | 0.03 | 0.83 | False | 429 |
| ret12_GOLD | enet | -0.01% | -1.06 | 0.86 | 1.00 | False | 429 |
| ret12_GOLD | rf | -9.54% | 1.04 | 0.15 | 1.00 | False | 429 |
| ret12_GOLD | gbm | -12.63% | 2.04 | 0.02 | 0.70 | False | 429 |
| ret12_GOLD | mlp | -60.88% | -0.81 | 0.79 | 1.00 | False | 429 |
| ret12_GOLD | regime_rf | -7.92% | 1.13 | 0.13 | 1.00 | False | 429 |
| ret12_GOLD | ensemble | -5.59% | 0.95 | 0.17 | 1.00 | False | 429 |

## Family K: risk forecasts vs random walk (Diebold-Mariano, two-sided; Holm over the family)

| target | model | r2_os | stat | p_value | holm_adj_p | holm_reject_5pct | n |
|---|---|---|---|---|---|---|---|
| lrv_mkt | har | +20.00% | 4.15 | 0.00 | 0.00 | True | 440 |
| lrv_mkt | garch | +19.32% | 5.01 | 0.00 | 0.00 | True | 440 |
| lrv_mkt | enet | +19.46% | 3.45 | 0.00 | 0.01 | True | 440 |
| lrv_mkt | rf | +11.20% | 1.56 | 0.12 | 0.59 | False | 440 |
| lrv_mkt | gbm | +14.10% | 2.17 | 0.03 | 0.27 | False | 440 |
| lrv_mkt | mlp | +16.83% | 2.70 | 0.01 | 0.08 | False | 440 |
| lrv_mkt | ensemble | +18.83% | 3.19 | 0.00 | 0.02 | True | 440 |
| lrv_ust | har | +27.76% | 6.35 | 0.00 | 0.00 | True | 440 |
| lrv_ust | garch | +20.65% | 4.43 | 0.00 | 0.00 | True | 440 |
| lrv_ust | enet | +15.77% | 3.48 | 0.00 | 0.01 | True | 440 |
| lrv_ust | rf | +14.23% | 2.50 | 0.01 | 0.13 | False | 440 |
| lrv_ust | gbm | +17.43% | 3.06 | 0.00 | 0.03 | True | 440 |
| lrv_ust | mlp | +0.38% | 0.04 | 0.97 | 0.97 | False | 440 |
| lrv_ust | ensemble | +18.47% | 3.42 | 0.00 | 0.01 | True | 440 |
| sbc3 | har | +10.74% | 1.54 | 0.12 | 0.59 | False | 438 |
| sbc3 | enet | -20.70% | -1.74 | 0.08 | 0.52 | False | 438 |
| sbc3 | rf | -16.44% | -1.30 | 0.19 | 0.59 | False | 438 |
| sbc3 | gbm | -24.86% | -1.78 | 0.07 | 0.52 | False | 438 |
| sbc3 | mlp | -25.98% | -1.87 | 0.06 | 0.49 | False | 438 |
| sbc3 | ensemble | -14.84% | -1.20 | 0.23 | 0.59 | False | 438 |

## Regime-enhanced RF vs plain RF (Diebold-Mariano, two-sided; Holm over 6)

| target | r2_regimeRF_vs_RF | dm_stat | p_value | holm_reject_5pct | holm_adj_p |
|---|---|---|---|---|---|
| ret1_MKT | -0.00 | -0.35 | 0.72 | False | 1.00 |
| ret1_UST10 | 0.00 | 0.38 | 0.71 | False | 1.00 |
| ret1_GOLD | -0.00 | -0.80 | 0.42 | False | 1.00 |
| ret12_MKT | -0.02 | -1.11 | 0.27 | False | 1.00 |
| ret12_UST10 | -0.02 | -1.22 | 0.22 | False | 1.00 |
| ret12_GOLD | 0.01 | 1.21 | 0.22 | False | 1.00 |

## Stage-1 regime classifier vs 'regime persists'

|  | value |
|---|---|
| months | 438.00 |
| accuracy_stage1 | 0.77 |
| accuracy_persist | 0.77 |
| logloss_stage1 | 0.71 |
| logloss_persist | 0.74 |
| mcnemar_b_stage1_only_right | 5.00 |
| mcnemar_c_persist_only_right | 6.00 |
| mcnemar_p | 1.00 |

## Economic tests (Holm over 4); E2 static control holds 11.9% cash

| test | control | statistic | diff | ci_low | ci_high | p_value | holm_adj_p | holm_reject_5pct |
|---|---|---|---|---|---|---|---|---|
| E1 return tilt | Core 1/3 | Sharpe | 0.05 | -0.09 | 0.19 | 0.44 | 1.00 | False |
| E1 return tilt | Core 1/3 | MaxDD | -0.01 | -0.05 | 0.03 | 0.59 | 1.00 | False |
| E2 risk scaling | Core + 12% cash (static control) | Sharpe | 0.01 | -0.06 | 0.07 | 0.80 | 1.00 | False |
| E2 risk scaling | Core + 12% cash (static control) | MaxDD | 0.02 | -0.01 | 0.04 | 0.16 | 0.64 | False |

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) | Months |
|---|---|---|---|---|---|---|---|---|
| E1 return tilt | 9.1% | 7.7% | 0.82 | -16.7% | 0.55 | -6.3% | -4.0% | 440.00 |
| Core 1/3 | 8.0% | 6.9% | 0.77 | -15.8% | 0.51 | -7.0% | -3.5% | 440.00 |
| E2 risk scaling | 7.2% | 5.8% | 0.77 | -12.2% | 0.59 | -4.5% | -2.9% | 440.00 |
| Core + 12% cash (static control) | 7.4% | 6.1% | 0.77 | -14.0% | 0.53 | -6.1% | -3.1% | 440.00 |

## Current forecasts (latest decision month)

```json
{
  "decision_month": "2026-08",
  "ret1_MKT": {
    "enet": 0.006297637795275591,
    "rf": 0.003906432128487974,
    "gbm": -0.00012079763467529825,
    "mlp": 6.14283772687671e-05,
    "ensemble": 0.0025361751665892583,
    "hist_mean": 0.006297637795275591,
    "regime_rf": 0.0038369089311500754
  },
  "ret1_UST10": {
    "enet": 0.001790651716615282,
    "rf": -0.0024515430629116685,
    "gbm": -0.001037160766365478,
    "mlp": 0.0007774816811186214,
    "ensemble": -0.00023014260788581083,
    "hist_mean": 0.001790651716615282,
    "regime_rf": -0.002440320712036175
  },
  "ret1_GOLD": {
    "enet": 0.011641493863524192,
    "rf": 0.027514258963250677,
    "gbm": 0.039037654623768354,
    "mlp": 0.02395936453011972,
    "ensemble": 0.02553819299516574,
    "hist_mean": 0.004185701852745564,
    "regime_rf": 0.028342884772897876
  },
  "ret12_MKT": {
    "enet": 0.08338946791361108,
    "rf": -0.0573728582593606,
    "gbm": -0.09225160074599072,
    "mlp": -0.1402145969535064,
    "ensemble": -0.051612397011311664,
    "hist_mean": 0.08338946791361108,
    "regime_rf": -0.040916843599222
  },
  "ret12_UST10": {
    "enet": 0.00890673884445732,
    "rf": 0.0006243028831081621,
    "gbm": -0.012389483239419505,
    "mlp": -0.0632084033910253,
    "ensemble": -0.01651671122571983,
    "hist_mean": 0.023513203200089483,
    "regime_rf": 0.0039017652944734593,
    "yield_anchor": 0.012700000000000003
  },
  "ret12_GOLD": {
    "enet": 0.051692275927323963,
    "rf": 0.10703959371146664,
    "gbm": 0.16021730072449417,
    "mlp": 0.212132573578434,
    "ensemble": 0.1327704359854297,
    "hist_mean": 0.051692275927323963,
    "regime_rf": 0.09755169463222732
  },
  "lrv_mkt": {
    "enet": -6.68465665478472,
    "rf": -6.7272071150254495,
    "gbm": -6.666800145052975,
    "mlp": -6.708723289682203,
    "ensemble": -6.696846801136337,
    "rw": -6.917664210692261,
    "har": -6.718379109709286,
    "garch": -6.888942103332267
  },
  "lrv_ust": {
    "enet": -8.213710346624248,
    "rf": -8.301279637682763,
    "gbm": -8.547812217090616,
    "mlp": -8.814975034554983,
    "ensemble": -8.469444308988152,
    "rw": -8.236213219449589,
    "har": -8.276938218666562,
    "garch": -8.219241578885311
  },
  "sbc3": {
    "enet": 0.2441295779267743,
    "rf": 0.06841995379867458,
    "gbm": 0.07213512663471139,
    "mlp": 0.04804701907048481,
    "ensemble": 0.10818291935766126,
    "rw": 0.471985369669044,
    "har": 0.35792777084345545
  },
  "regime_probs": {
    "G": 0.10364238385482538,
    "R": 0.7994137960271581,
    "S": 0.08320724122972291,
    "D": 0.013736578888294312
  },
  "y10": 0.0475,
  "rf_annual": 0.0348
}
```