# Application benchmark 02-smooth-diffusion-v1

This specification instantiates task 01 contract **1.0.0**, addressing C1-6 (review 1 p. 2) and C2-3 (review 2 pp. 3–4). Quantities below are dimensionless after fixing domain length, conductivity and temperature reference scales to one. Status labels distinguish mathematical derivations from modeling choices. `benchmark-pp.json` is a schema-compatible `pp` fragment, not a complete resource evaluation.

## Scientific problem and scope

**Chosen model:** steady heat conduction in a square plate, with spatially varying isotropic conductivity and prescribed volumetric source. On Ω=(0,1)² solve

    −∇·(a∇u)=f,    u|∂Ω=0,    a(X,Y)=1+βX,    β≥0.

Primary parameter β=9 gives conductivity contrast C=10. β=0 is the Poisson control. Define q(t)=t(1−t), and choose the manufactured temperature

    U(X,Y)=q(X)q(Y)(1+XY),
    f=−(1+βX)(U_XX+U_YY)−βU_X,
    U_X=q(Y)[(1−2X)(1+XY)+q(X)Y],
    U_XX=q(Y)[−2(1+XY)+2(1−2X)Y],
    U_YY=q(X)[−2(1+XY)+2(1−2Y)X].

The source is an explicit smooth polynomial, independent of mesh size; it may include heating and cooling. This is a canonical diffusion **verification workload**, not measured material data or a production simulation. It avoids discontinuous-source regularity assumptions and single-eigenvector RHS tests. The scalar is the mean nondimensional temperature (the area is one):

    J=∫Ωu dX dY=5/144.

**Known-answer limitation:** an unrestricted algorithm can return 5/144 directly. Consequently this workload can compare the costs and correctness of specified discretize-and-solve pipelines, but cannot establish application-level quantum advantage. The analytic answer must be available to both branches; hiding it from the classical baseline would be unfair. Even within solver comparisons, low-rank/separable structure should be exploited classically. A production crossover requires a separately versioned, nonmanufactured source/coefficient family, its own continuum certificate and renewed access analysis. The present task does not claim that such a family is supplied. A manufactured problem is chosen deliberately to deliver a fully checkable common contract now, rather than an unsupported continuum accuracy claim.

The relationship between a linear functional of a PDE solution and end-to-end precision is also the focus of [Montanaro and Pallister, PRA 93, 032324 (2016)](https://arxiv.org/abs/1512.05903v2). Their finite-element results motivate this accounting; they are not a theorem for the finite-difference circuit proposed here.

## Discrete operator, dimensions and spectrum (derived)

Use m≥3 interior nodes in each coordinate, h=1/(m+1), N=m². Node (i,j), 1≤i,j≤m, has flattened index (i−1)m+(j−1), with Y varying fastest. Store the **unscaled** system Ax=b, with b_ij=f(ih,jh). On each incident edge use its midpoint conductivity w_e=a_e/h², including edges ending on the zero boundary. Set A_ii=Σ_e w_e and A_ij=−w_e for interior neighbors. Thus the operator is a symmetric conservative five-point stencil. The four-neighbor terms plus diagonal give s_row=s_col=5, nnz=5m²−4m. Corners/edges have fewer entries. Zero boundary values do not alter b.

For the unit-conductivity matrix P, the discrete sine basis gives

    λ_pq(P)=4h⁻²[sin²(pπh/2)+sin²(qπh/2)], 1≤p,q≤m,
    λ₀=λ_min(P)=8h⁻² sin²(πh/2),
    λ₁=λ_max(P)=8h⁻² cos²(πh/2), κ₀=cot²(πh/2).

The edge energy vᵀAv=Σ_edges a_e(v_i−v_j)²/h², with boundary values zero, establishes P≼A≼CP. Hence A is real SPD, λ_min(A)≥λ₀, λ_max(A)≤Cλ₁ and

    max(1,κ₀/C) ≤ κ₂(A) ≤ Cκ₀.

The lower bound follows from λ_max(A)≥λ₁ and λ_min(A)≤Cλ₀. At fixed finite C, κ₂(A)=Θ(m²)=Θ(N), while s=5. The bounds are not numerical equality when β>0. Original κ remains unknown within this interval until evaluated; resource scenarios may use the upper bound, clearly labeled. Neither κ nor s equals log N. Analogous constant-coefficient d-dimensional grids have N=m^d, s=2d+1 and κ=Θ(N^(2/d)); this is context only, not an authorized switch to a 3D instance.

For normalized algorithms use B=h²A and d=h²b; x is unchanged and κ(B)=κ(A). B has entries bounded by 4C and norm ≤8C. A generic sparse block encoding may use **α_B=5(4C)=20C**, subject to actual circuit construction; its normalized inverse gap can be bounded by α_B/(h²λ₀). This is not κ₂(A), nor a gate count. A tighter encoding requires its own proof. To run on n=ceil(log₂N) index qubits, pad B to D=2^n as B⊕4C I_(D−N), and pad d,c with zeros. The padded spectrum lies within [h²λ₀,8C], giving the safe effective condition upper bound 8C/(h²λ₀). Record D and this effective bound separately from original N,κ. The output is unchanged. Never pad with a singular zero block.

## Continuum error and common delivery contract (derived + chosen budget)

The required output is **one real number** Ĵ in host memory satisfying

    Pr(|Ĵ−J|≤ε_out) ≥ 1−δ_total,
    ε_out=10⁻⁴, δ_total=0.01, reference scale=1, B_outputs=1.

Both quantum and classical solvers target exactly this scalar and continuum tolerance. Intermediate discrete scalar J_h=cᵀx uses **c=h²1**, not 1/N and not a normalized state observable. No relative error and no full-vector delivery is requested.

The midpoint flux truncation error is an exact polynomial identity:

    (A U_grid−b)_ij = β h² Y_j²(1−Y_j) = τ_ij,
    ||τ||₂ ≤ √N β h²(4/27).

To derive it, midpoint differencing of a linear a times the gradient of a cubic U differs from (a U_X)_X by h² a_X U_XXX/6; U_XXX=−6Y²(1−Y). The Y difference is exact. Therefore

    |cᵀ(x−U_grid)| ≤ ||c||₂ ||τ||₂/λ₀ ≤ β h⁴ N(4/27)/λ₀.

The quadrature identity is h²ΣU_grid=5(1−h²)²/144, since hΣq(ih)=(1−h²)/6 and hΣih q(ih)=(1−h²)/12. Thus the complete deterministic mesh allowance is

    D_h = 5(2h²−h⁴)/144 + β h⁴ N(4/27)/λ₀,
    |J−J_h| ≤ D_h.

Require D_h≤ε_out/4. An inadmissible mesh is rejected, not rescued by tightening QLSA state accuracy. At fixed β, sufficient m=O(ε_out^−1/2), N=O(ε_out^−1) and κ upper=O(C ε_out^−1). These are sufficient resolution scalings for this second-order certificate, not lower bounds on every method; higher order schemes and analytic shortcuts are available. The CSV marks admissibility for every row.

| Error source | Maximum contribution to absolute scalar error | Owner |
|---|---:|---|
| Discretization plus quadrature | ε_out/4 | 02, mesh check |
| Algebraic solve / normalized-state bias converted to J_h | ε_out/4 | 03/04/05 or 08 |
| Matrix and RHS representation | ε_out/8 | 05/08 |
| Output estimation, including norm and signed overlap estimates | ε_out/4 | 05/08 |
| Remaining arithmetic, coefficient evaluation, synthesis and scalar reduction | ε_out/8 | 03–05/08, assigned once |

This is a sufficient fixed allocation, not an assertion of achieved precision. Classical deterministic readout may leave its allowance unused. Reallocation requires a recorded certificate with the same ε_out and must not double-count algorithm or representation error. The inverse perturbation bound below already accounts for representation effects; it is not added again as a state bias.

For a classical candidate x̂, recompute the **original** residual r=b−Ax̂. Then |cᵀx̂−J_h|≤||c||₂||r||₂/λ₀, so relative residual tolerance ε_out λ₀/(4||c||₂||b||₂) is sufficient in exact arithmetic. A recursive CG residual alone is not a certificate. Rounding in the recomputation, dot product and inputs needs bounded arithmetic or a separately justified precision check. Reference solves must carry their own residual bound. The exact continuum value checks the entire pipeline but is not the exact discrete reference.

For quantum normalized solution |x⟩=x/||x||₂ and |c⟩=1/√N Σ|i⟩, recover

    J_h=||c||₂ ||x||₂ Re⟨c|x⟩,  ||c||₂=h²√N.

The relative phase must be fixed by a coherent implementation tied to b (not an independently phased state). State preparation alone does not deliver J_h. Writing Z=||x||₂, R=Re⟨c|x⟩, estimates obey

    |ẐR̂−ZR| ≤ |Ẑ−Z| + (Z+|Ẑ−Z|)|R̂−R|.

Multiply by ||c||₂ to allocate scalar readout error. If a phase-aligned state has Euclidean error η_x and Z≤X_max=||b||₂/λ₀, its scalar bias is at most ||c||₂ X_max η_x. A sufficient state allowance is η_x≤ε_out/(4||c||₂ X_max); this is not the QLSA internal ε without the adapter. Trace distance of a freely phased state alone does not certify a signed linear overlap. Norm recovery, coherent reference control, preparations/unpreparations, repetitions and failures all belong to task 05. No implemented efficient output circuit or complete query/gate count is asserted.

Failure-budget starting allocation on the quantum branch is δ_statistics=.004, δ_retry_or_abort=.002, δ_QEC=.003, δ_other=.001, summing to .01 per output. These are requests, not achieved bounds. Classical numerical work may be deterministic; its arithmetic guarantee and a justified hardware/delivery-failure bound ≤.01 still need task 08 evidence. Do not charge quantum δ components to the classical branch or sum failures across alternative machines. Batch extension uses δ per output ≤.01/B for a whole-batch target, unless a tighter joint bound is supplied.

## Representation precision (derived sufficient bound)

Round every nonzero of B and every entry of d with absolute error at most η=2^−p, preserving symmetry and the sparsity pattern. Then ||ΔB||₂≤5η and ||Δd||₂≤√Nη. For 5η<h²λ₀, inverse perturbation gives

    |cᵀ[(B+ΔB)⁻¹(d+Δd)−x]|
      ≤ ||c||₂(√N+5X_max)η/(h²λ₀−5η).

Use |f|≤F=3C+9β/16, so X_max≤√N F/λ₀, to choose p without a solve. The generator finds the smallest positive p satisfying this bound ≤ε_out/8. This conservative common absolute fixed-point representation has p=O(log N+log(1/ε_out)+log C) at fixed shape, and needs sign and enough integer bits for B and d in addition. Its `fixed_fraction_bits_sufficient` is **not** total qubits, IEEE mantissa width or a full FP64 stability proof. Intermediate arithmetic guard bits, norm computation, reciprocal approximation and rotation synthesis have additional costs. A rounded-zero small entry does not change the declared maximum sparsity bound. If symmetry is lost, the SPD analysis is no longer applicable.

## Access model and preconditioning contract

Both branches start with the same compact analytic description (m, β, ε, boundary rule, polynomial f and c) in host memory. No CSR, RHS amplitudes, state-preparation tree, QRAM or preconditioner is already built. Classical generation/materialization and quantum reversible compilation/preparation are charged. Both branches may exploit the formulas and structure. Dense host arrays produced by the diagnostic generator are not evidence that a quantum oracle already exists.

| Capability | Evidence/status | Required cost treatment |
|---|---|---|
| Neighbor/index oracle | Constructive arithmetic description: decode (i,j), test boundary, enumerate center and up to four valid neighbors in fixed order; pad unused slots with zero-value flag and valid index | Reversible arithmetic in O(poly(log N)) at fixed value precision is available in principle; circuit/gate constants **unimplemented**. Enumeration costs are not zero |
| Entry oracle | Evaluate rational midpoint a and h²A entries; diagonal includes boundary edges | Include p-bit arithmetic, uncomputation, comparison and padding. No fixed arbitrary sparsity-pattern lookup assumption |
| RHS state | Evaluate polynomial f coherently on a uniform valid-index superposition, rotate an ancilla with signed amplitude f/F, herald/uncompute | Success p_b=||b||₂²/(NF²). Include this factor or coherent amplification exactly once, rotation precision and normalization; no prebuilt QRAM assumed |
| Uniform c state | Prepare uniform over N valid indices using n-qubit uniform state plus rejection (N/2^n>1/2) or exact preparation | Charge preparation/unpreparation; c's classical norm is h²√N |
| Efficient quantum input overall | Polynomial evaluation and finite-grid uniform preparation give a constructive route. For fixed β in the bounded sweep, p_b approaches a positive integral/F²; hence no asymptotic N-dependent vanishing success | Asymptotic route established by this argument; executable reversible circuit, finite-size success bound and gate resource model **unresolved** with task 05 |
| Unnormalized scalar output | Norm plus coherent signed overlap formula above | Efficient implementation and complete costs **unavailable in supplied code**; not a free O(1) measurement |

The polynomial f is nonzero for every β≥0 because its zero-Dirichlet solution U is nonzero and A_continuum is coercive. Its square has positive integral. Continuity over a compact β range supplies a positive asymptotic lower bound on p_b; finite-grid values can be evaluated by sums of powers or charged explicit generation. A small measured p_b is not a circuit-cost proof. Generic tabulated/noisy coefficients or RHS invalidate this access scenario and require an explicit new input contract; never retain the analytic oracle while swapping in task 08's random RHS.

Default quantum comparator is unpreconditioned. Classical candidates include CG, Jacobi as a control, and **Poisson-preconditioned CG**, applying P⁻¹ by separable type-I sine transforms and diagonal division. From P≼A≼CP, κ₂(P^−1/2 A P^−1/2)≤C, independent of N. The inverse application takes O(N log m) arithmetic and O(N) storage; setup includes sine-eigenvalue tables/denominator generation, workspace and transform planning. β=0 permits a direct DST solve. This uses the eigenbasis derived above; the implementation convention is documented by [SciPy's DST reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.dst.html). PCG eligibility and its symmetric transformation are described in the [PETSc KSPCG documentation](https://petsc.org/release/manualpages/KSP/KSPCG/).

Because a depends only on X, a Y sine transform also reduces A to m independent tridiagonal X systems. Include this O(N log m) direct classical competitor at β>0, with O(N) storage, tridiagonal factor setup and possible factor reuse. Generic multigrid/AMG and sparse Cholesky are further candidates, but require measured setup, solve, memory and parallel schedules. No universal O(1) iteration count is credited. For repeated changed RHS with fixed A, transform/tridiagonal factors can be reused; new RHS must be separately specified and prepared. Repeating the identical deterministic scalar can use a cached result on both branches, not B artificial solves.

A quantum Poisson-preconditioned variant must encode K=P^−1/2 A P^−1/2, prepare P^−1/2 b, and recover cᵀP^−1/2 y. K is generally dense even though A is sparse. κ(K)≤C does not establish sparse access, favorable block normalization, inexpensive inverse square roots, success probability or cheap recovery. All those costs are unresolved; it is forbidden to replace κ by C while retaining s=5 and the original input/output circuits. Record preconditioned effective quantities in `cq/cc`, preserving `pp`.

## Sensitivity ranges and limits

`parameters.csv` contains 108 formula-generated rows: m=15,31,63,127,255,511,1023,4095,16383; β=0,1,9,99 (C=1,2,10,100); ε_out=10⁻²,10⁻⁴,10⁻⁶. Default is m=127, β=9, ε=10⁻⁴. Small grids validate formulas; m up to 1023 exercises workstation-scale storage, and the two largest sizes are capacity/projection scenarios requiring allocated HPC resources. These ranges are engineering sweeps for a smooth diffusion model, **not a survey of production workloads**. β=99 tests strong contrast and can be overconservative under the global bounds. N and ε are coupled by mesh admissibility, and κ bounds depend jointly on N,C. Do not independently sweep arbitrary κ at fixed (m,β) as though it describes this same instance.

Only small correctness runs were performed, m≤127. No time, power, GPU, multi-node or quantum hardware measurement is reported. Downstream hardware models must enforce memory capacity and distinguish original N from padded D. One FP64 vector uses 8N bytes, and CSR with 64-bit indices uses 16 nnz+8(N+1) bytes; matrix-free access avoids CSR but not classical solver vectors. Tiny NumPy runs are not a production solver baseline.
