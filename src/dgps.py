
import numpy as np
from typing import Tuple, Optional
from scipy.stats import norm

def generate_pvalues(
    m: int,
    pi0: float,
    L: float = 10.0,
    pattern: str = "equal",
    random_state: Optional[int] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate one replication of Z-statistics and p-values under a specified configuration.

    Parameters
    ----------
    m : int
        Total number of hypotheses (e.g. 4, 8, 16, 32, 64).
    pi0 : float
        Proportion of true null hypotheses (0.0, 0.25, 0.5, 0.75).
    L : float, default = 10
        Signal strength; paper used L = 5 and 10 but Fig. 1 shows L = 10.
    random_state : int | None
        Optional RNG seed for reproducibility.

    Returns
    -------
    pvals : ndarray of shape (m,)
        One-sided p-values = 1 − Φ(Z_i).
    truth : ndarray of bool, shape (m,)
        True-null indicator; True = null hypothesis is true.
    """
    rng = np.random.default_rng(random_state)

    # 1. number of true and false nulls
    m0 = int(round(pi0 * m))
    m1 = m - m0

    # 2. assign means μ_i
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

        # fill μ for false nulls; remaining m0 are true nulls (μ = 0)
        mu[m0:] = mu_nonnull[: m1]

    # 3. simulate test statistics and p-values
    Z = rng.normal(loc=mu, scale=1.0, size=m)
    pvals = 2 * (1 - norm.cdf(np.abs(Z)))
    truth = np.zeros(m, dtype=bool)
    truth[:m0] = True  # first m0 are true nulls

    return pvals, truth


if __name__ == "__main__":
    # quick sanity check
    p, t = generate_pvalues(m=16, pi0=0.5, L=10, pattern="decreasing", random_state=123)
    print("Example p-values:", np.round(p, 4))
    print("True null flags:", t)