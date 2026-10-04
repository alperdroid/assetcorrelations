# Study 4 pre-registration: is trend + cash (H4a) timing, or just holding cash?

Written and committed 2026-10-04, before any Study 4 code or result existed. **Status:
robustness / decomposition analysis on data already seen in Study 3.** It is not a confirmatory
test, and it is reported as such.

## Question

In Study 3, H4a (each 1/3 sleeve of equity, UST10 and GOLD goes to T-bills when its 12-month
return is below T-bills) roughly halved max drawdown against Static 1/3 in all five universes. It
also held about 40% cash on average. Does the trend timing add protection beyond what a constant
cash allocation of the same size would give?

## Controls (per universe, same window as Study 3)

- **C1, cash-matched static:** a constant mix of (1 - c) × Static 1/3 + c × CASH, rebalanced
  monthly with the same costs (cash costs nothing). c is H4a's average cash weight over the
  evaluation window. This is computed after the fact and is a benchmark, not a tradable strategy.
- **C2, volatility-matched static (secondary):** the same construction, with c chosen so that
  C2's realised volatility equals H4a's over the window (solved numerically).

## Hypothesis

- **H6:** H4a has a shallower max drawdown AND a higher Sharpe ratio than C1.
- **Primary test (Developed ex US, 1991-07 to 2026-08):**
  - max drawdown difference (H4a - C1) and Sharpe difference (H4a - C1);
  - paired stationary block bootstrap (mean block 12, 5,000 resamples, seed 20260101), two-sided,
    centred;
  - Holm correction over these 2 tests.
  - SUPPORTED only if both differences favour H4a AND at least one survives Holm at 5%.
- **Also reported, not tests:**
  - the same comparisons for Europe, Japan, Asia Pacific ex Japan and the US (1973-2026), and
    against C2;
  - CAGR, volatility, Calmar, CVaR 5% and worst month;
  - returns in the stress episodes, including 2022.

## Expectation stated in advance

Scaling a portfolio down with cash shrinks its drawdown roughly in proportion. So C1's drawdown
should be about 60% of Static 1/3's (around -12% in Developed ex US), against -10.4% for H4a. A
small or insignificant gap is the expected result. If so, H4a's protection is mostly holding cash.

## Deviations from this plan

(none yet)
