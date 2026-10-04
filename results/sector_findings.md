# Sector findings (the sector dimension of the study)

*Descriptive analysis; no new strategy is tested. Full tables are in `results/sector_deepdive.md`
(produced by `sector_analysis.py`), with charts in `results/sector_charts/`. Data: Ken French 12
value-weighted industries, 1972-01 to 2026-08. The industries are SIC-based, so GICS analogues are
approximate (NoDur ≈ staples, BusEq ≈ tech, Durbl ≈ autos/durables, Money ≈ financials).*

## 1. Sectors' risk character is persistent; their regime returns are not

- **Persistent:** sector beta and down-market behaviour keep their ranking across eras.
  - The rank correlation of down capture between 1972-89 and 1990-2026 is 0.69, and of beta 0.62.
  - Since 1990 the most defensive sectors have been Utilities (down capture 0.33), Staples
    (0.51) and Health (0.64).
  - The most aggressive have been Tech (BusEq, 1.35) and Durables (1.33).
- **Not persistent:** sector *returns* within each macro regime.
  - The rank correlation of sector Sharpe ratios between eras is -0.07 to 0.10 within each regime,
    and -0.14 unconditionally.
  - Example: in stagflation, the top three sectors were Energy, Other and Materials (Chems) in
    1972-89, but Utilities, Staples and Health after 1990.
- **Implication:** you can reliably pick sectors that *fall less*, but not sectors that *earn more*
  in a given regime. That explains why Study 1's regime map, which tilts on regime-conditional
  returns, did not carry over.

## 2. Defensive sectors soften crashes but do not hedge them

Across the 10 stress episodes from 1973-74 to the 2025 tariff shock:
- **Health and Utilities beat the market in 9 of 10 episodes, and Staples in 8.** None of the three
  was ever among the 3 worst sectors.
- **Durables was among the 3 worst sectors in 8 of 10 episodes;** Tech and Financials in 5 each.
- **Even defensive sectors lost heavily in the big bear markets.** Utilities lost 41.7% in 1973-74
  and 37.6% in the GFC; Staples lost 51.9% and 33.1%.
- **The best sector was positive in only 6 of 10 episodes, and it is only known after the fact.**
  The 10y Treasury was positive in 9 of 10 and gold in 7 of 10.
- **Energy is the one sector that hedged an inflation shock:** +70.2% in 2022, when the market
  lost 18.8% and Treasuries 18.3%. It was also the worst sector in the 2020 Covid crash (-44.6%)
  and lost in 1973-74 (-30.1%), so it is not a general hedge.

## 3. "Bonds no longer hedge stocks" holds for most sectors, not all

Correlation of each sector with the 10y Treasury, by decade:
- **Negative for every sector in the 2000s and 2010s.** In the 2010s it ran from -0.18 for Staples
  to -0.68 for Financials. Utilities was the one exception in the 2010s (+0.16).
- **Positive again in 2020-26 for 11 of 12 sectors,** and +0.28 for the market. This matches the
  1970s-1990s pattern.
- **Energy is the exception (-0.19):** in an inflation shock, Energy and bonds move in opposite
  directions.
- **Utilities was positively correlated with bonds in five of six decades** (-0.03 in the 2000s,
  when every other sector was clearly negative). It behaves like a bond proxy, so it diversifies
  away from bonds least.
- **Gold's correlation with every sector stayed near zero in every decade** (-0.23 to +0.21).

## 4. Did Study 1's regime strategy gain anything from its sector bets?

Regime Tilt minus Uncond. Tilt, 1990-2026, gross of costs, in pp a year:

| Component | Mean | 95% CI | p |
|---|---|---|---|
| Sector selection (mix within equities) | +0.78 | [+0.22, +1.39] | 0.01 |
| Equity sleeve size | -0.78 | [-1.26, -0.29] | <0.01 |
| Treasury + gold holdings | +0.56 | [-0.06, +1.26] | 0.09 |
| **Total** | +0.56 | [-0.52, +1.65] | 0.31 |

- **Sector selection was the only positive component, but it is fragile.**
  - 1990-2019: +0.29 pp a year (p = 0.12).
  - 2020-26: +2.98 pp a year.
  - In 2020-26, Durables alone contributed 2.11 pp, mainly in 2020 and 2023. The regime map
    overweighted Durables in Disinflationary slowdown (7.9% vs 2.5% in the control).
  - Ken French's Durables portfolio is the autos industry, likely dominated recently by a few very
    large stocks. That is one industry's run, not a repeatable rotation skill.
- **Cutting equity in Reflation and Stagflation cost as much as selection added.** Equity was 55%
  of the portfolio in Reflation and 67% in Stagflation, against 77% in the control.
- **The Treasury + gold bets explain 2022:** -3.16 pp annualised over January-October 2022.

These bootstraps are exploratory. They split up a result already reported, and they were not
pre-registered.

## What the sector analysis adds to the conclusions

1. **Within equities, defensiveness is real and persistent:** Utilities, Staples and Health
   consistently lose less. A defensive equity tilt is a legitimate way to lower equity risk. It is
   not a substitute for Treasuries or gold, which actually rose in most crises.
2. **Sector rotation by macro regime is not supported.** Regime-conditional sector rankings
   reshuffle completely between eras, and the one period of successful selection is dominated by a
   single industry.
3. **The breakdown of the bond hedge is broad-based.** It reappeared in 2020-26 for nearly every
   sector. Energy is the only equity-based inflation hedge, and only in inflation shocks.

## Possible next test (not run; would need pre-registration)

"Defensive equity sleeve": replace the market in Static 1/3 with an equal-weight mix of
Utilities, Staples and Health. Its motivation comes from data already seen (sections 1-2), so it
could only be tested on new data. The only candidate within the approved sources is the Ken French
international industry data. It would need to be checked first, without looking at returns.
