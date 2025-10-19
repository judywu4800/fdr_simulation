"""
simulation.py
--------------
Reproduce Setting (b) from Benjamini & Hochberg (1995).

For each combination of (m, pi0), repeat simulations, apply
Bonferroni, Hochberg, and BH procedures, compute empirical FDR & Power.

Outputs:
    - results/raw/sim_summary.csv : summarized metrics
    - results/figures/power_vs_m.png : BH-style figure
"""

import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

from src.dgps import generate_pvalues
from src.methods import apply_method
from src.metrics import compute_fdr, compute_power, summarize_metrics
from src.visualization import plot_power_vs_m


# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------
N_REPS = 5000       # number of replications per (m, pi0)
ALPHA = 0.05
M_VALUES = [4, 8, 16, 32, 64]
PI0_VALUES = [0.75, 0.5, 0.25, 0.0]
L = 10.0
METHODS = ["bonferroni", "hochberg", "bh"]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "results", "raw")
FIG_DIR = os.path.join(BASE_DIR, "results", "figures")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)


# ---------------------------------------------------------------------
# MAIN SIMULATION
# ---------------------------------------------------------------------
def run_simulation():
    records = []

    for pi0 in PI0_VALUES:
        for m in M_VALUES:
            desc = f"pi0={pi0:.2f}, m={m}"
            sim_results = {method: [] for method in METHODS}

            for _ in tqdm(range(N_REPS), desc=desc):
                pvals, truth = generate_pvalues(m=m, pi0=pi0, L=L, pattern="equal")
                for method in METHODS:
                    rejects = apply_method(pvals, ALPHA, method)
                    fdr = compute_fdr(rejects, truth)
                    power = compute_power(rejects, truth)
                    sim_results[method].append({"fdr": fdr, "power": power})

            # aggregate across replications
            for method in METHODS:
                summary = summarize_metrics(sim_results[method])
                records.append({
                    "pi0": pi0,
                    "m": m,
                    "method": method,
                    **summary
                })

    df = pd.DataFrame(records)
    df.to_csv(os.path.join(RAW_DIR, "sim_summary.csv"), index=False)
    print(f"\nSaved summary to {RAW_DIR}/sim_summary.csv")
    return df




if __name__ == "__main__":
    np.random.seed(0)
    df_summary = run_simulation()
    plot_power_vs_m(df_summary)
