# Analysis Report
**Project:** Reproducing Benjamini & Hochberg (1995)

---

## 1. Reproduction Accuracy

The simulation reproduced the qualitative patterns from *Benjamini & Hochberg (1995)*, Figure 1 Setting b.  
Across numbers of tested hypotheses $ m \in \{4, 8, 16, 32, 64\}$  and proportions of true nulls  $\pi_0 \in \{0.75, 0.5, 0.25, 0\}$ , the Benjamini–Hochberg (BH) procedure achieved the highest power while maintaining the false discovery rate (FDR) below 0.05. Hochberg and Bonferroni were more conservative, yielding smaller FDR and lower power, consistent with the original paper.

Small numerical differences arose because the original study used more replications and possibly different random number generation. Our implementation used 5000 repetitions with explicit seeds.  

The diagnostic boxplots confirm that the method ranking and FDR control pattern remain consistent.

---

## 2. Neutrality of the Simulation Design

Overall, the design is neutral in the sense that all methods were evaluated on the same data and significance level $ \alpha = 0.05 $.  
However, several structural choices in BH (1995) inherently favor the new FDR procedure:

- **Effect size distribution.**  
  Non-null hypotheses were divided equally into four groups with means $\{L/4, L/2, 3L/4, L\}$. This setup creates many weak signals, penalizing strict FWER methods (Bonferroni, Hochberg)  
  that must correct for all tests simultaneously. It highlights BH’s relative advantage.

- **Independence assumption.**  
  Test statistics were independent $Z_i \sim \mathcal{N}(\mu_i, 1)$. Real data often exhibit dependence, which can inflate FDR.  
  The independence assumption slightly idealizes BH’s control.

- **Uniform α level.**  
  Each method used $\alpha = 0.05$, even though FWER ≤ $\alpha$ (Bonferroni/Hochberg) and FDR ≤ $\alpha$ (BH) are not equivalent error criteria. Using the same $\alpha$ makes BH appear more powerful by design.

Hence the simulation is informative but not entirely neutral—it emphasizes conditions where FDR control is expected to outperform FWER control.

---

## 3. Potential Improvements

To strengthen neutrality and realism, I would include **modern FDR procedures** (e.g., Benjamini–Yekutieli, Storey’s q-value) for context. I may also add **confidence intervals** for mean FDR and power to quantify simulation uncertainty.

---

## 4. Visualization Evaluation

Two plots were produced from this project: 

- The **power-vs-m line plots** clearly show trends by π₀, include uncertainty bands,  
  and use consistent log₂ scales across panels.
- The **diagnostic boxplots**  reveal variability across replications. 

## 5. Summary
We reproduced the main result from Benjamini & Hochberg (1995). The analysis generated the original power comparison plot and an additional diagnostic figure for further evaluation.



