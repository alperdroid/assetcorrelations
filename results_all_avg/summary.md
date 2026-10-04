# Regime-aware bonds / gold / equity-sector allocation: results

Data run: free public data (Ken French, FRED, World Bank/WGC gold); regime confirmation = 1 month(s); ALL asset returns from monthly-average prices. Return sample 1972-01 to 2026-08; out-of-sample from 1990-01.
Gold price source: World Bank monthly average (datahub mirror).

## 1. Regime frequency (real-time labels)
| regime | months | share |
|---|---|---|
| Goldilocks (G+ I-) | 186 | 28.4% |
| Reflation (G+ I+) | 182 | 27.8% |
| Stagflation (G- I+) | 138 | 21.1% |
| Disinflationary slowdown (G- I-) | 149 | 22.7% |

Regime switches: 136. Real-time label equals oracle label in 72% of months.

## 2. Out-of-sample performance
|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) | Months | Avg monthly turnover |
|---|---|---|---|---|---|---|---|---|---|
| 60/40 | 8.9% | 7.8% | 0.79 | -26.4% | 0.34 | -12.8% | -4.8% | 440 | 0.8% |
| Static 1/3 | 7.9% | 6.2% | 0.83 | -17.2% | 0.46 | -8.1% | -3.4% | 440 | 1.0% |
| Uncond. ERC | 9.0% | 7.7% | 0.81 | -28.1% | 0.32 | -14.4% | -4.9% | 440 | 1.1% |
| Uncond. Tilt | 8.9% | 8.4% | 0.74 | -30.8% | 0.29 | -16.0% | -5.5% | 440 | 0.5% |
| Regime ERC | 9.1% | 7.8% | 0.82 | -27.8% | 0.33 | -14.4% | -5.0% | 440 | 2.2% |
| Regime Tilt | 9.5% | 8.3% | 0.81 | -30.3% | 0.31 | -15.1% | -5.3% | 440 | 6.7% |
| Oracle Tilt | 10.1% | 7.9% | 0.92 | -28.5% | 0.36 | -12.2% | -5.0% | 440 | 6.0% |

Value of the regime map (Regime Tilt minus Uncond. Tilt), annualized: +0.57%.  
Cost of detection lag (Oracle Tilt minus Regime Tilt), annualized: +0.62%.

## 3. Stress episodes (strategies, cumulative return)
|  | 60/40 | Static 1/3 | Uncond. ERC | Uncond. Tilt | Regime ERC | Regime Tilt | Oracle Tilt |
|---|---|---|---|---|---|---|---|
| 1990 Gulf war recession | -9.4% | -2.4% | -9.3% | -9.0% | -9.8% | -10.2% | -7.4% |
| 1998 LTCM | -3.2% | -1.3% | -5.1% | -6.0% | -5.4% | -6.9% | -7.4% |
| 2000-02 dot-com bust | -16.8% | -1.9% | -11.1% | -18.9% | -11.4% | -18.3% | -16.3% |
| 2007-09 GFC | -24.1% | -4.6% | -24.7% | -27.7% | -24.6% | -27.0% | -23.2% |
| 2020 Covid crash | -8.2% | -2.9% | -10.6% | -13.4% | -10.6% | -10.3% | -7.7% |
| 2022 inflation shock | -19.4% | -15.2% | -12.5% | -11.3% | -12.3% | -10.2% | -7.8% |
| 2025 tariff shock | -5.0% | 3.6% | -0.9% | -2.2% | -1.3% | -3.5% | -3.4% |

## 4. Stress episodes (individual assets, cumulative return)
|  | NoDur | Durbl | Manuf | Enrgy | Chems | BusEq | Telcm | Utils | Shops | Hlth | Money | Other | UST10 | GOLD | MKT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1973-74 oil shock / stagflation | -48.2% | -50.7% | -39.1% | -26.1% | -30.6% | -47.5% | -18.7% | -42.1% | -53.9% | -39.8% | -52.4% | -52.0% | 0.6% | 137.5% | -42.7% |
| 1980-82 Volcker tightening | 45.7% | 24.2% | 4.9% | 0.6% | 6.2% | 9.5% | 36.6% | 27.3% | 47.2% | 39.1% | 21.0% | 21.4% | 13.2% | -25.5% | 17.9% |
| 1987 crash | -24.7% | -30.9% | -28.6% | -24.2% | -26.4% | -29.3% | -12.4% | -8.7% | -33.9% | -25.2% | -23.8% | -31.1% | 1.6% | 1.5% | -25.6% |
| 1990 Gulf war recession | -8.7% | -27.7% | -21.5% | 1.0% | -16.2% | -26.2% | -13.5% | -1.0% | -23.5% | -2.1% | -29.0% | -22.6% | 1.3% | 8.2% | -16.0% |
| 1998 LTCM | -12.6% | -16.2% | -16.8% | -7.3% | -18.3% | -0.6% | -1.9% | 0.2% | -10.3% | -0.7% | -17.5% | -17.1% | 6.9% | -1.0% | -9.8% |
| 2000-02 dot-com bust | 12.9% | -19.0% | -19.7% | -11.4% | 10.9% | -74.5% | -61.5% | -16.6% | -9.1% | -25.9% | -8.2% | -37.8% | 29.3% | 16.2% | -39.4% |
| 2007-09 GFC | -27.9% | -69.1% | -54.0% | -34.4% | -37.5% | -44.5% | -47.6% | -28.9% | -32.0% | -22.2% | -66.8% | -54.6% | 20.0% | 24.9% | -45.3% |
| 2020 Covid crash | -17.1% | -21.0% | -26.4% | -44.4% | -16.0% | -16.4% | -16.2% | -16.0% | -12.6% | -13.3% | -26.4% | -22.5% | 8.8% | 2.0% | -19.3% |
| 2022 inflation shock | -3.1% | -33.3% | -19.1% | 60.6% | -20.2% | -30.7% | -23.0% | -3.1% | -20.8% | -10.6% | -13.3% | -23.6% | -18.0% | -7.0% | -20.5% |
| 2025 tariff shock | 5.5% | -31.9% | -11.1% | -9.4% | -5.9% | -16.5% | 3.2% | -0.1% | -9.5% | -3.3% | -8.5% | -4.3% | 3.9% | 18.7% | -10.7% |

## 5. Stability of the regime map (1972-1989 vs 1990-latest)
Spearman rank correlation of asset Sharpe ratios within each regime. Values near 1 mean the same assets win in that regime in both eras; values near 0 mean the map is not stable.

| regime | months_pre | months_post | rank_corr_sharpe |
|---|---|---|---|
| Goldilocks (G+ I-) | 67 | 120 | 0.50 |
| Reflation (G+ I+) | 52 | 129 | -0.06 |
| Stagflation (G- I+) | 50 | 88 | -0.06 |
| Disinflationary slowdown (G- I-) | 47 | 102 | -0.03 |

## 6. Sub-period robustness (Sharpe ratio by out-of-sample start)
|  | from 1990-01 | from 2000-01 | from 2010-01 | from 2020-01 |
|---|---|---|---|---|
| 60/40 | 0.79 | 0.67 | 1.16 | 0.73 |
| Static 1/3 | 0.83 | 0.94 | 1.13 | 1.07 |
| Uncond. ERC | 0.81 | 0.77 | 1.14 | 0.82 |
| Uncond. Tilt | 0.74 | 0.65 | 1.06 | 0.71 |
| Regime ERC | 0.82 | 0.77 | 1.13 | 0.83 |
| Regime Tilt | 0.81 | 0.79 | 1.25 | 0.98 |
| Oracle Tilt | 0.92 | 0.92 | 1.42 | 1.19 |

Charts: regimes.png, regime_sharpe_heatmap.png, oos_performance.png, weights_regime_tilt.png.
Full tables: CSV files in this folder.