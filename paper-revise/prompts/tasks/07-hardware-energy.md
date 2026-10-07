# Task 07 — Build a defensible physical hardware model

Follow `paper-revise/prompts/tasks/README.md`. Use task 01 and coordinate with task 06. Address C2-2.

Verify and assess the proposed sources: https://arxiv.org/pdf/2603.28627, https://arxiv.org/pdf/2308.08648, and https://arxiv.org/abs/2505.15907. Use applicable published models or explain why they cannot transfer to this architecture.

Model hardware power and energy with explicit boundaries, including relevant cooling, control, decoding, factory, and idle/active contributions. Distinguish fixed infrastructure costs from quantities that scale with qubit count or runtime. Give units, provenance, plausible ranges, and dependencies between parameters; avoid unsupported linear scaling.

Deliver to `paper-revise/results/07-hardware-energy/` an executable model, sourced parameter/scenario table, validation calculations, and proposed methods text. Supply task 09 with sensitivity variables and consistent scenario constraints. Coordinate energy boundaries with task 08.

Acceptance: reported total energy follows transparently from power and runtime, and uncertainty in speculative hardware parameters remains visible in downstream comparisons.
