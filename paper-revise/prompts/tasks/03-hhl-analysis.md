# Task 03 — Repair the HHL scaling analysis

Follow `paper-revise/prompts/tasks/README.md`. Use tasks 01–02. Address C1-5 and the HHL implications of C1-6.

Trace Statement 1, Eq. B19, Figure 9, and their implementation in `num/` and `src/HHL/`. Audit the numerical-to-asymptotic inference. Remove the fixed matrix-element-position assumption or explicitly delimit any surviving restricted result. Seek a justified bound; if unavailable, label empirical evidence as empirical and revise every dependent scaling claim.

Deliver to `paper-revise/results/03-hhl-analysis/` corrected derivations and manuscript text, a logical-resource model compatible with task 01, and reproducible experiments across matrix sizes and sparsity patterns. Report distributions, sample counts, seeds, errors, and uncertainty; give Figure 9 complete axes, caption, and setup. Cover task 02's regime and distinguish it from synthetic ensembles.

Acceptance: no claim of size-independent error relies only on small-matrix observations. List changes to downstream resource and crossover estimates and provide validation against tractable instances.
