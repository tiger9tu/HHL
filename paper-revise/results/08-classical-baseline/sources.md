# Source audit — retrieved 20 September 2026

- Manuscript PDF, Appendix D p. 24, Figure 13, Theorem 4 and D1: arithmetic expression and variant; Appendix F p. 28 F1: energy as work/rate × power. Relevant page-marked extracts are in `sources/` with both complete referee-text extracts.
- [Official HPCG November 2025 list](https://www.hpcg-benchmark.org/custom/sc25.html): four frozen HPCG scores. Column is HPCG PFLOP/s, not HPL Rmax. Local `sources/hpcg-sc25.html`.
- [TOP500 November 2025](https://www.top500.org/lists/top500/2025/11/): same-system reported power kW and core counts. These are power proxies for this task, not verified HPCG-run electrical measurements. Local `sources/top500-2025-11.html`.
- [HPCG project](https://www.hpcg-benchmark.org/): benchmark kernel mix and multigrid-PCG driver. This is a different workload from the paper recurrence.
- [Official HPCG FAQ](https://www.hpcg-benchmark.org/faq/index.html): FP64 requirement, large-memory/long-duration benchmark conditions and memory/collective behavior. Local `sources/hpcg-faq.html`.
- [Netlib Templates](https://www.netlib.org/templates/templates.pdf): CG and CGNE/CGNR algorithm definitions. The paper's numerical formula is transcribed from the local manuscript, not attributed to a new exact-instruction theorem in this reference.
- Task 01 `interface.md` and task 02 `specification.md`/`benchmark-pp.json`: local ownership, input/output and parameter contracts. Captured in the input manifest.

The original hardware list and source precision are intentionally frozen. Downloading a source again can change bytes; model regeneration uses local JSON values and needs no network. No primary source consulted supplies paired HPCG power for all four selected measurements. The report keeps that uncertainty explicit and applies no inferred PUE.
