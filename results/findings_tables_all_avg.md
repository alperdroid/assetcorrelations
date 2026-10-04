# Supporting tables for the findings draft

Inputs: results_all_avg (ALL assets on monthly-average prices), returns 1972-01 to 2026-08. Labels are real-time labels known at the end of month t-1, paired with returns in month t.

## 1. Hedging by regime, 1972-latest (descriptive, in-sample)

Average monthly return in months when the US market fell (down-market months), with the market's own average in the last row. Higher = better hedge.

| asset | Goldilocks (n=57) | Reflation (n=67) | Stagflation (n=56) | Disinflationary slowdown (n=48) |
|---|---|---|---|---|
| NoDur | -1.33 | -2.0 | -1.98 | -1.07 |
| Durbl | -3.2 | -4.08 | -5.83 | -2.28 |
| Manuf | -2.48 | -2.63 | -4.07 | -2.85 |
| Enrgy | -1.34 | -0.98 | -2.22 | -2.55 |
| Chems | -1.97 | -2.03 | -2.62 | -2.15 |
| BusEq | -3.46 | -3.1 | -5.63 | -3.35 |
| Telcm | -0.99 | -1.76 | -3.07 | -2.19 |
| Utils | -0.61 | -0.56 | -1.3 | -1.45 |
| Shops | -2.24 | -3.26 | -3.39 | -1.81 |
| Hlth | -2.2 | -2.14 | -2.17 | -1.36 |
| Money | -2.32 | -2.86 | -4.56 | -3.18 |
| Other | -3.07 | -3.29 | -4.26 | -3.25 |
| UST10 | 0.21 | 0.12 | 0.99 | 0.35 |
| GOLD | -0.26 | 1.91 | 1.21 | 0.76 |
| MKT | -2.35 | -2.77 | -3.9 | -2.47 |

Correlation with the US market by regime:

| asset | Goldilocks | Reflation | Stagflation | Disinflationary slowdown |
|---|---|---|---|---|
| NoDur | 0.76 | 0.77 | 0.83 | 0.75 |
| Durbl | 0.71 | 0.75 | 0.83 | 0.7 |
| Manuf | 0.9 | 0.89 | 0.93 | 0.92 |
| Enrgy | 0.52 | 0.52 | 0.65 | 0.53 |
| Chems | 0.84 | 0.72 | 0.85 | 0.83 |
| BusEq | 0.87 | 0.86 | 0.9 | 0.88 |
| Telcm | 0.64 | 0.74 | 0.77 | 0.75 |
| Utils | 0.53 | 0.5 | 0.65 | 0.55 |
| Shops | 0.82 | 0.85 | 0.9 | 0.86 |
| Hlth | 0.74 | 0.75 | 0.77 | 0.69 |
| Money | 0.89 | 0.83 | 0.9 | 0.89 |
| Other | 0.92 | 0.92 | 0.96 | 0.94 |
| UST10 | 0.03 | -0.0 | -0.0 | 0.12 |
| GOLD | -0.02 | -0.09 | 0.07 | -0.01 |

Annualised Sharpe ratio by regime (approximate iid standard error in brackets):

| asset | Goldilocks (n=187) | Reflation (n=181) | Stagflation (n=138) | Disinflationary slowdown (n=149) |
|---|---|---|---|---|
| NoDur | 1.07 (0.32) | 0.18 (0.26) | 0.42 (0.31) | 0.94 (0.34) |
| Durbl | 0.4 (0.26) | -0.06 (0.26) | -0.39 (0.31) | 1.23 (0.38) |
| Manuf | 0.74 (0.29) | 0.28 (0.26) | 0.13 (0.3) | 0.97 (0.34) |
| Enrgy | 0.49 (0.27) | 0.47 (0.27) | 0.42 (0.31) | 0.48 (0.3) |
| Chems | 0.78 (0.29) | 0.12 (0.26) | 0.27 (0.3) | 0.81 (0.33) |
| BusEq | 0.57 (0.27) | 0.49 (0.27) | -0.2 (0.3) | 1.05 (0.35) |
| Telcm | 1.0 (0.31) | 0.31 (0.26) | -0.09 (0.3) | 0.66 (0.31) |
| Utils | 0.72 (0.28) | 0.48 (0.27) | 0.47 (0.31) | 0.51 (0.3) |
| Shops | 0.87 (0.3) | -0.07 (0.26) | 0.33 (0.3) | 1.13 (0.36) |
| Hlth | 0.87 (0.3) | 0.42 (0.27) | 0.34 (0.3) | 0.58 (0.31) |
| Money | 0.93 (0.3) | 0.25 (0.26) | 0.07 (0.3) | 0.69 (0.32) |
| Other | 0.49 (0.27) | -0.03 (0.26) | 0.18 (0.3) | 0.79 (0.32) |
| UST10 | 0.15 (0.25) | 0.26 (0.26) | 0.46 (0.31) | 0.25 (0.29) |
| GOLD | -0.32 (0.26) | 0.59 (0.28) | 0.47 (0.31) | 0.53 (0.3) |
| MKT | 0.87 (0.3) | 0.33 (0.26) | 0.06 (0.3) | 1.11 (0.36) |

## 2. Hypothesis scorecard (README table)

Rank of each asset's Sharpe ratio among the 14 tradable assets within the regime (1 = best). 'Supported' = expected winner in the top 5, or expected loser in the bottom 5, on the full sample. Months per regime and era are in regime_stability.csv.

| regime | asset | hypothesis | rank full | Sharpe full | rank 1972-89 | Sharpe 1972-89 | rank 1990-latest | Sharpe 1990-latest | full-sample verdict |
|---|---|---|---|---|---|---|---|---|---|
| Goldilocks | BusEq | expected winner | 9/14 | 0.57 | 10/14 | 0.57 | 9/14 | 0.56 | not supported |
| Goldilocks | Shops | expected winner | 5/14 | 0.87 | 7/14 | 0.79 | 2/14 | 0.93 | supported |
| Goldilocks | Durbl | expected winner | 12/14 | 0.40 | 5/14 | 1.03 | 13/14 | 0.18 | not supported |
| Goldilocks | GOLD | expected loser | 14/14 | -0.32 | 14/14 | -0.75 | 14/14 | 0.05 | supported |
| Goldilocks | Enrgy | expected loser | 10/14 | 0.49 | 12/14 | 0.40 | 10/14 | 0.54 | supported |
| Reflation | Enrgy | expected winner | 4/14 | 0.47 | 3/14 | 0.10 | 5/14 | 0.58 | supported |
| Reflation | Chems | expected winner | 11/14 | 0.12 | 7/14 | -0.28 | 10/14 | 0.32 | not supported |
| Reflation | Money | expected winner | 9/14 | 0.25 | 8/14 | -0.34 | 6/14 | 0.51 | not supported |
| Reflation | UST10 | expected loser | 8/14 | 0.26 | 6/14 | -0.04 | 8/14 | 0.41 | not supported |
| Stagflation | Enrgy | expected winner | 4/14 | 0.42 | 2/14 | 0.66 | 7/14 | 0.30 | supported |
| Stagflation | GOLD | expected winner | 2/14 | 0.47 | 1/14 | 0.81 | 9/14 | 0.13 | supported |
| Stagflation | NoDur | expected winner | 5/14 | 0.42 | 6/14 | 0.05 | 3/14 | 0.74 | supported |
| Stagflation | UST10 | expected loser | 3/14 | 0.46 | 12/14 | -0.26 | 1/14 | 1.02 | not supported |
| Stagflation | BusEq | expected loser | 13/14 | -0.20 | 14/14 | -0.37 | 12/14 | -0.12 | supported |
| Disinflationary slowdown | UST10 | expected winner | 14/14 | 0.25 | 3/14 | 0.89 | 14/14 | -0.24 | not supported |
| Disinflationary slowdown | NoDur | expected winner | 5/14 | 0.94 | 2/14 | 1.02 | 5/14 | 0.92 | supported |
| Disinflationary slowdown | Hlth | expected winner | 10/14 | 0.58 | 13/14 | 0.51 | 10/14 | 0.63 | not supported |
| Disinflationary slowdown | Utils | expected winner | 12/14 | 0.51 | 1/14 | 1.21 | 13/14 | 0.19 | not supported |
| Disinflationary slowdown | Durbl | expected loser | 1/14 | 1.23 | 5/14 | 0.88 | 1/14 | 1.38 | not supported |
| Disinflationary slowdown | Enrgy | expected loser | 13/14 | 0.48 | 9/14 | 0.67 | 12/14 | 0.38 | supported |
| Disinflationary slowdown | Money | expected loser | 8/14 | 0.69 | 12/14 | 0.51 | 9/14 | 0.77 | not supported |

Era stability (Spearman rank correlation of Sharpe ratios, 1972-89 vs 1990-latest, includes MKT):

| regime | months_pre | months_post | rank_corr_sharpe |
|---|---|---|---|
| Goldilocks (G+ I-) | 67 | 120 | 0.5 |
| Reflation (G+ I+) | 52 | 129 | -0.06 |
| Stagflation (G- I+) | 50 | 88 | -0.06 |
| Disinflationary slowdown (G- I-) | 47 | 102 | -0.03 |

## 3. 2022 inflation shock, month by month (out-of-sample)

| date | label used (t-1) | sb corr | Regime Tilt | Uncond. Tilt | 60/40 | Static 1/3 | MKT | UST10 | GOLD | RT: UST10/GOLD/equity | UT: UST10/GOLD/equity | RT top sectors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2021-10 | Reflation | -0.35 | -0.2% | +0.0% | -0.5% | -0.4% | +0.4% | -1.8% | +0.1% | 26%/21%/53% | 18%/5%/78% | Utils 9%, Telcm 9%, BusEq 7% |
| 2021-11 | Reflation | -0.16 | +2.0% | +2.5% | +2.8% | +2.4% | +4.5% | +0.3% | +2.5% | 25%/22%/53% | 17%/5%/78% | Utils 10%, Telcm 8%, BusEq 7% |
| 2021-12 | Reflation | -0.29 | -0.6% | -0.5% | -0.5% | -0.7% | -1.4% | +1.0% | -1.8% | 24%/23%/54% | 17%/5%/79% | Utils 10%, Telcm 8%, BusEq 7% |
| 2022-01 | Reflation | -0.43 | -0.4% | -0.2% | -2.9% | -1.4% | -3.1% | -2.6% | +1.5% | 25%/22%/53% | 17%/5%/78% | Utils 10%, BusEq 7%, Telcm 7% |
| 2022-02 | Reflation | -0.27 | -0.6% | -1.5% | -2.3% | -0.7% | -2.8% | -1.4% | +2.2% | 23%/23%/54% | 17%/5%/79% | Utils 11%, Telcm 7%, BusEq 7% |
| 2022-03 | Reflation | -0.22 | +1.5% | +0.3% | -1.2% | +0.8% | -1.0% | -1.6% | +5.0% | 23%/23%/54% | 16%/5%/79% | Utils 10%, Telcm 7%, BusEq 6% |
| 2022-04 | Reflation | -0.15 | -0.2% | +1.2% | -2.3% | -2.0% | -0.4% | -5.2% | -0.6% | 22%/24%/54% | 16%/5%/79% | Utils 11%, Telcm 7%, Enrgy 6% |
| 2022-05 | Reflation | -0.09 | -4.2% | -4.8% | -5.6% | -4.7% | -8.6% | -1.1% | -4.5% | 19%/24%/57% | 15%/5%/80% | Utils 12%, Telcm 7%, Enrgy 7% |
| 2022-06 | Reflation | -0.13 | -2.0% | -2.6% | -2.7% | -1.9% | -3.3% | -1.8% | -0.6% | 20%/23%/57% | 15%/5%/79% | Utils 12%, Enrgy 7%, Telcm 6% |
| 2022-07 | Stagflation | 0.09 | -0.2% | -0.0% | +1.3% | -0.9% | +0.6% | +2.4% | -5.7% | 35%/12%/53% | 15%/5%/80% | Utils 10%, NoDur 7%, Enrgy 7% |
| 2022-08 | Stagflation | 0.08 | +3.7% | +4.7% | +4.2% | +3.0% | +6.9% | +0.2% | +1.8% | 35%/12%/53% | 16%/5%/79% | Utils 10%, NoDur 8%, Hlth 6% |
| 2022-09 | Stagflation | 0.27 | -5.0% | -5.5% | -6.3% | -5.6% | -7.2% | -4.9% | -4.8% | 35%/11%/54% | 15%/5%/80% | Utils 10%, NoDur 8%, Enrgy 6% |
| 2022-10 | Stagflation | 0.26 | -2.8% | -3.0% | -3.2% | -2.5% | -2.9% | -3.5% | -1.0% | 34%/12%/54% | 15%/5%/80% | Utils 11%, NoDur 8%, Enrgy 7% |
| 2022-11 | Stagflation | 0.39 | +4.2% | +5.2% | +3.3% | +3.2% | +4.7% | +1.1% | +3.7% | 32%/12%/56% | 14%/5%/80% | Utils 9%, Enrgy 8%, NoDur 8% |
| 2022-12 | Stagflation | 0.48 | +1.4% | +0.9% | +0.8% | +2.1% | -0.4% | +2.6% | +4.2% | 31%/12%/57% | 14%/5%/80% | Utils 9%, Enrgy 8%, NoDur 8% |

Cumulative over the window: 60/40 -14.5%, Static 1/3 -9.5%, Uncond. ERC -5.8%, Uncond. Tilt -4.0%, Regime ERC -5.8%, Regime Tilt -4.1%, Oracle Tilt -1.1%

## 3. 2025 tariff shock, month by month (out-of-sample)

| date | label used (t-1) | sb corr | Regime Tilt | Uncond. Tilt | 60/40 | Static 1/3 | MKT | UST10 | GOLD | RT: UST10/GOLD/equity | UT: UST10/GOLD/equity | RT top sectors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-12 | Disinflationary slowdown | -0.22 | +1.6% | -0.4% | +1.1% | +0.6% | +1.7% | +0.1% | -0.1% | 9%/8%/83% | 12%/6%/83% | NoDur 13%, Shops 11%, Durbl 9% |
| 2025-01 | Disinflationary slowdown | 0.01 | -1.0% | -0.8% | -0.9% | +0.1% | -0.4% | -1.5% | +2.3% | 9%/9%/82% | 12%/6%/83% | NoDur 13%, Shops 11%, Durbl 9% |
| 2025-02 | Goldilocks | 0.12 | +2.2% | +2.5% | +1.3% | +3.2% | +1.0% | +1.8% | +6.8% | 12%/4%/84% | 11%/6%/83% | NoDur 11%, Telcm 10%, Utils 8% |
| 2025-03 | Goldilocks | 0.25 | -2.3% | -1.7% | -3.2% | -0.6% | -6.4% | +1.7% | +3.0% | 12%/4%/84% | 11%/6%/83% | NoDur 11%, Telcm 11%, Hlth 8% |
| 2025-04 | Goldilocks | -0.15 | -3.3% | -2.9% | -3.1% | +0.9% | -5.5% | +0.4% | +7.9% | 12%/4%/84% | 12%/6%/82% | NoDur 11%, Telcm 11%, Hlth 8% |
| 2025-05 | Disinflationary slowdown | -0.24 | +6.0% | +3.8% | +4.9% | +3.6% | +8.7% | -0.8% | +2.8% | 9%/9%/82% | 12%/6%/82% | NoDur 12%, Shops 11%, Durbl 9% |
| 2025-06 | Disinflationary slowdown | -0.27 | +1.9% | +1.7% | +2.7% | +2.0% | +4.0% | +0.7% | +1.3% | 9%/9%/82% | 11%/6%/82% | NoDur 12%, Shops 11%, Durbl 9% |

Cumulative over the window: 60/40 +2.5%, Static 1/3 +10.2%, Uncond. ERC +4.0%, Uncond. Tilt +2.0%, Regime ERC +3.9%, Regime Tilt +4.8%, Oracle Tilt +2.8%

## 4. Out-of-sample strategy returns by real-time regime (annualised mean, %)

| regime | 60/40 | Static 1/3 | Uncond. ERC | Uncond. Tilt | Regime ERC | Regime Tilt | Oracle Tilt | months |
|---|---|---|---|---|---|---|---|---|
| Disinflationary slowdown | 12.3 | 11.1 | 12.1 | 11.6 | 12.5 | 13.9 | 13.7 | 102 |
| Goldilocks | 8.5 | 6.2 | 8.3 | 9.2 | 8.4 | 9.5 | 9.5 | 120 |
| Reflation | 7.8 | 7.5 | 7.6 | 7.5 | 7.6 | 7.2 | 8.8 | 129 |
| Stagflation | 6.6 | 6.5 | 7.9 | 7.6 | 7.9 | 7.5 | 8.1 | 88 |
| nan | 14.9 | 29.9 | 21.8 | 20.2 | 21.8 | 19.6 | 22.3 | 1 |
