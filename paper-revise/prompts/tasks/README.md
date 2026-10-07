# Paper revision tasks

Give an agent one numbered prompt below together with this README. Paths are relative to the repository root (`HHL/`). These prompts plan the revision; they do not assert that the proposed algorithms, references, or assumptions have been validated.

## Shared instructions for every agent

- Read `paper-revise/prompts/paper-revise.md`, both reviewer PDFs in `paper-revise/docs/`, and the relevant parts of the manuscript PDF in `paper/`. Use the actual reviews to check the summary and identify minor comments too.
- Inspect relevant repository code before replacing or extending it. Preserve unrelated work. The repository currently contains a manuscript PDF; do not assume editable manuscript sources exist.
- Put your report, proposed manuscript text, assumptions, citations, and handoff notes in `paper-revise/results/NN-name/`. Keep scripts and generated artifacts there unless your task explicitly calls for integration. Explain any proposed changes to shared source files before integration.
- Verify technical references against primary sources. Distinguish established results, assumptions, measured results, and unresolved questions. Do not fabricate evidence or treat requested conclusions as established facts.
- Use the notation and interfaces from task 01. If starting early, state provisional assumptions and reconcile them before completion. Record input versions, commands, units, uncertainty, and validation appropriate to the work.
- End with a concise handoff: deliverables, reviewer comments addressed, limitations, and inputs needed by downstream tasks. If essential data or tools are unavailable, deliver the supported work and identify the exact blocker.

## Tasks and dependencies

“Depends on” means the upstream handoff is needed to finalize the task. Literature review and code inspection may start earlier.

| Task | Prompt | Depends on | Main review coverage |
| --- | --- | --- | --- |
| 01 | [Framework and contracts](01-framework.md) | — | C2-1 |
| 02 | [Application and benchmark specification](02-application.md) | 01 | C1-6, C2-3 |
| 03 | [Repair HHL analysis](03-hhl-analysis.md) | 01, 02 | C1-5, C1-6 |
| 04 | [Modern QLSA resource model](04-modern-qlsa.md) | 01, 02 | C1-1 |
| 05 | [Input, output, and error accounting](05-input-output.md) | 01, 02; reconcile with 03, 04 | C1-2 |
| 06 | [QEC audit and adapter](06-qec.md) | 01; finalize with 03–05 | Existing QEC consistency |
| 07 | [Physical hardware and energy model](07-hardware-energy.md) | 01; finalize with 06 | C2-2 |
| 08 | [Classical baseline rebuild](08-classical-baseline.md) | 01, 02, 05 | C1-3, C1-4, C2-3 |
| 09 | [End-to-end results and sensitivity](09-results-sensitivity.md) | 02–08 | C1-4, C1-6, C2-2, C2-3 |
| 10 | [Manuscript revision](10-manuscript.md) | 01–09 | C2-1, C2-4, C2-5; all technical changes |
| 11 | [Reviewer response and coverage audit](11-reviewer-response.md) | 10; inventory can start immediately | All major and minor comments |
| 12 | [Final integration and reproducibility](12-integration.md) | 09–11 | Final consistency and reproducibility |

Suggested execution: establish 01 and 02 first; develop 03–08 concurrently where their inputs permit; then execute 09–12 in order. Task 05 owns the common input/output contract and task 06 owns the QEC adapter, avoiding double counting between models. Task 12 owns shared-code integration. No agents need to be launched merely to use this task list.
