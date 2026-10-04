#!/usr/bin/env bash
# Phase 5-7: every run, each into its own folder, then the consolidated robustness table.
# Requires network access to fred.stlouisfed.org (and api.statistiken.bundesbank.de for month-end gold).
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-python}

# Month-end gold from the Bundesbank; if this fails, the runs fall back to World Bank averages.
$PY fetch_gold_bundesbank.py || echo "Bundesbank gold not available - using World Bank monthly averages"

$PY validate_data.py
$PY run_study.py --out results_main
if [ -f data/gold_override.csv ]; then
  $PY run_study.py --gold-avg --out results_gold_avg
fi
$PY run_study.py --industries 17 --out results_ind17
$PY run_study.py --confirm 2 --out results_confirm2
$PY run_study.py --oos-start 2000-01 --out results_oos2000
$PY run_study.py --sample-start 1982-01 --oos-start 2000-01 --out results_start1982
$PY run_study.py --cost-mult 2 --out results_costx2
$PY summarize_runs.py
