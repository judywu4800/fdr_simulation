import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_DIR = os.path.join(BASE_DIR, "results", "raw")
    FIG_DIR = os.path.join(BASE_DIR, "results", "figures")
    os.makedirs(FIG_DIR, exist_ok=True)

    N_REPS = 10000

    df = pd.read_csv(os.path.join(RAW_DIR, "timing_summary.csv"))

    methods_to_plot = ["hochberg", "bh","bonferroni"]
    colors = {"hochberg": None, "bh": None, "bonferroni": None}

    plt.figure()

    for method in methods_to_plot:
        sub = df[(df.component == "method") & (df.method == method)]
        grp = sub.groupby("m")["time_sec"].mean()
        avg_rep_time = grp / N_REPS
        m_values = grp.index.values

        plt.loglog(m_values, avg_rep_time, marker="o", label=method)

        logs_m = np.log(m_values)
        logs_t = np.log(avg_rep_time.values)
        slope, intercept = np.polyfit(logs_m, logs_t, 1)
        print(f"{method} slope ≈ {slope:.3f}")

    plt.xlabel("m (log scale)")
    plt.ylabel("Avg method time per replication (log scale)")
    plt.title("Empirical Complexity of Hochberg & BH")
    plt.legend()
    out_path = os.path.join(FIG_DIR, "complexity_loglog_methods.png")
    plt.savefig(out_path)
    print("Saved:", out_path)
