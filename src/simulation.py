"""
simulation.py
--------------
Reproduce Setting (1) from Benjamini & Hochberg (1995) — linearly decreasing means.

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


# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------
N_REPS = 20000       # number of replications per (m, pi0)
ALPHA = 0.05
M_VALUES = [4, 8, 16, 32, 64]
PI0_VALUES = [0.75, 0.5, 0.25, 0.0]
L = 8.0
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
                pvals, truth = generate_pvalues(m=m, pi0=pi0, L=L, pattern="decreasing")
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


# ---------------------------------------------------------------------
# PLOTTING
# ---------------------------------------------------------------------
def plot_power_vs_m(df):
    """
    Plot power vs m for each pi0 level (each as one subplot),
    showing three methods in each panel, matching Figure 1 layout.
    """
    import matplotlib.pyplot as plt

    pi0_levels = sorted(df["pi0"].unique(), reverse=True)
    methods = ["bonferroni", "hochberg", "bh"]
    colors = {"bonferroni": "black", "hochberg": "gray", "bh": "red"}
    linestyles = {"bonferroni": ":", "hochberg": "--", "bh": "-"}

    n_rows = len(pi0_levels)
    fig, axes = plt.subplots(
        n_rows, 1, figsize=(6, 2.2 * n_rows), sharex=True, sharey=True
    )

    if n_rows == 1:
        axes = [axes]

    for i, pi0 in enumerate(pi0_levels):
        ax = axes[i]
        subset = df[df["pi0"] == pi0]

        for method in methods:
            d = subset[subset["method"] == method]
            ax.plot(
                d["m"],
                d["mean_power"],
                marker="o",
                color=colors[method],
                linestyle=linestyles[method],
                label=method.capitalize(),
            )

        ax.set_xscale("log", base=2)
        ax.set_xticks([4, 8, 16, 32, 64])
        ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

        ax.set_ylim(0.2, 1.0)
        ax.set_title(f"{int(pi0 * 100)}% Null", fontsize=10)
        ax.set_ylabel("Average Power")
        ax.grid(alpha=0.3, linestyle="--")

        if i == n_rows - 1:
            ax.set_xlabel("Number of Tested Hypotheses (m)")

        if i == 0:
            ax.legend(
                loc="upper right",
                frameon=False,
                fontsize=8,
                title="Method",
                title_fontsize=9,
            )

    plt.suptitle("Setting 1: Decreasing means (L=10)", fontsize=12, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    path = os.path.join(FIG_DIR, "power_vs_m_grid.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    print(f"Saved figure to {path}")


if __name__ == "__main__":
    np.random.seed(0)
    df_summary = run_simulation()
    plot_power_vs_m(df_summary)
