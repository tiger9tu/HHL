# Quantum logical resource model

This component implements the logical layer described in [the paper framework](../../frame.md). It maps problem parameters to **logical T-gate count and peak logical circuit-qubit count**. Runtime, physical qubits, power, energy, and error-correction scheduling belong to the QEC and hardware layers.

The implemented algorithm is the **discrete-adiabatic modern QLSA with eigenstate filtering**, using the finite resource model in Dalzell et al., *End-to-end resource analysis for quantum interior point methods and portfolio optimization*, [arXiv:2211.12489v1](https://arxiv.org/pdf/2211.12489v1). It is the QLSA subroutine, without portfolio-optimization iterations. The formulas are Tables III–V (PDF pages 14 and 22), Eqs. (64)–(67) (page 26), and Proposition 4 for optional readout.

This folder is self-contained. `modern_qlsa.py` incorporates the previously developed task-04 Table V estimator and adds logical width. It imports nothing from `paper-revise/results`. The old-HHL logical model mentioned in the framework is a separate, not-yet-integrated component; these costs must not be labeled as HHL. The framework's older `q-resource/logical` path corresponds to the user-selected `quantum/logical` directory used here.

## Interface and units

```python
from modern_qlsa import estimate, f
p = {"N": 1024, "kappa": 100,
     "epsilon_state": "0.01", "delta": "0.01"}
result = estimate(p)
T = result["T_total"]                 # integer modeled logical T count
qubits = result["logical_qubits_peak"] # peak simultaneous logical circuit qubits
assert f(p) == T
with_readout = estimate(dict(p, include_readout=True))
```

Python 3.11+ is required; only the standard library is used. T and T-dagger gates count equally. Counts are calculated with 80-digit decimal arithmetic and rounded as described below. The returned integer is a rounded **paper-model estimate, not a certified sufficient circuit upper bound**.

| Parameter | Meaning/default |
|---|---|
| `N` | Original matrix dimension, integer at least 2. |
| `kappa` | Ordinary spectral condition upper bound, at least 1. |
| `epsilon_state` | Normalized solution-state vector-error target; default .01, allowed `(0,.1]`. |
| `delta` | State-only abort allowance under the ideal success model; default .01. |
| `frobenius_over_spectral` | Optional certified normalization-ratio bound; default sqrt(padded dimension). |
| `effective_inverse_gap` | Optional direct normalized inverse-gap bound; mutually exclusive with the ratio. |
| `adiabatic_constant` | Numerical schedule constant C, default 2000. |
| `include_readout` | Boolean; default false. True enables full real-vector tomography. |
| `epsilon_readout` | Total normalized classical-vector error target; defaults to `epsilon_state`. |
| `delta_readout` | Tomography failure allowance; defaults to `delta`. |

Sparsity is not an input to this particular adapter: its access circuit handles general dense classical data and gives no discount for a sparse matrix. A sparsity-aware model requires replacing the circuit and its normalization together. Unknown keys are rejected, so unsupported sparsity or hardware parameters cannot silently affect the result. Matrices are real and nonsingular; any padding must preserve nonsingularity and the condition bound. The program does not verify externally supplied spectral certificates.

## 1. Normalization and solver schedule

Let

$$
\ell=\lceil\log_2N\rceil,\quad L=2^\ell,
\qquad K\ge\|A\|_F/\sigma_{\min}(A).
$$

The matrix block encoding contains $A/\|A\|_F$. Thus $K$ differs from the ordinary condition number. Without more matrix information, use $K=\kappa\sqrt L$, since $\|A\|_F/\|A\|_2\le\sqrt L$. Nonsingular padding can use a positive scalar within the original singular-value range.

Using the source's numerical schedule approximation and our even-degree rounding,

$$
Q=\lceil2CK\rceil,\qquad
 d=2\left\lceil K\ln(2/\epsilon_{\rm qsp})\right\rceil.
$$

Here $Q$ describes the adiabatic evolution and $d$ the QSVT filtering polynomial. One solver execution uses $2(Q+d)$ controlled matrix-block calls and $4(Q+d)$ RHS preparation/unpreparation calls. Forward and inverse calls are both included.

For a state-only target $\epsilon$, let $s=\epsilon/5$ and choose

$$
\epsilon_{\rm qsp}=s,\quad
\epsilon_G=\frac{s}{2(Q+d)},\quad
\epsilon_h=\frac{s}{4(Q+d)},\quad
\epsilon_{\rm ar}=\frac{s}{4Q},\quad
\epsilon_z=\frac{s}{2d}.
$$

These choices assign equal contributions to the five terms of the paper's Eq. (64). The split is our adapter choice. We use the larger $2d\epsilon_z$ coefficient of Eq. (64), rather than the $d\epsilon_z$ displayed in Eq. (65).

## 2. Price each primitive and compose Table V

The paper chooses a **minimum-depth dense-data block encoding**, trading a large workspace for depth. Tables III and IV give

$$
T_{\rm BE}=[12\log_2(1/\epsilon_G)+56]L^2
 -24L-12\log_2(1/\epsilon_G)-32\ell-32,
$$
$$
T_{\rm cBE}=T_{\rm BE}+16(L-1),
$$
$$
T_{\rm SP}=[12\log_2(1/\epsilon_h)+40]L
 -12\log_2(1/\epsilon_h)-16\ell-40.
$$

These costs include coherent quantum data access and its uncomputation. Classical construction of the data structure is excluded. Table V combines the primitives as

$$
\begin{aligned}
T_U={}&2(Q+d)T_{\rm cBE}+4(Q+d)T_{\rm SP}\\
 &+12Q\log_2(1/\epsilon_{\rm ar})+Q(24\ell+31)\\
 &+3d\log_2(1/\epsilon_z)+d(32\ell-2).
\end{aligned}
$$

The six terms account for matrix access, RHS access, adiabatic rotations, remaining adiabatic gates, filter rotations, and remaining filter gates. Do not add another BE charge after using this expanded total.

For state-only delivery, the ideal per-attempt success probability is at least one half. With independent attempts, use

$$
r=\lceil\log_2(1/\delta)\rceil,\qquad T_{\rm state}=r\lceil T_U\rceil.
$$

This is a modeled retry budget, not an expected count; execution can stop earlier. It inherits the source's ideal-success assumption, which has not been recertified for the approximate synthesized circuit.

## 3. Optional readout

`include_readout=True` selects the source's **full real normalized-vector tomography**, including sign recovery. It is not a scalar-observable readout or recovery of the physical solution norm.

For total classical-vector error target $\xi$, our 90/5/5 allocation is

$$
\epsilon_{\rm tomo}=0.9\xi,\quad
\epsilon_{\rm core}=\min(\epsilon_{\rm state},0.05\xi/1.58),\quad
\epsilon_{\rm tsp}=\frac{0.05\xi}{1.58\sqrt L}.
$$

The core solver is repriced at $\epsilon_{\rm core}$. Proposition 4's modeled output error is at most $\epsilon_{\rm tomo}+1.58\sqrt L\epsilon_{\rm tsp}+1.58\epsilon_{\rm core}\le\xi$. The program checks its applicability condition too.

The repetitions **per circuit family** are

$$
k_{\rm tomo}=\left\lceil
\frac{57.5L\ln(6L/\delta_{\rm ro})}
{\epsilon_{\rm tomo}^2(1-\epsilon_{\rm tomo}^2/4)}
\right\rceil.
$$

The controlled sign-recovery circuit is the other Table V column:

$$
T_V=T_U+20Q+3d\log_2(1/\epsilon_z)
 +12(L-1)\log_2(1/\epsilon_{\rm tsp})+16(L-\ell-1).
$$

The complete readout workload costs

$$
T_{\rm readout}=k_{\rm tomo}(\lceil T_U\rceil+\lceil T_V\rceil).
$$

**No extra retry or success-probability multiplier is applied:** the sampling formula already accounts for unsuccessful solver flags. Do not add the standalone state-only budget to this total. The requested output has changed, and solver precision is retuned for it.

## 4. Peak logical-qubit count

Tables III and V give the following circuit allocations:

$$
n_{\rm BE}=4L^2-3L+2\ell-1,\quad
n_{\rm cBE}=n_{\rm BE}+L,
$$
$$
n_U=n_{\rm cBE}+5=4L^2-2L+2\ell+4,
\qquad n_V=n_U+1.
$$

State-only peak width is $n_U$; tomography peak width is $n_V$. The model executes attempts and samples **serially, reusing registers**. Thus repetition counts multiply T gates, not peak qubits. QEC redundancy, physical layout/routing allocation, and magic-state factories are not included. This is the paper's chosen circuit allocation, not a minimum-qubit lower bound.

## 5. Reproduce data

From the repository root:

```sh
python3.11 paper-revise-clean/quantum/logical/validate.py
python3.11 paper-revise-clean/quantum/logical/generate_data.py
```

The generator writes `data/inputs.json`, `data/resources.json`, `data/resources.csv`, and `data/manifest.json`. JSON retains integer T/qubit counts and high-precision decimal strings; the CSV contains the actual selected workload's schedule and component costs. Avoid converting large integers to binary64 when importing them into plotting or spreadsheet software.

For other parameters, pass a JSON object or list through `--input my_cases.json`. Use `--sweep --output-dir sweep-data` for a 36-case dimension/condition/accuracy sweep in both readout modes. The default output directory is anchored to this script, not the working directory. The manifest records Python/model versions, source-code hashes, input/output hashes, and generation time.

For $(N,\kappa,\epsilon,\delta)=(1024,100,.01,.01)$, with readout target .01 when enabled:

| Output mode | T count | Peak logical qubits |
|---|---:|---:|
| State only, seven-attempt budget | 86,705,344,699,164,751 | 4,192,280 |
| Full-vector tomography | 271,767,176,507,565,562,710,978,575 | 4,192,281 |

The first mode has $K=3200$, $Q=12{,}800{,}000$, $d=44{,}210$. The second retunes $d$ and primitive precision and uses 9,688,792,223 executions of each circuit family. These are different output tasks, not interchangeable accuracy guarantees for a single scientific observable.

## 6. Handoff to QEC and limits

`estimate(p)['qec_input']` contains `T_count`, `logical_qubits`, the count statistic, and the model status. Depth/Clifford/measurement scheduling fields are explicitly `null` rather than inferred from T count. QEC should use the selected total (`T_total`), not the retained state-only `T_retry_budget` diagnostic when readout is enabled. Top-level Q/d/precision likewise describe the state-only baseline; actual readout values are nested under `readout`. The generated CSV selects those nested values automatically.

The QEC/hardware layers may use these count/width inputs for a declared count-based scheduling model, but must specify their assumptions about dependency, factory throughput, layout, and measurement timing. The logical layer does not itself predict physical runtime or energy.

The source uses C=2000 as a numerical assumption, drops the O(sqrt(K)) schedule term, suppresses some subleading terms in the BE/state-preparation formulas, and uses the synthesis model $3\log_2(1/\epsilon)$ without compiled gate certificates. These limitations are retained explicitly as `certified_upper_bound=False`. Switching C to a larger analytic constant alone does not certify the other approximations.

For the framework's later old-HHL comparison, use the same problem and output contract, but price HHL's Hamiltonian simulation separately. Future structured BE and scalar-readout adapters must identify their normalization, circuit costs, and error budget rather than reusing the dense/tomographic formulas without adjustment.

## References and provenance

- Dalzell et al., [arXiv:2211.12489v1](https://arxiv.org/pdf/2211.12489v1): solver accounting, Tables III–V, and full-vector tomography.
- Costa et al., [PRX Quantum 3, 040303 (2022)](https://doi.org/10.1103/PRXQuantum.3.040303): discrete-adiabatic QLSA with filtering.
- Clader et al., [IEEE TQE 3, 3103323 (2022)](https://doi.org/10.1109/TQE.2022.3231194): dense-data block-encoding circuit resources.
- Code provenance: self-contained snapshot of `paper-revise/results/04-modern-qlsa/table-v/paper_table_v.py`, version 04-table-v-1.1.0; T-count behavior preserved, with Tables III/V qubit formulas and QEC handoff fields added. The older task artifacts are retained unchanged.
