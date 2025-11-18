# Reproducing Setting (1) — Linearly Decreasing Means from Figure 1 in Benjamini & Hochberg (1995)

## Aims
We reproduce **Setting (1)** from Section 4.1 of *Benjamini & Hochberg (1995)* to compare the **average power** of three multiple-testing procedures:
1. **Bonferroni** (family-wise error control)
2. **Hochberg (1988)** step-up FWER control
3. **Benjamini–Hochberg (1995)** FDR control  

The aim is to evaluate how average power changes with the **number of tested hypotheses (m)** and the **proportion of true nulls (π₀)** when the non-null means decrease linearly away from zero.

---

## Data-Generating Mechanism
Each simulation generates *m* independent normal test statistics.  

### Parameters
- **Number of hypotheses**: $m \in \{4, 8, 16, 32, 64\} $
- **Proportion of true nulls**: $\pi_0 \in \{0 \%, 25 \%, 50 \%, 75 \%\} $  
  (so the number of true nulls = 0, m/4, m/2, 3m/4)  
- **Nominal level**: $\alpha = 0.05  $
- **Mean pattern (Setting 1 – Decreasing)**:  
  The *$m (1 – \pi_0)$* false nulls are divided into four equal groups, and the non-zero expectations decrease linearly away from 0:
 $  \mu_i ∈ \{+L, +L/2, +L/3, +L/4\}
$
  where *L* controls the signal strength.  
- **Variance**: $Var(Z_i) = 1$ 
- **Signal level**: $L =10$ as the signal-to-noise ratio  

### Generation Steps (per replication)
1. For each configuration (m, $\pi_0$, L):  
   - Generate *$m_0 = \pi_0 m$* nulls $Z_i \sim N(0, 1)$  
   - Generate *$m_1 = m − m_0$* non-nulls with decreasing means:  
     first $\frac{1}{4}$ with μ = L, next $\frac{1}{4}$ = L/2, next $\frac{1}{4}$ = L/3, last $\frac{1}{4}$ = L/4  
2. Compute one-sided p-values $p_i = 1 − \Phi(Z_i)$.  
3. Apply each multiple-testing method at $\alpha = 0.05$.

Each condition is replicated **R = 2 000** times.

---

## Estimands / Targets
- **Average Power** = $E[T / m_1]$,  
  where T = number of correctly rejected false nulls.  
- (Optional) **Empirical FDR** = $E[V / \max(R, 1)]$ for validation.

---

## Methods
| Method | Description |
|---------|--------------|
| **Bonferroni** | Reject if $p_i ≤ \alpha / m$ |
| **Hochberg (1988)** | Step-up FWER procedure using ordered p-values |
| **BH (1995)** | Step-up FDR procedure |

All procedures applied to the same generated p-values at $\alpha = 0.05$.

---

## Performance Measures
- **Average Power** = mean (T / $m_1$) over replications  
- **Monte-Carlo SE** (optional, expected $\approx$ 0.001)  

Results will be summarized as mean power vs number of tested hypotheses (m) for each $\pi_0$ and L.

---

## Design Matrix

|$\pi_0$ | L | m values | Pattern | Methods |
|----|---|-----------|----------|----------|
| 0 % | 10 | 4 – 64 | Decreasing (D) | BH, Bonferroni, Hochberg |
| 25 % | 10 | 4 – 64 | Decreasing (D) | BH, Bonferroni, Hochberg |
| 50 % |  10 | 4 – 64 | Decreasing (D) | BH, Bonferroni, Hochberg |
| 75 % |10 | 4 – 64 | Decreasing (D) | BH, Bonferroni, Hochberg |

---

## Notes
- All tests are independent (covariance = 0).  
- Each configuration uses the same random Z-scores for all methods to match the paper’s correlated-comparison setup.  
- The resulting figure should show **average power vs number of hypotheses** (m) for each $\pi_0$, similar to **the left column of Figure 1** in the paper.  
- Expected outcome: power decreases as m increases, and **BH ≫ Hochberg ≫ Bonferroni** in power.
