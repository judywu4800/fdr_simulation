# Project: Reproducing Benjamini & Hochberg (1995)

**Goal:** Reproduce *Benjamini & Hochberg (1995)*, Figure 1 (Setting b), comparing multiple‐testing procedures that control either the Family-Wise Error Rate (FWER) or the False Discovery Rate (FDR).

This folder is organized as follows.

```
fdr_simulation
├── ADEMP.md
├── ANALYSIS.md
├── data
├── Makefile
├── pytest.ini
├── README.md
├── requirements.txt
├── results
│   ├── figures
│   │   ├── diagnostic_boxplots.png
│   │   └── power_vs_m_grid.png
│   └── raw
│       └── sim_summary.csv
├── src
│   ├── __init__.py
│   ├── dgps.py
│   ├── methods.py
│   ├── metrics.py
│   ├── simulation.py
│   └── visualization.py
└── tests
    ├── test_dgps.py
    ├── test_methods.py
    └── test_metrics.py
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

Intermediate and final outputs are saved under:
   ```bash
  results/raw/sim_summary.csv
  results/figures/power_vs_m_grid.png
  results/figures/diagnostic_boxplots.png
   ```
**Estimated run time**: 3-5 minutes.

## Summary of Key Findings
The Benjamini–Hochberg (BH) procedure achieves much higher power while keeping the false discovery rate below 0.05.
Bonferroni and Hochberg maintain stricter control of Type I error but lose power, especially as the number of hypotheses m increases.
These results replicate Figure 1 Column 2 from BH (1995) and confirm the trade-off between FDR control and FWER conservativeness.

