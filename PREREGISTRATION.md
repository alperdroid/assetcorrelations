# Study 2 pre-registration: rule-based hedging strategies

Written and committed 2026-10-04, **before any Study 2 strategy was coded or run**. The git
commit of this file is the timestamp. Any later change is logged at the bottom with a reason,
and the original text is kept.

## Context and honesty statement

Study 1 (README.md; `results/findings_draft.md`) found that a macro regime signal did not
improve on static diversification. A static mix of 1/3 US market, 1/3 10y Treasury and 1/3 gold
had the shallowest drawdown (1990-2026 max drawdown -15.8%). The hypotheses below were chosen
**after** seeing Study 1's 1990-2026 results; the PI chose them on 2026-10-04 from a short list.
They are therefore not independent of the data.

Mitigations:
- All parameters are literature defaults or fixed below, never tuned.
- Every rule is a fixed formula with no estimation window, so it can be evaluated from 1973.
- **1973-1989 has not been used to judge any strategy.** In Study 1 it was only a training and
  descriptive period, so it is reported separately as the cleanest out-of-sample evidence.
- All hypotheses and variants are reported, and primary tests are Holm-corrected.

## Common setup (identical for all hypotheses)

- **Assets and data:** as in Study 1.
  - MKT = Fama-French Mkt-RF + RF.
  - UST10 = 10y constant-maturity total return from FRED DGS10.
  - GOLD = World Bank monthly average (DEVIATIONS D2).
  - Sectors = Ken French 12 value-weighted industries.
  - RF = 1-month T-bill.
- **Timing:** weights for return month t use only information available at the end of month t-1.
- **Constraints:** long-only, fully invested, no cash, monthly rebalancing.
- **Transaction costs:** as Study 1 (equities 10 bp, Treasuries 5 bp, gold 15 bp, one-way, per
  unit of turnover).
- **Evaluation window:** return months 1973-01 to 2026-08. Signals may use earlier data (1972
  returns, daily data from 1926/1962).
- **Sub-periods (reported, not Holm-corrected):** 1973-01 to 1989-12 (unseen) and 1990-01 to
  2026-08 (seen in Study 1).

## Hypotheses (primary specifications)

### H1: Bond-hedge switch
- **Signal:** the 63-trading-day correlation of daily MKT and UST10 returns on the last trading
  day of month t-1. This is the same window Study 1 fixed in `config.py` before results.
- **Rule:**
  - If the correlation is > 0 (bonds currently not hedging), the weights are MKT 1/3, GOLD 2/3,
    UST10 0 (the Treasury sleeve moves to gold).
  - Otherwise the weights are Static 1/3.
- **Control:** Static 1/3.
- **H1:** the switch improves on Static 1/3, with a higher Sharpe ratio and a shallower max
  drawdown.

### H2a: Trend-following overlay, 3 assets
- **Signal:** the trailing 12-month total return of each asset (months t-12 to t-1) against the
  compounded T-bill return over the same months (time-series momentum, Moskowitz-Ooi-Pedersen
  2012).
- **Rule:**
  - Start from 1/3 in each of MKT, UST10 and GOLD.
  - An asset whose 12-month return does not beat T-bills loses its weight, which is spread
    equally over the assets that pass.
  - If no asset passes, hold 100% UST10, the closest asset to cash in a no-cash universe.
- **Control:** Static 1/3.

### H2b: Trend-following overlay, sectors
- **Rule:** the same as H2a on 14 assets (12 sectors, UST10 and GOLD), starting from equal weights
  of 1/14.
- **Control:** a static equal-weight portfolio of the 14 assets.

### H3: Volatility-managed equity
- **Signal:** RV(t-1), the realised variance of the market, i.e. the sum of squared daily MKT
  returns in month t-1. The target is the expanding mean of all monthly RV values from 1926-07
  to t-1, which is real-time and replaces Moreira & Muir's (2017) full-sample constant.
- **Rule:**
  - Equity weight w = clip((1/3) × target / RV(t-1), 0, 2/3). The cap of twice the base weight
    is our choice, fixed here.
  - UST10 and GOLD each get (1 - w)/2.
- **Control:** Static 1/3.

## Tests

- **Statistics:** for each hypothesis against its control, the Sharpe ratio difference and the
  max drawdown difference over 1973-01 to 2026-08.
- **Method:** paired stationary block bootstrap, as in Study 1 (mean block 12 months, 5,000
  resamples, seed 20260101), with a two-sided centred p-value.
- **Family:** 4 hypotheses × 2 statistics = 8 tests, **Holm-corrected at 5%**. A hypothesis is
  "supported" only if its Sharpe test survives Holm with a positive difference AND its drawdown
  difference is ≥ 0. Drawdown p-values are indicative, because block resampling shortens long
  drawdowns.
- **Also reported, not tests:**
  - CAGR, volatility, Calmar, CVaR 5%, worst month, turnover;
  - 60/40 and Static 1/3 rows;
  - sub-period statistics and bootstrap p-values (1973-89, 1990-2026);
  - cumulative returns in the Study 1 stress episodes (including 1973-74, 1980-82, 1987, 2008,
    2022 and 2025).

## Robustness variants (reported in full, not part of the Holm family)

- **R1** H1 with a 252-day correlation window.
- **R2** H2a and H2b with a 12-1 signal (months t-13 to t-2, skipping the latest month). This
  matters because averaged gold has positive autocorrelation (0.27, Study 1 Section C), which can
  flatter a trend rule on gold that includes the latest month.
- **R3** H2a and H2b with a 10-month lookback (Faber 2007).
- **R4** H3 without the cap (w clipped to [0, 1] only).
- **R5** All primary rules with every asset on monthly-average prices (`--avg-prices` basis,
  Study 1 D10).
- **R6** Transaction costs doubled.

## Deviations from this plan

(none yet)
