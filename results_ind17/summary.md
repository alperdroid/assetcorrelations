# Regime-aware bonds / gold / equity-sector allocation: results

Data run: free public data (Ken French, FRED, World Bank/WGC gold); regime confirmation = 1 month(s). Return sample 1972-01 to 2026-08; out-of-sample from 1990-01.
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
| 60/40 | 8.9% | 9.4% | 0.67 | -28.8% | 0.31 | -10.7% | -5.7% | 440 | 0.9% |
| Static 1/3 | 8.0% | 6.9% | 0.77 | -15.8% | 0.51 | -7.0% | -3.5% | 440 | 1.1% |
| Uncond. ERC | 9.4% | 9.8% | 0.69 | -31.4% | 0.30 | -13.1% | -6.1% | 440 | 1.5% |
| Uncond. Tilt | 9.4% | 10.3% | 0.67 | -32.5% | 0.29 | -13.2% | -6.4% | 440 | 0.6% |
| Regime ERC | 9.6% | 10.0% | 0.70 | -31.2% | 0.31 | -13.2% | -6.2% | 440 | 2.7% |
| Regime Tilt | 9.7% | 10.5% | 0.68 | -34.8% | 0.28 | -13.4% | -6.4% | 440 | 7.2% |
| Oracle Tilt | 10.2% | 10.5% | 0.73 | -34.7% | 0.29 | -12.0% | -6.2% | 440 | 6.2% |

Value of the regime map (Regime Tilt minus Uncond. Tilt), annualized: +0.28%.  
Cost of detection lag (Oracle Tilt minus Regime Tilt), annualized: +0.54%.

## 3. Stress episodes (strategies, cumulative return)
|  | 60/40 | Static 1/3 | Uncond. ERC | Uncond. Tilt | Regime ERC | Regime Tilt | Oracle Tilt |
|---|---|---|---|---|---|---|---|
| 1990 Gulf war recession | -9.7% | -2.5% | -11.3% | -9.9% | -12.0% | -13.1% | -10.9% |
| 1998 LTCM | -3.4% | -1.1% | -7.7% | -9.8% | -8.2% | -11.1% | -11.0% |
| 2000-02 dot-com bust | -20.8% | -4.3% | -8.8% | -14.0% | -9.7% | -15.6% | -15.8% |
| 2007-09 GFC | -28.8% | -8.1% | -30.4% | -32.3% | -30.7% | -34.3% | -32.9% |
| 2020 Covid crash | -9.4% | -3.8% | -12.7% | -14.3% | -11.8% | -9.5% | -9.7% |
| 2022 inflation shock | -18.3% | -14.4% | -12.6% | -10.7% | -11.9% | -11.2% | -8.2% |
| 2025 tariff shock | -3.4% | 4.5% | -1.3% | -2.4% | -1.7% | -4.5% | -4.0% |

## 4. Stress episodes (individual assets, cumulative return)
|  | Food | Mines | Oil | Clths | Durbl | Chems | Cnsum | Cnstr | Steel | FabPr | Machn | Cars | Trans | Utils | Rtail | Finan | Other | UST10 | GOLD | MKT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1973-74 oil shock / stagflation | -51.2% | -4.8% | -29.1% | -59.0% | -58.8% | -22.0% | -47.0% | -48.6% | -2.8% | -41.1% | -49.1% | -52.1% | -48.1% | -41.7% | -58.2% | -54.5% | -44.3% | 1.6% | 137.5% | -46.5% |
| 1980-82 Volcker tightening | 46.9% | -19.6% | -4.6% | 42.3% | 35.2% | -6.9% | 30.7% | -8.7% | -13.3% | 0.6% | 1.4% | 3.6% | 10.6% | 25.2% | 52.3% | 18.4% | 29.8% | 14.6% | -25.5% | 15.1% |
| 1987 crash | -26.5% | -25.2% | -30.4% | -42.3% | -34.1% | -32.1% | -28.0% | -33.9% | -25.9% | -34.0% | -34.5% | -36.1% | -36.0% | -11.4% | -39.2% | -28.6% | -28.4% | 2.3% | 1.5% | -29.9% |
| 1990 Gulf war recession | -5.2% | -15.9% | 1.0% | -36.4% | -23.1% | -17.4% | -6.2% | -24.6% | -21.1% | -24.8% | -25.8% | -27.1% | -21.9% | 1.5% | -26.2% | -30.3% | -17.4% | 1.4% | 8.2% | -16.5% |
| 1998 LTCM | -20.2% | -7.9% | -5.0% | -28.5% | -17.0% | -18.7% | -0.5% | -19.5% | -16.0% | -26.8% | -4.7% | -18.4% | -19.0% | 4.3% | -15.5% | -21.0% | -10.5% | 9.4% | -1.0% | -11.8% |
| 2000-02 dot-com bust | 10.7% | 3.9% | -24.7% | 11.1% | -9.5% | -15.8% | -17.3% | -12.4% | -75.4% | 1.2% | -79.0% | -21.6% | -4.3% | -21.4% | -7.0% | -15.4% | -59.7% | 30.7% | 16.2% | -45.0% |
| 2007-09 GFC | -27.6% | -58.4% | -40.7% | -56.9% | -64.0% | -56.0% | -30.2% | -49.6% | -72.8% | -51.3% | -55.6% | -63.6% | -51.7% | -37.6% | -32.0% | -69.7% | -50.0% | 17.9% | 24.9% | -50.3% |
| 2020 Covid crash | -18.2% | -21.8% | -44.9% | -26.7% | -27.4% | -26.9% | -9.7% | -26.0% | -30.1% | -22.7% | -17.8% | -27.8% | -31.9% | -21.6% | -10.6% | -28.7% | -17.1% | 8.0% | 2.0% | -20.2% |
| 2022 inflation shock | 4.5% | -17.5% | 71.6% | -38.9% | -42.9% | -12.2% | -0.4% | -26.2% | 1.6% | -20.3% | -28.4% | -28.0% | -13.9% | -2.6% | -24.1% | -9.0% | -25.7% | -18.3% | -7.0% | -18.8% |
| 2025 tariff shock | 4.3% | 1.8% | -8.0% | -27.9% | -15.6% | -16.5% | 3.7% | -11.8% | -4.3% | -9.8% | -12.7% | -22.8% | -5.4% | 1.4% | -11.8% | -9.6% | -7.6% | 4.4% | 18.7% | -8.5% |

## 5. Stability of the regime map (1972-1989 vs 1990-latest)
Spearman rank correlation of asset Sharpe ratios within each regime. Values near 1 mean the same assets win in that regime in both eras; values near 0 mean the map is not stable.

| regime | months_pre | months_post | rank_corr_sharpe |
|---|---|---|---|
| Goldilocks (G+ I-) | 67 | 120 | 0.58 |
| Reflation (G+ I+) | 52 | 129 | 0.18 |
| Stagflation (G- I+) | 50 | 88 | 0.00 |
| Disinflationary slowdown (G- I-) | 47 | 102 | -0.05 |

## 6. Sub-period robustness (Sharpe ratio by out-of-sample start)
|  | from 1990-01 | from 2000-01 | from 2010-01 | from 2020-01 |
|---|---|---|---|---|
| 60/40 | 0.67 | 0.57 | 0.90 | 0.56 |
| Static 1/3 | 0.77 | 0.89 | 1.02 | 0.93 |
| Uncond. ERC | 0.69 | 0.71 | 0.89 | 0.72 |
| Uncond. Tilt | 0.67 | 0.66 | 0.89 | 0.69 |
| Regime ERC | 0.70 | 0.73 | 0.90 | 0.75 |
| Regime Tilt | 0.68 | 0.74 | 1.01 | 0.86 |
| Oracle Tilt | 0.73 | 0.79 | 1.06 | 0.94 |

Charts: regimes.png, regime_sharpe_heatmap.png, oos_performance.png, weights_regime_tilt.png.
Full tables: CSV files in this folder.