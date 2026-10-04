"""Central settings for the regime-aware bonds / gold / equity-sector study."""
from dataclasses import dataclass, field


@dataclass
class Config:
    # Sample: gold floats freely after Bretton Woods ends (Aug 1971), so returns start Jan 1972.
    sample_start: str = "1972-01"
    # First out-of-sample month. Everything before is the initial training window
    # (1972-1989 contains the 1970s stagflation and the Volcker disinflation).
    oos_start: str = "1990-01"
    # Ken French industry set: 12 (closest to GICS sectors) or 17 (splits oil, mines, steel).
    industries: int = 12

    # Regime signals
    corr_window_days: int = 63          # rolling daily stock-bond correlation (~3 months)
    zscore_min_periods: int = 24        # expanding z-score warm-up (months)
    confirm_months: int = 1             # >1: switch regime only after k consecutive signals

    # Estimation
    cov_shrink_k: int = 36              # regime cov weight = n_r / (n_r + k)
    mean_shrink_k: int = 60             # regime mean weight = n_r / (n_r + k)
    min_regime_obs: int = 24            # below this, fall back to unconditional estimates

    # Allocation
    tilt_strength: float = 0.5          # lambda in exp(lambda * standardized score)
    tilt_clip: tuple = (0.25, 3.0)      # bounds on the tilt multiplier
    max_weight: float = 0.35            # per-asset cap (long-only, fully invested, no cash)

    # One-way transaction costs in basis points per unit of turnover
    cost_bps: dict = field(default_factory=lambda: {"equity": 10.0, "UST10": 5.0, "GOLD": 15.0})

    # Out-of-sample sub-periods for robustness
    robustness_starts: tuple = ("1990-01", "2000-01", "2010-01", "2020-01")

    # Stress episodes (inclusive months). Pre-1990 ones are used for descriptive asset tables only.
    episodes: dict = field(default_factory=lambda: {
        "1973-74 oil shock / stagflation": ("1973-01", "1974-09"),
        "1980-82 Volcker tightening": ("1980-01", "1982-07"),
        "1987 crash": ("1987-09", "1987-11"),
        "1990 Gulf war recession": ("1990-07", "1990-10"),
        "1998 LTCM": ("1998-07", "1998-09"),
        "2000-02 dot-com bust": ("2000-09", "2002-09"),
        "2007-09 GFC": ("2007-11", "2009-02"),
        "2020 Covid crash": ("2020-02", "2020-03"),
        "2022 inflation shock": ("2022-01", "2022-10"),
        "2025 tariff shock": ("2025-02", "2025-04"),
    })
