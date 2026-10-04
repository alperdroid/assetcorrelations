# Study 5 pre-registration: can models forecast returns, risk or regimes?

Written and committed 2026-10-04, **before any Study 5 code was written or any model was fitted**.
Before writing this, only availability was checked: the `arch` package installs, and FRED BAA/AAA
download for 1919-01 to 2026-09. The git commit is the timestamp. Later changes are logged at the
bottom, and the original text is kept.

## Why, and what we expect

The PI asked for a better forecast using machine learning, and for a two-stage "regime forecast +
random forest" model. The literature and Studies 1-4 suggest:
- **Monthly return direction is barely predictable.** Most predictors fail out of sample.
- **Volatility is predictable,** because it persists.
- **Starting yields anchor long-run Treasury returns.**
- **Regime knowledge has a low ceiling:** in Study 1, perfect regime knowledge added only
  +0.35 pp a year.

**Expectations stated in advance:**
- Return models will mostly fail to beat the historical mean.
- Risk models will beat the naive benchmark.
- The Treasury yield anchor will beat the historical mean at 12 months.
- The regime-enhanced random forest will not beat the plain random forest.

All results are reported whatever they show.

## Data and timing

Decision month t uses only information available at the end of month t:
- **Market data** (Ken French monthly and daily, FRED DGS10 daily, World Bank gold): through
  month t.
- **CPI and unemployment:** through t-1 (publication lag).
- **Philly Fed survey:** through t.
- **FRED BAA and AAA** (monthly averages of daily yields): through t.
- The October 2025 CPI/UNRATE gap is handled as in DEVIATIONS D7.

## Features (fixed list, decision month t)

1. **Rates:** 10y yield; term spread (10y yield minus annualised T-bill); credit spread
   (BAA - AAA).
2. **Macro:** CPI YoY; inflation score; growth score (Study 1, real time); 3-month change in
   unemployment; Philly Fed level.
3. **Momentum:** 1-month and 12-month returns of US stocks, the 10y Treasury and gold.
4. **Risk state:**
   - log realised variance of US stocks and of the 10y Treasury in month t (from daily data);
   - 3-month average log realised variance of stocks;
   - 63-day stock-bond correlation;
   - 12-month volatility of gold's monthly returns.
5. **Regime:** dummies for the Study 1 real-time label (Goldilocks is the omitted category).

## Targets

- **Returns (6 targets):** excess return over T-bills for US stocks (MKT), the 10y Treasury
  (UST10) and gold (GOLD), over:
  - the next month (t+1);
  - the next 12 months (t+1 to t+12, compounded).
- **Risk (3 targets):**
  - log realised variance of MKT in t+1;
  - log realised variance of UST10 in t+1;
  - the stock-bond correlation of daily returns over t+1 to t+3.
- **Regime (1 target):** the real-time regime label at decision month t+1.

## Walk-forward protocol

- **Training samples:** start at decision month 1973-01.
- **Out-of-sample forecasts:** decision months 1989-12 onward, so the first forecast target is
  1990-01.
- **Refits:** every 12 months, at each December decision month, on an expanding window.
- **No look-ahead in training:** a training sample is used only if its target was fully observed
  by the refit month. For 12-month targets the last 11 decision months are dropped; for the
  3-month correlation, the last 2.
- **Feature scaling** and all hyperparameter tuning use training data only.

## Models

### Benchmarks
- **Returns:** the expanding historical mean of the target.
- **Risk:** the random walk (last observed value of the same quantity).
- **Regime:** "the regime persists" (next label = current label).

### Return models (each target)
1. **Elastic net:** alpha and l1_ratio tuned by 5-fold time-series cross-validation inside each
   training window. Grid: alpha in {1e-4, 1e-3, 1e-2, 1e-1, 1}, l1_ratio in {0.2, 0.5, 0.8}.
2. **Random forest (RF):** 500 trees, max_depth 4, min_samples_leaf 24, max_features 0.5,
   seed 0.
3. **Gradient boosting:** scikit-learn HistGradientBoosting; learning_rate 0.03, max_depth 2,
   max_iter 200, l2_regularization 1.0, min_samples_leaf 24, seed 0.
4. **Neural net:** MLP (32, 16), ReLU, alpha 1e-3, early stopping, average of 5 seeds.
5. **Regime-enhanced RF (two-stage, requested by the PI):**
   - Stage 1 is an RF classifier (500 trees, max_depth 4, min_samples_leaf 12, seed 0) trained
     to predict the regime at t+1 from the features at t. Its training samples are fully
     observed regimes only.
   - Stage 2 is the RF of model 2, trained on the features plus the stage-1 predicted
     probabilities of the four regimes.
   - In training, stage-1 probabilities are out-of-fold: 5-fold time-series cross-validation
     inside the training window, so stage 2 never sees in-sample classifier fits.
6. **ML ensemble:** the simple average of models 1-4. Model 5 is excluded, so the ensemble
   stays a fixed control.
7. **Treasury yield anchor** (UST10, 12-month target only): forecast = the 10y yield minus
   12 × the T-bill rate. No estimation.

### Risk models (each risk target)
- **HAR:** OLS of the target on its own 1-, 3- and 12-month trailing averages.
- **GARCH(1,1)** (MKT and UST10 variance targets only):
  - fitted on daily returns with Student-t errors;
  - parameters refit at each December;
  - each month's forecast is the sum of the next 21 daily variance forecasts from data through
    month t.
- **Elastic net, RF, gradient boosting, neural net:** the same settings as above, on the full
  feature list.
- **Risk ensemble:** the average of the 4 ML models.

### Regime model
The stage-1 classifier of model 5, scored on its own.

## Scoring and tests

All scoring uses out-of-sample forecasts, decision months 1989-12 onward.

- **Returns:**
  - **Score:** out-of-sample R² vs the historical mean (Campbell-Thompson):
    1 - MSE(model) / MSE(mean).
  - **Test:** the Clark-West test for nested models (one-sided, model better), with Newey-West
    standard errors (12 lags for the 12-month targets).
  - **Family R:** the 6 targets × models 1-6, plus the yield anchor = 37 tests, Holm-corrected
    at 5%.
- **Risk:**
  - **Score:** out-of-sample R² vs the random walk, using MSE (log variance; correlation in its
    own units).
  - **Test:** Diebold-Mariano (two-sided, Newey-West, 3 lags for the overlapping correlation
    target).
  - **Family K:** MKT variance (HAR, GARCH, 4 ML, ensemble = 7); UST10 variance (7);
    correlation (HAR, 4 ML, ensemble = 6). 20 tests, Holm-corrected at 5%.
- **Regime:**
  - **Score:** accuracy and log loss of stage 1 vs "regime persists".
  - **Test:** a McNemar test on accuracy.
  - Reported, not in a family.
- **Head-to-head (the PI's question):** regime-enhanced RF vs plain RF on each of the 6 return
  targets. Same Clark-West/Diebold-Mariano machinery, two-sided, reported and Holm-corrected
  within these 6 comparisons.

## Economic tests (family E, 4 tests, Holm-corrected at 5%)

Same backtest engine, costs and bootstrap as Studies 2-4.

- **E1, return tilt:** each month, Core 1/3 weights are tilted by the ML-ensemble 1-month return
  forecasts:
  - s_i = forecast_i / trailing 36-month volatility_i;
  - z = s standardised across the 3 assets;
  - w_i ∝ (1/3) × exp(0.5 z_i), clipped to [0.25, 3] × 1/3 and renormalised (the Study 1 tilt
    rule).
  - Compared with Core 1/3: Sharpe difference and max-drawdown difference.
- **E2, risk scaling:**
  - risky weight = min(1, target / forecast core volatility), and the rest goes to T-bills;
  - forecast core volatility uses the risk-ensemble variance forecasts for MKT and UST10, gold's
    trailing 12-month volatility, and trailing 36-month correlations;
  - the target is the expanding median of past forecast core volatility.
  - Compared with a static Core 1/3 + cash portfolio holding E2's average cash share (the
    Study 4 design): Sharpe and max-drawdown differences.

## What the site's forecast will use (decided now)

- **Return forecasts:** replace resampled-history returns only for a target whose best model
  passes Holm in family R. Otherwise the page keeps resampled history and says that no return
  model beat the historical average.
- **Treasury yield anchor:** if it passes, simulated Treasury returns are shifted so their
  average equals the current yield. Otherwise no shift.
- **Volatility:** if a risk model passes Holm in family K for a target, the first 12 simulated
  months of that asset's returns are rescaled to the passing model's current volatility
  forecast. If several pass, the one with the highest out-of-sample R² is used. After month 12
  the rescaling stops. Otherwise no rescaling.
- **The site shows the full horse-race table,** including failures.

## Deviations from this plan

- **2026-10-04, after results.** The 1-month gold return forecast (elastic net) passed family R
  but is **not used by the site**. An exploratory diagnostic shows the predictability comes from
  the World Bank gold series being a monthly average:
  - an AR(1) model on gold's own last month has out-of-sample R² +2.55%, against +1.66% for the
    elastic net;
  - stocks rebuilt on monthly averages show the same lag-1 autocorrelation (0.24, against 0.03
    at month-end).
  The effect is not tradable. The test result is reported unchanged. See
  `results/study5_findings.md` and DEVIATIONS D15.
- **Implementation details not specified above:**
  - missing real-time features are forward-filled;
  - the earliest cross-validation block's stage-1 probabilities are set to that block's class
    frequencies;
  - persistence log loss uses Laplace-smoothed transition frequencies.
