# Supporting tables for the findings draft

Inputs: results_main, returns 1972-01 to 2026-08. Labels are real-time labels known at the end of month t-1, paired with returns in month t.

## 1. Hedging by regime, 1972-latest (descriptive, in-sample)

Average monthly return in months when the US market fell (down-market months), with the market's own average in the last row. Higher = better hedge.

| asset | Goldilocks (n=68) | Reflation (n=65) | Stagflation (n=58) | Disinflationary slowdown (n=52) |
|---|---|---|---|---|
| NoDur | -2.0 | -2.51 | -2.21 | -2.06 |
| Durbl | -3.53 | -5.25 | -6.46 | -2.28 |
| Manuf | -3.24 | -3.92 | -4.86 | -3.47 |
| Enrgy | -1.86 | -2.07 | -2.65 | -3.47 |
| Chems | -2.83 | -3.02 | -2.96 | -2.79 |
| BusEq | -3.67 | -4.31 | -6.42 | -3.91 |
| Telcm | -1.67 | -2.46 | -3.84 | -2.95 |
| Utils | -1.09 | -1.16 | -1.37 | -1.89 |
| Shops | -2.8 | -4.1 | -4.05 | -2.75 |
| Hlth | -2.24 | -2.31 | -2.73 | -2.96 |
| Money | -2.93 | -3.57 | -4.82 | -3.66 |
| Other | -3.52 | -4.25 | -4.74 | -3.88 |
| UST10 | 0.13 | 0.26 | 0.82 | -0.09 |
| GOLD | 0.15 | 1.57 | 1.06 | 0.94 |
| MKT | -2.82 | -3.61 | -4.45 | -3.24 |

Correlation with the US market by regime:

| asset | Goldilocks | Reflation | Stagflation | Disinflationary slowdown |
|---|---|---|---|---|
| NoDur | 0.81 | 0.77 | 0.8 | 0.78 |
| Durbl | 0.73 | 0.76 | 0.8 | 0.69 |
| Manuf | 0.92 | 0.88 | 0.93 | 0.91 |
| Enrgy | 0.53 | 0.58 | 0.67 | 0.64 |
| Chems | 0.85 | 0.81 | 0.83 | 0.83 |
| BusEq | 0.88 | 0.86 | 0.88 | 0.83 |
| Telcm | 0.68 | 0.73 | 0.77 | 0.75 |
| Utils | 0.56 | 0.47 | 0.61 | 0.59 |
| Shops | 0.86 | 0.87 | 0.86 | 0.85 |
| Hlth | 0.78 | 0.74 | 0.72 | 0.75 |
| Money | 0.91 | 0.82 | 0.87 | 0.87 |
| Other | 0.93 | 0.92 | 0.96 | 0.93 |
| UST10 | 0.11 | -0.02 | 0.01 | 0.23 |
| GOLD | -0.04 | -0.09 | 0.04 | -0.09 |

Annualised Sharpe ratio by regime (approximate iid standard error in brackets):

| asset | Goldilocks (n=187) | Reflation (n=181) | Stagflation (n=138) | Disinflationary slowdown (n=149) |
|---|---|---|---|---|
| NoDur | 0.76 (0.29) | 0.25 (0.26) | 0.41 (0.31) | 0.78 (0.32) |
| Durbl | 0.37 (0.26) | 0.01 (0.26) | -0.36 (0.3) | 1.11 (0.36) |
| Manuf | 0.56 (0.27) | 0.34 (0.26) | 0.15 (0.3) | 0.78 (0.32) |
| Enrgy | 0.45 (0.27) | 0.4 (0.27) | 0.44 (0.31) | 0.35 (0.29) |
| Chems | 0.52 (0.27) | 0.26 (0.26) | 0.27 (0.3) | 0.6 (0.31) |
| BusEq | 0.45 (0.27) | 0.55 (0.28) | -0.2 (0.3) | 0.93 (0.34) |
| Telcm | 0.74 (0.29) | 0.41 (0.27) | -0.14 (0.3) | 0.49 (0.3) |
| Utils | 0.63 (0.28) | 0.34 (0.26) | 0.54 (0.32) | 0.39 (0.29) |
| Shops | 0.57 (0.27) | 0.14 (0.26) | 0.23 (0.3) | 1.05 (0.35) |
| Hlth | 0.74 (0.29) | 0.52 (0.27) | 0.31 (0.3) | 0.32 (0.29) |
| Money | 0.72 (0.28) | 0.35 (0.27) | 0.04 (0.29) | 0.6 (0.31) |
| Other | 0.38 (0.26) | 0.13 (0.26) | 0.17 (0.3) | 0.63 (0.31) |
| UST10 | 0.1 (0.25) | 0.29 (0.26) | 0.44 (0.31) | 0.19 (0.29) |
| GOLD | -0.32 (0.26) | 0.59 (0.28) | 0.47 (0.31) | 0.53 (0.3) |
| MKT | 0.67 (0.28) | 0.41 (0.27) | 0.03 (0.29) | 0.91 (0.34) |

## 2. Hypothesis scorecard (README table)

Rank of each asset's Sharpe ratio among the 14 tradable assets within the regime (1 = best). 'Supported' = expected winner in the top 5, or expected loser in the bottom 5, on the full sample. Months per regime and era are in regime_stability.csv.

| regime | asset | hypothesis | rank full | Sharpe full | rank 1972-89 | Sharpe 1972-89 | rank 1990-latest | Sharpe 1990-latest | full-sample verdict |
|---|---|---|---|---|---|---|---|---|---|
| Goldilocks | BusEq | expected winner | 10/14 | 0.45 | 11/14 | 0.42 | 9/14 | 0.46 | not supported |
| Goldilocks | Shops | expected winner | 6/14 | 0.57 | 8/14 | 0.61 | 3/14 | 0.54 | not supported |
| Goldilocks | Durbl | expected winner | 12/14 | 0.37 | 5/14 | 0.87 | 13/14 | 0.16 | not supported |
| Goldilocks | GOLD | expected loser | 14/14 | -0.32 | 14/14 | -0.75 | 14/14 | 0.05 | supported |
| Goldilocks | Enrgy | expected loser | 9/14 | 0.45 | 12/14 | 0.33 | 4/14 | 0.53 | not supported |
| Reflation | Enrgy | expected winner | 5/14 | 0.40 | 4/14 | 0.08 | 6/14 | 0.50 | supported |
| Reflation | Chems | expected winner | 10/14 | 0.26 | 6/14 | -0.12 | 8/14 | 0.48 | not supported |
| Reflation | Money | expected winner | 6/14 | 0.35 | 10/14 | -0.18 | 4/14 | 0.58 | not supported |
| Reflation | UST10 | expected loser | 9/14 | 0.29 | 7/14 | -0.15 | 7/14 | 0.50 | not supported |
| Stagflation | Enrgy | expected winner | 4/14 | 0.44 | 2/14 | 0.58 | 7/14 | 0.36 | supported |
| Stagflation | GOLD | expected winner | 2/14 | 0.47 | 1/14 | 0.81 | 9/14 | 0.13 | supported |
| Stagflation | NoDur | expected winner | 5/14 | 0.41 | 8/14 | -0.01 | 3/14 | 0.80 | supported |
| Stagflation | UST10 | expected loser | 3/14 | 0.44 | 12/14 | -0.26 | 2/14 | 0.94 | not supported |
| Stagflation | BusEq | expected loser | 13/14 | -0.20 | 14/14 | -0.29 | 12/14 | -0.17 | supported |
| Disinflationary slowdown | UST10 | expected winner | 14/14 | 0.19 | 2/14 | 1.02 | 14/14 | -0.35 | not supported |
| Disinflationary slowdown | NoDur | expected winner | 5/14 | 0.78 | 3/14 | 0.88 | 6/14 | 0.73 | supported |
| Disinflationary slowdown | Hlth | expected winner | 13/14 | 0.32 | 13/14 | 0.40 | 11/14 | 0.27 | not supported |
| Disinflationary slowdown | Utils | expected winner | 11/14 | 0.39 | 1/14 | 1.07 | 13/14 | 0.03 | not supported |
| Disinflationary slowdown | Durbl | expected loser | 1/14 | 1.11 | 6/14 | 0.71 | 1/14 | 1.26 | not supported |
| Disinflationary slowdown | Enrgy | expected loser | 12/14 | 0.35 | 8/14 | 0.59 | 12/14 | 0.24 | supported |
| Disinflationary slowdown | Money | expected loser | 8/14 | 0.60 | 11/14 | 0.49 | 7/14 | 0.64 | not supported |

Era stability (Spearman rank correlation of Sharpe ratios, 1972-89 vs 1990-latest, includes MKT):

| regime | months_pre | months_post | rank_corr_sharpe |
|---|---|---|---|
| Goldilocks (G+ I-) | 67 | 120 | 0.28 |
| Reflation (G+ I+) | 52 | 129 | -0.02 |
| Stagflation (G- I+) | 50 | 88 | -0.04 |
| Disinflationary slowdown (G- I-) | 47 | 102 | -0.22 |

## 3. 2022 inflation shock, month by month (out-of-sample)

| date | label used (t-1) | sb corr | Regime Tilt | Uncond. Tilt | 60/40 | Static 1/3 | MKT | UST10 | GOLD | RT: UST10/GOLD/equity | UT: UST10/GOLD/equity | RT top sectors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2021-10 | Reflation | -0.35 | +2.3% | +3.9% | +3.9% | +2.2% | +6.6% | -0.1% | +0.1% | 24%/24%/52% | 17%/6%/77% | Telcm 9%, BusEq 8%, Hlth 7% |
| 2021-11 | Reflation | -0.16 | -0.6% | -1.7% | -0.5% | +0.7% | -1.6% | +1.2% | +2.5% | 22%/25%/53% | 16%/6%/78% | BusEq 9%, Telcm 9%, Hlth 8% |
| 2021-12 | Reflation | -0.29 | +1.8% | +4.1% | +1.7% | +0.3% | +3.2% | -0.7% | -1.8% | 23%/26%/51% | 16%/6%/77% | BusEq 9%, Telcm 7%, Hlth 7% |
| 2022-01 | Reflation | -0.43 | -2.4% | -3.0% | -4.6% | -2.3% | -6.2% | -2.3% | +1.5% | 22%/24%/53% | 16%/6%/78% | BusEq 9%, Telcm 8%, Hlth 8% |
| 2022-02 | Reflation | -0.27 | -0.0% | -0.6% | -1.5% | -0.1% | -2.3% | -0.2% | +2.2% | 21%/26%/52% | 16%/6%/78% | BusEq 8%, Telcm 8%, Hlth 7% |
| 2022-03 | Reflation | -0.22 | +2.2% | +2.3% | +0.2% | +1.3% | +3.1% | -4.2% | +5.0% | 21%/27%/52% | 16%/6%/78% | BusEq 8%, Telcm 8%, Hlth 7% |
| 2022-04 | Reflation | -0.15 | -4.7% | -4.7% | -7.5% | -4.9% | -9.4% | -4.7% | -0.6% | 18%/29%/53% | 15%/7%/79% | BusEq 8%, Telcm 7%, Utils 7% |
| 2022-05 | Reflation | -0.09 | -0.0% | +0.9% | +0.0% | -1.4% | -0.3% | +0.6% | -4.5% | 17%/31%/52% | 14%/7%/79% | Utils 7%, BusEq 7%, Hlth 7% |
| 2022-06 | Reflation | -0.13 | -4.6% | -5.9% | -5.4% | -3.3% | -8.3% | -0.9% | -0.6% | 17%/28%/54% | 15%/7%/79% | Utils 8%, Telcm 7%, BusEq 7% |
| 2022-07 | Stagflation | 0.09 | +3.8% | +5.5% | +7.0% | +2.3% | +9.7% | +2.9% | -5.7% | 35%/16%/49% | 15%/7%/78% | Utils 11%, NoDur 7%, Enrgy 6% |
| 2022-08 | Stagflation | 0.08 | -1.9% | -2.2% | -3.7% | -1.9% | -3.6% | -3.8% | +1.8% | 35%/14%/51% | 15%/7%/78% | Utils 11%, NoDur 7%, Enrgy 6% |
| 2022-09 | Stagflation | 0.27 | -7.2% | -8.3% | -7.6% | -6.4% | -9.2% | -5.3% | -4.8% | 35%/15%/50% | 14%/7%/79% | Utils 11%, NoDur 7%, Enrgy 6% |
| 2022-10 | Stagflation | 0.26 | +3.8% | +6.6% | +4.1% | +1.7% | +8.1% | -1.9% | -1.0% | 34%/16%/50% | 14%/7%/79% | Utils 10%, NoDur 7%, Enrgy 6% |
| 2022-11 | Stagflation | 0.39 | +4.5% | +4.8% | +4.5% | +4.1% | +4.9% | +3.8% | +3.7% | 32%/15%/53% | 13%/7%/79% | Utils 11%, Enrgy 7%, NoDur 7% |
| 2022-12 | Stagflation | 0.48 | -1.9% | -3.3% | -4.2% | -1.0% | -6.0% | -1.3% | +4.2% | 32%/15%/53% | 14%/7%/79% | Utils 11%, NoDur 7%, Enrgy 7% |

Cumulative over the window: 60/40 -14.0%, Static 1/3 -8.9%, Uncond. ERC -5.5%, Uncond. Tilt -3.0%, Regime ERC -5.7%, Regime Tilt -5.8%, Oracle Tilt -3.8%

## 3. 2025 tariff shock, month by month (out-of-sample)

| date | label used (t-1) | sb corr | Regime Tilt | Uncond. Tilt | 60/40 | Static 1/3 | MKT | UST10 | GOLD | RT: UST10/GOLD/equity | UT: UST10/GOLD/equity | RT top sectors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-12 | Disinflationary slowdown | -0.22 | -3.0% | -4.8% | -2.8% | -1.9% | -2.8% | -2.8% | -0.1% | 9%/13%/78% | 11%/8%/81% | Shops 12%, NoDur 12%, Durbl 8% |
| 2025-01 | Disinflationary slowdown | 0.01 | +2.7% | +2.8% | +2.1% | +2.0% | +3.2% | +0.4% | +2.3% | 9%/14%/77% | 10%/8%/82% | Shops 12%, NoDur 11%, Durbl 9% |
| 2025-02 | Goldilocks | 0.12 | +1.2% | +1.7% | -0.0% | +2.6% | -2.1% | +3.1% | +6.8% | 11%/5%/84% | 10%/8%/82% | Utils 10%, NoDur 10%, Telcm 10% |
| 2025-03 | Goldilocks | 0.25 | -2.2% | -1.8% | -3.5% | -0.9% | -6.0% | +0.4% | +3.0% | 12%/5%/84% | 11%/9%/81% | Utils 10%, NoDur 10%, Telcm 10% |
| 2025-04 | Goldilocks | -0.15 | -1.4% | -0.8% | +0.0% | +2.7% | -0.5% | +0.8% | +7.9% | 12%/5%/83% | 11%/9%/81% | Utils 11%, NoDur 10%, Telcm 10% |
| 2025-05 | Disinflationary slowdown | -0.24 | +4.8% | +2.9% | +3.2% | +2.6% | +6.4% | -1.6% | +2.8% | 9%/14%/77% | 11%/9%/80% | Shops 12%, NoDur 11%, Durbl 9% |
| 2025-06 | Disinflationary slowdown | -0.27 | +1.8% | +1.9% | +3.8% | +2.8% | +5.2% | +1.7% | +1.3% | 8%/15%/77% | 10%/9%/81% | Shops 12%, NoDur 11%, Durbl 9% |

Cumulative over the window: 60/40 +2.6%, Static 1/3 +10.2%, Uncond. ERC +4.1%, Uncond. Tilt +1.7%, Regime ERC +4.2%, Regime Tilt +3.7%, Oracle Tilt +3.6%

## 4. Out-of-sample strategy returns by real-time regime (annualised mean, %)

| regime | 60/40 | Static 1/3 | Uncond. ERC | Uncond. Tilt | Regime ERC | Regime Tilt | Oracle Tilt | months |
|---|---|---|---|---|---|---|---|---|
| Disinflationary slowdown | 11.3 | 10.4 | 11.5 | 10.9 | 12.2 | 13.9 | 13.4 | 102 |
| Goldilocks | 8.5 | 6.2 | 7.7 | 8.4 | 7.8 | 8.7 | 8.4 | 120 |
| Reflation | 9.4 | 8.5 | 9.1 | 9.0 | 8.9 | 8.0 | 9.7 | 129 |
| Stagflation | 6.6 | 6.6 | 8.3 | 8.0 | 8.4 | 7.6 | 7.5 | 88 |
| nan | -4.7 | 17.8 | 6.7 | -0.4 | 6.6 | -1.0 | 9.9 | 1 |
