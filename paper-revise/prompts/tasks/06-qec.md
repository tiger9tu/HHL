# Task 06 — Audit QEC overhead and provide an adapter

Follow `paper-revise/prompts/tasks/README.md`. Use task 01 and final logical resources from tasks 03–05. Preserve the existing QEC approach unless an identified inconsistency requires correction.

Inspect the manuscript's QEC analysis, `tools/surface_code_opt.py`, and relevant notebooks. Audit code distance, logical failure budget, gate/depth conversion, magic-state factories, routing assumptions, and runtime/qubit tradeoffs. Clarify whether failure budgets apply per solve, shot, or full computation.

Deliver to `paper-revise/results/06-qec/` an adapter from logical resources to physical qubits, runtime, and quantities needed by task 07; a short audit; and reproducible validation examples. Assess whether Qultran or another available estimator supports the same model before attempting an independent cross-check. Record tool versions and explain differences; if unavailable, provide an analytic check and state the limitation.

Acceptance: both quantum algorithms pass through the same explicit QEC assumptions, and any departure from the original analysis is justified and identified for manuscript updates.
