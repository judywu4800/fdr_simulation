import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import time
from src.dgps import generate_pvalues, generate_pvalues_matrix
from src.methods import apply_method, compute_rejections
from src.metrics import compute_fdr, compute_power, summarize_metrics, compute_fdp_power
from src.visualization import plot_power_vs_m
from src.simulation import *
from joblib import Parallel, delayed

if __name__ == "__main__":
    np.random.seed(0)
    run_simulation(save_profiling=True, save_result=False)


