# ============================================================
# Makefile for FDR Simulation Project (BH 1995 reproduction)
# ============================================================

# Variables
PYTHON := python
SRC_DIR := src
RESULTS_DIR := results
RAW_DIR := $(RESULTS_DIR)/raw
FIG_DIR := $(RESULTS_DIR)/figures
SIM_SCRIPT := $(SRC_DIR)/simulation.py
TEST_DIR := tests

# ============================================================
# Targets
# ============================================================

# 1. Run the full pipeline
all: simulate analyze figures
	@echo "All tasks completed successfully."

# 2. Run simulations and save raw results
simulate:
	@echo "Running simulations..."
	$(PYTHON)  -m src.simulation
	@echo "Simulation complete. Results saved in $(RAW_DIR)"

# 3. Process raw results (if you plan to analyze or summarize)
analyze:
	@echo "Analyzing raw simulation results..."
	$(PYTHON) -c "import pandas as pd; df=pd.read_csv('$(RAW_DIR)/sim_summary.csv'); print(df.groupby(['pi0','method'])[['mean_fdr','mean_power']].mean())"
	@echo "Analysis summary printed."

# 4. Create visualizations
figures:
	@echo "Generating figures..."
	$(PYTHON) -m src.visualization
	@echo "Figures saved in $(FIG_DIR)"

# 5. Remove generated files
clean:
	@echo "Cleaning up results..."
	rm -rf $(RESULTS_DIR)
	@echo "All generated files removed."

# 6. Run test suite (if you have tests/)
test:
	@echo "Running tests..."
	pytest $(TEST_DIR) -v
	@echo "All tests passed."

profile:
	@echo "Running profiling..."
	$(PYTHON) -m profiling.profiling
	@echo "All profiling analysis done."

complexity:
	@echo "Running complexity..."
	$(PYTHON) -m profiling.profile_m
	$(PYTHON) -m profiling.profile_N_rep
	@echo "All complexity analysis done."

make benchmark:
	@echo "Running timing comparison..."
	$(PYTHON) -m profiling.benchmark
	@echo "All timing comparison analysis done."

make parallel:
	@echo "Running parallelized version..."
	$(PYTHON) -m src.simulation_optimized
	@echo "Done."


# ============================================================
# Phony targets (not actual files)
# ============================================================
.PHONY: all simulate analyze figures clean test profile complexity benchmark parallel
