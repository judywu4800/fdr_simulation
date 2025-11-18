import numpy as np
import pandas as pd

import src.simulation as sim

N_REPS_TEST = 2000
M_TEST = [4, 8, 16]
PI0_TEST = [0.75, 0.25]
ALPHA = sim.ALPHA
L = sim.L


def baseline_for_test():
    old_M = sim.M_VALUES
    old_pi0 = sim.PI0_VALUES
    old_N = sim.N_REPS

    sim.M_VALUES = M_TEST
    sim.PI0_VALUES = PI0_TEST
    sim.N_REPS = N_REPS_TEST

    try:
        df = sim.run_simulation(save_result=False, save_profiling=False)
    finally:
        sim.M_VALUES = old_M
        sim.PI0_VALUES = old_pi0
        sim.N_REPS = old_N

    df = df[df["method"] == "bh"]
    df = df[["pi0", "m", "method", "mean_power"]]
    return df


def optimized_for_test():
    df_opt, _ = sim.run_simulation_optimized_parallel(
        M_list=M_TEST,
        pi0_list=PI0_TEST,
        N_reps=N_REPS_TEST,
        alpha=ALPHA,
        L=L,
        seed0=0,
        n_jobs=-1,
        save_result=False,
        save_profiling=False,
    )

    rows = []
    for _, row in df_opt.iterrows():
        rows.append({
            "pi0": row["pi0"],
            "m": row["M"],
            "method": "bh",
            "mean_power": row["Power_BH"],
        })
    return pd.DataFrame(rows)


def assert_close(a, b, tol=0.02):
    assert abs(a - b) <= tol, f"{a} vs {b} differ > {tol}"


def test_regression():
    df_base = baseline_for_test()
    df_opt = optimized_for_test()

    merged = df_base.merge(df_opt, on=["pi0", "m", "method"], suffixes=("_base", "_opt"))

    for _, row in merged.iterrows():
        assert_close(row["mean_power_base"], row["mean_power_opt"])
