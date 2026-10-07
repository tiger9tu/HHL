# Task 01 — Define the comparison framework

Follow `paper-revise/prompts/tasks/README.md`. Address C2-1 by making the reusable framework the organizing contribution.

Define problem parameters `pp`, quantum configuration `cq`, and classical configuration `cc`, with maps to time, space, and energy. Separate logical algorithm costs, input/output costs, QEC overhead, and physical hardware costs; separate classical operation counts from hardware performance. Specify units, accuracy and success criteria, preprocessing/amortization rules, and energy-system boundaries.

Deliver to `paper-revise/results/01-framework/`:
- A concise framework section and diagram specification.
- A parameter dictionary and machine-readable interface/schema for downstream models, including gate counts, depth, logical qubits, repetitions, classical operations, memory, and data movement.
- A ledger of assumptions and fair-comparison rules, including how uncertainty propagates.

Acceptance: downstream agents can combine their models without changing meanings, mixing units, or double counting costs. Show an illustrative symbolic calculation; do not invent numerical results.
