# Study 5: can machine learning forecast returns, risk or regimes?

*Pre-registered in `PREREGISTRATION_STUDY5.md` (commit 2cfa63a). The code and leakage tests were
committed before the real run (2283a42). Full tables are in `results_study5/report.md`.
Out-of-sample: decision months December 1989 to August 2026, annual refits on an expanding
window, using only data available at each decision date.*

## Verdict

| Question | Answer |
|---|---|
| Can ML forecast stock or Treasury returns? | **No.** No model beat the historical average after correction. Over 12 months every ML model was worse than the average; the neural net reached -79% R² on stocks. |
| Can it forecast gold returns? | **Only an artefact.** Elastic net "passed" for 1-month gold (R² +1.7%, adjusted p = 0.01), but a model using only gold's previous month did better (R² +2.6%). This is the autocorrelation that monthly-average prices create, and it cannot be traded. |
| Does the starting yield anchor 12-month Treasury returns? | **Promising but not proven.** R² +6.3%, the best 12-month result, but adjusted p = 0.83. |
| Can models forecast risk? | **Yes, volatility.** Stock volatility: R² +20% (HAR). Treasury volatility: R² +28% (HAR). HAR, GARCH and elastic net all pass. Complex ML adds nothing over HAR, and the neural net fails for Treasuries. |
| Can they forecast the stock-bond correlation? | **No.** Every ML model is worse than "same as the last 3 months". HAR: +10.7%, not significant. |
| Can a random forest forecast the next regime? | **No.** It was right 77% of the time, the same as "next month's regime = this month's" (77%), p = 1.00. |
| Does adding regime forecasts to a random forest help (the PI's two-stage model)? | **No.** The difference from the plain random forest is about 0 on all six return targets (all p ≥ 0.22). |
| Do the forecasts make a better portfolio? | **No significant gain.** ML return tilt: Sharpe 0.82 vs 0.77 for Core 1/3, adjusted p = 1.00. Risk-scaled core: worst drawdown -12.2% vs -14.0% for a static mix with the same 12% cash, adjusted p = 0.64. |

## What this means

1. **Return direction remains unforecastable with these inputs and models.** Machine learning
   does not change the Study 1-4 conclusion. More flexible models did worse out of sample: they
   fit noise in 200-640 training months.
2. **Risk is forecastable, and simple models are enough.** A three-term regression on past
   volatility (HAR) matched or beat GARCH and every ML model.
   - Useful: today's risk level is predictable.
   - Not useful: tests E2 and Study 4 found that acting on it did not improve drawdowns beyond
     simply holding cash.
3. **Regimes add nothing.** The regime classifier cannot beat persistence, and feeding its
   probabilities into a random forest changes nothing. This matches Study 1: even perfect regime
   knowledge was worth only +0.35 pp a year.

## What the site uses

The rules were set in the pre-registration.
- **Volatility conditioning:** the first 12 simulated months are rescaled to the HAR forecasts.
  As of August 2026, stock volatility is 0.67× its post-1990 average and Treasury volatility
  0.75×.
- **No return-mean conditioning.** The gold "pass" is excluded as an artefact (deviation below).
- **No yield anchor,** because it did not pass.
- **Results table:** the site shows the full horse race, including every failure.

## Deviation from the pre-registration

The pre-registered site rule would have used the passing gold 1-month forecast. It is excluded
because the diagnostic above shows the effect comes from the World Bank series being a monthly
average (Study 1, Section C):
- a pure AR(1) model on gold's own last month beats the elastic net out of sample;
- stocks rebuilt on monthly-average prices show the same autocorrelation (0.24, against 0.03 at
  month-end).

The diagnostic was run after the results were seen and is exploratory. The test result itself
is reported unchanged.

## Implementation details not specified in the pre-registration

- **Missing features:** where a real-time feature is missing (decision month 2025-11, see D7),
  features are forward-filled. This is what an investor would have had.
- **Stage-1 regime probabilities:** the earliest block of each training window gets that
  block's class frequencies, because time-series cross-validation produces no out-of-fold
  prediction for it.
- **Persistence log loss:** computed with Laplace-smoothed transition frequencies from labels
  known at the time. A hard 0/1 persistence forecast has infinite log loss.
