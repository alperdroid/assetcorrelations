# Study 2 results: pre-registered rule-based hedging strategies

Specification: `PREREGISTRATION.md` (committed before any code or run). Evaluation: return months 1973-01 to 2026-08, after costs. Gold = World Bank monthly average.

## Verdicts (Holm-corrected, 8 tests)

- **H1 bond-hedge switch**: not supported
- **H2a trend overlay (3 assets)**: not supported
- **H2b trend overlay (sectors)**: not supported
- **H3 volatility-managed equity**: not supported

Rule: supported only if the Sharpe difference vs control survives Holm at 5% with a positive sign AND the max drawdown is no worse than the control.

## Primary tests, 1973-latest

| hypothesis | control | statistic | diff | 95% CI | p_value | holm_adj_p | holm_reject_5pct |
|---|---|---|---|---|---|---|---|
| H1 bond-hedge switch | Static 1/3 | Sharpe | -0.20 | [-0.34, -0.06] | 0.00 | 0.04 | True |
| H1 bond-hedge switch | Static 1/3 | MaxDD | -19.4pp | [-25.6, -1.5]pp | 0.01 | 0.05 | True |
| H2a trend overlay (3 assets) | Static 1/3 | Sharpe | +0.12 | [-0.10, +0.33] | 0.27 | 0.97 | False |
| H2a trend overlay (3 assets) | Static 1/3 | MaxDD | -8.1pp | [-19.1, +3.7]pp | 0.14 | 0.83 | False |
| H2b trend overlay (sectors) | EW 14 assets | Sharpe | +0.10 | [-0.07, +0.28] | 0.27 | 0.97 | False |
| H2b trend overlay (sectors) | EW 14 assets | MaxDD | +13.6pp | [-5.9, +27.8]pp | 0.18 | 0.90 | False |
| H3 volatility-managed equity | Static 1/3 | Sharpe | +0.00 | [-0.14, +0.14] | 0.96 | 0.97 | False |
| H3 volatility-managed equity | Static 1/3 | MaxDD | +3.1pp | [-3.1, +7.0]pp | 0.24 | 0.97 | False |

## Performance, 1973-latest

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) | Months | Turnover/m |
|---|---|---|---|---|---|---|---|---|---|
| 60/40 | 9.5% | 10.3% | 0.52 | -29.0% | 0.33 | -11.3% | -6.0% | 644.00 | 0.9% |
| Static 1/3 | 9.2% | 8.2% | 0.59 | -20.2% | 0.45 | -9.0% | -4.2% | 644.00 | 1.2% |
| EW 14 assets | 11.0% | 13.1% | 0.54 | -42.3% | 0.26 | -18.3% | -8.1% | 644.00 | 1.3% |
| H1 Bond-hedge switch | 8.4% | 11.3% | 0.39 | -39.6% | 0.21 | -15.0% | -6.1% | 644.00 | 3.8% |
| H2a Trend 3-asset | 13.0% | 12.3% | 0.71 | -28.3% | 0.46 | -14.2% | -6.2% | 644.00 | 12.0% |
| H2b Trend sectors | 12.4% | 13.0% | 0.64 | -28.7% | 0.43 | -21.3% | -7.4% | 644.00 | 17.4% |
| H3 Vol-managed equity | 9.6% | 9.0% | 0.59 | -17.1% | 0.56 | -9.9% | -4.8% | 644.00 | 11.0% |

## Performance, 1973-1989 (unseen)

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) | Months |
|---|---|---|---|---|---|---|---|---|
| 60/40 | 10.9% | 11.9% | 0.28 | -29.0% | 0.38 | -11.3% | -6.5% | 204.00 |
| Static 1/3 | 11.7% | 10.6% | 0.37 | -20.2% | 0.58 | -9.0% | -5.1% | 204.00 |
| EW 14 assets | 12.2% | 14.6% | 0.33 | -34.6% | 0.35 | -18.3% | -8.6% | 204.00 |
| H1 Bond-hedge switch | 10.8% | 16.5% | 0.23 | -39.6% | 0.27 | -15.0% | -8.6% | 204.00 |
| H2a Trend 3-asset | 21.3% | 17.3% | 0.76 | -21.2% | 1.00 | -14.2% | -8.0% | 204.00 |
| H2b Trend sectors | 14.9% | 15.5% | 0.47 | -28.7% | 0.52 | -21.3% | -8.6% | 204.00 |
| H3 Vol-managed equity | 11.7% | 11.7% | 0.34 | -17.1% | 0.68 | -9.9% | -6.0% | 204.00 |

## Performance, 1990-latest (seen in Study 1)

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) | Months |
|---|---|---|---|---|---|---|---|---|
| 60/40 | 8.9% | 9.4% | 0.67 | -28.8% | 0.31 | -10.7% | -5.7% | 440.00 |
| Static 1/3 | 8.0% | 6.9% | 0.77 | -15.8% | 0.51 | -7.0% | -3.5% | 440.00 |
| EW 14 assets | 10.5% | 12.3% | 0.65 | -42.3% | 0.25 | -15.5% | -7.8% | 440.00 |
| H1 Bond-hedge switch | 7.4% | 7.8% | 0.60 | -16.5% | 0.45 | -7.8% | -4.0% | 440.00 |
| H2a Trend 3-asset | 9.4% | 8.9% | 0.75 | -28.3% | 0.33 | -9.4% | -5.2% | 440.00 |
| H2b Trend sectors | 11.3% | 11.6% | 0.75 | -21.3% | 0.53 | -12.5% | -6.7% | 440.00 |
| H3 Vol-managed equity | 8.7% | 7.4% | 0.80 | -14.8% | 0.59 | -6.0% | -4.0% | 440.00 |

## Sharpe difference vs control by sub-period (bootstrap p, not Holm-corrected)

| hypothesis | diff 1973-1989 (unseen) | diff 1990-latest (seen in Study 1) | p_value 1973-1989 (unseen) | p_value 1990-latest (seen in Study 1) |
|---|---|---|---|---|
| H1 bond-hedge switch | -0.14 | -0.16 | 0.29 | 0.03 |
| H2a trend overlay (3 assets) | 0.39 | -0.02 | 0.02 | 0.91 |
| H2b trend overlay (sectors) | 0.14 | 0.10 | 0.51 | 0.29 |
| H3 volatility-managed equity | -0.03 | 0.03 | 0.81 | 0.72 |

## Robustness variants (all reported)

| variant | hypothesis | Sharpe | control Sharpe | MaxDD | control MaxDD | CAGR | control CAGR |
|---|---|---|---|---|---|---|---|
| Primary | H1 bond-hedge switch | 0.39 | 0.59 | -39.6% | -20.2% | 8.4% | 9.2% |
| Primary | H2a trend overlay (3 assets) | 0.71 | 0.59 | -28.3% | -20.2% | 13.0% | 9.2% |
| Primary | H2b trend overlay (sectors) | 0.64 | 0.54 | -28.7% | -42.3% | 12.4% | 11.0% |
| Primary | H3 volatility-managed equity | 0.59 | 0.59 | -17.1% | -20.2% | 9.6% | 9.2% |
| H1 252-day window | H1 bond-hedge switch | 0.42 | 0.59 | -39.6% | -20.2% | 8.9% | 9.2% |
| H1 252-day window | H2a trend overlay (3 assets) | 0.71 | 0.59 | -28.3% | -20.2% | 13.0% | 9.2% |
| H1 252-day window | H2b trend overlay (sectors) | 0.64 | 0.54 | -28.7% | -42.3% | 12.4% | 11.0% |
| H1 252-day window | H3 volatility-managed equity | 0.59 | 0.59 | -17.1% | -20.2% | 9.6% | 9.2% |
| Trend 12-1 (skip month) | H1 bond-hedge switch | 0.39 | 0.59 | -39.6% | -20.2% | 8.4% | 9.2% |
| Trend 12-1 (skip month) | H2a trend overlay (3 assets) | 0.67 | 0.59 | -20.8% | -20.2% | 12.7% | 9.2% |
| Trend 12-1 (skip month) | H2b trend overlay (sectors) | 0.58 | 0.54 | -28.3% | -42.3% | 11.9% | 11.0% |
| Trend 12-1 (skip month) | H3 volatility-managed equity | 0.59 | 0.59 | -17.1% | -20.2% | 9.6% | 9.2% |
| Trend 10-month | H1 bond-hedge switch | 0.39 | 0.59 | -39.6% | -20.2% | 8.4% | 9.2% |
| Trend 10-month | H2a trend overlay (3 assets) | 0.76 | 0.59 | -24.8% | -20.2% | 13.7% | 9.2% |
| Trend 10-month | H2b trend overlay (sectors) | 0.59 | 0.54 | -33.1% | -42.3% | 11.7% | 11.0% |
| Trend 10-month | H3 volatility-managed equity | 0.59 | 0.59 | -17.1% | -20.2% | 9.6% | 9.2% |
| H3 uncapped | H1 bond-hedge switch | 0.39 | 0.59 | -39.6% | -20.2% | 8.4% | 9.2% |
| H3 uncapped | H2a trend overlay (3 assets) | 0.71 | 0.59 | -28.3% | -20.2% | 13.0% | 9.2% |
| H3 uncapped | H2b trend overlay (sectors) | 0.64 | 0.54 | -28.7% | -42.3% | 12.4% | 11.0% |
| H3 uncapped | H3 volatility-managed equity | 0.53 | 0.59 | -15.7% | -20.2% | 9.6% | 9.2% |
| All assets on monthly averages | H1 bond-hedge switch | 0.39 | 0.61 | -40.1% | -20.7% | 8.4% | 9.1% |
| All assets on monthly averages | H2a trend overlay (3 assets) | 0.79 | 0.61 | -25.6% | -20.7% | 13.4% | 9.1% |
| All assets on monthly averages | H2b trend overlay (sectors) | 0.76 | 0.60 | -28.2% | -40.8% | 12.9% | 10.8% |
| All assets on monthly averages | H3 volatility-managed equity | 0.80 | 0.61 | -16.7% | -20.7% | 10.7% | 9.1% |
| Costs x2 | H1 bond-hedge switch | 0.38 | 0.58 | -39.7% | -20.3% | 8.3% | 9.1% |
| Costs x2 | H2a trend overlay (3 assets) | 0.69 | 0.58 | -29.0% | -20.3% | 12.7% | 9.1% |
| Costs x2 | H2b trend overlay (sectors) | 0.60 | 0.54 | -28.7% | -42.3% | 11.9% | 11.0% |
| Costs x2 | H3 volatility-managed equity | 0.56 | 0.58 | -17.4% | -20.3% | 9.3% | 9.1% |

## Stress episodes (cumulative return)

|  | 60/40 | Static 1/3 | EW 14 assets | H1 Bond-hedge switch | H2a Trend 3-asset | H2b Trend sectors | H3 Vol-managed equity |
|---|---|---|---|---|---|---|---|
| 1973-74 oil shock / stagflation | -30.3% | 12.3% | -36.3% | 21.9% | 113.5% | 20.9% | 1.3% |
| 1980-82 Volcker tightening | 16.2% | 4.0% | 18.4% | -14.0% | 43.2% | 21.3% | 1.9% |
| 1987 crash | -17.4% | -9.1% | -25.0% | -9.5% | -11.3% | -28.7% | -9.8% |
| 1990 Gulf war recession | -9.7% | -2.5% | -13.9% | -0.4% | -4.1% | -11.1% | -7.0% |
| 1998 LTCM | -3.4% | -1.1% | -9.1% | -1.1% | -1.9% | -9.4% | -3.2% |
| 2000-02 dot-com bust | -20.8% | -4.3% | -23.4% | -4.7% | 17.4% | -12.3% | -2.5% |
| 2007-09 GFC | -28.8% | -8.1% | -42.3% | -8.1% | 6.8% | -7.7% | 3.2% |
| 2020 Covid crash | -9.4% | -3.8% | -19.0% | -3.8% | -3.8% | -15.6% | -5.1% |
| 2022 inflation shock | -18.3% | -14.4% | -10.9% | -14.8% | -28.3% | -10.7% | -14.7% |
| 2025 tariff shock | -3.4% | 4.5% | -3.8% | 6.6% | 4.5% | -3.8% | 1.4% |

Chart: study2_performance.png