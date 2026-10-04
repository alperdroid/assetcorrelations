# Study 4: is trend + cash (H4a) timing, or just holding cash?

*Pre-registered in `PREREGISTRATION_STUDY4.md` (commit 77004ff). This is a robustness /
decomposition analysis on data already seen in Study 3, not a confirmatory test. Full tables are
in `results_study4/report.md`.*

## Verdict

**H6 is not supported. Most of H4a's drawdown protection comes from holding cash, not from
timing.**

Developed ex US, 1991-07 to 2026-08:

| | Max DD | Sharpe | CAGR | Vol |
|---|---|---|---|---|
| Static 1/3 | -20.1% | 0.59 | 6.8% | 7.5% |
| C1: Static + constant 40.2% cash | -12.0% | 0.59 | 5.2% | 4.5% |
| C2: Static + 27.6% cash (same volatility as H4a) | -14.6% | 0.59 | 5.7% | 5.4% |
| **H4a Trend + cash** | **-10.4%** | **0.72** | **6.5%** | 5.4% |

Primary tests (H4a vs C1, Holm over 2):
- **Max drawdown:** +1.7 pp (CI [-3.9, +7.7] pp), p = 0.61.
- **Sharpe:** +0.13 (CI [-0.09, +0.35]), p = 0.26.

Neither is significant.

## How to read it

1. **Decomposition of the drawdown improvement.** Of H4a's 9.7-point improvement over Static 1/3,
   about 8.1 points come from holding cash (C1) and about 1.7 points from timing. The timing part
   is not distinguishable from zero.
2. **At the same volatility (C2, the fairer comparison), timing looks a little better.**
   - The drawdown is 4.2 pp shallower (p = 0.21) and CAGR is 0.8 pp higher.
   - The same sign appears in all four international regions (+3.8 to +6.0 pp) and in the US
     (+2.4 pp).
   - None of these differences is individually significant, and they are correlated (Study 3).
3. **A consistent but insignificant Sharpe edge.** H4a's Sharpe is higher than the cash-matched
   control in every universe (+0.10 to +0.26). That reaches p < 0.05 only in the US, which had
   already been seen (+0.22, p = 0.02).
4. **Crisis behaviour.**
   - H4a beat its cash-matched control in the dot-com bust and the GFC in every universe; it was
     positive in all of them, while C1 lost 1-8% in the GFC.
   - It also beat C1 in 2022 everywhere (Developed ex US -5.7% vs -9.7%).
   - It lost slightly more in the 1987 crash (-7.2% vs -5.1%, US), which came too fast for a
     12-month signal.

**Bottom line.** "Trend + cash halves drawdowns" is mostly "holding 40% cash reduces drawdowns."
Timing adds a small, consistently signed but statistically unproven improvement, concentrated in
slow bear markets (2000-02, 2008, 2022) and absent in sudden crashes (1987, 2020).
