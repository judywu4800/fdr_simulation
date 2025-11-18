# Project: Reproducing Benjamini & Hochberg (1995)

**Goal:** Reproduce *Benjamini & Hochberg (1995)*, Figure 1 (Setting b), comparing multiple‐testing procedures that control either the Family-Wise Error Rate (FWER) or the False Discovery Rate (FDR).

This folder is organized as follows.

```
fdr_simulation
├── data
├── doc
│   ├── ADEMP.md
│   ├── ANALYSIS.md
│   ├── baseline.md
│   └── optimization.md
├── Makefile
├── profiling
│   ├── benchmark.py
│   ├── profile_m.py
│   ├── profile_N_rep.py
│   └── profiling.py
├── pytest.ini
├── README.md
├── requirements.txt
├── results
│   ├── figures
│   │   ├── complexity_loglog_methods.png
│   │   ├── diagnostic_boxplots.png
│   │   ├── power_vs_m_grid_baseline.png
│   │   ├── power_vs_m_grid_optimized.png
│   │   ├── power_vs_m_grid.png
│   │   ├── runtime_total_vs_N_baseline.png
│   │   └── runtime_total_vs_N_comparison.png
│   └── raw
│       ├── sim_summary_optimized.csv
│       ├── sim_summary.csv
│       └── timing_summary.csv
├── src
│   ├── __init__.py
│   ├── debug.py
│   ├── dgps.py
│   ├── methods.py
│   ├── metrics.py
│   ├── simulation_optimized.py
│   ├── simulation.py
│   └── visualization.py
└── tests
    ├── test_dgps.py
    ├── test_methods.py
    ├── test_metrics.py
    └── test_regression.py
```

## Setup Instructions

1. **Clone this repository**
   ```bash
   git clone git@github.com:judywu4800/fdr_simulation.git
   cd fdr_simulation
   ```
   
2. **Create and activate a virtual environment**
    ```bash
   python3 -m venv .venv
    source .venv/bin/activate
    ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
## Run the Complete Analysis
- `make all`: Run simulations and save raw results.
- `make simulate`: Run simulations and save raw results.
- `make analyze`: Summarize FDR and power metrics.
- `make figures`: Generate publication-quality and diagnostic plots.
- `make profile`: Run profiling on representative simulation.
- `make complexity`: Run computational complexity analysis.
- `make benchmark`: Run timing comparison between baseline and optimized method.
- `make parallel`: Run optimized version with parallelization.

Intermediate and final outputs are saved under:
   ```bash
  results/raw
  results/figures
   ```

## Summary of Key Findings
The Benjamini–Hochberg (BH) procedure achieves much higher power while keeping the false discovery rate below 0.05.
Bonferroni and Hochberg maintain stricter control of Type I error but lose power, especially as the number of hypotheses m increases.
These results replicate Figure 1 Column 2 from BH (1995) and confirm the trade-off between FDR control and FWER conservativeness.

## Summary of Unit 3
See `doc/baseline.md` and `doc/optimization.md` 

