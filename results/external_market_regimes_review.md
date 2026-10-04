# Triangulation: the market-regimes repository (Markov switching, GMM and random forest)

*Exploratory, not pre-registered. Source: [alperdroid/market-regimes](https://github.com/alperdroid/market-regimes)
(commit 817c515, read-only). The forward test is in `external/market_regimes_forward_test.py`, with
output in `results/external_market_regimes_forward_test.md`.*

## What that repository found (its own numbers)

The repository covers SPDR sector ETFs, 2006-2025, out of sample, net of 10 bp costs. It compares
three regime classifiers (a VIX rule, a walk-forward 3-state HMM, and a GMM), all feeding the same
portfolio construction.

| Strategy | Ann. return | Sharpe | Max DD |
|---|---|---|---|
| SPY buy-and-hold | 7.0% | 0.44 | -59.6% |
| HMM minimum variance | 6.6% | 0.53 | -37.3% |
| GMM minimum variance | 6.7% | 0.54 | -39.8% |
| VIX-rule minimum variance | 6.0% | 0.50 | -34.4% |
| HMM tangency (return timing) | 5.0% | 0.37 | -58.1% |

- **Headline:** the gains are risk reduction, not returns. Every return-timing (tangency) variant
  fails. White's Reality Check against SPY gives p = 0.98.
- **Classifier sophistication hardly matters:** the HMM and GMM give Sharpe 0.53-0.54, the simple
  VIX rule 0.50.
- **The random-forest strategy (GMM labels + RF, "ML-TPF")** appears only in an earlier notebook
  run: 10.2% a year, Sharpe 0.65.
  - That run used assumed turnover figures, not measured trading.
  - Its own significance note gives White's Reality Check p = 0.56, so no return edge over SPY
    after correcting for the search.
  - The current pipeline dropped it.

## Issues found while reviewing it

1. **One-day look-ahead on rebalance days** (`market_regimes/portfolio/backtest.py`).
   - On rebalance day t, the regime label for day t uses day t's own data (the VIX close and that
     day's returns). The new weights are then applied to day t's return (`w @ today_ret`).
   - The strategy therefore trades on knowledge of the rebalance day's move, about 1 day in 21.
   - This favours the regime strategies, particularly crisis-cash switches made on crash days.
   - **Fix:** apply new weights from day t+1.
   - Not fixed here: this session has read-only access to that repository.
2. **The regime statistics tables describe the past rather than forecast it.** The HMM's Calm
   regime has Sharpe +2.96 and its Crisis regime -0.90, but a day's label is partly determined by
   that day's own return. These tables say what regimes look like, not what follows them.

## Forward test of its saved out-of-sample labels

Today's label against the next 21 trading days of SPY, using 238 non-overlapping windows from
2006 to 2025.

| | Calm | Transitional | Crisis | Returns differ? (ANOVA p) |
|---|---|---|---|---|
| HMM: next-month SPY return, annualised | +5.1% | +12.8% | +32.1% | 0.15 |
| HMM: next-month volatility | 13.5% | 17.7% | 23.8% | |
| Ensemble: next-month SPY return | +5.8% | +11.1% | +39.7% | 0.06 |

- **Labels do not significantly forecast returns** (R² 1-2%, ANOVA p 0.06-0.22). The point
  estimates point the opposite way to "crisis means cash": after a Crisis label, SPY rebounded.
  Crisis-cash rules therefore cost return, and tangency variants built on regime means fail.
- **Labels carry volatility information, but less than a simple volatility measure.** Past
  21-day volatility alone explains 43% of next-month volatility. The labels explain 8% (HMM) to
  36% (VIX rule). Adding a label to past volatility adds only 0.2-2.6 points (HMM: 0.2).
- **The Markov states are not very persistent at a monthly horizon.** The HMM label is the same
  21 trading days later only 61% of the time (VIX rule: 75%).

## How this fits Studies 1-5

Three independent setups now agree:
- this study (macro regimes, 1972-2026, with US sectors, Treasuries and gold);
- Study 5 (ML horse race);
- market-regimes (Markov switching, GMM and random forest on sector ETFs, 2006-2025).

1. **Regime models do not forecast returns.** Markov switching, GMM, macro regimes and random
   forests all fail on return timing once tested out of sample and corrected for data snooping.
2. **What regime models capture is mostly volatility,** and a plain volatility forecast (past
   volatility, HAR) captures it as well or better.
3. **Their practical value is risk control.** Minimum-variance construction, cash and holding
   several hedges deliver it without needing a regime model.
