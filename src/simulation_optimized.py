import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import time
from src.dgps import generate_pvalues, generate_pvalues_matrix
from src.methods import apply_method, compute_rejections
from src.metrics import compute_fdr, compute_power, summarize_metrics, compute_fdp_power
from src.visualization import plot_power_vs_m
from joblib import Parallel, delayed
from src.simulation import *


if __name__ == "__main__":
    np.random.seed(0)
    #df_summary = run_simulation()
    #plot_power_vs_m(df_summary)
    M_list = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
    pi0_list = [0.75, 0.5, 0.25, 0.0]
    df, df_timing = run_simulation_optimized_parallel(M_list, pi0_list, 10000, 0.05, 10.0, save_profiling=False)
    df_long = pd.DataFrame({
        "m": [],
        "pi0": [],
        "method": [],
        "mean_fdr": [],
        "mean_power": []
    })

    rows = []
    for _, row in df.iterrows():
        rows.append({"m": row["M"], "pi0": row["pi0"], "method": "bonferroni",
                     "mean_fdr": row["FDP_Bonf"], "mean_power": row["Power_Bonf"]})
        rows.append({"m": row["M"], "pi0": row["pi0"], "method": "hochberg",
                     "mean_fdr": row["FDP_Hoch"], "mean_power": row["Power_Hoch"]})
        rows.append({"m": row["M"], "pi0": row["pi0"], "method": "bh",
                     "mean_fdr": row["FDP_BH"], "mean_power": row["Power_BH"]})

    df_long = pd.DataFrame(rows)
    plot_power_vs_m(df_long, name = "power_vs_m_grid_optimized.png")


