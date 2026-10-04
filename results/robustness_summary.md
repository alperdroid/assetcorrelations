# Robustness summary: all runs

RT = Regime Tilt (main strategy), UT = Uncond. Tilt (same machinery, no regime information). Value of the regime map = CAGR(RT) - CAGR(UT); cost of detection lag = CAGR(Oracle Tilt) - CAGR(RT). All figures are out-of-sample, after transaction costs. Every run is reported, favourable or not.

Runs not found (not run or failed): results_gold_avg

## Headline

| run | folder | OOS | gold | RT Sharpe | UT Sharpe | 60/40 Sharpe | RT MaxDD | UT MaxDD | 60/40 MaxDD | RT CAGR | UT CAGR | Value of regime map | Cost of detection lag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Main (default settings) | results_main | 1990-01 to 2026-08 | avg | 0.69 | 0.64 | 0.67 | -30.2% | -31.3% | -28.8% | 9.37% | 8.92% | +0.45% | +0.35% |
| 17 industries | results_ind17 | 1990-01 to 2026-08 | avg | 0.68 | 0.67 | 0.67 | -34.8% | -32.5% | -28.8% | 9.66% | 9.38% | +0.28% | +0.54% |
| Regime confirmation 2 months | results_confirm2 | 1990-01 to 2026-08 | avg | 0.72 | 0.64 | 0.67 | -27.1% | -31.3% | -28.8% | 9.66% | 8.92% | +0.75% | +0.05% |
| OOS start 2000-01 | results_oos2000 | 2000-01 to 2026-08 | avg | 0.72 | 0.58 | 0.57 | -30.2% | -31.3% | -28.8% | 8.84% | 7.46% | +1.38% | +0.36% |
| Sample 1982-, OOS 2000-01 | results_start1982 | 2000-01 to 2026-08 | avg | 0.70 | 0.63 | 0.57 | -28.9% | -28.1% | -28.8% | 8.47% | 7.35% | +1.12% | +0.27% |
| Transaction costs x2 | results_costx2 | 1990-01 to 2026-08 | avg | 0.67 | 0.64 | 0.67 | -30.3% | -31.3% | -28.8% | 9.17% | 8.90% | +0.27% | +0.38% |
| Oct-2025 gap not interpolated | results_gap_asis | 1990-01 to 2026-08 | avg | 0.70 | 0.64 | 0.67 | -30.2% | -31.3% | -28.8% | 9.44% | 8.92% | +0.52% | +0.27% |
| All assets on monthly-average prices | results_all_avg | 1990-01 to 2026-08 | avg | 0.81 | 0.74 | 0.79 | -30.3% | -30.8% | -26.4% | 9.52% | 8.95% | +0.57% | +0.62% |

## All strategies, all runs

| run | strategy | Sharpe | MaxDD | CAGR | Vol | Turnover/m |
|---|---|---|---|---|---|---|
| Main (default settings) | Regime Tilt | 0.69 | -30.2% | 9.37% | 9.8% | 7.3% |
| Main (default settings) | Uncond. Tilt | 0.64 | -31.3% | 8.92% | 10.0% | 0.6% |
| Main (default settings) | Regime ERC | 0.73 | -27.5% | 9.23% | 8.9% | 2.4% |
| Main (default settings) | Uncond. ERC | 0.73 | -27.7% | 9.09% | 8.8% | 1.4% |
| Main (default settings) | Oracle Tilt | 0.73 | -30.3% | 9.71% | 9.7% | 5.9% |
| Main (default settings) | 60/40 | 0.67 | -28.8% | 8.91% | 9.4% | 0.9% |
| Main (default settings) | Static 1/3 | 0.77 | -15.8% | 8.01% | 6.9% | 1.1% |
| 17 industries | Regime Tilt | 0.68 | -34.8% | 9.66% | 10.5% | 7.2% |
| 17 industries | Uncond. Tilt | 0.67 | -32.5% | 9.38% | 10.3% | 0.6% |
| 17 industries | Regime ERC | 0.70 | -31.2% | 9.56% | 10.0% | 2.7% |
| 17 industries | Uncond. ERC | 0.69 | -31.4% | 9.37% | 9.8% | 1.5% |
| 17 industries | Oracle Tilt | 0.73 | -34.7% | 10.21% | 10.5% | 6.2% |
| 17 industries | 60/40 | 0.67 | -28.8% | 8.91% | 9.4% | 0.9% |
| 17 industries | Static 1/3 | 0.77 | -15.8% | 8.01% | 6.9% | 1.1% |
| Regime confirmation 2 months | Regime Tilt | 0.72 | -27.1% | 9.66% | 9.7% | 4.9% |
| Regime confirmation 2 months | Uncond. Tilt | 0.64 | -31.3% | 8.92% | 10.0% | 0.6% |
| Regime confirmation 2 months | Regime ERC | 0.71 | -27.9% | 9.04% | 9.0% | 2.2% |
| Regime confirmation 2 months | Uncond. ERC | 0.73 | -27.7% | 9.09% | 8.8% | 1.4% |
| Regime confirmation 2 months | Oracle Tilt | 0.73 | -30.3% | 9.71% | 9.7% | 5.9% |
| Regime confirmation 2 months | 60/40 | 0.67 | -28.8% | 8.91% | 9.4% | 0.9% |
| Regime confirmation 2 months | Static 1/3 | 0.77 | -15.8% | 8.01% | 6.9% | 1.1% |
| OOS start 2000-01 | Regime Tilt | 0.72 | -30.2% | 8.84% | 9.8% | 7.0% |
| OOS start 2000-01 | Uncond. Tilt | 0.58 | -31.3% | 7.46% | 10.0% | 0.5% |
| OOS start 2000-01 | Regime ERC | 0.74 | -27.5% | 8.39% | 9.0% | 2.4% |
| OOS start 2000-01 | Uncond. ERC | 0.73 | -27.7% | 8.23% | 8.8% | 1.4% |
| OOS start 2000-01 | Oracle Tilt | 0.76 | -30.3% | 9.20% | 9.7% | 6.1% |
| OOS start 2000-01 | 60/40 | 0.57 | -28.8% | 7.03% | 9.4% | 1.0% |
| OOS start 2000-01 | Static 1/3 | 0.89 | -15.8% | 8.22% | 7.0% | 1.1% |
| Sample 1982-, OOS 2000-01 | Regime Tilt | 0.70 | -28.9% | 8.47% | 9.6% | 4.9% |
| Sample 1982-, OOS 2000-01 | Uncond. Tilt | 0.63 | -28.1% | 7.35% | 9.0% | 0.7% |
| Sample 1982-, OOS 2000-01 | Regime ERC | 0.77 | -27.3% | 8.55% | 8.7% | 2.2% |
| Sample 1982-, OOS 2000-01 | Uncond. ERC | 0.76 | -26.5% | 8.39% | 8.6% | 1.4% |
| Sample 1982-, OOS 2000-01 | Oracle Tilt | 0.73 | -28.7% | 8.75% | 9.5% | 4.7% |
| Sample 1982-, OOS 2000-01 | 60/40 | 0.57 | -28.8% | 7.03% | 9.4% | 1.0% |
| Sample 1982-, OOS 2000-01 | Static 1/3 | 0.89 | -15.8% | 8.22% | 7.0% | 1.1% |
| Transaction costs x2 | Regime Tilt | 0.67 | -30.3% | 9.17% | 9.8% | 7.3% |
| Transaction costs x2 | Uncond. Tilt | 0.64 | -31.3% | 8.90% | 10.0% | 0.6% |
| Transaction costs x2 | Regime ERC | 0.73 | -27.5% | 9.16% | 8.9% | 2.4% |
| Transaction costs x2 | Uncond. ERC | 0.73 | -27.7% | 9.06% | 8.8% | 1.4% |
| Transaction costs x2 | Oracle Tilt | 0.71 | -30.4% | 9.55% | 9.7% | 5.9% |
| Transaction costs x2 | 60/40 | 0.67 | -28.8% | 8.89% | 9.4% | 0.9% |
| Transaction costs x2 | Static 1/3 | 0.76 | -15.8% | 7.98% | 6.9% | 1.1% |
| Oct-2025 gap not interpolated | Regime Tilt | 0.70 | -30.2% | 9.44% | 9.8% | 7.1% |
| Oct-2025 gap not interpolated | Uncond. Tilt | 0.64 | -31.3% | 8.92% | 10.0% | 0.6% |
| Oct-2025 gap not interpolated | Regime ERC | 0.74 | -27.5% | 9.24% | 8.9% | 2.4% |
| Oct-2025 gap not interpolated | Uncond. ERC | 0.73 | -27.7% | 9.09% | 8.8% | 1.4% |
| Oct-2025 gap not interpolated | Oracle Tilt | 0.73 | -30.3% | 9.71% | 9.7% | 5.7% |
| Oct-2025 gap not interpolated | 60/40 | 0.67 | -28.8% | 8.91% | 9.4% | 0.9% |
| Oct-2025 gap not interpolated | Static 1/3 | 0.77 | -15.8% | 8.01% | 6.9% | 1.1% |
| All assets on monthly-average prices | Regime Tilt | 0.81 | -30.3% | 9.52% | 8.3% | 6.7% |
| All assets on monthly-average prices | Uncond. Tilt | 0.74 | -30.8% | 8.95% | 8.4% | 0.5% |
| All assets on monthly-average prices | Regime ERC | 0.82 | -27.8% | 9.12% | 7.8% | 2.2% |
| All assets on monthly-average prices | Uncond. ERC | 0.81 | -28.1% | 8.99% | 7.7% | 1.1% |
| All assets on monthly-average prices | Oracle Tilt | 0.92 | -28.5% | 10.14% | 7.9% | 6.0% |
| All assets on monthly-average prices | 60/40 | 0.79 | -26.4% | 8.86% | 7.8% | 0.8% |
| All assets on monthly-average prices | Static 1/3 | 0.83 | -17.2% | 7.94% | 6.2% | 1.0% |

## Block-bootstrap tests (stationary bootstrap, mean block 12 months, 5,000 resamples)

Max-drawdown difference > 0 means Regime Tilt's drawdown was shallower.

| run | test | diff | 95% CI | p-value |
|---|---|---|---|---|
| Main (default settings) | Regime Tilt - Uncond. Tilt: Sharpe ratio | +0.05 | [-0.06, +0.16] | 0.356 |
| Main (default settings) | Regime Tilt - Uncond. Tilt: Max drawdown | +1.1% | [-4.0%, +4.3%] | 0.456 |
| Main (default settings) | Regime Tilt - 60/40: Sharpe ratio | +0.02 | [-0.15, +0.20] | 0.828 |
| Main (default settings) | Regime Tilt - 60/40: Max drawdown | -1.4% | [-9.2%, +7.2%] | 0.602 |
| 17 industries | Regime Tilt - Uncond. Tilt: Sharpe ratio | +0.01 | [-0.09, +0.12] | 0.803 |
| 17 industries | Regime Tilt - Uncond. Tilt: Max drawdown | -2.4% | [-6.0%, +1.9%] | 0.152 |
| 17 industries | Regime Tilt - 60/40: Sharpe ratio | +0.01 | [-0.18, +0.21] | 0.930 |
| 17 industries | Regime Tilt - 60/40: Max drawdown | -6.0% | [-11.7%, +6.6%] | 0.257 |
| Regime confirmation 2 months | Regime Tilt - Uncond. Tilt: Sharpe ratio | +0.09 | [+0.01, +0.16] | 0.023 |
| Regime confirmation 2 months | Regime Tilt - Uncond. Tilt: Max drawdown | +4.2% | [-2.4%, +6.6%] | 0.236 |
| Regime confirmation 2 months | Regime Tilt - 60/40: Sharpe ratio | +0.05 | [-0.09, +0.21] | 0.474 |
| Regime confirmation 2 months | Regime Tilt - 60/40: Max drawdown | +1.7% | [-7.6%, +7.5%] | 0.581 |
| OOS start 2000-01 | Regime Tilt - Uncond. Tilt: Sharpe ratio | +0.14 | [+0.02, +0.26] | 0.025 |
| OOS start 2000-01 | Regime Tilt - Uncond. Tilt: Max drawdown | +1.1% | [-3.3%, +5.4%] | 0.455 |
| OOS start 2000-01 | Regime Tilt - 60/40: Sharpe ratio | +0.15 | [-0.05, +0.34] | 0.127 |
| OOS start 2000-01 | Regime Tilt - 60/40: Max drawdown | -1.4% | [-9.0%, +7.7%] | 0.615 |
| Sample 1982-, OOS 2000-01 | Regime Tilt - Uncond. Tilt: Sharpe ratio | +0.07 | [-0.00, +0.13] | 0.043 |
| Sample 1982-, OOS 2000-01 | Regime Tilt - Uncond. Tilt: Max drawdown | -0.9% | [-3.4%, +1.4%] | 0.338 |
| Sample 1982-, OOS 2000-01 | Regime Tilt - 60/40: Sharpe ratio | +0.13 | [-0.01, +0.25] | 0.055 |
| Sample 1982-, OOS 2000-01 | Regime Tilt - 60/40: Max drawdown | -0.1% | [-4.1%, +8.3%] | 0.837 |
| Transaction costs x2 | Regime Tilt - Uncond. Tilt: Sharpe ratio | +0.03 | [-0.08, +0.15] | 0.533 |
| Transaction costs x2 | Regime Tilt - Uncond. Tilt: Max drawdown | +1.1% | [-4.3%, +4.2%] | 0.473 |
| Transaction costs x2 | Regime Tilt - 60/40: Sharpe ratio | +0.00 | [-0.17, +0.18] | 0.968 |
| Transaction costs x2 | Regime Tilt - 60/40: Max drawdown | -1.4% | [-9.5%, +7.1%] | 0.600 |
| Oct-2025 gap not interpolated | Regime Tilt - Uncond. Tilt: Sharpe ratio | +0.06 | [-0.05, +0.17] | 0.286 |
| Oct-2025 gap not interpolated | Regime Tilt - Uncond. Tilt: Max drawdown | +1.1% | [-3.5%, +4.4%] | 0.440 |
| Oct-2025 gap not interpolated | Regime Tilt - 60/40: Sharpe ratio | +0.03 | [-0.15, +0.21] | 0.757 |
| Oct-2025 gap not interpolated | Regime Tilt - 60/40: Max drawdown | -1.4% | [-8.9%, +7.2%] | 0.596 |
| All assets on monthly-average prices | Regime Tilt - Uncond. Tilt: Sharpe ratio | +0.07 | [-0.04, +0.18] | 0.195 |
| All assets on monthly-average prices | Regime Tilt - Uncond. Tilt: Max drawdown | +0.5% | [-3.1%, +3.6%] | 0.547 |
| All assets on monthly-average prices | Regime Tilt - 60/40: Sharpe ratio | +0.03 | [-0.15, +0.23] | 0.789 |
| All assets on monthly-average prices | Regime Tilt - 60/40: Max drawdown | -4.0% | [-10.2%, +8.6%] | 0.291 |
