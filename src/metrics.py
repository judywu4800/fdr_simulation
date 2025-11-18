import numpy as np


def compute_fdr(rejections, truth):
    R = np.sum(rejections)
    if R == 0:
        return 0.0
    V = np.sum(rejections & truth)  # rejected AND null = false positives
    return V / R


def compute_power(rejections, truth):
    m1 = np.sum(~truth)
    if m1 == 0:
        return 0.0
    S = np.sum(rejections & ~truth)  # rejected AND non-null = true positives
    return S / m1


def summarize_metrics(results):
    fdr_vals = [r["fdr"] for r in results]
    power_vals = [r["power"] for r in results]
    return {
        "mean_fdr": np.mean(fdr_vals),
        "mean_power": np.mean(power_vals),
        "sd_fdr": np.std(fdr_vals),
        "sd_power": np.std(power_vals),
    }

# optimization
def compute_fdp_power(rej, null_mask):
    R = rej.sum(axis=1)
    V = rej[:, null_mask].sum(axis=1)
    FDP = np.where(R>0, V/R, 0.0)
    m1 = (~null_mask).sum()
    if m1 == 0:
        return FDP.mean(), 0.0

    TP = rej[:, ~null_mask].sum(axis=1)
    power = TP / m1
    return FDP.mean(), power.mean()


if __name__ == "__main__":
    np.random.seed(123)
    truth = np.array([True, True, False, False, False])  # first two are true nulls
    rejections = np.array([False, True, True, True, False])

    fdr = compute_fdr(rejections, truth)
    power = compute_power(rejections, truth)
    print(f"FDR: {fdr:.3f}, Power: {power:.3f}")