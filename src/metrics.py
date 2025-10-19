import numpy as np


def compute_fdr(rejections: np.ndarray, truth: np.ndarray) -> float:
    """
    Compute empirical FDR for one simulation run.

    Parameters
    ----------
    rejections : ndarray of bool
        True for rejected hypotheses.
    truth : ndarray of bool
        True for true null hypotheses.

    Returns
    -------
    fdr : float
        False discovery proportion (V / max(R, 1)).
    """
    R = np.sum(rejections)
    if R == 0:
        return 0.0
    V = np.sum(rejections & truth)  # rejected AND null = false positives
    return V / R


def compute_power(rejections: np.ndarray, truth: np.ndarray) -> float:
    """
    Compute empirical power for one simulation run.

    Parameters
    ----------
    rejections : ndarray of bool
        True for rejected hypotheses.
    truth : ndarray of bool
        True for true null hypotheses.

    Returns
    -------
    power : float
        True positive rate (S / m1), averaged over non-nulls.
    """
    m1 = np.sum(~truth)
    if m1 == 0:
        return 0.0
    S = np.sum(rejections & ~truth)  # rejected AND non-null = true positives
    return S / m1


def summarize_metrics(results: list[dict]) -> dict:
    """
    Aggregate results across replications.

    Parameters
    ----------
    results : list of dict
        Each element contains keys {"fdr", "power"} from individual runs.

    Returns
    -------
    summary : dict
        Average FDR and power across all replications.
    """
    fdr_vals = [r["fdr"] for r in results]
    power_vals = [r["power"] for r in results]
    return {
        "mean_fdr": np.mean(fdr_vals),
        "mean_power": np.mean(power_vals),
        "sd_fdr": np.std(fdr_vals),
        "sd_power": np.std(power_vals),
    }


if __name__ == "__main__":
    # quick test
    np.random.seed(123)
    truth = np.array([True, True, False, False, False])  # first two are true nulls
    rejections = np.array([False, True, True, True, False])

    fdr = compute_fdr(rejections, truth)
    power = compute_power(rejections, truth)
    print(f"FDR: {fdr:.3f}, Power: {power:.3f}")