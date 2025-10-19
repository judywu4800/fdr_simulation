import numpy as np


# ---------------------------------------------------------------------
# 1. Bonferroni correction
# ---------------------------------------------------------------------
def bonferroni(pvals: np.ndarray, alpha: float = 0.05) -> np.ndarray:
    """
    Bonferroni correction: reject if p_i <= alpha / m
    """
    m = len(pvals)
    cutoff = alpha / m
    return pvals <= cutoff


# ---------------------------------------------------------------------
# 2. Hochberg (1988) step-up procedure for FWER control
# ---------------------------------------------------------------------
def hochberg(pvals: np.ndarray, alpha: float = 0.05) -> np.ndarray:
    """
    Hochberg step-up method controlling FWER.

    Procedure:
      1. Sort p-values in descending order: p_(m) >= ... >= p_(1)
      2. Find the smallest k such that p_(m−k+1) <= α / k
      3. Reject all hypotheses with p_i <= α / k
    """
    m = len(pvals)
    sorted_idx = np.argsort(pvals)[::-1]  # descending
    sorted_p = pvals[sorted_idx]

    reject = np.zeros(m, dtype=bool)
    for k in range(m, 0, -1):
        threshold = alpha / k
        if sorted_p[m - k] <= threshold:
            reject[pvals <= threshold] = True
            break

    return reject


# ---------------------------------------------------------------------
# 3. Benjamini–Hochberg (1995) step-up FDR control
# ---------------------------------------------------------------------
def benjamini_hochberg(pvals: np.ndarray, alpha: float = 0.05) -> np.ndarray:
    """
    Benjamini–Hochberg FDR-controlling procedure.

    Procedure:
      1. Sort p-values ascending: p_(1) <= ... <= p_(m)
      2. Find largest k such that p_(k) <= (k/m) * alpha
      3. Reject all hypotheses with p_i <= p_(k)
    """
    m = len(pvals)
    order = np.argsort(pvals)
    sorted_p = pvals[order]

    thresholds = (np.arange(1, m + 1) / m) * alpha
    below = sorted_p <= thresholds

    reject = np.zeros(m, dtype=bool)
    if np.any(below):
        k = np.max(np.where(below)[0])
        cutoff = sorted_p[k]
        reject = pvals <= cutoff
    return reject


# ---------------------------------------------------------------------
# Optional unified interface
# ---------------------------------------------------------------------
def apply_method(pvals: np.ndarray, alpha: float, method: str) -> np.ndarray:
    """
    Apply one of the multiple-testing procedures.

    method ∈ {"bonferroni", "hochberg", "bh"}
    """
    method = method.lower()
    if method == "bonferroni":
        return bonferroni(pvals, alpha)
    elif method == "hochberg":
        return hochberg(pvals, alpha)
    elif method in {"bh", "benjamini-hochberg"}:
        return benjamini_hochberg(pvals, alpha)
    else:
        raise ValueError(f"Unknown method '{method}'")

if __name__ == "__main__":
    np.random.seed(42)
    pvals = np.random.uniform(0, 1, 10)  # 10 random p-values
    alpha = 0.05

    print("P-values:", np.round(pvals, 3))

    print("\nBonferroni rejects:")
    print(bonferroni(pvals, alpha))

    print("\nHochberg rejects:")
    print(hochberg(pvals, alpha))

    print("\nBenjamini–Hochberg rejects:")
    print(benjamini_hochberg(pvals, alpha))

    print("\nUnified interface (apply_method):")
    for m in ["bonferroni", "hochberg", "bh"]:
        print(f"{m:15s}:", apply_method(pvals, alpha, m))