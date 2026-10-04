# Regime-aware bonds / gold / equity-sector allocation: results

Data run: free public data (Ken French, FRED, World Bank/WGC gold); regime confirmation = 1 month(s). Return sample 1982-01 to 2026-08; out-of-sample from 2000-01.
Gold price source: World Bank monthly average (datahub mirror).

## 1. Regime frequency (real-time labels)
| regime | months | share |
|---|---|---|
| Goldilocks (G+ I-) | 149 | 27.9% |
| Reflation (G+ I+) | 158 | 29.5% |
| Stagflation (G- I+) | 96 | 17.9% |
| Disinflationary slowdown (G- I-) | 132 | 24.7% |

Regime switches: 120. Real-time label equals oracle label in 70% of months.

## 2. Out-of-sample performance
|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) | Months | Avg monthly turnover |
|---|---|---|---|---|---|---|---|---|---|
| 60/40 | 7.0% | 9.4% | 0.57 | -28.8% | 0.24 | -10.7% | -5.8% | 320 | 1.0% |
| Static 1/3 | 8.2% | 7.0% | 0.89 | -15.8% | 0.52 | -7.0% | -3.6% | 320 | 1.1% |
| Uncond. ERC | 8.4% | 8.6% | 0.76 | -26.5% | 0.32 | -10.9% | -5.2% | 320 | 1.4% |
| Uncond. Tilt | 7.4% | 9.0% | 0.63 | -28.1% | 0.26 | -11.1% | -5.8% | 320 | 0.7% |
| Regime ERC | 8.6% | 8.7% | 0.77 | -27.3% | 0.31 | -10.8% | -5.3% | 320 | 2.2% |
| Regime Tilt | 8.5% | 9.6% | 0.70 | -28.9% | 0.29 | -10.7% | -6.0% | 320 | 4.9% |
| Oracle Tilt | 8.7% | 9.5% | 0.73 | -28.7% | 0.31 | -9.5% | -5.8% | 320 | 4.7% |

Value of the regime map (Regime Tilt minus Uncond. Tilt), annualized: +1.12%.  
Cost of detection lag (Oracle Tilt minus Regime Tilt), annualized: +0.27%.

## 3. Stress episodes (strategies, cumulative return)
|  | 60/40 | Static 1/3 | Uncond. ERC | Uncond. Tilt | Regime ERC | Regime Tilt | Oracle Tilt |
|---|---|---|---|---|---|---|---|
| 2000-02 dot-com bust | -20.8% | -4.3% | -10.8% | -13.5% | -11.2% | -15.1% | -15.3% |
| 2007-09 GFC | -28.8% | -8.1% | -25.5% | -28.1% | -26.2% | -28.9% | -28.7% |
| 2020 Covid crash | -9.4% | -3.8% | -10.8% | -11.3% | -10.6% | -11.3% | -11.2% |
| 2022 inflation shock | -18.3% | -14.4% | -10.9% | -11.8% | -11.1% | -14.1% | -9.0% |
| 2025 tariff shock | -3.4% | 4.5% | 1.5% | -1.1% | 1.1% | -2.5% | -1.3% |

## 4. Stress episodes (individual assets, cumulative return)
|  | NoDur | Durbl | Manuf | Enrgy | Chems | BusEq | Telcm | Utils | Shops | Hlth | Money | Other | UST10 | GOLD | MKT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
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
| Goldilocks (G+ I-) | 29 | 120 | 0.17 |
| Reflation (G+ I+) | 28 | 129 | -0.20 |
| Stagflation (G- I+) | 8 | 88 | 0.30 |
| Disinflationary slowdown (G- I-) | 31 | 102 | -0.20 |

## 6. Sub-period robustness (Sharpe ratio by out-of-sample start)
|  | from 2000-01 | from 2010-01 | from 2020-01 |
|---|---|---|---|
| 60/40 | 0.57 | 0.90 | 0.56 |
| Static 1/3 | 0.89 | 1.02 | 0.93 |
| Uncond. ERC | 0.76 | 0.96 | 0.74 |
| Uncond. Tilt | 0.63 | 0.87 | 0.54 |
| Regime ERC | 0.77 | 0.96 | 0.75 |
| Regime Tilt | 0.70 | 0.97 | 0.69 |
| Oracle Tilt | 0.73 | 1.02 | 0.82 |

Charts: regimes.png, regime_sharpe_heatmap.png, oos_performance.png, weights_regime_tilt.png.
Full tables: CSV files in this folder.