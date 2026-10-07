# Task 02 — Specify a realistic application benchmark

Follow `paper-revise/prompts/tasks/README.md`. Use task 01. Address C1-6 and C2-3.

Investigate an elliptic PDE with a specified scalar output as the primary candidate. Choose and justify a concrete problem, discretization, boundary conditions, right-hand side, and observable. Derive or source how dimension, sparsity, conditioning, and required precision vary with problem size. Include discretization error, preconditioning costs, and assumptions about accessing matrix entries and preparing inputs. Do not impose `s = kappa = log(N)` without evidence.

Deliver to `paper-revise/results/02-application/` a benchmark specification, parameter table, small reproducible instance generator, and proposed application text. Define exactly the same output and total accuracy target for quantum and classical solvers. Document whether efficient quantum input/output is established, assumed, or unavailable. Include realistic parameter ranges for sensitivity studies.

Acceptance: tasks 03–05 and 08 can evaluate the same scientific problem from the specification without choosing incompatible access models or accuracy targets.
