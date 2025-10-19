"""
Unit tests for src/methods.py
Verify correctness of Bonferroni, Hochberg, and Benjamini–Hochberg procedures.
Run with: pytest -v
"""

import numpy as np
import pytest
from src.methods import bonferroni, hochberg, benjamini_hochberg, apply_method


# ---------------------------------------------------------------------
# Utility data
# ---------------------------------------------------------------------
@pytest.fixture
def simple_pvals():
    """A simple, reproducible set of p-values."""
    return np.array([0.001, 0.01, 0.02, 0.04, 0.2, 0.6, 0.8])


ALPHA = 0.05


# ---------------------------------------------------------------------
# 1. Bonferroni
# ---------------------------------------------------------------------
def test_bonferroni_threshold(simple_pvals):
    """Bonferroni rejects only those <= alpha/m."""
    m = len(simple_pvals)
    cutoff = ALPHA / m
    expected = simple_pvals <= cutoff
    got = bonferroni(simple_pvals, ALPHA)
    np.testing.assert_array_equal(got, expected)


def test_bonferroni_no_false_rejects(simple_pvals):
    """Bonferroni should never reject p > alpha/m."""
    rejects = bonferroni(simple_pvals, ALPHA)
    assert np.all(simple_pvals[~rejects] > ALPHA / len(simple_pvals))


# ---------------------------------------------------------------------
# 2. Hochberg
# ---------------------------------------------------------------------
def test_hochberg_monotonic(simple_pvals):
    """Hochberg step-up is always at least as powerful as Bonferroni."""
    rej_bonf = bonferroni(simple_pvals, ALPHA)
    rej_hoch = hochberg(simple_pvals, ALPHA)
    # Hochberg never rejects fewer hypotheses than Bonferroni
    assert np.sum(rej_hoch) >= np.sum(rej_bonf)


def test_hochberg_correct_behavior():
    """Check Hochberg with a known example."""
    pvals = np.array([0.01, 0.03, 0.04, 0.35])
    expected = np.array([True, True, True, False])  # Hochberg FWER result
    got = hochberg(pvals, 0.05)
    np.testing.assert_array_equal(got, expected)


# ---------------------------------------------------------------------
# 3. Benjamini–Hochberg (BH)
# ---------------------------------------------------------------------
def test_bh_known_case():
    """Check BH procedure on a known example (Wikipedia BH example)."""
    pvals = np.array([0.001, 0.004, 0.008, 0.04, 0.05, 0.2])
    alpha = 0.05
    # sorted: [0.001,0.004,0.008,0.04,0.05,0.2]
    # thresholds: [0.0083,0.0167,0.025,0.0333,0.0417,0.05]
    # largest k where p(k) <= threshold: k=3 (0.008 <= 0.025)
    expected = pvals <= 0.008
    got = benjamini_hochberg(pvals, alpha)
    np.testing.assert_array_equal(got, expected)


def test_bh_monotonic(simple_pvals):
    """BH should reject at least as many as Bonferroni."""
    rej_bonf = bonferroni(simple_pvals, ALPHA)
    rej_bh = benjamini_hochberg(simple_pvals, ALPHA)
    assert np.sum(rej_bh) >= np.sum(rej_bonf)


# ---------------------------------------------------------------------
# 4. Unified interface
# ---------------------------------------------------------------------
def test_apply_method_dispatch(simple_pvals):
    """apply_method should call the correct function."""
    res1 = apply_method(simple_pvals, ALPHA, "bonferroni")
    res2 = bonferroni(simple_pvals, ALPHA)
    np.testing.assert_array_equal(res1, res2)

    res3 = apply_method(simple_pvals, ALPHA, "hochberg")
    np.testing.assert_array_equal(res3, hochberg(simple_pvals, ALPHA))

    res4 = apply_method(simple_pvals, ALPHA, "bh")
    np.testing.assert_array_equal(res4, benjamini_hochberg(simple_pvals, ALPHA))


def test_apply_method_invalid(simple_pvals):
    """Unknown method name should raise ValueError."""
    with pytest.raises(ValueError):
        apply_method(simple_pvals, ALPHA, "random")
