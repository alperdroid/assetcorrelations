"""Shared fixtures: synthetic panels (offline) so the timing tests never need the internet."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config import Config  # noqa: E402
from data import build_panels, load_raw  # noqa: E402
from synthetic import write_synthetic  # noqa: E402


@pytest.fixture(scope="session")
def panels(tmp_path_factory):
    raw_dir = tmp_path_factory.mktemp("synthetic") / "raw"
    write_synthetic(raw_dir)
    return build_panels(load_raw(raw_dir, 12, use_gold_override=False))


@pytest.fixture
def cfg():
    # Short out-of-sample window keeps the walk-forward tests fast.
    c = Config()
    c.oos_start = "2024-01"
    return c
