# Task 04 — Add a modern QLSA comparison

Follow `paper-revise/prompts/tasks/README.md`. Use tasks 01–02 and coordinate the cost boundary with task 05. Address C1-1.

Verify the intended “shortcut to optimal QLSA” reference and Costa, Dalzell, An, and Berry, “Constant Factor Analysis of Optimal Quantum Linear Solvers in Practice” (2026), including bibliographic details and applicability. Select a defensible modern algorithm and explain the choice against the reviewer's request; do not infer practical superiority from asymptotic optimality.

Deliver to `paper-revise/results/04-modern-qlsa/` a cited algorithm summary, explicit assumptions, and a reproducible logical-resource model. Expose constant factors, precision, condition number, sparsity/access model, oracle or block-encoding implementation, ancillas, gate counts, and depth where supported. Flag unavailable quantities needed by QEC instead of silently estimating them.

Acceptance: HHL and the modern solver can be evaluated under the same task 02 problem, output accuracy, and hardware assumptions. State which costs the model includes and which task 05 must supply.
