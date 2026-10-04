# Study 3 results

Specification: `PREREGISTRATION_STUDY3.md` (committed before any code or international return was examined). After costs. Gold = World Bank monthly average. H4 may hold cash (T-bills); H5 and the control may not.

## Verdicts: primary family (Developed ex US, Holm over 6 tests)

- **H4a Trend + cash (Faber)**: not supported
- **H4b Trend redistribute, cash fallback**: not supported
- **H5 Vol-managed equity**: not supported

Supported = Sharpe difference vs Static 1/3 survives Holm at 5% with a positive sign AND the max drawdown is no worse.

| test | diff | 95% CI | p_value | holm_adj_p | holm_reject_5pct |
|---|---|---|---|---|---|
| H4a Sharpe | +0.13 | [-0.09, +0.35] | 0.26 | 1.00 | False |
| H4a MaxDD | +9.7pp | [+1.4, +20.1]pp | 0.04 | 0.22 | False |
| H4b Sharpe | +0.09 | [-0.19, +0.38] | 0.53 | 1.00 | False |
| H4b MaxDD | -6.3pp | [-13.2, +11.1]pp | 0.46 | 1.00 | False |
| H5 Sharpe | -0.09 | [-0.25, +0.08] | 0.29 | 1.00 | False |
| H5 MaxDD | -0.4pp | [-10.3, +3.7]pp | 0.71 | 1.00 | False |

## Performance: Developed ex US, 1991-07 to 2026-08

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) | Months | Turnover/m | Avg cash |
|---|---|---|---|---|---|---|---|---|---|---|
| Static 1/3 (control) | 6.8% | 7.5% | 0.59 | -20.1% | 0.34 | -8.3% | -3.9% | 422.00 | 1.1% | 0.0% |
| H4a Trend + cash | 6.5% | 5.4% | 0.72 | -10.4% | 0.62 | -4.9% | -2.7% | 422.00 | 11.4% | 40.2% |
| H4b Trend, cash fallback | 8.3% | 8.6% | 0.68 | -26.4% | 0.32 | -8.5% | -4.7% | 422.00 | 16.2% | 5.0% |
| H5 Vol-managed equity | 6.5% | 8.3% | 0.50 | -20.5% | 0.32 | -7.1% | -4.6% | 422.00 | 12.5% | 0.0% |

## Performance: Europe, 1991-07 to 2026-08

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) | Months | Turnover/m | Avg cash |
|---|---|---|---|---|---|---|---|---|---|---|
| Static 1/3 (control) | 7.4% | 7.6% | 0.65 | -21.5% | 0.34 | -8.6% | -4.0% | 422.00 | 1.1% | 0.0% |
| H4a Trend + cash | 6.7% | 5.5% | 0.76 | -9.7% | 0.69 | -4.9% | -2.6% | 422.00 | 11.0% | 39.0% |
| H4b Trend, cash fallback | 8.9% | 8.6% | 0.74 | -25.8% | 0.35 | -6.7% | -4.5% | 422.00 | 15.1% | 4.7% |
| H5 Vol-managed equity | 7.7% | 8.2% | 0.64 | -20.6% | 0.37 | -7.0% | -4.3% | 422.00 | 12.2% | 0.0% |

## Performance: Japan, 1991-07 to 2026-08

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) | Months | Turnover/m | Avg cash |
|---|---|---|---|---|---|---|---|---|---|---|
| Static 1/3 (control) | 5.8% | 8.1% | 0.43 | -21.3% | 0.27 | -6.4% | -4.4% | 422.00 | 1.2% | 0.0% |
| H4a Trend + cash | 6.6% | 5.8% | 0.69 | -9.3% | 0.70 | -5.8% | -3.1% | 422.00 | 11.2% | 42.3% |
| H4b Trend, cash fallback | 9.0% | 9.5% | 0.69 | -17.1% | 0.53 | -8.6% | -5.4% | 422.00 | 16.1% | 6.6% |
| H5 Vol-managed equity | 4.6% | 9.7% | 0.25 | -29.8% | 0.15 | -10.6% | -5.5% | 422.00 | 13.9% | 0.0% |

## Performance: Asia Pacific ex Japan, 1991-07 to 2026-08

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) | Months | Turnover/m | Avg cash |
|---|---|---|---|---|---|---|---|---|---|---|
| Static 1/3 (control) | 7.6% | 8.6% | 0.61 | -22.6% | 0.34 | -9.9% | -4.8% | 422.00 | 1.2% | 0.0% |
| H4a Trend + cash | 6.8% | 6.1% | 0.70 | -11.1% | 0.61 | -6.3% | -3.3% | 422.00 | 11.4% | 39.4% |
| H4b Trend, cash fallback | 8.5% | 9.4% | 0.65 | -26.2% | 0.32 | -9.7% | -5.3% | 422.00 | 15.7% | 5.5% |
| H5 Vol-managed equity | 7.6% | 9.6% | 0.55 | -21.6% | 0.35 | -8.6% | -5.7% | 422.00 | 12.9% | 0.0% |

## Performance: US (seen, exploratory), 1973-01 to 2026-08

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) | Months | Turnover/m | Avg cash |
|---|---|---|---|---|---|---|---|---|---|---|
| Static 1/3 (control) | 9.2% | 8.2% | 0.59 | -20.2% | 0.45 | -9.0% | -4.2% | 644.00 | 1.2% | 0.0% |
| H4a Trend + cash | 9.9% | 6.7% | 0.80 | -10.6% | 0.93 | -9.1% | -3.1% | 644.00 | 9.0% | 39.3% |
| H4b Trend, cash fallback | 12.6% | 12.0% | 0.69 | -24.5% | 0.51 | -14.2% | -6.2% | 644.00 | 13.3% | 6.4% |
| H5 Vol-managed equity | 9.6% | 9.0% | 0.59 | -17.1% | 0.56 | -9.9% | -4.8% | 644.00 | 11.0% | 0.0% |

## Secondary family: other regions, Sharpe difference vs Static 1/3 (Holm over 9)

| region | test | diff | 95% CI | p_value | holm_adj_p | holm_reject_5pct |
|---|---|---|---|---|---|---|
| Europe | H4a Sharpe | +0.10 | [-0.14, +0.35] | 0.41 | 1.00 | False |
| Europe | H4b Sharpe | +0.09 | [-0.19, +0.38] | 0.53 | 1.00 | False |
| Europe | H5 Sharpe | -0.01 | [-0.18, +0.15] | 0.87 | 1.00 | False |
| Japan | H4a Sharpe | +0.26 | [-0.02, +0.55] | 0.07 | 0.56 | False |
| Japan | H4b Sharpe | +0.26 | [-0.05, +0.58] | 0.11 | 0.75 | False |
| Japan | H5 Sharpe | -0.18 | [-0.33, -0.05] | 0.01 | 0.13 | False |
| Asia Pacific ex Japan | H4a Sharpe | +0.09 | [-0.13, +0.30] | 0.39 | 1.00 | False |
| Asia Pacific ex Japan | H4b Sharpe | +0.05 | [-0.21, +0.29] | 0.72 | 1.00 | False |
| Asia Pacific ex Japan | H5 Sharpe | -0.06 | [-0.24, +0.12] | 0.53 | 1.00 | False |

## US exploratory (data already seen in Study 2; no confirmatory claim)

| test | diff | 95% CI | p_value |
|---|---|---|---|
| 1973-latest: H4a Sharpe | +0.21 | [+0.03, +0.40] | 0.03 |
| 1973-latest: H4a MaxDD | +9.6pp | [+1.6, +17.8]pp | 0.02 |
| 1973-latest: H4b Sharpe | +0.11 | [-0.10, +0.31] | 0.32 |
| 1973-latest: H4b MaxDD | -4.3pp | [-15.2, +5.4]pp | 0.33 |
| 1973-latest: H5 Sharpe | +0.00 | [-0.14, +0.14] | 0.96 |
| 1973-latest: H5 MaxDD | +3.1pp | [-3.1, +7.0]pp | 0.24 |
| 1973-1989: H4a Sharpe | +0.37 | [+0.07, +0.71] | 0.02 |
| 1973-1989: H4a MaxDD | +9.6pp | [+1.2, +17.9]pp | 0.03 |
| 1973-1989: H4b Sharpe | +0.36 | [+0.03, +0.68] | 0.03 |
| 1973-1989: H4b MaxDD | -1.0pp | [-14.4, +7.4]pp | 0.82 |
| 1973-1989: H5 Sharpe | -0.03 | [-0.27, +0.20] | 0.81 |
| 1973-1989: H5 MaxDD | +3.1pp | [-3.9, +5.5]pp | 0.33 |
| 1990-latest: H4a Sharpe | +0.13 | [-0.09, +0.33] | 0.23 |
| 1990-latest: H4a MaxDD | +8.3pp | [+0.8, +14.8]pp | 0.02 |
| 1990-latest: H4b Sharpe | -0.02 | [-0.30, +0.24] | 0.90 |
| 1990-latest: H4b MaxDD | -8.7pp | [-14.2, +6.2]pp | 0.24 |
| 1990-latest: H5 Sharpe | +0.03 | [-0.14, +0.21] | 0.72 |
| 1990-latest: H5 MaxDD | +1.0pp | [-3.1, +6.2]pp | 0.45 |

## Robustness variants (all reported)

| variant | universe | strategy | Sharpe | control Sharpe | MaxDD | control MaxDD |
|---|---|---|---|---|---|---|
| Primary | Developed ex US | H4a Trend + cash | 0.72 | 0.59 | -10.4% | -20.1% |
| Primary | Developed ex US | H4b Trend, cash fallback | 0.68 | 0.59 | -26.4% | -20.1% |
| Primary | Developed ex US | H5 Vol-managed equity | 0.50 | 0.59 | -20.5% | -20.1% |
| Primary | Europe | H4a Trend + cash | 0.76 | 0.65 | -9.7% | -21.5% |
| Primary | Europe | H4b Trend, cash fallback | 0.74 | 0.65 | -25.8% | -21.5% |
| Primary | Europe | H5 Vol-managed equity | 0.64 | 0.65 | -20.6% | -21.5% |
| Primary | Japan | H4a Trend + cash | 0.69 | 0.43 | -9.3% | -21.3% |
| Primary | Japan | H4b Trend, cash fallback | 0.69 | 0.43 | -17.1% | -21.3% |
| Primary | Japan | H5 Vol-managed equity | 0.25 | 0.43 | -29.8% | -21.3% |
| Primary | Asia Pacific ex Japan | H4a Trend + cash | 0.70 | 0.61 | -11.1% | -22.6% |
| Primary | Asia Pacific ex Japan | H4b Trend, cash fallback | 0.65 | 0.61 | -26.2% | -22.6% |
| Primary | Asia Pacific ex Japan | H5 Vol-managed equity | 0.55 | 0.61 | -21.6% | -22.6% |
| Primary | US (seen, exploratory) | H4a Trend + cash | 0.80 | 0.59 | -10.6% | -20.2% |
| Primary | US (seen, exploratory) | H4b Trend, cash fallback | 0.69 | 0.59 | -24.5% | -20.2% |
| Primary | US (seen, exploratory) | H5 Vol-managed equity | 0.59 | 0.59 | -17.1% | -20.2% |
| R1 trend 12-1 | Developed ex US | H4a Trend + cash | 0.63 | 0.59 | -8.5% | -20.1% |
| R1 trend 12-1 | Developed ex US | H4b Trend, cash fallback | 0.64 | 0.59 | -15.0% | -20.1% |
| R1 trend 12-1 | Developed ex US | H5 Vol-managed equity | 0.50 | 0.59 | -20.5% | -20.1% |
| R1 trend 12-1 | Europe | H4a Trend + cash | 0.72 | 0.65 | -8.0% | -21.5% |
| R1 trend 12-1 | Europe | H4b Trend, cash fallback | 0.76 | 0.65 | -15.6% | -21.5% |
| R1 trend 12-1 | Europe | H5 Vol-managed equity | 0.64 | 0.65 | -20.6% | -21.5% |
| R1 trend 12-1 | Japan | H4a Trend + cash | 0.54 | 0.43 | -9.3% | -21.3% |
| R1 trend 12-1 | Japan | H4b Trend, cash fallback | 0.53 | 0.43 | -22.0% | -21.3% |
| R1 trend 12-1 | Japan | H5 Vol-managed equity | 0.25 | 0.43 | -29.8% | -21.3% |
| R1 trend 12-1 | Asia Pacific ex Japan | H4a Trend + cash | 0.61 | 0.61 | -8.8% | -22.6% |
| R1 trend 12-1 | Asia Pacific ex Japan | H4b Trend, cash fallback | 0.59 | 0.61 | -22.1% | -22.6% |
| R1 trend 12-1 | Asia Pacific ex Japan | H5 Vol-managed equity | 0.55 | 0.61 | -21.6% | -22.6% |
| R1 trend 12-1 | US (seen, exploratory) | H4a Trend + cash | 0.71 | 0.59 | -10.5% | -20.2% |
| R1 trend 12-1 | US (seen, exploratory) | H4b Trend, cash fallback | 0.63 | 0.59 | -21.5% | -20.2% |
| R1 trend 12-1 | US (seen, exploratory) | H5 Vol-managed equity | 0.59 | 0.59 | -17.1% | -20.2% |
| R2 H5 uncapped | Developed ex US | H4a Trend + cash | 0.72 | 0.59 | -10.4% | -20.1% |
| R2 H5 uncapped | Developed ex US | H4b Trend, cash fallback | 0.68 | 0.59 | -26.4% | -20.1% |
| R2 H5 uncapped | Developed ex US | H5 Vol-managed equity | 0.44 | 0.59 | -20.8% | -20.1% |
| R2 H5 uncapped | Europe | H4a Trend + cash | 0.76 | 0.65 | -9.7% | -21.5% |
| R2 H5 uncapped | Europe | H4b Trend, cash fallback | 0.74 | 0.65 | -25.8% | -21.5% |
| R2 H5 uncapped | Europe | H5 Vol-managed equity | 0.57 | 0.65 | -20.6% | -21.5% |
| R2 H5 uncapped | Japan | H4a Trend + cash | 0.69 | 0.43 | -9.3% | -21.3% |
| R2 H5 uncapped | Japan | H4b Trend, cash fallback | 0.69 | 0.43 | -17.1% | -21.3% |
| R2 H5 uncapped | Japan | H5 Vol-managed equity | 0.16 | 0.43 | -39.0% | -21.3% |
| R2 H5 uncapped | Asia Pacific ex Japan | H4a Trend + cash | 0.70 | 0.61 | -11.1% | -22.6% |
| R2 H5 uncapped | Asia Pacific ex Japan | H4b Trend, cash fallback | 0.65 | 0.61 | -26.2% | -22.6% |
| R2 H5 uncapped | Asia Pacific ex Japan | H5 Vol-managed equity | 0.48 | 0.61 | -25.5% | -22.6% |
| R2 H5 uncapped | US (seen, exploratory) | H4a Trend + cash | 0.80 | 0.59 | -10.6% | -20.2% |
| R2 H5 uncapped | US (seen, exploratory) | H4b Trend, cash fallback | 0.69 | 0.59 | -24.5% | -20.2% |
| R2 H5 uncapped | US (seen, exploratory) | H5 Vol-managed equity | 0.53 | 0.59 | -15.7% | -20.2% |
| R3 costs x2 | Developed ex US | H4a Trend + cash | 0.69 | 0.59 | -11.0% | -20.1% |
| R3 costs x2 | Developed ex US | H4b Trend, cash fallback | 0.64 | 0.59 | -27.4% | -20.1% |
| R3 costs x2 | Developed ex US | H5 Vol-managed equity | 0.46 | 0.59 | -20.7% | -20.1% |
| R3 costs x2 | Europe | H4a Trend + cash | 0.73 | 0.65 | -10.2% | -21.6% |
| R3 costs x2 | Europe | H4b Trend, cash fallback | 0.70 | 0.65 | -26.6% | -21.6% |
| R3 costs x2 | Europe | H5 Vol-managed equity | 0.60 | 0.65 | -20.9% | -21.6% |
| R3 costs x2 | Japan | H4a Trend + cash | 0.66 | 0.43 | -9.5% | -21.3% |
| R3 costs x2 | Japan | H4b Trend, cash fallback | 0.66 | 0.43 | -17.3% | -21.3% |
| R3 costs x2 | Japan | H5 Vol-managed equity | 0.22 | 0.43 | -30.8% | -21.3% |
| R3 costs x2 | Asia Pacific ex Japan | H4a Trend + cash | 0.68 | 0.60 | -11.8% | -22.6% |
| R3 costs x2 | Asia Pacific ex Japan | H4b Trend, cash fallback | 0.62 | 0.60 | -27.6% | -22.6% |
| R3 costs x2 | Asia Pacific ex Japan | H5 Vol-managed equity | 0.52 | 0.60 | -22.0% | -22.6% |
| R3 costs x2 | US (seen, exploratory) | H4a Trend + cash | 0.78 | 0.58 | -10.7% | -20.3% |
| R3 costs x2 | US (seen, exploratory) | H4b Trend, cash fallback | 0.67 | 0.58 | -25.4% | -20.3% |
| R3 costs x2 | US (seen, exploratory) | H5 Vol-managed equity | 0.56 | 0.58 | -17.4% | -20.3% |

## Stress episodes: Developed ex US

|  | Static 1/3 (control) | H4a Trend + cash | H4b Trend, cash fallback | H5 Vol-managed equity |
|---|---|---|---|---|
| 1998 LTCM | -2.0% | 3.9% | 9.3% | -1.5% |
| 2000-02 dot-com bust | -2.5% | 14.5% | 27.2% | -9.4% |
| 2007-09 GFC | -11.4% | 3.7% | 5.5% | -5.2% |
| 2020 Covid crash | -4.2% | 0.4% | 0.9% | -7.0% |
| 2022 inflation shock | -16.2% | -5.7% | -16.9% | -16.8% |
| 2025 tariff shock | 9.7% | 7.0% | 13.9% | 7.8% |

## Stress episodes: Europe

|  | Static 1/3 (control) | H4a Trend + cash | H4b Trend, cash fallback | H5 Vol-managed equity |
|---|---|---|---|---|
| 1998 LTCM | -2.0% | -1.2% | -2.5% | -1.1% |
| 2000-02 dot-com bust | -2.2% | 14.6% | 27.3% | -2.3% |
| 2007-09 GFC | -13.3% | 3.6% | 4.3% | -4.2% |
| 2020 Covid crash | -4.7% | 0.3% | 0.9% | -7.0% |
| 2022 inflation shock | -17.1% | -6.4% | -18.8% | -17.3% |
| 2025 tariff shock | 10.2% | 9.0% | 13.0% | 8.9% |

## Stress episodes: Japan

|  | Static 1/3 (control) | H4a Trend + cash | H4b Trend, cash fallback | H5 Vol-managed equity |
|---|---|---|---|---|
| 1998 LTCM | -1.8% | 4.0% | 9.4% | -0.8% |
| 2000-02 dot-com bust | -4.7% | 14.6% | 27.3% | -15.6% |
| 2007-09 GFC | -3.7% | 9.1% | 15.2% | -3.4% |
| 2020 Covid crash | -1.7% | -0.0% | 0.5% | -7.1% |
| 2022 inflation shock | -16.1% | -1.5% | -6.0% | -18.4% |
| 2025 tariff shock | 9.5% | 6.7% | 18.6% | 7.2% |

## Stress episodes: Asia Pacific ex Japan

|  | Static 1/3 (control) | H4a Trend + cash | H4b Trend, cash fallback | H5 Vol-managed equity |
|---|---|---|---|---|
| 1998 LTCM | 0.8% | 4.0% | 9.4% | 1.2% |
| 2000-02 dot-com bust | 6.0% | 12.4% | 21.7% | -7.6% |
| 2007-09 GFC | -13.7% | 2.8% | 5.1% | -0.8% |
| 2020 Covid crash | -5.2% | 1.1% | 1.6% | -7.9% |
| 2022 inflation shock | -14.8% | -4.8% | -13.0% | -16.9% |
| 2025 tariff shock | 8.1% | 6.8% | 9.7% | 4.7% |

## Stress episodes: US (seen, exploratory)

|  | Static 1/3 (control) | H4a Trend + cash | H4b Trend, cash fallback | H5 Vol-managed equity |
|---|---|---|---|---|
| 1973-74 oil shock / stagflation | 12.3% | 44.4% | 113.5% | 1.3% |
| 1980-82 Volcker tightening | 4.0% | 42.4% | 30.1% | 1.9% |
| 1987 crash | -9.1% | -7.2% | -11.3% | -9.8% |
| 1990 Gulf war recession | -2.5% | 1.1% | -1.9% | -7.0% |
| 1998 LTCM | -1.1% | -2.3% | -1.9% | -3.2% |
| 2000-02 dot-com bust | -4.3% | 9.4% | 17.4% | -2.5% |
| 2007-09 GFC | -8.1% | 5.0% | 6.8% | 3.2% |
| 2020 Covid crash | -3.8% | -3.8% | -3.8% | -5.1% |
| 2022 inflation shock | -14.4% | -6.3% | -18.4% | -14.7% |
| 2025 tariff shock | 4.5% | 3.4% | 4.5% | 1.4% |

Chart: study3_performance.png