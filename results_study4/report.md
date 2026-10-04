# Study 4 results: is trend + cash (H4a) timing, or just holding cash?

Specification: `PREREGISTRATION_STUDY4.md`. Robustness / decomposition on data already seen in Study 3; not confirmatory. After costs.

## Verdict (primary: Developed ex US, H4a vs C1, Holm over 2 tests)

- **H6**: not supported

| statistic | diff | 95% CI | p_value | holm_adj_p | holm_reject_5pct |
|---|---|---|---|---|---|
| MaxDD | +1.7pp | [-3.9, +7.7]pp | 0.61 | 0.61 | False |
| Sharpe | +0.13 | [-0.09, +0.35] | 0.26 | 0.51 | False |

## Developed ex US: C1 cash = 40.2%, C2 cash = 27.6%

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) |
|---|---|---|---|---|---|---|---|
| H4a Trend + cash | 6.5% | 5.4% | 0.72 | -10.4% | 0.62 | -4.9% | -2.7% |
| C1 cash-matched static | 5.2% | 4.5% | 0.59 | -12.0% | 0.43 | -4.9% | -2.3% |
| C2 vol-matched static | 5.7% | 5.4% | 0.59 | -14.6% | 0.39 | -6.0% | -2.8% |
| Static 1/3 | 6.8% | 7.5% | 0.59 | -20.1% | 0.34 | -8.3% | -3.9% |

## Europe: C1 cash = 39.0%, C2 cash = 28.0%

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) |
|---|---|---|---|---|---|---|---|
| H4a Trend + cash | 6.7% | 5.5% | 0.76 | -9.7% | 0.69 | -4.9% | -2.6% |
| C1 cash-matched static | 5.6% | 4.6% | 0.65 | -13.2% | 0.42 | -5.2% | -2.4% |
| C2 vol-matched static | 6.1% | 5.5% | 0.65 | -15.7% | 0.39 | -6.2% | -2.8% |
| Static 1/3 | 7.4% | 7.6% | 0.65 | -21.5% | 0.34 | -8.6% | -4.0% |

## Japan: C1 cash = 42.3%, C2 cash = 28.4%

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) |
|---|---|---|---|---|---|---|---|
| H4a Trend + cash | 6.6% | 5.8% | 0.69 | -9.3% | 0.70 | -5.8% | -3.1% |
| C1 cash-matched static | 4.5% | 4.7% | 0.43 | -10.6% | 0.43 | -3.6% | -2.4% |
| C2 vol-matched static | 5.0% | 5.8% | 0.43 | -13.1% | 0.38 | -4.5% | -3.1% |
| Static 1/3 | 5.8% | 8.1% | 0.43 | -21.3% | 0.27 | -6.4% | -4.4% |

## Asia Pacific ex Japan: C1 cash = 39.4%, C2 cash = 29.7%

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) |
|---|---|---|---|---|---|---|---|
| H4a Trend + cash | 6.8% | 6.1% | 0.70 | -11.1% | 0.61 | -6.3% | -3.3% |
| C1 cash-matched static | 5.7% | 5.2% | 0.61 | -13.8% | 0.41 | -6.0% | -2.8% |
| C2 vol-matched static | 6.2% | 6.1% | 0.61 | -16.0% | 0.38 | -6.9% | -3.3% |
| Static 1/3 | 7.6% | 8.6% | 0.61 | -22.6% | 0.34 | -9.9% | -4.8% |

## US (1973-, seen): C1 cash = 39.3%, C2 cash = 19.2%

|  | CAGR | Vol | Sharpe | MaxDD | Calmar | Worst month | CVaR 5% (monthly) |
|---|---|---|---|---|---|---|---|
| H4a Trend + cash | 9.9% | 6.7% | 0.80 | -10.6% | 0.93 | -9.1% | -3.1% |
| C1 cash-matched static | 7.4% | 5.0% | 0.58 | -9.6% | 0.77 | -5.0% | -2.3% |
| C2 vol-matched static | 8.3% | 6.7% | 0.59 | -13.1% | 0.63 | -7.0% | -3.3% |
| Static 1/3 | 9.2% | 8.2% | 0.59 | -20.2% | 0.45 | -9.0% | -4.2% |

## All comparisons (H4a minus control; not Holm-corrected; MaxDD > 0 = H4a shallower)

| universe | control | statistic | diff | p_value |
|---|---|---|---|---|
| Developed ex US | C1 cash-matched static | MaxDD | +1.7pp | 0.61 |
| Developed ex US | C1 cash-matched static | Sharpe | +0.13 | 0.26 |
| Developed ex US | C2 vol-matched static | MaxDD | +4.2pp | 0.21 |
| Developed ex US | C2 vol-matched static | Sharpe | +0.13 | 0.26 |
| Europe | C1 cash-matched static | MaxDD | +3.6pp | 0.27 |
| Europe | C1 cash-matched static | Sharpe | +0.11 | 0.40 |
| Europe | C2 vol-matched static | MaxDD | +6.0pp | 0.13 |
| Europe | C2 vol-matched static | Sharpe | +0.11 | 0.40 |
| Japan | C1 cash-matched static | MaxDD | +1.2pp | 0.66 |
| Japan | C1 cash-matched static | Sharpe | +0.26 | 0.07 |
| Japan | C2 vol-matched static | MaxDD | +3.8pp | 0.28 |
| Japan | C2 vol-matched static | Sharpe | +0.26 | 0.07 |
| Asia Pacific ex Japan | C1 cash-matched static | MaxDD | +2.7pp | 0.45 |
| Asia Pacific ex Japan | C1 cash-matched static | Sharpe | +0.10 | 0.38 |
| Asia Pacific ex Japan | C2 vol-matched static | MaxDD | +5.0pp | 0.18 |
| Asia Pacific ex Japan | C2 vol-matched static | Sharpe | +0.10 | 0.38 |
| US (1973-, seen) | C1 cash-matched static | MaxDD | -1.0pp | 0.62 |
| US (1973-, seen) | C1 cash-matched static | Sharpe | +0.22 | 0.02 |
| US (1973-, seen) | C2 vol-matched static | MaxDD | +2.4pp | 0.37 |
| US (1973-, seen) | C2 vol-matched static | Sharpe | +0.21 | 0.02 |

## Stress episodes, H4a vs C1 (cumulative return)

|  | Developed ex US: H4a | Developed ex US: C1 | Europe: H4a | Europe: C1 | Japan: H4a | Japan: C1 | Asia Pacific ex Japan: H4a | Asia Pacific ex Japan: C1 | US: H4a | US: C1 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1973-74 oil shock / stagflation |  |  |  |  |  |  |  |  | 44.4% | 13.1% |
| 1980-82 Volcker tightening |  |  |  |  |  |  |  |  | 42.4% | 16.7% |
| 1987 crash |  |  |  |  |  |  |  |  | -7.2% | -5.1% |
| 1990 Gulf war recession |  |  |  |  |  |  |  |  | 1.1% | -0.5% |
| 1998 LTCM | 3.9% | -0.7% | -1.2% | -0.7% | 4.0% | -0.5% | 4.0% | 1.1% | -2.3% | -0.1% |
| 2000-02 dot-com bust | 14.5% | 1.4% | 14.6% | 1.5% | 14.6% | 0.3% | 12.4% | 6.6% | 9.4% | 0.2% |
| 2007-09 GFC | 3.7% | -5.9% | 3.6% | -7.3% | 9.1% | -1.0% | 2.8% | -7.5% | 5.0% | -4.0% |
| 2020 Covid crash | 0.4% | -2.4% | 0.3% | -2.8% | -0.0% | -0.9% | 1.1% | -3.1% | -3.8% | -2.2% |
| 2022 inflation shock | -5.7% | -9.7% | -6.4% | -10.4% | -1.5% | -9.3% | -4.8% | -8.9% | -6.3% | -8.6% |
| 2025 tariff shock | 7.0% | 6.1% | 9.0% | 6.5% | 6.7% | 5.9% | 6.8% | 5.2% | 3.4% | 3.1% |
