import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.dgps import generate_pvalues
from src.methods import apply_method
from src.metrics import compute_fdr, compute_power
from src.simulation import run_single_block

def run_single_experiment(M, pi0, N_reps, alpha, L, seed):
    rng = np.random.default_rng(seed)

    start = time.perf_counter()

    for _ in range(N_reps):
        # DGP —— baseline: pvals is 1D for each replicate
        pvals, truth = generate_pvalues(
            m=M, pi0=pi0, L=L, pattern="equal", random_state=rng.integers(1e9)
        )

        # baseline method (apply_method = slow per replicate)
        rejects_bonf = apply_method(pvals, alpha, "bonferroni")
        rejects_h = apply_method(pvals, alpha, "hochberg")
        rejects_bh = apply_method(pvals, alpha, "bh")

        # metrics (baseline version)
        fdr_bonf = compute_fdr(rejects_bonf, truth)
        power_bonf = compute_power(rejects_bonf, truth)

        fdr_h = compute_fdr(rejects_h, truth)
        power_h = compute_power(rejects_h, truth)

        fdr_bh = compute_fdr(rejects_bh, truth)
        power_bh = compute_power(rejects_bh, truth)

    end = time.perf_counter()
    return end - start


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FIG_DIR = os.path.join(BASE_DIR, "results", "figures")
    os.makedirs(FIG_DIR, exist_ok=True)

    # ---------------------------------------------------------
    # Settings for the experiment
    # ---------------------------------------------------------
    M = 1024          # hypothesis count
    pi0 = 0.5         # proportion of nulls
    alpha = 0.05
    L = 10.0
    idx_cache = {M: np.arange(1, M + 1) for M in [M]}

    N_list = np.logspace(3, 5, num=8, dtype=int)   # from 1000 to 100000
    runtimes_baseline = []
    runtimes_opt = []

    for i, N in enumerate(N_list):
        print(f"Running N_REPS = {N} ...")

        t_base = run_single_experiment(M, pi0, N, alpha, L, seed=100 + i)
        t0 = time.perf_counter()
        run_single_block(M, pi0, N, alpha, L, seed=200 + i, idx_cache =idx_cache)
        t_opt = time.perf_counter() - t0
        runtimes_baseline.append(t_base)
        runtimes_opt.append(t_opt)

        print(f"   baseline = {t_base:.4f} sec")
        print(f"   optimized = {t_opt:.4f} sec\n")

    runtimes_baseline = np.array(runtimes_baseline)
    runtimes_opt = np.array(runtimes_opt)

    # Total time vs N_REPS (log–log)
    plt.figure(figsize=(6, 5))
    plt.loglog(N_list, runtimes_baseline, marker='o', label="Baseline")
    plt.loglog(N_list, runtimes_opt, marker='s', label="Optimized")
    plt.xlabel("N_REPS (log scale)")
    plt.ylabel("Total runtime (seconds, log scale)")
    plt.title("Total Runtime vs N_REPS (log–log)")
    plt.legend()
    path = os.path.join(FIG_DIR, "runtime_total_vs_N_comparison.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(6, 5))
    plt.loglog(N_list, runtimes_baseline, marker='o', label="Baseline")
    plt.xlabel("N_REPS (log scale)")
    plt.ylabel("Total runtime (seconds, log scale)")
    plt.title("Total Runtime vs N_REPS (log–log)")
    path = os.path.join(FIG_DIR, "runtime_total_vs_N_baseline.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()

