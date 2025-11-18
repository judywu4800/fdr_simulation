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

# CONFIGURATION
N_REPS = 10000       # number of replications per (m, pi0)
ALPHA = 0.05
M_VALUES = [4, 8, 16, 32, 64,128,256,512,1024,2048, 4096]
PI0_VALUES = [0.75, 0.5, 0.25, 0.0]
L = 10.0
METHODS = ["bonferroni", "hochberg", "bh"]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "results", "raw")
FIG_DIR = os.path.join(BASE_DIR, "results", "figures")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)


# MAIN SIMULATION
def run_simulation(save_profiling=False, save_result= True):
    records = []
    timing_records = []
    block_times = []
    dgp_total = 0.0
    method_total = {m: 0.0 for m in METHODS}
    metric_total = {m: 0.0 for m in METHODS}
    total_start = time.perf_counter()
    for pi0 in PI0_VALUES:
        for m in M_VALUES:
            dgp_time = 0
            method_time = {method: 0.0 for method in METHODS}
            metric_time = {method: 0.0 for method in METHODS}


            block_start = time.perf_counter()
            desc = f"pi0={pi0:.2f}, m={m}"
            sim_results = {method: [] for method in METHODS}

            for _ in tqdm(range(N_REPS), desc=desc):
                t0 = time.perf_counter()
                pvals, truth = generate_pvalues(m=m, pi0=pi0, L=L, pattern="equal")
                t1 = time.perf_counter()
                dgp_time += (t1 - t0)

                for method in METHODS:
                    t2 = time.perf_counter()
                    rejects = apply_method(pvals, ALPHA, method)
                    t3 = time.perf_counter()
                    method_time[method] += (t3 - t2)

                    t4 = time.perf_counter()
                    fdr = compute_fdr(rejects, truth)
                    power = compute_power(rejects, truth)

                    t5 = time.perf_counter()
                    metric_time[method] += (t5 - t4)
                    sim_results[method].append({"fdr": fdr, "power": power})

            for method in METHODS:
                summary = summarize_metrics(sim_results[method])
                records.append({
                    "pi0": pi0,
                    "m": m,
                    "method": method,
                    **summary
                })
            block_end = time.perf_counter()
            block_time = block_end - block_start
            block_times.append(block_time)
            print(f"[pi0={pi0:.2f}, m={m}] block took {block_end - block_start:.3f} seconds")
            for method in METHODS:
                timing_records.append({
                    "pi0": pi0,
                    "m": m,
                    "component": "dgp",
                    "method": None,
                    "time_sec": dgp_time
                })
                timing_records.append({
                    "pi0": pi0,
                    "m": m,
                    "component": "method",
                    "method": method,
                    "time_sec": method_time[method]
                })
                timing_records.append({
                    "pi0": pi0,
                    "m": m,
                    "component": "metrics",
                    "method": method,
                    "time_sec": metric_time[method]
                })

            print(f"\n[pi0={pi0:.2f}, m={m}] timing summary:")
            print(f"  DGP time: {dgp_time:.3f} seconds")
            for method in METHODS:
                print(f"  {method:10s}  method={method_time[method]:.3f}s   metrics={metric_time[method]:.3f}s")
            print("==================================================\n")
            dgp_total += dgp_time
            for method in METHODS:
                method_total[method] += method_time[method]
                metric_total[method] += metric_time[method]

    total_end = time.perf_counter()
    print(f"Total simulation runtime: {total_end - total_start:.3f} seconds")

    # ----------- GLOBAL SUMMARY (for baseline.md) -----------
    total_end = time.perf_counter()
    total_runtime = total_end - total_start

    avg_block_time = np.mean(block_times)
    avg_rep_time = total_runtime / (len(M_VALUES) * len(PI0_VALUES) * N_REPS)

    print("\n============= GLOBAL BASELINE SUMMARY =============")
    print(f"Total simulation runtime: {total_runtime:.3f} seconds")
    print(f"Average block time:       {avg_block_time:.3f} seconds")
    print(f"Average per replication:  {avg_rep_time:.6f} seconds")
    print("\n--- Component totals ---")
    print(f"DGP total time: {dgp_total:.3f} seconds")

    for method in METHODS:
        print(f"{method:10s} method_total={method_total[method]:.3f}s   "
              f"metrics_total={metric_total[method]:.3f}s")
    print("====================================================\n")

    # -------------------------------------------------------


    df = pd.DataFrame(records)
    if save_result:
        df.to_csv(os.path.join(RAW_DIR, "sim_summary.csv"), index=False)
        print(f"\nSaved summary to {RAW_DIR}/sim_summary.csv")

    if save_profiling:
        df_timing = pd.DataFrame(timing_records)
        df_timing.to_csv(os.path.join(RAW_DIR, "timing_summary.csv"), index=False)
        print(f"Saved timing summary to {RAW_DIR}/timing_summary.csv")

    return df


## Optimization: Array programming + Parallelization
def run_single_block(M, pi0, N_reps, alpha, L, seed, idx_cache):
    block_start = time.perf_counter()

    idx = idx_cache[M]

    t0 = time.perf_counter()
    pvals, truth = generate_pvalues_matrix(M, N_reps, pi0, L, seed)
    t1 = time.perf_counter()
    dgp_time = t1 - t0

    t2 = time.perf_counter()
    rej_bonf, rej_h, rej_bh = compute_rejections(pvals, alpha, idx)
    t3 = time.perf_counter()
    method_time = t3 - t2

    t4 = time.perf_counter()
    fdp_bonf, pow_bonf = compute_fdp_power(rej_bonf, truth)
    fdp_h, pow_h = compute_fdp_power(rej_h, truth)
    fdp_bh, pow_bh = compute_fdp_power(rej_bh, truth)
    t5 = time.perf_counter()
    metric_time = t5 - t4

    block_time = time.perf_counter() - block_start

    return {
        "record": {
            "pi0": pi0,
            "M": M,
            "FDP_Bonf": fdp_bonf,
            "Power_Bonf": pow_bonf,
            "FDP_Hoch": fdp_h,
            "Power_Hoch": pow_h,
            "FDP_BH": fdp_bh,
            "Power_BH": pow_bh
        },
        "timings": [
            {"pi0": pi0, "m": M, "component": "dgp", "time_sec": dgp_time},
            {"pi0": pi0, "m": M, "component": "method", "time_sec": method_time},
            {"pi0": pi0, "m": M, "component": "metrics", "time_sec": metric_time},
        ],
        "block_time": block_time
    }

def run_simulation_optimized_parallel(M_list, pi0_list, N_reps, alpha, L, seed0=0, n_jobs=-1, save_result= True, save_profiling=False):
    idx_cache = {M: np.arange(1, M + 1) for M in M_list}

    total_start = time.perf_counter()

    tasks = []
    seed = seed0
    for pi0 in pi0_list:
        for M in M_list:
            tasks.append((M, pi0, seed))
            seed += 1

    results = Parallel(n_jobs=n_jobs)(
        delayed(run_single_block)(M, pi0, N_reps, alpha, L, seed, idx_cache)
        for (M, pi0, seed) in tasks
    )

    total_end = time.perf_counter()
    total_runtime = total_end - total_start

    records = [r["record"] for r in results]
    timing_records = sum([r["timings"] for r in results], [])
    block_times = [r["block_time"] for r in results]

    print("\n================ OPTIMIZED PARALLEL SUMMARY ================")
    print(f"Total runtime:       {total_runtime:.3f} seconds")
    print(f"Average block time:  {np.mean(block_times):.3f} seconds")
    print(f"n_jobs = {n_jobs}")
    print("============================================================\n")

    df = pd.DataFrame(records)
    df_timing = pd.DataFrame(timing_records)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_DIR = os.path.join(BASE_DIR, "results", "raw")


    if save_result:
        df.to_csv(os.path.join(RAW_DIR, "sim_summary_optimized.csv"), index=False)
    if save_profiling:
        df_timing.to_csv(os.path.join(RAW_DIR, "timing_summary_optimized.csv"), index=False)

    return df, df_timing




if __name__ == "__main__":
    np.random.seed(0)
    df_summary = run_simulation()
    plot_power_vs_m(df_summary, name = "power_vs_m_grid_baseline.png")


