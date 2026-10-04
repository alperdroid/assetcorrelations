# Study 2: rule-based hedging strategies, findings

*Pre-registered in `PREREGISTRATION.md` (commit 265f2d6). The code and tests were committed
before the real-data run (commit c8851cf). Full tables are in
`results_study2/report.md`. Evaluation: return months 1973-01 to 2026-08 (644 months), after
costs. Gold is the World Bank monthly average. 1973-89 had not been used to judge any strategy
before this study.*

## Verdict

**None of the three pre-registered hypotheses is supported.** One is significantly contradicted.

| Hypothesis | Control | Sharpe diff | Max DD diff | Verdict |
|---|---|---|---|---|
| H1 Bond-hedge switch | Static 1/3 | **-0.20** (Holm p = 0.04) | **-19.4 pp** (Holm p = 0.05) | **Rejected: significantly worse** |
| H2a Trend, 3 assets | Static 1/3 | +0.12 (Holm p = 0.97) | -8.1 pp (p = 0.14) | Not supported |
| H2b Trend, sectors | Equal-weight 14 | +0.10 (Holm p = 0.97) | +13.6 pp (p = 0.18) | Not supported |
| H3 Vol-managed equity | Static 1/3 | +0.00 (Holm p = 0.97) | +3.1 pp (p = 0.24) | Not supported |

Performance, 1973-01 to 2026-08:

| Strategy | CAGR | Vol | Sharpe | Max DD | Turnover per month |
|---|---|---|---|---|---|
| Static 1/3 | 9.2% | 8.2% | 0.59 | -20.2% | 1.2% |
| 60/40 | 9.5% | 10.3% | 0.52 | -29.0% | 0.9% |
| H1 Bond-hedge switch | 8.4% | 11.3% | 0.39 | -39.6% | 3.8% |
| H2a Trend, 3 assets | 13.0% | 12.3% | 0.71 | -28.3% | 12.0% |
| H2b Trend, sectors | 12.4% | 13.0% | 0.64 | -28.7% | 17.4% |
| H3 Vol-managed equity | 9.6% | 9.0% | 0.59 | -17.1% | 11.0% |

## What each test shows

**H1: switching from bonds to gold when the stock-bond correlation is positive backfires.**
- Before 1990 the correlation was positive in 95% of months, so the rule held 2/3 gold almost
  continuously. It then took gold's 1980-82 collapse: a max drawdown of -39.6% from 1980-09 to
  1982-06, against -20.2% for Static 1/3.
- After 1990 it is also slightly worse (Sharpe -0.16, p = 0.03 unadjusted).
- A positive stock-bond correlation is a poor signal for what will hedge next. Replacing one hedge
  with the other concentrates risk; holding both is what worked.
- The result does not depend on the correlation window (252 days: Sharpe 0.42, same drawdown).

**H2a: trend-following raised returns but not protection, and failed in 2022.**
- It earned the highest CAGR (13.0%) and Sharpe (0.71), but none of the gain is statistically
  reliable after correction. Its drawdown was worse than Static 1/3 (-28.3% vs -20.2%).
- The whole Sharpe gain comes from 1973-89 (+0.39, p = 0.02 unadjusted). From 1990 the
  difference was -0.02.
- **1973-74:** only gold was trending, so the rule held 96% gold (+113.5% over the episode).
- **2022:** its worst drawdown (December 2021 to October 2022). Nothing was trending, so the
  pre-registered fallback held 100% Treasuries in June and from August to October, during the
  worst bond year in the sample.
  - In a no-cash universe, a trend rule has nowhere to go when every asset falls. The fallback
    asset decides the outcome.
- The averaging bias in gold does not explain the gain: the skip-month signal still gives a
  Sharpe of 0.67 (vs 0.71). The 10-month version gives 0.76. Doubling costs gives 0.69.

**H2b: trend on sectors cuts the equal-weight portfolio's drawdown, but not significantly.**
- Max drawdown -28.7% vs -42.3% for the static equal-weight 14-asset portfolio. That difference
  is meaningful in size, but the p-value is 0.18 and turnover is high (17% a month).
- It is not better than Static 1/3 on drawdown (-28.7% vs -20.2%).

**H3: volatility management gives a small, consistent drawdown improvement that is not
significant.**
- Same Sharpe as Static 1/3 (0.59). Max drawdown -17.1% vs -20.2% over the full sample and
  -14.8% vs -15.8% since 1990.
- It is the only rule whose drawdown was no worse than Static 1/3's in every variant (uncapped,
  averaged prices, doubled costs).
- It is the most promising direction, but the evidence is too weak to claim an effect
  (p = 0.24).

## Synthesis across Studies 1 and 2

1. **The simplest portfolio remains the one to beat.** Holding 1/3 equities, 1/3 Treasuries and
   1/3 gold with monthly rebalancing was not beaten on drawdown by any regime-based or rule-based
   strategy:
   - 2 studies, 9 active strategies (Study 1: Regime Tilt, Regime ERC, Uncond. Tilt, Uncond. ERC,
     Oracle Tilt; Study 2: H1, H2a, H2b, H3);
   - drawdown -20.2% since 1973 and -15.8% since 1990.
2. **Timing between hedges fails, and holding both works.** In different eras Treasuries and gold
   each failed as hedges (Treasuries in 2022, gold in 1980-82). Every rule that concentrated into
   one of them (the H1 switch, the H2a fallback, Study 1's stagflation bet on Treasuries) was
   hurt exactly when that hedge failed.
3. **Higher-return rules are not better hedges.** Trend-following (H2a) delivered the highest
   returns, mostly from the 1970s gold boom. It also had the largest 2022 loss of any rule
   (-28.3% from January to October, against -14.4% for Static 1/3).
4. **Risk scaling is the only idea with a consistent, if insignificant, edge.** Volatility-managed
   equity (H3) slightly improved drawdowns in every variant.

## Caveats

- **Post-hoc design.** The hypotheses were chosen after Study 1's results were seen.
  Pre-registration and Holm correction limit, but do not remove, the risk of data snooping.
  1973-89 is the cleanest evidence.
- **Gold data.** Gold is a monthly average throughout. The all-averages variant gives the same
  ordering.
- **No cash, by design.** Allowing T-bills would change H2 materially. That would be a new
  hypothesis and has not been tested.
- **Drawdown p-values are indicative only,** because block resampling shortens long drawdowns.
