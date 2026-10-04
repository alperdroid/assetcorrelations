# Synthesis: Studies 1-4

**Research question:** can a simple, real-time rule allocating between US Treasuries, gold and
equities give better drawdown protection than static diversification, now that bonds no longer
reliably hedge stocks?

**Answer: not reliably.** Across four studies and ten active strategies, no rule beat static
diversification under its pre-agreed test. The one recurring improvement, trend-following into
cash, turns out to be mostly the effect of holding less risk.

## The studies

| Study | Idea | Data | Pre-registered verdict | Key numbers |
|---|---|---|---|---|
| 1 | Macro regime (growth × inflation) tilts across 12 sectors, Treasuries, gold | US, OOS 1990-2026 | Not supported | Regime value +0.45 pp a year (p = 0.36); max DD -30.2% vs Static 1/3 -15.8% |
| 2 | H1 bond↔gold switch on stock-bond correlation | US 1973-2026 | **Significantly worse** | Sharpe -0.20 (Holm p = 0.04); max DD -39.6% vs -20.2% |
| 2 | H2a/H2b trend, no cash | US 1973-2026 | Not supported | Higher return; worst 2022 loss (-28.3%) |
| 2 | H3 volatility-managed equity | US 1973-2026 | Not supported | Sharpe +0.00; max DD +3.1 pp (p = 0.24) |
| 3 | H5 volatility management, international confirmation | 4 regions 1991-2026 | Not supported; **US result not replicated** | Sharpe -0.01 to -0.18 in every region |
| 3 | H4b trend, cash as last resort | 4 regions + US | Not supported | Concentration, not lack of cash, was the problem |
| 3 | H4a trend, failing sleeve to cash | 4 regions + US | Not supported (Holm) | Max DD about -10% vs -20% everywhere (correlated evidence) |
| 4 | Is H4a timing or just cash? | Same as Study 3 | Not supported | About 8 of the 9.7 pp drawdown gain comes from cash; timing +1.7 pp (p = 0.61) |

## Five conclusions

1. **Static diversification across equities, Treasuries and gold is a hard benchmark.** Holding
   1/3 each, rebalanced monthly, had a max drawdown of -20% since 1973 and -16% since 1990. That
   was better than 60/40 (-29%) and every timing rule that had to stay fully invested.
2. **Switching between hedges fails, and holding both works.**
   - Treasuries failed as a hedge in 2022 and gold in 1980-82.
   - Every rule that concentrated into whichever hedge looked best was hurt exactly when that hedge
     failed: Study 1's stagflation bet on Treasuries, the H1 switch, and trend without cash.
3. **Which assets hedge in which macro regime is not stable over time.** The regime map from
   1972-89 does not predict 1990-2026 (rank correlations -0.22 to 0.28). For example, Treasuries
   in stagflation ranked 12th of 14 assets before 1990 and 2nd after.
4. **Volatility management did not generalise.** A small US improvement was not confirmed in four
   international regions. This is the cleanest test in the project, on data not used before.
5. **"Trend + cash" protection is mostly cash.**
   - Most of the halving of drawdowns is reproduced by a static portfolio holding the same
     average cash.
   - Timing adds a small, consistently signed edge in slow bear markets (2000-02, 2008, 2022), but
     it is not statistically established.

## Practical implication (cautious)

For a long-only investor worried that bonds no longer hedge stocks, the evidence here supports
two things:
- **holding both Treasuries and gold permanently** alongside equities;
- **deciding the overall risk level directly**, by holding cash.

It does not support timing between hedges with macro, correlation, volatility or trend signals.
A trend-into-cash rule is defensible as a way to cut risk during prolonged declines. Its benefit
over simply holding the same cash is unproven.

## Integrity notes

- Study 1's design was fixed before results.
- Studies 2-4 were each pre-registered (`PREREGISTRATION*.md`) and committed before code and
  results. The git history shows the order.
- All variants are reported, including unfavourable ones, and Holm corrections are applied.
- Studies 2-4 were conceived after earlier results were seen. Only Study 3's international equity
  data was new.
- Every result-altering data choice is in `DEVIATIONS.md`.

## Main limitations

- **Gold data:** gold is a World Bank monthly average throughout (no free month-end series within
  the approved sources).
- **US-only bonds and gold:** the Treasury and gold legs are US-based in every universe.
- **Few independent episodes:** there are few independent crisis episodes, and bootstrap drawdown
  tests have low power.
- **Industry definitions:** Ken French industries are not GICS sectors.

## Where to read more

- `results/findings_draft.md`: Study 1.
- `results/study2_findings.md`, `results/study3_findings.md`, `results/study4_findings.md`.
- Full tables: `results_study*/report.md`.
