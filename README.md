# Regime-aware allocation across Treasuries, gold and equity sectors (1972–2026)

Research pipeline for the study question: *can a simple, real-time macro regime signal, used to
allocate between US Treasuries, gold and equity sectors (no cash), deliver better drawdown
protection than static diversification, now that bonds no longer reliably hedge stocks?*

Everything uses free public data and runs with one command.

## Quick start

```bash
pip install -r requirements.txt
python run_study.py              # downloads data to data/raw/, writes results/
```

Options: `--refresh` (re-download), `--industries 17`, `--oos-start 2000-01`,
`--confirm 2` (regime must persist 2 months before switching), `--sample-start 1982-01`,
`--cost-mult 2` (scale all transaction costs), `--gold-avg` (ignore `data/gold_override.csv`),
`--bootstrap 5000` (block-bootstrap resamples for `significance.csv`; 0 skips), `--out results_x`.
`./run_all.sh` runs data validation, the main run and every robustness run, then
`summarize_runs.py`. `python -m pytest tests` runs the no-look-ahead tests (offline).
Changes affecting results are logged in `DEVIATIONS.md`.
`python run_study.py --synthetic` runs an offline smoke test on fake data (results meaningless).

## Data (all free)

| Item | Source | Notes |
|---|---|---|
| 12 (or 17) industry portfolios, value-weighted | Kenneth French Data Library | Consistent SIC definitions since 1926 (no GICS reclassification breaks) |
| US market return, 1-month T-bill | Kenneth French Data Library | Monthly and daily |
| 10-year Treasury total return | Built from FRED `DGS10` (daily) | Swinkels (2019) method: buy a par bond, reprice next period |
| Gold | World Bank Pink Sheet via datahub mirror | **Monthly averages** (see caveats). Put an end-of-month series in `data/gold_override.csv` (`date,price`) and it is used automatically |
| Inflation signal | FRED `CPIAUCNS` | Not seasonally adjusted, so never revised: a true real-time series |
| Growth signal | FRED `GACDFSA066MSFRBPHI` (Philly Fed manufacturing, from 1968) and `UNRATE` | Minor seasonal revisions only |

Ken French industries vs. GICS sectors (approximate): NoDur ≈ consumer staples, Durbl ≈ autos and
durables, Manuf ≈ industrials, Enrgy ≈ energy, Chems ≈ materials, BusEq ≈ information technology,
Telcm ≈ communication services, Utils ≈ utilities, Shops ≈ retail / consumer discretionary,
Hlth ≈ health care, Money ≈ financials, Other ≈ remainder (incl. construction, transport, services).

## Method (fixed before looking at results)

**Regimes.** At the end of each month t, using only data published by then:
- Inflation score = 3-month avg of CPI YoY minus its 12-month avg (CPI lagged 1 month for publication).
- Growth score = average of (a) Philly Fed index 3m avg minus 12m avg and (b) minus the change in
  unemployment (3m avg minus 12m avg, lagged 1 month), each scaled by an expanding standard deviation.
- Four regimes from the signs: Goldilocks (G+ I−), Reflation (G+ I+), Stagflation (G− I+),
  Disinflationary slowdown (G− I−).
- Also recorded: 63-day stock-bond correlation from daily data (shock-type diagnostic).
- Oracle label = the regime of the month being traded, computed without publication lags (upper bound).

**Universe.** 12 industry portfolios + 10y Treasury + gold. Long-only, fully invested, no cash,
max 35% per asset, monthly rebalancing, transaction costs (equities 10 bp, Treasuries 5 bp, gold 15 bp).

**Walk-forward.** Initial training 1972–1989 (includes 1970s stagflation and Volcker); out-of-sample
1990-01 onward with an expanding window re-estimated every month.

**Strategies.**

| Strategy | Role |
|---|---|
| 60/40 (market / 10y) | Industry benchmark |
| Static 1/3 (market / 10y / gold) | Naive three-asset diversification |
| Uncond. ERC | Equal risk contribution, full-history covariance (control, no regime info) |
| Uncond. Tilt | ERC tilted by full-history risk-adjusted returns (control) |
| Regime ERC | ERC with regime-conditional covariance, shrunk toward unconditional |
| Regime Tilt | Regime ERC tilted by regime-conditional risk-adjusted returns (main strategy) |
| Oracle Tilt | Regime Tilt with perfect regime knowledge (upper bound) |

Two headline decompositions:
- **Value of the regime map** = Regime Tilt − Uncond. Tilt (same machinery, only regime info differs).
- **Cost of detection lag** = Oracle Tilt − Regime Tilt.

**Hypotheses to test.**

| Regime | Expected winners | Expected losers |
|---|---|---|
| Goldilocks | BusEq, Shops, Durbl | Gold, Enrgy |
| Reflation | Enrgy, Chems, Money | Treasuries |
| Stagflation | Enrgy, gold, NoDur | Treasuries, BusEq |
| Disinflationary slowdown | Treasuries, NoDur, Hlth, Utils | Durbl, Enrgy, Money |

## Outputs (`results/`)

- `summary.md`: all key tables in one place
- `regimes.csv`, `regimes.png`: regime history with CPI, growth score, stock-bond correlation
- `regime_asset_stats.csv`, `regime_sharpe_heatmap.png`: return, vol, Sharpe, correlation with market
  and with Treasuries, downside correlation, per asset per regime
- `regime_stability*.csv`: does the regime map hold in 1972–89 and 1990–today?
- `episodes_assets.csv`, `episodes_strategies.csv`: 1973–74, Volcker, 1987, 1990, 1998, 2000–02, GFC,
  Covid, 2022, April 2025
- `oos_summary.csv`, `oos_performance.png`, `robustness_sharpe.csv`: CAGR, vol, Sharpe, max drawdown,
  Calmar, CVaR, turnover, sub-period Sharpe
- `weights_*.csv`, `weights_regime_tilt.png`: allocations over time

## Known caveats (state these in the paper)

1. **Gold averages.** World Bank prices are monthly averages, which smooth returns, lower volatility
   and blur correlations. Use an end-of-month series via `gold_override.csv` for the final results.
2. **Start-date effects.** Gold rose from roughly $45 to about $850 between 1972 and 1980; Treasuries suffered
   in the 1970s and then had a 40-year bull market. Judge assets on hedging behaviour (conditional
   correlations, drawdown contribution), and report sub-periods.
3. **Few stagflation episodes.** Conclusions for that quadrant rest on the 1970s, 1990 and 2021–22.
4. **Minor revisions.** Philly Fed and unemployment have small seasonal revisions; ALFRED vintages
   can be swapped in as a robustness check (free API key).
5. **Industry ≠ GICS.** Ken French industries are SIC-based; mapping above is approximate. A
   1999–2026 robustness check with SPDR sector ETFs (free prices from Stooq/Yahoo) shows investability.
6. **US only.** International robustness can use Swinkels' international bond return data.

## Files

`config.py` settings · `data.py` downloads and parsing · `regimes.py` signals ·
`portfolio.py` allocation and walk-forward backtest · `analysis.py` tables, charts, report ·
`run_study.py` entry point · `synthetic.py` offline test data · `significance.py` block bootstrap ·
`validate_data.py` input checks · `fetch_gold_bundesbank.py` month-end gold · `summarize_runs.py`
robustness table · `tests/` timing tests
