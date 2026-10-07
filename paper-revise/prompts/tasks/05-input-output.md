# Task 05 — Account for loading, readout, and total error

Follow `paper-revise/prompts/tasks/README.md`. Use tasks 01–02 and reconcile interfaces with tasks 03–04. Address C1-2.

Build the common end-to-end cost and error contract for both quantum solvers. Verify and assess the relevance of https://arxiv.org/abs/2111.10485. Account for classical data preprocessing, access/oracle construction, state preparation, solve success or amplification, and extraction of the specified scalar observable. Distinguish reusable work from costs repeated per shot or coherent algorithm call.

Treat the plan's claim that state preparation is negligible as a hypothesis: quantify it in the chosen access model and identify when it fails. Derive readout repetitions or coherent estimation costs with their precision and confidence dependence, without counting algorithm-internal repetitions twice.

Deliver to `paper-revise/results/05-input-output/` formulas, a callable cost/error wrapper, and proposed manuscript text. Allocate the total error budget, including discretization and observable normalization.

Acceptance: one auditable calculation connects scientific-output accuracy to total quantum execution cost for each solver, with no hidden free data access.
