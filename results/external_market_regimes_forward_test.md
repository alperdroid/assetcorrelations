# Forward test of market-regimes labels (exploratory)

SPY, 2006-02-03 to 2025-11-14, 238 non-overlapping 21-trading-day windows. Label = the classifier's out-of-sample label at the close of day t; outcome = the next 21 trading days. Returns are SPY excess log returns, annualised (x12); volatility is annualised daily volatility.

## Next-month SPY outcome by today's regime label

| classifier   | regime today   |   windows | next-month return (ann.)   |   t-stat | next-month vol (ann.)   |
|:-------------|:---------------|----------:|:---------------------------|---------:|:------------------------|
| VIX          | Calm           |       154 | +6.2%                      |     1.59 | 12.0%                   |
| VIX          | Transitional   |        59 | +12.4%                     |     1.51 | 18.6%                   |
| VIX          | Crisis         |        25 | +31.1%                     |     1.41 | 33.9%                   |
| HMM          | Calm           |       128 | +5.1%                      |     1.02 | 13.5%                   |
| HMM          | Transitional   |        89 | +12.8%                     |     1.88 | 17.7%                   |
| HMM          | Crisis         |        21 | +32.1%                     |     1.98 | 23.8%                   |
| GMM          | Calm           |       145 | +5.8%                      |     1.21 | 13.5%                   |
| GMM          | Transitional   |        70 | +13.8%                     |     1.99 | 16.6%                   |
| GMM          | Crisis         |        23 | +28.3%                     |     1.55 | 29.8%                   |
| Ensemble     | Calm           |       147 | +5.8%                      |     1.35 | 12.6%                   |
| Ensemble     | Transitional   |        70 | +11.1%                     |     1.29 | 18.8%                   |
| Ensemble     | Crisis         |        21 | +39.7%                     |     2.35 | 30.3%                   |

## How much does today's label explain? (in-sample R² across windows)

| classifier   |   R² next-month return |   ANOVA p (returns) |   R² next-month vol |   R² vol: past 21-day vol only |   R² vol: past vol + label |
|:-------------|-----------------------:|--------------------:|--------------------:|-------------------------------:|---------------------------:|
| VIX          |                  0.015 |                0.16 |               0.361 |                          0.432 |                      0.458 |
| HMM          |                  0.016 |                0.15 |               0.079 |                          0.432 |                      0.434 |
| GMM          |                  0.013 |                0.22 |               0.178 |                          0.432 |                      0.454 |
| Ensemble     |                  0.024 |                0.06 |               0.217 |                          0.432 |                      0.452 |

Reading: a label 'forecasts' returns only if returns differ by regime beyond noise (ANOVA p); it adds risk information only if 'past vol + label' clearly beats 'past vol only'.

## Persistence

| classifier   | same label 21 days later   |
|:-------------|:---------------------------|
| HMM          | 61%                        |
| GMM          | 62%                        |
| VIX          | 75%                        |
