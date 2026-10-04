# Sector deep dive

Descriptive analysis of the 12 Ken French value-weighted industries, 1972-01 to 2026-08, monthly, month-end returns (gold: World Bank monthly average). No strategy is tested here. GICS analogues: NoDur ≈ staples, Durbl ≈ autos/durables, Manuf ≈ industrials, Enrgy ≈ energy, Chems ≈ materials, BusEq ≈ tech, Telcm ≈ communication, Utils ≈ utilities, Shops ≈ retail, Hlth ≈ health care, Money ≈ financials.

## A. Sector risk profile by era

Down capture = average return in months the US market fell, divided by the market's average in those months (1.00 = falls as much as the market; lower = more defensive).

|  | Sharpe 72-89 | Sharpe 90- | MaxDD 72-89 | MaxDD 90- | Beta 72-89 | Beta 90- | DownCap 72-89 | DownCap 90- | Corr UST 72-89 | Corr UST 90- | Corr Gold 72-89 | Corr Gold 90- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NoDur | 0.48 | 0.58 | -51.9% | -33.6% | 0.95 | 0.62 | 0.85 | 0.51 | 0.31 | 0.08 | -0.08 | -0.03 |
| Durbl | 0.18 | 0.37 | -56.6% | -73.7% | 1.04 | 1.40 | 1.11 | 1.33 | 0.19 | -0.13 | -0.03 | -0.03 |
| Manuf | 0.22 | 0.56 | -43.8% | -59.4% | 1.10 | 1.12 | 1.16 | 1.07 | 0.18 | -0.10 | 0.01 | -0.05 |
| Enrgy | 0.40 | 0.41 | -49.0% | -64.7% | 0.89 | 0.81 | 0.70 | 0.70 | 0.04 | -0.16 | 0.07 | -0.02 |
| Chems | 0.27 | 0.49 | -36.6% | -43.6% | 1.03 | 0.75 | 1.04 | 0.73 | 0.20 | -0.01 | -0.02 | -0.02 |
| BusEq | 0.06 | 0.57 | -52.0% | -79.6% | 1.10 | 1.33 | 1.19 | 1.35 | 0.16 | -0.09 | 0.02 | -0.06 |
| Telcm | 0.65 | 0.28 | -23.1% | -72.0% | 0.60 | 0.89 | 0.39 | 0.94 | 0.36 | -0.01 | -0.12 | -0.06 |
| Utils | 0.37 | 0.52 | -42.6% | -37.9% | 0.63 | 0.43 | 0.50 | 0.33 | 0.44 | 0.20 | -0.06 | -0.01 |
| Shops | 0.25 | 0.60 | -57.5% | -38.0% | 1.14 | 0.91 | 1.22 | 0.86 | 0.27 | -0.03 | -0.09 | -0.11 |
| Hlth | 0.27 | 0.62 | -47.1% | -35.3% | 0.96 | 0.70 | 0.89 | 0.64 | 0.29 | 0.09 | -0.04 | -0.00 |
| Money | 0.26 | 0.49 | -54.8% | -72.5% | 1.03 | 1.07 | 1.06 | 1.05 | 0.36 | -0.09 | -0.06 | -0.13 |
| Other | 0.24 | 0.36 | -58.0% | -59.4% | 1.20 | 1.04 | 1.29 | 1.10 | 0.19 | -0.08 | 0.03 | -0.07 |
| MKT | 0.30 | 0.59 | -46.5% | -50.3% | 1.00 | 1.00 | 1.00 | 1.00 | 0.26 | -0.06 | -0.01 | -0.07 |
| UST10 | 0.13 | 0.32 | -15.7% | -26.1% | 0.14 | -0.03 | 0.02 | -0.13 | 1.00 | 1.00 | -0.11 | 0.12 |
| GOLD | 0.32 | 0.37 | -55.7% | -39.3% | -0.02 | -0.05 | -0.25 | -0.28 | -0.11 | 0.12 | 1.00 | 1.00 |

Most defensive sectors by down capture: 1972-89 Telcm, Utils, Enrgy; 1990-latest Utils, NoDur, Hlth. Rank correlation of sector down capture across eras: 0.69; of sector beta: 0.62; of sector Sharpe: -0.14.

## B. Do bonds still hedge sectors? Correlation with the 10y Treasury by decade

Monthly-return correlation within each decade. Negative = the Treasury hedged that sector.

|  | 1972-79 | 1980s | 1990s | 2000s | 2010s | 2020-26 |
|---|---|---|---|---|---|---|
| NoDur | 0.26 | 0.34 | 0.30 | -0.07 | -0.18 | 0.22 |
| Durbl | 0.20 | 0.18 | 0.13 | -0.28 | -0.50 | 0.11 |
| Manuf | 0.23 | 0.17 | 0.20 | -0.24 | -0.49 | 0.23 |
| Enrgy | 0.22 | -0.02 | 0.26 | -0.13 | -0.50 | -0.19 |
| Chems | 0.19 | 0.21 | 0.19 | -0.20 | -0.33 | 0.28 |
| BusEq | 0.21 | 0.14 | 0.15 | -0.30 | -0.42 | 0.31 |
| Telcm | 0.37 | 0.35 | 0.35 | -0.25 | -0.34 | 0.31 |
| Utils | 0.39 | 0.52 | 0.59 | -0.03 | 0.16 | 0.24 |
| Shops | 0.24 | 0.29 | 0.15 | -0.21 | -0.32 | 0.29 |
| Hlth | 0.23 | 0.34 | 0.31 | -0.10 | -0.24 | 0.38 |
| Money | 0.31 | 0.41 | 0.32 | -0.14 | -0.68 | 0.07 |
| Other | 0.26 | 0.17 | 0.18 | -0.23 | -0.48 | 0.27 |
| MKT | 0.28 | 0.26 | 0.31 | -0.25 | -0.49 | 0.28 |

Correlation with gold by decade:

|  | 1972-79 | 1980s | 1990s | 2000s | 2010s | 2020-26 |
|---|---|---|---|---|---|---|
| NoDur | -0.14 | 0.02 | -0.09 | -0.01 | -0.08 | 0.12 |
| Durbl | -0.16 | 0.09 | -0.01 | -0.18 | -0.08 | 0.11 |
| Manuf | -0.12 | 0.13 | -0.02 | -0.12 | -0.05 | 0.04 |
| Enrgy | -0.16 | 0.21 | 0.01 | -0.07 | -0.03 | -0.01 |
| Chems | -0.10 | 0.06 | -0.01 | -0.10 | -0.00 | 0.13 |
| BusEq | -0.15 | 0.15 | -0.10 | -0.08 | -0.04 | 0.08 |
| Telcm | -0.14 | -0.08 | -0.05 | -0.12 | -0.09 | 0.19 |
| Utils | -0.14 | 0.06 | -0.09 | -0.10 | 0.00 | 0.17 |
| Shops | -0.14 | -0.02 | -0.11 | -0.22 | -0.09 | 0.06 |
| Hlth | -0.01 | -0.03 | 0.05 | -0.02 | -0.05 | 0.08 |
| Money | -0.10 | 0.02 | 0.04 | -0.16 | -0.23 | -0.10 |
| Other | -0.11 | 0.17 | -0.03 | -0.14 | -0.11 | 0.07 |
| MKT | -0.14 | 0.11 | -0.05 | -0.10 | -0.10 | 0.07 |

## C. Stress episodes: which sectors protected?

|  | NoDur | Durbl | Manuf | Enrgy | Chems | BusEq | Telcm | Utils | Shops | Hlth | Money | Other | MKT | UST10 | GOLD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1973-74 oil shock / stagflation | -51.9% | -54.5% | -43.8% | -30.1% | -36.6% | -51.0% | -23.1% | -41.7% | -57.5% | -46.6% | -54.5% | -54.4% | -46.5% | 1.6% | 137.5% |
| 1980-82 Volcker tightening | 43.7% | 20.6% | 1.2% | -4.1% | 1.9% | 8.5% | 37.2% | 25.2% | 44.4% | 36.8% | 18.3% | 14.9% | 15.1% | 14.6% | -25.5% |
| 1987 crash | -29.3% | -35.3% | -31.2% | -30.3% | -30.0% | -35.0% | -17.3% | -11.4% | -38.3% | -29.6% | -28.6% | -33.5% | -29.9% | 2.3% | 1.5% |
| 1990 Gulf war recession | -9.6% | -28.4% | -22.4% | 1.0% | -15.7% | -26.5% | -10.1% | 1.5% | -25.4% | -7.0% | -30.3% | -24.2% | -16.5% | 1.4% | 8.2% |
| 1998 LTCM | -15.6% | -19.2% | -18.2% | -5.4% | -20.0% | -4.7% | 0.4% | 4.3% | -15.5% | -2.0% | -21.0% | -18.4% | -11.8% | 9.4% | -1.0% |
| 2000-02 dot-com bust | 12.0% | -22.5% | -26.9% | -15.4% | 7.4% | -78.7% | -64.3% | -21.4% | -13.1% | -28.6% | -15.4% | -43.0% | -45.0% | 30.7% | 16.2% |
| 2007-09 GFC | -33.1% | -72.3% | -59.4% | -41.3% | -42.3% | -50.1% | -48.8% | -37.6% | -34.6% | -30.8% | -69.7% | -59.4% | -50.3% | 17.9% | 24.9% |
| 2020 Covid crash | -18.7% | -28.3% | -27.1% | -44.6% | -17.8% | -16.0% | -18.6% | -21.6% | -14.1% | -10.2% | -28.7% | -24.6% | -20.2% | 8.0% | 2.0% |
| 2022 inflation shock | -1.2% | -33.0% | -15.2% | 70.2% | -20.1% | -30.2% | -19.4% | -2.6% | -21.0% | -9.0% | -9.0% | -21.8% | -18.8% | -18.3% | -7.0% |
| 2025 tariff shock | 5.3% | -26.4% | -9.2% | -8.1% | -6.1% | -11.7% | 2.6% | 1.4% | -10.0% | -1.5% | -9.6% | -2.5% | -8.5% | 4.4% | 18.7% |

Best and worst sector in each episode:

|  | best sector | best | worst sector | worst | market | 10y Treasury | gold |
|---|---|---|---|---|---|---|---|
| 1973-74 oil shock / stagflation | Telcm | -23.1% | Shops | -57.5% | -46.5% | 1.6% | 137.5% |
| 1980-82 Volcker tightening | Shops | 44.4% | Enrgy | -4.1% | 15.1% | 14.6% | -25.5% |
| 1987 crash | Utils | -11.4% | Shops | -38.3% | -29.9% | 2.3% | 1.5% |
| 1990 Gulf war recession | Utils | 1.5% | Money | -30.3% | -16.5% | 1.4% | 8.2% |
| 1998 LTCM | Utils | 4.3% | Money | -21.0% | -11.8% | 9.4% | -1.0% |
| 2000-02 dot-com bust | NoDur | 12.0% | BusEq | -78.7% | -45.0% | 30.7% | 16.2% |
| 2007-09 GFC | Hlth | -30.8% | Durbl | -72.3% | -50.3% | 17.9% | 24.9% |
| 2020 Covid crash | Hlth | -10.2% | Enrgy | -44.6% | -20.2% | 8.0% | 2.0% |
| 2022 inflation shock | Enrgy | 70.2% | Durbl | -33.0% | -18.8% | -18.3% | -7.0% |
| 2025 tariff shock | NoDur | 5.3% | Durbl | -26.4% | -8.5% | 4.4% | 18.7% |

Episodes (of 10) in which each sector beat the market: Hlth 9, Utils 9, NoDur 8, Telcm 8, Enrgy 7, Chems 6, Money 4, Shops 4, BusEq 3, Manuf 3, Durbl 2, Other 2.

Times in the top 3 sectors: NoDur 5, Utils 5, Telcm 5, Hlth 4, Shops 4, Enrgy 3, Chems 2, BusEq 1, Money 1, Durbl 0, Manuf 0, Other 0.  
Times in the bottom 3 sectors: Durbl 8, BusEq 5, Money 5, Shops 3, Other 3, Chems 2, Enrgy 2, Manuf 1, Telcm 1, NoDur 0, Utils 0, Hlth 0.

Episodes with a positive return: 10y Treasury 9, gold 7, best sector 6 of 10 (the best sector is only known after the fact).

## D. Sector-level regime map: does the same sector win in the same regime in both eras?

Spearman rank correlation of the 12 sectors' Sharpe ratios within each real-time regime, 1972-89 vs 1990-latest (Treasuries and gold excluded).

| regime | rank corr (sectors only) | top 3 sectors 1972-89 | top 3 sectors 1990- | bottom 3 sectors 1972-89 | bottom 3 sectors 1990- |
|---|---|---|---|---|---|
| Goldilocks | -0.07 | Telcm, NoDur, Utils | Hlth, Money, Shops | Enrgy, BusEq, Other | Durbl, Other, Chems |
| Reflation | 0.05 | Telcm, Hlth, Enrgy | BusEq, Hlth, Utils | Durbl, Utils, BusEq | Durbl, Shops, Other |
| Stagflation | 0.10 | Enrgy, Other, Chems | Utils, NoDur, Hlth | BusEq, Durbl, Shops | Durbl, Telcm, BusEq |
| Disinflationary slowdown | -0.06 | Utils, NoDur, Shops | Durbl, Shops, BusEq | Hlth, BusEq, Money | Utils, Enrgy, Hlth |

## E. Study 1 attribution: did Regime Tilt's sector bets add value?

Regime Tilt minus Uncond. Tilt, monthly return gap split additively into: sector selection (mix within the equity sleeve), equity sleeve size (more or less equity, valued at the control's sector mix), and the Treasury + gold holdings (difference in UST10 and GOLD weights times their returns). Annualised arithmetic means in percentage points, gross of costs, using target weights at the start of each month (within-month drift ignored).

|  | sector selection | equity sleeve size | Treasury + gold holdings | total (gross, before costs) |
|---|---|---|---|---|
| 1990-latest | 0.78 | -0.78 | 0.56 | 0.56 |
| 1990s | -0.10 | -1.38 | -0.26 | -1.74 |
| 2000s | 0.42 | -0.23 | 1.09 | 1.28 |
| 2010s | 0.56 | -0.48 | 0.79 | 0.87 |
| 2020-26 | 2.98 | -1.15 | 0.64 | 2.47 |
| 2008 GFC (2007-11..2009-02) | -0.37 | 0.56 | 0.98 | 1.18 |
| 2022 (Jan-Oct) | -0.74 | 1.80 | -3.16 | -2.10 |

Is any component distinguishable from zero? Stationary block bootstrap of the 1990-latest mean (mean block 12, 5,000 resamples, seed 20260101; descriptive, not a pre-registered test):

|  | mean (pp/yr) | 95% CI low | 95% CI high | p (two-sided) |
|---|---|---|---|---|
| sector selection | 0.78 | 0.22 | 1.39 | 0.01 |
| equity sleeve size | -0.78 | -1.26 | -0.29 | 0.00 |
| Treasury + gold holdings | 0.56 | -0.06 | 1.26 | 0.09 |
| total (gross, before costs) | 0.56 | -0.52 | 1.65 | 0.31 |

Average Regime Tilt weights by real-time regime (out-of-sample 1990-latest):

|  | Goldilocks | Reflation | Stagflation | Disinflationary slowdown | Uncond. Tilt (all months) |
|---|---|---|---|---|---|
| NoDur | 11.0% | 4.1% | 7.7% | 13.4% | 12.8% |
| Durbl | 4.4% | 1.3% | 2.1% | 7.9% | 2.5% |
| Manuf | 5.2% | 3.8% | 4.0% | 4.8% | 4.5% |
| Enrgy | 6.2% | 6.4% | 11.0% | 6.1% | 8.1% |
| Chems | 6.1% | 3.5% | 5.7% | 5.8% | 5.8% |
| BusEq | 3.4% | 5.0% | 1.9% | 4.7% | 2.9% |
| Telcm | 12.4% | 11.3% | 6.1% | 5.8% | 11.1% |
| Utils | 10.7% | 6.4% | 8.6% | 8.1% | 9.9% |
| Shops | 5.3% | 2.1% | 4.4% | 9.7% | 4.9% |
| Hlth | 7.2% | 5.6% | 6.1% | 3.8% | 7.0% |
| Money | 6.9% | 3.6% | 5.9% | 3.4% | 5.0% |
| Other | 3.6% | 1.9% | 4.1% | 3.0% | 2.4% |
| Total equity | 82.3% | 55.2% | 67.4% | 76.5% | 77.1% |
| UST10 | 13.2% | 17.0% | 18.8% | 14.0% | 15.1% |
| GOLD | 4.5% | 27.8% | 13.8% | 9.5% | 7.8% |
