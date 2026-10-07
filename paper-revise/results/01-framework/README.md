# Task 01 handoff: framework and contracts

Completed task 01 as a revision proposal and downstream contract, version **1.0.0**. The reusable framework is the organizing contribution; HHL and modern QLSA are interchangeable case-study models behind explicit interfaces. No numerical resource or crossover result is asserted.

## Deliverables

- [Four-page illustrated introduction (PDF)](framework-introduction.pdf) and [editable PDF build script](build_intro_pdf.py).

- [Proposed manuscript section, Mermaid diagram specification and symbolic calculation](framework.md).
- [Parameter dictionary and interface semantics](interface.md).
- [Machine-readable JSON Schema](interface.schema.json) and [symbolic capped-schedule example](symbolic-example.json).
- [Assumptions, fair comparison, error accounting and uncertainty ledger](assumptions.md).
- [Verified primary references and scope of support](references.md).
- [Validator](validate.py), [input manifest](input-manifest.json), [input capture script](capture_inputs.py), and page-marked PDF text in `source-extracts/`.

## Review coverage and manuscript placement

**C2-1:** direct response. Insert the framework section and diagram before algorithm-specific results. The proposed narrative separates logical work, I/O composition, QEC, hardware performance and energy, with a common output contract for both branches. HHL remains a case study; the framework does not claim novelty for its individual component models.

**C1 minor 1:** distinct symbols and typed fields replace overloaded T: use `G_T` for T-gate count, `D_T` for T-depth, `R`/M/K for repetitions/samples/attempt cap, `C_cyc` for code cycles, and t for seconds. Denote the SWAP operator explicitly as `SWAP`.

The interfaces enable, but do not finish, C1-1–6 and C2-2–3. They also support C2-4–5 through a framework-first audience and conditional conclusions. Reviewer 1 minor 4 should be handled in task 10 by restating the actual final limitations. Minor 2 calls the unlabeled figure “Fig. 19” while major 5 names Figure 9; the supplied manuscript has Figure 9 on PDF page 18 following B19 on page 17. Preserve this discrepancy in the response inventory and identify the figure by content. Minor 3's spelling/grammar audit and actual figure repair remain with tasks 03/10/11.

Both complete reviews were read (3 and 5 pages). Relevant manuscript material inspected: introduction/definitions/results framing on pages 1–3; methods and conclusions on pages 5–6; references on 6–7; B19 and its assumptions on 17–19; QEC on 19–23; classical baselines on 24–25. The manuscript PDF is the editing reference; no editable manuscript source was assumed or changed.

## Existing-code observations for downstream owners

These are inspection findings, not repaired implementations:

- `tools/surface_code_opt.py` accepts T counts and logical-qubit counts, without general logical depth, complete I/O, host work or data movement. `HHL.__init__` embeds the manuscript scaling and declares a fixed ancilla count that is not added to `logical_qubit_count`. Task 03 must audit validity and peak lifetimes.
- That file's `total_clock_cycles` derives from tile/protocol magic-state timing, while the code-distance failure estimate separately multiplies time by d. The manuscript describes patches as d² qubits while code uses `2*d*d` per tile. These need an explicit syndrome-cycle and physical-qubit convention in task 06; the new contract does not silently choose a conversion for the legacy return value.
- Default distillation selection uses a target of 0.01 rather than an explicit full-workload per-magic-state budget. Code distance is selected before final configuration optimization; infeasibility can appear as a sentinel distance or `None` results. Task 06 must recheck the final complete workload and emit explicit infeasibility. The contract's QEC cycle count already includes any distance conversion.
- `src/HHL/HHL.qs` prepares b inside the circuit. `OneSparseHHLSimulation` repeats until heralded success, whereas the general `HHLSimulation` has its retry loop commented out. `DumpMachine` is a simulator diagnostic, not an implemented physical output-extraction protocol. Counts from these scopes cannot be used interchangeably.
- `src/test/GateCountTest.qs` counts primitive gates and oracle calls in the same invocation. Treat oracle-call counters as diagnostic when their bodies are expanded; audit decomposition/basis before adding gate buckets. The counters do not supply a complete dependency schedule.
- `num/hhl.m` is a normalized state-vector simulation with explicit postselection and dense matrix operations. It does not model physical postselection retries, physical readout, or a practical classical solver baseline.

No shared code was changed. Tasks 03/05/06/08 can use these observations to propose adapters and repairs; task 12 owns integration.

## Validation and reproducibility

Input snapshot: git HEAD `66a01648db95465abbd2f099d9b8f103679555b6`, with the actual working-tree file SHA-256 hashes in `input-manifest.json`. Existing user changes to revision prompts were preserved. Repository instructions were checked; no applicable AGENTS.md was found in the inspected workspace/ancestor paths.

Commands from repository root:

```sh
python3 paper-revise/results/01-framework/validate.py --self-test
python3 paper-revise/results/01-framework/capture_inputs.py --pypdf-path /tmp/hhl-framework-pypdf-3
```

Validation environment: Python 3.6.15, jsonschema 3.2.0 using Draft 7. Outcome: schema checked; symbolic example valid; nine deliberately invalid fixtures rejected (wrong cycle units, contradictory unknown quantity, duplicate primitive cost, duplicate repetition at both schema/semantic levels, omitted output work, boundary mismatch, unresolved result declared evaluated, and invalid κ₂). This is contract validation, not numerical simulation or independent certification of the physical models. Local deliverable links, source hashes and authored-file whitespace were also checked. Repository-wide `git diff --check` reports only pre-existing whitespace in the user-edited revision prompt; that file was left untouched.

PDF extraction used pypdf 3.17.4 with dataclasses 0.8 and typing_extensions 4.1.1 in a temporary directory. System `pdftotext` and pip were unavailable, so the versioned wheels were downloaded from PyPI via Python's standard library and unpacked locally. To regenerate elsewhere, install these versions in a compatible environment (or provide pypdf on the interpreter path) and omit `--pypdf-path` if unnecessary. The extraction script does not require network access. Mathematical typography in text extracts can be imperfect; preserve the original PDFs as authoritative inputs.

## Remaining inputs and acceptance limits

Tasks 02/05 must supply an application-backed `pp`, input-access implementation, output-error conversion, sampling/retry model and budget certificate. Tasks 03/04 must supply validated logical counts, exclusive gate bases, depth or scheduling assumptions, and model versions. Task 06 must deliver a full-workload QEC schedule and failure guarantee. Tasks 07/08 must supply calibrated or explicitly bounded hardware, power, memory, movement and classical performance models. Task 09 must evaluate feasibility and correlated uncertainty before making comparisons. Task 10 integrates the proposed prose once those results are available.

The schema permits symbolic and partial records so downstream work can proceed now. It does not execute expressions or prove completeness of a model's declared cost inventory. Omitted physical costs, unsupported accuracy conversions and unjustified scheduling assumptions remain scientific review failures even when a record passes structural validation. There is no blocker to delivering task 01; numerical instantiation is intentionally the responsibility of tasks 02–09.

## PDF introduction (9 September 2026)

`framework-introduction.pdf` introduces the workflow, `pp`/`cq`/`cc`, resource contracts, comparison rules and a symbolic observable example. It uses selectable text, embedded Liberation Sans fonts, a vector workflow diagram and four clickable primary-reference links. It presents no new numerical results.

Rebuild from the repository root with Python 3.11 and ReportLab 4.4.3:

```sh
PYTHONPATH=/tmp/hhl-pdf-deps python3.11 paper-revise/results/01-framework/build_intro_pdf.py
```

The temporary dependency directory used ReportLab 4.4.3, Pillow 11.3.0 and charset-normalizer 3.4.3; omit `PYTHONPATH` if installed in your environment. The builder uses Liberation Sans regular, bold and italic from `/usr/share/fonts/truetype/`; adjust the font directory for another system. PyMuPDF 1.26.4 was used only for validation and page rendering. All four final pages were visually checked; page count, text boundaries, character coverage and the four reference links passed checks.
