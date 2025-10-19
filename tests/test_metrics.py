"""
Unit tests for src/metrics.py
Tests FDR, power, and summarization logic.
Run with: pytest -v
"""

import numpy as np
import pytest
from src.metrics import compute_fdr, compute_power, summarize_metrics


# ---------------------------------------------------------------------
# 1. FDR computation
# ---------------------------------------------------------------------
def test_fdr_basic():
    """When no rejections, FDR should be 0."""
    truth = np.array([True, False, False, True])  # True = null
    rejections = np.array([False, False, False, False])
    assert compute_fdr(rejections, truth) == 0.0


def test_fdr_all_false_positives():
    """When all rejections are false positives, FDR = 1."""
    truth = np.array([True, True, False, False])
    rejections = np.array([True, True, False, False])
    assert compute_fdr(rejections, truth) == pytest.approx(1.0)


def test_fdr_mixed_case():
    """Check FDR = V/R when some true and false rejections."""
    truth = np.array([True, False, False, True, False])
    rejections = np.array([True, True, False, True, False])
    # R = 3; V = rejected & true-null = [0,3] = 2 → FDR = 2/3
    expected = 2 / 3
    got = compute_fdr(rejections, truth)
    assert got == pytest.approx(expected)


# ---------------------------------------------------------------------
# 2. Power computation
# ---------------------------------------------------------------------
def test_power_all_correct():
    """When all non-nulls are rejected, power = 1."""
    truth = np.array([True, False, False])
    rejections = np.array([False, True, True])
    assert compute_power(rejections, truth) == 1.0


def test_power_none_rejected():
    """When no non-nulls are rejected, power = 0."""
    truth = np.array([True, False, False])
    rejections = np.array([False, False, False])
    assert compute_power(rejections, truth) == 0.0


def test_power_partial_rejection():
    """Half the non-nulls rejected => power = 0.5."""
    truth = np.array([True, False, False, False])
    rejections = np.array([False, True, False, False])
    assert compute_power(rejections, truth) == pytest.approx(1 / 3, rel=1e-8)


def test_power_when_all_nulls():
    """When m1=0 (no non-nulls), power should be 0."""
    truth = np.array([True, True, True])
    rejections = np.array([True, False, False])
    assert compute_power(rejections, truth) == 0.0


# ---------------------------------------------------------------------
# 3. summarize_metrics
# ---------------------------------------------------------------------
def test_summarize_metrics_mean_and_sd():
    """Check averaging across replications."""
    results = [
        {"fdr": 0.1, "power": 0.9},
        {"fdr": 0.2, "power": 0.8},
        {"fdr": 0.3, "power": 0.7},
    ]
    summary = summarize_metrics(results)

    assert np.isclose(summary["mean_fdr"], 0.2)
    assert np.isclose(summary["mean_power"], 0.8)
    assert "sd_fdr" in summary and "sd_power" in summary
    assert summary["sd_fdr"] > 0 and summary["sd_power"] > 0
