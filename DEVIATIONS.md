# Deviations log

Every change that alters (or could alter) results, every departure from the README plan, and every
data substitution is listed here: what, why, and the effect on results. Entries are never
deleted. If a later entry supersedes an earlier one, the later entry says so.

Status as of 2026-10-04: **the real-data study has not been run yet.** FRED and the Bundesbank
API are blocked by this environment's network policy (see D1 and D2), so no main or robustness
results exist. Nothing below changed the methodology in README.md.

---

## D1. FRED unreachable, so the real-data study has not run (blocking, unresolved)

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

- **What:** `api.statistiken.bundesbank.de` is blocked by the same egress policy (403).
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

## Pending checks (run as soon as FRED is reachable; may create new entries)

1. **Possible missing October 2025 CPI and unemployment observations.** The October 2025 federal
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
   returns. The difference is small but non-standard. I have not changed it, because changing it
   would alter reported numbers. It is flagged here for your decision.

## Data vintage

- Ken French files: built from the 202608 CRSP database, downloaded 2026-10-04; returns run to 2026-08.
- World Bank gold (datahub mirror `datasets/gold-prices`, `data/monthly.csv`), downloaded
  2026-10-04; runs to 2026-09. 1960 onward is the World Bank Pink Sheet (monthly averages).
- Raw files are committed in `data/raw/`, so the exact vintage can be reproduced.
