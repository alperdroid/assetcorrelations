# Regime-aware bonds / gold / equity-sector allocation: results

Data run: free public data (Ken French, FRED, World Bank/WGC gold); regime confirmation = 2 month(s). Return sample 1972-01 to 2026-08; out-of-sample from 1990-01.
Gold price source: World Bank monthly average (datahub mirror).

## 1. Regime frequency (real-time labels)
| regime | months | share |
|---|---|---|
| Goldilocks (G+ I-) | 188 | 28.7% |
| Reflation (G+ I+) | 179 | 27.3% |
| Stagflation (G- I+) | 141 | 21.5% |
| Disinflationary slowdown (G- I-) | 148 | 22.6% |

Regime switches: 97. Real-time label equals oracle label in 60% of months.

## 2. Out-of-sample performance
|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) | Months | Avg monthly turnover |
|---|---|---|---|---|---|---|---|---|---|
| 60/40 | 8.9% | 9.4% | 0.67 | -28.8% | 0.31 | -10.7% | -5.7% | 440 | 0.9% |
| Static 1/3 | 8.0% | 6.9% | 0.77 | -15.8% | 0.51 | -7.0% | -3.5% | 440 | 1.1% |
| Uncond. ERC | 9.1% | 8.8% | 0.73 | -27.7% | 0.33 | -11.3% | -5.3% | 440 | 1.4% |
| Uncond. Tilt | 8.9% | 10.0% | 0.64 | -31.3% | 0.28 | -12.2% | -6.3% | 440 | 0.6% |
| Regime ERC | 9.0% | 9.0% | 0.71 | -27.9% | 0.32 | -11.3% | -5.4% | 440 | 2.2% |
| Regime Tilt | 9.7% | 9.7% | 0.72 | -27.1% | 0.36 | -11.3% | -6.1% | 440 | 4.9% |
| Oracle Tilt | 9.7% | 9.7% | 0.73 | -30.3% | 0.32 | -10.9% | -5.7% | 440 | 5.9% |

Value of the regime map (Regime Tilt minus Uncond. Tilt), annualized: +0.75%.  
Cost of detection lag (Oracle Tilt minus Regime Tilt), annualized: +0.05%.

## 3. Stress episodes (strategies, cumulative return)
|  | 60/40 | Static 1/3 | Uncond. ERC | Uncond. Tilt | Regime ERC | Regime Tilt | Oracle Tilt |
|---|---|---|---|---|---|---|---|
| 1990 Gulf war recession | -9.7% | -2.5% | -8.8% | -8.2% | -9.9% | -7.3% | -7.1% |
| 1998 LTCM | -3.4% | -1.1% | -4.9% | -6.3% | -5.6% | -7.8% | -8.0% |
| 2000-02 dot-com bust | -20.8% | -4.3% | -12.3% | -21.2% | -13.9% | -19.9% | -20.4% |
| 2007-09 GFC | -28.8% | -8.1% | -27.3% | -31.3% | -27.8% | -25.9% | -28.8% |
| 2020 Covid crash | -9.4% | -3.8% | -11.4% | -14.2% | -10.8% | -14.0% | -8.8% |
| 2022 inflation shock | -18.3% | -14.4% | -11.1% | -9.9% | -11.5% | -12.2% | -7.2% |
| 2025 tariff shock | -3.4% | 4.5% | 0.8% | -1.0% | 0.9% | -4.1% | -1.5% |

## 4. Stress episodes (individual assets, cumulative return)
|  | NoDur | Durbl | Manuf | Enrgy | Chems | BusEq | Telcm | Utils | Shops | Hlth | Money | Other | UST10 | GOLD | MKT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1973-74 oil shock / stagflation | -51.9% | -54.5% | -43.8% | -30.1% | -36.6% | -51.0% | -23.1% | -41.7% | -57.5% | -46.6% | -54.5% | -54.4% | 1.6% | 137.5% | -46.5% |
| 1980-82 Volcker tightening | 43.7% | 20.6% | 1.2% | -4.1% | 1.9% | 8.5% | 37.2% | 25.2% | 44.4% | 36.8% | 18.3% | 14.9% | 14.6% | -25.5% | 15.1% |
| 1987 crash | -29.3% | -35.3% | -31.2% | -30.3% | -30.0% | -35.0% | -17.3% | -11.4% | -38.3% | -29.6% | -28.6% | -33.5% | 2.3% | 1.5% | -29.9% |
| 1990 Gulf war recession | -9.6% | -28.4% | -22.4% | 1.0% | -15.7% | -26.5% | -10.1% | 1.5% | -25.4% | -7.0% | -30.3% | -24.2% | 1.4% | 8.2% | -16.5% |
| 1998 LTCM | -15.6% | -19.2% | -18.2% | -5.4% | -20.0% | -4.7% | 0.4% | 4.3% | -15.5% | -2.0% | -21.0% | -18.4% | 9.4% | -1.0% | -11.8% |
| 2000-02 dot-com bust | 12.0% | -22.5% | -26.9% | -15.4% | 7.4% | -78.7% | -64.3% | -21.4% | -13.1% | -28.6% | -15.4% | -43.0% | 30.7% | 16.2% | -45.0% |
| 2007-09 GFC | -33.1% | -72.3% | -59.4% | -41.3% | -42.3% | -50.1% | -48.8% | -37.6% | -34.6% | -30.8% | -69.7% | -59.4% | 17.9% | 24.9% | -50.3% |
| 2020 Covid crash | -18.7% | -28.3% | -27.1% | -44.6% | -17.8% | -16.0% | -18.6% | -21.6% | -14.1% | -10.2% | -28.7% | -24.6% | 8.0% | 2.0% | -20.2% |
| 2022 inflation shock | -1.2% | -33.0% | -15.2% | 70.2% | -20.1% | -30.2% | -19.4% | -2.6% | -21.0% | -9.0% | -9.0% | -21.8% | -18.3% | -7.0% | -18.8% |
| 2025 tariff shock | 5.3% | -26.4% | -9.2% | -8.1% | -6.1% | -11.7% | 2.6% | 1.4% | -10.0% | -1.5% | -9.6% | -2.5% | 4.4% | 18.7% | -8.5% |

## 5. Stability of the regime map (1972-1989 vs 1990-latest)
Spearman rank correlation of asset Sharpe ratios within each regime. Values near 1 mean the same assets win in that regime in both eras; values near 0 mean the map is not stable.

| regime | months_pre | months_post | rank_corr_sharpe |
|---|---|---|---|
| Goldilocks (G+ I-) | 66 | 123 | 0.38 |
| Reflation (G+ I+) | 56 | 122 | 0.01 |
| Stagflation (G- I+) | 47 | 94 | 0.29 |
| Disinflationary slowdown (G- I-) | 47 | 101 | -0.22 |

## 6. Sub-period robustness (Sharpe ratio by out-of-sample start)
|  | from 1990-01 | from 2000-01 | from 2010-01 | from 2020-01 |
|---|---|---|---|---|
| 60/40 | 0.67 | 0.57 | 0.90 | 0.56 |
| Static 1/3 | 0.77 | 0.89 | 1.02 | 0.93 |
| Uncond. ERC | 0.73 | 0.73 | 0.94 | 0.70 |
| Uncond. Tilt | 0.64 | 0.58 | 0.86 | 0.59 |
| Regime ERC | 0.71 | 0.72 | 0.93 | 0.72 |
| Regime Tilt | 0.72 | 0.73 | 0.99 | 0.69 |
| Oracle Tilt | 0.73 | 0.76 | 1.06 | 0.88 |

Charts: regimes.png, regime_sharpe_heatmap.png, oos_performance.png, weights_regime_tilt.png.
Full tables: CSV files in this folder.