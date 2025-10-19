import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def plot_power_vs_m(df):
    """
    Plot power vs m for each pi0 level (each as one subplot),
    arranged horizontally (4 columns), matching BH (1995) Figure 1 style.
    """
    import os
    import matplotlib.pyplot as plt

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FIG_DIR = os.path.join(BASE_DIR, "results", "figures")
    os.makedirs(FIG_DIR, exist_ok=True)

    pi0_levels = sorted(df["pi0"].unique())  # left-to-right increasing
    methods = ["bonferroni", "hochberg", "bh"]
    colors = {"bonferroni": "black", "hochberg": "gray", "bh": "red"}
    linestyles = {"bonferroni": ":", "hochberg": "--", "bh": "-"}

    n_cols = len(pi0_levels)
    fig, axes = plt.subplots(
        1, n_cols, figsize=(2.0 * n_cols + 2, 3), sharey=True, sharex=True
    )

    if n_cols == 1:
        axes = [axes]

    for j, pi0 in enumerate(pi0_levels):
        ax = axes[j]
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

        ax.set_ylim(0.6, 1.0)
        ax.set_title(f"{int(pi0 * 100)}% Null", fontsize=10)
        if j == 0:
            ax.set_ylabel("Average Power")
        ax.grid(alpha=0.3, linestyle="--")

        if j == n_cols - 1:
            ax.legend(
                loc="lower right",
                frameon=False,
                fontsize=8,
                title="Method",
                title_fontsize=9,
            )

    fig.supxlabel("Number of Tested Hypotheses (m)", fontsize=10)
    fig.supylabel("Average Power", fontsize=10, x=0.04)
    plt.suptitle("Setting 1: Equal number per group (L=10)", fontsize=12, y=1.05)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    path = os.path.join(FIG_DIR, "power_vs_m_grid.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    print(f"Saved figure to {path}")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "results", "raw")
FIG_DIR = os.path.join(BASE_DIR, "results", "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def plot_diagnostic(df):
    """Create diagnostic boxplots of FDR and Power."""
    sns.set(style="whitegrid", font_scale=1.0)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=False)

    sns.boxplot(
        data=df, x="method", y="mean_fdr", hue="pi0",
        ax=axes[0], palette="Set2"
    )
    axes[0].axhline(0.05, color="red", linestyle="--", alpha=0.6)
    axes[0].set_title("Distribution of FDR across methods")
    axes[0].set_xlabel("Method")
    axes[0].set_ylabel("Empirical FDR")

    sns.boxplot(
        data=df, x="method", y="mean_power", hue="pi0",
        ax=axes[1], palette="Set1"
    )
    axes[1].set_title("Distribution of Power across methods")
    axes[1].set_xlabel("Method")
    axes[1].set_ylabel("Empirical Power")

    plt.tight_layout()
    path = os.path.join(FIG_DIR, "diagnostic_boxplots.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    print(f"Saved diagnostic plot to {path}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_DIR = os.path.join(BASE_DIR, "results", "raw")
    path_csv = os.path.join(RAW_DIR, "sim_summary.csv")

    if not os.path.exists(path_csv):
        raise FileNotFoundError(
            f"Cannot find simulation summary at {path_csv}. "
            "Run `make simulate` first."
        )

    df = pd.read_csv(path_csv)
    plot_power_vs_m(df)
    plot_diagnostic(df)