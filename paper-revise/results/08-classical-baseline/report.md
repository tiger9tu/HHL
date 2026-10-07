# Classical baseline: paper CG arithmetic and HPCG physical model

Revision: 20 September 2026. This report implements the **9/20 section** of task 08, replacing the earlier multi-solver scope. The active pipeline is:

**Problem parameters → paper CG FLOPs → published HPCG FLOP/s → runtime → system power × runtime.**

No active LU, Cholesky or independently modeled multigrid solver is retained. The superseded reports and multi-solver archive have been removed at the user’s request.

## 1. Extracted logical arithmetic formula

Manuscript Appendix D, p. 24, Figure 13 / Theorem 4 / Eq. (D1), gives:

| Work per iteration | Paper FLOP count |
|---|---:|
| Two sparse matrix-vector products | 4Ns |
| Three vector updates | 6N |
| Coefficient calculations | 8N |
| Total | N(4s+14) |

Here N is the original square matrix dimension, s bounds nonzeros per row **and column**, κ is the original matrix condition number, and ε is the paper's relative solution-error tolerance. Use natural logarithms. Distinguish κ from the iteration count K.

The paper states K ≥ (κ/2) ln(2/ε), and combines it with the iteration count as

\[
f_{D1}(N,\kappa,s,\epsilon)=\frac{\kappa}{2}\ln\frac2\epsilon\,(4Ns+14N).
\]

This is the exact transcription of the **paper expression**. For whole iterations use

\[
K_{\rm model}=\left\lceil\frac{\kappa}{2}\ln\frac2\epsilon\right\rceil,
\qquad n_{\rm FLOPs}=K_{\rm model}(4Ns+14N).
\]

The executable exports both. Their difference is less than one modeled iteration. The closed-form scaling is O(Nsκ ln(1/ε)). The notebook `tools/heatmap.ipynb` uses the same unrounded D1 expression. Appendix F, p. 28, Eq. (F1), already uses work/rate × power; this revision replaces CPU frequency with HPCG FLOP/s.

### Meaning of “exact instruction count”

D1 is a floating-point **arithmetic model**, not an exact executed instruction counter. It substitutes Ns for actual nnz, groups coefficient work into 8N, and omits startup, input construction, output/certification and integer/address instructions. The iteration expression is an analytical claim, not a measured iteration count or a verified FP64 guarantee. An FMA is two FLOPs but may be one instruction; complex arithmetic and precision-specific costs are not specified by D1. We assume real FP64 to align the rate proxy with HPCG. This task preserves the formula requested by the user without making its evidentiary status stronger than the source supports.

### CG naming and reviewer C1-3

The paper calls Figure 13 “CGNE”; its z=Aᵀr, p=z+βp, x-update recurrence is CGLS/CGNR, namely implicit CG on AᵀAx=Aᵀb. Two operator actions and linear original-κ dependence are consistent with normal-equation conditioning. Ordinary SPD CG has one matvec per iteration and a different condition-number dependence. Therefore this report calls the retained method **paper CG-family baseline (D1)** and explicitly records the variant. We do not silently relabel D1 as an exact count for ordinary SPD CG. No alternative solver is introduced into the active numerical model. [Netlib Templates](https://www.netlib.org/templates/templates.pdf) supports the algorithm distinction; the manuscript itself supplies D1. The prior statement of Theorem 4 is inherited, not re-proved or certified here.

## 2. HPCG-based runtime and energy

Let R_HPCG be the published whole-system HPCG score in PFLOP/s and P_kW the selected system power in kW. The requested baseline is

\[
t_{\rm core}[s]=\frac{n_{\rm FLOPs}}{10^{15}R_{\rm HPCG}},\quad
E_{\rm core}[J]=10^3P_{\rm kW}\,t_{\rm core},\quad
E_{\rm core}[kWh]=E_{\rm core}[J]/(3.6\times10^6).
\]

Do not multiply the HPCG score by core count, by the displayed fraction of peak, or by an additional generic parallel-efficiency factor. It is already an aggregate benchmark result. Do not substitute the neighboring HPL Rmax column. The baseline sets all transfer multipliers to one.

For sensitivity only, use R_effective=η R_HPCG and P_effective=ρ P, so time scales as 1/η and energy as ρ/η. η is an application-to-HPCG rate assumption, not a second measurement of benchmark parallel efficiency. It may exceed one if the application is faster than HPCG. The supplied grid uses η={.25,.5,1,2} and ρ={.7,1,1.3}: 48 rows over four systems, with no probability interpretation.

## 3. Frozen hardware inputs

Edition: **November 2025**, retrieved 20 September 2026. This is a pinned source edition, not a claim that it is the newest possible list. Rates use the official HPCG page; powers use the same-edition TOP500 page. Matching names/core counts do not prove matching measurement runs or scopes.

| System | HPCG PFLOP/s | Power kW | Core count shown in both listings |
|---|---:|---:|---:|
| El Capitan | 17.41 | 29,685 | 11,340,000 |
| Fugaku | 16.00 | 29,899 | 7,630,848 |
| Frontier | 14.05 | 24,607 | 9,066,176 |
| Aurora | 5.613 | 38,698 | 9,264,128 |

Sources: [HPCG SC25 results](https://www.hpcg-benchmark.org/custom/sc25.html), [TOP500 November 2025](https://www.top500.org/lists/top500/2025/11/). Source snapshots and SHA-256 hashes are retained. These values replace the 1 GHz/50 W desktop assumption. Rates are published benchmark results; powers are published system-power **proxies for this calculation**, not measured HPCG job power. Consequently P/R is a hybrid projection coefficient, not a measured HPCG energy efficiency.

The default energy boundary is the reported system-power proxy over the modeled core interval. The available table does not settle facility/cooling inclusion, gross versus incremental allocation, or host/network metering scope. No PUE or cooling multiplier is added. Task 07 must establish a common energy boundary before a quantum/classical energy ratio is published. Unknown scope is not silently called facility energy.

## 4. Transfer assumptions and scope

HPCG exercises sparse matvecs, vector updates, reductions and smoothing through multigrid-preconditioned CG. Its algorithm and problem are different from the paper's normal-equation CG count. Using the HPCG score as R_effective is the requested **proxy assumption**, not a claim to have run that recurrence at the reported rate. The score already reflects benchmark memory and synchronization effects; application-specific differences remain unresolved. [HPCG overview](https://www.hpcg-benchmark.org/) and [FAQ](https://www.hpcg-benchmark.org/faq/index.html).

The FAQ specifies FP64 computations and large official benchmark runs, normally at least 1800 seconds, with substantial main-memory use. A tiny problem cannot be assumed to sustain a whole-supercomputer score. Formal fractions-of-a-second results remain algebraic core projections, not observed latency. Startup, input generation, data transfers and final scalar/residual checks are outside D1. Optional memory limits reject cases that cannot hold even one FP64 vector, 8N bytes; passing this test does not establish total memory feasibility. The script never marks a projection as eligible for an advantage claim and leaves complete-workload time/energy null.

This deliberately narrow revision does not build a second memory-bandwidth/communication performance model or add a new preconditioner cost. Such additions would change the user's requested pipeline. An end-to-end estimate would require separately owned and costed missing phases, not silently treat them as zero.

## 5. Task-02 compatibility

Task 02 now defines `02-smooth-diffusion-v1`: m=127, N=16,129, β=9, s=5 by default, continuum output J=5/144, c=h²1 and ε_out=10⁻⁴. It is a known-answer manufactured verification problem, so direct evaluation of 5/144 defeats any unrestricted application-advantage claim. The compact analytic input is shared between branches and generation is not free.

D1's ε is relative solution error, not ε_out. If the paper's solution-error claim holds and λ_min(A)≥λ₀, a sufficient scalar conversion is

\[
|c^T(\hat x-x)|\le\|c\|_2\epsilon\|x\|_2
\le\frac{\|c\|_2\|b\|_2}{\lambda_0}\epsilon.
\]

For task 02, ||c||=h²√N and ||b||≤√N F, where F=3(1+β)+9β/16. With its algebraic allowance ε_alg=ε_out/4, choose

\[
\epsilon_{D1}=\epsilon_{alg}\lambda_0/(h^2NF),\quad
\lambda_0=8h^{-2}\sin^2(\pi h/2),\quad
\kappa_{scenario}=(1+\beta)\cot^2(\pi h/2).
\]

`task02-adapter.json` evaluates this conditional conversion, preserves original κ as an upper-bound scenario, checks the mesh budget, and records that no solve/accuracy certification was run. Representation, arithmetic and failure budgets remain separate. Generation and scalar recovery are not included in the D1 core model, so this is not a finalized task-01 end-to-end record.

## 6. Replacement claims and handoff

C1-3: accurately identify the paper's retained CG variant; the requested reuse of D1 does not resolve the reviewer's demand for an ordinary-SPD/competitive-preconditioned comparison. C1-4: replace CPU-frequency arithmetic with published HPCG-rate scenarios, retaining clear power and transfer assumptions. C2-3: use a scientific-computing rate proxy and the available application error conversion; no new production benchmark evidence is claimed. Minor C1-1/4: separate κ, iteration count, time and power, and restate scope limits.

The earlier Cholesky comparison is outside the revised active scope, so its 2¹⁰⁰/200-hour crossover is not carried forward. Merely replacing the rate cannot validate any crossing; one vector at N=2¹⁰⁰ needs about 1.014×10³¹ bytes. The superseded report has been removed.

Deliverables are the executable D1/HPCG model, pinned parameters/source snapshots, unit checks, scaling/sensitivity outputs, task-02 conditional adapter, PDF, and replacement passages. Task 05 must complete matched input/output and reliability accounting; task 07 must resolve energy scope and power evidence; task 09 must validate application-rate transfer, capacity, complete costs and both accuracy guarantees before publishing ratios. Shared notebooks, task-02 files and manuscript PDF were not changed. The September 20 scope supersedes the earlier task's requirement to retain direct methods and a multigrid solver model.
