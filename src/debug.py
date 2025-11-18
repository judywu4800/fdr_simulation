import numpy as np
from dgps import generate_pvalues, generate_pvalues_matrix
from methods import apply_method
from metrics import compute_fdp_power
from methods import compute_rejections

M = 16
pi0 = 0.75
L = 10
alpha = 0.05
N = 10

print("=== Baseline 10 replicates ===")
fdrs = []
for i in range(N):
    pvals, truth = generate_pvalues(m=M, pi0=pi0, L=L, pattern="equal")
    rejects = apply_method(pvals, alpha, "bonferroni")
    fdp, power = compute_fdp_power(rejects.reshape(1, -1), truth)
    fdrs.append(fdp)
print("baseline mean FDP:", np.mean(fdrs))


print("=== Optimized 10 replicates ===")
idx = np.arange(1, M+1)
pvals_matrix, truth2 = generate_pvalues_matrix(M, N, pi0, L, 0)
rej_bonf, _, _ = compute_rejections(pvals_matrix, alpha, idx)
fdp2, power2 = compute_fdp_power(rej_bonf, truth2)
print("optimized mean FDP:", fdp2)
