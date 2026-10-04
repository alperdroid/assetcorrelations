# Study 3 pre-registration: trend with a cash fallback, and an international confirmation of volatility management

Written and committed 2026-10-04, **before any Study 3 code was written or any international
return was examined**. Before writing this, only the file structure and date ranges of the
international files were checked (1990-07 to 2026-08, no missing values). The git commit is the
timestamp. Any later change is logged at the bottom, and the original text is kept.

## Why this study, and what has already been seen

Study 2 (`PREREGISTRATION.md`, `results/study2_findings.md`) showed two things:
- The trend rule H2a failed in 2022 because, with no cash allowed, its fallback was 100%
  Treasuries.
- Volatility-managed equity (H3) gave a small drawdown improvement in every variant, but it was
  not significant (Sharpe diff +0.00, max drawdown diff +3.1 pp, p = 0.24).

The PI approved both follow-ups on 2026-10-04, including **allowing cash (T-bills) for the first
time**. That is a change to the Study 1 and 2 design and applies to Study 3 only.

What has already been seen, and how this study handles it:
- **The US data (1973-2026) has been seen** for trend rules, including how they behaved in
  1973-89. US results are therefore reported as **secondary and exploratory**.
- **The primary test uses data neither study has used:** the Ken French international equity
  markets, in US dollars, from 1990-07.
- The Treasury and gold series in those portfolios are the same US series as before, so only the
  equity leg is new. This is a partial out-of-sample test, and is stated as such.

## Data

- **New data, from the Ken French Data Library:** regional 3-factor files, monthly and daily,
  1990-07 to 2026-08. Regional equity return = Mkt-RF + RF.
  - **Primary region:** Developed ex US (`Developed_ex_US_3_Factors[_Daily]_CSV.zip`).
  - **Secondary regions:** Europe, Japan, Asia Pacific ex Japan.
- **As in Studies 1 and 2:**
  - UST10 = 10y total return from FRED DGS10;
  - GOLD = World Bank monthly average;
  - CASH = 1-month T-bill (Fama-French RF);
  - US equity (secondary universe) = Fama-French Mkt-RF + RF.

## Common setup

- **Universe for each region:** EQ (that region's equity market), UST10, GOLD and, for H4 only,
  CASH.
- **Control for every hypothesis:** Static 1/3 = 1/3 EQ, 1/3 UST10, 1/3 GOLD, rebalanced monthly.
- **Timing:** weights for return month t use only information available at the end of month t-1.
- **Constraints:** long-only and fully invested. Cash is allowed only where stated (H4).
- **Transaction costs:** as before (equity 10 bp, UST10 5 bp, gold 15 bp, one-way per unit of
  turnover). Cash costs nothing.
- **Evaluation windows:**
  - International: return months 1991-07 to 2026-08. 1991-07 is the first month with 12 months
    of returns and realised variance history.
  - US (secondary): 1973-01 to 2026-08, the same as Study 2.

## Hypotheses

### H4a: Trend with cash, Faber style
- **Rule:** each 1/3 sleeve (EQ, UST10, GOLD) is held if its compounded return over months t-12
  to t-1 beats compounded T-bills over the same months. Otherwise that sleeve goes to CASH.
- **Literature:** Faber (2007) and Moskowitz-Ooi-Pedersen (2012).
- **Claim:** this improves on Static 1/3, with a higher Sharpe ratio and a shallower max drawdown.

### H4b: Study 2's H2a with a cash fallback
- **Rule:** the same as Study 2's H2a. A failing sleeve's weight is redistributed equally to the
  passing sleeves, but when NO sleeve passes the portfolio holds 100% CASH instead of 100% UST10.
- **Claim:** as for H4a.

### H5: Volatility-managed equity, confirmatory
- **Rule:** exactly Study 2's H3.
  - Equity weight w = clip((1/3) × target / RV(t-1), 0, 2/3), where RV(t-1) is the sum of
    squared daily EQ returns in month t-1.
  - The target is the expanding mean of monthly RV up to t-1, with at least 12 months. For the
    US, the history runs from 1926.
  - UST10 and GOLD each get (1 - w)/2. There is no cash.
- **Claim:** this improves on Static 1/3, with a higher Sharpe ratio and a shallower max drawdown.
- **Expectation stated in advance:** a small effect. Study 2 found +0.00 Sharpe and +3.1 pp
  drawdown on US data, so this test may lack power. A null result would be informative.

## Tests

- **PRIMARY family (Developed ex US, 1991-07 to 2026-08):** {H4a, H4b, H5} × {Sharpe difference,
  max drawdown difference} = 6 tests, Holm-corrected at 5%.
  - Method: paired stationary block bootstrap (mean block 12, 5,000 resamples, seed 20260101),
    two-sided, centred.
  - A hypothesis is SUPPORTED only if its Sharpe test survives Holm with a positive difference
    AND its max drawdown is no worse than the control's.
- **SECONDARY family:** Europe, Japan and Asia Pacific ex Japan × {H4a, H4b, H5} × Sharpe
  difference = 9 tests, Holm-corrected within the family. Max drawdown is reported for each.
- **SECONDARY, exploratory:** the US universe, 1973-2026 and the sub-periods 1973-89 and
  1990-2026, all of which have been seen. Reported without a confirmatory claim.
- **Also reported:**
  - CAGR, volatility, Calmar, CVaR 5%, worst month, turnover and average cash weight;
  - cumulative returns in the stress episodes that fall inside each window, including 2022 (the
    motivating case for H4) and 2025.

## Robustness variants (reported, not in any test family)

- **R1** H4a and H4b with a 12-1 signal (months t-13 to t-2).
- **R2** H5 uncapped (w in [0, 1]).
- **R3** Transaction costs doubled.

## Deviations from this plan

(none yet)
