# Study 3: trend with cash, and an international test of volatility management

*Pre-registered in `PREREGISTRATION_STUDY3.md` (commit 00412ae) before any code was written or
any international return was examined. The code and tests were committed before the real run.
Full tables are in `results_study3/report.md`. Primary test: Developed ex US equity (Ken French,
USD) + US 10y Treasury + gold, return months 1991-07 to 2026-08 (422 months), after costs.*

## Verdict

**Under the pre-registered criterion, no hypothesis is supported.** H4a, trend-following with
cash, nevertheless shows a large and consistent drawdown reduction. That pattern is worth a
separate confirmatory test, with caveats.

| Hypothesis (Developed ex US) | Sharpe vs Static 1/3 | Max DD vs Static 1/3 | Verdict |
|---|---|---|---|
| H4a Trend + cash (Faber) | 0.72 vs 0.59 (+0.13, Holm p = 1.00) | **-10.4% vs -20.1%** (+9.7 pp, p = 0.04 unadjusted, Holm p = 0.22) | Not supported |
| H4b Trend, cash fallback only | 0.68 vs 0.59 (+0.09, Holm p = 1.00) | -26.4% vs -20.1% (worse) | Not supported |
| H5 Vol-managed equity | 0.50 vs 0.59 (-0.09, Holm p = 1.00) | -20.5% vs -20.1% | Not supported; **US result not confirmed** |

## What each test shows

**H5: volatility management does not carry over to international markets.**
- Its Sharpe ratio is lower than Static 1/3's in every international region:
  - Developed ex US -0.09;
  - Europe -0.01;
  - Asia Pacific ex Japan -0.06;
  - Japan -0.18 (p = 0.01 unadjusted, Holm p = 0.13).
- Its drawdown is no better: -20.5% vs -20.1% in Developed ex US, and -29.8% vs -21.3% in Japan.
- The small US improvement from Study 2 (+3.1 pp drawdown) does not replicate, so it should be
  treated as noise.
- **This is the clearest result of Study 3: the one promising idea from Study 2 failed its
  confirmation.**

**H4b: adding cash only as a last resort did not fix 2022.**
- In 2022 it lost 16.9% (Developed ex US) against 16.2% for the control, and its max drawdown was
  worse in every region except Japan.
- The cause was concentration, not the lack of cash: usually one asset still passed the trend
  filter and received all the weight.
- So the Study 2 diagnosis was incomplete. Redistributing to the "survivors" is the weak point.

**H4a: holding cash in place of each failing asset halved drawdowns, but the evidence is weaker
than it looks.**
- Max drawdown was about half the control's in all five universes:

  | Universe | H4a max DD | Static 1/3 max DD |
  |---|---|---|
  | Developed ex US | -10.4% | -20.1% |
  | Europe | -9.7% | -21.5% |
  | Japan | -9.3% | -21.3% |
  | Asia Pacific ex Japan | -11.1% | -22.6% |
  | US, 1973-2026 | -10.6% | -20.2% |

- The reduction holds with a skip-month signal and with doubled costs.
- **2022:** it lost 5.7% against 16.2% for the control (Developed ex US). It was 100% in cash from
  August to December 2022.
- Every stress episode in the window was better than the control, except the 2025 tariff shock,
  when it gained less (+7.0% vs +9.7%).
- **Why this is weaker evidence than it looks:**
  1. It fails the pre-registered test. The Sharpe gain is not significant, and the drawdown test
     (p = 0.04 unadjusted) does not survive Holm correction (0.22).
  2. The five universes are not independent. Treasuries and gold make up 2/3 of every portfolio
     and are the same series everywhere. H4a's monthly returns are correlated 0.66-0.93 across
     regions, so this is roughly one result seen five times, not five confirmations.
  3. Much of the protection comes from simply holding about 40% cash on average. It lowers
     volatility (5.4% vs 7.5%) and CAGR (6.5% vs 6.8%). A fair comparison would be a static mix
     with the same average cash.
  4. The US data (1973-89 and 1990+) had been seen. H4a is significant there unadjusted (Sharpe
     +0.21, p = 0.03), but that is exploratory.

## Synthesis across Studies 1-3

| Idea | Study | Result |
|---|---|---|
| Macro regime tilting | 1 | Small, insignificant gain; no drawdown benefit |
| Switch between bonds and gold on stock-bond correlation | 2 | Significantly worse |
| Trend with no cash | 2 | Higher return, worse drawdown, failed in 2022 |
| Volatility-managed equity | 2 → 3 | Small US benefit, **not confirmed** internationally |
| Trend, cash only as last resort | 3 | No improvement; concentration hurts |
| Trend, cash per failing sleeve | 3 | **Drawdown halved in all universes**; not significant after correction, and the evidence is correlated |

1. **Static diversification across equities, Treasuries and gold is a hard benchmark.** No
   pre-registered rule beat it under the agreed criteria in three studies.
2. **Concentrating into whichever hedge looks good fails** (Studies 1, 2 and H4b). Treasuries
   failed in 2022 and gold in 1980-82.
3. **The only pattern that recurs is "step aside into cash when an asset is in a downtrend".** That
   is a cash-management effect, not a better hedge. It needs confirmation against a static
   portfolio with the same cash share, before it is claimed.

## Suggested next step (not run; it would need its own pre-registration)

Test H4a against **a static portfolio holding H4a's long-run average cash share** (about 40%), with
**max drawdown as the primary statistic**. This separates timing skill from simply holding less
risk. Data neither study has used is now scarce: international bond and gold series in local
currency are not in the approved free sources. Any such test should be labelled as a robustness
analysis of seen data.
