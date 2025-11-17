
import numpy as np
from typing import Tuple, Optional
from scipy.stats import norm

def generate_pvalues(m, pi0, L = 10.0, pattern = "equal", random_state = None):
    """
    Generate one replication of Z-statistics and p-values under a specified configuration.

    Parameters
    ----------
    m : int
        Total number of hypotheses (e.g. 4, 8, 16, 32, 64).
    pi0 : float
        Proportion of true null hypotheses (0.0, 0.25, 0.5, 0.75).
    L : float, default = 10
        Signal strength; paper used L = 5 and 10, shows L = 10 for illustration.
    random_state : int | None
        Optional RNG seed for reproducibility.

    Returns
    -------
    pvals : ndarray of shape (m,)
        One-sided p-values = 1 − \Phi(Z_i).
    truth : ndarray of bool, shape (m,)
        True-null indicator; True = null hypothesis is true.
    """
    rng = np.random.default_rng(random_state)

    m0 = int(round(pi0 * m))
    m1 = m - m0

    mu = np.zeros(m)
    if m1 > 0:
        if pattern.lower() != "equal":
            raise NotImplementedError("Only 'equal' pattern implemented (Setting 1).")

        # false nulls divided into four equal groups
        group_sizes = np.full(4, m1 // 4)
        remainder = m1 % 4
        group_sizes[:remainder] += 1  # handle uneven split

        effect_levels = np.array([L, 3 * L / 4, L / 2, L / 4])
        mu_nonnull = np.repeat(effect_levels, group_sizes)

        mu[m0:] = mu_nonnull[: m1]

    Z = rng.normal(loc=mu, scale=1.0, size=m)
    pvals = 2 * (1 - norm.cdf(np.abs(Z)))
    truth = np.zeros(m, dtype=bool)
    truth[:m0] = True

    return pvals, truth


if __name__ == "__main__":
    p, t = generate_pvalues(m=16, pi0=0.5, L=10, pattern="decreasing", random_state=123)
    print("Example p-values:", np.round(p, 4))
    print("True null flags:", t)