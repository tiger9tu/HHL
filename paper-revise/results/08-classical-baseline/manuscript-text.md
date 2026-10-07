# Replacement main-text passage

We retain the paper's CG-family arithmetic model from Appendix D,

\[
n_{\mathrm{FLOPs}}=\left\lceil\frac{\kappa}{2}\ln\frac{2}{\epsilon}\right\rceil(4Ns+14N),
\]

where N is the original dimension, s bounds row/column sparsity, κ is the original condition number and ε is the relative solution-error parameter. The unrounded expression is Eq. (D1). This is a modeled arithmetic count; it is not an executed processor-instruction count. The recurrence shown in Figure 13 is a normal-equation CG variant (CGLS/CGNR), despite its CGNE caption, and must be identified consistently in the main text and appendix.

We replace the desktop CPU-frequency model with published HPCG performance. For a system reporting R_HPCG PFLOP/s, the modeled solver-core time is t=n_FLOPs/(10¹⁵R_HPCG). Its projected energy is E=P_system t, with power converted to watts. We use a pinned November 2025 HPCG list and report system power separately. The power values from TOP500 are proxies rather than paired HPCG-job measurements. No facility overhead multiplier is assumed.

HPCG exercises a different, multigrid-preconditioned CG workload, so transferring its measured rate to the paper recurrence is an explicit performance assumption. This comparison estimates solver-core resources; input construction, output evaluation, accuracy certification and facility-energy coverage remain separate requirements. No new quantum crossover follows solely from substituting HPCG rates.

# Appendix / methods replacement

Decompose each modeled iteration into two sparse matrix-vector products (4Ns FLOPs), three vector updates (6N), and coefficient work (8N). Use a natural logarithm and distinguish iteration count K from condition number κ. Export both the literal D1 expression and the whole-iteration version; their difference is less than 4Ns+14N FLOPs. The coefficients follow the manuscript's accounting conventions and do not account for all runtime instructions or startup work.

Read the HPCG PFLOP/s column directly: multiplying again by cores or the fraction of peak would double count benchmark throughput. For sensitivity, an application-rate multiplier η and power multiplier ρ give t=n_FLOPs/(η10¹⁵R_HPCG) and E=ρP_system t. The nominal case is η=ρ=1. This is not a measured application energy efficiency, and capacity-infeasible or unresolved cases cannot support an advantage claim.

The previous Cholesky performance comparison and its numerical crossover are omitted from this CG-only revision. The limitations of the retained solver variant, benchmark-rate transfer and incomplete energy boundary are stated in the conclusions.
