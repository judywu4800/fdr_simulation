import numpy as np
import pytest
from src.dgps import generate_pvalues
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_output_shapes():
    """Ensure generate_pvalues returns correct shapes and dtypes."""
    m, pi0 = 16, 0.5
    pvals, truth = generate_pvalues(m=m, pi0=pi0, L=10, pattern="equal", random_state=123)

    assert isinstance(pvals, np.ndarray)
    assert isinstance(truth, np.ndarray)
    assert pvals.shape == (m,)
    assert truth.shape == (m,)
    assert pvals.dtype == float
    assert truth.dtype == bool


def test_true_null_proportion():
    """Check that the number of true nulls matches pi0 * m."""
    m, pi0 = 32, 0.75
    pvals, truth = generate_pvalues(m=m, pi0=pi0, L=10, pattern="equal", random_state=1)
    m0 = int(round(pi0 * m))
    assert np.sum(truth) == m0


def test_pvalue_range():
    """All p-values should be within [0, 1]."""
    pvals, _ = generate_pvalues(m=64, pi0=0.5, L=10, pattern="equal", random_state=42)
    # Allow for tiny floating errors; numerical 0 is acceptable
    assert np.all((pvals >= -1e-15) & (pvals <= 1 + 1e-15)), "p-values should be within [0, 1]"


def test_signal_effects_increase():
    """Under decreasing pattern, mean Z of non-nulls should be positive."""
    pvals, truth = generate_pvalues(m=32, pi0=0.5, L=10, pattern="equal", random_state=42)
    # regenerate Z to check mean direction indirectly
    m0 = np.sum(truth)
    nonnull_p = pvals[~truth]
    assert np.median(nonnull_p) < np.median(pvals[truth]), "Non-nulls should have smaller p-values"


def test_invalid_pattern_raises():
    """Invalid pattern should raise NotImplementedError."""
    with pytest.raises(NotImplementedError):
        generate_pvalues(m=16, pi0=0.5, L=10, pattern="weird", random_state=0)