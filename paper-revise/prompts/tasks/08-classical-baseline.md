# Task 08 — Rebuild the classical comparison

## 9/9 prompt
Follow `paper-revise/prompts/tasks/README.md`. Use tasks 01–02 and 05; align energy boundaries with task 07. Address C1-3, C1-4, and C2-3.

Resolve the main-text CG versus Appendix D CGNE inconsistency. Select solvers appropriate to the benchmark's matrix structure, including credible preconditioning and scientific-computing alternatives. Explain applicability, convergence assumptions, setup costs, conditioning effects, precision, and memory/data-movement costs. Reassess the role of direct methods rather than applying dense estimates indiscriminately.

Replace the single 1 GHz/50 W desktop baseline with justified hardware scenarios and fair accuracy/output targets. Separate operation counts, attainable performance, and power; distinguish measurements from projections and document parallel-efficiency assumptions.

Deliver to `paper-revise/results/08-classical-baseline/` executable cost models, feasible representative benchmarks, sourced hardware parameters, and replacement main-text/appendix passages. Reconcile the existing Cholesky/supercomputer crossover claim and flag infeasible extrapolations.

Acceptance: readers can reproduce classical time, memory, and energy estimates and compare them with quantum results under explicit, compatible assumptions.

## 9/20 prompt
Now I know what to do, just restart doing this task, do the following:
1. only preserve the CG method, extract the analytical formula for the the exact logical instruction counter, which can be found on our paper
2. refer to https://www.hpcg-benchmark.org/ for the physical computing model, using HPCG PFLOPS to get the runtime, multiply the power to get the energy cost.
