# Deviations log

Every change that alters (or could alter) results, every departure from the README plan, and every
data substitution is listed here: what, why, and the effect on results. Entries are never
deleted. If a later entry supersedes an earlier one, the later entry says so.

Status (updated 2026-10-04, second session): network access to FRED and the Bundesbank was
granted, all data downloaded, and the main and robustness runs completed. Result-altering
entries: **D7** (October 2025 macro gap interpolated, at the PI's choice). D2 is a data
substitution (World Bank average gold kept because the Bundesbank has no USD gold series).
Nothing else changed the methodology in README.md.

---

## D1. FRED unreachable, so the real-data study has not run (RESOLVED, see D6)

- **What:** every request to `fred.stlouisfed.org` fails with `ProxyError ... 403 Forbidden`.
  The four FRED inputs (DGS10, CPIAUCNS, GACDFSA066MSFRBPHI, UNRATE) could not be downloaded.
  `python run_study.py` stops at the first FRED download.
- **Why:** the cloud environment's egress policy does not allow the host. This is not a FRED outage.
- **What I did not do:** I did not substitute FRED mirrors from other sites (for example GitHub
  copies of H.15 yields or BLS CPI). That would breach ground rule 3 and change the data sources
  in the study design. There is also no free mirror of the Philly Fed series that I could verify.
- **Effect on results:** none exist yet. Phases 2 (Treasury and macro checks), 5, 6 and 7 are
  blocked. Ken French and World Bank gold downloaded and validated (see `results/data_validation.md`).
- **To resolve:** allow `fred.stlouisfed.org`, or put the four FRED CSVs in `data/raw/`
  (`fred_DGS10.csv`, `fred_CPIAUCNS.csv`, `fred_GACDFSA066MSFRBPHI.csv`, `fred_UNRATE.csv`;
  the files from fredgraph.csv?id=...). Cached files are used automatically. Then run
  `./run_all.sh`.

## D2. Month-end gold (Phase 3) not obtained: World Bank monthly averages remain in use

- **Update after network access was granted (supersedes the "could not be run" part below):**
  the API is reachable, but **BBEX3 contains no gold price in USD**. Queried:
  - `https://api.statistiken.bundesbank.de/rest/data/BBEX3/.XAU.USD.EA..?detail=nodata`
    (also with the `D.` and `M.` prefixes, and `..USD.EA..`): HTTP 404, which the API uses for
    "no series matches the request".
  - `https://api.statistiken.bundesbank.de/rest/data/BBEX3/.XAU....?detail=nodata` (any
    XAU series): three series only, all the Frankfurt Stock Exchange fixing in DM per kg, which
    ends in 1998: `A.XAU.DEM.EA.AC.C03`, `D.XAU.DEM.EA.AC.C01`, and
    `M.XAU.DEM.EA.AC.C02` (a monthly average).
  - The dataflow list (`/rest/metadata/dataflow/BBK`, 94 dataflows) has no other gold price
    flow. `BBFI3` is the international investment position in fine troy ounces, which is a
    quantity, not a price.
  None of these is a usable USD month-end series for 1972-2026, so per the instructions the
  study continues with the World Bank series. No override was written.
- **Original entry:** `api.statistiken.bundesbank.de` was blocked by the same egress policy (403).
  `fetch_gold_bundesbank.py` was written to discover the BBEX3 series. It queries
  `BBEX3/.XAU.USD.EA..?detail=nodata`, prefers a daily London USD price, takes the last
  observation of each month, and rejects monthly averages. It could not be run, so **no series
  key or URL has been verified**, and none is recorded here. `data/gold_override.csv` does not exist.
- **Effect on results:** the main run will use the World Bank monthly-AVERAGE gold series
  (README caveat 1). On 1972-2026 data, this series has 17.2% annualised volatility and a
  first-order autocorrelation of 0.27, which is the expected smoothing artefact. Gold's volatility
  and correlations will be understated. `results_gold_avg` would be identical to `results_main`,
  so `run_all.sh` skips it.
- **To resolve:** allow the host and run `python fetch_gold_bundesbank.py`. It writes
  `data/gold_override.csv` and `data/gold_override_source.json` (series key, title, URL,
  retrieval date). That key and URL must then be copied into a new entry here.

## D3. Phase 4 timing tests: no look-ahead bug found, no fix made

- **What:** added `tests/` (27 tests, run on the offline synthetic panel). They show:
  - The label at decision month t is unchanged when CPI or unemployment are altered from month t
    onward, or Philly Fed from t+1 onward (with 1- and 2-month confirmation). It does change when
    CPI or unemployment at t-1, or Philly at t, are altered.
  - Weights for month t are bit-identical when all returns from month t onward are shocked. They
    are unchanged when the label of decision month t changes, and they do change when the label
    of t-1 changes.
  - Future macro data (from month T onward) changes only Oracle Tilt's weights for T. Scrambling
    the oracle column changes no strategy except Oracle Tilt. A static check confirms the oracle is
    referenced only in its definition, the Oracle Tilt strategy, the agreement diagnostic and the
    detection-lag calculation.
  - Constant yields give a bond return of exactly y/12 per month (and y·dt daily), including
    end-to-end through `build_panels`.
- **Effect on results:** none (no code changes needed).

## D4. Code additions that do not change default results

- `run_study.py` new flags: `--sample-start`, `--cost-mult`, `--gold-avg` (ignore the gold
  override), `--bootstrap N` (default 5000; 0 skips). New outputs per run: `headline.csv` (regime
  value, detection cost, run settings), `rf.csv`, `significance.csv`.
- `data.load_raw(..., use_gold_override=True)` adds a keyword that defaults to the old behaviour.
- New modules and scripts: `significance.py` (stationary block bootstrap), `validate_data.py`,
  `fetch_gold_bundesbank.py`, `summarize_runs.py`, `run_all.sh`.
- **Effect on results:** none. Verified by rerunning the synthetic smoke test with default flags:
  `oos_returns.csv` is byte-identical to the run before the changes.
- **Note on `--sample-start`:** it trims the RETURN panel (estimation window and descriptive
  tables). The regime signals still use the full macro history, because their expanding z-scores
  only ever use past data. This matches how the 1972 default treats pre-1972 macro data.

## D5. Bootstrap specification (Phase 6, fixed before seeing any real results)

- Stationary bootstrap (Politis-Romano), geometric blocks with a mean of 12 months, 5,000
  resamples, seed 20260101. The two strategies and the T-bill rate are resampled with the same
  indices (paired).
- Two-sided p-value from the centred bootstrap distribution: P*(|d* - d̂| >= |d̂|). The 95% CI is
  the percentile interval of d*.
- The Sharpe definition matches `analysis.perf_stats`: mean excess return / std of total return × √12.
- Max drawdown is path dependent and block resampling shortens long drawdowns. Drawdown p-values
  are therefore indicative only and will be reported that way.

## D6. Downloader: custom User-Agent removed (no effect on results)

- **What:** `data._fetch` sent `User-Agent: Mozilla/5.0 (regime-study)`. Once the domain was
  allowed, FRED still closed every connection that carried this header ("Remote end closed
  connection without response"). Requests with the default `python-requests` User-Agent succeed
  (tested 4 out of 4 each way). The header was removed, and the same change was made in
  `fetch_gold_bundesbank.py`.
- **Effect on results:** none, because it only changes how files are downloaded.

## D7. October 2025 CPI and unemployment gap interpolated (changes results from 2025-11 on)

- **What:** FRED has no value for 2025-10 in CPIAUCNS or UNRATE (the rows are blank). These
  observations were never published because of the US federal government shutdown. All other
  months are complete.
- **Problem with the code as written (pandas 3.0.6):** the missing month propagates through
  `pct_change(12)` and the 3- and 12-month rolling means. That left the real-time regime label
  EMPTY for decision months 2025-11 to 2026-07 (9 months, covering returns from 2025-12 to
  2026-08), and the regime strategies silently fell back to unconditional estimates. Under
  pandas 2.x, `pct_change` would have forward-filled instead, so the behaviour depended on the
  pandas version.
- **Decision (made by the PI when asked, 2026-10-04):** interpolate October.
  - CPI is interpolated log-linearly (324.461, between Sep 324.800 and Nov 324.122) and UNRATE
    linearly (4.45, between 4.4 and 4.5).
  - Only interior gaps are filled (`data.fill_internal_gaps`); the ragged edge at the end of the
    sample is left alone.
  - Look-ahead guard (`regimes.unpublished_interp_months`): the interpolated October value uses
    November's figure. November's figure is published in December, so it is first usable at
    decision month 2025-12. Decision month **2025-11** would therefore see unpublished data, and
    its real-time label is left empty (scores NaN). For that one month the regime strategies use
    unconditional estimates; with `--confirm 2` the previous regime is held. The oracle label is
    allowed to use the interpolated values.
- **Effect on results:**
  - Real-time scores and labels up to decision month 2025-10 are bit-identical with and without
    interpolation, verified on the real data.
  - Labels from 2025-12 on now exist: Stagflation for 2025-12 and 2026-01, Goldilocks for
    2026-02 and 2026-03, then Reflation from 2026-04.
  - This only affects the last 9 out-of-sample months. Checked against `results_gap_asis`:
    the monthly returns of every real-time strategy are identical through 2025-12 and first
    differ in 2026-01. Oracle Tilt differs from 2025-10, as designed, because the oracle uses
    the interpolated October values.
  - Main-run regime value: +0.45 pp a year with interpolation, +0.52 pp without.
  - The un-interpolated version is reported as the robustness run `results_gap_asis`
    (`--no-interp`); see `results/robustness_summary.md` for both.
- **Tests:** `tests/test_gap_interpolation.py` checks the log-linear fill, the
  blocked-decision-month rule, and that labels after the gap ignore later-published data.

## D8. Supplementary analyses beyond the specified outputs (no effect on specified results)

- `results_main/significance_supplementary_static13.csv`: the same block bootstrap applied to
  Regime Tilt vs Static 1/3, for the main run and the 2000-start run. Added because the research
  question asks about static diversification, and Static 1/3 had the shallowest drawdown. It is
  reported as supplementary, not as a pre-specified test.
- `findings_tables.py` writes `results/findings_tables.md`, `results/regime_hedging_full.csv`
  and `results/hypothesis_scorecard.csv`. These contain:
  - down-market-month returns by regime;
  - approximate iid Sharpe standard errors (Lo 2002);
  - a README hypothesis scorecard. The "supported" rule (top 5 or bottom 5 of 14) was set
    when the table was written, after the results had been seen. It is a summary device only.
- `results_gap_asis`: robustness run without the D7 interpolation (`--no-interp`).

## D9. World Gold Council workbook supplied by the PI: checked and NOT used (no effect on results)

- **File:** `Gold_price_averages_in_a_range_of_currencies_since_1978.xlsx`, uploaded 2026-10-04.
  It was not copied into the repository (see the licence point below). Its sheets are Disclaimer,
  Yearly_Avg, Quarterly_Avg and Monthly_Avg. The USD column of Monthly_Avg has 585 rows, from
  1978-01 to 2026-09.
- **Why not used:**
  1. **It is monthly AVERAGES, not month-end prices.** There is no daily or end-of-period sheet,
     so it does not fix the smoothing problem in D2. From 1999 onward it matches the World Bank
     series to within about 0.5% (both are averages of the LBMA PM price). On 1990-2026 returns
     the two series have a correlation of 0.88, annualised volatility of 12.7% vs 12.5%, and
     first-order autocorrelation of 0.17 vs 0.18.
  2. **The monthly sheet is misdated for 1978-01 to 1998-11.** The value at WGC month m equals the
     World Bank value at month m+11. For example, WGC 1979-02 is 675.31 and the World Bank's
     1980-01 is 675; WGC 1998-11 is 310.72 and the World Bank's 1999-10 is 311. The months
     1999-01 to 1999-10 therefore appear twice.
     - The file contradicts itself: its own Yearly_Avg gives 1979 = 304.68 and 1980 = 614.50
       (the World Bank gives 306.75 and 607.83), but the mean of its 1979 monthly values is 600.91.
     - Using it would have shifted gold returns by 11 months for the whole 1978-89 training window
       and most of the 1990s.
  3. **Licence.** The workbook's disclaimer says LBMA Gold Price information "may be used by you
     internally to review the analysis provided by the World Gold Council, but may not be used for
     any other purpose" and "may not be disclosed by you to anyone else", and it prohibits
     redistribution. This conflicts with ground rule 3 (no LBMA price data that needs a licence)
     and with publishing results based on it.
- **Effect on results:** none. Gold remains the World Bank monthly-average series.

## Pending checks (from the first session; resolution noted)

1. RESOLVED: the gap exists, see D7. Original note: **Possible missing October 2025 CPI and unemployment observations.** The October 2025 federal
   shutdown may have left gaps in CPIAUCNS and UNRATE. Under pandas 3.x (installed: 3.0.6),
   `pct_change` and the rolling means do not fill gaps. One missing month would make the inflation
   or growth score NaN for up to about 12 months, so the regime label becomes empty (and with
   1-month confirmation the strategy falls back to unconditional estimates). Under pandas 2.x,
   `pct_change` forward-fills by default, so **results would depend on the pandas version**.
   `validate_data.py` lists every missing month. If a gap exists, I will propose a real-time-safe
   treatment and ask before applying it, because it touches the signal definition.
2. **Unpinned dependencies.** `requirements.txt` has lower bounds only. This run used numpy 2.4.6,
   pandas 3.0.6, scipy 1.17.1, scikit-learn 1.9.1, matplotlib 3.11.2 (Python 3.11.15).
3. **Sharpe definition.** `perf_stats` divides mean excess return by the std of total (not excess)
   returns. The difference is small but non-standard. DECIDED (PI, 2026-10-04): keep as coded and
   state the definition in the paper. Not changed.

## Data vintage

- Ken French files: built from the 202608 CRSP database, downloaded 2026-10-04; returns run to 2026-08.
- World Bank gold (datahub mirror `datasets/gold-prices`, `data/monthly.csv`), downloaded
  2026-10-04; runs to 2026-09. 1960 onward is the World Bank Pink Sheet (monthly averages).
- FRED DGS10, CPIAUCNS, GACDFSA066MSFRBPHI and UNRATE (fredgraph.csv), downloaded 2026-10-04.
  DGS10 runs to 2026-10-01, CPI to 2026-08, Philly Fed and UNRATE to 2026-09.
- Raw files are committed in `data/raw/`, so the exact vintage can be reproduced.
