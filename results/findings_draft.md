# Results (draft)

*Draft results section. All figures come from `results_main/` unless another run is named; the
supporting tables are in `results/findings_tables.md`, `results/robustness_summary.md` and
`results/data_validation.md`. Data deviations are logged in `DEVIATIONS.md`.*

**Data and setup.**
- Monthly returns run from 1972-01 to 2026-08: Ken French 12 value-weighted industries, a
  constant-maturity 10-year Treasury rebuilt from FRED DGS10, and gold.
- **Gold is the World Bank monthly-average price.** No free month-end USD series was available
  from the permitted sources: the Bundesbank's BBEX3 holds only a DM fixing that ends in 1998
  (DEVIATIONS D2).
- The October 2025 CPI and unemployment figures were never published. They were interpolated,
  and the one decision month that would have used unpublished information was left unlabelled
  (D7).
- To test whether mixing averaged gold with month-end equities and Treasuries drives the results,
  the whole study was rerun with every asset built from monthly-average prices
  (`results_all_avg`; DEVIATIONS D10). Section C reports this check. Claims it does not support
  are flagged in the text.
- The sections below keep two kinds of evidence apart:
  - **Section A** is descriptive and in-sample: what each asset did in each regime, 1972-2026.
  - **Section B** is the out-of-sample walk-forward, 1990-01 to 2026-08, 440 months, after
    transaction costs.

---

## A. Descriptive evidence: the regime map, 1972-2026 (in-sample)

Real-time labels are known at the end of month t-1 and paired with returns in month t.

**Regime frequency.** The four regimes are fairly evenly populated:

| Regime | Months | Share |
|---|---|---|
| Goldilocks | 186 | 28% |
| Reflation | 182 | 28% |
| Stagflation | 138 | 21% |
| Disinflationary slowdown | 149 | 23% |

The label switched 136 times in 655 months, an average spell of under five months. The real-time
label matches the oracle (no-publication-lag) label in 72% of months.

### A1. Which assets hedged in each regime?

**Only Treasuries and gold hedged equities, and none of the equity sectors did.** In every regime,
every one of the 12 industries had a correlation of at least 0.47 with the US market. The least
correlated were Utilities (0.47-0.61) and Energy (0.53-0.67). Treasuries (-0.02 to 0.23) and gold
(-0.09 to 0.04) were close to uncorrelated in all four regimes (findings_tables §1).

Average monthly return in months when the US market fell:

| | Goldilocks | Reflation | Stagflation | Disinfl. slowdown |
|---|---|---|---|---|
| Down-market months | 68 | 65 | 58 | 52 |
| US market | -2.82% | -3.61% | -4.45% | -3.24% |
| 10y Treasury | +0.13% | +0.26% | **+0.82%** | -0.09% |
| Gold | +0.15% | **+1.57%** | +1.06% | +0.94% |
| Utilities (best sector) | -1.09% | -1.16% | -1.37% | -1.89% |

- **Gold** had a positive average return in down-market months in all four regimes, most strongly
  when inflation was rising (Reflation and Stagflation). With all assets on monthly-average prices
  the Goldilocks figure turns slightly negative (-0.26%); the inflation-regime result holds
  (+1.91% and +1.21%).
- **Treasuries** cushioned equity losses most in Stagflation in both versions (+0.82%; +0.99%
  averaged). The draft's earlier observation that they failed to hedge in Disinflationary slowdown
  (-0.09% per month) **is not robust**: with averaged prices they returned +0.35% there, so no
  conclusion should be drawn for that regime.
- Among sectors, Utilities lost least in every regime. Energy, Consumer Staples (NoDur) and, in
  Goldilocks, Telecom came next. Sectors reduced losses but never offset them.

### A2. Did the stagflation regime behave as hypothesised?

**Partly, and for reasons that changed between eras.** On the full sample:

- Four of the five stagflation hypotheses hold. Energy ranks 4th of 14 assets by Sharpe ratio,
  gold 2nd and Consumer Staples 5th; Business Equipment is a loser at 13th.
- **Treasuries contradict the hypothesis.** They are the 3rd-best asset in stagflation (Sharpe
  0.44), not a loser.

The split by era explains the contradiction (findings_tables §2):

- **1972-89 (50 stagflation months, essentially 1973-74 and 1979-80):** the textbook pattern.
  Gold ranked 1st (Sharpe 0.81) and Energy 2nd; Treasuries ranked 12th (Sharpe -0.26).
- **1990-2026 (88 months):** Treasuries ranked 2nd (Sharpe 0.94) and gold fell to 9th (0.13).
  - The post-1990 "stagflation" months are mostly short supply-shock spells: rising headline
    inflation plus falling activity, typically just before demand collapsed.
  - The largest block is the 12 months of 2008, when the 10y Treasury's summed monthly return
    was +19.3% while the market's was -42.5%. 2008 and 2020 together account for 30% of
    Treasuries' post-1990 excess return in this regime.
  - The 2022 stagflation months were the exception: Treasuries summed -5.6% across six months.

With 138 stagflation months in total, the approximate standard error of a regime Sharpe ratio
is about 0.3. Differences between assets of less than about 0.6 should therefore not be read as
meaningful.

### A3. Is the regime map stable between 1972-89 and 1990-today?

**No.** The rank correlation of asset Sharpe ratios between the two eras, within each regime, is:

| Regime | Rank correlation |
|---|---|
| Goldilocks | 0.28 |
| Reflation | -0.02 |
| Stagflation | -0.04 |
| Disinflationary slowdown | -0.22 |

None is large enough to suggest a stable ranking. Some examples:

- **Disinflationary slowdown:** Treasuries went from 2nd to 14th (Sharpe 1.02 → -0.35) and
  Utilities from 1st to 13th.
- **Goldilocks:** Durables went from 5th to 13th.

Of the 21 README hypotheses:

- **Full sample:** 8 are supported (an expected winner in the top 5 of 14, or an expected loser
  in the bottom 5).
- **By era:** 12 hold in 1972-89, 6 in 1990-2026, and only 2 in both: gold loses in Goldilocks
  and Business Equipment loses in Stagflation.

The hypothesis table describes the 1970s better than the period the strategy is tested on.

---

## B. Out-of-sample strategy evidence (1990-01 to 2026-08, after costs)

| Strategy | CAGR | Vol | Sharpe | Max DD | Turnover per month |
|---|---|---|---|---|---|
| Regime Tilt (main) | 9.37% | 9.8% | 0.69 | -30.2% | 7.3% |
| Uncond. Tilt (control) | 8.92% | 10.0% | 0.64 | -31.3% | 0.6% |
| Regime ERC | 9.23% | 8.9% | 0.73 | -27.5% | 2.4% |
| Uncond. ERC | 9.09% | 8.8% | 0.73 | -27.7% | 1.4% |
| Oracle Tilt (upper bound) | 9.71% | 9.7% | 0.73 | -30.3% | 5.9% |
| 60/40 | 8.91% | 9.4% | 0.67 | -28.8% | 0.9% |
| Static 1/3 (market / Treasuries / gold) | 8.01% | 6.9% | 0.77 | -15.8% | 1.1% |

The Sharpe ratio is mean excess return divided by the volatility of total returns, as
pre-specified in the code.

### B1. Does the regime strategy beat its no-regime control after costs?

**It is ahead on point estimates, but the difference is not statistically significant in the
main specification.**

**Main specification.**
- Regime Tilt earns +0.45 percentage points a year more than Uncond. Tilt (the "value of the
  regime map"), with a Sharpe ratio 0.05 higher and a maximum drawdown 1.1 points shallower.
- Stationary block bootstrap (mean block 12 months, 5,000 resamples):
  - Sharpe difference: 95% CI [-0.06, +0.16], p = 0.36.
  - Drawdown difference: CI [-4.0%, +4.3%], p = 0.46.
- At the risk-parity level there is no regime effect: Regime ERC and Uncond. ERC both have a
  Sharpe ratio of 0.73.

**Robustness.** The value of the regime map is positive in all seven runs, from +0.27 pp a year
(costs doubled) to +1.38 pp (evaluation from 2000). The Sharpe difference reaches p < 0.05 in
three runs:

| Run | Sharpe difference | p-value |
|---|---|---|
| 2-month confirmation | +0.09 | 0.023 |
| Evaluation from 2000 | +0.14 | 0.025 |
| Sample from 1982, evaluation from 2000 | +0.07 | 0.043 |

It is not significant in the main run, with 17 industries (+0.01, p = 0.80), with costs doubled
(+0.03, p = 0.53) or without the October 2025 interpolation (+0.06, p = 0.29). These runs are
overlapping, correlated variations of one test, so the scattered p < 0.05 results should not be
read as confirmation.

**The sign depends on the decade.** Annualised, Regime Tilt minus Uncond. Tilt was:

| Period | Difference |
|---|---|
| 1990s | -2.11 pp |
| 2000s | +1.17 pp |
| 2010s | +0.81 pp |
| 2020-2026 | +2.57 pp |

The "evaluation from 2000" run looks better only because it drops the 1990s.

**Other caveats.**
- Regime Tilt turns over 7.3% a month against 0.6% for the control. Doubling costs cuts the
  regime value from +0.45 to +0.27 pp a year.
- The 17-industry version has a deeper drawdown than its control (-34.8% vs -32.5%).

**Cost of detection lag.** The oracle, which knows the current regime without publication lags,
adds only +0.35 pp a year. With 2-month confirmation the real-time strategy almost matches it
(+0.05 pp). The limiting factor is the instability of the regime map itself, not late detection.

### B2. Drawdown protection versus static diversification (the research question)

**No regime strategy delivered better drawdown protection than simple static diversification.**

- Static 1/3 had a maximum drawdown of -15.8%, against -30.2% for Regime Tilt and -28.8% for
  60/40. It also had the highest Sharpe ratio (0.77).
- Regime Tilt's worst drawdown matches its 2007-09 GFC loss (-30.2% from 2007-11 to 2009-02).
  Over the same window 60/40 lost 28.8% and Static 1/3 lost 8.1%.
- A supplementary bootstrap, outside the pre-specified test list, compares Regime Tilt with
  Static 1/3:
  - Drawdown difference: -14.4 points, 95% CI [-23.5%, +1.4%], p = 0.064.
  - Sharpe difference: -0.08, p = 0.55.

  So the static portfolio's advantage is large but not significant at 5%
  (`results_main/significance_supplementary_static13.csv`).
- Against 60/40, Regime Tilt's drawdown is 1.4 points deeper (p = 0.60) and its Sharpe ratio
  0.02 higher (p = 0.83).

**Caveats on the static result.** Static 1/3 holds a third in gold, and gold is measured with
monthly averages.
- A concern was that the mixed basis flatters it: averaged gold looks less volatile and less
  correlated next to month-end equities. That is not what drives the result. With every asset on
  monthly-average prices (Section C), Static 1/3 still has a drawdown of -17.2% against -30.3%
  for Regime Tilt (supplementary bootstrap: -13.1 points, CI [-23.0%, +4.3%], p = 0.087).
- Two caveats remain:
  - gold's strong rise over 2000-2026 helps any portfolio holding a third in gold;
  - averaging smooths every asset, so neither version measures true month-end drawdowns.

A month-end gold price would still be the definitive test.

### B3. What happened in 2022 and in the 2025 tariff shock?

**2022 (Jan-Oct): Regime Tilt beat 60/40 but not clearly its control, and its one regime switch
went the wrong way** (findings_tables §3).

| Strategy | Jan-Oct 2022 |
|---|---|
| Regime Tilt | -11.1% |
| Uncond. Tilt | -9.9% |
| Uncond. ERC | -11.1% |
| Static 1/3 | -14.4% |
| 60/40 | -18.3% |
| Oracle Tilt | -7.2% |

- Against its control the ranking is fragile. With all assets on monthly-average prices it
  reverses: Regime Tilt -10.2% vs Uncond. Tilt -11.3%. The two should be described as roughly
  equal in 2022.
- The advantage over 60/40 came from structural, not regime-driven, holdings: about 20%
  Treasuries and about 25% gold, against 40% Treasuries in 60/40.
- The signal read Reflation through the decision at end-May 2022 and switched to Stagflation for
  July. Because post-1990 history showed Treasuries as the best stagflation hedge (A2), the
  strategy doubled its Treasury weight from 17% to 35%.
- Treasuries then fell 3.8% in August, 5.3% in September and 1.9% in October.
- Meanwhile the 63-day stock-bond correlation rose from -0.43 (January) to +0.48 (December).
  This is the failure mode behind the research question: a regime map learned in an era of
  negative stock-bond correlation mis-hedged a positive-correlation inflation shock.

**2025 tariff shock (Feb-Apr 2025): the regime signal did not help.**

| Strategy | Feb-Apr 2025 |
|---|---|
| Regime Tilt | -2.5% |
| Uncond. Tilt | -1.0% |
| 60/40 | -3.4% |
| Static 1/3 | +4.5% |

- The label was Goldilocks, driven by a strong Philly Fed survey. Gold is historically the worst
  Goldilocks asset, so Regime Tilt held only 5% gold (Uncond. Tilt about 9%). Gold rose 6.8%,
  3.0% and 7.9% in February, March and April (World Bank monthly averages).
- The shock was largely intra-month. Daily Fama-French data show the US market falling 19.6%
  from its 19 February peak to its 8 April trough. Yet April's monthly market return was only
  -0.5%, and the 10y Treasury gained 0.8% in April after an intra-month low of -1.9%.
- A month-end macro signal cannot react to such a shock. The label moved to Disinflationary
  slowdown only at the end of April.

---

## C. Robustness check: all assets on monthly-average prices

Gold is only available as monthly averages, while equities and Treasuries are month-end. So the
whole study was rerun with industries (Ken French daily value-weighted portfolios), the market
and the 10y Treasury all rebuilt from monthly-average price levels (`results_all_avg`,
`results/findings_tables_all_avg.md`).

**Averaging produces the same artefacts in every asset.**
- Monthly autocorrelation rises from about 0 to between 0.16 and 0.32 (market: 0.03 → 0.24;
  10y Treasury: 0.12 → 0.32).
- Volatility falls by about 15% (market: 15.7% → 13.2%).
- Gold's autocorrelation of 0.27 is therefore what averaging alone would produce.

**What survives:**

| | Main | All averaged |
|---|---|---|
| Regime Tilt Sharpe / max DD | 0.69 / -30.2% | 0.81 / -30.3% |
| Uncond. Tilt Sharpe / max DD | 0.64 / -31.3% | 0.74 / -30.8% |
| 60/40 Sharpe / max DD | 0.67 / -28.8% | 0.79 / -26.4% |
| Static 1/3 Sharpe / max DD | 0.77 / -15.8% | 0.83 / -17.2% |
| Value of the regime map | +0.45 pp (p = 0.36) | +0.57 pp (p = 0.19) |
| Cost of detection lag | +0.35 pp | +0.62 pp |
| Era stability (rank correlations) | 0.28 / -0.02 / -0.04 / -0.22 | 0.50 / -0.06 / -0.06 / -0.03 |
| Stagflation: Treasuries rank 1972-89 → 1990+ | 12th → 2nd | 12th → 1st |
| Stagflation: gold rank 1972-89 → 1990+ | 1st → 9th | 1st → 9th |

- **Higher Sharpe ratios are an artefact.** All Sharpe ratios rise by about 0.1 under averaging.
  That is the volatility understatement, not better performance.
- **Robust:** the main conclusions do not depend on mixing price bases:
  - a small, insignificant value from the regime map;
  - no drawdown advantage over static diversification;
  - an era split in which stagflation hedges changed;
  - an unstable regime map in three of four regimes.
- **Not robust (flagged above):**
  - Treasuries failing to hedge in Disinflationary slowdown;
  - gold hedging in Goldilocks;
  - Regime Tilt losing more than its control in 2022.

## D. Limitations

1. **Few stagflation episodes.**
   - 138 stagflation months in total, 50 of them before 1990 from essentially two episodes
     (1973-74 and 1979-80).
   - After 1990, stagflation consists mostly of short supply-shock spells, and 2008 alone
     contributes 12 months.
   - Per-regime Sharpe ratios carry standard errors of about 0.3, and the regime map is unstable
     between eras (A3). Conclusions about stagflation hedges rest on very little independent
     evidence.
2. **Industry definitions differ from GICS.**
   - Ken French industries are SIC-based, and the mapping to GICS sectors is approximate. For
     example, BusEq ≠ Information Technology, Telcm ≠ Communication Services.
   - Results with 17 industries differ in detail: the regime value is +0.28 pp and the drawdown
     is deeper.
   - Investability with sector ETFs (1999 onward) has not been checked.
3. **Gold data quality.**
   - The World Bank price is a monthly average. That smooths returns (autocorrelation 0.27),
     lowers measured volatility and correlations, and makes annual returns run from December
     average to December average.
   - No permitted free source offered a month-end USD series (LBMA feeds need a licence; the
     Bundesbank has none; the World Gold Council workbook is also an average series and is
     licence-restricted, see D9).
   - The all-averages rerun (Section C) shows the mixed price basis does not drive the
     conclusions. True month-end behaviour of gold is still untested.
4. **US only.** The study uses US equities, US Treasuries and US macro signals. Whether the
   pattern holds internationally is untested.
5. **Statistical power and multiple testing.**
   - The main comparisons are not significant.
   - The three p < 0.05 results come from overlapping robustness runs, and the drawdown bootstrap
     is only indicative, because resampling breaks long drawdowns apart (DEVIATIONS D5).
6. **Data handling.**
   - The October 2025 CPI and unemployment values are interpolated (D7). This only affects the
     last 9 months; the un-interpolated run gives a regime value of +0.52 pp against +0.45 pp.
   - Philly Fed and unemployment data are the current vintages, with minor seasonal revisions,
     not real-time ALFRED vintages.
   - Monthly rebalancing cannot capture intra-month shocks such as April 2025.

**Summary for the abstract (cautious).**
- A simple real-time growth × inflation signal tilted a bond / gold / sector portfolio towards
  slightly higher returns than an identical no-regime control: +0.45 pp a year after costs over
  1990-2026, positive in all seven specifications. The gain is not statistically significant in
  the main specification and depends on the decade.
- The strategy did not provide better drawdown protection than static three-asset
  diversification, and the in-sample regime map, including which assets hedge stagflation, was
  not stable between 1972-89 and 1990-2026.
